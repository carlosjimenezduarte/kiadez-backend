from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Index, Integer, LargeBinary, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class OracleResponseType(str, Enum):
    public = "public"
    secret = "secret"
    heart = "heart"


class OracleUserState(Base):
    __tablename__ = "oracle_user_states"
    __table_args__ = (UniqueConstraint("user_id", name="uq_oracle_user_state_user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    cycle: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    cycle_started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    last_pick_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

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


class OracleResponse(Base):
    __tablename__ = "oracle_responses"
    __table_args__ = (
        Index("ix_oracle_responses_user_cycle", "user_id", "cycle"),
        Index("ix_oracle_responses_user_cycle_card", "user_id", "cycle", "card_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    card_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    cycle: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    response_type: Mapped[OracleResponseType] = mapped_column(
        SAEnum(OracleResponseType, name="oracle_response_type"),
        nullable=False,
        index=True,
    )

    # Public response content (plaintext), when response_type = public
    text_public: Mapped[str | None] = mapped_column(String(4000), nullable=True)

    # Secret response content (E2EE payload), when response_type = secret
    ciphertext: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    nonce: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)

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
