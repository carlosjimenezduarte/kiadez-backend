import secrets
from datetime import datetime, timedelta, timezone


def generate_password_reset_token() -> str:
    return secrets.token_urlsafe(32)


def get_password_reset_expiry(minutes: int = 60):
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)
