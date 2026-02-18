from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class GuardianWishRequestStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


class GuardianWishRequest(Base):
    __tablename__ = "guardian_wish_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    requester_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Optional assignment to a specific Guardian (otherwise visible to the Guardian pool).
    guardian_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    wish_owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    public_wish_id: Mapped[int] = mapped_column(
        ForeignKey("public_personal_wishes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Snapshot to preserve context even if the wish text changes later.
    wish_text: Mapped[str] = mapped_column(Text, nullable=False)
    wish_type: Mapped[str] = mapped_column(String(40), nullable=False)

    reason: Mapped[str] = mapped_column(Text, nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(255), nullable=False)

    evidence_media_id: Mapped[int | None] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    status: Mapped[GuardianWishRequestStatus] = mapped_column(
        SAEnum(GuardianWishRequestStatus, name="guardian_wish_request_status"),
        nullable=False,
        default=GuardianWishRequestStatus.open,
        index=True,
    )
    commitment_code: Mapped[str | None] = mapped_column(String(32), nullable=True, unique=True, index=True)
    commitment_sealed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    denied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

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
