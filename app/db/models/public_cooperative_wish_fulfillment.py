from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class PublicCooperativeWishFulfillment(Base):
    __tablename__ = "public_cooperative_wish_fulfillments"
    __table_args__ = (
        UniqueConstraint("wish_id", name="uq_public_coop_wish_fulfillment_wish"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    wish_id: Mapped[int] = mapped_column(
        ForeignKey("public_cooperative_wishes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    wish_owner_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    final_evidence_media_id: Mapped[int | None] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    oath_accepted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    fulfilled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
