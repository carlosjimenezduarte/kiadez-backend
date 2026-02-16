"""create oracle tables

Revision ID: 8f6c4b2d1a79
Revises: 6d3ba271e395
Create Date: 2026-02-16 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "8f6c4b2d1a79"
down_revision: Union[str, Sequence[str], None] = "6d3ba271e395"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    response_type_enum = postgresql.ENUM(
        "public",
        "secret",
        "heart",
        name="oracle_response_type",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE oracle_response_type AS ENUM ('public', 'secret', 'heart'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "oracle_user_states",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("cycle", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("cycle_started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_pick_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", name="uq_oracle_user_state_user_id"),
    )

    op.create_index("ix_oracle_user_states_id", "oracle_user_states", ["id"], unique=False)
    op.create_index("ix_oracle_user_states_user_id", "oracle_user_states", ["user_id"], unique=False)

    op.create_table(
        "oracle_responses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("card_id", sa.Integer(), nullable=False),
        sa.Column("cycle", sa.Integer(), nullable=False),
        sa.Column("response_type", response_type_enum, nullable=False),
        sa.Column("text_public", sa.String(length=4000), nullable=True),
        sa.Column("ciphertext", sa.LargeBinary(), nullable=True),
        sa.Column("nonce", sa.LargeBinary(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index("ix_oracle_responses_id", "oracle_responses", ["id"], unique=False)
    op.create_index("ix_oracle_responses_user_id", "oracle_responses", ["user_id"], unique=False)
    op.create_index("ix_oracle_responses_card_id", "oracle_responses", ["card_id"], unique=False)
    op.create_index("ix_oracle_responses_cycle", "oracle_responses", ["cycle"], unique=False)
    op.create_index("ix_oracle_responses_response_type", "oracle_responses", ["response_type"], unique=False)
    op.create_index("ix_oracle_responses_created_at", "oracle_responses", ["created_at"], unique=False)
    op.create_index("ix_oracle_responses_user_cycle", "oracle_responses", ["user_id", "cycle"], unique=False)
    op.create_index(
        "ix_oracle_responses_user_cycle_card",
        "oracle_responses",
        ["user_id", "cycle", "card_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_oracle_responses_user_cycle_card", table_name="oracle_responses")
    op.drop_index("ix_oracle_responses_user_cycle", table_name="oracle_responses")
    op.drop_index("ix_oracle_responses_created_at", table_name="oracle_responses")
    op.drop_index("ix_oracle_responses_response_type", table_name="oracle_responses")
    op.drop_index("ix_oracle_responses_cycle", table_name="oracle_responses")
    op.drop_index("ix_oracle_responses_card_id", table_name="oracle_responses")
    op.drop_index("ix_oracle_responses_user_id", table_name="oracle_responses")
    op.drop_index("ix_oracle_responses_id", table_name="oracle_responses")
    op.drop_table("oracle_responses")

    op.drop_index("ix_oracle_user_states_user_id", table_name="oracle_user_states")
    op.drop_index("ix_oracle_user_states_id", table_name="oracle_user_states")
    op.drop_table("oracle_user_states")

    op.execute("DROP TYPE IF EXISTS oracle_response_type;")
