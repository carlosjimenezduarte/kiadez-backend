<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";

  const API = "http://127.0.0.1:8000";
  const FEED_LIMIT = 160;

  const SETTINGS_LAYOUT_ROW_1 = [
    { key: "calendar_enabled", emoji: "📆", title: "Calendario", help: "Racha y logros del calendario." },
    { key: "oracle_enabled", emoji: "🔮", title: "Oráculo", help: "Recordatorios de disponibilidad cada 3 días." },
    { key: "followers_enabled", emoji: "👥", title: "Seguidores", help: "Cuando alguien comienza a seguirte." },
  ];

  const SETTINGS_LAYOUT_ROW_2 = [
    { key: "messages_enabled", emoji: "💬", title: "Mensajería", help: "Cuando llegue un mensaje de Guardián." },
    { key: "achievements_enabled", emoji: "🏆", title: "Logros", help: "Desbloqueos por acciones en la red social." },
    { key: "mentions_enabled", emoji: "🏷️", title: "Etiquetado", help: "Cuando te mencionen entre seguidores mutuos." },
  ];

  const SETTINGS_LAYOUT_STAR = {
    key: "stars_enabled",
    emoji: "⭐",
    title: "Estrellas",
    help: "Cada vez que alguien te dona una estrella.",
  };

  let notificationsLoading = true;
  let notificationsError = "";
  let notificationsItems = [];

  let preferencesLoading = true;
  let preferencesError = "";
  let preferencesStatus = "";
  let savingPreferenceKey = "";
  let preferences = {
    calendar_enabled: true,
    oracle_enabled: true,
    followers_enabled: true,
    messages_enabled: true,
    achievements_enabled: true,
    mentions_enabled: true,
    stars_enabled: true,
  };

  const getAccessToken = () =>
    localStorage.getItem("access_token") || localStorage.getItem("kiadez_access_token") || "";

  const wait = (ms) =>
    new Promise((resolve) => {
      window.setTimeout(resolve, ms);
    });

  const parseJsonSafe = async (res) => {
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

    const response = await fetch(`${API}${path}`, { ...options, headers });
    if (response.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login.html";
      throw new Error("Sesión expirada.");
    }
    return response;
  };

  const formatDateHeading = (isoDate) => {
    if (!isoDate) return "";
    const dateValue = new Date(isoDate);
    if (Number.isNaN(dateValue.getTime())) return "";
    return new Intl.DateTimeFormat("es-CO", {
      weekday: "long",
      day: "numeric",
      month: "long",
      year: "numeric",
    }).format(dateValue);
  };

  const formatDateTime = (isoDate) => {
    if (!isoDate) return "";
    const dateValue = new Date(isoDate);
    if (Number.isNaN(dateValue.getTime())) return "";
    return new Intl.DateTimeFormat("es-CO", {
      hour: "2-digit",
      minute: "2-digit",
      day: "2-digit",
      month: "short",
    }).format(dateValue);
  };

  const notificationHref = (item) => {
    const raw = String(item?.href || "").trim();
    if (!raw) return "/notifications.html";
    if (raw.startsWith("http://") || raw.startsWith("https://")) return raw;
    if (raw.startsWith("/")) return raw;
    return `/${raw}`;
  };

  const loadNotifications = async () => {
    notificationsLoading = true;
    notificationsError = "";
    try {
      const res = await apiFetch(`/notifications/feed?limit=${encodeURIComponent(String(FEED_LIMIT))}`);
      const data = await parseJsonSafe(res);
      if (!res.ok) throw new Error(data.detail || "No se pudo cargar el Centro de Notificaciones.");
      notificationsItems = Array.isArray(data?.items) ? data.items : [];
    } catch (error) {
      notificationsItems = [];
      notificationsError = error?.message || "No se pudo cargar el Centro de Notificaciones.";
    } finally {
      notificationsLoading = false;
    }
  };

  const normalizeNotificationId = (value) => String(value || "").trim();

  const markNotificationsReadOnServer = async (notificationIds, { keepalive = false } = {}) => {
    const ids = Array.isArray(notificationIds)
      ? notificationIds
          .map((value) => normalizeNotificationId(value))
          .filter(Boolean)
          .slice(0, 64)
      : [];
    if (!ids.length) return false;

    try {
      const res = await apiFetch("/notifications/read", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ notification_ids: ids }),
        keepalive,
      });
      return res.ok;
    } catch {
      return false;
    }
  };

  const markNotificationAsReadInList = (notificationId) => {
    if (!notificationId) return;
    notificationsItems = notificationsItems.map((item) => {
      if (normalizeNotificationId(item?.id) !== notificationId) return item;
      if (item?.is_read) return item;
      return {
        ...item,
        is_read: true,
      };
    });
  };

  const handleNotificationClick = async (event, item) => {
    const notificationId = normalizeNotificationId(item?.id);
    if (!notificationId || item?.is_read) return;

    markNotificationAsReadInList(notificationId);

    const isModifiedClick = Boolean(event.metaKey || event.ctrlKey || event.shiftKey || event.altKey);
    if (isModifiedClick) {
      void markNotificationsReadOnServer([notificationId], { keepalive: true });
      return;
    }

    event.preventDefault();
    const href = notificationHref(item);
    await Promise.race([markNotificationsReadOnServer([notificationId], { keepalive: true }), wait(260)]);
    window.location.assign(href);
  };

  const loadPreferences = async () => {
    preferencesLoading = true;
    preferencesError = "";
    try {
      const res = await apiFetch("/notifications/preferences");
      const data = await parseJsonSafe(res);
      if (!res.ok) throw new Error(data.detail || "No se pudieron cargar las preferencias.");
      preferences = {
        ...preferences,
        ...data,
      };
    } catch (error) {
      preferencesError = error?.message || "No se pudieron cargar las preferencias.";
    } finally {
      preferencesLoading = false;
    }
  };

  const togglePreference = async (key) => {
    if (!key) return;
    const currentValue = Boolean(preferences?.[key]);
    const nextValue = !currentValue;

    preferencesError = "";
    preferencesStatus = "";
    savingPreferenceKey = key;
    preferences = {
      ...preferences,
      [key]: nextValue,
    };

    try {
      const res = await apiFetch("/notifications/preferences", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ [key]: nextValue }),
      });
      const data = await parseJsonSafe(res);
      if (!res.ok) throw new Error(data.detail || "No se pudo guardar la preferencia.");
      preferences = {
        ...preferences,
        ...data,
      };
      preferencesStatus = "Preferencias actualizadas.";
      await loadNotifications();
    } catch (error) {
      preferences = {
        ...preferences,
        [key]: currentValue,
      };
      preferencesError = error?.message || "No se pudo guardar la preferencia.";
    } finally {
      savingPreferenceKey = "";
    }
  };

  $: groupedNotifications = (() => {
    const groupsMap = new Map();
    const sortedItems = Array.isArray(notificationsItems) ? [...notificationsItems] : [];
    sortedItems.sort((a, b) => {
      const aTs = Date.parse(a?.created_at || "");
      const bTs = Date.parse(b?.created_at || "");
      return (Number.isNaN(bTs) ? 0 : bTs) - (Number.isNaN(aTs) ? 0 : aTs);
    });

    for (const item of sortedItems) {
      const createdAt = String(item?.created_at || "").trim();
      const dateKey = createdAt ? createdAt.slice(0, 10) : "sin-fecha";
      if (!groupsMap.has(dateKey)) {
        groupsMap.set(dateKey, {
          key: dateKey,
          label: formatDateHeading(createdAt) || "Sin fecha",
          items: [],
        });
      }
      groupsMap.get(dateKey).items.push(item);
    }

    return Array.from(groupsMap.values());
  })();

  onMount(() => {
    initPurposeCoverModule();
    void syncProfileStarsTotal("notificationsStarsTotal");

    void (async () => {
      await Promise.all([loadPreferences(), loadNotifications()]);
    })();

    const onFocus = () => {
      void loadNotifications();
    };
    window.addEventListener("focus", onFocus);

    return () => {
      window.removeEventListener("focus", onFocus);
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Centro de Notificaciones</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background notifications-page">
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
          <img src="/assets/avatar-default.jpg" alt="Perfil del usuario" />
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/privacy-and-settings.html" role="menuitem">Configuración y privacidad</a>
          <button type="button" role="menuitem" on:click={logout}>Cerrar sesión</button>
        </div>
      </details>

      <button class="topbar-icon" type="button" aria-label="Notificaciones">
        🔔
        <span class="topbar-badge">0</span>
      </button>

      <details class="topbar-dropdown">
        <summary class="topbar-menu-btn" aria-label="Abrir menú">
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">Menú</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem">Mi Home</a>
          <a href="/notifications.html" role="menuitem">Centro de Notificaciones</a>
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
    <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="/assets/cover-default.jpg" alt="Portada" />
      </div>
    </section>

    <div class="home-body notifications-body">
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
          <span class="nav-icon">⭐</span>
          <span><strong id="notificationsStarsTotal">0</strong> estrellas</span>
        </a>
        <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
        <a class="nav-pill is-active" href="/notifications.html" title="Notificaciones">Notificaciones</a>
      </nav>

      <section class="notifications-shell">
        <article class="panel notifications-settings-panel">
          <div class="panel-head">
            <h2 class="panel-title">Centro de Notificaciones</h2>
            <span class="panel-badge">Preferencias</span>
          </div>
          <p class="panel-muted notifications-settings-intro">
            Controla qué tipos de notificación deseas recibir en tu campanita y en este centro.
          </p>

          {#if preferencesLoading}
            <p class="panel-muted">Cargando preferencias...</p>
          {:else}
            <div class="notifications-settings-grid">
              {#each SETTINGS_LAYOUT_ROW_1 as item}
                <article class="notifications-setting-card">
                  <div class="notifications-setting-main">
                    <h3><span>{item.emoji}</span> {item.title}</h3>
                    <p>{item.help}</p>
                  </div>
                  <label class="switch" aria-label={`Activar o desactivar ${item.title}`}>
                    <input
                      type="checkbox"
                      checked={Boolean(preferences[item.key])}
                      disabled={Boolean(savingPreferenceKey)}
                      on:change={() => togglePreference(item.key)}
                    />
                    <span class="slider"></span>
                  </label>
                </article>
              {/each}

              {#each SETTINGS_LAYOUT_ROW_2 as item}
                <article class="notifications-setting-card">
                  <div class="notifications-setting-main">
                    <h3><span>{item.emoji}</span> {item.title}</h3>
                    <p>{item.help}</p>
                  </div>
                  <label class="switch" aria-label={`Activar o desactivar ${item.title}`}>
                    <input
                      type="checkbox"
                      checked={Boolean(preferences[item.key])}
                      disabled={Boolean(savingPreferenceKey)}
                      on:change={() => togglePreference(item.key)}
                    />
                    <span class="slider"></span>
                  </label>
                </article>
              {/each}

              <article class="notifications-setting-card is-star">
                <div class="notifications-setting-main">
                  <h3><span>{SETTINGS_LAYOUT_STAR.emoji}</span> {SETTINGS_LAYOUT_STAR.title}</h3>
                  <p>{SETTINGS_LAYOUT_STAR.help}</p>
                </div>
                <label class="switch" aria-label="Activar o desactivar notificaciones de estrellas">
                  <input
                    type="checkbox"
                    checked={Boolean(preferences[SETTINGS_LAYOUT_STAR.key])}
                    disabled={Boolean(savingPreferenceKey)}
                    on:change={() => togglePreference(SETTINGS_LAYOUT_STAR.key)}
                  />
                  <span class="slider"></span>
                </label>
              </article>
            </div>
          {/if}

          {#if preferencesError}
            <p class="settings-form-error" role="alert">{preferencesError}</p>
          {/if}
          {#if preferencesStatus}
            <p class="settings-form-success" role="status">{preferencesStatus}</p>
          {/if}
        </article>

        <article class="panel notifications-list-panel">
          <div class="panel-head">
            <h3 class="panel-title">Historial de Notificaciones</h3>
            <button class="btn btn-outline btn-compact" type="button" on:click={() => loadNotifications()}>
              Actualizar
            </button>
          </div>

          {#if notificationsLoading}
            <p class="panel-muted">Cargando notificaciones...</p>
          {:else if notificationsError}
            <p class="settings-form-error" role="alert">{notificationsError}</p>
          {:else if !groupedNotifications.length}
            <p class="panel-muted">No hay notificaciones para mostrar con la configuración actual.</p>
          {:else}
            <div class="notifications-day-groups">
              {#each groupedNotifications as group (group.key)}
                <section class="notifications-day-section">
                  <h4 class="notifications-day-title">{group.label}</h4>
                  <ul class="notifications-day-list">
                    {#each group.items as item (item.id)}
                      <li>
                        <a
                          class={`notifications-feed-item ${item?.is_read ? "is-read" : "is-unread"}`}
                          href={notificationHref(item)}
                          on:click={(event) => handleNotificationClick(event, item)}
                        >
                          <span class="notifications-feed-emoji" aria-hidden="true">{item.emoji || "🔔"}</span>
                          <span class="notifications-feed-content">
                            <strong>{item.title}</strong>
                            <span>{item.message}</span>
                            <small>{formatDateTime(item.created_at)}</small>
                          </span>
                        </a>
                      </li>
                    {/each}
                  </ul>
                </section>
              {/each}
            </div>
          {/if}
        </article>
      </section>
    </div>
  </main>
</div>
