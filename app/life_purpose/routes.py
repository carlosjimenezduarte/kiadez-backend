from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
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

def _resolve_owned_media(*, db: Session, media_id: int | None, user_id: int) -> Media | None:
    if media_id is None:
        return None

    media = db.query(Media).filter(Media.id == media_id).one_or_none()
    if media is None:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if media.owner_id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado para usar esta media.")
    if media.status != "ready":
        raise HTTPException(status_code=409, detail="Media aún no disponible.")
    return media


def _parse_hex_bytes(value: str | None, *, field: str) -> bytes:
    if not value:
        raise HTTPException(status_code=400, detail=f"Campo requerido: {field}.")
    try:
        return bytes.fromhex(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"{field} inválido (hex).") from exc



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
    payload: LifePurposeSaveRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not payload.slots:
        raise HTTPException(status_code=400, detail="No hay propositos para guardar.")

    seen_slots = set()
    for slot in payload.slots:
        if slot.slot_number in seen_slots:
            raise HTTPException(status_code=400, detail="Slot duplicado en el payload.")
        seen_slots.add(slot.slot_number)

        try:
            ciphertext = bytes.fromhex(slot.ciphertext_hex) if slot.ciphertext_hex else None
            nonce = bytes.fromhex(slot.nonce_hex) if slot.nonce_hex else None
        except ValueError:
            raise HTTPException(status_code=400, detail="ciphertext_hex o nonce_hex invalidos.")

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
    payload: LifePurposeRevealRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(LifePurpose)
        .filter(
            LifePurpose.user_id == current.user_number,
            LifePurpose.slot_number == payload.slot_number,
        )
        .one_or_none()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Propósito no encontrado.")

    record.is_private = False
    record.status = "active"
    record.text_public = payload.text_public
    record.ciphertext = None
    record.nonce = None
    db.commit()

    return {"revealed": True, "slot_number": payload.slot_number}


@router.post("/fulfill", response_model=LifePurposeFulfillResponse)
def fulfill_life_purpose(
    payload: LifePurposeFulfillRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(LifePurpose)
        .filter(
            LifePurpose.user_id == current.user_number,
            LifePurpose.slot_number == payload.slot_number,
        )
        .one_or_none()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Propósito no encontrado.")
    if record.status == "fulfilled":
        raise HTTPException(status_code=409, detail="Este propósito ya fue marcado como cumplido.")

    evidence_media = _resolve_owned_media(
        db=db,
        media_id=payload.evidence_media_id,
        user_id=current.user_number,
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
        ciphertext = _parse_hex_bytes(payload.ciphertext_hex, field="ciphertext_hex")
        nonce = _parse_hex_bytes(payload.nonce_hex, field="nonce_hex")
        if len(nonce) != 12:
            raise HTTPException(status_code=400, detail="nonce_hex inválido (se esperan 12 bytes).")

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
