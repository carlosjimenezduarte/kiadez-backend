<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";

  const API = "http://127.0.0.1:8000";
  const MIN_YEAR = 2000;
  const MAX_YEAR = 2100;
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

  const MONTH_LABELS = [
    tr("Enero", "January", "Janvier"),
    tr("Febrero", "February", "Février"),
    tr("Marzo", "March", "Mars"),
    tr("Abril", "April", "Avril"),
    tr("Mayo", "May", "Mai"),
    tr("Junio", "June", "Juin"),
    tr("Julio", "July", "Juillet"),
    tr("Agosto", "August", "Août"),
    tr("Septiembre", "September", "Septembre"),
    tr("Octubre", "October", "Octobre"),
    tr("Noviembre", "November", "Novembre"),
    tr("Diciembre", "December", "Décembre"),
  ];

  const DAILY_METRIC_DEFINITIONS = [
    { key: "stars_received", icon: "⭐", label: tr("Estrellas", "Stars", "Étoiles") },
    { key: "fulfilled_wishes", icon: "✅", label: tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis") },
    { key: "public_wishes", icon: "🌟", label: tr("Deseos públicos", "Public wishes", "Souhaits publics") },
    { key: "achievements", icon: "🏆", label: tr("Logros", "Achievements", "Réalisations") },
    { key: "posts", icon: "📝", label: tr("Publicaciones", "Posts", "Publications") },
  ];

  let isViewingOwnProfile = true;
  let viewerUserId = null;
  let viewerUsername = "";
  let activeProfileUserId = null;
  let activeProfileUsername = "";
  let activeProfileFullName = "";

  let pageTitle = tr("Kiadez — Calendario", "Kiadez — Calendar", "Kiadez — Calendrier");
  let calendarTitle = tr("Calendario", "Calendar", "Calendrier");
  let calendarYear = new Date().getUTCFullYear();

  let calendarAllowed = true;
  let calendarAccessError = "";
  let calendarLoading = false;
  let calendarLoadError = "";

  let calendarItems = [];
  let activeDaysTotal = 0;
  let todayUtc = "";
  let selectedDateUtc = "";
  let daySummaryOpen = false;
  let daySummaryDateUtc = "";
  let daySummaryLoading = false;
  let daySummaryError = "";
  let daySummaryData = null;

  const DAY_SUMMARY_EMPTY_TOTALS = {
    stars_received: 0,
    fulfilled_wishes: 0,
    public_wishes: 0,
    achievements: 0,
    posts: 0,
    total_interactions: 0,
  };
  const daySummaryCache = new Map();

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
      throw new Error(tr("No hay sesión activa.", "No active session.", "Aucune session active."));
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    };
    const res = await fetch(`${API}${path}`, { ...options, headers });
    if (res.status === 401) {
      throw new Error(tr("Sesión expirada. Inicia sesión nuevamente.", "Session expired. Sign in again.", "Session expirée. Connecte-toi à nouveau."));
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
    return safe.toLocaleString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO");
  };

  const formatDateLabel = (isoDate) => {
    const normalized = toIsoDateUtc(isoDate);
    if (!normalized) return "";
    try {
      const dt = new Date(`${normalized}T00:00:00Z`);
      return new Intl.DateTimeFormat(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
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

  const formatTimeLabel = (value) => {
    if (!value) return "";
    const dt = new Date(value);
    if (Number.isNaN(dt.getTime())) return "";
    return new Intl.DateTimeFormat(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
      hour: "2-digit",
      minute: "2-digit",
      timeZone: "UTC",
    }).format(dt);
  };

  const addDaysIsoUtc = (isoDate, daysToAdd) => {
    const normalized = toIsoDateUtc(isoDate);
    if (!normalized) return "";
    const base = new Date(`${normalized}T00:00:00Z`);
    if (Number.isNaN(base.getTime())) return "";
    base.setUTCDate(base.getUTCDate() + Number(daysToAdd || 0));
    return base.toISOString().slice(0, 10);
  };

  const currentTodayIsoUtc = () => toIsoDateUtc(todayUtc) || new Date().toISOString().slice(0, 10);

  const isClosedCalendarDay = (isoDate) => {
    const normalized = toIsoDateUtc(isoDate);
    if (!normalized) return false;
    const todayIso = currentTodayIsoUtc();
    return normalized < todayIso;
  };

  const buildPendingDaySummary = (isoDate, message) => ({
    user_id: Number(activeProfileUserId || 0),
    date_utc: isoDate,
    available_from_utc: addDaysIsoUtc(isoDate, 1) || isoDate,
    is_day_closed: false,
    message: String(message || ""),
    totals: { ...DAY_SUMMARY_EMPTY_TOTALS },
    posts_items: [],
    fulfilled_wishes_items: [],
    achievements_items: [],
  });

  const fetchViewerIdentity = async () => {
    const res = await apiFetch("/auth/me");
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(data.detail || tr("No se pudo cargar tu perfil.", "Could not load your profile.", "Impossible de charger ton profil."));
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
      if (!res.ok) throw new Error(data.detail || tr("No se pudo cargar el perfil.", "Could not load profile.", "Impossible de charger le profil."));
      return data;
    }
    if (usernameValue) {
      const res = await apiFetch(`/follows/profile?username=${encodeURIComponent(usernameValue)}`);
      const data = await parseResponseJson(res);
      if (!res.ok) throw new Error(data.detail || tr("No se pudo cargar el perfil.", "Could not load profile.", "Impossible de charger le profil."));
      return data;
    }
    throw new Error(tr("Parámetros inválidos para cargar perfil.", "Invalid parameters to load profile.", "Paramètres invalides pour charger le profil."));
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
      ? tr("Kiadez — Calendario", "Kiadez — Calendar", "Kiadez — Calendrier")
      : isEn
        ? `Kiadez — ${activeProfileFullName || "user"}'s Calendar`
        : `Kiadez — Calendario de ${activeProfileFullName || "usuario"}`;
    calendarTitle = isViewingOwnProfile
      ? tr(`Calendario ${calendarYear}`, `Calendar ${calendarYear}`, `Calendar ${calendarYear}`)
      : isEn
        ? `${activeProfileFullName || "user"}'s Calendar · ${calendarYear}`
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
      const detail = data?.detail || tr("No se pudo cargar el calendario.", "Could not load calendar.", "Impossible de charger le calendrier.");
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
        calendarAccessError = error?.message || tr("Este calendario es privado.", "This calendar is private.", "Ce calendrier est privé.");
        calendarItems = [];
        activeDaysTotal = 0;
        selectedDateUtc = "";
      } else {
        calendarLoadError = error?.message || tr("No se pudo cargar el calendario.", "Could not load calendar.", "Impossible de charger le calendrier.");
      }
    } finally {
      calendarLoading = false;
    }
  };

  const setSelectedDate = (isoDate) => {
    selectedDateUtc = toIsoDateUtc(isoDate);
  };

  const closeDaySummaryModal = () => {
    daySummaryOpen = false;
    daySummaryLoading = false;
    daySummaryError = "";
  };

  const openDaySummaryModal = async (isoDate) => {
    const normalized = toIsoDateUtc(isoDate);
    if (!normalized) return;

    setSelectedDate(normalized);
    daySummaryDateUtc = normalized;
    daySummaryError = "";
    daySummaryLoading = false;
    daySummaryData = null;
    daySummaryOpen = true;

    if (!isViewingOwnProfile) {
      daySummaryData = buildPendingDaySummary(
        normalized,
        tr(
          "Este resumen detallado está disponible solo en tu propio calendario.",
          "This detailed summary is available only in your own calendar."
        )
      );
      return;
    }

    if (!isClosedCalendarDay(normalized)) {
      const dayLabel = formatDateLabel(normalized) || normalized;
      const availableIso = addDaysIsoUtc(normalized, 1) || normalized;
      const availableLabel = formatDateLabel(availableIso) || availableIso;
      daySummaryData = buildPendingDaySummary(
        normalized,
        isEn
          ? `Summary for ${dayLabel} becomes available when that day ends. Available from ${availableLabel}.`
          : `El resumen de ${dayLabel} se habilita cuando ese día finaliza. Disponible desde ${availableLabel}.`
      );
      return;
    }

    const cached = daySummaryCache.get(normalized);
    if (cached) {
      daySummaryData = cached;
      return;
    }

    daySummaryLoading = true;
    try {
      const res = await apiFetch(`/calendar/mine/day-summary?date_utc=${encodeURIComponent(normalized)}`);
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data?.detail || tr("No se pudo cargar el resumen del día.", "Could not load day summary.", "Impossible de charger le résumé du jour."));
      }
      daySummaryData = data && typeof data === "object" ? data : null;
      if (daySummaryData) {
        daySummaryCache.set(normalized, daySummaryData);
      }
    } catch (error) {
      daySummaryError = error?.message || tr("No se pudo cargar el resumen del día.", "Could not load day summary.", "Impossible de charger le résumé du jour.");
    } finally {
      daySummaryLoading = false;
    }
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
          title: `${formatDateLabel(isoDate)} · ${
            hasActivity ? tr(`${formatCount(total)} interacciones`, `${formatCount(total)} interactions`, `${formatCount(total)} interactions`) : tr("Sin actividad", "No activity", "Aucune activité")
          }`,
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

  $: daySummaryDateLabel = daySummaryDateUtc ? formatDateLabel(daySummaryDateUtc) : "";
  $: daySummaryTotals = daySummaryData?.totals || DAY_SUMMARY_EMPTY_TOTALS;
  $: daySummaryPosts = Array.isArray(daySummaryData?.posts_items) ? daySummaryData.posts_items : [];
  $: daySummaryFulfilledWishes = Array.isArray(daySummaryData?.fulfilled_wishes_items)
    ? daySummaryData.fulfilled_wishes_items
    : [];
  $: daySummaryAchievements = Array.isArray(daySummaryData?.achievements_items)
    ? daySummaryData.achievements_items
    : [];
  $: daySummaryMetrics = DAILY_METRIC_DEFINITIONS.map((metric) => {
    const value = Number(daySummaryTotals?.[metric.key] || 0);
    return {
      ...metric,
      value,
      valueLabel: formatCount(value),
    };
  });
  $: daySummaryMessage = String(daySummaryData?.message || "");
  $: daySummaryIsClosed = Boolean(daySummaryData?.is_day_closed);

  onMount(() => {
    initPurposeCoverModule();
    void syncProfileStarsTotal("calendarStarsTotal");

    (async () => {
      try {
        await resolveProfileContext();
      } catch (error) {
        console.error(error);
        calendarLoadError = error?.message || tr("No se pudo resolver el perfil.", "Could not resolve profile.", "Impossible de resolve profile.");
      }
      await loadCalendarYearActivity();
    })();

    const onKeyDown = (event) => {
      if (event.key === "Escape" && daySummaryOpen) {
        closeDaySummaryModal();
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
    };
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
        <input type="search" placeholder={tr("Buscar en Kiadez", "Search on Kiadez", "Rechercher sur Kiadez")} aria-label={tr("Buscar", "Search", "Rechercher")} />
      </form>
    </div>

    <div class="feed-topbar-zone feed-topbar-center">
      <a class="topbar-btn" href="/home_user.html" data-profile-module="home">🏠 Home</a>
      <a class="topbar-btn" href="/gallery.html">🖼️ {tr("Galería", "Gallery", "Galerie")}</a>
      <a class="topbar-btn" href="/my-public-whishes.html" data-profile-module="public_wishes">🌐 {tr("Deseos públicos", "Public wishes", "Souhaits publics")}</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 {tr("Deseos privados", "Private wishes", "Souhaits privés")}</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html" data-profile-module="fulfilled_wishes">✅ {tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</a>
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown">
        <summary class="topbar-avatar-btn" aria-label={tr("Perfil del usuario", "User profile", "Profil utilisateur")}>
          <img src="/assets/avatar-default.jpg" alt={tr("Foto de perfil del usuario", "User profile photo", "Photo de profil de l'utilisateur")} />
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/privacy-and-settings.html" role="menuitem">{tr("Configuración y privacidad", "Settings and privacy", "Paramètres et confidentialité")}</a>
          <button type="button" role="menuitem" on:click={logout}>{tr("Cerrar sesión", "Sign out", "Se déconnecter")}</button>
        </div>
      </details>

      <button class="topbar-icon" type="button" aria-label={tr("Notificaciones", "Notifications", "Alertes")}>
        🔔
        <span class="topbar-badge">3</span>
      </button>

      <details class="topbar-dropdown">
        <summary class="topbar-menu-btn" aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}>
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">{tr("Menú", "Menu", "Navigation")}</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem" data-my-home>{tr("Mi Home", "My Home", "Mon accueil")}</a>
          <a href="/achievements.html" role="menuitem">{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
          <a href="/gallery.html" role="menuitem">{tr("Galería", "Gallery", "Galerie")}</a>
          <a href="/calendar.html" role="menuitem" data-profile-module="calendar">{tr("Calendario", "Calendar", "Calendrier")}</a>
          <a href="/my-biography.html" role="menuitem">{tr("Mi Biografía", "My Biography", "Ma biographie")}</a>
          <a href="/messages.html" role="menuitem">{tr("Mensajes", "Messages", "Messagerie")}</a>
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt={tr("Portada", "Cover", "Couverture")} />

        <div class="cover-actions">
          <button class="icon-btn" id="btnChangeCover" type="button" title={tr("Cambiar portada", "Change cover", "Changer la couverture")}>
            {tr("Cambiar portada", "Change cover", "Changer la couverture")}
          </button>
          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button" title={tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier ma mission de vie")}>
            {tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier ma mission de vie")}
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="purpose-triangle" aria-label={tr("Deseos de propósito", "Purpose wishes", "Souhaits de mission")}>
          <button class="purpose-pill purpose-top" type="button" id="purpose1">{tr("Deseo #1: Secreto", "Wish #1: Secret", "Souhait n°1 : Secret")}</button>
          <button class="purpose-pill purpose-left" type="button" id="purpose2">{tr("Deseo construir el Reino de Combray", "I wish to build the Kingdom of Combray", "Je souhaite construire le Royaume de Combray")}</button>
          <button class="purpose-pill purpose-right" type="button" id="purpose3">{tr("Deseo estar unido a Jesús", "I wish to be united with Jesus", "Je souhaite être uni à Jésus")}</button>
        </div>

        <div class="cover-hint" id="coverHint">{tr("Arrastra la portada para encuadrarla", "Drag the cover to frame it", "Déplace la couverture pour l'ajuster")}</div>
      </div>
    </section>

    <div class="calendar-body">
      <nav class="profile-nav" aria-label={tr("Navegación de perfil", "Profile navigation", "Navigation du profil")}>
        <a class="nav-pill" href="/home_user.html" title={tr("Home", "Home", "Accueil")} data-profile-module="home">{tr("Home", "Home", "Accueil")}</a>
        <a class="nav-pill" href="/star-pool-found.html" title={tr("Estrellas", "Stars", "Étoiles")}>
          <span class="nav-icon">⭐</span>
          <span><strong id="calendarStarsTotal">0</strong> {tr("estrellas", "stars", "étoiles")}</span>
        </a>

        <a class="nav-pill" href="/followers.html" title={tr("Seguidores", "Followers", "Abonnés")}>{tr("Seguidores", "Followers", "Abonnés")}</a>
        <a class="nav-pill" href="/achievements.html" title={tr("Logros recientes", "Recent achievements", "Réalisations récentes")}>{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
        <a class="nav-pill" href="/gallery.html" title={tr("Galería", "Gallery", "Galerie")}>{tr("Galería", "Gallery", "Galerie")}</a>
        <a class="nav-pill" href="/calendar.html" title={tr("Calendario", "Calendar", "Calendrier")} data-profile-module="calendar">{tr("Calendario", "Calendar", "Calendrier")}</a>
        <a class="nav-pill" href="/my-biography.html" title={tr("Mi biografía", "My biography", "Ma biographie")}>{tr("Mi biografía", "My biography", "Ma biographie")}</a>
        <a class="nav-pill" href="/messages.html" title={tr("Mensajes", "Messages", "Messagerie")}>{tr("Mensajes", "Messages", "Messagerie")}</a>
      </nav>

      {#if calendarAllowed}
        <section class="calendar-shell" aria-label={tr("Calendario anual", "Yearly calendar", "Calendrier annuel")}>
          <div class="calendar-head">
            <h2 class="calendar-title">{calendarTitle}</h2>
            <div class="calendar-head-actions">
              <button class="btn btn-outline btn-compact" type="button" on:click={() => void changeYear(-1)}>{tr("Año anterior", "Previous year", "Année précédente")}</button>
              <span class="calendar-year-chip">{calendarYear}</span>
              <button class="btn btn-outline btn-compact" type="button" on:click={() => void changeYear(1)}>{tr("Año siguiente", "Next year", "Année suivante")}</button>
            </div>
          </div>

          <div class="calendar-legend">
            <span><strong>{tr("Día activo", "Active day", "Jour actif")}</strong> {tr("en verde", "in green", "en vert")}</span>
            <span><strong>{tr("Sin actividad", "No activity", "Aucune activité")}</strong> {tr("en blanco", "in white", "en blanc")}</span>
            <span><strong>{formatCount(activeDaysTotal)}</strong> {tr("días activos en", "active days in", "jours actifs en")} {calendarYear}</span>
          </div>

          {#if calendarLoading}
            <article class="calendar-current" aria-label={tr("Carga de calendario", "Calendar loading", "Chargement du calendrier")}>
              <p class="panel-muted">{tr("Cargando actividad del calendario...", "Loading calendar activity...", "Chargement de l'activité du calendrier...")}</p>
            </article>
          {:else if calendarLoadError}
            <article class="calendar-current" aria-label={tr("Error de calendario", "Calendar error", "Erreur du calendrier")}>
              <p class="achievements-sync-error">{calendarLoadError}</p>
            </article>
          {:else}
            <article class="calendar-current" aria-label={tr("Interacciones diarias", "Daily interactions", "Interactions quotidiennes")}>
              <div class="current-head">
                <h3 class="current-month">{tr("Interacciones del día", "Day interactions", "Interactions du jour")}</h3>
                <div class="calendar-legend">
                  <span>{selectedDateLabel || tr("Sin fecha seleccionada", "No selected date", "Aucune date sélectionnée")}</span>
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
                {tr("Interacciones totales del día:", "Total interactions for the day:", "Interactions totales du jour :")}
                <strong>{formatCount(selectedDay?.total_interactions || 0)}</strong>
              </p>

              {#if !selectedDay?.has_activity}
                <p class="panel-muted">{tr("No hay actividad registrada para este día.", "There is no recorded activity for this day.", "Aucune activité enregistrée pour ce jour.")}</p>
              {/if}
            </article>

            <article class="calendar-year" aria-label={`Vista anual ${calendarYear}`}>
              <h3 class="year-label">{calendarYear} · {tr("Enero a Diciembre", "January to December", "Janvier à décembre")}</h3>
              <p class="calendar-year-note">{tr("Pulsa un día para abrir el resumen diario (disponible al día siguiente).", "Tap a day to open daily summary (available the next day).", "Appuie sur un jour pour ouvrir le résumé quotidien (disponible le lendemain).")}</p>
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
                          on:click={() => void openDaySummaryModal(day.date_utc)}
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
        <section class="panel calendar-shell" aria-label={tr("Calendario privado", "Private calendar", "Calendrier privé")}>
          <div class="panel-head">
            <h2 class="panel-title">{tr("Calendario privado", "Private calendar", "Calendrier privé")}</h2>
            <span class="panel-badge">🔒</span>
          </div>
          <p class="panel-muted">{calendarAccessError || tr("Este calendario es privado.", "This calendar is private.", "Ce calendrier est privé.")}</p>
        </section>
      {/if}
    </div>
  </main>

  <div
    class={`modal-overlay calendar-day-summary-overlay ${daySummaryOpen ? "" : "hidden"}`}
    aria-hidden={daySummaryOpen ? "false" : "true"}
    on:click={(event) => {
      if (event.target === event.currentTarget) closeDaySummaryModal();
    }}
  >
    <div
      class="modal wish-modal calendar-day-summary-modal"
      role="dialog"
      aria-modal="true"
      aria-label={tr("Resumen diario del calendario", "Calendar daily summary", "Résumé quotidien du calendrier")}
      tabindex="-1"
    >
      <div class="modal-head">
        <h3>{tr("Resumen diario", "Daily summary", "Résumé quotidien")}</h3>
        <button class="modal-close" type="button" on:click={() => closeDaySummaryModal()}>✕</button>
      </div>

      <div class="modal-body">
        <div class="calendar-summary-meta">
          <span class="calendar-summary-chip">{daySummaryDateLabel || tr("Sin fecha seleccionada", "No selected date", "Aucune date sélectionnée")}</span>
          <span class="calendar-summary-chip">
            {tr("Disponible desde:", "Available from:", "Disponible à partir de :")} {formatDateLabel(daySummaryData?.available_from_utc || addDaysIsoUtc(daySummaryDateUtc, 1))}
          </span>
        </div>

        {#if daySummaryLoading}
          <p class="panel-muted">{tr("Cargando resumen del día...", "Loading day summary...", "Chargement du résumé du jour...")}</p>
        {:else if daySummaryError}
          <p class="achievements-sync-error">{daySummaryError}</p>
        {:else if !daySummaryData}
          <p class="panel-muted">{tr("Selecciona un día para ver su resumen.", "Select a day to view its summary.", "Sélectionne un jour pour voir son résumé.")}</p>
        {:else if !daySummaryIsClosed}
          <p class="calendar-summary-pending">{daySummaryMessage || tr("Este resumen estará disponible cuando el día finalice.", "This summary will be available when the day ends.", "Ce résumé sera disponible à la fin de la journée.")}</p>
        {:else}
          <div class="calendar-daily-grid calendar-summary-daily-grid">
            {#each daySummaryMetrics as metric}
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
            {tr("Interacciones totales:", "Total interactions:", "Interactions totales :")}
            <strong>{formatCount(daySummaryTotals?.total_interactions || 0)}</strong>
          </p>

          <section class="calendar-summary-section" aria-label={tr("Publicaciones del día", "Posts of the day", "Publications du jour")}>
            <div class="calendar-summary-section-head">
              <h4>{tr("Publicaciones del día", "Posts of the day", "Publications du jour")}</h4>
              <span>{formatCount(daySummaryPosts.length)}</span>
            </div>
            {#if !daySummaryPosts.length}
              <p class="panel-muted">{tr("No se registraron publicaciones para este día.", "No posts were recorded for this day.", "Aucune publication n'a été enregistrée pour ce jour.")}</p>
            {:else}
              <div class="calendar-summary-posts">
                {#each daySummaryPosts as post}
                  <article class="calendar-summary-post-card" aria-label={`${tr("Publicación", "Post", "Publication")} ${post.id}`}>
                    {#if post.media_url}
                      {#if post.media_kind === "video"}
                        <video class="calendar-summary-media" src={post.media_url} controls preload="metadata">
                          <track kind="captions" />
                        </video>
                      {:else}
                        <img class="calendar-summary-media" src={post.media_url} alt={tr("Publicación del día", "Post of the day", "Publication du jour")} />
                      {/if}
                    {:else}
                      <div class="calendar-summary-media calendar-summary-media-placeholder">{tr("Sin archivo visual", "No visual file", "Aucun fichier visuel")}</div>
                    {/if}
                    <div class="calendar-summary-post-content">
                      <p class="calendar-summary-post-text">{post.text || tr("Publicación sin texto.", "Post without text.", "Publication sans texte.")}</p>
                      <p class="calendar-summary-post-meta">
                        {formatTimeLabel(post.created_at)} UTC · ⭐ {formatCount(post.star_count || 0)} ·
                        💬 {formatCount(post.comment_count || 0)} · 🔁 {formatCount(post.share_count || 0)}
                      </p>
                    </div>
                  </article>
                {/each}
              </div>
            {/if}
          </section>

          <section class="calendar-summary-section" aria-label={tr("Deseos cumplidos del día", "Fulfilled wishes of the day", "Souhaits accomplis du jour")}>
            <div class="calendar-summary-section-head">
              <h4>{tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</h4>
              <span>{formatCount(daySummaryFulfilledWishes.length)}</span>
            </div>
            {#if !daySummaryFulfilledWishes.length}
              <p class="panel-muted">{tr("No se registraron deseos cumplidos para este día.", "No fulfilled wishes were recorded for this day.", "Aucun souhait accompli n'a été enregistré pour ce jour.")}</p>
            {:else}
              <div class="calendar-summary-list">
                {#each daySummaryFulfilledWishes as wish}
                  <article class="calendar-summary-list-item">
                    <p class="calendar-summary-list-title">{wish.wish_text}</p>
                    <p class="calendar-summary-list-meta">
                      {wish.wish_type || tr("Deseo", "Wish", "Souhait")} · {formatTimeLabel(wish.fulfilled_at)} UTC
                    </p>
                  </article>
                {/each}
              </div>
            {/if}
          </section>

          <section class="calendar-summary-section" aria-label={tr("Logros del día", "Achievements of the day", "Réalisations du jour")}>
            <div class="calendar-summary-section-head">
              <h4>{tr("Logros", "Achievements", "Réalisations")}</h4>
              <span>{formatCount(daySummaryAchievements.length)}</span>
            </div>
            {#if !daySummaryAchievements.length}
              <p class="panel-muted">{tr("No hubo logros desbloqueados este día.", "There were no achievements unlocked this day.", "Aucune réalisation n'a été débloquée ce jour-là.")}</p>
            {:else}
              <div class="calendar-summary-list">
                {#each daySummaryAchievements as achievement}
                  <article class="calendar-summary-list-item calendar-summary-achievement-item">
                    {#if achievement.image_url}
                      <img class="calendar-summary-achievement-img" src={achievement.image_url} alt={achievement.title} />
                    {/if}
                    <div class="calendar-summary-achievement-content">
                      <p class="calendar-summary-list-title">{achievement.title}</p>
                      <p class="calendar-summary-list-meta">{achievement.description}</p>
                    </div>
                  </article>
                {/each}
              </div>
            {/if}
          </section>
        {/if}
      </div>

      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" on:click={() => closeDaySummaryModal()}>
          {tr("Cerrar", "Close", "Fermer")}
        </button>
      </div>
    </div>
  </div>
  <AuthFooter />
</div>
