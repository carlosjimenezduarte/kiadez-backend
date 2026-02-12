"""create public personal wishes table

Revision ID: c9f4a6e2b1d7
Revises: f5c1d2e3a4b6
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "c9f4a6e2b1d7"
down_revision: Union[str, Sequence[str], None] = "f5c1d2e3a4b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    status_enum = postgresql.ENUM(
        "active",
        "fulfilled",
        name="public_personal_wish_status",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE public_personal_wish_status AS ENUM ('active', 'fulfilled'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "public_personal_wishes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("wish_text", sa.Text(), nullable=False),
        sa.Column("wish_type", sa.String(length=40), nullable=False),
        sa.Column("media_id", sa.Integer(), sa.ForeignKey("media.id", ondelete="SET NULL"), nullable=True),
        sa.Column(
            "fulfilled_evidence_media_id",
            sa.Integer(),
            sa.ForeignKey("media.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("status", status_enum, nullable=False, server_default=sa.text("'active'")),
        sa.Column("fulfilled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index("ix_public_personal_wishes_id", "public_personal_wishes", ["id"], unique=False)
    op.create_index("ix_public_personal_wishes_user_id", "public_personal_wishes", ["user_id"], unique=False)
    op.create_index("ix_public_personal_wishes_media_id", "public_personal_wishes", ["media_id"], unique=False)
    op.create_index(
        "ix_public_personal_wishes_fulfilled_evidence_media_id",
        "public_personal_wishes",
        ["fulfilled_evidence_media_id"],
        unique=False,
    )
    op.create_index("ix_public_personal_wishes_status", "public_personal_wishes", ["status"], unique=False)
    op.create_index("ix_public_personal_wishes_fulfilled_at", "public_personal_wishes", ["fulfilled_at"], unique=False)
    op.create_index("ix_public_personal_wishes_created_at", "public_personal_wishes", ["created_at"], unique=False)

    op.execute("ALTER TABLE public_personal_wishes ALTER COLUMN status DROP DEFAULT")


def downgrade() -> None:
    op.drop_index("ix_public_personal_wishes_created_at", table_name="public_personal_wishes")
    op.drop_index("ix_public_personal_wishes_fulfilled_at", table_name="public_personal_wishes")
    op.drop_index("ix_public_personal_wishes_status", table_name="public_personal_wishes")
    op.drop_index("ix_public_personal_wishes_fulfilled_evidence_media_id", table_name="public_personal_wishes")
    op.drop_index("ix_public_personal_wishes_media_id", table_name="public_personal_wishes")
    op.drop_index("ix_public_personal_wishes_user_id", table_name="public_personal_wishes")
    op.drop_index("ix_public_personal_wishes_id", table_name="public_personal_wishes")
    op.drop_table("public_personal_wishes")

    op.execute("DROP TYPE IF EXISTS public_personal_wish_status")
