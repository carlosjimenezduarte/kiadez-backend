<script>
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";

  const APK_URL = "https://www.kiadez.com/app/KiadezV7.apk";
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";

  const copy = isEn
    ? {
        metaTitle: "Kiadez - Download App",
        heroTitle: "📱 Download Kiadez for Android",
        heroQuestion: "Would you like to use Kiadez on your phone?",
        heroDescription: "Download the official APK and install it directly on your device.",
        downloadButton: "Download Kiadez App",
        downloadLinkLabel: "Link:",
        installTitle: "How to install Kiadez on your Android phone",
        installSteps: [
          "Download the application by clicking the button above.",
          "Open the Downloads folder on your phone and locate the Kiadez APK file (you will recognize it by its name and official icon).",
          "Android may display a warning indicating that this is an external application. This message is standard for any APK that is not distributed through Google Play.",
          "If you choose to proceed, manually authorize the installation from your device settings.",
          "The application will install automatically.",
          "Locate the Kiadez icon on your home screen or in the app drawer.",
          "If you wish, you can pin it to your home screen for quicker access.",
        ],
        installClosing: "You’re all set — enjoy the experience and keep building your dreams.",
        whyTitle: "Why isn't Kiadez available on Google Play?",
        whyParagraphs: [
          "Kiadez is currently distributed directly, without intermediaries.",
          "During the Google Play developer registration process, administrative restrictions arose that required additional payments, extended verification procedures, and potential compliance reviews.",
          "Instead of investing time and resources in processes that did not add real value to the project, I chose direct distribution — aligned with the philosophy of technological independence, transparency, and open access.",
          "Kiadez is delivered from its official source, without external dependencies.",
        ],
        noticeTitle: "🔒 Important Notice",
        noticeIntro: "For your safety:",
        noticeBullets: [
          "Do not install Kiadez if it was sent to you via email, messaging platforms, or third parties.",
          "Download only the official version available on this website.",
        ],
        noticeParagraphs: [
          "Any version distributed through other channels may have been modified.",
          "The only official application is the one published directly from this site.",
        ],
      }
    : isFr
      ? {
          metaTitle: "Kiadez - Télécharger l'application",
          heroTitle: "📱 Télécharger Kiadez pour Android",
          heroQuestion: "Souhaitez-vous utiliser Kiadez sur votre téléphone ?",
          heroDescription: "Téléchargez l'APK officiel et installez-le directement sur votre appareil.",
          downloadButton: "Télécharger l’application Kiadez",
          downloadLinkLabel: "Lien :",
          installTitle: "Comment installer Kiadez sur votre téléphone Android",
          installSteps: [
            "Téléchargez l'application en cliquant sur le bouton ci-dessus.",
            "Ouvrez le dossier Téléchargements sur votre téléphone et localisez le fichier APK de Kiadez (vous le reconnaîtrez grâce à son nom et à son icône officielle).",
            "Android peut afficher un avertissement indiquant qu'il s'agit d'une application externe. Ce message est standard pour tout APK qui ne provient pas du Google Play Store.",
            "Si vous décidez de continuer, autorisez manuellement l'installation depuis les paramètres de votre appareil.",
            "L'application s'installera automatiquement.",
            "Recherchez l'icône Kiadez sur votre écran d'accueil ou dans le menu des applications.",
            "Si vous le souhaitez, vous pouvez l'ajouter à votre écran principal pour un accès plus rapide.",
          ],
          installClosing: "C’est fait — profitez de l'expérience et continuez à construire vos rêves.",
          whyTitle: "Pourquoi Kiadez n'est-il pas disponible sur Google Play ?",
          whyParagraphs: [
            "Kiadez est actuellement distribué directement, sans intermédiaires.",
            "Lors du processus d'inscription en tant que développeur Google Play, des restrictions administratives ont nécessité des paiements supplémentaires, des procédures de vérification prolongées et d'éventuels contrôles de conformité.",
            "Plutôt que d'investir du temps et des ressources dans des démarches qui n'apportaient pas de valeur réelle au projet, j'ai choisi une distribution directe — cohérente avec une philosophie d'indépendance technologique, de transparence et d'accès libre.",
            "Kiadez est fourni depuis sa source officielle, sans dépendances externes.",
          ],
          noticeTitle: "🔒 Avertissement important",
          noticeIntro: "Pour votre sécurité :",
          noticeBullets: [
            "N’installez pas Kiadez si l’application vous a été envoyée par email, messagerie ou par des tiers.",
            "Téléchargez uniquement la version officielle disponible sur ce site web.",
          ],
          noticeParagraphs: [
            "Toute version distribuée par d’autres canaux pourrait avoir été modifiée.",
            "La seule application officielle est celle publiée directement depuis ce site.",
          ],
        }
      : {
          metaTitle: "Kiadez - Descarga la app",
          heroTitle: "📱 Descarga Kiadez para Android",
          heroQuestion: "¿Quieres usar Kiadez desde tu teléfono?",
          heroDescription: "Descarga la aplicación oficial en formato APK e instálala directamente en tu dispositivo.",
          downloadButton: "Descargar aplicación Kiadez",
          downloadLinkLabel: "Enlace:",
          installTitle: "¿Cómo instalar Kiadez en tu teléfono Android?",
          installSteps: [
            "Descarga la aplicación haciendo clic en el botón anterior.",
            "Abre la carpeta Descargas en tu teléfono y localiza el archivo APK de Kiadez (lo reconocerás por su nombre e icono oficial).",
            "Es posible que Android muestre una advertencia indicando que se trata de una aplicación externa. Este aviso es estándar para cualquier APK que no provenga de Google Play.",
            "Si decides continuar, autoriza manualmente la instalación desde tu dispositivo.",
            "La aplicación se instalará automáticamente.",
            "Busca el icono de Kiadez en la pantalla principal o en el menú de aplicaciones.",
            "Si lo deseas, puedes fijarla en tu pantalla de inicio para acceder más rápido.",
          ],
          installClosing: "Ahora sí: disfruta la experiencia y sigue construyendo tus deseos.",
          whyTitle: "¿Por qué Kiadez no está en Google Play Store?",
          whyParagraphs: [
            "Kiadez actualmente se distribuye de forma directa, sin intermediarios.",
            "Durante el proceso de registro como desarrollador en Google Play surgieron restricciones administrativas que implicaban nuevos pagos, procesos extensos de verificación y posibles auditorías adicionales.",
            "En lugar de invertir tiempo y recursos en trámites que no aportaban valor real al proyecto, decidí optar por una distribución directa, coherente con la filosofía de independencia tecnológica, transparencia y acceso libre.",
            "Kiadez se entrega desde su fuente oficial, sin dependencias externas.",
          ],
          noticeTitle: "🔒 Advertencia importante",
          noticeIntro: "Por tu seguridad:",
          noticeBullets: [
            "No instales Kiadez si te fue enviada por correo, mensajería o terceros.",
            "Descarga únicamente la versión oficial disponible en esta web.",
          ],
          noticeParagraphs: [
            "Cualquier versión distribuida por otros medios podría estar modificada.",
            "La única aplicación oficial es la publicada directamente desde este sitio.",
          ],
        };
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{copy.metaTitle}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-kiadez">
  <main class="content-center">
    <article class="content-card legal-content-card download-app-card">
      <h1 class="content-title">{copy.heroTitle}</h1>

      <div class="content-text legal-doc download-doc">
        <p>{copy.heroQuestion}</p>
        <p>{copy.heroDescription}</p>

        <div class="download-cta">
          <a class="btn btn-primary" href={APK_URL} target="_blank" rel="noopener noreferrer">
            {copy.downloadButton}
          </a>
          <p class="download-link-line">
            <strong>{copy.downloadLinkLabel}</strong>
            <a href={APK_URL} target="_blank" rel="noopener noreferrer">{APK_URL}</a>
          </p>
        </div>

        <hr class="legal-divider" />

        <h2>{copy.installTitle}</h2>
        <ol>
          {#each copy.installSteps as step}
            <li>{step}</li>
          {/each}
        </ol>
        <p>{copy.installClosing}</p>

        <hr class="legal-divider" />

        <h2>{copy.whyTitle}</h2>
        {#each copy.whyParagraphs as paragraph}
          <p>{paragraph}</p>
        {/each}

        <hr class="legal-divider" />

        <h2>{copy.noticeTitle}</h2>
        <p>{copy.noticeIntro}</p>
        <ul>
          {#each copy.noticeBullets as bullet}
            <li>{bullet}</li>
          {/each}
        </ul>
        {#each copy.noticeParagraphs as paragraph}
          <p>{paragraph}</p>
        {/each}
      </div>
    </article>
  </main>

  <AuthFooter />
</div>
