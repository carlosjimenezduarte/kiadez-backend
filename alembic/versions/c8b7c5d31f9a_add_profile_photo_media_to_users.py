"""add profile photo media reference to users

Revision ID: c8b7c5d31f9a
Revises: b7d4f0a9c2e1
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c8b7c5d31f9a"
down_revision: Union[str, Sequence[str], None] = "b7d4f0a9c2e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("profile_photo_media_id", sa.Integer(), nullable=True))
    op.create_index("ix_users_profile_photo_media_id", "users", ["profile_photo_media_id"], unique=False)
    op.create_foreign_key(
        "fk_users_profile_photo_media_id_media",
        "users",
        "media",
        ["profile_photo_media_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_users_profile_photo_media_id_media", "users", type_="foreignkey")
    op.drop_index("ix_users_profile_photo_media_id", table_name="users")
    op.drop_column("users", "profile_photo_media_id")
