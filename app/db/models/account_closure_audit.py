from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AccountClosureReason(str, Enum):
    no_support = "no_support"
    prefer_private_space = "prefer_private_space"
    personal_pause = "personal_pause"
    misaligned_platform = "misaligned_platform"
    goals_reached = "goals_reached"
    other = "other"


class AccountClosureRestoreMethod(str, Enum):
    login = "login"
    password_reset = "password_reset"
    manual = "manual"


class AccountClosureAudit(Base):
    __tablename__ = "account_closure_audits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    user_email_snapshot: Mapped[str] = mapped_column(String(255), nullable=False)
    user_username_snapshot: Mapped[str | None] = mapped_column(String(30), nullable=True)

    reason: Mapped[AccountClosureReason] = mapped_column(
        SAEnum(AccountClosureReason, name="account_closure_reason"),
        nullable=False,
        index=True,
    )
    other_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    restore_deadline_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    restored_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )
    restore_method: Mapped[AccountClosureRestoreMethod | None] = mapped_column(
        SAEnum(AccountClosureRestoreMethod, name="account_closure_restore_method"),
        nullable=True,
    )
    purged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
