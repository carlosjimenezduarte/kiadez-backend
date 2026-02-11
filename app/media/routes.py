from pathlib import Path
from uuid import uuid4

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.routes import get_current_user
from app.auth.models import UserPublic
from app.core.config import settings
from app.core.security import decode_token
from app.core.storage import (
    S3NotConfiguredError,
    ensure_s3_configured,
    delete_object,
    generate_presigned_get_url,
    generate_presigned_put_url,
    head_object,
)
from app.db.database import get_db
from app.db.models.media import Media, MediaVisibility
from app.db.repositories.user_repository import UserRepository
from app.media.schemas import (
    MediaConfirmRequest,
    MediaDeleteResponse,
    MediaPresignRequest,
    MediaPresignResponse,
    MediaURLResponse,
)

router = APIRouter(prefix="/media", tags=["media"])
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def _ensure_media_storage_ready() -> None:
    try:
        ensure_s3_configured()
    except S3NotConfiguredError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Storage de media no configurado ({exc}).",
        ) from exc


def _normalize_content_type(content_type: str) -> str:
    return content_type.split(";")[0].strip().lower()


def _validate_media_size(content_type: str, size_bytes: int) -> None:
    normalized = _normalize_content_type(content_type)
    if normalized.startswith("image/"):
        max_bytes = settings.MEDIA_MAX_IMAGE_MB * 1024 * 1024
    elif normalized.startswith("video/"):
        max_bytes = settings.MEDIA_MAX_VIDEO_MB * 1024 * 1024
    else:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido.")

    if size_bytes <= 0:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")

    if size_bytes > max_bytes:
        raise HTTPException(status_code=400, detail="Archivo supera el tamaño permitido.")


def _build_object_key(user_id: int, visibility: MediaVisibility, filename: str | None) -> str:
    ext = ""
    if filename:
        ext = Path(filename).suffix.lower()
        if len(ext) > 10:
            ext = ""
    return f"{visibility.value}/{user_id}/{uuid4().hex}{ext}"


def _get_user_from_token(token: str | None, db: Session):
    if not token:
        return None
    try:
        payload = decode_token(token)
        if payload.get("typ") != "access":
            return None
        user_id = int(payload["sub"])
    except Exception:
        return None

    repo = UserRepository(db)
    user = repo.get_user_by_id(user_id)
    if not user or not user.is_active:
        return None
    return user


@router.post("/presign/upload", response_model=MediaPresignResponse)
def presign_upload(
    payload: MediaPresignRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()
    _validate_media_size(payload.content_type, payload.size_bytes)

    object_key = _build_object_key(
        user_id=current.user_number,
        visibility=payload.visibility,
        filename=payload.filename,
    )

    media = Media(
        owner_id=current.user_number,
        visibility=payload.visibility,
        status="pending",
        bucket=settings.S3_BUCKET,
        object_key=object_key,
        original_filename=payload.filename,
        mime_type=_normalize_content_type(payload.content_type),
        size_bytes=payload.size_bytes,
    )

    db.add(media)
    db.flush()

    expires_in = settings.MEDIA_UPLOAD_EXPIRE_MINUTES * 60
    try:
        upload_url = generate_presigned_put_url(
            key=object_key,
            content_type=_normalize_content_type(payload.content_type),
            expires_in=expires_in,
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="No se pudo generar URL de subida.")

    db.commit()
    db.refresh(media)

    return MediaPresignResponse(
        media_id=media.id,
        object_key=object_key,
        upload_url=upload_url,
        expires_in=expires_in,
        required_headers={"Content-Type": _normalize_content_type(payload.content_type)},
    )


@router.post("/confirm", response_model=MediaURLResponse)
def confirm_upload(
    payload: MediaConfirmRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()
    media = db.query(Media).filter(Media.id == payload.media_id).one_or_none()
    if not media:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if media.owner_id != current.user_number:
        raise HTTPException(status_code=403, detail="No autorizado.")

    try:
        head = head_object(key=media.object_key)
    except ClientError:
        raise HTTPException(status_code=400, detail="Archivo no encontrado en storage.")

    content_type = head.get("ContentType") or media.mime_type
    if not content_type:
        raise HTTPException(status_code=400, detail="No se pudo detectar el tipo de archivo.")

    size_bytes = int(head.get("ContentLength") or media.size_bytes or 0)
    _validate_media_size(content_type, size_bytes)

    media.size_bytes = size_bytes
    media.mime_type = _normalize_content_type(content_type)
    media.status = "ready"

    if payload.title is not None:
        media.title = payload.title
    if payload.text is not None:
        media.text = payload.text
    if payload.published_at is not None:
        media.published_at = payload.published_at
    if payload.duration_seconds is not None:
        media.duration_seconds = payload.duration_seconds
    if payload.width is not None:
        media.width = payload.width
    if payload.height is not None:
        media.height = payload.height

    db.commit()

    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    url = generate_presigned_get_url(key=media.object_key, expires_in=expires_in)
    return MediaURLResponse(media_id=media.id, url=url, expires_in=expires_in)


@router.get("/{media_id}", response_model=MediaURLResponse)
def get_media_url(
    media_id: int,
    token: str | None = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()
    media = db.query(Media).filter(Media.id == media_id).one_or_none()
    if not media:
        raise HTTPException(status_code=404, detail="Media no encontrada.")

    if media.status != "ready":
        raise HTTPException(status_code=409, detail="Media aún no disponible.")

    if media.visibility == MediaVisibility.private:
        user = _get_user_from_token(token, db)
        if not user or media.owner_id != user.id:
            raise HTTPException(status_code=403, detail="No autorizado.")

    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    url = generate_presigned_get_url(key=media.object_key, expires_in=expires_in)
    return MediaURLResponse(media_id=media.id, url=url, expires_in=expires_in)


@router.delete("/{media_id}", response_model=MediaDeleteResponse)
def delete_media(
    media_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()
    media = db.query(Media).filter(Media.id == media_id).one_or_none()
    if not media:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if media.owner_id != current.user_number:
        raise HTTPException(status_code=403, detail="No autorizado.")

    try:
        delete_object(key=media.object_key)
    except ClientError:
        raise HTTPException(status_code=500, detail="No se pudo eliminar el objeto.")

    db.delete(media)
    db.commit()
    return MediaDeleteResponse(deleted=True)
