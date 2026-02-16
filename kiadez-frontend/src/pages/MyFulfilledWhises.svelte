<script>
  import { onMount } from "svelte";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";
  import { logout } from "../lib/logout";

  const API = "http://127.0.0.1:8000";
  const FULFILLED_VISIBLE_SLOTS = 10;
  const PLACEHOLDER_FULFILLED_MESSAGE = "Aquí se publicará tu deseo cuando lo marques como cumplido.";

  const personalTypeIconMap = {
    "Espiritual": "/css/icons/Espiritual.webp",
    "Material": "/css/icons/Material.webp",
    "Monetario": "/css/icons/Monetario.webp",
    "Profesional": "/css/icons/Profesional.webp",
    "Salud y cuerpo": "/css/icons/Salud.webp",
    "Relacional": "/css/icons/Relacional.webp",
    "Vivencial": "/css/icons/Vivencial.webp"
  };

  const personalCompletedSlots = Array.from({ length: FULFILLED_VISIBLE_SLOTS }, (_, index) => index + 1);
  const cooperativeCompletedSlots = Array.from({ length: FULFILLED_VISIBLE_SLOTS }, (_, index) => index + 1);

  let personalFulfilledItems = [];
  let personalCompletedView = personalCompletedSlots.map((slot) => ({ slot, wish: null }));
  let personalFulfilledTotal = 0;
  let personalFulfilledError = "";
  let personalFulfilledLoading = false;

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
      throw new Error("No hay sesión activa.");
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`
    };
    const res = await fetch(`${API}${path}`, { ...options, headers });
    if (res.status === 401) {
      throw new Error("Sesión expirada. Inicia sesión nuevamente.");
    }
    return res;
  };

  const fetchFulfilledPersonalWishes = async (limit = FULFILLED_VISIBLE_SLOTS, offset = 0) => {
    const res = await apiFetch(`/public-wishes/personal/fulfilled?limit=${limit}&offset=${offset}`);
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(data.detail || "No se pudieron cargar tus deseos personales cumplidos.");
    }
    return data;
  };

  const formatFulfilledDate = (value) => {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleDateString("es-CO", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric"
    });
  };

  const getTypeIconSrc = (wishType) => personalTypeIconMap[wishType] || personalTypeIconMap["Espiritual"];

  const getWishTypeHint = (wishType) => {
    const normalized = String(wishType || "").trim();
    if (!normalized) return "Deseo personal";
    return `Deseo ${normalized.toLowerCase()}`;
  };

  const PURPOSE_ORIGIN_HINT = "Este deseo fue alguna vez un deseo de propósito de vida";

  const DEFAULT_PURPOSE_ICON_SRC = "/css/icons/iconelemental.webp";

  const purposeIconMap = {
    air: "/assets/air.png",
    earth: "/assets/earth.png",
    water: "/assets/water.png",
    fire: "/assets/fire.png",
  };

  const getPurposeIconLabel = (iconKey) => {
    if (iconKey === "air") return "Aire";
    if (iconKey === "earth") return "Tierra";
    if (iconKey === "water") return "Agua";
    if (iconKey === "fire") return "Fuego";
    return "Propósito";
  };

  const getPurposeIconSrc = (iconKey) => purposeIconMap[String(iconKey || "")] || "";
  const getLifePurposeIconSrc = (iconKey) => getPurposeIconSrc(iconKey) || DEFAULT_PURPOSE_ICON_SRC;
  const isFromLifePurpose = (wish) => Boolean(wish?.life_purpose_slot_number || wish?.life_purpose_icon_key);

  const loadFulfilledPersonalWishes = async () => {
    personalFulfilledLoading = true;
    personalFulfilledError = "";

    try {
      const data = await fetchFulfilledPersonalWishes();
      personalFulfilledItems = Array.isArray(data?.items) ? data.items : [];
      personalFulfilledTotal = Number(data?.total) || personalFulfilledItems.length;
    } catch (error) {
      personalFulfilledItems = [];
      personalFulfilledTotal = 0;
      personalFulfilledError = error instanceof Error
        ? error.message
        : "No se pudieron cargar tus deseos personales cumplidos.";
    } finally {
      personalFulfilledLoading = false;
    }
  };

  $: personalCompletedView = personalCompletedSlots.map((slot, index) => ({
    slot,
    wish: personalFulfilledItems[index] || null
  }));

  onMount(() => {
    const cleanup = initPurposeCoverModule();
    void syncProfileStarsTotal("fulfilledWishesStarsTotal");
    const onFulfilledChanged = (event) => {
      const scope = event?.detail?.scope;
      if (scope !== "public") return;
      void loadFulfilledPersonalWishes();
    };
    window.addEventListener("kiadez:fulfilled-wishes-changed", onFulfilledChanged);
    loadFulfilledPersonalWishes();
    return () => {
      window.removeEventListener("kiadez:fulfilled-wishes-changed", onFulfilledChanged);
      if (typeof cleanup === "function") cleanup();
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Mis deseos cumplidos</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user public-wishes-background fulfilled-wishes-page">
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
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="/assets/cover-default.jpg" alt="Portada" />

        <div class="cover-actions">
          <details class="cover-menu">
            <summary class="icon-btn" id="btnChangeCover" title="Editar imagen de portada">
              Editar imagen de portada
            </summary>
            <div class="cover-menu-panel">
              <button class="cover-menu-item" type="button" id="coverSelectExisting">
                Seleccionar imagen
              </button>
              <button class="cover-menu-item" type="button" id="coverUpload">
                Subir imagen
              </button>
              <button class="cover-menu-item" type="button" id="coverMove">
                Mover imagen
              </button>
            </div>
          </details>

          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button"
            title="Editar mi propósito de vida">
            Editar mi propósito de vida
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="cover-save-actions hidden" id="coverSaveActions">
          <button class="btn btn-primary btn-compact" type="button" id="coverSaveBtn">
            Guardar cambios
          </button>
          <button class="btn btn-outline btn-compact" type="button" id="coverCancelBtn">
            Cancelar
          </button>
        </div>

        <div class="purpose-stack" aria-label="Deseos de propósito">
          <div class="purpose-list">
            <div class="purpose-pill-row">
              <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="1"
                title="Marcar deseo 1 como cumplido">
                <img src="/css/icons/iconfulfill.webp" alt="Marcar deseo cumplido" />
              </button>
              <button class="purpose-pill" type="button" id="purpose1">
                Deseo #1: Secreto
              </button>
              <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock1"
                data-slot="1" title="Desbloquear deseo 1">
                <img src="/css/icons/iconkey.webp" alt="Desbloquear deseo secreto" />
              </button>
            </div>

            <div class="purpose-pill-row">
              <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="2"
                title="Marcar deseo 2 como cumplido">
                <img src="/css/icons/iconfulfill.webp" alt="Marcar deseo cumplido" />
              </button>
              <button class="purpose-pill" type="button" id="purpose2">
                Deseo construir el Reino de Combray
              </button>
              <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock2"
                data-slot="2" title="Desbloquear deseo 2">
                <img src="/css/icons/iconkey.webp" alt="Desbloquear deseo secreto" />
              </button>
            </div>

            <div class="purpose-pill-row">
              <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="3"
                title="Marcar deseo 3 como cumplido">
                <img src="/css/icons/iconfulfill.webp" alt="Marcar deseo cumplido" />
              </button>
              <button class="purpose-pill" type="button" id="purpose3">
                Deseo estar unido a Jesús
              </button>
              <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock3"
                data-slot="3" title="Desbloquear deseo 3">
                <img src="/css/icons/iconkey.webp" alt="Desbloquear deseo secreto" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div class="public-wishes-body">
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
          <span class="nav-icon">⭐</span>
          <span><strong id="fulfilledWishesStarsTotal">0</strong> estrellas</span>
        </a>
        <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
      </nav>

      <section class="public-wishes-shell" aria-label="Mis deseos cumplidos">
        <header class="public-wishes-head">
          <div>
            <h2 class="public-wishes-title">Mis deseos cumplidos</h2>
            <p class="public-wishes-subtitle">
              Este espacio mostrará los deseos que marques como cumplidos.
            </p>
          </div>
        </header>

        <section class="wish-lists-grid" aria-label="Listas de deseos cumplidos">
          <article class="panel wish-list-panel">
            <div class="panel-head">
              <h3 class="panel-title">Deseos personales cumplidos</h3>
              <span class="panel-badge">
                {Math.min(personalFulfilledTotal, FULFILLED_VISIBLE_SLOTS)} / {FULFILLED_VISIBLE_SLOTS}
              </span>
            </div>
            <ol class="wish-slot-list wish-slot-list-fulfilled" aria-label="Deseos personales cumplidos">
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
                                  Cumplido el {formatFulfilledDate(item.wish.fulfilled_at)}
                                </span>
                              {/if}
                            </div>
                          </div>
                        </div>

                        {#if fulfilledImageUrl}
                          <div class="wish-slot-image-wrap">
                            <img
                              class="wish-slot-image wish-slot-image-fulfilled"
                              src={fulfilledImageUrl}
                              alt="Evidencia del deseo cumplido"
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
            {#if personalFulfilledLoading}
              <p class="wish-fulfilled-status">Cargando deseos cumplidos...</p>
            {:else if personalFulfilledError}
              <p class="wish-fulfilled-status is-error">{personalFulfilledError}</p>
            {:else if personalFulfilledTotal > FULFILLED_VISIBLE_SLOTS}
              <p class="wish-fulfilled-status">
                Mostrando los últimos {FULFILLED_VISIBLE_SLOTS} de {personalFulfilledTotal} deseos cumplidos.
              </p>
            {/if}
          </article>

          <article class="panel wish-list-panel">
            <div class="panel-head">
              <h3 class="panel-title">Deseos cooperativos cumplidos</h3>
              <span class="panel-badge">0 / 10</span>
            </div>
            <ol class="wish-slot-list wish-slot-list-fulfilled" aria-label="Deseos cooperativos cumplidos">
              {#each cooperativeCompletedSlots as slot}
                <li class="wish-slot is-filled wish-slot-fulfilled" data-slot={slot}>
                  <div class="wish-slot-row wish-slot-row-fulfilled">
                    <p class="wish-slot-fulfilled-message">
                      {PLACEHOLDER_FULFILLED_MESSAGE}
                    </p>
                  </div>
                </li>
              {/each}
            </ol>
          </article>
        </section>
      </section>
    </div>
  </main>
</div>
