"""create user follows table

Revision ID: a7f4c1e9d2b6
Revises: e2b9c1d4f7a8
Create Date: 2026-02-17 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a7f4c1e9d2b6"
down_revision: Union[str, Sequence[str], None] = "e2b9c1d4f7a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_follows",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("follower_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("followed_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("follower_id", "followed_id", name="uq_user_follows_follower_followed"),
        sa.CheckConstraint("follower_id <> followed_id", name="ck_user_follows_no_self_follow"),
    )

    op.create_index("ix_user_follows_id", "user_follows", ["id"], unique=False)
    op.create_index("ix_user_follows_follower_id", "user_follows", ["follower_id"], unique=False)
    op.create_index("ix_user_follows_followed_id", "user_follows", ["followed_id"], unique=False)
    op.create_index("ix_user_follows_created_at", "user_follows", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_user_follows_created_at", table_name="user_follows")
    op.drop_index("ix_user_follows_followed_id", table_name="user_follows")
    op.drop_index("ix_user_follows_follower_id", table_name="user_follows")
    op.drop_index("ix_user_follows_id", table_name="user_follows")
    op.drop_table("user_follows")
