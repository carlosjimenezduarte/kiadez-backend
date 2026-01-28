from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.routes import get_current_user
from app.auth.models import UserPublic
from app.db.database import get_db
from app.db.models.life_purpose import LifePurpose
from app.life_purpose.schemas import LifePurposeSaveRequest


router = APIRouter(prefix="/life-purpose", tags=["life-purpose"])


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
