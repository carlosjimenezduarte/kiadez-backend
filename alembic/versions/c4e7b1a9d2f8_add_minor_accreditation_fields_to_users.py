"""add minor accreditation fields to users

Revision ID: c4e7b1a9d2f8
Revises: b8f6d3c1a2e4
Create Date: 2026-02-23 18:40:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c4e7b1a9d2f8"
down_revision: Union[str, Sequence[str], None] = "b8f6d3c1a2e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "minor_accreditation_status",
            sa.String(length=32),
            nullable=False,
            server_default=sa.text("'not_required'"),
        ),
    )
    op.add_column("users", sa.Column("minor_guardian_phone", sa.String(length=40), nullable=True))
    op.add_column("users", sa.Column("minor_guardian_email", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("minor_guardian_relationship", sa.String(length=40), nullable=True))
    op.add_column("users", sa.Column("minor_accreditation_requested_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("minor_accreditation_approved_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("minor_accreditation_token_hash", sa.String(length=128), nullable=True))
    op.add_column("users", sa.Column("minor_accreditation_token_expires_at", sa.DateTime(timezone=True), nullable=True))

    op.create_index(
        "ix_users_minor_accreditation_token_hash",
        "users",
        ["minor_accreditation_token_hash"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_users_minor_accreditation_token_hash", table_name="users")
    op.drop_column("users", "minor_accreditation_token_expires_at")
    op.drop_column("users", "minor_accreditation_token_hash")
    op.drop_column("users", "minor_accreditation_approved_at")
    op.drop_column("users", "minor_accreditation_requested_at")
    op.drop_column("users", "minor_guardian_relationship")
    op.drop_column("users", "minor_guardian_email")
    op.drop_column("users", "minor_guardian_phone")
    op.drop_column("users", "minor_accreditation_status")
