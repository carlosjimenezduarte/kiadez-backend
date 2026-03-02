from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr

from app.core.i18n import locale_from_request, tr
from app.core.mailer import send_contact_email


class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str


router = APIRouter(prefix="/support", tags=["support"])


@router.post("/contact")
def contact(payload: ContactRequest, request: Request):
    locale = locale_from_request(request, default="en")
    try:
        send_contact_email(
            name=payload.name.strip(),
            email=payload.email.strip().lower(),
            message=payload.message.strip(),
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=tr(
                locale,
                es="No se pudo enviar el mensaje.",
                en="Could not send the message.",
                fr="Impossible d'envoyer le message.",
            ),
        )

    return {
        "message": tr(
            locale,
            es="Gracias, hemos recibido tu mensaje.",
            en="Thank you, we have received your message.",
            fr="Merci, nous avons bien reçu votre message.",
        )
    }
