"""create private personal wishes table

Revision ID: d2a1f3c4b5e6
Revises: c9f4a6e2b1d7
Create Date: 2026-02-13 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "d2a1f3c4b5e6"
down_revision: Union[str, Sequence[str], None] = "c9f4a6e2b1d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    status_enum = postgresql.ENUM(
        "active",
        "fulfilled",
        name="private_personal_wish_status",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE private_personal_wish_status AS ENUM ('active', 'fulfilled'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "private_personal_wishes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("ciphertext", sa.LargeBinary(), nullable=False),
        sa.Column("nonce", sa.LargeBinary(), nullable=False),
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

    op.create_index("ix_private_personal_wishes_id", "private_personal_wishes", ["id"], unique=False)
    op.create_index("ix_private_personal_wishes_user_id", "private_personal_wishes", ["user_id"], unique=False)
    op.create_index("ix_private_personal_wishes_media_id", "private_personal_wishes", ["media_id"], unique=False)
    op.create_index(
        "ix_private_personal_wishes_fulfilled_evidence_media_id",
        "private_personal_wishes",
        ["fulfilled_evidence_media_id"],
        unique=False,
    )
    op.create_index("ix_private_personal_wishes_status", "private_personal_wishes", ["status"], unique=False)
    op.create_index("ix_private_personal_wishes_fulfilled_at", "private_personal_wishes", ["fulfilled_at"], unique=False)
    op.create_index("ix_private_personal_wishes_created_at", "private_personal_wishes", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_private_personal_wishes_created_at", table_name="private_personal_wishes")
    op.drop_index("ix_private_personal_wishes_fulfilled_at", table_name="private_personal_wishes")
    op.drop_index("ix_private_personal_wishes_status", table_name="private_personal_wishes")
    op.drop_index("ix_private_personal_wishes_fulfilled_evidence_media_id", table_name="private_personal_wishes")
    op.drop_index("ix_private_personal_wishes_media_id", table_name="private_personal_wishes")
    op.drop_index("ix_private_personal_wishes_user_id", table_name="private_personal_wishes")
    op.drop_index("ix_private_personal_wishes_id", table_name="private_personal_wishes")
    op.drop_table("private_personal_wishes")
    op.execute("DROP TYPE IF EXISTS private_personal_wish_status;")

