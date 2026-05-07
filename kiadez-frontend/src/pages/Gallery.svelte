<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";
  import { syncTopbarAvatar } from "../lib/topbarAvatar";
  import { showUiConfirm } from "../lib/uiFeedback";

  const API = import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") || "http://localhost:8000";
  const RECENT_LIMIT = 20;
  const POSTS_FETCH_LIMIT = 100;
  const SHOW_ALBUMS_PANEL = false;
  const SHOW_ALBUM_CREATION_UI = false;
  let pageTitle = "Kiadez — Galería";
  let isViewingOwnProfile = true;
  let viewerUserId = null;
  let viewerUsername = "";
  let activeProfileUserId = null;
  let activeProfileUsername = "";
  let activeProfileFullName = "";
  let profileStarsTotal = null;

  let isLoading = true;
  let loadError = "";

  let statusMessage = "";
  let statusIsError = false;

  let recentImagePosts = [];
  let folders = [];

  let activeFolderId = "";
  let activeFolderDetail = null;
  let folderDetailLoading = false;

  let renameFolderName = "";
  let renameLoading = false;

  let deletingFolder = false;

  let showCreateAlbumModal = false;
  let albumName = "";
  let albumVisibility = "public";
  let albumFiles = [];
  let albumPublishing = false;
  let albumModalStatus = "";
  let albumModalStatusIsError = false;

  let showPostViewer = false;
  let viewerPostIndex = -1;
  let currentViewerPost = null;
  let viewerCanPrev = false;
  let viewerCanNext = false;

  let viewerComments = [];
  let viewerCommentsLoading = false;
  let viewerCommentText = "";
  let viewerCommentSubmitting = false;
  let viewerActionLoading = false;
  let viewerStatusMessage = "";
  let viewerStatusIsError = false;
  let viewerLoadedPostId = 0;

  const getAccessToken = () =>
    localStorage.getItem("access_token") ||
    localStorage.getItem("kiadez_access_token") ||
    "";

  const parsePositiveId = (value) => {
    const numeric = Number(value);
    return Number.isFinite(numeric) && numeric > 0 ? Math.trunc(numeric) : null;
  };

  const normalizeUsername = (value) => {
    let normalized = String(value || "").trim().toLowerCase();
    while (normalized.startsWith("@")) normalized = normalized.slice(1);
    return normalized;
  };

  const parseResponseJson = async (response) => {
    try {
      return await response.json();
    } catch {
      return {};
    }
  };

  const readApiError = (payload, fallback = "Error inesperado.") => {
    const detail = payload?.detail;
    if (typeof detail === "string" && detail.trim()) {
      return detail.trim();
    }

    if (Array.isArray(detail) && detail.length) {
      const first = detail[0];
      if (typeof first === "string" && first.trim()) {
        return first.trim();
      }
      if (first && typeof first === "object") {
        if (typeof first.msg === "string" && first.msg.trim()) {
          return first.msg.trim();
        }
        if (typeof first.message === "string" && first.message.trim()) {
          return first.message.trim();
        }
      }
    }

    if (detail && typeof detail === "object") {
      if (typeof detail.msg === "string" && detail.msg.trim()) {
        return detail.msg.trim();
      }
      if (typeof detail.message === "string" && detail.message.trim()) {
        return detail.message.trim();
      }
    }

    const message = payload?.message;
    if (typeof message === "string" && message.trim()) {
      return message.trim();
    }

    return fallback;
  };

  const readUnknownError = (error, fallback = "Error inesperado.") => {
    if (!error) return fallback;

    if (typeof error === "string" && error.trim()) {
      return error.trim();
    }

    if (error instanceof Error) {
      const fromMessage = readApiError({ detail: error.message }, "");
      if (fromMessage) return fromMessage;
    }

    if (typeof error === "object") {
      const parsed = readApiError(error, "");
      if (parsed) return parsed;

      const maybeMessage = error?.message;
      if (typeof maybeMessage === "string" && maybeMessage.trim()) {
        return maybeMessage.trim();
      }
    }

    return fallback;
  };

  const escapeHtml = (value) =>
    String(value || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");

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

  const fetchViewerIdentity = async () => {
    const res = await apiFetch("/auth/me");
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(data.detail || "No se pudo cargar tu perfil.");
    }
    return {
      user_id: parsePositiveId(data?.user_number),
      username: normalizeUsername(data?.username || ""),
    };
  };

  const fetchFollowProfile = async ({ userId = null, username = null } = {}) => {
    const idValue = parsePositiveId(userId);
    const usernameValue = normalizeUsername(username || "");
    if (idValue) {
      const res = await apiFetch(`/follows/profile?user_id=${encodeURIComponent(String(idValue))}`);
      const data = await parseResponseJson(res);
      if (!res.ok) throw new Error(data.detail || "No se pudo cargar el perfil.");
      return data;
    }
    if (usernameValue) {
      const res = await apiFetch(`/follows/profile?username=${encodeURIComponent(usernameValue)}`);
      const data = await parseResponseJson(res);
      if (!res.ok) throw new Error(data.detail || "No se pudo cargar el perfil.");
      return data;
    }
    throw new Error("Parámetros inválidos para cargar perfil.");
  };

  const buildProfileQueryParams = () => {
    if (activeProfileUsername) return { key: "u", value: activeProfileUsername };
    if (activeProfileUserId) return { key: "id", value: String(activeProfileUserId) };
    return null;
  };

  const buildProfileModuleUrl = (path) => {
    const raw = String(path || "").trim();
    if (!raw) return "";
    try {
      const url = new URL(raw, window.location.origin);
      const qp = buildProfileQueryParams();
      url.searchParams.delete("u");
      url.searchParams.delete("id");
      if (qp) url.searchParams.set(qp.key, qp.value);
      return `${url.pathname}${url.search}${url.hash}`;
    } catch {
      return raw;
    }
  };

  const buildViewerHomeUrl = () => {
    if (viewerUsername) return `/home_user.html?u=${encodeURIComponent(viewerUsername)}`;
    if (viewerUserId) return `/home_user.html?id=${encodeURIComponent(String(viewerUserId))}`;
    return "/home_user.html";
  };

  const PROFILE_MODULE_ROUTES = {
    home: "/home_user.html",
    public_wishes: "/my-public-whishes.html",
    fulfilled_wishes: "/my-fulfilled-whises.html",
    followers: "/followers.html",
    achievements: "/achievements.html",
    gallery: "/gallery.html",
    stars: "/star-pool-found.html",
    calendar: "/calendar.html",
    biography: "/my-biography.html",
  };

  const syncProfileModuleLinks = () => {
    document.querySelectorAll("a[data-profile-module]").forEach((link) => {
      const key = String(link.getAttribute("data-profile-module") || "").trim();
      const basePath = PROFILE_MODULE_ROUTES[key] || link.getAttribute("href") || "";
      const nextHref = buildProfileModuleUrl(basePath);
      if (nextHref) link.href = nextHref;
    });
  };

  const setMyHomeLinks = (href) => {
    const nextHref = String(href || "").trim();
    if (!nextHref) return;
    document.querySelectorAll("a[data-my-home]").forEach((link) => {
      link.href = nextHref;
    });
  };

  const applyReadOnlyProfileMode = () => {
    document.body.dataset.visitor = "true";
    document.querySelectorAll('a[href="/my-private-whishes.html"]').forEach((link) => link.classList.add("hidden"));
    document.getElementById("btnChangeCover")?.classList.add("hidden");
    document.getElementById("btnEditPurposes")?.classList.add("hidden");
  };

  const applyPageTitle = () => {
    pageTitle = isViewingOwnProfile
      ? "Kiadez — Galería"
      : `Kiadez — Galería de ${activeProfileFullName || "usuario"}`;
  };

  const syncStarsLabel = () => {
    const label = document.getElementById("galleryStarsTotal");
    if (!label) return;
    if (profileStarsTotal === null || profileStarsTotal === undefined) {
      label.textContent = "0";
      return;
    }
    label.textContent = Number(profileStarsTotal || 0).toLocaleString("es-CO");
  };

  const resolveProfileContext = async () => {
    const params = new URLSearchParams(window.location.search);
    const requestedUserId = parsePositiveId(params.get("id"));
    const requestedUsername = normalizeUsername(params.get("u") || "");

    const me = await fetchViewerIdentity();
    viewerUserId = me.user_id;
    viewerUsername = me.username;

    activeProfileUserId = viewerUserId;
    activeProfileUsername = viewerUsername;
    activeProfileFullName = "";
    profileStarsTotal = null;
    isViewingOwnProfile = true;
    document.body.dataset.visitor = "false";

    if (requestedUserId || requestedUsername) {
      const isSelfById = requestedUserId && viewerUserId && requestedUserId === viewerUserId;
      const isSelfByUsername = requestedUsername && viewerUsername && requestedUsername === viewerUsername;
      if (!isSelfById && !isSelfByUsername) {
        const profile = await fetchFollowProfile({
          userId: requestedUserId,
          username: requestedUserId ? null : requestedUsername,
        });
        activeProfileUserId = parsePositiveId(profile?.user_id) || requestedUserId;
        activeProfileUsername = normalizeUsername(profile?.username || requestedUsername);
        activeProfileFullName = String(profile?.full_name || "").trim();
        profileStarsTotal = Number(profile?.received_stars_total || 0);
        isViewingOwnProfile = Boolean(viewerUserId && activeProfileUserId === viewerUserId);
        if (!isViewingOwnProfile) {
          applyReadOnlyProfileMode();
        }
      }
    }

    applyPageTitle();
    setMyHomeLinks(buildViewerHomeUrl());
    syncProfileModuleLinks();
    syncStarsLabel();
  };

  const buildPostsEndpoint = () => {
    const profileId = parsePositiveId(activeProfileUserId);
    if (!isViewingOwnProfile && profileId) {
      return `/posts/user/${encodeURIComponent(String(profileId))}?context=gallery&limit=${POSTS_FETCH_LIMIT}`;
    }
    return `/posts/mine?limit=${POSTS_FETCH_LIMIT}`;
  };

  const setStatus = (message, isError = false) => {
    statusMessage = String(message || "").trim();
    statusIsError = Boolean(isError);
  };

  const setViewerStatus = (message, isError = false) => {
    viewerStatusMessage = String(message || "").trim();
    viewerStatusIsError = Boolean(isError);
  };

  const clearViewerStatus = () => {
    viewerStatusMessage = "";
    viewerStatusIsError = false;
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
      if (future) return `en ${amount} ${label}`;
      return `hace ${amount} ${label}`;
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

  const normalizePostsForGallery = (items) => {
    const list = Array.isArray(items) ? [...items] : [];
    return list
      .filter((post) => {
        const mediaKind = String(post?.media_kind || "").toLowerCase();
        const mediaId = Number(post?.media_id || 0);
        const mediaUrl = String(post?.media_url || "").trim();
        return mediaKind === "image" && mediaId > 0 && !!mediaUrl;
      })
      .sort((a, b) => {
        const aTs = Date.parse(a?.created_at || "");
        const bTs = Date.parse(b?.created_at || "");
        const aSafe = Number.isNaN(aTs) ? 0 : aTs;
        const bSafe = Number.isNaN(bTs) ? 0 : bTs;
        return bSafe - aSafe;
      })
      .slice(0, RECENT_LIMIT);
  };

  const closePostViewer = () => {
    showPostViewer = false;
    viewerPostIndex = -1;
    viewerComments = [];
    viewerCommentsLoading = false;
    viewerCommentText = "";
    viewerCommentSubmitting = false;
    viewerActionLoading = false;
    viewerLoadedPostId = 0;
    clearViewerStatus();
  };

  const syncViewerAfterPostRefresh = ({ preferredPostId = 0 } = {}) => {
    if (!showPostViewer) return;

    if (!recentImagePosts.length) {
      closePostViewer();
      return;
    }

    const preferred = Number(preferredPostId || 0);
    if (preferred > 0) {
      const preferredIndex = recentImagePosts.findIndex(
        (post) => Number(post?.id || 0) === preferred
      );
      if (preferredIndex >= 0) {
        viewerPostIndex = preferredIndex;
        return;
      }
    }

    if (viewerPostIndex < 0) {
      viewerPostIndex = 0;
      return;
    }

    if (viewerPostIndex >= recentImagePosts.length) {
      viewerPostIndex = recentImagePosts.length - 1;
    }
  };

  const applyRecentPosts = ({ items, preferredViewerPostId = 0 } = {}) => {
    recentImagePosts = normalizePostsForGallery(items);
    syncViewerAfterPostRefresh({ preferredPostId: preferredViewerPostId });

    const activeViewerPostId = Number(
      showPostViewer &&
        viewerPostIndex >= 0 &&
        viewerPostIndex < recentImagePosts.length
        ? recentImagePosts[viewerPostIndex]?.id || 0
        : 0
    );

    if (showPostViewer && activeViewerPostId > 0) {
      viewerLoadedPostId = activeViewerPostId;
    }
  };

  const loadViewerCommentsForPost = async (postId) => {
    viewerComments = [];
    viewerCommentsLoading = false;
    viewerLoadedPostId = Number(postId || 0);
    return;

    const normalizedPostId = Number(postId || 0);
    if (!normalizedPostId) {
      viewerComments = [];
      viewerLoadedPostId = 0;
      return;
    }

    viewerCommentsLoading = true;
    try {
      const response = await apiFetch(`/posts/${normalizedPostId}/comments?limit=200`);
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudieron cargar los comentarios."));
      }

      viewerComments = Array.isArray(data) ? data : [];
      viewerLoadedPostId = normalizedPostId;
    } catch (error) {
      viewerComments = [];
      viewerLoadedPostId = 0;
      setViewerStatus(readUnknownError(error, "No se pudieron cargar los comentarios."), true);
    } finally {
      viewerCommentsLoading = false;
    }
  };

  const loadRecentPostsOnly = async ({ preferredViewerPostId = 0 } = {}) => {
    const response = await apiFetch(buildPostsEndpoint());
    const data = await parseResponseJson(response);
    if (!response.ok) {
      throw new Error(
        readApiError(data, "No se pudieron cargar las publicaciones de imagen.")
      );
    }

    applyRecentPosts({ items: data, preferredViewerPostId });
  };

  const setAlbumModalStatus = (message, isError = false) => {
    albumModalStatus = String(message || "").trim();
    albumModalStatusIsError = Boolean(isError);
  };

  const clearAlbumFiles = () => {
    for (const item of albumFiles) {
      if (item?.preview_url && String(item.preview_url).startsWith("blob:")) {
        URL.revokeObjectURL(item.preview_url);
      }
    }
    albumFiles = [];
  };

  const closeCreateAlbumModal = () => {
    showCreateAlbumModal = false;
    albumName = "";
    albumVisibility = "public";
    albumPublishing = false;
    setAlbumModalStatus("");
    clearAlbumFiles();
    const input = document.getElementById("galleryAlbumFilesInput");
    if (input) input.value = "";
  };

  const openCreateAlbumModal = () => {
    showCreateAlbumModal = true;
    albumName = "";
    albumVisibility = "public";
    albumPublishing = false;
    setAlbumModalStatus("");
    clearAlbumFiles();
  };

  const normalizeAlbumFileKind = (file) => {
    const mime = String(file?.type || "").toLowerCase();
    if (mime.startsWith("video/")) return "video";
    if (mime.startsWith("image/")) return "image";
    return "";
  };

  const handleAlbumFilesChange = (event) => {
    const files = Array.from(event?.target?.files || []);
    clearAlbumFiles();

    const next = [];
    let ignored = 0;
    for (const file of files) {
      const mediaKind = normalizeAlbumFileKind(file);
      if (!mediaKind) {
        ignored += 1;
        continue;
      }

      next.push({
        file,
        media_kind: mediaKind,
        preview_url: URL.createObjectURL(file),
        name: file.name || "archivo",
      });
    }
    albumFiles = next;

    if (ignored > 0) {
      setAlbumModalStatus(
        `${ignored} archivo(s) ignorado(s). Solo se permiten imágenes y videos.`,
        true
      );
      return;
    }

    setAlbumModalStatus("");
  };

  const loadFolderDetail = async (folderId) => {
    const normalizedFolderId = Number(folderId || 0);
    if (!normalizedFolderId) {
      activeFolderDetail = null;
      return;
    }

    folderDetailLoading = true;
    try {
      const response = await apiFetch(`/gallery/mine/folders/${normalizedFolderId}`);
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo cargar el álbum."));
      }

      activeFolderDetail = data;
      renameFolderName = String(data?.name || "");
    } catch (error) {
      activeFolderDetail = null;
      setStatus(readUnknownError(error, "No se pudo cargar el álbum."), true);
    } finally {
      folderDetailLoading = false;
    }
  };

  const loadGallery = async ({
    preserveFolder = true,
    preferredViewerPostId = 0,
    preferredAlbumId = 0,
  } = {}) => {
    isLoading = true;
    loadError = "";

    try {
      const postsResponse = await apiFetch(buildPostsEndpoint());
      const postsData = await parseResponseJson(postsResponse);
      if (!postsResponse.ok) {
        throw new Error(
          readApiError(postsData, "No se pudieron cargar tus publicaciones.")
        );
      }
      applyRecentPosts({ items: postsData, preferredViewerPostId });

      if (!SHOW_ALBUMS_PANEL || !isViewingOwnProfile) {
        folders = [];
        activeFolderId = "";
        activeFolderDetail = null;
        renameFolderName = "";
        return;
      }

      const galleryResponse = await apiFetch(`/gallery/mine?recent_limit=${RECENT_LIMIT}`);
      const galleryData = await parseResponseJson(galleryResponse);
      if (!galleryResponse.ok) {
        folders = [];
        activeFolderId = "";
        activeFolderDetail = null;
        renameFolderName = "";
        setStatus(
          readApiError(
            galleryData,
            "No se pudieron cargar los álbumes. Tus publicaciones siguen disponibles."
          ),
          true
        );
        return;
      }

      folders = Array.isArray(galleryData?.folders) ? galleryData.folders : [];
      if (!folders.length) {
        activeFolderId = "";
        activeFolderDetail = null;
        renameFolderName = "";
        return;
      }

      const preferredFromQuery = String(preferredAlbumId || "").trim();
      const hasPreferredFromQuery = preferredFromQuery
        ? folders.some((folder) => String(folder.id) === preferredFromQuery)
        : false;

      if (hasPreferredFromQuery) {
        activeFolderId = preferredFromQuery;
      } else {
        const preferredId = preserveFolder ? String(activeFolderId || "") : "";
        const hasPreferred = preferredId
          ? folders.some((folder) => String(folder.id) === preferredId)
          : false;
        activeFolderId = hasPreferred ? preferredId : String(folders[0].id);
      }
      await loadFolderDetail(activeFolderId);
    } catch (error) {
      loadError = readUnknownError(error, "No se pudo cargar la galería.");
      activeFolderId = "";
      activeFolderDetail = null;
    } finally {
      isLoading = false;
    }
  };

  const selectFolder = async (folderId) => {
    activeFolderId = String(folderId || "");
    await loadFolderDetail(activeFolderId);
  };

  const uploadAlbumMediaFile = async (file, visibilityValue) => {
    const mediaKind = normalizeAlbumFileKind(file);
    if (!mediaKind) {
      throw new Error("Solo se permiten imágenes y videos.");
    }

    if (mediaKind === "image") {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("visibility", String(visibilityValue || "public").toLowerCase());

      const uploadRes = await apiFetch("/media/upload/direct", {
        method: "POST",
        body: formData,
      });
      const uploadData = await parseResponseJson(uploadRes);
      if (!uploadRes.ok) {
        throw new Error(readApiError(uploadData, "No se pudo subir una imagen."));
      }

      const mediaId = Number(uploadData?.media_id || 0);
      if (!mediaId) {
        throw new Error("No se recibió el identificador de la media subida.");
      }
      return mediaId;
    }

    const presignRes = await apiFetch("/media/presign/upload", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        filename: file.name || "video.mp4",
        content_type: file.type || "video/mp4",
        size_bytes: Number(file.size || 0),
        visibility: String(visibilityValue || "public").toLowerCase(),
      }),
    });
    const presignData = await parseResponseJson(presignRes);
    if (!presignRes.ok) {
      throw new Error(readApiError(presignData, "No se pudo preparar la carga del video."));
    }

    const mediaId = Number(presignData?.media_id || 0);
    if (!mediaId) {
      throw new Error("No se recibió un media_id válido para el video.");
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

    return mediaId;
  };

  const publishAlbum = async () => {
    if (albumPublishing) return;

    const normalizedName = String(albumName || "").trim();
    if (!normalizedName) {
      setAlbumModalStatus("Debes escribir el nombre del álbum.", true);
      return;
    }
    if (!albumFiles.length) {
      setAlbumModalStatus("Adjunta al menos una imagen o video.", true);
      return;
    }

    albumPublishing = true;
    setAlbumModalStatus("Subiendo contenido del álbum...");

    try {
      const uploadedMediaIds = [];
      for (const albumFile of albumFiles) {
        const mediaId = await uploadAlbumMediaFile(albumFile.file, albumVisibility);
        uploadedMediaIds.push(mediaId);
      }

      setAlbumModalStatus("Publicando álbum...");
      const response = await apiFetch("/gallery/mine/albums/publish", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: normalizedName,
          visibility: albumVisibility,
          media_ids: uploadedMediaIds,
        }),
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo publicar el álbum."));
      }

      const albumId = Number(data?.album?.id || 0);
      closeCreateAlbumModal();
      setStatus("Álbum publicado correctamente.");
      await loadGallery({
        preserveFolder: true,
        preferredViewerPostId: 0,
      });
      if (albumId > 0) {
        activeFolderId = String(albumId);
        await loadFolderDetail(activeFolderId);
      }
    } catch (error) {
      setAlbumModalStatus(readUnknownError(error, "No se pudo publicar el álbum."), true);
    } finally {
      albumPublishing = false;
    }
  };

  const renameFolder = async () => {
    if (renameLoading) return;

    const normalizedFolderId = Number(activeFolderId || 0);
    if (!normalizedFolderId) {
      setStatus("Selecciona un álbum para renombrar.", true);
      return;
    }

    const nextName = String(renameFolderName || "").trim();
    if (!nextName) {
      setStatus("Debes escribir un nuevo nombre.", true);
      return;
    }

    renameLoading = true;
    try {
      const response = await apiFetch(`/gallery/mine/folders/${normalizedFolderId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: nextName }),
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo renombrar el álbum."));
      }

      setStatus("Álbum renombrado correctamente.");
      await loadGallery({ preserveFolder: true });
    } catch (error) {
      setStatus(readUnknownError(error, "No se pudo renombrar el álbum."), true);
    } finally {
      renameLoading = false;
    }
  };

  const deleteFolder = async () => {
    if (deletingFolder) return;

    const normalizedFolderId = Number(activeFolderId || 0);
    if (!normalizedFolderId) {
      setStatus("Selecciona un álbum para eliminar.", true);
      return;
    }

    const confirmed = await showUiConfirm(
      "¿Deseas eliminar este álbum? Sus asociaciones de media se perderán.",
      {
        title: "Eliminar álbum",
        confirmLabel: "Eliminar",
        cancelLabel: "Cancelar",
        danger: true,
      }
    );
    if (!confirmed) return;

    deletingFolder = true;
    try {
      const response = await apiFetch(`/gallery/mine/folders/${normalizedFolderId}`, {
        method: "DELETE",
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo eliminar el álbum."));
      }

      activeFolderId = "";
      activeFolderDetail = null;
      renameFolderName = "";
      setStatus("Álbum eliminado.");
      await loadGallery({ preserveFolder: false });
    } catch (error) {
      setStatus(readUnknownError(error, "No se pudo eliminar el álbum."), true);
    } finally {
      deletingFolder = false;
    }
  };

  const removeImageFromFolder = async (mediaId) => {
    const normalizedFolderId = Number(activeFolderId || 0);
    const normalizedMediaId = Number(mediaId || 0);
    if (!normalizedFolderId || !normalizedMediaId) return;

    try {
      const response = await apiFetch(
        `/gallery/mine/folders/${normalizedFolderId}/items/${normalizedMediaId}`,
        {
          method: "DELETE",
        }
      );
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(
          readApiError(data, "No se pudo quitar la media del álbum.")
        );
      }

      setStatus("Media retirada del álbum.");
      await loadGallery({ preserveFolder: true });
    } catch (error) {
      setStatus(
        readUnknownError(error, "No se pudo quitar la media del álbum."),
        true
      );
    }
  };

  const handleRenameFolderSubmit = async () => {
    await renameFolder();
  };

  const openPostViewerAt = async (index) => {
    const normalizedIndex = Number(index);
    if (
      !Number.isFinite(normalizedIndex) ||
      normalizedIndex < 0 ||
      normalizedIndex >= recentImagePosts.length
    ) {
      return;
    }

    showPostViewer = true;
    viewerPostIndex = normalizedIndex;
    viewerComments = [];
    viewerCommentText = "";
    viewerLoadedPostId = 0;
    clearViewerStatus();

    const postId = Number(recentImagePosts[normalizedIndex]?.id || 0);
  };

  const goViewerPrev = async () => {
    if (!viewerCanPrev) return;
    const nextIndex = viewerPostIndex - 1;
    viewerPostIndex = nextIndex;
    viewerCommentText = "";
    clearViewerStatus();

    const postId = Number(recentImagePosts[nextIndex]?.id || 0);
  };

  const goViewerNext = async () => {
    if (!viewerCanNext) return;
    const nextIndex = viewerPostIndex + 1;
    viewerPostIndex = nextIndex;
    viewerCommentText = "";
    clearViewerStatus();

    const postId = Number(recentImagePosts[nextIndex]?.id || 0);
  };

  const focusViewerCommentInput = () => {
    const input = document.getElementById("galleryViewerCommentInput");
    input?.focus();
  };

  const donateViewerPostStar = async () => {
    const postId = Number(currentViewerPost?.id || 0);
    if (!postId || viewerActionLoading) return;

    if (currentViewerPost?.is_mine) {
      setViewerStatus("No puedes donarte estrellas a ti mismo.", true);
      return;
    }

    if (currentViewerPost?.starred_by_me) {
      setViewerStatus("Ya donaste una estrella a esta publicación.", true);
      return;
    }

    viewerActionLoading = true;
    clearViewerStatus();
    try {
      const response = await apiFetch(`/posts/${postId}/stars`, {
        method: "POST",
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo donar la estrella."));
      }

      await loadRecentPostsOnly({ preferredViewerPostId: postId });
      setViewerStatus("Estrella donada.");
    } catch (error) {
      setViewerStatus(readUnknownError(error, "No se pudo donar la estrella."), true);
    } finally {
      viewerActionLoading = false;
    }
  };

  const shareViewerPost = async () => {
    return;

    const postId = Number(currentViewerPost?.id || 0);
    if (!postId || viewerActionLoading) return;

    viewerActionLoading = true;
    clearViewerStatus();

    try {
      const response = await apiFetch(`/posts/${postId}/share`, {
        method: "POST",
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo compartir la publicación."));
      }

      const shareUrlObject = new URL("/home_user.html", window.location.origin);
      const profileQuery = buildProfileQueryParams();
      if (profileQuery) {
        shareUrlObject.searchParams.set(profileQuery.key, profileQuery.value);
      }
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

      await loadRecentPostsOnly({ preferredViewerPostId: postId });
      setViewerStatus("Publicación compartida.");
    } catch (error) {
      setViewerStatus(
        readUnknownError(error, "No se pudo compartir la publicación."),
        true
      );
    } finally {
      viewerActionLoading = false;
    }
  };

  const submitViewerComment = async () => {
    return;

    const postId = Number(currentViewerPost?.id || 0);
    if (!postId || viewerCommentSubmitting) return;

    const text = String(viewerCommentText || "").trim();
    if (!text) {
      setViewerStatus("Escribe un comentario antes de enviar.", true);
      return;
    }

    viewerCommentSubmitting = true;
    clearViewerStatus();

    try {
      const response = await apiFetch(`/posts/${postId}/comments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, "No se pudo guardar el comentario."));
      }

      viewerCommentText = "";
      await Promise.all([
        loadViewerCommentsForPost(postId),
        loadRecentPostsOnly({ preferredViewerPostId: postId }),
      ]);
      setViewerStatus("Comentario publicado.");
    } catch (error) {
      setViewerStatus(
        readUnknownError(error, "No se pudo guardar el comentario."),
        true
      );
    } finally {
      viewerCommentSubmitting = false;
    }
  };

  const handleGlobalKeydown = (event) => {
    if (!showPostViewer) return;

    if (event.key === "Escape") {
      closePostViewer();
      return;
    }

    if (event.key === "ArrowLeft") {
      event.preventDefault();
      void goViewerPrev();
      return;
    }

    if (event.key === "ArrowRight") {
      event.preventDefault();
      void goViewerNext();
    }
  };

  $: currentViewerPost =
    showPostViewer &&
    viewerPostIndex >= 0 &&
    viewerPostIndex < recentImagePosts.length
      ? recentImagePosts[viewerPostIndex]
      : null;

  $: viewerCanPrev = showPostViewer && viewerPostIndex > 0;
  $: viewerCanNext =
    showPostViewer && viewerPostIndex >= 0 && viewerPostIndex < recentImagePosts.length - 1;

  onMount(() => {
    let cleanupPurposeCover = () => {};
    void syncTopbarAvatar();

    (async () => {
      try {
        await resolveProfileContext();
        cleanupPurposeCover = initPurposeCoverModule({
          isOwnProfile: isViewingOwnProfile,
          profileUserId: activeProfileUserId,
          profileUsername: activeProfileUsername,
        });
        if (isViewingOwnProfile) {
          const stars = await syncProfileStarsTotal("galleryStarsTotal");
          if (stars !== null && stars !== undefined) {
            profileStarsTotal = Number(stars || 0);
            syncStarsLabel();
          }
        }
      } catch (error) {
        loadError = readUnknownError(error, "No se pudo resolver el perfil.");
      }

      const query = new URLSearchParams(window.location.search);
      const preferredAlbumId = Number(query.get("album") || 0);
      await loadGallery({
        preferredAlbumId: Number.isFinite(preferredAlbumId) ? preferredAlbumId : 0,
      });
    })();

    window.addEventListener("keydown", handleGlobalKeydown);

    return () => {
      window.removeEventListener("keydown", handleGlobalKeydown);
      cleanupPurposeCover?.();
      clearAlbumFiles();
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{pageTitle}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background gallery-page">
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
      <a class="topbar-btn" href="/home_user.html" data-profile-module="home">🏠 Home</a>
      <a class="topbar-btn" href="/gallery.html" data-profile-module="gallery">🖼️ Galería</a>
      <a class="topbar-btn" href="/my-public-whishes.html" data-profile-module="public_wishes">🌐 Deseos públicos</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 Deseos privados</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html" data-profile-module="fulfilled_wishes">✅ Deseos cumplidos</a>
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown">
        <summary class="topbar-avatar-btn" aria-label="Perfil del usuario">
          <img src="/assets/avatar-default.jpg" alt="Perfil de usuario" />
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

      <details class="topbar-dropdown">
        <summary class="topbar-menu-btn" aria-label="Abrir menú">
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">Menú</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem" data-profile-module="home" data-my-home="true">Mi Home</a>
          <a href="/achievements.html" role="menuitem" data-profile-module="achievements">Logros recientes</a>
          <a href="/gallery.html" role="menuitem" data-profile-module="gallery">Galería</a>
          <a href="/calendar.html" role="menuitem" data-profile-module="calendar">Calendario</a>
          <a href="/my-biography.html" role="menuitem" data-profile-module="biography">Mi Biografía</a>
          <a href="/messages.html" role="menuitem">Mensajes</a>
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt="Portada" />

        <div class="cover-actions">
          <button class="icon-btn" id="btnChangeCover" type="button" title="Cambiar portada">
            Cambiar portada
          </button>
          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button" title="Editar mi propósito de vida">
            Editar mi propósito de vida
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="purpose-triangle" aria-label="Deseos de propósito">
          <button class="purpose-pill purpose-top" type="button" id="purpose1">
            Deseo #1: Secreto
          </button>

          <button class="purpose-pill purpose-left" type="button" id="purpose2">
            Deseo construir el Reino de Combray
          </button>

          <button class="purpose-pill purpose-right" type="button" id="purpose3">
            Deseo estar unido a Jesús
          </button>
        </div>

        <div class="cover-hint" id="coverHint">
          Arrastra la portada para encuadrarla
        </div>
      </div>
    </section>

    <div class="home-body gallery-body">
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home" data-profile-module="home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas" data-profile-module="stars">
          <span class="nav-icon">⭐</span>
          <span><strong id="galleryStarsTotal">0</strong> estrellas</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Seguidores" data-profile-module="followers">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes" data-profile-module="achievements">Logros recientes</a>
        <a class="nav-pill is-active" href="/gallery.html" title="Galería" data-profile-module="gallery">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario" data-profile-module="calendar">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía" data-profile-module="biography">Mi biografía</a>
        <a class="nav-pill" href="/messages.html" title="Mensajes">Mensajes</a>
      </nav>

      {#if isLoading}
        <section class="panel">
          <p class="panel-muted">{isViewingOwnProfile ? "Cargando tu galería..." : "Cargando galería del perfil..."}</p>
        </section>
      {:else if loadError}
        <section class="panel">
          <p class="posts-status posts-status-error">{loadError}</p>
          <button class="btn btn-outline" type="button" on:click={() => loadGallery({ preserveFolder: true })}>
            Reintentar
          </button>
        </section>
      {:else}
        <section class="panel">
          <div class="panel-head gallery-head">
            <div>
              <h2 class="panel-title">Últimas imágenes</h2>
            </div>
          </div>

          {#if statusMessage}
            <p class={`posts-status ${statusIsError ? "posts-status-error" : ""}`} aria-live="polite">
              {statusMessage}
            </p>
          {/if}

          {#if recentImagePosts.length === 0}
            <p class="panel-muted">
              {isViewingOwnProfile
                ? "Aún no tienes publicaciones con imagen."
                : "Este perfil aún no tiene publicaciones con imagen."}
            </p>
          {:else}
            <div class="gallery-recent-grid" aria-label="Publicaciones con imagen">
              {#each recentImagePosts as post, index (post.id)}
                <article class="gallery-recent-item">
                  <button
                    class="gallery-recent-open"
                    type="button"
                    title="Abrir publicación"
                    on:click={() => openPostViewerAt(index)}
                  >
                    <img src={post.media_url} alt={`Publicación con imagen ${index + 1}`} loading="lazy" />
                  </button>
                </article>
              {/each}
            </div>
          {/if}
        </section>

        {#if SHOW_ALBUMS_PANEL}
          <section class="panel">
            <div class="panel-head">
              <h3 class="panel-title">Álbumes</h3>
              <span class="panel-badge">{folders.length} álbumes</span>
            </div>

            <div class="gallery-folders-layout">
              <aside class="gallery-folders-sidebar">
                {#if SHOW_ALBUM_CREATION_UI}
                  <button class="gallery-album-create-card" type="button" on:click={openCreateAlbumModal}>
                    <span class="gallery-album-create-plus">+</span>
                    <span>Crear álbum</span>
                  </button>
                {/if}

                {#if folders.length === 0}
                  <p class="panel-muted">Aún no tienes álbumes.</p>
                {:else}
                  <div class="gallery-folder-list" aria-label="Lista de álbumes">
                    {#each folders as folder (folder.id)}
                      <button
                        class={`gallery-folder-item ${String(folder.id) === String(activeFolderId) ? "is-active" : ""}`}
                        type="button"
                        on:click={() => selectFolder(folder.id)}
                      >
                        <strong>{folder.name}</strong>
                        <span>
                          {folder.images_count} archivo(s) · {folder.visibility === "private" ? "Privado" : "Público"}
                        </span>
                      </button>
                    {/each}
                  </div>
                {/if}
              </aside>

              <div class="gallery-folder-detail">
                {#if !activeFolderId}
                  <div class="gallery-folder-placeholder">
                    <p class="panel-muted">Selecciona un álbum para ver su contenido.</p>
                  </div>
                {:else if folderDetailLoading}
                  <div class="gallery-folder-placeholder">
                    <p class="panel-muted">Cargando álbum...</p>
                  </div>
                {:else if activeFolderDetail}
                  <div class="gallery-folder-head">
                    <div>
                      <h4>{activeFolderDetail.name}</h4>
                      <p>
                        {activeFolderDetail.images_count} archivo(s) en este álbum ·
                        {activeFolderDetail.visibility === "private" ? "Privado" : "Público"}
                      </p>
                    </div>
                  </div>

                  <form class="gallery-rename-form" on:submit|preventDefault={handleRenameFolderSubmit}>
                    <input
                      class="modal-input"
                      type="text"
                      maxlength="120"
                      placeholder="Nombre del álbum"
                      bind:value={renameFolderName}
                    />
                    <button class="btn btn-outline" type="submit" disabled={renameLoading}>
                      {renameLoading ? "Guardando..." : "Renombrar"}
                    </button>
                    <button
                      class="btn btn-outline gallery-delete-folder-btn"
                      type="button"
                      on:click={deleteFolder}
                      disabled={deletingFolder}
                    >
                      {deletingFolder ? "Eliminando..." : "Eliminar álbum"}
                    </button>
                  </form>

                  {#if !activeFolderDetail.images || activeFolderDetail.images.length === 0}
                    <p class="panel-muted">
                      Este álbum está vacío.
                    </p>
                  {:else}
                    <div class="gallery-folder-grid" aria-label="Archivos del álbum">
                      {#each activeFolderDetail.images as image (image.media_id)}
                        <article class="gallery-folder-card">
                          {#if image.media_kind === "video"}
                            <video src={image.url} controls preload="metadata">
                              <track kind="captions" />
                            </video>
                          {:else}
                            <img src={image.url} alt={`Media ${image.media_id}`} loading="lazy" />
                          {/if}
                          <button
                            class="gallery-folder-remove"
                            type="button"
                            title="Quitar del álbum"
                            on:click={() => removeImageFromFolder(image.media_id)}
                          >
                            ✕
                          </button>
                        </article>
                      {/each}
                    </div>
                  {/if}
                {:else}
                  <div class="gallery-folder-placeholder">
                    <p class="panel-muted">No se pudo cargar el contenido del álbum seleccionado.</p>
                  </div>
                {/if}
              </div>
            </div>
          </section>
        {/if}
      {/if}
    </div>
  </main>

  {#if SHOW_ALBUM_CREATION_UI && showCreateAlbumModal}
    <div class="modal-overlay gallery-album-modal-overlay" aria-hidden="false">
      <button
        class="gallery-album-modal-backdrop"
        type="button"
        aria-label="Cerrar creación de álbum"
        on:click={closeCreateAlbumModal}
      ></button>
      <div class="modal gallery-album-modal" role="dialog" aria-modal="true" aria-label="Crear álbum">
        <div class="modal-head">
          <h3>Crear álbum</h3>
          <button class="modal-close" type="button" on:click={closeCreateAlbumModal}>✕</button>
        </div>

        <div class="modal-body gallery-album-modal-body">
          <label class="modal-label" for="galleryAlbumNameInput">Nombre del álbum</label>
          <input
            id="galleryAlbumNameInput"
            class="modal-input"
            type="text"
            maxlength="120"
            placeholder="Ejemplo: Viaje de verano"
            bind:value={albumName}
          />

          <label class="modal-label" for="galleryAlbumVisibilitySelect">Visibilidad</label>
          <select
            id="galleryAlbumVisibilitySelect"
            class="modal-select"
            bind:value={albumVisibility}
          >
            <option value="public">Público</option>
            <option value="private">Privado</option>
          </select>

          <label class="modal-label" for="galleryAlbumFilesInput">
            Subir contenido: fotos/videos 🖼️
          </label>
          <input
            id="galleryAlbumFilesInput"
            class="modal-input"
            type="file"
            accept="image/*,video/*"
            multiple
            on:change={handleAlbumFilesChange}
            disabled={albumPublishing}
          />

          <div class="gallery-album-preview-head">
            <strong>Previsualización</strong>
            <span>{albumFiles.length} archivo(s)</span>
          </div>

          {#if albumFiles.length === 0}
            <p class="panel-muted">Aún no has seleccionado archivos para este álbum.</p>
          {:else}
            <div class="gallery-album-preview-grid" aria-label="Previsualización del álbum">
              {#each albumFiles as item, index (`${item.name}-${index}`)}
                <article class="gallery-album-preview-card">
                  {#if item.media_kind === "video"}
                    <video src={item.preview_url} controls preload="metadata">
                      <track kind="captions" />
                    </video>
                  {:else}
                    <img src={item.preview_url} alt={`Archivo ${index + 1}`} loading="lazy" />
                  {/if}
                  <p>{item.name}</p>
                </article>
              {/each}
            </div>
          {/if}

          {#if albumModalStatus}
            <p class={`posts-status ${albumModalStatusIsError ? "posts-status-error" : ""}`} aria-live="polite">
              {albumModalStatus}
            </p>
          {/if}
        </div>

        <div class="modal-actions">
          <button
            class="btn btn-outline btn-compact"
            type="button"
            on:click={closeCreateAlbumModal}
            disabled={albumPublishing}
          >
            Cancelar
          </button>
          <button
            class="btn btn-primary btn-compact"
            type="button"
            on:click={publishAlbum}
            disabled={albumPublishing}
          >
            {albumPublishing ? "Publicando..." : "Publicar álbum"}
          </button>
        </div>
      </div>
    </div>
  {/if}

  {#if showPostViewer && currentViewerPost}
    <div class="modal-overlay gallery-post-viewer-overlay" aria-hidden="false">
      <button class="gallery-post-viewer-backdrop" type="button" aria-label="Cerrar publicación" on:click={closePostViewer}></button>
      <div class="modal gallery-post-viewer" role="dialog" aria-modal="true" aria-label="Publicación con imagen">
        <div class="modal-head">
          <h3>Publicación con imagen</h3>
          <button class="modal-close" type="button" on:click={closePostViewer}>✕</button>
        </div>

        <div class="gallery-post-viewer-layout">
          <section class="gallery-post-viewer-media">
            <button
              class="gallery-post-viewer-nav gallery-post-viewer-nav-prev"
              type="button"
              on:click={() => void goViewerPrev()}
              disabled={!viewerCanPrev}
              aria-label="Imagen anterior"
            >
              ‹
            </button>

            <img src={currentViewerPost.media_url} alt="Publicación en vista completa" loading="eager" />

            <button
              class="gallery-post-viewer-nav gallery-post-viewer-nav-next"
              type="button"
              on:click={() => void goViewerNext()}
              disabled={!viewerCanNext}
              aria-label="Siguiente imagen"
            >
              ›
            </button>

            <p class="gallery-post-viewer-counter">{viewerPostIndex + 1} de {recentImagePosts.length}</p>
          </section>

          <aside class="gallery-post-viewer-side">
            <header class="gallery-post-viewer-author">
              <strong>{currentViewerPost.author?.name || "Usuario"}</strong>
              <span>{relativeTime(currentViewerPost.created_at)}</span>
            </header>

            {#if currentViewerPost.text}
              <p class="gallery-post-viewer-text">{currentViewerPost.text}</p>
            {/if}

            <div class="post-actions gallery-post-viewer-actions">
              <button
                class="post-btn"
                type="button"
                on:click={donateViewerPostStar}
                disabled={
                  viewerActionLoading ||
                  Boolean(currentViewerPost?.is_mine) ||
                  Boolean(currentViewerPost?.starred_by_me)
                }
              >
                {#if currentViewerPost?.starred_by_me}
                  ⭐ Estrella donada ({currentViewerPost.star_count})
                {:else}
                  ⭐ Donar estrella ({currentViewerPost.star_count})
                {/if}
              </button>

            </div>

            {#if viewerStatusMessage}
              <p class={`posts-status ${viewerStatusIsError ? "posts-status-error" : ""}`} aria-live="polite">
                {viewerStatusMessage}
              </p>
            {/if}

          </aside>
        </div>
      </div>
    </div>
  {/if}

  <footer class="kiadez-footer">
    <div class="footer-main">
      <div class="footer-column footer-origin">
        <p class="footer-poem">
          Kiadez fue llamado por una estrella a subir el Monte Manjaro.<br />
          No para dominar, sino para orientar.<br />
          Su luz no deslumbra: acompaña.
        </p>
      </div>

      <div class="footer-columns">
        <div class="footer-column">
          <h4>Sobre nuestra red social</h4>
          <ul>
            <li><a href="/what-is-kiadez.html">Qué es Kiadez</a></li>
            <li><a href="/downloadapp.html">Descarga la app</a></li>
            <li><a href="/guardians-rank.html">Rangos de Guardianes</a></li>
            <li><a href="/be-a-guardian.html">Ser Guardián</a></li>
            <li><a href="/contact.html">Contacto</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>Idiomas</h4>
          <ul>
            <li><a href="/?lang=es">Español</a></li>
            <li><a href="/?lang=pt">Português</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>Contacto</h4>
          <ul>
            <li>info@kiadez.com</li>
            <li>+57 333 225 6078</li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>Información legal</h4>
          <ul>
            <li><a href="/mygamerules.html">Mis reglas de juego</a></li>
            <li><a href="/terms.html">Términos y condiciones</a></li>
            <li><a href="/privacy.html">Privacidad</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      © 2026 Kiadez — Una red social para cumplir deseos.
    </div>
  </footer>
</div>
