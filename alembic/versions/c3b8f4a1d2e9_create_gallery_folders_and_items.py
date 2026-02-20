"""create gallery folders and items

Revision ID: c3b8f4a1d2e9
Revises: a7c9d1e5f4b2
Create Date: 2026-02-19 16:25:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3b8f4a1d2e9"
down_revision: Union[str, Sequence[str], None] = "a7c9d1e5f4b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "gallery_folders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("owner_id", "name", name="uq_gallery_folders_owner_name"),
    )
    op.create_index("ix_gallery_folders_id", "gallery_folders", ["id"], unique=False)
    op.create_index("ix_gallery_folders_owner_id", "gallery_folders", ["owner_id"], unique=False)
    op.create_index("ix_gallery_folders_created_at", "gallery_folders", ["created_at"], unique=False)
    op.create_index("ix_gallery_folders_updated_at", "gallery_folders", ["updated_at"], unique=False)

    op.create_table(
        "gallery_folder_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("folder_id", sa.Integer(), nullable=False),
        sa.Column("media_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["folder_id"], ["gallery_folders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["media_id"], ["media.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "folder_id",
            "media_id",
            name="uq_gallery_folder_items_folder_media",
        ),
    )
    op.create_index("ix_gallery_folder_items_id", "gallery_folder_items", ["id"], unique=False)
    op.create_index("ix_gallery_folder_items_folder_id", "gallery_folder_items", ["folder_id"], unique=False)
    op.create_index("ix_gallery_folder_items_media_id", "gallery_folder_items", ["media_id"], unique=False)
    op.create_index("ix_gallery_folder_items_created_at", "gallery_folder_items", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_gallery_folder_items_created_at", table_name="gallery_folder_items")
    op.drop_index("ix_gallery_folder_items_media_id", table_name="gallery_folder_items")
    op.drop_index("ix_gallery_folder_items_folder_id", table_name="gallery_folder_items")
    op.drop_index("ix_gallery_folder_items_id", table_name="gallery_folder_items")
    op.drop_table("gallery_folder_items")

    op.drop_index("ix_gallery_folders_updated_at", table_name="gallery_folders")
    op.drop_index("ix_gallery_folders_created_at", table_name="gallery_folders")
    op.drop_index("ix_gallery_folders_owner_id", table_name="gallery_folders")
    op.drop_index("ix_gallery_folders_id", table_name="gallery_folders")
    op.drop_table("gallery_folders")
