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

    cover_photo_media_id: Mapped[int | None] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    cover_photo_offset_x: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    cover_photo_offset_y: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
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

    public_profile_show_cooperative_wishes: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_followers: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_gallery: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_recent_achievements: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_stars: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_cover_purposes: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    public_profile_show_biography: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    notif_calendar_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    notif_oracle_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    notif_followers_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    notif_messages_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    notif_achievements_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    notif_mentions_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    notif_stars_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    minor_accreditation_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="not_required",
    )

    minor_guardian_phone: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
    )

    minor_guardian_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    minor_guardian_relationship: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
    )

    minor_accreditation_requested_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    minor_accreditation_approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    minor_accreditation_token_hash: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )

    minor_accreditation_token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
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
