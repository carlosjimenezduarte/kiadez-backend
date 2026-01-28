from datetime import datetime, timezone
from sqlalchemy import Integer, DateTime, ForeignKey, LargeBinary, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class UserVault(Base):
    __tablename__ = "user_vaults"
    __table_args__ = (UniqueConstraint("user_id", name="uq_user_vault_user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # KDF params (versionables)
    kdf_name: Mapped[str] = mapped_column(String(20), default="pbkdf2_sha256", nullable=False)
    kdf_iters: Mapped[int] = mapped_column(Integer, default=310000, nullable=False)
    kdf_salt: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    # Wrapped DEK (AES-GCM)
    wrapped_dek_nonce: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    wrapped_dek: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", backref="vault")