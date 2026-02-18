from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class PublicWishFulfillmentAttributionMode(str, Enum):
    secret = "secret"
    public = "public"


class PublicWishFulfillment(Base):
    __tablename__ = "public_wish_fulfillments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    wish_id: Mapped[int] = mapped_column(
        ForeignKey("public_personal_wishes.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    wish_owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    fulfiller_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    guardian_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    wish_request_id: Mapped[int | None] = mapped_column(
        ForeignKey("guardian_wish_requests.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
        index=True,
    )
    commitment_code: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    attribution_mode: Mapped[PublicWishFulfillmentAttributionMode] = mapped_column(
        SAEnum(
            PublicWishFulfillmentAttributionMode,
            name="public_wish_fulfillment_attribution_mode",
        ),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
