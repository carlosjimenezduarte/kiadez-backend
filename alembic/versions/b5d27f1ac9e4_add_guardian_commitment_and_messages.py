"""add guardian commitment and messages

Revision ID: b5d27f1ac9e4
Revises: a91e5b73c8d4
Create Date: 2026-02-18 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "b5d27f1ac9e4"
down_revision: Union[str, Sequence[str], None] = "a91e5b73c8d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("guardian_wish_requests", sa.Column("commitment_code", sa.String(length=32), nullable=True))
    op.add_column(
        "guardian_wish_requests",
        sa.Column("commitment_sealed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column("guardian_wish_requests", sa.Column("denied_at", sa.DateTime(timezone=True), nullable=True))

    op.create_index(
        "ix_guardian_wish_requests_commitment_code",
        "guardian_wish_requests",
        ["commitment_code"],
        unique=True,
    )
    op.create_index(
        "ix_guardian_wish_requests_commitment_sealed_at",
        "guardian_wish_requests",
        ["commitment_sealed_at"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_requests_denied_at",
        "guardian_wish_requests",
        ["denied_at"],
        unique=False,
    )

    message_kind_enum = postgresql.ENUM(
        "denial",
        "owner_contact",
        name="guardian_wish_message_kind",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE guardian_wish_message_kind AS ENUM ('denial', 'owner_contact'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "guardian_wish_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "wish_request_id",
            sa.Integer(),
            sa.ForeignKey("guardian_wish_requests.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "sender_guardian_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "recipient_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", message_kind_enum, nullable=False),
        sa.Column("subject", sa.String(length=180), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_guardian_wish_messages_id", "guardian_wish_messages", ["id"], unique=False)
    op.create_index(
        "ix_guardian_wish_messages_wish_request_id",
        "guardian_wish_messages",
        ["wish_request_id"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_messages_sender_guardian_id",
        "guardian_wish_messages",
        ["sender_guardian_id"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_messages_recipient_user_id",
        "guardian_wish_messages",
        ["recipient_user_id"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_messages_kind",
        "guardian_wish_messages",
        ["kind"],
        unique=False,
    )
    op.create_index(
        "ix_guardian_wish_messages_created_at",
        "guardian_wish_messages",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_guardian_wish_messages_created_at", table_name="guardian_wish_messages")
    op.drop_index("ix_guardian_wish_messages_kind", table_name="guardian_wish_messages")
    op.drop_index("ix_guardian_wish_messages_recipient_user_id", table_name="guardian_wish_messages")
    op.drop_index("ix_guardian_wish_messages_sender_guardian_id", table_name="guardian_wish_messages")
    op.drop_index("ix_guardian_wish_messages_wish_request_id", table_name="guardian_wish_messages")
    op.drop_index("ix_guardian_wish_messages_id", table_name="guardian_wish_messages")
    op.drop_table("guardian_wish_messages")
    op.execute("DROP TYPE IF EXISTS guardian_wish_message_kind")

    op.drop_index("ix_guardian_wish_requests_denied_at", table_name="guardian_wish_requests")
    op.drop_index("ix_guardian_wish_requests_commitment_sealed_at", table_name="guardian_wish_requests")
    op.drop_index("ix_guardian_wish_requests_commitment_code", table_name="guardian_wish_requests")
    op.drop_column("guardian_wish_requests", "denied_at")
    op.drop_column("guardian_wish_requests", "commitment_sealed_at")
    op.drop_column("guardian_wish_requests", "commitment_code")
