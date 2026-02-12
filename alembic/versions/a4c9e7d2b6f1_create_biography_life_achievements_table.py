"""create biography life achievements table

Revision ID: a4c9e7d2b6f1
Revises: c2d4e6f8a1b3
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a4c9e7d2b6f1"
down_revision: Union[str, Sequence[str], None] = "c2d4e6f8a1b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "biography_life_achievements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("section_title", sa.String(length=200), nullable=True),
        sa.Column("section_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_biography_life_ach_user_id"),
    )
    op.create_index("ix_biography_life_achievements_id", "biography_life_achievements", ["id"], unique=False)
    op.create_index("ix_biography_life_achievements_user_id", "biography_life_achievements", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_biography_life_achievements_user_id", table_name="biography_life_achievements")
    op.drop_index("ix_biography_life_achievements_id", table_name="biography_life_achievements")
    op.drop_table("biography_life_achievements")
