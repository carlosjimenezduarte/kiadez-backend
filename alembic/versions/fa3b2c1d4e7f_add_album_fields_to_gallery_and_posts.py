"""add album fields to gallery and posts

Revision ID: fa3b2c1d4e7f
Revises: c3b8f4a1d2e9
Create Date: 2026-02-19 18:20:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fa3b2c1d4e7f"
down_revision: Union[str, Sequence[str], None] = "c3b8f4a1d2e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "gallery_folders",
        sa.Column("visibility", sa.String(length=10), nullable=False, server_default="public"),
    )
    op.add_column(
        "gallery_folders",
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.alter_column("gallery_folders", "visibility", server_default=None)

    op.add_column("posts", sa.Column("album_id", sa.Integer(), nullable=True))
    op.create_index("ix_posts_album_id", "posts", ["album_id"], unique=False)
    op.create_foreign_key(
        "fk_posts_album_id_gallery_folders",
        "posts",
        "gallery_folders",
        ["album_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_posts_album_id_gallery_folders", "posts", type_="foreignkey")
    op.drop_index("ix_posts_album_id", table_name="posts")
    op.drop_column("posts", "album_id")

    op.drop_column("gallery_folders", "published_at")
    op.drop_column("gallery_folders", "visibility")
