<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";

  const API = "http://127.0.0.1:8000";
  const GUARDIAN_REQUIRED_RANK = 3;

  const getAccessToken = () => localStorage.getItem("access_token") || "";

  const parseResponseJson = async (res) => {
    try {
      return await res.json();
    } catch {
      return {};
    }
  };

  const apiFetch = async (path, options = {}) => {
    const token = getAccessToken();
    if (!token) {
      window.location.href = "/login.html";
      throw new Error("No hay sesión activa.");
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    };
    const res = await fetch(`${API}${path}`, { ...options, headers });
    if (res.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login.html";
      throw new Error("Sesión expirada.");
    }
    return res;
  };

  let guardianRank = 0;
  let isGuardian = false;
  let isLoading = true;
  let loadError = "";

  const modules = [
    {
      key: "reported_posts",
      icon: "🚩",
      title: "Publicaciones denunciadas",
      note: "Revisar reportes y tomar acciones.",
    },
    {
      key: "reported_profiles",
      icon: "🧾",
      title: "Perfiles denunciados",
      note: "Validar perfiles y resolver apelaciones.",
    },
    {
      key: "wish_management",
      icon: "🪄",
      title: "Gestión de deseos",
      note: "Solicitudes: “Yo puedo cumplir este deseo”.",
    },
    {
      key: "messaging",
      icon: "💬",
      title: "Mensajería",
      note: "Conversaciones y coordinación con usuarios.",
    },
  ];

  let activeModuleKey = modules[0].key;

  const setActiveModule = (key) => {
    activeModuleKey = String(key || modules[0].key);
  };

  const getActiveModule = () => modules.find((item) => item.key === activeModuleKey) || modules[0];

  onMount(() => {
    document.body.dataset.visitor = "false";

    (async () => {
      isLoading = true;
      loadError = "";
      guardianRank = 0;
      isGuardian = false;
      try {
        const res = await apiFetch("/auth/me");
        const data = await parseResponseJson(res);
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo cargar tu perfil.");
        }
        guardianRank = Number(data?.guardian_rank || 0) || 0;
        isGuardian = guardianRank >= GUARDIAN_REQUIRED_RANK;
      } catch (err) {
        loadError = err?.message || "No se pudo cargar el Centro del Guardián.";
      } finally {
        isLoading = false;
      }
    })();
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Centro del Guardián</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background settings-page guardian-center-page">
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
          <img src="/assets/avatar-default.jpg" alt="Perfil de usuario" />
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
    <div class="home-body settings-body guardian-center-body">
      <section class="panel guardian-center-panel" aria-label="Centro del Guardián">
        <div class="panel-head guardian-center-head">
          <div>
            <h2 class="panel-title">Centro del Guardián</h2>
            <p class="panel-muted guardian-center-subtitle">
              Escenario de autoridad para Guardianes. Aquí se gestionan reportes, solicitudes y coordinación.
            </p>
          </div>
          <span class="panel-badge">
            {#if isLoading}
              Cargando...
            {:else if isGuardian}
              Guardián · Rango {guardianRank}
            {:else}
              Acceso restringido
            {/if}
          </span>
        </div>

        {#if loadError}
          <div class="guardian-center-empty is-error">{loadError}</div>
        {:else if isLoading}
          <div class="guardian-center-empty">Cargando tu autorización...</div>
        {:else if !isGuardian}
          <div class="guardian-center-lock">
            <p class="guardian-center-lock-text">
              Este módulo está disponible solo para usuarios con rango de Guardián (Rango {GUARDIAN_REQUIRED_RANK}).
            </p>
            <div class="guardian-center-lock-actions">
              <a class="btn btn-outline btn-compact" href="/guardians-rank.html">Ver rangos</a>
              <a class="btn btn-primary btn-compact" href="/be-a-guardian.html">Ser Guardián</a>
            </div>
          </div>
        {:else}
          <div class="settings-actions guardian-center-actions" aria-label="Módulos del Guardián">
            {#each modules as module (module.key)}
              <button
                type="button"
                class={`settings-action guardian-center-action${activeModuleKey === module.key ? " is-active" : ""}`}
                aria-pressed={activeModuleKey === module.key}
                on:click={() => setActiveModule(module.key)}
              >
                <span class="settings-action-icon" aria-hidden="true">{module.icon}</span>
                <span class="settings-action-meta">
                  <span class="settings-action-label">{module.title}</span>
                  <span class="settings-action-note">{module.note}</span>
                </span>
                <span class="guardian-center-cta" aria-hidden="true">Abrir</span>
              </button>
            {/each}
          </div>

          <div class="guardian-center-divider" aria-hidden="true"></div>

          {@const activeModule = getActiveModule()}
          <section class="guardian-center-module" aria-label={activeModule.title}>
            <div class="guardian-center-module-head">
              <h3 class="guardian-center-module-title">{activeModule.title}</h3>
              <span class="guardian-center-module-pill">Próximamente</span>
            </div>
            <p class="panel-muted guardian-center-module-note">
              Este módulo está listo en interfaz. Mañana lo conectamos con base de datos y lógica real.
            </p>

            {#if activeModuleKey === "reported_posts"}
              <div class="guardian-center-empty">No hay publicaciones denunciadas por ahora.</div>
            {:else if activeModuleKey === "reported_profiles"}
              <div class="guardian-center-empty">No hay perfiles denunciados por ahora.</div>
            {:else if activeModuleKey === "wish_management"}
              <div class="guardian-center-empty">
                Aquí aparecerán las solicitudes de otros usuarios para que un Guardián pueda cumplir sus deseos.
              </div>
            {:else if activeModuleKey === "messaging"}
              <div class="guardian-center-empty">
                Aquí aparecerán conversaciones y coordinación entre Guardianes y usuarios.
              </div>
            {/if}
          </section>
        {/if}
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

