"""add cover photo fields to users

Revision ID: b9e8f1a2c3d4
Revises: f6d2a4c8b1e9
Create Date: 2026-02-24 18:30:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b9e8f1a2c3d4"
down_revision: Union[str, Sequence[str], None] = "f6d2a4c8b1e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("cover_photo_media_id", sa.Integer(), nullable=True))
    op.add_column(
        "users",
        sa.Column("cover_photo_offset_x", sa.Integer(), nullable=False, server_default=sa.text("0")),
    )
    op.add_column(
        "users",
        sa.Column("cover_photo_offset_y", sa.Integer(), nullable=False, server_default=sa.text("0")),
    )

    op.create_index("ix_users_cover_photo_media_id", "users", ["cover_photo_media_id"], unique=False)
    op.create_foreign_key(
        "fk_users_cover_photo_media_id_media",
        "users",
        "media",
        ["cover_photo_media_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.alter_column("users", "cover_photo_offset_x", server_default=None)
    op.alter_column("users", "cover_photo_offset_y", server_default=None)


def downgrade() -> None:
    op.drop_constraint("fk_users_cover_photo_media_id_media", "users", type_="foreignkey")
    op.drop_index("ix_users_cover_photo_media_id", table_name="users")
    op.drop_column("users", "cover_photo_offset_y")
    op.drop_column("users", "cover_photo_offset_x")
    op.drop_column("users", "cover_photo_media_id")
