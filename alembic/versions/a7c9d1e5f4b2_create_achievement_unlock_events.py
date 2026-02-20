"""create achievement unlock events

Revision ID: a7c9d1e5f4b2
Revises: f9a1d6c4b2e8
Create Date: 2026-02-19 13:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a7c9d1e5f4b2"
down_revision: Union[str, Sequence[str], None] = "f9a1d6c4b2e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "achievement_unlock_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("achievement_key", sa.String(length=80), nullable=False),
        sa.Column("category", sa.String(length=40), nullable=False),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=False),
        sa.Column("image_url", sa.String(length=255), nullable=False),
        sa.Column("unlocked_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "achievement_key", name="uq_achievement_unlock_user_key"),
    )
    op.create_index(
        op.f("ix_achievement_unlock_events_id"),
        "achievement_unlock_events",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_achievement_unlock_events_user_id"),
        "achievement_unlock_events",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_achievement_unlock_events_achievement_key"),
        "achievement_unlock_events",
        ["achievement_key"],
        unique=False,
    )
    op.create_index(
        op.f("ix_achievement_unlock_events_category"),
        "achievement_unlock_events",
        ["category"],
        unique=False,
    )
    op.create_index(
        op.f("ix_achievement_unlock_events_unlocked_at"),
        "achievement_unlock_events",
        ["unlocked_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_achievement_unlock_events_unlocked_at"), table_name="achievement_unlock_events")
    op.drop_index(op.f("ix_achievement_unlock_events_category"), table_name="achievement_unlock_events")
    op.drop_index(op.f("ix_achievement_unlock_events_achievement_key"), table_name="achievement_unlock_events")
    op.drop_index(op.f("ix_achievement_unlock_events_user_id"), table_name="achievement_unlock_events")
    op.drop_index(op.f("ix_achievement_unlock_events_id"), table_name="achievement_unlock_events")
    op.drop_table("achievement_unlock_events")
