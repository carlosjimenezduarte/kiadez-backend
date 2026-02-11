from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.db.database import get_db
from app.db.repositories.refresh_token_repository import RefreshTokenRepository
from app.db.repositories.user_repository import UserRepository


router = APIRouter(prefix="/dev", tags=["dev"])


class DevLoginAsRequest(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None


def _ensure_dev_login_allowed(x_dev_secret: Optional[str]) -> None:
    if settings.APP_ENV.lower() not in {"dev", "local", "test"}:
        raise HTTPException(status_code=404, detail="Not found")

    if not settings.DEV_LOGIN_AS_ENABLED:
        raise HTTPException(status_code=404, detail="Not found")

    if settings.DEV_LOGIN_AS_SECRET and x_dev_secret != settings.DEV_LOGIN_AS_SECRET:
        raise HTTPException(status_code=401, detail="Dev secret invalid.")


@router.post("/login-as")
def dev_login_as(
    payload: DevLoginAsRequest,
    db: Session = Depends(get_db),
    x_dev_secret: Optional[str] = Header(default=None, alias="X-Dev-Secret"),
):
    _ensure_dev_login_allowed(x_dev_secret)

    if bool(payload.user_id) == bool(payload.email):
        raise HTTPException(status_code=400, detail="Provide exactly one of: user_id or email.")

    user_repo = UserRepository(db)
    if payload.user_id is not None:
        user = user_repo.get_user_by_id(payload.user_id)
    else:
        user = user_repo.get_user_by_email((payload.email or "").strip())

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not user.is_active:
        user.is_active = True
        db.commit()
        db.refresh(user)

    access = create_access_token(
        sub=user.id,
        role=user.role,
        gr=user.guardian_rank,
    )

    refresh = create_refresh_token(sub=user.id)
    refresh_repo = RefreshTokenRepository(db)
    refresh_repo.create(
        user_id=user.id,
        jti=refresh["jti"],
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return {
        "access_token": access,
        "refresh_token": refresh["token"],
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "guardian_rank": user.guardian_rank,
            "is_active": user.is_active,
        },
    }
