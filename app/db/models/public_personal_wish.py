from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class PublicPersonalWishStatus(str, Enum):
    active = "active"
    fulfilled = "fulfilled"


class PublicPersonalWish(Base):
    __tablename__ = "public_personal_wishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    wish_text: Mapped[str] = mapped_column(Text, nullable=False)
    wish_type: Mapped[str] = mapped_column(String(40), nullable=False)

    # Optional metadata when a fulfilled wish originates from a Life Purpose slot.
    life_purpose_slot_number: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    life_purpose_icon_key: Mapped[str | None] = mapped_column(String(20), nullable=True)

    media_id: Mapped[int | None] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    fulfilled_evidence_media_id: Mapped[int | None] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    status: Mapped[PublicPersonalWishStatus] = mapped_column(
        SAEnum(PublicPersonalWishStatus, name="public_personal_wish_status"),
        nullable=False,
        default=PublicPersonalWishStatus.active,
        index=True,
    )
    fulfilled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
