"""add account closure audit and restore window fields

Revision ID: c6e9a2b4d1f7
Revises: f2c4b6a8d1e3
Create Date: 2026-02-20 19:10:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "c6e9a2b4d1f7"
down_revision: Union[str, Sequence[str], None] = "f2c4b6a8d1e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    account_closure_reason = postgresql.ENUM(
        "no_support",
        "prefer_private_space",
        "personal_pause",
        "misaligned_platform",
        "goals_reached",
        "other",
        name="account_closure_reason",
        create_type=False,
    )
    account_closure_restore_method = postgresql.ENUM(
        "login",
        "password_reset",
        "manual",
        name="account_closure_restore_method",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE account_closure_reason AS ENUM ("
        "'no_support', 'prefer_private_space', 'personal_pause', 'misaligned_platform', 'goals_reached', 'other'"
        "); EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )
    op.execute(
        "DO $$ BEGIN CREATE TYPE account_closure_restore_method AS ENUM ('login', 'password_reset', 'manual'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.add_column("users", sa.Column("account_closure_requested_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("account_closure_restore_deadline_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index(
        "ix_users_account_closure_requested_at",
        "users",
        ["account_closure_requested_at"],
        unique=False,
    )
    op.create_index(
        "ix_users_account_closure_restore_deadline_at",
        "users",
        ["account_closure_restore_deadline_at"],
        unique=False,
    )

    op.create_table(
        "account_closure_audits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("user_email_snapshot", sa.String(length=255), nullable=False),
        sa.Column("user_username_snapshot", sa.String(length=30), nullable=True),
        sa.Column("reason", account_closure_reason, nullable=False),
        sa.Column("other_reason", sa.Text(), nullable=True),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("restore_deadline_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("restored_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("restore_method", account_closure_restore_method, nullable=True),
        sa.Column("purged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_account_closure_audits_id", "account_closure_audits", ["id"], unique=False)
    op.create_index("ix_account_closure_audits_user_id", "account_closure_audits", ["user_id"], unique=False)
    op.create_index("ix_account_closure_audits_reason", "account_closure_audits", ["reason"], unique=False)
    op.create_index(
        "ix_account_closure_audits_requested_at",
        "account_closure_audits",
        ["requested_at"],
        unique=False,
    )
    op.create_index(
        "ix_account_closure_audits_restore_deadline_at",
        "account_closure_audits",
        ["restore_deadline_at"],
        unique=False,
    )
    op.create_index(
        "ix_account_closure_audits_restored_at",
        "account_closure_audits",
        ["restored_at"],
        unique=False,
    )
    op.create_index("ix_account_closure_audits_purged_at", "account_closure_audits", ["purged_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_account_closure_audits_purged_at", table_name="account_closure_audits")
    op.drop_index("ix_account_closure_audits_restored_at", table_name="account_closure_audits")
    op.drop_index("ix_account_closure_audits_restore_deadline_at", table_name="account_closure_audits")
    op.drop_index("ix_account_closure_audits_requested_at", table_name="account_closure_audits")
    op.drop_index("ix_account_closure_audits_reason", table_name="account_closure_audits")
    op.drop_index("ix_account_closure_audits_user_id", table_name="account_closure_audits")
    op.drop_index("ix_account_closure_audits_id", table_name="account_closure_audits")
    op.drop_table("account_closure_audits")

    op.drop_index("ix_users_account_closure_restore_deadline_at", table_name="users")
    op.drop_index("ix_users_account_closure_requested_at", table_name="users")
    op.drop_column("users", "account_closure_restore_deadline_at")
    op.drop_column("users", "account_closure_requested_at")

    op.execute("DROP TYPE IF EXISTS account_closure_restore_method")
    op.execute("DROP TYPE IF EXISTS account_closure_reason")
