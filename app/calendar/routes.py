from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.achievements.service import compute_achievements_state, sync_achievement_unlock_events
from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.calendar.schemas import CalendarDayActivityOut, CalendarYearActivityOut
from app.db.database import get_db
from app.db.models.achievement_unlock_event import AchievementUnlockEvent
from app.db.models.post import Post, PostStar
from app.db.models.public_cooperative_wish import PublicCooperativeWish
from app.db.models.public_personal_wish import PublicPersonalWish, PublicPersonalWishStatus
from app.db.models.user import User


router = APIRouter(prefix="/calendar", tags=["calendar"])

DEFAULT_YEAR = datetime.now(timezone.utc).year


def _utc_today() -> date:
    return datetime.now(timezone.utc).date()


def _year_window_utc(year: int) -> tuple[datetime, datetime]:
    start = datetime(year, 1, 1, tzinfo=timezone.utc)
    end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    return start, end


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


def _day_count_map(rows: list[tuple[object, object]]) -> dict[date, int]:
    out: dict[date, int] = {}
    for day_value, count in rows:
        day = _coerce_day(day_value)
        if day is None:
            continue
        out[day] = int(count or 0)
    return out


def _merge_count_maps(*maps: dict[date, int]) -> dict[date, int]:
    out: dict[date, int] = {}
    for item_map in maps:
        for day, count in item_map.items():
            out[day] = int(out.get(day, 0)) + int(count or 0)
    return out


def _sync_unlock_events_for_user(*, db: Session, user: User) -> None:
    state = compute_achievements_state(db=db, user=user)
    added = sync_achievement_unlock_events(db=db, user=user, state=state)
    if added <= 0:
        return
    try:
        db.commit()
    except IntegrityError:
        db.rollback()


def _load_current_user_or_404(*, db: Session, current: UserPublic) -> User:
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user


def _load_target_user_or_404(*, db: Session, user_id: int) -> User:
    user = db.execute(
        select(User).where(User.id == user_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user


def _build_year_activity(
    *,
    db: Session,
    user_id: int,
    year: int,
) -> CalendarYearActivityOut:
    start_utc, end_utc = _year_window_utc(year)

    post_day_expr = func.date(Post.created_at)
    posts_map = _day_count_map(
        db.execute(
            select(post_day_expr, func.count(Post.id))
            .where(Post.author_id == user_id)
            .where(Post.created_at >= start_utc)
            .where(Post.created_at < end_utc)
            .group_by(post_day_expr)
        ).all()
    )

    star_day_expr = func.date(PostStar.created_at)
    stars_map = _day_count_map(
        db.execute(
            select(star_day_expr, func.count(PostStar.id))
            .join(Post, Post.id == PostStar.post_id)
            .where(Post.author_id == user_id)
            .where(PostStar.created_at >= start_utc)
            .where(PostStar.created_at < end_utc)
            .group_by(star_day_expr)
        ).all()
    )

    personal_wish_day_expr = func.date(PublicPersonalWish.created_at)
    personal_public_wishes_map = _day_count_map(
        db.execute(
            select(personal_wish_day_expr, func.count(PublicPersonalWish.id))
            .where(PublicPersonalWish.user_id == user_id)
            .where(PublicPersonalWish.created_at >= start_utc)
            .where(PublicPersonalWish.created_at < end_utc)
            .group_by(personal_wish_day_expr)
        ).all()
    )

    cooperative_wish_day_expr = func.date(PublicCooperativeWish.created_at)
    cooperative_public_wishes_map = _day_count_map(
        db.execute(
            select(cooperative_wish_day_expr, func.count(PublicCooperativeWish.id))
            .where(PublicCooperativeWish.user_id == user_id)
            .where(PublicCooperativeWish.created_at >= start_utc)
            .where(PublicCooperativeWish.created_at < end_utc)
            .group_by(cooperative_wish_day_expr)
        ).all()
    )
    public_wishes_map = _merge_count_maps(personal_public_wishes_map, cooperative_public_wishes_map)

    fulfilled_at_expr = func.coalesce(PublicPersonalWish.fulfilled_at, PublicPersonalWish.created_at)
    fulfilled_day_expr = func.date(fulfilled_at_expr)
    fulfilled_wishes_map = _day_count_map(
        db.execute(
            select(fulfilled_day_expr, func.count(PublicPersonalWish.id))
            .where(PublicPersonalWish.user_id == user_id)
            .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
            .where(fulfilled_at_expr >= start_utc)
            .where(fulfilled_at_expr < end_utc)
            .group_by(fulfilled_day_expr)
        ).all()
    )

    achievement_day_expr = func.date(AchievementUnlockEvent.unlocked_at)
    achievements_map = _day_count_map(
        db.execute(
            select(achievement_day_expr, func.count(AchievementUnlockEvent.id))
            .where(AchievementUnlockEvent.user_id == user_id)
            .where(AchievementUnlockEvent.unlocked_at >= start_utc)
            .where(AchievementUnlockEvent.unlocked_at < end_utc)
            .group_by(achievement_day_expr)
        ).all()
    )

    items: list[CalendarDayActivityOut] = []
    active_days_total = 0
    cursor = start_utc.date()
    end_day = (end_utc - timedelta(days=1)).date()
    while cursor <= end_day:
        stars_received = int(stars_map.get(cursor, 0))
        fulfilled_wishes = int(fulfilled_wishes_map.get(cursor, 0))
        public_wishes = int(public_wishes_map.get(cursor, 0))
        achievements = int(achievements_map.get(cursor, 0))
        posts = int(posts_map.get(cursor, 0))
        total_interactions = (
            stars_received
            + fulfilled_wishes
            + public_wishes
            + achievements
            + posts
        )
        has_activity = total_interactions > 0
        if has_activity:
            active_days_total += 1

        items.append(
            CalendarDayActivityOut(
                date_utc=cursor,
                stars_received=stars_received,
                fulfilled_wishes=fulfilled_wishes,
                public_wishes=public_wishes,
                achievements=achievements,
                posts=posts,
                total_interactions=total_interactions,
                has_activity=has_activity,
            )
        )
        cursor += timedelta(days=1)

    return CalendarYearActivityOut(
        user_id=int(user_id),
        year=int(year),
        today_utc=_utc_today(),
        active_days_total=active_days_total,
        items=items,
    )


@router.get("/mine", response_model=CalendarYearActivityOut)
def my_calendar_activity(
    year: int = Query(default=DEFAULT_YEAR, ge=2000, le=2100),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = _load_current_user_or_404(db=db, current=current)
    _sync_unlock_events_for_user(db=db, user=user)
    return _build_year_activity(db=db, user_id=int(user.id), year=year)


@router.get("/user/{user_id}", response_model=CalendarYearActivityOut)
def user_calendar_activity(
    user_id: int,
    year: int = Query(default=DEFAULT_YEAR, ge=2000, le=2100),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target = _load_target_user_or_404(db=db, user_id=user_id)

    is_owner = int(current.user_number) == int(target.id)
    if not is_owner and not bool(target.public_profile_show_calendar):
        raise HTTPException(status_code=403, detail="Este calendario es privado.")

    if is_owner:
        _sync_unlock_events_for_user(db=db, user=target)

    return _build_year_activity(db=db, user_id=int(target.id), year=year)
