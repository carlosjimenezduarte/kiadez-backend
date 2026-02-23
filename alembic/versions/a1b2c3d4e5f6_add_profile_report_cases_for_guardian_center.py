"""add profile report cases for guardian center moderation

Revision ID: a1b2c3d4e5f6
Revises: c6e9a2b4d1f7
Create Date: 2026-02-23 15:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "c6e9a2b4d1f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    profile_report_reason = postgresql.ENUM(
        "fake_or_illegal",
        "external_manipulation",
        "star_manipulation",
        "abusive_or_coercive",
        "wish_system_abuse",
        "safety_risk",
        "other",
        name="profile_report_reason",
        create_type=False,
    )
    profile_report_case_status = postgresql.ENUM(
        "open",
        "reviewed",
        name="profile_report_case_status",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE profile_report_reason AS ENUM ("
        "'fake_or_illegal', 'external_manipulation', 'star_manipulation', "
        "'abusive_or_coercive', 'wish_system_abuse', 'safety_risk', 'other'"
        "); EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )
    op.execute(
        "DO $$ BEGIN CREATE TYPE profile_report_case_status AS ENUM ('open', 'reviewed'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "profile_report_cases",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("reported_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "status",
            profile_report_case_status,
            nullable=False,
            server_default=sa.text("'open'"),
        ),
        sa.Column("report_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("first_reported_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_reported_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "resolved_by_guardian_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("reported_user_id", name="uq_profile_report_cases_reported_user"),
    )

    op.create_index("ix_profile_report_cases_id", "profile_report_cases", ["id"], unique=False)
    op.create_index(
        "ix_profile_report_cases_reported_user_id",
        "profile_report_cases",
        ["reported_user_id"],
        unique=False,
    )
    op.create_index("ix_profile_report_cases_status", "profile_report_cases", ["status"], unique=False)
    op.create_index(
        "ix_profile_report_cases_first_reported_at",
        "profile_report_cases",
        ["first_reported_at"],
        unique=False,
    )
    op.create_index(
        "ix_profile_report_cases_last_reported_at",
        "profile_report_cases",
        ["last_reported_at"],
        unique=False,
    )
    op.create_index("ix_profile_report_cases_resolved_at", "profile_report_cases", ["resolved_at"], unique=False)
    op.create_index(
        "ix_profile_report_cases_resolved_by_guardian_id",
        "profile_report_cases",
        ["resolved_by_guardian_id"],
        unique=False,
    )

    op.create_table(
        "profile_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "case_id",
            sa.Integer(),
            sa.ForeignKey("profile_report_cases.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "reported_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "reporter_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("reason", profile_report_reason, nullable=False),
        sa.Column("other_reason", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("case_id", "reporter_id", name="uq_profile_reports_case_reporter"),
    )

    op.create_index("ix_profile_reports_id", "profile_reports", ["id"], unique=False)
    op.create_index("ix_profile_reports_case_id", "profile_reports", ["case_id"], unique=False)
    op.create_index(
        "ix_profile_reports_reported_user_id",
        "profile_reports",
        ["reported_user_id"],
        unique=False,
    )
    op.create_index("ix_profile_reports_reporter_id", "profile_reports", ["reporter_id"], unique=False)
    op.create_index("ix_profile_reports_created_at", "profile_reports", ["created_at"], unique=False)

    op.alter_column("profile_report_cases", "status", server_default=None)
    op.alter_column("profile_report_cases", "report_count", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_profile_reports_created_at", table_name="profile_reports")
    op.drop_index("ix_profile_reports_reporter_id", table_name="profile_reports")
    op.drop_index("ix_profile_reports_reported_user_id", table_name="profile_reports")
    op.drop_index("ix_profile_reports_case_id", table_name="profile_reports")
    op.drop_index("ix_profile_reports_id", table_name="profile_reports")
    op.drop_table("profile_reports")

    op.drop_index(
        "ix_profile_report_cases_resolved_by_guardian_id",
        table_name="profile_report_cases",
    )
    op.drop_index("ix_profile_report_cases_resolved_at", table_name="profile_report_cases")
    op.drop_index("ix_profile_report_cases_last_reported_at", table_name="profile_report_cases")
    op.drop_index("ix_profile_report_cases_first_reported_at", table_name="profile_report_cases")
    op.drop_index("ix_profile_report_cases_status", table_name="profile_report_cases")
    op.drop_index("ix_profile_report_cases_reported_user_id", table_name="profile_report_cases")
    op.drop_index("ix_profile_report_cases_id", table_name="profile_report_cases")
    op.drop_table("profile_report_cases")

    op.execute("DROP TYPE IF EXISTS profile_report_case_status")
    op.execute("DROP TYPE IF EXISTS profile_report_reason")
