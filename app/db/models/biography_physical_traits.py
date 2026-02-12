from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class BiographyPhysicalTraits(Base):
    __tablename__ = "biography_physical_traits"
    __table_args__ = (UniqueConstraint("user_id", name="uq_biography_physical_traits_user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    height: Mapped[str | None] = mapped_column(String(40), nullable=True)
    weight: Mapped[str | None] = mapped_column(String(40), nullable=True)
    eyes: Mapped[str | None] = mapped_column(String(80), nullable=True)
    hair: Mapped[str | None] = mapped_column(String(80), nullable=True)

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

