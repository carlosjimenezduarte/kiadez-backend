"""create media table

Revision ID: 4f2a8c7d9b1e
Revises: 8a2b2c9d1c3b
Create Date: 2026-01-28 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "4f2a8c7d9b1e"
down_revision: Union[str, Sequence[str], None] = "8a2b2c9d1c3b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    visibility_enum = postgresql.ENUM(
        "public",
        "private",
        name="media_visibility",
        create_type=False,
    )
    visibility_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "media",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("visibility", visibility_enum, nullable=False, server_default="private"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("bucket", sa.String(length=255), nullable=False),
        sa.Column("object_key", sa.String(length=512), nullable=False, unique=True),
        sa.Column("original_filename", sa.String(length=255), nullable=True),
        sa.Column("mime_type", sa.String(length=255), nullable=True),
        sa.Column("size_bytes", sa.BigInteger(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.Column("text", sa.String(length=2000), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("media")
    visibility_enum = postgresql.ENUM(
        "public",
        "private",
        name="media_visibility",
        create_type=False,
    )
    visibility_enum.drop(op.get_bind(), checkfirst=True)
