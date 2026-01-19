from app.core.security import decode_2fa_temp_token

from app.core.security import create_2fa_temp_token
from app.db.repositories.user_2fa_repository import User2FARepository

from fastapi import Depends, HTTPException

from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from datetime import date


from app.db.models.user_2fa import User2FA

from app.core.two_fa_totp import generate_totp_secret, build_totp_uri
from app.core.two_fa_crypto import encrypt_secret
from app.core.two_fa_qr import generate_qr_base64
from app.core.two_fa_crypto import decrypt_secret
from app.core.two_fa_totp import verify_totp_code

from app.core.config import settings

# SQLAlchemy
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.repositories.user_repository import UserRepository

# FastAPI
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi import Body


from app.db.repositories.refresh_token_repository import RefreshTokenRepository
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.mailer import send_verification_email



# Auth
from .models import RegisterRequest, LoginRequest, TokenPair, UserPublic,  TwoFAVerifyRequest
from app.core.security import (
    validate_password_policy,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

from app.db.models.email_verification_token import EmailVerificationToken
from app.core.email_verification import (
    generate_email_verification_token,
    get_email_verification_expiry,
)
from app.db.models.user import User

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

def calculate_age(birth_date: date) -> int:
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


@router.post("/register", response_model=UserPublic)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    # 1. Validar política de contraseña
    validate_password_policy(data.password)
    pw_hash = hash_password(data.password)

    # 2. Validar fecha de nacimiento
    birth_date = data.birth_date.date()

    if birth_date > date.today():
        raise HTTPException(
            status_code=400,
            detail="La fecha de nacimiento no es válida.",
        )

    # 3. Calcular edad
    age = calculate_age(birth_date)

    # 4. Decidir estado inicial
    #is_active = age >= 18

    repo = UserRepository(db)

    try:
        user = repo.create_user(
            email=data.email,
            password_hash=pw_hash,
            first_name=data.first_name,
            last_name=data.last_name,
            birth_date=birth_date,
            gender=data.gender,
            role="user",
            is_active=False
        )
        token = generate_email_verification_token()

        verification = EmailVerificationToken(
        user_id=user.id,
        token=token,
        expires_at=get_email_verification_expiry(),
    )

        db.add(verification)
        db.commit()

        send_verification_email(
            to_email=user.email,
            token=token,
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está registrado.",
        )

    return UserPublic(
        user_number=user.id,
        email=user.email,
        role=user.role,
        guardian_rank=user.guardian_rank,
        is_active=user.is_active,
    )



@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_user_by_email(data.email)

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # 🔐 Revisar si tiene 2FA activo
    two_fa_repo = User2FARepository(db)
    two_fa = two_fa_repo.get_by_user_id(user.id)

    if two_fa and two_fa.is_enabled:
        temp_token = create_2fa_temp_token(sub=user.id)
        return {
            "2fa_required": True,
            "temp_token": temp_token,
        }

    # 🟢 Login normal (sin 2FA)
    access = create_access_token(
        sub=user.id,
        role=user.role,
        gr=user.guardian_rank,
    )
    refresh = create_refresh_token(sub=user.id)

    return {
        "access_token": access,
        "refresh_token": refresh["token"],
        "token_type": "bearer",
    }


 
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

@router.post("/2fa/setup")
def setup_2fa(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 1. Verificar si ya existe 2FA activo
    existing = (
        db.query(User2FA)
        .filter(User2FA.user_id == current.user_number)
        .one_or_none()
    )

    if existing and existing.is_enabled:
        raise HTTPException(
            status_code=400,
            detail="2FA ya está habilitado para este usuario.",
        )

    # 2. Generar secreto TOTP
    secret = generate_totp_secret()

    # 3. Cifrar el secreto
    secret_encrypted = encrypt_secret(secret)

    # 4. Crear o actualizar registro user_2fa
    if existing:
        existing.secret_encrypted = secret_encrypted
        existing.is_enabled = False
        existing.is_confirmed = False
        existing.confirmed_at = None
        existing.created_at = datetime.now(timezone.utc)
        two_fa = existing
    else:
        two_fa = User2FA(
            user_id=current.user_number,
            method="totp",
            secret_encrypted=secret_encrypted,
            is_enabled=False,
            is_confirmed=False,
        )
        db.add(two_fa)

    db.commit()

    # 5. Construir URI otpauth://
    uri = build_totp_uri(
        secret=secret,
        email=current.email,
        issuer=settings.JWT_ISSUER,
    )

    # 6. Generar QR en base64
    qr_base64 = generate_qr_base64(uri)

    # 7. Responder (QR + código manual)
    return {
        "qr_code": f"data:image/png;base64,{qr_base64}",
        "manual_code": secret,
        "issuer": settings.JWT_ISSUER,
    }

@router.post("/2fa/confirm")
def confirm_2fa(
    code: str = Body(..., embed=True),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # 1. Buscar registro 2FA del usuario
    two_fa = (
        db.query(User2FA)
        .filter(User2FA.user_id == current.user_number)
        .one_or_none()
    )

    if not two_fa:
        raise HTTPException(
            status_code=400,
            detail="2FA no está configurado para este usuario.",
        )

    if two_fa.is_enabled:
        raise HTTPException(
            status_code=400,
            detail="2FA ya está habilitado.",
        )

    # 2. Descifrar el secreto
    secret = decrypt_secret(two_fa.secret_encrypted)

    # 3. Verificar el código TOTP
    if not verify_totp_code(secret=secret, code=code):
        raise HTTPException(
            status_code=400,
            detail="Código 2FA inválido.",
        )

    # 4. Activar oficialmente 2FA
    now = datetime.now(timezone.utc)
    two_fa.is_enabled = True
    two_fa.is_confirmed = True
    two_fa.confirmed_at = now
    two_fa.last_used_at = now

    db.commit()

    return {
        "2fa_enabled": True,
        "confirmed_at": now.isoformat(),
    }

@router.post("/2fa/verify")
def verify_2fa(
    data: TwoFAVerifyRequest,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    # Extraer token
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token inválido")

    temp_token = authorization.replace("Bearer ", "")

    try:
        user_id = decode_2fa_temp_token(temp_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token 2FA inválido")

    repo = UserRepository(db)
    user = repo.get_user_by_id(user_id)

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario inválido")

    # Validar TOTP
    two_fa_repo = User2FARepository(db)
    two_fa = two_fa_repo.get_by_user_id(user.id)

    if not two_fa or not two_fa.is_enabled:
        raise HTTPException(status_code=400, detail="2FA no configurado")

    secret = decrypt_secret(two_fa.secret_encrypted)

    if not verify_totp_code(secret=secret, code=data.code):

        raise HTTPException(status_code=401, detail="Código incorrecto")


    # 🎉 Login exitoso
    access = create_access_token(
        sub=user.id,
        role=user.role,
        gr=user.guardian_rank,
    )
    refresh = create_refresh_token(sub=user.id)

    return {
        "access_token": access,
        "refresh_token": refresh["token"],
        "token_type": "bearer",
    }

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    verification = (
        db.query(EmailVerificationToken)
        .filter(EmailVerificationToken.token == token)
        .first()
    )

    if not verification:
        raise HTTPException(status_code=400, detail="Token inválido")

    if verification.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expirado")

    user = db.query(User).filter(User.id == verification.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.is_active = True
    db.delete(verification)
    db.commit()

    return RedirectResponse(
        url=f"{settings.FRONTEND_URL}/email-verified.html",
        status_code=302
    )
