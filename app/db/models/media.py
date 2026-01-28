from enum import Enum
from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MediaVisibility(str, Enum):
    public = "public"
    private = "private"


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    visibility: Mapped[MediaVisibility] = mapped_column(
        SAEnum(MediaVisibility, name="media_visibility"),
        nullable=False,
        default=MediaVisibility.private,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
    )

    bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    object_key: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    original_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)

    mime_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    text: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)

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
