from datetime import date
from typing import Optional, List

from pydantic import BaseModel, Field, root_validator


class LifePurposeSlotIn(BaseModel):
    slot_number: int = Field(..., ge=1, le=3)
    is_private: bool = False
    text_public: Optional[str] = Field(default=None, max_length=500)
    ciphertext_hex: Optional[str] = None
    nonce_hex: Optional[str] = None
    reveal_at: Optional[date] = None
    icon_key: Optional[str] = Field(default=None, max_length=20)

    @root_validator
    def validate_content(cls, values):
        is_private = values.get("is_private")
        text_public = values.get("text_public")
        ciphertext_hex = values.get("ciphertext_hex")
        nonce_hex = values.get("nonce_hex")

        if is_private:
            if not ciphertext_hex or not nonce_hex:
                raise ValueError("ciphertext_hex y nonce_hex son requeridos si es privado.")
            values["text_public"] = None
        else:
            if not text_public:
                raise ValueError("text_public es requerido si es publico.")
            values["ciphertext_hex"] = None
            values["nonce_hex"] = None

        return values


class LifePurposeSaveRequest(BaseModel):
    slots: List[LifePurposeSlotIn]
