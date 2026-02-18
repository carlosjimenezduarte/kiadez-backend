"""add public wish freeze flow

Revision ID: a91e5b73c8d4
Revises: f0c8b3a1d2e7
Create Date: 2026-02-18 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "a91e5b73c8d4"
down_revision: Union[str, Sequence[str], None] = "f0c8b3a1d2e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "public_personal_wishes",
        sa.Column("frozen_by_guardian_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
    )
    op.add_column(
        "public_personal_wishes",
        sa.Column("frozen_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_public_personal_wishes_frozen_by_guardian_id",
        "public_personal_wishes",
        ["frozen_by_guardian_id"],
        unique=False,
    )
    op.create_index(
        "ix_public_personal_wishes_frozen_at",
        "public_personal_wishes",
        ["frozen_at"],
        unique=False,
    )

    action_enum = postgresql.ENUM(
        "freeze",
        "unfreeze",
        name="public_wish_freeze_audit_action",
        create_type=False,
    )
    reason_enum = postgresql.ENUM(
        "error",
        "unexpected",
        name="public_wish_unfreeze_reason_type",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE public_wish_freeze_audit_action AS ENUM ('freeze', 'unfreeze'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )
    op.execute(
        "DO $$ BEGIN CREATE TYPE public_wish_unfreeze_reason_type AS ENUM ('error', 'unexpected'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "public_wish_freeze_audits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "wish_id",
            sa.Integer(),
            sa.ForeignKey("public_personal_wishes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "actor_guardian_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("action", action_enum, nullable=False),
        sa.Column("reason_type", reason_enum, nullable=True),
        sa.Column("reason_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_public_wish_freeze_audits_id", "public_wish_freeze_audits", ["id"], unique=False)
    op.create_index("ix_public_wish_freeze_audits_wish_id", "public_wish_freeze_audits", ["wish_id"], unique=False)
    op.create_index(
        "ix_public_wish_freeze_audits_actor_guardian_id",
        "public_wish_freeze_audits",
        ["actor_guardian_id"],
        unique=False,
    )
    op.create_index("ix_public_wish_freeze_audits_action", "public_wish_freeze_audits", ["action"], unique=False)
    op.create_index("ix_public_wish_freeze_audits_reason_type", "public_wish_freeze_audits", ["reason_type"], unique=False)
    op.create_index("ix_public_wish_freeze_audits_created_at", "public_wish_freeze_audits", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_public_wish_freeze_audits_created_at", table_name="public_wish_freeze_audits")
    op.drop_index("ix_public_wish_freeze_audits_reason_type", table_name="public_wish_freeze_audits")
    op.drop_index("ix_public_wish_freeze_audits_action", table_name="public_wish_freeze_audits")
    op.drop_index("ix_public_wish_freeze_audits_actor_guardian_id", table_name="public_wish_freeze_audits")
    op.drop_index("ix_public_wish_freeze_audits_wish_id", table_name="public_wish_freeze_audits")
    op.drop_index("ix_public_wish_freeze_audits_id", table_name="public_wish_freeze_audits")
    op.drop_table("public_wish_freeze_audits")

    op.execute("DROP TYPE IF EXISTS public_wish_unfreeze_reason_type")
    op.execute("DROP TYPE IF EXISTS public_wish_freeze_audit_action")

    op.drop_index("ix_public_personal_wishes_frozen_at", table_name="public_personal_wishes")
    op.drop_index("ix_public_personal_wishes_frozen_by_guardian_id", table_name="public_personal_wishes")
    op.drop_column("public_personal_wishes", "frozen_at")
    op.drop_column("public_personal_wishes", "frozen_by_guardian_id")

