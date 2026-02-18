"""create guardian wish requests table

Revision ID: f0c8b3a1d2e7
Revises: db18e7ec7a66
Create Date: 2026-02-18 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "f0c8b3a1d2e7"
down_revision: Union[str, Sequence[str], None] = "db18e7ec7a66"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    status_enum = postgresql.ENUM(
        "open",
        "in_progress",
        "closed",
        name="guardian_wish_request_status",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE guardian_wish_request_status AS ENUM "
        "('open', 'in_progress', 'closed'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "guardian_wish_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("requester_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("guardian_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("wish_owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "public_wish_id",
            sa.Integer(),
            sa.ForeignKey("public_personal_wishes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("wish_text", sa.Text(), nullable=False),
        sa.Column("wish_type", sa.String(length=40), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("contact_phone", sa.String(length=50), nullable=False),
        sa.Column("contact_email", sa.String(length=255), nullable=False),
        sa.Column("evidence_media_id", sa.Integer(), sa.ForeignKey("media.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", status_enum, nullable=False, server_default=sa.text("'open'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index("ix_guardian_wish_requests_id", "guardian_wish_requests", ["id"], unique=False)
    op.create_index(
        "ix_guardian_wish_requests_requester_id",
        "guardian_wish_requests",
        ["requester_id"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_requests_guardian_id",
        "guardian_wish_requests",
        ["guardian_id"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_requests_wish_owner_id",
        "guardian_wish_requests",
        ["wish_owner_id"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_requests_public_wish_id",
        "guardian_wish_requests",
        ["public_wish_id"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_requests_evidence_media_id",
        "guardian_wish_requests",
        ["evidence_media_id"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_requests_status",
        "guardian_wish_requests",
        ["status"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_requests_created_at",
        "guardian_wish_requests",
        ["created_at"],
        unique=False,
    )

    op.execute("ALTER TABLE guardian_wish_requests ALTER COLUMN status DROP DEFAULT")


def downgrade() -> None:
    op.drop_index("ix_guardian_wish_requests_created_at", table_name="guardian_wish_requests")
    op.drop_index("ix_guardian_wish_requests_status", table_name="guardian_wish_requests")
    op.drop_index("ix_guardian_wish_requests_evidence_media_id", table_name="guardian_wish_requests")
    op.drop_index("ix_guardian_wish_requests_public_wish_id", table_name="guardian_wish_requests")
    op.drop_index("ix_guardian_wish_requests_wish_owner_id", table_name="guardian_wish_requests")
    op.drop_index("ix_guardian_wish_requests_guardian_id", table_name="guardian_wish_requests")
    op.drop_index("ix_guardian_wish_requests_requester_id", table_name="guardian_wish_requests")
    op.drop_index("ix_guardian_wish_requests_id", table_name="guardian_wish_requests")
    op.drop_table("guardian_wish_requests")

    op.execute("DROP TYPE IF EXISTS guardian_wish_request_status")

