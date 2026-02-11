from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.config import settings
from app.core.storage import S3NotConfiguredError, generate_presigned_get_url
from app.db.database import get_db
from app.db.models.media import Media
from app.db.models.post import (
    Post,
    PostComment,
    PostMediaKind,
    PostReport,
    PostReportReason,
    PostStar,
    PostVisibility,
)
from app.db.models.user import User
from app.posts.schemas import (
    MyPostStatsOut,
    PostAuthorOut,
    PostCommentCreateRequest,
    PostCommentOut,
    PostCreateRequest,
    PostDeleteResponse,
    PostOut,
    PostReportCreateRequest,
    PostReportResponse,
    PostShareResponse,
    PostStarResponse,
)

router = APIRouter(prefix="/posts", tags=["posts"])


def _author_out(user: User) -> PostAuthorOut:
    full_name = f"{user.first_name} {user.last_name}".strip()
    return PostAuthorOut(
        id=user.id,
        name=full_name,
        role=user.role,
        guardian_rank=user.guardian_rank,
    )


def _ensure_post_access(post: Post, current_user_id: int) -> None:
    if post.visibility == PostVisibility.private and post.author_id != current_user_id:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")


def _build_media_url(post: Post, media_map: dict[int, Media]) -> str | None:
    if post.media_id is None:
        return None
    media = media_map.get(post.media_id)
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


def _post_out(
    *,
    post: Post,
    author: User,
    is_mine: bool,
    starred_by_me: bool,
    media_url: str | None,
) -> PostOut:
    return PostOut(
        id=post.id,
        author=_author_out(author),
        text=post.text,
        visibility=post.visibility,
        media_id=post.media_id,
        media_kind=post.media_kind,
        media_url=media_url,
        star_count=post.star_count,
        comment_count=post.comment_count,
        share_count=post.share_count,
        starred_by_me=starred_by_me,
        is_mine=is_mine,
        created_at=post.created_at,
    )


@router.get("/feed", response_model=list[PostOut])
def get_feed(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user_id = current.user_number

    stmt = (
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(
            (Post.visibility == PostVisibility.public)
            | (Post.author_id == current_user_id)
        )
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    rows = db.execute(stmt).all()

    if not rows:
        return []

    post_ids = [row[0].id for row in rows]
    media_ids = [row[0].media_id for row in rows if row[0].media_id is not None]

    starred_ids: set[int] = set()
    if post_ids:
        starred_rows = db.execute(
            select(PostStar.post_id).where(
                PostStar.user_id == current_user_id,
                PostStar.post_id.in_(post_ids),
            )
        ).all()
        starred_ids = {row[0] for row in starred_rows}

    media_map: dict[int, Media] = {}
    if media_ids:
        media_rows = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {media.id: media for media in media_rows}

    result: list[PostOut] = []
    for post, author in rows:
        result.append(
            _post_out(
                post=post,
                author=author,
                is_mine=post.author_id == current_user_id,
                starred_by_me=post.id in starred_ids,
                media_url=_build_media_url(post, media_map),
            )
        )
    return result


@router.get("/me/stats", response_model=MyPostStatsOut)
def my_post_stats(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    me = db.execute(select(User).where(User.id == current.user_number)).scalar_one()
    posts_total = db.execute(
        select(func.count(Post.id)).where(Post.author_id == current.user_number)
    ).scalar_one()
    return MyPostStatsOut(
        my_received_stars_total=me.received_stars_total or 0,
        my_posts_total=posts_total or 0,
    )


@router.post("", response_model=PostOut)
def create_post(
    payload: PostCreateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    text = (payload.text or "").strip() or None
    media: Media | None = None

    if payload.media_id is not None:
        media = db.execute(select(Media).where(Media.id == payload.media_id)).scalar_one_or_none()
        if media is None:
            raise HTTPException(status_code=404, detail="Media no encontrada.")
        if media.owner_id != current.user_number:
            raise HTTPException(status_code=403, detail="No autorizado para usar esta media.")
        if media.status != "ready":
            raise HTTPException(status_code=409, detail="Media aún no disponible.")

    media_kind = payload.media_kind
    if media and media_kind is None and media.mime_type:
        mime = media.mime_type.lower()
        if mime.startswith("image/"):
            media_kind = PostMediaKind.image
        elif mime.startswith("video/"):
            media_kind = PostMediaKind.video

    post = Post(
        author_id=current.user_number,
        text=text,
        visibility=payload.visibility,
        media_id=payload.media_id,
        media_kind=media_kind,
        star_count=0,
        comment_count=0,
        share_count=0,
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    author = db.execute(select(User).where(User.id == current.user_number)).scalar_one()
    media_map = {media.id: media} if media else {}
    return _post_out(
        post=post,
        author=author,
        is_mine=True,
        starred_by_me=False,
        media_url=_build_media_url(post, media_map),
    )


@router.delete("/{post_id}", response_model=PostDeleteResponse)
def delete_post(
    post_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    if post.author_id != current.user_number:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar esta publicación.")

    removed_stars = post.star_count or 0
    db.delete(post)

    me = db.execute(select(User).where(User.id == current.user_number)).scalar_one()
    me.received_stars_total = max(0, (me.received_stars_total or 0) - removed_stars)

    db.commit()
    return PostDeleteResponse(deleted=True, removed_stars=removed_stars)


@router.post("/{post_id}/stars", response_model=PostStarResponse)
def donate_star(
    post_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    _ensure_post_access(post, current.user_number)

    if post.author_id == current.user_number:
        raise HTTPException(status_code=400, detail="No puedes donarte estrellas a ti mismo.")

    db.add(PostStar(post_id=post_id, user_id=current.user_number))
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya donaste una estrella a esta publicación. La donación es irreversible.",
        )

    post.star_count = (post.star_count or 0) + 1
    author = db.execute(select(User).where(User.id == post.author_id)).scalar_one()
    author.received_stars_total = (author.received_stars_total or 0) + 1
    db.commit()

    return PostStarResponse(starred=True, post_id=post.id, star_count=post.star_count)


@router.post("/{post_id}/share", response_model=PostShareResponse)
def share_post(
    post_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    _ensure_post_access(post, current.user_number)

    post.share_count = (post.share_count or 0) + 1
    db.commit()
    return PostShareResponse(shared=True, post_id=post.id, share_count=post.share_count)


@router.get("/{post_id}/comments", response_model=list[PostCommentOut])
def list_comments(
    post_id: int,
    limit: int = Query(default=100, ge=1, le=300),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    _ensure_post_access(post, current.user_number)

    rows = db.execute(
        select(PostComment, User)
        .join(User, User.id == PostComment.user_id)
        .where(PostComment.post_id == post_id)
        .order_by(PostComment.created_at.asc())
        .offset(offset)
        .limit(limit)
    ).all()

    return [
        PostCommentOut(
            id=comment.id,
            post_id=comment.post_id,
            author=_author_out(author),
            text=comment.text,
            created_at=comment.created_at,
        )
        for comment, author in rows
    ]


@router.post("/{post_id}/comments", response_model=PostCommentOut)
def create_comment(
    post_id: int,
    payload: PostCommentCreateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    _ensure_post_access(post, current.user_number)

    comment = PostComment(
        post_id=post.id,
        user_id=current.user_number,
        text=payload.text.strip(),
    )
    db.add(comment)
    post.comment_count = (post.comment_count or 0) + 1
    db.commit()
    db.refresh(comment)

    author = db.execute(select(User).where(User.id == current.user_number)).scalar_one()
    return PostCommentOut(
        id=comment.id,
        post_id=comment.post_id,
        author=_author_out(author),
        text=comment.text,
        created_at=comment.created_at,
    )


@router.post("/{post_id}/reports", response_model=PostReportResponse)
def report_post(
    post_id: int,
    payload: PostReportCreateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    _ensure_post_access(post, current.user_number)
    if post.author_id == current.user_number:
        raise HTTPException(status_code=400, detail="No puedes reportar tu propia publicación.")

    report = PostReport(
        post_id=post.id,
        reporter_id=current.user_number,
        reason=payload.reason,
        other_reason=(payload.other_reason or "").strip() or None,
    )
    db.add(report)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya reportaste esta publicación.")

    return PostReportResponse(reported=True, post_id=post.id, reason=payload.reason)
