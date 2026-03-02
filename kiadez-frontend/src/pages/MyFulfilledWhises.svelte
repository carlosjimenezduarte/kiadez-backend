<script>
  import { onMount } from "svelte";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";
  import { logout } from "../lib/logout";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";

  const API = "http://127.0.0.1:8000";
  const FULFILLED_VISIBLE_SLOTS = 10;
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);
  const PLACEHOLDER_FULFILLED_MESSAGE = tr(
    "Aqui se publicara tu deseo cuando lo marques como cumplido.",
    "Your wish will appear here when you mark it as fulfilled."
  );

  let isViewingOwnProfile = true;
  let viewerUserId = null;
  let viewerUsername = "";
  let activeProfileUserId = null;
  let activeProfileUsername = "";
  let activeProfileFullName = "";

  let pageTitle = tr("Kiadez — Mis deseos cumplidos", "Kiadez — My fulfilled wishes", "Kiadez — Mes souhaits accomplis");
  let headerTitle = tr("Mis deseos cumplidos", "My fulfilled wishes", "Mes souhaits accomplis");
  let headerSubtitle = tr(
    "Este espacio mostrara los deseos que marques como cumplidos.",
    "This space will display the wishes you mark as fulfilled."
  );

  const personalTypeIconMap = {
    "Espiritual": "/css/icons/Espiritual.webp",
    "Material": "/css/icons/Material.webp",
    "Monetario": "/css/icons/Monetario.webp",
    "Profesional": "/css/icons/Profesional.webp",
    "Salud y cuerpo": "/css/icons/Salud.webp",
    "Relacional": "/css/icons/Relacional.webp",
    "Vivencial": "/css/icons/Vivencial.webp"
  };

  let personalCompletedSlots = Array.from({ length: FULFILLED_VISIBLE_SLOTS }, (_, index) => index + 1);
  let cooperativeCompletedSlots = Array.from({ length: FULFILLED_VISIBLE_SLOTS }, (_, index) => index + 1);

  let personalFulfilledItems = [];
  let personalCompletedView = personalCompletedSlots.map((slot) => ({ slot, wish: null }));
  let personalFulfilledTotal = 0;
  let personalFulfilledError = "";
  let personalFulfilledLoading = false;
  let personalFulfilledPage = 1;
  let personalFulfilledTotalPages = 1;
  let personalFulfilledPageNumbers = [1];
  let personalFulfilledRangeStart = 0;
  let personalFulfilledRangeEnd = 0;

  let cooperativeFulfilledItems = [];
  let cooperativeCompletedView = cooperativeCompletedSlots.map((slot) => ({ slot, wish: null }));
  let cooperativeFulfilledTotal = 0;
  let cooperativeFulfilledError = "";
  let cooperativeFulfilledLoading = false;
  let cooperativeFulfilledPage = 1;
  let cooperativeFulfilledTotalPages = 1;
  let cooperativeFulfilledPageNumbers = [1];
  let cooperativeFulfilledRangeStart = 0;
  let cooperativeFulfilledRangeEnd = 0;

  let personalFulfilledRequestId = 0;
  let cooperativeFulfilledRequestId = 0;

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
      throw new Error(tr("No hay sesion activa.", "No active session.", "Aucune session active."));
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`
    };
    const res = await fetch(`${API}${path}`, { ...options, headers });
    if (res.status === 401) {
      throw new Error(tr("Sesion expirada. Inicia sesion nuevamente.", "Session expired. Sign in again.", "Session expirée. Connecte-toi à nouveau."));
    }
    return res;
  };

  const normalizeUsername = (value) => {
    let normalized = String(value || "").trim().toLowerCase();
    while (normalized.startsWith("@")) normalized = normalized.slice(1);
    return normalized;
  };

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
    throw new Error(tr("Parametros invalidos para cargar perfil.", "Invalid parameters to load profile.", "Paramètres invalides pour charger le profil."));
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
    document.querySelectorAll(".purpose-side-btn").forEach((btn) => btn.classList.add("hidden"));
  };

  const applyProfileHeader = () => {
    headerTitle = isViewingOwnProfile
      ? tr("Mis deseos cumplidos", "My fulfilled wishes", "Mes souhaits accomplis")
      : tr(
        `Deseos cumplidos de ${activeProfileFullName || "usuario"}`,
        `Fulfilled wishes of ${activeProfileFullName || "user"}`
      );
    headerSubtitle = isViewingOwnProfile
      ? tr(
        "Este espacio mostrara los deseos que marques como cumplidos.",
        "This space will display the wishes you mark as fulfilled."
      )
      : tr(
        "Este espacio muestra los deseos que esta persona marco como cumplidos.",
        "This space shows the wishes this person marked as fulfilled."
      );
    pageTitle = isViewingOwnProfile
      ? tr("Kiadez — Mis deseos cumplidos", "Kiadez — My fulfilled wishes", "Kiadez — Mes souhaits accomplis")
      : tr(
        `Kiadez — Deseos cumplidos de ${activeProfileFullName || "usuario"}`,
        `Kiadez — Fulfilled wishes of ${activeProfileFullName || "user"}`
      );
  };

  const resolveProfileContext = async () => {
    const params = new URLSearchParams(window.location.search);
    const requestedIdRaw = params.get("id");
    const requestedId = Number(requestedIdRaw);
    const requestedUserId =
      Number.isFinite(requestedId) && requestedId > 0 ? requestedId : null;
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
        activeProfileUserId = Number(profile?.user_id) || requestedUserId;
        activeProfileUsername = normalizeUsername(profile?.username || requestedUsername);
        activeProfileFullName = String(profile?.full_name || "").trim();
        isViewingOwnProfile = Boolean(viewerUserId && activeProfileUserId === viewerUserId);
        if (!isViewingOwnProfile) {
          applyReadOnlyProfileMode();
        }
      }
    }

    applyProfileHeader();
    setMyHomeLinks(buildViewerHomeUrl());
    syncProfileModuleLinks();
  };

  const fetchFulfilledPersonalWishes = async (limit = FULFILLED_VISIBLE_SLOTS, offset = 0) => {
    const profileId = Number(activeProfileUserId);
    const endpoint =
      !isViewingOwnProfile && Number.isFinite(profileId) && profileId > 0
        ? `/public-wishes/user/${encodeURIComponent(String(profileId))}/personal/fulfilled?limit=${limit}&offset=${offset}`
        : `/public-wishes/personal/fulfilled?limit=${limit}&offset=${offset}`;
    const res = await apiFetch(endpoint);
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(
        data.detail || tr("No se pudieron cargar los deseos personales cumplidos.", "Could not load fulfilled personal wishes.", "Impossible de load fulfilled personal wishes.")
      );
    }
    return data;
  };

  const fetchFulfilledCooperativeWishes = async (limit = FULFILLED_VISIBLE_SLOTS, offset = 0) => {
    const profileId = Number(activeProfileUserId);
    const endpoint =
      !isViewingOwnProfile && Number.isFinite(profileId) && profileId > 0
        ? `/public-wishes/user/${encodeURIComponent(String(profileId))}/cooperative/fulfilled?limit=${limit}&offset=${offset}`
        : `/public-wishes/cooperative/fulfilled/list?limit=${limit}&offset=${offset}`;
    const res = await apiFetch(endpoint);
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(
        data.detail || tr("No se pudieron cargar los deseos cooperativos cumplidos.", "Could not load fulfilled cooperative wishes.", "Impossible de load fulfilled cooperative wishes.")
      );
    }
    return data;
  };

  const formatFulfilledDate = (value) => {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleDateString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric"
    });
  };

  const getTypeIconSrc = (wishType) => personalTypeIconMap[wishType] || personalTypeIconMap["Espiritual"];

  const wishTypeLabelMap = {
    Espiritual: tr("espiritual", "spiritual", "spirituel"),
    Material: tr("material", "material", "matériel"),
    Monetario: tr("monetario", "monetary", "monétaire"),
    Profesional: tr("profesional", "professional", "professionnel"),
    "Salud y cuerpo": tr("salud y cuerpo", "health and body", "santé et corps"),
    Relacional: tr("relacional", "relational", "relationnel"),
    Vivencial: tr("vivencial", "experiential", "expérientiel")
  };

  const getWishTypeHint = (wishType) => {
    const normalized = String(wishType || "").trim();
    if (!normalized) return tr("Deseo personal", "Personal wish", "Souhait personnel");
    const mapped = wishTypeLabelMap[normalized] || normalized.toLowerCase();
    return tr(`Deseo ${mapped}`, `Wish ${mapped}`, `Wish ${mapped}`);
  };

  const PURPOSE_ORIGIN_HINT = tr(
    "Este deseo fue alguna vez un deseo de proposito de vida",
    "This wish was once a life purpose wish"
  );

  const DEFAULT_PURPOSE_ICON_SRC = "/css/icons/iconelemental.webp";

  const purposeIconMap = {
    air: "/assets/air.png",
    earth: "/assets/earth.png",
    water: "/assets/water.png",
    fire: "/assets/fire.png",
  };

  const getPurposeIconLabel = (iconKey) => {
    if (iconKey === "air") return tr("Aire", "Air", "Air");
    if (iconKey === "earth") return tr("Tierra", "Earth", "Terre");
    if (iconKey === "water") return tr("Agua", "Water", "Eau");
    if (iconKey === "fire") return tr("Fuego", "Fire", "Feu");
    return tr("Proposito", "Purpose", "Mission");
  };

  const getPurposeIconSrc = (iconKey) => purposeIconMap[String(iconKey || "")] || "";
  const getLifePurposeIconSrc = (iconKey) => getPurposeIconSrc(iconKey) || DEFAULT_PURPOSE_ICON_SRC;
  const isFromLifePurpose = (wish) => Boolean(wish?.life_purpose_slot_number || wish?.life_purpose_icon_key);

  const buildFulfilledSlots = (pageNumber = 1) => {
    const normalizedPage = Math.max(1, Math.trunc(Number(pageNumber || 1)));
    const base = (normalizedPage - 1) * FULFILLED_VISIBLE_SLOTS;
    return Array.from({ length: FULFILLED_VISIBLE_SLOTS }, (_, index) => base + index + 1);
  };

  const loadFulfilledPersonalWishes = async (page = personalFulfilledPage) => {
    const requestId = (personalFulfilledRequestId += 1);
    const requestedPage = Math.max(1, Math.trunc(Number(page || 1)));
    const offset = (requestedPage - 1) * FULFILLED_VISIBLE_SLOTS;
    personalFulfilledPage = requestedPage;
    personalFulfilledLoading = true;
    personalFulfilledError = "";

    try {
      const data = await fetchFulfilledPersonalWishes(FULFILLED_VISIBLE_SLOTS, offset);
      if (requestId !== personalFulfilledRequestId) return;
      const items = Array.isArray(data?.items) ? data.items : [];
      personalFulfilledItems = items;
      personalFulfilledTotal = Number(data?.total) || items.length;
    } catch (error) {
      if (requestId !== personalFulfilledRequestId) return;
      personalFulfilledItems = [];
      personalFulfilledTotal = 0;
      personalFulfilledError = error instanceof Error
        ? error.message
        : tr(
          "No se pudieron cargar tus deseos personales cumplidos.",
          "Could not load your fulfilled personal wishes."
        );
    } finally {
      if (requestId === personalFulfilledRequestId) {
        personalFulfilledLoading = false;
      }
    }
  };

  const loadFulfilledCooperativeWishes = async (page = cooperativeFulfilledPage) => {
    const requestId = (cooperativeFulfilledRequestId += 1);
    const requestedPage = Math.max(1, Math.trunc(Number(page || 1)));
    const offset = (requestedPage - 1) * FULFILLED_VISIBLE_SLOTS;
    cooperativeFulfilledPage = requestedPage;
    cooperativeFulfilledLoading = true;
    cooperativeFulfilledError = "";

    try {
      const data = await fetchFulfilledCooperativeWishes(FULFILLED_VISIBLE_SLOTS, offset);
      if (requestId !== cooperativeFulfilledRequestId) return;
      const items = Array.isArray(data?.items) ? data.items : [];
      cooperativeFulfilledItems = items;
      cooperativeFulfilledTotal = Number(data?.total) || items.length;
    } catch (error) {
      if (requestId !== cooperativeFulfilledRequestId) return;
      cooperativeFulfilledItems = [];
      cooperativeFulfilledTotal = 0;
      cooperativeFulfilledError = error instanceof Error
        ? error.message
        : tr(
          "No se pudieron cargar tus deseos cooperativos cumplidos.",
          "Could not load your fulfilled cooperative wishes."
        );
    } finally {
      if (requestId === cooperativeFulfilledRequestId) {
        cooperativeFulfilledLoading = false;
      }
    }
  };

  const goToPersonalFulfilledPage = (page) => {
    const next = Number(page);
    if (!Number.isFinite(next)) return;
    const clamped = Math.max(1, Math.min(Math.trunc(next), personalFulfilledTotalPages || 1));
    if (clamped === personalFulfilledPage) return;
    personalFulfilledPage = clamped;
    void loadFulfilledPersonalWishes(clamped);
  };

  const goToCooperativeFulfilledPage = (page) => {
    const next = Number(page);
    if (!Number.isFinite(next)) return;
    const clamped = Math.max(1, Math.min(Math.trunc(next), cooperativeFulfilledTotalPages || 1));
    if (clamped === cooperativeFulfilledPage) return;
    cooperativeFulfilledPage = clamped;
    void loadFulfilledCooperativeWishes(clamped);
  };

  $: personalFulfilledTotalPages = Math.max(
    1,
    Math.ceil(personalFulfilledTotal / FULFILLED_VISIBLE_SLOTS)
  );
  $: personalFulfilledPage = Math.min(personalFulfilledPage, personalFulfilledTotalPages);
  $: personalFulfilledPage = Math.max(personalFulfilledPage, 1);
  $: personalFulfilledPageNumbers = Array.from(
    { length: personalFulfilledTotalPages },
    (_, index) => index + 1
  );
  $: personalFulfilledRangeStart = personalFulfilledTotal
    ? (personalFulfilledPage - 1) * FULFILLED_VISIBLE_SLOTS + 1
    : 0;
  $: personalFulfilledRangeEnd = personalFulfilledTotal
    ? Math.min(personalFulfilledPage * FULFILLED_VISIBLE_SLOTS, personalFulfilledTotal)
    : 0;
  $: personalCompletedSlots = buildFulfilledSlots(personalFulfilledPage);
  $: personalCompletedView = personalCompletedSlots.map((slot, index) => ({
    slot,
    wish: personalFulfilledItems[index] || null
  }));

  $: cooperativeFulfilledTotalPages = Math.max(
    1,
    Math.ceil(cooperativeFulfilledTotal / FULFILLED_VISIBLE_SLOTS)
  );
  $: cooperativeFulfilledPage = Math.min(cooperativeFulfilledPage, cooperativeFulfilledTotalPages);
  $: cooperativeFulfilledPage = Math.max(cooperativeFulfilledPage, 1);
  $: cooperativeFulfilledPageNumbers = Array.from(
    { length: cooperativeFulfilledTotalPages },
    (_, index) => index + 1
  );
  $: cooperativeFulfilledRangeStart = cooperativeFulfilledTotal
    ? (cooperativeFulfilledPage - 1) * FULFILLED_VISIBLE_SLOTS + 1
    : 0;
  $: cooperativeFulfilledRangeEnd = cooperativeFulfilledTotal
    ? Math.min(cooperativeFulfilledPage * FULFILLED_VISIBLE_SLOTS, cooperativeFulfilledTotal)
    : 0;
  $: cooperativeCompletedSlots = buildFulfilledSlots(cooperativeFulfilledPage);
  $: cooperativeCompletedView = cooperativeCompletedSlots.map((slot, index) => ({
    slot,
    wish: cooperativeFulfilledItems[index] || null
  }));

  onMount(() => {
    const cleanup = initPurposeCoverModule();
    void syncProfileStarsTotal("fulfilledWishesStarsTotal");
    const onFulfilledChanged = (event) => {
      const scope = event?.detail?.scope;
      if (scope === "public") {
        personalFulfilledPage = 1;
        void loadFulfilledPersonalWishes(1);
        return;
      }
      if (scope === "public-cooperative") {
        cooperativeFulfilledPage = 1;
        void loadFulfilledCooperativeWishes(1);
        return;
      }
      if (!scope) {
        personalFulfilledPage = 1;
        cooperativeFulfilledPage = 1;
        void Promise.all([
          loadFulfilledPersonalWishes(1),
          loadFulfilledCooperativeWishes(1),
        ]);
      }
    };
    window.addEventListener("kiadez:fulfilled-wishes-changed", onFulfilledChanged);
    (async () => {
      try {
        await resolveProfileContext();
      } catch (error) {
        console.error(error);
      } finally {
        personalFulfilledPage = 1;
        cooperativeFulfilledPage = 1;
        void Promise.all([
          loadFulfilledPersonalWishes(1),
          loadFulfilledCooperativeWishes(1),
        ]);
      }
    })();
    return () => {
      window.removeEventListener("kiadez:fulfilled-wishes-changed", onFulfilledChanged);
      if (typeof cleanup === "function") cleanup();
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{pageTitle}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user public-wishes-background fulfilled-wishes-page">
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input
          type="search"
          placeholder={tr("Buscar en Kiadez", "Search on Kiadez", "Rechercher sur Kiadez")}
          aria-label={tr("Buscar", "Search", "Rechercher")}
        />
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
        <img id="coverImg" class="cover-img" src="/assets/cover-default.jpg" alt={tr("Portada", "Cover", "Couverture")} />

        <div class="cover-actions">
          <details class="cover-menu">
            <summary class="icon-btn" id="btnChangeCover" title={tr("Editar imagen de portada", "Edit cover image", "Modifier l'image de couverture")}>
              {tr("Editar imagen de portada", "Edit cover image", "Modifier l'image de couverture")}
            </summary>
            <div class="cover-menu-panel">
              <button class="cover-menu-item" type="button" id="coverUpload">
                {tr("Subir imagen", "Upload image", "Téléverser une image")}
              </button>
              <button class="cover-menu-item" type="button" id="coverMove">
                {tr("Mover imagen", "Move image", "Déplacer l'image")}
              </button>
            </div>
          </details>

          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button"
            title={tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier ma mission de vie")}>
            {tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier ma mission de vie")}
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="cover-save-actions hidden" id="coverSaveActions">
          <button class="btn btn-primary btn-compact" type="button" id="coverSaveBtn">
            {tr("Guardar cambios", "Save changes", "Enregistrer les modifications")}
          </button>
          <button class="btn btn-outline btn-compact" type="button" id="coverCancelBtn">
            {tr("Cancelar", "Cancel", "Annuler")}
          </button>
        </div>

        <div class="purpose-stack" aria-label={tr("Deseos de propósito", "Purpose wishes", "Souhaits de mission")}>
          <div class="purpose-list">
            <div class="purpose-pill-row">
              <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="1"
                title={tr("Marcar deseo 1 como cumplido", "Mark wish 1 as fulfilled", "Marquer le souhait 1 comme accompli")}>
                <img src="/css/icons/iconfulfill.webp" alt={tr("Marcar deseo cumplido", "Mark wish as fulfilled", "Marquer le souhait comme accompli")} />
              </button>
              <button class="purpose-pill" type="button" id="purpose1">
                {tr("Deseo #1: Secreto", "Wish #1: Secret", "Souhait n°1 : Secret")}
              </button>
              <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock1"
                data-slot="1" title={tr("Desbloquear deseo 1", "Unlock wish 1", "Déverrouiller le souhait 1")}>
                <img src="/css/icons/iconkey.webp" alt={tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller le souhait secret")} />
              </button>
            </div>

            <div class="purpose-pill-row">
              <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="2"
                title={tr("Marcar deseo 2 como cumplido", "Mark wish 2 as fulfilled", "Marquer le souhait 2 comme accompli")}>
                <img src="/css/icons/iconfulfill.webp" alt={tr("Marcar deseo cumplido", "Mark wish as fulfilled", "Marquer le souhait comme accompli")} />
              </button>
              <button class="purpose-pill" type="button" id="purpose2">
                {tr("Deseo construir el Reino de Combray", "I wish to build the Kingdom of Combray", "Je souhaite construire le Royaume de Combray")}
              </button>
              <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock2"
                data-slot="2" title={tr("Desbloquear deseo 2", "Unlock wish 2", "Déverrouiller le souhait 2")}>
                <img src="/css/icons/iconkey.webp" alt={tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller le souhait secret")} />
              </button>
            </div>

            <div class="purpose-pill-row">
              <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="3"
                title={tr("Marcar deseo 3 como cumplido", "Mark wish 3 as fulfilled", "Marquer le souhait 3 comme accompli")}>
                <img src="/css/icons/iconfulfill.webp" alt={tr("Marcar deseo cumplido", "Mark wish as fulfilled", "Marquer le souhait comme accompli")} />
              </button>
              <button class="purpose-pill" type="button" id="purpose3">
                {tr("Deseo estar unido a Jesús", "I wish to be united with Jesus", "Je souhaite être uni à Jésus")}
              </button>
              <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock3"
                data-slot="3" title={tr("Desbloquear deseo 3", "Unlock wish 3", "Déverrouiller le souhait 3")}>
                <img src="/css/icons/iconkey.webp" alt={tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller le souhait secret")} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div class="public-wishes-body">
      <nav class="profile-nav" aria-label={tr("Navegación de perfil", "Profile navigation", "Navigation du profil")}>
        <a class="nav-pill" href="/home_user.html" title={tr("Home", "Home", "Accueil")} data-profile-module="home">{tr("Home", "Home", "Accueil")}</a>
        <a class="nav-pill" href="/star-pool-found.html" title={tr("Estrellas", "Stars", "Étoiles")}>
          <span class="nav-icon">⭐</span>
          <span><strong id="fulfilledWishesStarsTotal">0</strong> {tr("estrellas", "stars", "étoiles")}</span>
        </a>
        <a class="nav-pill" href="/followers.html" title={tr("Seguidores", "Followers", "Abonnés")}>{tr("Seguidores", "Followers", "Abonnés")}</a>
        <a class="nav-pill" href="/achievements.html" title={tr("Logros recientes", "Recent achievements", "Réalisations récentes")}>{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
        <a class="nav-pill" href="/gallery.html" title={tr("Galería", "Gallery", "Galerie")}>{tr("Galería", "Gallery", "Galerie")}</a>
        <a class="nav-pill" href="/calendar.html" title={tr("Calendario", "Calendar", "Calendrier")} data-profile-module="calendar">{tr("Calendario", "Calendar", "Calendrier")}</a>
        <a class="nav-pill" href="/my-biography.html" title={tr("Mi biografía", "My biography", "Ma biographie")}>{tr("Mi biografía", "My biography", "Ma biographie")}</a>
        <a class="nav-pill" href="/messages.html" title={tr("Mensajes", "Messages", "Messagerie")}>{tr("Mensajes", "Messages", "Messagerie")}</a>
      </nav>

      <section class="public-wishes-shell" aria-label={tr("Mis deseos cumplidos", "My fulfilled wishes", "Mes souhaits accomplis")}>
        <header class="public-wishes-head">
          <div>
            <h2 class="public-wishes-title">{headerTitle}</h2>
            <p class="public-wishes-subtitle">
              {headerSubtitle}
            </p>
          </div>
        </header>

        <section class="wish-lists-grid" aria-label={tr("Listas de deseos cumplidos", "Fulfilled wishes lists", "Listes de souhaits accomplis")}>
          <article class="panel wish-list-panel">
            <div class="panel-head">
              <h3 class="panel-title">{tr("Deseos personales cumplidos", "Fulfilled personal wishes", "Souhaits personnels accomplis")}</h3>
              <span class="panel-badge">
                {personalFulfilledItems.length} / {FULFILLED_VISIBLE_SLOTS}
              </span>
            </div>
            <ol
              class="wish-slot-list wish-slot-list-fulfilled"
              aria-label={tr("Deseos personales cumplidos", "Fulfilled personal wishes", "Souhaits personnels accomplis")}
              style={`counter-reset: wish ${Math.max(0, personalFulfilledRangeStart - 1)};`}
            >
              {#each personalCompletedView as item}
                <li class="wish-slot is-filled" data-slot={item.slot}>
                  {#if item.wish}
                    {@const fulfilledImageUrl = item.wish.fulfilled_evidence_media_url || item.wish.media_url || null}
                    <div class="wish-slot-row">
                      <div class={`wish-slot-body${fulfilledImageUrl ? "" : " single"}`}>
                        <div class="wish-slot-left">
                          <div class="wish-slot-header">
                            <button
                              class="wish-category-hint"
                              type="button"
                              data-hint={isFromLifePurpose(item.wish) ? PURPOSE_ORIGIN_HINT : getWishTypeHint(item.wish.wish_type)}
                              aria-label={isFromLifePurpose(item.wish) ? PURPOSE_ORIGIN_HINT : getWishTypeHint(item.wish.wish_type)}
	                            >
	                              <img
	                                class={`wish-slot-category-icon${isFromLifePurpose(item.wish) ? " is-purpose-icon" : ""}`}
	                                src={isFromLifePurpose(item.wish) ? getLifePurposeIconSrc(item.wish.life_purpose_icon_key) : getTypeIconSrc(item.wish.wish_type)}
	                                alt={isFromLifePurpose(item.wish) ? getPurposeIconLabel(item.wish.life_purpose_icon_key) : getWishTypeHint(item.wish.wish_type)}
	                                loading="lazy"
	                              />
	                            </button>
	                            <br />
                            <div class="wish-slot-title">{item.wish.wish_text}</div>
                            <div class="wish-slot-meta wish-slot-meta-fulfilled">
                              {#if item.wish.fulfilled_at}
                                <span class="wish-type-pill wish-fulfilled-date-pill">
                                  {tr("Cumplido el", "Fulfilled on", "Accompli le")} {formatFulfilledDate(item.wish.fulfilled_at)}
                                </span>
                              {/if}
                            </div>
                            {#if item.wish.fulfillment_message}
                              {#if item.wish.fulfilled_by_profile_url}
                                <a class="wish-fulfilled-grant-bubble" href={item.wish.fulfilled_by_profile_url}>
                                  {item.wish.fulfillment_message}
                                </a>
                              {:else}
                                <span class="wish-fulfilled-grant-bubble">
                                  {item.wish.fulfillment_message}
                                </span>
                              {/if}
                            {/if}
                          </div>
                        </div>

                        {#if fulfilledImageUrl}
                          <div class="wish-slot-image-wrap">
                            <img
                              class="wish-slot-image wish-slot-image-fulfilled"
                              src={fulfilledImageUrl}
                              alt={tr("Evidencia del deseo cumplido", "Fulfilled wish evidence", "Preuve du souhait accompli")}
                              loading="lazy"
                            />
                          </div>
                        {/if}
                      </div>
                    </div>
                  {:else}
                    <div class="wish-slot-row wish-slot-row-fulfilled">
                      <p class="wish-slot-fulfilled-message">{PLACEHOLDER_FULFILLED_MESSAGE}</p>
                    </div>
                  {/if}
                </li>
              {/each}
            </ol>
            {#if personalFulfilledTotalPages > 1}
              <nav class="wish-pagination" aria-label={tr("Paginación de deseos personales cumplidos", "Fulfilled personal wishes pagination", "Pagination des souhaits personnels accomplis")}>
                <button
                  class="wish-page-btn is-arrow"
                  type="button"
                  aria-label={tr("Página anterior", "Previous page", "Page précédente")}
                  on:click={() => goToPersonalFulfilledPage(personalFulfilledPage - 1)}
                  disabled={personalFulfilledPage <= 1}
                >
                  &lt;&lt;
                </button>
                {#each personalFulfilledPageNumbers as page}
                  <button
                    class={`wish-page-btn${page === personalFulfilledPage ? " is-active" : ""}`}
                    type="button"
                    aria-current={page === personalFulfilledPage ? "page" : undefined}
                    on:click={() => goToPersonalFulfilledPage(page)}
                  >
                    {page}
                  </button>
                {/each}
                <button
                  class="wish-page-btn is-arrow"
                  type="button"
                  aria-label={tr("Página siguiente", "Next page", "Page suivante")}
                  on:click={() => goToPersonalFulfilledPage(personalFulfilledPage + 1)}
                  disabled={personalFulfilledPage >= personalFulfilledTotalPages}
                >
                  &gt;&gt;
                </button>
              </nav>
            {/if}
            {#if personalFulfilledLoading}
              <p class="wish-fulfilled-status">{tr("Cargando deseos cumplidos...", "Loading fulfilled wishes...", "Chargement des souhaits accomplis...")}</p>
            {:else if personalFulfilledError}
              <p class="wish-fulfilled-status is-error">{personalFulfilledError}</p>
            {:else if personalFulfilledTotalPages > 1}
              <p class="wish-fulfilled-status">
                {tr("Mostrando", "Showing", "Affichage")} {personalFulfilledRangeStart}-{personalFulfilledRangeEnd} {tr("de", "of", "de")} {personalFulfilledTotal} {tr("deseos cumplidos.", "fulfilled wishes.", "souhaits accomplis.")}
              </p>
            {/if}
          </article>

          <article class="panel wish-list-panel">
            <div class="panel-head">
              <h3 class="panel-title">{tr("Deseos cooperativos cumplidos", "Fulfilled cooperative wishes", "Souhaits coopératifs accomplis")}</h3>
              <span class="panel-badge">
                {cooperativeFulfilledItems.length} / {FULFILLED_VISIBLE_SLOTS}
              </span>
            </div>
            <ol
              class="wish-slot-list wish-slot-list-fulfilled"
              aria-label={tr("Deseos cooperativos cumplidos", "Fulfilled cooperative wishes", "Souhaits coopératifs accomplis")}
              style={`counter-reset: wish ${Math.max(0, cooperativeFulfilledRangeStart - 1)};`}
            >
              {#each cooperativeCompletedView as item}
                <li class="wish-slot is-filled" data-slot={item.slot}>
                  {#if item.wish}
                    {@const fulfilledImageUrl = item.wish.fulfilled_evidence_media_url || item.wish.media_url || null}
                    <div class="wish-slot-row">
                      <div class={`wish-slot-body${fulfilledImageUrl ? "" : " single"}`}>
                        <div class="wish-slot-left">
                          <div class="wish-slot-header">
                            <button
                              class="wish-category-hint"
                              type="button"
                              data-hint={getWishTypeHint(item.wish.wish_type)}
                              aria-label={getWishTypeHint(item.wish.wish_type)}
                            >
                              <img
                                class="wish-slot-category-icon"
                                src={getTypeIconSrc(item.wish.wish_type)}
                                alt={getWishTypeHint(item.wish.wish_type)}
                                loading="lazy"
                              />
                            </button>
                            <br />
                            <div class="wish-slot-title">{item.wish.wish_text}</div>
                            <div class="wish-slot-meta wish-slot-meta-fulfilled">
                              {#if item.wish.fulfilled_at}
                                <span class="wish-type-pill wish-fulfilled-date-pill">
                                  {tr("Cumplido el", "Fulfilled on", "Accompli le")} {formatFulfilledDate(item.wish.fulfilled_at)}
                                </span>
                              {/if}
                              <span class="wish-type-pill">
                                {tr("Equipo validado:", "Validated team:", "Équipe validée :")} {Number(item.wish.participants_current || 0)} / {Number(item.wish.participants_goal || 0)}
                              </span>
                            </div>
                          </div>
                        </div>

                        {#if fulfilledImageUrl}
                          <div class="wish-slot-image-wrap">
                            <img
                              class="wish-slot-image wish-slot-image-fulfilled"
                              src={fulfilledImageUrl}
                              alt={tr("Evidencia del deseo cooperativo cumplido", "Fulfilled cooperative wish evidence", "Preuve du souhait coopératif accompli")}
                              loading="lazy"
                            />
                          </div>
                        {/if}
                      </div>
                    </div>
                  {:else}
                    <div class="wish-slot-row wish-slot-row-fulfilled">
                      <p class="wish-slot-fulfilled-message">
                        {PLACEHOLDER_FULFILLED_MESSAGE}
                      </p>
                    </div>
                  {/if}
                </li>
              {/each}
            </ol>
            {#if cooperativeFulfilledTotalPages > 1}
              <nav class="wish-pagination" aria-label={tr("Paginación de deseos cooperativos cumplidos", "Fulfilled cooperative wishes pagination", "Pagination des souhaits coopératifs accomplis")}>
                <button
                  class="wish-page-btn is-arrow"
                  type="button"
                  aria-label={tr("Página anterior", "Previous page", "Page précédente")}
                  on:click={() => goToCooperativeFulfilledPage(cooperativeFulfilledPage - 1)}
                  disabled={cooperativeFulfilledPage <= 1}
                >
                  &lt;&lt;
                </button>
                {#each cooperativeFulfilledPageNumbers as page}
                  <button
                    class={`wish-page-btn${page === cooperativeFulfilledPage ? " is-active" : ""}`}
                    type="button"
                    aria-current={page === cooperativeFulfilledPage ? "page" : undefined}
                    on:click={() => goToCooperativeFulfilledPage(page)}
                  >
                    {page}
                  </button>
                {/each}
                <button
                  class="wish-page-btn is-arrow"
                  type="button"
                  aria-label={tr("Página siguiente", "Next page", "Page suivante")}
                  on:click={() => goToCooperativeFulfilledPage(cooperativeFulfilledPage + 1)}
                  disabled={cooperativeFulfilledPage >= cooperativeFulfilledTotalPages}
                >
                  &gt;&gt;
                </button>
              </nav>
            {/if}
            {#if cooperativeFulfilledLoading}
              <p class="wish-fulfilled-status">{tr("Cargando deseos cumplidos...", "Loading fulfilled wishes...", "Chargement des souhaits accomplis...")}</p>
            {:else if cooperativeFulfilledError}
              <p class="wish-fulfilled-status is-error">{cooperativeFulfilledError}</p>
            {:else if cooperativeFulfilledTotalPages > 1}
              <p class="wish-fulfilled-status">
                {tr("Mostrando", "Showing", "Affichage")} {cooperativeFulfilledRangeStart}-{cooperativeFulfilledRangeEnd} {tr("de", "of", "de")} {cooperativeFulfilledTotal} {tr("deseos cumplidos.", "fulfilled wishes.", "souhaits accomplis.")}
              </p>
            {/if}
          </article>
        </section>
      </section>
    </div>
  </main>

  <AuthFooter />
</div>
