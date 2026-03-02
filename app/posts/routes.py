from __future__ import annotations

from datetime import datetime, timezone
import re

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from sqlalchemy import and_, delete, func, or_, select, tuple_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.minor_accreditation import is_minor_protected
from app.auth.models import UserPublic
from app.auth.routes import get_current_user
from app.core.config import settings
from app.core.i18n import locale_from_request, tr as i18n_tr
from app.core.storage import S3NotConfiguredError, generate_presigned_get_url
from app.db.database import get_db
from app.db.models.media import Media
from app.db.models.post import (
    Hashtag,
    Post,
    PostComment,
    PostHashtag,
    PostMediaKind,
    PostMention,
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
    PostSearchHashtagOut,
    PostSearchOut,
    PostSearchUserOut,
    PostUpdateTextRequest,
    PostMentionOut,
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
    ("astral_1a", "Illumination", 1, "/css/AKI/Astral/Star1/1a.webp"),
    ("astral_1b", "Stellar", 5, "/css/AKI/Astral/Star1/1b.webp"),
    ("astral_1c", "Astral", 10, "/css/AKI/Astral/Star1/1c.webp"),
    ("astral_1d", "Star Collector", 30, "/css/AKI/Astral/Star1/1d.webp"),
    ("astral_1e", "Astronomer", 100, "/css/AKI/Astral/Star1/1e.webp"),
    ("astral_2a", "Sky Cartographer", 200, "/css/AKI/Astral/Star2/2a.webp"),
    ("astral_2b", "Skywatcher", 300, "/css/AKI/Astral/Star2/2b.webp"),
    ("astral_2c", "Constellation Weaver", 500, "/css/AKI/Astral/Star2/2c.webp"),
    ("astral_2d", "Celestial Chronicler", 800, "/css/AKI/Astral/Star2/2d.webp"),
    ("astral_2e", "Star Interpreter", 1000, "/css/AKI/Astral/Star2/2e.webp"),
    ("astral_3a", "Constellation Architect", 1500, "/css/AKI/Astral/Star3/3a.webp"),
    ("astral_3b", "Guardian of the Night Sky", 2000, "/css/AKI/Astral/Star3/3b.webp"),
    ("astral_3c", "Sage of the Firmament", 2500, "/css/AKI/Astral/Star3/3c.webp"),
    ("astral_3d", "Astral Navigator", 3000, "/css/AKI/Astral/Star3/3d.webp"),
    ("astral_3e", "Keeper of the Light", 4000, "/css/AKI/Astral/Star3/3e.webp"),
    ("astral_4a", "Stellar Herald", 5000, "/css/AKI/Astral/Star4/4a.webp"),
    ("astral_4b", "Lord of Constellations", 10000, "/css/AKI/Astral/Star4/4b.webp"),
    ("astral_4c", "Master of the Deep Sky", 20000, "/css/AKI/Astral/Star4/4c.webp"),
    ("astral_4d", "Orchestrator of Stars", 30000, "/css/AKI/Astral/Star4/4d.webp"),
    ("astral_4e", "Regent of the Firmament", 50000, "/css/AKI/Astral/Star4/4e.webp"),
    ("astral_5a", "Forger of Universes", 70000, "/css/AKI/Astral/Star5/5a.webp"),
    ("astral_5b", "Bearer of the Sky", 100000, "/css/AKI/Astral/Star5/5b.webp"),
    ("astral_5c", "Sovereign of the Stars", 150000, "/css/AKI/Astral/Star5/5c.webp"),
    ("astral_5d", "Architect of the Cosmos", 200000, "/css/AKI/Astral/Star5/5d.webp"),
    ("astral_5e", "Sentinel of Infinity", 300000, "/css/AKI/Astral/Star5/5e.webp"),
    ("astral_6a", "Child of the Cosmos", 600000, "/css/AKI/Astral/Star6/6a.webp"),
    ("astral_6b", "Stellar Consciousness", 1000000, "/css/AKI/Astral/Star6/6b.webp"),
    ("astral_6c", "Soul of the Firmament", 1500000, "/css/AKI/Astral/Star6/6c.webp"),
    ("astral_6d", "Throne of the Stars", 2000000, "/css/AKI/Astral/Star6/6d.webp"),
    ("astral_6e", "Eternal Star", 5000000, "/css/AKI/Astral/Star6/6e.webp"),
]

DONATION_STAR_ACHIEVEMENTS: list[tuple[str, str, int, str]] = [
    ("donation_1", "Explorer of Mystery", 1000, "/css/AKI/Donation/1.webp"),
    ("donation_2", "Trusting the Universe", 5000, "/css/AKI/Donation/2.webp"),
    ("donation_3", "Believer in Nebulae", 10000, "/css/AKI/Donation/3.webp"),
    ("donation_4", "Guardian of Stellar Flow", 20000, "/css/AKI/Donation/4.webp"),
    ("donation_5", "Bearer of the Fertile Void", 50000, "/css/AKI/Donation/5.webp"),
    ("donation_6", "Keeper of the Common Pool", 100000, "/css/AKI/Donation/6.webp"),
    ("donation_7", "Constellation Weaver", 200000, "/css/AKI/Donation/7.webp"),
    ("donation_8", "Voice of Cosmic Silence", 300000, "/css/AKI/Donation/8.webp"),
    ("donation_9", "Architect of the Common Good", 500000, "/css/AKI/Donation/9.webp"),
    ("donation_10", "Seed of Infinity", 1000000, "/css/AKI/Donation/10.webp"),
]

MENTION_PATTERN = re.compile(r"(?<![A-Za-z0-9._])@([A-Za-z0-9._]{4,30})(?![A-Za-z0-9._])")
HASHTAG_PATTERN = re.compile(r"(?<![A-Za-z0-9_])#([A-Za-z0-9_]{2,50})(?![A-Za-z0-9_])")


def _locale(request: Request | None) -> str:
    return locale_from_request(request, default="en")


def _td(locale: str, en: str, **fmt: object) -> str:
    translations: dict[str, tuple[str, str]] = {
        "Could not tag: {users}.": (
            "No se pudo etiquetar a: {users}.",
            "Impossible de taguer : {users}.",
        ),
        "You can only tag users with mutual follow status. Please review: {users}.": (
            "Solo puedes etiquetar usuarios con seguimiento mutuo. Revisa: {users}.",
            "Vous ne pouvez taguer que des utilisateurs avec suivi mutuel. Vérifiez : {users}.",
        ),
        "Post not found.": ("Publicación no encontrada.", "Publication introuvable."),
        "This account is in protected mode and its public posts are not available.": (
            "Esta cuenta está en modo protegido y sus publicaciones públicas no están disponibles.",
            "Ce compte est en mode protégé et ses publications publiques ne sont pas disponibles.",
        ),
        "This account is in protected mode and does not expose public posts.": (
            "Esta cuenta está en modo protegido y no expone publicaciones públicas.",
            "Ce compte est en mode protégé et n'expose pas de publications publiques.",
        ),
        "This profile personal posts are hidden for privacy.": (
            "Las publicaciones personales de este perfil están ocultas por privacidad.",
            "Les publications personnelles de ce profil sont masquées pour des raisons de confidentialité.",
        ),
        "Type text to search.": ("Escribe texto para buscar.", "Saisissez du texte à rechercher."),
        "User not found.": ("Usuario no encontrado.", "Utilisateur introuvable."),
        "Media not found.": ("Medio no encontrado.", "Média introuvable."),
        "Not authorized to use this media.": ("No autorizado para usar este medio.", "Non autorisé à utiliser ce média."),
        "Media not available yet.": ("El medio aún no está disponible.", "Le média n'est pas encore disponible."),
        "Not authorized to edit this post.": (
            "No autorizado para editar esta publicación.",
            "Non autorisé à modifier cette publication.",
        ),
        "Post text cannot be empty.": (
            "El texto de la publicación no puede estar vacío.",
            "Le texte de la publication ne peut pas être vide.",
        ),
        "Not authorized to delete this post.": (
            "No autorizado para eliminar esta publicación.",
            "Non autorisé à supprimer cette publication.",
        ),
        "You cannot donate stars to yourself.": (
            "No puedes donar estrellas a ti mismo.",
            "Vous ne pouvez pas donner des étoiles à vous-même.",
        ),
        "You already donated a star to this post. Donation is irreversible.": (
            "Ya donaste una estrella a esta publicación. La donación es irreversible.",
            "Vous avez déjà donné une étoile à cette publication. Le don est irréversible.",
        ),
        "You cannot report your own post.": (
            "No puedes reportar tu propia publicación.",
            "Vous ne pouvez pas signaler votre propre publication.",
        ),
        "You already reported this post.": (
            "Ya reportaste esta publicación.",
            "Vous avez déjà signalé cette publication.",
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


def _extract_mentions_from_text(text: str | None) -> list[tuple[str, int, int]]:
    if not text:
        return []
    matches: list[tuple[str, int, int]] = []
    for match in MENTION_PATTERN.finditer(text):
        username = (match.group(1) or "").strip().lower()
        if not username:
            continue
        matches.append((username, int(match.start()), int(match.end())))
    return matches


def _normalize_search_query(raw: str | None) -> str:
    value = re.sub(r"\s+", " ", str(raw or "").strip())
    return value


def _normalize_hashtag_query(raw: str | None) -> str:
    value = str(raw or "").strip().lower()
    while value.startswith("#"):
        value = value[1:]
    if not value:
        return ""
    return re.sub(r"[^a-z0-9_]", "", value)


def _extract_hashtags_from_text(text: str | None) -> list[str]:
    if not text:
        return []
    hashtags: list[str] = []
    seen: set[str] = set()
    for match in HASHTAG_PATTERN.finditer(text):
        tag = (match.group(1) or "").strip().lower()
        if not tag or tag in seen:
            continue
        seen.add(tag)
        hashtags.append(tag)
    return hashtags


def _attach_post_hashtags(
    *,
    db: Session,
    post_id: int,
    text: str | None,
) -> None:
    tags = _extract_hashtags_from_text(text)
    if not tags:
        return

    existing_rows = db.execute(select(Hashtag).where(Hashtag.tag.in_(tags))).scalars().all()
    existing_by_tag = {str(row.tag).strip().lower(): row for row in existing_rows}

    missing_tags = [tag for tag in tags if tag not in existing_by_tag]
    if missing_tags:
        db.add_all([Hashtag(tag=tag) for tag in missing_tags])
        db.flush()
        refreshed_rows = db.execute(select(Hashtag).where(Hashtag.tag.in_(missing_tags))).scalars().all()
        for row in refreshed_rows:
            existing_by_tag[str(row.tag).strip().lower()] = row

    for tag in tags:
        hashtag = existing_by_tag.get(tag)
        if hashtag is None:
            continue
        db.add(PostHashtag(post_id=int(post_id), hashtag_id=int(hashtag.id)))


def _search_users(
    *,
    db: Session,
    query_text: str,
    limit: int,
) -> list[PostSearchUserOut]:
    normalized_query = _normalize_search_query(query_text).lower()
    if not normalized_query:
        return []

    search_like = f"%{normalized_query}%"
    rows = db.execute(
        select(User).where(
            User.is_active.is_(True),
            User.username.is_not(None),
            User.username != "",
            or_(
                func.lower(User.username).like(search_like),
                func.lower(
                    func.concat(
                        func.coalesce(User.first_name, ""),
                        " ",
                        func.coalesce(User.last_name, ""),
                    )
                ).like(search_like),
            ),
        )
        .order_by(func.lower(User.username).asc(), User.id.asc())
        .limit(max(1, int(limit)))
    ).scalars().all()

    return [
        PostSearchUserOut(
            user_id=int(user.id),
            full_name=f"{(user.first_name or '').strip()} {(user.last_name or '').strip()}".strip() or f"User {user.id}",
            username=(user.username or "").strip() or None,
            handle=_build_handle(username=(user.username or "").strip() or None, user_id=int(user.id)),
            profile_url=_build_profile_url((user.username or "").strip() or None, user_id=int(user.id)),
        )
        for user in rows
    ]


def _search_hashtags(
    *,
    db: Session,
    current_user_id: int,
    hashtag_prefix: str,
    limit: int,
) -> list[PostSearchHashtagOut]:
    normalized_prefix = _normalize_hashtag_query(hashtag_prefix)
    filters = [
        User.is_active.is_(True),
        or_(
            Post.author_id == int(current_user_id),
            and_(
                Post.visibility == PostVisibility.public,
                User.public_profile_show_personal_posts.is_(True),
            ),
        ),
    ]
    if normalized_prefix:
        filters.append(func.lower(Hashtag.tag).like(f"{normalized_prefix}%"))

    post_count_expr = func.count(func.distinct(Post.id))
    rows = db.execute(
        select(Hashtag.tag, post_count_expr)
        .join(PostHashtag, PostHashtag.hashtag_id == Hashtag.id)
        .join(Post, Post.id == PostHashtag.post_id)
        .join(User, User.id == Post.author_id)
        .where(*filters)
        .group_by(Hashtag.id, Hashtag.tag)
        .order_by(post_count_expr.desc(), Hashtag.tag.asc())
        .limit(max(1, int(limit)))
    ).all()

    return [
        PostSearchHashtagOut(
            tag=f"#{tag}",
            normalized_tag=tag,
            post_count=int(post_count),
            href=f"/feed.html?search=%23{tag}",
        )
        for tag, post_count in rows
    ]


def _search_posts_by_hashtag(
    *,
    db: Session,
    current_user_id: int,
    hashtag: str,
    limit: int,
) -> list[PostOut]:
    normalized_hashtag = _normalize_hashtag_query(hashtag)
    if not normalized_hashtag:
        return []

    stmt = (
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .join(PostHashtag, PostHashtag.post_id == Post.id)
        .join(Hashtag, Hashtag.id == PostHashtag.hashtag_id)
        .where(
            User.is_active.is_(True),
            Hashtag.tag == normalized_hashtag,
            or_(
                Post.author_id == int(current_user_id),
                and_(
                    Post.visibility == PostVisibility.public,
                    User.public_profile_show_personal_posts.is_(True),
                ),
            ),
        )
        .order_by(Post.created_at.desc())
        .limit(max(1, int(limit)))
    )
    return _query_posts(stmt=stmt, current_user_id=current_user_id, db=db)


def _resolve_post_mentions_payload(
    *,
    db: Session,
    author_id: int,
    text: str | None,
    locale: str,
) -> list[dict[str, int]]:
    extracted = _extract_mentions_from_text(text)
    if not extracted:
        return []

    usernames = sorted({item[0] for item in extracted if item[0]})
    users = db.execute(
        select(User).where(
            User.username.in_(usernames),
            User.is_active.is_(True),
        )
    ).scalars().all()
    user_by_username = {(user.username or "").strip().lower(): user for user in users if (user.username or "").strip()}

    missing = sorted({username for username in usernames if username not in user_by_username})
    if missing:
        formatted = ", ".join(f"@{item}" for item in missing[:5])
        suffix = "..." if len(missing) > 5 else ""
        raise HTTPException(
            status_code=400,
            detail=_td(locale, "Could not tag: {users}.", users=f"{formatted}{suffix}"),
        )

    mentioned_user_ids = sorted({int(user_by_username[username].id) for username in usernames})
    outgoing_rows = db.execute(
        select(UserFollow.followed_id).where(
            UserFollow.follower_id == int(author_id),
            UserFollow.followed_id.in_(mentioned_user_ids),
        )
    ).all()
    outgoing_ids = {int(row[0]) for row in outgoing_rows}

    incoming_rows = db.execute(
        select(UserFollow.follower_id).where(
            UserFollow.followed_id == int(author_id),
            UserFollow.follower_id.in_(mentioned_user_ids),
        )
    ).all()
    incoming_ids = {int(row[0]) for row in incoming_rows}

    mutual_ids = outgoing_ids & incoming_ids
    disallowed_usernames = sorted(
        username
        for username in usernames
        if int(user_by_username[username].id) not in mutual_ids
    )
    if disallowed_usernames:
        formatted = ", ".join(f"@{item}" for item in disallowed_usernames[:5])
        suffix = "..." if len(disallowed_usernames) > 5 else ""
        raise HTTPException(
            status_code=400,
            detail=_td(
                locale,
                "You can only tag users with mutual follow status. Please review: {users}.",
                users=f"{formatted}{suffix}",
            ),
        )

    mentions_payload: list[dict[str, int]] = []
    for username, start_index, end_index in extracted:
        user = user_by_username[username]
        mentions_payload.append(
            {
                "mentioned_user_id": int(user.id),
                "start_index": int(start_index),
                "end_index": int(end_index),
            }
        )
    return mentions_payload



def _publication_achievement_description(threshold: int) -> str:
    return f"You reached {threshold:,} stars from your posts".replace(",", ".")


def _donation_achievement_description(threshold: int) -> str:
    base = f"You accumulated a donation of more than {threshold:,} stars to the Common Star Pool"
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


def _ensure_post_access(post: Post, current_user_id: int, locale: str) -> None:
    if post.visibility == PostVisibility.private and post.author_id != current_user_id:
        raise HTTPException(status_code=404, detail=_td(locale, "Post not found."))


def _ensure_author_posts_visibility(author: User, viewer_user_id: int, locale: str) -> None:
    if int(author.id) == int(viewer_user_id):
        return
    if is_minor_protected(author):
        raise HTTPException(
            status_code=403,
            detail=_td(locale, "This account is in protected mode and its public posts are not available."),
        )
    if not bool(author.public_profile_show_personal_posts):
        raise HTTPException(
            status_code=403,
            detail=_td(locale, "This profile personal posts are hidden for privacy."),
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


def _load_post_mentions_by_post_id(
    *,
    db: Session,
    posts_by_id: dict[int, Post],
) -> dict[int, list[PostMentionOut]]:
    post_ids = sorted(int(post_id) for post_id in posts_by_id.keys())
    if not post_ids:
        return {}

    mention_rows = db.execute(
        select(PostMention, User)
        .join(User, User.id == PostMention.mentioned_user_id)
        .where(PostMention.post_id.in_(post_ids))
        .order_by(PostMention.post_id.asc(), PostMention.start_index.asc(), PostMention.id.asc())
    ).all()
    if not mention_rows:
        return {}

    relation_pairs: set[tuple[int, int]] = set()
    for mention, _mentioned_user in mention_rows:
        post = posts_by_id.get(int(mention.post_id))
        if post is None:
            continue
        author_id = int(post.author_id)
        mentioned_user_id = int(mention.mentioned_user_id)
        if author_id <= 0 or mentioned_user_id <= 0 or author_id == mentioned_user_id:
            continue
        relation_pairs.add((author_id, mentioned_user_id))
        relation_pairs.add((mentioned_user_id, author_id))

    follow_edges: set[tuple[int, int]] = set()
    if relation_pairs:
        follow_rows = db.execute(
            select(UserFollow.follower_id, UserFollow.followed_id).where(
                tuple_(UserFollow.follower_id, UserFollow.followed_id).in_(list(relation_pairs))
            )
        ).all()
        follow_edges = {(int(follower_id), int(followed_id)) for follower_id, followed_id in follow_rows}

    mentions_by_post_id: dict[int, list[PostMentionOut]] = {}
    for mention, mentioned_user in mention_rows:
        post_id = int(mention.post_id)
        post = posts_by_id.get(post_id)
        if post is None:
            continue

        author_id = int(post.author_id)
        mentioned_user_id = int(mention.mentioned_user_id)
        is_active = (
            bool(mentioned_user.is_active)
            and author_id != mentioned_user_id
            and (author_id, mentioned_user_id) in follow_edges
            and (mentioned_user_id, author_id) in follow_edges
        )

        username = (mentioned_user.username or "").strip() or None
        mentions_by_post_id.setdefault(post_id, []).append(
            PostMentionOut(
                mentioned_user_id=mentioned_user_id,
                username=username,
                handle=_build_handle(username=username, user_id=mentioned_user_id),
                profile_url=_build_profile_url(username, user_id=mentioned_user_id),
                start_index=max(0, int(mention.start_index)),
                end_index=max(1, int(mention.end_index)),
                is_active=is_active,
            )
        )

    return mentions_by_post_id


def _post_out(
    *,
    post: Post,
    author: User,
    is_mine: bool,
    starred_by_me: bool,
    media_url: str | None,
    album_name: str | None = None,
    mentions: list[PostMentionOut] | None = None,
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
        mentions=mentions or [],
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

    posts_by_id = {int(post.id): post for post, _author in rows}
    mentions_map = _load_post_mentions_by_post_id(db=db, posts_by_id=posts_by_id)

    result: list[PostOut] = []
    for post, author in rows:
        if int(post.author_id) != int(current_user_id) and is_minor_protected(author):
            continue
        result.append(
            _post_out(
                post=post,
                author=author,
                is_mine=post.author_id == current_user_id,
                starred_by_me=post.id in starred_ids,
                media_url=_build_media_url(post, media_map),
                album_name=album_name_map.get(int(post.album_id)) if post.album_id is not None else None,
                mentions=mentions_map.get(int(post.id), []),
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


@router.get("/search", response_model=PostSearchOut)
def search_posts_and_people(
    request: Request,
    q: str = Query(..., min_length=1, max_length=80),
    user_limit: int = Query(default=8, ge=1, le=20),
    hashtag_limit: int = Query(default=10, ge=1, le=20),
    post_limit: int = Query(default=40, ge=1, le=100),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    normalized_query = _normalize_search_query(q)
    if not normalized_query:
        raise HTTPException(status_code=400, detail=_td(locale, "Type text to search."))

    normalized_user_query = normalized_query
    while normalized_user_query.startswith("@"):
        normalized_user_query = normalized_user_query[1:]
    normalized_user_query = _normalize_search_query(normalized_user_query)

    hashtag = _normalize_hashtag_query(normalized_query) if normalized_query.startswith("#") else ""
    query_type = "hashtag" if hashtag else "mixed"

    users: list[PostSearchUserOut] = []
    if normalized_user_query:
        users = _search_users(
            db=db,
            query_text=normalized_user_query,
            limit=user_limit,
        )

    hashtag_prefix = hashtag or _normalize_hashtag_query(normalized_user_query)
    hashtags = _search_hashtags(
        db=db,
        current_user_id=int(current.user_number),
        hashtag_prefix=hashtag_prefix,
        limit=hashtag_limit,
    )

    posts: list[PostOut] = []
    if hashtag:
        posts = _search_posts_by_hashtag(
            db=db,
            current_user_id=int(current.user_number),
            hashtag=hashtag,
            limit=post_limit,
        )

    return PostSearchOut(
        query=normalized_query,
        query_type=query_type,
        hashtag=f"#{hashtag}" if hashtag else None,
        users=users,
        hashtags=hashtags,
        posts=posts,
    )


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
    request: Request,
    user_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    current_user_id = current.user_number
    target = db.execute(
        select(User).where(
            User.id == user_id,
            User.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    is_owner = int(user_id) == int(current_user_id)
    if not is_owner and is_minor_protected(target):
        raise HTTPException(
            status_code=403,
            detail=_td(locale, "This account is in protected mode and does not expose public posts."),
        )
    if not is_owner and not bool(target.public_profile_show_personal_posts):
        raise HTTPException(
            status_code=403,
            detail=_td(locale, "This profile personal posts are hidden for privacy."),
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
    request: Request,
    payload: PostCreateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    author = db.execute(
        select(User).where(User.id == current.user_number, User.is_active.is_(True))
    ).scalar_one_or_none()
    if author is None:
        raise HTTPException(status_code=404, detail=_td(locale, "User not found."))

    text = (payload.text or "").strip() or None
    media: Media | None = None

    if payload.media_id is not None:
        media = db.execute(select(Media).where(Media.id == payload.media_id)).scalar_one_or_none()
        if media is None:
            raise HTTPException(status_code=404, detail=_td(locale, "Media not found."))
        if media.owner_id != current.user_number:
            raise HTTPException(status_code=403, detail=_td(locale, "Not authorized to use this media."))
        if media.status != "ready":
            raise HTTPException(status_code=409, detail=_td(locale, "Media not available yet."))

    media_kind = payload.media_kind
    if media and media_kind is None and media.mime_type:
        mime = media.mime_type.lower()
        if mime.startswith("image/"):
            media_kind = PostMediaKind.image
        elif mime.startswith("video/"):
            media_kind = PostMediaKind.video

    effective_visibility = payload.visibility
    if is_minor_protected(author):
        effective_visibility = PostVisibility.private

    mentions_payload = _resolve_post_mentions_payload(
        db=db,
        author_id=int(current.user_number),
        text=text,
        locale=locale,
    )

    post = Post(
        author_id=current.user_number,
        text=text,
        visibility=effective_visibility,
        media_id=payload.media_id,
        media_kind=media_kind,
        star_count=0,
        comment_count=0,
        share_count=0,
    )
    db.add(post)
    db.flush()

    for mention in mentions_payload:
        db.add(
            PostMention(
                post_id=int(post.id),
                mentioned_user_id=int(mention["mentioned_user_id"]),
                start_index=int(mention["start_index"]),
                end_index=int(mention["end_index"]),
            )
        )

    _attach_post_hashtags(
        db=db,
        post_id=int(post.id),
        text=text,
    )

    db.commit()
    db.refresh(post)

    media_map = {media.id: media} if media else {}
    mentions_map = _load_post_mentions_by_post_id(
        db=db,
        posts_by_id={int(post.id): post},
    )
    return _post_out(
        post=post,
        author=author,
        is_mine=True,
        starred_by_me=False,
        media_url=_build_media_url(post, media_map),
        album_name=None,
        mentions=mentions_map.get(int(post.id), []),
    )


@router.patch("/{post_id}", response_model=PostOut)
def update_post_text(
    request: Request,
    post_id: int,
    payload: PostUpdateTextRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Post not found."))

    post, author = row
    if int(post.author_id) != int(current.user_number):
        raise HTTPException(status_code=403, detail=_td(locale, "Not authorized to edit this post."))

    text = (payload.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail=_td(locale, "Post text cannot be empty."))

    post.text = text

    # Mentions and hashtags are derived from text and must stay in sync when text changes.
    db.execute(delete(PostMention).where(PostMention.post_id == int(post.id)))
    db.execute(delete(PostHashtag).where(PostHashtag.post_id == int(post.id)))

    mentions_payload = _resolve_post_mentions_payload(
        db=db,
        author_id=int(current.user_number),
        text=text,
        locale=locale,
    )
    for mention in mentions_payload:
        db.add(
            PostMention(
                post_id=int(post.id),
                mentioned_user_id=int(mention["mentioned_user_id"]),
                start_index=int(mention["start_index"]),
                end_index=int(mention["end_index"]),
            )
        )

    _attach_post_hashtags(
        db=db,
        post_id=int(post.id),
        text=text,
    )

    report_case = db.execute(
        select(PostReportCase).where(PostReportCase.post_id == int(post.id))
    ).scalar_one_or_none()
    if report_case is not None:
        report_case.post_text_snapshot = text
        report_case.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(post)

    media_map: dict[int, Media] = {}
    if post.media_id is not None:
        media = db.execute(select(Media).where(Media.id == int(post.media_id))).scalar_one_or_none()
        if media is not None:
            media_map[int(media.id)] = media

    mentions_map = _load_post_mentions_by_post_id(
        db=db,
        posts_by_id={int(post.id): post},
    )

    return _post_out(
        post=post,
        author=author,
        is_mine=True,
        starred_by_me=False,
        media_url=_build_media_url(post, media_map),
        album_name=None,
        mentions=mentions_map.get(int(post.id), []),
    )


@router.delete("/{post_id}", response_model=PostDeleteResponse)
def delete_post(
    request: Request,
    post_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    post = db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail=_td(locale, "Post not found."))
    if post.author_id != current.user_number:
        raise HTTPException(status_code=403, detail=_td(locale, "Not authorized to delete this post."))

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
    request: Request,
    post_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Post not found."))
    post, author = row
    _ensure_post_access(post, current.user_number, locale)
    _ensure_author_posts_visibility(author, current.user_number, locale)

    if post.author_id == current.user_number:
        raise HTTPException(status_code=400, detail=_td(locale, "You cannot donate stars to yourself."))

    db.add(PostStar(post_id=post_id, user_id=current.user_number))
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=_td(locale, "You already donated a star to this post. Donation is irreversible."),
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
    request: Request,
    post_id: int,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Post not found."))
    post, author = row
    _ensure_post_access(post, current.user_number, locale)
    _ensure_author_posts_visibility(author, current.user_number, locale)

    post.share_count = (post.share_count or 0) + 1
    db.commit()
    return PostShareResponse(shared=True, post_id=post.id, share_count=post.share_count)


@router.get("/{post_id}/comments", response_model=list[PostCommentOut])
def list_comments(
    request: Request,
    post_id: int,
    limit: int = Query(default=100, ge=1, le=300),
    offset: int = Query(default=0, ge=0),
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Post not found."))
    post, author = row
    _ensure_post_access(post, current.user_number, locale)
    _ensure_author_posts_visibility(author, current.user_number, locale)

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
    request: Request,
    post_id: int,
    payload: PostCommentCreateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Post not found."))
    post, author = row
    _ensure_post_access(post, current.user_number, locale)
    _ensure_author_posts_visibility(author, current.user_number, locale)

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
    request: Request,
    post_id: int,
    payload: PostReportCreateRequest,
    current: UserPublic = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = _locale(request)
    row = db.execute(
        select(Post, User)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
    ).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=_td(locale, "Post not found."))
    post, author = row
    _ensure_post_access(post, current.user_number, locale)
    _ensure_author_posts_visibility(author, current.user_number, locale)
    if post.author_id == current.user_number:
        raise HTTPException(status_code=400, detail=_td(locale, "You cannot report your own post."))

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
        raise HTTPException(status_code=409, detail=_td(locale, "You already reported this post."))

    return PostReportResponse(reported=True, post_id=post.id, reason=payload.reason)
