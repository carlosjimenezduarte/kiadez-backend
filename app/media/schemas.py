from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.db.models.media import MediaVisibility


class MediaPresignRequest(BaseModel):
    filename: Optional[str] = None
    content_type: str
    size_bytes: int = Field(..., gt=0)
    visibility: MediaVisibility = MediaVisibility.private
    obfuscate_owner: bool = False


class MediaPresignResponse(BaseModel):
    media_id: int
    object_key: str
    upload_url: str
    method: str = "PUT"
    expires_in: int
    required_headers: dict[str, str]


class MediaConfirmRequest(BaseModel):
    media_id: int
    title: Optional[str] = None
    text: Optional[str] = None
    published_at: Optional[datetime] = None
    duration_seconds: Optional[int] = Field(default=None, ge=0)
    width: Optional[int] = Field(default=None, ge=0)
    height: Optional[int] = Field(default=None, ge=0)


class MediaURLResponse(BaseModel):
    media_id: int
    url: str
    expires_in: int


class MediaDeleteResponse(BaseModel):
    deleted: bool


class MediaImageOption(BaseModel):
    media_id: int
    url: str
    created_at: datetime
    original_filename: Optional[str] = None


class MediaImageOptionListResponse(BaseModel):
    items: list[MediaImageOption]
    expires_in: int


class ProfilePhotoSetRequest(BaseModel):
    media_id: Optional[int] = Field(default=None, gt=0)


class ProfilePhotoResponse(BaseModel):
    media_id: Optional[int] = None
    url: Optional[str] = None
    expires_in: int = 0
