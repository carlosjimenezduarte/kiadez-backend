from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Text, UniqueConstraint
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
        Index("ix_pcwp_evidence_media_id", "evidence_media_id"),
        Index("ix_pcwp_evidence_submitted_at", "evidence_submitted_at"),
        Index("ix_pcwp_owner_validated_at", "owner_validated_at"),
        Index("ix_pcwp_owner_validated_by_uid", "owner_validated_by_user_id"),
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
    evidence_media_id: Mapped[int | None] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"),
        nullable=True,
    )
    evidence_submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    oath_accepted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    owner_validated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    owner_validated_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
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
