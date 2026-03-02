from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.config import settings
from app.core.i18n import locale_from_request, tr as i18n_tr
from app.core.storage import S3NotConfiguredError, generate_presigned_get_url
from app.db.database import get_db
from app.db.models.media import Media
from app.db.models.private_personal_wish import PrivatePersonalWish, PrivatePersonalWishStatus
from app.db.models.user import User
from app.private_wishes.schemas import (
    PrivatePersonalWishDeleteResponse,
    PrivatePersonalWishFulfilledListOut,
    PrivatePersonalWishFulfillRequest,
    PrivatePersonalWishListOut,
    PrivatePersonalWishOut,
    PrivatePersonalWishUpsertRequest,
)

router = APIRouter(prefix="/private-wishes", tags=["private-wishes"])

PERSONAL_ACTIVE_LIMIT = 50


def _locale(request: Request | None) -> str:
    return locale_from_request(request, default="en")


def _td(locale: str, en: str, **fmt: object) -> str:
    translations: dict[str, tuple[str, str]] = {
        "Media not found.": ("Medio no encontrado.", "Média introuvable."),
        "Not authorized to use this media.": ("No autorizado para usar este medio.", "Non autorisé à utiliser ce média."),
        "Media not available yet.": ("El medio aún no está disponible.", "Le média n'est pas encore disponible."),
        "Required field: {field}.": ("Campo requerido: {field}.", "Champ requis : {field}."),
        "Invalid {field} (hex).": ("{field} inválido (hex).", "{field} invalide (hex)."),
        "User not found.": ("Usuario no encontrado.", "Utilisateur introuvable."),
        "You already reached the maximum of {limit} active private wishes.": (
            "Ya alcanzaste el máximo de {limit} deseos privados activos.",
            "Vous avez déjà atteint le maximum de {limit} souhaits privés actifs.",
        ),
        "Invalid nonce_hex (expected 12 bytes).": (
            "nonce_hex inválido (se esperaban 12 bytes).",
            "nonce_hex invalide (12 octets attendus).",
        ),
        "Private wish not found.": ("Deseo privado no encontrado.", "Souhait privé introuvable."),
    }
    english = en.format(**fmt) if fmt else en
    pair = translations.get(en)
    if not pair:
        return english
    es, fr = pair
    return i18n_tr(
        locale,
        es=(es.format(**fmt) if fmt else es),
        en=english,
        fr=(fr.format(**fmt) if fmt else fr),
    )


def _build_media_url(media: Media | None) -> str | None:
    if not media or media.status != "ready":
        return None
    try:
        return generate_presigned_get_url(
            key=media.object_key,
            expires_in=settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600,
        )
    except S3NotConfiguredError:
        return None
    except Exception:
        return None


def _wish_out(*, wish: PrivatePersonalWish, media_map: dict[int, Media]) -> PrivatePersonalWishOut:
    media = media_map.get(wish.media_id) if wish.media_id else None
    evidence_media = media_map.get(wish.fulfilled_evidence_media_id) if wish.fulfilled_evidence_media_id else None
    return PrivatePersonalWishOut(
        id=wish.id,
        ciphertext_hex=wish.ciphertext.hex(),
        nonce_hex=wish.nonce.hex(),
        media_id=wish.media_id,
        media_url=_build_media_url(media),
        fulfilled_evidence_media_id=wish.fulfilled_evidence_media_id,
        fulfilled_evidence_media_url=_build_media_url(evidence_media),
        status=wish.status,
        fulfilled_at=wish.fulfilled_at,
        created_at=wish.created_at,
        updated_at=wish.updated_at,
    )


def _resolve_owned_media(*, db: Session, media_id: int | None, user_id: int, locale: str) -> Media | None:
    if media_id is None:
        return None

    media = db.execute(select(Media).where(Media.id == media_id)).scalar_one_or_none()
    if media is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Media not found."))
    if media.owner_id != user_id:
        raise HTTPException(status_code=403, detail=_td(locale, "Not authorized to use this media."))
    if media.status != "ready":
        raise HTTPException(status_code=409, detail=_td(locale, "Media not available yet."))
    return media


def _parse_hex_bytes(value: str | None, *, field: str, locale: str) -> bytes:
    if not value:
        raise HTTPException(status_code=400, detail=_td(locale, "Required field: {field}.", field=field))
    try:
        return bytes.fromhex(value)
    except ValueError:
        raise HTTPException(status_code=400, detail=_td(locale, "Invalid {field} (hex).", field=field))


@router.get("/personal", response_model=PrivatePersonalWishListOut)
def list_personal_private_wishes(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    wishes = db.execute(
        select(PrivatePersonalWish)
        .where(PrivatePersonalWish.user_id == current.user_number)
        .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.active)
        .order_by(PrivatePersonalWish.created_at.asc())
    ).scalars().all()

    fulfilled_total = db.execute(
        select(func.count(PrivatePersonalWish.id))
        .where(PrivatePersonalWish.user_id == current.user_number)
        .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.fulfilled)
    ).scalar_one()

    media_ids = {
        media_id
        for wish in wishes
        for media_id in (wish.media_id, wish.fulfilled_evidence_media_id)
        if media_id is not None
    }
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}

    return PrivatePersonalWishListOut(
        items=[_wish_out(wish=wish, media_map=media_map) for wish in wishes],
        active_count=len(wishes),
        active_limit=PERSONAL_ACTIVE_LIMIT,
        fulfilled_total=fulfilled_total or 0,
    )


@router.get("/personal/fulfilled", response_model=PrivatePersonalWishFulfilledListOut)
def list_fulfilled_personal_private_wishes(
    request: Request,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    total = db.execute(
        select(func.count(PrivatePersonalWish.id))
        .where(PrivatePersonalWish.user_id == current.user_number)
        .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.fulfilled)
    ).scalar_one()

    wishes = db.execute(
        select(PrivatePersonalWish)
        .where(PrivatePersonalWish.user_id == current.user_number)
        .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.fulfilled)
        .order_by(PrivatePersonalWish.fulfilled_at.desc().nullslast(), PrivatePersonalWish.id.desc())
        .offset(offset)
        .limit(limit)
    ).scalars().all()

    media_ids = {
        media_id
        for wish in wishes
        for media_id in (wish.media_id, wish.fulfilled_evidence_media_id)
        if media_id is not None
    }
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}

    return PrivatePersonalWishFulfilledListOut(
        items=[_wish_out(wish=wish, media_map=media_map) for wish in wishes],
        total=total or 0,
        limit=limit,
        offset=offset,
    )


@router.post("/personal", response_model=PrivatePersonalWishOut)
def create_personal_private_wish(
    request: Request,
    payload: PrivatePersonalWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    active_count = db.execute(
        select(func.count(PrivatePersonalWish.id))
        .where(PrivatePersonalWish.user_id == current.user_number)
        .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.active)
    ).scalar_one()
    if active_count >= PERSONAL_ACTIVE_LIMIT:
        raise HTTPException(
            status_code=409,
            detail=_td(
                locale,
                "You already reached the maximum of {limit} active private wishes.",
                limit=PERSONAL_ACTIVE_LIMIT,
            ),
        )

    ciphertext = _parse_hex_bytes(payload.ciphertext_hex, field="ciphertext_hex", locale=locale)
    nonce = _parse_hex_bytes(payload.nonce_hex, field="nonce_hex", locale=locale)
    if len(nonce) != 12:
        raise HTTPException(status_code=400, detail=_td(locale, "Invalid nonce_hex (expected 12 bytes)."))

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number, locale=locale)

    wish = PrivatePersonalWish(
        user_id=current.user_number,
        ciphertext=ciphertext,
        nonce=nonce,
        media_id=media.id if media else None,
        status=PrivatePersonalWishStatus.active,
        fulfilled_at=None,
        fulfilled_evidence_media_id=None,
    )
    db.add(wish)
    db.commit()
    db.refresh(wish)

    media_map = {media.id: media} if media else {}
    return _wish_out(wish=wish, media_map=media_map)


@router.put("/personal/{wish_id}", response_model=PrivatePersonalWishOut)
def update_personal_private_wish(
    request: Request,
    wish_id: int,
    payload: PrivatePersonalWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    wish = db.execute(
        select(PrivatePersonalWish)
        .where(PrivatePersonalWish.id == wish_id)
        .where(PrivatePersonalWish.user_id == current.user_number)
        .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Private wish not found."))

    ciphertext = _parse_hex_bytes(payload.ciphertext_hex, field="ciphertext_hex", locale=locale)
    nonce = _parse_hex_bytes(payload.nonce_hex, field="nonce_hex", locale=locale)
    if len(nonce) != 12:
        raise HTTPException(status_code=400, detail=_td(locale, "Invalid nonce_hex (expected 12 bytes)."))

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number, locale=locale)

    wish.ciphertext = ciphertext
    wish.nonce = nonce
    wish.media_id = media.id if media else None

    db.commit()
    db.refresh(wish)

    media_map = {media.id: media} if media else {}
    return _wish_out(wish=wish, media_map=media_map)


@router.delete("/personal/{wish_id}", response_model=PrivatePersonalWishDeleteResponse)
def delete_personal_private_wish(
    request: Request,
    wish_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    wish = db.execute(
        select(PrivatePersonalWish)
        .where(PrivatePersonalWish.id == wish_id)
        .where(PrivatePersonalWish.user_id == current.user_number)
        .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Private wish not found."))

    db.delete(wish)
    db.commit()
    return PrivatePersonalWishDeleteResponse(deleted=True)


@router.post("/personal/{wish_id}/fulfill", response_model=PrivatePersonalWishOut)
def fulfill_personal_private_wish(
    request: Request,
    wish_id: int,
    payload: PrivatePersonalWishFulfillRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    wish = db.execute(
        select(PrivatePersonalWish)
        .where(PrivatePersonalWish.id == wish_id)
        .where(PrivatePersonalWish.user_id == current.user_number)
        .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Private wish not found."))

    evidence_media = _resolve_owned_media(
        db=db,
        media_id=payload.evidence_media_id,
        user_id=current.user_number,
        locale=locale,
    )

    wish.status = PrivatePersonalWishStatus.fulfilled
    wish.fulfilled_at = datetime.now(timezone.utc)
    wish.fulfilled_evidence_media_id = evidence_media.id if evidence_media else None

    db.commit()
    db.refresh(wish)

    media_map: dict[int, Media] = {}
    if wish.media_id:
        media = db.execute(select(Media).where(Media.id == wish.media_id)).scalar_one_or_none()
        if media:
            media_map[media.id] = media
    if evidence_media:
        media_map[evidence_media.id] = evidence_media
    return _wish_out(wish=wish, media_map=media_map)
