import re
import uuid
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import jwt, JWTError
from .config import settings


# =========================
# Password policy
# =========================

UPPERCASE_RE = re.compile(r"[A-Z]")
NON_ALPHA_RE = re.compile(r"[^a-zA-Z]")  # número o símbolo


def validate_password_policy(password: str) -> None:
    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if not UPPERCASE_RE.search(password):
        raise ValueError("La contraseña debe contener al menos 1 mayúscula.")
    if not NON_ALPHA_RE.search(password):
        raise ValueError("La contraseña debe contener al menos 1 número o símbolo.")


# =========================
# Password hashing (bcrypt directo)
# =========================

def hash_password(password: str) -> str:
    pw = password.encode("utf-8")

    # bcrypt solo acepta hasta 72 bytes
    if len(pw) > 72:
        raise ValueError("La contraseña es demasiado larga (máximo 72 bytes).")

    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )


# =========================
# JWT helpers
# =========================

def _read_key(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


PRIVATE_KEY = _read_key(settings.JWT_PRIVATE_KEY_PATH)
PUBLIC_KEY = _read_key(settings.JWT_PUBLIC_KEY_PATH)


def create_access_token(*, sub: int, role: str, gr: Optional[int]) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jti = str(uuid.uuid4())

    payload = {
        "sub": str(sub),
        "role": role,
        "gr": gr,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": jti,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "typ": "access",
    }

    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")


def create_refresh_token(*, sub: int) -> Dict[str, str]:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())

    payload = {
        "sub": str(sub),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": jti,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "typ": "refresh",
    }

    token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return {"token": token, "jti": jti}


def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )
    except JWTError as e:
        raise ValueError("Token inválido o expirado.") from e

def create_2fa_temp_token(sub: int) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=5)
    jti = str(uuid.uuid4())

    payload = {
        "sub": str(sub),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": jti,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "typ": "2fa_pending",
    }

    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")


def decode_2fa_temp_token(token: str) -> int:
    payload = decode_token(token)

    if payload.get("typ") != "2fa_pending":
        raise ValueError("Token no es 2FA pending")

    return int(payload["sub"])

def create_vault_token(*, sub: int) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=20)  # vault session corta
    jti = str(uuid.uuid4())

    payload = {
        "sub": str(sub),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": jti,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "typ": "vault",
    }

    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")


def decode_vault_token(token: str) -> int:
    payload = decode_token(token)

    if payload.get("typ") != "vault":
        raise ValueError("Token no es vault")

    return int(payload["sub"])
