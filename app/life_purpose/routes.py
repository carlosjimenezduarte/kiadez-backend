from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.routes import get_current_user
from app.auth.models import UserPublic
from app.db.database import get_db
from app.db.models.life_purpose import LifePurpose
from app.life_purpose.schemas import (
    LifePurposeListResponse,
    LifePurposeRevealRequest,
    LifePurposeSaveRequest,
)


router = APIRouter(prefix="/life-purpose", tags=["life-purpose"])


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
