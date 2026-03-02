<script>
  import { onMount } from 'svelte';
  import { initPurposeCoverModule } from '../lib/purposeCover';
  import { logout } from '../lib/logout';
  import { getLocale } from '../lib/i18n';

  const API = 'http://127.0.0.1:8000';
  const locale = getLocale();
  const isEn = locale === 'en';
  const isFr = locale === 'fr';
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

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

  const formatStars = (value) => Number(value || 0).toLocaleString(isEn ? 'en-US' : isFr ? 'fr-FR' : 'es-CO');

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
      throw new Error(tr('No hay sesión activa.', 'No active session.', 'Aucune session active.'));
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
      throw new Error(tr('Sesión expirada.', 'Session expired.', 'Session expirée.'));
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
        throw new Error(
          data.detail ||
            tr(
              'No se pudieron cargar las estrellas.',
              'Could not load stars.',
              'Impossible de charger les étoiles.'
            )
        );
      }

      starPool = data;
    } catch (error) {
      statusError =
        error.message ||
        tr('No se pudieron cargar las estrellas.', 'Could not load stars.', 'Impossible de charger les étoiles.');
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
      statusError = tr(
        'No tienes estrellas nuevas por donar en este momento.',
        'You do not have new stars to donate right now.',
        "Tu n'as pas de nouvelles étoiles à donner pour le moment."
      );
      return;
    }

    isDonating = true;
    statusError = '';
    statusMessage = '';

    try {
      const response = await apiFetch('/posts/star-pool/donate', { method: 'POST' });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            tr(
              'No se pudo registrar la donación.',
              'Could not register the donation.',
              "Impossible d'enregistrer le don."
            )
        );
      }

      starPool = data.state;
      recentDonationAmount = Number(data.donated_now || 0);
      justDonated = recentDonationAmount > 0;

      if (justDonated) {
        statusMessage = tr(
          `Donación registrada: ${formatStars(recentDonationAmount)} estrellas.`,
          `Donation recorded: ${formatStars(recentDonationAmount)} stars.`,
          `Don enregistré : ${formatStars(recentDonationAmount)} étoiles.`
        );
      } else {
        statusMessage = tr(
          'Tus estrellas ya estaban donadas al Fondo Común.',
          'Your stars were already donated to the Common Pool.',
          'Tes étoiles étaient déjà versées au Fonds commun.'
        );
      }

      showModal = false;
    } catch (error) {
      statusError =
        error.message ||
        tr(
          'No se pudo registrar la donación.',
          'Could not register the donation.',
          "Impossible d'enregistrer le don."
        );
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
  <title>{tr('Kiadez — Fondo Común de Estrellas', 'Kiadez — Common Star Pool', 'Kiadez — Fonds commun des étoiles')}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user star-pool-background">
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input type="search" placeholder={tr('Buscar en Kiadez', 'Search on Kiadez', 'Rechercher sur Kiadez')} aria-label={tr('Buscar', 'Search', 'Rechercher')} />
      </form>
    </div>

    <div class="feed-topbar-zone feed-topbar-center">
      <a class="topbar-btn" href="/home_user.html">🏠 Home</a>
      <a class="topbar-btn" href="/gallery.html">🖼️ {tr('Galería', 'Gallery', 'Galerie')}</a>
      <a class="topbar-btn" href="/my-public-whishes.html">🌐 {tr('Deseos públicos', 'Public wishes', 'Souhaits publics')}</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 {tr('Deseos privados', 'Private wishes', 'Souhaits privés')}</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html">✅ {tr('Deseos cumplidos', 'Fulfilled wishes', 'Souhaits accomplis')}</a>
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown" id="profileDropdown">
        <summary class="topbar-avatar-btn" aria-label={tr('Perfil del usuario', 'User profile', 'Profil utilisateur')}>
          <img src="/assets/avatar-default.jpg" alt={tr('Foto de perfil del usuario', 'User profile photo', "Photo de profil de l'utilisateur")} />
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/privacy-and-settings.html" role="menuitem">{tr('Configuración y privacidad', 'Settings and privacy', 'Paramètres et confidentialité')}</a>
          <button type="button" role="menuitem" on:click={logout}>{tr('Cerrar sesión', 'Sign out', 'Se déconnecter')}</button>
        </div>
      </details>

      <button class="topbar-icon" type="button" aria-label={tr('Notificaciones', 'Notifications', 'Notifications')}>
        🔔
        <span class="topbar-badge">3</span>
      </button>

      <details class="topbar-dropdown" id="menuDropdown">
        <summary class="topbar-menu-btn" aria-label={tr('Abrir menú', 'Open menu', 'Ouvrir le menu')}>
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">{tr('Menú', 'Menu', 'Menu')}</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem">{tr('Mi Home', 'My Home', 'Mon Home')}</a>
          <a href="/achievements.html" role="menuitem">{tr('Logros recientes', 'Recent achievements', 'Réalisations récentes')}</a>
          <a href="/gallery.html" role="menuitem">{tr('Galería', 'Gallery', 'Galerie')}</a>
          <a href="/calendar.html" role="menuitem">{tr('Calendario', 'Calendar', 'Calendrier')}</a>
          <a href="/my-biography.html" role="menuitem">{tr('Mi Biografía', 'My Biography', 'Ma biographie')}</a>
          <a href="/messages.html" role="menuitem">{tr('Mensajes', 'Messages', 'Messagerie')}</a>
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt={tr('Portada', 'Cover', 'Couverture')} />

        <div class="cover-actions">
          <button class="icon-btn" id="btnChangeCover" type="button" title={tr('Cambiar portada', 'Change cover', 'Changer la couverture')}>
            {tr('Cambiar portada', 'Change cover', 'Changer la couverture')}
          </button>
          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button" title={tr('Editar mi propósito de vida', 'Edit my life purpose', 'Modifier mon objectif de vie')}>
            {tr('Editar mi propósito de vida', 'Edit my life purpose', 'Modifier mon objectif de vie')}
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="purpose-triangle" aria-label={tr('Deseos de propósito', 'Purpose wishes', 'Souhaits de finalité')}>
          <button class="purpose-pill purpose-top" type="button" id="purpose1">
            {tr('Deseo #1: Secreto', 'Wish #1: Secret', 'Souhait n°1 : Secret')}
          </button>

          <button class="purpose-pill purpose-left" type="button" id="purpose2">
            {tr('Deseo de propósito sin definir', 'Undefined purpose wish', 'Souhait de finalité non défini')}
          </button>

          <button class="purpose-pill purpose-right" type="button" id="purpose3">
            {tr('Deseo estar unido a Jesús', 'Wish to be united with Jesus', 'Souhait d’être uni à Jésus')}
          </button>
        </div>

        <div class="cover-hint" id="coverHint">
          {tr('Arrastra la portada para encuadrarla', 'Drag the cover to frame it', 'Fais glisser la couverture pour la cadrer')}
        </div>
      </div>
    </section>

    <div class="star-pool-body">
      <nav class="profile-nav" aria-label={tr('Navegación de perfil', 'Profile navigation', 'Navigation du profil')}>
        <a class="nav-pill" href="/home_user.html" title={tr('Home', 'Home', 'Accueil')}>{tr('Home', 'Home', 'Accueil')}</a>
        <a class="nav-pill" href="/star-pool-found.html" title={tr('Estrellas', 'Stars', 'Étoiles')}>
          <span class="nav-icon">⭐</span>
          <span><strong>{formatStars(starPool.my_received_stars_total)}</strong> {tr('estrellas', 'stars', 'étoiles')}</span>
        </a>

        <a class="nav-pill" href="/followers.html" title={tr('Seguidores', 'Followers', 'Abonnés')}>{tr('Seguidores', 'Followers', 'Abonnés')}</a>
        <a class="nav-pill" href="/achievements.html" title={tr('Logros recientes', 'Recent achievements', 'Réalisations récentes')}>{tr('Logros recientes', 'Recent achievements', 'Réalisations récentes')}</a>
        <a class="nav-pill" href="/gallery.html" title={tr('Galería', 'Gallery', 'Galerie')}>{tr('Galería', 'Gallery', 'Galerie')}</a>
        <a class="nav-pill" href="/calendar.html" title={tr('Calendario', 'Calendar', 'Calendrier')}>{tr('Calendario', 'Calendar', 'Calendrier')}</a>
        <a class="nav-pill" href="/my-biography.html" title={tr('Mi biografía', 'My biography', 'Ma biographie')}>{tr('Mi biografía', 'My biography', 'Ma biographie')}</a>
        <a class="nav-pill" href="/messages.html" title={tr('Mensajes', 'Messages', 'Messagerie')}>{tr('Mensajes', 'Messages', 'Messagerie')}</a>
      </nav>

      <section class="star-pool-shell" aria-label={tr('Fondo Común de Estrellas', 'Common Star Pool', 'Fonds commun des étoiles')}>
        <header class="star-pool-head">
          <div>
            <h2 class="star-pool-title">{tr('Fondo Común de Estrellas', 'Common Star Pool', 'Fonds commun des étoiles')}</h2>
            <p class="star-pool-subtitle">{tr('Gracias por sostener el brillo colectivo.', 'Thank you for sustaining the collective brightness.', "Merci de soutenir l'éclat collectif.")}</p>
          </div>
        </header>

        {#if isLoading}
          <p class="star-pool-status">{tr('Cargando estado del Fondo Común...', 'Loading Common Pool status...', 'Chargement de l’état du Fonds commun...')}</p>
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
              <img src="/css/fundstar.webp" alt={tr('Acumulado del Fondo Común de Estrellas', 'Common Star Pool accumulated total', 'Total cumulé du Fonds commun des étoiles')} />
            </div>
            <div>
              <h3 class="star-pool-message">{tr('Acumulado actual del Fondo Común de Estrellas', 'Current accumulated total of the Common Star Pool', 'Total cumulé actuel du Fonds commun des étoiles')}</h3>
              <p class="star-pool-thanks"><strong>{formatStars(starPool.common_pool_stars_total)}</strong> {tr('estrellas', 'stars', 'étoiles')}</p>
              {#if justDonated && recentDonationAmount > 0}
                <p class="star-pool-thanks">
                  {tr(
                    `Tu donación de ${formatStars(recentDonationAmount)} estrellas ya se sumó al acumulado global.`,
                    `Your donation of ${formatStars(recentDonationAmount)} stars has already been added to the global total.`,
                    `Ton don de ${formatStars(recentDonationAmount)} étoiles a déjà été ajouté au total global.`
                  )}
                </p>
              {/if}
            </div>
          </div>

          <div class="star-pool-stats">
            <div class="star-pool-stat">
              <div class="star-circle star-circle-md">
                <img src="/css/astral.webp" alt={tr('Estrellas donadas', 'Donated stars', 'Étoiles données')} />
              </div>
              <div>
                <div class="star-pool-stat-label">
                  {tr(
                    'Estrellas donadas por ti hasta ahora al Fondo Común de Estrellas',
                    'Stars donated by you so far to the Common Star Pool',
                    "Étoiles que tu as données jusqu'à présent au Fonds commun des étoiles"
                  )}
                </div>
                <div class="star-pool-stat-value">{formatStars(starPool.my_donated_stars_total)}</div>
              </div>
            </div>

            <div class="star-pool-stat">
              <div class="star-circle star-circle-md">
                <img src="/css/star.webp" alt={tr('Estrellas disponibles', 'Available stars', 'Étoiles disponibles')} />
              </div>
              <div>
                <div class="star-pool-stat-label">{tr('Estrellas actualmente disponibles para donar', 'Stars currently available to donate', 'Étoiles actuellement disponibles pour un don')}</div>
                <div class="star-pool-stat-value">{formatStars(starPool.my_donatable_stars_total)}</div>
                {#if canDonate}
                  <button class="btn btn-primary btn-compact btn-inline" type="button" on:click={openStars}>
                    {tr('Donar estrellas', 'Donate stars', 'Donner des étoiles')}
                  </button>
                {/if}
              </div>
            </div>

            <div class="star-pool-total">
              <div class="star-pool-total-label">{tr('Total actual del Fondo Común de Estrellas:', 'Current total of the Common Star Pool:', 'Total actuel du Fonds commun des étoiles :')}</div>
              <div class="star-pool-total-value">{formatStars(starPool.common_pool_stars_total)} {tr('estrellas', 'stars', 'étoiles')}</div>
            </div>
          </div>

          <div class="star-pool-achievements">
            <h4>{tr('Logros de donación desbloqueados', 'Unlocked donation achievements', 'Réalisations de don débloquées')}</h4>

            {#if unlockedDonationAchievements.length === 0}
              <p class="panel-muted">
                {tr(
                  'Aún no tienes logros de donación desbloqueados. Tu primer logro aparece al llegar a 1.000 estrellas donadas.',
                  'You do not have unlocked donation achievements yet. Your first achievement appears at 1,000 donated stars.',
                  "Tu n'as pas encore de réalisations de don débloquées. La première apparaît à 1 000 étoiles données."
                )}
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
          {tr(
            'Kiadez fue llamado por una estrella a subir el Monte Manjaro.\nNo para dominar, sino para orientar.\nSu luz no deslumbra: acompaña.',
            'Kiadez was called by a star to climb Mount Manjaro.\nNot to dominate, but to guide.\nIts light does not dazzle: it accompanies.',
            "Kiadez fut appelé par une étoile à gravir le mont Manjaro.\nNon pour dominer, mais pour orienter.\nSa lumière n'éblouit pas : elle accompagne."
          )}
        </p>
      </div>

      <div class="footer-columns">
        <div class="footer-column">
          <h4>{tr('Sobre nuestra red social', 'About our social network', 'À propos de notre réseau social')}</h4>
          <ul>
            <li><a href="/what-is-kiadez.html">{tr('Qué es Kiadez', 'What is Kiadez', "Qu'est-ce que Kiadez")}</a></li>
            <li><a href="/guardians-rank.html">{tr('Rangos de Guardianes', 'Guardian ranks', 'Rangs des Gardiens')}</a></li>
            <li><a href="/be-a-guardian.html">{tr('Ser Guardián', 'Be a Guardian', 'Devenir Gardien')}</a></li>
            <li><a href="/contact.html">{tr('Contacto', 'Contact', 'Contact')}</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>{tr('Idiomas', 'Languages', 'Langues')}</h4>
          <ul>
            <li><a href="/?lang=es">Español</a></li>
            <li><a href="/?lang=en">English</a></li>
            <li><a href="/?lang=fr">Français</a></li>
            <li><a href="/?lang=pt">Português</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>{tr('Contacto', 'Contact', 'Contact')}</h4>
          <ul>
            <li>info@kiadez.com</li>
            <li>+57 333 225 6078</li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>{tr('Información legal', 'Legal information', 'Informations légales')}</h4>
          <ul>
            <li><a href="/mygamerules.html">{tr('Mis reglas de juego', 'My game rules', 'Mes règles du jeu')}</a></li>
            <li><a href="/terms.html">{tr('Términos y condiciones', 'Terms and conditions', 'Termes et conditions')}</a></li>
            <li><a href="/privacy.html">{tr('Privacidad', 'Privacy', 'Confidentialité')}</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      {tr('© 2026 Kiadez — Una red social para cumplir deseos.', '© 2026 Kiadez — A social network to fulfill wishes.', '© 2026 Kiadez — Un réseau social pour accomplir des souhaits.')}
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
  <div class="modal star-modal" role="dialog" aria-modal="true" aria-label={tr('Estrellas acumuladas', 'Accumulated stars', 'Étoiles accumulées')}>
    <div class="modal-head">
      <h3>{tr('Estrellas acumuladas', 'Accumulated stars', 'Étoiles accumulées')}</h3>
      <button class="modal-close" type="button" id="closeStarModal" on:click={closeStars}>✕</button>
    </div>

    <div class="modal-body">
      <p class="panel-muted">{tr('Estrellas que has acumulado hasta ahora con tus publicaciones', 'Stars you have accumulated so far with your posts', 'Étoiles que tu as accumulées jusqu’ici avec tes publications')}</p>

      <div class="star-modal-row">
        <div class="star-circle star-circle-lg">
          <img src="/css/star.webp" alt={tr('Estrella acumulada', 'Accumulated star', 'Étoile accumulée')} />
        </div>
        <div class="star-modal-number">{formatStars(starPool.my_received_stars_total)}</div>
      </div>

      <div class="star-modal-metrics">
        <div>
          <strong>{tr('Disponibles para donar:', 'Available to donate:', 'Disponibles pour donner :')}</strong>
          {formatStars(starPool.my_donatable_stars_total)}
        </div>
        <div>
          <strong>{tr('Ya donadas al Fondo Común:', 'Already donated to the Common Pool:', 'Déjà données au Fonds commun :')}</strong>
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
          {tr('Donando...', 'Donating...', 'Don en cours...')}
        {:else if canDonate}
          {tr('Donar mis estrellas al Fondo Común de Estrellas', 'Donate my stars to the Common Star Pool', 'Donner mes étoiles au Fonds commun des étoiles')}
        {:else}
          {tr('No tienes estrellas nuevas por donar', 'You do not have new stars to donate', "Tu n'as pas de nouvelles étoiles à donner")}
        {/if}
      </button>
      <a class="btn btn-outline btn-compact visitor-only" href="/game-star.html">
        {tr('Regalarle una estrella', 'Give them a star', 'Offrir une étoile')}
      </a>
    </div>

    {#if statusError}
      <div class="star-modal-note star-modal-note-error">{statusError}</div>
    {:else if statusMessage}
      <div class="star-modal-note">{statusMessage}</div>
    {/if}
  </div>
</div>
