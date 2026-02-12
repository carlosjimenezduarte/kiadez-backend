"""create biography personal info table

Revision ID: e6b47d2f1a90
Revises: c8b7c5d31f9a
Create Date: 2026-02-12 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e6b47d2f1a90"
down_revision: Union[str, Sequence[str], None] = "c8b7c5d31f9a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "biography_personal_info",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("birth_name", sa.String(length=200), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("birth_city", sa.String(length=120), nullable=True),
        sa.Column("birth_region", sa.String(length=120), nullable=True),
        sa.Column("birth_country", sa.String(length=120), nullable=True),
        sa.Column("residence", sa.String(length=255), nullable=True),
        sa.Column("nationality", sa.String(length=120), nullable=True),
        sa.Column("native_language", sa.String(length=120), nullable=True),
        sa.Column("pseudonyms", sa.String(length=300), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_biography_personal_info_user_id"),
    )
    op.create_index("ix_biography_personal_info_id", "biography_personal_info", ["id"], unique=False)
    op.create_index("ix_biography_personal_info_user_id", "biography_personal_info", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_biography_personal_info_user_id", table_name="biography_personal_info")
    op.drop_index("ix_biography_personal_info_id", table_name="biography_personal_info")
    op.drop_table("biography_personal_info")
