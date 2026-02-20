from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.privacy.schemas import PublicProfilePrivacyOut, PublicProfilePrivacyUpdateRequest


router = APIRouter(prefix="/privacy", tags=["privacy"])


def _serialize(user: User) -> PublicProfilePrivacyOut:
    return PublicProfilePrivacyOut(
        public_profile_show_public_wishes=bool(user.public_profile_show_public_wishes),
        public_profile_show_about=bool(user.public_profile_show_about),
        public_profile_show_fulfilled_wishes=bool(user.public_profile_show_fulfilled_wishes),
        public_profile_show_calendar=bool(user.public_profile_show_calendar),
        public_profile_show_oracle=bool(user.public_profile_show_oracle),
        public_profile_show_personal_posts=bool(user.public_profile_show_personal_posts),
    )


@router.get("/mine", response_model=PublicProfilePrivacyOut)
def get_my_privacy_settings(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return _serialize(user)


@router.put("/mine", response_model=PublicProfilePrivacyOut)
def update_my_privacy_settings(
    payload: PublicProfilePrivacyUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        if value is None:
            continue
        if hasattr(user, key):
            setattr(user, key, bool(value))

    db.commit()
    db.refresh(user)
    return _serialize(user)


@router.get("/user/{user_id}", response_model=PublicProfilePrivacyOut)
def get_user_privacy_settings(
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == user_id, User.is_active.is_(True))).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return _serialize(user)
