from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class GuardianWishMessageKind(str, Enum):
    denial = "denial"
    owner_contact = "owner_contact"


class GuardianWishMessage(Base):
    __tablename__ = "guardian_wish_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    wish_request_id: Mapped[int] = mapped_column(
        ForeignKey("guardian_wish_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    sender_guardian_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    recipient_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    kind: Mapped[GuardianWishMessageKind] = mapped_column(
        SAEnum(GuardianWishMessageKind, name="guardian_wish_message_kind"),
        nullable=False,
        index=True,
    )

    subject: Mapped[str] = mapped_column(String(180), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
