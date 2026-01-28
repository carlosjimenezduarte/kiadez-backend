from datetime import datetime, timezone
from sqlalchemy import Integer, DateTime, ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class PrivateDesire(Base):
    __tablename__ = "private_desires"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)  # active|fulfilled

    ciphertext: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    nonce: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
