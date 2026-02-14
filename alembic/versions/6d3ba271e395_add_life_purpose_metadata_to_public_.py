"""add life purpose metadata to public wishes

Revision ID: 6d3ba271e395
Revises: d2a1f3c4b5e6
Create Date: 2026-02-14 10:31:49.579704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d3ba271e395'
down_revision: Union[str, Sequence[str], None] = 'd2a1f3c4b5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "public_personal_wishes",
        sa.Column("life_purpose_slot_number", sa.Integer(), nullable=True),
    )
    op.add_column(
        "public_personal_wishes",
        sa.Column("life_purpose_icon_key", sa.String(length=20), nullable=True),
    )
    op.create_index(
        "ix_public_personal_wishes_life_purpose_slot_number",
        "public_personal_wishes",
        ["life_purpose_slot_number"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_public_personal_wishes_life_purpose_slot_number", table_name="public_personal_wishes")
    op.drop_column("public_personal_wishes", "life_purpose_icon_key")
    op.drop_column("public_personal_wishes", "life_purpose_slot_number")
