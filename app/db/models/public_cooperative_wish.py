from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class PublicCooperativeWish(Base):
    __tablename__ = "public_cooperative_wishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    wish_text: Mapped[str] = mapped_column(Text, nullable=False)
    wish_type: Mapped[str] = mapped_column(String(40), nullable=False)
    participants_goal: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    template_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    security_code: Mapped[str] = mapped_column(String(6), nullable=False)

    media_id: Mapped[int | None] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

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
