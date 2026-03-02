from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.i18n import locale_from_request, tr as i18n_tr
from app.db.database import get_db
from app.db.models.life_purpose import LifePurpose
from app.db.models.media import Media
from app.db.models.private_personal_wish import PrivatePersonalWish, PrivatePersonalWishStatus
from app.db.models.public_personal_wish import PublicPersonalWish, PublicPersonalWishStatus
from app.life_purpose.schemas import (
    LifePurposeFulfillRequest,
    LifePurposeFulfillResponse,
    LifePurposeListResponse,
    LifePurposeRevealRequest,
    LifePurposeSaveRequest,
)


router = APIRouter(prefix="/life-purpose", tags=["life-purpose"])


def _locale(request: Request | None) -> str:
    return locale_from_request(request, default="en")


def _td(locale: str, en: str, **fmt: object) -> str:
    translations: dict[str, tuple[str, str]] = {
        "Media not found.": ("Medio no encontrado.", "Média introuvable."),
        "Not authorized to use this media.": ("No autorizado para usar este medio.", "Non autorisé à utiliser ce média."),
        "Media not available yet.": ("El medio aún no está disponible.", "Le média n'est pas encore disponible."),
        "Required field: {field}.": ("Campo requerido: {field}.", "Champ requis : {field}."),
        "Invalid {field} (hex).": ("{field} inválido (hex).", "{field} invalide (hex)."),
        "There are no purposes to save.": ("No hay propósitos para guardar.", "Il n'y a aucun objectif à enregistrer."),
        "Duplicate slot in payload.": ("Ranura duplicada en la carga.", "Emplacement en double dans la requête."),
        "ciphertext_hex or nonce_hex are invalid.": (
            "ciphertext_hex o nonce_hex son inválidos.",
            "ciphertext_hex ou nonce_hex sont invalides.",
        ),
        "Purpose not found.": ("Propósito no encontrado.", "Objectif introuvable."),
        "This purpose has already been marked as fulfilled.": (
            "Este propósito ya fue marcado como cumplido.",
            "Cet objectif a déjà été marqué comme accompli.",
        ),
        "Invalid nonce_hex (expected 12 bytes).": (
            "nonce_hex inválido (se esperaban 12 bytes).",
            "nonce_hex invalide (12 octets attendus).",
        ),
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


def _resolve_owned_media(*, db: Session, media_id: int | None, user_id: int, locale: str) -> Media | None:
    if media_id is None:
        return None

    media = db.query(Media).filter(Media.id == media_id).one_or_none()
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
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=_td(locale, "Invalid {field} (hex).", field=field)) from exc



@router.get("/mine", response_model=LifePurposeListResponse)
def get_my_life_purposes(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    records = (
        db.query(LifePurpose)
        .filter(LifePurpose.user_id == current.user_number)
        .order_by(LifePurpose.slot_number.asc())
        .all()
    )

    slots = []
    for record in records:
        slots.append(
            {
                "slot_number": record.slot_number,
                "is_private": record.is_private,
                "status": record.status,
                "reveal_at": record.reveal_at,
                "text_public": record.text_public,
                "ciphertext_hex": record.ciphertext.hex() if record.ciphertext else None,
                "nonce_hex": record.nonce.hex() if record.nonce else None,
                "icon_key": record.icon_key,
            }
        )

    return {"slots": slots}


@router.post("/save")
def save_life_purposes(
    request: Request,
    payload: LifePurposeSaveRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    if not payload.slots:
        raise HTTPException(status_code=400, detail=_td(locale, "There are no purposes to save."))

    seen_slots = set()
    for slot in payload.slots:
        if slot.slot_number in seen_slots:
            raise HTTPException(status_code=400, detail=_td(locale, "Duplicate slot in payload."))
        seen_slots.add(slot.slot_number)

        try:
            ciphertext = bytes.fromhex(slot.ciphertext_hex) if slot.ciphertext_hex else None
            nonce = bytes.fromhex(slot.nonce_hex) if slot.nonce_hex else None
        except ValueError:
            raise HTTPException(status_code=400, detail=_td(locale, "ciphertext_hex or nonce_hex are invalid."))

        text_public = slot.text_public.strip() if slot.text_public else None

        record = (
            db.query(LifePurpose)
            .filter(
                LifePurpose.user_id == current.user_number,
                LifePurpose.slot_number == slot.slot_number,
            )
            .one_or_none()
        )

        if record:
            record.is_private = slot.is_private
            record.status = "active"
            record.reveal_at = slot.reveal_at
            record.text_public = text_public if not slot.is_private else None
            record.ciphertext = ciphertext if slot.is_private else None
            record.nonce = nonce if slot.is_private else None
            record.icon_key = slot.icon_key
        else:
            record = LifePurpose(
                user_id=current.user_number,
                slot_number=slot.slot_number,
                is_private=slot.is_private,
                status="active",
                reveal_at=slot.reveal_at,
                text_public=text_public if not slot.is_private else None,
                ciphertext=ciphertext if slot.is_private else None,
                nonce=nonce if slot.is_private else None,
                icon_key=slot.icon_key,
            )
            db.add(record)

    db.commit()
    return {"saved": len(payload.slots)}


@router.post("/reveal")
def reveal_life_purpose(
    request: Request,
    payload: LifePurposeRevealRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    record = (
        db.query(LifePurpose)
        .filter(
            LifePurpose.user_id == current.user_number,
            LifePurpose.slot_number == payload.slot_number,
        )
        .one_or_none()
    )
    if not record:
        raise HTTPException(status_code=404, detail=_td(locale, "Purpose not found."))

    record.is_private = False
    record.status = "active"
    record.text_public = payload.text_public
    record.ciphertext = None
    record.nonce = None
    db.commit()

    return {"revealed": True, "slot_number": payload.slot_number}


@router.post("/fulfill", response_model=LifePurposeFulfillResponse)
def fulfill_life_purpose(
    request: Request,
    payload: LifePurposeFulfillRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    record = (
        db.query(LifePurpose)
        .filter(
            LifePurpose.user_id == current.user_number,
            LifePurpose.slot_number == payload.slot_number,
        )
        .one_or_none()
    )
    if not record:
        raise HTTPException(status_code=404, detail=_td(locale, "Purpose not found."))
    if record.status == "fulfilled":
        raise HTTPException(status_code=409, detail=_td(locale, "This purpose has already been marked as fulfilled."))

    evidence_media = _resolve_owned_media(
        db=db,
        media_id=payload.evidence_media_id,
        user_id=current.user_number,
        locale=locale,
    )

    now = datetime.now(timezone.utc)

    public_wish_id: int | None = None
    private_wish_id: int | None = None

    if payload.publish_to == "public":
        # If the user is publishing publicly, we must wipe any private slot data,
        # but we do not keep the plaintext in the life-purpose slot after fulfillment.
        record.is_private = False
        record.ciphertext = None
        record.nonce = None

        wish = PublicPersonalWish(
            user_id=current.user_number,
            wish_text=payload.wish_text,
            wish_type=payload.wish_type,
            media_id=None,
            fulfilled_evidence_media_id=evidence_media.id if evidence_media else None,
            status=PublicPersonalWishStatus.fulfilled,
            fulfilled_at=now,
            life_purpose_slot_number=record.slot_number,
            life_purpose_icon_key=record.icon_key,
        )
        db.add(wish)
        db.flush()
        public_wish_id = wish.id
    else:
        ciphertext = _parse_hex_bytes(payload.ciphertext_hex, field="ciphertext_hex", locale=locale)
        nonce = _parse_hex_bytes(payload.nonce_hex, field="nonce_hex", locale=locale)
        if len(nonce) != 12:
            raise HTTPException(status_code=400, detail=_td(locale, "Invalid nonce_hex (expected 12 bytes)."))

        wish = PrivatePersonalWish(
            user_id=current.user_number,
            ciphertext=ciphertext,
            nonce=nonce,
            media_id=None,
            fulfilled_evidence_media_id=evidence_media.id if evidence_media else None,
            status=PrivatePersonalWishStatus.fulfilled,
            fulfilled_at=now,
        )
        db.add(wish)
        db.flush()
        private_wish_id = wish.id

    # After migration to fulfilled wishes, clear the slot so the user is prompted
    # to define a new purpose explicitly from the cover editor.
    record.status = "fulfilled"
    record.is_private = False
    record.reveal_at = None
    record.text_public = None
    record.ciphertext = None
    record.nonce = None
    record.icon_key = None

    db.commit()

    return LifePurposeFulfillResponse(
        slot_number=payload.slot_number,
        publish_to=payload.publish_to,
        public_wish_id=public_wish_id,
        private_wish_id=private_wish_id,
    )
