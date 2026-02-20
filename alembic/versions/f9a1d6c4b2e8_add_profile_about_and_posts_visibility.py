"""add profile about and personal posts visibility flags

Revision ID: f9a1d6c4b2e8
Revises: e9b6f3c2d1a4
Create Date: 2026-02-19 10:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f9a1d6c4b2e8"
down_revision: Union[str, Sequence[str], None] = "e9b6f3c2d1a4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_about",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_personal_posts",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "public_profile_show_personal_posts")
    op.drop_column("users", "public_profile_show_about")
