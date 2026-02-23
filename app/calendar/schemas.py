from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class CalendarDayActivityOut(BaseModel):
    date_utc: date
    stars_received: int = Field(default=0, ge=0)
    fulfilled_wishes: int = Field(default=0, ge=0)
    public_wishes: int = Field(default=0, ge=0)
    achievements: int = Field(default=0, ge=0)
    posts: int = Field(default=0, ge=0)
    total_interactions: int = Field(default=0, ge=0)
    has_activity: bool = False


class CalendarYearActivityOut(BaseModel):
    user_id: int
    year: int
    today_utc: date
    active_days_total: int = Field(default=0, ge=0)
    items: list[CalendarDayActivityOut]


class CalendarDaySummaryTotalsOut(BaseModel):
    stars_received: int = Field(default=0, ge=0)
    fulfilled_wishes: int = Field(default=0, ge=0)
    public_wishes: int = Field(default=0, ge=0)
    achievements: int = Field(default=0, ge=0)
    posts: int = Field(default=0, ge=0)
    total_interactions: int = Field(default=0, ge=0)


class CalendarDaySummaryPostOut(BaseModel):
    id: int
    text: str | None = None
    media_kind: str | None = None
    media_url: str | None = None
    star_count: int = Field(default=0, ge=0)
    comment_count: int = Field(default=0, ge=0)
    share_count: int = Field(default=0, ge=0)
    created_at: datetime


class CalendarDaySummaryWishOut(BaseModel):
    id: int
    wish_text: str
    wish_type: str | None = None
    evidence_media_kind: str | None = None
    evidence_media_url: str | None = None
    fulfilled_at: datetime


class CalendarDaySummaryAchievementOut(BaseModel):
    achievement_key: str
    category: str
    title: str
    description: str
    image_url: str
    unlocked_at: datetime


class CalendarDaySummaryOut(BaseModel):
    user_id: int
    date_utc: date
    available_from_utc: date
    is_day_closed: bool = False
    message: str | None = None
    totals: CalendarDaySummaryTotalsOut
    posts_items: list[CalendarDaySummaryPostOut]
    fulfilled_wishes_items: list[CalendarDaySummaryWishOut]
    achievements_items: list[CalendarDaySummaryAchievementOut]
