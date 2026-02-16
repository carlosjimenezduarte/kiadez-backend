<script>
  import { onMount } from 'svelte';
  import { initPurposeCoverModule } from '../lib/purposeCover';
  import { logout } from '../lib/logout';

  const API = 'http://127.0.0.1:8000';

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

  $: canDonate = Number(starPool.my_donatable_stars_total || 0) > 0;
  $: unlockedDonationAchievements = (starPool.donation_achievements || []).filter((achievement) =>
    Boolean(achievement.unlocked)
  );

  const formatStars = (value) => Number(value || 0).toLocaleString('es-CO');

  const openStars = (event) => {
    event?.preventDefault();
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

  const getAccessToken = () => localStorage.getItem('access_token') || '';

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

  const loadStarPoolState = async () => {
    isLoading = true;
    statusError = '';

    try {
      const response = await apiFetch('/posts/star-pool');
      const data = await response.json();

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
    initPurposeCoverModule();
    void loadStarPoolState();
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Fondo Común de Estrellas</title>
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
      <a class="topbar-btn" href="/home_user.html">🏠 Home</a>
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
        <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" id="openStarModal" title="Estrellas" on:click={openStars}>
          <span class="nav-icon">⭐</span>
          <span><strong>{formatStars(starPool.my_received_stars_total)}</strong> estrellas</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
      </nav>

      <section class="star-pool-shell" aria-label="Fondo Común de Estrellas">
        <header class="star-pool-head">
          <div>
            <h2 class="star-pool-title">Fondo Común de Estrellas</h2>
            <p class="star-pool-subtitle">Gracias por sostener el brillo colectivo.</p>
          </div>
          <div class="star-pool-tags">
            <span class="panel-badge">{justDonated ? 'Donación confirmada' : 'Estado actual'}</span>
            <span class="panel-badge">
              {starPool.unlocked_donation_achievements}/{starPool.donation_achievements.length || 10}
              logros por donación
            </span>
            <span class="panel-badge">
              {starPool.unlocked_publication_achievements}/{starPool.publication_achievements.length || 30}
              logros por publicaciones
            </span>
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
              <img src={justDonated ? '/css/star.webp' : '/css/fundstar.webp'} alt="Fondo Común de Estrellas" />
            </div>
            <div>
              {#if justDonated}
                <h3 class="star-pool-message">
                  Acabas de donar {formatStars(recentDonationAmount)} estrellas al Fondo Común de Estrellas
                </h3>
                <p class="star-pool-thanks">¡Muchas gracias por tu donación!</p>
              {:else}
                <h3 class="star-pool-message">Estrellas donadas por ti hasta ahora al Fondo Común de Estrellas</h3>
                <p class="star-pool-thanks"><strong>{formatStars(starPool.my_donated_stars_total)}</strong> estrellas</p>
              {/if}
            </div>
          </div>

          <div class="star-pool-stats">
            <div class="star-pool-stat">
              <div class="star-circle star-circle-md">
                <img src="/css/astral.webp" alt="Estrellas donadas" />
              </div>
              <div>
                <div class="star-pool-stat-label">Estrellas donadas por ti hasta ahora al Fondo Común de Estrellas</div>
                <div class="star-pool-stat-value">{formatStars(starPool.my_donated_stars_total)}</div>
              </div>
            </div>

            <div class="star-pool-stat">
              <div class="star-circle star-circle-md">
                <img src="/css/star.webp" alt="Estrellas disponibles" />
              </div>
              <div>
                <div class="star-pool-stat-label">Estrellas actualmente disponibles para donar</div>
                <div class="star-pool-stat-value">{formatStars(starPool.my_donatable_stars_total)}</div>
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
