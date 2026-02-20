from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ProfileReportReason(str, Enum):
    fake_or_illegal = "fake_or_illegal"
    external_manipulation = "external_manipulation"
    star_manipulation = "star_manipulation"
    abusive_or_coercive = "abusive_or_coercive"
    wish_system_abuse = "wish_system_abuse"
    safety_risk = "safety_risk"
    other = "other"


class ProfileReportCaseStatus(str, Enum):
    open = "open"
    reviewed = "reviewed"


class ProfileReportCase(Base):
    __tablename__ = "profile_report_cases"
    __table_args__ = (UniqueConstraint("reported_user_id", name="uq_profile_report_cases_reported_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reported_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[ProfileReportCaseStatus] = mapped_column(
        SAEnum(ProfileReportCaseStatus, name="profile_report_case_status"),
        nullable=False,
        default=ProfileReportCaseStatus.open,
        index=True,
    )
    report_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    first_reported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    last_reported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )
    resolved_by_guardian_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
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


class ProfileReport(Base):
    __tablename__ = "profile_reports"
    __table_args__ = (UniqueConstraint("case_id", "reporter_id", name="uq_profile_reports_case_reporter"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_id: Mapped[int] = mapped_column(
        ForeignKey("profile_report_cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reported_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reporter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reason: Mapped[ProfileReportReason] = mapped_column(
        SAEnum(ProfileReportReason, name="profile_report_reason"),
        nullable=False,
    )
    other_reason: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
