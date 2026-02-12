"""add emblem media reference to users

Revision ID: b1a4d3e7c9f2
Revises: a8e5c2f1d4b9
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1a4d3e7c9f2"
down_revision: Union[str, Sequence[str], None] = "a8e5c2f1d4b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("emblem_media_id", sa.Integer(), nullable=True))
    op.create_index("ix_users_emblem_media_id", "users", ["emblem_media_id"], unique=False)
    op.create_foreign_key(
        "fk_users_emblem_media_id_media",
        "users",
        "media",
        ["emblem_media_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_users_emblem_media_id_media", "users", type_="foreignkey")
    op.drop_index("ix_users_emblem_media_id", table_name="users")
    op.drop_column("users", "emblem_media_id")

