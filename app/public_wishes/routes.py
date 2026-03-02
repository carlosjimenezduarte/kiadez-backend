from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.minor_accreditation import is_minor_protected
from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.config import settings
from app.core.i18n import locale_from_request, tr as i18n_tr
from app.core.storage import S3NotConfiguredError, generate_presigned_get_url
from app.db.database import get_db
from app.db.models.guardian_wish_request import GuardianWishRequest, GuardianWishRequestStatus
from app.db.models.media import Media
from app.db.models.public_cooperative_wish import PublicCooperativeWish
from app.db.models.public_cooperative_wish_fulfillment import PublicCooperativeWishFulfillment
from app.db.models.public_cooperative_wish_participation import PublicCooperativeWishParticipation
from app.db.models.public_personal_wish import PublicPersonalWish, PublicPersonalWishStatus
from app.db.models.public_wish_fulfillment import (
    PublicWishFulfillment,
    PublicWishFulfillmentAttributionMode,
)
from app.db.models.public_wish_freeze_audit import (
    PublicWishFreezeAudit,
    PublicWishFreezeAuditAction,
    PublicWishUnfreezeReasonType,
)
from app.db.models.user import User
from app.public_wishes.schemas import (
    PublicCooperativeWishFulfilledListOut,
    PublicCooperativeWishFulfilledOut,
    PublicCooperativeWishListOut,
    PublicCooperativeWishOut,
    PublicCooperativeWishFulfillRequest,
    PublicCooperativeWishParticipantReviewOut,
    PublicCooperativeWishParticipationCompleteRequest,
    PublicCooperativeWishParticipationUpsertRequest,
    PublicCooperativeWishUpsertRequest,
    PublicPersonalWishDeleteResponse,
    PublicPersonalWishFulfilledListOut,
    PublicPersonalWishFulfillRequest,
    PublicPersonalWishGuardianFulfillRequest,
    PublicPersonalWishListOut,
    PublicPersonalWishOut,
    PublicPersonalWishUnfreezeRequest,
    PublicPersonalWishUpsertRequest,
)

router = APIRouter(prefix="/public-wishes", tags=["public-wishes"])

PERSONAL_ACTIVE_LIMIT = 50
COOPERATIVE_ACTIVE_LIMIT = 20
GUARDIAN_REQUIRED_RANK = 3


def _locale(request: Request | None) -> str:
    return locale_from_request(request, default="en")


def _td(locale: str, en: str, **fmt: object) -> str:
    translations: dict[str, tuple[str, str]] = {
        "Media not found.": ("Medio no encontrado.", "Média introuvable."),
        "Not authorized to use this media.": ("No autorizado para usar este medio.", "Non autorisé à utiliser ce média."),
        "Media not available yet.": ("El medio aún no está disponible.", "Le média n'est pas encore disponible."),
        "User not found.": ("Usuario no encontrado.", "Utilisateur introuvable."),
        "This module is private.": ("Este módulo es privado.", "Ce module est privé."),
        "Restricted access (Guardian rank required).": (
            "Acceso restringido (se requiere rango de Guardián).",
            "Accès restreint (rang de Gardien requis).",
        ),
        "Cooperative wish not found.": ("Deseo cooperativo no encontrado.", "Souhait coopératif introuvable."),
        "This cooperative wish has already been marked as fulfilled.": (
            "Este deseo cooperativo ya fue marcado como cumplido.",
            "Ce souhait coopératif a déjà été marqué comme accompli.",
        ),
        "You cannot register participation in your own cooperative wish.": (
            "No puedes registrar participación en tu propio deseo cooperativo.",
            "Tu ne peux pas enregistrer une participation à ton propre souhait coopératif.",
        ),
        "Invalid security code.": ("Código de seguridad inválido.", "Code de sécurité invalide."),
        "Your participation has already been validated by the creator and cannot be edited.": (
            "Tu participación ya fue validada por el creador y no puede editarse.",
            "Ta participation a déjà été validée par le créateur et ne peut pas être modifiée.",
        ),
        "You cannot cancel participation in your own cooperative wish.": (
            "No puedes cancelar la participación en tu propio deseo cooperativo.",
            "Tu ne peux pas annuler une participation à ton propre souhait coopératif.",
        ),
        "You have no registered participation in this wish.": (
            "No tienes participación registrada en este deseo.",
            "Tu n'as aucune participation enregistrée dans ce souhait.",
        ),
        "Your participation has already been validated by the creator and cannot be canceled.": (
            "Tu participación ya fue validada por el creador y no puede cancelarse.",
            "Ta participation a déjà été validée par le créateur et ne peut pas être annulée.",
        ),
        "You must first register your participation.": (
            "Primero debes registrar tu participación.",
            "Tu dois d'abord enregistrer ta participation.",
        ),
        "Your participation has already been validated by the creator and cannot be modified.": (
            "Tu participación ya fue validada por el creador y no puede modificarse.",
            "Ta participation a déjà été validée par le créateur et ne peut pas être modifiée.",
        ),
        "Participation not found.": ("Participación no encontrada.", "Participation introuvable."),
        "This participation still has no evidence to validate.": (
            "Esta participación aún no tiene evidencia para validar.",
            "Cette participation n'a pas encore de preuve à valider.",
        ),
        "The participation did not accept the required oath for its evidence.": (
            "La participación no aceptó el juramento requerido para su evidencia.",
            "La participation n'a pas accepté le serment requis pour sa preuve.",
        ),
        "There is participation evidence without a valid oath. It must be submitted again.": (
            "Hay evidencia de participación sin un juramento válido. Debe enviarse nuevamente.",
            "Il existe une preuve de participation sans serment valide. Elle doit être soumise à nouveau.",
        ),
        "There is still no participation evidence to close this cooperative wish.": (
            "Aún no hay evidencia de participación para cerrar este deseo cooperativo.",
            "Il n'y a toujours pas de preuve de participation pour clôturer ce souhait coopératif.",
        ),
        "You must validate all participations with evidence before marking this wish as fulfilled.": (
            "Debes validar todas las participaciones con evidencia antes de marcar este deseo como cumplido.",
            "Tu dois valider toutes les participations avec preuve avant de marquer ce souhait comme accompli.",
        ),
        "You cannot delete a cooperative wish that is already fulfilled.": (
            "No puedes eliminar un deseo cooperativo que ya está cumplido.",
            "Tu ne peux pas supprimer un souhait coopératif déjà accompli.",
        ),
        "Personal wish not found.": ("Deseo personal no encontrado.", "Souhait personnel introuvable."),
        "This wish is no longer active.": ("Este deseo ya no está activo.", "Ce souhait n'est plus actif."),
        "This wish is not frozen.": ("Este deseo no está congelado.", "Ce souhait n'est pas gelé."),
        "Only the guardian who froze the wish can mark it as fulfilled.": (
            "Solo el guardián que congeló el deseo puede marcarlo como cumplido.",
            "Seul le gardien qui a gelé le souhait peut le marquer comme accompli.",
        ),
        "You must provide the commitment code.": (
            "Debes proporcionar el código de compromiso.",
            "Tu dois fournir le code d'engagement.",
        ),
        "This commitment code has already been used.": (
            "Este código de compromiso ya fue usado.",
            "Ce code d'engagement a déjà été utilisé.",
        ),
        "Commitment code not found.": ("Código de compromiso no encontrado.", "Code d'engagement introuvable."),
        "The commitment code does not match this wish.": (
            "El código de compromiso no coincide con este deseo.",
            "Le code d'engagement ne correspond pas à ce souhait.",
        ),
        "The commitment code has not been sealed yet.": (
            "El código de compromiso aún no ha sido sellado.",
            "Le code d'engagement n'a pas encore été scellé.",
        ),
        "This request was denied and cannot be closed as fulfilled.": (
            "Esta solicitud fue denegada y no puede cerrarse como cumplida.",
            "Cette demande a été refusée et ne peut pas être clôturée comme accomplie.",
        ),
        "This commitment is assigned to another guardian.": (
            "Este compromiso está asignado a otro guardián.",
            "Cet engagement est attribué à un autre gardien.",
        ),
        "Could not find the user who granted the wish.": (
            "No se pudo encontrar al usuario que concedió el deseo.",
            "Impossible de trouver l'utilisateur qui a accordé le souhait.",
        ),
        "This wish is already frozen.": ("Este deseo ya está congelado.", "Ce souhait est déjà gelé."),
        "Only the guardian who froze the wish can unfreeze it.": (
            "Solo el guardián que congeló el deseo puede descongelarlo.",
            "Seul le gardien qui a gelé le souhait peut le dégeler.",
        ),
        "Your account is in protected mode. You must complete accreditation to enable public actions.": (
            "Tu cuenta está en modo protegido. Debes completar la acreditación para habilitar acciones públicas.",
            "Ton compte est en mode protégé. Tu dois terminer l'accréditation pour activer les actions publiques.",
        ),
        "You already reached the maximum of {limit} active cooperative wishes.": (
            "Ya alcanzaste el máximo de {limit} deseos cooperativos activos.",
            "Tu as déjà atteint le maximum de {limit} souhaits coopératifs actifs.",
        ),
        "This wish already reached the maximum of {limit} participants.": (
            "Este deseo ya alcanzó el máximo de {limit} participantes.",
            "Ce souhait a déjà atteint le maximum de {limit} participants.",
        ),
        "You already reached the maximum of {limit} active personal wishes.": (
            "Ya alcanzaste el máximo de {limit} deseos personales activos.",
            "Tu as déjà atteint le maximum de {limit} souhaits personnels actifs.",
        ),
    }
    english = en.format(**fmt) if fmt else en
    pair = translations.get(en)
    if not pair:
        return english
    es, fr = pair
    return i18n_tr(
        locale,
        es=(es.format(**fmt) if fmt else es),
        en=english,
        fr=(fr.format(**fmt) if fmt else fr),
    )


def _msg_fulfillment_secret(locale: str) -> str:
    return i18n_tr(
        locale,
        es="La persona que cumplió el deseo eligió actuar desde el secreto.",
        en="The person who fulfilled the wish chose to act from secrecy.",
        fr="La personne qui a accompli le souhait a choisi d'agir dans le secret.",
    )


def _msg_fulfillment_public(locale: str, handle: str) -> str:
    return i18n_tr(
        locale,
        es=f"Deseo cumplido gracias a {handle}",
        en=f"Wish fulfilled thanks to {handle}",
        fr=f"Souhait accompli grâce à {handle}",
    )


def _build_media_url(media: Media | None) -> str | None:
    if not media or media.status != "ready":
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


def _build_profile_url(username: str | None, *, user_id: int) -> str:
    normalized = (username or "").strip()
    if normalized:
        return f"/home_user.html?u={normalized}"
    return f"/home_user.html?id={int(user_id)}"


def _build_handle(*, username: str | None, user_id: int) -> str:
    normalized = (username or "").strip()
    if normalized:
        return f"@{normalized}"
    return f"@id{int(user_id)}"


def _load_fulfillment_maps_for_wishes(
    *,
    db: Session,
    wishes: list[PublicPersonalWish],
) -> tuple[dict[int, PublicWishFulfillment], dict[int, User]]:
    wish_ids = sorted({int(wish.id) for wish in wishes if wish.id is not None})
    if not wish_ids:
        return {}, {}

    fulfillments = db.execute(
        select(PublicWishFulfillment).where(PublicWishFulfillment.wish_id.in_(wish_ids))
    ).scalars().all()
    fulfillment_map = {int(row.wish_id): row for row in fulfillments}

    public_fulfiller_ids = sorted({
        int(row.fulfiller_user_id)
        for row in fulfillments
        if row.attribution_mode == PublicWishFulfillmentAttributionMode.public and row.fulfiller_user_id is not None
    })
    if not public_fulfiller_ids:
        return fulfillment_map, {}

    users = db.execute(select(User).where(User.id.in_(public_fulfiller_ids))).scalars().all()
    users_map = {int(user.id): user for user in users}
    return fulfillment_map, users_map


def _wish_out(
    *,
    wish: PublicPersonalWish,
    locale: str,
    media_map: dict[int, Media],
    user_map: dict[int, User] | None = None,
    fulfillment_map: dict[int, PublicWishFulfillment] | None = None,
    public_fulfiller_map: dict[int, User] | None = None,
) -> PublicPersonalWishOut:
    media = media_map.get(wish.media_id) if wish.media_id else None
    evidence_media = media_map.get(wish.fulfilled_evidence_media_id) if wish.fulfilled_evidence_media_id else None
    frozen_by_user = None
    if user_map and wish.frozen_by_guardian_id:
        frozen_by_user = user_map.get(int(wish.frozen_by_guardian_id))

    frozen_full_name = None
    frozen_profile_url = None
    if frozen_by_user is not None:
        frozen_full_name = f"{(frozen_by_user.first_name or '').strip()} {(frozen_by_user.last_name or '').strip()}".strip()
        if not frozen_full_name:
            frozen_full_name = f"User {frozen_by_user.id}"
        username = (frozen_by_user.username or "").strip()
        if username:
            frozen_profile_url = f"/home_user.html?u={username}"
        else:
            frozen_profile_url = f"/home_user.html?id={int(frozen_by_user.id)}"

    fulfillment_row = None
    if fulfillment_map:
        fulfillment_row = fulfillment_map.get(int(wish.id))

    fulfilled_commitment_code = None
    fulfillment_attribution_mode = None
    fulfillment_message = None
    fulfilled_by_user_id = None
    fulfilled_by_handle = None
    fulfilled_by_profile_url = None
    if fulfillment_row is not None:
        fulfilled_commitment_code = (fulfillment_row.commitment_code or "").strip() or None
        mode_value = (
            fulfillment_row.attribution_mode.value
            if isinstance(fulfillment_row.attribution_mode, PublicWishFulfillmentAttributionMode)
            else str(fulfillment_row.attribution_mode or "").strip()
        )
        if mode_value == PublicWishFulfillmentAttributionMode.secret.value:
            fulfillment_attribution_mode = "secret"
            fulfillment_message = _msg_fulfillment_secret(locale)
        elif mode_value == PublicWishFulfillmentAttributionMode.public.value:
            fulfillment_attribution_mode = "public"
            fulfilled_by_user_id = int(fulfillment_row.fulfiller_user_id)
            fulfiller_user = None
            if public_fulfiller_map:
                fulfiller_user = public_fulfiller_map.get(int(fulfillment_row.fulfiller_user_id))
            if fulfiller_user is not None:
                fulfilled_by_handle = _build_handle(
                    username=fulfiller_user.username,
                    user_id=int(fulfiller_user.id),
                )
                fulfilled_by_profile_url = _build_profile_url(
                    fulfiller_user.username,
                    user_id=int(fulfiller_user.id),
                )
            else:
                fulfilled_by_handle = _build_handle(
                    username=None,
                    user_id=int(fulfillment_row.fulfiller_user_id),
                )
                fulfilled_by_profile_url = _build_profile_url(
                    None,
                    user_id=int(fulfillment_row.fulfiller_user_id),
                )
            fulfillment_message = _msg_fulfillment_public(locale, fulfilled_by_handle)

    return PublicPersonalWishOut(
        id=wish.id,
        wish_text=wish.wish_text,
        wish_type=wish.wish_type,
        life_purpose_slot_number=wish.life_purpose_slot_number,
        life_purpose_icon_key=wish.life_purpose_icon_key,
        media_id=wish.media_id,
        media_url=_build_media_url(media),
        fulfilled_evidence_media_id=wish.fulfilled_evidence_media_id,
        fulfilled_evidence_media_url=_build_media_url(evidence_media),
        status=wish.status,
        is_frozen=bool(wish.frozen_by_guardian_id and wish.frozen_at),
        frozen_at=wish.frozen_at,
        frozen_by_guardian_id=wish.frozen_by_guardian_id,
        frozen_by_guardian_full_name=frozen_full_name,
        frozen_by_guardian_profile_url=frozen_profile_url,
        fulfilled_commitment_code=fulfilled_commitment_code,
        fulfillment_attribution_mode=fulfillment_attribution_mode,
        fulfillment_message=fulfillment_message,
        fulfilled_by_user_id=fulfilled_by_user_id,
        fulfilled_by_handle=fulfilled_by_handle,
        fulfilled_by_profile_url=fulfilled_by_profile_url,
        fulfilled_at=wish.fulfilled_at,
        created_at=wish.created_at,
        updated_at=wish.updated_at,
    )


def _resolve_owned_media(*, db: Session, media_id: int | None, user_id: int, locale: str) -> Media | None:
    if media_id is None:
        return None

    media = db.execute(select(Media).where(Media.id == media_id)).scalar_one_or_none()
    if media is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Media not found."))
    if media.owner_id != user_id:
        raise HTTPException(status_code=403, detail=_td(locale, "Not authorized to use this media."))
    if media.status != "ready":
        raise HTTPException(status_code=409, detail=_td(locale, "Media not available yet."))
    return media


def _require_public_actions_allowed(*, db: Session, user_id: int, locale: str) -> User:
    user = db.execute(select(User).where(User.id == user_id, User.is_active.is_(True))).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))
    if is_minor_protected(user):
        raise HTTPException(
            status_code=403,
            detail=_td(
                locale,
                "Your account is in protected mode. You must complete accreditation to enable public actions.",
            ),
        )
    return user


def _load_cooperative_fulfillment_for_wish(
    *,
    db: Session,
    wish_id: int,
) -> PublicCooperativeWishFulfillment | None:
    return db.execute(
        select(PublicCooperativeWishFulfillment).where(PublicCooperativeWishFulfillment.wish_id == wish_id)
    ).scalar_one_or_none()


def _ensure_cooperative_visibility(
    *,
    owner: User,
    viewer_user_id: int,
    locale: str,
) -> None:
    if int(owner.id) == int(viewer_user_id):
        return
    if is_minor_protected(owner):
        raise HTTPException(status_code=403, detail=_td(locale, "This module is private."))
    if not bool(owner.public_profile_show_cooperative_wishes):
        raise HTTPException(status_code=403, detail=_td(locale, "This module is private."))


def _load_cooperative_participations_map(
    *,
    db: Session,
    wish_ids: list[int],
) -> dict[int, list[PublicCooperativeWishParticipation]]:
    if not wish_ids:
        return {}

    rows = db.execute(
        select(PublicCooperativeWishParticipation)
        .where(PublicCooperativeWishParticipation.wish_id.in_(wish_ids))
        .order_by(
            PublicCooperativeWishParticipation.created_at.asc(),
            PublicCooperativeWishParticipation.id.asc(),
        )
    ).scalars().all()
    out: dict[int, list[PublicCooperativeWishParticipation]] = {}
    for row in rows:
        out.setdefault(int(row.wish_id), []).append(row)
    return out


def _build_participants_count_map(
    *,
    participations_map: dict[int, list[PublicCooperativeWishParticipation]],
) -> dict[int, int]:
    return {
        int(wish_id): int(len(items or []))
        for wish_id, items in participations_map.items()
    }


def _load_users_map(
    *,
    db: Session,
    user_ids: set[int],
) -> dict[int, User]:
    if not user_ids:
        return {}
    rows = db.execute(select(User).where(User.id.in_(sorted(user_ids)))).scalars().all()
    return {int(user.id): user for user in rows}


def _build_cooperative_render_context(
    *,
    db: Session,
    wishes: list[PublicCooperativeWish],
    current_user_id: int,
    fulfillment_map: dict[int, PublicCooperativeWishFulfillment] | None = None,
) -> dict[str, object]:
    wish_ids = [int(wish.id) for wish in wishes if wish.id is not None]
    participations_map = _load_cooperative_participations_map(db=db, wish_ids=wish_ids)
    participants_count_map = _build_participants_count_map(participations_map=participations_map)

    viewer_participation_map: dict[int, PublicCooperativeWishParticipation] = {}
    participant_user_ids: set[int] = set()
    for wish_id, rows in participations_map.items():
        for row in rows:
            participant_user_ids.add(int(row.participant_user_id))
            if int(row.participant_user_id) == int(current_user_id):
                viewer_participation_map[int(wish_id)] = row

    participant_user_map = _load_users_map(db=db, user_ids=participant_user_ids)

    media_ids: set[int] = set()
    for wish in wishes:
        if wish.media_id is not None:
            media_ids.add(int(wish.media_id))

    for rows in participations_map.values():
        for row in rows:
            if row.evidence_media_id is not None:
                media_ids.add(int(row.evidence_media_id))

    for user in participant_user_map.values():
        if user.profile_photo_media_id is not None:
            media_ids.add(int(user.profile_photo_media_id))

    for fulfillment in (fulfillment_map or {}).values():
        if fulfillment.final_evidence_media_id is not None:
            media_ids.add(int(fulfillment.final_evidence_media_id))

    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(sorted(media_ids)))).scalars().all()
        media_map = {int(media.id): media for media in medias}

    return {
        "media_map": media_map,
        "participants_count_map": participants_count_map,
        "viewer_participation_map": viewer_participation_map,
        "participations_map": participations_map,
        "participant_user_map": participant_user_map,
    }


def _cooperative_participation_status(
    participation: PublicCooperativeWishParticipation | None,
) -> str | None:
    if participation is None:
        return None
    if participation.owner_validated_at is not None:
        return "validated"
    if participation.evidence_submitted_at is not None and participation.evidence_media_id is not None:
        return "completed"
    return "pending"


def _cooperative_wish_out(
    *,
    wish: PublicCooperativeWish,
    locale: str,
    media_map: dict[int, Media],
    current_user_id: int,
    participants_count_map: dict[int, int] | None = None,
    viewer_participation_map: dict[int, PublicCooperativeWishParticipation] | None = None,
    participations_map: dict[int, list[PublicCooperativeWishParticipation]] | None = None,
    participant_user_map: dict[int, User] | None = None,
    fulfillment_map: dict[int, PublicCooperativeWishFulfillment] | None = None,
) -> PublicCooperativeWishOut:
    wish_id = int(wish.id)
    media = media_map.get(wish.media_id) if wish.media_id else None
    participants_current = int((participants_count_map or {}).get(wish_id, 0))
    is_owner = int(current_user_id) == int(wish.user_id)
    viewer_participation = (
        (viewer_participation_map or {}).get(wish_id)
        if viewer_participation_map is not None
        else None
    )
    fulfillment = (fulfillment_map or {}).get(wish_id)
    is_fulfilled = fulfillment is not None

    owner_review_items: list[PublicCooperativeWishParticipantReviewOut] = []
    owner_pending_validation_count = 0
    if is_owner:
        for row in (participations_map or {}).get(wish_id, []):
            if row.evidence_submitted_at is None or row.evidence_media_id is None:
                continue

            participant = (participant_user_map or {}).get(int(row.participant_user_id))
            participant_username = participant.username if participant is not None else None
            participant_user_id = int(row.participant_user_id)

            profile_photo_media = None
            if participant is not None and participant.profile_photo_media_id is not None:
                profile_photo_media = media_map.get(int(participant.profile_photo_media_id))

            evidence_media = media_map.get(int(row.evidence_media_id))
            item = PublicCooperativeWishParticipantReviewOut(
                participation_id=int(row.id),
                participant_user_id=participant_user_id,
                participant_handle=_build_handle(
                    username=participant_username,
                    user_id=participant_user_id,
                ),
                participant_profile_url=_build_profile_url(
                    participant_username,
                    user_id=participant_user_id,
                ),
                participant_profile_photo_url=_build_media_url(profile_photo_media),
                participation_text=row.participation_text,
                evidence_media_id=int(row.evidence_media_id),
                evidence_media_url=_build_media_url(evidence_media),
                completed_at=row.evidence_submitted_at,
                validated_at=row.owner_validated_at,
                is_validated=row.owner_validated_at is not None,
            )
            owner_review_items.append(item)
            if row.owner_validated_at is None:
                owner_pending_validation_count += 1

    owner_can_mark_fulfilled = bool(owner_review_items) and owner_pending_validation_count == 0 and not is_fulfilled

    return PublicCooperativeWishOut(
        id=wish_id,
        user_id=int(wish.user_id),
        wish_text=wish.wish_text,
        wish_type=wish.wish_type,
        participants_goal=int(wish.participants_goal or 0),
        participants_current=participants_current,
        template_text=wish.template_text,
        security_code=wish.security_code if is_owner else None,
        media_id=wish.media_id,
        media_url=_build_media_url(media),
        viewer_participation_id=int(viewer_participation.id) if viewer_participation is not None else None,
        viewer_participation_text=viewer_participation.participation_text if viewer_participation else None,
        viewer_participation_status=_cooperative_participation_status(viewer_participation),
        viewer_participation_has_evidence=bool(
            viewer_participation
            and viewer_participation.evidence_media_id is not None
            and viewer_participation.evidence_submitted_at is not None
        ),
        viewer_participation_completed_at=(
            viewer_participation.evidence_submitted_at if viewer_participation is not None else None
        ),
        viewer_participation_validated_at=(
            viewer_participation.owner_validated_at if viewer_participation is not None else None
        ),
        owner_review_items=owner_review_items if is_owner else [],
        owner_pending_validation_count=owner_pending_validation_count if is_owner else 0,
        owner_can_mark_fulfilled=owner_can_mark_fulfilled if is_owner else False,
        is_fulfilled=is_fulfilled,
        fulfilled_at=fulfillment.fulfilled_at if fulfillment is not None else None,
        created_at=wish.created_at,
        updated_at=wish.updated_at,
    )


def _cooperative_fulfilled_wish_out(
    *,
    wish: PublicCooperativeWish,
    locale: str,
    fulfillment: PublicCooperativeWishFulfillment,
    media_map: dict[int, Media],
    participants_count_map: dict[int, int] | None = None,
) -> PublicCooperativeWishFulfilledOut:
    wish_id = int(wish.id)
    wish_media = media_map.get(int(wish.media_id)) if wish.media_id is not None else None
    evidence_media = (
        media_map.get(int(fulfillment.final_evidence_media_id))
        if fulfillment.final_evidence_media_id is not None
        else None
    )
    participants_current = int((participants_count_map or {}).get(wish_id, 0))

    return PublicCooperativeWishFulfilledOut(
        id=wish_id,
        user_id=int(wish.user_id),
        wish_text=wish.wish_text,
        wish_type=wish.wish_type,
        participants_goal=int(wish.participants_goal or 0),
        participants_current=participants_current,
        media_id=int(wish.media_id) if wish.media_id is not None else None,
        media_url=_build_media_url(wish_media),
        fulfilled_evidence_media_id=(
            int(fulfillment.final_evidence_media_id)
            if fulfillment.final_evidence_media_id is not None
            else None
        ),
        fulfilled_evidence_media_url=_build_media_url(evidence_media),
        fulfilled_at=fulfillment.fulfilled_at,
        created_at=wish.created_at,
        updated_at=wish.updated_at,
    )


def _resolve_guardian_user(*, db: Session, user_id: int, locale: str) -> User:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))
    if int(user.guardian_rank or 0) < GUARDIAN_REQUIRED_RANK:
        raise HTTPException(status_code=403, detail=_td(locale, "Restricted access (Guardian rank required)."))
    return user


def _load_frozen_guardians_map(*, db: Session, wishes: list[PublicPersonalWish]) -> dict[int, User]:
    frozen_ids = sorted({
        int(wish.frozen_by_guardian_id)
        for wish in wishes
        if wish.frozen_by_guardian_id is not None
    })
    if not frozen_ids:
        return {}
    users = db.execute(select(User).where(User.id.in_(frozen_ids))).scalars().all()
    return {int(user.id): user for user in users}


@router.get("/personal", response_model=PublicPersonalWishListOut)
def list_personal_wishes(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    wishes = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
        .order_by(PublicPersonalWish.created_at.desc(), PublicPersonalWish.id.desc())
    ).scalars().all()

    fulfilled_total = db.execute(
        select(func.count(PublicPersonalWish.id))
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
    ).scalar_one()

    media_ids = {
        media_id
        for wish in wishes
        for media_id in (wish.media_id, wish.fulfilled_evidence_media_id)
        if media_id is not None
    }
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}
    guardian_map = _load_frozen_guardians_map(db=db, wishes=wishes)

    return PublicPersonalWishListOut(
        items=[_wish_out(locale=locale, wish=wish, media_map=media_map, user_map=guardian_map) for wish in wishes],
        active_count=len(wishes),
        active_limit=PERSONAL_ACTIVE_LIMIT,
        fulfilled_total=fulfilled_total or 0,
    )


@router.get("/user/{user_id}/personal", response_model=PublicPersonalWishListOut)
def list_user_personal_wishes(
    request: Request,
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    target = db.execute(
        select(User).where(User.id == user_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    is_owner = int(current.user_number) == int(user_id)
    if not is_owner and is_minor_protected(target):
        raise HTTPException(status_code=403, detail=_td(locale, "This module is private."))
    if not is_owner and not bool(target.public_profile_show_public_wishes):
        raise HTTPException(status_code=403, detail=_td(locale, "This module is private."))

    wishes = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.user_id == user_id)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
        .order_by(PublicPersonalWish.created_at.desc(), PublicPersonalWish.id.desc())
    ).scalars().all()

    fulfilled_total = db.execute(
        select(func.count(PublicPersonalWish.id))
        .where(PublicPersonalWish.user_id == user_id)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
    ).scalar_one()

    media_ids = {
        media_id
        for wish in wishes
        for media_id in (wish.media_id, wish.fulfilled_evidence_media_id)
        if media_id is not None
    }
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}
    guardian_map = _load_frozen_guardians_map(db=db, wishes=wishes)

    return PublicPersonalWishListOut(
        items=[_wish_out(locale=locale, wish=wish, media_map=media_map, user_map=guardian_map) for wish in wishes],
        active_count=len(wishes),
        active_limit=PERSONAL_ACTIVE_LIMIT,
        fulfilled_total=fulfilled_total or 0,
    )


@router.get("/cooperative", response_model=PublicCooperativeWishListOut)
def list_cooperative_wishes(
    request: Request,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    wishes = db.execute(
        select(PublicCooperativeWish)
        .outerjoin(
            PublicCooperativeWishFulfillment,
            PublicCooperativeWishFulfillment.wish_id == PublicCooperativeWish.id,
        )
        .where(PublicCooperativeWish.user_id == current.user_number)
        .where(PublicCooperativeWishFulfillment.id.is_(None))
        .order_by(PublicCooperativeWish.created_at.desc(), PublicCooperativeWish.id.desc())
    ).scalars().all()

    render_context = _build_cooperative_render_context(
        db=db,
        wishes=wishes,
        current_user_id=current.user_number,
        fulfillment_map={},
    )
    media_map = render_context["media_map"]
    participants_count_map = render_context["participants_count_map"]
    viewer_participation_map = render_context["viewer_participation_map"]
    participations_map = render_context["participations_map"]
    participant_user_map = render_context["participant_user_map"]

    return PublicCooperativeWishListOut(
        items=[
            _cooperative_wish_out(locale=locale, 
                wish=wish,
                media_map=media_map,
                current_user_id=current.user_number,
                participants_count_map=participants_count_map,
                viewer_participation_map=viewer_participation_map,
                participations_map=participations_map,
                participant_user_map=participant_user_map,
                fulfillment_map={},
            )
            for wish in wishes
        ],
        active_count=len(wishes),
        active_limit=COOPERATIVE_ACTIVE_LIMIT,
    )


@router.get("/user/{user_id}/cooperative", response_model=PublicCooperativeWishListOut)
def list_user_cooperative_wishes(
    request: Request,
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    target = db.execute(
        select(User).where(User.id == user_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    _ensure_cooperative_visibility(owner=target, viewer_user_id=current.user_number, locale=locale)

    wishes = db.execute(
        select(PublicCooperativeWish)
        .outerjoin(
            PublicCooperativeWishFulfillment,
            PublicCooperativeWishFulfillment.wish_id == PublicCooperativeWish.id,
        )
        .where(PublicCooperativeWish.user_id == user_id)
        .where(PublicCooperativeWishFulfillment.id.is_(None))
        .order_by(PublicCooperativeWish.created_at.desc(), PublicCooperativeWish.id.desc())
    ).scalars().all()

    render_context = _build_cooperative_render_context(
        db=db,
        wishes=wishes,
        current_user_id=current.user_number,
        fulfillment_map={},
    )
    media_map = render_context["media_map"]
    participants_count_map = render_context["participants_count_map"]
    viewer_participation_map = render_context["viewer_participation_map"]
    participations_map = render_context["participations_map"]
    participant_user_map = render_context["participant_user_map"]

    return PublicCooperativeWishListOut(
        items=[
            _cooperative_wish_out(locale=locale, 
                wish=wish,
                media_map=media_map,
                current_user_id=current.user_number,
                participants_count_map=participants_count_map,
                viewer_participation_map=viewer_participation_map,
                participations_map=participations_map,
                participant_user_map=participant_user_map,
                fulfillment_map={},
            )
            for wish in wishes
        ],
        active_count=len(wishes),
        active_limit=COOPERATIVE_ACTIVE_LIMIT,
    )


@router.post("/cooperative", response_model=PublicCooperativeWishOut)
def create_cooperative_wish(
    request: Request,
    payload: PublicCooperativeWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    active_count = db.execute(
        select(func.count(PublicCooperativeWish.id))
        .select_from(PublicCooperativeWish)
        .outerjoin(
            PublicCooperativeWishFulfillment,
            PublicCooperativeWishFulfillment.wish_id == PublicCooperativeWish.id,
        )
        .where(PublicCooperativeWish.user_id == current.user_number)
        .where(PublicCooperativeWishFulfillment.id.is_(None))
    ).scalar_one()
    if int(active_count or 0) >= COOPERATIVE_ACTIVE_LIMIT:
        raise HTTPException(
            status_code=409,
            detail=_td(locale, "You already reached the maximum of {limit} active cooperative wishes.", limit=COOPERATIVE_ACTIVE_LIMIT),
        )

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number, locale=locale)
    wish = PublicCooperativeWish(
        user_id=current.user_number,
        wish_text=payload.wish_text,
        wish_type=payload.wish_type,
        participants_goal=payload.participants_goal,
        template_text=payload.template_text,
        security_code=payload.security_code,
        media_id=media.id if media else None,
    )
    db.add(wish)
    db.commit()
    db.refresh(wish)

    render_context = _build_cooperative_render_context(
        db=db,
        wishes=[wish],
        current_user_id=current.user_number,
        fulfillment_map={},
    )
    media_map = render_context["media_map"]
    participants_count_map = render_context["participants_count_map"]
    viewer_participation_map = render_context["viewer_participation_map"]
    participations_map = render_context["participations_map"]
    participant_user_map = render_context["participant_user_map"]

    return _cooperative_wish_out(locale=locale, 
        wish=wish,
        media_map=media_map,
        current_user_id=current.user_number,
        participants_count_map=participants_count_map,
        viewer_participation_map=viewer_participation_map,
        participations_map=participations_map,
        participant_user_map=participant_user_map,
        fulfillment_map={},
    )


@router.put("/cooperative/{wish_id}", response_model=PublicCooperativeWishOut)
def update_cooperative_wish(
    request: Request,
    wish_id: int,
    payload: PublicCooperativeWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(
        select(PublicCooperativeWish)
        .where(PublicCooperativeWish.id == wish_id)
        .where(PublicCooperativeWish.user_id == current.user_number)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Cooperative wish not found."))
    if _load_cooperative_fulfillment_for_wish(db=db, wish_id=int(wish.id)) is not None:
        raise HTTPException(status_code=409, detail=_td(locale, "This cooperative wish has already been marked as fulfilled."))

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number, locale=locale)
    wish.wish_text = payload.wish_text
    wish.wish_type = payload.wish_type
    wish.participants_goal = payload.participants_goal
    wish.template_text = payload.template_text
    wish.security_code = payload.security_code
    wish.media_id = media.id if media else None

    db.commit()
    db.refresh(wish)

    render_context = _build_cooperative_render_context(
        db=db,
        wishes=[wish],
        current_user_id=current.user_number,
        fulfillment_map={},
    )
    media_map = render_context["media_map"]
    participants_count_map = render_context["participants_count_map"]
    viewer_participation_map = render_context["viewer_participation_map"]
    participations_map = render_context["participations_map"]
    participant_user_map = render_context["participant_user_map"]

    return _cooperative_wish_out(locale=locale, 
        wish=wish,
        media_map=media_map,
        current_user_id=current.user_number,
        participants_count_map=participants_count_map,
        viewer_participation_map=viewer_participation_map,
        participations_map=participations_map,
        participant_user_map=participant_user_map,
        fulfillment_map={},
    )


@router.post("/cooperative/{wish_id}/participate", response_model=PublicCooperativeWishOut)
def participate_in_cooperative_wish(
    request: Request,
    wish_id: int,
    payload: PublicCooperativeWishParticipationUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(select(PublicCooperativeWish).where(PublicCooperativeWish.id == wish_id)).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Cooperative wish not found."))
    if _load_cooperative_fulfillment_for_wish(db=db, wish_id=int(wish.id)) is not None:
        raise HTTPException(status_code=409, detail=_td(locale, "This cooperative wish has already been marked as fulfilled."))

    owner = db.execute(
        select(User).where(User.id == int(wish.user_id), User.is_active.is_(True))
    ).scalar_one_or_none()
    if owner is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    if int(current.user_number) == int(wish.user_id):
        raise HTTPException(status_code=409, detail=_td(locale, "You cannot register participation in your own cooperative wish."))

    _ensure_cooperative_visibility(owner=owner, viewer_user_id=current.user_number, locale=locale)

    participation = db.execute(
        select(PublicCooperativeWishParticipation)
        .where(PublicCooperativeWishParticipation.wish_id == int(wish.id))
        .where(PublicCooperativeWishParticipation.participant_user_id == int(current.user_number))
    ).scalar_one_or_none()
    if participation is None:
        expected_code = (wish.security_code or "").strip()
        provided_code = (payload.security_code or "").strip()
        if not expected_code or expected_code != provided_code:
            raise HTTPException(status_code=403, detail=_td(locale, "Invalid security code."))

        participants_current = db.execute(
            select(func.count(PublicCooperativeWishParticipation.id))
            .where(PublicCooperativeWishParticipation.wish_id == int(wish.id))
        ).scalar_one()
        if int(participants_current or 0) >= int(wish.participants_goal or 0):
            raise HTTPException(
                status_code=409,
                detail=_td(
                    locale,
                    "This wish already reached the maximum of {limit} participants.",
                    limit=int(wish.participants_goal or 0),
                ),
            )

        participation = PublicCooperativeWishParticipation(
            wish_id=int(wish.id),
            participant_user_id=int(current.user_number),
            participation_text=payload.participation_text,
        )
        db.add(participation)
    else:
        if participation.owner_validated_at is not None:
            raise HTTPException(
                status_code=409,
                detail=_td(
                    locale,
                    "Your participation has already been validated by the creator and cannot be edited.",
                ),
            )
        participation.participation_text = payload.participation_text

    db.commit()
    db.refresh(wish)

    render_context = _build_cooperative_render_context(
        db=db,
        wishes=[wish],
        current_user_id=current.user_number,
        fulfillment_map={},
    )
    media_map = render_context["media_map"]
    participants_count_map = render_context["participants_count_map"]
    viewer_participation_map = render_context["viewer_participation_map"]
    participations_map = render_context["participations_map"]
    participant_user_map = render_context["participant_user_map"]

    return _cooperative_wish_out(locale=locale, 
        wish=wish,
        media_map=media_map,
        current_user_id=current.user_number,
        participants_count_map=participants_count_map,
        viewer_participation_map=viewer_participation_map,
        participations_map=participations_map,
        participant_user_map=participant_user_map,
        fulfillment_map={},
    )


@router.delete("/cooperative/{wish_id}/participation/mine", response_model=PublicCooperativeWishOut)
def cancel_my_cooperative_participation(
    request: Request,
    wish_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(select(PublicCooperativeWish).where(PublicCooperativeWish.id == wish_id)).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Cooperative wish not found."))
    if _load_cooperative_fulfillment_for_wish(db=db, wish_id=int(wish.id)) is not None:
        raise HTTPException(status_code=409, detail=_td(locale, "This cooperative wish has already been marked as fulfilled."))

    if int(current.user_number) == int(wish.user_id):
        raise HTTPException(status_code=409, detail=_td(locale, "You cannot cancel participation in your own cooperative wish."))

    owner = db.execute(
        select(User).where(User.id == int(wish.user_id), User.is_active.is_(True))
    ).scalar_one_or_none()
    if owner is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))
    _ensure_cooperative_visibility(owner=owner, viewer_user_id=current.user_number, locale=locale)

    participation = db.execute(
        select(PublicCooperativeWishParticipation)
        .where(PublicCooperativeWishParticipation.wish_id == int(wish.id))
        .where(PublicCooperativeWishParticipation.participant_user_id == int(current.user_number))
    ).scalar_one_or_none()
    if participation is None:
        raise HTTPException(status_code=404, detail=_td(locale, "You have no registered participation in this wish."))
    if participation.owner_validated_at is not None:
        raise HTTPException(
            status_code=409,
            detail=_td(
                locale,
                "Your participation has already been validated by the creator and cannot be canceled.",
            ),
        )

    db.delete(participation)
    db.commit()
    db.refresh(wish)

    render_context = _build_cooperative_render_context(
        db=db,
        wishes=[wish],
        current_user_id=current.user_number,
        fulfillment_map={},
    )
    media_map = render_context["media_map"]
    participants_count_map = render_context["participants_count_map"]
    viewer_participation_map = render_context["viewer_participation_map"]
    participations_map = render_context["participations_map"]
    participant_user_map = render_context["participant_user_map"]

    return _cooperative_wish_out(locale=locale, 
        wish=wish,
        media_map=media_map,
        current_user_id=current.user_number,
        participants_count_map=participants_count_map,
        viewer_participation_map=viewer_participation_map,
        participations_map=participations_map,
        participant_user_map=participant_user_map,
        fulfillment_map={},
    )


@router.post("/cooperative/{wish_id}/participation/complete", response_model=PublicCooperativeWishOut)
def complete_my_cooperative_participation(
    request: Request,
    wish_id: int,
    payload: PublicCooperativeWishParticipationCompleteRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(select(PublicCooperativeWish).where(PublicCooperativeWish.id == wish_id)).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Cooperative wish not found."))
    if _load_cooperative_fulfillment_for_wish(db=db, wish_id=int(wish.id)) is not None:
        raise HTTPException(status_code=409, detail=_td(locale, "This cooperative wish has already been marked as fulfilled."))

    if int(current.user_number) == int(wish.user_id):
        raise HTTPException(status_code=409, detail=_td(locale, "You cannot register participation in your own cooperative wish."))

    owner = db.execute(
        select(User).where(User.id == int(wish.user_id), User.is_active.is_(True))
    ).scalar_one_or_none()
    if owner is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))
    _ensure_cooperative_visibility(owner=owner, viewer_user_id=current.user_number, locale=locale)

    participation = db.execute(
        select(PublicCooperativeWishParticipation)
        .where(PublicCooperativeWishParticipation.wish_id == int(wish.id))
        .where(PublicCooperativeWishParticipation.participant_user_id == int(current.user_number))
    ).scalar_one_or_none()
    if participation is None:
        raise HTTPException(status_code=404, detail=_td(locale, "You must first register your participation."))
    if participation.owner_validated_at is not None:
        raise HTTPException(
            status_code=409,
            detail=_td(
                locale,
                "Your participation has already been validated by the creator and cannot be modified.",
            ),
        )

    evidence_media = _resolve_owned_media(
        db=db,
        media_id=int(payload.evidence_media_id),
        user_id=int(current.user_number),
        locale=locale,
    )
    participation.evidence_media_id = int(evidence_media.id)
    participation.evidence_submitted_at = datetime.now(timezone.utc)
    participation.oath_accepted = bool(payload.oath_accepted)

    db.commit()
    db.refresh(wish)

    render_context = _build_cooperative_render_context(
        db=db,
        wishes=[wish],
        current_user_id=current.user_number,
        fulfillment_map={},
    )
    media_map = render_context["media_map"]
    participants_count_map = render_context["participants_count_map"]
    viewer_participation_map = render_context["viewer_participation_map"]
    participations_map = render_context["participations_map"]
    participant_user_map = render_context["participant_user_map"]

    return _cooperative_wish_out(locale=locale, 
        wish=wish,
        media_map=media_map,
        current_user_id=current.user_number,
        participants_count_map=participants_count_map,
        viewer_participation_map=viewer_participation_map,
        participations_map=participations_map,
        participant_user_map=participant_user_map,
        fulfillment_map={},
    )


@router.post("/cooperative/{wish_id}/participation/{participation_id}/validate", response_model=PublicCooperativeWishOut)
def validate_cooperative_participation(
    request: Request,
    wish_id: int,
    participation_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(
        select(PublicCooperativeWish)
        .where(PublicCooperativeWish.id == wish_id)
        .where(PublicCooperativeWish.user_id == current.user_number)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Cooperative wish not found."))
    if _load_cooperative_fulfillment_for_wish(db=db, wish_id=int(wish.id)) is not None:
        raise HTTPException(status_code=409, detail=_td(locale, "This cooperative wish has already been marked as fulfilled."))

    participation = db.execute(
        select(PublicCooperativeWishParticipation)
        .where(PublicCooperativeWishParticipation.id == participation_id)
        .where(PublicCooperativeWishParticipation.wish_id == int(wish.id))
    ).scalar_one_or_none()
    if participation is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Participation not found."))
    if participation.evidence_submitted_at is None or participation.evidence_media_id is None:
        raise HTTPException(status_code=409, detail=_td(locale, "This participation still has no evidence to validate."))
    if participation.oath_accepted is not True:
        raise HTTPException(
            status_code=409,
            detail=_td(locale, "The participation did not accept the required oath for its evidence."),
        )

    if participation.owner_validated_at is None:
        participation.owner_validated_at = datetime.now(timezone.utc)
        participation.owner_validated_by_user_id = int(current.user_number)
        db.commit()
        db.refresh(wish)
    else:
        db.refresh(wish)

    render_context = _build_cooperative_render_context(
        db=db,
        wishes=[wish],
        current_user_id=current.user_number,
        fulfillment_map={},
    )
    media_map = render_context["media_map"]
    participants_count_map = render_context["participants_count_map"]
    viewer_participation_map = render_context["viewer_participation_map"]
    participations_map = render_context["participations_map"]
    participant_user_map = render_context["participant_user_map"]

    return _cooperative_wish_out(locale=locale, 
        wish=wish,
        media_map=media_map,
        current_user_id=current.user_number,
        participants_count_map=participants_count_map,
        viewer_participation_map=viewer_participation_map,
        participations_map=participations_map,
        participant_user_map=participant_user_map,
        fulfillment_map={},
    )


@router.post("/cooperative/{wish_id}/fulfill", response_model=PublicCooperativeWishOut)
def fulfill_cooperative_wish(
    request: Request,
    wish_id: int,
    payload: PublicCooperativeWishFulfillRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(
        select(PublicCooperativeWish)
        .where(PublicCooperativeWish.id == wish_id)
        .where(PublicCooperativeWish.user_id == current.user_number)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Cooperative wish not found."))
    existing_fulfillment = _load_cooperative_fulfillment_for_wish(db=db, wish_id=int(wish.id))
    if existing_fulfillment is not None:
        raise HTTPException(status_code=409, detail=_td(locale, "This cooperative wish has already been marked as fulfilled."))

    invalid_oath_count = db.execute(
        select(func.count(PublicCooperativeWishParticipation.id))
        .where(PublicCooperativeWishParticipation.wish_id == int(wish.id))
        .where(PublicCooperativeWishParticipation.evidence_submitted_at.is_not(None))
        .where(PublicCooperativeWishParticipation.evidence_media_id.is_not(None))
        .where(PublicCooperativeWishParticipation.oath_accepted.is_(False))
    ).scalar_one()
    if int(invalid_oath_count or 0) > 0:
        raise HTTPException(
            status_code=409,
            detail=_td(locale, "There is participation evidence without a valid oath. It must be submitted again."),
        )

    participation_rows = db.execute(
        select(PublicCooperativeWishParticipation)
        .where(PublicCooperativeWishParticipation.wish_id == int(wish.id))
        .where(PublicCooperativeWishParticipation.evidence_submitted_at.is_not(None))
        .where(PublicCooperativeWishParticipation.evidence_media_id.is_not(None))
        .where(PublicCooperativeWishParticipation.oath_accepted.is_(True))
    ).scalars().all()
    if not participation_rows:
        raise HTTPException(
            status_code=409,
            detail=_td(locale, "There is still no participation evidence to close this cooperative wish."),
        )

    pending_validation_exists = any(row.owner_validated_at is None for row in participation_rows)
    if pending_validation_exists:
        raise HTTPException(
            status_code=409,
            detail=_td(locale, "You must validate all participations with evidence before marking this wish as fulfilled."),
        )

    evidence_media = _resolve_owned_media(
        db=db,
        media_id=int(payload.evidence_media_id),
        user_id=int(current.user_number),
        locale=locale,
    )

    fulfillment = PublicCooperativeWishFulfillment(
        wish_id=int(wish.id),
        wish_owner_user_id=int(current.user_number),
        final_evidence_media_id=int(evidence_media.id),
        oath_accepted=bool(payload.oath_accepted),
        fulfilled_at=datetime.now(timezone.utc),
    )
    db.add(fulfillment)
    db.commit()
    db.refresh(wish)
    db.refresh(fulfillment)

    fulfillment_map = {int(wish.id): fulfillment}
    render_context = _build_cooperative_render_context(
        db=db,
        wishes=[wish],
        current_user_id=current.user_number,
        fulfillment_map=fulfillment_map,
    )
    media_map = render_context["media_map"]
    participants_count_map = render_context["participants_count_map"]
    viewer_participation_map = render_context["viewer_participation_map"]
    participations_map = render_context["participations_map"]
    participant_user_map = render_context["participant_user_map"]

    return _cooperative_wish_out(locale=locale, 
        wish=wish,
        media_map=media_map,
        current_user_id=current.user_number,
        participants_count_map=participants_count_map,
        viewer_participation_map=viewer_participation_map,
        participations_map=participations_map,
        participant_user_map=participant_user_map,
        fulfillment_map=fulfillment_map,
    )


@router.delete("/cooperative/{wish_id}", response_model=PublicPersonalWishDeleteResponse)
def delete_cooperative_wish(
    request: Request,
    wish_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(
        select(PublicCooperativeWish)
        .where(PublicCooperativeWish.id == wish_id)
        .where(PublicCooperativeWish.user_id == current.user_number)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Cooperative wish not found."))
    if _load_cooperative_fulfillment_for_wish(db=db, wish_id=int(wish.id)) is not None:
        raise HTTPException(status_code=409, detail=_td(locale, "You cannot delete a cooperative wish that is already fulfilled."))

    db.delete(wish)
    db.commit()
    return PublicPersonalWishDeleteResponse(deleted=True)


@router.get("/cooperative/fulfilled/list", response_model=PublicCooperativeWishFulfilledListOut)
def list_fulfilled_cooperative_wishes(
    request: Request,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    total = db.execute(
        select(func.count(PublicCooperativeWishFulfillment.id))
        .select_from(PublicCooperativeWishFulfillment)
        .join(
            PublicCooperativeWish,
            PublicCooperativeWish.id == PublicCooperativeWishFulfillment.wish_id,
        )
        .where(PublicCooperativeWish.user_id == current.user_number)
    ).scalar_one()

    rows = db.execute(
        select(PublicCooperativeWish, PublicCooperativeWishFulfillment)
        .join(
            PublicCooperativeWishFulfillment,
            PublicCooperativeWishFulfillment.wish_id == PublicCooperativeWish.id,
        )
        .where(PublicCooperativeWish.user_id == current.user_number)
        .order_by(
            PublicCooperativeWishFulfillment.fulfilled_at.desc().nullslast(),
            PublicCooperativeWishFulfillment.id.desc(),
        )
        .offset(offset)
        .limit(limit)
    ).all()

    wishes = [row[0] for row in rows]
    fulfillments_map = {int(row[0].id): row[1] for row in rows}
    wish_ids = [int(wish.id) for wish in wishes if wish.id is not None]

    participations_map = _load_cooperative_participations_map(db=db, wish_ids=wish_ids)
    participants_count_map = _build_participants_count_map(participations_map=participations_map)

    media_ids: set[int] = set()
    for wish in wishes:
        if wish.media_id is not None:
            media_ids.add(int(wish.media_id))

    for fulfillment in fulfillments_map.values():
        if fulfillment.final_evidence_media_id is not None:
            media_ids.add(int(fulfillment.final_evidence_media_id))

    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(sorted(media_ids)))).scalars().all()
        media_map = {int(media.id): media for media in medias}

    return PublicCooperativeWishFulfilledListOut(
        items=[
            _cooperative_fulfilled_wish_out(locale=locale, 
                wish=wish,
                fulfillment=fulfillments_map[int(wish.id)],
                media_map=media_map,
                participants_count_map=participants_count_map,
            )
            for wish in wishes
        ],
        total=int(total or 0),
        limit=limit,
        offset=offset,
    )


@router.get("/user/{user_id}/cooperative/fulfilled", response_model=PublicCooperativeWishFulfilledListOut)
def list_user_fulfilled_cooperative_wishes(
    request: Request,
    user_id: int,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    target = db.execute(
        select(User).where(User.id == user_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    is_owner = int(current.user_number) == int(user_id)
    if not is_owner and is_minor_protected(target):
        raise HTTPException(status_code=403, detail=_td(locale, "This module is private."))
    if not is_owner and not bool(target.public_profile_show_fulfilled_wishes):
        raise HTTPException(status_code=403, detail=_td(locale, "This module is private."))
    if not is_owner and not bool(target.public_profile_show_cooperative_wishes):
        raise HTTPException(status_code=403, detail=_td(locale, "This module is private."))

    total = db.execute(
        select(func.count(PublicCooperativeWishFulfillment.id))
        .select_from(PublicCooperativeWishFulfillment)
        .join(
            PublicCooperativeWish,
            PublicCooperativeWish.id == PublicCooperativeWishFulfillment.wish_id,
        )
        .where(PublicCooperativeWish.user_id == user_id)
    ).scalar_one()

    rows = db.execute(
        select(PublicCooperativeWish, PublicCooperativeWishFulfillment)
        .join(
            PublicCooperativeWishFulfillment,
            PublicCooperativeWishFulfillment.wish_id == PublicCooperativeWish.id,
        )
        .where(PublicCooperativeWish.user_id == user_id)
        .order_by(
            PublicCooperativeWishFulfillment.fulfilled_at.desc().nullslast(),
            PublicCooperativeWishFulfillment.id.desc(),
        )
        .offset(offset)
        .limit(limit)
    ).all()

    wishes = [row[0] for row in rows]
    fulfillments_map = {int(row[0].id): row[1] for row in rows}
    wish_ids = [int(wish.id) for wish in wishes if wish.id is not None]

    participations_map = _load_cooperative_participations_map(db=db, wish_ids=wish_ids)
    participants_count_map = _build_participants_count_map(participations_map=participations_map)

    media_ids: set[int] = set()
    for wish in wishes:
        if wish.media_id is not None:
            media_ids.add(int(wish.media_id))

    for fulfillment in fulfillments_map.values():
        if fulfillment.final_evidence_media_id is not None:
            media_ids.add(int(fulfillment.final_evidence_media_id))

    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(sorted(media_ids)))).scalars().all()
        media_map = {int(media.id): media for media in medias}

    return PublicCooperativeWishFulfilledListOut(
        items=[
            _cooperative_fulfilled_wish_out(locale=locale, 
                wish=wish,
                fulfillment=fulfillments_map[int(wish.id)],
                media_map=media_map,
                participants_count_map=participants_count_map,
            )
            for wish in wishes
        ],
        total=int(total or 0),
        limit=limit,
        offset=offset,
    )


@router.get("/personal/fulfilled", response_model=PublicPersonalWishFulfilledListOut)
def list_fulfilled_personal_wishes(
    request: Request,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    total = db.execute(
        select(func.count(PublicPersonalWish.id))
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
    ).scalar_one()

    wishes = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
        .order_by(PublicPersonalWish.fulfilled_at.desc().nullslast(), PublicPersonalWish.id.desc())
        .offset(offset)
        .limit(limit)
    ).scalars().all()

    media_ids = {
        media_id
        for wish in wishes
        for media_id in (wish.media_id, wish.fulfilled_evidence_media_id)
        if media_id is not None
    }
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}
    guardian_map = _load_frozen_guardians_map(db=db, wishes=wishes)
    fulfillment_map, fulfiller_map = _load_fulfillment_maps_for_wishes(db=db, wishes=wishes)

    return PublicPersonalWishFulfilledListOut(
        items=[
            _wish_out(locale=locale, 
                wish=wish,
                media_map=media_map,
                user_map=guardian_map,
                fulfillment_map=fulfillment_map,
                public_fulfiller_map=fulfiller_map,
            )
            for wish in wishes
        ],
        total=total or 0,
        limit=limit,
        offset=offset,
    )


@router.get("/user/{user_id}/personal/fulfilled", response_model=PublicPersonalWishFulfilledListOut)
def list_user_fulfilled_personal_wishes(
    request: Request,
    user_id: int,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    target = db.execute(
        select(User).where(User.id == user_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    is_owner = int(current.user_number) == int(user_id)
    if not is_owner and is_minor_protected(target):
        raise HTTPException(status_code=403, detail=_td(locale, "This module is private."))
    if not is_owner and not bool(target.public_profile_show_fulfilled_wishes):
        raise HTTPException(status_code=403, detail=_td(locale, "This module is private."))

    total = db.execute(
        select(func.count(PublicPersonalWish.id))
        .where(PublicPersonalWish.user_id == user_id)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
    ).scalar_one()

    wishes = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.user_id == user_id)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.fulfilled)
        .order_by(PublicPersonalWish.fulfilled_at.desc().nullslast(), PublicPersonalWish.id.desc())
        .offset(offset)
        .limit(limit)
    ).scalars().all()

    media_ids = {
        media_id
        for wish in wishes
        for media_id in (wish.media_id, wish.fulfilled_evidence_media_id)
        if media_id is not None
    }
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}
    guardian_map = _load_frozen_guardians_map(db=db, wishes=wishes)
    fulfillment_map, fulfiller_map = _load_fulfillment_maps_for_wishes(db=db, wishes=wishes)

    return PublicPersonalWishFulfilledListOut(
        items=[
            _wish_out(locale=locale, 
                wish=wish,
                media_map=media_map,
                user_map=guardian_map,
                fulfillment_map=fulfillment_map,
                public_fulfiller_map=fulfiller_map,
            )
            for wish in wishes
        ],
        total=total or 0,
        limit=limit,
        offset=offset,
    )


@router.post("/personal", response_model=PublicPersonalWishOut)
def create_personal_wish(
    request: Request,
    payload: PublicPersonalWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    active_count = db.execute(
        select(func.count(PublicPersonalWish.id))
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one()
    if active_count >= PERSONAL_ACTIVE_LIMIT:
        raise HTTPException(
            status_code=409,
            detail=_td(locale, "You already reached the maximum of {limit} active personal wishes.", limit=PERSONAL_ACTIVE_LIMIT),
        )

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number, locale=locale)

    wish = PublicPersonalWish(
        user_id=current.user_number,
        wish_text=payload.wish_text,
        wish_type=payload.wish_type,
        media_id=media.id if media else None,
        status=PublicPersonalWishStatus.active,
        fulfilled_at=None,
        fulfilled_evidence_media_id=None,
    )
    db.add(wish)
    db.commit()
    db.refresh(wish)

    media_map = {media.id: media} if media else {}
    return _wish_out(locale=locale, wish=wish, media_map=media_map, user_map={})


@router.put("/personal/{wish_id}", response_model=PublicPersonalWishOut)
def update_personal_wish(
    request: Request,
    wish_id: int,
    payload: PublicPersonalWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Personal wish not found."))

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number, locale=locale)

    wish.wish_text = payload.wish_text
    wish.wish_type = payload.wish_type
    wish.media_id = media.id if media else None

    db.commit()
    db.refresh(wish)

    media_map = {media.id: media} if media else {}
    return _wish_out(locale=locale, wish=wish, media_map=media_map, user_map={})


@router.post("/personal/{wish_id}/fulfill", response_model=PublicPersonalWishOut)
def fulfill_personal_wish(
    request: Request,
    wish_id: int,
    payload: PublicPersonalWishFulfillRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Personal wish not found."))

    evidence_media = _resolve_owned_media(
        db=db,
        media_id=payload.evidence_media_id,
        user_id=current.user_number,
        locale=locale,
    )

    wish.status = PublicPersonalWishStatus.fulfilled
    wish.fulfilled_at = datetime.now(timezone.utc)
    wish.fulfilled_evidence_media_id = evidence_media.id if evidence_media else None

    db.commit()
    db.refresh(wish)

    media_ids = {media_id for media_id in (wish.media_id, wish.fulfilled_evidence_media_id) if media_id is not None}
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}

    guardian_map = _load_frozen_guardians_map(db=db, wishes=[wish])
    return _wish_out(locale=locale, wish=wish, media_map=media_map, user_map=guardian_map)


@router.post("/personal/{wish_id}/guardian-fulfill", response_model=PublicPersonalWishOut)
def guardian_fulfill_personal_wish(
    request: Request,
    wish_id: int,
    payload: PublicPersonalWishGuardianFulfillRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    guardian_user = _resolve_guardian_user(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(
        select(PublicPersonalWish).where(PublicPersonalWish.id == wish_id)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Personal wish not found."))
    if wish.status != PublicPersonalWishStatus.active:
        raise HTTPException(status_code=409, detail=_td(locale, "This wish is no longer active."))

    if not (wish.frozen_by_guardian_id and wish.frozen_at):
        raise HTTPException(status_code=409, detail=_td(locale, "This wish is not frozen."))
    if int(wish.frozen_by_guardian_id) != int(guardian_user.id):
        raise HTTPException(status_code=403, detail=_td(locale, "Only the guardian who froze the wish can mark it as fulfilled."))

    commitment_code = (payload.commitment_code or "").strip().upper()
    if not commitment_code:
        raise HTTPException(status_code=400, detail=_td(locale, "You must provide the commitment code."))

    existing_by_wish = db.execute(
        select(PublicWishFulfillment).where(PublicWishFulfillment.wish_id == int(wish.id))
    ).scalar_one_or_none()
    existing_by_code = db.execute(
        select(PublicWishFulfillment).where(PublicWishFulfillment.commitment_code == commitment_code)
    ).scalar_one_or_none()
    if existing_by_wish is not None or existing_by_code is not None:
        raise HTTPException(status_code=409, detail=_td(locale, "This commitment code has already been used."))

    wish_request = db.execute(
        select(GuardianWishRequest).where(GuardianWishRequest.commitment_code == commitment_code)
    ).scalar_one_or_none()
    if wish_request is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Commitment code not found."))
    if int(wish_request.public_wish_id) != int(wish.id):
        raise HTTPException(status_code=409, detail=_td(locale, "The commitment code does not match this wish."))
    if wish_request.commitment_sealed_at is None:
        raise HTTPException(status_code=409, detail=_td(locale, "The commitment code has not been sealed yet."))
    if wish_request.denied_at is not None:
        raise HTTPException(status_code=409, detail=_td(locale, "This request was denied and cannot be closed as fulfilled."))
    if wish_request.guardian_id is not None and int(wish_request.guardian_id) != int(guardian_user.id):
        raise HTTPException(status_code=409, detail=_td(locale, "This commitment is assigned to another guardian."))

    fulfiller_user = db.execute(
        select(User).where(User.id == wish_request.requester_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if fulfiller_user is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Could not find the user who granted the wish."))

    evidence_media = _resolve_owned_media(
        db=db,
        media_id=payload.evidence_media_id,
        user_id=current.user_number,
        locale=locale,
    )

    wish.status = PublicPersonalWishStatus.fulfilled
    wish.fulfilled_at = datetime.now(timezone.utc)
    wish.fulfilled_evidence_media_id = evidence_media.id if evidence_media else None
    wish.frozen_by_guardian_id = None
    wish.frozen_at = None

    wish_request.guardian_id = int(guardian_user.id)
    wish_request.status = GuardianWishRequestStatus.closed

    db.add(
        PublicWishFulfillment(
            wish_id=int(wish.id),
            wish_owner_id=int(wish.user_id),
            fulfiller_user_id=int(fulfiller_user.id),
            guardian_user_id=int(guardian_user.id),
            wish_request_id=int(wish_request.id),
            commitment_code=commitment_code,
            attribution_mode=PublicWishFulfillmentAttributionMode(payload.attribution_mode),
        )
    )

    db.commit()
    db.refresh(wish)

    media_ids = {media_id for media_id in (wish.media_id, wish.fulfilled_evidence_media_id) if media_id is not None}
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}

    guardian_map = _load_frozen_guardians_map(db=db, wishes=[wish])
    fulfillment_map, fulfiller_map = _load_fulfillment_maps_for_wishes(db=db, wishes=[wish])
    return _wish_out(locale=locale, 
        wish=wish,
        media_map=media_map,
        user_map=guardian_map,
        fulfillment_map=fulfillment_map,
        public_fulfiller_map=fulfiller_map,
    )


@router.post("/personal/{wish_id}/freeze", response_model=PublicPersonalWishOut)
def freeze_personal_wish(
    request: Request,
    wish_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    guardian_user = _resolve_guardian_user(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Personal wish not found."))

    if wish.frozen_by_guardian_id and wish.frozen_at:
        raise HTTPException(status_code=409, detail=_td(locale, "This wish is already frozen."))

    wish.frozen_by_guardian_id = int(guardian_user.id)
    wish.frozen_at = datetime.now(timezone.utc)

    db.add(
        PublicWishFreezeAudit(
            wish_id=int(wish.id),
            actor_guardian_id=int(guardian_user.id),
            action=PublicWishFreezeAuditAction.freeze,
            reason_type=None,
            reason_text=None,
        )
    )

    db.commit()
    db.refresh(wish)

    media_ids = {media_id for media_id in (wish.media_id, wish.fulfilled_evidence_media_id) if media_id is not None}
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}

    guardian_map = _load_frozen_guardians_map(db=db, wishes=[wish])
    return _wish_out(locale=locale, wish=wish, media_map=media_map, user_map=guardian_map)


@router.post("/personal/{wish_id}/unfreeze", response_model=PublicPersonalWishOut)
def unfreeze_personal_wish(
    request: Request,
    wish_id: int,
    payload: PublicPersonalWishUnfreezeRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    guardian_user = _resolve_guardian_user(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Personal wish not found."))

    if not (wish.frozen_by_guardian_id and wish.frozen_at):
        raise HTTPException(status_code=409, detail=_td(locale, "This wish is not frozen."))

    if int(wish.frozen_by_guardian_id) != int(guardian_user.id):
        raise HTTPException(status_code=403, detail=_td(locale, "Only the guardian who froze the wish can unfreeze it."))

    reason_type = (
        PublicWishUnfreezeReasonType.error
        if payload.reason_type == "error"
        else PublicWishUnfreezeReasonType.unexpected
    )
    reason_text = payload.reason_text

    wish.frozen_by_guardian_id = None
    wish.frozen_at = None

    db.add(
        PublicWishFreezeAudit(
            wish_id=int(wish.id),
            actor_guardian_id=int(guardian_user.id),
            action=PublicWishFreezeAuditAction.unfreeze,
            reason_type=reason_type,
            reason_text=reason_text,
        )
    )

    db.commit()
    db.refresh(wish)

    media_ids = {media_id for media_id in (wish.media_id, wish.fulfilled_evidence_media_id) if media_id is not None}
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in medias}

    guardian_map = _load_frozen_guardians_map(db=db, wishes=[wish])
    return _wish_out(locale=locale, wish=wish, media_map=media_map, user_map=guardian_map)


@router.delete("/personal/{wish_id}", response_model=PublicPersonalWishDeleteResponse)
def delete_personal_wish(
    request: Request,
    wish_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    _require_public_actions_allowed(db=db, user_id=current.user_number, locale=locale)

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Personal wish not found."))

    db.delete(wish)
    db.commit()
    return PublicPersonalWishDeleteResponse(deleted=True)
