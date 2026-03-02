<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";
  import { syncTopbarAvatar } from "../lib/topbarAvatar";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";

  const API = "http://127.0.0.1:8000";
  const RECENT_LIMIT = 20;
  const POSTS_FETCH_LIMIT = 100;
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

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

  const parseResponseJson = async (response) => {
    try {
      return await response.json();
    } catch {
      return {};
    }
  };

  const readApiError = (payload, fallback = tr("Error inesperado.", "Unexpected error.", "Erreur inattendue.")) => {
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

  const readUnknownError = (error, fallback = tr("Error inesperado.", "Unexpected error.", "Erreur inattendue.")) => {
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
      throw new Error(tr("No hay sesión activa.", "No active session.", "Aucune session active."));
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
      throw new Error(tr("Tu sesión expiró. Inicia sesión nuevamente.", "Your session expired. Sign in again.", "Ta session a expiré. Connecte-toi de nouveau."));
    }

    return response;
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

    if (isEn) {
      const formatEn = (num, unit) => {
        const amount = Math.max(1, Math.floor(num));
        const label = amount === 1 ? unit : `${unit}s`;
        return future ? `in ${amount} ${label}` : `${amount} ${label} ago`;
      };
      if (absMs < minute) return future ? "in moments" : "moments ago";
      if (absMs < hour) return formatEn(absMs / minute, "minute");
      if (absMs < day) return formatEn(absMs / hour, "hour");
      if (absMs < 7 * day) return formatEn(absMs / day, "day");
    } else {
      if (absMs < minute) return future ? "en instantes" : "hace instantes";
      if (absMs < hour) return format(absMs / minute, "minuto");
      if (absMs < day) return format(absMs / hour, "hora");
      if (absMs < 7 * day) return format(absMs / day, "día");
    }

    return date.toLocaleString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
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

    if (
      showPostViewer &&
      activeViewerPostId > 0 &&
      activeViewerPostId !== Number(viewerLoadedPostId || 0)
    ) {
      void loadViewerCommentsForPost(activeViewerPostId);
    }
  };

  const loadViewerCommentsForPost = async (postId) => {
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
        throw new Error(readApiError(data, tr("No se pudieron cargar los comentarios.", "Could not load comments.", "Impossible de charger les commentaires.")));
      }

      viewerComments = Array.isArray(data) ? data : [];
      viewerLoadedPostId = normalizedPostId;
    } catch (error) {
      viewerComments = [];
      viewerLoadedPostId = 0;
      setViewerStatus(readUnknownError(error, tr("No se pudieron cargar los comentarios.", "Could not load comments.", "Impossible de charger les commentaires.")), true);
    } finally {
      viewerCommentsLoading = false;
    }
  };

  const loadRecentPostsOnly = async ({ preferredViewerPostId = 0 } = {}) => {
    const response = await apiFetch(`/posts/mine?limit=${POSTS_FETCH_LIMIT}`);
    const data = await parseResponseJson(response);
    if (!response.ok) {
      throw new Error(
        readApiError(data, tr("No se pudieron cargar las publicaciones de imagen.", "Could not load image posts.", "Impossible de load image posts."))
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
        tr(
          `${ignored} archivo(s) ignorado(s). Solo se permiten imágenes y videos.`,
          `${ignored} file(s) ignored. Only images and videos are allowed.`
        ),
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
        throw new Error(readApiError(data, tr("No se pudo cargar el álbum.", "Could not load album.", "Impossible de charger l'album.")));
      }

      activeFolderDetail = data;
      renameFolderName = String(data?.name || "");
    } catch (error) {
      activeFolderDetail = null;
      setStatus(readUnknownError(error, tr("No se pudo cargar el álbum.", "Could not load album.", "Impossible de charger l'album.")), true);
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
      const postsResponse = await apiFetch(`/posts/mine?limit=${POSTS_FETCH_LIMIT}`);
      const postsData = await parseResponseJson(postsResponse);
      if (!postsResponse.ok) {
        throw new Error(
          readApiError(postsData, tr("No se pudieron cargar tus publicaciones.", "Could not load your posts.", "Impossible de load your posts."))
        );
      }
      applyRecentPosts({ items: postsData, preferredViewerPostId });

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
            tr(
              "No se pudieron cargar los álbumes. Tus publicaciones siguen disponibles.",
              "Could not load albums. Your posts are still available."
            )
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
      loadError = readUnknownError(error, tr("No se pudo cargar la galería.", "Could not load gallery.", "Impossible de load gallery."));
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
      throw new Error(tr("Solo se permiten imágenes y videos.", "Only images and videos are allowed.", "Seules les images et vidéos sont autorisées."));
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
        throw new Error(readApiError(uploadData, tr("No se pudo subir una imagen.", "Could not upload an image.", "Impossible de upload an image.")));
      }

      const mediaId = Number(uploadData?.media_id || 0);
      if (!mediaId) {
        throw new Error(tr("No se recibió el identificador de la media subida.", "No uploaded media identifier was received.", "Aucun identifiant de média téléversé n'a été reçu."));
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
      throw new Error(readApiError(presignData, tr("No se pudo preparar la carga del video.", "Could not prepare video upload.", "Impossible de préparer l'envoi vidéo.")));
    }

    const mediaId = Number(presignData?.media_id || 0);
    if (!mediaId) {
      throw new Error(tr("No se recibió un media_id válido para el video.", "No valid media_id was received for the video.", "Aucun media_id valide n'a été reçu pour la vidéo."));
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
      throw new Error(readApiError(proxyData, tr("No se pudo subir el video.", "Could not upload video.", "Impossible de upload video.")));
    }

    return mediaId;
  };

  const publishAlbum = async () => {
    if (albumPublishing) return;

    const normalizedName = String(albumName || "").trim();
    if (!normalizedName) {
      setAlbumModalStatus(tr("Debes escribir el nombre del álbum.", "You must enter the album name.", "Tu dois enter the album name."), true);
      return;
    }
    if (!albumFiles.length) {
      setAlbumModalStatus(tr("Adjunta al menos una imagen o video.", "Attach at least one image or video.", "Joins au moins une image ou une vidéo."), true);
      return;
    }

    albumPublishing = true;
    setAlbumModalStatus(tr("Subiendo contenido del álbum...", "Uploading album content...", "Téléversement du contenu de l'album..."));

    try {
      const uploadedMediaIds = [];
      for (const albumFile of albumFiles) {
        const mediaId = await uploadAlbumMediaFile(albumFile.file, albumVisibility);
        uploadedMediaIds.push(mediaId);
      }

      setAlbumModalStatus(tr("Publicando álbum...", "Publishing album...", "Publication de l'album..."));
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
        throw new Error(readApiError(data, tr("No se pudo publicar el álbum.", "Could not publish album.", "Impossible de publier l'album.")));
      }

      const albumId = Number(data?.album?.id || 0);
      closeCreateAlbumModal();
      setStatus(tr("Álbum publicado correctamente.", "Album published successfully.", "Album publié avec succès."));
      await loadGallery({
        preserveFolder: true,
        preferredViewerPostId: 0,
      });
      if (albumId > 0) {
        activeFolderId = String(albumId);
        await loadFolderDetail(activeFolderId);
      }
    } catch (error) {
      setAlbumModalStatus(readUnknownError(error, tr("No se pudo publicar el álbum.", "Could not publish album.", "Impossible de publier l'album.")), true);
    } finally {
      albumPublishing = false;
    }
  };

  const renameFolder = async () => {
    if (renameLoading) return;

    const normalizedFolderId = Number(activeFolderId || 0);
    if (!normalizedFolderId) {
      setStatus(tr("Selecciona un álbum para renombrar.", "Select an album to rename.", "Sélectionne un album à renommer."), true);
      return;
    }

    const nextName = String(renameFolderName || "").trim();
    if (!nextName) {
      setStatus(tr("Debes escribir un nuevo nombre.", "You must enter a new name.", "Tu dois enter a new name."), true);
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
        throw new Error(readApiError(data, tr("No se pudo renombrar el álbum.", "Could not rename album.", "Impossible de renommer l'album.")));
      }

      setStatus(tr("Álbum renombrado correctamente.", "Album renamed successfully.", "Album renommé avec succès."));
      await loadGallery({ preserveFolder: true });
    } catch (error) {
      setStatus(readUnknownError(error, tr("No se pudo renombrar el álbum.", "Could not rename album.", "Impossible de renommer l'album.")), true);
    } finally {
      renameLoading = false;
    }
  };

  const deleteFolder = async () => {
    if (deletingFolder) return;

    const normalizedFolderId = Number(activeFolderId || 0);
    if (!normalizedFolderId) {
      setStatus(tr("Selecciona un álbum para eliminar.", "Select an album to delete.", "Sélectionne un album à supprimer."), true);
      return;
    }

    const confirmed = window.confirm(
      tr(
        "¿Deseas eliminar este álbum? Sus asociaciones de media se perderán.",
        "Do you want to delete this album? Its media associations will be lost."
      )
    );
    if (!confirmed) return;

    deletingFolder = true;
    try {
      const response = await apiFetch(`/gallery/mine/folders/${normalizedFolderId}`, {
        method: "DELETE",
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(readApiError(data, tr("No se pudo eliminar el álbum.", "Could not delete album.", "Impossible de supprimer l'album.")));
      }

      activeFolderId = "";
      activeFolderDetail = null;
      renameFolderName = "";
      setStatus(tr("Álbum eliminado.", "Album deleted.", "Album supprimé."));
      await loadGallery({ preserveFolder: false });
    } catch (error) {
      setStatus(readUnknownError(error, tr("No se pudo eliminar el álbum.", "Could not delete album.", "Impossible de supprimer l'album.")), true);
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
          readApiError(data, tr("No se pudo quitar la media del álbum.", "Could not remove media from album.", "Impossible de supprimer le média de l'album."))
        );
      }

      setStatus(tr("Media retirada del álbum.", "Media removed from album.", "Média retiré de l'album."));
      await loadGallery({ preserveFolder: true });
    } catch (error) {
      setStatus(
        readUnknownError(error, tr("No se pudo quitar la media del álbum.", "Could not remove media from album.", "Impossible de supprimer le média de l'album.")),
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
    await loadViewerCommentsForPost(postId);
  };

  const goViewerPrev = async () => {
    if (!viewerCanPrev) return;
    const nextIndex = viewerPostIndex - 1;
    viewerPostIndex = nextIndex;
    viewerCommentText = "";
    clearViewerStatus();

    const postId = Number(recentImagePosts[nextIndex]?.id || 0);
    await loadViewerCommentsForPost(postId);
  };

  const goViewerNext = async () => {
    if (!viewerCanNext) return;
    const nextIndex = viewerPostIndex + 1;
    viewerPostIndex = nextIndex;
    viewerCommentText = "";
    clearViewerStatus();

    const postId = Number(recentImagePosts[nextIndex]?.id || 0);
    await loadViewerCommentsForPost(postId);
  };

  const focusViewerCommentInput = () => {
    const input = document.getElementById("galleryViewerCommentInput");
    input?.focus();
  };

  const donateViewerPostStar = async () => {
    const postId = Number(currentViewerPost?.id || 0);
    if (!postId || viewerActionLoading) return;

    if (currentViewerPost?.is_mine) {
      setViewerStatus(tr("No puedes donarte estrellas a ti mismo.", "You cannot donate stars to yourself.", "Tu ne peux pas donner d'étoiles à toi-même."), true);
      return;
    }

    if (currentViewerPost?.starred_by_me) {
      setViewerStatus(tr("Ya donaste una estrella a esta publicación.", "You already donated a star to this post.", "Tu as déjà donné une étoile à cette publication."), true);
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
        throw new Error(readApiError(data, tr("No se pudo donar la estrella.", "Could not donate star.", "Impossible de donner une étoile.")));
      }

      await loadRecentPostsOnly({ preferredViewerPostId: postId });
      setViewerStatus(tr("Estrella donada.", "Star donated.", "Étoile donnée."));
    } catch (error) {
      setViewerStatus(readUnknownError(error, tr("No se pudo donar la estrella.", "Could not donate star.", "Impossible de donner une étoile.")), true);
    } finally {
      viewerActionLoading = false;
    }
  };

  const shareViewerPost = async () => {
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
        throw new Error(readApiError(data, tr("No se pudo compartir la publicación.", "Could not share post.", "Impossible de partager la publication.")));
      }

      const shareUrlObject = new URL("/home_user.html", window.location.origin);
      shareUrlObject.searchParams.set("post", String(postId));
      const shareUrl = shareUrlObject.toString();

      try {
        if (navigator.share) {
          await navigator.share({
            title: "Kiadez",
            text: tr("Mira esta publicación", "See this post", "Voir cette publication"),
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
      setViewerStatus(tr("Publicación compartida.", "Post shared.", "Publication partagée."));
    } catch (error) {
      setViewerStatus(
        readUnknownError(error, tr("No se pudo compartir la publicación.", "Could not share post.", "Impossible de partager la publication.")),
        true
      );
    } finally {
      viewerActionLoading = false;
    }
  };

  const submitViewerComment = async () => {
    const postId = Number(currentViewerPost?.id || 0);
    if (!postId || viewerCommentSubmitting) return;

    const text = String(viewerCommentText || "").trim();
    if (!text) {
      setViewerStatus(tr("Escribe un comentario antes de enviar.", "Write a comment before sending.", "Écris un commentaire avant d'envoyer."), true);
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
        throw new Error(readApiError(data, tr("No se pudo guardar el comentario.", "Could not save comment.", "Impossible d'enregistrer le commentaire.")));
      }

      viewerCommentText = "";
      await Promise.all([
        loadViewerCommentsForPost(postId),
        loadRecentPostsOnly({ preferredViewerPostId: postId }),
      ]);
      setViewerStatus(tr("Comentario publicado.", "Comment posted.", "Commentaire publié."));
    } catch (error) {
      setViewerStatus(
        readUnknownError(error, tr("No se pudo guardar el comentario.", "Could not save comment.", "Impossible d'enregistrer le commentaire.")),
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
    initPurposeCoverModule();
    void syncProfileStarsTotal("galleryStarsTotal");
    void syncTopbarAvatar();
    const query = new URLSearchParams(window.location.search);
    const preferredAlbumId = Number(query.get("album") || 0);
    void loadGallery({
      preferredAlbumId: Number.isFinite(preferredAlbumId) ? preferredAlbumId : 0,
    });

    window.addEventListener("keydown", handleGlobalKeydown);

    return () => {
      window.removeEventListener("keydown", handleGlobalKeydown);
      clearAlbumFiles();
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{tr("Kiadez — Galería", "Kiadez — Gallery", "Kiadez — Galerie")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background gallery-page">
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
      <a class="topbar-btn" href="/home_user.html">🏠 Home</a>
      <a class="topbar-btn" href="/gallery.html">🖼️ {tr("Galería", "Gallery", "Galerie")}</a>
      <a class="topbar-btn" href="/my-public-whishes.html">🌐 {tr("Deseos públicos", "Public wishes", "Souhaits publics")}</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 {tr("Deseos privados", "Private wishes", "Souhaits privés")}</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html">✅ {tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</a>
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown">
        <summary class="topbar-avatar-btn" aria-label={tr("Perfil del usuario", "User profile", "Profil utilisateur")}>
          <img src="/assets/avatar-default.jpg" alt={tr("Foto de perfil del usuario", "User profile photo", "Photo de profil de l'utilisateur")} />
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

      <details class="topbar-dropdown">
        <summary class="topbar-menu-btn" aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}>
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">{tr("Menú", "Menu", "Navigation")}</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem">{tr("Mi Home", "My Home", "Mon accueil")}</a>
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
    <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt={tr("Portada", "Cover", "Couverture")} />

        <div class="cover-actions">
          <button class="icon-btn" id="btnChangeCover" type="button" title={tr("Cambiar portada", "Change cover", "Changer la couverture")}>
            {tr("Cambiar portada", "Change cover", "Changer la couverture")}
          </button>
          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button" title={tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier ma mission de vie")}>
            {tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier ma mission de vie")}
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="purpose-triangle" aria-label={tr("Deseos de propósito", "Purpose wishes", "Souhaits de mission")}>
          <button class="purpose-pill purpose-top" type="button" id="purpose1">
            {tr("Deseo #1: Secreto", "Wish #1: Secret", "Souhait n°1 : Secret")}
          </button>

          <button class="purpose-pill purpose-left" type="button" id="purpose2">
            {tr("Deseo construir el Reino de Combray", "I wish to build the Kingdom of Combray", "Je souhaite construire le Royaume de Combray")}
          </button>

          <button class="purpose-pill purpose-right" type="button" id="purpose3">
            {tr("Deseo estar unido a Jesús", "I wish to be united with Jesus", "Je souhaite être uni à Jésus")}
          </button>
        </div>

        <div class="cover-hint" id="coverHint">
          {tr("Arrastra la portada para encuadrarla", "Drag the cover to frame it", "Déplace la couverture pour l'ajuster")}
        </div>
      </div>
    </section>

    <div class="home-body gallery-body">
      <nav class="profile-nav" aria-label={tr("Navegación de perfil", "Profile navigation", "Navigation du profil")}>
        <a class="nav-pill" href="/home_user.html" title={tr("Home", "Home", "Accueil")}>{tr("Home", "Home", "Accueil")}</a>
        <a class="nav-pill" href="/star-pool-found.html" title={tr("Estrellas", "Stars", "Étoiles")}>
          <span class="nav-icon">⭐</span>
          <span><strong id="galleryStarsTotal">0</strong> {tr("estrellas", "stars", "étoiles")}</span>
        </a>

        <a class="nav-pill" href="/followers.html" title={tr("Seguidores", "Followers", "Abonnés")}>{tr("Seguidores", "Followers", "Abonnés")}</a>
        <a class="nav-pill" href="/achievements.html" title={tr("Logros recientes", "Recent achievements", "Réalisations récentes")}>{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
        <a class="nav-pill is-active" href="/gallery.html" title={tr("Galería", "Gallery", "Galerie")}>{tr("Galería", "Gallery", "Galerie")}</a>
        <a class="nav-pill" href="/calendar.html" title={tr("Calendario", "Calendar", "Calendrier")}>{tr("Calendario", "Calendar", "Calendrier")}</a>
        <a class="nav-pill" href="/my-biography.html" title={tr("Mi biografía", "My biography", "Ma biographie")}>{tr("Mi biografía", "My biography", "Ma biographie")}</a>
        <a class="nav-pill" href="/messages.html" title={tr("Mensajes", "Messages", "Messagerie")}>{tr("Mensajes", "Messages", "Messagerie")}</a>
      </nav>

      {#if isLoading}
        <section class="panel">
          <p class="panel-muted">{tr("Cargando tu galería...", "Loading your gallery...", "Chargement de ta galerie...")}</p>
        </section>
      {:else if loadError}
        <section class="panel">
          <p class="posts-status posts-status-error">{loadError}</p>
          <button class="btn btn-outline" type="button" on:click={() => loadGallery({ preserveFolder: true })}>
            {tr("Reintentar", "Retry", "Réessayer")}
          </button>
        </section>
      {:else}
        <section class="panel">
          <div class="panel-head gallery-head">
            <div>
              <h2 class="panel-title">{tr("Últimas imágenes", "Latest images", "Dernières images")}</h2>
            </div>
          </div>

          {#if statusMessage}
            <p class={`posts-status ${statusIsError ? "posts-status-error" : ""}`} aria-live="polite">
              {statusMessage}
            </p>
          {/if}

          {#if recentImagePosts.length === 0}
            <p class="panel-muted">
              {tr("Aún no tienes publicaciones con imagen.", "You do not have image posts yet.", "Tu n'as pas encore de publications avec image.")}
            </p>
          {:else}
            <div class="gallery-recent-grid" aria-label={tr("Publicaciones con imagen", "Posts with image", "Publications avec image")}>
              {#each recentImagePosts as post, index (post.id)}
                <article class="gallery-recent-item">
                  <button
                    class="gallery-recent-open"
                    type="button"
                    title={tr("Abrir publicación", "Open post", "Ouvrir la publication")}
                    on:click={() => openPostViewerAt(index)}
                  >
                    <img src={post.media_url} alt={`${tr("Publicación con imagen", "Post with image", "Publication avec image")} ${index + 1}`} loading="lazy" />
                  </button>
                </article>
              {/each}
            </div>
          {/if}
        </section>

        <section class="panel">
          <div class="panel-head">
            <h3 class="panel-title">{tr("Álbumes", "Albums", "Albums")}</h3>
            <span class="panel-badge">{folders.length} {tr("álbumes", "albums", "albums")}</span>
          </div>

          <div class="gallery-folders-layout">
            <aside class="gallery-folders-sidebar">
              <button class="gallery-album-create-card" type="button" on:click={openCreateAlbumModal}>
                <span class="gallery-album-create-plus">+</span>
                <span>{tr("Crear álbum", "Create album", "Créer un album")}</span>
              </button>

              {#if folders.length === 0}
                <p class="panel-muted">{tr("Aún no tienes álbumes. Crea el primero para publicar contenido agrupado.", "You do not have albums yet. Create the first one to publish grouped content.", "Tu n'as pas encore d'albums. Crée le premier pour publier du contenu groupé.")}</p>
              {:else}
                <div class="gallery-folder-list" aria-label={tr("Lista de álbumes", "Albums list", "Liste des albums")}>
                  {#each folders as folder (folder.id)}
                    <button
                      class={`gallery-folder-item ${String(folder.id) === String(activeFolderId) ? "is-active" : ""}`}
                      type="button"
                      on:click={() => selectFolder(folder.id)}
                    >
                      <strong>{folder.name}</strong>
                      <span>
                        {folder.images_count} {tr("archivo(s)", "file(s)", "fichier(s)")} · {folder.visibility === "private" ? tr("Privado", "Private", "Privé") : tr("Público", "Public", "Public")}
                      </span>
                    </button>
                  {/each}
                </div>
              {/if}
            </aside>

            <div class="gallery-folder-detail">
              {#if !activeFolderId}
                <div class="gallery-folder-placeholder">
                  <p class="panel-muted">{tr("Selecciona o crea un álbum para ver su contenido.", "Select or create an album to view its content.", "Sélectionne ou crée un album pour voir son contenu.")}</p>
                </div>
              {:else if folderDetailLoading}
                <div class="gallery-folder-placeholder">
                  <p class="panel-muted">{tr("Cargando álbum...", "Loading album...", "Chargement de l'album...")}</p>
                </div>
              {:else if activeFolderDetail}
                <div class="gallery-folder-head">
                  <div>
                    <h4>{activeFolderDetail.name}</h4>
                    <p>
                      {activeFolderDetail.images_count} {tr("archivo(s) en este álbum", "file(s) in this album", "fichier(s) dans cet album")} ·
                      {activeFolderDetail.visibility === "private" ? tr("Privado", "Private", "Privé") : tr("Público", "Public", "Public")}
                    </p>
                  </div>
                </div>

                <form class="gallery-rename-form" on:submit|preventDefault={handleRenameFolderSubmit}>
                  <input
                    class="modal-input"
                    type="text"
                    maxlength="120"
                    placeholder={tr("Nombre del álbum", "Album name", "Nom de l'album")}
                    bind:value={renameFolderName}
                  />
                  <button class="btn btn-outline" type="submit" disabled={renameLoading}>
                    {renameLoading ? tr("Guardando...", "Saving...", "Enregistrement...") : tr("Renombrar", "Rename", "Renommer")}
                  </button>
                  <button
                    class="btn btn-outline gallery-delete-folder-btn"
                    type="button"
                    on:click={deleteFolder}
                    disabled={deletingFolder}
                  >
                    {deletingFolder ? tr("Eliminando...", "Deleting...", "Suppression...") : tr("Eliminar álbum", "Delete album", "Supprimer l'album")}
                  </button>
                </form>

                {#if !activeFolderDetail.images || activeFolderDetail.images.length === 0}
                  <p class="panel-muted">
                    {tr("Este álbum está vacío.", "This album is empty.", "Cet album est vide.")}
                  </p>
                {:else}
                  <div class="gallery-folder-grid" aria-label={tr("Archivos del álbum", "Album files", "Fichiers de l'album")}>
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
                          title={tr("Quitar del álbum", "Remove from album", "Retirer de l'album")}
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
                  <p class="panel-muted">{tr("No se pudo cargar el contenido del álbum seleccionado.", "Could not load selected album content.", "Impossible de load selected album content.")}</p>
                </div>
              {/if}
            </div>
          </div>
        </section>
      {/if}
    </div>
  </main>

  {#if showCreateAlbumModal}
    <div class="modal-overlay gallery-album-modal-overlay" aria-hidden="false">
      <button
        class="gallery-album-modal-backdrop"
        type="button"
        aria-label={tr("Cerrar creación de álbum", "Close album creation", "Fermer la création d'album")}
        on:click={closeCreateAlbumModal}
      ></button>
      <div class="modal gallery-album-modal" role="dialog" aria-modal="true" aria-label={tr("Crear álbum", "Create album", "Créer un album")}>
        <div class="modal-head">
          <h3>{tr("Crear álbum", "Create album", "Créer un album")}</h3>
          <button class="modal-close" type="button" on:click={closeCreateAlbumModal}>✕</button>
        </div>

        <div class="modal-body gallery-album-modal-body">
          <label class="modal-label" for="galleryAlbumNameInput">{tr("Nombre del álbum", "Album name", "Nom de l'album")}</label>
          <input
            id="galleryAlbumNameInput"
            class="modal-input"
            type="text"
            maxlength="120"
            placeholder={tr("Ejemplo: Viaje de verano", "Example: Summer trip", "Exemple : Voyage d'été")}
            bind:value={albumName}
          />

          <label class="modal-label" for="galleryAlbumVisibilitySelect">{tr("Visibilidad", "Visibility", "Visibilité")}</label>
          <select
            id="galleryAlbumVisibilitySelect"
            class="modal-select"
            bind:value={albumVisibility}
          >
            <option value="public">{tr("Público", "Public", "Public")}</option>
            <option value="private">{tr("Privado", "Private", "Privé")}</option>
          </select>

          <label class="modal-label" for="galleryAlbumFilesInput">
            {tr("Subir contenido: fotos/videos 🖼️", "Upload content: photos/videos 🖼️", "Téléverser du contenu : photos/vidéos 🖼️")}
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
            <strong>{tr("Previsualización", "Preview", "Aperçu")}</strong>
            <span>{albumFiles.length} {tr("archivo(s)", "file(s)", "fichier(s)")}</span>
          </div>

          {#if albumFiles.length === 0}
            <p class="panel-muted">{tr("Aún no has seleccionado archivos para este álbum.", "You have not selected files for this album yet.", "Tu n'as pas encore sélectionné de fichiers pour cet album.")}</p>
          {:else}
            <div class="gallery-album-preview-grid" aria-label={tr("Previsualización del álbum", "Album preview", "Aperçu de l'album")}>
              {#each albumFiles as item, index (`${item.name}-${index}`)}
                <article class="gallery-album-preview-card">
                  {#if item.media_kind === "video"}
                    <video src={item.preview_url} controls preload="metadata">
                      <track kind="captions" />
                    </video>
                  {:else}
                    <img src={item.preview_url} alt={`${tr("Archivo", "File", "Fichier")} ${index + 1}`} loading="lazy" />
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
            {tr("Cancelar", "Cancel", "Annuler")}
          </button>
          <button
            class="btn btn-primary btn-compact"
            type="button"
            on:click={publishAlbum}
            disabled={albumPublishing}
          >
            {albumPublishing ? tr("Publicando...", "Publishing...", "Publication...") : tr("Publicar álbum", "Publish album", "Publier l'album")}
          </button>
        </div>
      </div>
    </div>
  {/if}

  {#if showPostViewer && currentViewerPost}
    <div class="modal-overlay gallery-post-viewer-overlay" aria-hidden="false">
      <button class="gallery-post-viewer-backdrop" type="button" aria-label={tr("Cerrar publicación", "Close post", "Fermer la publication")} on:click={closePostViewer}></button>
      <div class="modal gallery-post-viewer" role="dialog" aria-modal="true" aria-label={tr("Publicación con imagen", "Post with image", "Publication avec image")}>
        <div class="modal-head">
          <h3>{tr("Publicación con imagen", "Post with image", "Publication avec image")}</h3>
          <button class="modal-close" type="button" on:click={closePostViewer}>✕</button>
        </div>

        <div class="gallery-post-viewer-layout">
          <section class="gallery-post-viewer-media">
            <button
              class="gallery-post-viewer-nav gallery-post-viewer-nav-prev"
              type="button"
              on:click={() => void goViewerPrev()}
              disabled={!viewerCanPrev}
              aria-label={tr("Imagen anterior", "Previous image", "Image précédente")}
            >
              ‹
            </button>

            <img src={currentViewerPost.media_url} alt={tr("Publicación en vista completa", "Full view post", "Voir la publication en grand")} loading="eager" />

            <button
              class="gallery-post-viewer-nav gallery-post-viewer-nav-next"
              type="button"
              on:click={() => void goViewerNext()}
              disabled={!viewerCanNext}
              aria-label={tr("Siguiente imagen", "Next image", "Image suivante")}
            >
              ›
            </button>

            <p class="gallery-post-viewer-counter">{viewerPostIndex + 1} {tr("de", "of", "de")} {recentImagePosts.length}</p>
          </section>

          <aside class="gallery-post-viewer-side">
            <header class="gallery-post-viewer-author">
              <strong>{currentViewerPost.author?.name || tr("Usuario", "User", "Utilisateur")}</strong>
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
                  ⭐ {tr("Estrella donada", "Star donated", "Étoile donnée")} ({currentViewerPost.star_count})
                {:else}
                  ⭐ {tr("Donar estrella", "Donate star", "Donner une étoile")} ({currentViewerPost.star_count})
                {/if}
              </button>

              <button class="post-btn" type="button" on:click={focusViewerCommentInput}>
                💬 {tr("Comentar", "Comment", "Commenter")} ({currentViewerPost.comment_count})
              </button>

              <button
                class="post-btn"
                type="button"
                on:click={shareViewerPost}
                disabled={viewerActionLoading}
              >
                🔁 {tr("Compartir", "Share", "Partager")} ({currentViewerPost.share_count})
              </button>
            </div>

            {#if viewerStatusMessage}
              <p class={`posts-status ${viewerStatusIsError ? "posts-status-error" : ""}`} aria-live="polite">
                {viewerStatusMessage}
              </p>
            {/if}

            <section class="gallery-post-viewer-comments">
              <h4>{tr("Comentarios", "Comments", "Commentaires")}</h4>

              {#if viewerCommentsLoading}
                <p class="panel-muted">{tr("Cargando comentarios...", "Loading comments...", "Chargement des commentaires...")}</p>
              {:else if viewerComments.length === 0}
                <p class="post-comments-empty">{tr("Aún no hay comentarios.", "There are no comments yet.", "Il n'y a pas encore de commentaires.")}</p>
              {:else}
                <div class="post-comments-list gallery-viewer-comments-list">
                  {#each viewerComments as comment (comment.id)}
                    <article class="post-comment-item">
                      <div class="post-comment-head">
                        <strong>{comment.author?.name || tr("Usuario", "User", "Utilisateur")}</strong>
                        <span>{relativeTime(comment.created_at)}</span>
                      </div>
                      <p>{@html escapeHtml(comment.text)}</p>
                    </article>
                  {/each}
                </div>
              {/if}
            </section>

            <form class="gallery-post-viewer-comment-form" on:submit|preventDefault={submitViewerComment}>
              <textarea
                id="galleryViewerCommentInput"
                class="modal-textarea gallery-post-viewer-comment-input"
                rows="3"
                maxlength="1200"
                placeholder={tr("Escribe un comentario...", "Write a comment...", "Écris un commentaire...")}
                bind:value={viewerCommentText}
              ></textarea>
              <div class="gallery-post-viewer-comment-actions">
                <button
                  class="btn btn-primary btn-compact"
                  type="submit"
                  disabled={viewerCommentSubmitting}
                >
                  {viewerCommentSubmitting ? tr("Enviando...", "Sending...", "Envoi...") : tr("Comentar", "Comment", "Commenter")}
                </button>
              </div>
            </form>
          </aside>
        </div>
      </div>
    </div>
  {/if}
  <AuthFooter />
</div>
