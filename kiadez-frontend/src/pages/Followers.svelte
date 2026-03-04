<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";
  import { syncTopbarAvatar } from "../lib/topbarAvatar";
  import { followApi } from "../lib/api";

  const PAGE_SIZE = 25;
  const PAGE_WINDOW = 7;
  const DEFAULT_AVATAR_SRC = "/assets/avatar-default.jpg";

  let pageTitle = "Kiadez — Seguidores";
  let isViewingOwnProfile = true;
  let viewerUserId = null;
  let viewerUsername = "";
  let activeProfileUserId = null;
  let activeProfileUsername = "";
  let activeProfileFullName = "";
  let profileStarsTotal = null;

  const createSectionState = () => ({
    items: [],
    page: 1,
    page_size: PAGE_SIZE,
    total: 0,
    total_pages: 1,
    range_start: 0,
    range_end: 0,
    loading: false,
    error: "",
  });

  let suggestions = createSectionState();
  let followers = createSectionState();
  let following = createSectionState();

  let followActionError = "";
  let pendingFollowIds = new Set();

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

  const apiFetch = async (path, options = {}) => {
    const token = getAccessToken();
    if (!token) {
      window.location.href = "/login.html";
      throw new Error("No hay sesión activa.");
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    };

    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") || "http://localhost:8000"}${path}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("kiadez_access_token");
      window.location.href = "/login.html";
      throw new Error("Sesión expirada. Inicia sesión nuevamente.");
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
      ? "Kiadez — Seguidores"
      : `Kiadez — Red de ${activeProfileFullName || "usuario"}`;
  };

  const syncStarsLabel = () => {
    const label = document.getElementById("followersStarsTotal");
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
    isViewingOwnProfile = true;
    profileStarsTotal = null;
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

  const parseErrorMessage = (error) => {
    const message = String(error?.message || "").trim();
    return message || "No se pudo completar la solicitud.";
  };

  const formatCount = (value) => Number(value || 0).toLocaleString("es-CO");

  const getDisplayName = (item) => {
    const fullName = String(item?.full_name || "").trim();
    if (fullName) return fullName;
    const userId = Number(item?.user_id || 0);
    return userId > 0 ? `Usuario ${userId}` : "Usuario";
  };

  const getHandle = (item) => {
    const handle = String(item?.handle || "").trim();
    if (handle) return handle;
    const username = String(item?.username || "").trim();
    if (username) return `@${username}`;
    const userId = Number(item?.user_id || 0);
    return userId > 0 ? `@id${userId}` : "@usuario";
  };

  const getProfileHref = (item) => {
    const href = String(item?.profile_url || "").trim();
    return href || "/home_user.html";
  };

  const getAvatarSrc = (item) => {
    const url = String(item?.avatar_url || "").trim();
    return url || DEFAULT_AVATAR_SRC;
  };

  const isFollowPending = (userId) => pendingFollowIds.has(Number(userId));

  const setFollowPending = (userId, pending) => {
    const normalizedId = Number(userId);
    const next = new Set(pendingFollowIds);
    if (pending) {
      next.add(normalizedId);
    } else {
      next.delete(normalizedId);
    }
    pendingFollowIds = next;
  };

  const getState = (section) => {
    if (section === "suggestions") return suggestions;
    if (section === "followers") return followers;
    return following;
  };

  const setState = (section, patch) => {
    if (section === "suggestions") {
      suggestions = { ...suggestions, ...patch };
      return;
    }
    if (section === "followers") {
      followers = { ...followers, ...patch };
      return;
    }
    following = { ...following, ...patch };
  };

  const getFetcher = (section) => {
    if (section === "suggestions") return followApi.listSuggestions;
    if (section === "followers") return followApi.listFollowers;
    return followApi.listFollowing;
  };

  const buildVisiblePages = (sectionState) => {
    const totalPages = Math.max(1, Number(sectionState?.total_pages || 1));
    const currentPage = Math.max(1, Math.min(Number(sectionState?.page || 1), totalPages));

    if (totalPages <= PAGE_WINDOW) {
      return Array.from({ length: totalPages }, (_, index) => index + 1);
    }

    const side = Math.floor(PAGE_WINDOW / 2);
    let start = Math.max(1, currentPage - side);
    let end = Math.min(totalPages, start + PAGE_WINDOW - 1);

    if (end - start + 1 < PAGE_WINDOW) {
      start = Math.max(1, end - PAGE_WINDOW + 1);
    }

    return Array.from({ length: end - start + 1 }, (_, index) => start + index);
  };

  const loadSection = async (section, requestedPage = 1) => {
    const fetcher = getFetcher(section);
    const normalizedPage = Math.max(1, Number(requestedPage || 1));
    const targetUserId = parsePositiveId(activeProfileUserId);

    setState(section, {
      loading: true,
      error: "",
    });

    try {
      const params = {
        page: normalizedPage,
        page_size: PAGE_SIZE,
      };
      if (section !== "suggestions" && targetUserId) {
        params.user_id = targetUserId;
      }
      const data = await fetcher(params);

      setState(section, {
        items: Array.isArray(data?.items) ? data.items : [],
        page: Math.max(1, Number(data?.page) || normalizedPage),
        page_size: Math.max(1, Number(data?.page_size) || PAGE_SIZE),
        total: Math.max(0, Number(data?.total) || 0),
        total_pages: Math.max(1, Number(data?.total_pages) || 1),
        range_start: Math.max(0, Number(data?.range_start) || 0),
        range_end: Math.max(0, Number(data?.range_end) || 0),
        loading: false,
        error: "",
      });
    } catch (error) {
      setState(section, {
        loading: false,
        items: [],
        error: parseErrorMessage(error),
      });
    }
  };

  const refreshAllSections = async () => {
    const tasks = [
      loadSection("followers", followers.page),
      loadSection("following", following.page),
    ];
    if (isViewingOwnProfile) {
      tasks.unshift(loadSection("suggestions", suggestions.page));
    } else {
      suggestions = createSectionState();
    }
    await Promise.all(tasks);
  };

  const goToPage = (section, page) => {
    const state = getState(section);
    const totalPages = Math.max(1, Number(state.total_pages || 1));
    const normalizedPage = Math.max(1, Math.min(Number(page || 1), totalPages));
    if (normalizedPage === state.page) return;
    void loadSection(section, normalizedPage);
  };

  const toggleFollow = async (item) => {
    const userId = Number(item?.user_id || 0);
    if (!userId || isFollowPending(userId)) return;

    const shouldFollow = !item.is_following;
    followActionError = "";
    setFollowPending(userId, true);

    try {
      if (shouldFollow) {
        await followApi.follow(userId);
      } else {
        await followApi.unfollow(userId);
      }
      await refreshAllSections();
    } catch (error) {
      followActionError = parseErrorMessage(error);
    } finally {
      setFollowPending(userId, false);
    }
  };

  onMount(() => {
    let cleanupPurposeCover = () => {};
    void syncTopbarAvatar();

    (async () => {
      try {
        await resolveProfileContext();
        cleanupPurposeCover = initPurposeCoverModule({
          isOwnProfile: isViewingOwnProfile,
          profileUserId: activeProfileUserId,
        });
        if (isViewingOwnProfile) {
          const stars = await syncProfileStarsTotal("followersStarsTotal");
          if (stars !== null && stars !== undefined) {
            profileStarsTotal = Number(stars || 0);
            syncStarsLabel();
          }
        }
      } catch (error) {
        followActionError = parseErrorMessage(error);
      }
      await refreshAllSections();
    })();

    return () => {
      cleanupPurposeCover?.();
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{pageTitle}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background followers-page">
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
          <img src="/assets/avatar-default.jpg" alt="Perfil del usuario" />
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

    <div class="home-body">
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home" data-profile-module="home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas" data-profile-module="stars">
          <span class="nav-icon">⭐</span>
          <span><strong id="followersStarsTotal">0</strong> estrellas</span>
        </a>
        <a class="nav-pill" href="/followers.html" title="Seguidores" data-profile-module="followers">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes" data-profile-module="achievements">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería" data-profile-module="gallery">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario" data-profile-module="calendar">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía" data-profile-module="biography">Mi biografía</a>
        <a class="nav-pill" href="/messages.html" title="Mensajes">Mensajes</a>
      </nav>

      {#if followActionError}
        <section class="panel followers-message-panel" aria-live="polite">
          <p class="followers-status is-error">{followActionError}</p>
        </section>
      {/if}

      {#if isViewingOwnProfile}
      <section class="panel followers-section" aria-label="Sugerencias de usuarios a seguir">
        <div class="panel-head">
          <h2 class="panel-title">Sugerencias de usuarios a seguir</h2>
          <span class="panel-badge">{formatCount(suggestions.total)} sugerencias</span>
        </div>
        <p class="panel-muted">
          Modelos a seguir priorizados por guardianes, usuarios recientes y perfiles destacados.
        </p>

        {#if suggestions.error}
          <p class="followers-status is-error">{suggestions.error}</p>
        {:else if suggestions.loading}
          <p class="followers-status">Cargando sugerencias...</p>
        {:else if suggestions.items.length === 0}
          <p class="followers-status">No hay sugerencias disponibles por ahora.</p>
        {:else}
          <div class="followers-grid">
            {#each suggestions.items as item (item.user_id)}
              <article class="follower-card">
                <a class="follower-avatar-link" href={getProfileHref(item)} aria-label={`Ver perfil de ${getDisplayName(item)}`}>
                  <img class="follower-avatar" src={getAvatarSrc(item)} alt={`Foto de perfil de ${getDisplayName(item)}`} loading="lazy" />
                </a>
                <h3 class="follower-name">{getDisplayName(item)}</h3>
                <p class="follower-handle">{getHandle(item)}</p>
                <p class="follower-count">{formatCount(item.followers_count)} seguidores</p>
                <div class="follower-actions">
                  <button
                    class={`btn btn-compact${item.is_following ? " btn-outline" : " btn-primary"}`}
                    type="button"
                    disabled={isFollowPending(item.user_id)}
                    on:click={() => toggleFollow(item)}
                  >
                    {#if isFollowPending(item.user_id)}
                      Procesando...
                    {:else if item.is_following}
                      Dejar de seguir
                    {:else}
                      Seguir
                    {/if}
                  </button>
                  <a class="btn btn-outline btn-compact" href={getProfileHref(item)}>Ver perfil</a>
                </div>
              </article>
            {/each}
          </div>
        {/if}

        {#if suggestions.total_pages > 1}
          <nav class="followers-pagination" aria-label="Paginación de sugerencias">
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label="Página anterior"
              on:click={() => goToPage("suggestions", suggestions.page - 1)}
              disabled={suggestions.page <= 1}
            >
              &lt;&lt;
            </button>
            {#each buildVisiblePages(suggestions) as page}
              <button
                class={`followers-page-btn${page === suggestions.page ? " is-active" : ""}`}
                type="button"
                aria-current={page === suggestions.page ? "page" : undefined}
                on:click={() => goToPage("suggestions", page)}
              >
                {page}
              </button>
            {/each}
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label="Página siguiente"
              on:click={() => goToPage("suggestions", suggestions.page + 1)}
              disabled={suggestions.page >= suggestions.total_pages}
            >
              &gt;&gt;
            </button>
          </nav>
        {/if}

        {#if !suggestions.loading && !suggestions.error && suggestions.total > 0}
          <p class="followers-range">
            Mostrando {suggestions.range_start}-{suggestions.range_end} de {formatCount(suggestions.total)} sugerencias.
          </p>
        {/if}
      </section>
      {/if}

      <section class="panel followers-section" aria-label="Seguidores">
        <div class="panel-head">
          <h2 class="panel-title">Seguidores</h2>
          <span class="panel-badge">{formatCount(followers.total)} seguidores</span>
        </div>
        <p class="panel-muted">
          {isViewingOwnProfile
            ? "Personas que siguen tu camino y celebran tus logros."
            : "Personas que siguen el camino de este perfil y celebran sus logros."}
        </p>

        {#if followers.error}
          <p class="followers-status is-error">{followers.error}</p>
        {:else if followers.loading}
          <p class="followers-status">Cargando seguidores...</p>
        {:else if followers.items.length === 0}
          <p class="followers-status">Aún no tienes seguidores registrados.</p>
        {:else}
          <div class="followers-grid">
            {#each followers.items as item (item.user_id)}
              <article class="follower-card">
                <a class="follower-avatar-link" href={getProfileHref(item)} aria-label={`Ver perfil de ${getDisplayName(item)}`}>
                  <img class="follower-avatar" src={getAvatarSrc(item)} alt={`Foto de perfil de ${getDisplayName(item)}`} loading="lazy" />
                </a>
                <h3 class="follower-name">{getDisplayName(item)}</h3>
                <p class="follower-handle">{getHandle(item)}</p>
                <p class="follower-count">{formatCount(item.followers_count)} seguidores</p>
                <div class="follower-actions">
                  <button
                    class={`btn btn-compact${item.is_following ? " btn-outline" : " btn-primary"}`}
                    type="button"
                    disabled={isFollowPending(item.user_id)}
                    on:click={() => toggleFollow(item)}
                  >
                    {#if isFollowPending(item.user_id)}
                      Procesando...
                    {:else if item.is_following}
                      Dejar de seguir
                    {:else}
                      Seguir
                    {/if}
                  </button>
                  <a class="btn btn-outline btn-compact" href={getProfileHref(item)}>Ver perfil</a>
                </div>
              </article>
            {/each}
          </div>
        {/if}

        {#if followers.total_pages > 1}
          <nav class="followers-pagination" aria-label="Paginación de seguidores">
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label="Página anterior"
              on:click={() => goToPage("followers", followers.page - 1)}
              disabled={followers.page <= 1}
            >
              &lt;&lt;
            </button>
            {#each buildVisiblePages(followers) as page}
              <button
                class={`followers-page-btn${page === followers.page ? " is-active" : ""}`}
                type="button"
                aria-current={page === followers.page ? "page" : undefined}
                on:click={() => goToPage("followers", page)}
              >
                {page}
              </button>
            {/each}
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label="Página siguiente"
              on:click={() => goToPage("followers", followers.page + 1)}
              disabled={followers.page >= followers.total_pages}
            >
              &gt;&gt;
            </button>
          </nav>
        {/if}

        {#if !followers.loading && !followers.error && followers.total > 0}
          <p class="followers-range">
            Mostrando {followers.range_start}-{followers.range_end} de {formatCount(followers.total)} seguidores.
          </p>
        {/if}
      </section>

      <section class="panel followers-section" aria-label="Siguiendo">
        <div class="panel-head">
          <h2 class="panel-title">{isViewingOwnProfile ? "Siguiendo" : "Usuarios que sigue"}</h2>
          <span class="panel-badge">{formatCount(following.total)} siguiendo</span>
        </div>
        <p class="panel-muted">
          {isViewingOwnProfile
            ? "Usuarios a quienes sigues actualmente."
            : "Usuarios a quienes este perfil sigue actualmente."}
        </p>

        {#if following.error}
          <p class="followers-status is-error">{following.error}</p>
        {:else if following.loading}
          <p class="followers-status">Cargando usuarios seguidos...</p>
        {:else if following.items.length === 0}
          <p class="followers-status">Aún no sigues a ningún usuario.</p>
        {:else}
          <div class="followers-grid">
            {#each following.items as item (item.user_id)}
              <article class="follower-card">
                <a class="follower-avatar-link" href={getProfileHref(item)} aria-label={`Ver perfil de ${getDisplayName(item)}`}>
                  <img class="follower-avatar" src={getAvatarSrc(item)} alt={`Foto de perfil de ${getDisplayName(item)}`} loading="lazy" />
                </a>
                <h3 class="follower-name">{getDisplayName(item)}</h3>
                <p class="follower-handle">{getHandle(item)}</p>
                <p class="follower-count">{formatCount(item.followers_count)} seguidores</p>
                <div class="follower-actions">
                  <button
                    class={`btn btn-compact${item.is_following ? " btn-outline" : " btn-primary"}`}
                    type="button"
                    disabled={isFollowPending(item.user_id)}
                    on:click={() => toggleFollow(item)}
                  >
                    {#if isFollowPending(item.user_id)}
                      Procesando...
                    {:else if item.is_following}
                      Dejar de seguir
                    {:else}
                      Seguir
                    {/if}
                  </button>
                  <a class="btn btn-outline btn-compact" href={getProfileHref(item)}>Ver perfil</a>
                </div>
              </article>
            {/each}
          </div>
        {/if}

        {#if following.total_pages > 1}
          <nav class="followers-pagination" aria-label="Paginación de siguiendo">
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label="Página anterior"
              on:click={() => goToPage("following", following.page - 1)}
              disabled={following.page <= 1}
            >
              &lt;&lt;
            </button>
            {#each buildVisiblePages(following) as page}
              <button
                class={`followers-page-btn${page === following.page ? " is-active" : ""}`}
                type="button"
                aria-current={page === following.page ? "page" : undefined}
                on:click={() => goToPage("following", page)}
              >
                {page}
              </button>
            {/each}
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label="Página siguiente"
              on:click={() => goToPage("following", following.page + 1)}
              disabled={following.page >= following.total_pages}
            >
              &gt;&gt;
            </button>
          </nav>
        {/if}

        {#if !following.loading && !following.error && following.total > 0}
          <p class="followers-range">
            Mostrando {following.range_start}-{following.range_end} de {formatCount(following.total)} seguidos.
          </p>
        {/if}
      </section>
    </div>
  </main>

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
