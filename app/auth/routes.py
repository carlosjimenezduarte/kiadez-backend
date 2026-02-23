from app.core.security import decode_2fa_temp_token
from fastapi import Query
from app.core.security import create_2fa_temp_token
from app.db.repositories.user_2fa_repository import User2FARepository
import hashlib
import re
import secrets

from sqlalchemy.exc import IntegrityError
from datetime import date

from sqlalchemy import delete, or_, select, text


from app.db.models.user_2fa import User2FA
from app.db.models.account_closure_audit import (
    AccountClosureAudit,
    AccountClosureReason as AccountClosureReasonDB,
    AccountClosureRestoreMethod,
)
from app.db.models.achievement_unlock_event import AchievementUnlockEvent
from app.db.models.biography_about import BiographyAbout
from app.db.models.biography_curiosities import BiographyCuriosities
from app.db.models.biography_distinctions import BiographyDistinctions
from app.db.models.biography_dream import BiographyDream
from app.db.models.biography_education import BiographyEducation
from app.db.models.biography_favorite_quotes import BiographyFavoriteQuotes
from app.db.models.biography_life_achievements import BiographyLifeAchievements
from app.db.models.biography_personal_info import BiographyPersonalInfo
from app.db.models.biography_physical_traits import BiographyPhysicalTraits
from app.db.models.biography_professional_achievements import BiographyProfessionalAchievements
from app.db.models.biography_professional_info import BiographyProfessionalInfo
from app.db.models.gallery_folder import GalleryFolder
from app.db.models.guardian_wish_message import GuardianWishMessage
from app.db.models.guardian_wish_request import GuardianWishRequest
from app.db.models.life_purpose import LifePurpose
from app.db.models.media import Media
from app.db.models.message_entry import MessageEntry
from app.db.models.message_thread import MessageThread
from app.db.models.oracle import OracleResponse, OracleUserState
from app.db.models.post import Post, PostComment, PostReport, PostReportCase, PostStar
from app.db.models.private_personal_wish import PrivatePersonalWish
from app.db.models.public_cooperative_wish import PublicCooperativeWish
from app.db.models.public_cooperative_wish_fulfillment import PublicCooperativeWishFulfillment
from app.db.models.public_cooperative_wish_participation import PublicCooperativeWishParticipation
from app.db.models.public_personal_wish import PublicPersonalWish
from app.db.models.public_wish_fulfillment import PublicWishFulfillment
from app.db.models.user_follow import UserFollow

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
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi import Body


from app.db.repositories.refresh_token_repository import RefreshTokenRepository
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.mailer import (
    send_verification_email,
    send_password_reset_email,
    send_email_change_confirmation_email,
    send_email_change_security_alert_email,
    send_minor_account_accreditation_email,
)
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
    EmailChangeRequest,
    AccountClosureRequest,
    AccountClosureResponse,
    UsernameState,
    UsernameAvailabilityOut,
    UsernameUpdateRequest,
    UsernameUpdateResponse,
    MinorAccreditationRequest,
    MinorAccreditationStatusOut,
    MinorAccreditationRequestOut,
)
from .minor_accreditation import (
    MINOR_STATUS_APPROVED,
    MINOR_STATUS_NOT_REQUIRED,
    MINOR_STATUS_PENDING,
    MINOR_STATUS_REQUESTED,
    MINOR_RELATIONSHIP_VALUES,
    calculate_age,
    force_minor_private_profile_flags,
    is_minor_protected,
    is_underage,
    normalize_minor_relationship,
    resolve_minor_status,
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

USERNAME_PATTERN = re.compile(r"^[a-z0-9._]{4,30}$")
USERNAME_COOLDOWN_DAYS = 30
ACCOUNT_CLOSURE_GRACE_DAYS = 30
MINOR_ACCREDITATION_TOKEN_EXPIRE_DAYS = 7
USERNAME_RESERVED = {
    "admin",
    "support",
    "root",
    "api",
    "auth",
    "login",
    "register",
    "feed",
    "home",
    "home_user",
    "settings",
    "privacy",
}


def _normalize_username(raw: str) -> str:
    username = (raw or "").strip().lower()
    while username.startswith("@"):
        username = username[1:]
    return username


def _to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _next_username_change_at(user: User) -> datetime | None:
    if user.username_updated_at is None:
        return None
    return _to_utc(user.username_updated_at) + timedelta(days=USERNAME_COOLDOWN_DAYS)


def _validate_username_or_raise(username: str) -> None:
    if not USERNAME_PATTERN.match(username):
        raise HTTPException(
            status_code=400,
            detail="Nombre de usuario inválido. Usa 4-30 caracteres (a-z, 0-9, punto o guión bajo).",
        )
    if username in USERNAME_RESERVED:
        raise HTTPException(status_code=400, detail="Ese nombre de usuario está reservado.")


def _build_profile_url(username: str | None) -> str:
    if username:
        return f"/home_user.html?u={username}"
    return "/home_user.html"


def _hash_minor_approval_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _to_user_public(user: User) -> UserPublic:
    minor_status = resolve_minor_status(user)
    minor_required = minor_status != MINOR_STATUS_NOT_REQUIRED
    protected = is_minor_protected(user)
    return UserPublic(
        user_number=user.id,
        email=user.email,
        role=user.role,
        guardian_rank=user.guardian_rank,
        username=user.username,
        username_updated_at=user.username_updated_at,
        is_active=user.is_active,
        minor_accreditation_status=minor_status,
        minor_accreditation_required=minor_required,
        is_minor_protected=protected,
        can_publish_public=not protected,
    )


def _minor_status_out(user: User) -> MinorAccreditationStatusOut:
    status = resolve_minor_status(user)
    required = status != MINOR_STATUS_NOT_REQUIRED
    protected = status in {MINOR_STATUS_PENDING, MINOR_STATUS_REQUESTED}

    relationship_raw = (user.minor_guardian_relationship or "").strip().lower()
    relationship = relationship_raw if relationship_raw in MINOR_RELATIONSHIP_VALUES else None

    return MinorAccreditationStatusOut(
        required=required,
        status=status,
        is_minor_protected=protected,
        can_publish_public=not protected,
        guardian_phone=(user.minor_guardian_phone or None),
        guardian_email=(user.minor_guardian_email or None),
        relationship=relationship,
        requested_at=user.minor_accreditation_requested_at,
        approved_at=user.minor_accreditation_approved_at,
    )


def _sync_minor_protected_state(*, db: Session, user: User) -> User:
    changed = False

    resolved_status = resolve_minor_status(user)
    if (user.minor_accreditation_status or "").strip().lower() != resolved_status:
        user.minor_accreditation_status = resolved_status
        changed = True

    if resolved_status == MINOR_STATUS_NOT_REQUIRED:
        if user.minor_accreditation_token_hash is not None:
            user.minor_accreditation_token_hash = None
            changed = True
        if user.minor_accreditation_token_expires_at is not None:
            user.minor_accreditation_token_expires_at = None
            changed = True
    elif resolved_status == MINOR_STATUS_APPROVED:
        if user.minor_accreditation_token_hash is not None:
            user.minor_accreditation_token_hash = None
            changed = True
        if user.minor_accreditation_token_expires_at is not None:
            user.minor_accreditation_token_expires_at = None
            changed = True

    if force_minor_private_profile_flags(user):
        changed = True

    if changed:
        db.commit()
        db.refresh(user)

    return user


def _build_username_state(user: User, now: datetime | None = None) -> UsernameState:
    now_utc = now or datetime.now(timezone.utc)
    next_change_at = _next_username_change_at(user)
    can_update = next_change_at is None or now_utc >= next_change_at
    remaining_days = 0
    if not can_update and next_change_at is not None:
        remaining_days = max(1, int((next_change_at - now_utc).total_seconds() // 86400) + 1)

    return UsernameState(
        username=user.username,
        can_update=can_update,
        cooldown_until=next_change_at if not can_update else None,
        cooldown_remaining_days=remaining_days,
        profile_url=_build_profile_url(user.username),
    )


def _is_account_closure_pending(user: User, *, now: datetime) -> bool:
    requested_at = user.account_closure_requested_at
    deadline_at = user.account_closure_restore_deadline_at
    if requested_at is None or deadline_at is None:
        return False
    return _to_utc(deadline_at) >= now


def _mark_account_closure_restored(
    *,
    db: Session,
    user: User,
    now: datetime,
    method: AccountClosureRestoreMethod,
) -> None:
    user.is_active = True
    user.account_closure_requested_at = None
    user.account_closure_restore_deadline_at = None

    # Restore default visibility for users that return after closing their account.
    user.public_profile_show_about = True
    user.public_profile_show_fulfilled_wishes = True
    user.public_profile_show_public_wishes = True
    user.public_profile_show_calendar = True
    user.public_profile_show_oracle = True
    user.public_profile_show_personal_posts = True
    user.public_profile_show_cooperative_wishes = True
    user.public_profile_show_followers = True
    user.public_profile_show_gallery = True
    user.public_profile_show_recent_achievements = True
    user.public_profile_show_stars = True
    user.public_profile_show_cover_purposes = True
    user.public_profile_show_biography = True

    audit = db.execute(
        select(AccountClosureAudit)
        .where(
            AccountClosureAudit.user_id == user.id,
            AccountClosureAudit.restored_at.is_(None),
            AccountClosureAudit.purged_at.is_(None),
        )
        .order_by(AccountClosureAudit.requested_at.desc(), AccountClosureAudit.id.desc())
        .limit(1)
    ).scalar_one_or_none()
    if audit is not None:
        audit.restored_at = now
        audit.restore_method = method


def _recompute_post_counters(db: Session) -> None:
    db.execute(
        text(
            """
            UPDATE posts p
            SET star_count = COALESCE(s.star_count, 0)
            FROM (
                SELECT post_id, COUNT(*)::int AS star_count
                FROM post_stars
                GROUP BY post_id
            ) s
            WHERE p.id = s.post_id
            """
        )
    )
    db.execute(
        text(
            """
            UPDATE posts
            SET star_count = 0
            WHERE id NOT IN (SELECT DISTINCT post_id FROM post_stars)
            """
        )
    )

    db.execute(
        text(
            """
            UPDATE posts p
            SET comment_count = COALESCE(c.comment_count, 0)
            FROM (
                SELECT post_id, COUNT(*)::int AS comment_count
                FROM post_comments
                GROUP BY post_id
            ) c
            WHERE p.id = c.post_id
            """
        )
    )
    db.execute(
        text(
            """
            UPDATE posts
            SET comment_count = 0
            WHERE id NOT IN (SELECT DISTINCT post_id FROM post_comments)
            """
        )
    )

    db.execute(
        text(
            """
            UPDATE users u
            SET received_stars_total = COALESCE(t.total, 0)
            FROM (
                SELECT author_id, COALESCE(SUM(star_count), 0)::int AS total
                FROM posts
                GROUP BY author_id
            ) t
            WHERE u.id = t.author_id
            """
        )
    )
    db.execute(
        text(
            """
            UPDATE users
            SET received_stars_total = 0
            WHERE id NOT IN (SELECT DISTINCT author_id FROM posts)
            """
        )
    )
    db.execute(
        text(
            """
            UPDATE users
            SET donated_stars_total = LEAST(COALESCE(donated_stars_total, 0), COALESCE(received_stars_total, 0))
            """
        )
    )


def _purge_user_content_for_account_closure(*, db: Session, user_id: int) -> None:
    db.execute(delete(UserFollow).where(or_(UserFollow.follower_id == user_id, UserFollow.followed_id == user_id)))

    db.execute(text("UPDATE guardian_wish_requests SET guardian_id = NULL WHERE guardian_id = :user_id"), {"user_id": user_id})
    db.execute(
        text("UPDATE public_wish_fulfillments SET guardian_user_id = NULL WHERE guardian_user_id = :user_id"),
        {"user_id": user_id},
    )
    db.execute(
        text("UPDATE message_threads SET guardian_user_id = NULL WHERE guardian_user_id = :user_id"),
        {"user_id": user_id},
    )
    db.execute(
        text("UPDATE post_report_cases SET resolved_by_guardian_id = NULL WHERE resolved_by_guardian_id = :user_id"),
        {"user_id": user_id},
    )

    db.execute(delete(PostStar).where(PostStar.user_id == user_id))
    db.execute(delete(PostComment).where(PostComment.user_id == user_id))
    db.execute(delete(PostReport).where(PostReport.reporter_id == user_id))
    db.execute(delete(Post).where(Post.author_id == user_id))
    db.execute(delete(PostReportCase).where(PostReportCase.post_author_id == user_id))

    db.execute(delete(PublicCooperativeWishParticipation).where(PublicCooperativeWishParticipation.participant_user_id == user_id))
    db.execute(delete(PublicCooperativeWishFulfillment).where(PublicCooperativeWishFulfillment.wish_owner_user_id == user_id))
    db.execute(delete(PublicCooperativeWish).where(PublicCooperativeWish.user_id == user_id))

    db.execute(
        delete(PublicWishFulfillment).where(
            or_(
                PublicWishFulfillment.wish_owner_id == user_id,
                PublicWishFulfillment.fulfiller_user_id == user_id,
            )
        )
    )

    db.execute(
        delete(GuardianWishMessage).where(
            or_(
                GuardianWishMessage.recipient_user_id == user_id,
                GuardianWishMessage.sender_guardian_id == user_id,
            )
        )
    )
    db.execute(
        delete(GuardianWishRequest).where(
            or_(
                GuardianWishRequest.requester_id == user_id,
                GuardianWishRequest.wish_owner_id == user_id,
            )
        )
    )

    db.execute(delete(PublicPersonalWish).where(PublicPersonalWish.user_id == user_id))
    db.execute(delete(PrivatePersonalWish).where(PrivatePersonalWish.user_id == user_id))

    db.execute(delete(BiographyPersonalInfo).where(BiographyPersonalInfo.user_id == user_id))
    db.execute(delete(BiographyPhysicalTraits).where(BiographyPhysicalTraits.user_id == user_id))
    db.execute(delete(BiographyEducation).where(BiographyEducation.user_id == user_id))
    db.execute(delete(BiographyCuriosities).where(BiographyCuriosities.user_id == user_id))
    db.execute(delete(BiographyProfessionalInfo).where(BiographyProfessionalInfo.user_id == user_id))
    db.execute(delete(BiographyAbout).where(BiographyAbout.user_id == user_id))
    db.execute(delete(BiographyDream).where(BiographyDream.user_id == user_id))
    db.execute(delete(BiographyProfessionalAchievements).where(BiographyProfessionalAchievements.user_id == user_id))
    db.execute(delete(BiographyLifeAchievements).where(BiographyLifeAchievements.user_id == user_id))
    db.execute(delete(BiographyFavoriteQuotes).where(BiographyFavoriteQuotes.user_id == user_id))
    db.execute(delete(BiographyDistinctions).where(BiographyDistinctions.user_id == user_id))

    db.execute(delete(LifePurpose).where(LifePurpose.user_id == user_id))
    db.execute(delete(AchievementUnlockEvent).where(AchievementUnlockEvent.user_id == user_id))
    db.execute(delete(OracleResponse).where(OracleResponse.user_id == user_id))
    db.execute(delete(OracleUserState).where(OracleUserState.user_id == user_id))

    db.execute(delete(MessageEntry).where(MessageEntry.sender_user_id == user_id))
    db.execute(delete(MessageThread).where(MessageThread.recipient_user_id == user_id))

    db.execute(delete(GalleryFolder).where(GalleryFolder.owner_id == user_id))
    db.execute(delete(Media).where(Media.owner_id == user_id))

    _recompute_post_counters(db)


def _purge_expired_closed_accounts(*, db: Session, now: datetime) -> None:
    expired_users = db.execute(
        select(User)
        .where(
            User.is_active.is_(False),
            User.account_closure_requested_at.is_not(None),
            User.account_closure_restore_deadline_at.is_not(None),
            User.account_closure_restore_deadline_at < now,
        )
        .limit(50)
    ).scalars().all()

    if not expired_users:
        return

    for user in expired_users:
        db.execute(
            text(
                """
                UPDATE account_closure_audits
                SET purged_at = :purged_at, updated_at = :updated_at
                WHERE user_id = :user_id
                  AND restored_at IS NULL
                  AND purged_at IS NULL
                """
            ),
            {
                "purged_at": now,
                "updated_at": now,
                "user_id": user.id,
            },
        )
        db.delete(user)

    db.commit()

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

        user = _sync_minor_protected_state(db=db, user=user)
        return _to_user_public(user)
    except Exception:
        raise HTTPException(status_code=401, detail="No autorizado")


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

    initial_minor_status = MINOR_STATUS_PENDING if age < 18 else MINOR_STATUS_NOT_REQUIRED

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
        user.minor_accreditation_status = initial_minor_status
        if initial_minor_status != MINOR_STATUS_NOT_REQUIRED:
            force_minor_private_profile_flags(user)

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

    return _to_user_public(user)



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
    now_utc = datetime.now(timezone.utc)
    _purge_expired_closed_accounts(db=db, now=now_utc)

    repo = UserRepository(db)
    user = repo.get_user_by_email(data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not user.is_active:
        if not _is_account_closure_pending(user, now=now_utc):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        if not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        _mark_account_closure_restored(
            db=db,
            user=user,
            now=now_utc,
            method=AccountClosureRestoreMethod.login,
        )
        db.commit()
        db.refresh(user)
    else:
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


@router.get("/minor-accreditation/status", response_model=MinorAccreditationStatusOut)
def get_minor_accreditation_status(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="No autorizado")

    user = _sync_minor_protected_state(db=db, user=user)
    return _minor_status_out(user)


@router.post("/minor-accreditation/request", response_model=MinorAccreditationRequestOut)
def request_minor_accreditation(
    payload: MinorAccreditationRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="No autorizado")

    user = _sync_minor_protected_state(db=db, user=user)
    current_status = resolve_minor_status(user)

    if current_status == MINOR_STATUS_NOT_REQUIRED:
        return MinorAccreditationRequestOut(
            requested=False,
            status=MINOR_STATUS_NOT_REQUIRED,
            is_minor_protected=False,
            can_publish_public=True,
            message="Tu cuenta no requiere acreditación por edad.",
        )

    if current_status == MINOR_STATUS_APPROVED:
        return MinorAccreditationRequestOut(
            requested=False,
            status=MINOR_STATUS_APPROVED,
            is_minor_protected=False,
            can_publish_public=True,
            message="Tu cuenta ya fue acreditada por un adulto responsable.",
        )

    guardian_phone = " ".join((payload.guardian_phone or "").strip().split())
    guardian_email = str(payload.guardian_email or "").strip().lower()
    relationship = normalize_minor_relationship(payload.relationship)

    if not guardian_phone:
        raise HTTPException(status_code=400, detail="Debes registrar el teléfono del adulto responsable.")
    if not guardian_email:
        raise HTTPException(status_code=400, detail="Debes registrar el correo del adulto responsable.")

    token = secrets.token_urlsafe(32)
    token_hash = _hash_minor_approval_token(token)
    now_utc = datetime.now(timezone.utc)
    token_expires_at = now_utc + timedelta(days=MINOR_ACCREDITATION_TOKEN_EXPIRE_DAYS)

    user.minor_guardian_phone = guardian_phone
    user.minor_guardian_email = guardian_email
    user.minor_guardian_relationship = relationship
    user.minor_accreditation_status = MINOR_STATUS_REQUESTED
    user.minor_accreditation_requested_at = now_utc
    user.minor_accreditation_approved_at = None
    user.minor_accreditation_token_hash = token_hash
    user.minor_accreditation_token_expires_at = token_expires_at
    force_minor_private_profile_flags(user)

    db.commit()
    db.refresh(user)

    profile_username = (user.username or "").strip()
    if profile_username:
        minor_username = f"@{profile_username}"
    else:
        minor_username = f"{(user.first_name or '').strip()} {(user.last_name or '').strip()}".strip() or f"Usuario {user.id}"

    registration_date_label = (
        user.created_at.astimezone(timezone.utc).strftime("%Y-%m-%d")
        if user.created_at
        else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )
    approval_url = f"{settings.BACKEND_URL}/auth/minor-accreditation/approve?token={token}"

    try:
        send_minor_account_accreditation_email(
            to_email=guardian_email,
            minor_username=minor_username,
            minor_email=user.email,
            registration_date_label=registration_date_label,
            approval_url=approval_url,
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo enviar el correo de acreditación al adulto responsable.",
        )

    return MinorAccreditationRequestOut(
        requested=True,
        status=MINOR_STATUS_REQUESTED,
        is_minor_protected=True,
        can_publish_public=False,
        message="Solicitud enviada. El adulto responsable debe aprobarla desde el enlace seguro.",
    )


def _minor_approval_html(*, title: str, body: str, success: bool) -> HTMLResponse:
    safe_title = title.strip() or "Validación de cuenta"
    safe_body = body.strip() or "No se pudo procesar la solicitud."
    color = "#0b5f2a" if success else "#8f1e1e"
    status_code = 200 if success else 400
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>{safe_title}</title>
    </head>
    <body style="margin:0;padding:0;background:#0e1a14;font-family:Arial,Helvetica,sans-serif;">
      <main style="max-width:640px;margin:48px auto;padding:24px;background:#fff;border-radius:14px;">
        <h1 style="margin:0 0 12px;color:{color};font-size:24px;">{safe_title}</h1>
        <p style="margin:0;color:#1e1e1e;line-height:1.7;">{safe_body}</p>
      </main>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=status_code)


@router.get("/minor-accreditation/approve", response_class=HTMLResponse)
def approve_minor_accreditation(
    token: str = Query(..., min_length=24, max_length=255),
    db: Session = Depends(get_db),
):
    raw_token = (token or "").strip()
    if not raw_token:
        return _minor_approval_html(
            title="Enlace inválido",
            body="No se encontró un token válido de aprobación.",
            success=False,
        )

    token_hash = _hash_minor_approval_token(raw_token)
    now_utc = datetime.now(timezone.utc)

    user = db.execute(
        select(User).where(
            User.minor_accreditation_token_hash == token_hash,
            User.minor_accreditation_token_expires_at.is_not(None),
            User.minor_accreditation_token_expires_at >= now_utc,
        )
    ).scalar_one_or_none()
    if user is None:
        return _minor_approval_html(
            title="Enlace expirado o inválido",
            body="El enlace de aprobación ya no está disponible. Solicita uno nuevo desde la cuenta del menor.",
            success=False,
        )

    if not user.is_active:
        return _minor_approval_html(
            title="Cuenta no disponible",
            body="La cuenta del menor no está activa en este momento.",
            success=False,
        )

    if is_underage(user.birth_date):
        user.minor_accreditation_status = MINOR_STATUS_APPROVED
        user.minor_accreditation_approved_at = now_utc
        message = "La validación fue aprobada correctamente. La cuenta ya puede habilitar funciones públicas."
    else:
        user.minor_accreditation_status = MINOR_STATUS_NOT_REQUIRED
        user.minor_accreditation_approved_at = None
        message = "La cuenta ya no requiere validación por edad."

    user.minor_accreditation_token_hash = None
    user.minor_accreditation_token_expires_at = None

    db.commit()

    return _minor_approval_html(
        title="Validación completada",
        body=message,
        success=True,
    )


@router.get("/username", response_model=UsernameState)
def username_state(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current.user_number).one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="No autorizado")
    return _build_username_state(user)


@router.get("/username/check", response_model=UsernameAvailabilityOut)
def check_username_availability(
    username: str = Query(..., min_length=4, max_length=30),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    normalized = _normalize_username(username)
    _validate_username_or_raise(normalized)

    current_username = (current.username or "").strip().lower()
    if normalized == current_username:
        return UsernameAvailabilityOut(
            username=normalized,
            available=True,
            detail="Este ya es tu nombre de usuario actual.",
        )

    existing = (
        db.query(User.id)
        .filter(User.username == normalized, User.id != current.user_number)
        .first()
    )
    if existing:
        return UsernameAvailabilityOut(
            username=normalized,
            available=False,
            detail="Ese nombre de usuario ya está en uso.",
        )

    return UsernameAvailabilityOut(
        username=normalized,
        available=True,
        detail="Nombre de usuario disponible.",
    )


@router.put("/username", response_model=UsernameUpdateResponse)
def update_username(
    payload: UsernameUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current.user_number).one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="No autorizado")

    normalized = _normalize_username(payload.username)
    _validate_username_or_raise(normalized)

    if normalized == (user.username or ""):
        return UsernameUpdateResponse(
            updated=False,
            state=_build_username_state(user),
        )

    now_utc = datetime.now(timezone.utc)
    next_change_at = _next_username_change_at(user)
    if next_change_at is not None and now_utc < next_change_at:
        raise HTTPException(
            status_code=429,
            detail=f"Podrás modificar tu nombre de usuario nuevamente el {next_change_at.date().isoformat()}.",
        )

    existing = (
        db.query(User.id)
        .filter(User.username == normalized, User.id != current.user_number)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Ese nombre de usuario ya está en uso.")

    user.username = normalized
    user.username_updated_at = now_utc
    db.commit()
    db.refresh(user)

    return UsernameUpdateResponse(
        updated=True,
        state=_build_username_state(user, now=now_utc),
    )


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


@router.post("/email/change")
def change_email(
    payload: EmailChangeRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)
    user = repo.get_user_by_id(current.user_number)

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="No autorizado")

    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta.")

    new_email = payload.new_email.strip().lower()
    current_email = user.email.strip().lower()

    if new_email == current_email:
        raise HTTPException(status_code=400, detail="El nuevo correo debe ser distinto al actual.")

    existing = repo.get_user_by_email(new_email)
    if existing and existing.id != user.id:
        raise HTTPException(status_code=409, detail="El correo electrónico ya está registrado.")

    previous_email = user.email
    user.email = new_email

    # Seguridad: al cambiar correo, invalidamos refresh tokens existentes.
    db.execute(delete(RefreshToken).where(RefreshToken.user_id == user.id))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El correo electrónico ya está registrado.")

    delivery_issues: list[str] = []

    try:
        send_email_change_confirmation_email(
            to_email=user.email,
            previous_email=previous_email,
        )
    except Exception:
        delivery_issues.append("new")

    if previous_email.strip().lower() != user.email.strip().lower():
        try:
            send_email_change_security_alert_email(
                to_email=previous_email,
                new_email=user.email,
            )
        except Exception:
            delivery_issues.append("previous")

    if delivery_issues:
        return {
            "changed": True,
            "email": user.email,
            "message": "Correo actualizado, pero no se pudieron enviar todas las notificaciones de seguridad.",
        }

    return {
        "changed": True,
        "email": user.email,
        "message": "Correo actualizado correctamente. Enviamos confirmación al nuevo correo y alerta al correo anterior.",
    }


@router.post("/account/close", response_model=AccountClosureResponse)
def close_account(
    payload: AccountClosureRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    now_utc = datetime.now(timezone.utc)
    _purge_expired_closed_accounts(db=db, now=now_utc)

    repo = UserRepository(db)
    user = repo.get_user_by_id(current.user_number)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="No autorizado")

    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta.")

    other_reason = (payload.other_reason or "").strip()
    if payload.reason.value == "other" and not other_reason:
        raise HTTPException(status_code=400, detail="Debes especificar el motivo en “Otro”.")
    if payload.reason.value != "other":
        other_reason = ""

    try:
        reason_db = AccountClosureReasonDB(payload.reason.value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Motivo de cierre inválido.") from exc

    restore_deadline = now_utc + timedelta(days=ACCOUNT_CLOSURE_GRACE_DAYS)

    audit = AccountClosureAudit(
        user_id=user.id,
        user_email_snapshot=user.email,
        user_username_snapshot=user.username,
        reason=reason_db,
        other_reason=other_reason or None,
        requested_at=now_utc,
        restore_deadline_at=restore_deadline,
        created_at=now_utc,
        updated_at=now_utc,
    )
    db.add(audit)

    _purge_user_content_for_account_closure(db=db, user_id=user.id)

    user.public_profile_show_about = False
    user.public_profile_show_fulfilled_wishes = False
    user.public_profile_show_public_wishes = False
    user.public_profile_show_calendar = False
    user.public_profile_show_oracle = False
    user.public_profile_show_personal_posts = False
    user.public_profile_show_cooperative_wishes = False
    user.public_profile_show_followers = False
    user.public_profile_show_gallery = False
    user.public_profile_show_recent_achievements = False
    user.public_profile_show_stars = False
    user.public_profile_show_cover_purposes = False
    user.public_profile_show_biography = False
    user.account_closure_requested_at = now_utc
    user.account_closure_restore_deadline_at = restore_deadline
    user.is_active = False

    db.execute(delete(RefreshToken).where(RefreshToken.user_id == user.id))

    db.commit()
    return AccountClosureResponse(
        closed=True,
        restore_deadline_at=restore_deadline,
        message=(
            "Tu cuenta fue cerrada y tu información pública quedó inhabilitada. "
            "Tienes 30 días para volver a ingresar con tu clave o restaurarla. "
            "Después de ese plazo, la cuenta se eliminará de forma permanente."
        ),
    )


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
    now_utc = datetime.now(timezone.utc)
    _purge_expired_closed_accounts(db=db, now=now_utc)

    email = payload.email.strip().lower()

    # Respuesta genérica para evitar enumeración
    generic = {"message": "Si el correo existe, enviaremos un enlace de recuperación."}

    repo = UserRepository(db)
    user = repo.get_user_by_email(email)
    if not user:
        return generic
    if not user.is_active and not _is_account_closure_pending(user, now=now_utc):
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
    now_utc = datetime.now(timezone.utc)
    _purge_expired_closed_accounts(db=db, now=now_utc)

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

    if reset.expires_at < now_utc:
        raise HTTPException(status_code=400, detail="Token expirado.")

    repo = UserRepository(db)
    user = repo.get_user_by_id(reset.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario inválido.")

    restore_after_reset = False
    if not user.is_active:
        if not _is_account_closure_pending(user, now=now_utc):
            raise HTTPException(status_code=400, detail="Usuario inválido.")
        restore_after_reset = True

    validate_password_policy(payload.new_password)
    user.password_hash = hash_password(payload.new_password)
    if restore_after_reset:
        _mark_account_closure_restored(
            db=db,
            user=user,
            now=now_utc,
            method=AccountClosureRestoreMethod.password_reset,
        )
    reset.is_used = True

    db.commit()
    return {"reset": True}
