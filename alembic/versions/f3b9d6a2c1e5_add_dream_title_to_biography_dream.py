"""add dream title to biography dream

Revision ID: f3b9d6a2c1e5
Revises: e7f2c4a1b9d8
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f3b9d6a2c1e5"
down_revision: Union[str, Sequence[str], None] = "e7f2c4a1b9d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("biography_dream", sa.Column("dream_title", sa.String(length=200), nullable=True))


def downgrade() -> None:
    op.drop_column("biography_dream", "dream_title")
