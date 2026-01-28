from datetime import datetime, date, timezone
from sqlalchemy import Integer, DateTime, ForeignKey, LargeBinary, Boolean, String, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class LifePurpose(Base):
    __tablename__ = "life_purposes"
    __table_args__ = (
        UniqueConstraint("user_id", "slot_number", name="uq_life_purpose_user_slot"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    slot_number: Mapped[int] = mapped_column(Integer, nullable=False)  # 1,2,3

    is_private: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)  # active|fulfilled

    # Revelación asistida (fecha programada)
    reveal_at: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Si público (o revelado):
    text_public: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Si privado:
    ciphertext: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    nonce: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)

    icon_key: Mapped[str | None] = mapped_column(String(20), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
