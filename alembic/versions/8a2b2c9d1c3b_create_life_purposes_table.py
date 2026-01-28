"""create life_purposes table

Revision ID: 8a2b2c9d1c3b
Revises: 356acc72ad15
Create Date: 2026-01-08 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8a2b2c9d1c3b"
down_revision: Union[str, Sequence[str], None] = "356acc72ad15"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "life_purposes",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("slot_number", sa.Integer(), nullable=False),
        sa.Column("is_private", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("reveal_at", sa.Date(), nullable=True),
        sa.Column("text_public", sa.String(length=500), nullable=True),
        sa.Column("ciphertext", sa.LargeBinary(), nullable=True),
        sa.Column("nonce", sa.LargeBinary(), nullable=True),
        sa.Column("icon_key", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "slot_number", name="uq_life_purpose_user_slot"),
    )


def downgrade() -> None:
    op.drop_table("life_purposes")
