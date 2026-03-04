<script>
  import { onMount } from 'svelte';
  import { initPurposeCoverModule } from '../lib/purposeCover';
  import { logout } from '../lib/logout';
  import { syncTopbarAvatar } from "../lib/topbarAvatar";

  const API = import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") || "http://localhost:8000";
  let pageTitle = "Kiadez — Fondo Común de Estrellas";
  let isViewingOwnProfile = true;
  let viewerUserId = null;
  let viewerUsername = "";
  let activeProfileUserId = null;
  let activeProfileUsername = "";
  let activeProfileFullName = "";

  let showModal = false;
  let isLoading = true;
  let isDonating = false;
  let statusMessage = '';
  let statusError = '';
  let justDonated = false;
  let recentDonationAmount = 0;

  let starPool = {
    my_received_stars_total: 0,
    my_donated_stars_total: 0,
    my_donatable_stars_total: 0,
    common_pool_stars_total: 0,
    unlocked_publication_achievements: 0,
    unlocked_donation_achievements: 0,
    publication_achievements: [],
    donation_achievements: [],
  };

  $: canDonate = isViewingOwnProfile && Number(starPool.my_donatable_stars_total || 0) > 0;
  $: unlockedDonationAchievements = (starPool.donation_achievements || []).filter((achievement) =>
    Boolean(achievement.unlocked)
  );

  const formatStars = (value) => Number(value || 0).toLocaleString('es-CO');

  const openStars = (event) => {
    event?.preventDefault();
    if (!isViewingOwnProfile) return;
    showModal = true;
  };

  const closeStars = () => {
    showModal = false;
  };

  const handleOverlayClick = (event) => {
    if (event.currentTarget === event.target) {
      closeStars();
    }
  };

  const getAccessToken = () =>
    localStorage.getItem('access_token') ||
    localStorage.getItem('kiadez_access_token') ||
    '';

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
      window.location.href = '/login.html';
      throw new Error('No hay sesión activa.');
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    };

    const response = await fetch(`${API}${path}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login.html';
      throw new Error('Sesión expirada.');
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
      ? "Kiadez — Fondo Común de Estrellas"
      : `Kiadez — Estrellas de ${activeProfileFullName || "usuario"}`;
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
        isViewingOwnProfile = Boolean(viewerUserId && activeProfileUserId === viewerUserId);
        if (!isViewingOwnProfile) {
          applyReadOnlyProfileMode();
        }
      }
    }

    applyPageTitle();
    setMyHomeLinks(buildViewerHomeUrl());
    syncProfileModuleLinks();
  };

  const loadStarPoolState = async () => {
    isLoading = true;
    statusError = '';

    try {
      const profileId = parsePositiveId(activeProfileUserId);
      const endpoint =
        !isViewingOwnProfile && profileId
          ? `/posts/star-pool/user/${encodeURIComponent(String(profileId))}`
          : '/posts/star-pool';
      const response = await apiFetch(endpoint);
      const data = await parseResponseJson(response);

      if (!response.ok) {
        throw new Error(data.detail || 'No se pudieron cargar las estrellas.');
      }

      starPool = data;
    } catch (error) {
      statusError = error.message || 'No se pudieron cargar las estrellas.';
    } finally {
      isLoading = false;
    }
  };

  const handleDonateClick = async (event) => {
    event.preventDefault();

    if (!isViewingOwnProfile) {
      statusError = "La donación solo está disponible en tu propio perfil.";
      return;
    }

    if (isDonating || isLoading) {
      return;
    }

    if (!canDonate) {
      statusError = 'No tienes estrellas nuevas por donar en este momento.';
      return;
    }

    isDonating = true;
    statusError = '';
    statusMessage = '';

    try {
      const response = await apiFetch('/posts/star-pool/donate', { method: 'POST' });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'No se pudo registrar la donación.');
      }

      starPool = data.state;
      recentDonationAmount = Number(data.donated_now || 0);
      justDonated = recentDonationAmount > 0;

      if (justDonated) {
        statusMessage = `Donación registrada: ${formatStars(recentDonationAmount)} estrellas.`;
      } else {
        statusMessage = 'Tus estrellas ya estaban donadas al Fondo Común.';
      }

      showModal = false;
    } catch (error) {
      statusError = error.message || 'No se pudo registrar la donación.';
    } finally {
      isDonating = false;
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
      } catch (error) {
        statusError = error?.message || 'No se pudo resolver el perfil.';
      }
      await loadStarPoolState();
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

<div class="page-background page-background-user star-pool-background">
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
            Deseo de propósito sin definir
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

    <div class="star-pool-body">
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home" data-profile-module="home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas" data-profile-module="stars">
          <span class="nav-icon">⭐</span>
          <span><strong>{formatStars(starPool.my_received_stars_total)}</strong> estrellas</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Seguidores" data-profile-module="followers">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes" data-profile-module="achievements">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería" data-profile-module="gallery">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario" data-profile-module="calendar">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía" data-profile-module="biography">Mi biografía</a>
        <a class="nav-pill" href="/messages.html" title="Mensajes">Mensajes</a>
      </nav>

      <section class="star-pool-shell" aria-label="Fondo Común de Estrellas">
        <header class="star-pool-head">
          <div>
            <h2 class="star-pool-title">Fondo Común de Estrellas</h2>
            <p class="star-pool-subtitle">Gracias por sostener el brillo colectivo.</p>
          </div>
        </header>

        {#if isLoading}
          <p class="star-pool-status">Cargando estado del Fondo Común...</p>
        {/if}

        {#if statusMessage}
          <p class="star-pool-status">{statusMessage}</p>
        {/if}

        {#if statusError}
          <p class="star-pool-status is-error">{statusError}</p>
        {/if}

        <article class="panel star-pool-card" id="donationSummary">
          <div class="star-pool-highlight">
            <div class="star-circle star-circle-lg">
              <img src="/css/fundstar.webp" alt="Acumulado del Fondo Común de Estrellas" />
            </div>
            <div>
              <h3 class="star-pool-message">Acumulado actual del Fondo Común de Estrellas</h3>
              <p class="star-pool-thanks"><strong>{formatStars(starPool.common_pool_stars_total)}</strong> estrellas</p>
              {#if justDonated && recentDonationAmount > 0}
                <p class="star-pool-thanks">
                  Tu donación de {formatStars(recentDonationAmount)} estrellas ya se sumó al acumulado global.
                </p>
              {/if}
            </div>
          </div>

          <div class="star-pool-stats">
            <div class="star-pool-stat">
              <div class="star-circle star-circle-md">
                <img src="/css/astral.webp" alt="Estrellas donadas" />
              </div>
              <div>
                <div class="star-pool-stat-label">
                  {isViewingOwnProfile
                    ? "Estrellas donadas por ti hasta ahora al Fondo Común de Estrellas"
                    : "Estrellas donadas por este perfil al Fondo Común de Estrellas"}
                </div>
                <div class="star-pool-stat-value">{formatStars(starPool.my_donated_stars_total)}</div>
              </div>
            </div>

            <div class="star-pool-stat">
              <div class="star-circle star-circle-md">
                <img src="/css/star.webp" alt="Estrellas disponibles" />
              </div>
              <div>
                <div class="star-pool-stat-label">
                  {isViewingOwnProfile
                    ? "Estrellas actualmente disponibles para donar"
                    : "Estrellas donables (vista pública)"}
                </div>
                <div class="star-pool-stat-value">{formatStars(starPool.my_donatable_stars_total)}</div>
                {#if canDonate}
                  <button class="btn btn-primary btn-compact btn-inline" type="button" on:click={openStars}>
                    Donar estrellas
                  </button>
                {/if}
              </div>
            </div>

            <div class="star-pool-total">
              <div class="star-pool-total-label">Total actual del Fondo Común de Estrellas:</div>
              <div class="star-pool-total-value">{formatStars(starPool.common_pool_stars_total)} estrellas</div>
            </div>
          </div>

          <div class="star-pool-achievements">
            <h4>Logros de donación desbloqueados</h4>

            {#if unlockedDonationAchievements.length === 0}
              <p class="panel-muted">
                Aún no tienes logros de donación desbloqueados. Tu primer logro aparece al llegar a 1.000 estrellas donadas.
              </p>
            {:else}
              <div class="donation-badges">
                {#each unlockedDonationAchievements as achievement}
                  <div class="donation-badge">
                    <div class="star-circle star-circle-sm">
                      <img src={achievement.image_url} alt={achievement.title} />
                    </div>
                    <span>{achievement.title}</span>
                  </div>
                {/each}
              </div>
            {/if}
          </div>
        </article>
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

<div
  class="modal-overlay"
  id="starsModalOverlay"
  aria-hidden={showModal ? 'false' : 'true'}
  class:hidden={!showModal}
  on:click={handleOverlayClick}
>
  <div class="modal star-modal" role="dialog" aria-modal="true" aria-label="Estrellas acumuladas">
    <div class="modal-head">
      <h3>Estrellas acumuladas</h3>
      <button class="modal-close" type="button" id="closeStarModal" on:click={closeStars}>✕</button>
    </div>

    <div class="modal-body">
      <p class="panel-muted">Estrellas que has acumulado hasta ahora con tus publicaciones</p>

      <div class="star-modal-row">
        <div class="star-circle star-circle-lg">
          <img src="/css/star.webp" alt="Estrella acumulada" />
        </div>
        <div class="star-modal-number">{formatStars(starPool.my_received_stars_total)}</div>
      </div>

      <div class="star-modal-metrics">
        <div>
          <strong>Disponibles para donar:</strong>
          {formatStars(starPool.my_donatable_stars_total)}
        </div>
        <div>
          <strong>Ya donadas al Fondo Común:</strong>
          {formatStars(starPool.my_donated_stars_total)}
        </div>
      </div>
    </div>

    <div class="modal-actions">
      <button
        class="btn btn-primary btn-compact"
        type="button"
        id="donateStarsBtn"
        on:click={handleDonateClick}
        disabled={!canDonate || isDonating || isLoading}
      >
        {#if isDonating}
          Donando...
        {:else if canDonate}
          Donar mis estrellas al Fondo Común de Estrellas
        {:else}
          No tienes estrellas nuevas por donar
        {/if}
      </button>
      <a class="btn btn-outline btn-compact visitor-only" href="/game-star.html">
        Regalarle una estrella
      </a>
    </div>

    {#if statusError}
      <div class="star-modal-note star-modal-note-error">{statusError}</div>
    {:else if statusMessage}
      <div class="star-modal-note">{statusMessage}</div>
    {/if}
  </div>
</div>
