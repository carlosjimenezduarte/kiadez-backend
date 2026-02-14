from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.db.models.private_personal_wish import PrivatePersonalWishStatus


class PrivatePersonalWishUpsertRequest(BaseModel):
    ciphertext_hex: str = Field(..., min_length=2)
    nonce_hex: str = Field(..., min_length=2)
    media_id: int | None = Field(default=None, gt=0)


class PrivatePersonalWishFulfillRequest(BaseModel):
    evidence_media_id: int | None = Field(default=None, gt=0)


class PrivatePersonalWishOut(BaseModel):
    id: int
    ciphertext_hex: str
    nonce_hex: str
    media_id: int | None = None
    media_url: str | None = None
    fulfilled_evidence_media_id: int | None = None
    fulfilled_evidence_media_url: str | None = None
    status: PrivatePersonalWishStatus
    fulfilled_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class PrivatePersonalWishListOut(BaseModel):
    items: list[PrivatePersonalWishOut]
    active_count: int
    active_limit: int
    fulfilled_total: int


class PrivatePersonalWishFulfilledListOut(BaseModel):
    items: list[PrivatePersonalWishOut]
    total: int
    limit: int
    offset: int


class PrivatePersonalWishDeleteResponse(BaseModel):
    deleted: bool

