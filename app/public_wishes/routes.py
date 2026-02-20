from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.config import settings
from app.core.storage import S3NotConfiguredError, generate_presigned_get_url
from app.db.database import get_db
from app.db.models.guardian_wish_request import GuardianWishRequest, GuardianWishRequestStatus
from app.db.models.media import Media
from app.db.models.public_cooperative_wish import PublicCooperativeWish
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
    PublicCooperativeWishListOut,
    PublicCooperativeWishOut,
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
FULFILLMENT_SECRET_MESSAGE = "Quien cumplió el deseo decidió obrar desde lo secreto."


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
            frozen_full_name = f"Usuario {frozen_by_user.id}"
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
            fulfillment_message = FULFILLMENT_SECRET_MESSAGE
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
            fulfillment_message = f"Deseo cumplido gracias a {fulfilled_by_handle}"

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


def _resolve_owned_media(*, db: Session, media_id: int | None, user_id: int) -> Media | None:
    if media_id is None:
        return None

    media = db.execute(select(Media).where(Media.id == media_id)).scalar_one_or_none()
    if media is None:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if media.owner_id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado para usar esta media.")
    if media.status != "ready":
        raise HTTPException(status_code=409, detail="Media aún no disponible.")
    return media


def _load_cooperative_participants_count_map(
    *,
    db: Session,
    wish_ids: list[int],
) -> dict[int, int]:
    if not wish_ids:
        return {}

    rows = db.execute(
        select(
            PublicCooperativeWishParticipation.wish_id,
            func.count(PublicCooperativeWishParticipation.id),
        )
        .where(PublicCooperativeWishParticipation.wish_id.in_(wish_ids))
        .group_by(PublicCooperativeWishParticipation.wish_id)
    ).all()
    return {int(row[0]): int(row[1]) for row in rows}


def _load_viewer_cooperative_participation_map(
    *,
    db: Session,
    wish_ids: list[int],
    viewer_user_id: int,
) -> dict[int, PublicCooperativeWishParticipation]:
    if not wish_ids:
        return {}

    rows = db.execute(
        select(PublicCooperativeWishParticipation)
        .where(PublicCooperativeWishParticipation.wish_id.in_(wish_ids))
        .where(PublicCooperativeWishParticipation.participant_user_id == viewer_user_id)
    ).scalars().all()
    return {int(row.wish_id): row for row in rows}


def _cooperative_wish_out(
    *,
    wish: PublicCooperativeWish,
    media_map: dict[int, Media],
    current_user_id: int,
    participants_count_map: dict[int, int] | None = None,
    viewer_participation_map: dict[int, PublicCooperativeWishParticipation] | None = None,
) -> PublicCooperativeWishOut:
    media = media_map.get(wish.media_id) if wish.media_id else None
    participants_current = int((participants_count_map or {}).get(int(wish.id), 0))
    is_owner = int(current_user_id) == int(wish.user_id)
    viewer_participation = (
        (viewer_participation_map or {}).get(int(wish.id))
        if viewer_participation_map is not None
        else None
    )
    return PublicCooperativeWishOut(
        id=int(wish.id),
        user_id=int(wish.user_id),
        wish_text=wish.wish_text,
        wish_type=wish.wish_type,
        participants_goal=int(wish.participants_goal or 0),
        participants_current=participants_current,
        template_text=wish.template_text,
        security_code=wish.security_code if is_owner else None,
        media_id=wish.media_id,
        media_url=_build_media_url(media),
        viewer_participation_text=viewer_participation.participation_text if viewer_participation else None,
        created_at=wish.created_at,
        updated_at=wish.updated_at,
    )


def _resolve_guardian_user(*, db: Session, user_id: int) -> User:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if int(user.guardian_rank or 0) < GUARDIAN_REQUIRED_RANK:
        raise HTTPException(status_code=403, detail="Acceso restringido (rango de Guardián requerido).")
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
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

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
        items=[_wish_out(wish=wish, media_map=media_map, user_map=guardian_map) for wish in wishes],
        active_count=len(wishes),
        active_limit=PERSONAL_ACTIVE_LIMIT,
        fulfilled_total=fulfilled_total or 0,
    )


@router.get("/user/{user_id}/personal", response_model=PublicPersonalWishListOut)
def list_user_personal_wishes(
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target = db.execute(
        select(User).where(User.id == user_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    is_owner = int(current.user_number) == int(user_id)
    if not is_owner and not bool(target.public_profile_show_public_wishes):
        raise HTTPException(status_code=403, detail="Este módulo es privado.")

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
        items=[_wish_out(wish=wish, media_map=media_map, user_map=guardian_map) for wish in wishes],
        active_count=len(wishes),
        active_limit=PERSONAL_ACTIVE_LIMIT,
        fulfilled_total=fulfilled_total or 0,
    )


@router.get("/cooperative", response_model=PublicCooperativeWishListOut)
def list_cooperative_wishes(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    wishes = db.execute(
        select(PublicCooperativeWish)
        .where(PublicCooperativeWish.user_id == current.user_number)
        .order_by(PublicCooperativeWish.created_at.desc(), PublicCooperativeWish.id.desc())
    ).scalars().all()

    wish_ids = [int(wish.id) for wish in wishes]
    media_ids = {int(wish.media_id) for wish in wishes if wish.media_id is not None}
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {int(media.id): media for media in medias}

    participants_count_map = _load_cooperative_participants_count_map(db=db, wish_ids=wish_ids)
    viewer_participation_map = _load_viewer_cooperative_participation_map(
        db=db,
        wish_ids=wish_ids,
        viewer_user_id=current.user_number,
    )

    return PublicCooperativeWishListOut(
        items=[
            _cooperative_wish_out(
                wish=wish,
                media_map=media_map,
                current_user_id=current.user_number,
                participants_count_map=participants_count_map,
                viewer_participation_map=viewer_participation_map,
            )
            for wish in wishes
        ],
        active_count=len(wishes),
        active_limit=COOPERATIVE_ACTIVE_LIMIT,
    )


@router.get("/user/{user_id}/cooperative", response_model=PublicCooperativeWishListOut)
def list_user_cooperative_wishes(
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target = db.execute(
        select(User).where(User.id == user_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    is_owner = int(current.user_number) == int(user_id)
    if not is_owner and not bool(target.public_profile_show_public_wishes):
        raise HTTPException(status_code=403, detail="Este módulo es privado.")

    wishes = db.execute(
        select(PublicCooperativeWish)
        .where(PublicCooperativeWish.user_id == user_id)
        .order_by(PublicCooperativeWish.created_at.desc(), PublicCooperativeWish.id.desc())
    ).scalars().all()

    wish_ids = [int(wish.id) for wish in wishes]
    media_ids = {int(wish.media_id) for wish in wishes if wish.media_id is not None}
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {int(media.id): media for media in medias}

    participants_count_map = _load_cooperative_participants_count_map(db=db, wish_ids=wish_ids)
    viewer_participation_map = _load_viewer_cooperative_participation_map(
        db=db,
        wish_ids=wish_ids,
        viewer_user_id=current.user_number,
    )

    return PublicCooperativeWishListOut(
        items=[
            _cooperative_wish_out(
                wish=wish,
                media_map=media_map,
                current_user_id=current.user_number,
                participants_count_map=participants_count_map,
                viewer_participation_map=viewer_participation_map,
            )
            for wish in wishes
        ],
        active_count=len(wishes),
        active_limit=COOPERATIVE_ACTIVE_LIMIT,
    )


@router.post("/cooperative", response_model=PublicCooperativeWishOut)
def create_cooperative_wish(
    payload: PublicCooperativeWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    active_count = db.execute(
        select(func.count(PublicCooperativeWish.id)).where(PublicCooperativeWish.user_id == current.user_number)
    ).scalar_one()
    if int(active_count or 0) >= COOPERATIVE_ACTIVE_LIMIT:
        raise HTTPException(
            status_code=409,
            detail=f"Ya alcanzaste el máximo de {COOPERATIVE_ACTIVE_LIMIT} deseos cooperativos activos.",
        )

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number)
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

    media_map = {int(media.id): media} if media else {}
    return _cooperative_wish_out(
        wish=wish,
        media_map=media_map,
        current_user_id=current.user_number,
        participants_count_map={int(wish.id): 0},
        viewer_participation_map={},
    )


@router.put("/cooperative/{wish_id}", response_model=PublicCooperativeWishOut)
def update_cooperative_wish(
    wish_id: int,
    payload: PublicCooperativeWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    wish = db.execute(
        select(PublicCooperativeWish)
        .where(PublicCooperativeWish.id == wish_id)
        .where(PublicCooperativeWish.user_id == current.user_number)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo cooperativo no encontrado.")

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number)
    wish.wish_text = payload.wish_text
    wish.wish_type = payload.wish_type
    wish.participants_goal = payload.participants_goal
    wish.template_text = payload.template_text
    wish.security_code = payload.security_code
    wish.media_id = media.id if media else None

    db.commit()
    db.refresh(wish)

    media_ids = {int(wish.media_id)} if wish.media_id is not None else set()
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {int(media.id): media for media in medias}

    participants_count_map = _load_cooperative_participants_count_map(db=db, wish_ids=[int(wish.id)])
    viewer_participation_map = _load_viewer_cooperative_participation_map(
        db=db,
        wish_ids=[int(wish.id)],
        viewer_user_id=current.user_number,
    )
    return _cooperative_wish_out(
        wish=wish,
        media_map=media_map,
        current_user_id=current.user_number,
        participants_count_map=participants_count_map,
        viewer_participation_map=viewer_participation_map,
    )


@router.post("/cooperative/{wish_id}/participate", response_model=PublicCooperativeWishOut)
def participate_in_cooperative_wish(
    wish_id: int,
    payload: PublicCooperativeWishParticipationUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    wish = db.execute(select(PublicCooperativeWish).where(PublicCooperativeWish.id == wish_id)).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo cooperativo no encontrado.")

    owner = db.execute(
        select(User).where(User.id == int(wish.user_id), User.is_active.is_(True))
    ).scalar_one_or_none()
    if owner is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    if int(current.user_number) == int(wish.user_id):
        raise HTTPException(status_code=409, detail="No puedes registrar participación en tu propio deseo cooperativo.")

    if not bool(owner.public_profile_show_public_wishes):
        raise HTTPException(status_code=403, detail="Este módulo es privado.")

    expected_code = (wish.security_code or "").strip()
    provided_code = (payload.security_code or "").strip()
    if not expected_code or expected_code != provided_code:
        raise HTTPException(status_code=403, detail="Código de seguridad inválido.")

    participation = db.execute(
        select(PublicCooperativeWishParticipation)
        .where(PublicCooperativeWishParticipation.wish_id == int(wish.id))
        .where(PublicCooperativeWishParticipation.participant_user_id == int(current.user_number))
    ).scalar_one_or_none()
    if participation is None:
        participation = PublicCooperativeWishParticipation(
            wish_id=int(wish.id),
            participant_user_id=int(current.user_number),
            participation_text=payload.participation_text,
        )
        db.add(participation)
    else:
        participation.participation_text = payload.participation_text

    db.commit()
    db.refresh(wish)

    media_ids = {int(wish.media_id)} if wish.media_id is not None else set()
    media_map: dict[int, Media] = {}
    if media_ids:
        medias = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {int(media.id): media for media in medias}

    participants_count_map = _load_cooperative_participants_count_map(db=db, wish_ids=[int(wish.id)])
    viewer_participation_map = _load_viewer_cooperative_participation_map(
        db=db,
        wish_ids=[int(wish.id)],
        viewer_user_id=current.user_number,
    )
    return _cooperative_wish_out(
        wish=wish,
        media_map=media_map,
        current_user_id=current.user_number,
        participants_count_map=participants_count_map,
        viewer_participation_map=viewer_participation_map,
    )


@router.delete("/cooperative/{wish_id}", response_model=PublicPersonalWishDeleteResponse)
def delete_cooperative_wish(
    wish_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    wish = db.execute(
        select(PublicCooperativeWish)
        .where(PublicCooperativeWish.id == wish_id)
        .where(PublicCooperativeWish.user_id == current.user_number)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo cooperativo no encontrado.")

    db.delete(wish)
    db.commit()
    return PublicPersonalWishDeleteResponse(deleted=True)


@router.get("/personal/fulfilled", response_model=PublicPersonalWishFulfilledListOut)
def list_fulfilled_personal_wishes(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

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
            _wish_out(
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
    user_id: int,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target = db.execute(
        select(User).where(User.id == user_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    is_owner = int(current.user_number) == int(user_id)
    if not is_owner and not bool(target.public_profile_show_fulfilled_wishes):
        raise HTTPException(status_code=403, detail="Este módulo es privado.")

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
            _wish_out(
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
    payload: PublicPersonalWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    active_count = db.execute(
        select(func.count(PublicPersonalWish.id))
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one()
    if active_count >= PERSONAL_ACTIVE_LIMIT:
        raise HTTPException(
            status_code=409,
            detail=f"Ya alcanzaste el máximo de {PERSONAL_ACTIVE_LIMIT} deseos personales activos.",
        )

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number)

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
    return _wish_out(wish=wish, media_map=media_map, user_map={})


@router.put("/personal/{wish_id}", response_model=PublicPersonalWishOut)
def update_personal_wish(
    wish_id: int,
    payload: PublicPersonalWishUpsertRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo personal no encontrado.")

    media = _resolve_owned_media(db=db, media_id=payload.media_id, user_id=current.user_number)

    wish.wish_text = payload.wish_text
    wish.wish_type = payload.wish_type
    wish.media_id = media.id if media else None

    db.commit()
    db.refresh(wish)

    media_map = {media.id: media} if media else {}
    return _wish_out(wish=wish, media_map=media_map, user_map={})


@router.post("/personal/{wish_id}/fulfill", response_model=PublicPersonalWishOut)
def fulfill_personal_wish(
    wish_id: int,
    payload: PublicPersonalWishFulfillRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo personal no encontrado.")

    evidence_media = _resolve_owned_media(
        db=db,
        media_id=payload.evidence_media_id,
        user_id=current.user_number,
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
    return _wish_out(wish=wish, media_map=media_map, user_map=guardian_map)


@router.post("/personal/{wish_id}/guardian-fulfill", response_model=PublicPersonalWishOut)
def guardian_fulfill_personal_wish(
    wish_id: int,
    payload: PublicPersonalWishGuardianFulfillRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    guardian_user = _resolve_guardian_user(db=db, user_id=current.user_number)

    wish = db.execute(
        select(PublicPersonalWish).where(PublicPersonalWish.id == wish_id)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo personal no encontrado.")
    if wish.status != PublicPersonalWishStatus.active:
        raise HTTPException(status_code=409, detail="Este deseo ya no está activo.")

    if not (wish.frozen_by_guardian_id and wish.frozen_at):
        raise HTTPException(status_code=409, detail="Este deseo no está congelado.")
    if int(wish.frozen_by_guardian_id) != int(guardian_user.id):
        raise HTTPException(status_code=403, detail="Solo el guardián que congeló el deseo puede marcarlo como cumplido.")

    commitment_code = (payload.commitment_code or "").strip().upper()
    if not commitment_code:
        raise HTTPException(status_code=400, detail="Debes indicar el código de compromiso.")

    existing_by_wish = db.execute(
        select(PublicWishFulfillment).where(PublicWishFulfillment.wish_id == int(wish.id))
    ).scalar_one_or_none()
    existing_by_code = db.execute(
        select(PublicWishFulfillment).where(PublicWishFulfillment.commitment_code == commitment_code)
    ).scalar_one_or_none()
    if existing_by_wish is not None or existing_by_code is not None:
        raise HTTPException(status_code=409, detail="Este código de compromiso ya fue utilizado.")

    wish_request = db.execute(
        select(GuardianWishRequest).where(GuardianWishRequest.commitment_code == commitment_code)
    ).scalar_one_or_none()
    if wish_request is None:
        raise HTTPException(status_code=404, detail="Código de compromiso no encontrado.")
    if int(wish_request.public_wish_id) != int(wish.id):
        raise HTTPException(status_code=409, detail="El código de compromiso no corresponde a este deseo.")
    if wish_request.commitment_sealed_at is None:
        raise HTTPException(status_code=409, detail="El código de compromiso no ha sido sellado todavía.")
    if wish_request.denied_at is not None:
        raise HTTPException(status_code=409, detail="Esta petición fue denegada y no puede cerrarse como cumplida.")
    if wish_request.guardian_id is not None and int(wish_request.guardian_id) != int(guardian_user.id):
        raise HTTPException(status_code=409, detail="Este compromiso está asignado a otro guardián.")

    fulfiller_user = db.execute(
        select(User).where(User.id == wish_request.requester_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if fulfiller_user is None:
        raise HTTPException(status_code=404, detail="No se encontró al usuario que concedió el deseo.")

    evidence_media = _resolve_owned_media(
        db=db,
        media_id=payload.evidence_media_id,
        user_id=current.user_number,
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
    return _wish_out(
        wish=wish,
        media_map=media_map,
        user_map=guardian_map,
        fulfillment_map=fulfillment_map,
        public_fulfiller_map=fulfiller_map,
    )


@router.post("/personal/{wish_id}/freeze", response_model=PublicPersonalWishOut)
def freeze_personal_wish(
    wish_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    guardian_user = _resolve_guardian_user(db=db, user_id=current.user_number)

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo personal no encontrado.")

    if wish.frozen_by_guardian_id and wish.frozen_at:
        raise HTTPException(status_code=409, detail="Este deseo ya está congelado.")

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
    return _wish_out(wish=wish, media_map=media_map, user_map=guardian_map)


@router.post("/personal/{wish_id}/unfreeze", response_model=PublicPersonalWishOut)
def unfreeze_personal_wish(
    wish_id: int,
    payload: PublicPersonalWishUnfreezeRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    guardian_user = _resolve_guardian_user(db=db, user_id=current.user_number)

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo personal no encontrado.")

    if not (wish.frozen_by_guardian_id and wish.frozen_at):
        raise HTTPException(status_code=409, detail="Este deseo no está congelado.")

    if int(wish.frozen_by_guardian_id) != int(guardian_user.id):
        raise HTTPException(status_code=403, detail="Solo el guardián que congeló el deseo puede descongelarlo.")

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
    return _wish_out(wish=wish, media_map=media_map, user_map=guardian_map)


@router.delete("/personal/{wish_id}", response_model=PublicPersonalWishDeleteResponse)
def delete_personal_wish(
    wish_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.id == current.user_number)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    wish = db.execute(
        select(PublicPersonalWish)
        .where(PublicPersonalWish.id == wish_id)
        .where(PublicPersonalWish.user_id == current.user_number)
        .where(PublicPersonalWish.status == PublicPersonalWishStatus.active)
    ).scalar_one_or_none()
    if wish is None:
        raise HTTPException(status_code=404, detail="Deseo personal no encontrado.")

    db.delete(wish)
    db.commit()
    return PublicPersonalWishDeleteResponse(deleted=True)
