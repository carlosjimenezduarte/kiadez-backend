from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Boolean,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User2FA(Base):
    __tablename__ = "user_2fa"

    __table_args__ = (
        UniqueConstraint("user_id", name="uq_user_2fa_user"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    method: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="totp",
    )

    secret_encrypted: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user = relationship("User", backref="two_fa")
