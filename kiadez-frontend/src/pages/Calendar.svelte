<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";

  const API = "http://127.0.0.1:8000";

  let isViewingOwnProfile = true;
  let viewerUserId = null;
  let viewerUsername = "";
  let activeProfileUserId = null;
  let activeProfileUsername = "";
  let activeProfileFullName = "";

  let pageTitle = "Kiadez — Calendario";
  let calendarTitle = "Calendario 2026";
  let calendarAllowed = true;
  let calendarAccessError = "";

  const getAccessToken = () =>
    localStorage.getItem("access_token") || localStorage.getItem("kiadez_access_token") || "";

  const parseResponseJson = async (res) => {
    try {
      return await res.json();
    } catch {
      return {};
    }
  };

  const apiFetch = async (path, options = {}) => {
    const token = getAccessToken();
    if (!token) {
      throw new Error("No hay sesión activa.");
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    };
    const res = await fetch(`${API}${path}`, { ...options, headers });
    if (res.status === 401) {
      throw new Error("Sesión expirada. Inicia sesión nuevamente.");
    }
    return res;
  };

  const normalizeUsername = (value) => {
    let normalized = String(value || "").trim().toLowerCase();
    while (normalized.startsWith("@")) normalized = normalized.slice(1);
    return normalized;
  };

  const fetchViewerIdentity = async () => {
    const res = await apiFetch("/auth/me");
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(data.detail || "No se pudo cargar tu perfil.");
    }
    const userId = Number(data?.user_number);
    return {
      user_id: Number.isFinite(userId) && userId > 0 ? userId : null,
      username: normalizeUsername(data?.username || ""),
    };
  };

  const fetchFollowProfile = async ({ userId = null, username = null } = {}) => {
    const idValue = Number(userId);
    const usernameValue = normalizeUsername(username || "");
    if (Number.isFinite(idValue) && idValue > 0) {
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

  const buildViewerHomeUrl = () => {
    if (viewerUsername) return `/home_user.html?u=${encodeURIComponent(viewerUsername)}`;
    if (viewerUserId) return `/home_user.html?id=${encodeURIComponent(String(viewerUserId))}`;
    return "/home_user.html";
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
      return `${url.pathname}${url.search}`;
    } catch {
      return raw;
    }
  };

  const PROFILE_MODULE_ROUTES = {
    home: "/home_user.html",
    public_wishes: "/my-public-whishes.html",
    fulfilled_wishes: "/my-fulfilled-whises.html",
    calendar: "/calendar.html",
    oracle: "/oracle.html",
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

  const applyCalendarHeader = () => {
    pageTitle = isViewingOwnProfile
      ? "Kiadez — Calendario"
      : `Kiadez — Calendario de ${activeProfileFullName || "usuario"}`;
    calendarTitle = isViewingOwnProfile
      ? "Calendario 2026"
      : `Calendario de ${activeProfileFullName || "usuario"} · 2026`;
  };

  const checkCalendarVisibility = async () => {
    if (isViewingOwnProfile) {
      calendarAllowed = true;
      calendarAccessError = "";
      return;
    }
    const profileId = Number(activeProfileUserId);
    if (!Number.isFinite(profileId) || profileId <= 0) {
      calendarAllowed = true;
      calendarAccessError = "";
      return;
    }

    try {
      const res = await apiFetch(`/privacy/user/${encodeURIComponent(String(profileId))}`);
      const data = await parseResponseJson(res);
      if (!res.ok) {
        calendarAllowed = true;
        calendarAccessError = "";
        return;
      }
      calendarAllowed = Boolean(data?.public_profile_show_calendar);
      calendarAccessError = calendarAllowed ? "" : "Este calendario es privado.";
    } catch (error) {
      console.error(error);
      calendarAllowed = true;
      calendarAccessError = "";
    }
  };

  const resolveProfileContext = async () => {
    const params = new URLSearchParams(window.location.search);
    const requestedIdRaw = params.get("id");
    const requestedId = Number(requestedIdRaw);
    const requestedUserId =
      Number.isFinite(requestedId) && requestedId > 0 ? requestedId : null;
    const requestedUsername = normalizeUsername(params.get("u") || "");

    const me = await fetchViewerIdentity();
    viewerUserId = me.user_id;
    viewerUsername = me.username;

    activeProfileUserId = viewerUserId;
    activeProfileUsername = viewerUsername;
    activeProfileFullName = "";
    isViewingOwnProfile = true;
    document.body.dataset.visitor = "false";
    calendarAllowed = true;
    calendarAccessError = "";

    const wantsOtherProfile = Boolean(requestedUserId || requestedUsername);
    if (wantsOtherProfile) {
      const isSelfById = requestedUserId && viewerUserId && requestedUserId === viewerUserId;
      const isSelfByUsername = requestedUsername && viewerUsername && requestedUsername === viewerUsername;
      if (!isSelfById && !isSelfByUsername) {
        const profile = await fetchFollowProfile({
          userId: requestedUserId,
          username: requestedUserId ? null : requestedUsername,
        });
        activeProfileUserId = Number(profile?.user_id) || requestedUserId;
        activeProfileUsername = normalizeUsername(profile?.username || requestedUsername);
        activeProfileFullName = String(profile?.full_name || "").trim();
        isViewingOwnProfile = Boolean(viewerUserId && activeProfileUserId === viewerUserId);
        if (!isViewingOwnProfile) {
          applyReadOnlyProfileMode();
        }
      }
    }

    await checkCalendarVisibility();
    applyCalendarHeader();
    setMyHomeLinks(buildViewerHomeUrl());
    syncProfileModuleLinks();
  };

  onMount(() => {
    initPurposeCoverModule();
    void syncProfileStarsTotal("calendarStarsTotal");

    (async () => {
      try {
        await resolveProfileContext();
      } catch (error) {
        console.error(error);
      }
    })();
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{pageTitle}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user calendar-background">
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
        <a class="topbar-btn" href="/gallery.html">🖼️ Galería</a>
        <a class="topbar-btn" href="/my-public-whishes.html" data-profile-module="public_wishes">🌐 Deseos públicos</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 Deseos privados</a>
        <a class="topbar-btn" href="/my-fulfilled-whises.html" data-profile-module="fulfilled_wishes">✅ Deseos cumplidos</a>
      </div>

      <div class="feed-topbar-zone feed-topbar-right">
        <details class="topbar-dropdown">
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

        <details class="topbar-dropdown">
          <summary class="topbar-menu-btn" aria-label="Abrir menú">
            <span class="topbar-menu-icon" aria-hidden="true">☰</span>
            <span class="topbar-menu-label">Menú</span>
          </summary>
          <div class="dropdown-menu" role="menu">
            <a href="/home_user.html" role="menuitem" data-my-home>Mi Home</a>
            <a href="/achievements.html" role="menuitem">Logros recientes</a>
            <a href="/gallery.html" role="menuitem">Galería</a>
            <a href="/calendar.html" role="menuitem" data-profile-module="calendar">Calendario</a>
            <a href="/my-biography.html" role="menuitem">Mi Biografía</a>
          </div>
        </details>
      </div>
    </header>

    <main class="user-home">

      <!-- =========================
       *  PORTADA / COVER
       *  ========================= -->
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

      <div class="calendar-body">
        <!-- =========================
         *  NAV / LINKS
         *  ========================= -->
        <nav class="profile-nav" aria-label="Navegación de perfil">
          <a class="nav-pill" href="/home_user.html" title="Home" data-profile-module="home">Home</a>
          <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
            <span class="nav-icon">⭐</span>
            <span><strong id="calendarStarsTotal">0</strong> estrellas</span>
          </a>

          <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
          <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
          <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
          <a class="nav-pill" href="/calendar.html" title="Calendario" data-profile-module="calendar">Calendario</a>
          <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
        </nav>

        <!-- =========================
         *  CALENDARIO 2026
         *  ========================= -->
        {#if calendarAllowed}
        <section class="calendar-shell" aria-label="Calendario anual">
          <div class="calendar-head">
            <h2 class="calendar-title">{calendarTitle}</h2>
            <div class="calendar-legend">
              <span><strong>Disponible</strong> (hasta el 23 de enero)</span>
            </div>
          </div>

        <article class="calendar-year" aria-label="Vista anual 2026">
          <h3 class="year-label">2026 · Enero a Diciembre</h3>
          <div class="month-grid">
            <article class="month-card">
              <div class="month-name">Enero<span class="month-status">Actual</span></div>
              <div class="month-dots">
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Febrero<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Marzo<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Abril<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Mayo<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Junio<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Julio<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Agosto<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Septiembre<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Octubre<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Noviembre<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Diciembre<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
          </div>
        </article>

        <article class="calendar-current" aria-label="Detalle del mes actual">
          <div class="current-head">
            <h3 class="current-month">Enero 2026</h3>
            <div class="calendar-legend">
              <span>⭐ Estrellas</span>
              <span>✅ Deseos cumplidos</span>
              <span>🌟 Deseos públicos</span>
              <span>🏆 Logros</span>
              <span>📝 Publicaciones</span>
            </div>
          </div>

          <div class="calendar-grid">
            <div class="weekday">Lun</div>
            <div class="weekday">Mar</div>
            <div class="weekday">Mié</div>
            <div class="weekday">Jue</div>
            <div class="weekday">Vie</div>
            <div class="weekday">Sáb</div>
            <div class="weekday">Dom</div>
            <div class="day-cell is-empty"></div>
            <div class="day-cell is-empty"></div>
            <div class="day-cell is-empty"></div>
            <div class="day-cell">
              <div class="day-number"><span>1</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>2</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>3</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>⭐</span><span>120 estrellas</span></div>
                <div class="day-metric"><span>✅</span><span>2 deseos cumplidos</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>4</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>5</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>6</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>7</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>🌟</span><span>1 deseo público</span></div>
                <div class="day-metric"><span>📝</span><span>2 publicaciones</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>8</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>9</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>10</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>11</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>12</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>🏆</span><span>1 logro</span></div>
                <div class="day-metric"><span>📝</span><span>1 publicación</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>13</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>14</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>15</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>16</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>17</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>18</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>⭐</span><span>60 estrellas</span></div>
                <div class="day-metric"><span>✅</span><span>1 deseo cumplido</span></div>
                <div class="day-metric"><span>📝</span><span>3 publicaciones</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>19</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>20</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>21</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>22</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>🌟</span><span>2 deseos públicos</span></div>
                <div class="day-metric"><span>🏆</span><span>1 logro</span></div>
              </div>
            </div>
            <div class="day-cell is-today">
              <div class="day-number"><span>23</span><span class="day-badge">Hoy</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>24</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>25</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>26</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>27</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>28</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>29</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>30</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>31</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-empty"></div>
          </div>
        </article>
      </section>
        {:else}
        <section class="panel calendar-shell" aria-label="Calendario privado">
          <div class="panel-head">
            <h2 class="panel-title">Calendario privado</h2>
            <span class="panel-badge">🔒</span>
          </div>
          <p class="panel-muted">{calendarAccessError || "Este calendario es privado."}</p>
        </section>
        {/if}
      </div>

    </main>

    <!-- FOOTER reutilizado -->
    <footer class="kiadez-footer">
      <div class="footer-main">

        <div class="footer-column footer-origin">
          <p class="footer-poem">
            Kiadez fue llamado por una estrella a subir el Monte Manjaro.<br>
            No para dominar, sino para orientar.<br>
            Su luz no deslumbra: acompaña.
          </p>
        </div>

        <div class="footer-columns">
          <div class="footer-column">
            <h4>Sobre nuestra red social</h4>
            <ul>
              <li><a href="/what-is-kiadez.html">Qué es Kiadez</a></li>
              <li><a href="/guardians-rank.html">Rangos de Guardianes</a></li>
              <li><a href="/be-a-guardian.html">Ser Guardián</a></li>
              <li><a href="/contact.html">Contacto</a></li>
            </ul>
          </div>

          <div class="footer-column">
            <h4>Idiomas</h4>
            <ul>
              <li><a href="/?lang=es">Español</a></li>
              <li><a href="/?lang=en">English</a></li>
              <li><a href="/?lang=fr">Français</a></li>
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
