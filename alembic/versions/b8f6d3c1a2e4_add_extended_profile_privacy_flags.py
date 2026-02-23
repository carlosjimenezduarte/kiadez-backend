"""add extended public profile privacy flags

Revision ID: b8f6d3c1a2e4
Revises: a1b2c3d4e5f6
Create Date: 2026-02-23 16:20:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b8f6d3c1a2e4"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_cooperative_wishes",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_followers",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_gallery",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_recent_achievements",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_stars",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_cover_purposes",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_biography",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "public_profile_show_biography")
    op.drop_column("users", "public_profile_show_cover_purposes")
    op.drop_column("users", "public_profile_show_stars")
    op.drop_column("users", "public_profile_show_recent_achievements")
    op.drop_column("users", "public_profile_show_gallery")
    op.drop_column("users", "public_profile_show_followers")
    op.drop_column("users", "public_profile_show_cooperative_wishes")
