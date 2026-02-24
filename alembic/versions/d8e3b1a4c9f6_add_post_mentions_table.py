"""add post mentions table

Revision ID: d8e3b1a4c9f6
Revises: c4e7b1a9d2f8
Create Date: 2026-02-24 09:20:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d8e3b1a4c9f6"
down_revision: Union[str, Sequence[str], None] = "c4e7b1a9d2f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "post_mentions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mentioned_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("start_index", sa.Integer(), nullable=False),
        sa.Column("end_index", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "post_id",
            "mentioned_user_id",
            "start_index",
            "end_index",
            name="uq_post_mentions_post_user_span",
        ),
        sa.CheckConstraint("start_index >= 0", name="ck_post_mentions_start_non_negative"),
        sa.CheckConstraint("end_index > start_index", name="ck_post_mentions_span_positive"),
    )

    op.create_index("ix_post_mentions_id", "post_mentions", ["id"], unique=False)
    op.create_index("ix_post_mentions_post_id", "post_mentions", ["post_id"], unique=False)
    op.create_index("ix_post_mentions_mentioned_user_id", "post_mentions", ["mentioned_user_id"], unique=False)
    op.create_index("ix_post_mentions_created_at", "post_mentions", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_post_mentions_created_at", table_name="post_mentions")
    op.drop_index("ix_post_mentions_mentioned_user_id", table_name="post_mentions")
    op.drop_index("ix_post_mentions_post_id", table_name="post_mentions")
    op.drop_index("ix_post_mentions_id", table_name="post_mentions")
    op.drop_table("post_mentions")
