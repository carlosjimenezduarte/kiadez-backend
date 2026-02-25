from __future__ import annotations

from datetime import datetime, timezone
from math import ceil
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case, delete, desc, func, select, update
from sqlalchemy.orm import Session

from app.auth.minor_accreditation import is_minor_protected
from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.config import settings
from app.core.storage import S3NotConfiguredError, generate_presigned_get_url
from app.db.database import get_db
from app.db.models.guardian_wish_message import GuardianWishMessage, GuardianWishMessageKind
from app.db.models.guardian_wish_request import GuardianWishRequest, GuardianWishRequestStatus
from app.db.models.message_entry import MessageEntry
from app.db.models.message_thread import MessageThread
from app.db.models.media import Media
from app.db.models.post import Post, PostReport, PostReportCase, PostReportCaseStatus
from app.db.models.profile_report import ProfileReport, ProfileReportCase, ProfileReportCaseStatus
from app.db.models.public_personal_wish import PublicPersonalWish, PublicPersonalWishStatus
from app.db.models.refresh_token import RefreshToken
from app.db.models.user import User
from app.guardian_center.schemas import (
    GuardianRankPromotionOut,
    GuardianRankUserOut,
    GuardianReportedPostListOut,
    GuardianReportedPostOut,
    GuardianReportedPostReportOut,
    GuardianReportedProfileListOut,
    GuardianReportedProfileOut,
    GuardianReportedProfilePostListOut,
    GuardianReportedProfilePostOut,
    GuardianReportedProfileReportOut,
    GuardianWishMessageOut,
    GuardianWishRequestCreate,
    GuardianWishRequestDenyInput,
    GuardianWishRequestListOut,
    GuardianWishRequestOwnerMessageInput,
    GuardianWishRequestOut,
    GuardianWishRequestUserOut,
)

router = APIRouter(prefix="/guardian-center", tags=["guardian-center"])

GUARDIANS_MIN_RANK = 3
GUARDIANS_MAX_RANK = 8
GUARDIAN_RANK_NAMES: dict[int, str] = {
    0: "Sin rango",
    1: "Aspirante",
    2: "Aprendiz",
    3: "Guardián",
    4: "Guardián Consagrado",
    5: "Guardián Mayor",
    6: "Guardián del Logos",
    7: "Guardián del Umbral",
    8: "Guardián de Guardianes",
}
ACCOUNT_MODERATION_STATUS_ACTIVE = "active"
ACCOUNT_MODERATION_STATUS_SUSPENDED = "suspended"
ACCOUNT_MODERATION_STATUS_CLOSED = "closed"
PAGE_SIZE_DEFAULT = 10
PAGE_SIZE_MAX = 25
REPORTED_POSTS_PAGE_SIZE_DEFAULT = 10
REPORTED_POSTS_PAGE_SIZE_MAX = 25
REPORTED_PROFILES_PAGE_SIZE_DEFAULT = 10
REPORTED_PROFILES_PAGE_SIZE_MAX = 25
REPORTED_PROFILE_POSTS_PAGE_SIZE_DEFAULT = 10
REPORTED_PROFILE_POSTS_PAGE_SIZE_MAX = 25


def _require_guardian(current: UserPublic) -> None:
    rank = int(current.guardian_rank or 0)
    if rank < GUARDIANS_MIN_RANK:
        raise HTTPException(status_code=403, detail="Acceso restringido (rango de Guardián requerido).")


def _build_profile_url(username: str | None, *, user_id: int) -> str:
    normalized = (username or "").strip()
    if normalized:
        return f"/home_user.html?u={normalized}"
    return f"/home_user.html?id={int(user_id)}"


def _build_handle(*, username: str | None, user_id: int) -> str:
    normalized = (username or "").strip()
    if normalized:
        return f"@{normalized}"
    return f"@id{int(user_id)}"


def _guardian_rank_name(rank: int) -> str:
    return GUARDIAN_RANK_NAMES.get(int(rank), f"Rango {int(rank)}")


def _normalize_account_moderation_status(raw: str | None) -> str:
    value = str(raw or "").strip().lower()
    if value in {
        ACCOUNT_MODERATION_STATUS_SUSPENDED,
        ACCOUNT_MODERATION_STATUS_CLOSED,
    }:
        return value
    return ACCOUNT_MODERATION_STATUS_ACTIVE


def _set_profile_case_reviewed(
    *,
    item: ProfileReportCase,
    guardian_user_id: int,
    now: datetime,
) -> None:
    item.status = ProfileReportCaseStatus.reviewed
    item.resolved_at = now
    item.resolved_by_guardian_id = int(guardian_user_id)
    item.updated_at = now


def _parse_rank_lookup_query(raw: str) -> tuple[int | None, str | None]:
    normalized = str(raw or "").strip()
    if not normalized:
        raise HTTPException(status_code=400, detail="Debes escribir un @id o @username.")

    while normalized.startswith("@"):
        normalized = normalized[1:]
    normalized = normalized.strip().lower()
    if not normalized:
        raise HTTPException(status_code=400, detail="Debes escribir un @id o @username.")

    if normalized.startswith("id"):
        suffix = normalized[2:].strip()
        if suffix.isdigit():
            return int(suffix), None
    if normalized.isdigit():
        return int(normalized), None
    return None, normalized


def _rank_user_out(*, user: User, current_user_id: int) -> GuardianRankUserOut:
    base = _user_out(user)
    current_rank = max(0, int(user.guardian_rank or 0))
    next_rank = current_rank + 1 if current_rank < GUARDIANS_MAX_RANK else None
    return GuardianRankUserOut(
        user_id=base.user_id,
        full_name=base.full_name,
        username=base.username,
        handle=base.handle,
        profile_url=base.profile_url,
        role=str(user.role or "user"),
        guardian_rank=current_rank,
        guardian_rank_name=_guardian_rank_name(current_rank),
        next_guardian_rank=next_rank,
        next_guardian_rank_name=(_guardian_rank_name(next_rank) if next_rank is not None else None),
        can_promote=(next_rank is not None),
        is_self=(int(user.id) == int(current_user_id)),
    )


def _build_wish_url(*, wish_owner: User, wish_id: int) -> str:
    qp: dict[str, str] = {"wish": str(int(wish_id))}
    username = (wish_owner.username or "").strip()
    if username:
        qp["u"] = username
    else:
        qp["id"] = str(int(wish_owner.id))
    return f"/my-public-whishes.html?{urlencode(qp)}"


def _build_post_url(*, post_author: User, post_id: int | None) -> str | None:
    if not post_id:
        return None
    qp: dict[str, str] = {"post": str(int(post_id))}
    username = (post_author.username or "").strip()
    if username:
        qp["u"] = username
    else:
        qp["id"] = str(int(post_author.id))
    return f"/home_user.html?{urlencode(qp)}"


def _build_commitment_code(request_id: int) -> str:
    return f"KZ-204-{int(request_id):05d}"


def _build_media_url(media: Media | None) -> str | None:
    if not media or media.status != "ready":
        return None
    try:
        return generate_presigned_get_url(
            key=media.object_key,
            expires_in=settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600,
        )
    except S3NotConfiguredError:
        return None
    except Exception:
        return None


def _resolve_owned_media(*, db: Session, media_id: int, user_id: int) -> Media:
    media = db.execute(select(Media).where(Media.id == media_id)).scalar_one_or_none()
    if media is None:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if int(media.owner_id) != int(user_id):
        raise HTTPException(status_code=403, detail="No autorizado para usar esta media.")
    if media.status != "ready":
        raise HTTPException(status_code=409, detail="Media aún no disponible.")
    return media


def _resolve_wish_request_for_guardian_action(
    *,
    db: Session,
    request_id: int,
    guardian_user_id: int,
    allow_closed: bool = False,
) -> GuardianWishRequest:
    req = db.execute(
        select(GuardianWishRequest).where(GuardianWishRequest.id == request_id)
    ).scalar_one_or_none()
    if req is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    assigned_guardian_id = int(req.guardian_id) if req.guardian_id else None
    if assigned_guardian_id is not None and assigned_guardian_id != int(guardian_user_id):
        raise HTTPException(status_code=409, detail="Esta solicitud ya fue asumida por otro Guardián.")

    if not allow_closed and req.status == GuardianWishRequestStatus.closed:
        raise HTTPException(status_code=409, detail="Esta solicitud ya está cerrada.")

    if req.guardian_id is None:
        req.guardian_id = int(guardian_user_id)

    return req


def _load_related_maps_for_request(
    *,
    db: Session,
    req: GuardianWishRequest,
) -> tuple[dict[int, User], dict[int, Media]]:
    user_ids = {
        int(req.requester_id),
        int(req.wish_owner_id),
    }
    if req.guardian_id:
        user_ids.add(int(req.guardian_id))

    media_ids: set[int] = set()
    if req.evidence_media_id:
        media_ids.add(int(req.evidence_media_id))

    users = db.execute(select(User).where(User.id.in_(sorted(user_ids)))).scalars().all()
    users_map = {int(user.id): user for user in users}

    medias_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(sorted(media_ids)))).scalars().all()
        medias_map = {int(media.id): media for media in medias}

    return users_map, medias_map


def _user_out(user: User) -> GuardianWishRequestUserOut:
    first_name = (user.first_name or "").strip()
    last_name = (user.last_name or "").strip()
    full_name = f"{first_name} {last_name}".strip() or f"Usuario {user.id}"
    username = (user.username or "").strip() or None
    return GuardianWishRequestUserOut(
        user_id=int(user.id),
        full_name=full_name,
        username=username,
        handle=_build_handle(username=username, user_id=int(user.id)),
        profile_url=_build_profile_url(username, user_id=int(user.id)),
    )


def _request_out(
    *,
    req: GuardianWishRequest,
    users: dict[int, User],
    medias: dict[int, Media],
) -> GuardianWishRequestOut:
    requester = users.get(int(req.requester_id))
    wish_owner = users.get(int(req.wish_owner_id))
    if requester is None or wish_owner is None:
        raise HTTPException(status_code=500, detail="No se pudo construir la respuesta (usuarios faltantes).")

    guardian = users.get(int(req.guardian_id)) if req.guardian_id else None
    evidence_media = medias.get(int(req.evidence_media_id)) if req.evidence_media_id else None

    return GuardianWishRequestOut(
        id=int(req.id),
        status=req.status,
        created_at=req.created_at,
        updated_at=req.updated_at,
        requester=_user_out(requester),
        guardian=_user_out(guardian) if guardian else None,
        wish_owner=_user_out(wish_owner),
        public_wish_id=int(req.public_wish_id),
        wish_text=req.wish_text,
        wish_type=req.wish_type,
        wish_url=_build_wish_url(wish_owner=wish_owner, wish_id=int(req.public_wish_id)),
        reason=req.reason,
        contact_phone=req.contact_phone,
        contact_email=req.contact_email,
        evidence_media_id=int(req.evidence_media_id) if req.evidence_media_id else None,
        evidence_mime_type=(evidence_media.mime_type if evidence_media else None),
        evidence_url=_build_media_url(evidence_media),
        commitment_code=(str(req.commitment_code).strip() if req.commitment_code else None),
        commitment_sealed_at=req.commitment_sealed_at,
        denied_at=req.denied_at,
    )


def _message_out(*, msg: GuardianWishMessage, recipient: User) -> GuardianWishMessageOut:
    return GuardianWishMessageOut(
        id=int(msg.id),
        wish_request_id=int(msg.wish_request_id),
        kind=msg.kind,
        recipient_user_id=int(recipient.id),
        recipient_handle=_build_handle(username=recipient.username, user_id=int(recipient.id)),
        subject=msg.subject,
        body=msg.body,
        created_at=msg.created_at,
    )


def _load_reporter_handles(
    *,
    db: Session,
    case_ids: list[int],
) -> dict[int, list[GuardianReportedPostReportOut]]:
    if not case_ids:
        return {}

    rows = db.execute(
        select(PostReport, User)
        .join(User, User.id == PostReport.reporter_id)
        .where(PostReport.case_id.in_(case_ids))
        .order_by(desc(PostReport.created_at), desc(PostReport.id))
    ).all()

    out: dict[int, list[GuardianReportedPostReportOut]] = {}
    for report, reporter in rows:
        case_id = int(report.case_id)
        bucket = out.setdefault(case_id, [])
        if len(bucket) >= 5:
            continue
        bucket.append(
            GuardianReportedPostReportOut(
                id=int(report.id),
                reporter_user_id=int(reporter.id),
                reporter_handle=_build_handle(username=reporter.username, user_id=int(reporter.id)),
                reason=report.reason,
                other_reason=(report.other_reason or None),
                created_at=report.created_at,
            )
        )
    return out


def _reported_post_out(
    *,
    item: PostReportCase,
    users: dict[int, User],
    medias: dict[int, Media],
    reports_map: dict[int, list[GuardianReportedPostReportOut]],
) -> GuardianReportedPostOut:
    author = users.get(int(item.post_author_id)) if item.post_author_id else None
    if author is None:
        raise HTTPException(status_code=500, detail="No se pudo construir el reporte (autor faltante).")

    resolver = users.get(int(item.resolved_by_guardian_id)) if item.resolved_by_guardian_id else None
    media = medias.get(int(item.post_media_id_snapshot)) if item.post_media_id_snapshot else None

    return GuardianReportedPostOut(
        id=int(item.id),
        status=item.status,
        report_count=max(0, int(item.report_count or 0)),
        post_id=int(item.post_id) if item.post_id else None,
        post_text=item.post_text_snapshot,
        post_media_kind=item.post_media_kind_snapshot,
        post_media_url=_build_media_url(media),
        post_author=_user_out(author),
        resolved_by_guardian=_user_out(resolver) if resolver else None,
        first_reported_at=item.first_reported_at,
        last_reported_at=item.last_reported_at,
        resolved_at=item.resolved_at,
        reports=reports_map.get(int(item.id), []),
    )


def _load_related_maps_for_report_cases(
    *,
    db: Session,
    items: list[PostReportCase],
) -> tuple[dict[int, User], dict[int, Media], dict[int, list[GuardianReportedPostReportOut]]]:
    user_ids: set[int] = set()
    media_ids: set[int] = set()
    case_ids: list[int] = []

    for item in items:
        case_ids.append(int(item.id))
        if item.post_author_id:
            user_ids.add(int(item.post_author_id))
        if item.resolved_by_guardian_id:
            user_ids.add(int(item.resolved_by_guardian_id))
        if item.post_media_id_snapshot:
            media_ids.add(int(item.post_media_id_snapshot))

    users_map: dict[int, User] = {}
    if user_ids:
        users = db.execute(select(User).where(User.id.in_(sorted(user_ids)))).scalars().all()
        users_map = {int(user.id): user for user in users}

    medias_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(sorted(media_ids)))).scalars().all()
        medias_map = {int(media.id): media for media in medias}

    reports_map = _load_reporter_handles(db=db, case_ids=case_ids)
    return users_map, medias_map, reports_map


def _load_profile_reporter_handles(
    *,
    db: Session,
    case_ids: list[int],
) -> dict[int, list[GuardianReportedProfileReportOut]]:
    if not case_ids:
        return {}

    rows = db.execute(
        select(ProfileReport, User)
        .join(User, User.id == ProfileReport.reporter_id)
        .where(ProfileReport.case_id.in_(case_ids))
        .order_by(desc(ProfileReport.created_at), desc(ProfileReport.id))
    ).all()

    out: dict[int, list[GuardianReportedProfileReportOut]] = {}
    for report, reporter in rows:
        case_id = int(report.case_id)
        bucket = out.setdefault(case_id, [])
        if len(bucket) >= 5:
            continue
        bucket.append(
            GuardianReportedProfileReportOut(
                id=int(report.id),
                reporter_user_id=int(reporter.id),
                reporter_handle=_build_handle(username=reporter.username, user_id=int(reporter.id)),
                reason=report.reason,
                other_reason=(report.other_reason or None),
                created_at=report.created_at,
            )
        )
    return out


def _load_related_maps_for_profile_report_cases(
    *,
    db: Session,
    items: list[ProfileReportCase],
) -> tuple[dict[int, User], dict[int, list[GuardianReportedProfileReportOut]]]:
    user_ids: set[int] = set()
    case_ids: list[int] = []

    for item in items:
        case_ids.append(int(item.id))
        if item.reported_user_id:
            user_ids.add(int(item.reported_user_id))
        if item.resolved_by_guardian_id:
            user_ids.add(int(item.resolved_by_guardian_id))

    users_map: dict[int, User] = {}
    if user_ids:
        users = db.execute(select(User).where(User.id.in_(sorted(user_ids)))).scalars().all()
        users_map = {int(user.id): user for user in users}

    moderator_user_ids: set[int] = set()
    for item in items:
        reported_user = users_map.get(int(item.reported_user_id)) if item.reported_user_id else None
        if reported_user is None or not reported_user.guardian_moderated_by_user_id:
            continue
        moderator_user_ids.add(int(reported_user.guardian_moderated_by_user_id))

    missing_moderator_ids = sorted(moderator_user_ids.difference(users_map.keys()))
    if missing_moderator_ids:
        moderators = db.execute(select(User).where(User.id.in_(missing_moderator_ids))).scalars().all()
        for moderator in moderators:
            users_map[int(moderator.id)] = moderator

    reports_map = _load_profile_reporter_handles(db=db, case_ids=case_ids)
    return users_map, reports_map


def _reported_profile_post_out(
    *,
    item: PostReportCase,
    post_author: User,
) -> GuardianReportedProfilePostOut:
    return GuardianReportedProfilePostOut(
        id=int(item.id),
        status=item.status,
        report_count=max(0, int(item.report_count or 0)),
        post_id=int(item.post_id) if item.post_id else None,
        post_text=item.post_text_snapshot,
        post_media_kind=item.post_media_kind_snapshot,
        post_author=_user_out(post_author),
        post_url=_build_post_url(post_author=post_author, post_id=(int(item.post_id) if item.post_id else None)),
        first_reported_at=item.first_reported_at,
        last_reported_at=item.last_reported_at,
    )


def _load_reported_posts_for_profile(
    *,
    db: Session,
    reported_user: User,
    page: int = 1,
    page_size: int = REPORTED_PROFILE_POSTS_PAGE_SIZE_DEFAULT,
) -> GuardianReportedProfilePostListOut:
    total = int(
        db.execute(
            select(func.count(PostReportCase.id)).where(PostReportCase.post_author_id == int(reported_user.id))
        ).scalar_one()
        or 0
    )
    normalized_size = max(1, min(int(page_size), REPORTED_PROFILE_POSTS_PAGE_SIZE_MAX))
    total_pages = max(1, ceil(total / normalized_size)) if total else 1
    normalized_page = max(1, min(int(page), total_pages))
    offset = (normalized_page - 1) * normalized_size

    status_priority = case(
        (PostReportCase.status == PostReportCaseStatus.open, 0),
        else_=1,
    )
    rows = db.execute(
        select(PostReportCase)
        .where(PostReportCase.post_author_id == int(reported_user.id))
        .order_by(status_priority.asc(), desc(PostReportCase.last_reported_at), desc(PostReportCase.id))
        .offset(offset)
        .limit(normalized_size)
    ).scalars().all()

    items = [_reported_profile_post_out(item=item, post_author=reported_user) for item in rows]
    range_start = offset + 1 if total > 0 and items else 0
    range_end = offset + len(items) if total > 0 and items else 0
    return GuardianReportedProfilePostListOut(
        items=items,
        page=normalized_page,
        page_size=normalized_size,
        total=total,
        total_pages=total_pages,
        range_start=range_start,
        range_end=range_end,
    )


def _reported_profile_out(
    *,
    db: Session,
    item: ProfileReportCase,
    users: dict[int, User],
    reports_map: dict[int, list[GuardianReportedProfileReportOut]],
    current_user_id: int,
) -> GuardianReportedProfileOut:
    reported_user = users.get(int(item.reported_user_id)) if item.reported_user_id else None
    if reported_user is None:
        raise HTTPException(status_code=500, detail="No se pudo construir el reporte (usuario faltante).")
    resolver = users.get(int(item.resolved_by_guardian_id)) if item.resolved_by_guardian_id else None
    moderation_status = _normalize_account_moderation_status(reported_user.guardian_moderation_status)
    account_moderated_by_guardian = (
        users.get(int(reported_user.guardian_moderated_by_user_id))
        if reported_user.guardian_moderated_by_user_id
        else None
    )
    is_self_target = int(reported_user.id) == int(current_user_id)
    reported_posts = _load_reported_posts_for_profile(
        db=db,
        reported_user=reported_user,
        page=1,
        page_size=REPORTED_PROFILE_POSTS_PAGE_SIZE_DEFAULT,
    )
    return GuardianReportedProfileOut(
        id=int(item.id),
        status=item.status,
        report_count=max(0, int(item.report_count or 0)),
        reported_user=_user_out(reported_user),
        account_moderation_status=moderation_status,
        account_moderated_at=reported_user.guardian_moderated_at,
        account_moderated_by_guardian=(
            _user_out(account_moderated_by_guardian) if account_moderated_by_guardian else None
        ),
        can_suspend_account=(not is_self_target and moderation_status == ACCOUNT_MODERATION_STATUS_ACTIVE),
        can_enable_account=(not is_self_target and moderation_status == ACCOUNT_MODERATION_STATUS_SUSPENDED),
        can_close_account=(not is_self_target and moderation_status != ACCOUNT_MODERATION_STATUS_CLOSED),
        resolved_by_guardian=_user_out(resolver) if resolver else None,
        first_reported_at=item.first_reported_at,
        last_reported_at=item.last_reported_at,
        resolved_at=item.resolved_at,
        reports=reports_map.get(int(item.id), []),
        reported_posts=reported_posts,
    )


def _mirror_guardian_message_in_inbox(*, db: Session, msg: GuardianWishMessage) -> None:
    sender_guardian_id = int(msg.sender_guardian_id) if msg.sender_guardian_id else None
    if sender_guardian_id is None:
        return

    created_at = msg.created_at or datetime.now(timezone.utc)
    thread = MessageThread(
        guardian_user_id=sender_guardian_id,
        recipient_user_id=int(msg.recipient_user_id),
        subject=msg.subject,
        source_guardian_wish_message_id=int(msg.id),
        is_guardian_center_origin=True,
        created_at=created_at,
        updated_at=created_at,
    )
    db.add(thread)
    db.flush()

    entry = MessageEntry(
        thread_id=int(thread.id),
        sender_user_id=sender_guardian_id,
        body=msg.body,
        created_at=created_at,
    )
    db.add(entry)


@router.post("/wish-requests", response_model=GuardianWishRequestOut)
def create_wish_request(
    payload: GuardianWishRequestCreate,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    requester = db.execute(
        select(User).where(User.id == current.user_number, User.is_active.is_(True))
    ).scalar_one_or_none()
    if requester is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if is_minor_protected(requester):
        raise HTTPException(
            status_code=403,
            detail="Tu cuenta está en modo protegido. No puedes formalizar acuerdos hasta completar la acreditación.",
        )

    reason = (payload.reason or "").strip()
    phone = (payload.phone or "").strip()
    email = str(payload.email or "").strip().lower()
    if not reason:
        raise HTTPException(status_code=400, detail="Debes describir el motivo.")
    if not phone:
        raise HTTPException(status_code=400, detail="Debes indicar un número telefónico.")
    if not email:
        raise HTTPException(status_code=400, detail="Debes indicar un e-mail válido.")

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == payload.public_wish_id)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo no encontrado o ya no está activo.")
    if int(wish.user_id) == int(current.user_number):
        raise HTTPException(status_code=400, detail="No puedes solicitar un Guardián para tu propio deseo.")

    wish_owner = db.execute(
        select(User).where(User.id == wish.user_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if wish_owner is None:
        raise HTTPException(status_code=404, detail="El usuario dueño del deseo no existe.")
    if not bool(wish_owner.public_profile_show_public_wishes):
        raise HTTPException(status_code=403, detail="Este módulo es privado.")

    guardian: User | None = None
    if payload.guardian_user_id is not None:
        guardian = db.execute(
            select(User).where(User.id == payload.guardian_user_id, User.is_active.is_(True))
        ).scalar_one_or_none()
        if guardian is None:
            raise HTTPException(status_code=404, detail="Guardián no encontrado.")
        if int(guardian.guardian_rank or 0) < GUARDIANS_MIN_RANK:
            raise HTTPException(status_code=400, detail="El usuario seleccionado no es un Guardián válido.")

    evidence = _resolve_owned_media(db=db, media_id=int(payload.evidence_media_id), user_id=current.user_number)

    req = GuardianWishRequest(
        requester_id=current.user_number,
        guardian_id=int(guardian.id) if guardian else None,
        wish_owner_id=int(wish_owner.id),
        public_wish_id=int(wish.id),
        wish_text=wish.wish_text,
        wish_type=wish.wish_type,
        reason=reason,
        contact_phone=phone,
        contact_email=email,
        evidence_media_id=int(evidence.id) if evidence else None,
        status=GuardianWishRequestStatus.open,
    )

    db.add(req)
    db.commit()
    db.refresh(req)

    users = {
        int(requester.id): requester,
        int(wish_owner.id): wish_owner,
    }
    if guardian is not None:
        users[int(guardian.id)] = guardian
    medias = {int(evidence.id): evidence} if evidence is not None else {}

    return _request_out(req=req, users=users, medias=medias)


@router.get("/wish-requests", response_model=GuardianWishRequestListOut)
def list_wish_requests(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=PAGE_SIZE_DEFAULT, ge=1, le=PAGE_SIZE_MAX),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    total = int(db.execute(select(func.count(GuardianWishRequest.id))).scalar_one() or 0)
    normalized_size = max(1, min(int(page_size), PAGE_SIZE_MAX))
    total_pages = max(1, ceil(total / normalized_size)) if total else 1
    normalized_page = max(1, min(int(page), total_pages))
    offset = (normalized_page - 1) * normalized_size

    rows = db.execute(
        select(GuardianWishRequest)
        .order_by(desc(GuardianWishRequest.created_at), desc(GuardianWishRequest.id))
        .offset(offset)
        .limit(normalized_size)
    ).scalars().all()

    user_ids: set[int] = set()
    media_ids: set[int] = set()
    for req in rows:
        user_ids.add(int(req.requester_id))
        user_ids.add(int(req.wish_owner_id))
        if req.guardian_id:
            user_ids.add(int(req.guardian_id))
        if req.evidence_media_id:
            media_ids.add(int(req.evidence_media_id))

    users_map: dict[int, User] = {}
    if user_ids:
        users = db.execute(select(User).where(User.id.in_(sorted(user_ids)))).scalars().all()
        users_map = {int(user.id): user for user in users}

    medias_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(sorted(media_ids)))).scalars().all()
        medias_map = {int(media.id): media for media in medias}

    items = [_request_out(req=req, users=users_map, medias=medias_map) for req in rows]

    range_start = offset + 1 if total > 0 and items else 0
    range_end = offset + len(items) if total > 0 and items else 0

    return GuardianWishRequestListOut(
        items=items,
        page=normalized_page,
        page_size=normalized_size,
        total=total,
        total_pages=total_pages,
        range_start=range_start,
        range_end=range_end,
    )


@router.get("/rank-management/user", response_model=GuardianRankUserOut)
def get_rank_management_user(
    query: str = Query(..., min_length=1, max_length=80),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    user_id, username = _parse_rank_lookup_query(query)
    target: User | None = None
    if user_id is not None:
        target = db.execute(
            select(User).where(User.id == int(user_id), User.is_active.is_(True))
        ).scalar_one_or_none()
    elif username is not None:
        target = db.execute(
            select(User).where(User.username == username, User.is_active.is_(True))
        ).scalar_one_or_none()

    if target is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return _rank_user_out(user=target, current_user_id=current.user_number)


@router.post("/rank-management/users/{user_id}/promote", response_model=GuardianRankPromotionOut)
def promote_user_guardian_rank(
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    target = db.execute(
        select(User).where(User.id == int(user_id), User.is_active.is_(True))
    ).scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    previous_rank = max(0, int(target.guardian_rank or 0))
    if previous_rank >= GUARDIANS_MAX_RANK:
        raise HTTPException(
            status_code=409,
            detail=f"Este usuario ya está en el rango máximo ({GUARDIANS_MAX_RANK}).",
        )

    target.guardian_rank = previous_rank + 1
    if str(target.role or "").strip().lower() == "user":
        target.role = "guardian"

    db.commit()
    db.refresh(target)

    return GuardianRankPromotionOut(
        promoted=True,
        previous_guardian_rank=previous_rank,
        previous_guardian_rank_name=_guardian_rank_name(previous_rank),
        target=_rank_user_out(user=target, current_user_id=current.user_number),
    )


@router.get("/reported-posts", response_model=GuardianReportedPostListOut)
def list_reported_posts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=REPORTED_POSTS_PAGE_SIZE_DEFAULT, ge=1, le=REPORTED_POSTS_PAGE_SIZE_MAX),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    total = int(db.execute(select(func.count(PostReportCase.id))).scalar_one() or 0)
    normalized_size = max(1, min(int(page_size), REPORTED_POSTS_PAGE_SIZE_MAX))
    total_pages = max(1, ceil(total / normalized_size)) if total else 1
    normalized_page = max(1, min(int(page), total_pages))
    offset = (normalized_page - 1) * normalized_size

    status_priority = case(
        (PostReportCase.status == PostReportCaseStatus.open, 0),
        else_=1,
    )

    rows = db.execute(
        select(PostReportCase)
        .order_by(status_priority.asc(), desc(PostReportCase.last_reported_at), desc(PostReportCase.id))
        .offset(offset)
        .limit(normalized_size)
    ).scalars().all()

    users_map, medias_map, reports_map = _load_related_maps_for_report_cases(db=db, items=rows)
    items = [
        _reported_post_out(item=item, users=users_map, medias=medias_map, reports_map=reports_map)
        for item in rows
    ]

    range_start = offset + 1 if total > 0 and items else 0
    range_end = offset + len(items) if total > 0 and items else 0

    return GuardianReportedPostListOut(
        items=items,
        page=normalized_page,
        page_size=normalized_size,
        total=total,
        total_pages=total_pages,
        range_start=range_start,
        range_end=range_end,
    )


@router.get("/reported-profiles", response_model=GuardianReportedProfileListOut)
def list_reported_profiles(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=REPORTED_PROFILES_PAGE_SIZE_DEFAULT, ge=1, le=REPORTED_PROFILES_PAGE_SIZE_MAX),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    total = int(db.execute(select(func.count(ProfileReportCase.id))).scalar_one() or 0)
    normalized_size = max(1, min(int(page_size), REPORTED_PROFILES_PAGE_SIZE_MAX))
    total_pages = max(1, ceil(total / normalized_size)) if total else 1
    normalized_page = max(1, min(int(page), total_pages))
    offset = (normalized_page - 1) * normalized_size

    status_priority = case(
        (ProfileReportCase.status == ProfileReportCaseStatus.open, 0),
        else_=1,
    )
    rows = db.execute(
        select(ProfileReportCase)
        .order_by(status_priority.asc(), desc(ProfileReportCase.last_reported_at), desc(ProfileReportCase.id))
        .offset(offset)
        .limit(normalized_size)
    ).scalars().all()

    users_map, reports_map = _load_related_maps_for_profile_report_cases(db=db, items=rows)
    items = [
        _reported_profile_out(
            db=db,
            item=item,
            users=users_map,
            reports_map=reports_map,
            current_user_id=int(current.user_number),
        )
        for item in rows
    ]

    range_start = offset + 1 if total > 0 and items else 0
    range_end = offset + len(items) if total > 0 and items else 0
    return GuardianReportedProfileListOut(
        items=items,
        page=normalized_page,
        page_size=normalized_size,
        total=total,
        total_pages=total_pages,
        range_start=range_start,
        range_end=range_end,
    )


@router.get("/reported-profiles/{case_id}/reported-posts", response_model=GuardianReportedProfilePostListOut)
def list_reported_posts_for_profile_case(
    case_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(
        default=REPORTED_PROFILE_POSTS_PAGE_SIZE_DEFAULT,
        ge=1,
        le=REPORTED_PROFILE_POSTS_PAGE_SIZE_MAX,
    ),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    profile_case = db.execute(
        select(ProfileReportCase).where(ProfileReportCase.id == int(case_id))
    ).scalar_one_or_none()
    if profile_case is None:
        raise HTTPException(status_code=404, detail="Reporte de perfil no encontrado.")

    reported_user = db.execute(
        select(User).where(User.id == int(profile_case.reported_user_id))
    ).scalar_one_or_none()
    if reported_user is None:
        raise HTTPException(status_code=404, detail="Usuario reportado no encontrado.")

    return _load_reported_posts_for_profile(
        db=db,
        reported_user=reported_user,
        page=page,
        page_size=page_size,
    )


def _resolve_profile_case_and_target_user(
    *,
    db: Session,
    case_id: int,
    guardian_user_id: int,
) -> tuple[ProfileReportCase, User]:
    item = db.execute(
        select(ProfileReportCase).where(ProfileReportCase.id == int(case_id))
    ).scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Reporte de perfil no encontrado.")

    target_user = db.execute(
        select(User).where(User.id == int(item.reported_user_id))
    ).scalar_one_or_none()
    if target_user is None:
        raise HTTPException(status_code=404, detail="Usuario reportado no encontrado.")
    if int(target_user.id) == int(guardian_user_id):
        raise HTTPException(status_code=400, detail="No puedes moderar tu propia cuenta.")

    return item, target_user


def _build_reported_profile_case_response(
    *,
    db: Session,
    item: ProfileReportCase,
    current_user_id: int,
) -> GuardianReportedProfileOut:
    users_map, reports_map = _load_related_maps_for_profile_report_cases(db=db, items=[item])
    return _reported_profile_out(
        db=db,
        item=item,
        users=users_map,
        reports_map=reports_map,
        current_user_id=current_user_id,
    )


@router.post("/reported-profiles/{case_id}/suspend-account", response_model=GuardianReportedProfileOut)
def suspend_reported_profile_account(
    case_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    item, target_user = _resolve_profile_case_and_target_user(
        db=db,
        case_id=case_id,
        guardian_user_id=int(current.user_number),
    )

    current_status = _normalize_account_moderation_status(target_user.guardian_moderation_status)
    if current_status == ACCOUNT_MODERATION_STATUS_CLOSED:
        raise HTTPException(status_code=409, detail="La cuenta ya está cerrada de forma definitiva.")
    if current_status == ACCOUNT_MODERATION_STATUS_SUSPENDED:
        raise HTTPException(status_code=409, detail="La cuenta ya está suspendida.")

    now = datetime.now(timezone.utc)
    target_user.guardian_moderation_status = ACCOUNT_MODERATION_STATUS_SUSPENDED
    target_user.guardian_moderated_at = now
    target_user.guardian_moderated_by_user_id = int(current.user_number)
    target_user.is_active = False
    target_user.account_closure_requested_at = None
    target_user.account_closure_restore_deadline_at = None
    target_user.updated_at = now

    _set_profile_case_reviewed(item=item, guardian_user_id=int(current.user_number), now=now)
    db.execute(delete(RefreshToken).where(RefreshToken.user_id == int(target_user.id)))

    db.commit()
    db.refresh(item)

    return _build_reported_profile_case_response(
        db=db,
        item=item,
        current_user_id=int(current.user_number),
    )


@router.post("/reported-profiles/{case_id}/enable-account", response_model=GuardianReportedProfileOut)
def enable_reported_profile_account(
    case_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    item, target_user = _resolve_profile_case_and_target_user(
        db=db,
        case_id=case_id,
        guardian_user_id=int(current.user_number),
    )

    current_status = _normalize_account_moderation_status(target_user.guardian_moderation_status)
    if current_status == ACCOUNT_MODERATION_STATUS_CLOSED:
        raise HTTPException(status_code=409, detail="La cuenta cerrada de forma definitiva no se puede habilitar.")
    if current_status != ACCOUNT_MODERATION_STATUS_SUSPENDED:
        raise HTTPException(status_code=409, detail="Solo una cuenta suspendida puede volver a habilitarse.")

    now = datetime.now(timezone.utc)
    target_user.guardian_moderation_status = ACCOUNT_MODERATION_STATUS_ACTIVE
    target_user.guardian_moderated_at = now
    target_user.guardian_moderated_by_user_id = int(current.user_number)
    target_user.is_active = True
    target_user.account_closure_requested_at = None
    target_user.account_closure_restore_deadline_at = None
    target_user.updated_at = now

    _set_profile_case_reviewed(item=item, guardian_user_id=int(current.user_number), now=now)
    db.execute(delete(RefreshToken).where(RefreshToken.user_id == int(target_user.id)))

    db.commit()
    db.refresh(item)

    return _build_reported_profile_case_response(
        db=db,
        item=item,
        current_user_id=int(current.user_number),
    )


@router.post("/reported-profiles/{case_id}/close-account", response_model=GuardianReportedProfileOut)
def close_reported_profile_account(
    case_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    item, target_user = _resolve_profile_case_and_target_user(
        db=db,
        case_id=case_id,
        guardian_user_id=int(current.user_number),
    )

    current_status = _normalize_account_moderation_status(target_user.guardian_moderation_status)
    if current_status == ACCOUNT_MODERATION_STATUS_CLOSED:
        raise HTTPException(status_code=409, detail="La cuenta ya fue cerrada de forma definitiva.")

    now = datetime.now(timezone.utc)
    target_user.guardian_moderation_status = ACCOUNT_MODERATION_STATUS_CLOSED
    target_user.guardian_moderated_at = now
    target_user.guardian_moderated_by_user_id = int(current.user_number)
    target_user.is_active = False
    target_user.account_closure_requested_at = None
    target_user.account_closure_restore_deadline_at = None
    target_user.updated_at = now

    _set_profile_case_reviewed(item=item, guardian_user_id=int(current.user_number), now=now)
    db.execute(delete(RefreshToken).where(RefreshToken.user_id == int(target_user.id)))

    db.commit()
    db.refresh(item)

    return _build_reported_profile_case_response(
        db=db,
        item=item,
        current_user_id=int(current.user_number),
    )


@router.post("/reported-posts/{case_id}/delete-post", response_model=GuardianReportedPostOut)
def delete_reported_post(
    case_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    item = db.execute(
        select(PostReportCase).where(PostReportCase.id == case_id)
    ).scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado.")

    now = datetime.now(timezone.utc)
    post = None
    if item.post_id:
        post = db.execute(select(Post).where(Post.id == item.post_id)).scalar_one_or_none()

    if post is not None:
        removed_stars = max(0, int(post.star_count or 0))
        author = db.execute(select(User).where(User.id == post.author_id)).scalar_one_or_none()
        if author is not None:
            author.received_stars_total = max(0, int(author.received_stars_total or 0) - removed_stars)
            if int(author.donated_stars_total or 0) > int(author.received_stars_total or 0):
                author.donated_stars_total = int(author.received_stars_total or 0)

        item.post_text_snapshot = item.post_text_snapshot or post.text
        item.post_media_id_snapshot = item.post_media_id_snapshot or post.media_id
        item.post_media_kind_snapshot = item.post_media_kind_snapshot or post.media_kind

        db.execute(
            update(PostReport)
            .where(PostReport.case_id == item.id)
            .values(post_id=None)
        )
        db.delete(post)
    else:
        db.execute(
            update(PostReport)
            .where(PostReport.case_id == item.id, PostReport.post_id.is_not(None))
            .values(post_id=None)
        )

    item.post_id = None
    item.status = PostReportCaseStatus.deleted
    item.resolved_at = now
    item.resolved_by_guardian_id = int(current.user_number)
    item.updated_at = now

    db.commit()
    db.refresh(item)

    users_map, medias_map, reports_map = _load_related_maps_for_report_cases(db=db, items=[item])
    return _reported_post_out(item=item, users=users_map, medias=medias_map, reports_map=reports_map)


@router.post("/reported-posts/{case_id}/keep-post", response_model=GuardianReportedPostOut)
def keep_reported_post(
    case_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    item = db.execute(
        select(PostReportCase).where(PostReportCase.id == case_id)
    ).scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado.")

    if item.post_id:
        post = db.execute(select(Post).where(Post.id == item.post_id)).scalar_one_or_none()
        if post is not None:
            item.post_text_snapshot = post.text
            item.post_media_id_snapshot = post.media_id
            item.post_media_kind_snapshot = post.media_kind

    now = datetime.now(timezone.utc)
    item.status = PostReportCaseStatus.kept
    item.resolved_at = now
    item.resolved_by_guardian_id = int(current.user_number)
    item.updated_at = now

    db.commit()
    db.refresh(item)

    users_map, medias_map, reports_map = _load_related_maps_for_report_cases(db=db, items=[item])
    return _reported_post_out(item=item, users=users_map, medias=medias_map, reports_map=reports_map)


@router.post("/wish-requests/{request_id}/seal-commitment", response_model=GuardianWishRequestOut)
def seal_wish_request_commitment(
    request_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    req = _resolve_wish_request_for_guardian_action(
        db=db,
        request_id=request_id,
        guardian_user_id=current.user_number,
        allow_closed=False,
    )

    if not req.commitment_code:
        req.commitment_code = _build_commitment_code(int(req.id))
    if req.commitment_sealed_at is None:
        req.commitment_sealed_at = datetime.now(timezone.utc)
    req.status = GuardianWishRequestStatus.in_progress

    db.commit()
    db.refresh(req)

    users_map, medias_map = _load_related_maps_for_request(db=db, req=req)
    return _request_out(req=req, users=users_map, medias=medias_map)


@router.post("/wish-requests/{request_id}/deny", response_model=GuardianWishRequestOut)
def deny_wish_request(
    request_id: int,
    payload: GuardianWishRequestDenyInput,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    req = _resolve_wish_request_for_guardian_action(
        db=db,
        request_id=request_id,
        guardian_user_id=current.user_number,
        allow_closed=False,
    )

    requester = db.execute(
        select(User).where(User.id == req.requester_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if requester is None:
        raise HTTPException(status_code=404, detail="Solicitante no encontrado.")

    msg = GuardianWishMessage(
        wish_request_id=int(req.id),
        sender_guardian_id=int(current.user_number),
        recipient_user_id=int(requester.id),
        kind=GuardianWishMessageKind.denial,
        subject=payload.subject,
        body=payload.body,
    )
    db.add(msg)
    db.flush()
    _mirror_guardian_message_in_inbox(db=db, msg=msg)

    req.status = GuardianWishRequestStatus.closed
    req.denied_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(req)

    users_map, medias_map = _load_related_maps_for_request(db=db, req=req)
    return _request_out(req=req, users=users_map, medias=medias_map)


@router.post("/wish-requests/{request_id}/message-owner", response_model=GuardianWishMessageOut)
def message_wish_owner(
    request_id: int,
    payload: GuardianWishRequestOwnerMessageInput,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)

    req = _resolve_wish_request_for_guardian_action(
        db=db,
        request_id=request_id,
        guardian_user_id=current.user_number,
        allow_closed=False,
    )

    wish_owner = db.execute(
        select(User).where(User.id == req.wish_owner_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if wish_owner is None:
        raise HTTPException(status_code=404, detail="Dueño del deseo no encontrado.")

    msg = GuardianWishMessage(
        wish_request_id=int(req.id),
        sender_guardian_id=int(current.user_number),
        recipient_user_id=int(wish_owner.id),
        kind=GuardianWishMessageKind.owner_contact,
        subject=payload.subject,
        body=payload.body,
    )
    db.add(msg)
    db.flush()
    _mirror_guardian_message_in_inbox(db=db, msg=msg)
    db.commit()
    db.refresh(msg)

    return _message_out(msg=msg, recipient=wish_owner)
