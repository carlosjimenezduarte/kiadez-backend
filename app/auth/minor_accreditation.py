from __future__ import annotations

from datetime import date

from app.db.models.user import User


MINOR_AGE_LIMIT = 18

MINOR_STATUS_NOT_REQUIRED = "not_required"
MINOR_STATUS_PENDING = "pending"
MINOR_STATUS_REQUESTED = "requested"
MINOR_STATUS_APPROVED = "approved"
MINOR_STATUS_VALUES = {
    MINOR_STATUS_NOT_REQUIRED,
    MINOR_STATUS_PENDING,
    MINOR_STATUS_REQUESTED,
    MINOR_STATUS_APPROVED,
}

MINOR_RELATIONSHIP_FATHER = "padre"
MINOR_RELATIONSHIP_MOTHER = "madre"
MINOR_RELATIONSHIP_LEGAL_GUARDIAN = "tutor_legal"
MINOR_RELATIONSHIP_RESPONSIBLE_ADULT = "adulto_responsable"
MINOR_RELATIONSHIP_VALUES = {
    MINOR_RELATIONSHIP_FATHER,
    MINOR_RELATIONSHIP_MOTHER,
    MINOR_RELATIONSHIP_LEGAL_GUARDIAN,
    MINOR_RELATIONSHIP_RESPONSIBLE_ADULT,
}
MINOR_RELATIONSHIP_LABELS = {
    MINOR_RELATIONSHIP_FATHER: "Padre",
    MINOR_RELATIONSHIP_MOTHER: "Madre",
    MINOR_RELATIONSHIP_LEGAL_GUARDIAN: "Tutor legal",
    MINOR_RELATIONSHIP_RESPONSIBLE_ADULT: "Adulto responsable",
}

MINOR_PRIVATE_PROFILE_FIELDS = (
    "public_profile_show_public_wishes",
    "public_profile_show_about",
    "public_profile_show_fulfilled_wishes",
    "public_profile_show_calendar",
    "public_profile_show_oracle",
    "public_profile_show_personal_posts",
    "public_profile_show_cooperative_wishes",
    "public_profile_show_followers",
    "public_profile_show_gallery",
    "public_profile_show_recent_achievements",
    "public_profile_show_stars",
    "public_profile_show_cover_purposes",
    "public_profile_show_biography",
)


def calculate_age(birth_date: date, today: date | None = None) -> int:
    current_day = today or date.today()
    return current_day.year - birth_date.year - (
        (current_day.month, current_day.day) < (birth_date.month, birth_date.day)
    )


def is_underage(birth_date: date, today: date | None = None) -> bool:
    return calculate_age(birth_date, today=today) < MINOR_AGE_LIMIT


def normalize_minor_status(raw_status: str | None) -> str:
    value = str(raw_status or "").strip().lower()
    if value in MINOR_STATUS_VALUES:
        return value
    return MINOR_STATUS_NOT_REQUIRED


def normalize_minor_relationship(raw_relationship: str | None) -> str:
    value = str(raw_relationship or "").strip().lower()
    if value in MINOR_RELATIONSHIP_VALUES:
        return value
    return MINOR_RELATIONSHIP_RESPONSIBLE_ADULT


def minor_relationship_label(relationship: str | None) -> str:
    normalized = normalize_minor_relationship(relationship)
    return MINOR_RELATIONSHIP_LABELS.get(normalized, "Adulto responsable")


def resolve_minor_status(user: User, today: date | None = None) -> str:
    birth_date = getattr(user, "birth_date", None)
    if not birth_date or not is_underage(birth_date, today=today):
        return MINOR_STATUS_NOT_REQUIRED

    status = normalize_minor_status(getattr(user, "minor_accreditation_status", None))
    if status == MINOR_STATUS_NOT_REQUIRED:
        return MINOR_STATUS_PENDING
    return status


def is_minor_protected(user: User, today: date | None = None) -> bool:
    return resolve_minor_status(user, today=today) in {
        MINOR_STATUS_PENDING,
        MINOR_STATUS_REQUESTED,
    }


def can_publish_public(user: User, today: date | None = None) -> bool:
    return not is_minor_protected(user, today=today)


def force_minor_private_profile_flags(user: User, today: date | None = None) -> bool:
    if not is_minor_protected(user, today=today):
        return False

    changed = False
    for field_name in MINOR_PRIVATE_PROFILE_FIELDS:
        if bool(getattr(user, field_name, False)):
            setattr(user, field_name, False)
            changed = True
    return changed
