"""create email verification tokens table

Revision ID: 49424f1937af
Revises: 7a02cbd7b0d1
Create Date: 2026-01-16 17:49:38.001419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49424f1937af'
down_revision: Union[str, Sequence[str], None] = '7a02cbd7b0d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "email_verification_tokens",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("token", sa.String(64), nullable=False, unique=True),
        sa.Column("is_used", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_email_verification_tokens_token",
        "email_verification_tokens",
        ["token"],
    )


def downgrade():
    op.drop_index("ix_email_verification_tokens_token")
    op.drop_table("email_verification_tokens")