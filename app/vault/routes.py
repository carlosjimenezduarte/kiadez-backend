# app/vault/routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth.routes import get_current_user
from app.auth.models import UserPublic
from app.core.i18n import locale_from_request, tr as i18n_tr
from app.db.models.user_vault import UserVault
from app.db.models.life_purpose import LifePurpose
from app.db.models.private_personal_wish import PrivatePersonalWish
from app.db.models.media import Media, MediaVisibility
from app.db.models.oracle import OracleResponse, OracleResponseType
from app.core.storage import S3NotConfiguredError, delete_object
from app.vault.schemas import VaultResetKeywordsOut, VaultResetOut, VaultResetRequest

router = APIRouter(prefix="/vault", tags=["vault"])

RESET_KEYWORDS = {
    "es": "ELIMINAR",
    "en": "DELETE",
    "fr": "SUPPRIMER",
}


def _locale(request: Request | None) -> str:
    return locale_from_request(request, default="en")


def _td(locale: str, en: str) -> str:
    translations: dict[str, tuple[str, str]] = {
        "No vault found.": ("No se encontró bóveda.", "Aucun coffre trouvé."),
        "Incomplete vault payload.": (
            "Carga de bóveda incompleta.",
            "Charge utile du coffre incomplète.",
        ),
        "Vault already exists.": ("La bóveda ya existe.", "Le coffre existe déjà."),
        "Incomplete payload.": ("Carga incompleta.", "Charge utile incomplète."),
        "Invalid confirmation keyword.": (
            "Palabra clave de confirmación inválida.",
            "Mot-clé de confirmation invalide.",
        ),
    }
    pair = translations.get(en)
    if not pair:
        return en
    es, fr = pair
    return i18n_tr(locale, es=es, en=en, fr=fr)


@router.get("/status")
def vault_status(current: UserPublic = Depends(get_current_user), db: Session = Depends(get_db)):
    vault = db.query(UserVault).filter(UserVault.user_id == current.user_number).one_or_none()
    return {"has_vault": bool(vault)}

@router.get("/record")
def vault_record(request: Request, current: UserPublic = Depends(get_current_user), db: Session = Depends(get_db)):
    locale = _locale(request)
    vault = db.query(UserVault).filter(UserVault.user_id == current.user_number).one_or_none()
    if not vault:
        raise HTTPException(status_code=404, detail=_td(locale, "No vault found."))
    # Solo metadatos (zero-knowledge)
    return {
        "kdf_name": vault.kdf_name,
        "kdf_iters": vault.kdf_iters,
        "kdf_salt_b64": vault.kdf_salt.hex(),  # puedes usar base64 si prefieres; hex es simple
        "wrapped_dek_nonce_b64": vault.wrapped_dek_nonce.hex(),
        "wrapped_dek_b64": vault.wrapped_dek.hex(),
    }

@router.post("/setup")
def vault_setup(request: Request, payload: dict, current: UserPublic = Depends(get_current_user), db: Session = Depends(get_db)):
    locale = _locale(request)
    # Esperamos bytes en hex para simplicidad
    kdf_name = payload.get("kdf_name") or "pbkdf2_sha256"
    kdf_iters = int(payload.get("kdf_iters") or 310000)

    salt_hex = payload.get("kdf_salt_hex")
    nonce_hex = payload.get("wrapped_dek_nonce_hex")
    wrapped_hex = payload.get("wrapped_dek_hex")

    if not salt_hex or not nonce_hex or not wrapped_hex:
        raise HTTPException(status_code=400, detail=_td(locale, "Incomplete vault payload."))

    existing = db.query(UserVault).filter(UserVault.user_id == current.user_number).one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail=_td(locale, "Vault already exists."))

    vault = UserVault(
        user_id=current.user_number,
        kdf_name=kdf_name,
        kdf_iters=kdf_iters,
        kdf_salt=bytes.fromhex(salt_hex),
        wrapped_dek_nonce=bytes.fromhex(nonce_hex),
        wrapped_dek=bytes.fromhex(wrapped_hex),
    )
    db.add(vault)
    db.commit()

    return {"vault_created": True}

@router.post("/rewrap")
def vault_rewrap(request: Request, payload: dict, current: UserPublic = Depends(get_current_user), db: Session = Depends(get_db)):
    locale = _locale(request)
    # IMPORTANTE: este endpoint debe exigir 2FA (política), para evitar sabotaje con access token robado.
    # Aquí lo dejamos “listo” y luego amarramos la verificación 2FA al endpoint.

    vault = db.query(UserVault).filter(UserVault.user_id == current.user_number).one_or_none()
    if not vault:
        raise HTTPException(status_code=404, detail=_td(locale, "No vault found."))

    kdf_name = payload.get("kdf_name") or vault.kdf_name
    kdf_iters = int(payload.get("kdf_iters") or vault.kdf_iters)

    salt_hex = payload.get("kdf_salt_hex")
    nonce_hex = payload.get("wrapped_dek_nonce_hex")
    wrapped_hex = payload.get("wrapped_dek_hex")

    if not salt_hex or not nonce_hex or not wrapped_hex:
        raise HTTPException(status_code=400, detail=_td(locale, "Incomplete payload."))

    vault.kdf_name = kdf_name
    vault.kdf_iters = kdf_iters
    vault.kdf_salt = bytes.fromhex(salt_hex)
    vault.wrapped_dek_nonce = bytes.fromhex(nonce_hex)
    vault.wrapped_dek = bytes.fromhex(wrapped_hex)

    db.commit()
    return {"vault_rewrapped": True}


@router.get("/reset-keywords", response_model=VaultResetKeywordsOut)
def vault_reset_keywords(current: UserPublic = Depends(get_current_user)):
    # Confirmación multi-idioma para acciones destructivas.
    return {"keywords": RESET_KEYWORDS}


@router.post("/reset", response_model=VaultResetOut)
def vault_reset(request: Request, payload: VaultResetRequest, current: UserPublic = Depends(get_current_user), db: Session = Depends(get_db)):
    locale = _locale(request)
    confirm = (payload.confirm_keyword or "").strip().upper()
    allowed = {value.upper() for value in RESET_KEYWORDS.values()}
    if confirm not in allowed:
        raise HTTPException(status_code=400, detail=_td(locale, "Invalid confirmation keyword."))

    vault = db.query(UserVault).filter(UserVault.user_id == current.user_number).one_or_none()
    if not vault:
        raise HTTPException(status_code=404, detail=_td(locale, "No vault found."))

    # Al eliminar el vault se pierde el DEK; cualquier dato cifrado es irrecuperable.
    # Limpiamos datos privados ligados al vault para que el usuario pueda reiniciar su espacio.
    cleared_life_purpose = (
        db.query(LifePurpose)
        .filter(LifePurpose.user_id == current.user_number, LifePurpose.is_private.is_(True))
        .delete(synchronize_session=False)
    )

    # Wishes privados (cifrados) + media asociada (también cifrada) son irrecuperables tras el reset.
    private_wishes = db.query(PrivatePersonalWish).filter(PrivatePersonalWish.user_id == current.user_number).all()
    media_ids: set[int] = set()
    for wish in private_wishes:
        if wish.media_id:
            media_ids.add(int(wish.media_id))
        if wish.fulfilled_evidence_media_id:
            media_ids.add(int(wish.fulfilled_evidence_media_id))

    cleared_private_wishes = (
        db.query(PrivatePersonalWish)
        .filter(PrivatePersonalWish.user_id == current.user_number)
        .delete(synchronize_session=False)
    )

    # Respuestas secretas del Oráculo (cifradas) dejan de ser recuperables tras resetear el vault.
    cleared_oracle_secret_responses = (
        db.query(OracleResponse)
        .filter(
            OracleResponse.user_id == current.user_number,
            OracleResponse.response_type == OracleResponseType.secret,
        )
        .delete(synchronize_session=False)
    )

    deleted_media = 0
    if media_ids:
        medias = db.query(Media).filter(Media.id.in_(media_ids)).all()
        for media in medias:
            # Best-effort deletion from storage.
            try:
                if media.visibility == MediaVisibility.private:
                    delete_object(key=media.object_key)
            except S3NotConfiguredError:
                pass
            except Exception:
                pass
            if media.owner_id == current.user_number:
                db.delete(media)
                deleted_media += 1

    db.delete(vault)
    db.commit()

    return {
        "vault_deleted": True,
        "life_purpose_private_cleared": int(cleared_life_purpose or 0),
        "private_wishes_cleared": int(cleared_private_wishes or 0),
        "private_media_deleted": int(deleted_media or 0),
        "oracle_secret_responses_cleared": int(cleared_oracle_secret_responses or 0),
    }
