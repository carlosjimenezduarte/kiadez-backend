"""create biography about table

Revision ID: d4e8f1b3c7a9
Revises: b1a4d3e7c9f2
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d4e8f1b3c7a9"
down_revision: Union[str, Sequence[str], None] = "b1a4d3e7c9f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "biography_about",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("display_name", sa.String(length=200), nullable=True),
        sa.Column("about_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_biography_about_user_id"),
    )
    op.create_index("ix_biography_about_id", "biography_about", ["id"], unique=False)
    op.create_index("ix_biography_about_user_id", "biography_about", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_biography_about_user_id", table_name="biography_about")
    op.drop_index("ix_biography_about_id", table_name="biography_about")
    op.drop_table("biography_about")

