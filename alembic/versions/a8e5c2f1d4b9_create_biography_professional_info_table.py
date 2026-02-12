"""create biography professional info table

Revision ID: a8e5c2f1d4b9
Revises: c6a2f8d9e7b1
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a8e5c2f1d4b9"
down_revision: Union[str, Sequence[str], None] = "c6a2f8d9e7b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "biography_professional_info",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("occupation", sa.String(length=500), nullable=True),
        sa.Column("active_years", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_biography_professional_info_user_id"),
    )
    op.create_index("ix_biography_professional_info_id", "biography_professional_info", ["id"], unique=False)
    op.create_index("ix_biography_professional_info_user_id", "biography_professional_info", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_biography_professional_info_user_id", table_name="biography_professional_info")
    op.drop_index("ix_biography_professional_info_id", table_name="biography_professional_info")
    op.drop_table("biography_professional_info")

