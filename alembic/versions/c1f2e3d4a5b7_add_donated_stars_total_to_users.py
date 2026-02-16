"""add donated_stars_total to users

Revision ID: c1f2e3d4a5b7
Revises: 8f6c4b2d1a79
Create Date: 2026-02-16 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c1f2e3d4a5b7"
down_revision: Union[str, Sequence[str], None] = "8f6c4b2d1a79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("donated_stars_total", sa.Integer(), nullable=False, server_default=sa.text("0")),
    )
    op.alter_column("users", "donated_stars_total", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "donated_stars_total")
