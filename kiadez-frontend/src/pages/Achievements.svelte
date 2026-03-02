<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";

  const API = "http://127.0.0.1:8000";
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);
  let achievementsSyncError = "";
  let weeklySyncError = "";
  let weeklyLoading = true;
  let weeklyAchievements = [];
  const WEEKLY_CATEGORY_LINES = {
    publication_stars: tr(
      "Del nacimiento de la luz a la soberania estelar.",
      "From the birth of light to stellar sovereignty.",
    ),
    fulfilled_wishes: tr(
      "El camino de orden, la palabra y la accion.",
      "The path of order, word, and action.",
    ),
    granted_wishes: tr(
      "Cuando el servicio se convierte en vocacion.",
      "When service becomes vocation.",
    ),
    calendar_streak: tr(
      "La Senda de la Constancia.",
      "The Path of Consistency.",
    ),
    donation_stars: tr(
      "El viaje hacia la union con el Universo.",
      "The journey toward union with the Universe.",
    ),
    guardian_rank: tr(
      "Hacia la conquista del corazon propio.",
      "Toward the conquest of one's own heart.",
    ),
  };

  const GUARDIAN_RANK_BADGES = [
    {
      rank: 1,
      image: "/css/AKI/Ranks/1.webp",
      es: "Aspirante",
      en: "Aspirant",
      fr: "Aspirant",
    },
    {
      rank: 2,
      image: "/css/AKI/Ranks/2.webp",
      es: "Aprendiz",
      en: "Apprentice",
      fr: "Apprenti",
    },
    {
      rank: 3,
      image: "/css/AKI/Ranks/3.webp",
      es: "Guardián",
      en: "Guardian",
      fr: "Gardien",
    },
    {
      rank: 4,
      image: "/css/AKI/Ranks/4.webp",
      es: "Guardián Consagrado",
      en: "Consecrated Guardian",
      fr: "Gardien consacré",
    },
    {
      rank: 5,
      image: "/css/AKI/Ranks/5.webp",
      es: "Guardián Mayor",
      en: "Senior Guardian",
      fr: "Gardien majeur",
    },
    {
      rank: 6,
      image: "/css/AKI/Ranks/6.webp",
      es: "Guardián del Logos",
      en: "Guardian of the Logos",
      fr: "Gardien du Logos",
    },
    {
      rank: 7,
      image: "/css/AKI/Ranks/7.webp",
      es: "Guardián del Umbral",
      en: "Guardian of the Threshold",
      fr: "Gardien du Seuil",
    },
    {
      rank: 8,
      image: "/css/AKI/Ranks/8.webp",
      es: "Guardián de Guardianes",
      en: "Guardian of Guardians",
      fr: "Gardien des Gardiens",
    },
  ];

  const guardianRankTitle = (badge) => tr(badge.es, badge.en, badge.fr);
  const guardianRankDescription = (badge) =>
    tr(
      `Has ascendido al Rango ${badge.rank} de la Jerarquía de Guardianes: ¡Ahora eres ${badge.es}!`,
      `You have advanced to Rank ${badge.rank} of the Guardian Hierarchy: You are now ${badge.en}!`,
      `Tu as accédé au rang ${badge.rank} de la hiérarchie des Gardiens : tu es maintenant ${badge.fr} !`,
    );

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
      const imagePath = normalizeImagePath(
        badgeImage?.getAttribute("src") || "",
      );
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
    if (Number.isNaN(date.getTime()))
      return tr("Sin fecha", "No date", "Aucune date");
    const text = date.toLocaleDateString(
      isEn ? "en-US" : isFr ? "fr-FR" : "es-CO",
      { weekday: "long" },
    );
    return text.charAt(0).toUpperCase() + text.slice(1);
  };

  const unlockHourLabel = (isoValue) => {
    const date = new Date(isoValue);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleTimeString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const weeklyCategoryLine = (category) => {
    return (
      WEEKLY_CATEGORY_LINES[category] ||
      tr(
        "Logro desbloqueado en esta semana.",
        "Achievement unlocked this week.",
        "Réalisation débloquée cette semaine.",
      )
    );
  };

  const normalizeCatalogText = (value) =>
    String(value || "")
      .trim()
      .replace(/\s+/g, " ")
      .replace(/[¡!]/g, "")
      .replace(/°/g, "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");

  const buildNormalizedMap = (source) =>
    Object.fromEntries(
      Object.entries(source).map(([key, val]) => [
        normalizeCatalogText(key),
        val,
      ]),
    );

  const RAW_CATALOG_TERM_TRANSLATIONS = {
    Aficionado: "Enthusiast",
    "Aliado de la Verdad": "Ally of Truth",
    "Alma del Firmamento": "Soul of the Firmament",
    Alumbramiento: "Illumination",
    Amable: "Kind",
    Aprendiz: "Apprentice",
    "Arquitecto de Constelaciones": "Architect of Constellations",
    "Arquitecto de Deseos": "Architect of Wishes",
    "Arquitecto de la Verdad": "Architect of Truth",
    "Arquitecto del Bien Común": "Architect of the Common Good",
    "Arquitecto del Cosmos": "Architect of the Cosmos",
    "Arquitecto del Tiempo": "Architect of Time",
    Aspirante: "Aspirant",
    Astral: "Astral",
    Astrónomo: "Astronomer",
    "Autor de su Camino": "Author of Their Path",
    Benefactor: "Benefactor",
    "Benefactor Eterno": "Eternal Benefactor",
    "Buen Samaritano": "Good Samaritan",
    "Caballero de la Virtud": "Knight of Virtue",
    "Cartógrafo del Cielo": "Cartographer of the Sky",
    "Coleccionista de Estrellas": "Star Collector",
    "Columna de la Comunidad": "Pillar of the Community",
    Comprometido: "Committed",
    "Conciencia Estelar": "Stellar Consciousness",
    "Confiado en el Universo": "Trusting the Universe",
    Consolidador: "Consolidator",
    Constante: "Consistent",
    "Constructor de Metas": "Goal Builder",
    "Corazón Firme": "Steadfast Heart",
    "Creyente de las Nebulosas": "Believer in the Nebulae",
    "Cronista Celeste": "Celestial Chronicler",
    "Custodio de la Luz": "Custodian of Light",
    "Custodio de su Palabra": "Keeper of Their Word",
    "Custodio del Bien": "Custodian of Good",
    "Custodio del Fondo Común": "Custodian of the Common Pool",
    "Custodio del Ritmo": "Custodian of Rhythm",
    Disciplinado: "Disciplined",
    Ejecutor: "Executor",
    "Ejemplo Vivo": "Living Example",
    Estelar: "Stellar",
    "Estrella Eterna": "Eternal Star",
    "Explorador del Misterio": "Explorer of Mystery",
    "Fiel al Proceso": "Faithful to the Process",
    "Forjador de Logros": "Forger of Achievements",
    "Forjador de Universos": "Forger of Universes",
    "Forjador del Hábito": "Habit Forger",
    Generoso: "Generous",
    "Gestor de Propósito": "Purpose Steward",
    Guardián: "Guardian",
    "Guardián Consagrado": "Consecrated Guardian",
    "Guardián Mayor": "Senior Guardian",
    "Guardián Solidario": "Supportive Guardian",
    "Guardián de Guardianes": "Guardian of Guardians",
    "Guardián del Cielo Nocturno": "Guardian of the Night Sky",
    "Guardián del Flujo Estelar": "Guardian of Stellar Flow",
    "Guardián del Logos": "Guardian of the Logos",
    "Guardián del Tiempo": "Guardian of Time",
    "Guardián del Umbral": "Guardian of the Threshold",
    "Guía por el Ejemplo": "Guide by Example",
    "Hacedor Consistente": "Consistent Doer",
    "Heraldo Estelar": "Stellar Herald",
    "Heraldo de la Generosidad": "Herald of Generosity",
    "Hijo del Cosmos": "Child of the Cosmos",
    Inquebrantable: "Unbreakable",
    Inspirado: "Inspired",
    "Intérprete de las Estrellas": "Interpreter of the Stars",
    "Maestro de la Acción": "Master of Action",
    "Maestro del Cielo Profundo": "Master of the Deep Sky",
    "Manantial de Ayuda": "Fountain of Help",
    "Mano Abierta": "Open Hand",
    "Navegante Astral": "Astral Navigator",
    "Orquestador de Astros": "Orchestrator of Stars",
    Persistente: "Persistent",
    "Pilar de Apoyo": "Pillar of Support",
    "Pilar de la Comunidad": "Pillar of the Community",
    "Portador del Cielo": "Bearer of the Sky",
    "Portador del Vacío Fértil": "Bearer of the Fertile Void",
    "Protector de Sueños": "Protector of Dreams",
    Realizador: "Achiever",
    "Referente de Coherencia": "Coherence Reference",
    "Regente del Firmamento": "Regent of the Firmament",
    "Sabio del Firmamento": "Sage of the Firmament",
    "Semilla del Infinito": "Seed of Infinity",
    "Servidor del Bien": "Servant of Good",
    "Señor de las Constelaciones": "Lord of the Constellations",
    "Soberano de las Estrellas": "Sovereign of the Stars",
    "Tejedor de Constelaciones": "Weaver of Constellations",
    "Tejedor de Destinos": "Weaver of Destinies",
    "Testimonio de Perseverancia": "Testament of Perseverance",
    "Trono de las Estrellas": "Throne of the Stars",
    "Vigilante del Firmamento": "Sentinel of the Firmament",
    "Vigía del Infinito": "Sentinel of Infinity",
    "Vinculado al Ritmo": "Linked to the Rhythm",
    Visionario: "Visionary",
    "Voluntad Activa": "Active Will",
    "Voz del Silencio Cósmico": "Voice of Cosmic Silence",
  };

  const RAW_CATALOG_SUBTITLE_TRANSLATIONS = {
    "I. Primer contacto con la luz": "I. First contact with light",
    "II. Observador del firmamento": "II. Observer of the firmament",
    "III. Dominio celeste": "III. Celestial mastery",
    "IV. Expansión cósmica": "IV. Cosmic expansion",
    "V. Trascendencia estelar": "V. Stellar transcendence",
    "VI. Eternidad": "VI. Eternity",
    "I. Despertar de la acción": "I. Awakening of action",
    "II. Dominio personal": "II. Personal mastery",
    "III. Solidez y coherencia": "III. Solidity and coherence",
    "IV. Ejemplo visible": "IV. Visible example",
    "Etapa I — Bondad consciente": "Stage I - Conscious kindness",
    "Etapa II — Virtud activa": "Stage II - Active virtue",
    "Etapa III — Servicio constante": "Stage III - Consistent service",
    "Etapa IV — Custodia y responsabilidad":
      "Stage IV - Stewardship and responsibility",
    "Etapa V — Trascendencia del acto": "Stage V - Transcendence of action",
    "Etapa I — El inicio (descubrimiento)":
      "Stage I - The beginning (discovery)",
    "Etapa II — El hábito (estructura)": "Stage II - Habit (structure)",
    "Etapa III — La identidad (arraigo)": "Stage III - Identity (rootedness)",
    "Etapa IV — La madurez (resistencia)": "Stage IV - Maturity (resilience)",
    "Etapa V — La maestría (ejemplo)": "Stage V - Mastery (example)",
    "Etapa VI — La consagración (año completo)":
      "Stage VI - Consecration (full year)",
    "Rangos de Guardianes": "Guardian ranks",
  };

  const RAW_CATALOG_TIER_TRANSLATIONS = {
    "Nivel I — Primer desprendimiento": "Level I - First release",
    "Nivel II — Confianza inicial": "Level II - Initial trust",
    "Nivel III — Fe cósmica": "Level III - Cosmic faith",
    "Nivel IV — Comprensión del flujo": "Level IV - Understanding the flow",
    "Nivel V — Entrega consciente": "Level V - Conscious offering",
    "Nivel VI — Servicio silencioso": "Level VI - Silent service",
    "Nivel VII — Sabiduría del compartir": "Level VII - Wisdom of sharing",
    "Nivel VIII — Donación como lenguaje": "Level VIII - Donation as language",
    "Nivel IX — Trascendencia colectiva": "Level IX - Collective transcendence",
    "Nivel X — Mito": "Level X - Myth",
  };

  const CATALOG_TERM_TRANSLATIONS = buildNormalizedMap(
    RAW_CATALOG_TERM_TRANSLATIONS,
  );
  const CATALOG_SUBTITLE_TRANSLATIONS = buildNormalizedMap(
    RAW_CATALOG_SUBTITLE_TRANSLATIONS,
  );
  const CATALOG_TIER_TRANSLATIONS = buildNormalizedMap(
    RAW_CATALOG_TIER_TRANSLATIONS,
  );

  const translateCatalogTerm = (value) => {
    const text = String(value || "").trim();
    if (!text) return text;
    return CATALOG_TERM_TRANSLATIONS[normalizeCatalogText(text)] || text;
  };

  const translateCatalogDescription = (value) => {
    const text = String(value || "")
      .trim()
      .replace(/\s+/g, " ");
    if (!text) return text;

    const normalized = normalizeCatalogText(text);
    let match = normalized.match(
      /^has alcanzado ([0-9\.\,]+) estrellas? por tus publicaciones$/,
    );
    if (match) {
      const amount = match[1];
      const unit = amount === "1" ? "star" : "stars";
      return `You have reached ${amount} ${unit} through your posts.`;
    }

    match = normalized.match(/^has cumplido ([0-9\.\,]+) deseos?$/);
    if (match) {
      const amount = match[1];
      const unit = amount === "1" ? "wish" : "wishes";
      return `You have fulfilled ${amount} ${unit}.`;
    }

    match = normalized.match(/^has ayudado a cumplir ([0-9\.\,]+) deseos?$/);
    if (match) {
      const amount = match[1];
      const unit = amount === "1" ? "wish" : "wishes";
      return `You have helped fulfill ${amount} ${unit}.`;
    }

    if (normalized === "has hecho tu 1 publicacion en el calendario") {
      return "You made your first post on the calendar.";
    }
    if (normalized === "has publicado 3 dias consecutivos") {
      return "You posted 3 consecutive days.";
    }
    if (normalized === "has tenido una racha de 7 dias de publicaciones") {
      return "You have had a 7-day posting streak.";
    }

    match = normalized.match(
      /^has publicado activamente en esta red social, manteniendo una racha de ([0-9\.\,]+) dias$/,
    );
    if (match) {
      return `You have posted actively on this social network, maintaining a ${match[1]}-day streak.`;
    }

    match = normalized.match(
      /^has acumulado una donacion de mas de ([0-9\.\,]+) estrellas al fondo comun de estrellas$/,
    );
    if (match) {
      return `You have accumulated a donation of more than ${match[1]} stars to the Common Star Pool.`;
    }

    match = normalized.match(
      /^has ascendido al rango ([0-9]+) de la jerarquia de guardianes: ahora eres (.+)$/,
    );
    if (match) {
      const rank = match[1];
      const role = translateCatalogTerm(match[2]);
      return `You have advanced to Rank ${rank} of the Guardian Hierarchy: You are now ${role}!`;
    }

    return text;
  };

  const localizeAchievementsCatalog = () => {
    if (!isEn) return;

    document.querySelectorAll(".badge-label, .badge-name").forEach((node) => {
      const translated = translateCatalogTerm(node.textContent || "");
      if (translated) node.textContent = translated;
    });

    document.querySelectorAll(".badge-subtitle").forEach((node) => {
      const text = String(node.textContent || "").trim();
      const translated =
        CATALOG_SUBTITLE_TRANSLATIONS[normalizeCatalogText(text)];
      if (translated) node.textContent = translated;
    });

    document.querySelectorAll(".badge-tier").forEach((node) => {
      const text = String(node.textContent || "").trim();
      const translated = CATALOG_TIER_TRANSLATIONS[normalizeCatalogText(text)];
      if (translated) node.textContent = translated;
    });

    document.querySelectorAll(".badge-desc").forEach((node) => {
      const translated = translateCatalogDescription(node.textContent || "");
      if (translated) node.textContent = translated;
    });

    document.querySelectorAll(".badge-figure img").forEach((node) => {
      const rawAlt = String(node.getAttribute("alt") || "").trim();
      const match = rawAlt.match(/^Insignia\s+(.+)$/i);
      if (!match) return;
      const translated = translateCatalogTerm(match[1]);
      node.setAttribute("alt", `Badge ${translated}`);
    });
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
        throw new Error(
          data.detail ||
            tr(
              "No se pudo sincronizar el estado de logros.",
              "Could not sync achievements state.",
              "Impossible de synchroniser l'état des réalisations.",
            ),
        );
      }

      const totalStarsLabel = document.getElementById("achievementsStarsTotal");
      if (totalStarsLabel) {
        totalStarsLabel.textContent = Number(
          data.my_received_stars_total || 0,
        ).toLocaleString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO");
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
      achievementsSyncError =
        error.message ||
        tr(
          "No se pudo sincronizar el estado de logros.",
          "Could not sync achievements state.",
          "Impossible de synchroniser l'état des réalisations.",
        );
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
        throw new Error(
          data.detail ||
            tr(
              "No se pudieron cargar los logros de esta semana.",
              "Could not load this week's achievements.",
              "Impossible de charger les réalisations de cette semaine.",
            ),
        );
      }

      weeklyAchievements = Array.isArray(data.items) ? data.items : [];
    } catch (error) {
      weeklySyncError =
        error.message ||
        tr(
          "No se pudieron cargar los logros de esta semana.",
          "Could not load this week's achievements.",
          "Impossible de charger les réalisations de cette semaine.",
        );
    } finally {
      weeklyLoading = false;
    }
  };

  onMount(() => {
    initPurposeCoverModule();
    localizeAchievementsCatalog();
    void Promise.all([loadAchievementsState(), loadWeeklyAchievements()]);
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title
    >{tr(
      "Kiadez — Logros",
      "Kiadez — Achievements",
      "Kiadez — Réalisations",
    )}</title
  >
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user achievements-background">
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input
          type="search"
          placeholder={tr(
            "Buscar en Kiadez",
            "Search on Kiadez",
            "Rechercher sur Kiadez",
          )}
          aria-label={tr("Buscar", "Search", "Rechercher")}
        />
      </form>
    </div>

    <div class="feed-topbar-zone feed-topbar-center">
      <a class="topbar-btn" href="/home_user.html">🏠 Home</a>
      <a class="topbar-btn" href="/gallery.html"
        >🖼️ {tr("Galería", "Gallery", "Galerie")}</a
      >
      <a class="topbar-btn" href="/my-public-whishes.html"
        >🌐 {tr("Deseos públicos", "Public wishes", "Souhaits publics")}</a
      >
      <a class="topbar-btn" href="/my-private-whishes.html"
        >🔒 {tr("Deseos privados", "Private wishes", "Souhaits privés")}</a
      >
      <a class="topbar-btn" href="/my-fulfilled-whises.html"
        >✅ {tr(
          "Deseos cumplidos",
          "Fulfilled wishes",
          "Souhaits accomplis",
        )}</a
      >
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown">
        <summary
          class="topbar-avatar-btn"
          aria-label={tr(
            "Perfil del usuario",
            "User profile",
            "Profil utilisateur",
          )}
        >
          <img
            src="/assets/avatar-default.jpg"
            alt={tr(
              "Foto de perfil del usuario",
              "User profile photo",
              "Photo de profil de l'utilisateur",
            )}
          />
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/privacy-and-settings.html" role="menuitem"
            >{tr(
              "Configuración y privacidad",
              "Settings and privacy",
              "Paramètres et confidentialité",
            )}</a
          >
          <button type="button" role="menuitem" on:click={logout}
            >{tr("Cerrar sesión", "Sign out", "Se déconnecter")}</button
          >
        </div>
      </details>

      <button
        class="topbar-icon"
        type="button"
        aria-label={tr("Notificaciones", "Notifications", "Alertes")}
      >
        🔔
        <span class="topbar-badge">3</span>
      </button>

      <details class="topbar-dropdown">
        <summary
          class="topbar-menu-btn"
          aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}
        >
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label"
            >{tr("Menú", "Menu", "Navigation")}</span
          >
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem"
            >{tr("Mi Home", "My Home", "Mon accueil")}</a
          >
          <a href="/achievements.html" role="menuitem"
            >{tr(
              "Logros recientes",
              "Recent achievements",
              "Réalisations récentes",
            )}</a
          >
          <a href="/gallery.html" role="menuitem"
            >{tr("Galería", "Gallery", "Galerie")}</a
          >
          <a href="/calendar.html" role="menuitem"
            >{tr("Calendario", "Calendar", "Calendrier")}</a
          >
          <a href="/my-biography.html" role="menuitem"
            >{tr("Mi Biografía", "My Biography", "Ma biographie")}</a
          >
          <a href="/messages.html" role="menuitem"
            >{tr("Mensajes", "Messages", "Messagerie")}</a
          >
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
        <img
          id="coverImg"
          class="cover-img"
          src="assets/cover-default.jpg"
          alt={tr("Portada", "Cover", "Couverture")}
        />

        <div class="cover-actions">
          <button
            class="icon-btn"
            id="btnChangeCover"
            type="button"
            title={tr(
              "Cambiar portada",
              "Change cover",
              "Changer la couverture",
            )}
          >
            {tr("Cambiar portada", "Change cover", "Changer la couverture")}
          </button>
          <button
            class="icon-btn cover-purpose-btn"
            id="btnEditPurposes"
            type="button"
            title={tr(
              "Editar mi propósito de vida",
              "Edit my life purpose",
              "Modifier ma mission de vie",
            )}
          >
            {tr(
              "Editar mi propósito de vida",
              "Edit my life purpose",
              "Modifier ma mission de vie",
            )}
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div
          class="purpose-triangle"
          aria-label={tr(
            "Deseos de propósito",
            "Purpose wishes",
            "Souhaits de mission",
          )}
        >
          <button class="purpose-pill purpose-top" type="button" id="purpose1">
            {tr("Deseo #1: Secreto", "Wish #1: Secret", "Souhait n°1 : Secret")}
          </button>

          <button class="purpose-pill purpose-left" type="button" id="purpose2">
            {tr(
              "Deseo construir el Reino de Combray",
              "I wish to build the Kingdom of Combray",
              "Je souhaite construire le Royaume de Combray",
            )}
          </button>

          <button
            class="purpose-pill purpose-right"
            type="button"
            id="purpose3"
          >
            {tr(
              "Deseo estar unido a Jesús",
              "I wish to be united with Jesus",
              "Je souhaite être uni à Jésus",
            )}
          </button>
        </div>

        <div class="cover-hint" id="coverHint">
          {tr(
            "Arrastra la portada para encuadrarla",
            "Drag the cover to frame it",
            "Déplace la couverture pour l'ajuster",
          )}
        </div>
      </div>
    </section>

    <div class="achievements-body">
      <!-- =========================
       *  NAV / LINKS
       *  ========================= -->
      <nav
        class="profile-nav"
        aria-label={tr(
          "Navegación de perfil",
          "Profile navigation",
          "Navigation du profil",
        )}
      >
        <a
          class="nav-pill"
          href="/home_user.html"
          title={tr("Home", "Home", "Accueil")}
          >{tr("Home", "Home", "Accueil")}</a
        >
        <a
          class="nav-pill"
          href="/star-pool-found.html"
          title={tr("Estrellas", "Stars", "Étoiles")}
        >
          <span class="nav-icon">⭐</span>
          <span
            ><strong id="achievementsStarsTotal">0</strong>
            {tr("estrellas", "stars", "étoiles")}</span
          >
        </a>

        <a
          class="nav-pill"
          href="/followers.html"
          title={tr("Seguidores", "Followers", "Abonnés")}
          >{tr("Seguidores", "Followers", "Abonnés")}</a
        >
        <a
          class="nav-pill"
          href="/achievements.html"
          title={tr(
            "Logros recientes",
            "Recent achievements",
            "Réalisations récentes",
          )}
          >{tr(
            "Logros recientes",
            "Recent achievements",
            "Réalisations récentes",
          )}</a
        >
        <a
          class="nav-pill"
          href="/gallery.html"
          title={tr("Galería", "Gallery", "Galerie")}
          >{tr("Galería", "Gallery", "Galerie")}</a
        >
        <a
          class="nav-pill"
          href="/calendar.html"
          title={tr("Calendario", "Calendar", "Calendrier")}
          >{tr("Calendario", "Calendar", "Calendrier")}</a
        >
        <a
          class="nav-pill"
          href="/my-biography.html"
          title={tr("Mi biografía", "My biography", "Ma biographie")}
          >{tr("Mi biografía", "My biography", "Ma biographie")}</a
        >
        <a
          class="nav-pill"
          href="/messages.html"
          title={tr("Mensajes", "Messages", "Messagerie")}
          >{tr("Mensajes", "Messages", "Messagerie")}</a
        >
      </nav>

      <!-- =========================
       *  LOGROS
       *  ========================= -->
      <section
        class="achievements-shell"
        aria-label={tr(
          "Logros e insignias",
          "Achievements and badges",
          "Réalisations et badges",
        )}
      >
        <header class="achievements-head">
          <div>
            <h2 class="achievements-title">
              {tr(
                "Logros e insignias",
                "Achievements and badges",
                "Réalisations et badges",
              )}
            </h2>
            <p class="achievements-subtitle">
              {tr(
                "Ordenados como colección y notificación semanal.",
                "Organized as collection and weekly notification.",
                "Organisé en collection et notification hebdomadaire.",
              )}
            </p>
          </div>
          <div class="achievements-tags">
            <span class="panel-badge"
              >{tr("Semana actual", "Current week", "Semaine en cours")}</span
            >
            <span class="panel-badge"
              >{tr(
                "Reinicio cada lunes",
                "Resets every Monday",
                "Réinitialisation chaque lundi",
              )}</span
            >
          </div>
        </header>

        {#if achievementsSyncError}
          <p class="achievements-sync-error">{achievementsSyncError}</p>
        {/if}

        <article class="panel weekly-achievements">
          <div class="panel-head">
            <h3 class="panel-title">
              {tr(
                "Logros obtenidos esta semana",
                "Achievements earned this week",
                "Réalisations obtenues cette semaine",
              )}
            </h3>
            <span class="panel-badge"
              >{tr(
                "Más reciente primero",
                "Most recent first",
                "Les plus récentes d'abord",
              )}</span
            >
          </div>
          <p class="panel-muted">
            {tr(
              "Esta sección se vacía el lunes siguiente y vuelve a revelar los logros de la nueva semana.",
              "This section is cleared the following Monday and reveals the achievements of the new week again.",
            )}
          </p>

          {#if weeklyLoading}
            <p class="panel-muted week-empty">
              {tr(
                "Cargando logros semanales...",
                "Loading weekly achievements...",
                "Chargement des réalisations hebdomadaires...",
              )}
            </p>
          {:else if weeklySyncError}
            <p class="achievements-sync-error">{weeklySyncError}</p>
          {:else if weeklyAchievements.length === 0}
            <p class="panel-muted week-empty">
              {tr(
                "Aún no desbloqueaste logros esta semana. Cuando ocurra, aparecerán aquí.",
                "You have not unlocked achievements this week yet. When you do, they will appear here.",
              )}
            </p>
          {:else}
            <div class="weekly-list">
              {#each weeklyAchievements as achievement (achievement.achievement_key)}
                <article class="week-day">
                  <div class="week-day-title">
                    {weekdayLabel(achievement.unlocked_at)}
                  </div>
                  <div class="week-day-line">
                    {weeklyCategoryLine(achievement.category)}
                  </div>
                  <div class="week-achievement">
                    <img
                      class="week-badge"
                      src={achievement.image_url}
                      alt={`${tr("Insignia", "Badge", "Badge")} ${achievement.title}`}
                    />
                    <div class="week-info">
                      <strong>{achievement.title}</strong>
                      <span>{achievement.description}</span>
                      <span class="week-time"
                        >{unlockHourLabel(achievement.unlocked_at)}</span
                      >
                    </div>
                  </div>
                </article>
              {/each}
            </div>
          {/if}
        </article>

        <section
          class="badge-collection"
          aria-label={tr("Insignias", "Badges", "Badges")}
        >
          <div class="panel-head">
            <h3 class="panel-title">{tr("Insignias", "Badges", "Badges")}</h3>
            <span class="panel-badge"
              >{tr(
                "Colección completa",
                "Full collection",
                "Collection complète",
              )}</span
            >
          </div>

          <!-- =========================
           *  ESTRELLAS POR PUBLICACIONES
           *  ========================= -->
          <article class="panel badge-group" id="publicationStarsBadges">
            <div>
              <h3 class="panel-title">
                {tr(
                  "Del nacimiento de la luz a la soberanía estelar",
                  "From the birth of light to stellar sovereignty",
                  "De la naissance de la lumière à la souveraineté stellaire",
                )}
              </h3>
              <p class="panel-muted">
                {tr(
                  "Sistema de logros — Estrellas por publicaciones.",
                  "Achievement system — Stars from posts.",
                  "Système de réalisations — Étoiles des publications.",
                )}
              </p>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">I. Primer contacto con la luz</h4>
              <div class="badge-grid">
                <div class="badge-item is-unlocked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star1/1a.webp"
                      alt="Insignia Alumbramiento"
                    />
                    <span class="badge-label">Alumbramiento</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Alumbramiento</div>
                    <div class="badge-desc">
                      Has alcanzado 1 estrella por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star1/1b.webp"
                      alt="Insignia Estelar"
                    />
                    <span class="badge-label">Estelar</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Estelar</div>
                    <div class="badge-desc">
                      Has alcanzado 5 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star1/1c.webp"
                      alt="Insignia Astral"
                    />
                    <span class="badge-label">Astral</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Astral</div>
                    <div class="badge-desc">
                      Has alcanzado 10 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star1/1d.webp"
                      alt="Insignia Coleccionista de Estrellas"
                    />
                    <span class="badge-label">Coleccionista de Estrellas</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Coleccionista de Estrellas</div>
                    <div class="badge-desc">
                      Has alcanzado 30 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star1/1e.webp"
                      alt="Insignia Astrónomo"
                    />
                    <span class="badge-label">Astrónomo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Astrónomo</div>
                    <div class="badge-desc">
                      Has alcanzado 100 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">II. Observador del firmamento</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star2/2a.webp"
                      alt="Insignia Cartógrafo del Cielo"
                    />
                    <span class="badge-label">Cartógrafo del Cielo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Cartógrafo del Cielo</div>
                    <div class="badge-desc">
                      Has alcanzado 200 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star2/2b.webp"
                      alt="Insignia Vigilante del Firmamento"
                    />
                    <span class="badge-label">Vigilante del Firmamento</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Vigilante del Firmamento</div>
                    <div class="badge-desc">
                      Has alcanzado 300 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star2/2c.webp"
                      alt="Insignia Tejedor de Constelaciones"
                    />
                    <span class="badge-label">Tejedor de Constelaciones</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Tejedor de Constelaciones</div>
                    <div class="badge-desc">
                      Has alcanzado 500 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star2/2d.webp"
                      alt="Insignia Cronista Celeste"
                    />
                    <span class="badge-label">Cronista Celeste</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Cronista Celeste</div>
                    <div class="badge-desc">
                      Has alcanzado 800 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star2/2e.webp"
                      alt="Insignia Intérprete de las Estrellas"
                    />
                    <span class="badge-label">Intérprete de las Estrellas</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Intérprete de las Estrellas</div>
                    <div class="badge-desc">
                      Has alcanzado 1.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">III. Dominio celeste</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star3/3a.webp"
                      alt="Insignia Arquitecto de Constelaciones"
                    />
                    <span class="badge-label">Arquitecto de Constelaciones</span
                    >
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Arquitecto de Constelaciones</div>
                    <div class="badge-desc">
                      Has alcanzado 1.500 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star3/3b.webp"
                      alt="Insignia Guardián del Cielo Nocturno"
                    />
                    <span class="badge-label">Guardián del Cielo Nocturno</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián del Cielo Nocturno</div>
                    <div class="badge-desc">
                      Has alcanzado 2.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star3/3c.webp"
                      alt="Insignia Sabio del Firmamento"
                    />
                    <span class="badge-label">Sabio del Firmamento</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Sabio del Firmamento</div>
                    <div class="badge-desc">
                      Has alcanzado 2.500 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star3/3d.webp"
                      alt="Insignia Navegante Astral"
                    />
                    <span class="badge-label">Navegante Astral</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Navegante Astral</div>
                    <div class="badge-desc">
                      Has alcanzado 3.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star3/3e.webp"
                      alt="Insignia Custodio de la Luz"
                    />
                    <span class="badge-label">Custodio de la Luz</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Custodio de la Luz</div>
                    <div class="badge-desc">
                      Has alcanzado 4.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">IV. Expansión cósmica</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star4/4a.webp"
                      alt="Insignia Heraldo Estelar"
                    />
                    <span class="badge-label">Heraldo Estelar</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Heraldo Estelar</div>
                    <div class="badge-desc">
                      Has alcanzado 5.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star4/4b.webp"
                      alt="Insignia Señor de las Constelaciones"
                    />
                    <span class="badge-label">Señor de las Constelaciones</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Señor de las Constelaciones</div>
                    <div class="badge-desc">
                      Has alcanzado 10.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star4/4c.webp"
                      alt="Insignia Maestro del Cielo Profundo"
                    />
                    <span class="badge-label">Maestro del Cielo Profundo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Maestro del Cielo Profundo</div>
                    <div class="badge-desc">
                      Has alcanzado 20.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star4/4d.webp"
                      alt="Insignia Orquestador de Astros"
                    />
                    <span class="badge-label">Orquestador de Astros</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Orquestador de Astros</div>
                    <div class="badge-desc">
                      Has alcanzado 30.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star4/4e.webp"
                      alt="Insignia Regente del Firmamento"
                    />
                    <span class="badge-label">Regente del Firmamento</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Regente del Firmamento</div>
                    <div class="badge-desc">
                      Has alcanzado 50.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">V. Trascendencia estelar</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star5/5a.webp"
                      alt="Insignia Forjador de Universos"
                    />
                    <span class="badge-label">Forjador de Universos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Forjador de Universos</div>
                    <div class="badge-desc">
                      Has alcanzado 70.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star5/5b.webp"
                      alt="Insignia Portador del Cielo"
                    />
                    <span class="badge-label">Portador del Cielo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Portador del Cielo</div>
                    <div class="badge-desc">
                      Has alcanzado 100.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star5/5c.webp"
                      alt="Insignia Soberano de las Estrellas"
                    />
                    <span class="badge-label">Soberano de las Estrellas</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Soberano de las Estrellas</div>
                    <div class="badge-desc">
                      Has alcanzado 150.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star5/5d.webp"
                      alt="Insignia Arquitecto del Cosmos"
                    />
                    <span class="badge-label">Arquitecto del Cosmos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Arquitecto del Cosmos</div>
                    <div class="badge-desc">
                      Has alcanzado 200.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star5/5e.webp"
                      alt="Insignia Vigía del Infinito"
                    />
                    <span class="badge-label">Vigía del Infinito</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Vigía del Infinito</div>
                    <div class="badge-desc">
                      Has alcanzado 300.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">VI. Eternidad</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star6/6a.webp"
                      alt="Insignia Hijo del Cosmos"
                    />
                    <span class="badge-label">Hijo del Cosmos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Hijo del Cosmos</div>
                    <div class="badge-desc">
                      Has alcanzado 600.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star6/6b.webp"
                      alt="Insignia Conciencia Estelar"
                    />
                    <span class="badge-label">Conciencia Estelar</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Conciencia Estelar</div>
                    <div class="badge-desc">
                      Has alcanzado 1.000.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star6/6c.webp"
                      alt="Insignia Alma del Firmamento"
                    />
                    <span class="badge-label">Alma del Firmamento</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Alma del Firmamento</div>
                    <div class="badge-desc">
                      Has alcanzado 1.500.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star6/6d.webp"
                      alt="Insignia Trono de las Estrellas"
                    />
                    <span class="badge-label">Trono de las Estrellas</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Trono de las Estrellas</div>
                    <div class="badge-desc">
                      Has alcanzado 2.000.000 estrellas por tus publicaciones
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Astral/Star6/6e.webp"
                      alt="Insignia Estrella Eterna"
                    />
                    <span class="badge-label">Estrella Eterna</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Estrella Eterna</div>
                    <div class="badge-desc">
                      Has alcanzado 5.000.000 estrellas por tus publicaciones
                    </div>
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
              <h3 class="panel-title">
                {tr(
                  "El camino de orden, la palabra y la acción",
                  "The path of order, word, and action",
                  "Le chemin de l'ordre, de la parole et de l'action",
                )}
              </h3>
              <p class="panel-muted">
                {tr(
                  "Logros de deseos cumplidos.",
                  "Fulfilled wishes achievements.",
                  "Réalisations des souhaits accomplis.",
                )}
              </p>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">I. Despertar de la acción</h4>
              <div class="badge-grid">
                <div class="badge-item is-unlocked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish1/1a.webp"
                      alt="Insignia Realizador"
                    />
                    <span class="badge-label">Realizador</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Realizador</div>
                    <div class="badge-desc">Has cumplido 1 deseo</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish1/1b.webp"
                      alt="Insignia Comprometido"
                    />
                    <span class="badge-label">Comprometido</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Comprometido</div>
                    <div class="badge-desc">Has cumplido 3 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish1/1c.webp"
                      alt="Insignia Constante"
                    />
                    <span class="badge-label">Constante</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Constante</div>
                    <div class="badge-desc">Has cumplido 7 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish1/1d.webp"
                      alt="Insignia Visionario"
                    />
                    <span class="badge-label">Visionario</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Visionario</div>
                    <div class="badge-desc">Has cumplido 10 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish1/1e.webp"
                      alt="Insignia Ejecutor"
                    />
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
                    <img
                      src="/css/AKI/Fulfilled/Wish2/2a.webp"
                      alt="Insignia Constructor de Metas"
                    />
                    <span class="badge-label">Constructor de Metas</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Constructor de Metas</div>
                    <div class="badge-desc">Has cumplido 30 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish2/2b.webp"
                      alt="Insignia Voluntad Activa"
                    />
                    <span class="badge-label">Voluntad Activa</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Voluntad Activa</div>
                    <div class="badge-desc">Has cumplido 50 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish2/2c.webp"
                      alt="Insignia Forjador de Logros"
                    />
                    <span class="badge-label">Forjador de Logros</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Forjador de Logros</div>
                    <div class="badge-desc">Has cumplido 100 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish2/2d.webp"
                      alt="Insignia Arquitecto de Deseos"
                    />
                    <span class="badge-label">Arquitecto de Deseos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Arquitecto de Deseos</div>
                    <div class="badge-desc">Has cumplido 200 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish2/2e.webp"
                      alt="Insignia Gestor de Propósito"
                    />
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
                    <img
                      src="/css/AKI/Fulfilled/Wish3/3a.webp"
                      alt="Insignia Hacedor Consistente"
                    />
                    <span class="badge-label">Hacedor Consistente</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Hacedor Consistente</div>
                    <div class="badge-desc">Has cumplido 400 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish3/3b.webp"
                      alt="Insignia Custodio de su Palabra"
                    />
                    <span class="badge-label">Custodio de su Palabra</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Custodio de su Palabra</div>
                    <div class="badge-desc">Has cumplido 500 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish3/3c.webp"
                      alt="Insignia Maestro de la Acción"
                    />
                    <span class="badge-label">Maestro de la Acción</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Maestro de la Acción</div>
                    <div class="badge-desc">Has cumplido 600 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish3/3d.webp"
                      alt="Insignia Consolidador"
                    />
                    <span class="badge-label">Consolidador</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Consolidador</div>
                    <div class="badge-desc">Has cumplido 700 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Fulfilled/Wish3/3e.webp"
                      alt="Insignia Autor de su Camino"
                    />
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
                    <img
                      src="/css/AKI/Fulfilled/Wish4/4a.webp"
                      alt="Insignia Referente de Coherencia"
                    />
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
              <h3 class="panel-title">
                {tr(
                  "Cuando el servicio se convierte en vocación",
                  "When service becomes vocation",
                  "Quand le service devient vocation",
                )}
              </h3>
              <p class="panel-muted">
                {tr(
                  "Logros de deseos concedidos.",
                  "Granted wishes achievements.",
                  "Réalisations des souhaits accordés.",
                )}
              </p>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa I — Bondad consciente</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill1/1a.webp"
                      alt="Insignia Amable"
                    />
                    <span class="badge-label">Amable</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Amable</div>
                    <div class="badge-desc">Has ayudado a cumplir 1 deseo</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill1/1b.webp"
                      alt="Insignia Generoso"
                    />
                    <span class="badge-label">Generoso</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Generoso</div>
                    <div class="badge-desc">Has ayudado a cumplir 3 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill1/1c.webp"
                      alt="Insignia Mano Abierta"
                    />
                    <span class="badge-label">Mano Abierta</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Mano Abierta</div>
                    <div class="badge-desc">Has ayudado a cumplir 7 deseos</div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill1/1d.webp"
                      alt="Insignia Buen Samaritano"
                    />
                    <span class="badge-label">Buen Samaritano</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Buen Samaritano</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 10 deseos
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa II — Virtud activa</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill2/2a.webp"
                      alt="Insignia Caballero de la Virtud"
                    />
                    <span class="badge-label">Caballero de la Virtud</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Caballero de la Virtud</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 20 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill2/2b.webp"
                      alt="Insignia Servidor del Bien"
                    />
                    <span class="badge-label">Servidor del Bien</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Servidor del Bien</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 30 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill2/2c.webp"
                      alt="Insignia Corazón Firme"
                    />
                    <span class="badge-label">Corazón Firme</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Corazón Firme</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 50 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill2/2d.webp"
                      alt="Insignia Aliado de la Verdad"
                    />
                    <span class="badge-label">Aliado de la Verdad</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Aliado de la Verdad</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 70 deseos
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa III — Servicio constante</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill3/3a.webp"
                      alt="Insignia Benefactor"
                    />
                    <span class="badge-label">Benefactor</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Benefactor</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 100 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill3/3b.webp"
                      alt="Insignia Pilar de Apoyo"
                    />
                    <span class="badge-label">Pilar de Apoyo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Pilar de Apoyo</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 150 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill3/3c.webp"
                      alt="Insignia Guardián Solidario"
                    />
                    <span class="badge-label">Guardián Solidario</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián Solidario</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 200 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill3/3d.webp"
                      alt="Insignia Manantial de Ayuda"
                    />
                    <span class="badge-label">Manantial de Ayuda</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Manantial de Ayuda</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 300 deseos
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">
                Etapa IV — Custodia y responsabilidad
              </h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill4/4a.webp"
                      alt="Insignia Custodio del Bien"
                    />
                    <span class="badge-label">Custodio del Bien</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Custodio del Bien</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 400 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill4/4b.webp"
                      alt="Insignia Protector de Sueños"
                    />
                    <span class="badge-label">Protector de Sueños</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Protector de Sueños</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 500 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill4/4c.webp"
                      alt="Insignia Arquitecto de la Verdad"
                    />
                    <span class="badge-label">Arquitecto de la Verdad</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Arquitecto de la Verdad</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 600 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill4/4d.webp"
                      alt="Insignia Guía por el Ejemplo"
                    />
                    <span class="badge-label">Guía por el Ejemplo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guía por el Ejemplo</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 700 deseos
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa V — Trascendencia del acto</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill5/5a.webp"
                      alt="Insignia Heraldo de la Generosidad"
                    />
                    <span class="badge-label">Heraldo de la Generosidad</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Heraldo de la Generosidad</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 1.000 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill5/5b.webp"
                      alt="Insignia Tejedor de Destinos"
                    />
                    <span class="badge-label">Tejedor de Destinos</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Tejedor de Destinos</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 2.000 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill5/5c.webp"
                      alt="Insignia Columna de la Comunidad"
                    />
                    <span class="badge-label">Columna de la Comunidad</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Columna de la Comunidad</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 3.000 deseos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Granted/Fullfill5/5d.webp"
                      alt="Insignia Benefactor Eterno"
                    />
                    <span class="badge-label">Benefactor Eterno</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Benefactor Eterno</div>
                    <div class="badge-desc">
                      Has ayudado a cumplir 5.000 deseos
                    </div>
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
              <h3 class="panel-title">
                {tr(
                  "La Senda de la Constancia",
                  "The Path of Consistency",
                  "Le chemin de la constance",
                )}
              </h3>
              <p class="panel-muted">
                {tr(
                  "Logros de calendario.",
                  "Calendar achievements.",
                  "Réalisations du calendrier.",
                )}
              </p>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">
                Etapa I — El inicio (descubrimiento)
              </h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar1/1a.webp"
                      alt="Insignia Aficionado"
                    />
                    <span class="badge-label">Aficionado</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Aficionado</div>
                    <div class="badge-desc">
                      Has hecho tu 1° publicación en el calendario
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar1/1b.webp"
                      alt="Insignia Inspirado"
                    />
                    <span class="badge-label">Inspirado</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Inspirado</div>
                    <div class="badge-desc">
                      Has publicado 3 días consecutivos
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar1/1c.webp"
                      alt="Insignia Disciplinado"
                    />
                    <span class="badge-label">Disciplinado</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Disciplinado</div>
                    <div class="badge-desc">
                      Has tenido una racha de 7 días de publicaciones
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa II — El hábito (estructura)</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar2/2a.webp"
                      alt="Insignia Constante"
                    />
                    <span class="badge-label">Constante</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Constante</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 15 días
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar2/2b.webp"
                      alt="Insignia Comprometido"
                    />
                    <span class="badge-label">Comprometido</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Comprometido</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 21 días
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar2/2c.webp"
                      alt="Insignia Persistente"
                    />
                    <span class="badge-label">Persistente</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Persistente</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 30 días
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa III — La identidad (arraigo)</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar3/3a.webp"
                      alt="Insignia Forjador del Hábito"
                    />
                    <span class="badge-label">Forjador del Hábito</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Forjador del Hábito</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 90 días
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar3/3b.webp"
                      alt="Insignia Vinculado al Ritmo"
                    />
                    <span class="badge-label">Vinculado al Ritmo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Vinculado al Ritmo</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 120 días
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar3/3c.webp"
                      alt="Insignia Fiel al Proceso"
                    />
                    <span class="badge-label">Fiel al Proceso</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Fiel al Proceso</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 150 días
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">
                Etapa IV — La madurez (resistencia)
              </h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar4/4a.webp"
                      alt="Insignia Inquebrantable"
                    />
                    <span class="badge-label">Inquebrantable</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Inquebrantable</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 180 días
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar4/4b.webp"
                      alt="Insignia Custodio del Ritmo"
                    />
                    <span class="badge-label">Custodio del Ritmo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Custodio del Ritmo</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 220 días
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar4/4c.webp"
                      alt="Insignia Arquitecto del Tiempo"
                    />
                    <span class="badge-label">Arquitecto del Tiempo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Arquitecto del Tiempo</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 250 días
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">Etapa V — La maestría (ejemplo)</h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar5/5a.webp"
                      alt="Insignia Ejemplo Vivo"
                    />
                    <span class="badge-label">Ejemplo Vivo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Ejemplo Vivo</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 280 días
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar5/5b.webp"
                      alt="Insignia Pilar de la Comunidad"
                    />
                    <span class="badge-label">Pilar de la Comunidad</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Pilar de la Comunidad</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 310 días
                    </div>
                  </div>
                </div>

                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar5/5c.webp"
                      alt="Insignia Testimonio de Perseverancia"
                    />
                    <span class="badge-label">Testimonio de Perseverancia</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Testimonio de Perseverancia</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 340 días
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">
                Etapa VI — La consagración (año completo)
              </h4>
              <div class="badge-grid">
                <div class="badge-item is-locked">
                  <button class="badge-figure" type="button">
                    <img
                      src="/css/AKI/Calendar/Calendar6/6a.webp"
                      alt="Insignia Guardián del Tiempo"
                    />
                    <span class="badge-label">Guardián del Tiempo</span>
                  </button>
                  <div class="badge-body">
                    <div class="badge-name">Guardián del Tiempo</div>
                    <div class="badge-desc">
                      Has publicado activamente en esta red social, manteniendo
                      una racha de 365 días
                    </div>
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
              <h3 class="panel-title">
                {tr(
                  "El viaje hacia la unión con el Universo",
                  "The journey toward union with the Universe",
                  "Le voyage vers l'union avec l'Univers",
                )}
              </h3>
              <p class="panel-muted">
                {tr(
                  "Logros de donación de estrellas.",
                  "Star donation achievements.",
                  "Réalisations liées aux dons d'étoiles.",
                )}
              </p>
            </div>

            <div class="badge-grid badge-grid-5">
              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img
                    src="/css/AKI/Donation/1.webp"
                    alt="Insignia Explorador del Misterio"
                  />
                  <span class="badge-label">Explorador del Misterio</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel I — Primer desprendimiento</div>
                  <div class="badge-name">Explorador del Misterio</div>
                  <div class="badge-desc">
                    Has acumulado una donación de más de 1.000 estrellas al
                    Fondo Común de Estrellas
                  </div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img
                    src="/css/AKI/Donation/2.webp"
                    alt="Insignia Confiado en el Universo"
                  />
                  <span class="badge-label">Confiado en el Universo</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel II — Confianza inicial</div>
                  <div class="badge-name">Confiado en el Universo</div>
                  <div class="badge-desc">
                    Has acumulado una donación de más de 5.000 estrellas al
                    Fondo Común de Estrellas
                  </div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img
                    src="/css/AKI/Donation/3.webp"
                    alt="Insignia Creyente de las Nebulosas"
                  />
                  <span class="badge-label">Creyente de las Nebulosas</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel III — Fe cósmica</div>
                  <div class="badge-name">Creyente de las Nebulosas</div>
                  <div class="badge-desc">
                    Has acumulado una donación de más de 10.000 estrellas al
                    Fondo Común de Estrellas
                  </div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img
                    src="/css/AKI/Donation/4.webp"
                    alt="Insignia Guardián del Flujo Estelar"
                  />
                  <span class="badge-label">Guardián del Flujo Estelar</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel IV — Comprensión del flujo</div>
                  <div class="badge-name">Guardián del Flujo Estelar</div>
                  <div class="badge-desc">
                    Has acumulado una donación de más de 20.000 estrellas al
                    Fondo Común de Estrellas
                  </div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img
                    src="/css/AKI/Donation/5.webp"
                    alt="Insignia Portador del Vacío Fértil"
                  />
                  <span class="badge-label">Portador del Vacío Fértil</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel V — Entrega consciente</div>
                  <div class="badge-name">Portador del Vacío Fértil</div>
                  <div class="badge-desc">
                    Has acumulado una donación de más de 50.000 estrellas al
                    Fondo Común de Estrellas
                  </div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img
                    src="/css/AKI/Donation/6.webp"
                    alt="Insignia Custodio del Fondo Común"
                  />
                  <span class="badge-label">Custodio del Fondo Común</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel VI — Servicio silencioso</div>
                  <div class="badge-name">Custodio del Fondo Común</div>
                  <div class="badge-desc">
                    Has acumulado una donación de más de 100.000 estrellas al
                    Fondo Común de Estrellas
                  </div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img
                    src="/css/AKI/Donation/7.webp"
                    alt="Insignia Tejedor de Constelaciones"
                  />
                  <span class="badge-label">Tejedor de Constelaciones</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">
                    Nivel VII — Sabiduría del compartir
                  </div>
                  <div class="badge-name">Tejedor de Constelaciones</div>
                  <div class="badge-desc">
                    Has acumulado una donación de más de 200.000 estrellas al
                    Fondo Común de Estrellas
                  </div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img
                    src="/css/AKI/Donation/8.webp"
                    alt="Insignia Voz del Silencio Cósmico"
                  />
                  <span class="badge-label">Voz del Silencio Cósmico</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">
                    Nivel VIII — Donación como lenguaje
                  </div>
                  <div class="badge-name">Voz del Silencio Cósmico</div>
                  <div class="badge-desc">
                    Has acumulado una donación de más de 300.000 estrellas al
                    Fondo Común de Estrellas
                  </div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img
                    src="/css/AKI/Donation/9.webp"
                    alt="Insignia Arquitecto del Bien Común"
                  />
                  <span class="badge-label">Arquitecto del Bien Común</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">
                    Nivel IX — Trascendencia colectiva
                  </div>
                  <div class="badge-name">Arquitecto del Bien Común</div>
                  <div class="badge-desc">
                    Has acumulado una donación de más de 500.000 estrellas al
                    Fondo Común de Estrellas
                  </div>
                </div>
              </div>

              <div class="badge-item is-locked">
                <button class="badge-figure" type="button">
                  <img
                    src="/css/AKI/Donation/10.webp"
                    alt="Insignia Semilla del Infinito"
                  />
                  <span class="badge-label">Semilla del Infinito</span>
                </button>
                <div class="badge-body">
                  <div class="badge-tier">Nivel X — Mito</div>
                  <div class="badge-name">Semilla del Infinito</div>
                  <div class="badge-desc">
                    Has acumulado una donación de más de 1.000.000 estrellas al
                    Fondo Común de Estrellas
                  </div>
                </div>
              </div>
            </div>
          </article>

          <!-- =========================
           *  JERARQUÍA DE GUARDIANES
           *  ========================= -->
          <article class="panel badge-group">
            <div>
              <h3 class="panel-title">
                {tr(
                  "Hacía la conquista del corazón propio",
                  "Toward conquering one's own heart",
                  "Vers la conquête de son propre cœur",
                )}
              </h3>
              <p class="panel-muted">
                {tr(
                  "Logros de Jerarquía de Guardianes.",
                  "Guardian Hierarchy achievements.",
                  "Réalisations de la hiérarchie des Gardiens.",
                )}
              </p>
            </div>

            <div class="badge-subgroup">
              <h4 class="badge-subtitle">
                {tr(
                  "Rangos de Guardianes",
                  "Guardian ranks",
                  "Rangs de Gardien",
                )}
              </h4>
              <div class="badge-grid">
                {#each GUARDIAN_RANK_BADGES as badge}
                  <div class="badge-item is-locked">
                    <button class="badge-figure" type="button">
                      <img
                        src={badge.image}
                        alt={`${tr("Insignia", "Badge", "Insigne")} ${guardianRankTitle(badge)}`}
                      />
                      <span class="badge-label">{guardianRankTitle(badge)}</span>
                    </button>
                    <div class="badge-body">
                      <div class="badge-name">{guardianRankTitle(badge)}</div>
                      <div class="badge-desc">{guardianRankDescription(badge)}</div>
                    </div>
                  </div>
                {/each}
              </div>
            </div>
          </article>
        </section>
      </section>
    </div>
  </main>

  <AuthFooter />
</div>
