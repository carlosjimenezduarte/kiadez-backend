from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class PublicCooperativeWishParticipation(Base):
    __tablename__ = "public_cooperative_wish_participations"
    __table_args__ = (
        UniqueConstraint(
            "wish_id",
            "participant_user_id",
            name="uq_public_coop_wish_participant",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    wish_id: Mapped[int] = mapped_column(
        ForeignKey("public_cooperative_wishes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    participant_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    participation_text: Mapped[str] = mapped_column(Text, nullable=False)

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
