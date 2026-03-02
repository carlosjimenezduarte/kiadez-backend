<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { syncTopbarAvatar } from "../lib/topbarAvatar";
  import { getLocale } from "../lib/i18n";

  const API = "http://127.0.0.1:8000";
  const FEED_LIMIT = 40;
  const ORACLE_BACK_CARD_IMAGE = "/css/oracle/carta.webp";
  const DEFAULT_PROFILE_AVATAR = "/assets/avatar-default.jpg";
  const GUARDIANS_MIN_RANK = 3;
  const HASHTAG_PATTERN = /(^|[^A-Za-z0-9_])#([A-Za-z0-9_]{2,50})/g;
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

  let feedLoading = true;
  let feedError = "";
  let feedPosts = [];
  let displayPosts = [];
  let postActionBusyMap = {};
  let postsStatus = "";
  let postsStatusIsError = false;
  let minorProtectedState = null;
  let minorProtectedVisible = false;
  let minorProtectedCollapsed = false;
  let showMinorAccreditationModal = false;
  let minorAccreditationBusy = false;
  let minorAccreditationStatus = "";
  let minorAccreditationStatusIsError = false;
  let minorGuardianPhone = "";
  let minorGuardianEmail = "";
  let minorRelationship = "padre";
  let oracleLoading = true;
  let oracleError = "";
  let oracleHasSelection = false;
  let oracleLatestCardImage = ORACLE_BACK_CARD_IMAGE;
  let oracleLatestCardAlt = tr("Carta del Oráculo en reverso", "Oracle card back", "Dos de carte Oracle");
  let oracleLatestSummary = tr(
    "Conoce El Oráculo y elige tu primera carta para reflexionar sobre tu presente.",
    "Discover the Oracle and choose your first card to reflect on your present."
  );
  let sideProfileName = tr("Usuario Kiadez", "Kiadez User", "Utilisateur Kiadez");
  let sideProfileHandle = tr("@usuario", "@user", "@utilisateur");
  let sideProfileUrl = "/home_user.html";
  let sideProfileAvatarUrl = DEFAULT_PROFILE_AVATAR;
  let showGuardianPanel = false;
  let viewerProfileName = tr("Usuario Kiadez", "Kiadez User", "Utilisateur Kiadez");
  let viewerProfileAvatarUrl = DEFAULT_PROFILE_AVATAR;
  let feedSearchQuery = "";
  let feedSearchType = "mixed";
  let feedSearchHashtag = "";
  let feedSearchLoading = false;
  let feedSearchError = "";
  let feedSearchUsers = [];
  let feedSearchHashtags = [];
  let feedSearchPostsCount = 0;
  let composerSelectedFile = null;
  let selectedEditPostId = null;
  let editPostText = "";
  let editPostBusy = false;
  let selectedDeletePostId = null;
  let selectedReportPostId = null;
  let deletePostBusy = false;
  let reportPostBusy = false;
  let postReportReason = "violent";
  let postReportReasonOther = "";

  const getAccessToken = () =>
    localStorage.getItem("access_token") ||
    localStorage.getItem("kiadez_access_token") ||
    "";

  const parseResponseJson = async (response) => {
    try {
      return await response.json();
    } catch {
      return {};
    }
  };

  const readApiError = (payload, fallback = tr("Error inesperado.", "Unexpected error.", "Erreur inattendue.")) => {
    const detail = payload?.detail;
    if (typeof detail === "string" && detail.trim()) return detail.trim();
    if (Array.isArray(detail) && detail.length) {
      const first = detail[0];
      if (typeof first === "string" && first.trim()) return first.trim();
      if (first && typeof first === "object") {
        if (typeof first.msg === "string" && first.msg.trim()) return first.msg.trim();
        if (typeof first.message === "string" && first.message.trim()) return first.message.trim();
      }
    }
    if (detail && typeof detail === "object") {
      if (typeof detail.msg === "string" && detail.msg.trim()) return detail.msg.trim();
      if (typeof detail.message === "string" && detail.message.trim()) return detail.message.trim();
    }
    if (typeof payload?.message === "string" && payload.message.trim()) return payload.message.trim();
    return fallback;
  };

  const readUnknownError = (error, fallback = tr("Error inesperado.", "Unexpected error.", "Erreur inattendue.")) => {
    if (!error) return fallback;
    if (typeof error === "string" && error.trim()) return error.trim();
    if (error instanceof Error) {
      const fromError = readApiError({ detail: error.message }, "");
      if (fromError) return fromError;
    }
    if (typeof error === "object") {
      const parsed = readApiError(error, "");
      if (parsed) return parsed;
      if (typeof error?.message === "string" && error.message.trim()) return error.message.trim();
    }
    return fallback;
  };

  const normalizeUsername = (value) => {
    let normalized = String(value || "").trim().toLowerCase();
    while (normalized.startsWith("@")) normalized = normalized.slice(1);
    return normalized;
  };

  const normalizeSearchQuery = (value) =>
    String(value || "")
      .replace(/\s+/g, " ")
      .trim();

  const normalizeHashtag = (value) => {
    let normalized = normalizeSearchQuery(value).toLowerCase();
    while (normalized.startsWith("#")) normalized = normalized.slice(1);
    return normalized.replace(/[^a-z0-9_]/g, "");
  };

  const isHashtagSearchQuery = (value) => normalizeSearchQuery(value).startsWith("#");

  const readTopbarSearchQuery = () => {
    const params = new URLSearchParams(window.location.search);
    return normalizeSearchQuery(params.get("search"));
  };

  const buildFeedHashtagHref = (value) => {
    const hashtag = normalizeHashtag(value);
    if (!hashtag) return "/feed.html";
    return `/feed.html?search=%23${encodeURIComponent(hashtag)}`;
  };

  const buildProfileUrl = ({ userId = null, username = "" } = {}) => {
    const normalizedUsername = normalizeUsername(username);
    if (normalizedUsername) {
      return `/home_user.html?u=${encodeURIComponent(normalizedUsername)}`;
    }
    const normalizedUserId = Number(userId || 0);
    if (Number.isFinite(normalizedUserId) && normalizedUserId > 0) {
      return `/home_user.html?id=${encodeURIComponent(String(normalizedUserId))}`;
    }
    return "/home_user.html";
  };

  const resolveFeedTargetProfile = () => {
    const params = new URLSearchParams(window.location.search);
    const requestedIdRaw = params.get("id");
    const requestedId = Number(requestedIdRaw);
    const requestedUserId =
      Number.isFinite(requestedId) && requestedId > 0 ? requestedId : null;
    const requestedUsername = normalizeUsername(params.get("u"));

    if (requestedUserId || requestedUsername) {
      return {
        user_id: requestedUserId,
        username: requestedUsername || "",
      };
    }

    // Fallback: preserve profile context when arriving from another profile page.
    try {
      const referrerRaw = String(document.referrer || "").trim();
      if (!referrerRaw) {
        return { user_id: null, username: "" };
      }

      const referrerUrl = new URL(referrerRaw, window.location.origin);
      if (referrerUrl.origin !== window.location.origin) {
        return { user_id: null, username: "" };
      }

      const refIdRaw = referrerUrl.searchParams.get("id");
      const refId = Number(refIdRaw);
      const refUserId = Number.isFinite(refId) && refId > 0 ? refId : null;
      const refUsername = normalizeUsername(referrerUrl.searchParams.get("u"));

      return {
        user_id: refUserId,
        username: refUsername || "",
      };
    } catch {
      return { user_id: null, username: "" };
    }
  };

  const setSideProfileFromPayload = (payload) => {
    const fullName = String(payload?.full_name || "").trim();
    const handle = String(payload?.handle || "").trim();
    const profileUrl = String(payload?.profile_url || "").trim();
    const avatarUrl = String(payload?.avatar_url || "").trim();
    const username = normalizeUsername(payload?.username);
    const userId = Number(payload?.user_id || 0);

    sideProfileName = fullName || tr("Usuario Kiadez", "Kiadez User", "Utilisateur Kiadez");
    sideProfileHandle = handle || (username ? `@${username}` : tr("@usuario", "@user", "@utilisateur"));
    sideProfileUrl = profileUrl || buildProfileUrl({ userId, username });
    sideProfileAvatarUrl = avatarUrl || DEFAULT_PROFILE_AVATAR;
  };

  const setViewerProfileFromPayload = (payload) => {
    const fullName = String(payload?.full_name || "").trim();
    const avatarUrl = String(payload?.avatar_url || "").trim();
    viewerProfileName = fullName || tr("Usuario Kiadez", "Kiadez User", "Utilisateur Kiadez");
    viewerProfileAvatarUrl = avatarUrl || DEFAULT_PROFILE_AVATAR;
  };

  const fetchFollowProfile = async ({ userId = null, username = "" } = {}) => {
    const normalizedUserId = Number(userId || 0);
    const normalizedUsername = normalizeUsername(username);
    if (Number.isFinite(normalizedUserId) && normalizedUserId > 0) {
      const response = await apiFetch(`/follows/profile?user_id=${encodeURIComponent(String(normalizedUserId))}`);
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo cargar el perfil.", "Could not load the profile.", "Impossible de charger le profil.")));
      }
      return data;
    }
    if (normalizedUsername) {
      const response = await apiFetch(`/follows/profile?username=${encodeURIComponent(normalizedUsername)}`);
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo cargar el perfil.", "Could not load the profile.", "Impossible de charger le profil.")));
      }
      return data;
    }
    throw new Error(tr("Parámetros inválidos para perfil.", "Invalid profile parameters.", "Paramètres de profil invalides."));
  };

  const truncateText = (value, maxLength = 220) => {
    const normalized = String(value || "").replace(/\s+/g, " ").trim();
    if (!normalized) return "";
    if (normalized.length <= maxLength) return normalized;
    return `${normalized.slice(0, Math.max(1, maxLength - 1)).trimEnd()}…`;
  };

  const apiFetch = async (path, options = {}) => {
    const token = getAccessToken();
    if (!token) {
      window.location.href = "/login.html";
      throw new Error(tr("No hay sesión activa.", "There is no active session.", "Il n'y a pas de session active."));
    }

    const response = await fetch(`${API}${path}`, {
      ...options,
      headers: {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("kiadez_access_token");
      window.location.href = "/login.html";
      throw new Error(tr("Tu sesión expiró. Inicia sesión nuevamente.", "Your session has expired. Sign in again.", "Ta session a expiré. Connecte-toi de nouveau."));
    }

    return response;
  };

  const setPostsStatus = (message, isError = false) => {
    postsStatus = String(message || "").trim();
    postsStatusIsError = Boolean(isError);
  };

  const setMinorAccreditationStatus = (message, isError = false) => {
    minorAccreditationStatus = String(message || "").trim();
    minorAccreditationStatusIsError = Boolean(isError);
  };

  const minorStatusLabel = (status) => {
    if (status === "requested") return tr("Solicitud enviada a adulto responsable", "Request sent to responsible adult", "Demande envoyée à l'adulte responsable");
    if (status === "pending") return tr("Acreditación pendiente", "Accreditation pending", "Accréditation en attente");
    if (status === "approved") return tr("Cuenta acreditada", "Accredited account", "Compte accrédité");
    return "";
  };

  const applyMinorAccreditationPayload = (payload) => {
    minorProtectedState = payload || null;
    minorProtectedVisible = Boolean(payload?.is_minor_protected);
    if (!minorProtectedVisible) {
      showMinorAccreditationModal = false;
      return;
    }

    minorGuardianPhone = String(payload?.guardian_phone || "").trim();
    minorGuardianEmail = String(payload?.guardian_email || "").trim();
    const relationship = String(payload?.relationship || "padre").trim().toLowerCase();
    if (["padre", "madre", "tutor_legal", "adulto_responsable"].includes(relationship)) {
      minorRelationship = relationship;
    } else {
      minorRelationship = "padre";
    }
  };

  const loadMinorAccreditationStatus = async () => {
    try {
      const response = await apiFetch("/auth/minor-accreditation/status");
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(
          readApiError(data, tr("No se pudo cargar la acreditación de cuenta.", "Could not load account accreditation.", "Impossible de charger l'accréditation du compte."))
        );
      }
      applyMinorAccreditationPayload(data);
    } catch (error) {
      applyMinorAccreditationPayload(null);
      console.error(error);
    }
  };

  const toggleMinorProtectedPanel = () => {
    minorProtectedCollapsed = !minorProtectedCollapsed;
  };

  const openMinorAccreditationModal = () => {
    if (!minorProtectedVisible) return;
    setMinorAccreditationStatus("");
    showMinorAccreditationModal = true;
  };

  const closeMinorAccreditationModal = () => {
    showMinorAccreditationModal = false;
    setMinorAccreditationStatus("");
  };

  const submitMinorAccreditationRequest = async () => {
    const guardianPhone = String(minorGuardianPhone || "").trim();
    const guardianEmail = String(minorGuardianEmail || "").trim();
    const relationship = String(minorRelationship || "padre").trim().toLowerCase();

    if (!guardianPhone) {
      setMinorAccreditationStatus(
        tr("Debes registrar el teléfono del adulto responsable.", "You must enter the responsible adult's phone number.", "Tu dois saisir le téléphone de l'adulte responsable."),
        true
      );
      return;
    }
    if (!guardianEmail) {
      setMinorAccreditationStatus(
        tr("Debes registrar el correo del adulto responsable.", "You must enter the responsible adult's email.", "Tu dois saisir l'e-mail de l'adulte responsable."),
        true
      );
      return;
    }

    minorAccreditationBusy = true;
    setMinorAccreditationStatus("");

    try {
      const response = await apiFetch("/auth/minor-accreditation/request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          guardian_phone: guardianPhone,
          guardian_email: guardianEmail,
          relationship,
        }),
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo enviar la solicitud.", "Could not send the request.", "Impossible d'envoyer la demande.")));
      }

      await loadMinorAccreditationStatus();
      setMinorAccreditationStatus(
        data?.message ||
          tr(
            "Solicitud enviada. El adulto responsable debe aprobarla por correo.",
            "Request sent. The responsible adult must approve it by email."
          )
      );
    } catch (error) {
      setMinorAccreditationStatus(
        readUnknownError(error, tr("No se pudo enviar la solicitud.", "Could not send the request.", "Impossible d'envoyer la demande.")),
        true
      );
    } finally {
      minorAccreditationBusy = false;
    }
  };

  const relativeTime = (value) => {
    const date = new Date(value || "");
    if (Number.isNaN(date.getTime())) return "";

    const diffMs = Date.now() - date.getTime();
    const future = diffMs < 0;
    const absMs = Math.abs(diffMs);
    const minute = 60 * 1000;
    const hour = 60 * minute;
    const day = 24 * hour;

    const format = (num, unitEs, unitEn) => {
      const amount = Math.max(1, Math.floor(num));
      const unit = isEn || isFr ? unitEn : unitEs;
      const label = amount === 1 ? unit : `${unit}s`;
      return future
        ? isEn || isFr
          ? `in ${amount} ${label}`
          : `en ${amount} ${label}`
        : isEn || isFr
          ? `${amount} ${label} ago`
          : `hace ${amount} ${label}`;
    };

    if (absMs < minute) return future ? tr("en instantes", "in moments", "dans quelques instants") : tr("hace instantes", "moments ago", "il y a quelques instants");
    if (absMs < hour) return format(absMs / minute, "minuto", "minute");
    if (absMs < day) return format(absMs / hour, "hora", "hour");
    if (absMs < 7 * day) return format(absMs / day, "día", "day");

    return date.toLocaleString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const buildAuthorProfileUrl = (author) => {
    const authorId = Number(author?.id || 0);
    if (Number.isFinite(authorId) && authorId > 0) {
      return `/home_user.html?id=${encodeURIComponent(String(authorId))}`;
    }
    return "/home_user.html";
  };

  const escapeHtml = (value) =>
    String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");

  const uploadComposerMediaFile = async (file, visibilityValue) => {
    if (!file) return null;
    const normalizedVisibility = String(visibilityValue || "private").toLowerCase();
    const fileType = String(file?.type || "").toLowerCase();
    const isImage = fileType.startsWith("image/");
    const isVideo = fileType.startsWith("video/");

    if (!isImage && !isVideo) {
      throw new Error(tr("Solo se permiten archivos de imagen o video.", "Only image or video files are allowed.", "Seuls les fichiers image ou vidéo sont autorisés."));
    }

    if (isImage) {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("visibility", normalizedVisibility);

      const uploadRes = await apiFetch("/media/upload/direct", {
        method: "POST",
        body: formData,
      });
      const uploadData = await parseResponseJson(uploadRes);
      if (!uploadRes.ok) {
        throw new Error(readApiError(uploadData, tr("No se pudo subir la imagen.", "Could not upload the image.", "Impossible de téléverser l'image.")));
      }
      return {
        media_id: Number(uploadData?.media_id || 0) || null,
        media_kind: "image",
      };
    }

    const presignRes = await apiFetch("/media/presign/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filename: String(file?.name || "archivo"),
        content_type: fileType || "application/octet-stream",
        size_bytes: Number(file?.size || 0),
        visibility: normalizedVisibility,
      }),
    });
    const presignData = await parseResponseJson(presignRes);
    if (!presignRes.ok) {
      throw new Error(
        readApiError(
          presignData,
          tr("No se pudo preparar la carga del archivo.", "Could not prepare file upload.", "Impossible de préparer le téléversement du fichier.")
        )
      );
    }

    const mediaId = Number(presignData?.media_id || 0);
    if (!mediaId) {
      throw new Error(tr("No se recibió media_id para la carga de video.", "No media_id was returned for video upload.", "Aucun media_id n'a été renvoyé pour le téléversement vidéo."));
    }

    const proxyForm = new FormData();
    proxyForm.append("media_id", String(mediaId));
    proxyForm.append("file", file);

    const proxyRes = await apiFetch("/media/upload/proxy", {
      method: "POST",
      body: proxyForm,
    });
    const proxyData = await parseResponseJson(proxyRes);
    if (!proxyRes.ok) {
      throw new Error(readApiError(proxyData, tr("No se pudo subir el video.", "Could not upload the video.", "Impossible de téléverser la vidéo.")));
    }

    return {
      media_id: mediaId,
      media_kind: "video",
    };
  };

  const renderPlainTextWithHashtags = (value) => {
    const text = String(value || "");
    if (!text) return "";

    HASHTAG_PATTERN.lastIndex = 0;
    let cursor = 0;
    let html = "";
    let match;
    while ((match = HASHTAG_PATTERN.exec(text)) !== null) {
      const full = String(match[0] || "");
      const prefix = full.startsWith("#") ? "" : full[0];
      const tag = String(match[2] || "").trim();
      if (!tag) continue;

      const token = `#${tag}`;
      const tokenStart = Number(match.index) + prefix.length;
      if (tokenStart < cursor) continue;

      html += escapeHtml(text.slice(cursor, Number(match.index)));
      html += escapeHtml(prefix);
      html += `<a class="post-hashtag-link" href="${escapeHtml(buildFeedHashtagHref(tag))}">${escapeHtml(token)}</a>`;
      cursor = tokenStart + token.length;
    }

    html += escapeHtml(text.slice(cursor));
    return html;
  };

  const renderPostTextHtml = (post) => {
    const text = String(post?.text || "");
    if (!text) return "";

    const mentions = Array.isArray(post?.mentions)
      ? post.mentions
          .filter((item) => Number.isFinite(Number(item?.start_index)) && Number.isFinite(Number(item?.end_index)))
          .map((item) => ({
            start_index: Number(item.start_index),
            end_index: Number(item.end_index),
            profile_url: String(item?.profile_url || "").trim(),
            is_active: Boolean(item?.is_active),
          }))
          .sort((a, b) => a.start_index - b.start_index || a.end_index - b.end_index)
      : [];

    if (!mentions.length) return renderPlainTextWithHashtags(text);

    let cursor = 0;
    let html = "";
    for (const mention of mentions) {
      const start = Math.max(0, mention.start_index);
      const end = Math.min(text.length, Math.max(start, mention.end_index));
      if (start < cursor || end <= start) continue;

      html += renderPlainTextWithHashtags(text.slice(cursor, start));
      const fragment = text.slice(start, end);
      if (mention.is_active && mention.profile_url) {
        html += `<a class="post-mention-link" href="${escapeHtml(mention.profile_url)}">${escapeHtml(fragment)}</a>`;
      } else {
        html += escapeHtml(fragment);
      }
      cursor = end;
    }
    html += renderPlainTextWithHashtags(text.slice(cursor));
    return html;
  };

  const buildDisplayPosts = (posts) => {
    const list = Array.isArray(posts) ? posts : [];
    const grouped = new Map();
    const display = [];

    for (const post of list) {
      const albumId = Number(post?.album_id || 0);
      if (!albumId) {
        display.push({ ...post, __kind: "single" });
        continue;
      }

      const existing = grouped.get(albumId);
      if (!existing) {
        const group = {
          __kind: "album",
          album_id: albumId,
          album_name: String(post?.album_name || "").trim() || `Álbum ${albumId}`,
          album_items: [post],
        };
        grouped.set(albumId, group);
        display.push(group);
        continue;
      }

      existing.album_items.push(post);
    }

    return display.map((item) => {
      if (item.__kind !== "album") return item;

      const albumItems = Array.isArray(item.album_items) ? item.album_items : [];
      const coverPost = albumItems[0] || null;
      const previewItems = albumItems.slice(0, 4);
      const extraItems = Math.max(0, albumItems.length - previewItems.length);

      return {
        ...coverPost,
        __kind: "album",
        album_id: item.album_id,
        album_name: item.album_name,
        album_items: albumItems,
        album_preview_items: previewItems,
        album_total_items: albumItems.length,
        album_extra_items: extraItems,
      };
    });
  };

  const applyFeedPosts = (items) => {
    feedPosts = Array.isArray(items) ? items : [];
    displayPosts = buildDisplayPosts(feedPosts);
  };

  const isPostBusy = (postId) => Boolean(postActionBusyMap[Number(postId || 0)]);

  const setPostBusy = (postId, isBusy) => {
    const id = Number(postId || 0);
    if (!id) return;
    const next = { ...postActionBusyMap };
    if (isBusy) {
      next[id] = true;
    } else {
      delete next[id];
    }
    postActionBusyMap = next;
  };

  const patchFeedPost = (postId, updater) => {
    const normalizedPostId = Number(postId || 0);
    if (!normalizedPostId || typeof updater !== "function") return;

    let changed = false;
    const next = feedPosts.map((post) => {
      if (Number(post?.id || 0) !== normalizedPostId) return post;
      changed = true;
      return updater(post);
    });
    if (!changed) return;

    applyFeedPosts(next);
  };

  const enrichPostsWithAuthorProfiles = async (posts) => {
    const sourcePosts = Array.isArray(posts) ? posts : [];
    if (!sourcePosts.length) return [];

    const uniqueAuthorIds = Array.from(
      new Set(
        sourcePosts
          .map((post) => Number(post?.author?.id || 0))
          .filter((id) => Number.isFinite(id) && id > 0)
      )
    );

    const profilesByAuthorId = new Map();
    await Promise.all(
      uniqueAuthorIds.map(async (authorId) => {
        try {
          const profile = await fetchFollowProfile({ userId: authorId });
          profilesByAuthorId.set(authorId, profile);
        } catch {
          profilesByAuthorId.set(authorId, null);
        }
      })
    );

    return sourcePosts.map((post) => {
      const authorId = Number(post?.author?.id || 0);
      const profile = profilesByAuthorId.get(authorId);
      const authorAvatarUrl = String(profile?.avatar_url || "").trim() || DEFAULT_PROFILE_AVATAR;
      const authorProfileUrl =
        String(profile?.profile_url || "").trim() || buildAuthorProfileUrl(post?.author);
      return {
        ...post,
        __author_avatar_url: authorAvatarUrl,
        __author_profile_url: authorProfileUrl,
      };
    });
  };

  const loadFeed = async () => {
    feedLoading = true;
    feedError = "";
    setPostsStatus("");

    try {
      const response = await apiFetch(`/posts/feed?limit=${FEED_LIMIT}&offset=0`);
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo cargar el feed.", "Could not load the feed.", "Impossible de charger le feed.")));
      }
      const enrichedPosts = await enrichPostsWithAuthorProfiles(data);
      applyFeedPosts(enrichedPosts);
    } catch (error) {
      feedError = readUnknownError(error, tr("No se pudo cargar el feed.", "Could not load the feed.", "Impossible de charger le feed."));
      applyFeedPosts([]);
    } finally {
      feedLoading = false;
    }
  };

  const loadFeedSearch = async (query) => {
    const normalizedQuery = normalizeSearchQuery(query);
    feedSearchQuery = normalizedQuery;
    feedSearchLoading = true;
    feedSearchError = "";
    const hashtagMode = isHashtagSearchQuery(normalizedQuery);
    feedSearchType = hashtagMode ? "hashtag" : "mixed";
    feedSearchHashtag = "";
    feedSearchUsers = [];
    feedSearchHashtags = [];
    feedSearchPostsCount = 0;

    if (hashtagMode) {
      feedLoading = true;
      feedError = "";
      applyFeedPosts([]);
    }

    if (!normalizedQuery) {
      feedSearchLoading = false;
      return;
    }

    try {
      const searchParams = new URLSearchParams();
      searchParams.set("q", normalizedQuery);
      searchParams.set("user_limit", "8");
      searchParams.set("hashtag_limit", "10");
      searchParams.set("post_limit", String(FEED_LIMIT));

      const response = await apiFetch(`/posts/search?${searchParams.toString()}`);
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo ejecutar la búsqueda.", "Could not run the search.", "Impossible d'exécuter la recherche.")));
      }

      feedSearchType = data?.query_type === "hashtag" ? "hashtag" : "mixed";
      feedSearchHashtag = String(data?.hashtag || "").trim();
      feedSearchUsers = Array.isArray(data?.users) ? data.users : [];
      feedSearchHashtags = Array.isArray(data?.hashtags) ? data.hashtags : [];

      if (feedSearchType === "hashtag") {
        const sourcePosts = Array.isArray(data?.posts) ? data.posts : [];
        const enrichedPosts = await enrichPostsWithAuthorProfiles(sourcePosts);
        feedSearchPostsCount = enrichedPosts.length;
        applyFeedPosts(enrichedPosts);
        feedError = "";
        feedLoading = false;
      }
    } catch (error) {
      feedSearchError = readUnknownError(error, tr("No se pudo ejecutar la búsqueda.", "Could not run the search.", "Impossible d'exécuter la recherche."));
      if (hashtagMode) {
        feedSearchPostsCount = 0;
        applyFeedPosts([]);
        feedLoading = false;
      }
    } finally {
      feedSearchLoading = false;
    }
  };

  const reloadFeedCenter = async () => {
    if (feedSearchQuery && isHashtagSearchQuery(feedSearchQuery)) {
      await loadFeedSearch(feedSearchQuery);
      return;
    }
    await loadFeed();
  };

  const getOracleCardImage = (cardId) => `/css/oracle/Oracle${cardId}.webp`;

  const applyOracleNoSelectionState = () => {
    oracleHasSelection = false;
    oracleLatestCardImage = ORACLE_BACK_CARD_IMAGE;
    oracleLatestCardAlt = tr("Carta del Oráculo en reverso", "Oracle card back", "Dos de carte Oracle");
    oracleLatestSummary = tr(
      "Conoce El Oráculo y elige tu primera carta para reflexionar sobre tu presente.",
      "Discover the Oracle and choose your first card to reflect on your present."
    );
  };

  const loadOracleState = async () => {
    oracleLoading = true;
    oracleError = "";

    try {
      const response = await apiFetch("/oracle/state");
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(
          readApiError(data, tr("No se pudo cargar tu estado del Oráculo.", "Could not load your Oracle status.", "Impossible de charger ton état Oracle."))
        );
      }

      const responses = Array.isArray(data?.responses) ? data.responses : [];
      const latest = responses.find((entry) => {
        const cardId = Number(entry?.card_id || 0);
        return Number.isFinite(cardId) && cardId >= 1 && cardId <= 30;
      });

      if (!latest) {
        applyOracleNoSelectionState();
        return;
      }

      const cardId = Number(latest.card_id || 0);
      const responseType = String(latest?.response_type || "").trim().toLowerCase();
      const textPublic = String(latest?.text_public || "").trim();

      oracleHasSelection = true;
      oracleLatestCardImage = getOracleCardImage(cardId);
      oracleLatestCardAlt = tr(
        `Carta más reciente elegida en El Oráculo (${cardId})`,
        `Most recent card chosen in the Oracle (${cardId})`
      );

      if (responseType === "public" && textPublic) {
        oracleLatestSummary = truncateText(textPublic);
      } else if (responseType === "secret") {
        oracleLatestSummary = tr(
          "Tu respuesta a esta carta está guardada en secreto en tu Vault.",
          "Your response to this card is stored privately in your Vault."
        );
      } else if (responseType === "heart") {
        oracleLatestSummary = tr(
          "Elegiste dejar esta carta reposando en tu corazón.",
          "You chose to keep this card resting in your heart."
        );
      } else {
        oracleLatestSummary = tr(
          "Esta es la carta más reciente que elegiste en El Oráculo.",
          "This is the most recent card you chose in the Oracle."
        );
      }
    } catch (error) {
      applyOracleNoSelectionState();
      oracleError = readUnknownError(error, tr("No se pudo cargar tu estado del Oráculo.", "Could not load your Oracle status.", "Impossible de charger ton état Oracle."));
    } finally {
      oracleLoading = false;
    }
  };

  const loadFeedProfilePanelContext = async () => {
    try {
      const meResponse = await apiFetch("/auth/me");
      const meData = await parseResponseJson(meResponse);
      if (!meResponse.ok) {
        throw new Error(readApiError(meData, tr("No se pudo cargar tu identidad.", "Could not load your identity.", "Impossible de charger ton identité.")));
      }

      const myUserId = Number(meData?.user_number || 0);
      const myUsername = normalizeUsername(meData?.username);
      const myGuardianRank = Number(meData?.guardian_rank || 0);
      showGuardianPanel = Number.isFinite(myGuardianRank) && myGuardianRank >= GUARDIANS_MIN_RANK;
      const myProfile = await fetchFollowProfile({ userId: myUserId });
      setViewerProfileFromPayload(myProfile);

      const requested = resolveFeedTargetProfile();
      const hasRequestedProfile = Boolean(requested.user_id || requested.username);
      const isMyProfileById = hasRequestedProfile && requested.user_id && myUserId && requested.user_id === myUserId;
      const isMyProfileByUsername =
        hasRequestedProfile && requested.username && myUsername && requested.username === myUsername;

      if (!hasRequestedProfile || isMyProfileById || isMyProfileByUsername) {
        setSideProfileFromPayload(myProfile);
        return;
      }

      const targetProfile = await fetchFollowProfile({
        userId: requested.user_id,
        username: requested.user_id ? "" : requested.username,
      });
      setSideProfileFromPayload(targetProfile);
    } catch (error) {
      showGuardianPanel = false;
      console.error(error);
      sideProfileName = tr("Usuario Kiadez", "Kiadez User", "Utilisateur Kiadez");
      sideProfileHandle = tr("@usuario", "@user", "@utilisateur");
      sideProfileUrl = "/home_user.html";
      sideProfileAvatarUrl = DEFAULT_PROFILE_AVATAR;
      viewerProfileName = tr("Usuario Kiadez", "Kiadez User", "Utilisateur Kiadez");
      viewerProfileAvatarUrl = DEFAULT_PROFILE_AVATAR;
    }
  };

  const donateStar = async (post) => {
    const postId = Number(post?.id || 0);
    if (!postId || isPostBusy(postId)) return;

    if (post?.is_mine) {
      setPostsStatus(tr("No puedes donarte estrellas a ti mismo.", "You cannot donate stars to yourself.", "Tu ne peux pas te donner d'étoiles à toi-même."), true);
      return;
    }
    if (post?.starred_by_me) {
      setPostsStatus(tr("Ya donaste una estrella a esta publicación.", "You already donated a star to this post.", "Tu as déjà donné une étoile à cette publication."), true);
      return;
    }

    setPostBusy(postId, true);
    setPostsStatus("");
    try {
      const response = await apiFetch(`/posts/${postId}/stars`, { method: "POST" });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo donar la estrella.", "Could not donate the star.", "Impossible de donner l'étoile.")));
      }

      patchFeedPost(postId, (current) => ({
        ...current,
        starred_by_me: true,
        star_count: Number(data?.star_count ?? current?.star_count ?? 0),
      }));
      setPostsStatus(tr("Estrella donada.", "Star donated.", "Étoile donnée."));
    } catch (error) {
      setPostsStatus(readUnknownError(error, tr("No se pudo donar la estrella.", "Could not donate the star.", "Impossible de donner l'étoile.")), true);
    } finally {
      setPostBusy(postId, false);
    }
  };

  const commentOnPost = async (post) => {
    const postId = Number(post?.id || 0);
    if (!postId || isPostBusy(postId)) return;

    const text = window.prompt(tr("Escribe tu comentario:", "Write your comment:", "Écris ton commentaire :"));
    if (text === null) return;

    const normalizedText = String(text || "").trim();
    if (!normalizedText) {
      setPostsStatus(tr("El comentario no puede estar vacío.", "The comment cannot be empty.", "Le commentaire ne peut pas être vide."), true);
      return;
    }

    setPostBusy(postId, true);
    setPostsStatus("");
    try {
      const response = await apiFetch(`/posts/${postId}/comments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: normalizedText }),
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(
          readApiError(data, tr("No se pudo comentar la publicación.", "Could not comment on the post.", "Impossible de commenter la publication."))
        );
      }

      patchFeedPost(postId, (current) => ({
        ...current,
        comment_count: Math.max(0, Number(current?.comment_count || 0) + 1),
      }));
      setPostsStatus(tr("Comentario publicado.", "Comment posted.", "Commentaire publié."));
    } catch (error) {
      setPostsStatus(readUnknownError(error, tr("No se pudo comentar la publicación.", "Could not comment on the post.", "Impossible de commenter la publication.")), true);
    } finally {
      setPostBusy(postId, false);
    }
  };

  const sharePost = async (post) => {
    const postId = Number(post?.id || 0);
    if (!postId || isPostBusy(postId)) return;

    setPostBusy(postId, true);
    setPostsStatus("");
    try {
      const response = await apiFetch(`/posts/${postId}/share`, { method: "POST" });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo compartir la publicación.", "Could not share the post.", "Impossible de partager la publication.")));
      }

      patchFeedPost(postId, (current) => ({
        ...current,
        share_count: Number(data?.share_count ?? current?.share_count ?? 0),
      }));

      const shareUrlObject = new URL("/home_user.html", window.location.origin);
      shareUrlObject.searchParams.set("post", String(postId));
      const shareUrl = shareUrlObject.toString();

      try {
        if (navigator.share) {
          await navigator.share({
            title: "Kiadez",
            text: tr("Mira esta publicación", "Check out this post", "Regarde cette publication"),
            url: shareUrl,
          });
        } else if (navigator.clipboard?.writeText) {
          await navigator.clipboard.writeText(shareUrl);
        }
      } catch (shareError) {
        if (shareError?.name !== "AbortError") {
          throw shareError;
        }
      }

      setPostsStatus(tr("Publicación compartida.", "Post shared.", "Publication partagée."));
    } catch (error) {
      setPostsStatus(readUnknownError(error, tr("No se pudo compartir la publicación.", "Could not share the post.", "Impossible de partager la publication.")), true);
    } finally {
      setPostBusy(postId, false);
    }
  };

  const openAlbumGallery = (albumId) => {
    const normalizedAlbumId = Number(albumId || 0);
    if (!normalizedAlbumId) return;
    window.location.href = `/gallery.html?album=${encodeURIComponent(String(normalizedAlbumId))}`;
  };

  const openEditPostModal = (post) => {
    if (!post?.is_mine) return;
    const normalizedPostId = Number(post?.id || 0);
    if (!normalizedPostId) return;
    selectedEditPostId = normalizedPostId;
    editPostText = String(post?.text || "");
    selectedDeletePostId = null;
    selectedReportPostId = null;
  };

  const closeEditPostModal = () => {
    if (editPostBusy) return;
    selectedEditPostId = null;
    editPostText = "";
  };

  const submitEditPost = async () => {
    const postId = Number(selectedEditPostId || 0);
    if (!postId || editPostBusy) return;

    const normalizedText = String(editPostText || "").trim();
    if (!normalizedText) {
      setPostsStatus(tr("El texto de la publicación no puede estar vacío.", "Post text cannot be empty.", "Le texte de publication ne peut pas être vide."), true);
      return;
    }

    editPostBusy = true;
    setPostsStatus("");
    try {
      const response = await apiFetch(`/posts/${postId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: normalizedText }),
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo editar la publicación.", "Could not edit the post.", "Impossible de modifier la publication.")));
      }

      selectedEditPostId = null;
      editPostText = "";
      await reloadFeedCenter();
      setPostsStatus(tr("Publicación actualizada.", "Post updated.", "Publication mise à jour."));
    } catch (error) {
      setPostsStatus(readUnknownError(error, tr("No se pudo editar la publicación.", "Could not edit the post.", "Impossible de modifier la publication.")), true);
    } finally {
      editPostBusy = false;
    }
  };

  const openDeletePostModal = (postId) => {
    const normalizedPostId = Number(postId || 0);
    if (!normalizedPostId) return;
    selectedEditPostId = null;
    selectedDeletePostId = normalizedPostId;
  };

  const closeDeletePostModal = () => {
    if (deletePostBusy) return;
    selectedDeletePostId = null;
  };

  const confirmDeletePost = async () => {
    const postId = Number(selectedDeletePostId || 0);
    if (!postId || deletePostBusy) return;

    deletePostBusy = true;
    setPostsStatus("");
    try {
      const response = await apiFetch(`/posts/${postId}`, { method: "DELETE" });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo eliminar la publicación.", "Could not delete the post.", "Impossible de supprimer la publication.")));
      }

      selectedDeletePostId = null;
      setPostsStatus(
        tr(
          `Publicación eliminada. Se restaron ${Number(data?.removed_stars || 0)} estrellas asociadas.`,
          `Post deleted. ${Number(data?.removed_stars || 0)} associated stars were deducted.`
        )
      );
      await reloadFeedCenter();
    } catch (error) {
      setPostsStatus(
        readUnknownError(error, tr("No se pudo eliminar la publicación.", "Could not delete the post.", "Impossible de supprimer la publication.")),
        true
      );
    } finally {
      deletePostBusy = false;
    }
  };

  const openReportPostModal = (postId) => {
    const normalizedPostId = Number(postId || 0);
    if (!normalizedPostId) return;
    selectedEditPostId = null;
    selectedReportPostId = normalizedPostId;
    postReportReason = "violent";
    postReportReasonOther = "";
  };

  const closeReportPostModal = () => {
    if (reportPostBusy) return;
    selectedReportPostId = null;
    postReportReason = "violent";
    postReportReasonOther = "";
  };

  const submitPostReport = async () => {
    const postId = Number(selectedReportPostId || 0);
    if (!postId || reportPostBusy) return;

    const reason = String(postReportReason || "").trim();
    if (!reason) {
      setPostsStatus(tr("Debes elegir una razón de reporte.", "You must choose a report reason.", "Tu dois choisir une raison de signalement."), true);
      return;
    }
    const otherReason = String(postReportReasonOther || "").trim();
    if (reason === "other" && !otherReason) {
      setPostsStatus(
        tr('', '', ''),
        true
      );
      return;
    }

    reportPostBusy = true;
    setPostsStatus("");
    try {
      const response = await apiFetch(`/posts/${postId}/reports`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          reason,
          other_reason: otherReason || null,
        }),
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo enviar el reporte.", "Could not send the report.", "Impossible d'envoyer le signalement.")));
      }

      selectedReportPostId = null;
      postReportReason = "violent";
      postReportReasonOther = "";
      setPostsStatus(tr("Reporte enviado correctamente.", "Report sent successfully.", "Signalement envoyé avec succès."));
    } catch (error) {
      setPostsStatus(readUnknownError(error, tr("No se pudo enviar el reporte.", "Could not send the report.", "Impossible d'envoyer le signalement.")), true);
    } finally {
      reportPostBusy = false;
    }
  };

  onMount(() => {
    void syncTopbarAvatar();

    const cleanupFns = [];
    let previewObjectUrl = "";
    minorProtectedCollapsed = false;

    const bind = (element, eventName, handler) => {
      if (!element) return;
      element.addEventListener(eventName, handler);
      cleanupFns.push(() => element.removeEventListener(eventName, handler));
    };

    const promptOptions = [
      tr("Publica algo que motive a tus seguidores", "Post something that motivates your followers", "Publie quelque chose qui motive tes abonnés"),
      tr("¿Cómo estás trabajando hoy por tus sueños?", "How are you working today toward your dreams?", "Comment travailles-tu aujourd'hui vers tes rêves ?"),
      tr("¿Qué ha pasado de fantástico hoy?", "What fantastic thing happened today?", "Quelle chose fantastique s'est produite aujourd'hui ?"),
    ];

    const composerInput = document.getElementById("openPostModal");
    const feedHomeBtn = document.getElementById("feedHomeBtn");

    const setRandomPrompt = () => {
      if (!composerInput) return;
      const prompt = promptOptions[Math.floor(Math.random() * promptOptions.length)];
      composerInput.textContent = prompt;
    };
    setRandomPrompt();

    bind(feedHomeBtn, "click", () => {
      setRandomPrompt();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    const menuPublishBtn = document.getElementById("menuPublishBtn");
    const menuDropdown = document.getElementById("menuDropdown");
    const postModalOverlay = document.getElementById("postModalOverlay");
    const closePostModal = document.getElementById("closePostModal");
    const cancelPost = document.getElementById("cancelPost");
    const postFile = document.getElementById("postFile");
    const uploadHint = document.getElementById("uploadHint");
    const postPreview = document.getElementById("postPreview");
    const postTextInput = document.getElementById("postText");
    const postVisibility = document.getElementById("postVisibility");
    const publishPostBtn = document.getElementById("publishPost");

    const applyMinorPostVisibilityGuard = () => {
      if (!postVisibility) return;
      const publicOption = postVisibility.querySelector('option[value="public"]');
      if (publicOption) {
        publicOption.disabled = minorProtectedVisible;
      }
      if (minorProtectedVisible && postVisibility.value === "public") {
        postVisibility.value = "private";
      }
    };

    const resetPreview = () => {
      if (previewObjectUrl) {
        URL.revokeObjectURL(previewObjectUrl);
        previewObjectUrl = "";
      }
      composerSelectedFile = null;
      if (postPreview) {
        postPreview.innerHTML = "";
        postPreview.classList.add("hidden");
      }
      if (uploadHint) uploadHint.textContent = tr("Sin archivo adjunto", "No file attached", "Aucun fichier joint");
      if (postFile) postFile.value = "";
    };

    const openPost = () => {
      if (!postModalOverlay) return;
      applyMinorPostVisibilityGuard();
      postModalOverlay.classList.remove("hidden");
      postModalOverlay.setAttribute("aria-hidden", "false");
    };

    const closePost = () => {
      if (!postModalOverlay) return;
      postModalOverlay.classList.add("hidden");
      postModalOverlay.setAttribute("aria-hidden", "true");
      resetPreview();
      if (postTextInput) postTextInput.value = "";
      if (postVisibility) {
        postVisibility.value = minorProtectedVisible ? "private" : "public";
      }
      applyMinorPostVisibilityGuard();
    };

    bind(composerInput, "click", openPost);
    bind(menuPublishBtn, "click", () => {
      openPost();
      menuDropdown?.removeAttribute("open");
    });

    bind(closePostModal, "click", closePost);
    bind(cancelPost, "click", closePost);
    bind(postModalOverlay, "click", (event) => {
      if (event.target === postModalOverlay) closePost();
    });

    bind(postFile, "change", (event) => {
      const file = event?.target?.files?.[0];
      composerSelectedFile = file || null;
      if (!file) {
        resetPreview();
        return;
      }

      resetPreview();
      composerSelectedFile = file;
      if (uploadHint) uploadHint.textContent = file.name || tr("archivo", "file", "fichier");

      previewObjectUrl = URL.createObjectURL(file);
      if (!postPreview) return;
      postPreview.classList.remove("hidden");

      if (String(file.type || "").startsWith("image/")) {
        postPreview.innerHTML = `<img src="${previewObjectUrl}" alt="${tr("Previsualización", "Preview", "Aperçu")}" />`;
        return;
      }
      if (String(file.type || "").startsWith("video/")) {
        postPreview.innerHTML = `<video src="${previewObjectUrl}" controls><track kind="captions" /></video>`;
        return;
      }

      composerSelectedFile = null;
      setPostsStatus(tr("Solo se permiten archivos de imagen o video.", "Only image or video files are allowed.", "Seuls les fichiers image ou vidéo sont autorisés."), true);
      postPreview.innerHTML = "";
      postPreview.classList.add("hidden");
    });

    bind(publishPostBtn, "click", async () => {
      const text = String(postTextInput?.value || "").trim();
      if (!text && !composerSelectedFile) {
        setPostsStatus(tr("Debes escribir texto o adjuntar imagen/video.", "You must write text or attach image/video.", "Tu dois écrire du texte ou joindre une image/vidéo."), true);
        return;
      }

      const previousLabel = publishPostBtn?.textContent || tr("Publicar", "Publish", "Publier");
      if (publishPostBtn) {
        publishPostBtn.disabled = true;
        publishPostBtn.textContent = tr("Publicando...", "Publishing...", "Publication...");
      }

      if (minorProtectedVisible && postVisibility?.value === "public") {
        postVisibility.value = "private";
        setPostsStatus(
          tr(
            "Tu cuenta está en modo protegido. La publicación se guardará en privado.",
            "Your account is in protected mode. The post will be saved as private."
          )
        );
      }

      try {
        const visibilityValue = String(postVisibility?.value || "public").toLowerCase();
        const mediaData = await uploadComposerMediaFile(composerSelectedFile, visibilityValue);
        const response = await apiFetch("/posts", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text: text || null,
            visibility: visibilityValue,
            media_id: mediaData?.media_id ?? null,
            media_kind: mediaData?.media_kind ?? null,
          }),
        });
        const data = await parseResponseJson(response);
        if (!response.ok) {
          throw new Error(readApiError(data, tr("No se pudo crear la publicación.", "Could not create the post.", "Impossible de créer la publication.")));
        }

        closePost();
        await reloadFeedCenter();
        setPostsStatus(tr("Publicación creada correctamente.", "Post created successfully.", "Publication créée avec succès."));
      } catch (error) {
        setPostsStatus(readUnknownError(error, tr("No se pudo publicar.", "Could not publish.", "Impossible de publier.")), true);
      } finally {
        if (publishPostBtn) {
          publishPostBtn.disabled = false;
          publishPostBtn.textContent = previousLabel;
        }
      }
    });

    void (async () => {
      const initialSearchQuery = readTopbarSearchQuery();
      feedSearchQuery = initialSearchQuery;
      const searchModeHashtag = isHashtagSearchQuery(initialSearchQuery);

      const baseRequests = [
        loadMinorAccreditationStatus(),
        loadOracleState(),
        loadFeedProfilePanelContext(),
      ];

      if (initialSearchQuery) {
        await Promise.all([
          ...baseRequests,
          loadFeedSearch(initialSearchQuery),
          searchModeHashtag ? Promise.resolve() : loadFeed(),
        ]);
      } else {
        await Promise.all([...baseRequests, loadFeed()]);
      }

      applyMinorPostVisibilityGuard();
    })();

    return () => {
      for (const cleanup of cleanupFns) cleanup();
      if (previewObjectUrl) URL.revokeObjectURL(previewObjectUrl);
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{tr("Kiadez — Feed", "Kiadez — Feed", "Kiadez — Fil")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user feed-background">
  <!-- =========================
   *  BARRA SUPERIOR
   *  ========================= -->
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input type="search" placeholder={tr("Buscar en Kiadez", "Search on Kiadez", "Rechercher sur Kiadez")} aria-label={tr("Buscar", "Search", "Rechercher")} />
      </form>
    </div>

    <div class="feed-topbar-zone feed-topbar-center">
      <button class="topbar-btn is-active" id="feedHomeBtn" type="button">🏠 {tr("Home", "Home", "Accueil")}</button>
      <a class="topbar-btn" href="/gallery.html">🖼️ {tr("Galería", "Gallery", "Galerie")}</a>
      <a class="topbar-btn" href="/my-public-whishes.html">🌐 {tr("Deseos públicos", "Public wishes", "Souhaits publics")}</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 {tr("Deseos privados", "Private wishes", "Souhaits privés")}</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html">✅ {tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</a>
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown" id="profileDropdown">
        <summary class="topbar-avatar-btn" aria-label={tr("Perfil del usuario", "User profile", "Profil utilisateur")}>
          <img src="/assets/avatar-default.jpg" alt={tr("Foto de perfil del usuario", "User profile photo", "Photo de profil utilisateur")} />
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/privacy-and-settings.html" role="menuitem">{tr("Configuración y privacidad", "Settings and privacy", "Paramètres et confidentialité")}</a>
          <button type="button" role="menuitem" on:click={logout}>{tr("Cerrar sesión", "Sign out", "Se déconnecter")}</button>
        </div>
      </details>

      <button class="topbar-icon" type="button" aria-label={tr("Notificaciones", "Notifications", "Alertes")}>
        🔔
        <span class="topbar-badge">3</span>
      </button>

      <details class="topbar-dropdown" id="menuDropdown">
        <summary class="topbar-menu-btn" aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}>
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">{tr("Menú", "Menu", "Navigation")}</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <button class="dropdown-action" id="menuPublishBtn" type="button" role="menuitem">
            {tr("Publicar", "Publish", "Publier")}
          </button>
          <a href="/home_user.html" role="menuitem">{tr("Mi Home", "My Home", "Mon Home")}</a>
          <a href="/achievements.html" role="menuitem">{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
          <a href="/gallery.html" role="menuitem">{tr("Galería", "Gallery", "Galerie")}</a>
          <a href="/calendar.html" role="menuitem">{tr("Calendario", "Calendar", "Calendrier")}</a>
          <a href="/my-biography.html" role="menuitem">{tr("Mi Biografía", "My Biography", "Ma biographie")}</a>
          <a href="/messages.html" role="menuitem">{tr("Mensajes", "Messages", "Messagerie")}</a>
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <div class="feed-body">
      <section class="feed-grid" aria-label="Feed social">
        <!-- =========================
         *  LADO IZQUIERDO
         *  ========================= -->
        <aside class="feed-side feed-side-left" aria-label={tr("Oráculo", "Oracle", "Oracle")}>
          <article class="panel oracle-panel">
            <div class="panel-head">
              <h2 class="panel-title">{tr("Tu imagen del Oráculo", "Your Oracle image", "Ton image de l'Oracle")}</h2>
              <span class="panel-badge">{tr("Última visión", "Latest vision", "Dernière vision")}</span>
            </div>

            <div class="oracle-card">
              <img src={oracleLatestCardImage} alt={oracleLatestCardAlt} />
            </div>

            <div class="oracle-response-block">
              {#if oracleLoading}
                <p class="oracle-response">{tr("Cargando tu estado del Oráculo...", "Loading your Oracle status...", "Chargement de ton état Oracle...")}</p>
              {:else if oracleError}
                <p class="oracle-response">{oracleError}</p>
                <a class="btn btn-outline btn-compact oracle-feed-link" href="/oracle.html">{tr("Ir al Oráculo", "Go to Oracle", "Aller à l'Oracle")}</a>
              {:else if oracleHasSelection}
                <div class="oracle-response-title">{tr("Carta más reciente del Oráculo", "Most recent Oracle card", "Carte Oracle la plus récente")}</div>
                <p class="oracle-response">{oracleLatestSummary}</p>
                <a class="btn btn-outline btn-compact oracle-feed-link" href="/oracle.html">{tr("Ir al Oráculo", "Go to Oracle", "Aller à l'Oracle")}</a>
              {:else}
                <div class="oracle-response-title">{tr("Aún no has elegido una carta", "You have not chosen a card yet", "Tu n'as pas encore choisi de carte")}</div>
                <p class="oracle-response">{oracleLatestSummary}</p>
                <a class="btn btn-outline btn-compact oracle-feed-link" href="/oracle.html">{tr("Conocer El Oráculo", "Discover the Oracle", "Découvrir l'Oracle")}</a>
              {/if}
            </div>
          </article>
        </aside>

        <!-- =========================
         *  LADO CENTRAL
         *  ========================= -->
        <section class="feed-center">
          <article class="panel composer">
            <div class="composer-row">
              <img
                class="avatar avatar-sm composer-avatar"
                src={viewerProfileAvatarUrl}
                alt={`${tr("Foto de perfil de", "Profile photo of", "Photo de profil de")} ${viewerProfileName}`}
              />
              <button class="composer-input" id="openPostModal" type="button">
                {tr("Publica algo que motive a tus seguidores...", "Post something that inspires your followers...", "Publie quelque chose qui inspire tes abonnés...")}
              </button>
            </div>
          </article>

          {#if minorProtectedVisible}
            <article class="panel minor-protected-panel">
              <div class="panel-head minor-protected-head">
                <h3 class="panel-title">{tr("Cuenta en modo protegido", "Account in protected mode", "Compte en mode protégé")}</h3>
                <button class="btn btn-outline btn-compact minor-protected-toggle" type="button" on:click={toggleMinorProtectedPanel}>
                  {minorProtectedCollapsed ? tr("Expandir", "Expand", "Déployer") : tr("Reducir", "Collapse", "Réduire")}
                </button>
              </div>
              {#if !minorProtectedCollapsed}
                <div class="minor-protected-body">
                  <p class="panel-muted">
                    {tr(
                      "Según la fecha de nacimiento registrada, tu perfil requiere validación de un padre, madre o tutor legal para habilitar funciones públicas. Puedes usar la plataforma con normalidad, pero tu contenido permanecerá privado hasta completar este proceso.",
                      "Based on your registered birth date, your profile requires validation by a parent or legal guardian to enable public features. You can use the platform normally, but your content will remain private until this process is completed."
                    )}
                  </p>
                  <p class="panel-muted minor-protected-state">{minorStatusLabel(minorProtectedState?.status)}</p>
                  <div class="minor-protected-actions">
                    <button class="btn btn-primary btn-compact" type="button" on:click={openMinorAccreditationModal}>
                      {tr("Acreditar cuenta", "Accredit account", "Accréditer le compte")}
                    </button>
                  </div>
                </div>
              {/if}
            </article>
          {/if}

          {#if postsStatus}
            <p class={`posts-status ${postsStatusIsError ? "posts-status-error" : ""}`} aria-live="polite">
              {postsStatus}
            </p>
          {/if}

          {#if feedSearchQuery}
            <article class="panel feed-search-panel" aria-label={tr("Resultados de búsqueda", "Search results", "Résultats de recherche")}>
              <div class="panel-head">
                <h3 class="panel-title">{tr("Resultados para", "Results for", "Résultats pour")} "{feedSearchQuery}"</h3>
                <span class="panel-badge">
                  {feedSearchType === "hashtag" ? tr("Hashtag", "Hashtag", "Hashtag") : tr("Usuarios y hashtags", "Users and hashtags", "Utilisateurs et hashtags")}
                </span>
              </div>

              {#if feedSearchLoading}
                <p class="panel-muted">{tr("Buscando resultados...", "Searching...", "Recherche...")}</p>
              {:else if feedSearchError}
                <p class="posts-status posts-status-error">{feedSearchError}</p>
              {:else}
                {#if feedSearchUsers.length > 0}
                  <div class="feed-search-block">
                    <h4 class="feed-search-title">{tr("Usuarios", "Users", "Utilisateurs")}</h4>
                    <div class="feed-search-user-list">
                      {#each feedSearchUsers as user (user.user_id)}
                        <a class="feed-search-user-item" href={user.profile_url}>
                          <strong>{user.full_name}</strong>
                          <span>{user.handle}</span>
                        </a>
                      {/each}
                    </div>
                  </div>
                {/if}

                {#if feedSearchHashtags.length > 0}
                  <div class="feed-search-block">
                    <h4 class="feed-search-title">{tr("Hashtags relacionados", "Related hashtags", "Hashtags liés")}</h4>
                    <div class="feed-search-hashtag-list">
                      {#each feedSearchHashtags as hashtag (hashtag.normalized_tag)}
                        <a class="feed-search-hashtag-item" href={hashtag.href}>
                          <span>{hashtag.tag}</span>
                          <small>{Number(hashtag.post_count || 0)} {tr("publicaciones", "posts", "publications")}</small>
                        </a>
                      {/each}
                    </div>
                  </div>
                {/if}

                {#if feedSearchType === "hashtag"}
                  <p class="panel-muted">
                    {#if isEn || isFr}
                      {feedSearchPostsCount} post(s) found for {feedSearchHashtag || feedSearchQuery}.
                    {:else}
                      {feedSearchPostsCount} publicación(es) encontradas para {feedSearchHashtag || feedSearchQuery}.
                    {/if}
                  </p>
                {/if}

                {#if feedSearchType !== "hashtag" && feedSearchUsers.length === 0 && feedSearchHashtags.length === 0}
                  <p class="panel-muted">
                    {tr("No se encontraron usuarios ni hashtags con ese criterio.", "No users or hashtags were found for that query.", "Aucun utilisateur ni hashtag trouvé pour cette recherche.")}
                  </p>
                {/if}
              {/if}
            </article>
          {/if}

          {#if feedLoading}
            <article class="panel post post-empty">
              <p class="post-text">{tr("Cargando publicaciones del feed...", "Loading feed posts...", "Chargement des publications du feed...")}</p>
            </article>
          {:else if feedError}
            <article class="panel post post-empty">
              <p class="posts-status posts-status-error">{feedError}</p>
              <button class="btn btn-outline" type="button" on:click={() => void reloadFeedCenter()}>
                {tr("Reintentar", "Retry", "Réessayer")}
              </button>
            </article>
          {:else if displayPosts.length === 0}
            <article class="panel post post-empty">
              <p class="post-text">
                {feedSearchType === "hashtag" && feedSearchQuery
                  ? tr(
                    `No encontramos publicaciones para ${feedSearchHashtag || feedSearchQuery}.`,
                    `No posts found for ${feedSearchHashtag || feedSearchQuery}.`
                  )
                  : tr("Aún no hay publicaciones en tu feed.", "There are no posts in your feed yet.", "Il n'y a pas encore de publications dans ton feed.")}
              </p>
            </article>
          {:else}
            {#each displayPosts as post (post.id)}
              {@const isAlbumGroup = post.__kind === "album" && Number(post.album_total_items || 0) > 1}
              {@const authorProfileUrl = String(post.__author_profile_url || buildAuthorProfileUrl(post?.author))}
              {@const authorAvatarUrl = String(post.__author_avatar_url || DEFAULT_PROFILE_AVATAR)}
              <article class="panel post">
                <div class="post-head">
                  <div class="post-head-author">
                    <a class="post-author-avatar-link" href={authorProfileUrl}>
                      <img
                        class="post-author-avatar"
                        src={authorAvatarUrl}
                        alt={`${tr("Foto de perfil de", "Profile photo of", "Photo de profil de")} ${post.author?.name || tr("Usuario", "User", "Utilisateur")}`}
                        loading="lazy"
                      />
                    </a>
                    <div class="post-head-main">
                      <a class="post-author-link" href={authorProfileUrl}>{post.author?.name || tr("Usuario", "User", "Utilisateur")}</a>
                      <span class="post-meta">
                        · {relativeTime(post.created_at)} · {post.visibility === "private" ? tr("Privado", "Private", "Privé") : tr("Público", "Public", "Public")}
                      </span>
                    </div>
                  </div>
                  <div class="post-head-actions">
                    {#if !post.is_mine}
                      <button
                        class="post-head-btn"
                        type="button"
                        title={tr("Reportar publicación", "Report post", "Signaler la publication")}
                        aria-label={tr("Reportar publicación", "Report post", "Signaler la publication")}
                        on:click={() => openReportPostModal(post.id)}
                      >
                        🚩
                      </button>
                    {/if}
                    {#if post.is_mine}
                      <button
                        class="post-head-btn"
                        type="button"
                        title={tr("Editar texto de la publicación", "Edit post text", "Modifier le texte de la publication")}
                        aria-label={tr("Editar texto de la publicación", "Edit post text", "Modifier le texte de la publication")}
                        on:click={() => openEditPostModal(post)}
                      >
                        📝
                      </button>
                    {/if}
                    {#if post.is_mine}
                      <button
                        class="post-head-btn"
                        type="button"
                        title={tr("Eliminar publicación", "Delete post", "Supprimer la publication")}
                        aria-label={tr("Eliminar publicación", "Delete post", "Supprimer la publication")}
                        on:click={() => openDeletePostModal(post.id)}
                      >
                        🗑
                      </button>
                    {/if}
                  </div>
                </div>

                {#if isAlbumGroup}
                  <p class="post-album-meta">
                    {post.album_name || tr("Álbum", "Album", "Album")} · {Number(post.album_total_items || 0)} {tr("archivo(s)", "file(s)", "fichier(s)")}
                  </p>
                {/if}

                {#if post.text}
                  <p class="post-text">{@html renderPostTextHtml(post)}</p>
                {/if}

                {#if isAlbumGroup}
                  <div class="post-album-grid" aria-label={tr("Publicación agrupada de álbum", "Album grouped post", "Publication groupée d'album")}>
                    {#each post.album_preview_items || [] as albumPost, index (`${post.id}-${albumPost.id}-${index}`)}
                      <div class="post-album-cell">
                        {#if albumPost.media_kind === "video"}
                          <video src={albumPost.media_url} muted playsinline preload="metadata">
                            <track kind="captions" />
                          </video>
                        {:else}
                          <img src={albumPost.media_url} alt={tr("Archivo del álbum", "Album file", "Fichier d'album")} loading="lazy" />
                        {/if}
                        {#if index === 3 && Number(post.album_extra_items || 0) > 0}
                          <span class="post-album-more">+{Number(post.album_extra_items || 0)}</span>
                        {/if}
                      </div>
                    {/each}
                  </div>
                {:else if post.media_url}
                  <div class="post-media">
                    {#if post.media_kind === "video"}
                      <video src={post.media_url} controls preload="metadata">
                        <track kind="captions" />
                      </video>
                    {:else}
                      <img src={post.media_url} alt={tr("Media de la publicación", "Post media", "Média de publication")} loading="lazy" />
                    {/if}
                  </div>
                {/if}

                <div class="post-actions">
                  <button
                    class="post-btn"
                    type="button"
                    on:click={() => void donateStar(post)}
                    disabled={isPostBusy(post.id) || Boolean(post.starred_by_me) || Boolean(post.is_mine)}
                  >
                    {post.starred_by_me
                      ? `⭐ ${tr("Estrella donada", "Star donated", "Étoile donnée")} (${Number(post.star_count || 0)})`
                      : `⭐ ${tr("Donar estrella", "Donate star", "Donner une étoile")} (${Number(post.star_count || 0)})`}
                  </button>

                  <button
                    class="post-btn"
                    type="button"
                    on:click={() => void commentOnPost(post)}
                    disabled={isPostBusy(post.id)}
                  >
                    💬 {tr("Comentar", "Comment", "Commenter")} ({Number(post.comment_count || 0)})
                  </button>

                  <button
                    class="post-btn"
                    type="button"
                    on:click={() => void sharePost(post)}
                    disabled={isPostBusy(post.id)}
                  >
                    🔁 {tr("Compartir", "Share", "Partager")} ({Number(post.share_count || 0)})
                  </button>

                  {#if isAlbumGroup}
                    <button
                      class="post-btn"
                      type="button"
                      on:click={() => openAlbumGallery(post.album_id)}
                    >
                      🖼️ {tr("Hojear álbum", "Browse album", "Parcourir l'album")} ({Number(post.album_total_items || 0)})
                    </button>
                  {/if}
                </div>
              </article>
            {/each}
          {/if}
        </section>

        <!-- =========================
         *  LADO DERECHO
         *  ========================= -->
	        <aside class="feed-side feed-side-right" aria-label={tr("Perfil y accesos rápidos", "Profile and quick links", "Profil et liens rapides")}>
          <article class="panel profile-card feed-profile-card">
            <div class="profile-row">
              <a class="feed-profile-link" href={sideProfileUrl}>
                <img class="avatar" src={sideProfileAvatarUrl} alt={`${tr("Foto de perfil de", "Profile photo of", "Photo de profil de")} ${sideProfileName}`} />
              </a>
              <div class="profile-meta">
                <a class="profile-name feed-profile-link" href={sideProfileUrl}>{sideProfileName}</a>
                <p class="profile-rank">{sideProfileHandle}</p>
                <a class="btn btn-outline btn-compact" href={sideProfileUrl}>{tr("Ver perfil", "View profile", "Voir le profil")}</a>
              </div>
            </div>
          </article>

          <article class="panel">
            <h3 class="panel-title">{tr("Mi comunidad", "My community", "Ma communauté")}</h3>
            <ul class="feed-link-list">
              <li><a href="/followers.html">{tr("Seguidores", "Followers", "Abonnés")}</a></li>
              <li><a href="/achievements.html">{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a></li>
              <li><a href="/gallery.html">{tr("Galería", "Gallery", "Galerie")}</a></li>
              <li><a href="/calendar.html">{tr("Calendario", "Calendar", "Calendrier")}</a></li>
              <li><a href="/my-biography.html">{tr("Mi Biografía", "My Biography", "Ma biographie")}</a></li>
              <li><a href="/messages.html">{tr("Mensajería de Guardianes", "Guardian messaging", "Messagerie des Gardiens")}</a></li>
              <li><a href="/privacy-and-settings.html">{tr("Notificaciones", "Notifications", "Alertes")}</a></li>
            </ul>
          </article>

          {#if showGuardianPanel}
            <article class="panel guardian-panel">
              <h3 class="panel-title">{tr("Yo soy Guardián", "I am a Guardian", "Je suis un Gardien")}</h3>
              <p class="panel-muted">{tr("Escenario de gestión y notificaciones para Guardianes activos.", "Management and notifications area for active Guardians.", "Zone de gestion et notifications pour les Gardiens actifs.")}</p>
              <a class="btn btn-primary btn-compact" href="/guardiancenter.html">{tr("Entrar al módulo de Guardianes", "Open Guardian module", "Ouvrir le module Gardien")}</a>
            </article>
          {/if}

          <div class="feed-mini-footer">
            <a href="/mygamerules.html">{tr("Mis reglas de juego", "My game rules", "Mes règles du jeu")}</a>
            <a href="/terms.html">{tr("Términos y condiciones", "Terms and conditions", "Termes et conditions")}</a>
            <a href="/privacy.html">{tr("Privacidad", "Privacy", "Confidentialité")}</a>
            <a href="/privacy-and-settings.html">{tr("Cookies", "Cookies", "Cookies")}</a>
            <a href="/privacy-and-settings.html">{tr("Idiomas", "Languages", "Langues")}</a>
          </div>
        </aside>
      </section>
    </div>
  </main>

  <!-- =========================
   *  MODAL: CREAR PUBLICACIÓN
   *  ========================= -->
  <div class="modal-overlay hidden" id="postModalOverlay" aria-hidden="true">
    <div class="modal modal-wide" role="dialog" aria-modal="true" aria-label={tr("Crear publicación", "Create post", "Créer une publication")}>
      <div class="modal-head">
        <h3>{tr("Crear publicación", "Create post", "Créer une publication")}</h3>
        <button class="modal-close" type="button" id="closePostModal">✕</button>
      </div>

      <div class="modal-body">
        <div class="post-modal-top">
          <img
            class="avatar avatar-sm composer-avatar"
            src={viewerProfileAvatarUrl}
            alt={`${tr("Foto de perfil de", "Profile photo of", "Photo de profil de")} ${viewerProfileName}`}
          />
          <div>
            <div class="post-modal-name"><strong>{viewerProfileName}</strong></div>
            <select class="modal-select" id="postVisibility">
              <option value="public">{tr("Público", "Public", "Public")}</option>
              <option value="private">{tr("Privado", "Private", "Privé")}</option>
            </select>
          </div>
        </div>

        <textarea class="modal-textarea" id="postText" rows="5" placeholder={tr("Escribe algo...", "Write something...", "Écris quelque chose...")}></textarea>

        <div class="upload-row">
          <label class="upload-btn" for="postFile">{tr("Adjuntar imagen o video", "Attach image or video", "Joindre image ou vidéo")}</label>
          <input id="postFile" type="file" accept="image/*,video/*" class="hidden" />
          <div class="upload-hint" id="uploadHint">{tr("Sin archivo adjunto", "No file attached", "Aucun fichier joint")}</div>
        </div>

        <div class="preview hidden" id="postPreview"></div>
      </div>

      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" id="cancelPost">{tr("Cancelar", "Cancel", "Annuler")}</button>
        <button class="btn btn-primary btn-compact" type="button" id="publishPost">{tr("Publicar", "Publish", "Publier")}</button>
      </div>
    </div>
  </div>

  <div
    class={`modal-overlay ${selectedEditPostId ? "" : "hidden"}`}
    aria-hidden={selectedEditPostId ? "false" : "true"}
    on:click={(event) => {
      if (event.target === event.currentTarget) closeEditPostModal();
    }}
  >
    <div class="modal wish-modal" role="dialog" aria-modal="true" aria-label={tr("Editar texto de publicación", "Edit post text", "Modifier le texte de la publication")}>
      <div class="modal-head">
        <h3>{tr("Editar publicación", "Edit post", "Modifier la publication")}</h3>
        <button class="modal-close" type="button" on:click={closeEditPostModal}>✕</button>
      </div>
      <div class="modal-body">
        <p class="panel-muted">{tr("Puedes corregir ortografía o gramática del texto publicado.", "You can fix spelling or grammar in the published text.", "Tu peux corriger l'orthographe ou la grammaire du texte publié.")}</p>
        <label class="modal-label" for="feedEditPostText">{tr("Texto", "Text", "Texte")}</label>
        <textarea
          class="modal-textarea"
          id="feedEditPostText"
          rows="5"
          maxlength="2000"
          bind:value={editPostText}
          placeholder={tr("Escribe el texto actualizado", "Write the updated text", "Écris le texte mis à jour")}
        ></textarea>
      </div>
      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" disabled={editPostBusy} on:click={closeEditPostModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
        <button class="btn btn-primary btn-compact" type="button" disabled={editPostBusy} on:click={() => void submitEditPost()}>
          {editPostBusy ? tr("Guardando...", "Saving...", "Enregistrement...") : tr("Guardar cambios", "Save changes", "Enregistrer les modifications")}
        </button>
      </div>
    </div>
  </div>

  <div
    class={`modal-overlay ${selectedDeletePostId ? "" : "hidden"}`}
    aria-hidden={selectedDeletePostId ? "false" : "true"}
    on:click={(event) => {
      if (event.target === event.currentTarget) closeDeletePostModal();
    }}
  >
    <div class="modal wish-modal delete-wish-modal" role="dialog" aria-modal="true" aria-label={tr("Eliminar publicación", "Delete post", "Supprimer la publication")}>
      <div class="modal-head">
        <h3>{tr("Eliminar publicación", "Delete post", "Supprimer la publication")}</h3>
        <button class="modal-close" type="button" on:click={closeDeletePostModal}>✕</button>
      </div>
      <div class="modal-body">
        <p class="panel-muted">
          {tr(
            "¿Seguro que deseas eliminar esta publicación? Las estrellas asociadas se descontarán del total recibido.",
            "Are you sure you want to delete this post? Associated stars will be deducted from the total received."
          )}
        </p>
      </div>
      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" disabled={deletePostBusy} on:click={closeDeletePostModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
        <button class="btn btn-primary btn-compact" type="button" disabled={deletePostBusy} on:click={() => void confirmDeletePost()}>
          {deletePostBusy ? tr("Eliminando...", "Deleting...", "Suppression...") : tr("Eliminar", "Delete", "Supprimer")}
        </button>
      </div>
    </div>
  </div>

  <div
    class={`modal-overlay ${selectedReportPostId ? "" : "hidden"}`}
    aria-hidden={selectedReportPostId ? "false" : "true"}
    on:click={(event) => {
      if (event.target === event.currentTarget) closeReportPostModal();
    }}
  >
    <div class="modal wish-modal report-post-modal" role="dialog" aria-modal="true" aria-label={tr("Reportar publicación", "Report post", "Signaler la publication")}>
      <div class="modal-head">
        <h3>{tr("Reportar publicación", "Report post", "Signaler la publication")}</h3>
        <button class="modal-close" type="button" on:click={closeReportPostModal}>✕</button>
      </div>
      <div class="modal-body">
        <p class="panel-muted">
          {tr("Selecciona la razón por la cual deseas reportar esta publicación.", "Select the reason why you want to report this post.", "Sélectionne la raison pour laquelle tu veux signaler cette publication.")}
        </p>
        <div class="report-reasons">
          <label class="report-option">
            <input type="radio" name="feedPostReportReason" value="violent" bind:group={postReportReason} />
            {tr("Contenido violento o perturbador", "Violent or disturbing content", "Contenu violent ou perturbant")}
          </label>
          <label class="report-option">
            <input type="radio" name="feedPostReportReason" value="divisive" bind:group={postReportReason} />
            {tr("Contenido que promueve confrontación o división excesiva", "Content that promotes confrontation or excessive division", "Contenu qui favorise la confrontation ou une division excessive")}
          </label>
          <label class="report-option">
            <input type="radio" name="feedPostReportReason" value="sexual" bind:group={postReportReason} />
            {tr("Contenido sexual explícito o inapropiado", "Explicit or inappropriate sexual content", "Contenu sexuel explicite ou inapproprié")}
          </label>
          <label class="report-option">
            <input type="radio" name="feedPostReportReason" value="other" bind:group={postReportReason} />
            {tr("Otra razón", "Other reason", "Autre raison")}
          </label>
        </div>
        <div class={`report-other-wrap ${postReportReason === "other" ? "" : "hidden"}`}>
          <label class="modal-label" for="feedPostReportReasonOther">{tr("Describe la razón", "Describe the reason", "Décris la raison")}</label>
          <textarea
            class="modal-textarea"
            id="feedPostReportReasonOther"
            rows="3"
            placeholder={tr("Escribe tu razón", "Write your reason", "Écris ta raison")}
            bind:value={postReportReasonOther}
          ></textarea>
        </div>
      </div>
      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" disabled={reportPostBusy} on:click={closeReportPostModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
        <button class="btn btn-primary btn-compact" type="button" disabled={reportPostBusy} on:click={() => void submitPostReport()}>
          {reportPostBusy ? tr("Enviando...", "Sending...", "Envoi...") : tr("Enviar reporte", "Send report", "Envoyer le signalement")}
        </button>
      </div>
    </div>
  </div>

  <div
    class={`modal-overlay ${showMinorAccreditationModal ? "" : "hidden"}`}
    aria-hidden={showMinorAccreditationModal ? "false" : "true"}
    on:click={(event) => {
      if (event.target === event.currentTarget) closeMinorAccreditationModal();
    }}
  >
    <div class="modal minor-accreditation-modal" role="dialog" aria-modal="true" aria-label={tr("Acreditar cuenta", "Accredit account", "Accréditer le compte")}>
      <div class="modal-head">
        <h3>{tr("Acreditar cuenta", "Accredit account", "Accréditer le compte")}</h3>
        <button class="modal-close" type="button" on:click={closeMinorAccreditationModal}>✕</button>
      </div>

      <div class="modal-body">
        <p class="panel-muted">
          {tr(
            "Registra los datos del padre, madre o tutor legal para enviar la solicitud de validación.",
            "Register the parent or legal guardian details to send the validation request."
          )}
        </p>

        <label class="modal-label" for="feedMinorGuardianPhone">{tr("Teléfono del padre, madre o tutor legal", "Phone of parent or legal guardian", "Téléphone du parent ou tuteur légal")}</label>
        <input
          class="modal-input"
          id="feedMinorGuardianPhone"
          type="tel"
          maxlength="40"
          placeholder={isEn || isFr ? "+1 555 123 4567" : "+57 321 6852619"}
          bind:value={minorGuardianPhone}
        />

        <label class="modal-label" for="feedMinorGuardianEmail">{tr("Correo electrónico del adulto responsable", "Responsible adult email", "E-mail de l'adulte responsable")}</label>
        <input
          class="modal-input"
          id="feedMinorGuardianEmail"
          type="email"
          maxlength="255"
          placeholder={isEn || isFr ? "example@email.com" : "ejemplo@correo.com"}
          bind:value={minorGuardianEmail}
        />

        <label class="modal-label" for="feedMinorRelationship">{tr("Parentesco", "Relationship", "Relation")}</label>
        <select class="modal-select" id="feedMinorRelationship" bind:value={minorRelationship}>
          <option value="padre">{tr("Padre", "Father", "Père")}</option>
          <option value="madre">{tr("Madre", "Mother", "Mère")}</option>
          <option value="tutor_legal">{tr("Tutor legal", "Legal guardian", "Tuteur légal")}</option>
          <option value="adulto_responsable">{tr("Adulto responsable", "Responsible adult", "Adulte responsable")}</option>
        </select>

        {#if minorAccreditationStatus}
          <p class={`minor-accreditation-modal-status ${minorAccreditationStatusIsError ? "is-error" : ""}`}>
            {minorAccreditationStatus}
          </p>
        {/if}
      </div>

      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" on:click={closeMinorAccreditationModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
        <button
          class="btn btn-primary btn-compact"
          type="button"
          disabled={minorAccreditationBusy}
          on:click={() => void submitMinorAccreditationRequest()}
        >
          {minorAccreditationBusy ? tr("Enviando...", "Sending...", "Envoi...") : tr("Enviar solicitud", "Send request", "Envoyer la demande")}
        </button>
      </div>
    </div>
  </div>
</div>
