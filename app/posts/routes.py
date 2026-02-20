from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timezone

from sqlalchemy import func, or_, select, update
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
    PostReportCase,
    PostReportCaseStatus,
    PostReportReason,
    PostStar,
    PostVisibility,
)
from app.db.models.achievement_unlock_event import AchievementUnlockEvent
from app.db.models.gallery_folder import GalleryFolder
from app.db.models.user import User
from app.db.models.user_follow import UserFollow
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
    StarAchievementOut,
    StarPoolDonateResponse,
    StarPoolStateOut,
)

router = APIRouter(prefix="/posts", tags=["posts"])

PUBLICATION_STAR_ACHIEVEMENTS: list[tuple[str, str, int, str]] = [
    ("astral_1a", "Alumbramiento", 1, "/css/AKI/Astral/Star1/1a.webp"),
    ("astral_1b", "Estelar", 5, "/css/AKI/Astral/Star1/1b.webp"),
    ("astral_1c", "Astral", 10, "/css/AKI/Astral/Star1/1c.webp"),
    ("astral_1d", "Coleccionista de Estrellas", 30, "/css/AKI/Astral/Star1/1d.webp"),
    ("astral_1e", "Astrónomo", 100, "/css/AKI/Astral/Star1/1e.webp"),
    ("astral_2a", "Cartógrafo del Cielo", 200, "/css/AKI/Astral/Star2/2a.webp"),
    ("astral_2b", "Vigilante del Firmamento", 300, "/css/AKI/Astral/Star2/2b.webp"),
    ("astral_2c", "Tejedor de Constelaciones", 500, "/css/AKI/Astral/Star2/2c.webp"),
    ("astral_2d", "Cronista Celeste", 800, "/css/AKI/Astral/Star2/2d.webp"),
    ("astral_2e", "Intérprete de las Estrellas", 1000, "/css/AKI/Astral/Star2/2e.webp"),
    ("astral_3a", "Arquitecto de Constelaciones", 1500, "/css/AKI/Astral/Star3/3a.webp"),
    ("astral_3b", "Guardián del Cielo Nocturno", 2000, "/css/AKI/Astral/Star3/3b.webp"),
    ("astral_3c", "Sabio del Firmamento", 2500, "/css/AKI/Astral/Star3/3c.webp"),
    ("astral_3d", "Navegante Astral", 3000, "/css/AKI/Astral/Star3/3d.webp"),
    ("astral_3e", "Custodio de la Luz", 4000, "/css/AKI/Astral/Star3/3e.webp"),
    ("astral_4a", "Heraldo Estelar", 5000, "/css/AKI/Astral/Star4/4a.webp"),
    ("astral_4b", "Señor de las Constelaciones", 10000, "/css/AKI/Astral/Star4/4b.webp"),
    ("astral_4c", "Maestro del Cielo Profundo", 20000, "/css/AKI/Astral/Star4/4c.webp"),
    ("astral_4d", "Orquestador de Astros", 30000, "/css/AKI/Astral/Star4/4d.webp"),
    ("astral_4e", "Regente del Firmamento", 50000, "/css/AKI/Astral/Star4/4e.webp"),
    ("astral_5a", "Forjador de Universos", 70000, "/css/AKI/Astral/Star5/5a.webp"),
    ("astral_5b", "Portador del Cielo", 100000, "/css/AKI/Astral/Star5/5b.webp"),
    ("astral_5c", "Soberano de las Estrellas", 150000, "/css/AKI/Astral/Star5/5c.webp"),
    ("astral_5d", "Arquitecto del Cosmos", 200000, "/css/AKI/Astral/Star5/5d.webp"),
    ("astral_5e", "Vigía del Infinito", 300000, "/css/AKI/Astral/Star5/5e.webp"),
    ("astral_6a", "Hijo del Cosmos", 600000, "/css/AKI/Astral/Star6/6a.webp"),
    ("astral_6b", "Conciencia Estelar", 1000000, "/css/AKI/Astral/Star6/6b.webp"),
    ("astral_6c", "Alma del Firmamento", 1500000, "/css/AKI/Astral/Star6/6c.webp"),
    ("astral_6d", "Trono de las Estrellas", 2000000, "/css/AKI/Astral/Star6/6d.webp"),
    ("astral_6e", "Estrella Eterna", 5000000, "/css/AKI/Astral/Star6/6e.webp"),
]

DONATION_STAR_ACHIEVEMENTS: list[tuple[str, str, int, str]] = [
    ("donation_1", "Explorador del Misterio", 1000, "/css/AKI/Donation/1.webp"),
    ("donation_2", "Confiado en el Universo", 5000, "/css/AKI/Donation/2.webp"),
    ("donation_3", "Creyente de las Nebulosas", 10000, "/css/AKI/Donation/3.webp"),
    ("donation_4", "Guardián del Flujo Estelar", 20000, "/css/AKI/Donation/4.webp"),
    ("donation_5", "Portador del Vacío Fértil", 50000, "/css/AKI/Donation/5.webp"),
    ("donation_6", "Custodio del Fondo Común", 100000, "/css/AKI/Donation/6.webp"),
    ("donation_7", "Tejedor de Constelaciones", 200000, "/css/AKI/Donation/7.webp"),
    ("donation_8", "Voz del Silencio Cósmico", 300000, "/css/AKI/Donation/8.webp"),
    ("donation_9", "Arquitecto del Bien Común", 500000, "/css/AKI/Donation/9.webp"),
    ("donation_10", "Semilla del Infinito", 1000000, "/css/AKI/Donation/10.webp"),
]


def _publication_achievement_description(threshold: int) -> str:
    return f"Has alcanzado {threshold:,} estrellas por tus publicaciones".replace(",", ".")


def _donation_achievement_description(threshold: int) -> str:
    base = f"Has acumulado una donación de más de {threshold:,} estrellas al Fondo Común de Estrellas"
    return base.replace(",", ".")


def _newly_unlocked_thresholds(
    *,
    previous_total: int,
    current_total: int,
    definitions: list[tuple[str, str, int, str]],
) -> list[tuple[str, str, int, str]]:
    if current_total <= previous_total:
        return []
    return [
        (key, title, threshold, image_url)
        for key, title, threshold, image_url in definitions
        if previous_total < threshold <= current_total
    ]


def _record_achievement_unlock_events(
    *,
    db: Session,
    user_id: int,
    category: str,
    previous_total: int,
    current_total: int,
    definitions: list[tuple[str, str, int, str]],
    description_for_threshold,
) -> None:
    unlocked_defs = _newly_unlocked_thresholds(
        previous_total=previous_total,
        current_total=current_total,
        definitions=definitions,
    )
    if not unlocked_defs:
        return

    keys = [key for key, _, _, _ in unlocked_defs]
    existing_keys = set(
        db.execute(
            select(AchievementUnlockEvent.achievement_key).where(
                AchievementUnlockEvent.user_id == user_id,
                AchievementUnlockEvent.achievement_key.in_(keys),
            )
        ).scalars().all()
    )

    for key, title, threshold, image_url in unlocked_defs:
        if key in existing_keys:
            continue
        db.add(
            AchievementUnlockEvent(
                user_id=user_id,
                achievement_key=key,
                category=category,
                title=title,
                description=description_for_threshold(threshold),
                image_url=image_url,
            )
        )


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


def _ensure_author_posts_visibility(author: User, viewer_user_id: int) -> None:
    if int(author.id) == int(viewer_user_id):
        return
    if not bool(author.public_profile_show_personal_posts):
        raise HTTPException(
            status_code=403,
            detail="Las publicaciones personales de este perfil están ocultas por privacidad.",
        )


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
    album_name: str | None = None,
) -> PostOut:
    return PostOut(
        id=post.id,
        author=_author_out(author),
        text=post.text,
        visibility=post.visibility,
        media_id=post.media_id,
        media_kind=post.media_kind,
        media_url=media_url,
        album_id=post.album_id,
        album_name=album_name,
        star_count=post.star_count,
        comment_count=post.comment_count,
        share_count=post.share_count,
        starred_by_me=starred_by_me,
        is_mine=is_mine,
        created_at=post.created_at,
    )

def _query_posts(
    *,
    stmt,
    current_user_id: int,
    db: Session,
) -> list[PostOut]:
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
        starred_ids = {int(row[0]) for row in starred_rows}

    media_map: dict[int, Media] = {}
    if media_ids:
        media_rows = db.execute(select(Media).where(Media.id.in_(media_ids))).scalars().all()
        media_map = {int(media.id): media for media in media_rows}

    album_name_map: dict[int, str] = {}
    album_ids = [int(row[0].album_id) for row in rows if row[0].album_id is not None]
    if album_ids:
        album_rows = db.execute(
            select(GalleryFolder.id, GalleryFolder.name).where(GalleryFolder.id.in_(album_ids))
        ).all()
        album_name_map = {int(album_id): str(name) for album_id, name in album_rows}

    result: list[PostOut] = []
    for post, author in rows:
        result.append(
            _post_out(
                post=post,
                author=author,
                is_mine=post.author_id == current_user_id,
                starred_by_me=post.id in starred_ids,
                media_url=_build_media_url(post, media_map),
                album_name=album_name_map.get(int(post.album_id)) if post.album_id is not None else None,
            )
        )
    return result


def _normalized_star_totals(user: User) -> tuple[int, int]:
    received = max(0, int(user.received_stars_total or 0))
    donated = max(0, int(user.donated_stars_total or 0))
    donated = min(donated, received)
    return received, donated


def _build_achievements(
    *,
    current_total: int,
    definitions: list[tuple[str, str, int, str]],
) -> list[StarAchievementOut]:
    return [
        StarAchievementOut(
            key=key,
            title=title,
            threshold=threshold,
            image_url=image_url,
            unlocked=current_total >= threshold,
        )
        for key, title, threshold, image_url in definitions
    ]


def _build_star_pool_state(*, user: User, db: Session) -> StarPoolStateOut:
    received, donated = _normalized_star_totals(user)
    common_pool_total = int(
        db.execute(select(func.coalesce(func.sum(User.donated_stars_total), 0))).scalar_one()
        or 0
    )

    publication_achievements = _build_achievements(
        current_total=received,
        definitions=PUBLICATION_STAR_ACHIEVEMENTS,
    )
    donation_achievements = _build_achievements(
        current_total=donated,
        definitions=DONATION_STAR_ACHIEVEMENTS,
    )

    return StarPoolStateOut(
        my_received_stars_total=received,
        my_donated_stars_total=donated,
        my_donatable_stars_total=max(0, received - donated),
        common_pool_stars_total=max(0, common_pool_total),
        unlocked_publication_achievements=sum(1 for item in publication_achievements if item.unlocked),
        unlocked_donation_achievements=sum(1 for item in donation_achievements if item.unlocked),
        publication_achievements=publication_achievements,
        donation_achievements=donation_achievements,
    )


@router.get("/feed", response_model=list[PostOut])
def get_feed(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user_id = current.user_number
    following_ids = (
        db.execute(
            select(UserFollow.followed_id).where(UserFollow.follower_id == current_user_id)
        )
        .scalars()
        .all()
    )
    following_ids = [int(user_id) for user_id in following_ids]
    author_ids = set(following_ids)
    author_ids.add(int(current_user_id))

    stmt = (
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(
            Post.visibility == PostVisibility.public,
            User.is_active.is_(True),
            Post.author_id.in_(author_ids),
            or_(
                Post.author_id == current_user_id,
                User.public_profile_show_personal_posts.is_(True),
            ),
        )
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return _query_posts(stmt=stmt, current_user_id=current_user_id, db=db)


@router.get("/mine", response_model=list[PostOut])
def list_my_posts(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user_id = current.user_number
    stmt = (
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.author_id == current_user_id)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return _query_posts(stmt=stmt, current_user_id=current_user_id, db=db)


@router.get("/user/{user_id}", response_model=list[PostOut])
def list_user_posts(
    user_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user_id = current.user_number
    target = db.execute(
        select(User).where(
            User.id == user_id,
            User.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    is_owner = int(user_id) == int(current_user_id)
    if not is_owner and not bool(target.public_profile_show_personal_posts):
        raise HTTPException(
            status_code=403,
            detail="Las publicaciones personales de este perfil están ocultas por privacidad.",
        )

    filters = [Post.author_id == user_id]
    if not is_owner:
        filters.append(Post.visibility == PostVisibility.public)

    stmt = (
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(*filters)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return _query_posts(stmt=stmt, current_user_id=current_user_id, db=db)


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


@router.get("/star-pool", response_model=StarPoolStateOut)
def star_pool_state(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    me = db.execute(select(User).where(User.id == current.user_number)).scalar_one()
    return _build_star_pool_state(user=me, db=db)


@router.post("/star-pool/donate", response_model=StarPoolDonateResponse)
def donate_stars_to_pool(
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    me = db.execute(select(User).where(User.id == current.user_number)).scalar_one()
    received, donated = _normalized_star_totals(me)
    previous_donated_total = donated

    if donated != (me.donated_stars_total or 0):
        me.donated_stars_total = donated

    donated_now = max(0, received - donated)
    me.donated_stars_total = received

    _record_achievement_unlock_events(
        db=db,
        user_id=me.id,
        category="donation_stars",
        previous_total=previous_donated_total,
        current_total=received,
        definitions=DONATION_STAR_ACHIEVEMENTS,
        description_for_threshold=_donation_achievement_description,
    )

    db.commit()
    db.refresh(me)

    return StarPoolDonateResponse(
        donated_now=donated_now,
        state=_build_star_pool_state(user=me, db=db),
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
        album_name=None,
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

    report_case = db.execute(
        select(PostReportCase).where(PostReportCase.post_id == post.id)
    ).scalar_one_or_none()

    if report_case is not None:
        now = datetime.now(timezone.utc)
        report_case.post_id = None
        report_case.status = PostReportCaseStatus.deleted
        report_case.resolved_at = now
        report_case.resolved_by_guardian_id = None
        report_case.updated_at = now
        db.execute(
            update(PostReport)
            .where(PostReport.case_id == report_case.id)
            .values(post_id=None)
        )

    removed_stars = post.star_count or 0
    db.delete(post)

    me = db.execute(select(User).where(User.id == current.user_number)).scalar_one()
    me.received_stars_total = max(0, (me.received_stars_total or 0) - removed_stars)
    if (me.donated_stars_total or 0) > me.received_stars_total:
        me.donated_stars_total = me.received_stars_total

    db.commit()
    return PostDeleteResponse(deleted=True, removed_stars=removed_stars)


@router.post("/{post_id}/stars", response_model=PostStarResponse)
def donate_star(
    post_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    post, author = row
    _ensure_post_access(post, current.user_number)
    _ensure_author_posts_visibility(author, current.user_number)

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
    previous_received_total = max(0, int(author.received_stars_total or 0))
    author.received_stars_total = previous_received_total + 1

    _record_achievement_unlock_events(
        db=db,
        user_id=author.id,
        category="publication_stars",
        previous_total=previous_received_total,
        current_total=author.received_stars_total,
        definitions=PUBLICATION_STAR_ACHIEVEMENTS,
        description_for_threshold=_publication_achievement_description,
    )

    db.commit()

    return PostStarResponse(starred=True, post_id=post.id, star_count=post.star_count)


@router.post("/{post_id}/share", response_model=PostShareResponse)
def share_post(
    post_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    post, author = row
    _ensure_post_access(post, current.user_number)
    _ensure_author_posts_visibility(author, current.user_number)

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
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    post, author = row
    _ensure_post_access(post, current.user_number)
    _ensure_author_posts_visibility(author, current.user_number)

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
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    post, author = row
    _ensure_post_access(post, current.user_number)
    _ensure_author_posts_visibility(author, current.user_number)

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
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada.")
    post, author = row
    _ensure_post_access(post, current.user_number)
    _ensure_author_posts_visibility(author, current.user_number)
    if post.author_id == current.user_number:
        raise HTTPException(status_code=400, detail="No puedes reportar tu propia publicación.")

    now = datetime.now(timezone.utc)
    report_case = db.execute(
        select(PostReportCase).where(PostReportCase.post_id == post.id)
    ).scalar_one_or_none()
    if report_case is None:
        report_case = PostReportCase(
            post_id=post.id,
            post_author_id=post.author_id,
            post_text_snapshot=post.text,
            post_media_id_snapshot=post.media_id,
            post_media_kind_snapshot=post.media_kind,
            status=PostReportCaseStatus.open,
            report_count=0,
            first_reported_at=now,
            last_reported_at=now,
        )
        db.add(report_case)
        db.flush()
    else:
        report_case.post_author_id = post.author_id
        report_case.post_text_snapshot = post.text
        report_case.post_media_id_snapshot = post.media_id
        report_case.post_media_kind_snapshot = post.media_kind
        if report_case.status != PostReportCaseStatus.open:
            report_case.status = PostReportCaseStatus.open
            report_case.resolved_at = None
            report_case.resolved_by_guardian_id = None
        report_case.updated_at = now

    report = PostReport(
        case_id=report_case.id,
        post_id=post.id,
        reporter_id=current.user_number,
        reason=payload.reason,
        other_reason=(payload.other_reason or "").strip() or None,
    )
    db.add(report)

    report_case.report_count = max(0, int(report_case.report_count or 0)) + 1
    if report_case.first_reported_at is None:
        report_case.first_reported_at = now
    report_case.last_reported_at = now

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya reportaste esta publicación.")

    return PostReportResponse(reported=True, post_id=post.id, reason=payload.reason)
