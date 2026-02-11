<script>
  import { onMount } from 'svelte';
  import { initPurposeCoverModule } from '../lib/purposeCover';

  let showModal = false;
  let showConfirm = true;
  let showSummary = false;
  let isVisitor = false;

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

  const handleDonateClick = (event) => {
    event.preventDefault();
    sessionStorage.setItem('star_pool_force_confirm', '1');
    window.location.href = event.currentTarget.getAttribute('href');
  };

  onMount(() => {
    document.body.dataset.visitor = isVisitor ? 'true' : 'false';
    initPurposeCoverModule();

    const forceConfirm = sessionStorage.getItem('star_pool_force_confirm') === '1';
    const confirmShown = sessionStorage.getItem('star_pool_confirm_shown') === '1';

    if (forceConfirm) {
      showConfirm = true;
      showSummary = false;
      sessionStorage.setItem('star_pool_confirm_shown', '1');
      sessionStorage.removeItem('star_pool_force_confirm');
    } else if (confirmShown) {
      showConfirm = false;
      showSummary = true;
    } else {
      showConfirm = true;
      showSummary = false;
      sessionStorage.setItem('star_pool_confirm_shown', '1');
    }
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Fondo Común de Estrellas</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user star-pool-background">
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

    <div class="star-pool-body">
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" id="openStarModal" title="Estrellas" on:click={openStars}>
          <span class="nav-icon">⭐</span>
          <span><strong>5.000.000</strong> estrellas</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
        <a class="nav-pill" href="calendar.html" title="Calendario">Calendario</a>
        <a class="nav-pill" href="my-biography.html" title="Mi biografía">Mi biografía</a>
      </nav>

      <section class="star-pool-shell" aria-label="Fondo Común de Estrellas">
        <header class="star-pool-head">
          <div>
            <h2 class="star-pool-title">Fondo Común de Estrellas</h2>
            <p class="star-pool-subtitle">Gracias por sostener el brillo colectivo.</p>
          </div>
          <div class="star-pool-tags">
            <span class="panel-badge">Donación confirmada</span>
          </div>
        </header>

        <article class="panel star-pool-card" id="donationConfirm" class:hidden={!showConfirm}>
          <div class="star-pool-highlight">
            <div class="star-circle star-circle-lg">
              <img src="/css/star.webp" alt="Estrella" />
            </div>
            <div>
              <h3 class="star-pool-message">Acabas de donar 5 estrellas al Fondo Común de Estrellas</h3>
              <p class="star-pool-thanks">¡Muchas gracias por tu donación!</p>
            </div>
          </div>

          <div class="star-pool-stats">
            <div class="star-pool-stat">
              <div class="star-circle star-circle-md">
                <img src="/css/astral.webp" alt="Estrellas donadas" />
              </div>
              <div>
                <div class="star-pool-stat-label">Estrellas donadas por ti hasta ahora al Fondo Común de Estrellas</div>
                <div class="star-pool-stat-value">434</div>
              </div>
            </div>

            <div class="star-pool-total">
              <div class="star-pool-total-label">Con tu donación el Fondo Común de Estrellas ha ascendido a un total de:</div>
              <div class="star-pool-total-value">5.400.321 estrellas</div>
            </div>
          </div>

          <div class="star-pool-achievements">
            <h4>Esto te ha permitido obtener los siguientes Logros:</h4>
            <div class="donation-badges">
              <div class="donation-badge">
                <div class="star-circle star-circle-sm">
                  <img src="/css/AKI/Donation/1.webp" alt="Explorador del Misterio" />
                </div>
                <span>Explorador del Misterio</span>
              </div>
              <div class="donation-badge">
                <div class="star-circle star-circle-sm">
                  <img src="/css/AKI/Donation/2.webp" alt="Confiado en el Universo" />
                </div>
                <span>Confiado en el Universo</span>
              </div>
              <div class="donation-badge">
                <div class="star-circle star-circle-sm">
                  <img src="/css/AKI/Donation/3.webp" alt="Creyente de las Nebulosas" />
                </div>
                <span>Creyente de las Nebulosas</span>
              </div>
            </div>
          </div>
        </article>

        <article class="panel star-pool-card" id="donationSummary" class:hidden={!showSummary}>
          <div class="star-pool-highlight">
            <div class="star-circle star-circle-lg">
              <img src="/css/fundstar.webp" alt="Fondo Común de Estrellas" />
            </div>
            <div>
              <h3 class="star-pool-message">Estrellas donadas por ti hasta ahora al Fondo Común de Estrellas</h3>
              <p class="star-pool-thanks"><strong>434</strong> estrellas</p>
            </div>
          </div>

          <div class="star-pool-stats">
            <div class="star-pool-stat">
              <div class="star-circle star-circle-md">
                <img src="/css/fundstar.webp" alt="Estrellas donadas" />
              </div>
              <div>
                <div class="star-pool-stat-label">Estrellas donadas por ti hasta ahora al Fondo Común de Estrellas</div>
                <div class="star-pool-stat-value">434</div>
              </div>
            </div>

            <div class="star-pool-total">
              <div class="star-pool-total-label">Con tu donación el Fondo Común de Estrellas ha ascendido a un total de:</div>
              <div class="star-pool-total-value">5.400.321 estrellas</div>
            </div>
          </div>

          <div class="star-pool-achievements">
            <h4>Esto te ha permitido obtener los siguientes Logros:</h4>
            <div class="donation-badges">
              <div class="donation-badge">
                <div class="star-circle star-circle-sm">
                  <img src="/css/AKI/Donation/1.webp" alt="Explorador del Misterio" />
                </div>
                <span>Explorador del Misterio</span>
              </div>
              <div class="donation-badge">
                <div class="star-circle star-circle-sm">
                  <img src="/css/AKI/Donation/2.webp" alt="Confiado en el Universo" />
                </div>
                <span>Confiado en el Universo</span>
              </div>
              <div class="donation-badge">
                <div class="star-circle star-circle-sm">
                  <img src="/css/AKI/Donation/3.webp" alt="Creyente de las Nebulosas" />
                </div>
                <span>Creyente de las Nebulosas</span>
              </div>
            </div>
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
        <div class="star-modal-number">5.000.000</div>
      </div>
    </div>

    <div class="modal-actions">
      <a class="btn btn-primary btn-compact" href="/star-pool" id="donateStarsBtn" on:click={handleDonateClick}>
        Donar mis estrellas al Fondo Común de Estrellas
      </a>
      <a class="btn btn-outline btn-compact visitor-only" href="game-star.html">
        Regalarle una estrella
      </a>
    </div>

    <div class="star-modal-note">
      Esta opción solo aparece para visitantes. Para simularlo, cambia <code>isVisitor</code> a <code>true</code> en el
      script (eso actualiza <code>data-visitor</code> en <code>body</code>).
    </div>
  </div>
</div>
