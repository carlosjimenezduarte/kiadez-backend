from datetime import date
from typing import Optional, List

from pydantic import BaseModel, Field, model_validator


class LifePurposeSlotIn(BaseModel):
    slot_number: int = Field(..., ge=1, le=3)
    is_private: bool = False
    text_public: Optional[str] = Field(default=None, max_length=500)
    ciphertext_hex: Optional[str] = None
    nonce_hex: Optional[str] = None
    reveal_at: Optional[date] = None
    icon_key: Optional[str] = Field(default=None, max_length=20)

    @model_validator(mode="after")
    def validate_content(self):
        if self.is_private:
            if not self.ciphertext_hex or not self.nonce_hex:
                raise ValueError("ciphertext_hex y nonce_hex son requeridos si es privado.")
            self.text_public = None
        else:
            if not self.text_public:
                raise ValueError("text_public es requerido si es publico.")
            self.ciphertext_hex = None
            self.nonce_hex = None

        return self


class LifePurposeSaveRequest(BaseModel):
    slots: List[LifePurposeSlotIn]


class LifePurposeRevealRequest(BaseModel):
    slot_number: int = Field(..., ge=1, le=3)
    text_public: str = Field(..., min_length=1, max_length=500)

    @model_validator(mode="after")
    def normalize_text(self):
        self.text_public = self.text_public.strip()
        if not self.text_public:
            raise ValueError("text_public es requerido.")
        return self


class LifePurposeSlotOut(BaseModel):
    slot_number: int
    is_private: bool
    status: str
    reveal_at: Optional[date] = None
    text_public: Optional[str] = None
    ciphertext_hex: Optional[str] = None
    nonce_hex: Optional[str] = None
    icon_key: Optional[str] = None


class LifePurposeListResponse(BaseModel):
    slots: List[LifePurposeSlotOut]
