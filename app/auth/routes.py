# SQLAlchemy
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.repositories.user_repository import UserRepository

# FastAPI
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import Body

from app.db.repositories.refresh_token_repository import RefreshTokenRepository
from datetime import datetime, timedelta, timezone
from app.core.config import settings


# Auth
from .models import RegisterRequest, LoginRequest, TokenPair, UserPublic
from app.core.security import (
    validate_password_policy,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # aunque login sea JSON, sirve para dependencia

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserPublic:
    try:
        payload = decode_token(token)
        if payload.get("typ") != "access":
            raise ValueError("Tipo de token incorrecto.")

        user_id = int(payload["sub"])

        repo = UserRepository(db)
        user = repo.get_user_by_id(user_id)

        if not user or not user.is_active:
            raise ValueError("Usuario no encontrado o inactivo.")

        return UserPublic(
            user_number=user.id,
            email=user.email,
            role=user.role,
            guardian_rank=user.guardian_rank,
            is_active=user.is_active,
        )
    except Exception:
        raise HTTPException(status_code=401, detail="No autorizado")



@router.post("/register", response_model=UserPublic)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    try:
        validate_password_policy(data.password)
        pw_hash = hash_password(data.password)

        repo = UserRepository(db)
        user = repo.create_user(
            email=data.email,
            password_hash=pw_hash,
            role="user",
        )

        return UserPublic(
            user_number=user.id,
            email=user.email,
            role=user.role,
            guardian_rank=user.guardian_rank,
            is_active=user.is_active,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenPair)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)
    user = repo.get_user_by_email(data.email)

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

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
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return TokenPair(
        access_token=access,
        refresh_token=refresh["token"],
    )

 
@router.post("/refresh", response_model=TokenPair)
def refresh(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_token(refresh_token)
        if payload.get("typ") != "refresh":
            raise ValueError("Tipo de token incorrecto.")

        jti = payload.get("jti")
        if not jti:
            raise ValueError("Refresh token inválido.")

        refresh_repo = RefreshTokenRepository(db)
        token_row = refresh_repo.get_valid(jti)
        if not token_row:
            raise ValueError("Refresh token revocado o expirado.")

        user_id = int(payload["sub"])

        repo = UserRepository(db)
        user = repo.get_user_by_id(user_id)

        if not user or not user.is_active:
            raise ValueError("Usuario no encontrado o inactivo.")

        access = create_access_token(
            sub=user.id,
            role=user.role,
            gr=user.guardian_rank,
        )

        # 🔁 Rotación real
        refresh_repo.revoke(token_row)

        new_refresh = create_refresh_token(sub=user.id)
        refresh_repo.create(
            user_id=user.id,
            jti=new_refresh["jti"],
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return TokenPair(
            access_token=access,
            refresh_token=new_refresh["token"],
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh inválido.")



@router.get("/me", response_model=UserPublic)
def me(current: UserPublic = Depends(get_current_user)):
    return current
