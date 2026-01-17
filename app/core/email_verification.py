import secrets
from datetime import datetime, timedelta, timezone


def generate_email_verification_token() -> str:
    return secrets.token_urlsafe(32)


def get_email_verification_expiry(hours: int = 24):
    return datetime.now(timezone.utc) + timedelta(hours=hours)
