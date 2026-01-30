<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Galería</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background">
  <main class="user-home">
  <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt="Portada" />

        <div class="cover-actions">
          <button class="icon-btn" id="btnChangeCover" type="button" title="Cambiar portada">
            Cambiar portada
          </button>
          <button class="icon-btn" id="btnEditPurposes" type="button" title="Editar deseos de propósito">
            Editar propósito
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
        <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
          <span class="nav-icon">⭐</span>
          <span><strong>5.000.000</strong> estrellas</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
      </nav>

      <section class="panel">
        <div class="panel-head">
          <h2 class="panel-title">Galería</h2>
          <span class="panel-badge">Últimas publicaciones</span>
        </div>
        <p class="panel-muted">Un vistazo a tus recuerdos más luminosos.</p>
      </section>

      <section class="panel">
        <div class="badge-grid">
          <div class="badge-item is-unlocked">
            <button class="badge-figure" type="button">
              <img src="/css/star.webp" alt="Momento estelar" />
              <span class="badge-label">Momento estelar</span>
            </button>
            <div class="badge-body">
              <div class="badge-name">Noche de revelación</div>
              <div class="badge-desc">Imagen · 2 días</div>
            </div>
          </div>
          <div class="badge-item is-unlocked">
            <button class="badge-figure" type="button">
              <img src="/css/astral.webp" alt="Viaje astral" />
              <span class="badge-label">Viaje astral</span>
            </button>
            <div class="badge-body">
              <div class="badge-name">Testimonio del camino</div>
              <div class="badge-desc">Video · 5 días</div>
            </div>
          </div>
          <div class="badge-item is-unlocked">
            <button class="badge-figure" type="button">
              <img src="/css/fundstar.webp" alt="Fondo común" />
              <span class="badge-label">Fondo común</span>
            </button>
            <div class="badge-body">
              <div class="badge-name">Donación significativa</div>
              <div class="badge-desc">Imagen · 1 semana</div>
            </div>
          </div>
          <div class="badge-item is-unlocked">
            <button class="badge-figure" type="button">
              <img src="/css/star2.webp" alt="Ritual" />
              <span class="badge-label">Ritual</span>
            </button>
            <div class="badge-body">
              <div class="badge-name">Ritual de propósito</div>
              <div class="badge-desc">Imagen · 2 semanas</div>
            </div>
          </div>
        </div>
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
