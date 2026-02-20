# Python
from datetime import datetime, timezone, date

# SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    username: Mapped[str | None] = mapped_column(
        String(30),
        unique=True,
        nullable=True,
        index=True,
    )

    birth_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    gender: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="user",
    )

    guardian_rank: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    profile_photo_media_id: Mapped[int | None] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    emblem_media_id: Mapped[int | None] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    received_stars_total: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    donated_stars_total: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # Public profile visibility toggles (apply only to other viewers; owner can always access).
    public_profile_show_public_wishes: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_about: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_fulfilled_wishes: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_calendar: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_oracle: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_personal_posts: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    username_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    account_closure_requested_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )

    account_closure_restore_deadline_at: Mapped[datetime | None] = mapped_column(
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
