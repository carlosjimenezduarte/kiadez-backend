from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class PublicWishFreezeAuditAction(str, Enum):
    freeze = "freeze"
    unfreeze = "unfreeze"


class PublicWishUnfreezeReasonType(str, Enum):
    error = "error"
    unexpected = "unexpected"


class PublicWishFreezeAudit(Base):
    __tablename__ = "public_wish_freeze_audits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    wish_id: Mapped[int] = mapped_column(
        ForeignKey("public_personal_wishes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    actor_guardian_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    action: Mapped[PublicWishFreezeAuditAction] = mapped_column(
        SAEnum(PublicWishFreezeAuditAction, name="public_wish_freeze_audit_action"),
        nullable=False,
        index=True,
    )

    reason_type: Mapped[PublicWishUnfreezeReasonType | None] = mapped_column(
        SAEnum(PublicWishUnfreezeReasonType, name="public_wish_unfreeze_reason_type"),
        nullable=True,
        index=True,
    )

    reason_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

