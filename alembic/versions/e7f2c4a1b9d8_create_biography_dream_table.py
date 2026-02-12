"""create biography dream table

Revision ID: e7f2c4a1b9d8
Revises: d4e8f1b3c7a9
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e7f2c4a1b9d8"
down_revision: Union[str, Sequence[str], None] = "d4e8f1b3c7a9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "biography_dream",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("dream_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_biography_dream_user_id"),
    )
    op.create_index("ix_biography_dream_id", "biography_dream", ["id"], unique=False)
    op.create_index("ix_biography_dream_user_id", "biography_dream", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_biography_dream_user_id", table_name="biography_dream")
    op.drop_index("ix_biography_dream_id", table_name="biography_dream")
    op.drop_table("biography_dream")
