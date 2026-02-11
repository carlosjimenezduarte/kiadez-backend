"""create posts core tables

Revision ID: b7d4f0a9c2e1
Revises: 9c3f0e2a1b7a
Create Date: 2026-02-11 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "b7d4f0a9c2e1"
down_revision: Union[str, Sequence[str], None] = "9c3f0e2a1b7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("received_stars_total", sa.Integer(), nullable=False, server_default=sa.text("0")),
    )

    post_visibility = postgresql.ENUM("public", "private", name="post_visibility", create_type=False)
    post_media_kind = postgresql.ENUM("image", "video", name="post_media_kind", create_type=False)
    post_report_reason = postgresql.ENUM(
        "violent",
        "divisive",
        "sexual",
        "other",
        name="post_report_reason",
        create_type=False,
    )

    op.execute(
        "DO $$ BEGIN CREATE TYPE post_visibility AS ENUM ('public', 'private'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )
    op.execute(
        "DO $$ BEGIN CREATE TYPE post_media_kind AS ENUM ('image', 'video'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )
    op.execute(
        "DO $$ BEGIN CREATE TYPE post_report_reason AS ENUM ('violent', 'divisive', 'sexual', 'other'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("visibility", post_visibility, nullable=False, server_default=sa.text("'public'")),
        sa.Column("media_id", sa.Integer(), sa.ForeignKey("media.id", ondelete="SET NULL"), nullable=True),
        sa.Column("media_kind", post_media_kind, nullable=True),
        sa.Column("star_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("comment_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("share_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_posts_id", "posts", ["id"], unique=False)
    op.create_index("ix_posts_author_id", "posts", ["author_id"], unique=False)
    op.create_index("ix_posts_media_id", "posts", ["media_id"], unique=False)
    op.create_index("ix_posts_created_at", "posts", ["created_at"], unique=False)

    op.create_table(
        "post_stars",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("post_id", "user_id", name="uq_post_stars_post_user"),
    )
    op.create_index("ix_post_stars_id", "post_stars", ["id"], unique=False)
    op.create_index("ix_post_stars_post_id", "post_stars", ["post_id"], unique=False)
    op.create_index("ix_post_stars_user_id", "post_stars", ["user_id"], unique=False)

    op.create_table(
        "post_comments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_post_comments_id", "post_comments", ["id"], unique=False)
    op.create_index("ix_post_comments_post_id", "post_comments", ["post_id"], unique=False)
    op.create_index("ix_post_comments_user_id", "post_comments", ["user_id"], unique=False)
    op.create_index("ix_post_comments_created_at", "post_comments", ["created_at"], unique=False)

    op.create_table(
        "post_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reporter_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reason", post_report_reason, nullable=False),
        sa.Column("other_reason", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("post_id", "reporter_id", name="uq_post_reports_post_reporter"),
    )
    op.create_index("ix_post_reports_id", "post_reports", ["id"], unique=False)
    op.create_index("ix_post_reports_post_id", "post_reports", ["post_id"], unique=False)
    op.create_index("ix_post_reports_reporter_id", "post_reports", ["reporter_id"], unique=False)
    op.create_index("ix_post_reports_created_at", "post_reports", ["created_at"], unique=False)

    op.alter_column("users", "received_stars_total", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_post_reports_created_at", table_name="post_reports")
    op.drop_index("ix_post_reports_reporter_id", table_name="post_reports")
    op.drop_index("ix_post_reports_post_id", table_name="post_reports")
    op.drop_index("ix_post_reports_id", table_name="post_reports")
    op.drop_table("post_reports")

    op.drop_index("ix_post_comments_created_at", table_name="post_comments")
    op.drop_index("ix_post_comments_user_id", table_name="post_comments")
    op.drop_index("ix_post_comments_post_id", table_name="post_comments")
    op.drop_index("ix_post_comments_id", table_name="post_comments")
    op.drop_table("post_comments")

    op.drop_index("ix_post_stars_user_id", table_name="post_stars")
    op.drop_index("ix_post_stars_post_id", table_name="post_stars")
    op.drop_index("ix_post_stars_id", table_name="post_stars")
    op.drop_table("post_stars")

    op.drop_index("ix_posts_created_at", table_name="posts")
    op.drop_index("ix_posts_media_id", table_name="posts")
    op.drop_index("ix_posts_author_id", table_name="posts")
    op.drop_index("ix_posts_id", table_name="posts")
    op.drop_table("posts")

    op.drop_column("users", "received_stars_total")

    op.execute("DROP TYPE IF EXISTS post_report_reason")
    op.execute("DROP TYPE IF EXISTS post_media_kind")
    op.execute("DROP TYPE IF EXISTS post_visibility")
