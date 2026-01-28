# app/vault/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth.routes import get_current_user
from app.auth.models import UserPublic
from app.db.models.user_vault import UserVault

router = APIRouter(prefix="/vault", tags=["vault"])

@router.get("/status")
def vault_status(current: UserPublic = Depends(get_current_user), db: Session = Depends(get_db)):
    vault = db.query(UserVault).filter(UserVault.user_id == current.user_number).one_or_none()
    return {"has_vault": bool(vault)}

@router.get("/record")
def vault_record(current: UserPublic = Depends(get_current_user), db: Session = Depends(get_db)):
    vault = db.query(UserVault).filter(UserVault.user_id == current.user_number).one_or_none()
    if not vault:
        raise HTTPException(status_code=404, detail="No hay vault.")
    # Solo metadatos (zero-knowledge)
    return {
        "kdf_name": vault.kdf_name,
        "kdf_iters": vault.kdf_iters,
        "kdf_salt_b64": vault.kdf_salt.hex(),  # puedes usar base64 si prefieres; hex es simple
        "wrapped_dek_nonce_b64": vault.wrapped_dek_nonce.hex(),
        "wrapped_dek_b64": vault.wrapped_dek.hex(),
    }

@router.post("/setup")
def vault_setup(payload: dict, current: UserPublic = Depends(get_current_user), db: Session = Depends(get_db)):
    # Esperamos bytes en hex para simplicidad
    kdf_name = payload.get("kdf_name") or "pbkdf2_sha256"
    kdf_iters = int(payload.get("kdf_iters") or 310000)

    salt_hex = payload.get("kdf_salt_hex")
    nonce_hex = payload.get("wrapped_dek_nonce_hex")
    wrapped_hex = payload.get("wrapped_dek_hex")

    if not salt_hex or not nonce_hex or not wrapped_hex:
        raise HTTPException(status_code=400, detail="Datos incompletos de vault.")

    existing = db.query(UserVault).filter(UserVault.user_id == current.user_number).one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Vault ya existe.")

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
def vault_rewrap(payload: dict, current: UserPublic = Depends(get_current_user), db: Session = Depends(get_db)):
    # IMPORTANTE: este endpoint debe exigir 2FA (política), para evitar sabotaje con access token robado.
    # Aquí lo dejamos “listo” y luego amarramos la verificación 2FA al endpoint.

    vault = db.query(UserVault).filter(UserVault.user_id == current.user_number).one_or_none()
    if not vault:
        raise HTTPException(status_code=404, detail="No hay vault.")

    kdf_name = payload.get("kdf_name") or vault.kdf_name
    kdf_iters = int(payload.get("kdf_iters") or vault.kdf_iters)

    salt_hex = payload.get("kdf_salt_hex")
    nonce_hex = payload.get("wrapped_dek_nonce_hex")
    wrapped_hex = payload.get("wrapped_dek_hex")

    if not salt_hex or not nonce_hex or not wrapped_hex:
        raise HTTPException(status_code=400, detail="Datos incompletos.")

    vault.kdf_name = kdf_name
    vault.kdf_iters = kdf_iters
    vault.kdf_salt = bytes.fromhex(salt_hex)
    vault.wrapped_dek_nonce = bytes.fromhex(nonce_hex)
    vault.wrapped_dek = bytes.fromhex(wrapped_hex)

    db.commit()
    return {"vault_rewrapped": True}
