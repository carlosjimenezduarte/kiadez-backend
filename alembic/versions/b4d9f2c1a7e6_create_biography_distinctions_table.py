"""create biography distinctions table

Revision ID: b4d9f2c1a7e6
Revises: fa3b2c1d4e7f
Create Date: 2026-02-19 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b4d9f2c1a7e6"
down_revision: Union[str, Sequence[str], None] = "fa3b2c1d4e7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "biography_distinctions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("slot1_type", sa.String(length=120), nullable=True),
        sa.Column("slot1_description", sa.String(length=500), nullable=True),
        sa.Column("slot2_type", sa.String(length=120), nullable=True),
        sa.Column("slot2_description", sa.String(length=500), nullable=True),
        sa.Column("slot3_type", sa.String(length=120), nullable=True),
        sa.Column("slot3_description", sa.String(length=500), nullable=True),
        sa.Column("slot4_type", sa.String(length=120), nullable=True),
        sa.Column("slot4_description", sa.String(length=500), nullable=True),
        sa.Column("slot5_type", sa.String(length=120), nullable=True),
        sa.Column("slot5_description", sa.String(length=500), nullable=True),
        sa.Column("slot6_type", sa.String(length=120), nullable=True),
        sa.Column("slot6_description", sa.String(length=500), nullable=True),
        sa.Column("slot7_type", sa.String(length=120), nullable=True),
        sa.Column("slot7_description", sa.String(length=500), nullable=True),
        sa.Column("slot8_type", sa.String(length=120), nullable=True),
        sa.Column("slot8_description", sa.String(length=500), nullable=True),
        sa.Column("slot9_type", sa.String(length=120), nullable=True),
        sa.Column("slot9_description", sa.String(length=500), nullable=True),
        sa.Column("slot10_type", sa.String(length=120), nullable=True),
        sa.Column("slot10_description", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_biography_distinctions_user_id"),
    )
    op.create_index("ix_biography_distinctions_id", "biography_distinctions", ["id"], unique=False)
    op.create_index("ix_biography_distinctions_user_id", "biography_distinctions", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_biography_distinctions_user_id", table_name="biography_distinctions")
    op.drop_index("ix_biography_distinctions_id", table_name="biography_distinctions")
    op.drop_table("biography_distinctions")
