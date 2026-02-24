"""create post hashtags tables

Revision ID: f6d2a4c8b1e9
Revises: e7b1c2d3f4a5
Create Date: 2026-02-24 16:45:00.000000
"""

from datetime import datetime, timezone
import re
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f6d2a4c8b1e9"
down_revision: Union[str, Sequence[str], None] = "e7b1c2d3f4a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


HASHTAG_PATTERN = re.compile(r"(?<![A-Za-z0-9_])#([A-Za-z0-9_]{2,50})(?![A-Za-z0-9_])")


def _extract_hashtags(text: str | None) -> list[str]:
    if not text:
        return []
    tags: list[str] = []
    seen: set[str] = set()
    for match in HASHTAG_PATTERN.finditer(text):
        value = (match.group(1) or "").strip().lower()
        if not value or value in seen:
            continue
        seen.add(value)
        tags.append(value)
    return tags


def upgrade() -> None:
    op.create_table(
        "hashtags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tag", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_hashtags_id", "hashtags", ["id"], unique=False)
    op.create_index("ix_hashtags_tag", "hashtags", ["tag"], unique=True)
    op.create_index("ix_hashtags_created_at", "hashtags", ["created_at"], unique=False)

    op.create_table(
        "post_hashtags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("hashtag_id", sa.Integer(), sa.ForeignKey("hashtags.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("post_id", "hashtag_id", name="uq_post_hashtags_post_hashtag"),
    )
    op.create_index("ix_post_hashtags_id", "post_hashtags", ["id"], unique=False)
    op.create_index("ix_post_hashtags_post_id", "post_hashtags", ["post_id"], unique=False)
    op.create_index("ix_post_hashtags_hashtag_id", "post_hashtags", ["hashtag_id"], unique=False)
    op.create_index("ix_post_hashtags_created_at", "post_hashtags", ["created_at"], unique=False)

    connection = op.get_bind()
    now = datetime.now(timezone.utc)
    hashtag_id_by_tag: dict[str, int] = {}

    post_rows = connection.execute(
        sa.text(
            """
            SELECT id, text
            FROM posts
            WHERE text IS NOT NULL
              AND text LIKE :contains_hash
            """
        ),
        {"contains_hash": "%#%"},
    ).all()

    hashtag_table = sa.table(
        "hashtags",
        sa.column("id", sa.Integer()),
        sa.column("tag", sa.String(length=50)),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    post_hashtag_table = sa.table(
        "post_hashtags",
        sa.column("post_id", sa.Integer()),
        sa.column("hashtag_id", sa.Integer()),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )

    for post_id, text in post_rows:
        tags = _extract_hashtags(text)
        for tag in tags:
            hashtag_id = hashtag_id_by_tag.get(tag)
            if hashtag_id is None:
                connection.execute(
                    sa.insert(hashtag_table).values(
                        tag=tag,
                        created_at=now,
                    )
                )
                hashtag_id = int(
                    connection.execute(
                        sa.select(hashtag_table.c.id).where(hashtag_table.c.tag == tag)
                    ).scalar_one()
                )
                hashtag_id_by_tag[tag] = hashtag_id

            connection.execute(
                sa.insert(post_hashtag_table).values(
                    post_id=int(post_id),
                    hashtag_id=int(hashtag_id),
                    created_at=now,
                )
            )


def downgrade() -> None:
    op.drop_index("ix_post_hashtags_created_at", table_name="post_hashtags")
    op.drop_index("ix_post_hashtags_hashtag_id", table_name="post_hashtags")
    op.drop_index("ix_post_hashtags_post_id", table_name="post_hashtags")
    op.drop_index("ix_post_hashtags_id", table_name="post_hashtags")
    op.drop_table("post_hashtags")

    op.drop_index("ix_hashtags_created_at", table_name="hashtags")
    op.drop_index("ix_hashtags_tag", table_name="hashtags")
    op.drop_index("ix_hashtags_id", table_name="hashtags")
    op.drop_table("hashtags")
