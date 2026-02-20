"""add cooperative fulfillment flow

Revision ID: e3d1f4a9b7c2
Revises: d1a7c3f4b9e2
Create Date: 2026-02-20 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e3d1f4a9b7c2"
down_revision: Union[str, Sequence[str], None] = "d1a7c3f4b9e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "public_cooperative_wish_participations",
        sa.Column(
            "evidence_media_id",
            sa.Integer(),
            sa.ForeignKey("media.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.add_column(
        "public_cooperative_wish_participations",
        sa.Column("evidence_submitted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "public_cooperative_wish_participations",
        sa.Column(
            "oath_accepted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.add_column(
        "public_cooperative_wish_participations",
        sa.Column("owner_validated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "public_cooperative_wish_participations",
        sa.Column(
            "owner_validated_by_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_pcwp_evidence_media_id",
        "public_cooperative_wish_participations",
        ["evidence_media_id"],
        unique=False,
    )
    op.create_index(
        "ix_pcwp_evidence_submitted_at",
        "public_cooperative_wish_participations",
        ["evidence_submitted_at"],
        unique=False,
    )
    op.create_index(
        "ix_pcwp_owner_validated_at",
        "public_cooperative_wish_participations",
        ["owner_validated_at"],
        unique=False,
    )
    op.create_index(
        "ix_pcwp_owner_validated_by_uid",
        "public_cooperative_wish_participations",
        ["owner_validated_by_user_id"],
        unique=False,
    )

    op.alter_column(
        "public_cooperative_wish_participations",
        "oath_accepted",
        server_default=None,
    )

    op.create_table(
        "public_cooperative_wish_fulfillments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "wish_id",
            sa.Integer(),
            sa.ForeignKey("public_cooperative_wishes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "wish_owner_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "final_evidence_media_id",
            sa.Integer(),
            sa.ForeignKey("media.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("oath_accepted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("fulfilled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("wish_id", name="uq_public_coop_wish_fulfillment_wish"),
    )

    op.create_index(
        "ix_public_cooperative_wish_fulfillments_id",
        "public_cooperative_wish_fulfillments",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_public_cooperative_wish_fulfillments_wish_id",
        "public_cooperative_wish_fulfillments",
        ["wish_id"],
        unique=False,
    )
    op.create_index(
        "ix_public_cooperative_wish_fulfillments_wish_owner_user_id",
        "public_cooperative_wish_fulfillments",
        ["wish_owner_user_id"],
        unique=False,
    )
    op.create_index(
        "ix_public_cooperative_wish_fulfillments_final_evidence_media_id",
        "public_cooperative_wish_fulfillments",
        ["final_evidence_media_id"],
        unique=False,
    )
    op.create_index(
        "ix_public_cooperative_wish_fulfillments_fulfilled_at",
        "public_cooperative_wish_fulfillments",
        ["fulfilled_at"],
        unique=False,
    )

    op.alter_column(
        "public_cooperative_wish_fulfillments",
        "oath_accepted",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_public_cooperative_wish_fulfillments_fulfilled_at",
        table_name="public_cooperative_wish_fulfillments",
    )
    op.drop_index(
        "ix_public_cooperative_wish_fulfillments_final_evidence_media_id",
        table_name="public_cooperative_wish_fulfillments",
    )
    op.drop_index(
        "ix_public_cooperative_wish_fulfillments_wish_owner_user_id",
        table_name="public_cooperative_wish_fulfillments",
    )
    op.drop_index(
        "ix_public_cooperative_wish_fulfillments_wish_id",
        table_name="public_cooperative_wish_fulfillments",
    )
    op.drop_index(
        "ix_public_cooperative_wish_fulfillments_id",
        table_name="public_cooperative_wish_fulfillments",
    )
    op.drop_table("public_cooperative_wish_fulfillments")

    op.drop_index(
        "ix_pcwp_owner_validated_by_uid",
        table_name="public_cooperative_wish_participations",
    )
    op.drop_index(
        "ix_pcwp_owner_validated_at",
        table_name="public_cooperative_wish_participations",
    )
    op.drop_index(
        "ix_pcwp_evidence_submitted_at",
        table_name="public_cooperative_wish_participations",
    )
    op.drop_index(
        "ix_pcwp_evidence_media_id",
        table_name="public_cooperative_wish_participations",
    )

    op.drop_column("public_cooperative_wish_participations", "owner_validated_by_user_id")
    op.drop_column("public_cooperative_wish_participations", "owner_validated_at")
    op.drop_column("public_cooperative_wish_participations", "oath_accepted")
    op.drop_column("public_cooperative_wish_participations", "evidence_submitted_at")
    op.drop_column("public_cooperative_wish_participations", "evidence_media_id")
