<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { syncTopbarAvatar } from "../lib/topbarAvatar";

  const API = "http://127.0.0.1:8000";
  const FEED_LIMIT = 40;
  const MINOR_FEED_COLLAPSED_KEY = "feed_minor_protected_collapsed";

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
    try {
      localStorage.setItem(MINOR_FEED_COLLAPSED_KEY, minorProtectedCollapsed ? "1" : "0");
    } catch (error) {
      console.warn(error);
    }
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

      applyFeedPosts(data);
    } catch (error) {
      feedError = readUnknownError(error, "No se pudo cargar el feed.");
      applyFeedPosts([]);
    } finally {
      feedLoading = false;
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
      setPostsStatus("Estrella donada. Esta acción es irreversible.");
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

  onMount(() => {
    void syncTopbarAvatar();

    const cleanupFns = [];
    let previewObjectUrl = "";
    try {
      minorProtectedCollapsed = localStorage.getItem(MINOR_FEED_COLLAPSED_KEY) === "1";
    } catch (error) {
      console.warn(error);
      minorProtectedCollapsed = false;
    }

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

    document.querySelectorAll(".mini-action").forEach((btn) => {
      bind(btn, "click", openPost);
    });

    bind(closePostModal, "click", closePost);
    bind(cancelPost, "click", closePost);
    bind(postModalOverlay, "click", (event) => {
      if (event.target === postModalOverlay) closePost();
    });

    bind(postFile, "change", (event) => {
      const file = event?.target?.files?.[0];
      if (!file) return;

      resetPreview();
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

      postPreview.innerHTML = "";
      postPreview.classList.add("hidden");
    });

    bind(publishPostBtn, "click", () => {
      if (minorProtectedVisible && postVisibility?.value === "public") {
        postVisibility.value = "private";
        setPostsStatus("Tu cuenta está en modo protegido. La publicación se guardará en privado.");
      } else {
        setPostsStatus("Publicación creada (mock).");
      }
      alert("Publicación creada (mock). En backend luego la guardamos en DB.");
      closePost();
    });

    const oracleBlock = document.querySelector(".oracle-response-block");
    const oracleToggle = document.getElementById("oracleToggle");
    const oracleResponseText = document.getElementById("oracleResponseText");
    const oracleEmptyPrompt = document.getElementById("oracleEmptyPrompt");
    const hasOracleResponse = oracleBlock?.dataset.hasResponse !== "false";

    if (!hasOracleResponse) {
      oracleResponseText?.classList.add("hidden");
      oracleEmptyPrompt?.classList.remove("hidden");
      if (oracleToggle) oracleToggle.checked = false;
    }

    const syncOracleVisibility = () => {
      if (!oracleToggle || !oracleResponseText) return;
      if (!oracleToggle.checked || !hasOracleResponse) {
        oracleResponseText.classList.add("hidden");
      } else {
        oracleResponseText.classList.remove("hidden");
      }
    };

    bind(oracleToggle, "change", syncOracleVisibility);
    syncOracleVisibility();

    void (async () => {
      await Promise.all([loadFeed(), loadMinorAccreditationStatus()]);
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
              <img src="/css/oracle/Oracle1.png" alt="Última carta del Oráculo" />
            </div>

            <div class="oracle-response-block" data-has-response="true">
              <div class="oracle-toggle">
                <span class="oracle-toggle-label">Mostrar respuesta</span>
                <label class="switch">
                  <input type="checkbox" id="oracleToggle" checked />
                  <span class="slider"></span>
                </label>
              </div>

              <div class="oracle-response-title">Descripción de su respuesta:</div>
              <p class="oracle-response" id="oracleResponseText">
                “Cada paso que das hacia tu propósito abre nuevas puertas. La perseverancia será tu escudo
                hoy. Comparte tu avance y deja que otros también se inspiren.”
              </p>

              <button class="btn btn-outline btn-compact oracle-empty hidden" id="oracleEmptyPrompt" type="button">
                Responder ahora y publicar
              </button>
            </div>
          </article>
        </aside>

        <!-- =========================
         *  LADO CENTRAL
         *  ========================= -->
        <section class="feed-center">
          <article class="panel composer">
            <div class="composer-row">
              <img class="avatar avatar-sm" src="/assets/avatar-default.jpg" alt="Avatar" />
              <button class="composer-input" id="openPostModal" type="button">
                Publica algo que motive a tus seguidores...
              </button>
            </div>

            <div class="composer-actions">
              <button class="mini-action" type="button" data-kind="text">Texto</button>
              <button class="mini-action" type="button" data-kind="image">Imagen</button>
              <button class="mini-action" type="button" data-kind="video">Video</button>
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

          {#if feedLoading}
            <article class="panel post post-empty">
              <p class="post-text">Cargando publicaciones del feed...</p>
            </article>
          {:else if feedError}
            <article class="panel post post-empty">
              <p class="posts-status posts-status-error">{feedError}</p>
              <button class="btn btn-outline" type="button" on:click={() => void loadFeed()}>
                Reintentar
              </button>
            </article>
          {:else if displayPosts.length === 0}
            <article class="panel post post-empty">
              <p class="post-text">Aún no hay publicaciones en tu feed.</p>
            </article>
          {:else}
            {#each displayPosts as post (post.id)}
              {@const isAlbumGroup = post.__kind === "album" && Number(post.album_total_items || 0) > 1}
              {@const authorProfileUrl = buildAuthorProfileUrl(post?.author)}
              <article class="panel post">
                <div class="post-head">
                  <div>
                    <a class="post-author-link" href={authorProfileUrl}>{post.author?.name || "Usuario"}</a>
                    <span class="post-meta">
                      · {relativeTime(post.created_at)} · {post.visibility === "private" ? "Privado" : "Público"}
                    </span>
                  </div>
                </div>

                {#if isAlbumGroup}
                  <p class="post-album-meta">
                    {post.album_name || "Álbum"} · {Number(post.album_total_items || 0)} archivo(s)
                  </p>
                {/if}

                {#if post.text}
                  <p class="post-text">{post.text}</p>
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

                <p class="post-warning">La donación de estrella es irreversible.</p>

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
              <a class="feed-profile-link" href="/home_user.html">
                <img class="avatar" src="/assets/avatar-default.jpg" alt="Foto de perfil" />
              </a>
              <div class="profile-meta">
                <a class="profile-name feed-profile-link" href="/home_user.html">Carlos Jiménez Duarte</a>
                <p class="profile-rank">@carlosjduarte</p>
                <a class="btn btn-outline btn-compact" href="/home_user.html">Ver perfil</a>
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

          <article class="panel guardian-panel">
            <h3 class="panel-title">Yo soy Guardián</h3>
            <p class="panel-muted">Escenario de gestión y notificaciones para Guardianes activos.</p>
            <a class="btn btn-primary btn-compact" href="/guardiancenter.html">Entrar al módulo de Guardianes</a>
          </article>

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
          <img class="avatar avatar-sm" src="/assets/avatar-default.jpg" alt="Avatar" />
          <div>
            <div class="post-modal-name"><strong>Carlos Jiménez Duarte</strong></div>
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
