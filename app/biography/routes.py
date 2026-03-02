from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.biography.schemas import (
    BiographyAboutOut,
    BiographyAboutUpdateRequest,
    BiographyActivityStatsOut,
    BiographyCuriositiesOut,
    BiographyCuriositiesUpdateRequest,
    BiographyDreamOut,
    BiographyDreamUpdateRequest,
    BiographyDistinctionSlot,
    BiographyDistinctionsOut,
    BiographyDistinctionsUpdateRequest,
    BiographyFavoriteQuotesOut,
    BiographyFavoriteQuotesUpdateRequest,
    BiographyLifeAchievementsOut,
    BiographyLifeAchievementsUpdateRequest,
    BiographyProfessionalAchievementsOut,
    BiographyProfessionalAchievementsUpdateRequest,
    BiographyPersonalInfoOut,
    BiographyPersonalInfoUpdateRequest,
    BiographyEducationOut,
    BiographyEducationUpdateRequest,
    BiographyProfessionalInfoOut,
    BiographyProfessionalInfoUpdateRequest,
    BiographyPhysicalTraitsOut,
    BiographyPhysicalTraitsUpdateRequest,
)
from app.core.i18n import locale_from_request, tr as i18n_tr
from app.db.database import get_db
from app.db.models.biography_curiosities import BiographyCuriosities
from app.db.models.biography_personal_info import BiographyPersonalInfo
from app.db.models.biography_education import BiographyEducation
from app.db.models.biography_about import BiographyAbout
from app.db.models.biography_dream import BiographyDream
from app.db.models.biography_distinctions import BiographyDistinctions
from app.db.models.biography_favorite_quotes import BiographyFavoriteQuotes
from app.db.models.biography_life_achievements import BiographyLifeAchievements
from app.db.models.biography_professional_achievements import BiographyProfessionalAchievements
from app.db.models.biography_professional_info import BiographyProfessionalInfo
from app.db.models.biography_physical_traits import BiographyPhysicalTraits
from app.db.models.private_personal_wish import PrivatePersonalWish, PrivatePersonalWishStatus
from app.db.models.public_cooperative_wish_fulfillment import PublicCooperativeWishFulfillment
from app.db.models.public_personal_wish import PublicPersonalWish, PublicPersonalWishStatus
from app.db.models.public_wish_fulfillment import PublicWishFulfillment
from app.db.models.user import User

router = APIRouter(prefix="/biography", tags=["biography"])
MAX_ABOUT_WORDS = 1200
MAX_DREAM_WORDS = 1200
MAX_PRO_ACHIEVEMENTS_WORDS = 500
MAX_LIFE_ACHIEVEMENTS_WORDS = 500
MAX_FAVORITE_QUOTES_WORDS = 500
DISTINCTIONS_MAX_SLOTS = 10
GUARDIANS_MIN_RANK = 3
DEFAULT_DREAM_TITLES = {
    "es": "Sobre su mayor sueño",
    "en": "About their greatest dream",
    "fr": "À propos de leur plus grand rêve",
}
DEFAULT_PRO_ACHIEVEMENTS_TITLES = {
    "es": "Logros profesionales",
    "en": "Professional achievements",
    "fr": "Réalisations professionnelles",
}
DEFAULT_LIFE_ACHIEVEMENTS_TITLES = {
    "es": "Logros de vida",
    "en": "Life achievements",
    "fr": "Réalisations de vie",
}
DEFAULT_FAVORITE_QUOTES_TITLES = {
    "es": "Frases favoritas",
    "en": "Favorite quotes",
    "fr": "Citations favorites",
}

MONTH_NAMES = {
    "en": (
        "",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ),
    "es": (
        "",
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ),
    "fr": (
        "",
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "août",
        "septembre",
        "octobre",
        "novembre",
        "décembre",
    ),
}


def _locale(request: Request) -> str:
    return locale_from_request(request, default="en")


def _title_for_locale(locale: str, titles: dict[str, str]) -> str:
    return titles.get(locale, titles["en"])


def _msg_user_not_found(locale: str) -> str:
    return i18n_tr(locale, es="Usuario no encontrado.", en="User not found.", fr="Utilisateur introuvable.")


def _msg_guardian_only(locale: str) -> str:
    return i18n_tr(
        locale,
        es="Esta sección solo puede ser actualizada por Guardianes de Kiadez.com.",
        en="This section can only be updated by Kiadez.com Guardians.",
        fr="Cette section ne peut être mise à jour que par les Gardiens de Kiadez.com.",
    )


def _msg_biography_hidden(locale: str) -> str:
    return i18n_tr(
        locale,
        es="Esta biografía de perfil está oculta por configuración de privacidad.",
        en="This profile biography is hidden by privacy settings.",
        fr="Cette biographie de profil est masquée par les paramètres de confidentialité.",
    )


def _msg_about_hidden(locale: str) -> str:
    return i18n_tr(
        locale,
        es='La sección "Sobre mí" está oculta por configuración de privacidad.',
        en='The "About me" section is hidden by privacy settings.',
        fr='La section "À propos de moi" est masquée par les paramètres de confidentialité.',
    )


def _msg_birth_date_future(locale: str) -> str:
    return i18n_tr(
        locale,
        es="La fecha de nacimiento no puede estar en el futuro.",
        en="Birth date cannot be in the future.",
        fr="La date de naissance ne peut pas être dans le futur.",
    )


def _msg_word_limit(locale: str, *, section: str, max_words: int) -> str:
    if section == "biography":
        return i18n_tr(
            locale,
            es=f"La biografía permite un máximo de {max_words} palabras.",
            en=f"Biography allows a maximum of {max_words} words.",
            fr=f"La biographie autorise un maximum de {max_words} mots.",
        )
    if section == "dream":
        return i18n_tr(
            locale,
            es=f"El mayor sueño permite un máximo de {max_words} palabras.",
            en=f"Greatest dream allows a maximum of {max_words} words.",
            fr=f"Le plus grand rêve autorise un maximum de {max_words} mots.",
        )
    if section == "professional_achievements":
        return i18n_tr(
            locale,
            es=f"Los logros profesionales permiten un máximo de {max_words} palabras.",
            en=f"Professional achievements allow a maximum of {max_words} words.",
            fr=f"Les réalisations professionnelles autorisent un maximum de {max_words} mots.",
        )
    if section == "life_achievements":
        return i18n_tr(
            locale,
            es=f"Los logros de vida permiten un máximo de {max_words} palabras.",
            en=f"Life achievements allow a maximum of {max_words} words.",
            fr=f"Les réalisations de vie autorisent un maximum de {max_words} mots.",
        )
    return i18n_tr(
        locale,
        es=f"Las citas favoritas permiten un máximo de {max_words} palabras.",
        en=f"Favorite quotes allow a maximum of {max_words} words.",
        fr=f"Les citations favorites autorisent un maximum de {max_words} mots.",
    )


def _calculate_age(birth_date: date) -> int:
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def _compose_birth_display(
    *,
    locale: str,
    birth_date: date | None,
    birth_city: str | None,
    birth_region: str | None,
    birth_country: str | None,
) -> str | None:
    if birth_date is None:
        return None

    age = _calculate_age(birth_date)
    normalized_locale = locale if locale in MONTH_NAMES else "en"
    month = MONTH_NAMES[normalized_locale][birth_date.month]
    if normalized_locale == "es":
        formatted_date = f"{birth_date.day} de {month} de {birth_date.year}"
    elif normalized_locale == "fr":
        formatted_date = f"{birth_date.day} {month} {birth_date.year}"
    else:
        formatted_date = f"{month} {birth_date.day}, {birth_date.year}"
    age_label = i18n_tr(locale, es=f"{age} años", en=f"{age} years old", fr=f"{age} ans")

    location_parts = [part for part in (birth_city, birth_region, birth_country) if part]
    if location_parts:
        return f"{formatted_date} ({age_label}); {', '.join(location_parts)}"
    return f"{formatted_date} ({age_label})"


def _serialize_personal_info(
    *,
    locale: str,
    user: User,
    personal_info: BiographyPersonalInfo | None,
) -> BiographyPersonalInfoOut:
    birth_name = personal_info.birth_name if personal_info else None
    birth_date = personal_info.birth_date if personal_info else None
    birth_city = personal_info.birth_city if personal_info else None
    birth_region = personal_info.birth_region if personal_info else None
    birth_country = personal_info.birth_country if personal_info else None

    if birth_name is None:
        birth_name = f"{user.first_name} {user.last_name}".strip() or None
    if birth_date is None:
        birth_date = user.birth_date

    return BiographyPersonalInfoOut(
        birth_name=birth_name,
        birth_date=birth_date,
        birth_city=birth_city,
        birth_region=birth_region,
        birth_country=birth_country,
        birth_display=_compose_birth_display(
            locale=locale,
            birth_date=birth_date,
            birth_city=birth_city,
            birth_region=birth_region,
            birth_country=birth_country,
        ),
        residence=personal_info.residence if personal_info else None,
        nationality=personal_info.nationality if personal_info else None,
        native_language=personal_info.native_language if personal_info else None,
        pseudonyms=personal_info.pseudonyms if personal_info else None,
    )


def _serialize_physical_traits(
    *,
    physical_traits: BiographyPhysicalTraits | None,
) -> BiographyPhysicalTraitsOut:
    return BiographyPhysicalTraitsOut(
        height=physical_traits.height if physical_traits else None,
        weight=physical_traits.weight if physical_traits else None,
        eyes=physical_traits.eyes if physical_traits else None,
        hair=physical_traits.hair if physical_traits else None,
    )


def _serialize_education(
    *,
    education: BiographyEducation | None,
) -> BiographyEducationOut:
    return BiographyEducationOut(
        slot1=education.slot1 if education else None,
        slot2=education.slot2 if education else None,
        slot3=education.slot3 if education else None,
        slot4=education.slot4 if education else None,
    )


def _serialize_curiosities(
    *,
    curiosities: BiographyCuriosities | None,
) -> BiographyCuriositiesOut:
    return BiographyCuriositiesOut(
        favorite_superhero=curiosities.favorite_superhero if curiosities else None,
        favorite_song=curiosities.favorite_song if curiosities else None,
        favorite_food=curiosities.favorite_food if curiosities else None,
        videogames=curiosities.videogames if curiosities else None,
        favorite_book=curiosities.favorite_book if curiosities else None,
        other_hobbies=curiosities.other_hobbies if curiosities else None,
        motto=curiosities.motto if curiosities else None,
    )


def _serialize_professional_info(
    *,
    professional_info: BiographyProfessionalInfo | None,
) -> BiographyProfessionalInfoOut:
    return BiographyProfessionalInfoOut(
        occupation=professional_info.occupation if professional_info else None,
        active_years=professional_info.active_years if professional_info else None,
    )


def _count_words(value: str | None) -> int:
    if not value:
        return 0
    return len([word for word in value.split() if word])


def _serialize_about(
    *,
    user: User,
    about: BiographyAbout | None,
) -> BiographyAboutOut:
    fallback_name = f"{user.first_name} {user.last_name}".strip() or None
    display_name = about.display_name if about else None
    about_text = about.about_text if about else None
    return BiographyAboutOut(
        display_name=display_name or fallback_name,
        about_text=about_text,
        word_count=_count_words(about_text),
    )


def _serialize_dream(
    *,
    locale: str,
    dream: BiographyDream | None,
) -> BiographyDreamOut:
    dream_title = dream.dream_title if dream else None
    dream_text = dream.dream_text if dream else None
    return BiographyDreamOut(
        dream_title=dream_title or _title_for_locale(locale, DEFAULT_DREAM_TITLES),
        dream_text=dream_text,
        word_count=_count_words(dream_text),
    )


def _serialize_professional_achievements(
    *,
    locale: str,
    section: BiographyProfessionalAchievements | None,
) -> BiographyProfessionalAchievementsOut:
    section_title = section.section_title if section else None
    section_text = section.section_text if section else None
    return BiographyProfessionalAchievementsOut(
        section_title=section_title or _title_for_locale(locale, DEFAULT_PRO_ACHIEVEMENTS_TITLES),
        section_text=section_text,
        word_count=_count_words(section_text),
    )


def _serialize_life_achievements(
    *,
    locale: str,
    section: BiographyLifeAchievements | None,
) -> BiographyLifeAchievementsOut:
    section_title = section.section_title if section else None
    section_text = section.section_text if section else None
    return BiographyLifeAchievementsOut(
        section_title=section_title or _title_for_locale(locale, DEFAULT_LIFE_ACHIEVEMENTS_TITLES),
        section_text=section_text,
        word_count=_count_words(section_text),
    )


def _serialize_favorite_quotes(
    *,
    locale: str,
    section: BiographyFavoriteQuotes | None,
) -> BiographyFavoriteQuotesOut:
    section_title = section.section_title if section else None
    section_text = section.section_text if section else None
    return BiographyFavoriteQuotesOut(
        section_title=section_title or _title_for_locale(locale, DEFAULT_FAVORITE_QUOTES_TITLES),
        section_text=section_text,
        word_count=_count_words(section_text),
    )


def _is_guardian(current: UserPublic) -> bool:
    return int(current.guardian_rank or 0) >= GUARDIANS_MIN_RANK


def _require_guardian(current: UserPublic, locale: str) -> None:
    if _is_guardian(current):
        return
    raise HTTPException(
        status_code=403,
        detail=_msg_guardian_only(locale),
    )


def _ensure_public_biography_visibility(
    *,
    user: User,
    viewer_user_id: int,
    locale: str,
) -> None:
    if int(user.id) == int(viewer_user_id):
        return
    if not bool(user.public_profile_show_biography):
        raise HTTPException(status_code=403, detail=_msg_biography_hidden(locale))


def _serialize_distinctions(
    *,
    distinctions: BiographyDistinctions | None,
) -> BiographyDistinctionsOut:
    slots: list[BiographyDistinctionSlot] = []
    for slot_number in range(1, DISTINCTIONS_MAX_SLOTS + 1):
        slot_type = getattr(distinctions, f"slot{slot_number}_type", None) if distinctions else None
        slot_description = getattr(distinctions, f"slot{slot_number}_description", None) if distinctions else None
        slots.append(
            BiographyDistinctionSlot(
                distinction_type=slot_type,
                description=slot_description,
            )
        )
    return BiographyDistinctionsOut(slots=slots)


def _apply_distinctions_payload(
    *,
    distinctions: BiographyDistinctions,
    payload: BiographyDistinctionsUpdateRequest,
) -> None:
    slots = payload.slots[:DISTINCTIONS_MAX_SLOTS]
    for slot_number in range(1, DISTINCTIONS_MAX_SLOTS + 1):
        slot = slots[slot_number - 1] if slot_number - 1 < len(slots) else None
        setattr(
            distinctions,
            f"slot{slot_number}_type",
            slot.distinction_type if slot else None,
        )
        setattr(
            distinctions,
            f"slot{slot_number}_description",
            slot.description if slot else None,
        )


@router.get("/activity-stats", response_model=BiographyActivityStatsOut)
def get_activity_stats(
    request: Request,
    user_id: int | None = Query(default=None, ge=1),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    target_user_id = int(current.user_number)
    requested_user_id = int(user_id) if user_id is not None else None
    show_cooperative_stats = True

    if requested_user_id is not None and requested_user_id != int(current.user_number):
        target_user = db.execute(
            select(User).where(
                User.id == requested_user_id,
                User.is_active.is_(True),
            )
        ).scalar_one_or_none()
        if target_user is None:
            raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))
        _ensure_public_biography_visibility(
            user=target_user,
            viewer_user_id=current.user_number,
            locale=locale,
        )
        target_user_id = int(target_user.id)
        show_cooperative_stats = bool(target_user.public_profile_show_cooperative_wishes)
    else:
        current_user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
        if current_user is None:
            raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    public_wishes_fulfilled = int(
        db.execute(
            select(func.count(PublicPersonalWish.id))
            .where(PublicPersonalWish.user_id == target_user_id)
            .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
        ).scalar_one()
        or 0
    )

    private_wishes_fulfilled = int(
        db.execute(
            select(func.count(PrivatePersonalWish.id))
            .where(PrivatePersonalWish.user_id == target_user_id)
            .where(PrivatePersonalWish.status == PrivatePersonalWishStatus.fulfilled)
        ).scalar_one()
        or 0
    )

    cooperative_wishes_fulfilled = 0
    if show_cooperative_stats:
        cooperative_wishes_fulfilled = int(
            db.execute(
                select(func.count(PublicCooperativeWishFulfillment.id)).where(
                    PublicCooperativeWishFulfillment.wish_owner_user_id == target_user_id
                )
            ).scalar_one()
            or 0
        )

    wishes_fulfilled_total = max(0, public_wishes_fulfilled + private_wishes_fulfilled)

    wishes_granted = int(
        db.execute(
            select(func.count(PublicWishFulfillment.id)).where(
                PublicWishFulfillment.fulfiller_user_id == target_user_id
            )
        ).scalar_one()
        or 0
    )

    return BiographyActivityStatsOut(
        wishes_fulfilled=wishes_fulfilled_total,
        cooperative_wishes_fulfilled=max(0, cooperative_wishes_fulfilled),
        wishes_granted=max(0, wishes_granted),
    )


@router.get("/personal-info", response_model=BiographyPersonalInfoOut)
def get_personal_info(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    personal_info = db.execute(
        select(BiographyPersonalInfo).where(BiographyPersonalInfo.user_id == current.user_number)
    ).scalar_one_or_none()

    return _serialize_personal_info(locale=locale, user=user, personal_info=personal_info)


@router.put("/personal-info", response_model=BiographyPersonalInfoOut)
def upsert_personal_info(
    request: Request,
    payload: BiographyPersonalInfoUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    if payload.birth_date and payload.birth_date > date.today():
        raise HTTPException(status_code=400, detail=_msg_birth_date_future(locale))

    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    personal_info = db.execute(
        select(BiographyPersonalInfo).where(BiographyPersonalInfo.user_id == current.user_number)
    ).scalar_one_or_none()
    if personal_info is None:
        personal_info = BiographyPersonalInfo(user_id=current.user_number)
        db.add(personal_info)

    personal_info.birth_name = payload.birth_name
    personal_info.birth_date = payload.birth_date
    personal_info.birth_city = payload.birth_city
    personal_info.birth_region = payload.birth_region
    personal_info.birth_country = payload.birth_country
    personal_info.residence = payload.residence
    personal_info.nationality = payload.nationality
    personal_info.native_language = payload.native_language
    personal_info.pseudonyms = payload.pseudonyms

    db.commit()
    db.refresh(personal_info)

    return _serialize_personal_info(locale=locale, user=user, personal_info=personal_info)


@router.get("/physical-traits", response_model=BiographyPhysicalTraitsOut)
def get_physical_traits(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    physical_traits = db.execute(
        select(BiographyPhysicalTraits).where(BiographyPhysicalTraits.user_id == current.user_number)
    ).scalar_one_or_none()

    return _serialize_physical_traits(physical_traits=physical_traits)


@router.put("/physical-traits", response_model=BiographyPhysicalTraitsOut)
def upsert_physical_traits(
    request: Request,
    payload: BiographyPhysicalTraitsUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    physical_traits = db.execute(
        select(BiographyPhysicalTraits).where(BiographyPhysicalTraits.user_id == current.user_number)
    ).scalar_one_or_none()
    if physical_traits is None:
        physical_traits = BiographyPhysicalTraits(user_id=current.user_number)
        db.add(physical_traits)

    physical_traits.height = payload.height
    physical_traits.weight = payload.weight
    physical_traits.eyes = payload.eyes
    physical_traits.hair = payload.hair

    db.commit()
    db.refresh(physical_traits)

    return _serialize_physical_traits(physical_traits=physical_traits)


@router.get("/education", response_model=BiographyEducationOut)
def get_education(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    education = db.execute(select(BiographyEducation).where(BiographyEducation.user_id == current.user_number)).scalar_one_or_none()
    return _serialize_education(education=education)


@router.put("/education", response_model=BiographyEducationOut)
def upsert_education(
    request: Request,
    payload: BiographyEducationUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    education = db.execute(select(BiographyEducation).where(BiographyEducation.user_id == current.user_number)).scalar_one_or_none()
    if education is None:
        education = BiographyEducation(user_id=current.user_number)
        db.add(education)

    education.slot1 = payload.slot1
    education.slot2 = payload.slot2
    education.slot3 = payload.slot3
    education.slot4 = payload.slot4

    db.commit()
    db.refresh(education)

    return _serialize_education(education=education)


@router.get("/curiosities", response_model=BiographyCuriositiesOut)
def get_curiosities(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    curiosities = db.execute(select(BiographyCuriosities).where(BiographyCuriosities.user_id == current.user_number)).scalar_one_or_none()
    return _serialize_curiosities(curiosities=curiosities)


@router.put("/curiosities", response_model=BiographyCuriositiesOut)
def upsert_curiosities(
    request: Request,
    payload: BiographyCuriositiesUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    curiosities = db.execute(select(BiographyCuriosities).where(BiographyCuriosities.user_id == current.user_number)).scalar_one_or_none()
    if curiosities is None:
        curiosities = BiographyCuriosities(user_id=current.user_number)
        db.add(curiosities)

    curiosities.favorite_superhero = payload.favorite_superhero
    curiosities.favorite_song = payload.favorite_song
    curiosities.favorite_food = payload.favorite_food
    curiosities.videogames = payload.videogames
    curiosities.favorite_book = payload.favorite_book
    curiosities.other_hobbies = payload.other_hobbies
    curiosities.motto = payload.motto

    db.commit()
    db.refresh(curiosities)

    return _serialize_curiosities(curiosities=curiosities)


@router.get("/professional-info", response_model=BiographyProfessionalInfoOut)
def get_professional_info(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    professional_info = db.execute(
        select(BiographyProfessionalInfo).where(BiographyProfessionalInfo.user_id == current.user_number)
    ).scalar_one_or_none()
    return _serialize_professional_info(professional_info=professional_info)


@router.put("/professional-info", response_model=BiographyProfessionalInfoOut)
def upsert_professional_info(
    request: Request,
    payload: BiographyProfessionalInfoUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    professional_info = db.execute(
        select(BiographyProfessionalInfo).where(BiographyProfessionalInfo.user_id == current.user_number)
    ).scalar_one_or_none()
    if professional_info is None:
        professional_info = BiographyProfessionalInfo(user_id=current.user_number)
        db.add(professional_info)

    professional_info.occupation = payload.occupation
    professional_info.active_years = payload.active_years

    db.commit()
    db.refresh(professional_info)

    return _serialize_professional_info(professional_info=professional_info)


@router.get("/distinctions", response_model=BiographyDistinctionsOut)
def get_distinctions(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    distinctions = db.execute(
        select(BiographyDistinctions).where(BiographyDistinctions.user_id == current.user_number)
    ).scalar_one_or_none()
    return _serialize_distinctions(distinctions=distinctions)


@router.get("/distinctions/{user_id}", response_model=BiographyDistinctionsOut)
def get_distinctions_for_user(
    request: Request,
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(
        select(User).where(
            User.id == user_id,
            User.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    _ensure_public_biography_visibility(
        user=user,
        viewer_user_id=current.user_number,
        locale=locale,
    )

    distinctions = db.execute(
        select(BiographyDistinctions).where(BiographyDistinctions.user_id == user_id)
    ).scalar_one_or_none()
    return _serialize_distinctions(distinctions=distinctions)


@router.put("/distinctions", response_model=BiographyDistinctionsOut)
def upsert_distinctions(
    request: Request,
    payload: BiographyDistinctionsUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_guardian(current, locale)

    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    distinctions = db.execute(
        select(BiographyDistinctions).where(BiographyDistinctions.user_id == current.user_number)
    ).scalar_one_or_none()
    if distinctions is None:
        distinctions = BiographyDistinctions(user_id=current.user_number)
        db.add(distinctions)

    _apply_distinctions_payload(distinctions=distinctions, payload=payload)
    db.commit()
    db.refresh(distinctions)
    return _serialize_distinctions(distinctions=distinctions)


@router.put("/distinctions/{user_id}", response_model=BiographyDistinctionsOut)
def upsert_distinctions_for_user(
    request: Request,
    user_id: int,
    payload: BiographyDistinctionsUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_guardian(current, locale)

    user = db.execute(
        select(User).where(
            User.id == user_id,
            User.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    distinctions = db.execute(
        select(BiographyDistinctions).where(BiographyDistinctions.user_id == user_id)
    ).scalar_one_or_none()
    if distinctions is None:
        distinctions = BiographyDistinctions(user_id=user_id)
        db.add(distinctions)

    _apply_distinctions_payload(distinctions=distinctions, payload=payload)
    db.commit()
    db.refresh(distinctions)
    return _serialize_distinctions(distinctions=distinctions)


@router.get("/about", response_model=BiographyAboutOut)
def get_about(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    about = db.execute(select(BiographyAbout).where(BiographyAbout.user_id == current.user_number)).scalar_one_or_none()
    return _serialize_about(user=user, about=about)


@router.get("/about/{user_id}", response_model=BiographyAboutOut)
def get_about_for_user(
    request: Request,
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    # Public profile about section (requires auth, but exposes only non-sensitive fields).
    user = db.execute(
        select(User).where(
            User.id == user_id,
            User.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    _ensure_public_biography_visibility(
        user=user,
        viewer_user_id=current.user_number,
        locale=locale,
    )

    is_owner = int(current.user_number) == int(user_id)
    if not is_owner and not bool(user.public_profile_show_about):
        raise HTTPException(status_code=403, detail=_msg_about_hidden(locale))

    about = db.execute(select(BiographyAbout).where(BiographyAbout.user_id == user_id)).scalar_one_or_none()
    return _serialize_about(user=user, about=about)


@router.put("/about", response_model=BiographyAboutOut)
def upsert_about(
    request: Request,
    payload: BiographyAboutUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    if _count_words(payload.about_text) > MAX_ABOUT_WORDS:
        raise HTTPException(
            status_code=400,
            detail=_msg_word_limit(locale, section="biography", max_words=MAX_ABOUT_WORDS),
        )

    about = db.execute(select(BiographyAbout).where(BiographyAbout.user_id == current.user_number)).scalar_one_or_none()
    if about is None:
        about = BiographyAbout(user_id=current.user_number)
        db.add(about)

    about.display_name = payload.display_name
    about.about_text = payload.about_text

    db.commit()
    db.refresh(about)

    return _serialize_about(user=user, about=about)


@router.get("/dream", response_model=BiographyDreamOut)
def get_dream(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    dream = db.execute(select(BiographyDream).where(BiographyDream.user_id == current.user_number)).scalar_one_or_none()
    return _serialize_dream(locale=locale, dream=dream)


@router.put("/dream", response_model=BiographyDreamOut)
def upsert_dream(
    request: Request,
    payload: BiographyDreamUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    if _count_words(payload.dream_text) > MAX_DREAM_WORDS:
        raise HTTPException(
            status_code=400,
            detail=_msg_word_limit(locale, section="dream", max_words=MAX_DREAM_WORDS),
        )

    dream = db.execute(select(BiographyDream).where(BiographyDream.user_id == current.user_number)).scalar_one_or_none()
    if dream is None:
        dream = BiographyDream(user_id=current.user_number)
        db.add(dream)

    dream.dream_title = payload.dream_title
    dream.dream_text = payload.dream_text

    db.commit()
    db.refresh(dream)

    return _serialize_dream(locale=locale, dream=dream)


@router.get("/professional-achievements", response_model=BiographyProfessionalAchievementsOut)
def get_professional_achievements(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    section = db.execute(
        select(BiographyProfessionalAchievements).where(BiographyProfessionalAchievements.user_id == current.user_number)
    ).scalar_one_or_none()
    return _serialize_professional_achievements(locale=locale, section=section)


@router.put("/professional-achievements", response_model=BiographyProfessionalAchievementsOut)
def upsert_professional_achievements(
    request: Request,
    payload: BiographyProfessionalAchievementsUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    if _count_words(payload.section_text) > MAX_PRO_ACHIEVEMENTS_WORDS:
        raise HTTPException(
            status_code=400,
            detail=_msg_word_limit(
                locale,
                section="professional_achievements",
                max_words=MAX_PRO_ACHIEVEMENTS_WORDS,
            ),
        )

    section = db.execute(
        select(BiographyProfessionalAchievements).where(BiographyProfessionalAchievements.user_id == current.user_number)
    ).scalar_one_or_none()
    if section is None:
        section = BiographyProfessionalAchievements(user_id=current.user_number)
        db.add(section)

    section.section_title = payload.section_title
    section.section_text = payload.section_text

    db.commit()
    db.refresh(section)

    return _serialize_professional_achievements(locale=locale, section=section)


@router.get("/life-achievements", response_model=BiographyLifeAchievementsOut)
def get_life_achievements(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    section = db.execute(
        select(BiographyLifeAchievements).where(BiographyLifeAchievements.user_id == current.user_number)
    ).scalar_one_or_none()
    return _serialize_life_achievements(locale=locale, section=section)


@router.put("/life-achievements", response_model=BiographyLifeAchievementsOut)
def upsert_life_achievements(
    request: Request,
    payload: BiographyLifeAchievementsUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    if _count_words(payload.section_text) > MAX_LIFE_ACHIEVEMENTS_WORDS:
        raise HTTPException(
            status_code=400,
            detail=_msg_word_limit(
                locale,
                section="life_achievements",
                max_words=MAX_LIFE_ACHIEVEMENTS_WORDS,
            ),
        )

    section = db.execute(
        select(BiographyLifeAchievements).where(BiographyLifeAchievements.user_id == current.user_number)
    ).scalar_one_or_none()
    if section is None:
        section = BiographyLifeAchievements(user_id=current.user_number)
        db.add(section)

    section.section_title = payload.section_title
    section.section_text = payload.section_text

    db.commit()
    db.refresh(section)

    return _serialize_life_achievements(locale=locale, section=section)


@router.get("/favorite-quotes", response_model=BiographyFavoriteQuotesOut)
def get_favorite_quotes(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    section = db.execute(
        select(BiographyFavoriteQuotes).where(BiographyFavoriteQuotes.user_id == current.user_number)
    ).scalar_one_or_none()
    return _serialize_favorite_quotes(locale=locale, section=section)


@router.put("/favorite-quotes", response_model=BiographyFavoriteQuotesOut)
def upsert_favorite_quotes(
    request: Request,
    payload: BiographyFavoriteQuotesUpdateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_msg_user_not_found(locale))

    if _count_words(payload.section_text) > MAX_FAVORITE_QUOTES_WORDS:
        raise HTTPException(
            status_code=400,
            detail=_msg_word_limit(
                locale,
                section="favorite_quotes",
                max_words=MAX_FAVORITE_QUOTES_WORDS,
            ),
        )

    section = db.execute(
        select(BiographyFavoriteQuotes).where(BiographyFavoriteQuotes.user_id == current.user_number)
    ).scalar_one_or_none()
    if section is None:
        section = BiographyFavoriteQuotes(user_id=current.user_number)
        db.add(section)

    section.section_title = payload.section_title
    section.section_text = payload.section_text

    db.commit()
    db.refresh(section)

    return _serialize_favorite_quotes(locale=locale, section=section)
