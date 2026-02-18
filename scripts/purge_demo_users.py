#!/usr/bin/env python3
"""
Purge demo users (and optionally their media objects in S3) from the database.

This is intended as a one-time cleanup when switching from demo/dev accounts to real accounts.

Usage:
  ./venv/bin/python scripts/purge_demo_users.py --show
  ./venv/bin/python scripts/purge_demo_users.py --apply --yes
  ./venv/bin/python scripts/purge_demo_users.py --apply --yes --delete-s3
  ./venv/bin/python scripts/purge_demo_users.py --emails a@b.com,c@d.com --apply --yes
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sqlalchemy import delete, func, select


# Allow running as a script (python scripts/...) without requiring PYTHONPATH.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.storage import S3NotConfiguredError, delete_object, ensure_s3_configured
from app.db.database import SessionLocal
from app.db.models.media import Media
from app.db.models.post import Post
from app.db.models.refresh_token import RefreshToken
from app.db.models.user import User
from app.db.models.user_follow import UserFollow


DEFAULT_EMAILS = (
    "carlos.demo@kiadez.local",
    "david.demo@kiadez.local",
)


def _parse_emails(value: str) -> list[str]:
    emails: list[str] = []
    for part in (value or "").split(","):
        normalized = part.strip().lower()
        if normalized:
            emails.append(normalized)
    # stable order + dedupe
    seen: set[str] = set()
    out: list[str] = []
    for email in emails:
        if email in seen:
            continue
        seen.add(email)
        out.append(email)
    return out


def _count(db, stmt) -> int:
    value = db.execute(stmt).scalar_one()
    return int(value or 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--emails",
        default=",".join(DEFAULT_EMAILS),
        help="Comma-separated emails to purge (default: the legacy Kiadez demo accounts).",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Only show what would be deleted (default mode).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete the users and their data.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help='Skip interactive confirmation prompt (recommended for scripted usage).',
    )
    parser.add_argument(
        "--delete-s3",
        action="store_true",
        help="Also delete the users' media objects in S3 (best effort).",
    )
    args = parser.parse_args()

    emails = _parse_emails(args.emails)
    if not emails:
        print("No emails provided.")
        return 2

    db = SessionLocal()
    try:
        users = db.execute(select(User).where(User.email.in_(emails))).scalars().all()
        if not users:
            print("No matching users found for:")
            for email in emails:
                print(f"- {email}")
            return 0

        user_ids = [user.id for user in users]
        print("Users found:")
        for user in users:
            print(f"- id={user.id} email={user.email} username={user.username or ''} active={user.is_active}")

        posts_count = _count(db, select(func.count()).select_from(Post).where(Post.author_id.in_(user_ids)))
        media_count = _count(db, select(func.count()).select_from(Media).where(Media.owner_id.in_(user_ids)))
        follows_count = _count(
            db,
            select(func.count()).select_from(UserFollow).where(
                (UserFollow.follower_id.in_(user_ids)) | (UserFollow.followed_id.in_(user_ids))
            ),
        )
        refresh_count = _count(db, select(func.count()).select_from(RefreshToken).where(RefreshToken.user_id.in_(user_ids)))

        print("")
        print("Associated records (will be removed by DB cascades):")
        print(f"- posts: {posts_count}")
        print(f"- media: {media_count}")
        print(f"- follows: {follows_count}")
        print(f"- refresh tokens: {refresh_count}")

        if args.show or not args.apply:
            print("")
            print("Dry run. Re-run with: --apply --yes")
            return 0

        if not args.yes:
            confirm = input('Type "DELETE" to confirm: ').strip()
            if confirm != "DELETE":
                print("Aborted.")
                return 1

        keys: list[str] = []
        if args.delete_s3 and media_count:
            # Collect keys before deleting DB rows (after deletion, Media rows are gone).
            keys = db.execute(select(Media.object_key).where(Media.owner_id.in_(user_ids))).scalars().all()

        # Delete users at SQL level to rely on DB ON DELETE CASCADE, without ORM trying
        # to null-out foreign keys on related rows.
        try:
            db.execute(delete(User).where(User.id.in_(user_ids)))
            db.commit()
        except Exception:
            db.rollback()
            raise

        if args.delete_s3 and keys:
            try:
                ensure_s3_configured()
            except S3NotConfiguredError as exc:
                print(f"S3 not configured ({exc}); skipping --delete-s3.")
            else:
                deleted = 0
                failed = 0
                for key in keys:
                    try:
                        delete_object(key=key)
                        deleted += 1
                    except Exception:
                        failed += 1
                print("")
                print(f"S3 objects delete attempted: {len(keys)} (deleted={deleted}, failed={failed})")

        print("")
        print("Done. Demo users deleted.")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
