from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.db.models.post import PostMediaKind, PostReportReason, PostVisibility


class PostCreateRequest(BaseModel):
    text: str | None = Field(default=None, max_length=2000)
    visibility: PostVisibility = PostVisibility.public
    media_id: int | None = Field(default=None, gt=0)
    media_kind: PostMediaKind | None = None

    @model_validator(mode="after")
    def validate_payload(self):
        text = (self.text or "").strip()
        if not text and self.media_id is None:
            raise ValueError("La publicación debe tener texto o media.")
        if self.media_id is None and self.media_kind is not None:
            raise ValueError("media_kind requiere media_id.")
        return self


class PostAuthorOut(BaseModel):
    id: int
    name: str
    role: str
    guardian_rank: int | None = None


class PostOut(BaseModel):
    id: int
    author: PostAuthorOut
    text: str | None = None
    visibility: PostVisibility
    media_id: int | None = None
    media_kind: PostMediaKind | None = None
    media_url: str | None = None
    album_id: int | None = None
    album_name: str | None = None
    star_count: int
    comment_count: int
    share_count: int
    starred_by_me: bool = False
    is_mine: bool = False
    created_at: datetime


class PostDeleteResponse(BaseModel):
    deleted: bool
    removed_stars: int


class PostStarResponse(BaseModel):
    starred: bool
    post_id: int
    star_count: int


class PostShareResponse(BaseModel):
    shared: bool
    post_id: int
    share_count: int


class PostCommentCreateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1200)


class PostCommentOut(BaseModel):
    id: int
    post_id: int
    author: PostAuthorOut
    text: str
    created_at: datetime


class PostReportCreateRequest(BaseModel):
    reason: PostReportReason
    other_reason: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_other_reason(self):
        if self.reason == PostReportReason.other and not (self.other_reason or "").strip():
            raise ValueError("Debes describir la otra razón del reporte.")
        if self.reason != PostReportReason.other:
            self.other_reason = None
        return self


class PostReportResponse(BaseModel):
    reported: bool
    post_id: int
    reason: PostReportReason


class MyPostStatsOut(BaseModel):
    my_received_stars_total: int
    my_posts_total: int


class StarAchievementOut(BaseModel):
    key: str
    title: str
    threshold: int
    image_url: str
    unlocked: bool


class StarPoolStateOut(BaseModel):
    my_received_stars_total: int
    my_donated_stars_total: int
    my_donatable_stars_total: int
    common_pool_stars_total: int
    unlocked_publication_achievements: int
    unlocked_donation_achievements: int
    publication_achievements: list[StarAchievementOut]
    donation_achievements: list[StarAchievementOut]


class StarPoolDonateResponse(BaseModel):
    donated_now: int
    state: StarPoolStateOut
