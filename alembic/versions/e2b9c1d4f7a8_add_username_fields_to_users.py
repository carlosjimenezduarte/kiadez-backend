"""add username fields to users

Revision ID: e2b9c1d4f7a8
Revises: c1f2e3d4a5b7
Create Date: 2026-02-16 16:40:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e2b9c1d4f7a8"
down_revision: Union[str, Sequence[str], None] = "c1f2e3d4a5b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(length=30), nullable=True))
    op.add_column("users", sa.Column("username_updated_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_column("users", "username_updated_at")
    op.drop_column("users", "username")
