import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

UPPERCASE_RE = re.compile(r"[A-Z]")
NON_ALPHA_RE = re.compile(r"[^a-zA-Z]")  # número o símbolo

def validate_password_policy(password: str) -> None:
    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if not UPPERCASE_RE.search(password):
        raise ValueError("La contraseña debe contener al menos 1 mayúscula.")
    if not NON_ALPHA_RE.search(password):
        raise ValueError("La contraseña debe contener al menos 1 número o símbolo.")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)  # bcrypt con salt automático

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

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
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )
        return payload
    except JWTError as e:
        raise ValueError("Token inválido o expirado.") from e
