from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class BiographyPersonalInfo(Base):
    __tablename__ = "biography_personal_info"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_biography_personal_info_user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    birth_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    birth_city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    birth_region: Mapped[str | None] = mapped_column(String(120), nullable=True)
    birth_country: Mapped[str | None] = mapped_column(String(120), nullable=True)

    residence: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(120), nullable=True)
    native_language: Mapped[str | None] = mapped_column(String(120), nullable=True)
    pseudonyms: Mapped[str | None] = mapped_column(String(300), nullable=True)

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
