from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class BiographyDistinctions(Base):
    __tablename__ = "biography_distinctions"
    __table_args__ = (UniqueConstraint("user_id", name="uq_biography_distinctions_user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    slot1_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    slot1_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    slot2_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    slot2_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    slot3_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    slot3_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    slot4_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    slot4_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    slot5_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    slot5_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    slot6_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    slot6_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    slot7_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    slot7_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    slot8_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    slot8_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    slot9_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    slot9_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    slot10_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    slot10_description: Mapped[str | None] = mapped_column(String(500), nullable=True)

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
