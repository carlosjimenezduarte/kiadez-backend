"""create public wish fulfillments table

Revision ID: c4a7f9d2e1b6
Revises: b5d27f1ac9e4
Create Date: 2026-02-18 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "c4a7f9d2e1b6"
down_revision: Union[str, Sequence[str], None] = "b5d27f1ac9e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    attribution_mode_enum = postgresql.ENUM(
        "secret",
        "public",
        name="public_wish_fulfillment_attribution_mode",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE public_wish_fulfillment_attribution_mode AS ENUM ('secret', 'public'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "public_wish_fulfillments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "wish_id",
            sa.Integer(),
            sa.ForeignKey("public_personal_wishes.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "wish_owner_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "fulfiller_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "guardian_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "wish_request_id",
            sa.Integer(),
            sa.ForeignKey("guardian_wish_requests.id", ondelete="SET NULL"),
            nullable=True,
            unique=True,
        ),
        sa.Column("commitment_code", sa.String(length=32), nullable=False, unique=True),
        sa.Column("attribution_mode", attribution_mode_enum, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index("ix_public_wish_fulfillments_id", "public_wish_fulfillments", ["id"], unique=False)
    op.create_index("ix_public_wish_fulfillments_wish_id", "public_wish_fulfillments", ["wish_id"], unique=False)
    op.create_index(
        "ix_public_wish_fulfillments_wish_owner_id",
        "public_wish_fulfillments",
        ["wish_owner_id"],
        unique=False,
    )
    op.create_index(
        "ix_public_wish_fulfillments_fulfiller_user_id",
        "public_wish_fulfillments",
        ["fulfiller_user_id"],
        unique=False,
    )
    op.create_index(
        "ix_public_wish_fulfillments_guardian_user_id",
        "public_wish_fulfillments",
        ["guardian_user_id"],
        unique=False,
    )
    op.create_index(
        "ix_public_wish_fulfillments_wish_request_id",
        "public_wish_fulfillments",
        ["wish_request_id"],
        unique=False,
    )
    op.create_index(
        "ix_public_wish_fulfillments_commitment_code",
        "public_wish_fulfillments",
        ["commitment_code"],
        unique=True,
    )
    op.create_index(
        "ix_public_wish_fulfillments_attribution_mode",
        "public_wish_fulfillments",
        ["attribution_mode"],
        unique=False,
    )
    op.create_index(
        "ix_public_wish_fulfillments_created_at",
        "public_wish_fulfillments",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_public_wish_fulfillments_created_at", table_name="public_wish_fulfillments")
    op.drop_index("ix_public_wish_fulfillments_attribution_mode", table_name="public_wish_fulfillments")
    op.drop_index("ix_public_wish_fulfillments_commitment_code", table_name="public_wish_fulfillments")
    op.drop_index("ix_public_wish_fulfillments_wish_request_id", table_name="public_wish_fulfillments")
    op.drop_index("ix_public_wish_fulfillments_guardian_user_id", table_name="public_wish_fulfillments")
    op.drop_index("ix_public_wish_fulfillments_fulfiller_user_id", table_name="public_wish_fulfillments")
    op.drop_index("ix_public_wish_fulfillments_wish_owner_id", table_name="public_wish_fulfillments")
    op.drop_index("ix_public_wish_fulfillments_wish_id", table_name="public_wish_fulfillments")
    op.drop_index("ix_public_wish_fulfillments_id", table_name="public_wish_fulfillments")
    op.drop_table("public_wish_fulfillments")
    op.execute("DROP TYPE IF EXISTS public_wish_fulfillment_attribution_mode")
