#!/usr/bin/env python3
"""
Set guardian rank (and optional role) for a user.

Examples:
  ./venv/bin/python scripts/set_guardian_rank.py --list
  ./venv/bin/python scripts/set_guardian_rank.py --email carlos.demo@kiadez.local --rank 3 --apply --yes
  ./venv/bin/python scripts/set_guardian_rank.py --username carlosjduarte --rank 3 --role guardian --apply --yes
  ./venv/bin/python scripts/set_guardian_rank.py --user-id 1 --rank 3 --apply --yes
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sqlalchemy import select

# Allow running as a script (python scripts/...) without requiring PYTHONPATH.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.db.database import SessionLocal  # noqa: E402
from app.db.models.user import User  # noqa: E402


ROLE_CHOICES = ("user", "guardian", "admin")


def _normalize_username(value: str) -> str:
    normalized = str(value or "").strip().lower()
    while normalized.startswith("@"):
        normalized = normalized[1:]
    return normalized


def _print_user(prefix: str, user: User) -> None:
    username = (user.username or "").strip()
    full_name = f"{(user.first_name or '').strip()} {(user.last_name or '').strip()}".strip()
    gr = user.guardian_rank if user.guardian_rank is not None else 0
    print(
        f"{prefix}id={user.id} email={user.email} username={username} "
        f"name={full_name} role={user.role} guardian_rank={gr} active={user.is_active}"
    )


def _resolve_user(db, *, user_id: int | None, email: str | None, username: str | None) -> User | None:
    if user_id is not None:
        return db.execute(select(User).where(User.id == int(user_id))).scalar_one_or_none()
    if email:
        return db.execute(select(User).where(User.email == email.strip().lower())).scalar_one_or_none()
    if username:
        return db.execute(select(User).where(User.username == _normalize_username(username))).scalar_one_or_none()
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="List users (dry).")
    parser.add_argument("--limit", type=int, default=50, help="Max users to show with --list (default: 50).")

    ident = parser.add_argument_group("identify a single user")
    ident.add_argument("--user-id", type=int, default=None)
    ident.add_argument("--email", default=None)
    ident.add_argument("--username", default=None)

    parser.add_argument("--rank", type=int, default=3, help="Guardian rank to set (default: 3).")
    parser.add_argument(
        "--role",
        default=None,
        choices=ROLE_CHOICES,
        help='Optional role to set too ("user", "guardian", "admin").',
    )
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry run).")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt when using --apply.")

    args = parser.parse_args()

    if args.list and (args.user_id is not None or args.email or args.username):
        print("Use either --list or a user identifier (not both).")
        return 2

    identifiers = [args.user_id is not None, bool(args.email), bool(args.username)]
    if not args.list and sum(identifiers) != 1:
        print("Provide exactly one identifier: --user-id OR --email OR --username.")
        return 2

    if args.rank < 0 or args.rank > 10:
        print("--rank must be between 0 and 10.")
        return 2

    db = SessionLocal()
    try:
        if args.list:
            rows = db.execute(
                select(User).order_by(User.id.asc()).limit(max(1, int(args.limit or 50)))
            ).scalars().all()
            print(f"Users shown: {len(rows)}")
            for user in rows:
                _print_user("- ", user)
            return 0

        user = _resolve_user(db, user_id=args.user_id, email=args.email, username=args.username)
        if user is None:
            print("User not found.")
            return 1

        _print_user("Current: ", user)

        next_rank = int(args.rank)
        next_role = str(args.role).strip().lower() if args.role else None

        changes: list[str] = []
        current_rank = int(user.guardian_rank or 0)
        if current_rank != next_rank:
            changes.append(f"guardian_rank: {current_rank} -> {next_rank}")
        if next_role and user.role != next_role:
            changes.append(f"role: {user.role} -> {next_role}")

        if not changes:
            print("No changes needed.")
            return 0

        print("Proposed changes:")
        for change in changes:
            print(f"- {change}")

        if not args.apply:
            print("")
            print("Dry run. Re-run with: --apply --yes")
            return 0

        if not args.yes:
            confirm = input('Type "APPLY" to confirm: ').strip()
            if confirm != "APPLY":
                print("Aborted.")
                return 1

        user.guardian_rank = next_rank
        if next_role:
            user.role = next_role
        db.add(user)
        db.commit()
        db.refresh(user)

        _print_user("Updated: ", user)
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())

