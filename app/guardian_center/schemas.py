from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, model_validator

from app.db.models.guardian_wish_request import GuardianWishRequestStatus
from app.db.models.guardian_wish_message import GuardianWishMessageKind


class GuardianWishRequestCreate(BaseModel):
    public_wish_id: int = Field(..., gt=0)
    guardian_user_id: int | None = Field(default=None, gt=0)
    reason: str = Field(..., min_length=1, max_length=5000)
    phone: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    evidence_media_id: int = Field(..., gt=0)


class GuardianWishRequestUserOut(BaseModel):
    user_id: int
    full_name: str
    username: str | None = None
    handle: str
    profile_url: str


class GuardianWishRequestOut(BaseModel):
    id: int
    status: GuardianWishRequestStatus
    created_at: datetime
    updated_at: datetime

    requester: GuardianWishRequestUserOut
    guardian: GuardianWishRequestUserOut | None = None
    wish_owner: GuardianWishRequestUserOut

    public_wish_id: int
    wish_text: str
    wish_type: str
    wish_url: str

    reason: str
    contact_phone: str
    contact_email: str

    evidence_media_id: int | None = None
    evidence_mime_type: str | None = None
    evidence_url: str | None = None
    commitment_code: str | None = None
    commitment_sealed_at: datetime | None = None
    denied_at: datetime | None = None


class GuardianWishRequestDenyInput(BaseModel):
    subject: str = Field(..., min_length=1, max_length=180)
    body: str = Field(..., min_length=1, max_length=10000)

    @model_validator(mode="after")
    def normalize(self):
        self.subject = (self.subject or "").strip()
        self.body = (self.body or "").strip()
        if not self.subject:
            raise ValueError("Debes escribir el asunto.")
        if not self.body:
            raise ValueError("Debes escribir el mensaje.")
        return self


class GuardianWishRequestOwnerMessageInput(BaseModel):
    subject: str = Field(..., min_length=1, max_length=180)
    body: str = Field(..., min_length=1, max_length=10000)

    @model_validator(mode="after")
    def normalize(self):
        self.subject = (self.subject or "").strip()
        self.body = (self.body or "").strip()
        if not self.subject:
            raise ValueError("Debes escribir el asunto.")
        if not self.body:
            raise ValueError("Debes escribir el mensaje.")
        return self


class GuardianWishMessageOut(BaseModel):
    id: int
    wish_request_id: int
    kind: GuardianWishMessageKind
    recipient_user_id: int
    recipient_handle: str
    subject: str
    body: str
    created_at: datetime


class GuardianWishRequestListOut(BaseModel):
    items: list[GuardianWishRequestOut] = Field(default_factory=list)
    page: int = 1
    page_size: int = 10
    total: int = 0
    total_pages: int = 1
    range_start: int = 0
    range_end: int = 0
