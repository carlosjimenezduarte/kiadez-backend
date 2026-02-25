<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { syncTopbarAvatar } from "../lib/topbarAvatar";

  const API = "http://127.0.0.1:8000";
  const FEED_LIMIT = 40;
  const ORACLE_BACK_CARD_IMAGE = "/css/oracle/carta.webp";
  const DEFAULT_PROFILE_AVATAR = "/assets/avatar-default.jpg";
  const GUARDIANS_MIN_RANK = 3;
  const HASHTAG_PATTERN = /(^|[^A-Za-z0-9_])#([A-Za-z0-9_]{2,50})/g;

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
  let oracleLatestCardAlt = "Carta del Oráculo en reverso";
  let oracleLatestSummary =
    "Conoce El Oráculo y elige tu primera carta para reflexionar sobre tu presente.";
  let sideProfileName = "Usuario Kiadez";
  let sideProfileHandle = "@usuario";
  let sideProfileUrl = "/home_user.html";
  let sideProfileAvatarUrl = DEFAULT_PROFILE_AVATAR;
  let showGuardianPanel = false;
  let viewerProfileName = "Usuario Kiadez";
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

  const readApiError = (payload, fallback = "Error inesperado.") => {
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

  const readUnknownError = (error, fallback = "Error inesperado.") => {
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

    sideProfileName = fullName || "Usuario Kiadez";
    sideProfileHandle = handle || (username ? `@${username}` : "@usuario");
    sideProfileUrl = profileUrl || buildProfileUrl({ userId, username });
    sideProfileAvatarUrl = avatarUrl || DEFAULT_PROFILE_AVATAR;
  };

  const setViewerProfileFromPayload = (payload) => {
    const fullName = String(payload?.full_name || "").trim();
    const avatarUrl = String(payload?.avatar_url || "").trim();
    viewerProfileName = fullName || "Usuario Kiadez";
    viewerProfileAvatarUrl = avatarUrl || DEFAULT_PROFILE_AVATAR;
  };

  const fetchFollowProfile = async ({ userId = null, username = "" } = {}) => {
    const normalizedUserId = Number(userId || 0);
    const normalizedUsername = normalizeUsername(username);
    if (Number.isFinite(normalizedUserId) && normalizedUserId > 0) {
      const response = await apiFetch(`/follows/profile?user_id=${encodeURIComponent(String(normalizedUserId))}`);
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo cargar el perfil."));
      }
      return data;
    }
    if (normalizedUsername) {
      const response = await apiFetch(`/follows/profile?username=${encodeURIComponent(normalizedUsername)}`);
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo cargar el perfil."));
      }
      return data;
    }
    throw new Error("Parámetros inválidos para perfil.");
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
      throw new Error("No hay sesión activa.");
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
      throw new Error("Tu sesión expiró. Inicia sesión nuevamente.");
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
    if (status === "requested") return "Solicitud enviada a adulto responsable";
    if (status === "pending") return "Acreditación pendiente";
    if (status === "approved") return "Cuenta acreditada";
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
        throw new Error(readApiError(data, "No se pudo cargar la acreditación de cuenta."));
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
      setMinorAccreditationStatus("Debes registrar el teléfono del adulto responsable.", true);
      return;
    }
    if (!guardianEmail) {
      setMinorAccreditationStatus("Debes registrar el correo del adulto responsable.", true);
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
        throw new Error(readApiError(data, "No se pudo enviar la solicitud."));
      }

      await loadMinorAccreditationStatus();
      setMinorAccreditationStatus(
        data?.message || "Solicitud enviada. El adulto responsable debe aprobarla por correo."
      );
    } catch (error) {
      setMinorAccreditationStatus(readUnknownError(error, "No se pudo enviar la solicitud."), true);
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

    const format = (num, unit) => {
      const amount = Math.max(1, Math.floor(num));
      const label = amount === 1 ? unit : `${unit}s`;
      return future ? `en ${amount} ${label}` : `hace ${amount} ${label}`;
    };

    if (absMs < minute) return future ? "en instantes" : "hace instantes";
    if (absMs < hour) return format(absMs / minute, "minuto");
    if (absMs < day) return format(absMs / hour, "hora");
    if (absMs < 7 * day) return format(absMs / day, "día");

    return date.toLocaleString("es-CO", {
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
      throw new Error("Solo se permiten archivos de imagen o video.");
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
        throw new Error(readApiError(uploadData, "No se pudo subir la imagen."));
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
      throw new Error(readApiError(presignData, "No se pudo preparar la carga del archivo."));
    }

    const mediaId = Number(presignData?.media_id || 0);
    if (!mediaId) {
      throw new Error("No se recibió media_id para la carga de video.");
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
      throw new Error(readApiError(proxyData, "No se pudo subir el video."));
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
        throw new Error(readApiError(data, "No se pudo cargar el feed."));
      }
      const enrichedPosts = await enrichPostsWithAuthorProfiles(data);
      applyFeedPosts(enrichedPosts);
    } catch (error) {
      feedError = readUnknownError(error, "No se pudo cargar el feed.");
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
        throw new Error(readApiError(data, "No se pudo ejecutar la búsqueda."));
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
      feedSearchError = readUnknownError(error, "No se pudo ejecutar la búsqueda.");
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
    oracleLatestCardAlt = "Carta del Oráculo en reverso";
    oracleLatestSummary =
      "Conoce El Oráculo y elige tu primera carta para reflexionar sobre tu presente.";
  };

  const loadOracleState = async () => {
    oracleLoading = true;
    oracleError = "";

    try {
      const response = await apiFetch("/oracle/state");
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo cargar tu estado del Oráculo."));
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
      oracleLatestCardAlt = `Carta más reciente elegida en El Oráculo (${cardId})`;

      if (responseType === "public" && textPublic) {
        oracleLatestSummary = truncateText(textPublic);
      } else if (responseType === "secret") {
        oracleLatestSummary = "Tu respuesta a esta carta está guardada en secreto en tu Vault.";
      } else if (responseType === "heart") {
        oracleLatestSummary = "Elegiste dejar esta carta reposando en tu corazón.";
      } else {
        oracleLatestSummary = "Esta es la carta más reciente que elegiste en El Oráculo.";
      }
    } catch (error) {
      applyOracleNoSelectionState();
      oracleError = readUnknownError(error, "No se pudo cargar tu estado del Oráculo.");
    } finally {
      oracleLoading = false;
    }
  };

  const loadFeedProfilePanelContext = async () => {
    try {
      const meResponse = await apiFetch("/auth/me");
      const meData = await parseResponseJson(meResponse);
      if (!meResponse.ok) {
        throw new Error(readApiError(meData, "No se pudo cargar tu identidad."));
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
      sideProfileName = "Usuario Kiadez";
      sideProfileHandle = "@usuario";
      sideProfileUrl = "/home_user.html";
      sideProfileAvatarUrl = DEFAULT_PROFILE_AVATAR;
      viewerProfileName = "Usuario Kiadez";
      viewerProfileAvatarUrl = DEFAULT_PROFILE_AVATAR;
    }
  };

  const donateStar = async (post) => {
    const postId = Number(post?.id || 0);
    if (!postId || isPostBusy(postId)) return;

    if (post?.is_mine) {
      setPostsStatus("No puedes donarte estrellas a ti mismo.", true);
      return;
    }
    if (post?.starred_by_me) {
      setPostsStatus("Ya donaste una estrella a esta publicación.", true);
      return;
    }

    setPostBusy(postId, true);
    setPostsStatus("");
    try {
      const response = await apiFetch(`/posts/${postId}/stars`, { method: "POST" });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo donar la estrella."));
      }

      patchFeedPost(postId, (current) => ({
        ...current,
        starred_by_me: true,
        star_count: Number(data?.star_count ?? current?.star_count ?? 0),
      }));
      setPostsStatus("Estrella donada.");
    } catch (error) {
      setPostsStatus(readUnknownError(error, "No se pudo donar la estrella."), true);
    } finally {
      setPostBusy(postId, false);
    }
  };

  const commentOnPost = async (post) => {
    const postId = Number(post?.id || 0);
    if (!postId || isPostBusy(postId)) return;

    const text = window.prompt("Escribe tu comentario:");
    if (text === null) return;

    const normalizedText = String(text || "").trim();
    if (!normalizedText) {
      setPostsStatus("El comentario no puede estar vacío.", true);
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
        throw new Error(readApiError(data, "No se pudo comentar la publicación."));
      }

      patchFeedPost(postId, (current) => ({
        ...current,
        comment_count: Math.max(0, Number(current?.comment_count || 0) + 1),
      }));
      setPostsStatus("Comentario publicado.");
    } catch (error) {
      setPostsStatus(readUnknownError(error, "No se pudo comentar la publicación."), true);
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
        throw new Error(readApiError(data, "No se pudo compartir la publicación."));
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
            text: "Mira esta publicación",
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

      setPostsStatus("Publicación compartida.");
    } catch (error) {
      setPostsStatus(readUnknownError(error, "No se pudo compartir la publicación."), true);
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
      setPostsStatus("El texto de la publicación no puede estar vacío.", true);
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
        throw new Error(readApiError(data, "No se pudo editar la publicación."));
      }

      selectedEditPostId = null;
      editPostText = "";
      await reloadFeedCenter();
      setPostsStatus("Publicación actualizada.");
    } catch (error) {
      setPostsStatus(readUnknownError(error, "No se pudo editar la publicación."), true);
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
        throw new Error(readApiError(data, "No se pudo eliminar la publicación."));
      }

      selectedDeletePostId = null;
      setPostsStatus(
        `Publicación eliminada. Se restaron ${Number(data?.removed_stars || 0)} estrellas asociadas.`
      );
      await reloadFeedCenter();
    } catch (error) {
      setPostsStatus(readUnknownError(error, "No se pudo eliminar la publicación."), true);
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
      setPostsStatus("Debes elegir una razón de reporte.", true);
      return;
    }
    const otherReason = String(postReportReasonOther || "").trim();
    if (reason === "other" && !otherReason) {
      setPostsStatus('Debes escribir la razón cuando eliges "Otra razón".', true);
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
        throw new Error(readApiError(data, "No se pudo enviar el reporte."));
      }

      selectedReportPostId = null;
      postReportReason = "violent";
      postReportReasonOther = "";
      setPostsStatus("Reporte enviado correctamente.");
    } catch (error) {
      setPostsStatus(readUnknownError(error, "No se pudo enviar el reporte."), true);
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
      "Publica algo que motive a tus seguidores",
      "¿Cómo estás trabajando hoy por tus sueños?",
      "¿Qué ha pasado de fantástico hoy?",
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
      if (uploadHint) uploadHint.textContent = "Sin archivo adjunto";
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
      if (uploadHint) uploadHint.textContent = file.name || "archivo";

      previewObjectUrl = URL.createObjectURL(file);
      if (!postPreview) return;
      postPreview.classList.remove("hidden");

      if (String(file.type || "").startsWith("image/")) {
        postPreview.innerHTML = `<img src="${previewObjectUrl}" alt="Previsualización" />`;
        return;
      }
      if (String(file.type || "").startsWith("video/")) {
        postPreview.innerHTML = `<video src="${previewObjectUrl}" controls><track kind="captions" /></video>`;
        return;
      }

      composerSelectedFile = null;
      setPostsStatus("Solo se permiten archivos de imagen o video.", true);
      postPreview.innerHTML = "";
      postPreview.classList.add("hidden");
    });

    bind(publishPostBtn, "click", async () => {
      const text = String(postTextInput?.value || "").trim();
      if (!text && !composerSelectedFile) {
        setPostsStatus("Debes escribir texto o adjuntar imagen/video.", true);
        return;
      }

      const previousLabel = publishPostBtn?.textContent || "Publicar";
      if (publishPostBtn) {
        publishPostBtn.disabled = true;
        publishPostBtn.textContent = "Publicando...";
      }

      if (minorProtectedVisible && postVisibility?.value === "public") {
        postVisibility.value = "private";
        setPostsStatus("Tu cuenta está en modo protegido. La publicación se guardará en privado.");
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
          throw new Error(readApiError(data, "No se pudo crear la publicación."));
        }

        closePost();
        await reloadFeedCenter();
        setPostsStatus("Publicación creada correctamente.");
      } catch (error) {
        setPostsStatus(readUnknownError(error, "No se pudo publicar."), true);
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
  <title>Kiadez — Feed</title>
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
        <input type="search" placeholder="Buscar en Kiadez" aria-label="Buscar" />
      </form>
    </div>

    <div class="feed-topbar-zone feed-topbar-center">
      <button class="topbar-btn is-active" id="feedHomeBtn" type="button">🏠 Home</button>
      <a class="topbar-btn" href="/gallery.html">🖼️ Galería</a>
      <a class="topbar-btn" href="/my-public-whishes.html">🌐 Deseos públicos</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 Deseos privados</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html">✅ Deseos cumplidos</a>
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown" id="profileDropdown">
        <summary class="topbar-avatar-btn" aria-label="Perfil del usuario">
          <img src="/assets/avatar-default.jpg" alt="Perfil de Carlos Jiménez Duarte" />
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/privacy-and-settings.html" role="menuitem">Configuración y privacidad</a>
          <button type="button" role="menuitem" on:click={logout}>Cerrar sesión</button>
        </div>
      </details>

      <button class="topbar-icon" type="button" aria-label="Notificaciones">
        🔔
        <span class="topbar-badge">3</span>
      </button>

      <details class="topbar-dropdown" id="menuDropdown">
        <summary class="topbar-menu-btn" aria-label="Abrir menú">
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">Menú</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <button class="dropdown-action" id="menuPublishBtn" type="button" role="menuitem">
            Publicar
          </button>
          <a href="/home_user.html" role="menuitem">Mi Home</a>
          <a href="/achievements.html" role="menuitem">Logros recientes</a>
          <a href="/gallery.html" role="menuitem">Galería</a>
          <a href="/calendar.html" role="menuitem">Calendario</a>
          <a href="/my-biography.html" role="menuitem">Mi Biografía</a>
          <a href="/messages.html" role="menuitem">Mensajes</a>
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
        <aside class="feed-side feed-side-left" aria-label="Oráculo">
          <article class="panel oracle-panel">
            <div class="panel-head">
              <h2 class="panel-title">Tu imagen del Oráculo</h2>
              <span class="panel-badge">Última visión</span>
            </div>

            <div class="oracle-card">
              <img src={oracleLatestCardImage} alt={oracleLatestCardAlt} />
            </div>

            <div class="oracle-response-block">
              {#if oracleLoading}
                <p class="oracle-response">Cargando tu estado del Oráculo...</p>
              {:else if oracleError}
                <p class="oracle-response">{oracleError}</p>
                <a class="btn btn-outline btn-compact oracle-feed-link" href="/oracle.html">Ir al Oráculo</a>
              {:else if oracleHasSelection}
                <div class="oracle-response-title">Carta más reciente del Oráculo</div>
                <p class="oracle-response">{oracleLatestSummary}</p>
                <a class="btn btn-outline btn-compact oracle-feed-link" href="/oracle.html">Ir al Oráculo</a>
              {:else}
                <div class="oracle-response-title">Aún no has elegido una carta</div>
                <p class="oracle-response">{oracleLatestSummary}</p>
                <a class="btn btn-outline btn-compact oracle-feed-link" href="/oracle.html">Conocer El Oráculo</a>
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
                alt={`Foto de perfil de ${viewerProfileName}`}
              />
              <button class="composer-input" id="openPostModal" type="button">
                Publica algo que motive a tus seguidores...
              </button>
            </div>
          </article>

          {#if minorProtectedVisible}
            <article class="panel minor-protected-panel">
              <div class="panel-head minor-protected-head">
                <h3 class="panel-title">Cuenta en modo protegido</h3>
                <button class="btn btn-outline btn-compact minor-protected-toggle" type="button" on:click={toggleMinorProtectedPanel}>
                  {minorProtectedCollapsed ? "Expandir" : "Reducir"}
                </button>
              </div>
              {#if !minorProtectedCollapsed}
                <div class="minor-protected-body">
                  <p class="panel-muted">
                    Según la fecha de nacimiento registrada, tu perfil requiere validación de un padre, madre o tutor legal para habilitar funciones públicas.
                    Puedes usar la plataforma con normalidad, pero tu contenido permanecerá privado hasta completar este proceso.
                  </p>
                  <p class="panel-muted minor-protected-state">{minorStatusLabel(minorProtectedState?.status)}</p>
                  <div class="minor-protected-actions">
                    <button class="btn btn-primary btn-compact" type="button" on:click={openMinorAccreditationModal}>
                      Acreditar cuenta
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
            <article class="panel feed-search-panel" aria-label="Resultados de búsqueda">
              <div class="panel-head">
                <h3 class="panel-title">Resultados para "{feedSearchQuery}"</h3>
                <span class="panel-badge">
                  {feedSearchType === "hashtag" ? "Hashtag" : "Usuarios y hashtags"}
                </span>
              </div>

              {#if feedSearchLoading}
                <p class="panel-muted">Buscando resultados...</p>
              {:else if feedSearchError}
                <p class="posts-status posts-status-error">{feedSearchError}</p>
              {:else}
                {#if feedSearchUsers.length > 0}
                  <div class="feed-search-block">
                    <h4 class="feed-search-title">Usuarios</h4>
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
                    <h4 class="feed-search-title">Hashtags relacionados</h4>
                    <div class="feed-search-hashtag-list">
                      {#each feedSearchHashtags as hashtag (hashtag.normalized_tag)}
                        <a class="feed-search-hashtag-item" href={hashtag.href}>
                          <span>{hashtag.tag}</span>
                          <small>{Number(hashtag.post_count || 0)} publicaciones</small>
                        </a>
                      {/each}
                    </div>
                  </div>
                {/if}

                {#if feedSearchType === "hashtag"}
                  <p class="panel-muted">
                    {feedSearchPostsCount} publicación(es) encontradas para {feedSearchHashtag || feedSearchQuery}.
                  </p>
                {/if}

                {#if feedSearchType !== "hashtag" && feedSearchUsers.length === 0 && feedSearchHashtags.length === 0}
                  <p class="panel-muted">
                    No se encontraron usuarios ni hashtags con ese criterio.
                  </p>
                {/if}
              {/if}
            </article>
          {/if}

          {#if feedLoading}
            <article class="panel post post-empty">
              <p class="post-text">Cargando publicaciones del feed...</p>
            </article>
          {:else if feedError}
            <article class="panel post post-empty">
              <p class="posts-status posts-status-error">{feedError}</p>
              <button class="btn btn-outline" type="button" on:click={() => void reloadFeedCenter()}>
                Reintentar
              </button>
            </article>
          {:else if displayPosts.length === 0}
            <article class="panel post post-empty">
              <p class="post-text">
                {feedSearchType === "hashtag" && feedSearchQuery
                  ? `No encontramos publicaciones para ${feedSearchHashtag || feedSearchQuery}.`
                  : "Aún no hay publicaciones en tu feed."}
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
                        alt={`Foto de perfil de ${post.author?.name || "Usuario"}`}
                        loading="lazy"
                      />
                    </a>
                    <div class="post-head-main">
                      <a class="post-author-link" href={authorProfileUrl}>{post.author?.name || "Usuario"}</a>
                      <span class="post-meta">
                        · {relativeTime(post.created_at)} · {post.visibility === "private" ? "Privado" : "Público"}
                      </span>
                    </div>
                  </div>
                  <div class="post-head-actions">
                    {#if !post.is_mine}
                      <button
                        class="post-head-btn"
                        type="button"
                        title="Reportar publicación"
                        aria-label="Reportar publicación"
                        on:click={() => openReportPostModal(post.id)}
                      >
                        🚩
                      </button>
                    {/if}
                    {#if post.is_mine}
                      <button
                        class="post-head-btn"
                        type="button"
                        title="Editar texto de la publicación"
                        aria-label="Editar texto de la publicación"
                        on:click={() => openEditPostModal(post)}
                      >
                        📝
                      </button>
                    {/if}
                    {#if post.is_mine}
                      <button
                        class="post-head-btn"
                        type="button"
                        title="Eliminar publicación"
                        aria-label="Eliminar publicación"
                        on:click={() => openDeletePostModal(post.id)}
                      >
                        🗑
                      </button>
                    {/if}
                  </div>
                </div>

                {#if isAlbumGroup}
                  <p class="post-album-meta">
                    {post.album_name || "Álbum"} · {Number(post.album_total_items || 0)} archivo(s)
                  </p>
                {/if}

                {#if post.text}
                  <p class="post-text">{@html renderPostTextHtml(post)}</p>
                {/if}

                {#if isAlbumGroup}
                  <div class="post-album-grid" aria-label="Publicación agrupada de álbum">
                    {#each post.album_preview_items || [] as albumPost, index (`${post.id}-${albumPost.id}-${index}`)}
                      <div class="post-album-cell">
                        {#if albumPost.media_kind === "video"}
                          <video src={albumPost.media_url} muted playsinline preload="metadata">
                            <track kind="captions" />
                          </video>
                        {:else}
                          <img src={albumPost.media_url} alt="Archivo del álbum" loading="lazy" />
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
                      <img src={post.media_url} alt="Media de la publicación" loading="lazy" />
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
                      ? `⭐ Estrella donada (${Number(post.star_count || 0)})`
                      : `⭐ Donar estrella (${Number(post.star_count || 0)})`}
                  </button>

                  <button
                    class="post-btn"
                    type="button"
                    on:click={() => void commentOnPost(post)}
                    disabled={isPostBusy(post.id)}
                  >
                    💬 Comentar ({Number(post.comment_count || 0)})
                  </button>

                  <button
                    class="post-btn"
                    type="button"
                    on:click={() => void sharePost(post)}
                    disabled={isPostBusy(post.id)}
                  >
                    🔁 Compartir ({Number(post.share_count || 0)})
                  </button>

                  {#if isAlbumGroup}
                    <button
                      class="post-btn"
                      type="button"
                      on:click={() => openAlbumGallery(post.album_id)}
                    >
                      🖼️ Hojear álbum ({Number(post.album_total_items || 0)})
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
        <aside class="feed-side feed-side-right" aria-label="Perfil y accesos rápidos">
          <article class="panel profile-card feed-profile-card">
            <div class="profile-row">
              <a class="feed-profile-link" href={sideProfileUrl}>
                <img class="avatar" src={sideProfileAvatarUrl} alt={`Foto de perfil de ${sideProfileName}`} />
              </a>
              <div class="profile-meta">
                <a class="profile-name feed-profile-link" href={sideProfileUrl}>{sideProfileName}</a>
                <p class="profile-rank">{sideProfileHandle}</p>
                <a class="btn btn-outline btn-compact" href={sideProfileUrl}>Ver perfil</a>
              </div>
            </div>
          </article>

          <article class="panel">
            <h3 class="panel-title">Mi comunidad</h3>
            <ul class="feed-link-list">
              <li><a href="/followers.html">Seguidores</a></li>
              <li><a href="/achievements.html">Logros recientes</a></li>
              <li><a href="/gallery.html">Galería</a></li>
              <li><a href="/calendar.html">Calendario</a></li>
              <li><a href="/my-biography.html">Mi Biografía</a></li>
              <li><a href="/messages.html">Mensajería de Guardianes</a></li>
              <li><a href="/privacy-and-settings.html">Notificaciones</a></li>
            </ul>
          </article>

          {#if showGuardianPanel}
            <article class="panel guardian-panel">
              <h3 class="panel-title">Yo soy Guardián</h3>
              <p class="panel-muted">Escenario de gestión y notificaciones para Guardianes activos.</p>
              <a class="btn btn-primary btn-compact" href="/guardiancenter.html">Entrar al módulo de Guardianes</a>
            </article>
          {/if}

          <div class="feed-mini-footer">
            <a href="/mygamerules.html">Mis reglas de juego</a>
            <a href="/terms.html">Términos y condiciones</a>
            <a href="/privacy.html">Privacidad</a>
            <a href="/privacy-and-settings.html">Cookies</a>
            <a href="/privacy-and-settings.html">Idiomas</a>
          </div>
        </aside>
      </section>
    </div>
  </main>

  <!-- =========================
   *  MODAL: CREAR PUBLICACIÓN
   *  ========================= -->
  <div class="modal-overlay hidden" id="postModalOverlay" aria-hidden="true">
    <div class="modal modal-wide" role="dialog" aria-modal="true" aria-label="Crear publicación">
      <div class="modal-head">
        <h3>Crear publicación</h3>
        <button class="modal-close" type="button" id="closePostModal">✕</button>
      </div>

      <div class="modal-body">
        <div class="post-modal-top">
          <img
            class="avatar avatar-sm composer-avatar"
            src={viewerProfileAvatarUrl}
            alt={`Foto de perfil de ${viewerProfileName}`}
          />
          <div>
            <div class="post-modal-name"><strong>{viewerProfileName}</strong></div>
            <select class="modal-select" id="postVisibility">
              <option value="public">Público</option>
              <option value="private">Privado</option>
            </select>
          </div>
        </div>

        <textarea class="modal-textarea" id="postText" rows="5" placeholder="Escribe algo..."></textarea>

        <div class="upload-row">
          <label class="upload-btn" for="postFile">Adjuntar imagen o video</label>
          <input id="postFile" type="file" accept="image/*,video/*" class="hidden" />
          <div class="upload-hint" id="uploadHint">Sin archivo adjunto</div>
        </div>

        <div class="preview hidden" id="postPreview"></div>
      </div>

      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" id="cancelPost">Cancelar</button>
        <button class="btn btn-primary btn-compact" type="button" id="publishPost">Publicar</button>
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
    <div class="modal wish-modal" role="dialog" aria-modal="true" aria-label="Editar texto de publicación">
      <div class="modal-head">
        <h3>Editar publicación</h3>
        <button class="modal-close" type="button" on:click={closeEditPostModal}>✕</button>
      </div>
      <div class="modal-body">
        <p class="panel-muted">Puedes corregir ortografía o gramática del texto publicado.</p>
        <label class="modal-label" for="feedEditPostText">Texto</label>
        <textarea
          class="modal-textarea"
          id="feedEditPostText"
          rows="5"
          maxlength="2000"
          bind:value={editPostText}
          placeholder="Escribe el texto actualizado"
        ></textarea>
      </div>
      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" disabled={editPostBusy} on:click={closeEditPostModal}>
          Cancelar
        </button>
        <button class="btn btn-primary btn-compact" type="button" disabled={editPostBusy} on:click={() => void submitEditPost()}>
          {editPostBusy ? "Guardando..." : "Guardar cambios"}
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
    <div class="modal wish-modal delete-wish-modal" role="dialog" aria-modal="true" aria-label="Eliminar publicación">
      <div class="modal-head">
        <h3>Eliminar publicación</h3>
        <button class="modal-close" type="button" on:click={closeDeletePostModal}>✕</button>
      </div>
      <div class="modal-body">
        <p class="panel-muted">
          ¿Seguro que deseas eliminar esta publicación? Las estrellas asociadas se descontarán del total recibido.
        </p>
      </div>
      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" disabled={deletePostBusy} on:click={closeDeletePostModal}>
          Cancelar
        </button>
        <button class="btn btn-primary btn-compact" type="button" disabled={deletePostBusy} on:click={() => void confirmDeletePost()}>
          {deletePostBusy ? "Eliminando..." : "Eliminar"}
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
    <div class="modal wish-modal report-post-modal" role="dialog" aria-modal="true" aria-label="Reportar publicación">
      <div class="modal-head">
        <h3>Reportar publicación</h3>
        <button class="modal-close" type="button" on:click={closeReportPostModal}>✕</button>
      </div>
      <div class="modal-body">
        <p class="panel-muted">
          Selecciona la razón por la cual deseas reportar esta publicación.
        </p>
        <div class="report-reasons">
          <label class="report-option">
            <input type="radio" name="feedPostReportReason" value="violent" bind:group={postReportReason} />
            Contenido violento o perturbador
          </label>
          <label class="report-option">
            <input type="radio" name="feedPostReportReason" value="divisive" bind:group={postReportReason} />
            Contenido que promueve confrontación o división excesiva
          </label>
          <label class="report-option">
            <input type="radio" name="feedPostReportReason" value="sexual" bind:group={postReportReason} />
            Contenido sexual explícito o inapropiado
          </label>
          <label class="report-option">
            <input type="radio" name="feedPostReportReason" value="other" bind:group={postReportReason} />
            Otra razón
          </label>
        </div>
        <div class={`report-other-wrap ${postReportReason === "other" ? "" : "hidden"}`}>
          <label class="modal-label" for="feedPostReportReasonOther">Describe la razón</label>
          <textarea
            class="modal-textarea"
            id="feedPostReportReasonOther"
            rows="3"
            placeholder="Escribe tu razón"
            bind:value={postReportReasonOther}
          ></textarea>
        </div>
      </div>
      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" disabled={reportPostBusy} on:click={closeReportPostModal}>
          Cancelar
        </button>
        <button class="btn btn-primary btn-compact" type="button" disabled={reportPostBusy} on:click={() => void submitPostReport()}>
          {reportPostBusy ? "Enviando..." : "Enviar reporte"}
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
    <div class="modal minor-accreditation-modal" role="dialog" aria-modal="true" aria-label="Acreditar cuenta">
      <div class="modal-head">
        <h3>Acreditar cuenta</h3>
        <button class="modal-close" type="button" on:click={closeMinorAccreditationModal}>✕</button>
      </div>

      <div class="modal-body">
        <p class="panel-muted">
          Registra los datos del padre, madre o tutor legal para enviar la solicitud de validación.
        </p>

        <label class="modal-label" for="feedMinorGuardianPhone">Teléfono del padre, madre o tutor legal</label>
        <input
          class="modal-input"
          id="feedMinorGuardianPhone"
          type="tel"
          maxlength="40"
          placeholder="+57 321 6852619"
          bind:value={minorGuardianPhone}
        />

        <label class="modal-label" for="feedMinorGuardianEmail">Correo electrónico del adulto responsable</label>
        <input
          class="modal-input"
          id="feedMinorGuardianEmail"
          type="email"
          maxlength="255"
          placeholder="ejemplo@correo.com"
          bind:value={minorGuardianEmail}
        />

        <label class="modal-label" for="feedMinorRelationship">Parentesco</label>
        <select class="modal-select" id="feedMinorRelationship" bind:value={minorRelationship}>
          <option value="padre">Padre</option>
          <option value="madre">Madre</option>
          <option value="tutor_legal">Tutor legal</option>
          <option value="adulto_responsable">Adulto responsable</option>
        </select>

        {#if minorAccreditationStatus}
          <p class={`minor-accreditation-modal-status ${minorAccreditationStatusIsError ? "is-error" : ""}`}>
            {minorAccreditationStatus}
          </p>
        {/if}
      </div>

      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" on:click={closeMinorAccreditationModal}>
          Cancelar
        </button>
        <button
          class="btn btn-primary btn-compact"
          type="button"
          disabled={minorAccreditationBusy}
          on:click={() => void submitMinorAccreditationRequest()}
        >
          {minorAccreditationBusy ? "Enviando..." : "Enviar solicitud"}
        </button>
      </div>
    </div>
  </div>
</div>
