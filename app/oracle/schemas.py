from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.db.models.oracle import OracleResponseType

MAX_PUBLIC_RESPONSE_WORDS = 500


def _count_words(text: str) -> int:
    normalized = (text or "").strip()
    if not normalized:
        return 0
    return len([part for part in normalized.split() if part])


class OracleRespondRequest(BaseModel):
    card_id: int = Field(..., ge=1, le=30)
    response_type: OracleResponseType

    text_public: str | None = Field(default=None, max_length=4000)
    ciphertext_hex: str | None = None
    nonce_hex: str | None = None

    @model_validator(mode="after")
    def validate_payload(self):
        if self.response_type == OracleResponseType.public:
            text = (self.text_public or "").strip()
            if not text:
                raise ValueError("text_public es requerido si la respuesta es pública.")
            words = _count_words(text)
            if words > MAX_PUBLIC_RESPONSE_WORDS:
                raise ValueError(f"La respuesta pública supera el máximo de {MAX_PUBLIC_RESPONSE_WORDS} palabras.")
            self.text_public = text
            self.ciphertext_hex = None
            self.nonce_hex = None
            return self

        if self.response_type == OracleResponseType.secret:
            if not self.ciphertext_hex or not self.nonce_hex:
                raise ValueError("ciphertext_hex y nonce_hex son requeridos si la respuesta es secreta.")
            self.text_public = None
            return self

        self.text_public = None
        self.ciphertext_hex = None
        self.nonce_hex = None
        return self


class OracleResponseOut(BaseModel):
    id: int
    card_id: int
    cycle: int
    response_type: OracleResponseType
    created_at: datetime
    text_public: str | None = None
    ciphertext_hex: str | None = None
    nonce_hex: str | None = None


class OracleStateOut(BaseModel):
    cycle: int
    cycle_started_at: datetime
    last_pick_at: datetime | None = None
    cooldown_ms: int
    cooldown_remaining_ms: int
    cycle_complete: bool
    revealed_this_cycle: list[int]
    responses: list[OracleResponseOut]
