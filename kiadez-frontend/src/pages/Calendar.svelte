<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";

  const API = "http://127.0.0.1:8000";
  const MIN_YEAR = 2000;
  const MAX_YEAR = 2100;

  const MONTH_LABELS = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
  ];

  const DAILY_METRIC_DEFINITIONS = [
    { key: "stars_received", icon: "⭐", label: "Estrellas" },
    { key: "fulfilled_wishes", icon: "✅", label: "Deseos cumplidos" },
    { key: "public_wishes", icon: "🌟", label: "Deseos públicos" },
    { key: "achievements", icon: "🏆", label: "Logros" },
    { key: "posts", icon: "📝", label: "Publicaciones" },
  ];

  let isViewingOwnProfile = true;
  let viewerUserId = null;
  let viewerUsername = "";
  let activeProfileUserId = null;
  let activeProfileUsername = "";
  let activeProfileFullName = "";

  let pageTitle = "Kiadez — Calendario";
  let calendarTitle = "Calendario";
  let calendarYear = new Date().getUTCFullYear();

  let calendarAllowed = true;
  let calendarAccessError = "";
  let calendarLoading = false;
  let calendarLoadError = "";

  let calendarItems = [];
  let activeDaysTotal = 0;
  let todayUtc = "";
  let selectedDateUtc = "";

  const getAccessToken = () =>
    localStorage.getItem("access_token") || localStorage.getItem("kiadez_access_token") || "";

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
      throw new Error("No hay sesión activa.");
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    };
    const res = await fetch(`${API}${path}`, { ...options, headers });
    if (res.status === 401) {
      throw new Error("Sesión expirada. Inicia sesión nuevamente.");
    }
    return res;
  };

  const normalizeUsername = (value) => {
    let normalized = String(value || "").trim().toLowerCase();
    while (normalized.startsWith("@")) normalized = normalized.slice(1);
    return normalized;
  };

  const parsePositiveId = (value) => {
    const parsed = Number(value || 0);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : null;
  };

  const toIsoDateUtc = (value) => {
    if (!value) return "";
    if (typeof value === "string") {
      const normalized = value.trim();
      if (/^\d{4}-\d{2}-\d{2}$/.test(normalized)) return normalized;
      const parsed = new Date(normalized);
      if (Number.isNaN(parsed.getTime())) return "";
      return parsed.toISOString().slice(0, 10);
    }
    if (value instanceof Date) {
      if (Number.isNaN(value.getTime())) return "";
      return value.toISOString().slice(0, 10);
    }
    return "";
  };

  const formatCount = (value) => {
    const safe = Number.isFinite(Number(value)) ? Number(value) : 0;
    return safe.toLocaleString("es-CO");
  };

  const formatDateLabel = (isoDate) => {
    const normalized = toIsoDateUtc(isoDate);
    if (!normalized) return "";
    try {
      const dt = new Date(`${normalized}T00:00:00Z`);
      return new Intl.DateTimeFormat("es-CO", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
        timeZone: "UTC",
      }).format(dt);
    } catch {
      return normalized;
    }
  };

  const fetchViewerIdentity = async () => {
    const res = await apiFetch("/auth/me");
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(data.detail || "No se pudo cargar tu perfil.");
    }
    const userId = Number(data?.user_number);
    return {
      user_id: Number.isFinite(userId) && userId > 0 ? userId : null,
      username: normalizeUsername(data?.username || ""),
    };
  };

  const fetchFollowProfile = async ({ userId = null, username = null } = {}) => {
    const idValue = Number(userId);
    const usernameValue = normalizeUsername(username || "");
    if (Number.isFinite(idValue) && idValue > 0) {
      const res = await apiFetch(`/follows/profile?user_id=${encodeURIComponent(String(idValue))}`);
      const data = await parseResponseJson(res);
      if (!res.ok) throw new Error(data.detail || "No se pudo cargar el perfil.");
      return data;
    }
    if (usernameValue) {
      const res = await apiFetch(`/follows/profile?username=${encodeURIComponent(usernameValue)}`);
      const data = await parseResponseJson(res);
      if (!res.ok) throw new Error(data.detail || "No se pudo cargar el perfil.");
      return data;
    }
    throw new Error("Parámetros inválidos para cargar perfil.");
  };

  const buildViewerHomeUrl = () => {
    if (viewerUsername) return `/home_user.html?u=${encodeURIComponent(viewerUsername)}`;
    if (viewerUserId) return `/home_user.html?id=${encodeURIComponent(String(viewerUserId))}`;
    return "/home_user.html";
  };

  const buildProfileQueryParams = () => {
    if (activeProfileUsername) return { key: "u", value: activeProfileUsername };
    if (activeProfileUserId) return { key: "id", value: String(activeProfileUserId) };
    return null;
  };

  const buildProfileModuleUrl = (path) => {
    const raw = String(path || "").trim();
    if (!raw) return "";
    try {
      const url = new URL(raw, window.location.origin);
      const qp = buildProfileQueryParams();
      url.searchParams.delete("u");
      url.searchParams.delete("id");
      if (qp) url.searchParams.set(qp.key, qp.value);
      return `${url.pathname}${url.search}`;
    } catch {
      return raw;
    }
  };

  const PROFILE_MODULE_ROUTES = {
    home: "/home_user.html",
    public_wishes: "/my-public-whishes.html",
    fulfilled_wishes: "/my-fulfilled-whises.html",
    calendar: "/calendar.html",
    oracle: "/oracle.html",
  };

  const syncProfileModuleLinks = () => {
    document.querySelectorAll("a[data-profile-module]").forEach((link) => {
      const key = String(link.getAttribute("data-profile-module") || "").trim();
      const basePath = PROFILE_MODULE_ROUTES[key] || link.getAttribute("href") || "";
      const nextHref = buildProfileModuleUrl(basePath);
      if (nextHref) link.href = nextHref;
    });
  };

  const setMyHomeLinks = (href) => {
    const nextHref = String(href || "").trim();
    if (!nextHref) return;
    document.querySelectorAll("a[data-my-home]").forEach((link) => {
      link.href = nextHref;
    });
  };

  const applyReadOnlyProfileMode = () => {
    document.body.dataset.visitor = "true";
    document.querySelectorAll('a[href="/my-private-whishes.html"]').forEach((link) => link.classList.add("hidden"));
    document.getElementById("btnChangeCover")?.classList.add("hidden");
    document.getElementById("btnEditPurposes")?.classList.add("hidden");
  };

  const applyCalendarHeader = () => {
    pageTitle = isViewingOwnProfile
      ? "Kiadez — Calendario"
      : `Kiadez — Calendario de ${activeProfileFullName || "usuario"}`;
    calendarTitle = isViewingOwnProfile
      ? `Calendario ${calendarYear}`
      : `Calendario de ${activeProfileFullName || "usuario"} · ${calendarYear}`;
  };

  const resolveProfileContext = async () => {
    const params = new URLSearchParams(window.location.search);
    const requestedIdRaw = params.get("id");
    const requestedId = Number(requestedIdRaw);
    const requestedUserId = Number.isFinite(requestedId) && requestedId > 0 ? requestedId : null;
    const requestedUsername = normalizeUsername(params.get("u") || "");

    const me = await fetchViewerIdentity();
    viewerUserId = me.user_id;
    viewerUsername = me.username;

    activeProfileUserId = viewerUserId;
    activeProfileUsername = viewerUsername;
    activeProfileFullName = "";
    isViewingOwnProfile = true;
    document.body.dataset.visitor = "false";

    const wantsOtherProfile = Boolean(requestedUserId || requestedUsername);
    if (wantsOtherProfile) {
      const isSelfById = requestedUserId && viewerUserId && requestedUserId === viewerUserId;
      const isSelfByUsername = requestedUsername && viewerUsername && requestedUsername === viewerUsername;
      if (!isSelfById && !isSelfByUsername) {
        const profile = await fetchFollowProfile({
          userId: requestedUserId,
          username: requestedUserId ? null : requestedUsername,
        });
        activeProfileUserId = parsePositiveId(profile?.user_id) || requestedUserId;
        activeProfileUsername = normalizeUsername(profile?.username || requestedUsername);
        activeProfileFullName = String(profile?.full_name || "").trim();
        isViewingOwnProfile = Boolean(viewerUserId && activeProfileUserId === viewerUserId);
        if (!isViewingOwnProfile) {
          applyReadOnlyProfileMode();
        }
      }
    }

    setMyHomeLinks(buildViewerHomeUrl());
    syncProfileModuleLinks();
    applyCalendarHeader();
  };

  const fetchCalendarYearActivity = async () => {
    const profileId = parsePositiveId(activeProfileUserId);
    const endpoint =
      !isViewingOwnProfile && profileId
        ? `/calendar/user/${encodeURIComponent(String(profileId))}?year=${encodeURIComponent(String(calendarYear))}`
        : `/calendar/mine?year=${encodeURIComponent(String(calendarYear))}`;

    const res = await apiFetch(endpoint);
    const data = await parseResponseJson(res);
    if (!res.ok) {
      const detail = data?.detail || "No se pudo cargar el calendario.";
      const err = new Error(detail);
      err.status = res.status;
      throw err;
    }
    return data;
  };

  const ensureSelectedDate = () => {
    const items = Array.isArray(calendarItems) ? calendarItems : [];
    if (!items.length) {
      selectedDateUtc = "";
      return;
    }

    const selectedExists = items.some((item) => toIsoDateUtc(item?.date_utc) === selectedDateUtc);
    if (selectedExists) return;

    const todayNormalized = toIsoDateUtc(todayUtc);
    const todayItem = items.find((item) => toIsoDateUtc(item?.date_utc) === todayNormalized);
    if (todayItem) {
      selectedDateUtc = todayNormalized;
      return;
    }

    selectedDateUtc = toIsoDateUtc(items[0]?.date_utc);
  };

  const loadCalendarYearActivity = async () => {
    if (!calendarAllowed) return;

    calendarLoading = true;
    calendarLoadError = "";

    try {
      const data = await fetchCalendarYearActivity();
      const returnedYear = Number(data?.year || calendarYear);
      if (Number.isFinite(returnedYear) && returnedYear >= MIN_YEAR && returnedYear <= MAX_YEAR) {
        calendarYear = returnedYear;
      }

      calendarItems = Array.isArray(data?.items) ? data.items : [];
      activeDaysTotal = Number(data?.active_days_total || 0);
      todayUtc = toIsoDateUtc(data?.today_utc);

      calendarAllowed = true;
      calendarAccessError = "";
      ensureSelectedDate();
      applyCalendarHeader();
    } catch (error) {
      const status = Number(error?.status || 0);
      if (status === 403) {
        calendarAllowed = false;
        calendarAccessError = error?.message || "Este calendario es privado.";
        calendarItems = [];
        activeDaysTotal = 0;
        selectedDateUtc = "";
      } else {
        calendarLoadError = error?.message || "No se pudo cargar el calendario.";
      }
    } finally {
      calendarLoading = false;
    }
  };

  const setSelectedDate = (isoDate) => {
    selectedDateUtc = toIsoDateUtc(isoDate);
  };

  const changeYear = async (offset) => {
    const nextYear = Math.max(MIN_YEAR, Math.min(MAX_YEAR, Number(calendarYear || 0) + Number(offset || 0)));
    if (nextYear === calendarYear) return;
    calendarYear = nextYear;
    applyCalendarHeader();
    await loadCalendarYearActivity();
  };

  const buildYearMonths = ({ year, items, selectedIsoDate, todayIsoDate }) => {
    const itemMap = new Map(
      (Array.isArray(items) ? items : []).map((item) => [toIsoDateUtc(item?.date_utc), item])
    );

    const months = [];
    for (let monthIndex = 0; monthIndex < 12; monthIndex += 1) {
      const monthNumber = monthIndex + 1;
      const daysInMonth = new Date(Date.UTC(year, monthNumber, 0)).getUTCDate();
      const firstWeekday = (new Date(Date.UTC(year, monthIndex, 1)).getUTCDay() + 6) % 7;

      const days = [];
      let activeDays = 0;
      for (let day = 1; day <= daysInMonth; day += 1) {
        const isoDate = `${year}-${String(monthNumber).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
        const item = itemMap.get(isoDate);

        const stars = Number(item?.stars_received || 0);
        const fulfilled = Number(item?.fulfilled_wishes || 0);
        const publicWishes = Number(item?.public_wishes || 0);
        const achievements = Number(item?.achievements || 0);
        const posts = Number(item?.posts || 0);
        const total = Number(item?.total_interactions || stars + fulfilled + publicWishes + achievements + posts);
        const hasActivity = Boolean(item?.has_activity || total > 0);
        if (hasActivity) activeDays += 1;

        days.push({
          date_utc: isoDate,
          hasActivity,
          total,
          isSelected: isoDate === selectedIsoDate,
          isToday: isoDate === todayIsoDate,
          title: `${formatDateLabel(isoDate)} · ${hasActivity ? `${formatCount(total)} interacciones` : "Sin actividad"}`,
        });
      }

      months.push({
        month: monthNumber,
        name: MONTH_LABELS[monthIndex],
        activeDays,
        totalDays: daysInMonth,
        padding: Array.from({ length: firstWeekday }, (_, idx) => `pad-${monthNumber}-${idx}`),
        days,
      });
    }

    return months;
  };

  $: selectedDay =
    (Array.isArray(calendarItems)
      ? calendarItems.find((item) => toIsoDateUtc(item?.date_utc) === selectedDateUtc)
      : null) || null;

  $: selectedDateLabel = selectedDateUtc ? formatDateLabel(selectedDateUtc) : "";

  $: dailyMetrics = DAILY_METRIC_DEFINITIONS.map((metric) => {
    const value = Number(selectedDay?.[metric.key] || 0);
    return {
      ...metric,
      value,
      valueLabel: formatCount(value),
    };
  });

  $: yearMonths = buildYearMonths({
    year: calendarYear,
    items: calendarItems,
    selectedIsoDate: selectedDateUtc,
    todayIsoDate: toIsoDateUtc(todayUtc),
  });

  onMount(() => {
    initPurposeCoverModule();
    void syncProfileStarsTotal("calendarStarsTotal");

    (async () => {
      try {
        await resolveProfileContext();
      } catch (error) {
        console.error(error);
        calendarLoadError = error?.message || "No se pudo resolver el perfil.";
      }
      await loadCalendarYearActivity();
    })();
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{pageTitle}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user calendar-background">
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
      <a class="topbar-btn" href="/home_user.html" data-profile-module="home">🏠 Home</a>
      <a class="topbar-btn" href="/gallery.html">🖼️ Galería</a>
      <a class="topbar-btn" href="/my-public-whishes.html" data-profile-module="public_wishes">🌐 Deseos públicos</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 Deseos privados</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html" data-profile-module="fulfilled_wishes">✅ Deseos cumplidos</a>
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown">
        <summary class="topbar-avatar-btn" aria-label="Perfil del usuario">
          <img src="/assets/avatar-default.jpg" alt="Perfil" />
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
          <a href="/home_user.html" role="menuitem" data-my-home>Mi Home</a>
          <a href="/achievements.html" role="menuitem">Logros recientes</a>
          <a href="/gallery.html" role="menuitem">Galería</a>
          <a href="/calendar.html" role="menuitem" data-profile-module="calendar">Calendario</a>
          <a href="/my-biography.html" role="menuitem">Mi Biografía</a>
          <a href="/messages.html" role="menuitem">Mensajes</a>
        </div>
      </details>
    </div>
  </header>

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
          <button class="purpose-pill purpose-top" type="button" id="purpose1">Deseo #1: Secreto</button>
          <button class="purpose-pill purpose-left" type="button" id="purpose2">Deseo construir el Reino de Combray</button>
          <button class="purpose-pill purpose-right" type="button" id="purpose3">Deseo estar unido a Jesús</button>
        </div>

        <div class="cover-hint" id="coverHint">Arrastra la portada para encuadrarla</div>
      </div>
    </section>

    <div class="calendar-body">
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home" data-profile-module="home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
          <span class="nav-icon">⭐</span>
          <span><strong id="calendarStarsTotal">0</strong> estrellas</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario" data-profile-module="calendar">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
        <a class="nav-pill" href="/messages.html" title="Mensajes">Mensajes</a>
      </nav>

      {#if calendarAllowed}
        <section class="calendar-shell" aria-label="Calendario anual">
          <div class="calendar-head">
            <h2 class="calendar-title">{calendarTitle}</h2>
            <div class="calendar-head-actions">
              <button class="btn btn-outline btn-compact" type="button" on:click={() => void changeYear(-1)}>Año anterior</button>
              <span class="calendar-year-chip">{calendarYear}</span>
              <button class="btn btn-outline btn-compact" type="button" on:click={() => void changeYear(1)}>Año siguiente</button>
            </div>
          </div>

          <div class="calendar-legend">
            <span><strong>Día activo</strong> en verde</span>
            <span><strong>Sin actividad</strong> en blanco</span>
            <span><strong>{formatCount(activeDaysTotal)}</strong> días activos en {calendarYear}</span>
          </div>

          {#if calendarLoading}
            <article class="calendar-current" aria-label="Carga de calendario">
              <p class="panel-muted">Cargando actividad del calendario...</p>
            </article>
          {:else if calendarLoadError}
            <article class="calendar-current" aria-label="Error de calendario">
              <p class="achievements-sync-error">{calendarLoadError}</p>
            </article>
          {:else}
            <article class="calendar-current" aria-label="Interacciones diarias">
              <div class="current-head">
                <h3 class="current-month">Interacciones del día</h3>
                <div class="calendar-legend">
                  <span>{selectedDateLabel || "Sin fecha seleccionada"}</span>
                </div>
              </div>

              <div class="calendar-daily-grid">
                {#each dailyMetrics as metric}
                  <article class="calendar-daily-card" aria-label={`${metric.label}: ${metric.valueLabel}`}>
                    <div class="calendar-daily-icon" aria-hidden="true">{metric.icon}</div>
                    <div class="calendar-daily-content">
                      <h4>{metric.label}</h4>
                      <p>{metric.valueLabel}</p>
                    </div>
                  </article>
                {/each}
              </div>

              <p class="calendar-day-total">
                Interacciones totales del día:
                <strong>{formatCount(selectedDay?.total_interactions || 0)}</strong>
              </p>

              {#if !selectedDay?.has_activity}
                <p class="panel-muted">No hay actividad registrada para este día.</p>
              {/if}
            </article>

            <article class="calendar-year" aria-label={`Vista anual ${calendarYear}`}>
              <h3 class="year-label">{calendarYear} · Enero a Diciembre</h3>
              <p class="calendar-year-note">Pulsa un día para actualizar el resumen diario.</p>
              <div class="month-grid">
                {#each yearMonths as month}
                  <article class="month-card" aria-label={`Mes ${month.name}`}>
                    <div class="month-name">
                      {month.name}
                      <span class="month-status">{month.activeDays} / {month.totalDays}</span>
                    </div>
                    <div class="month-dots">
                      {#each month.padding as padKey}
                        <span class="month-dot is-pad" aria-hidden="true" data-key={padKey}></span>
                      {/each}

                      {#each month.days as day}
                        <button
                          class={`month-dot-btn ${day.hasActivity ? "is-active" : "is-idle"}${day.isToday ? " is-today" : ""}${day.isSelected ? " is-selected" : ""}`}
                          type="button"
                          title={day.title}
                          aria-label={day.title}
                          on:click={() => setSelectedDate(day.date_utc)}
                        ></button>
                      {/each}
                    </div>
                  </article>
                {/each}
              </div>
            </article>
          {/if}
        </section>
      {:else}
        <section class="panel calendar-shell" aria-label="Calendario privado">
          <div class="panel-head">
            <h2 class="panel-title">Calendario privado</h2>
            <span class="panel-badge">🔒</span>
          </div>
          <p class="panel-muted">{calendarAccessError || "Este calendario es privado."}</p>
        </section>
      {/if}
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
