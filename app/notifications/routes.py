from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import and_, desc, exists, func, or_, select
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.i18n import locale_from_request, tr as i18n_tr
from app.db.database import get_db
from app.db.models.achievement_unlock_event import AchievementUnlockEvent
from app.db.models.message_entry import MessageEntry
from app.db.models.message_thread import MessageThread
from app.db.models.notification_read import NotificationRead
from app.db.models.oracle import OracleUserState
from app.db.models.post import Post, PostMention, PostStar, PostVisibility
from app.db.models.user import User
from app.db.models.user_follow import UserFollow
from app.notifications.schemas import (
    NotificationFeedOut,
    NotificationItemOut,
    NotificationPreferencesOut,
    NotificationPreferencesUpdateIn,
    NotificationReadIn,
    NotificationReadOut,
)


router = APIRouter(prefix="/notifications", tags=["notifications"])

DEFAULT_FEED_LIMIT = 16
MAX_FEED_LIMIT = 160
NOTIFICATION_SOURCE_LIMIT = 48
GUARDIAN_MIN_RANK = 3
ORACLE_COOLDOWN = timedelta(hours=72)


def _locale(request: Request | None) -> str:
    return locale_from_request(request, default="en")


def _td(locale: str, en: str) -> str:
    translations: dict[str, tuple[str, str]] = {
        "User not found.": ("Usuario no encontrado.", "Utilisateur introuvable."),
    }
    pair = translations.get(en)
    if not pair:
        return en
    es, fr = pair
    return i18n_tr(locale, es=es, en=en, fr=fr)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _utc_day_start(dt: datetime) -> datetime:
    normalized = dt.astimezone(timezone.utc)
    return normalized.replace(hour=0, minute=0, second=0, microsecond=0)


def _coerce_day(value: object) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        normalized = value.strip()
        if not normalized:
            return None
        try:
            return date.fromisoformat(normalized[:10])
        except ValueError:
            return None
    return None


def _trim_text(value: str | None, *, limit: int = 140) -> str:
    normalized = " ".join((value or "").split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: max(1, limit - 1)].rstrip() + "…"


def _normalize_notification_id(value: str | None) -> str:
    normalized = (value or "").strip()
    if not normalized:
        return ""
    if len(normalized) > 120:
        return normalized[:120]
    return normalized


def _display_name(*, first_name: str | None, last_name: str | None, user_id: int) -> str:
    full_name = f"{(first_name or '').strip()} {(last_name or '').strip()}".strip()
    return full_name or f"User {int(user_id)}"


def _build_profile_url(*, user_id: int, username: str | None) -> str:
    normalized = (username or "").strip()
    if normalized:
        return f"/home_user.html?u={normalized}"
    return f"/home_user.html?id={int(user_id)}"


def _self_home_url(user: User) -> str:
    normalized = (user.username or "").strip()
    if normalized:
        return f"/home_user.html?u={normalized}"
    return f"/home_user.html?id={int(user.id)}"


def _preferences_out(user: User) -> NotificationPreferencesOut:
    return NotificationPreferencesOut(
        calendar_enabled=bool(user.notif_calendar_enabled),
        oracle_enabled=bool(user.notif_oracle_enabled),
        followers_enabled=bool(user.notif_followers_enabled),
        messages_enabled=bool(user.notif_messages_enabled),
        achievements_enabled=bool(user.notif_achievements_enabled),
        mentions_enabled=bool(user.notif_mentions_enabled),
        stars_enabled=bool(user.notif_stars_enabled),
    )


def _load_current_user_or_404(*, db: Session, current: UserPublic, locale: str) -> User:
    user = db.execute(
        select(User).where(User.id == int(current.user_number), User.is_active.is_(True))
    ).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))
    return user


def _collect_followers_notifications(*, db: Session, user_id: int, locale: str) -> list[NotificationItemOut]:
    rows = db.execute(
        select(
            UserFollow.id,
            UserFollow.created_at,
            User.id.label("follower_user_id"),
            User.username.label("follower_username"),
            User.first_name.label("follower_first_name"),
            User.last_name.label("follower_last_name"),
        )
        .join(User, User.id == UserFollow.follower_id)
        .where(UserFollow.followed_id == user_id)
        .order_by(desc(UserFollow.created_at), desc(UserFollow.id))
        .limit(NOTIFICATION_SOURCE_LIMIT)
    ).all()

    items: list[NotificationItemOut] = []
    for row in rows:
        follower_id = int(row.follower_user_id)
        follower_name = _display_name(
            first_name=row.follower_first_name,
            last_name=row.follower_last_name,
            user_id=follower_id,
        )
        items.append(
            NotificationItemOut(
                id=f"followers:{int(row.id)}",
                kind="followers",
                emoji="👥",
                title=i18n_tr(
                    locale,
                    es="Nuevo seguidor",
                    en="New follower",
                    fr="Nouveau suiveur",
                ),
                message=i18n_tr(
                    locale,
                    es=f"{follower_name} comenzó a seguirte.",
                    en=f"{follower_name} started following you.",
                    fr=f"{follower_name} a commencé à vous suivre.",
                ),
                created_at=row.created_at,
                href=_build_profile_url(user_id=follower_id, username=row.follower_username),
            )
        )
    return items


def _collect_messages_notifications(*, db: Session, user_id: int, locale: str) -> list[NotificationItemOut]:
    rows = db.execute(
        select(
            MessageEntry.id,
            MessageEntry.created_at,
            MessageEntry.body,
            MessageThread.id.label("thread_id"),
            MessageThread.subject.label("thread_subject"),
            User.id.label("sender_user_id"),
            User.username.label("sender_username"),
            User.first_name.label("sender_first_name"),
            User.last_name.label("sender_last_name"),
        )
        .join(MessageThread, MessageThread.id == MessageEntry.thread_id)
        .join(User, User.id == MessageEntry.sender_user_id)
        .where(
            MessageThread.recipient_user_id == user_id,
            MessageEntry.sender_user_id.isnot(None),
            MessageEntry.sender_user_id != user_id,
            or_(
                User.role == "guardian",
                func.coalesce(User.guardian_rank, 0) >= GUARDIAN_MIN_RANK,
            ),
        )
        .order_by(desc(MessageEntry.created_at), desc(MessageEntry.id))
        .limit(NOTIFICATION_SOURCE_LIMIT)
    ).all()

    items: list[NotificationItemOut] = []
    for row in rows:
        sender_id = int(row.sender_user_id)
        sender_name = _display_name(
            first_name=row.sender_first_name,
            last_name=row.sender_last_name,
            user_id=sender_id,
        )
        body_preview = _trim_text(row.body, limit=120)
        subject = _trim_text(row.thread_subject, limit=80)
        items.append(
            NotificationItemOut(
                id=f"messages:{int(row.id)}",
                kind="messages",
                emoji="💬",
                title=i18n_tr(
                    locale,
                    es="Nuevo mensaje de Guardián",
                    en="New message from Guardian",
                    fr="Nouveau message d'un Gardien",
                ),
                message=f"{sender_name} ({subject}): {body_preview}",
                created_at=row.created_at,
                href=f"/messages.html?thread={int(row.thread_id)}",
            )
        )
    return items


def _collect_achievements_notifications(*, db: Session, user_id: int, locale: str) -> list[NotificationItemOut]:
    rows = db.execute(
        select(AchievementUnlockEvent)
        .where(
            AchievementUnlockEvent.user_id == user_id,
            ~func.lower(AchievementUnlockEvent.category).like("calendar%"),
        )
        .order_by(desc(AchievementUnlockEvent.unlocked_at), desc(AchievementUnlockEvent.id))
        .limit(NOTIFICATION_SOURCE_LIMIT)
    ).scalars().all()

    items: list[NotificationItemOut] = []
    for event in rows:
        title = _trim_text(event.title, limit=90)
        description = _trim_text(event.description, limit=140)
        items.append(
            NotificationItemOut(
                id=f"achievements:{int(event.id)}",
                kind="achievements",
                emoji="🏆",
                title=i18n_tr(
                    locale,
                    es=f"Logro desbloqueado: {title}",
                    en=f"Achievement unlocked: {title}",
                    fr=f"Succès débloqué : {title}",
                ),
                message=description,
                created_at=event.unlocked_at,
                href="/achievements.html",
            )
        )
    return items


def _collect_calendar_notifications(
    *,
    db: Session,
    user: User,
    now_utc: datetime,
    locale: str,
) -> list[NotificationItemOut]:
    user_id = int(user.id)
    items: list[NotificationItemOut] = []

    # Calendar achievements are grouped in the calendar notification channel.
    calendar_events = db.execute(
        select(AchievementUnlockEvent)
        .where(
            AchievementUnlockEvent.user_id == user_id,
            func.lower(AchievementUnlockEvent.category).like("calendar%"),
        )
        .order_by(desc(AchievementUnlockEvent.unlocked_at), desc(AchievementUnlockEvent.id))
        .limit(NOTIFICATION_SOURCE_LIMIT)
    ).scalars().all()
    for event in calendar_events:
        title = _trim_text(event.title, limit=90)
        description = _trim_text(event.description, limit=140)
        items.append(
            NotificationItemOut(
                id=f"calendar-achievement:{int(event.id)}",
                kind="calendar",
                emoji="📆",
                title=i18n_tr(
                    locale,
                    es=f"Logro de calendario: {title}",
                    en=f"Calendar achievement: {title}",
                    fr=f"Succès de calendrier : {title}",
                ),
                message=description,
                created_at=event.unlocked_at,
                href="/calendar.html",
            )
        )

    today_start = _utc_day_start(now_utc)
    tomorrow_start = today_start + timedelta(days=1)
    posts_today = int(
        db.execute(
            select(func.count(Post.id)).where(
                Post.author_id == user_id,
                Post.created_at >= today_start,
                Post.created_at < tomorrow_start,
            )
        ).scalar_one()
        or 0
    )

    if posts_today > 0:
        return items

    lookback_start = today_start - timedelta(days=120)
    day_rows = db.execute(
        select(func.date(Post.created_at))
        .where(
            Post.author_id == user_id,
            Post.created_at >= lookback_start,
            Post.created_at < today_start,
        )
        .group_by(func.date(Post.created_at))
    ).all()

    posted_days = {day for value, in day_rows if (day := _coerce_day(value)) is not None}
    if not posted_days:
        return items

    streak = 0
    cursor = (today_start - timedelta(days=1)).date()
    while cursor in posted_days:
        streak += 1
        cursor -= timedelta(days=1)

    if streak <= 0:
        return items

    items.append(
        NotificationItemOut(
            id=f"calendar-reminder:{today_start.date().isoformat()}",
            kind="calendar",
            emoji="📆",
            title=i18n_tr(
                locale,
                es="Recordatorio de racha",
                en="Streak reminder",
                fr="Rappel de série",
            ),
            message=i18n_tr(
                locale,
                es=f"Aún no has publicado hoy. Si no publicas, podrías perder tu racha actual de {streak} día(s).",
                en=f"You have not posted today yet. If you do not post, you could lose your current streak of {streak} day(s).",
                fr=f"Vous n'avez pas encore publié aujourd'hui. Si vous ne publiez pas, vous pourriez perdre votre série actuelle de {streak} jour(s).",
            ),
            created_at=now_utc,
            href="/calendar.html",
        )
    )
    return items


def _collect_oracle_notifications(
    *,
    db: Session,
    user_id: int,
    now_utc: datetime,
    locale: str,
) -> list[NotificationItemOut]:
    state = db.execute(select(OracleUserState).where(OracleUserState.user_id == user_id)).scalar_one_or_none()
    if state is None or state.last_pick_at is None:
        return []

    last_pick_at = state.last_pick_at
    if last_pick_at.tzinfo is None:
        last_pick_at = last_pick_at.replace(tzinfo=timezone.utc)

    available_at = last_pick_at + ORACLE_COOLDOWN
    if available_at > now_utc:
        return []

    if available_at < now_utc - timedelta(days=30):
        return []

    return [
        NotificationItemOut(
            id=f"oracle-reminder:{available_at.date().isoformat()}",
            kind="oracle",
            emoji="🔮",
            title=i18n_tr(
                locale,
                es="Oráculo disponible",
                en="Oracle available",
                fr="Oracle disponible",
            ),
            message=i18n_tr(
                locale,
                es="Ya puedes abrir el Oráculo de nuevo y revelar una nueva carta.",
                en="You can now open the Oracle again and reveal a new card.",
                fr="Vous pouvez maintenant rouvrir l'Oracle et révéler une nouvelle carte.",
            ),
            created_at=available_at,
            href="/oracle.html",
        )
    ]


def _collect_mentions_notifications(*, db: Session, user_id: int, locale: str) -> list[NotificationItemOut]:
    author_follows_viewer = exists(
        select(UserFollow.id).where(
            UserFollow.follower_id == Post.author_id,
            UserFollow.followed_id == user_id,
        )
    )
    viewer_follows_author = exists(
        select(UserFollow.id).where(
            UserFollow.follower_id == user_id,
            UserFollow.followed_id == Post.author_id,
        )
    )

    rows = db.execute(
        select(
            PostMention.id,
            PostMention.created_at,
            PostMention.post_id,
            Post.text.label("post_text"),
            User.id.label("author_user_id"),
            User.username.label("author_username"),
            User.first_name.label("author_first_name"),
            User.last_name.label("author_last_name"),
        )
        .join(Post, Post.id == PostMention.post_id)
        .join(User, User.id == Post.author_id)
        .where(
            PostMention.mentioned_user_id == user_id,
            Post.author_id != user_id,
            Post.visibility == PostVisibility.public,
            and_(author_follows_viewer, viewer_follows_author),
        )
        .order_by(desc(PostMention.created_at), desc(PostMention.id))
        .limit(NOTIFICATION_SOURCE_LIMIT)
    ).all()

    items: list[NotificationItemOut] = []
    for row in rows:
        author_id = int(row.author_user_id)
        author_name = _display_name(
            first_name=row.author_first_name,
            last_name=row.author_last_name,
            user_id=author_id,
        )
        post_preview = _trim_text(row.post_text, limit=120)
        profile_url = _build_profile_url(user_id=author_id, username=row.author_username)
        joiner = "&" if "?" in profile_url else "?"
        items.append(
            NotificationItemOut(
                id=f"mentions:{int(row.id)}",
                kind="mentions",
                emoji="🏷️",
                title=i18n_tr(
                    locale,
                    es="Te etiquetaron en una publicación",
                    en="You were tagged in a post",
                    fr="Vous avez été mentionné dans une publication",
                ),
                message=i18n_tr(
                    locale,
                    es=f"{author_name} te mencionó: {post_preview or 'La publicación no tiene texto.'}",
                    en=f"{author_name} mentioned you: {post_preview or 'No text in the post.'}",
                    fr=f"{author_name} vous a mentionné : {post_preview or 'Publication sans texte.'}",
                ),
                created_at=row.created_at,
                href=f"{profile_url}{joiner}post={int(row.post_id)}",
            )
        )
    return items


def _collect_stars_notifications(*, db: Session, user: User, locale: str) -> list[NotificationItemOut]:
    user_id = int(user.id)
    home_url = _self_home_url(user)
    rows = db.execute(
        select(
            PostStar.id,
            PostStar.created_at,
            Post.id.label("post_id"),
            User.id.label("sender_user_id"),
            User.username.label("sender_username"),
            User.first_name.label("sender_first_name"),
            User.last_name.label("sender_last_name"),
        )
        .join(Post, Post.id == PostStar.post_id)
        .join(User, User.id == PostStar.user_id)
        .where(
            Post.author_id == user_id,
            PostStar.user_id != user_id,
        )
        .order_by(desc(PostStar.created_at), desc(PostStar.id))
        .limit(NOTIFICATION_SOURCE_LIMIT)
    ).all()

    items: list[NotificationItemOut] = []
    for row in rows:
        sender_id = int(row.sender_user_id)
        sender_name = _display_name(
            first_name=row.sender_first_name,
            last_name=row.sender_last_name,
            user_id=sender_id,
        )
        joiner = "&" if "?" in home_url else "?"
        items.append(
            NotificationItemOut(
                id=f"stars:{int(row.id)}",
                kind="stars",
                emoji="⭐",
                title=i18n_tr(
                    locale,
                    es="Nueva estrella recibida",
                    en="New star received",
                    fr="Nouvelle étoile reçue",
                ),
                message=i18n_tr(
                    locale,
                    es=f"{sender_name} donó una estrella a una de tus publicaciones.",
                    en=f"{sender_name} donated a star to one of your posts.",
                    fr=f"{sender_name} a donné une étoile à l'une de vos publications.",
                ),
                created_at=row.created_at,
                href=f"{home_url}{joiner}post={int(row.post_id)}",
            )
        )
    return items


@router.get("/preferences", response_model=NotificationPreferencesOut)
def get_notification_preferences(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = _load_current_user_or_404(db=db, current=current, locale=locale)
    return _preferences_out(user)


@router.put("/preferences", response_model=NotificationPreferencesOut)
def update_notification_preferences(
    request: Request,
    payload: NotificationPreferencesUpdateIn,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = _load_current_user_or_404(db=db, current=current, locale=locale)

    updates = {
        "notif_calendar_enabled": payload.calendar_enabled,
        "notif_oracle_enabled": payload.oracle_enabled,
        "notif_followers_enabled": payload.followers_enabled,
        "notif_messages_enabled": payload.messages_enabled,
        "notif_achievements_enabled": payload.achievements_enabled,
        "notif_mentions_enabled": payload.mentions_enabled,
        "notif_stars_enabled": payload.stars_enabled,
    }

    changed = False
    for attr_name, maybe_value in updates.items():
        if maybe_value is None:
            continue
        normalized_value = bool(maybe_value)
        if bool(getattr(user, attr_name)) != normalized_value:
            setattr(user, attr_name, normalized_value)
            changed = True

    if changed:
        db.add(user)
        db.commit()
        db.refresh(user)

    return _preferences_out(user)


@router.get("/feed", response_model=NotificationFeedOut)
def get_notifications_feed(
    request: Request,
    limit: int = Query(default=DEFAULT_FEED_LIMIT, ge=1, le=MAX_FEED_LIMIT),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = _load_current_user_or_404(db=db, current=current, locale=locale)
    now_utc = _utcnow()

    all_items: list[NotificationItemOut] = []
    if user.notif_calendar_enabled:
        all_items.extend(_collect_calendar_notifications(db=db, user=user, now_utc=now_utc, locale=locale))
    if user.notif_oracle_enabled:
        all_items.extend(_collect_oracle_notifications(db=db, user_id=int(user.id), now_utc=now_utc, locale=locale))
    if user.notif_followers_enabled:
        all_items.extend(_collect_followers_notifications(db=db, user_id=int(user.id), locale=locale))
    if user.notif_messages_enabled:
        all_items.extend(_collect_messages_notifications(db=db, user_id=int(user.id), locale=locale))
    if user.notif_achievements_enabled:
        all_items.extend(_collect_achievements_notifications(db=db, user_id=int(user.id), locale=locale))
    if user.notif_mentions_enabled:
        all_items.extend(_collect_mentions_notifications(db=db, user_id=int(user.id), locale=locale))
    if user.notif_stars_enabled:
        all_items.extend(_collect_stars_notifications(db=db, user=user, locale=locale))

    sorted_items = sorted(
        all_items,
        key=lambda item: (item.created_at, item.id),
        reverse=True,
    )

    notification_ids = [item.id for item in sorted_items if item.id]
    read_ids: set[str] = set()
    if notification_ids:
        rows = db.execute(
            select(NotificationRead.notification_id).where(
                NotificationRead.user_id == int(user.id),
                NotificationRead.notification_id.in_(notification_ids),
            )
        ).all()
        read_ids = {str(row.notification_id) for row in rows}

    unread_total = 0
    for item in sorted_items:
        is_read = item.id in read_ids
        item.is_read = is_read
        if not is_read:
            unread_total += 1

    total_count = len(sorted_items)
    visible_items = sorted_items[: int(limit)]
    unread_count = max(0, unread_total)

    return NotificationFeedOut(
        items=visible_items,
        total_count=total_count,
        unread_count=unread_count,
        has_more=total_count > len(visible_items),
    )


@router.post("/read", response_model=NotificationReadOut)
def mark_notifications_read(
    request: Request,
    payload: NotificationReadIn,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = _load_current_user_or_404(db=db, current=current, locale=locale)
    raw_ids = payload.notification_ids if isinstance(payload.notification_ids, list) else []

    unique_ids: list[str] = []
    seen: set[str] = set()
    for raw_value in raw_ids[:64]:
        normalized = _normalize_notification_id(str(raw_value))
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        unique_ids.append(normalized)

    if not unique_ids:
        return NotificationReadOut(marked=0)

    existing_rows = db.execute(
        select(NotificationRead.notification_id).where(
            NotificationRead.user_id == int(user.id),
            NotificationRead.notification_id.in_(unique_ids),
        )
    ).all()
    existing_ids = {str(row.notification_id) for row in existing_rows}

    missing_ids = [notif_id for notif_id in unique_ids if notif_id not in existing_ids]
    if not missing_ids:
        return NotificationReadOut(marked=0)

    now_utc = _utcnow()
    for notif_id in missing_ids:
        db.add(
            NotificationRead(
                user_id=int(user.id),
                notification_id=notif_id,
                read_at=now_utc,
            )
        )

    db.commit()
    return NotificationReadOut(marked=len(missing_ids))
