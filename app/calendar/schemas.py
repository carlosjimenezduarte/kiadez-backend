from __future__ import annotations

from datetime import date

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
