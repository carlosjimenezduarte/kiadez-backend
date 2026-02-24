from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, or_, select
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.config import settings
from app.db.database import get_db
from app.db.models.guardian_wish_message import GuardianWishMessage
from app.db.models.message_entry import MessageEntry
from app.db.models.message_thread import MessageThread
from app.db.models.user import User
from app.messages.schemas import (
    MessageEntryOut,
    MessageReplyInput,
    MessageThreadCreateInput,
    MessageThreadListOut,
    MessageThreadOut,
)

router = APIRouter(prefix="/messages", tags=["messages"])

GUARDIANS_MIN_RANK = 3
BROADCAST_ALL_USERS_KEYWORD = "allusers"


def _parse_csv_set(value: str | None) -> set[str]:
    raw = (value or "").strip()
    if not raw:
        return set()
    return {
        item.strip().lower()
        for item in raw.split(",")
        if item and item.strip()
    }


def _is_guardian(current: UserPublic) -> bool:
    return int(current.guardian_rank or 0) >= GUARDIANS_MIN_RANK


def _require_guardian(current: UserPublic) -> None:
    if not _is_guardian(current):
        raise HTTPException(
            status_code=403,
            detail="Solo los Guardianes pueden iniciar conversaciones.",
        )


def _normalize_username(value: str | None) -> str:
    normalized = (value or "").strip().lower()
    while normalized.startswith("@"):
        normalized = normalized[1:]
    return normalized


def _is_all_users_broadcast(payload: MessageThreadCreateInput) -> bool:
    return payload.to_user_id is None and _normalize_username(payload.to_username) == BROADCAST_ALL_USERS_KEYWORD


def _can_use_all_users_broadcast(current: UserPublic) -> bool:
    allowed_usernames = _parse_csv_set(settings.MESSAGES_BROADCAST_ALLOW_USERNAMES)
    allowed_emails = _parse_csv_set(settings.MESSAGES_BROADCAST_ALLOW_EMAILS)
    current_username = _normalize_username(current.username)
    current_email = (current.email or "").strip().lower()

    return (bool(current_username) and current_username in allowed_usernames) or (
        bool(current_email) and current_email in allowed_emails
    )


def _require_all_users_broadcast_access(current: UserPublic) -> None:
    if _can_use_all_users_broadcast(current):
        return
    raise HTTPException(
        status_code=403,
        detail="El envío a @allusers es exclusivo para cuentas autorizadas.",
    )


def _build_handle(*, username: str | None, user_id: int | None) -> str:
    normalized = (username or "").strip()
    if normalized:
        return f"@{normalized}"
    normalized_id = int(user_id or 0)
    if normalized_id > 0:
        return f"@id{normalized_id}"
    return "@usuario"


def _build_full_name(user: User | None, *, fallback_user_id: int | None) -> str:
    if user is not None:
        first_name = (user.first_name or "").strip()
        last_name = (user.last_name or "").strip()
        full_name = f"{first_name} {last_name}".strip()
        if full_name:
            return full_name
        return f"Usuario {int(user.id)}"
    fallback = int(fallback_user_id or 0)
    if fallback > 0:
        return f"Usuario {fallback}"
    return "Usuario"


def _load_users_map(*, db: Session, user_ids: set[int]) -> dict[int, User]:
    if not user_ids:
        return {}

    rows = db.execute(select(User).where(User.id.in_(sorted(user_ids)))).scalars().all()
    return {int(row.id): row for row in rows}


def _load_entries_by_thread_id(*, db: Session, thread_ids: list[int]) -> dict[int, list[MessageEntry]]:
    if not thread_ids:
        return {}

    rows = db.execute(
        select(MessageEntry)
        .where(MessageEntry.thread_id.in_(thread_ids))
        .order_by(MessageEntry.created_at.asc(), MessageEntry.id.asc())
    ).scalars().all()

    grouped: dict[int, list[MessageEntry]] = {}
    for row in rows:
        grouped.setdefault(int(row.thread_id), []).append(row)
    return grouped


def _load_source_guardian_message_map(
    *,
    db: Session,
    source_ids: set[int],
) -> dict[int, GuardianWishMessage]:
    if not source_ids:
        return {}

    rows = db.execute(
        select(GuardianWishMessage).where(GuardianWishMessage.id.in_(sorted(source_ids)))
    ).scalars().all()
    return {int(row.id): row for row in rows}


def _can_reply_thread(*, thread: MessageThread, current: UserPublic) -> bool:
    current_user_id = int(current.user_number)
    guardian_user_id = int(thread.guardian_user_id) if thread.guardian_user_id else None
    recipient_user_id = int(thread.recipient_user_id)

    is_participant = (
        (guardian_user_id is not None and guardian_user_id == current_user_id)
        or recipient_user_id == current_user_id
    )
    if not is_participant:
        return False

    if _is_guardian(current):
        return True

    return guardian_user_id is not None and recipient_user_id == current_user_id


def _thread_out(
    *,
    thread: MessageThread,
    entries: list[MessageEntry],
    users_map: dict[int, User],
    source_messages_map: dict[int, GuardianWishMessage],
    current: UserPublic,
) -> MessageThreadOut:
    guardian_user_id = int(thread.guardian_user_id) if thread.guardian_user_id else None
    recipient_user_id = int(thread.recipient_user_id)

    guardian_user = users_map.get(guardian_user_id) if guardian_user_id else None
    recipient_user = users_map.get(recipient_user_id)

    guardian_name = _build_full_name(guardian_user, fallback_user_id=guardian_user_id)
    recipient_name = _build_full_name(recipient_user, fallback_user_id=recipient_user_id)

    guardian_handle = _build_handle(
        username=(guardian_user.username if guardian_user else None),
        user_id=guardian_user_id,
    )
    recipient_handle = _build_handle(
        username=(recipient_user.username if recipient_user else None),
        user_id=recipient_user_id,
    )

    source_guardian_message_id = (
        int(thread.source_guardian_wish_message_id)
        if thread.source_guardian_wish_message_id
        else None
    )
    source_message = (
        source_messages_map.get(source_guardian_message_id)
        if source_guardian_message_id is not None
        else None
    )

    message_items: list[MessageEntryOut] = []
    for entry in entries:
        sender_user_id = int(entry.sender_user_id) if entry.sender_user_id else None
        sender_user = users_map.get(sender_user_id) if sender_user_id else None
        message_items.append(
            MessageEntryOut(
                id=int(entry.id),
                sender_user_id=sender_user_id,
                sender_name=_build_full_name(sender_user, fallback_user_id=sender_user_id),
                sender_handle=_build_handle(
                    username=(sender_user.username if sender_user else None),
                    user_id=sender_user_id,
                ),
                body=entry.body,
                created_at=entry.created_at,
            )
        )

    return MessageThreadOut(
        id=int(thread.id),
        subject=thread.subject,
        guardian_user_id=guardian_user_id,
        guardian_name=guardian_name if guardian_user_id is not None else None,
        guardian_handle=guardian_handle if guardian_user_id is not None else None,
        recipient_user_id=recipient_user_id,
        recipient_name=recipient_name,
        recipient_handle=recipient_handle,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
        is_guardian_center_origin=bool(thread.is_guardian_center_origin),
        source_guardian_wish_message_id=source_guardian_message_id,
        source_wish_request_id=(int(source_message.wish_request_id) if source_message else None),
        source_kind=(source_message.kind if source_message else None),
        can_reply=_can_reply_thread(thread=thread, current=current),
        messages=message_items,
    )


def _load_user_threads(*, db: Session, user_id: int) -> list[MessageThread]:
    return db.execute(
        select(MessageThread)
        .where(
            or_(
                MessageThread.guardian_user_id == user_id,
                MessageThread.recipient_user_id == user_id,
            )
        )
        .order_by(desc(MessageThread.updated_at), desc(MessageThread.id))
    ).scalars().all()


def _build_threads_out(
    *,
    db: Session,
    threads: list[MessageThread],
    current: UserPublic,
) -> list[MessageThreadOut]:
    if not threads:
        return []

    thread_ids = [int(thread.id) for thread in threads]
    entries_map = _load_entries_by_thread_id(db=db, thread_ids=thread_ids)

    user_ids: set[int] = set()
    source_ids: set[int] = set()

    for thread in threads:
        if thread.guardian_user_id:
            user_ids.add(int(thread.guardian_user_id))
        user_ids.add(int(thread.recipient_user_id))
        if thread.source_guardian_wish_message_id:
            source_ids.add(int(thread.source_guardian_wish_message_id))

    for thread_entries in entries_map.values():
        for entry in thread_entries:
            if entry.sender_user_id:
                user_ids.add(int(entry.sender_user_id))

    users_map = _load_users_map(db=db, user_ids=user_ids)
    source_map = _load_source_guardian_message_map(db=db, source_ids=source_ids)

    return [
        _thread_out(
            thread=thread,
            entries=entries_map.get(int(thread.id), []),
            users_map=users_map,
            source_messages_map=source_map,
            current=current,
        )
        for thread in threads
    ]


def _resolve_recipient_for_create(*, db: Session, payload: MessageThreadCreateInput) -> User:
    if payload.to_user_id is not None:
        user = db.execute(
            select(User).where(User.id == payload.to_user_id, User.is_active.is_(True))
        ).scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="Destinatario no encontrado.")
        return user

    username = _normalize_username(payload.to_username)
    if not username:
        raise HTTPException(status_code=400, detail="Destinatario inválido.")

    user = db.execute(
        select(User).where(User.username == username, User.is_active.is_(True))
    ).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Destinatario no encontrado.")
    return user


def _resolve_all_users_recipients(*, db: Session, sender_user_id: int) -> list[User]:
    recipients = db.execute(
        select(User).where(
            User.is_active.is_(True),
            User.id != sender_user_id,
        )
        .order_by(User.id.asc())
    ).scalars().all()
    return recipients


def _resolve_thread_for_participant(
    *,
    db: Session,
    thread_id: int,
    current_user_id: int,
) -> MessageThread:
    thread = db.execute(
        select(MessageThread).where(MessageThread.id == thread_id)
    ).scalar_one_or_none()
    if thread is None:
        raise HTTPException(status_code=404, detail="Conversación no encontrada.")

    guardian_user_id = int(thread.guardian_user_id) if thread.guardian_user_id else None
    recipient_user_id = int(thread.recipient_user_id)

    if guardian_user_id != current_user_id and recipient_user_id != current_user_id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta conversación.")

    return thread


@router.get("/threads", response_model=MessageThreadListOut)
def list_threads(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    threads = _load_user_threads(db=db, user_id=int(current.user_number))
    items = _build_threads_out(db=db, threads=threads, current=current)
    return MessageThreadListOut(items=items)


@router.post("/threads", response_model=MessageThreadOut)
def create_thread(
    payload: MessageThreadCreateInput,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_guardian(current)
    sender_user_id = int(current.user_number)

    if _is_all_users_broadcast(payload):
        _require_all_users_broadcast_access(current)
        recipients = _resolve_all_users_recipients(db=db, sender_user_id=sender_user_id)
        if not recipients:
            raise HTTPException(
                status_code=409,
                detail="No hay usuarios activos disponibles para enviar con @allusers.",
            )

        created_threads: list[MessageThread] = []
        for recipient in recipients:
            thread = MessageThread(
                guardian_user_id=sender_user_id,
                recipient_user_id=int(recipient.id),
                subject=payload.subject,
                is_guardian_center_origin=False,
            )
            db.add(thread)
            db.flush()

            entry = MessageEntry(
                thread_id=int(thread.id),
                sender_user_id=sender_user_id,
                body=payload.body,
            )
            db.add(entry)
            db.flush()

            thread.updated_at = entry.created_at or datetime.now(timezone.utc)
            created_threads.append(thread)

        db.commit()
        last_created_thread = created_threads[-1]
        db.refresh(last_created_thread)

        items = _build_threads_out(db=db, threads=[last_created_thread], current=current)
        return items[0]

    recipient = _resolve_recipient_for_create(db=db, payload=payload)

    if int(recipient.id) == sender_user_id:
        raise HTTPException(status_code=400, detail="No puedes enviarte mensajes a ti mismo.")

    thread = MessageThread(
        guardian_user_id=sender_user_id,
        recipient_user_id=int(recipient.id),
        subject=payload.subject,
        is_guardian_center_origin=False,
    )
    db.add(thread)
    db.flush()

    entry = MessageEntry(
        thread_id=int(thread.id),
        sender_user_id=sender_user_id,
        body=payload.body,
    )
    db.add(entry)
    db.flush()

    thread.updated_at = entry.created_at or datetime.now(timezone.utc)

    db.commit()
    db.refresh(thread)

    items = _build_threads_out(db=db, threads=[thread], current=current)
    return items[0]


@router.post("/threads/{thread_id}/reply", response_model=MessageThreadOut)
def reply_thread(
    thread_id: int,
    payload: MessageReplyInput,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user_id = int(current.user_number)
    thread = _resolve_thread_for_participant(
        db=db,
        thread_id=thread_id,
        current_user_id=current_user_id,
    )

    if not _can_reply_thread(thread=thread, current=current):
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos para responder en esta conversación.",
        )

    if thread.guardian_user_id is None and not _is_guardian(current):
        raise HTTPException(
            status_code=409,
            detail="Esta conversación ya no acepta respuestas.",
        )

    entry = MessageEntry(
        thread_id=int(thread.id),
        sender_user_id=current_user_id,
        body=payload.body,
    )
    db.add(entry)
    db.flush()

    thread.updated_at = entry.created_at or datetime.now(timezone.utc)

    db.commit()
    db.refresh(thread)

    items = _build_threads_out(db=db, threads=[thread], current=current)
    return items[0]
