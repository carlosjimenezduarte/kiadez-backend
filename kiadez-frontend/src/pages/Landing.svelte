<script>
  function handleSubmit(event) {
    event.preventDefault();
    alert('Aquí conectamos con Kiadez API 🔐');
  }
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background">
  <main class="hero">
    <section class="hero-left">
      <div class="auth-card">
        <h2 class="auth-title">Iniciar sesión en Kiadez</h2>

        <form id="auth-form" on:submit={handleSubmit}>
          <input type="email" placeholder="Correo electrónico" required />
          <input type="password" placeholder="Contraseña" required />

          <button type="submit" class="btn btn-primary">
            Iniciar sesión
          </button>

          <a href="/forgot-password.html" class="auth-link">
            ¿Olvidaste tu contraseña?
          </a>

          <div class="auth-divider"></div>
          <a href="register.html" class="btn btn-outline">
            Registrarse en Kiadez
          </a>
        </form>

        <div class="auth-brand">
          <img src="/css/logo-kiadez.webp" alt="Kiadez" />
          <span>Kiadez</span>
        </div>
      </div>
    </section>

    <section class="hero-right">
      <h1 class="hero-title">Kiadez</h1>

      <p class="hero-subtitle">
        Una red social pensada para cumplir los deseos
      </p>

      <blockquote class="hero-quote">
        La sabiduría suprema consiste en tener sueños lo suficientemente grandes
        para no perderlos de vista mientras se persiguen.
        <br />
        <br />
        <span>— William Faulkner</span>
      </blockquote>
    </section>
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
