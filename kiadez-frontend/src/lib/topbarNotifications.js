const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") ||
  "http://127.0.0.1:8000";

const FEED_LIMIT = 16;
const REFRESH_INTERVAL_MS = 60_000;
const BELL_SELECTOR =
  '.topbar-icon[aria-label="Notificaciones"], .topbar-icon[aria-label="Notifications"]';

const getUiLocale = () => {
  const saved = String(localStorage.getItem("kiadez_locale") || "").toLowerCase();
  if (saved === "es") return "es";
  if (saved === "fr") return "fr";
  return "en";
};

const tr = (es, en, fr = en) => {
  const locale = getUiLocale();
  if (locale === "es") return es;
  if (locale === "fr") return fr;
  return en;
};

const getAccessToken = () =>
  localStorage.getItem("access_token") ||
  localStorage.getItem("kiadez_access_token") ||
  "";

const parseJsonSafe = async (response) => {
  try {
    return await response.json();
  } catch {
    return {};
  }
};

const wait = (ms) =>
  new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });

const escapeHtml = (value) =>
  String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");

const formatRelativeLabel = (isoDate) => {
  if (!isoDate) return "";
  const dateValue = new Date(isoDate);
  if (Number.isNaN(dateValue.getTime())) return "";

  const deltaMs = dateValue.getTime() - Date.now();
  const minutes = Math.round(deltaMs / 60000);
  const absMinutes = Math.abs(minutes);
  if (absMinutes < 1) return tr("Ahora", "Now", "Maintenant");
  if (absMinutes < 60) {
    return minutes < 0
      ? tr(`Hace ${Math.abs(minutes)} min`, `${Math.abs(minutes)} min ago`, `Il y a ${Math.abs(minutes)} min`)
      : tr(`En ${minutes} min`, `In ${minutes} min`, `Dans ${minutes} min`);
  }

  const hours = Math.round(minutes / 60);
  const absHours = Math.abs(hours);
  if (absHours < 24) {
    return hours < 0
      ? tr(`Hace ${Math.abs(hours)} h`, `${Math.abs(hours)} h ago`, `Il y a ${Math.abs(hours)} h`)
      : tr(`En ${hours} h`, `In ${hours} h`, `Dans ${hours} h`);
  }

  const days = Math.round(hours / 24);
  const absDays = Math.abs(days);
  if (absDays < 7) {
    return days < 0
      ? tr(`Hace ${Math.abs(days)} día(s)`, `${Math.abs(days)} day(s) ago`, `Il y a ${Math.abs(days)} jour(s)`)
      : tr(`En ${days} día(s)`, `In ${days} day(s)`, `Dans ${days} jour(s)`);
  }

  const locale = getUiLocale() === "es" ? "es-CO" : getUiLocale() === "fr" ? "fr-FR" : "en-US";
  return new Intl.DateTimeFormat(locale, {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  }).format(dateValue);
};

const buildItemHref = (item) => {
  const raw = String(item?.href || "").trim();
  if (!raw) return "/notifications.html";
  if (raw.startsWith("http://") || raw.startsWith("https://")) return raw;
  if (raw.startsWith("/")) return raw;
  return `/${raw}`;
};

const fetchNotificationFeed = async () => {
  const token = getAccessToken();
  if (!token) {
    return {
      items: [],
      total_count: 0,
      unread_count: 0,
      has_more: false,
    };
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/notifications/feed?limit=${encodeURIComponent(String(FEED_LIMIT))}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (response.status === 401) {
      return {
        items: [],
        total_count: 0,
        unread_count: 0,
        has_more: false,
      };
    }

    const data = await parseJsonSafe(response);
    if (!response.ok) {
      return {
        items: [],
        total_count: 0,
        unread_count: 0,
        has_more: false,
        error: data?.detail || tr(
          "No se pudieron cargar las notificaciones.",
          "Could not load notifications.",
          "Impossible de charger les notifications."
        ),
      };
    }
    const normalizedData = data && typeof data === "object" ? data : {};
    return {
      ...normalizedData,
      items: Array.isArray(normalizedData?.items) ? normalizedData.items : [],
      unread_count: Math.max(0, Number(normalizedData?.unread_count || 0)),
    };
  } catch {
    return {
      items: [],
      total_count: 0,
      unread_count: 0,
      has_more: false,
      error: tr(
        "No se pudieron cargar las notificaciones.",
        "Could not load notifications.",
        "Impossible de charger les notifications."
      ),
    };
  }
};

const markNotificationsRead = async (notificationIds, { keepalive = false } = {}) => {
  const token = getAccessToken();
  if (!token) return false;

  const ids = Array.isArray(notificationIds)
    ? notificationIds
        .map((value) => String(value || "").trim())
        .filter(Boolean)
        .slice(0, 64)
    : [];
  if (!ids.length) return false;

  try {
    const response = await fetch(`${API_BASE_URL}/notifications/read`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ notification_ids: ids }),
      keepalive,
    });
    return response.ok;
  } catch {
    return false;
  }
};

const createPanelElements = () => {
  const panel = document.createElement("div");
  panel.className = "topbar-notifications-panel";
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", tr("Notificaciones", "Notifications", "Notifications"));
  panel.hidden = true;
  panel.innerHTML = `
    <div class="topbar-notifications-head">
      <strong>${tr("Notificaciones", "Notifications", "Notifications")}</strong>
    </div>
    <div class="topbar-notifications-list" aria-live="polite">
      <p class="topbar-notifications-status">${tr(
        "Cargando notificaciones...",
        "Loading notifications...",
        "Chargement des notifications..."
      )}</p>
    </div>
    <div class="topbar-notifications-foot">
      <a class="topbar-notifications-more" href="/notifications.html">${tr(
        "Ir al Centro de Notificaciones",
        "Go to Notification Center",
        "Aller au centre de notifications"
      )}</a>
    </div>
  `;
  return {
    panel,
    list: panel.querySelector(".topbar-notifications-list"),
  };
};

const renderNotificationList = (listNode, feed) => {
  if (!listNode) return;
  const items = Array.isArray(feed?.items) ? feed.items.slice(0, FEED_LIMIT) : [];
  const error = String(feed?.error || "").trim();

  if (error) {
    listNode.innerHTML = `<p class="topbar-notifications-status is-error">${escapeHtml(error)}</p>`;
    return;
  }

  if (!items.length) {
    listNode.innerHTML = `
      <p class="topbar-notifications-status">
        ${tr(
          "Aún no tienes notificaciones activas.",
          "You do not have active notifications yet.",
          "Vous n'avez pas encore de notifications actives."
        )}
      </p>
    `;
    return;
  }

  listNode.innerHTML = items
    .map((item) => {
      const href = buildItemHref(item);
      const emoji = escapeHtml(item?.emoji || "🔔");
      const title = escapeHtml(item?.title || tr("Notificación", "Notification", "Notification"));
      const message = escapeHtml(item?.message || "");
      const when = escapeHtml(formatRelativeLabel(item?.created_at));
      const itemId = String(item?.id || "").trim();
      const readClass = item?.is_read ? "is-read" : "is-unread";
      return `
        <a class="topbar-notification-item ${readClass}" data-notification-id="${escapeHtml(itemId)}" href="${escapeHtml(href)}">
          <span class="topbar-notification-emoji" aria-hidden="true">${emoji}</span>
          <span class="topbar-notification-content">
            <span class="topbar-notification-title">${title}</span>
            <span class="topbar-notification-message">${message}</span>
            <span class="topbar-notification-time">${when}</span>
          </span>
        </a>
      `;
    })
    .join("");
};

const applyBadge = (button, count) => {
  if (!button) return;
  let badge = button.querySelector(".topbar-badge");
  if (!badge) {
    badge = document.createElement("span");
    badge.className = "topbar-badge";
    button.appendChild(badge);
  }

  const safeCount = Math.max(0, Number(count || 0));
  if (safeCount <= 0) {
    badge.textContent = "";
    badge.classList.add("is-hidden");
    return;
  }

  badge.classList.remove("is-hidden");
  badge.textContent = safeCount > 99 ? "99+" : String(safeCount);
};

const closeAllPanels = (instances) => {
  instances.forEach((instance) => {
    instance.panel.hidden = true;
    instance.button.setAttribute("aria-expanded", "false");
  });
};

export function initTopbarNotifications() {
  const instances = [];
  let refreshTimer = null;
  let refreshInFlight = false;
  let observer = null;
  let currentUnreadCount = 0;

  const markAsReadInRenderedLists = (notificationId) => {
    if (!notificationId) return;
    instances.forEach((instance) => {
      const rows = instance.list?.querySelectorAll?.(".topbar-notification-item") || [];
      rows.forEach((row) => {
        const rowId = String(row.getAttribute("data-notification-id") || "").trim();
        if (rowId !== notificationId) return;
        row.classList.remove("is-unread");
        row.classList.add("is-read");
      });
    });
  };

  const wireButton = (button) => {
    if (!button || button.dataset.notificationsBound === "1") return;
    button.dataset.notificationsBound = "1";
    button.setAttribute("aria-haspopup", "dialog");
    button.setAttribute("aria-expanded", "false");

    const wrapper = document.createElement("div");
    wrapper.className = "topbar-notifications";
    button.parentNode?.insertBefore(wrapper, button);
    wrapper.appendChild(button);

    const panelRefs = createPanelElements();
    wrapper.appendChild(panelRefs.panel);

    const instance = {
      button,
      wrapper,
      panel: panelRefs.panel,
      list: panelRefs.list,
      itemClickHandler: null,
    };
    instances.push(instance);

    instance.itemClickHandler = (event) => {
      const link = event.target?.closest?.(".topbar-notification-item");
      if (!link) return;
      const notificationId = String(link.getAttribute("data-notification-id") || "").trim();
      if (!notificationId) return;
      const href = String(link.getAttribute("href") || "").trim() || "/notifications.html";
      const isModifiedClick = Boolean(event.metaKey || event.ctrlKey || event.shiftKey || event.altKey);

      const isUnread = link.classList.contains("is-unread");
      if (!isUnread) {
        closeAllPanels(instances);
        return;
      }

      markAsReadInRenderedLists(notificationId);
      currentUnreadCount = Math.max(0, currentUnreadCount - 1);
      instances.forEach((node) => applyBadge(node.button, currentUnreadCount));
      if (isModifiedClick) {
        void markNotificationsRead([notificationId], { keepalive: true });
        closeAllPanels(instances);
        return;
      }

      event.preventDefault();
      closeAllPanels(instances);
      void (async () => {
        await Promise.race([markNotificationsRead([notificationId], { keepalive: true }), wait(260)]);
        window.location.assign(href);
      })();
    };
    panelRefs.panel.addEventListener("click", instance.itemClickHandler);

    button.addEventListener("click", async (event) => {
      event.preventDefault();
      event.stopPropagation();
      const isOpen = !instance.panel.hidden;
      closeAllPanels(instances);
      if (isOpen) return;
      instance.panel.hidden = false;
      instance.button.setAttribute("aria-expanded", "true");

      const feed = await fetchNotificationFeed();
      renderNotificationList(instance.list, feed);
      currentUnreadCount = Math.max(0, Number(feed?.unread_count || 0));
      instances.forEach((node) => applyBadge(node.button, currentUnreadCount));
    });
  };

  const discoverButtons = () => {
    document.querySelectorAll(BELL_SELECTOR).forEach((node) => wireButton(node));
  };

  const refreshBadges = async () => {
    if (refreshInFlight) return;
    refreshInFlight = true;
    try {
      discoverButtons();
      const feed = await fetchNotificationFeed();
      currentUnreadCount = Math.max(0, Number(feed?.unread_count || 0));
      instances.forEach((instance) => {
        applyBadge(instance.button, currentUnreadCount);
        if (!instance.panel.hidden) {
          renderNotificationList(instance.list, feed);
        }
      });
    } finally {
      refreshInFlight = false;
    }
  };

  const handleDocumentClick = (event) => {
    const target = event.target;
    if (!(target instanceof Node)) return;
    const insideAnyPanel = instances.some((instance) => instance.wrapper.contains(target));
    if (!insideAnyPanel) closeAllPanels(instances);
  };

  const handleEscape = (event) => {
    if (event.key === "Escape") {
      closeAllPanels(instances);
    }
  };

  const handleFocus = () => {
    void refreshBadges();
  };

  discoverButtons();
  void refreshBadges();

  refreshTimer = window.setInterval(() => {
    void refreshBadges();
  }, REFRESH_INTERVAL_MS);

  observer = new MutationObserver(() => {
    discoverButtons();
  });
  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });

  document.addEventListener("click", handleDocumentClick);
  window.addEventListener("keydown", handleEscape);
  window.addEventListener("focus", handleFocus);

  return () => {
    if (refreshTimer) {
      window.clearInterval(refreshTimer);
      refreshTimer = null;
    }
    if (observer) {
      observer.disconnect();
      observer = null;
    }
    document.removeEventListener("click", handleDocumentClick);
    window.removeEventListener("keydown", handleEscape);
    window.removeEventListener("focus", handleFocus);
    instances.forEach((instance) => {
      if (instance.itemClickHandler) {
        instance.panel.removeEventListener("click", instance.itemClickHandler);
      }
    });
    instances.splice(0, instances.length);
  };
}
