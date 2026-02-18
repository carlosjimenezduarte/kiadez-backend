from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.db.database import get_db
from app.db.models.oracle import OracleResponse, OracleResponseType, OracleUserState
from app.db.models.user import User
from app.db.models.user_vault import UserVault
from app.oracle.schemas import OracleRespondRequest, OracleResponseOut, OracleStateOut


router = APIRouter(prefix="/oracle", tags=["oracle"])

TOTAL_CARDS = 30
COOLDOWN_MS = 72 * 60 * 60 * 1000
COOLDOWN_DELTA = timedelta(milliseconds=COOLDOWN_MS)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _parse_hex_bytes(value: str | None, *, field: str) -> bytes:
    if not value:
        raise HTTPException(status_code=400, detail=f"Campo requerido: {field}.")
    try:
        return bytes.fromhex(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"{field} inválido (hex).") from exc


def _cooldown_remaining_ms(last_pick_at: datetime | None, now: datetime) -> int:
    if not last_pick_at:
        return 0
    remaining = int((last_pick_at + COOLDOWN_DELTA - now).total_seconds() * 1000)
    return max(0, remaining)


def _get_or_create_state(*, db: Session, user_id: int) -> tuple[OracleUserState, bool]:
    state = db.query(OracleUserState).filter(OracleUserState.user_id == user_id).one_or_none()
    if state:
        return state, False

    state = OracleUserState(
        user_id=user_id,
        cycle=1,
        cycle_started_at=_utcnow(),
        last_pick_at=None,
    )
    db.add(state)
    db.flush()
    return state, True


def _revealed_card_ids(*, db: Session, user_id: int, cycle: int) -> list[int]:
    rows = (
        db.query(OracleResponse.card_id)
        .filter(OracleResponse.user_id == user_id, OracleResponse.cycle == cycle)
        .distinct()
        .all()
    )
    return sorted(int(row[0]) for row in rows if row[0] is not None)


def _maybe_advance_cycle(*, db: Session, user_id: int, state: OracleUserState, now: datetime) -> bool:
    revealed_ids = _revealed_card_ids(db=db, user_id=user_id, cycle=state.cycle)
    cycle_complete = len(revealed_ids) >= TOTAL_CARDS
    if not cycle_complete:
        return False

    if state.last_pick_at is None or now >= state.last_pick_at + COOLDOWN_DELTA:
        state.cycle = int(state.cycle) + 1
        state.cycle_started_at = now
        state.last_pick_at = None
        db.flush()
        return True

    return False


def _response_out(response: OracleResponse) -> OracleResponseOut:
    return OracleResponseOut(
        id=response.id,
        card_id=response.card_id,
        cycle=response.cycle,
        response_type=response.response_type,
        created_at=response.created_at,
        text_public=response.text_public,
        ciphertext_hex=response.ciphertext.hex() if response.ciphertext else None,
        nonce_hex=response.nonce.hex() if response.nonce else None,
    )


def _build_state_payload(*, db: Session, user_id: int, state: OracleUserState, now: datetime) -> OracleStateOut:
    revealed_this_cycle = _revealed_card_ids(db=db, user_id=user_id, cycle=state.cycle)
    responses = (
        db.query(OracleResponse)
        .filter(OracleResponse.user_id == user_id)
        .order_by(OracleResponse.created_at.desc(), OracleResponse.id.desc())
        .all()
    )

    return OracleStateOut(
        cycle=state.cycle,
        cycle_started_at=state.cycle_started_at,
        last_pick_at=state.last_pick_at,
        cooldown_ms=COOLDOWN_MS,
        cooldown_remaining_ms=_cooldown_remaining_ms(state.last_pick_at, now),
        cycle_complete=len(revealed_this_cycle) >= TOTAL_CARDS,
        revealed_this_cycle=revealed_this_cycle,
        responses=[_response_out(response) for response in responses],
    )


@router.get("/state", response_model=OracleStateOut)
def get_oracle_state(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = int(current.user_number)
    state, created = _get_or_create_state(db=db, user_id=user_id)

    now = _utcnow()
    advanced = _maybe_advance_cycle(db=db, user_id=user_id, state=state, now=now)

    if created or advanced:
        db.commit()
        db.refresh(state)

    return _build_state_payload(db=db, user_id=user_id, state=state, now=_utcnow())


@router.get("/public/{user_id}", response_model=OracleStateOut)
def get_public_oracle_state(
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_active.is_(True),
        )
        .one_or_none()
    )
    if target is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    is_owner = int(current.user_number) == int(user_id)
    if not is_owner and not bool(target.public_profile_show_oracle):
        raise HTTPException(status_code=403, detail="Este módulo es privado.")

    responses = (
        db.query(OracleResponse)
        .filter(
            OracleResponse.user_id == user_id,
            OracleResponse.response_type == OracleResponseType.public,
        )
        .order_by(OracleResponse.created_at.desc(), OracleResponse.id.desc())
        .all()
    )
    revealed_public = sorted(
        {int(response.card_id) for response in responses if response.card_id is not None}
    )

    now = _utcnow()
    return OracleStateOut(
        cycle=1,
        cycle_started_at=now,
        last_pick_at=None,
        cooldown_ms=COOLDOWN_MS,
        cooldown_remaining_ms=0,
        cycle_complete=False,
        revealed_this_cycle=revealed_public,
        responses=[_response_out(response) for response in responses],
    )


@router.post("/respond", response_model=OracleStateOut)
def respond_oracle_card(
    payload: OracleRespondRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = int(current.user_number)
    state, _ = _get_or_create_state(db=db, user_id=user_id)

    now = _utcnow()
    _maybe_advance_cycle(db=db, user_id=user_id, state=state, now=now)

    if payload.response_type == OracleResponseType.secret:
        has_vault = db.query(UserVault).filter(UserVault.user_id == user_id).one_or_none()
        if not has_vault:
            raise HTTPException(
                status_code=409,
                detail="Debes crear y desbloquear tu clave privada para guardar respuestas secretas.",
            )

    current_cycle_entries = (
        db.query(OracleResponse)
        .filter(
            OracleResponse.user_id == user_id,
            OracleResponse.cycle == state.cycle,
            OracleResponse.card_id == payload.card_id,
        )
        .order_by(OracleResponse.created_at.desc(), OracleResponse.id.desc())
        .all()
    )

    has_answered = any(
        entry.response_type in {OracleResponseType.public, OracleResponseType.secret}
        for entry in current_cycle_entries
    )
    if has_answered:
        raise HTTPException(
            status_code=409,
            detail="Esta carta ya tiene una respuesta pública o secreta en este ciclo.",
        )

    card_revealed = bool(current_cycle_entries)
    if not card_revealed:
        remaining_ms = _cooldown_remaining_ms(state.last_pick_at, now)
        if remaining_ms > 0:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Carta bloqueada temporalmente. "
                    "Debes esperar a que termine el cooldown para elegir una nueva carta."
                ),
            )
        state.last_pick_at = now

    text_public: str | None = None
    ciphertext: bytes | None = None
    nonce: bytes | None = None

    if payload.response_type == OracleResponseType.public:
        text_public = (payload.text_public or "").strip()
        if not text_public:
            raise HTTPException(status_code=400, detail="La respuesta pública no puede estar vacía.")
    elif payload.response_type == OracleResponseType.secret:
        ciphertext = _parse_hex_bytes(payload.ciphertext_hex, field="ciphertext_hex")
        nonce = _parse_hex_bytes(payload.nonce_hex, field="nonce_hex")
        if len(nonce) != 12:
            raise HTTPException(status_code=400, detail="nonce_hex inválido (se esperan 12 bytes).")

    response = OracleResponse(
        user_id=user_id,
        card_id=payload.card_id,
        cycle=state.cycle,
        response_type=payload.response_type,
        text_public=text_public,
        ciphertext=ciphertext,
        nonce=nonce,
    )
    db.add(response)
    db.commit()
    db.refresh(state)

    return _build_state_payload(db=db, user_id=user_id, state=state, now=_utcnow())


@router.delete("/responses/{response_id}", response_model=OracleStateOut)
def delete_oracle_response(
    response_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = int(current.user_number)
    state, _ = _get_or_create_state(db=db, user_id=user_id)

    now = _utcnow()
    _maybe_advance_cycle(db=db, user_id=user_id, state=state, now=now)

    response = (
        db.query(OracleResponse)
        .filter(
            OracleResponse.id == response_id,
            OracleResponse.user_id == user_id,
        )
        .one_or_none()
    )
    if response is None:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada.")

    if int(response.cycle) >= int(state.cycle):
        raise HTTPException(
            status_code=409,
            detail="Solo puedes borrar respuestas de ciclos pasados.",
        )

    db.delete(response)
    db.commit()
    db.refresh(state)

    return _build_state_payload(db=db, user_id=user_id, state=state, now=_utcnow())
