"""create public cooperative wishes tables

Revision ID: d1a7c3f4b9e2
Revises: b4d9f2c1a7e6
Create Date: 2026-02-19 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d1a7c3f4b9e2"
down_revision: Union[str, Sequence[str], None] = "b4d9f2c1a7e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "public_cooperative_wishes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("wish_text", sa.Text(), nullable=False),
        sa.Column("wish_type", sa.String(length=40), nullable=False),
        sa.Column("participants_goal", sa.Integer(), nullable=False),
        sa.Column("template_text", sa.Text(), nullable=True),
        sa.Column("security_code", sa.String(length=6), nullable=False),
        sa.Column("media_id", sa.Integer(), sa.ForeignKey("media.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_public_cooperative_wishes_id", "public_cooperative_wishes", ["id"], unique=False)
    op.create_index("ix_public_cooperative_wishes_user_id", "public_cooperative_wishes", ["user_id"], unique=False)
    op.create_index("ix_public_cooperative_wishes_media_id", "public_cooperative_wishes", ["media_id"], unique=False)
    op.create_index("ix_public_cooperative_wishes_created_at", "public_cooperative_wishes", ["created_at"], unique=False)

    op.create_table(
        "public_cooperative_wish_participations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("wish_id", sa.Integer(), sa.ForeignKey("public_cooperative_wishes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("participant_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("participation_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("wish_id", "participant_user_id", name="uq_public_coop_wish_participant"),
    )
    op.create_index(
        "ix_public_cooperative_wish_participations_id",
        "public_cooperative_wish_participations",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_public_cooperative_wish_participations_wish_id",
        "public_cooperative_wish_participations",
        ["wish_id"],
        unique=False,
    )
    op.create_index(
        "ix_public_cooperative_wish_participations_participant_user_id",
        "public_cooperative_wish_participations",
        ["participant_user_id"],
        unique=False,
    )
    op.create_index(
        "ix_public_cooperative_wish_participations_created_at",
        "public_cooperative_wish_participations",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_public_cooperative_wish_participations_created_at",
        table_name="public_cooperative_wish_participations",
    )
    op.drop_index(
        "ix_public_cooperative_wish_participations_participant_user_id",
        table_name="public_cooperative_wish_participations",
    )
    op.drop_index(
        "ix_public_cooperative_wish_participations_wish_id",
        table_name="public_cooperative_wish_participations",
    )
    op.drop_index(
        "ix_public_cooperative_wish_participations_id",
        table_name="public_cooperative_wish_participations",
    )
    op.drop_table("public_cooperative_wish_participations")

    op.drop_index("ix_public_cooperative_wishes_created_at", table_name="public_cooperative_wishes")
    op.drop_index("ix_public_cooperative_wishes_media_id", table_name="public_cooperative_wishes")
    op.drop_index("ix_public_cooperative_wishes_user_id", table_name="public_cooperative_wishes")
    op.drop_index("ix_public_cooperative_wishes_id", table_name="public_cooperative_wishes")
    op.drop_table("public_cooperative_wishes")
