"""create biography curiosities table

Revision ID: c6a2f8d9e7b1
Revises: b2c3a9d1e4f7
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c6a2f8d9e7b1"
down_revision: Union[str, Sequence[str], None] = "b2c3a9d1e4f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "biography_curiosities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("favorite_superhero", sa.String(length=120), nullable=True),
        sa.Column("favorite_song", sa.String(length=255), nullable=True),
        sa.Column("favorite_food", sa.String(length=160), nullable=True),
        sa.Column("videogames", sa.String(length=500), nullable=True),
        sa.Column("favorite_book", sa.String(length=255), nullable=True),
        sa.Column("other_hobbies", sa.String(length=500), nullable=True),
        sa.Column("motto", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_biography_curiosities_user_id"),
    )
    op.create_index("ix_biography_curiosities_id", "biography_curiosities", ["id"], unique=False)
    op.create_index("ix_biography_curiosities_user_id", "biography_curiosities", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_biography_curiosities_user_id", table_name="biography_curiosities")
    op.drop_index("ix_biography_curiosities_id", table_name="biography_curiosities")
    op.drop_table("biography_curiosities")

