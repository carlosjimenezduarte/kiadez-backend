from app.core.security import decode_2fa_temp_token
from fastapi import Query
from app.core.security import create_2fa_temp_token
from app.db.repositories.user_2fa_repository import User2FARepository

from sqlalchemy.exc import IntegrityError
from datetime import date

from sqlalchemy import delete


from app.db.models.user_2fa import User2FA

from app.core.two_fa_totp import generate_totp_secret, build_totp_uri
from app.core.two_fa_crypto import encrypt_secret
from app.core.two_fa_qr import generate_qr_base64
from app.core.two_fa_crypto import decrypt_secret
from app.core.two_fa_totp import verify_totp_code



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
from app.core.mailer import send_verification_email, send_password_reset_email
from app.core.password_reset import generate_password_reset_token, get_password_reset_expiry



# Auth
from .models import (
    RegisterRequest,
    LoginRequest,
    TokenPair,
    UserPublic,
    TwoFAVerifyRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChangeRequest,
)
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
from app.db.models.password_reset_token import PasswordResetToken
from app.db.models.refresh_token import RefreshToken

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



@router.get("/verification-status")
def verification_status(
    email: str = Query(..., min_length=3, max_length=320),
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)
    user = repo.get_user_by_email(email.strip().lower())

    # Importante: no revelamos si el usuario existe o no.
    # Solo decimos "verified true/false".
    return {"verified": bool(user and user.is_active)}


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


@router.post("/password/change")
def change_password(
    payload: PasswordChangeRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)
    user = repo.get_user_by_id(current.user_number)

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="No autorizado")

    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta.")

    if payload.new_password != payload.new_password_confirm:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden.")

    try:
        validate_password_policy(payload.new_password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    user.password_hash = hash_password(payload.new_password)

    # Seguridad: al cambiar la contraseña, invalidamos refresh tokens existentes (otras sesiones).
    db.execute(delete(RefreshToken).where(RefreshToken.user_id == user.id))

    db.commit()
    return {"changed": True}

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


@router.get("/2fa/status")
def two_fa_status(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    two_fa_repo = User2FARepository(db)
    two_fa = two_fa_repo.get_by_user_id(current.user_number)
    if not two_fa:
        return {
            "has_2fa": False,
            "is_enabled": False,
            "is_confirmed": False,
        }

    return {
        "has_2fa": True,
        "method": two_fa.method,
        "is_enabled": bool(two_fa.is_enabled),
        "is_confirmed": bool(two_fa.is_confirmed),
        "created_at": two_fa.created_at.isoformat() if two_fa.created_at else None,
        "confirmed_at": two_fa.confirmed_at.isoformat() if two_fa.confirmed_at else None,
        "last_used_at": two_fa.last_used_at.isoformat() if two_fa.last_used_at else None,
    }


@router.post("/2fa/disable")
def disable_2fa(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    two_fa = (
        db.query(User2FA)
        .filter(User2FA.user_id == current.user_number)
        .one_or_none()
    )

    if not two_fa:
        return {"disabled": True}

    two_fa.is_enabled = False
    two_fa.is_confirmed = False
    two_fa.confirmed_at = None
    two_fa.last_used_at = None

    db.commit()
    return {"disabled": True}

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
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    # 1. Buscar el token
    verification = (
        db.query(EmailVerificationToken)
        .filter(EmailVerificationToken.token == token)
        .first()
    )
    if not verification:
        # Redirect bonito al frontend (puedes crear invalid-token.html si quieres)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/email-verified.html?status=invalid", status_code=302)

    # 2. Verificar expiración
    if verification.expires_at < datetime.now(timezone.utc):
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/email-verified.html?status=expired", status_code=302)

    # 3. Buscar usuario
    user = db.query(User).filter(User.id == verification.user_id).first()
    if not user:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/email-verified.html?status=notfound", status_code=302)

    # 4. Activar usuario
    user.is_active = True

    # 5. Eliminar token (uso único)
    db.delete(verification)

    # 6. Persistir cambios
    db.commit()

    # 7. Redirect final al frontend (le pasamos email para autocompletar login)
    return RedirectResponse(
        url=f"{settings.FRONTEND_URL}/email-verified.html?status=ok&email={user.email}",
        status_code=302,
    )

@router.post("/resend-verification")
def resend_verification(
    email: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    email = email.strip().lower()

    repo = UserRepository(db)
    user = repo.get_user_by_email(email)

    # Respuesta genérica SIEMPRE (seguridad: no revelamos si existe)
    generic = {"message": "Si el correo existe y no está verificado, enviaremos un nuevo enlace."}

    if not user:
        return generic

    if user.is_active:
        return generic

    # Borrar tokens viejos del usuario (simple y sano)
    db.execute(
        delete(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id)
    )

    # Crear token nuevo
    token = generate_email_verification_token()
    verification = EmailVerificationToken(
        user_id=user.id,
        token=token,
        expires_at=get_email_verification_expiry(),
    )
    db.add(verification)
    db.commit()

    # Enviar correo
    try:
        from app.core.mailer import send_verification_email
        send_verification_email(to_email=user.email, token=token)
    except Exception:
        # El token quedó creado; si falla el SMTP, no exponemos detalles
        raise HTTPException(status_code=500, detail="No se pudo enviar el correo en este momento.")

    return {"message": "Listo. Si tu correo no estaba verificado, enviamos un enlace nuevo."}


@router.post("/password-reset/request")
def request_password_reset(
    payload: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    email = payload.email.strip().lower()

    # Respuesta genérica para evitar enumeración
    generic = {"message": "Si el correo existe, enviaremos un enlace de recuperación."}

    repo = UserRepository(db)
    user = repo.get_user_by_email(email)
    if not user or not user.is_active:
        return generic

    # limpiar tokens previos
    db.execute(
        delete(PasswordResetToken).where(PasswordResetToken.user_id == user.id)
    )

    token = generate_password_reset_token()
    reset = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=get_password_reset_expiry(settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES),
    )
    db.add(reset)
    db.commit()

    try:
        send_password_reset_email(to_email=user.email, token=token)
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo enviar el correo.")

    return generic


@router.post("/password-reset/confirm")
def confirm_password_reset(
    payload: PasswordResetConfirm,
    db: Session = Depends(get_db),
):
    token = payload.token.strip()
    if not token:
        raise HTTPException(status_code=400, detail="Token inválido.")

    reset = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token == token)
        .one_or_none()
    )

    if not reset or reset.is_used:
        raise HTTPException(status_code=400, detail="Token inválido o usado.")

    if reset.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expirado.")

    repo = UserRepository(db)
    user = repo.get_user_by_id(reset.user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inválido.")

    validate_password_policy(payload.new_password)
    user.password_hash = hash_password(payload.new_password)
    reset.is_used = True

    db.commit()
    return {"reset": True}
