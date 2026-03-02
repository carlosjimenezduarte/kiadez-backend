from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from app.db.models.profile_report import ProfileReportReason


class FollowUserOut(BaseModel):
    user_id: int
    full_name: str
    username: str | None = None
    handle: str
    profile_url: str
    avatar_url: str | None = None
    role: str
    guardian_rank: int | None = None
    followers_count: int = 0
    received_stars_total: int = 0
    is_following: bool = False
    follows_me: bool = False


class FollowListResponse(BaseModel):
    items: list[FollowUserOut] = Field(default_factory=list)
    page: int = 1
    page_size: int = 25
    total: int = 0
    total_pages: int = 1
    range_start: int = 0
    range_end: int = 0


class FollowActionResponse(BaseModel):
    ok: bool = True
    target_user_id: int
    is_following: bool
    my_following_total: int
    target_followers_total: int


class ProfileReportCreateRequest(BaseModel):
    reason: ProfileReportReason
    other_reason: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_other_reason(self):
        if self.reason == ProfileReportReason.other and not (self.other_reason or "").strip():
            raise ValueError("You must describe the other report reason.")
        if self.reason != ProfileReportReason.other:
            self.other_reason = None
        return self


class ProfileReportResponse(BaseModel):
    reported: bool
    target_user_id: int
    reason: ProfileReportReason
