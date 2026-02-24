"""create notification_reads table

Revision ID: e7b1c2d3f4a5
Revises: e1f7c9a4b2d5
Create Date: 2026-02-24 11:20:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e7b1c2d3f4a5"
down_revision: Union[str, Sequence[str], None] = "e1f7c9a4b2d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notification_reads",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("notification_id", sa.String(length=120), nullable=False),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "notification_id", name="uq_notification_reads_user_notification"),
    )

    op.create_index("ix_notification_reads_id", "notification_reads", ["id"], unique=False)
    op.create_index("ix_notification_reads_user_id", "notification_reads", ["user_id"], unique=False)
    op.create_index("ix_notification_reads_notification_id", "notification_reads", ["notification_id"], unique=False)
    op.create_index("ix_notification_reads_read_at", "notification_reads", ["read_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_notification_reads_read_at", table_name="notification_reads")
    op.drop_index("ix_notification_reads_notification_id", table_name="notification_reads")
    op.drop_index("ix_notification_reads_user_id", table_name="notification_reads")
    op.drop_index("ix_notification_reads_id", table_name="notification_reads")
    op.drop_table("notification_reads")
