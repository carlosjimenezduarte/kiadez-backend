from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class BiographyCuriosities(Base):
    __tablename__ = "biography_curiosities"
    __table_args__ = (UniqueConstraint("user_id", name="uq_biography_curiosities_user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    favorite_superhero: Mapped[str | None] = mapped_column(String(120), nullable=True)
    favorite_song: Mapped[str | None] = mapped_column(String(255), nullable=True)
    favorite_food: Mapped[str | None] = mapped_column(String(160), nullable=True)
    videogames: Mapped[str | None] = mapped_column(String(500), nullable=True)
    favorite_book: Mapped[str | None] = mapped_column(String(255), nullable=True)
    other_hobbies: Mapped[str | None] = mapped_column(String(500), nullable=True)
    motto: Mapped[str | None] = mapped_column(String(255), nullable=True)

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

