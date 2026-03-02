from __future__ import annotations

from datetime import datetime, timedelta, timezone
from math import ceil
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import asc, case, desc, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.config import settings
from app.core.i18n import locale_from_request, tr as i18n_tr
from app.core.storage import S3NotConfiguredError, generate_presigned_get_url
from app.db.database import get_db
from app.db.models.media import Media, MediaVisibility
from app.db.models.profile_report import ProfileReport, ProfileReportCase, ProfileReportCaseStatus
from app.db.models.user import User
from app.db.models.user_follow import UserFollow
from app.follows.schemas import (
    FollowActionResponse,
    FollowListResponse,
    FollowUserOut,
    ProfileReportCreateRequest,
    ProfileReportResponse,
)

router = APIRouter(prefix="/follows", tags=["follows"])

PAGE_SIZE_DEFAULT = 25
PAGE_SIZE_MAX = 25
SUGGESTIONS_MAX_PAGES = 20
SUGGESTIONS_RECENT_DAYS = 90
GUARDIANS_MIN_RANK = 3


def _locale(request: Request | None) -> str:
    return locale_from_request(request, default="en")


def _td(locale: str, en: str) -> str:
    translations: dict[str, tuple[str, str]] = {
        "You must send exactly one: user_id or username.": (
            "Debes enviar exactamente uno: user_id o username.",
            "Vous devez envoyer exactement un seul champ : user_id ou username.",
        ),
        "Invalid username.": ("Nombre de usuario inválido.", "Nom d'utilisateur invalide."),
        "User not found.": ("Usuario no encontrado.", "Utilisateur introuvable."),
        "You cannot report your own profile.": (
            "No puedes reportar tu propio perfil.",
            "Vous ne pouvez pas signaler votre propre profil.",
        ),
        "You already reported this profile.": (
            "Ya reportaste este perfil.",
            "Vous avez déjà signalé ce profil.",
        ),
        "You cannot follow yourself.": (
            "No puedes seguirte a ti mismo.",
            "Vous ne pouvez pas vous suivre vous-même.",
        ),
        "You cannot unfollow yourself.": (
            "No puedes dejar de seguirte a ti mismo.",
            "Vous ne pouvez pas arrêter de vous suivre vous-même.",
        ),
    }
    pair = translations.get(en)
    if not pair:
        return en
    es, fr = pair
    return i18n_tr(locale, es=es, en=en, fr=fr)


def _build_profile_url(username: str | None, *, user_id: int) -> str:
    normalized = (username or "").strip()
    if normalized:
        return f"/home_user.html?u={normalized}"
    return f"/home_user.html?id={int(user_id)}"


def _build_handle(*, username: str | None, user_id: int) -> str:
    normalized = (username or "").strip()
    if normalized:
        return f"@{normalized}"
    return f"@id{user_id}"


def _safe_avatar_url(media: Media | None, *, current_user_id: int) -> str | None:
    if media is None:
        return None
    if media.status != "ready":
        return None
    if not (media.mime_type or "").lower().startswith("image/"):
        return None
    if media.visibility == MediaVisibility.private and media.owner_id != current_user_id:
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


def _paginate(
    *,
    total: int,
    page: int,
    page_size: int,
    max_pages: int | None = None,
) -> dict[str, int]:
    normalized_size = max(1, min(int(page_size), PAGE_SIZE_MAX))
    capped_total = max(0, int(total))
    if max_pages is not None:
        capped_total = min(capped_total, normalized_size * max_pages)

    total_pages = max(1, ceil(capped_total / normalized_size)) if capped_total else 1
    normalized_page = max(1, min(int(page), total_pages))
    offset = (normalized_page - 1) * normalized_size

    return {
        "page": normalized_page,
        "page_size": normalized_size,
        "total": capped_total,
        "total_pages": total_pages,
        "offset": offset,
    }


def _followers_count_subquery():
    return (
        select(
            UserFollow.followed_id.label("user_id"),
            func.count(UserFollow.id).label("followers_count"),
        )
        .group_by(UserFollow.followed_id)
        .subquery()
    )


def _count_following(db: Session, *, user_id: int) -> int:
    return int(
        db.execute(
            select(func.count(UserFollow.id)).where(UserFollow.follower_id == user_id)
        ).scalar_one()
        or 0
    )


def _count_followers(db: Session, *, user_id: int) -> int:
    return int(
        db.execute(
            select(func.count(UserFollow.id)).where(UserFollow.followed_id == user_id)
        ).scalar_one()
        or 0
    )


def _load_media_map(db: Session, *, media_ids: list[int]) -> dict[int, Media]:
    if not media_ids:
        return {}
    rows = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
    return {int(media.id): media for media in rows}


def _rows_to_items(
    *,
    db: Session,
    rows: list[Any],
    current_user_id: int,
    is_following_ids: set[int],
    follows_me_ids: set[int],
) -> list[FollowUserOut]:
    if not rows:
        return []

    media_ids = [
        int(row._mapping["profile_photo_media_id"])
        for row in rows
        if row._mapping["profile_photo_media_id"] is not None
    ]
    media_map = _load_media_map(db, media_ids=media_ids)

    items: list[FollowUserOut] = []
    for row in rows:
        payload = row._mapping
        user_id = int(payload["user_id"])
        username = (payload["username"] or "").strip() or None
        first_name = (payload["first_name"] or "").strip()
        last_name = (payload["last_name"] or "").strip()
        full_name = f"{first_name} {last_name}".strip() or f"User {user_id}"
        show_followers_count = user_id == int(current_user_id) or bool(payload.get("public_profile_show_followers", True))
        show_stars_total = user_id == int(current_user_id) or bool(payload.get("public_profile_show_stars", True))

        media_id = payload["profile_photo_media_id"]
        media = media_map.get(int(media_id)) if media_id is not None else None

        items.append(
            FollowUserOut(
                user_id=user_id,
                full_name=full_name,
                username=username,
                handle=_build_handle(username=username, user_id=user_id),
                profile_url=_build_profile_url(username, user_id=user_id),
                avatar_url=_safe_avatar_url(media, current_user_id=current_user_id),
                role=payload["role"],
                guardian_rank=payload["guardian_rank"],
                followers_count=max(0, int(payload["followers_count"] or 0)) if show_followers_count else 0,
                received_stars_total=max(0, int(payload["received_stars_total"] or 0)) if show_stars_total else 0,
                is_following=user_id in is_following_ids,
                follows_me=user_id in follows_me_ids,
            )
        )

    return items


def _build_follow_list_response(
    *,
    page_data: dict[str, int],
    items: list[FollowUserOut],
) -> FollowListResponse:
    total = page_data["total"]
    offset = page_data["offset"]
    range_start = offset + 1 if total > 0 and items else 0
    range_end = offset + len(items) if total > 0 and items else 0

    return FollowListResponse(
        items=items,
        page=page_data["page"],
        page_size=page_data["page_size"],
        total=total,
        total_pages=page_data["total_pages"],
        range_start=range_start,
        range_end=range_end,
    )


def _fetch_following_ids(db: Session, *, current_user_id: int, target_ids: list[int]) -> set[int]:
    if not target_ids:
        return set()
    rows = db.execute(
        select(UserFollow.followed_id).where(
            UserFollow.follower_id == current_user_id,
            UserFollow.followed_id.in_(target_ids),
        )
    ).all()
    return {int(row[0]) for row in rows}


def _fetch_follows_me_ids(db: Session, *, current_user_id: int, target_ids: list[int]) -> set[int]:
    if not target_ids:
        return set()
    rows = db.execute(
        select(UserFollow.follower_id).where(
            UserFollow.followed_id == current_user_id,
            UserFollow.follower_id.in_(target_ids),
        )
    ).all()
    return {int(row[0]) for row in rows}


@router.get("/profile", response_model=FollowUserOut)
def get_user_profile(
    request: Request,
    user_id: int | None = Query(default=None, ge=1),
    username: str | None = Query(default=None),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    if bool(user_id) == bool(username):
        raise HTTPException(
            status_code=400,
            detail=_td(locale, "You must send exactly one: user_id or username."),
        )

    current_user_id = current.user_number
    target_user: User | None = None

    if user_id is not None:
        target_user = db.execute(
            select(User).where(
                User.id == user_id,
                User.is_active.is_(True),
            )
        ).scalar_one_or_none()
    else:
        normalized = (username or "").strip().lower()
        while normalized.startswith("@"):
            normalized = normalized[1:]
        if not normalized:
            raise HTTPException(status_code=400, detail=_td(locale, "Invalid username."))

        target_user = db.execute(
            select(User).where(
                User.username == normalized,
                User.is_active.is_(True),
            )
        ).scalar_one_or_none()

    if target_user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    media: Media | None = None
    if target_user.profile_photo_media_id is not None:
        media = db.execute(
            select(Media).where(Media.id == target_user.profile_photo_media_id)
        ).scalar_one_or_none()

    is_following_ids = _fetch_following_ids(
        db,
        current_user_id=current_user_id,
        target_ids=[int(target_user.id)],
    )
    follows_me_ids = _fetch_follows_me_ids(
        db,
        current_user_id=current_user_id,
        target_ids=[int(target_user.id)],
    )

    normalized_username = (target_user.username or "").strip() or None
    full_name = f"{(target_user.first_name or '').strip()} {(target_user.last_name or '').strip()}".strip() or f"User {target_user.id}"
    is_owner = int(target_user.id) == int(current_user_id)
    followers_count = _count_followers(db, user_id=int(target_user.id)) if is_owner or bool(target_user.public_profile_show_followers) else 0
    received_stars_total = max(0, int(target_user.received_stars_total or 0)) if is_owner or bool(target_user.public_profile_show_stars) else 0

    return FollowUserOut(
        user_id=int(target_user.id),
        full_name=full_name,
        username=normalized_username,
        handle=_build_handle(username=normalized_username, user_id=int(target_user.id)),
        profile_url=_build_profile_url(normalized_username, user_id=int(target_user.id)),
        avatar_url=_safe_avatar_url(media, current_user_id=current_user_id),
        role=target_user.role,
        guardian_rank=target_user.guardian_rank,
        followers_count=followers_count,
        received_stars_total=received_stars_total,
        is_following=int(target_user.id) in is_following_ids,
        follows_me=int(target_user.id) in follows_me_ids,
    )


@router.get("/suggestions", response_model=FollowListResponse)
def list_follow_suggestions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=PAGE_SIZE_DEFAULT, ge=1, le=PAGE_SIZE_MAX),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user_id = current.user_number
    followed_ids_subquery = select(UserFollow.followed_id).where(
        UserFollow.follower_id == current_user_id
    )

    base_filters = (
        User.is_active.is_(True),
        User.id != current_user_id,
        ~User.id.in_(followed_ids_subquery),
    )

    total = int(
        db.execute(select(func.count(User.id)).where(*base_filters)).scalar_one() or 0
    )
    page_data = _paginate(
        total=total,
        page=page,
        page_size=page_size,
        max_pages=SUGGESTIONS_MAX_PAGES,
    )

    followers_count_sq = _followers_count_subquery()
    recent_cutoff = datetime.now(timezone.utc) - timedelta(days=SUGGESTIONS_RECENT_DAYS)
    is_guardian_expr = case(
        (or_(User.role == "guardian", User.guardian_rank.is_not(None)), 1),
        else_=0,
    )
    is_recent_expr = case((User.created_at >= recent_cutoff, 1), else_=0)

    rows = db.execute(
        select(
            User.id.label("user_id"),
            User.first_name.label("first_name"),
            User.last_name.label("last_name"),
            User.username.label("username"),
            User.role.label("role"),
            User.guardian_rank.label("guardian_rank"),
            User.profile_photo_media_id.label("profile_photo_media_id"),
            User.received_stars_total.label("received_stars_total"),
            User.public_profile_show_followers.label("public_profile_show_followers"),
            User.public_profile_show_stars.label("public_profile_show_stars"),
            func.coalesce(followers_count_sq.c.followers_count, 0).label("followers_count"),
        )
        .outerjoin(followers_count_sq, followers_count_sq.c.user_id == User.id)
        .where(*base_filters)
        .order_by(
            desc(is_guardian_expr),
            desc(is_recent_expr),
            desc(func.coalesce(followers_count_sq.c.followers_count, 0)),
            desc(User.received_stars_total),
            desc(User.created_at),
            asc(User.id),
        )
        .offset(page_data["offset"])
        .limit(page_data["page_size"])
    ).all()

    user_ids = [int(row._mapping["user_id"]) for row in rows]
    is_following_ids = _fetch_following_ids(
        db,
        current_user_id=current_user_id,
        target_ids=user_ids,
    )
    follows_me_ids = _fetch_follows_me_ids(
        db,
        current_user_id=current_user_id,
        target_ids=user_ids,
    )
    items = _rows_to_items(
        db=db,
        rows=rows,
        current_user_id=current_user_id,
        is_following_ids=is_following_ids,
        follows_me_ids=follows_me_ids,
    )
    return _build_follow_list_response(page_data=page_data, items=items)


@router.get("/guardians", response_model=FollowListResponse)
def list_guardians(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=4, ge=1, le=PAGE_SIZE_MAX),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user_id = current.user_number

    base_filters = (
        User.is_active.is_(True),
        User.guardian_rank.is_not(None),
        User.guardian_rank >= GUARDIANS_MIN_RANK,
    )

    total = int(db.execute(select(func.count(User.id)).where(*base_filters)).scalar_one() or 0)
    page_data = _paginate(total=total, page=page, page_size=page_size, max_pages=None)

    followers_count_sq = _followers_count_subquery()
    rows = db.execute(
        select(
            User.id.label("user_id"),
            User.first_name.label("first_name"),
            User.last_name.label("last_name"),
            User.username.label("username"),
            User.role.label("role"),
            User.guardian_rank.label("guardian_rank"),
            User.profile_photo_media_id.label("profile_photo_media_id"),
            User.received_stars_total.label("received_stars_total"),
            User.public_profile_show_followers.label("public_profile_show_followers"),
            User.public_profile_show_stars.label("public_profile_show_stars"),
            func.coalesce(followers_count_sq.c.followers_count, 0).label("followers_count"),
        )
        .outerjoin(followers_count_sq, followers_count_sq.c.user_id == User.id)
        .where(*base_filters)
        .order_by(desc(User.guardian_rank), asc(User.id))
        .offset(page_data["offset"])
        .limit(page_data["page_size"])
    ).all()

    user_ids = [int(row._mapping["user_id"]) for row in rows]
    is_following_ids = _fetch_following_ids(db, current_user_id=current_user_id, target_ids=user_ids)
    follows_me_ids = _fetch_follows_me_ids(db, current_user_id=current_user_id, target_ids=user_ids)
    items = _rows_to_items(
        db=db,
        rows=rows,
        current_user_id=current_user_id,
        is_following_ids=is_following_ids,
        follows_me_ids=follows_me_ids,
    )
    return _build_follow_list_response(page_data=page_data, items=items)


@router.get("/followers", response_model=FollowListResponse)
def list_my_followers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=PAGE_SIZE_DEFAULT, ge=1, le=PAGE_SIZE_MAX),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user_id = current.user_number

    total = int(
        db.execute(
            select(func.count(User.id))
            .select_from(UserFollow)
            .join(User, User.id == UserFollow.follower_id)
            .where(
                UserFollow.followed_id == current_user_id,
                User.is_active.is_(True),
            )
        ).scalar_one()
        or 0
    )
    page_data = _paginate(total=total, page=page, page_size=page_size)

    followers_count_sq = _followers_count_subquery()
    rows = db.execute(
        select(
            User.id.label("user_id"),
            User.first_name.label("first_name"),
            User.last_name.label("last_name"),
            User.username.label("username"),
            User.role.label("role"),
            User.guardian_rank.label("guardian_rank"),
            User.profile_photo_media_id.label("profile_photo_media_id"),
            User.received_stars_total.label("received_stars_total"),
            User.public_profile_show_followers.label("public_profile_show_followers"),
            User.public_profile_show_stars.label("public_profile_show_stars"),
            func.coalesce(followers_count_sq.c.followers_count, 0).label("followers_count"),
        )
        .select_from(UserFollow)
        .join(User, User.id == UserFollow.follower_id)
        .outerjoin(followers_count_sq, followers_count_sq.c.user_id == User.id)
        .where(
            UserFollow.followed_id == current_user_id,
            User.is_active.is_(True),
        )
        .order_by(desc(UserFollow.created_at), asc(User.id))
        .offset(page_data["offset"])
        .limit(page_data["page_size"])
    ).all()

    user_ids = [int(row._mapping["user_id"]) for row in rows]
    is_following_ids = _fetch_following_ids(
        db,
        current_user_id=current_user_id,
        target_ids=user_ids,
    )
    items = _rows_to_items(
        db=db,
        rows=rows,
        current_user_id=current_user_id,
        is_following_ids=is_following_ids,
        follows_me_ids=set(user_ids),
    )
    return _build_follow_list_response(page_data=page_data, items=items)


@router.get("/following", response_model=FollowListResponse)
def list_my_following(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=PAGE_SIZE_DEFAULT, ge=1, le=PAGE_SIZE_MAX),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user_id = current.user_number

    total = int(
        db.execute(
            select(func.count(User.id))
            .select_from(UserFollow)
            .join(User, User.id == UserFollow.followed_id)
            .where(
                UserFollow.follower_id == current_user_id,
                User.is_active.is_(True),
            )
        ).scalar_one()
        or 0
    )
    page_data = _paginate(total=total, page=page, page_size=page_size)

    followers_count_sq = _followers_count_subquery()
    rows = db.execute(
        select(
            User.id.label("user_id"),
            User.first_name.label("first_name"),
            User.last_name.label("last_name"),
            User.username.label("username"),
            User.role.label("role"),
            User.guardian_rank.label("guardian_rank"),
            User.profile_photo_media_id.label("profile_photo_media_id"),
            User.received_stars_total.label("received_stars_total"),
            User.public_profile_show_followers.label("public_profile_show_followers"),
            User.public_profile_show_stars.label("public_profile_show_stars"),
            func.coalesce(followers_count_sq.c.followers_count, 0).label("followers_count"),
        )
        .select_from(UserFollow)
        .join(User, User.id == UserFollow.followed_id)
        .outerjoin(followers_count_sq, followers_count_sq.c.user_id == User.id)
        .where(
            UserFollow.follower_id == current_user_id,
            User.is_active.is_(True),
        )
        .order_by(desc(UserFollow.created_at), asc(User.id))
        .offset(page_data["offset"])
        .limit(page_data["page_size"])
    ).all()

    user_ids = [int(row._mapping["user_id"]) for row in rows]
    follows_me_ids = _fetch_follows_me_ids(
        db,
        current_user_id=current_user_id,
        target_ids=user_ids,
    )
    items = _rows_to_items(
        db=db,
        rows=rows,
        current_user_id=current_user_id,
        is_following_ids=set(user_ids),
        follows_me_ids=follows_me_ids,
    )
    return _build_follow_list_response(page_data=page_data, items=items)


@router.post("/profile/{target_user_id}/reports", response_model=ProfileReportResponse)
def report_profile(
    request: Request,
    target_user_id: int,
    payload: ProfileReportCreateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    current_user_id = int(current.user_number)
    if int(target_user_id) == current_user_id:
        raise HTTPException(status_code=400, detail=_td(locale, "You cannot report your own profile."))

    target_user = db.execute(
        select(User).where(
            User.id == target_user_id,
            User.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if target_user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    now = datetime.now(timezone.utc)
    report_case = db.execute(
        select(ProfileReportCase).where(ProfileReportCase.reported_user_id == int(target_user_id))
    ).scalar_one_or_none()
    if report_case is None:
        report_case = ProfileReportCase(
            reported_user_id=int(target_user_id),
            status=ProfileReportCaseStatus.open,
            report_count=0,
            first_reported_at=now,
            last_reported_at=now,
        )
        db.add(report_case)
        db.flush()
    else:
        if report_case.status != ProfileReportCaseStatus.open:
            report_case.status = ProfileReportCaseStatus.open
            report_case.resolved_at = None
            report_case.resolved_by_guardian_id = None
        report_case.updated_at = now

    report = ProfileReport(
        case_id=int(report_case.id),
        reported_user_id=int(target_user_id),
        reporter_id=current_user_id,
        reason=payload.reason,
        other_reason=(payload.other_reason or "").strip() or None,
    )
    db.add(report)

    report_case.report_count = max(0, int(report_case.report_count or 0)) + 1
    if report_case.first_reported_at is None:
        report_case.first_reported_at = now
    report_case.last_reported_at = now

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=_td(locale, "You already reported this profile."))

    return ProfileReportResponse(reported=True, target_user_id=int(target_user_id), reason=payload.reason)


@router.post("/{target_user_id}", response_model=FollowActionResponse, status_code=status.HTTP_200_OK)
def follow_user(
    request: Request,
    target_user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    current_user_id = current.user_number
    if target_user_id == current_user_id:
        raise HTTPException(status_code=400, detail=_td(locale, "You cannot follow yourself."))

    target_user = db.execute(
        select(User).where(
            User.id == target_user_id,
            User.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if target_user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    relation = db.execute(
        select(UserFollow).where(
            UserFollow.follower_id == current_user_id,
            UserFollow.followed_id == target_user_id,
        )
    ).scalar_one_or_none()

    if relation is None:
        db.add(
            UserFollow(
                follower_id=current_user_id,
                followed_id=target_user_id,
            )
        )
        try:
            db.commit()
        except IntegrityError:
            db.rollback()

    return FollowActionResponse(
        target_user_id=target_user_id,
        is_following=True,
        my_following_total=_count_following(db, user_id=current_user_id),
        target_followers_total=(
            _count_followers(db, user_id=target_user_id)
            if bool(target_user.public_profile_show_followers)
            else 0
        ),
    )


@router.delete("/{target_user_id}", response_model=FollowActionResponse)
def unfollow_user(
    request: Request,
    target_user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    current_user_id = current.user_number
    if target_user_id == current_user_id:
        raise HTTPException(status_code=400, detail=_td(locale, "You cannot unfollow yourself."))

    relation = db.execute(
        select(UserFollow).where(
            UserFollow.follower_id == current_user_id,
            UserFollow.followed_id == target_user_id,
        )
    ).scalar_one_or_none()

    if relation is not None:
        db.delete(relation)
        db.commit()

    target_user = db.execute(
        select(User).where(
            User.id == target_user_id,
            User.is_active.is_(True),
        )
    ).scalar_one_or_none()
    show_target_followers = bool(target_user.public_profile_show_followers) if target_user is not None else True

    return FollowActionResponse(
        target_user_id=target_user_id,
        is_following=False,
        my_following_total=_count_following(db, user_id=current_user_id),
        target_followers_total=_count_followers(db, user_id=target_user_id) if show_target_followers else 0,
    )
