from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.db.models.guardian_wish_message import GuardianWishMessageKind


class MessageThreadCreateInput(BaseModel):
    to_user_id: int | None = Field(default=None, gt=0)
    to_username: str | None = Field(default=None, min_length=1, max_length=30)
    subject: str = Field(..., min_length=1, max_length=180)
    body: str = Field(..., min_length=1, max_length=10000)

    @model_validator(mode="after")
    def normalize(self):
        username = (self.to_username or "").strip().lower()
        while username.startswith("@"):
            username = username[1:]

        if bool(self.to_user_id) == bool(username):
            raise ValueError("You must send exactly one: to_user_id or to_username.")

        self.to_username = username or None
        self.subject = (self.subject or "").strip()
        self.body = (self.body or "").strip()

        if not self.subject:
            raise ValueError("You must write the subject.")
        if not self.body:
            raise ValueError("You must write the message.")

        return self


class MessageReplyInput(BaseModel):
    body: str = Field(..., min_length=1, max_length=10000)

    @model_validator(mode="after")
    def normalize(self):
        self.body = (self.body or "").strip()
        if not self.body:
            raise ValueError("You must write the message.")
        return self


class MessageEntryOut(BaseModel):
    id: int
    sender_user_id: int | None = None
    sender_name: str
    sender_handle: str
    body: str
    created_at: datetime


class MessageThreadOut(BaseModel):
    id: int
    subject: str

    guardian_user_id: int | None = None
    guardian_name: str | None = None
    guardian_handle: str | None = None

    recipient_user_id: int
    recipient_name: str
    recipient_handle: str

    created_at: datetime
    updated_at: datetime

    is_guardian_center_origin: bool = False
    source_guardian_wish_message_id: int | None = None
    source_wish_request_id: int | None = None
    source_kind: GuardianWishMessageKind | None = None

    can_reply: bool = False

    messages: list[MessageEntryOut] = Field(default_factory=list)


class MessageThreadListOut(BaseModel):
    items: list[MessageThreadOut] = Field(default_factory=list)
