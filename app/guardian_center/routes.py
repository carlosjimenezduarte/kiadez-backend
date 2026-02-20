from __future__ import annotations

from datetime import datetime, timezone
from math import ceil
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

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
from app.db.models.public_personal_wish import PublicPersonalWish, PublicPersonalWishStatus
from app.db.models.user import User
from app.guardian_center.schemas import (
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
PAGE_SIZE_DEFAULT = 10
PAGE_SIZE_MAX = 25


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


def _build_wish_url(*, wish_owner: User, wish_id: int) -> str:
    qp: dict[str, str] = {"wish": str(int(wish_id))}
    username = (wish_owner.username or "").strip()
    if username:
        qp["u"] = username
    else:
        qp["id"] = str(int(wish_owner.id))
    return f"/my-public-whishes.html?{urlencode(qp)}"


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
