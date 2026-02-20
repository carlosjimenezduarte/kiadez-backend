from __future__ import annotations

from datetime import datetime, time, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.achievements.schemas import (
    AchievementsStateResponse,
    WeeklyAchievementOut,
    WeeklyAchievementsResponse,
)
from app.achievements.service import (
    build_achievements_state_response,
    compute_achievements_state,
    sync_achievement_unlock_events,
)
from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.db.database import get_db
from app.db.models.achievement_unlock_event import AchievementUnlockEvent
from app.db.models.user import User


router = APIRouter(prefix="/achievements", tags=["achievements"])


def _week_window_utc(now_utc: datetime) -> tuple[datetime, datetime]:
    # Python weekday: Monday=0 ... Sunday=6
    week_start_date = (now_utc - timedelta(days=now_utc.weekday())).date()
    start = datetime.combine(week_start_date, time.min, tzinfo=timezone.utc)
    end = start + timedelta(days=7)
    return start, end


def _load_current_user_or_404(*, db: Session, current: UserPublic) -> User:
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user


def _sync_user_achievements(*, db: Session, user: User) -> None:
    state = compute_achievements_state(db=db, user=user)
    added = sync_achievement_unlock_events(db=db, user=user, state=state)
    if added <= 0:
        return
    try:
        db.commit()
    except IntegrityError:
        db.rollback()


@router.get("/mine/state", response_model=AchievementsStateResponse)
def my_achievements_state(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = _load_current_user_or_404(db=db, current=current)
    state = compute_achievements_state(db=db, user=user)
    added = sync_achievement_unlock_events(db=db, user=user, state=state)
    if added > 0:
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
    return build_achievements_state_response(state=state)


@router.get("/mine/weekly", response_model=WeeklyAchievementsResponse)
def my_weekly_achievements(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = _load_current_user_or_404(db=db, current=current)
    _sync_user_achievements(db=db, user=user)

    now_utc = datetime.now(timezone.utc)
    week_start_utc, week_end_utc = _week_window_utc(now_utc)

    rows = db.execute(
        select(AchievementUnlockEvent)
        .where(AchievementUnlockEvent.user_id == current.user_number)
        .where(AchievementUnlockEvent.unlocked_at >= week_start_utc)
        .where(AchievementUnlockEvent.unlocked_at < week_end_utc)
        .order_by(AchievementUnlockEvent.unlocked_at.desc(), AchievementUnlockEvent.id.desc())
        .limit(200)
    ).scalars().all()

    items = [
        WeeklyAchievementOut(
            achievement_key=row.achievement_key,
            category=row.category,
            title=row.title,
            description=row.description,
            image_url=row.image_url,
            unlocked_at=row.unlocked_at,
        )
        for row in rows
    ]

    return WeeklyAchievementsResponse(
        week_start_utc=week_start_utc,
        week_end_utc=week_end_utc,
        items=items,
    )
