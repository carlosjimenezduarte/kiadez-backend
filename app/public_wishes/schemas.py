from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.db.models.public_personal_wish import PublicPersonalWishStatus

PublicPersonalWishType = Literal[
    "Espiritual",
    "Material",
    "Monetario",
    "Profesional",
    "Salud y cuerpo",
    "Relacional",
    "Vivencial",
]


class PublicPersonalWishUpsertRequest(BaseModel):
    wish_text: str = Field(..., min_length=1, max_length=120)
    wish_type: PublicPersonalWishType
    media_id: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def normalize_fields(self):
        self.wish_text = self.wish_text.strip()
        if not self.wish_text:
            raise ValueError("El deseo no puede estar vacío.")
        return self


class PublicPersonalWishFulfillRequest(BaseModel):
    evidence_media_id: int | None = Field(default=None, gt=0)


class PublicPersonalWishOut(BaseModel):
    id: int
    wish_text: str
    wish_type: PublicPersonalWishType
    media_id: int | None = None
    media_url: str | None = None
    fulfilled_evidence_media_id: int | None = None
    fulfilled_evidence_media_url: str | None = None
    status: PublicPersonalWishStatus
    fulfilled_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class PublicPersonalWishListOut(BaseModel):
    items: list[PublicPersonalWishOut]
    active_count: int
    active_limit: int
    fulfilled_total: int


class PublicPersonalWishFulfilledListOut(BaseModel):
    items: list[PublicPersonalWishOut]
    total: int
    limit: int
    offset: int


class PublicPersonalWishDeleteResponse(BaseModel):
    deleted: bool
