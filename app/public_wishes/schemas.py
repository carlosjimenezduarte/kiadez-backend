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

PublicCooperativeWishType = Literal[
    "Espiritual",
    "Material",
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


PublicWishFulfillmentAttributionModeLiteral = Literal["secret", "public"]


class PublicPersonalWishGuardianFulfillRequest(BaseModel):
    commitment_code: str = Field(..., min_length=1, max_length=32)
    attribution_mode: PublicWishFulfillmentAttributionModeLiteral
    evidence_media_id: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def normalize_fields(self):
        normalized_code = (self.commitment_code or "").strip().upper()
        if not normalized_code:
            raise ValueError("Debes indicar el código de compromiso.")
        self.commitment_code = normalized_code
        return self


class PublicPersonalWishUnfreezeRequest(BaseModel):
    reason_type: Literal["error", "unexpected"]
    reason_text: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_reason(self):
        text = (self.reason_text or "").strip()
        if self.reason_type == "unexpected":
            if not text:
                raise ValueError("Debes describir el imprevisto para descongelar el deseo.")
            words = [word for word in text.split() if word]
            if len(words) > 100:
                raise ValueError("La explicación no puede superar 100 palabras.")
            self.reason_text = text
            return self

        self.reason_text = None
        return self


class PublicPersonalWishOut(BaseModel):
    id: int
    wish_text: str
    wish_type: PublicPersonalWishType
    life_purpose_slot_number: int | None = None
    life_purpose_icon_key: str | None = None
    media_id: int | None = None
    media_url: str | None = None
    fulfilled_evidence_media_id: int | None = None
    fulfilled_evidence_media_url: str | None = None
    status: PublicPersonalWishStatus
    is_frozen: bool = False
    frozen_at: datetime | None = None
    frozen_by_guardian_id: int | None = None
    frozen_by_guardian_full_name: str | None = None
    frozen_by_guardian_profile_url: str | None = None
    fulfilled_commitment_code: str | None = None
    fulfillment_attribution_mode: PublicWishFulfillmentAttributionModeLiteral | None = None
    fulfillment_message: str | None = None
    fulfilled_by_user_id: int | None = None
    fulfilled_by_handle: str | None = None
    fulfilled_by_profile_url: str | None = None
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


class PublicCooperativeWishUpsertRequest(BaseModel):
    wish_text: str = Field(..., min_length=1, max_length=120)
    wish_type: PublicCooperativeWishType
    participants_goal: int = Field(..., ge=1, le=10)
    template_text: str | None = Field(default=None, max_length=500)
    security_code: str = Field(..., min_length=6, max_length=6)
    media_id: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def normalize_fields(self):
        self.wish_text = self.wish_text.strip()
        if not self.wish_text:
            raise ValueError("El deseo no puede estar vacío.")

        normalized_template = (self.template_text or "").strip()
        self.template_text = normalized_template if normalized_template else None

        normalized_code = "".join(ch for ch in (self.security_code or "") if ch.isdigit())
        if len(normalized_code) != 6:
            raise ValueError("El código de seguridad debe tener exactamente 6 dígitos.")
        self.security_code = normalized_code
        return self


class PublicCooperativeWishParticipationUpsertRequest(BaseModel):
    security_code: str | None = Field(default=None, min_length=6, max_length=6)
    participation_text: str = Field(..., min_length=1, max_length=255)

    @model_validator(mode="after")
    def normalize_fields(self):
        if self.security_code is not None:
            normalized_code = "".join(ch for ch in (self.security_code or "") if ch.isdigit())
            if len(normalized_code) != 6:
                raise ValueError("El código de seguridad debe tener exactamente 6 dígitos.")
            self.security_code = normalized_code
        else:
            self.security_code = None

        normalized_text = (self.participation_text or "").strip()
        if not normalized_text:
            raise ValueError("Debes describir tu participación.")
        self.participation_text = normalized_text
        return self


class PublicCooperativeWishParticipationCompleteRequest(BaseModel):
    evidence_media_id: int = Field(..., gt=0)
    oath_accepted: bool = False

    @model_validator(mode="after")
    def validate_oath(self):
        if self.oath_accepted is not True:
            raise ValueError("Debes aceptar el juramento para registrar la evidencia.")
        return self


class PublicCooperativeWishFulfillRequest(BaseModel):
    evidence_media_id: int = Field(..., gt=0)
    oath_accepted: bool = False

    @model_validator(mode="after")
    def validate_oath(self):
        if self.oath_accepted is not True:
            raise ValueError("Debes aceptar el juramento para marcar este deseo como cumplido.")
        return self


PublicCooperativeParticipationStatusLiteral = Literal["pending", "completed", "validated"]


class PublicCooperativeWishParticipantReviewOut(BaseModel):
    participation_id: int
    participant_user_id: int
    participant_handle: str
    participant_profile_url: str
    participant_profile_photo_url: str | None = None
    participation_text: str
    evidence_media_id: int
    evidence_media_url: str | None = None
    completed_at: datetime
    validated_at: datetime | None = None
    is_validated: bool = False


class PublicCooperativeWishOut(BaseModel):
    id: int
    user_id: int
    wish_text: str
    wish_type: PublicCooperativeWishType
    participants_goal: int
    participants_current: int
    template_text: str | None = None
    security_code: str | None = None
    media_id: int | None = None
    media_url: str | None = None
    viewer_participation_id: int | None = None
    viewer_participation_text: str | None = None
    viewer_participation_status: PublicCooperativeParticipationStatusLiteral | None = None
    viewer_participation_has_evidence: bool = False
    viewer_participation_completed_at: datetime | None = None
    viewer_participation_validated_at: datetime | None = None
    owner_review_items: list[PublicCooperativeWishParticipantReviewOut] = Field(default_factory=list)
    owner_pending_validation_count: int = 0
    owner_can_mark_fulfilled: bool = False
    is_fulfilled: bool = False
    fulfilled_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class PublicCooperativeWishListOut(BaseModel):
    items: list[PublicCooperativeWishOut]
    active_count: int
    active_limit: int


class PublicCooperativeWishFulfilledOut(BaseModel):
    id: int
    user_id: int
    wish_text: str
    wish_type: PublicCooperativeWishType
    participants_goal: int
    participants_current: int
    media_id: int | None = None
    media_url: str | None = None
    fulfilled_evidence_media_id: int | None = None
    fulfilled_evidence_media_url: str | None = None
    fulfilled_at: datetime
    created_at: datetime
    updated_at: datetime


class PublicCooperativeWishFulfilledListOut(BaseModel):
    items: list[PublicCooperativeWishFulfilledOut]
    total: int
    limit: int
    offset: int
