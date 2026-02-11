<script>
  import { onMount } from "svelte";
  import { initPurposeCoverModule } from "../lib/purposeCover";

  onMount(() => {
    initPurposeCoverModule();
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Seguidores</title>
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
          <h2 class="panel-title">Seguidores</h2>
          <span class="panel-badge">12 seguidores</span>
        </div>
        <p class="panel-muted">Personas que siguen tu camino y celebran tus logros.</p>
      </section>

      <section class="panel">
        <div class="profile-row">
          <img class="avatar avatar-sm" src="assets/avatar-default.jpg" alt="Avatar" />
          <div class="profile-meta">
            <div class="profile-name">Sofía Rojas</div>
            <div class="profile-rank">Rango 3 · Guardiana</div>
            <div class="profile-actions">
              <button class="btn btn-outline btn-compact" type="button">Ver perfil</button>
              <button class="btn btn-primary btn-compact" type="button">Enviar mensaje</button>
            </div>
          </div>
        </div>
      </section>

      <section class="panel">
        <div class="profile-row">
          <img class="avatar avatar-sm" src="assets/avatar-default.jpg" alt="Avatar" />
          <div class="profile-meta">
            <div class="profile-name">Mateo Castillo</div>
            <div class="profile-rank">Rango 2 · Aprendiz</div>
            <div class="profile-actions">
              <button class="btn btn-outline btn-compact" type="button">Ver perfil</button>
              <button class="btn btn-primary btn-compact" type="button">Enviar mensaje</button>
            </div>
          </div>
        </div>
      </section>

      <section class="panel">
        <div class="profile-row">
          <img class="avatar avatar-sm" src="assets/avatar-default.jpg" alt="Avatar" />
          <div class="profile-meta">
            <div class="profile-name">Lina Duarte</div>
            <div class="profile-rank">Rango 1 · Buscadora</div>
            <div class="profile-actions">
              <button class="btn btn-outline btn-compact" type="button">Ver perfil</button>
              <button class="btn btn-primary btn-compact" type="button">Enviar mensaje</button>
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
