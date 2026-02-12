"""create biography favorite quotes table

Revision ID: f5c1d2e3a4b6
Revises: a4c9e7d2b6f1
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f5c1d2e3a4b6"
down_revision: Union[str, Sequence[str], None] = "a4c9e7d2b6f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "biography_favorite_quotes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("section_title", sa.String(length=200), nullable=True),
        sa.Column("section_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_biography_favorite_quotes_user_id"),
    )
    op.create_index("ix_biography_favorite_quotes_id", "biography_favorite_quotes", ["id"], unique=False)
    op.create_index("ix_biography_favorite_quotes_user_id", "biography_favorite_quotes", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_biography_favorite_quotes_user_id", table_name="biography_favorite_quotes")
    op.drop_index("ix_biography_favorite_quotes_id", table_name="biography_favorite_quotes")
    op.drop_table("biography_favorite_quotes")
