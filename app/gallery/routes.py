from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, func, or_, select
from sqlalchemy.orm import Session

from app.auth.minor_accreditation import is_minor_protected
from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.config import settings
from app.core.storage import (
    S3NotConfiguredError,
    ensure_s3_configured,
    generate_presigned_get_url,
)
from app.db.database import get_db
from app.db.models.gallery_folder import GalleryFolder
from app.db.models.gallery_folder_item import GalleryFolderItem
from app.db.models.media import Media
from app.db.models.post import Post, PostMediaKind, PostVisibility
from app.db.models.user import User
from app.gallery.schemas import (
    GalleryAlbumPublishInput,
    GalleryAlbumPublishOut,
    GalleryAlbumPublishedPostOut,
    GalleryFolderAssignImagesInput,
    GalleryFolderCreateInput,
    GalleryFolderDetailOut,
    GalleryFolderSummaryOut,
    GalleryFolderUpdateInput,
    GalleryImageOut,
    GalleryMineOut,
    GalleryOperationStatusOut,
)

router = APIRouter(prefix="/gallery", tags=["gallery"])


def _ensure_media_storage_ready() -> None:
    try:
        ensure_s3_configured()
    except S3NotConfiguredError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Storage de media no configurado ({exc}).",
        ) from exc


def _to_media_out(*, media: Media, expires_in: int) -> GalleryImageOut:
    mime = str(media.mime_type or "").lower()
    if mime.startswith("video/"):
        media_kind = "video"
    elif mime.startswith("image/"):
        media_kind = "image"
    else:
        media_kind = "unknown"

    return GalleryImageOut(
        media_id=int(media.id),
        url=generate_presigned_get_url(key=media.object_key, expires_in=expires_in),
        media_kind=media_kind,
        created_at=media.created_at,
        original_filename=media.original_filename,
    )


def _folder_image_count(*, db: Session, folder_id: int) -> int:
    value = db.execute(
        select(func.count(GalleryFolderItem.id)).where(GalleryFolderItem.folder_id == folder_id)
    ).scalar_one()
    return int(value or 0)


def _folder_cover_url(
    *,
    db: Session,
    folder_id: int,
    owner_id: int,
    expires_in: int,
) -> str | None:
    media = db.execute(
        select(Media)
        .join(GalleryFolderItem, GalleryFolderItem.media_id == Media.id)
        .where(GalleryFolderItem.folder_id == folder_id)
        .where(Media.owner_id == owner_id)
        .where(Media.status == "ready")
        .where(
            or_(
                Media.mime_type.like("image/%"),
                Media.mime_type.like("video/%"),
            )
        )
        .order_by(GalleryFolderItem.created_at.desc(), GalleryFolderItem.id.desc())
        .limit(1)
    ).scalar_one_or_none()
    if media is None:
        return None
    return generate_presigned_get_url(key=media.object_key, expires_in=expires_in)


def _folder_to_summary(
    *,
    db: Session,
    folder: GalleryFolder,
    owner_id: int,
    expires_in: int,
) -> GalleryFolderSummaryOut:
    return GalleryFolderSummaryOut(
        id=int(folder.id),
        name=folder.name,
        visibility=str(folder.visibility or "public"),
        is_published=folder.published_at is not None,
        published_at=folder.published_at,
        images_count=_folder_image_count(db=db, folder_id=int(folder.id)),
        cover_image_url=_folder_cover_url(
            db=db,
            folder_id=int(folder.id),
            owner_id=owner_id,
            expires_in=expires_in,
        ),
        created_at=folder.created_at,
        updated_at=folder.updated_at,
    )


def _load_folder(
    *,
    db: Session,
    owner_id: int,
    folder_id: int,
) -> GalleryFolder:
    folder = db.execute(
        select(GalleryFolder).where(
            GalleryFolder.id == folder_id,
            GalleryFolder.owner_id == owner_id,
        )
    ).scalar_one_or_none()
    if folder is None:
        raise HTTPException(status_code=404, detail="Carpeta no encontrada.")
    return folder


def _list_folder_images(
    *,
    db: Session,
    owner_id: int,
    folder_id: int,
    expires_in: int,
) -> list[GalleryImageOut]:
    medias = db.execute(
        select(Media)
        .join(GalleryFolderItem, GalleryFolderItem.media_id == Media.id)
        .where(GalleryFolderItem.folder_id == folder_id)
        .where(Media.owner_id == owner_id)
        .where(Media.status == "ready")
        .where(
            or_(
                Media.mime_type.like("image/%"),
                Media.mime_type.like("video/%"),
            )
        )
        .order_by(GalleryFolderItem.created_at.desc(), GalleryFolderItem.id.desc())
    ).scalars().all()
    return [_to_media_out(media=media, expires_in=expires_in) for media in medias]


def _folder_to_detail(
    *,
    db: Session,
    owner_id: int,
    folder: GalleryFolder,
    expires_in: int,
) -> GalleryFolderDetailOut:
    images = _list_folder_images(
        db=db,
        owner_id=owner_id,
        folder_id=int(folder.id),
        expires_in=expires_in,
    )
    return GalleryFolderDetailOut(
        id=int(folder.id),
        name=folder.name,
        visibility=str(folder.visibility or "public"),
        is_published=folder.published_at is not None,
        published_at=folder.published_at,
        images_count=len(images),
        cover_image_url=(images[0].url if images else None),
        created_at=folder.created_at,
        updated_at=folder.updated_at,
        images=images,
        expires_in=expires_in,
    )


def _find_duplicate_folder_name(
    *,
    db: Session,
    owner_id: int,
    folder_name: str,
    exclude_folder_id: int | None = None,
) -> GalleryFolder | None:
    query = (
        select(GalleryFolder)
        .where(GalleryFolder.owner_id == owner_id)
        .where(func.lower(GalleryFolder.name) == folder_name.lower())
    )
    if exclude_folder_id is not None:
        query = query.where(GalleryFolder.id != exclude_folder_id)
    return db.execute(query).scalar_one_or_none()


def _post_media_kind_from_mime(mime_type: str | None) -> PostMediaKind | None:
    mime = str(mime_type or "").lower()
    if mime.startswith("image/"):
        return PostMediaKind.image
    if mime.startswith("video/"):
        return PostMediaKind.video
    return None


@router.get("/mine", response_model=GalleryMineOut)
def get_my_gallery(
    recent_limit: int = Query(default=20, ge=1, le=40),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()

    owner_id = int(current.user_number)
    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600

    recent_medias = db.execute(
        select(Media)
        .where(Media.owner_id == owner_id)
        .where(Media.status == "ready")
        .where(Media.mime_type.like("image/%"))
        .order_by(Media.created_at.desc(), Media.id.desc())
        .limit(recent_limit)
    ).scalars().all()

    folders = db.execute(
        select(GalleryFolder)
        .where(GalleryFolder.owner_id == owner_id)
        .order_by(desc(GalleryFolder.updated_at), desc(GalleryFolder.id))
    ).scalars().all()

    return GalleryMineOut(
        recent_limit=recent_limit,
        recent_images=[_to_media_out(media=media, expires_in=expires_in) for media in recent_medias],
        folders=[
            _folder_to_summary(
                db=db,
                folder=folder,
                owner_id=owner_id,
                expires_in=expires_in,
            )
            for folder in folders
        ],
        expires_in=expires_in,
    )


@router.post(
    "/mine/folders",
    response_model=GalleryFolderSummaryOut,
    status_code=status.HTTP_201_CREATED,
)
def create_folder(
    payload: GalleryFolderCreateInput,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()

    owner_id = int(current.user_number)
    owner = db.execute(
        select(User).where(User.id == owner_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if owner is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    if _find_duplicate_folder_name(
        db=db,
        owner_id=owner_id,
        folder_name=payload.name,
    ):
        raise HTTPException(status_code=409, detail="Ya tienes una carpeta con ese nombre.")

    effective_visibility = "private" if is_minor_protected(owner) else payload.visibility

    folder = GalleryFolder(
        owner_id=owner_id,
        name=payload.name,
        visibility=effective_visibility,
    )
    db.add(folder)
    db.commit()
    db.refresh(folder)

    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    return _folder_to_summary(
        db=db,
        folder=folder,
        owner_id=owner_id,
        expires_in=expires_in,
    )


@router.patch("/mine/folders/{folder_id}", response_model=GalleryFolderSummaryOut)
def rename_folder(
    folder_id: int,
    payload: GalleryFolderUpdateInput,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()

    owner_id = int(current.user_number)
    folder = _load_folder(db=db, owner_id=owner_id, folder_id=folder_id)

    if _find_duplicate_folder_name(
        db=db,
        owner_id=owner_id,
        folder_name=payload.name,
        exclude_folder_id=int(folder.id),
    ):
        raise HTTPException(status_code=409, detail="Ya tienes una carpeta con ese nombre.")

    folder.name = payload.name
    folder.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(folder)

    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    return _folder_to_summary(
        db=db,
        folder=folder,
        owner_id=owner_id,
        expires_in=expires_in,
    )


@router.delete("/mine/folders/{folder_id}", response_model=GalleryOperationStatusOut)
def delete_folder(
    folder_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    owner_id = int(current.user_number)
    folder = _load_folder(db=db, owner_id=owner_id, folder_id=folder_id)
    db.delete(folder)
    db.commit()
    return GalleryOperationStatusOut(deleted=True)


@router.get("/mine/folders/{folder_id}", response_model=GalleryFolderDetailOut)
def get_folder_detail(
    folder_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()

    owner_id = int(current.user_number)
    folder = _load_folder(db=db, owner_id=owner_id, folder_id=folder_id)

    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    return _folder_to_detail(
        db=db,
        owner_id=owner_id,
        folder=folder,
        expires_in=expires_in,
    )


@router.post("/mine/folders/{folder_id}/items", response_model=GalleryFolderDetailOut)
def add_images_to_folder(
    folder_id: int,
    payload: GalleryFolderAssignImagesInput,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()

    owner_id = int(current.user_number)
    folder = _load_folder(db=db, owner_id=owner_id, folder_id=folder_id)

    medias = db.execute(
        select(Media)
        .where(Media.id.in_(payload.media_ids))
        .where(Media.owner_id == owner_id)
        .where(Media.status == "ready")
        .where(
            or_(
                Media.mime_type.like("image/%"),
                Media.mime_type.like("video/%"),
            )
        )
    ).scalars().all()
    valid_media_ids = {int(media.id) for media in medias}

    invalid_media_ids = [media_id for media_id in payload.media_ids if media_id not in valid_media_ids]
    if invalid_media_ids:
        invalid_list = ", ".join(str(media_id) for media_id in invalid_media_ids[:12])
        raise HTTPException(
            status_code=400,
            detail=f"Algunas imágenes no son válidas para esta carpeta: {invalid_list}.",
        )

    existing_ids = set(
        db.execute(
            select(GalleryFolderItem.media_id).where(
                GalleryFolderItem.folder_id == int(folder.id),
                GalleryFolderItem.media_id.in_(payload.media_ids),
            )
        ).scalars().all()
    )

    additions = 0
    for media_id in payload.media_ids:
        if media_id in existing_ids:
            continue
        db.add(GalleryFolderItem(folder_id=int(folder.id), media_id=media_id))
        additions += 1

    if additions > 0:
        folder.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(folder)

    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    return _folder_to_detail(
        db=db,
        owner_id=owner_id,
        folder=folder,
        expires_in=expires_in,
    )


@router.delete(
    "/mine/folders/{folder_id}/items/{media_id}",
    response_model=GalleryOperationStatusOut,
)
def remove_image_from_folder(
    folder_id: int,
    media_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    owner_id = int(current.user_number)
    folder = _load_folder(db=db, owner_id=owner_id, folder_id=folder_id)

    item = db.execute(
        select(GalleryFolderItem).where(
            GalleryFolderItem.folder_id == int(folder.id),
            GalleryFolderItem.media_id == media_id,
        )
    ).scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=404,
            detail="La imagen no pertenece a esta carpeta.",
        )

    db.delete(item)
    folder.updated_at = datetime.now(timezone.utc)
    db.commit()
    return GalleryOperationStatusOut(deleted=True)


@router.post(
    "/mine/albums/publish",
    response_model=GalleryAlbumPublishOut,
    status_code=status.HTTP_201_CREATED,
)
def publish_album(
    payload: GalleryAlbumPublishInput,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ensure_media_storage_ready()

    owner_id = int(current.user_number)
    owner = db.execute(
        select(User).where(User.id == owner_id, User.is_active.is_(True))
    ).scalar_one_or_none()
    if owner is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    if _find_duplicate_folder_name(
        db=db,
        owner_id=owner_id,
        folder_name=payload.name,
    ):
        raise HTTPException(status_code=409, detail="Ya tienes un álbum con ese nombre.")

    medias = db.execute(
        select(Media)
        .where(Media.id.in_(payload.media_ids))
        .where(Media.owner_id == owner_id)
        .where(Media.status == "ready")
        .where(
            or_(
                Media.mime_type.like("image/%"),
                Media.mime_type.like("video/%"),
            )
        )
    ).scalars().all()
    media_map = {int(media.id): media for media in medias}

    invalid_media_ids = [media_id for media_id in payload.media_ids if media_id not in media_map]
    if invalid_media_ids:
        invalid_list = ", ".join(str(media_id) for media_id in invalid_media_ids[:12])
        raise HTTPException(
            status_code=400,
            detail=f"Algunas media no son válidas para este álbum: {invalid_list}.",
        )

    ordered_medias = [media_map[media_id] for media_id in payload.media_ids if media_id in media_map]
    if not ordered_medias:
        raise HTTPException(
            status_code=400,
            detail="Debes adjuntar al menos una imagen o video listo para publicar.",
        )

    effective_visibility = "private" if is_minor_protected(owner) else payload.visibility

    published_at = datetime.now(timezone.utc)
    album = GalleryFolder(
        owner_id=owner_id,
        name=payload.name,
        visibility=effective_visibility,
        published_at=published_at,
    )
    db.add(album)
    db.flush()

    for media in ordered_medias:
        db.add(GalleryFolderItem(folder_id=int(album.id), media_id=int(media.id)))

    post_visibility = (
        PostVisibility.private
        if effective_visibility == "private"
        else PostVisibility.public
    )
    created_posts: list[tuple[Post, Media]] = []
    for media in ordered_medias:
        media_kind = _post_media_kind_from_mime(media.mime_type)
        if media_kind is None:
            continue
        post = Post(
            author_id=owner_id,
            text=None,
            visibility=post_visibility,
            media_id=int(media.id),
            media_kind=media_kind,
            album_id=int(album.id),
            star_count=0,
            comment_count=0,
            share_count=0,
        )
        db.add(post)
        db.flush()
        created_posts.append((post, media))

    album.updated_at = published_at
    db.commit()
    db.refresh(album)

    expires_in = settings.MEDIA_DOWNLOAD_EXPIRE_HOURS * 3600
    album_detail = _folder_to_detail(
        db=db,
        owner_id=owner_id,
        folder=album,
        expires_in=expires_in,
    )

    posts_out: list[GalleryAlbumPublishedPostOut] = []
    for post, media in created_posts:
        posts_out.append(
            GalleryAlbumPublishedPostOut(
                post_id=int(post.id),
                media_id=int(media.id),
                media_kind=str(post.media_kind.value if post.media_kind else "unknown"),
                media_url=generate_presigned_get_url(
                    key=media.object_key,
                    expires_in=expires_in,
                ),
            )
        )

    return GalleryAlbumPublishOut(album=album_detail, posts=posts_out)
