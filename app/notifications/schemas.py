from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


NotificationKind = Literal[
    "calendar",
    "oracle",
    "followers",
    "messages",
    "achievements",
    "mentions",
    "stars",
]


class NotificationItemOut(BaseModel):
    id: str
    kind: NotificationKind
    emoji: str
    title: str
    message: str
    created_at: datetime
    href: str | None = None
    is_read: bool = False


class NotificationFeedOut(BaseModel):
    items: list[NotificationItemOut] = Field(default_factory=list)
    total_count: int = Field(default=0, ge=0)
    unread_count: int = Field(default=0, ge=0)
    has_more: bool = False


class NotificationPreferencesOut(BaseModel):
    calendar_enabled: bool = True
    oracle_enabled: bool = True
    followers_enabled: bool = True
    messages_enabled: bool = True
    achievements_enabled: bool = True
    mentions_enabled: bool = True
    stars_enabled: bool = True


class NotificationPreferencesUpdateIn(BaseModel):
    calendar_enabled: bool | None = None
    oracle_enabled: bool | None = None
    followers_enabled: bool | None = None
    messages_enabled: bool | None = None
    achievements_enabled: bool | None = None
    mentions_enabled: bool | None = None
    stars_enabled: bool | None = None


class NotificationReadIn(BaseModel):
    notification_ids: list[str] = Field(default_factory=list, max_length=64)


class NotificationReadOut(BaseModel):
    marked: int = Field(default=0, ge=0)
