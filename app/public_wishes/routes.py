from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.config import settings
from app.core.storage import S3NotConfiguredError, generate_presigned_get_url
from app.db.database import get_db
from app.db.models.media import Media
from app.db.models.public_personal_wish import PublicPersonalWish, PublicPersonalWishStatus
from app.db.models.user import User
from app.public_wishes.schemas import (
    PublicPersonalWishDeleteResponse,
    PublicPersonalWishFulfilledListOut,
    PublicPersonalWishFulfillRequest,
    PublicPersonalWishListOut,
    PublicPersonalWishOut,
    PublicPersonalWishUpsertRequest,
)

router = APIRouter(prefix="/public-wishes", tags=["public-wishes"])

PERSONAL_ACTIVE_LIMIT = 50


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


def _wish_out(
    *,
    wish: PublicPersonalWish,
    media_map: dict[int, Media],
) -> PublicPersonalWishOut:
    media = media_map.get(wish.media_id) if wish.media_id else None
    evidence_media = media_map.get(wish.fulfilled_evidence_media_id) if wish.fulfilled_evidence_media_id else None
    return PublicPersonalWishOut(
        id=wish.id,
        wish_text=wish.wish_text,
        wish_type=wish.wish_type,
        life_purpose_slot_number=wish.life_purpose_slot_number,
        life_purpose_icon_key=wish.life_purpose_icon_key,
        media_id=wish.media_id,
        media_url=_build_media_url(media),
        fulfilled_evidence_media_id=wish.fulfilled_evidence_media_id,
        fulfilled_evidence_media_url=_build_media_url(evidence_media),
        status=wish.status,
        fulfilled_at=wish.fulfilled_at,
        created_at=wish.created_at,
        updated_at=wish.updated_at,
    )


def _resolve_owned_media(*, db: Session, media_id: int | None, user_id: int) -> Media | None:
    if media_id is None:
        return None

    media = db.execute(select(Media).where(Media.id == media_id)).scalar_one_or_none()
    if media is None:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if media.owner_id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado para usar esta media.")
    if media.status != "ready":
        raise HTTPException(status_code=409, detail="Media aún no disponible.")
    return media


@router.get("/personal", response_model=PublicPersonalWishListOut)
def list_personal_wishes(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    wishes = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
        .order_by(PublicPersonalWish.created_at.asc())
    ).scalars().all()

    fulfilled_total = db.execute(
        select(func.count(PublicPersonalWish.id))
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
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

    return PublicPersonalWishListOut(
        items=[_wish_out(wish=wish, media_map=media_map) for wish in wishes],
        active_count=len(wishes),
        active_limit=PERSONAL_ACTIVE_LIMIT,
        fulfilled_total=fulfilled_total or 0,
    )


@router.get("/personal/fulfilled", response_model=PublicPersonalWishFulfilledListOut)
def list_fulfilled_personal_wishes(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    total = db.execute(
        select(func.count(PublicPersonalWish.id))
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
    ).scalar_one()

    wishes = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
        .order_by(PublicPersonalWish.fulfilled_at.desc().nullslast(), PublicPersonalWish.id.desc())
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

    return PublicPersonalWishFulfilledListOut(
        items=[_wish_out(wish=wish, media_map=media_map) for wish in wishes],
        total=total or 0,
        limit=limit,
        offset=offset,
    )


@router.post("/personal", response_model=PublicPersonalWishOut)
def create_personal_wish(
    payload: PublicPersonalWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    active_count = db.execute(
        select(func.count(PublicPersonalWish.id))
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one()
    if active_count >= PERSONAL_ACTIVE_LIMIT:
        raise HTTPException(
            status_code=409,
            detail=f"Ya alcanzaste el máximo de {PERSONAL_ACTIVE_LIMIT} deseos personales activos.",
        )

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number)

    wish = PublicPersonalWish(
        user_id=current.user_number,
        wish_text=payload.wish_text,
        wish_type=payload.wish_type,
        media_id=media.id if media else None,
        status=PublicPersonalWishStatus.active,
        fulfilled_at=None,
        fulfilled_evidence_media_id=None,
    )
    db.add(wish)
    db.commit()
    db.refresh(wish)

    media_map = {media.id: media} if media else {}
    return _wish_out(wish=wish, media_map=media_map)


@router.put("/personal/{wish_id}", response_model=PublicPersonalWishOut)
def update_personal_wish(
    wish_id: int,
    payload: PublicPersonalWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo personal no encontrado.")

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number)

    wish.wish_text = payload.wish_text
    wish.wish_type = payload.wish_type
    wish.media_id = media.id if media else None

    db.commit()
    db.refresh(wish)

    media_map = {media.id: media} if media else {}
    return _wish_out(wish=wish, media_map=media_map)


@router.post("/personal/{wish_id}/fulfill", response_model=PublicPersonalWishOut)
def fulfill_personal_wish(
    wish_id: int,
    payload: PublicPersonalWishFulfillRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo personal no encontrado.")

    evidence_media = _resolve_owned_media(
        db=db,
        media_id=payload.evidence_media_id,
        user_id=current.user_number,
    )

    wish.status = PublicPersonalWishStatus.fulfilled
    wish.fulfilled_at = datetime.now(timezone.utc)
    wish.fulfilled_evidence_media_id = evidence_media.id if evidence_media else None

    db.commit()
    db.refresh(wish)

    media_ids = {media_id for media_id in (wish.media_id, wish.fulfilled_evidence_media_id) if media_id is not None}
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}

    return _wish_out(wish=wish, media_map=media_map)


@router.delete("/personal/{wish_id}", response_model=PublicPersonalWishDeleteResponse)
def delete_personal_wish(
    wish_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo personal no encontrado.")

    db.delete(wish)
    db.commit()
    return PublicPersonalWishDeleteResponse(deleted=True)
