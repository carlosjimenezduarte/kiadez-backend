"""add public profile visibility flags

Revision ID: db18e7ec7a66
Revises: a7f4c1e9d2b6
Create Date: 2026-02-17 18:07:46.888401

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db18e7ec7a66'
down_revision: Union[str, Sequence[str], None] = 'a7f4c1e9d2b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_public_wishes",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_fulfilled_wishes",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_calendar",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "public_profile_show_oracle",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "public_profile_show_oracle")
    op.drop_column("users", "public_profile_show_calendar")
    op.drop_column("users", "public_profile_show_fulfilled_wishes")
    op.drop_column("users", "public_profile_show_public_wishes")
