from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.achievements.definitions import (
    CALENDAR_STREAK_ACHIEVEMENTS,
    DONATION_STAR_ACHIEVEMENTS,
    FULFILLED_WISH_ACHIEVEMENTS,
    GRANTED_WISH_ACHIEVEMENTS,
    GUARDIAN_RANK_ACHIEVEMENTS,
    PUBLICATION_STAR_ACHIEVEMENTS,
)
from app.achievements.schemas import (
    AchievementBadgeOut,
    AchievementsStateResponse,
    AchievementsTotalsOut,
)
from app.db.models.achievement_unlock_event import AchievementUnlockEvent
from app.db.models.post import Post, PostStar
from app.db.models.private_personal_wish import PrivatePersonalWish, PrivatePersonalWishStatus
from app.db.models.public_personal_wish import PublicPersonalWish, PublicPersonalWishStatus
from app.db.models.public_wish_fulfillment import PublicWishFulfillment
from app.db.models.user import User


CATEGORY_PUBLICATION_STARS = "publication_stars"
CATEGORY_FULFILLED_WISHES = "fulfilled_wishes"
CATEGORY_GRANTED_WISHES = "granted_wishes"
CATEGORY_CALENDAR_STREAK = "calendar_streak"
CATEGORY_DONATION_STARS = "donation_stars"
CATEGORY_GUARDIAN_RANK = "guardian_rank"


@dataclass(slots=True)
class AchievementsComputedState:
    my_received_stars_total: int
    my_donated_stars_total: int
    my_donatable_stars_total: int
    totals: AchievementsTotalsOut
    publication_achievements: list[AchievementBadgeOut]
    fulfilled_wishes_achievements: list[AchievementBadgeOut]
    granted_wishes_achievements: list[AchievementBadgeOut]
    calendar_achievements: list[AchievementBadgeOut]
    donation_achievements: list[AchievementBadgeOut]
    guardian_rank_achievements: list[AchievementBadgeOut]
    milestones_by_category: dict[str, dict[int, datetime]]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_aware_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _normalize_star_totals(user: User) -> tuple[int, int, int]:
    received = max(0, int(user.received_stars_total or 0))
    donated = max(0, int(user.donated_stars_total or 0))
    donated = min(donated, received)
    donatable = max(0, received - donated)
    return received, donated, donatable


def _build_badges(*, current_total: int, definitions: list[tuple[str, str, int, str]]) -> list[AchievementBadgeOut]:
    return [
        AchievementBadgeOut(
            key=key,
            title=title,
            threshold=threshold,
            image_url=image_url,
            unlocked=current_total >= threshold,
        )
        for key, title, threshold, image_url in definitions
    ]


def _build_threshold_milestones_from_timestamps(
    *,
    thresholds: list[int],
    timestamps: list[datetime],
) -> dict[int, datetime]:
    milestones: dict[int, datetime] = {}
    if not thresholds or not timestamps:
        return milestones

    ordered_thresholds = sorted({int(item) for item in thresholds if int(item) > 0})
    threshold_index = 0
    for index, ts in enumerate(timestamps, start=1):
        while threshold_index < len(ordered_thresholds) and index >= ordered_thresholds[threshold_index]:
            milestones[ordered_thresholds[threshold_index]] = ts
            threshold_index += 1
        if threshold_index >= len(ordered_thresholds):
            break
    return milestones


def _load_publication_star_milestones(*, db: Session, user_id: int) -> dict[int, datetime]:
    thresholds = [threshold for _, _, threshold, _ in PUBLICATION_STAR_ACHIEVEMENTS]
    rows = db.execute(
        select(PostStar.created_at)
        .join(Post, Post.id == PostStar.post_id)
        .where(Post.author_id == user_id)
        .order_by(PostStar.created_at.asc(), PostStar.id.asc())
    ).all()
    timestamps = [_ensure_aware_utc(row[0]) for row in rows]
    normalized = [item for item in timestamps if item is not None]
    return _build_threshold_milestones_from_timestamps(thresholds=thresholds, timestamps=normalized)


def _load_fulfilled_wish_timestamps(*, db: Session, user_id: int) -> list[datetime]:
    public_rows = db.execute(
        select(PublicPersonalWish.fulfilled_at, PublicPersonalWish.created_at)
        .where(PublicPersonalWish.user_id == user_id)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
        .order_by(PublicPersonalWish.fulfilled_at.asc().nullslast(), PublicPersonalWish.id.asc())
    ).all()
    private_rows = db.execute(
        select(PrivatePersonalWish.fulfilled_at, PrivatePersonalWish.created_at)
        .where(PrivatePersonalWish.user_id == user_id)
        .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.fulfilled)
        .order_by(PrivatePersonalWish.fulfilled_at.asc().nullslast(), PrivatePersonalWish.id.asc())
    ).all()

    merged: list[datetime] = []
    for fulfilled_at, created_at in [*public_rows, *private_rows]:
        resolved = _ensure_aware_utc(fulfilled_at) or _ensure_aware_utc(created_at)
        if resolved is not None:
            merged.append(resolved)
    merged.sort()
    return merged


def _load_granted_wish_timestamps(*, db: Session, user_id: int) -> list[datetime]:
    rows = db.execute(
        select(PublicWishFulfillment.created_at)
        .where(PublicWishFulfillment.fulfiller_user_id == user_id)
        .order_by(PublicWishFulfillment.created_at.asc(), PublicWishFulfillment.id.asc())
    ).all()
    timestamps = [_ensure_aware_utc(row[0]) for row in rows]
    return [item for item in timestamps if item is not None]


def _calendar_profile(*, db: Session, user_id: int) -> tuple[int, dict[int, datetime]]:
    rows = db.execute(
        select(Post.created_at)
        .where(Post.author_id == user_id)
        .order_by(Post.created_at.asc(), Post.id.asc())
    ).all()

    unique_days: list[date] = []
    last_day: date | None = None
    for row in rows:
        created_at = _ensure_aware_utc(row[0])
        if created_at is None:
            continue
        day = created_at.date()
        if day != last_day:
            unique_days.append(day)
            last_day = day

    if not unique_days:
        return 0, {}

    thresholds = sorted({threshold for _, _, threshold, _ in CALENDAR_STREAK_ACHIEVEMENTS})
    threshold_index = 0
    milestones: dict[int, datetime] = {}

    max_streak = 0
    current_streak = 0
    previous_day: date | None = None
    for day in unique_days:
        if previous_day is not None and day == previous_day + timedelta(days=1):
            current_streak += 1
        else:
            current_streak = 1
        max_streak = max(max_streak, current_streak)

        while threshold_index < len(thresholds) and current_streak >= thresholds[threshold_index]:
            threshold = thresholds[threshold_index]
            milestones[threshold] = datetime.combine(
                day,
                time(hour=23, minute=59, second=59, tzinfo=timezone.utc),
            )
            threshold_index += 1

        previous_day = day

    return max_streak, milestones


def _rank_milestones(*, user: User) -> dict[int, datetime]:
    rank = max(0, int(user.guardian_rank or 0))
    if rank <= 0:
        return {}

    unlocked_at = _ensure_aware_utc(user.updated_at) or _ensure_aware_utc(user.created_at) or _utc_now()
    return {
        threshold: unlocked_at
        for _, _, threshold, _ in GUARDIAN_RANK_ACHIEVEMENTS
        if rank >= threshold
    }


def compute_achievements_state(*, db: Session, user: User) -> AchievementsComputedState:
    received, donated, donatable = _normalize_star_totals(user)

    public_fulfilled_total = int(
        db.execute(
            select(func.count(PublicPersonalWish.id))
            .where(PublicPersonalWish.user_id == user.id)
            .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
        ).scalar_one()
        or 0
    )
    private_fulfilled_total = int(
        db.execute(
            select(func.count(PrivatePersonalWish.id))
            .where(PrivatePersonalWish.user_id == user.id)
            .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.fulfilled)
        ).scalar_one()
        or 0
    )
    fulfilled_total = max(0, public_fulfilled_total + private_fulfilled_total)

    granted_total = int(
        db.execute(
            select(func.count(PublicWishFulfillment.id)).where(PublicWishFulfillment.fulfiller_user_id == user.id)
        ).scalar_one()
        or 0
    )
    granted_total = max(0, granted_total)

    calendar_streak_days, calendar_milestones = _calendar_profile(db=db, user_id=int(user.id))
    guardian_rank_current = max(0, int(user.guardian_rank or 0))

    publication_milestones = _load_publication_star_milestones(db=db, user_id=int(user.id))

    fulfilled_milestones = _build_threshold_milestones_from_timestamps(
        thresholds=[threshold for _, _, threshold, _ in FULFILLED_WISH_ACHIEVEMENTS],
        timestamps=_load_fulfilled_wish_timestamps(db=db, user_id=int(user.id)),
    )
    granted_milestones = _build_threshold_milestones_from_timestamps(
        thresholds=[threshold for _, _, threshold, _ in GRANTED_WISH_ACHIEVEMENTS],
        timestamps=_load_granted_wish_timestamps(db=db, user_id=int(user.id)),
    )

    totals = AchievementsTotalsOut(
        publication_stars_total=received,
        donation_stars_total=donated,
        fulfilled_wishes_total=fulfilled_total,
        granted_wishes_total=granted_total,
        calendar_streak_days=calendar_streak_days,
        guardian_rank_current=guardian_rank_current,
    )

    return AchievementsComputedState(
        my_received_stars_total=received,
        my_donated_stars_total=donated,
        my_donatable_stars_total=donatable,
        totals=totals,
        publication_achievements=_build_badges(
            current_total=received,
            definitions=PUBLICATION_STAR_ACHIEVEMENTS,
        ),
        fulfilled_wishes_achievements=_build_badges(
            current_total=fulfilled_total,
            definitions=FULFILLED_WISH_ACHIEVEMENTS,
        ),
        granted_wishes_achievements=_build_badges(
            current_total=granted_total,
            definitions=GRANTED_WISH_ACHIEVEMENTS,
        ),
        calendar_achievements=_build_badges(
            current_total=calendar_streak_days,
            definitions=CALENDAR_STREAK_ACHIEVEMENTS,
        ),
        donation_achievements=_build_badges(
            current_total=donated,
            definitions=DONATION_STAR_ACHIEVEMENTS,
        ),
        guardian_rank_achievements=_build_badges(
            current_total=guardian_rank_current,
            definitions=GUARDIAN_RANK_ACHIEVEMENTS,
        ),
        milestones_by_category={
            CATEGORY_PUBLICATION_STARS: publication_milestones,
            CATEGORY_FULFILLED_WISHES: fulfilled_milestones,
            CATEGORY_GRANTED_WISHES: granted_milestones,
            CATEGORY_CALENDAR_STREAK: calendar_milestones,
            CATEGORY_DONATION_STARS: {},
            CATEGORY_GUARDIAN_RANK: _rank_milestones(user=user),
        },
    )


def build_achievements_state_response(*, state: AchievementsComputedState) -> AchievementsStateResponse:
    return AchievementsStateResponse(
        my_received_stars_total=state.my_received_stars_total,
        my_donated_stars_total=state.my_donated_stars_total,
        my_donatable_stars_total=state.my_donatable_stars_total,
        totals=state.totals,
        publication_achievements=state.publication_achievements,
        fulfilled_wishes_achievements=state.fulfilled_wishes_achievements,
        granted_wishes_achievements=state.granted_wishes_achievements,
        calendar_achievements=state.calendar_achievements,
        donation_achievements=state.donation_achievements,
        guardian_rank_achievements=state.guardian_rank_achievements,
    )


def _format_int_es(value: int) -> str:
    return f"{int(value):,}".replace(",", ".")


def _achievement_description(*, category: str, threshold: int, title: str) -> str:
    if category == CATEGORY_PUBLICATION_STARS:
        return f"You reached {_format_int_es(threshold)} stars from your posts"
    if category == CATEGORY_DONATION_STARS:
        return (
            "You accumulated a donation of more than "
            f"{_format_int_es(threshold)} stars to the Common Star Pool"
        )
    if category == CATEGORY_FULFILLED_WISHES:
        noun = "wish" if int(threshold) == 1 else "wishes"
        return f"You fulfilled {_format_int_es(threshold)} {noun}"
    if category == CATEGORY_GRANTED_WISHES:
        noun = "wish" if int(threshold) == 1 else "wishes"
        return f"You helped fulfill {_format_int_es(threshold)} {noun}"
    if category == CATEGORY_CALENDAR_STREAK:
        if int(threshold) == 1:
            return "You made your 1st calendar post"
        if int(threshold) == 3:
            return "You posted for 3 consecutive days"
        if int(threshold) == 7:
            return "You reached a 7-day posting streak"
        return (
            "You have posted actively on this social network, maintaining a streak of "
            f"{_format_int_es(threshold)} days"
        )
    if category == CATEGORY_GUARDIAN_RANK:
        return f"You were promoted to Rank {_format_int_es(threshold)} in the Guardian hierarchy: now you are {title}!"
    return "Achievement unlocked."


def _fallback_unlock_time_for_category(*, category: str, user: User, now_utc: datetime) -> datetime:
    if category in {CATEGORY_DONATION_STARS, CATEGORY_GUARDIAN_RANK}:
        return _ensure_aware_utc(user.updated_at) or _ensure_aware_utc(user.created_at) or now_utc
    return now_utc


def sync_achievement_unlock_events(
    *,
    db: Session,
    user: User,
    state: AchievementsComputedState,
) -> int:
    existing_keys = set(
        db.execute(
            select(AchievementUnlockEvent.achievement_key).where(AchievementUnlockEvent.user_id == user.id)
        ).scalars().all()
    )

    category_definitions: list[tuple[str, int, list[tuple[str, str, int, str]]]] = [
        (
            CATEGORY_PUBLICATION_STARS,
            int(state.totals.publication_stars_total),
            PUBLICATION_STAR_ACHIEVEMENTS,
        ),
        (
            CATEGORY_FULFILLED_WISHES,
            int(state.totals.fulfilled_wishes_total),
            FULFILLED_WISH_ACHIEVEMENTS,
        ),
        (
            CATEGORY_GRANTED_WISHES,
            int(state.totals.granted_wishes_total),
            GRANTED_WISH_ACHIEVEMENTS,
        ),
        (
            CATEGORY_CALENDAR_STREAK,
            int(state.totals.calendar_streak_days),
            CALENDAR_STREAK_ACHIEVEMENTS,
        ),
        (
            CATEGORY_DONATION_STARS,
            int(state.totals.donation_stars_total),
            DONATION_STAR_ACHIEVEMENTS,
        ),
        (
            CATEGORY_GUARDIAN_RANK,
            int(state.totals.guardian_rank_current),
            GUARDIAN_RANK_ACHIEVEMENTS,
        ),
    ]

    now_utc = _utc_now()
    added = 0
    for category, total, definitions in category_definitions:
        category_milestones = state.milestones_by_category.get(category, {})
        for key, title, threshold, image_url in definitions:
            if key in existing_keys:
                continue
            if total < threshold:
                continue

            unlocked_at = category_milestones.get(int(threshold))
            if unlocked_at is None:
                unlocked_at = _fallback_unlock_time_for_category(category=category, user=user, now_utc=now_utc)

            db.add(
                AchievementUnlockEvent(
                    user_id=int(user.id),
                    achievement_key=key,
                    category=category,
                    title=title,
                    description=_achievement_description(category=category, threshold=threshold, title=title),
                    image_url=image_url,
                    unlocked_at=unlocked_at,
                )
            )
            existing_keys.add(key)
            added += 1

    return added
