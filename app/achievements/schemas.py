from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AchievementBadgeOut(BaseModel):
    key: str
    title: str
    threshold: int
    image_url: str
    unlocked: bool


class AchievementsTotalsOut(BaseModel):
    publication_stars_total: int
    donation_stars_total: int
    fulfilled_wishes_total: int
    granted_wishes_total: int
    calendar_streak_days: int
    guardian_rank_current: int


class AchievementsStateResponse(BaseModel):
    my_received_stars_total: int
    my_donated_stars_total: int
    my_donatable_stars_total: int
    totals: AchievementsTotalsOut
    publication_achievements: list[AchievementBadgeOut]
    fulfilled_wishes_achievements: list[AchievementBadgeOut]
    granted_wishes_achievements: list[AchievementBadgeOut]
    calendar_achievements: list[AchievementBadgeOut]
    donation_achievements: list[AchievementBadgeOut]
    guardian_rank_achievements: list[AchievementBadgeOut]


class WeeklyAchievementOut(BaseModel):
    achievement_key: str
    category: str
    title: str
    description: str
    image_url: str
    unlocked_at: datetime


class WeeklyAchievementsResponse(BaseModel):
    week_start_utc: datetime
    week_end_utc: datetime
    items: list[WeeklyAchievementOut]
