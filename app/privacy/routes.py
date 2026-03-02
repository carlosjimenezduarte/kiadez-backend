from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.minor_accreditation import force_minor_private_profile_flags, is_minor_protected
from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.i18n import locale_from_request, tr as i18n_tr
from app.db.database import get_db
from app.db.models.user import User
from app.privacy.schemas import PublicProfilePrivacyOut, PublicProfilePrivacyUpdateRequest


router = APIRouter(prefix="/privacy", tags=["privacy"])


def _msg_user_not_found(locale: str) -> str:
    return i18n_tr(locale, es="Usuario no encontrado.", en="User not found.", fr="Utilisateur introuvable.")


def _serialize(user: User) -> PublicProfilePrivacyOut:
    if is_minor_protected(user):
        return PublicProfilePrivacyOut(
            public_profile_show_public_wishes=False,
            public_profile_show_about=False,
            public_profile_show_fulfilled_wishes=False,
            public_profile_show_calendar=False,
            public_profile_show_oracle=False,
            public_profile_show_personal_posts=False,
            public_profile_show_cooperative_wishes=False,
            public_profile_show_followers=False,
            public_profile_show_gallery=False,
            public_profile_show_recent_achievements=False,
            public_profile_show_stars=False,
            public_profile_show_cover_purposes=False,
            public_profile_show_biography=False,
        )

    return PublicProfilePrivacyOut(
        public_profile_show_public_wishes=bool(user.public_profile_show_public_wishes),
        public_profile_show_about=bool(user.public_profile_show_about),
        public_profile_show_fulfilled_wishes=bool(user.public_profile_show_fulfilled_wishes),
        public_profile_show_calendar=bool(user.public_profile_show_calendar),
        public_profile_show_oracle=bool(user.public_profile_show_oracle),
        public_profile_show_personal_posts=bool(user.public_profile_show_personal_posts),
        public_profile_show_cooperative_wishes=bool(user.public_profile_show_cooperative_wishes),
        public_profile_show_followers=bool(user.public_profile_show_followers),
        public_profile_show_gallery=bool(user.public_profile_show_gallery),
        public_profile_show_recent_achievements=bool(user.public_profile_show_recent_achievements),
        public_profile_show_stars=bool(user.public_profile_show_stars),
        public_profile_show_cover_purposes=bool(user.public_profile_show_cover_purposes),
        public_profile_show_biography=bool(user.public_profile_show_biography),
    )


@router.get("/mine", response_model=PublicProfilePrivacyOut)
def get_my_privacy_settings(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = locale_from_request(request, default="en")
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))
    return _serialize(user)


@router.put("/mine", response_model=PublicProfilePrivacyOut)
def update_my_privacy_settings(
    request: Request,
    payload: PublicProfilePrivacyUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = locale_from_request(request, default="en")
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        if value is None:
            continue
        if hasattr(user, key):
            setattr(user, key, bool(value))

    force_minor_private_profile_flags(user)

    db.commit()
    db.refresh(user)
    return _serialize(user)


@router.get("/user/{user_id}", response_model=PublicProfilePrivacyOut)
def get_user_privacy_settings(
    request: Request,
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = locale_from_request(request, default="en")
    user = db.execute(select(User).where(User.id == user_id, User.is_active.is_(True))).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))
    return _serialize(user)
