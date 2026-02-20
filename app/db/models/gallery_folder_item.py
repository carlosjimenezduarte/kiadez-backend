from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class GalleryFolderItem(Base):
    __tablename__ = "gallery_folder_items"
    __table_args__ = (
        UniqueConstraint(
            "folder_id",
            "media_id",
            name="uq_gallery_folder_items_folder_media",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    folder_id: Mapped[int] = mapped_column(
        ForeignKey("gallery_folders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    media_id: Mapped[int] = mapped_column(
        ForeignKey("media.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
