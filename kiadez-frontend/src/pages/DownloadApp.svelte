<script>
  const APK_URL = "https://www.kiadez.com/app/KiadezV8.apk";
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez - Descarga la app</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-kiadez">
  <main class="content-center">
    <article class="content-card legal-content-card download-app-card">
      <h1 class="content-title">📱 Descarga Kiadez para Android</h1>

      <div class="content-text legal-doc download-doc">
        <p>¿Quieres usar Kiadez desde tu teléfono?</p>
        <p>Descarga la aplicación oficial en formato APK e instálala directamente en tu dispositivo.</p>

        <div class="download-cta">
          <a class="btn btn-primary" href={APK_URL} target="_blank" rel="noopener noreferrer">
            Descargar aplicación Kiadez
          </a>
          <p class="download-link-line">
            <strong>Enlace:</strong>
            <a href={APK_URL} target="_blank" rel="noopener noreferrer">{APK_URL}</a>
          </p>
        </div>

        <hr class="legal-divider" />

        <h2>¿Cómo instalar Kiadez en tu teléfono Android?</h2>
        <ol>
          <li>Descarga la aplicación haciendo clic en el botón anterior.</li>
          <li>Abre la carpeta Descargas en tu teléfono y localiza el archivo APK de Kiadez (lo reconocerás por su nombre e icono oficial).</li>
          <li>Es posible que Android muestre una advertencia indicando que se trata de una aplicación externa. Este aviso es estándar para cualquier APK que no provenga de Google Play.</li>
          <li>Si decides continuar, autoriza manualmente la instalación desde tu dispositivo.</li>
          <li>La aplicación se instalará automáticamente.</li>
          <li>Busca el icono de Kiadez en la pantalla principal o en el menú de aplicaciones.</li>
          <li>Si lo deseas, puedes fijarla en tu pantalla de inicio para acceder más rápido.</li>
        </ol>
        <p>Ahora sí: disfruta la experiencia y sigue construyendo tus deseos.</p>

        <hr class="legal-divider" />

        <h2>¿Por qué Kiadez no está en Google Play Store?</h2>
        <p>Kiadez actualmente se distribuye de forma directa, sin intermediarios.</p>
        <p>Durante el proceso de registro como desarrollador en Google Play surgieron restricciones administrativas que implicaban nuevos pagos, procesos extensos de verificación y posibles auditorías adicionales.</p>
        <p>En lugar de invertir tiempo y recursos en trámites que no aportaban valor real al proyecto, decidí optar por una distribución directa, coherente con la filosofía de independencia tecnológica, transparencia y acceso libre.</p>
        <p>Kiadez se entrega desde su fuente oficial, sin dependencias externas.</p>

        <hr class="legal-divider" />

        <h2>🔒 Advertencia importante</h2>
        <p>Por tu seguridad:</p>
        <ul>
          <li>No instales Kiadez si te fue enviada por correo, mensajería o terceros.</li>
          <li>Descarga únicamente la versión oficial disponible en esta web.</li>
        </ul>
        <p>Cualquier versión distribuida por otros medios podría estar modificada.</p>
        <p>La única aplicación oficial es la publicada directamente desde este sitio.</p>
      </div>
    </article>
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
