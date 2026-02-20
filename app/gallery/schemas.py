from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

GalleryVisibility = Literal["public", "private"]


def _normalize_folder_name(value: str) -> str:
    return " ".join((value or "").strip().split())


class GalleryFolderCreateInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    visibility: GalleryVisibility = "public"

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = _normalize_folder_name(value)
        if not normalized:
            raise ValueError("Debes escribir el nombre de la carpeta.")
        return normalized

    @field_validator("visibility")
    @classmethod
    def validate_visibility(cls, value: str) -> str:
        normalized = str(value or "").strip().lower()
        if normalized not in {"public", "private"}:
            raise ValueError("La visibilidad debe ser public o private.")
        return normalized


class GalleryFolderUpdateInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = _normalize_folder_name(value)
        if not normalized:
            raise ValueError("Debes escribir el nombre de la carpeta.")
        return normalized


class GalleryFolderAssignImagesInput(BaseModel):
    media_ids: list[int] = Field(..., min_length=1, max_length=200)

    @field_validator("media_ids")
    @classmethod
    def validate_media_ids(cls, values: list[int]) -> list[int]:
        deduped: list[int] = []
        seen: set[int] = set()

        for raw in values:
            media_id = int(raw or 0)
            if media_id <= 0:
                raise ValueError("Todos los media_ids deben ser mayores a 0.")
            if media_id in seen:
                continue
            seen.add(media_id)
            deduped.append(media_id)

        if not deduped:
            raise ValueError("Debes enviar al menos una imagen.")

        return deduped


class GalleryImageOut(BaseModel):
    media_id: int
    url: str
    media_kind: str
    created_at: datetime
    original_filename: str | None = None


class GalleryFolderSummaryOut(BaseModel):
    id: int
    name: str
    visibility: GalleryVisibility = "public"
    is_published: bool = False
    published_at: datetime | None = None
    images_count: int
    cover_image_url: str | None = None
    created_at: datetime
    updated_at: datetime


class GalleryFolderDetailOut(BaseModel):
    id: int
    name: str
    visibility: GalleryVisibility = "public"
    is_published: bool = False
    published_at: datetime | None = None
    images_count: int
    cover_image_url: str | None = None
    created_at: datetime
    updated_at: datetime
    images: list[GalleryImageOut] = Field(default_factory=list)
    expires_in: int


class GalleryMineOut(BaseModel):
    recent_limit: int
    recent_images: list[GalleryImageOut] = Field(default_factory=list)
    folders: list[GalleryFolderSummaryOut] = Field(default_factory=list)
    expires_in: int


class GalleryOperationStatusOut(BaseModel):
    deleted: bool = True


class GalleryAlbumPublishInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    visibility: GalleryVisibility = "public"
    media_ids: list[int] = Field(..., min_length=1, max_length=200)

    @field_validator("name")
    @classmethod
    def validate_album_name(cls, value: str) -> str:
        normalized = _normalize_folder_name(value)
        if not normalized:
            raise ValueError("Debes escribir el nombre del álbum.")
        return normalized

    @field_validator("visibility")
    @classmethod
    def validate_album_visibility(cls, value: str) -> str:
        normalized = str(value or "").strip().lower()
        if normalized not in {"public", "private"}:
            raise ValueError("La visibilidad debe ser public o private.")
        return normalized

    @field_validator("media_ids")
    @classmethod
    def validate_album_media_ids(cls, values: list[int]) -> list[int]:
        deduped: list[int] = []
        seen: set[int] = set()

        for raw in values:
            media_id = int(raw or 0)
            if media_id <= 0:
                raise ValueError("Todos los media_ids deben ser mayores a 0.")
            if media_id in seen:
                continue
            seen.add(media_id)
            deduped.append(media_id)

        if not deduped:
            raise ValueError("Debes adjuntar al menos una imagen o video.")

        return deduped


class GalleryAlbumPublishedPostOut(BaseModel):
    post_id: int
    media_id: int
    media_kind: str
    media_url: str | None = None


class GalleryAlbumPublishOut(BaseModel):
    album: GalleryFolderDetailOut
    posts: list[GalleryAlbumPublishedPostOut] = Field(default_factory=list)
