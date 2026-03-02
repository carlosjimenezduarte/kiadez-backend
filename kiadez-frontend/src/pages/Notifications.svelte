<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";
  import { getLocale } from "../lib/i18n";

  const API = "http://127.0.0.1:8000";
  const FEED_LIMIT = 160;
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

  const SETTINGS_LAYOUT_ROW_1 = [
    {
      key: "calendar_enabled",
      emoji: "📆",
      title: tr("Calendario", "Calendar", "Calendrier"),
      help: tr("Racha y logros del calendario.", "Calendar streak and achievements.", "Série du calendrier et réalisations."),
    },
    {
      key: "oracle_enabled",
      emoji: "🔮",
      title: tr("Oráculo", "Oracle", "Oracle"),
      help: tr("Recordatorios de disponibilidad cada 3 días.", "Availability reminders every 3 days.", "Rappels de disponibilité tous les 3 jours."),
    },
    {
      key: "followers_enabled",
      emoji: "👥",
      title: tr("Seguidores", "Followers", "Abonnés"),
      help: tr("Cuando alguien comienza a seguirte.", "When someone starts following you.", "Quand quelqu'un commence à te suivre."),
    },
  ];

  const SETTINGS_LAYOUT_ROW_2 = [
    {
      key: "messages_enabled",
      emoji: "💬",
      title: tr("Mensajería", "Messaging", "Messagerie"),
      help: tr("Cuando llegue un mensaje de Guardián.", "When a Guardian message arrives.", "Quand un message de Gardien arrive."),
    },
    {
      key: "achievements_enabled",
      emoji: "🏆",
      title: tr("Logros", "Achievements", "Réalisations"),
      help: tr("Desbloqueos por acciones en la red social.", "Unlocks from actions in the social network.", "Déblocages issus des actions dans le réseau social."),
    },
    {
      key: "mentions_enabled",
      emoji: "🏷️",
      title: tr("Etiquetado", "Mentions", "Mentions"),
      help: tr("Cuando te mencionen entre seguidores mutuos.", "When you are mentioned among mutual followers.", "Quand tu es mentionné parmi les abonnés mutuels."),
    },
  ];

  const SETTINGS_LAYOUT_STAR = {
    key: "stars_enabled",
    emoji: "⭐",
    title: tr("Estrellas", "Stars", "Étoiles"),
    help: tr("Cada vez que alguien te dona una estrella.", "Every time someone donates a star to you.", "Chaque fois que quelqu'un te donne une étoile."),
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
      throw new Error(tr("No hay sesión activa.", "No active session.", "Aucune session active."));
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
      throw new Error(tr("Sesión expirada.", "Session expired.", "Session expirée."));
    }
    return response;
  };

  const formatDateHeading = (isoDate) => {
    if (!isoDate) return "";
    const dateValue = new Date(isoDate);
    if (Number.isNaN(dateValue.getTime())) return "";
    return new Intl.DateTimeFormat(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
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
    return new Intl.DateTimeFormat(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
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
      if (!res.ok) throw new Error(data.detail || tr("No se pudo cargar el Centro de Notificaciones.", "Could not load Notification Center.", "Impossible de charger le Centre de notifications."));
      notificationsItems = Array.isArray(data?.items) ? data.items : [];
    } catch (error) {
      notificationsItems = [];
      notificationsError = error?.message || tr("No se pudo cargar el Centro de Notificaciones.", "Could not load Notification Center.", "Impossible de charger le Centre de notifications.");
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
      if (!res.ok) throw new Error(data.detail || tr("No se pudieron cargar las preferencias.", "Could not load preferences.", "Impossible de charger les préférences."));
      preferences = {
        ...preferences,
        ...data,
      };
    } catch (error) {
      preferencesError = error?.message || tr("No se pudieron cargar las preferencias.", "Could not load preferences.", "Impossible de charger les préférences.");
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
      if (!res.ok) throw new Error(data.detail || tr("No se pudo guardar la preferencia.", "Could not save preference.", "Impossible d'enregistrer la préférence."));
      preferences = {
        ...preferences,
        ...data,
      };
      preferencesStatus = tr("Preferencias actualizadas.", "Preferences updated.", "Préférences mises à jour.");
      await loadNotifications();
    } catch (error) {
      preferences = {
        ...preferences,
        [key]: currentValue,
      };
      preferencesError = error?.message || tr("No se pudo guardar la preferencia.", "Could not save preference.", "Impossible d'enregistrer la préférence.");
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
      const dateKey = createdAt ? createdAt.slice(0, 10) : "no-date";
      if (!groupsMap.has(dateKey)) {
        groupsMap.set(dateKey, {
          key: dateKey,
          label: formatDateHeading(createdAt) || tr("Sin fecha", "No date", "Aucune date"),
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
  <title>{tr("Kiadez — Centro de Notificaciones", "Kiadez — Notification Center", "Kiadez — Centre de notifications")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background notifications-page">
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
      <a class="topbar-btn" href="/home_user.html">🏠 Home</a>
      <a class="topbar-btn" href="/gallery.html">🖼️ {tr("Galería", "Gallery", "Galerie")}</a>
      <a class="topbar-btn" href="/my-public-whishes.html">🌐 {tr("Deseos públicos", "Public wishes", "Souhaits publics")}</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 {tr("Deseos privados", "Private wishes", "Souhaits privés")}</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html">✅ {tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</a>
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
        <span class="topbar-badge">0</span>
      </button>

      <details class="topbar-dropdown">
        <summary class="topbar-menu-btn" aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}>
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">{tr("Menú", "Menu", "Navigation")}</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem">{tr("Mi Home", "My Home", "Mon accueil")}</a>
          <a href="/notifications.html" role="menuitem">{tr("Centro de Notificaciones", "Notification Center", "Centre de notifications")}</a>
          <a href="/achievements.html" role="menuitem">{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
          <a href="/gallery.html" role="menuitem">{tr("Galería", "Gallery", "Galerie")}</a>
          <a href="/calendar.html" role="menuitem">{tr("Calendario", "Calendar", "Calendrier")}</a>
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
      </div>
    </section>

    <div class="home-body notifications-body">
      <nav class="profile-nav" aria-label={tr("Navegación de perfil", "Profile navigation", "Navigation du profil")}>
        <a class="nav-pill" href="/home_user.html" title={tr("Home", "Home", "Accueil")}>{tr("Home", "Home", "Accueil")}</a>
        <a class="nav-pill" href="/star-pool-found.html" title={tr("Estrellas", "Stars", "Étoiles")}>
          <span class="nav-icon">⭐</span>
          <span><strong id="notificationsStarsTotal">0</strong> {tr("estrellas", "stars", "étoiles")}</span>
        </a>
        <a class="nav-pill" href="/followers.html" title={tr("Seguidores", "Followers", "Abonnés")}>{tr("Seguidores", "Followers", "Abonnés")}</a>
        <a class="nav-pill" href="/achievements.html" title={tr("Logros recientes", "Recent achievements", "Réalisations récentes")}>{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
        <a class="nav-pill" href="/gallery.html" title={tr("Galería", "Gallery", "Galerie")}>{tr("Galería", "Gallery", "Galerie")}</a>
        <a class="nav-pill" href="/calendar.html" title={tr("Calendario", "Calendar", "Calendrier")}>{tr("Calendario", "Calendar", "Calendrier")}</a>
        <a class="nav-pill" href="/my-biography.html" title={tr("Mi biografía", "My biography", "Ma biographie")}>{tr("Mi biografía", "My biography", "Ma biographie")}</a>
        <a class="nav-pill is-active" href="/notifications.html" title={tr("Notificaciones", "Notifications", "Alertes")}>{tr("Notificaciones", "Notifications", "Alertes")}</a>
      </nav>

      <section class="notifications-shell">
        <article class="panel notifications-settings-panel">
          <div class="panel-head">
            <h2 class="panel-title">{tr("Centro de Notificaciones", "Notification Center", "Centre de notifications")}</h2>
            <span class="panel-badge">{tr("Preferencias", "Preferences", "Préférences")}</span>
          </div>
          <p class="panel-muted notifications-settings-intro">
            {tr(
              "Controla qué tipos de notificación deseas recibir en tu campanita y en este centro.",
              "Control which notification types you want to receive in your bell and in this center."
            )}
          </p>

          {#if preferencesLoading}
            <p class="panel-muted">{tr("Cargando preferencias...", "Loading preferences...", "Chargement des préférences...")}</p>
          {:else}
            <div class="notifications-settings-grid">
              {#each SETTINGS_LAYOUT_ROW_1 as item}
                <article class="notifications-setting-card">
                  <div class="notifications-setting-main">
                    <h3><span>{item.emoji}</span> {item.title}</h3>
                    <p>{item.help}</p>
                  </div>
                  <label class="switch" aria-label={isEn || isFr ? `Enable or disable ${item.title}` : `Activar o desactivar ${item.title}`}>
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
                  <label class="switch" aria-label={isEn || isFr ? `Enable or disable ${item.title}` : `Activar o desactivar ${item.title}`}>
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
                <label class="switch" aria-label={tr("Activar o desactivar notificaciones de estrellas", "Enable or disable star notifications", "Activer ou désactiver les notifications d'étoiles")}>
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
            <h3 class="panel-title">{tr("Historial de Notificaciones", "Notification History", "Historique des notifications")}</h3>
            <button class="btn btn-outline btn-compact" type="button" on:click={() => loadNotifications()}>
              {tr("Actualizar", "Refresh", "Actualiser")}
            </button>
          </div>

          {#if notificationsLoading}
            <p class="panel-muted">{tr("Cargando notificaciones...", "Loading notifications...", "Chargement des notifications...")}</p>
          {:else if notificationsError}
            <p class="settings-form-error" role="alert">{notificationsError}</p>
          {:else if !groupedNotifications.length}
            <p class="panel-muted">{tr("No hay notificaciones para mostrar con la configuración actual.", "There are no notifications to show with the current settings.", "Aucune notification à afficher avec les paramètres actuels.")}</p>
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
