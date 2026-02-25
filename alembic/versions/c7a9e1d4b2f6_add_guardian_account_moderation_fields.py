"""add guardian account moderation fields

Revision ID: c7a9e1d4b2f6
Revises: b9e8f1a2c3d4
Create Date: 2026-02-25 18:05:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c7a9e1d4b2f6"
down_revision: Union[str, Sequence[str], None] = "b9e8f1a2c3d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "guardian_moderation_status",
            sa.String(length=32),
            nullable=False,
            server_default=sa.text("'active'"),
        ),
    )
    op.add_column("users", sa.Column("guardian_moderated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("guardian_moderated_by_user_id", sa.Integer(), nullable=True))

    op.create_index(
        "ix_users_guardian_moderated_by_user_id",
        "users",
        ["guardian_moderated_by_user_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_users_guardian_moderated_by_user_id_users",
        "users",
        "users",
        ["guardian_moderated_by_user_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.alter_column("users", "guardian_moderation_status", server_default=None)


def downgrade() -> None:
    op.drop_constraint("fk_users_guardian_moderated_by_user_id_users", "users", type_="foreignkey")
    op.drop_index("ix_users_guardian_moderated_by_user_id", table_name="users")
    op.drop_column("users", "guardian_moderated_by_user_id")
    op.drop_column("users", "guardian_moderated_at")
    op.drop_column("users", "guardian_moderation_status")

