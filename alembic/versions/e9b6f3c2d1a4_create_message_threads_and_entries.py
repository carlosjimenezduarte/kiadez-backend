"""create message threads and entries

Revision ID: e9b6f3c2d1a4
Revises: c4a7f9d2e1b6
Create Date: 2026-02-19 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e9b6f3c2d1a4"
down_revision: Union[str, Sequence[str], None] = "c4a7f9d2e1b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "message_threads",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "guardian_user_id",
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
        sa.Column("subject", sa.String(length=180), nullable=False),
        sa.Column(
            "source_guardian_wish_message_id",
            sa.Integer(),
            sa.ForeignKey("guardian_wish_messages.id", ondelete="SET NULL"),
            nullable=True,
            unique=True,
        ),
        sa.Column(
            "is_guardian_center_origin",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index("ix_message_threads_id", "message_threads", ["id"], unique=False)
    op.create_index("ix_message_threads_guardian_user_id", "message_threads", ["guardian_user_id"], unique=False)
    op.create_index("ix_message_threads_recipient_user_id", "message_threads", ["recipient_user_id"], unique=False)
    op.create_index("ix_message_threads_created_at", "message_threads", ["created_at"], unique=False)
    op.create_index("ix_message_threads_updated_at", "message_threads", ["updated_at"], unique=False)

    op.create_table(
        "message_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "thread_id",
            sa.Integer(),
            sa.ForeignKey("message_threads.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "sender_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index("ix_message_entries_id", "message_entries", ["id"], unique=False)
    op.create_index("ix_message_entries_thread_id", "message_entries", ["thread_id"], unique=False)
    op.create_index("ix_message_entries_sender_user_id", "message_entries", ["sender_user_id"], unique=False)
    op.create_index("ix_message_entries_created_at", "message_entries", ["created_at"], unique=False)

    op.execute(
        """
        INSERT INTO message_threads (
            guardian_user_id,
            recipient_user_id,
            subject,
            source_guardian_wish_message_id,
            is_guardian_center_origin,
            created_at,
            updated_at
        )
        SELECT
            gwm.sender_guardian_id,
            gwm.recipient_user_id,
            gwm.subject,
            gwm.id,
            TRUE,
            gwm.created_at,
            gwm.created_at
        FROM guardian_wish_messages gwm
        WHERE gwm.sender_guardian_id IS NOT NULL
        """
    )

    op.execute(
        """
        INSERT INTO message_entries (
            thread_id,
            sender_user_id,
            body,
            created_at
        )
        SELECT
            mt.id,
            gwm.sender_guardian_id,
            gwm.body,
            gwm.created_at
        FROM guardian_wish_messages gwm
        JOIN message_threads mt
          ON mt.source_guardian_wish_message_id = gwm.id
        WHERE gwm.sender_guardian_id IS NOT NULL
        """
    )


def downgrade() -> None:
    op.drop_index("ix_message_entries_created_at", table_name="message_entries")
    op.drop_index("ix_message_entries_sender_user_id", table_name="message_entries")
    op.drop_index("ix_message_entries_thread_id", table_name="message_entries")
    op.drop_index("ix_message_entries_id", table_name="message_entries")
    op.drop_table("message_entries")

    op.drop_index("ix_message_threads_updated_at", table_name="message_threads")
    op.drop_index("ix_message_threads_created_at", table_name="message_threads")
    op.drop_index("ix_message_threads_recipient_user_id", table_name="message_threads")
    op.drop_index("ix_message_threads_guardian_user_id", table_name="message_threads")
    op.drop_index("ix_message_threads_id", table_name="message_threads")
    op.drop_table("message_threads")
