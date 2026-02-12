"""create biography physical traits table

Revision ID: f1e7a4c2b9d0
Revises: e6b47d2f1a90
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f1e7a4c2b9d0"
down_revision: Union[str, Sequence[str], None] = "e6b47d2f1a90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "biography_physical_traits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("height", sa.String(length=40), nullable=True),
        sa.Column("weight", sa.String(length=40), nullable=True),
        sa.Column("eyes", sa.String(length=80), nullable=True),
        sa.Column("hair", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_biography_physical_traits_user_id"),
    )
    op.create_index("ix_biography_physical_traits_id", "biography_physical_traits", ["id"], unique=False)
    op.create_index("ix_biography_physical_traits_user_id", "biography_physical_traits", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_biography_physical_traits_user_id", table_name="biography_physical_traits")
    op.drop_index("ix_biography_physical_traits_id", table_name="biography_physical_traits")
    op.drop_table("biography_physical_traits")

