"""add notification preferences to users

Revision ID: e1f7c9a4b2d5
Revises: d8e3b1a4c9f6
Create Date: 2026-02-24 10:35:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e1f7c9a4b2d5"
down_revision: Union[str, Sequence[str], None] = "d8e3b1a4c9f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("notif_calendar_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "users",
        sa.Column("notif_oracle_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "users",
        sa.Column("notif_followers_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "users",
        sa.Column("notif_messages_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "users",
        sa.Column("notif_achievements_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "users",
        sa.Column("notif_mentions_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "users",
        sa.Column("notif_stars_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.alter_column("users", "notif_calendar_enabled", server_default=None)
    op.alter_column("users", "notif_oracle_enabled", server_default=None)
    op.alter_column("users", "notif_followers_enabled", server_default=None)
    op.alter_column("users", "notif_messages_enabled", server_default=None)
    op.alter_column("users", "notif_achievements_enabled", server_default=None)
    op.alter_column("users", "notif_mentions_enabled", server_default=None)
    op.alter_column("users", "notif_stars_enabled", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "notif_stars_enabled")
    op.drop_column("users", "notif_mentions_enabled")
    op.drop_column("users", "notif_achievements_enabled")
    op.drop_column("users", "notif_messages_enabled")
    op.drop_column("users", "notif_followers_enabled")
    op.drop_column("users", "notif_oracle_enabled")
    op.drop_column("users", "notif_calendar_enabled")
