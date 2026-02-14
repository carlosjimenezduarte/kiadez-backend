from pydantic import BaseModel, Field


class VaultResetKeywordsOut(BaseModel):
    keywords: dict[str, str]


class VaultResetRequest(BaseModel):
    confirm_keyword: str = Field(..., min_length=1)


class VaultResetOut(BaseModel):
    vault_deleted: bool
    life_purpose_private_cleared: int
    private_wishes_cleared: int = 0
    private_media_deleted: int = 0
