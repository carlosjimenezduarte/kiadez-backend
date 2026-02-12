"""create biography education table

Revision ID: b2c3a9d1e4f7
Revises: f1e7a4c2b9d0
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b2c3a9d1e4f7"
down_revision: Union[str, Sequence[str], None] = "f1e7a4c2b9d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "biography_education",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("slot1", sa.String(length=255), nullable=True),
        sa.Column("slot2", sa.String(length=255), nullable=True),
        sa.Column("slot3", sa.String(length=255), nullable=True),
        sa.Column("slot4", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_biography_education_user_id"),
    )
    op.create_index("ix_biography_education_id", "biography_education", ["id"], unique=False)
    op.create_index("ix_biography_education_user_id", "biography_education", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_biography_education_user_id", table_name="biography_education")
    op.drop_index("ix_biography_education_id", table_name="biography_education")
    op.drop_table("biography_education")

