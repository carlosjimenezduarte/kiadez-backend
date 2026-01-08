from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from .models import RegisterRequest, LoginRequest, TokenPair, UserPublic
from .store import store
from app.core.security import (
    validate_password_policy, hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # aunque login sea JSON, sirve para dependencia

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserPublic:
    try:
        payload = decode_token(token)
        if payload.get("typ") != "access":
            raise ValueError("Tipo de token incorrecto.")
        sub = int(payload["sub"])
        user = store.get_user_by_number(sub)
        if not user or not user.is_active:
            raise ValueError("Usuario no encontrado o inactivo.")
        return UserPublic(
            user_number=user.user_number,
            email=user.email,
            role=user.role,
            guardian_rank=user.guardian_rank,
            is_active=user.is_active,
        )
    except Exception:
        raise HTTPException(status_code=401, detail="No autorizado")

@router.post("/register", response_model=UserPublic)
def register(data: RegisterRequest):
    try:
        validate_password_policy(data.password)
        pw_hash = hash_password(data.password)
        user = store.create_user(email=data.email, password_hash=pw_hash, role="user")
        return UserPublic(
            user_number=user.user_number,
            email=user.email,
            role=user.role,
            guardian_rank=user.guardian_rank,
            is_active=user.is_active,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenPair)
def login(data: LoginRequest):
    user = store.get_user_by_email(data.email)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    access = create_access_token(sub=user.user_number, role=user.role, gr=user.guardian_rank)
    refresh = create_refresh_token(sub=user.user_number)
    store.add_refresh_jti(refresh["jti"])

    return TokenPair(access_token=access, refresh_token=refresh["token"])

@router.post("/refresh", response_model=TokenPair)
def refresh(refresh_token: str):
    # Nota: lo recibimos simple por ahora. Luego lo recibimos en body estructurado.
    try:
        payload = decode_token(refresh_token)
        if payload.get("typ") != "refresh":
            raise ValueError("Tipo de token incorrecto.")
        jti = payload.get("jti")
        if not jti or not store.has_refresh_jti(jti):
            raise ValueError("Refresh token revocado o desconocido.")

        sub = int(payload["sub"])
        user = store.get_user_by_number(sub)
        if not user or not user.is_active:
            raise ValueError("Usuario no encontrado o inactivo.")

        access = create_access_token(sub=user.user_number, role=user.role, gr=user.guardian_rank)

        # Rotación simple del refresh (recomendado):
        store.revoke_refresh_jti(jti)
        new_refresh = create_refresh_token(sub=user.user_number)
        store.add_refresh_jti(new_refresh["jti"])

        return TokenPair(access_token=access, refresh_token=new_refresh["token"])
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh inválido.")

@router.get("/me", response_model=UserPublic)
def me(current: UserPublic = Depends(get_current_user)):
    return current
