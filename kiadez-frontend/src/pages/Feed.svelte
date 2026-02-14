<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";

  onMount(() => {
    const promptOptions = [
      "Publica algo que motive a tus seguidores",
      "¿Cómo estás trabajando hoy por tus sueños?",
      "¿Qué ha pasado de fantástico hoy?"
    ];

    const composerInput = document.getElementById("openPostModal");
    const feedHomeBtn = document.getElementById("feedHomeBtn");

    const setRandomPrompt = () => {
      if (!composerInput) return;
      const prompt = promptOptions[Math.floor(Math.random() * promptOptions.length)];
      composerInput.textContent = prompt;
    };

    setRandomPrompt();

    if (feedHomeBtn) {
      feedHomeBtn.addEventListener("click", () => {
        setRandomPrompt();
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    }

    const menuPublishBtn = document.getElementById("menuPublishBtn");
    const menuDropdown = document.getElementById("menuDropdown");

    const postModalOverlay = document.getElementById("postModalOverlay");
    const closePostModal = document.getElementById("closePostModal");
    const cancelPost = document.getElementById("cancelPost");
    const postFile = document.getElementById("postFile");
    const uploadHint = document.getElementById("uploadHint");
    const postPreview = document.getElementById("postPreview");

    const openPost = () => {
      postModalOverlay.classList.remove("hidden");
      postModalOverlay.setAttribute("aria-hidden", "false");
    };

    const closePost = () => {
      postModalOverlay.classList.add("hidden");
      postModalOverlay.setAttribute("aria-hidden", "true");
      uploadHint.textContent = "Sin archivo adjunto";
      postPreview.innerHTML = "";
      postPreview.classList.add("hidden");
      postFile.value = "";
      document.getElementById("postText").value = "";
      document.getElementById("postVisibility").value = "public";
    };

    if (composerInput) composerInput.addEventListener("click", openPost);
    if (menuPublishBtn) {
      menuPublishBtn.addEventListener("click", () => {
        openPost();
        menuDropdown?.removeAttribute("open");
      });
    }

    document.querySelectorAll(".mini-action").forEach((btn) => {
      btn.addEventListener("click", openPost);
    });

    if (closePostModal) closePostModal.addEventListener("click", closePost);
    if (cancelPost) cancelPost.addEventListener("click", closePost);

    postModalOverlay.addEventListener("click", (e) => {
      if (e.target === postModalOverlay) closePost();
    });

    postFile.addEventListener("change", (e) => {
      const file = e.target.files?.[0];
      if (!file) return;

      uploadHint.textContent = file.name;
      const url = URL.createObjectURL(file);
      postPreview.classList.remove("hidden");

      if (file.type.startsWith("image/")) {
        postPreview.innerHTML = `<img src="${url}" alt="Previsualización" />`;
      } else if (file.type.startsWith("video/")) {
        postPreview.innerHTML = `<video src="${url}" controls></video>`;
      } else {
        postPreview.innerHTML = "";
        postPreview.classList.add("hidden");
      }
    });

    document.getElementById("publishPost").addEventListener("click", () => {
      alert("Publicación creada (mock). En backend luego la guardamos en DB.");
      closePost();
    });

    const oracleBlock = document.querySelector(".oracle-response-block");
    const oracleToggle = document.getElementById("oracleToggle");
    const oracleResponseText = document.getElementById("oracleResponseText");
    const oracleEmptyPrompt = document.getElementById("oracleEmptyPrompt");
    const hasOracleResponse = oracleBlock?.dataset.hasResponse !== "false";

    if (!hasOracleResponse) {
      oracleResponseText.classList.add("hidden");
      oracleEmptyPrompt.classList.remove("hidden");
      oracleToggle.checked = false;
    }

    const syncOracleVisibility = () => {
      if (!oracleToggle.checked || !hasOracleResponse) {
        oracleResponseText.classList.add("hidden");
      } else {
        oracleResponseText.classList.remove("hidden");
      }
    };

    if (oracleToggle) {
      oracleToggle.addEventListener("change", syncOracleVisibility);
      syncOracleVisibility();
    }
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Feed</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user feed-background">
  <!-- =========================
   *  BARRA SUPERIOR
   *  ========================= -->
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
      <button class="topbar-btn is-active" id="feedHomeBtn" type="button">🏠 Home</button>
      <button class="topbar-btn" type="button">🖼️ Galería</button>
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
          <button class="dropdown-action" id="menuPublishBtn" type="button" role="menuitem">
            Publicar
          </button>
          <a href="/home_user.html" role="menuitem">Mi Home</a>
          <a href="#" role="menuitem">Logros recientes</a>
          <a href="#" role="menuitem">Galería</a>
          <a href="/calendar.html" role="menuitem">Calendario</a>
          <a href="#" role="menuitem">Mi Biografía</a>
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <div class="feed-body">
      <section class="feed-grid" aria-label="Feed social">
        <!-- =========================
         *  LADO IZQUIERDO
         *  ========================= -->
        <aside class="feed-side feed-side-left" aria-label="Oráculo">
          <article class="panel oracle-panel">
            <div class="panel-head">
              <h2 class="panel-title">Tu imagen del Oráculo</h2>
              <span class="panel-badge">Última visión</span>
            </div>

            <div class="oracle-card">
              <img src="/css/oracle/Oracle1.png" alt="Última carta del Oráculo" />
            </div>

            <div class="oracle-response-block" data-has-response="true">
              <div class="oracle-toggle">
                <span class="oracle-toggle-label">Mostrar respuesta</span>
                <label class="switch">
                  <input type="checkbox" id="oracleToggle" checked />
                  <span class="slider"></span>
                </label>
              </div>

              <div class="oracle-response-title">Descripción de su respuesta:</div>
              <p class="oracle-response" id="oracleResponseText">
                “Cada paso que das hacia tu propósito abre nuevas puertas. La perseverancia será tu escudo
                hoy. Comparte tu avance y deja que otros también se inspiren.”
              </p>

              <button class="btn btn-outline btn-compact oracle-empty hidden" id="oracleEmptyPrompt" type="button">
                Responder ahora y publicar
              </button>
            </div>
          </article>
        </aside>

        <!-- =========================
         *  LADO CENTRAL
         *  ========================= -->
        <section class="feed-center">
          <article class="panel composer">
            <div class="composer-row">
              <img class="avatar avatar-sm" src="/assets/avatar-default.jpg" alt="Avatar" />
              <button class="composer-input" id="openPostModal" type="button">
                Publica algo que motive a tus seguidores...
              </button>
            </div>

            <div class="composer-actions">
              <button class="mini-action" type="button" data-kind="text">Texto</button>
              <button class="mini-action" type="button" data-kind="image">Imagen</button>
              <button class="mini-action" type="button" data-kind="video">Video</button>
            </div>
          </article>

          <article class="panel post">
            <div class="post-head">
              <div>
                <strong>Carlos Jiménez Duarte</strong>
                <span class="post-meta">· hace 20 min · Público</span>
              </div>
            </div>

            <p class="post-text">
              Hoy avancé en mi plan de estudios y terminé un módulo completo. #constancia #propósito
            </p>

            <div class="post-actions">
              <button class="post-btn" type="button">⭐ Estrella</button>
              <button class="post-btn" type="button">💬 Comentar</button>
              <button class="post-btn" type="button">🔁 Compartir</button>
            </div>
          </article>

          <article class="panel post">
            <div class="post-head">
              <div>
                <strong>María Fernanda López</strong>
                <span class="post-meta">· hace 1 hora · Público</span>
              </div>
            </div>

            <p class="post-text">
              Una caminata con mi equipo de Guardianes y una conversación que me recordó por qué empecé.
            </p>

            <div class="post-media">
              <img src="/assets/post-1.jpg" alt="Post con imagen" />
            </div>

            <div class="post-actions">
              <button class="post-btn" type="button">⭐ Estrella</button>
              <button class="post-btn" type="button">💬 Comentar</button>
              <button class="post-btn" type="button">🔁 Compartir</button>
            </div>
          </article>

          <article class="panel post">
            <div class="post-head">
              <div>
                <strong>Raúl Mendoza</strong>
                <span class="post-meta">· ayer · Público</span>
              </div>
            </div>

            <p class="post-text">
              “Si avanzas un 1% cada día, al final del año no serás el mismo”. ¿Qué es lo que más te motiva
              hoy? #hábitos
            </p>

            <div class="post-actions">
              <button class="post-btn" type="button">⭐ Estrella</button>
              <button class="post-btn" type="button">💬 Comentar</button>
              <button class="post-btn" type="button">🔁 Compartir</button>
            </div>
          </article>

          <article class="panel post">
            <div class="post-head">
              <div>
                <strong>Lucía Gómez</strong>
                <span class="post-meta">· hace 3 días · Público</span>
              </div>
            </div>

            <p class="post-text">
              Hoy grabé el video para mi primer taller. ¡Gracias por el apoyo! #crecimiento
            </p>

            <div class="post-media">
              <img src="/assets/post-2.jpg" alt="Post con imagen" />
            </div>

            <div class="post-actions">
              <button class="post-btn" type="button">⭐ Estrella</button>
              <button class="post-btn" type="button">💬 Comentar</button>
              <button class="post-btn" type="button">🔁 Compartir</button>
            </div>
          </article>
        </section>

        <!-- =========================
         *  LADO DERECHO
         *  ========================= -->
        <aside class="feed-side feed-side-right" aria-label="Perfil y accesos rápidos">
          <article class="panel profile-card feed-profile-card">
            <div class="profile-row">
              <a class="feed-profile-link" href="#">
                <img class="avatar" src="/assets/avatar-default.jpg" alt="Foto de perfil" />
              </a>
              <div class="profile-meta">
                <a class="profile-name feed-profile-link" href="#">Carlos Jiménez Duarte</a>
                <p class="profile-rank">@carlosjduarte</p>
                <a class="btn btn-outline btn-compact" href="#">Ver perfil</a>
              </div>
            </div>
          </article>

          <article class="panel">
            <h3 class="panel-title">Mi comunidad</h3>
            <ul class="feed-link-list">
              <li><a href="#">Seguidores</a></li>
              <li><a href="#">Logros recientes</a></li>
              <li><a href="#">Galería</a></li>
              <li><a href="/calendar.html">Calendario</a></li>
              <li><a href="#">Mi Biografía</a></li>
              <li><a href="#">Mensajería de Guardianes</a></li>
              <li><a href="#">Notificaciones</a></li>
            </ul>
          </article>

          <article class="panel guardian-panel">
            <h3 class="panel-title">Yo soy Guardián</h3>
            <p class="panel-muted">Escenario de gestión y notificaciones para Guardianes activos.</p>
            <a class="btn btn-primary btn-compact" href="#">Entrar al módulo de Guardianes</a>
          </article>

          <div class="feed-mini-footer">
            <a href="#">Términos y condiciones</a>
            <a href="#">Privacidad</a>
            <a href="#">Cookies</a>
            <a href="#">Idiomas</a>
          </div>
        </aside>
      </section>
    </div>
  </main>

  <!-- =========================
   *  MODAL: CREAR PUBLICACIÓN
   *  ========================= -->
  <div class="modal-overlay hidden" id="postModalOverlay" aria-hidden="true">
    <div class="modal modal-wide" role="dialog" aria-modal="true" aria-label="Crear publicación">
      <div class="modal-head">
        <h3>Crear publicación</h3>
        <button class="modal-close" type="button" id="closePostModal">✕</button>
      </div>

      <div class="modal-body">
        <div class="post-modal-top">
          <img class="avatar avatar-sm" src="/assets/avatar-default.jpg" alt="Avatar" />
          <div>
            <div class="post-modal-name"><strong>Carlos Jiménez Duarte</strong></div>
            <select class="modal-select" id="postVisibility">
              <option value="public">Público</option>
              <option value="private">Privado</option>
            </select>
          </div>
        </div>

        <textarea class="modal-textarea" id="postText" rows="5" placeholder="Escribe algo..."></textarea>

        <div class="upload-row">
          <label class="upload-btn" for="postFile">Adjuntar imagen o video</label>
          <input id="postFile" type="file" accept="image/*,video/*" class="hidden" />
          <div class="upload-hint" id="uploadHint">Sin archivo adjunto</div>
        </div>

        <div class="preview hidden" id="postPreview"></div>
      </div>

      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" id="cancelPost">Cancelar</button>
        <button class="btn btn-primary btn-compact" type="button" id="publishPost">Publicar</button>
      </div>
    </div>
  </div>
</div>
