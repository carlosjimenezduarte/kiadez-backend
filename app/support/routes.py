from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from app.core.mailer import send_contact_email


class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str


router = APIRouter(prefix="/support", tags=["support"])


@router.post("/contact")
def contact(payload: ContactRequest):
    try:
        send_contact_email(
            name=payload.name.strip(),
            email=payload.email.strip().lower(),
            message=payload.message.strip(),
        )
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo enviar el mensaje.")

    return {"message": "Gracias, hemos recibido tu mensaje."}
