<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";

  const API = "http://127.0.0.1:8000";
  let achievementsSyncError = "";
  let weeklySyncError = "";
  let weeklyLoading = true;
  let weeklyAchievements = [];
  const WEEKLY_CATEGORY_LINES = {
    publication_stars: "Del nacimiento de la luz a la soberanía estelar.",
    fulfilled_wishes: "El camino de orden, la palabra y la acción.",
    granted_wishes: "Cuando el servicio se convierte en vocación.",
    calendar_streak: "La Senda de la Constancia.",
    donation_stars: "El viaje hacia la unión con el Universo.",
    guardian_rank: "Hacía la conquista del corazón propio.",
  };

  const getAccessToken = () => localStorage.getItem("access_token") || "";

  const normalizeImagePath = (rawSrc) => {
    if (!rawSrc) return "";
    try {
      return new URL(rawSrc, window.location.origin).pathname;
    } catch (_error) {
      return rawSrc;
    }
  };

  const applyAllBadgeUnlockState = (achievementGroups = []) => {
    const unlockByImagePath = new Map();
    achievementGroups
      .filter((group) => Array.isArray(group))
      .forEach((group) => {
        group.forEach((achievement) => {
          unlockByImagePath.set(
            normalizeImagePath(achievement?.image_url || ""),
            Boolean(achievement?.unlocked),
          );
        });
      });

    const badgeItems = document.querySelectorAll(".badge-item");
    badgeItems.forEach((badgeItem) => {
      const badgeImage = badgeItem.querySelector("img");
      const imagePath = normalizeImagePath(badgeImage?.getAttribute("src") || "");
      if (!unlockByImagePath.has(imagePath)) return;

      const isUnlocked = unlockByImagePath.get(imagePath);
      badgeItem.classList.toggle("is-unlocked", isUnlocked);
      badgeItem.classList.toggle("is-locked", !isUnlocked);
    });
  };

  const clearAuthAndRedirectToLogin = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "/login.html";
  };

  const weekdayLabel = (isoValue) => {
    const date = new Date(isoValue);
    if (Number.isNaN(date.getTime())) return "Sin fecha";
    const text = date.toLocaleDateString("es-CO", { weekday: "long" });
    return text.charAt(0).toUpperCase() + text.slice(1);
  };

  const unlockHourLabel = (isoValue) => {
    const date = new Date(isoValue);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleTimeString("es-CO", { hour: "2-digit", minute: "2-digit" });
  };

  const weeklyCategoryLine = (category) => {
    return WEEKLY_CATEGORY_LINES[category] || "Logro desbloqueado en esta semana.";
  };

  const loadAchievementsState = async () => {
    achievementsSyncError = "";

    const token = getAccessToken();
    if (!token) {
      window.location.href = "/login.html";
      return;
    }

    try {
      const response = await fetch(`${API}/achievements/mine/state`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await response.json();

      if (response.status === 401) {
        clearAuthAndRedirectToLogin();
        return;
      }

      if (!response.ok) {
        throw new Error(data.detail || "No se pudo sincronizar el estado de logros.");
      }

      const totalStarsLabel = document.getElementById("achievementsStarsTotal");
      if (totalStarsLabel) {
        totalStarsLabel.textContent = Number(data.my_received_stars_total || 0).toLocaleString("es-CO");
      }

      applyAllBadgeUnlockState([
        data.publication_achievements || [],
        data.fulfilled_wishes_achievements || [],
        data.granted_wishes_achievements || [],
        data.calendar_achievements || [],
        data.donation_achievements || [],
        data.guardian_rank_achievements || [],
      ]);
    } catch (error) {
      achievementsSyncError = error.message || "No se pudo sincronizar el estado de logros.";
    }
  };

  const loadWeeklyAchievements = async () => {
    weeklySyncError = "";
    weeklyLoading = true;
    weeklyAchievements = [];

    const token = getAccessToken();
    if (!token) {
      weeklyLoading = false;
      window.location.href = "/login.html";
      return;
    }

    try {
      const response = await fetch(`${API}/achievements/mine/weekly`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await response.json();

      if (response.status === 401) {
        clearAuthAndRedirectToLogin();
        return;
      }

      if (!response.ok) {
        throw new Error(data.detail || "No se pudieron cargar los logros de esta semana.");
      }

      weeklyAchievements = Array.isArray(data.items) ? data.items : [];
    } catch (error) {
      weeklySyncError = error.message || "No se pudieron cargar los logros de esta semana.";
    } finally {
      weeklyLoading = false;
    }
  };

  onMount(() => {
    initPurposeCoverModule();
    void Promise.all([loadAchievementsState(), loadWeeklyAchievements()]);
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Logros</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user achievements-background">
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
        <details class="topbar-dropdown">
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

        <details class="topbar-dropdown">
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
          <a href="/messages.html" role="menuitem">Mensajes</a>
          </div>
        </details>
      </div>
    </header>

    <main class="user-home">

      <!-- =========================
       *  PORTADA / COVER
       *  ========================= -->
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

      <div class="achievements-body">
      <!-- =========================
       *  NAV / LINKS
       *  ========================= -->
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
          <span class="nav-icon">⭐</span>
          <span><strong id="achievementsStarsTotal">0</strong> estrellas</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
        <a class="nav-pill" href="/messages.html" title="Mensajes">Mensajes</a>
      </nav>

      <!-- =========================
       *  LOGROS
       *  ========================= -->
      <section class="achievements-shell" aria-label="Logros e insignias">
        <header class="achievements-head">
          <div>
            <h2 class="achievements-title">Logros e insignias</h2>
            <p class="achievements-subtitle">Ordenados como colección y notificación semanal.</p>
          </div>
          <div class="achievements-tags">
            <span class="panel-badge">Semana actual</span>
            <span class="panel-badge">Reinicio cada lunes</span>
          </div>
        </header>

        {#if achievementsSyncError}
          <p class="achievements-sync-error">{achievementsSyncError}</p>
        {/if}

        <article class="panel weekly-achievements">
          <div class="panel-head">
            <h3 class="panel-title">Logros obtenidos esta semana</h3>
            <span class="panel-badge">Más reciente primero</span>
          </div>
          <p class="panel-muted">
            Esta sección se vacía el lunes siguiente y vuelve a revelar los logros de la nueva semana.
          </p>

          {#if weeklyLoading}
            <p class="panel-muted week-empty">Cargando logros semanales...</p>
          {:else if weeklySyncError}
            <p class="achievements-sync-error">{weeklySyncError}</p>
          {:else if weeklyAchievements.length === 0}
            <p class="panel-muted week-empty">
              Aún no desbloqueaste logros esta semana. Cuando ocurra, aparecerán aquí.
            </p>
          {:else}
            <div class="weekly-list">
              {#each weeklyAchievements as achievement (achievement.achievement_key)}
                <article class="week-day">
                  <div class="week-day-title">{weekdayLabel(achievement.unlocked_at)}</div>
                  <div class="week-day-line">{weeklyCategoryLine(achievement.category)}</div>
                  <div class="week-achievement">
                    <img class="week-badge" src={achievement.image_url} alt={`Insignia ${achievement.title}`} />
                    <div class="week-info">
                      <strong>{achievement.title}</strong>
                      <span>{achievement.description}</span>
                      <span class="week-time">{unlockHourLabel(achievement.unlocked_at)}</span>
                    </div>
                  </div>
                </article>
              {/each}
            </div>
          {/if}
        </article>

        <section class="badge-collection" aria-label="Insignias">
          <div class="panel-head">
            <h3 class="panel-title">Insignias</h3>
            <span class="panel-badge">Colección completa</span>
          </div>

          <!-- =========================
           *  ESTRELLAS POR PUBLICACIONES
           *  ========================= -->
          <article class="panel badge-group" id="publicationStarsBadges">
            <div>
              <h3 class="panel-title">Del nacimiento de la luz a la soberanía estelar</h3>
              <p class="panel-muted">Sistema de logros — Estrellas por publicaciones.</p>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">I. Primer contacto con la luz</h4>
              <div class="badge-grid">
                <div class="badge-item is-unlocked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star1/1a.webp" alt="Insignia Alumbramiento" />
                    <span class="badge-label">Alumbramiento</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Alumbramiento</div>
                    <div class="badge-desc">Has alcanzado 1 estrella por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star1/1b.webp" alt="Insignia Estelar" />
                    <span class="badge-label">Estelar</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Estelar</div>
                    <div class="badge-desc">Has alcanzado 5 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star1/1c.webp" alt="Insignia Astral" />
                    <span class="badge-label">Astral</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Astral</div>
                    <div class="badge-desc">Has alcanzado 10 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star1/1d.webp" alt="Insignia Coleccionista de Estrellas" />
                    <span class="badge-label">Coleccionista de Estrellas</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Coleccionista de Estrellas</div>
                    <div class="badge-desc">Has alcanzado 30 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star1/1e.webp" alt="Insignia Astrónomo" />
                    <span class="badge-label">Astrónomo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Astrónomo</div>
                    <div class="badge-desc">Has alcanzado 100 estrellas por tus publicaciones</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">II. Observador del firmamento</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star2/2a.webp" alt="Insignia Cartógrafo del Cielo" />
                    <span class="badge-label">Cartógrafo del Cielo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Cartógrafo del Cielo</div>
                    <div class="badge-desc">Has alcanzado 200 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star2/2b.webp" alt="Insignia Vigilante del Firmamento" />
                    <span class="badge-label">Vigilante del Firmamento</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Vigilante del Firmamento</div>
                    <div class="badge-desc">Has alcanzado 300 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star2/2c.webp" alt="Insignia Tejedor de Constelaciones" />
                    <span class="badge-label">Tejedor de Constelaciones</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Tejedor de Constelaciones</div>
                    <div class="badge-desc">Has alcanzado 500 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star2/2d.webp" alt="Insignia Cronista Celeste" />
                    <span class="badge-label">Cronista Celeste</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Cronista Celeste</div>
                    <div class="badge-desc">Has alcanzado 800 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star2/2e.webp" alt="Insignia Intérprete de las Estrellas" />
                    <span class="badge-label">Intérprete de las Estrellas</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Intérprete de las Estrellas</div>
                    <div class="badge-desc">Has alcanzado 1.000 estrellas por tus publicaciones</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">III. Dominio celeste</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star3/3a.webp" alt="Insignia Arquitecto de Constelaciones" />
                    <span class="badge-label">Arquitecto de Constelaciones</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Arquitecto de Constelaciones</div>
                    <div class="badge-desc">Has alcanzado 1.500 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star3/3b.webp" alt="Insignia Guardián del Cielo Nocturno" />
                    <span class="badge-label">Guardián del Cielo Nocturno</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián del Cielo Nocturno</div>
                    <div class="badge-desc">Has alcanzado 2.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star3/3c.webp" alt="Insignia Sabio del Firmamento" />
                    <span class="badge-label">Sabio del Firmamento</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Sabio del Firmamento</div>
                    <div class="badge-desc">Has alcanzado 2.500 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star3/3d.webp" alt="Insignia Navegante Astral" />
                    <span class="badge-label">Navegante Astral</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Navegante Astral</div>
                    <div class="badge-desc">Has alcanzado 3.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star3/3e.webp" alt="Insignia Custodio de la Luz" />
                    <span class="badge-label">Custodio de la Luz</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Custodio de la Luz</div>
                    <div class="badge-desc">Has alcanzado 4.000 estrellas por tus publicaciones</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">IV. Expansión cósmica</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star4/4a.webp" alt="Insignia Heraldo Estelar" />
                    <span class="badge-label">Heraldo Estelar</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Heraldo Estelar</div>
                    <div class="badge-desc">Has alcanzado 5.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star4/4b.webp" alt="Insignia Señor de las Constelaciones" />
                    <span class="badge-label">Señor de las Constelaciones</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Señor de las Constelaciones</div>
                    <div class="badge-desc">Has alcanzado 10.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star4/4c.webp" alt="Insignia Maestro del Cielo Profundo" />
                    <span class="badge-label">Maestro del Cielo Profundo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Maestro del Cielo Profundo</div>
                    <div class="badge-desc">Has alcanzado 20.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star4/4d.webp" alt="Insignia Orquestador de Astros" />
                    <span class="badge-label">Orquestador de Astros</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Orquestador de Astros</div>
                    <div class="badge-desc">Has alcanzado 30.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star4/4e.webp" alt="Insignia Regente del Firmamento" />
                    <span class="badge-label">Regente del Firmamento</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Regente del Firmamento</div>
                    <div class="badge-desc">Has alcanzado 50.000 estrellas por tus publicaciones</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">V. Trascendencia estelar</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star5/5a.webp" alt="Insignia Forjador de Universos" />
                    <span class="badge-label">Forjador de Universos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Forjador de Universos</div>
                    <div class="badge-desc">Has alcanzado 70.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star5/5b.webp" alt="Insignia Portador del Cielo" />
                    <span class="badge-label">Portador del Cielo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Portador del Cielo</div>
                    <div class="badge-desc">Has alcanzado 100.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star5/5c.webp" alt="Insignia Soberano de las Estrellas" />
                    <span class="badge-label">Soberano de las Estrellas</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Soberano de las Estrellas</div>
                    <div class="badge-desc">Has alcanzado 150.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star5/5d.webp" alt="Insignia Arquitecto del Cosmos" />
                    <span class="badge-label">Arquitecto del Cosmos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Arquitecto del Cosmos</div>
                    <div class="badge-desc">Has alcanzado 200.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star5/5e.webp" alt="Insignia Vigía del Infinito" />
                    <span class="badge-label">Vigía del Infinito</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Vigía del Infinito</div>
                    <div class="badge-desc">Has alcanzado 300.000 estrellas por tus publicaciones</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">VI. Eternidad</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star6/6a.webp" alt="Insignia Hijo del Cosmos" />
                    <span class="badge-label">Hijo del Cosmos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Hijo del Cosmos</div>
                    <div class="badge-desc">Has alcanzado 600.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star6/6b.webp" alt="Insignia Conciencia Estelar" />
                    <span class="badge-label">Conciencia Estelar</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Conciencia Estelar</div>
                    <div class="badge-desc">Has alcanzado 1.000.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star6/6c.webp" alt="Insignia Alma del Firmamento" />
                    <span class="badge-label">Alma del Firmamento</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Alma del Firmamento</div>
                    <div class="badge-desc">Has alcanzado 1.500.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star6/6d.webp" alt="Insignia Trono de las Estrellas" />
                    <span class="badge-label">Trono de las Estrellas</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Trono de las Estrellas</div>
                    <div class="badge-desc">Has alcanzado 2.000.000 estrellas por tus publicaciones</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Astral/Star6/6e.webp" alt="Insignia Estrella Eterna" />
                    <span class="badge-label">Estrella Eterna</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Estrella Eterna</div>
                    <div class="badge-desc">Has alcanzado 5.000.000 estrellas por tus publicaciones</div>
                  </div>
                </div>
              </div>
            </div>
          </article>

          <!-- =========================
           *  DESEOS CUMPLIDOS
           *  ========================= -->
          <article class="panel badge-group">
            <div>
              <h3 class="panel-title">El camino de orden, la palabra y la acción</h3>
              <p class="panel-muted">Logros de deseos cumplidos.</p>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">I. Despertar de la acción</h4>
              <div class="badge-grid">
                <div class="badge-item is-unlocked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish1/1a.webp" alt="Insignia Realizador" />
                    <span class="badge-label">Realizador</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Realizador</div>
                    <div class="badge-desc">Has cumplido 1 deseo</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish1/1b.webp" alt="Insignia Comprometido" />
                    <span class="badge-label">Comprometido</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Comprometido</div>
                    <div class="badge-desc">Has cumplido 3 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish1/1c.webp" alt="Insignia Constante" />
                    <span class="badge-label">Constante</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Constante</div>
                    <div class="badge-desc">Has cumplido 7 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish1/1d.webp" alt="Insignia Visionario" />
                    <span class="badge-label">Visionario</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Visionario</div>
                    <div class="badge-desc">Has cumplido 10 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish1/1e.webp" alt="Insignia Ejecutor" />
                    <span class="badge-label">Ejecutor</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Ejecutor</div>
                    <div class="badge-desc">Has cumplido 20 deseos</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">II. Dominio personal</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish2/2a.webp" alt="Insignia Constructor de Metas" />
                    <span class="badge-label">Constructor de Metas</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Constructor de Metas</div>
                    <div class="badge-desc">Has cumplido 30 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish2/2b.webp" alt="Insignia Voluntad Activa" />
                    <span class="badge-label">Voluntad Activa</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Voluntad Activa</div>
                    <div class="badge-desc">Has cumplido 50 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish2/2c.webp" alt="Insignia Forjador de Logros" />
                    <span class="badge-label">Forjador de Logros</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Forjador de Logros</div>
                    <div class="badge-desc">Has cumplido 100 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish2/2d.webp" alt="Insignia Arquitecto de Deseos" />
                    <span class="badge-label">Arquitecto de Deseos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Arquitecto de Deseos</div>
                    <div class="badge-desc">Has cumplido 200 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish2/2e.webp" alt="Insignia Gestor de Propósito" />
                    <span class="badge-label">Gestor de Propósito</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Gestor de Propósito</div>
                    <div class="badge-desc">Has cumplido 300 deseos</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">III. Solidez y coherencia</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish3/3a.webp" alt="Insignia Hacedor Consistente" />
                    <span class="badge-label">Hacedor Consistente</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Hacedor Consistente</div>
                    <div class="badge-desc">Has cumplido 400 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish3/3b.webp" alt="Insignia Custodio de su Palabra" />
                    <span class="badge-label">Custodio de su Palabra</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Custodio de su Palabra</div>
                    <div class="badge-desc">Has cumplido 500 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish3/3c.webp" alt="Insignia Maestro de la Acción" />
                    <span class="badge-label">Maestro de la Acción</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Maestro de la Acción</div>
                    <div class="badge-desc">Has cumplido 600 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish3/3d.webp" alt="Insignia Consolidador" />
                    <span class="badge-label">Consolidador</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Consolidador</div>
                    <div class="badge-desc">Has cumplido 700 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish3/3e.webp" alt="Insignia Autor de su Camino" />
                    <span class="badge-label">Autor de su Camino</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Autor de su Camino</div>
                    <div class="badge-desc">Has cumplido 1.000 deseos</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">IV. Ejemplo visible</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Fulfilled/Wish4/4a.webp" alt="Insignia Referente de Coherencia" />
                    <span class="badge-label">Referente de Coherencia</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Referente de Coherencia</div>
                    <div class="badge-desc">Has cumplido 1.200 deseos</div>
                  </div>
                </div>
              </div>
            </div>
          </article>

          <!-- =========================
           *  DESEOS CONCEDIDOS
           *  ========================= -->
          <article class="panel badge-group">
            <div>
              <h3 class="panel-title">Cuando el servicio se convierte en vocación</h3>
              <p class="panel-muted">Logros de deseos concedidos.</p>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa I — Bondad consciente</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill1/1a.webp" alt="Insignia Amable" />
                    <span class="badge-label">Amable</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Amable</div>
                    <div class="badge-desc">Has ayudado a cumplir 1 deseo</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill1/1b.webp" alt="Insignia Generoso" />
                    <span class="badge-label">Generoso</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Generoso</div>
                    <div class="badge-desc">Has ayudado a cumplir 3 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill1/1c.webp" alt="Insignia Mano Abierta" />
                    <span class="badge-label">Mano Abierta</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Mano Abierta</div>
                    <div class="badge-desc">Has ayudado a cumplir 7 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill1/1d.webp" alt="Insignia Buen Samaritano" />
                    <span class="badge-label">Buen Samaritano</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Buen Samaritano</div>
                    <div class="badge-desc">Has ayudado a cumplir 10 deseos</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa II — Virtud activa</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill2/2a.webp" alt="Insignia Caballero de la Virtud" />
                    <span class="badge-label">Caballero de la Virtud</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Caballero de la Virtud</div>
                    <div class="badge-desc">Has ayudado a cumplir 20 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill2/2b.webp" alt="Insignia Servidor del Bien" />
                    <span class="badge-label">Servidor del Bien</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Servidor del Bien</div>
                    <div class="badge-desc">Has ayudado a cumplir 30 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill2/2c.webp" alt="Insignia Corazón Firme" />
                    <span class="badge-label">Corazón Firme</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Corazón Firme</div>
                    <div class="badge-desc">Has ayudado a cumplir 50 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill2/2d.webp" alt="Insignia Aliado de la Verdad" />
                    <span class="badge-label">Aliado de la Verdad</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Aliado de la Verdad</div>
                    <div class="badge-desc">Has ayudado a cumplir 70 deseos</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa III — Servicio constante</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill3/3a.webp" alt="Insignia Benefactor" />
                    <span class="badge-label">Benefactor</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Benefactor</div>
                    <div class="badge-desc">Has ayudado a cumplir 100 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill3/3b.webp" alt="Insignia Pilar de Apoyo" />
                    <span class="badge-label">Pilar de Apoyo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Pilar de Apoyo</div>
                    <div class="badge-desc">Has ayudado a cumplir 150 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill3/3c.webp" alt="Insignia Guardián Solidario" />
                    <span class="badge-label">Guardián Solidario</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián Solidario</div>
                    <div class="badge-desc">Has ayudado a cumplir 200 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill3/3d.webp" alt="Insignia Manantial de Ayuda" />
                    <span class="badge-label">Manantial de Ayuda</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Manantial de Ayuda</div>
                    <div class="badge-desc">Has ayudado a cumplir 300 deseos</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa IV — Custodia y responsabilidad</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill4/4a.webp" alt="Insignia Custodio del Bien" />
                    <span class="badge-label">Custodio del Bien</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Custodio del Bien</div>
                    <div class="badge-desc">Has ayudado a cumplir 400 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill4/4b.webp" alt="Insignia Protector de Sueños" />
                    <span class="badge-label">Protector de Sueños</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Protector de Sueños</div>
                    <div class="badge-desc">Has ayudado a cumplir 500 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill4/4c.webp" alt="Insignia Arquitecto de la Verdad" />
                    <span class="badge-label">Arquitecto de la Verdad</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Arquitecto de la Verdad</div>
                    <div class="badge-desc">Has ayudado a cumplir 600 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill4/4d.webp" alt="Insignia Guía por el Ejemplo" />
                    <span class="badge-label">Guía por el Ejemplo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guía por el Ejemplo</div>
                    <div class="badge-desc">Has ayudado a cumplir 700 deseos</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa V — Trascendencia del acto</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill5/5a.webp" alt="Insignia Heraldo de la Generosidad" />
                    <span class="badge-label">Heraldo de la Generosidad</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Heraldo de la Generosidad</div>
                    <div class="badge-desc">Has ayudado a cumplir 1.000 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill5/5b.webp" alt="Insignia Tejedor de Destinos" />
                    <span class="badge-label">Tejedor de Destinos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Tejedor de Destinos</div>
                    <div class="badge-desc">Has ayudado a cumplir 2.000 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill5/5c.webp" alt="Insignia Columna de la Comunidad" />
                    <span class="badge-label">Columna de la Comunidad</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Columna de la Comunidad</div>
                    <div class="badge-desc">Has ayudado a cumplir 3.000 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Granted/Fullfill5/5d.webp" alt="Insignia Benefactor Eterno" />
                    <span class="badge-label">Benefactor Eterno</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Benefactor Eterno</div>
                    <div class="badge-desc">Has ayudado a cumplir 5.000 deseos</div>
                  </div>
                </div>
              </div>
            </div>
          </article>

          <!-- =========================
           *  CALENDARIO
           *  ========================= -->
          <article class="panel badge-group">
            <div>
              <h3 class="panel-title">La Senda de la Constancia</h3>
              <p class="panel-muted">Logros de calendario.</p>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa I — El inicio (descubrimiento)</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar1/1a.webp" alt="Insignia Aficionado" />
                    <span class="badge-label">Aficionado</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Aficionado</div>
                    <div class="badge-desc">Has hecho tu 1° publicación en el calendario</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar1/1b.webp" alt="Insignia Inspirado" />
                    <span class="badge-label">Inspirado</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Inspirado</div>
                    <div class="badge-desc">Has publicado 3 días consecutivos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar1/1c.webp" alt="Insignia Disciplinado" />
                    <span class="badge-label">Disciplinado</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Disciplinado</div>
                    <div class="badge-desc">Has tenido una racha de 7 días de publicaciones</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa II — El hábito (estructura)</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar2/2a.webp" alt="Insignia Constante" />
                    <span class="badge-label">Constante</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Constante</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 15
                      días</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar2/2b.webp" alt="Insignia Comprometido" />
                    <span class="badge-label">Comprometido</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Comprometido</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 21
                      días</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar2/2c.webp" alt="Insignia Persistente" />
                    <span class="badge-label">Persistente</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Persistente</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 30
                      días</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa III — La identidad (arraigo)</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar3/3a.webp" alt="Insignia Forjador del Hábito" />
                    <span class="badge-label">Forjador del Hábito</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Forjador del Hábito</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 90
                      días</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar3/3b.webp" alt="Insignia Vinculado al Ritmo" />
                    <span class="badge-label">Vinculado al Ritmo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Vinculado al Ritmo</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 120
                      días</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar3/3c.webp" alt="Insignia Fiel al Proceso" />
                    <span class="badge-label">Fiel al Proceso</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Fiel al Proceso</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 150
                      días</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa IV — La madurez (resistencia)</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar4/4a.webp" alt="Insignia Inquebrantable" />
                    <span class="badge-label">Inquebrantable</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Inquebrantable</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 180
                      días</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar4/4b.webp" alt="Insignia Custodio del Ritmo" />
                    <span class="badge-label">Custodio del Ritmo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Custodio del Ritmo</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 220
                      días</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar4/4c.webp" alt="Insignia Arquitecto del Tiempo" />
                    <span class="badge-label">Arquitecto del Tiempo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Arquitecto del Tiempo</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 250
                      días</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa V — La maestría (ejemplo)</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar5/5a.webp" alt="Insignia Ejemplo Vivo" />
                    <span class="badge-label">Ejemplo Vivo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Ejemplo Vivo</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 280
                      días</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar5/5b.webp" alt="Insignia Pilar de la Comunidad" />
                    <span class="badge-label">Pilar de la Comunidad</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Pilar de la Comunidad</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 310
                      días</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar5/5c.webp" alt="Insignia Testimonio de Perseverancia" />
                    <span class="badge-label">Testimonio de Perseverancia</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Testimonio de Perseverancia</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 340
                      días</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa VI — La consagración (año completo)</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Calendar/Calendar6/6a.webp" alt="Insignia Guardián del Tiempo" />
                    <span class="badge-label">Guardián del Tiempo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián del Tiempo</div>
                    <div class="badge-desc">Has publicado activamente en esta red social, manteniendo una racha de 365
                      días</div>
                  </div>
                </div>
              </div>
            </div>
          </article>

          <!-- =========================
           *  DONACIÓN DE ESTRELLAS
           *  ========================= -->
          <article class="panel badge-group" id="donationStarsBadges">
            <div>
              <h3 class="panel-title">El viaje hacia la unión con el Universo</h3>
              <p class="panel-muted">Logros de donación de estrellas.</p>
            </div>

            <div class="badge-grid badge-grid-5">
              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img src="/css/AKI/Donation/1.webp" alt="Insignia Explorador del Misterio" />
                  <span class="badge-label">Explorador del Misterio</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel I — Primer desprendimiento</div>
                  <div class="badge-name">Explorador del Misterio</div>
                  <div class="badge-desc">Has acumulado una donación de más de 1.000 estrellas al Fondo Común de
                    Estrellas</div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img src="/css/AKI/Donation/2.webp" alt="Insignia Confiado en el Universo" />
                  <span class="badge-label">Confiado en el Universo</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel II — Confianza inicial</div>
                  <div class="badge-name">Confiado en el Universo</div>
                  <div class="badge-desc">Has acumulado una donación de más de 5.000 estrellas al Fondo Común de
                    Estrellas</div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img src="/css/AKI/Donation/3.webp" alt="Insignia Creyente de las Nebulosas" />
                  <span class="badge-label">Creyente de las Nebulosas</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel III — Fe cósmica</div>
                  <div class="badge-name">Creyente de las Nebulosas</div>
                  <div class="badge-desc">Has acumulado una donación de más de 10.000 estrellas al Fondo Común de
                    Estrellas</div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img src="/css/AKI/Donation/4.webp" alt="Insignia Guardián del Flujo Estelar" />
                  <span class="badge-label">Guardián del Flujo Estelar</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel IV — Comprensión del flujo</div>
                  <div class="badge-name">Guardián del Flujo Estelar</div>
                  <div class="badge-desc">Has acumulado una donación de más de 20.000 estrellas al Fondo Común de
                    Estrellas</div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img src="/css/AKI/Donation/5.webp" alt="Insignia Portador del Vacío Fértil" />
                  <span class="badge-label">Portador del Vacío Fértil</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel V — Entrega consciente</div>
                  <div class="badge-name">Portador del Vacío Fértil</div>
                  <div class="badge-desc">Has acumulado una donación de más de 50.000 estrellas al Fondo Común de
                    Estrellas</div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img src="/css/AKI/Donation/6.webp" alt="Insignia Custodio del Fondo Común" />
                  <span class="badge-label">Custodio del Fondo Común</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel VI — Servicio silencioso</div>
                  <div class="badge-name">Custodio del Fondo Común</div>
                  <div class="badge-desc">Has acumulado una donación de más de 100.000 estrellas al Fondo Común de
                    Estrellas</div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img src="/css/AKI/Donation/7.webp" alt="Insignia Tejedor de Constelaciones" />
                  <span class="badge-label">Tejedor de Constelaciones</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel VII — Sabiduría del compartir</div>
                  <div class="badge-name">Tejedor de Constelaciones</div>
                  <div class="badge-desc">Has acumulado una donación de más de 200.000 estrellas al Fondo Común de
                    Estrellas</div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img src="/css/AKI/Donation/8.webp" alt="Insignia Voz del Silencio Cósmico" />
                  <span class="badge-label">Voz del Silencio Cósmico</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel VIII — Donación como lenguaje</div>
                  <div class="badge-name">Voz del Silencio Cósmico</div>
                  <div class="badge-desc">Has acumulado una donación de más de 300.000 estrellas al Fondo Común de
                    Estrellas</div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img src="/css/AKI/Donation/9.webp" alt="Insignia Arquitecto del Bien Común" />
                  <span class="badge-label">Arquitecto del Bien Común</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel IX — Trascendencia colectiva</div>
                  <div class="badge-name">Arquitecto del Bien Común</div>
                  <div class="badge-desc">Has acumulado una donación de más de 500.000 estrellas al Fondo Común de
                    Estrellas</div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img src="/css/AKI/Donation/10.webp" alt="Insignia Semilla del Infinito" />
                  <span class="badge-label">Semilla del Infinito</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel X — Mito</div>
                  <div class="badge-name">Semilla del Infinito</div>
                  <div class="badge-desc">Has acumulado una donación de más de 1.000.000 estrellas al Fondo Común de
                    Estrellas</div>
                </div>
              </div>
            </div>
          </article>

          <!-- =========================
           *  JERARQUÍA DE GUARDIANES
           *  ========================= -->
          <article class="panel badge-group">
            <div>
              <h3 class="panel-title">Hacía la conquista del corazón propio</h3>
              <p class="panel-muted">Logros de Jerarquía de Guardianes.</p>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Rangos de Guardianes</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Ranks/1.webp" alt="Insignia Aspirante" />
                    <span class="badge-label">Aspirante</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Aspirante</div>
                    <div class="badge-desc">Has ascendido al Rango 1 de la Jerarquía de Guardianes: ¡Ahora eres
                      Aspirante!</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Ranks/2.webp" alt="Insignia Aprendiz" />
                    <span class="badge-label">Aprendiz</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Aprendiz</div>
                    <div class="badge-desc">Has ascendido al Rango 2 de la Jerarquía de Guardianes: ¡Ahora eres
                      Aprendiz!</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Ranks/3.webp" alt="Insignia Guardián" />
                    <span class="badge-label">Guardián</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián</div>
                    <div class="badge-desc">Has ascendido al Rango 1 de la Jerarquía de Guardianes: ¡Ahora eres
                      Guardián!</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Ranks/4.webp" alt="Insignia Guardián Consagrado" />
                    <span class="badge-label">Guardián Consagrado</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián Consagrado</div>
                    <div class="badge-desc">Has ascendido al Rango 1 de la Jerarquía de Guardianes: ¡Ahora eres Guardián
                      Consagrado!</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Ranks/5.webp" alt="Insignia Guardián Mayor" />
                    <span class="badge-label">Guardián Mayor</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián Mayor</div>
                    <div class="badge-desc">Has ascendido al Rango 1 de la Jerarquía de Guardianes: ¡Ahora eres Guardián
                      Mayor!</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Ranks/6.webp" alt="Insignia Guardián del Logos" />
                    <span class="badge-label">Guardián del Logos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián del Logos</div>
                    <div class="badge-desc">Has ascendido al Rango 1 de la Jerarquía de Guardianes: ¡Ahora eres Guardián
                      del Logos!</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Ranks/7.webp" alt="Insignia Guardián del Umbral" />
                    <span class="badge-label">Guardián del Umbral</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián del Umbral</div>
                    <div class="badge-desc">Has ascendido al Rango 1 de la Jerarquía de Guardianes: ¡Ahora eres Guardián
                      del Umbral!</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img src="/css/AKI/Ranks/8.webp" alt="Insignia Guardián de Guardianes" />
                    <span class="badge-label">Guardián de Guardianes</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián de Guardianes</div>
                    <div class="badge-desc">Has ascendido al Rango 1 de la Jerarquía de Guardianes: ¡Ahora eres Guardián
                      de Guardianes!</div>
                  </div>
                </div>
              </div>
            </div>
          </article>
        </section>
      </section>
      </div>

    </main>

    <!-- FOOTER reutilizado -->
    <footer class="kiadez-footer">
      <div class="footer-main">

        <div class="footer-column footer-origin">
          <p class="footer-poem">
            Kiadez fue llamado por una estrella a subir el Monte Manjaro.<br>
            No para dominar, sino para orientar.<br>
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
