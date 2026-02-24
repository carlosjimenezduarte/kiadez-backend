from pathlib import Path
from uuid import uuid4

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.auth.routes import get_current_user
from app.auth.models import UserPublic
from app.core.config import settings
from app.core.security import decode_token
from app.core.storage import (
    S3NotConfiguredError,
    get_s3_client,
    ensure_s3_configured,
    delete_object,
    generate_presigned_get_url,
    generate_presigned_put_url,
    head_object,
)
from app.db.database import get_db
from app.db.models.media import Media, MediaVisibility
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.media.schemas import (
    CoverPhotoResponse,
    CoverPhotoSetRequest,
    MediaConfirmRequest,
    MediaDeleteResponse,
    MediaImageOption,
    MediaImageOptionListResponse,
    MediaPresignRequest,
    MediaPresignResponse,
    MediaURLResponse,
    ProfilePhotoResponse,
    ProfilePhotoSetRequest,
)

router = APIRouter(prefix="/media", tags=["media"])
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

COVER_OFFSET_LIMIT = 4000


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


def _build_object_key(
    *,
    user_id: int,
    visibility: MediaVisibility,
    filename: str | None,
    obfuscate_owner: bool = False,
) -> str:
    ext = ""
    if filename:
        ext = Path(filename).suffix.lower()
        if len(ext) > 10:
            ext = ""
    if obfuscate_owner:
        # Avoid embedding user identifiers in the object key. Useful for zero-knowledge / E2EE objects.
        return f"{visibility.value}/{uuid4().hex}{ext}"
    return f"{visibility.value}/{user_id}/{uuid4().hex}{ext}"


def _iter_streaming_body(body, *, chunk_size: int = 1024 * 1024):
    try:
        while True:
            chunk = body.read(chunk_size)
            if not chunk:
                break
            yield chunk
    finally:
        try:
            body.close()
        except Exception:
            pass


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


def _clamp_cover_offset(value: int | None) -> int:
    normalized = int(value or 0)
    if normalized < -COVER_OFFSET_LIMIT:
        return -COVER_OFFSET_LIMIT
    if normalized > COVER_OFFSET_LIMIT:
        return COVER_OFFSET_LIMIT
    return normalized


def _cover_photo_response_for_user(
    *,
    user: User,
    current_user_id: int,
    db: Session,
    allow_cleanup: bool = False,
) -> CoverPhotoResponse:
    offset_x = _clamp_cover_offset(user.cover_photo_offset_x)
    offset_y = _clamp_cover_offset(user.cover_photo_offset_y)

    media_id = int(user.cover_photo_media_id) if user.cover_photo_media_id is not None else None
    if media_id is None:
        return CoverPhotoResponse(offset_x=offset_x, offset_y=offset_y)

    media = db.query(Media).filter(Media.id == media_id).one_or_none()
    if media is None:
        if allow_cleanup:
            user.cover_photo_media_id = None
            db.commit()
        return CoverPhotoResponse(offset_x=offset_x, offset_y=offset_y)

    if media.owner_id != int(user.id):
        if allow_cleanup:
            user.cover_photo_media_id = None
            db.commit()
        return CoverPhotoResponse(offset_x=offset_x, offset_y=offset_y)

    if media.status != "ready":
        return CoverPhotoResponse(offset_x=offset_x, offset_y=offset_y)

    if not (media.mime_type or "").lower().startswith("image/"):
        if allow_cleanup:
            user.cover_photo_media_id = None
            db.commit()
        return CoverPhotoResponse(offset_x=offset_x, offset_y=offset_y)

    if media.visibility == MediaVisibility.private and int(current_user_id) != int(user.id):
        return CoverPhotoResponse(offset_x=offset_x, offset_y=offset_y)

    _ensure_media_storage_ready()
    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    url = generate_presigned_get_url(key=media.object_key, expires_in=expires_in)
    return CoverPhotoResponse(
        media_id=media.id,
        url=url,
        offset_x=offset_x,
        offset_y=offset_y,
        expires_in=expires_in,
    )


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
        obfuscate_owner=bool(payload.obfuscate_owner),
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


@router.post("/upload/proxy", response_model=MediaURLResponse)
async def upload_proxy(
    media_id: int = Form(...),
    file: UploadFile = File(...),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Upload via backend (no browser->S3 CORS required). Intended for E2EE "rocks" (ciphertext) uploads.
    Workflow:
    1) Client calls /media/presign/upload to register Media and obtain media_id (and object_key).
    2) Client encrypts bytes locally.
    3) Client POSTs ciphertext bytes here with media_id.
    """
    _ensure_media_storage_ready()

    media = db.query(Media).filter(Media.id == media_id).one_or_none()
    if not media:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if media.owner_id != current.user_number:
        raise HTTPException(status_code=403, detail="No autorizado.")
    if media.status != "pending":
        raise HTTPException(status_code=409, detail="Media no está en estado pendiente.")

    # Keep the content-type that was registered in DB (caller provided it on /presign/upload).
    content_type = _normalize_content_type(media.mime_type or file.content_type or "")
    if not content_type:
        raise HTTPException(status_code=400, detail="No se pudo detectar el tipo de archivo.")

    content = await file.read()
    size_bytes = len(content)
    _validate_media_size(content_type, size_bytes)

    try:
        client = get_s3_client()
        client.put_object(
            Bucket=settings.S3_BUCKET,
            Key=media.object_key,
            Body=content,
            ContentType=content_type,
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="No se pudo subir la imagen al storage.")

    media.size_bytes = size_bytes
    media.mime_type = content_type
    media.status = "ready"
    db.commit()

    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    url = generate_presigned_get_url(key=media.object_key, expires_in=expires_in)
    return MediaURLResponse(media_id=media.id, url=url, expires_in=expires_in)


@router.get("/{media_id}/raw")
def download_media_raw(
    media_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Proxy media bytes through the backend (no bucket CORS needed).
    Useful for client-side decryption (E2EE) where JS needs access to bytes.
    """
    _ensure_media_storage_ready()
    media = db.query(Media).filter(Media.id == media_id).one_or_none()
    if not media:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if media.status != "ready":
        raise HTTPException(status_code=409, detail="Media aún no disponible.")

    if media.visibility == MediaVisibility.private and media.owner_id != current.user_number:
        raise HTTPException(status_code=403, detail="No autorizado.")

    try:
        client = get_s3_client()
        obj = client.get_object(Bucket=settings.S3_BUCKET, Key=media.object_key)
        body = obj["Body"]
    except ClientError:
        raise HTTPException(status_code=404, detail="Archivo no encontrado en storage.")
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo descargar el archivo.")

    # It's ciphertext for E2EE use cases, but keeping the stored mime_type is harmless for fetch().
    return StreamingResponse(
        _iter_streaming_body(body),
        media_type=media.mime_type or "application/octet-stream",
        headers={"Cache-Control": "no-store"},
    )


@router.post("/upload/direct", response_model=MediaURLResponse)
async def upload_direct(
    file: UploadFile = File(...),
    visibility: MediaVisibility = Form(default=MediaVisibility.private),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()

    content_type = _normalize_content_type(file.content_type or "")
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes en esta subida.")

    content = await file.read()
    size_bytes = len(content)
    _validate_media_size(content_type, size_bytes)

    object_key = _build_object_key(
        user_id=current.user_number,
        visibility=visibility,
        filename=file.filename,
    )

    media = Media(
        owner_id=current.user_number,
        visibility=visibility,
        status="pending",
        bucket=settings.S3_BUCKET,
        object_key=object_key,
        original_filename=file.filename,
        mime_type=content_type,
        size_bytes=size_bytes,
    )
    db.add(media)
    db.flush()

    try:
        client = get_s3_client()
        client.put_object(
            Bucket=settings.S3_BUCKET,
            Key=object_key,
            Body=content,
            ContentType=content_type,
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="No se pudo subir la imagen al storage.")

    media.status = "ready"
    db.commit()
    db.refresh(media)

    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    url = generate_presigned_get_url(key=media.object_key, expires_in=expires_in)
    return MediaURLResponse(media_id=media.id, url=url, expires_in=expires_in)


@router.get("/mine/images", response_model=MediaImageOptionListResponse)
def list_my_images(
    limit: int = Query(default=24, ge=1, le=100),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()
    medias = (
        db.query(Media)
        .filter(Media.owner_id == current.user_number)
        .filter(Media.status == "ready")
        .filter(Media.mime_type.like("image/%"))
        .order_by(Media.created_at.desc())
        .limit(limit)
        .all()
    )
    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    return MediaImageOptionListResponse(
        items=[
            MediaImageOption(
                media_id=media.id,
                url=generate_presigned_get_url(key=media.object_key, expires_in=expires_in),
                created_at=media.created_at,
                original_filename=media.original_filename,
            )
            for media in medias
        ],
        expires_in=expires_in,
    )


@router.get("/profile-photo", response_model=ProfilePhotoResponse)
def get_profile_photo(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current.user_number).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if user.profile_photo_media_id is None:
        return ProfilePhotoResponse()

    media = db.query(Media).filter(Media.id == user.profile_photo_media_id).one_or_none()
    if not media:
        user.profile_photo_media_id = None
        db.commit()
        return ProfilePhotoResponse()
    if media.owner_id != current.user_number:
        return ProfilePhotoResponse()
    if media.status != "ready":
        return ProfilePhotoResponse()
    if not (media.mime_type or "").lower().startswith("image/"):
        return ProfilePhotoResponse()

    _ensure_media_storage_ready()
    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    url = generate_presigned_get_url(key=media.object_key, expires_in=expires_in)
    return ProfilePhotoResponse(media_id=media.id, url=url, expires_in=expires_in)


@router.post("/profile-photo", response_model=ProfilePhotoResponse)
def set_profile_photo(
    payload: ProfilePhotoSetRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current.user_number).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    if payload.media_id is None:
        user.profile_photo_media_id = None
        db.commit()
        return ProfilePhotoResponse()

    media = db.query(Media).filter(Media.id == payload.media_id).one_or_none()
    if not media:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if media.owner_id != current.user_number:
        raise HTTPException(status_code=403, detail="No autorizado.")
    if media.status != "ready":
        raise HTTPException(status_code=409, detail="Media aún no disponible.")
    if not (media.mime_type or "").lower().startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo puedes asignar imágenes.")

    user.profile_photo_media_id = media.id
    db.commit()

    _ensure_media_storage_ready()
    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    url = generate_presigned_get_url(key=media.object_key, expires_in=expires_in)
    return ProfilePhotoResponse(media_id=media.id, url=url, expires_in=expires_in)


@router.get("/cover-photo", response_model=CoverPhotoResponse)
def get_cover_photo(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current.user_number).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return _cover_photo_response_for_user(
        user=user,
        current_user_id=int(current.user_number),
        db=db,
        allow_cleanup=True,
    )


@router.post("/cover-photo", response_model=CoverPhotoResponse)
def set_cover_photo(
    payload: CoverPhotoSetRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current.user_number).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    user.cover_photo_offset_x = _clamp_cover_offset(payload.offset_x)
    user.cover_photo_offset_y = _clamp_cover_offset(payload.offset_y)

    if payload.media_id is None:
        user.cover_photo_media_id = None
        db.commit()
        return CoverPhotoResponse(
            media_id=None,
            url=None,
            offset_x=int(user.cover_photo_offset_x or 0),
            offset_y=int(user.cover_photo_offset_y or 0),
            expires_in=0,
        )

    media = db.query(Media).filter(Media.id == payload.media_id).one_or_none()
    if not media:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if media.owner_id != current.user_number:
        raise HTTPException(status_code=403, detail="No autorizado.")
    if media.status != "ready":
        raise HTTPException(status_code=409, detail="Media aún no disponible.")
    if not (media.mime_type or "").lower().startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo puedes asignar imágenes.")

    user.cover_photo_media_id = media.id
    db.commit()
    db.refresh(user)

    return _cover_photo_response_for_user(
        user=user,
        current_user_id=int(current.user_number),
        db=db,
        allow_cleanup=True,
    )


@router.get("/cover-photo/user/{user_id}", response_model=CoverPhotoResponse)
def get_user_cover_photo(
    user_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == int(user_id), User.is_active.is_(True)).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    is_owner = int(user.id) == int(current.user_number)
    if not is_owner and not bool(user.public_profile_show_cover_purposes):
        return CoverPhotoResponse()

    return _cover_photo_response_for_user(
        user=user,
        current_user_id=int(current.user_number),
        db=db,
        allow_cleanup=is_owner,
    )


@router.get("/emblem", response_model=ProfilePhotoResponse)
def get_emblem(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current.user_number).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if user.emblem_media_id is None:
        return ProfilePhotoResponse()

    media = db.query(Media).filter(Media.id == user.emblem_media_id).one_or_none()
    if not media:
        user.emblem_media_id = None
        db.commit()
        return ProfilePhotoResponse()
    if media.owner_id != current.user_number:
        return ProfilePhotoResponse()
    if media.status != "ready":
        return ProfilePhotoResponse()
    if not (media.mime_type or "").lower().startswith("image/"):
        return ProfilePhotoResponse()

    _ensure_media_storage_ready()
    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    url = generate_presigned_get_url(key=media.object_key, expires_in=expires_in)
    return ProfilePhotoResponse(media_id=media.id, url=url, expires_in=expires_in)


@router.post("/emblem", response_model=ProfilePhotoResponse)
def set_emblem(
    payload: ProfilePhotoSetRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == current.user_number).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    if payload.media_id is None:
        user.emblem_media_id = None
        db.commit()
        return ProfilePhotoResponse()

    media = db.query(Media).filter(Media.id == payload.media_id).one_or_none()
    if not media:
        raise HTTPException(status_code=404, detail="Media no encontrada.")
    if media.owner_id != current.user_number:
        raise HTTPException(status_code=403, detail="No autorizado.")
    if media.status != "ready":
        raise HTTPException(status_code=409, detail="Media aún no disponible.")
    if not (media.mime_type or "").lower().startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo puedes asignar imágenes.")

    user.emblem_media_id = media.id
    db.commit()

    _ensure_media_storage_ready()
    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    url = generate_presigned_get_url(key=media.object_key, expires_in=expires_in)
    return ProfilePhotoResponse(media_id=media.id, url=url, expires_in=expires_in)


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
