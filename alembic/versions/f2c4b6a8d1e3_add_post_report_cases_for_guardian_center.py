"""add post report cases for guardian center moderation

Revision ID: f2c4b6a8d1e3
Revises: e3d1f4a9b7c2
Create Date: 2026-02-20 18:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "f2c4b6a8d1e3"
down_revision: Union[str, Sequence[str], None] = "e3d1f4a9b7c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    post_report_case_status = postgresql.ENUM(
        "open",
        "kept",
        "deleted",
        name="post_report_case_status",
        create_type=False,
    )
    post_media_kind = postgresql.ENUM(
        "image",
        "video",
        name="post_media_kind",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE post_report_case_status AS ENUM ('open', 'kept', 'deleted'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "post_report_cases",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="SET NULL"), nullable=True),
        sa.Column("post_author_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("post_text_snapshot", sa.Text(), nullable=True),
        sa.Column(
            "post_media_id_snapshot",
            sa.Integer(),
            sa.ForeignKey("media.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("post_media_kind_snapshot", post_media_kind, nullable=True),
        sa.Column(
            "status",
            post_report_case_status,
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
        sa.UniqueConstraint("post_id", name="uq_post_report_cases_post"),
    )

    op.create_index("ix_post_report_cases_id", "post_report_cases", ["id"], unique=False)
    op.create_index("ix_post_report_cases_post_id", "post_report_cases", ["post_id"], unique=False)
    op.create_index("ix_post_report_cases_post_author_id", "post_report_cases", ["post_author_id"], unique=False)
    op.create_index(
        "ix_post_report_cases_post_media_id_snapshot",
        "post_report_cases",
        ["post_media_id_snapshot"],
        unique=False,
    )
    op.create_index("ix_post_report_cases_status", "post_report_cases", ["status"], unique=False)
    op.create_index("ix_post_report_cases_first_reported_at", "post_report_cases", ["first_reported_at"], unique=False)
    op.create_index("ix_post_report_cases_last_reported_at", "post_report_cases", ["last_reported_at"], unique=False)
    op.create_index("ix_post_report_cases_resolved_at", "post_report_cases", ["resolved_at"], unique=False)
    op.create_index(
        "ix_post_report_cases_resolved_by_guardian_id",
        "post_report_cases",
        ["resolved_by_guardian_id"],
        unique=False,
    )

    op.add_column("post_reports", sa.Column("case_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_post_reports_case_id_post_report_cases",
        "post_reports",
        "post_report_cases",
        ["case_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index("ix_post_reports_case_id", "post_reports", ["case_id"], unique=False)

    # Backfill existing reports into cases so historical moderation starts with current data.
    op.execute(
        """
        INSERT INTO post_report_cases (
            post_id,
            post_author_id,
            post_text_snapshot,
            post_media_id_snapshot,
            post_media_kind_snapshot,
            status,
            report_count,
            first_reported_at,
            last_reported_at,
            created_at,
            updated_at
        )
        SELECT
            p.id,
            p.author_id,
            p.text,
            p.media_id,
            p.media_kind,
            'open'::post_report_case_status,
            COUNT(pr.id) AS report_count,
            MIN(pr.created_at) AS first_reported_at,
            MAX(pr.created_at) AS last_reported_at,
            NOW(),
            NOW()
        FROM post_reports pr
        JOIN posts p ON p.id = pr.post_id
        GROUP BY p.id, p.author_id, p.text, p.media_id, p.media_kind
        """
    )

    op.execute(
        """
        UPDATE post_reports pr
        SET case_id = c.id
        FROM post_report_cases c
        WHERE c.post_id = pr.post_id
        """
    )

    op.alter_column("post_reports", "case_id", existing_type=sa.Integer(), nullable=False)
    op.alter_column("post_reports", "post_id", existing_type=sa.Integer(), nullable=True)

    op.create_unique_constraint(
        "uq_post_reports_case_reporter",
        "post_reports",
        ["case_id", "reporter_id"],
    )

    op.alter_column("post_report_cases", "status", server_default=None)
    op.alter_column("post_report_cases", "report_count", server_default=None)


def downgrade() -> None:
    op.drop_constraint("uq_post_reports_case_reporter", "post_reports", type_="unique")

    # Remove report rows detached from posts before restoring NOT NULL constraint.
    op.execute("DELETE FROM post_reports WHERE post_id IS NULL")

    op.alter_column("post_reports", "post_id", existing_type=sa.Integer(), nullable=False)
    op.alter_column("post_reports", "case_id", existing_type=sa.Integer(), nullable=True)

    op.drop_index("ix_post_reports_case_id", table_name="post_reports")
    op.drop_constraint("fk_post_reports_case_id_post_report_cases", "post_reports", type_="foreignkey")
    op.drop_column("post_reports", "case_id")

    op.drop_index(
        "ix_post_report_cases_resolved_by_guardian_id",
        table_name="post_report_cases",
    )
    op.drop_index("ix_post_report_cases_resolved_at", table_name="post_report_cases")
    op.drop_index("ix_post_report_cases_last_reported_at", table_name="post_report_cases")
    op.drop_index("ix_post_report_cases_first_reported_at", table_name="post_report_cases")
    op.drop_index("ix_post_report_cases_status", table_name="post_report_cases")
    op.drop_index(
        "ix_post_report_cases_post_media_id_snapshot",
        table_name="post_report_cases",
    )
    op.drop_index("ix_post_report_cases_post_author_id", table_name="post_report_cases")
    op.drop_index("ix_post_report_cases_post_id", table_name="post_report_cases")
    op.drop_index("ix_post_report_cases_id", table_name="post_report_cases")
    op.drop_table("post_report_cases")

    op.execute("DROP TYPE IF EXISTS post_report_case_status")
