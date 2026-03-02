<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";

  onMount(() => {
    document.body.dataset.visitor = "false";
    initPurposeCoverModule();

    const oracleCards = [
          {
            id: 1,
            name: "El Ciclo",
            question: "¿Cuál es tu ciclo de las reencarnaciones?",
            context:
              "Enfocado en comprender situaciones que perturban tu viaje en este mundo. En tu vida diaria, ¿qué es eso que va y vuelve de la misma manera, por más que intentes evitarlo? Por ejemplo: discusiones repetidas, una adicción, un patrón emocional o el deseo constante de tener más de algo."
          },
          {
            id: 2,
            name: "La Calma",
            question: "Si pudieras vivir tu vida desde la calma, ¿qué decisión tomarías hoy?",
            context:
              "Enfocado en comprender por qué actúas como actúas actualmente. ¿Qué es lo que realmente te presiona a decidir con prisa? ¿Qué limita tu pensamiento, tu espíritu o tu manera natural de ser en este momento de tu vida?"
          },
          {
            id: 3,
            name: "El Silencio",
            question: "¿Te cuesta mantenerte en silencio?",
            context:
              "Enfocado en comprender si puedes escuchar tu propio pensamiento o si actúas solo por impulso. ¿Cuál es tu relación con el silencio? ¿Puedes estar diez minutos sin estímulos o sientes la necesidad de llenar ese espacio con música, pantallas o distracciones?"
          },
          {
            id: 4,
            name: "El Anhelo",
            question: "¿Cuál sería la vida de tus sueños?",
            context:
              "Enfocado en reconocer qué sientes que te falta para sentirte pleno. Si hoy fuera el último día de tu vida, ¿qué considerarías que no viviste? ¿Qué cualidades, experiencias o formas de ser te hubiera gustado manifestar?"
          },
          {
            id: 5,
            name: "La Elección",
            question: "Si pudieras cambiar algo del mundo, ¿qué elegirías?",
            context:
              "Enfocado en identificar aquello con lo que no estás de acuerdo. ¿Qué crees que no debería existir ni en tu vida ni en la de los demás? Si pudieras eliminarlo, ¿el mundo sería mejor? ¿Tú te sentirías más libre o en paz?"
          },
          {
            id: 6,
            name: "La Libertad",
            question: "¿Te consideras una persona libre?",
            context:
              "Enfocado en reconocer cómo te sientes con la vida que llevas. ¿Existe algo que percibas como una carga constante? ¿Alguna situación física, emocional o mental que afecte tu día a día? ¿O te sientes realmente cómodo con tu forma de vivir?"
          },
          {
            id: 7,
            name: "La Sombra",
            question: "¿Qué es lo que más evitas mirar de ti?",
            context:
              "Enfocado en reconocer aquello que prefieres no enfrentar. Puede ser una emoción, un recuerdo, una actitud o una verdad incómoda. A veces lo que evitamos mirar es justamente lo que más necesita atención para poder transformarse."
          },
          {
            id: 8,
            name: "El Refugio",
            question: "¿Qué te hace sentir en casa?",
            context:
              "Enfocado en identificar aquello que te brinda seguridad y tranquilidad. Puede ser un lugar, una persona, una actividad o un estado interior. Reconocerlo te ayuda a saber dónde recargar tu energía cuando la vida se vuelve exigente."
          },
          {
            id: 9,
            name: "El Gozo",
            question: "¿Qué parte de tu día disfrutas más?",
            context:
              "Enfocado en observar qué momentos te conectan con el gozo. A veces la felicidad no está en grandes logros, sino en instantes simples que solemos pasar por alto. ¿Qué te dice eso sobre lo que realmente valoras?"
          },
          {
            id: 10,
            name: "El Desgaste",
            question: "¿Qué te roba más energía?",
            context:
              "Enfocado en reconocer hábitos, personas o pensamientos que te desgastan. Identificar qué te drena es el primer paso para proteger tu bienestar y tomar decisiones más conscientes sobre a qué le entregas tu tiempo y tu atención."
          },
          {
            id: 11,
            name: "El Aprendiz",
            question: "¿Qué te gustaría aprender?",
            context:
              "Enfocado en conectar con tu curiosidad natural. Aprender no siempre tiene que ver con estudios formales; puede ser una habilidad, una forma de vivir o una manera distinta de relacionarte contigo y con los demás."
          },
          {
            id: 12,
            name: "El Mérito",
            question: "¿Cuándo fue la última vez que te sentiste orgulloso de ti?",
            context:
              "Enfocado en reconocer tus propios logros, grandes o pequeños. Muchas veces avanzamos sin detenernos a valorar lo que hemos superado. Recordarlo fortalece la autoestima y el respeto por tu propio camino."
          },
          {
            id: 13,
            name: "El Apego",
            question: "¿Qué te da miedo perder?",
            context:
              "Enfocado en identificar apegos importantes en tu vida. El miedo a perder algo suele revelar cuánto valor le damos y cuánto dependemos de ello. Observarlo con honestidad ayuda a comprender nuestras decisiones."
          },
          {
            id: 14,
            name: "La Vitalidad",
            question: "¿Qué te hace sentir vivo?",
            context:
              "Enfocado en descubrir aquello que despierta tu entusiasmo. Puede ser crear, ayudar, aprender, moverte o compartir. Reconocerlo te orienta hacia una vida más alineada con lo que te nutre internamente."
          },
          {
            id: 15,
            name: "La Demora",
            question: "¿Qué sueles postergar?",
            context:
              "Enfocado en observar aquello que dejas para después. A veces no se trata de pereza, sino de miedo, cansancio o falta de claridad. Entender por qué postergas algo puede darte pistas importantes sobre lo que necesitas."
          },
          {
            id: 16,
            name: "La Gratitud",
            question: "¿Qué agradeces hoy?",
            context:
              "Enfocado en ejercitar la gratitud consciente. Incluso en días difíciles siempre hay algo que reconocer. Agradecer no niega los problemas, pero cambia la forma en que los miras y los atraviesas."
          },
          {
            id: 17,
            name: "La Voz",
            question: "¿Qué te gustaría decir y no has dicho?",
            context:
              "Enfocado en reconocer palabras retenidas. A veces callamos por miedo a herir, a perder o a exponernos. Identificar lo que no expresas te ayuda a entender qué necesitas comunicar, aunque sea primero contigo mismo."
          },
          {
            id: 18,
            name: "La Paz",
            question: "¿Qué te hace sentir en paz?",
            context:
              "Enfocado en identificar estados, actividades o relaciones que aquietan tu mente. La paz no siempre llega sola; muchas veces se construye al elegir conscientemente aquello que te devuelve equilibrio."
          },
          {
            id: 19,
            name: "El Cuidado",
            question: "¿Qué parte de tu vida necesita más atención?",
            context:
              "Enfocado en observar áreas descuidadas. Puede ser tu cuerpo, tus emociones, tus vínculos o tu descanso. Detectarlo a tiempo permite pequeños ajustes antes de que el desequilibrio se haga mayor."
          },
          {
            id: 20,
            name: "La Lección",
            question: "¿Qué te enseñó tu último error?",
            context:
              "Enfocado en resignificar el error como aprendizaje. Más allá de la culpa o la frustración, cada error deja una lección. Reconocerla te permite avanzar con más claridad y menos peso."
          },
          {
            id: 21,
            name: "Lo Esencial",
            question: "¿Qué te gustaría simplificar?",
            context:
              "Enfocado en identificar excesos. A veces complicamos nuestra vida más de lo necesario. Simplificar puede significar soltar objetos, compromisos, pensamientos o expectativas que ya no te aportan bienestar."
          },
          {
            id: 22,
            name: "El Cuerpo",
            question: "¿Qué te conecta con tu cuerpo?",
            context:
              "Enfocado en reconocer cómo habitas tu cuerpo. Puede ser el movimiento, la respiración, el descanso o la alimentación. Escuchar al cuerpo es una forma directa de volver al presente."
          },
          {
            id: 23,
            name: "El Vínculo",
            question: "¿Qué te hace sentir acompañado?",
            context:
              "Enfocado en identificar vínculos reales. No siempre se trata de estar rodeado de gente, sino de sentir comprensión y presencia. Reconocerlo te ayuda a cuidar mejor tus relaciones."
          },
          {
            id: 24,
            name: "La Liberación",
            question: "¿Qué te gustaría soltar?",
            context:
              "Enfocado en observar cargas innecesarias. Puede ser un resentimiento, una culpa, una expectativa o un hábito. Soltar no es olvidar, es liberar espacio para algo nuevo."
          },
          {
            id: 25,
            name: "El Futuro",
            question: "¿Qué te entusiasma del futuro?",
            context:
              "Enfocado en conectar con la esperanza. Pensar en lo que viene no como ansiedad, sino como posibilidad. Reconocer qué te ilusiona te da dirección y energía para el presente."
          },
          {
            id: 26,
            name: "El Aporte",
            question: "¿Qué te hace sentir útil?",
            context:
              "Enfocado en reconocer tu aporte al mundo. Sentirte útil no depende de grandes logros, sino de saber que lo que haces tiene sentido para ti o para otros."
          },
          {
            id: 27,
            name: "El Reposo",
            question: "¿Qué necesitas descansar?",
            context:
              "Enfocado en identificar cansancios acumulados. A veces no es solo el cuerpo, sino la mente o el corazón. Reconocerlo es el primer paso para darte permiso de pausar."
          },
          {
            id: 28,
            name: "La Protección",
            question: "¿Qué te gustaría cuidar más?",
            context:
              "Enfocado en reconocer aquello que valoras. Puede ser tu salud, una relación, un sueño o tu tiempo. Cuidar algo implica presencia y decisiones conscientes."
          },
          {
            id: 29,
            name: "La Identidad",
            question: "¿Qué te recuerda quién eres?",
            context:
              "Enfocado en identificar anclas personales. Puede ser una actividad, una persona, un recuerdo o un valor. Reconocerlo te ayuda a no perderte cuando todo alrededor cambia."
          },
          {
            id: 30,
            name: "La Intención",
            question: "¿Qué intención eliges para hoy?",
            context:
              "Enfocado en cerrar el ciclo con conciencia. Elegir una intención no es imponer un resultado, sino orientar tu forma de estar en el día. Una pequeña intención puede transformar toda una jornada."
          }
        ];

    const API = "http://127.0.0.1:8000";
    const AAD_VAULT = new TextEncoder().encode("kiadez-vault-v1");
    const ORACLE_AAD_PREFIX = "kiadez-oracle-v1";
    const COOLDOWN_MS = 72 * 60 * 60 * 1000;
    const YEAR_MS = 365 * 24 * 60 * 60 * 1000;
    const MAX_HISTORY_ENTRIES = 4;
    const MAX_RESPONSE_WORDS = 500;
    const TOTAL_CARDS = oracleCards.length;
    let isViewingOwnProfile = true;
    let viewerUserId = null;
    let viewerUsername = "";
    let activeProfileUserId = null;
    let activeProfileUsername = "";
    let activeProfileFullName = "";
    let oracleUserName = "Usuario Kiadez";

    const oracleDeck = document.getElementById("oracleDeck");
    const oracleStatus = document.getElementById("oracleStatus");
    const oracleCooldown = document.getElementById("oracleCooldown");
    const oracleDeckEmpty = document.getElementById("oracleDeckEmpty");
    const oracleRevealed = document.getElementById("oracleRevealed");
    const oracleRevealedEmpty = document.getElementById("oracleRevealedEmpty");

    const oracleModalOverlay = document.getElementById("oracleModalOverlay");
    const closeOracleModal = document.getElementById("closeOracleModal");
    const oracleCardName = document.getElementById("oracleCardName");
    const oracleCardQuestion = document.getElementById("oracleCardQuestion");
    const oracleCardImage = document.getElementById("oracleCardImage");
    const oracleCardContext = document.getElementById("oracleCardContext");
    const oracleCardResponse = document.getElementById("oracleCardResponse");
    const oracleWordCounter = document.getElementById("oracleWordCounter");
    const oracleModalNote = document.getElementById("oracleModalNote");
    const oracleActionRow = document.getElementById("oracleActionRow");
    const oracleSecretActions = document.getElementById("oracleSecretActions");
    const oracleRevealSecretBtn = document.getElementById("oracleRevealSecretBtn");
    const oracleSecretUnlock = document.getElementById("oracleSecretUnlock");
    const oracleSecretUnlockPassword = document.getElementById("oracleSecretUnlockPassword");
    const oracleSecretUnlockError = document.getElementById("oracleSecretUnlockError");
    const oracleSecretUnlockConfirm = document.getElementById("oracleSecretUnlockConfirm");
    const oracleSecretUnlockCancel = document.getElementById("oracleSecretUnlockCancel");
    const oracleConfirm = document.getElementById("oracleConfirm");
    const oracleConfirmText = document.getElementById("oracleConfirmText");
    const oracleConfirmYes = document.getElementById("oracleConfirmYes");
    const oracleConfirmNo = document.getElementById("oracleConfirmNo");
    const oraclePrivatePasswordWrap = document.getElementById("oraclePrivatePasswordWrap");
    const oraclePrivatePasswordInput = document.getElementById("oraclePrivatePassword");
    const oraclePrivatePasswordError = document.getElementById("oraclePrivatePasswordError");
    const oraclePublishBtn = document.getElementById("oraclePublishBtn");
    const oracleSecretBtn = document.getElementById("oracleSecretBtn");
    const oracleHeartBtn = document.getElementById("oracleHeartBtn");
    const oracleHistory = document.getElementById("oracleHistory");
    const oracleHistoryNote = document.getElementById("oracleHistoryNote");
    const oracleHistoryList = document.getElementById("oracleHistoryList");

    const buildFallbackState = () => ({
      cycle: 1,
      cycleStartAt: Date.now(),
      lastPickAt: null,
      cooldownMs: COOLDOWN_MS,
      cooldownRemainingMs: 0,
      cycleComplete: false,
      revealedThisCycle: [],
      history: {}
    });

    let oracleState = buildFallbackState();
    const oracleEntriesById = new Map();
    let selectedCard = null;
    let pendingAction = null;
    let pendingDeleteEntryId = null;
    let pendingSecretRevealEntryId = null;
    let isSubmitting = false;

    const bufToHex = (buf) =>
      [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");

    const hexToBuf = (hex) => {
      const normalized = (hex || "").trim();
      if (!normalized) return new ArrayBuffer(0);
      const bytes = new Uint8Array(normalized.length / 2);
      for (let i = 0; i < bytes.length; i += 1) {
        bytes[i] = parseInt(normalized.substr(i * 2, 2), 16);
      }
      return bytes.buffer;
    };

    const getAccessToken = () =>
      localStorage.getItem("access_token") || localStorage.getItem("kiadez_access_token") || "";

    const countWords = (text) => {
      const value = String(text || "").trim();
      if (!value) return 0;
      return value.split(/\s+/).filter(Boolean).length;
    };

    const updateWordCounter = () => {
      if (!oracleWordCounter) return 0;
      const words = countWords(oracleCardResponse?.value || "");
      oracleWordCounter.textContent = `${words}/${MAX_RESPONSE_WORDS} palabras`;
      oracleWordCounter.classList.toggle("is-exceeded", words > MAX_RESPONSE_WORDS);
      return words;
    };

    const setPrivatePasswordError = (message) => {
      if (!oraclePrivatePasswordError) return;
      oraclePrivatePasswordError.textContent = message || "";
    };

    const setSecretUnlockError = (message) => {
      if (!oracleSecretUnlockError) return;
      oracleSecretUnlockError.textContent = message || "";
    };

    const resetSecretUnlockUi = () => {
      pendingSecretRevealEntryId = null;
      if (oracleSecretUnlock) {
        oracleSecretUnlock.classList.add("hidden");
      }
      if (oracleSecretUnlockPassword) {
        oracleSecretUnlockPassword.value = "";
      }
      setSecretUnlockError("");
    };

    const openSecretUnlockUi = (entryId) => {
      const id = Number(entryId || 0);
      if (!Number.isFinite(id) || id <= 0) return;
      pendingSecretRevealEntryId = id;
      pendingAction = null;
      pendingDeleteEntryId = null;
      oracleConfirm.classList.add("hidden");
      if (oracleSecretUnlock) {
        oracleSecretUnlock.classList.remove("hidden");
      }
      setSecretUnlockError("");
      setTimeout(() => oracleSecretUnlockPassword?.focus(), 0);
    };

    const resetPrivatePasswordUi = () => {
      if (oraclePrivatePasswordWrap) {
        oraclePrivatePasswordWrap.classList.add("hidden");
      }
      if (oraclePrivatePasswordInput) {
        oraclePrivatePasswordInput.value = "";
      }
      setPrivatePasswordError("");
    };

    const showPrivatePasswordUi = () => {
      if (oraclePrivatePasswordWrap) {
        oraclePrivatePasswordWrap.classList.remove("hidden");
      }
      setPrivatePasswordError("");
      setTimeout(() => oraclePrivatePasswordInput?.focus(), 0);
    };

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
        localStorage.removeItem("kiadez_access_token");
        window.location.href = "/login.html";
        throw new Error("Sesión expirada.");
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
      document.querySelectorAll(".purpose-side-btn").forEach((btn) => btn.classList.add("hidden"));
      document.querySelector(".oracle-deck")?.classList.add("hidden");
    };

    const applyOracleHeader = () => {
      const title = document.querySelector(".oracle-title");
      if (title) {
        title.textContent = isViewingOwnProfile
          ? "El Oráculo"
          : `Oráculo de ${activeProfileFullName || "usuario"}`;
      }
      const subtitle = document.querySelector(".oracle-subtitle");
      if (subtitle) {
        subtitle.textContent = isViewingOwnProfile
          ? "Selecciona una carta para comprender tu presente. Solo una carta cada 3 días."
          : "Solo podrás ver las respuestas públicas de este usuario.";
      }
      document.title = isViewingOwnProfile
        ? "Kiadez — Oráculo"
        : `Kiadez — Oráculo de ${activeProfileFullName || "usuario"}`;
      if (!isViewingOwnProfile && oracleRevealedEmpty) {
        oracleRevealedEmpty.textContent = "Aún no hay cartas públicas reveladas.";
      }
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

      oracleUserName = activeProfileFullName || "Este usuario";
      applyOracleHeader();
      setMyHomeLinks(buildViewerHomeUrl());
      syncProfileModuleLinks();
    };

    const pbkdf2Key = async (password, saltBuf, iters) => {
      const baseKey = await crypto.subtle.importKey(
        "raw",
        new TextEncoder().encode(password),
        "PBKDF2",
        false,
        ["deriveKey"]
      );
      return crypto.subtle.deriveKey(
        { name: "PBKDF2", salt: saltBuf, iterations: iters, hash: "SHA-256" },
        baseKey,
        { name: "AES-GCM", length: 256 },
        false,
        ["encrypt", "decrypt"]
      );
    };

    const decryptDekFromPassword = async (privatePassword) => {
      const vaultRes = await apiFetch("/vault/record");
      const vaultData = await parseResponseJson(vaultRes);
      if (!vaultRes.ok) {
        throw new Error(vaultData.detail || "No se pudo leer el vault.");
      }

      const kdfSalt = hexToBuf(vaultData.kdf_salt_b64 || "");
      const wrappedDekNonce = new Uint8Array(hexToBuf(vaultData.wrapped_dek_nonce_b64 || ""));
      const wrappedDek = hexToBuf(vaultData.wrapped_dek_b64 || "");
      const iters = Number(vaultData.kdf_iters || 310000);

      const kek = await pbkdf2Key(privatePassword, kdfSalt, iters);
      const dekRaw = await crypto.subtle.decrypt(
        { name: "AES-GCM", iv: wrappedDekNonce, additionalData: AAD_VAULT },
        kek,
        wrappedDek
      );
      return crypto.subtle.importKey("raw", dekRaw, { name: "AES-GCM" }, false, ["encrypt", "decrypt"]);
    };

    const aesGcmEncryptText = async (key, text, aadBuf) => {
      const nonce = crypto.getRandomValues(new Uint8Array(12));
      const ciphertext = await crypto.subtle.encrypt(
        { name: "AES-GCM", iv: nonce, additionalData: aadBuf },
        key,
        new TextEncoder().encode(text)
      );
      return { nonce, ciphertext };
    };

    const aesGcmDecryptText = async (key, ciphertextHex, nonceHex, aadBuf) => {
      const decrypted = await crypto.subtle.decrypt(
        { name: "AES-GCM", iv: new Uint8Array(hexToBuf(nonceHex)), additionalData: aadBuf },
        key,
        hexToBuf(ciphertextHex)
      );
      return new TextDecoder().decode(decrypted);
    };

    const buildOracleAad = (cardId, cycle) =>
      new TextEncoder().encode(`${ORACLE_AAD_PREFIX}:${cardId}:${cycle}`);

    const normalizeOracleState = (payload) => {
      const fallback = buildFallbackState();
      const history = {};
      oracleEntriesById.clear();

      const responses = Array.isArray(payload?.responses) ? payload.responses : [];
      responses.forEach((response) => {
        const cardId = Number(response?.card_id || 0);
        if (!Number.isFinite(cardId) || cardId < 1 || cardId > TOTAL_CARDS) return;

        const entry = {
          id: Number(response?.id || 0),
          cardId,
          cycle: Number(response?.cycle || 1),
          type: String(response?.response_type || "heart"),
          text: response?.text_public || "",
          ciphertextHex: response?.ciphertext_hex || "",
          nonceHex: response?.nonce_hex || "",
          date: response?.created_at || new Date().toISOString(),
        };

        if (!history[cardId]) history[cardId] = [];
        history[cardId].push(entry);
        if (entry.id > 0) {
          oracleEntriesById.set(entry.id, entry);
        }
      });

      Object.values(history).forEach((entries) => {
        entries.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
      });

      const revealedThisCycle = Array.isArray(payload?.revealed_this_cycle)
        ? payload.revealed_this_cycle
            .map((value) => Number(value))
            .filter((value) => Number.isFinite(value) && value >= 1 && value <= TOTAL_CARDS)
        : [];

      return {
        cycle: Number(payload?.cycle || fallback.cycle),
        cycleStartAt: payload?.cycle_started_at
          ? new Date(payload.cycle_started_at).getTime()
          : fallback.cycleStartAt,
        lastPickAt: payload?.last_pick_at ? new Date(payload.last_pick_at).getTime() : null,
        cooldownMs: Number(payload?.cooldown_ms || COOLDOWN_MS),
        cooldownRemainingMs: Math.max(0, Number(payload?.cooldown_remaining_ms || 0)),
        cycleComplete: Boolean(payload?.cycle_complete || revealedThisCycle.length >= TOTAL_CARDS),
        revealedThisCycle,
        history,
      };
    };

    const shuffleCards = (cards) => {
      const shuffled = [...cards];
      for (let i = shuffled.length - 1; i > 0; i -= 1) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
      }
      return shuffled;
    };

    const getCardImage = (cardId) => `/css/oracle/Oracle${cardId}.webp`;

    const formatDate = (date) => {
      const months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
      ];
      const day = date.getDate();
      const month = months[date.getMonth()];
      let hours = date.getHours();
      const minutes = date.getMinutes().toString().padStart(2, "0");
      const isPm = hours >= 12;
      hours = hours % 12;
      hours = hours === 0 ? 12 : hours;
      const suffix = isPm ? "p.m." : "a.m.";
      return `${day} de ${month} a las ${hours}:${minutes} ${suffix}`;
    };

    const formatCooldown = (remainingMs) => {
      const daysLeft = Math.ceil(remainingMs / (24 * 60 * 60 * 1000));
      if (daysLeft <= 1) {
        return "En 1 día podrás elegir una nueva carta.";
      }
      return `En ${daysLeft} días podrás elegir una nueva carta.`;
    };

    const getCardHistory = (cardId) => {
      const entries = oracleState.history[cardId] || [];
      return entries.slice().sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    };

    const isUserResponseEntry = (entry) =>
      Boolean(entry && (entry.type === "public" || entry.type === "secret"));

    const getCardHistoryForDisplay = (cardId) => {
      const allResponses = getCardHistory(cardId).filter((entry) => isUserResponseEntry(entry));
      const now = Date.now();
      const yearlyResponses = allResponses.filter((entry) => {
        const timestamp = new Date(entry.date).getTime();
        if (!Number.isFinite(timestamp)) return false;
        return now - timestamp <= YEAR_MS;
      });
      const source = yearlyResponses.length ? yearlyResponses : allResponses;
      return {
        visible: source.slice(0, MAX_HISTORY_ENTRIES),
        total: allResponses.length,
        sourceType: yearlyResponses.length ? "year" : "all",
      };
    };

    const getCurrentCycleEntries = (cardId) =>
      getCardHistory(cardId).filter((entry) => Number(entry.cycle) === Number(oracleState.cycle));

    const updateCooldownStatus = () => {
      const now = Date.now();
      const cooldownMs = Number(oracleState.cooldownMs || COOLDOWN_MS);
      const remainingMs = oracleState.lastPickAt
        ? Math.max(0, cooldownMs - (now - oracleState.lastPickAt))
        : 0;
      const cooldownActive = remainingMs > 0;
      const cycleComplete = Boolean(oracleState.cycleComplete || oracleState.revealedThisCycle.length >= TOTAL_CARDS);

      if (!cooldownActive && !cycleComplete) {
        oracleStatus.textContent = "Selecciona una carta";
        oracleCooldown.textContent = "";
      } else {
        oracleStatus.textContent = "Carta bloqueada temporalmente";
        oracleCooldown.textContent = formatCooldown(remainingMs || cooldownMs);
      }

      return { cooldownActive, cycleComplete, remainingMs };
    };

    const summarizeEntry = (entry) => {
      if (!entry) return "Carta revelada.";
      if (entry.type === "heart") {
        return `${oracleUserName} decidió no responder inmediatamente y dejó esta respuesta asentándose en su corazón.`;
      }
      if (entry.type === "secret") {
        return "Respuesta secreta cifrada en tu vault privado.";
      }
      return entry.text || "Respuesta registrada.";
    };

    const renderOracleDeck = (cards, cooldownActive, cycleComplete, remainingMs) => {
      oracleDeck.innerHTML = "";
      oracleDeckEmpty.classList.add("hidden");

      const remainingCards = cards.filter((card) => !oracleState.revealedThisCycle.includes(card.id));

      if (remainingCards.length === 0) {
        oracleDeckEmpty.textContent = cooldownActive
          ? formatCooldown(remainingMs || COOLDOWN_MS)
          : "En 3 días podrás elegir una nueva carta.";
        oracleDeckEmpty.classList.remove("hidden");
        return;
      }

      remainingCards.forEach((card) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "oracle-deck-card";
        button.dataset.cardId = `${card.id}`;
        if (cooldownActive || cycleComplete) {
          button.classList.add("is-locked");
          button.disabled = true;
        }
        button.innerHTML = `<img src="/css/oracle/carta.webp" alt="Carta del Oráculo" />`;
        button.addEventListener("click", () => openOracleModal(card.id));
        oracleDeck.appendChild(button);
      });
    };

    const renderRevealed = () => {
      oracleRevealed.innerHTML = "";
      const revealedIds = oracleState.revealedThisCycle;

      if (!revealedIds.length) {
        oracleRevealedEmpty.style.display = "block";
        return;
      }

      oracleRevealedEmpty.style.display = "none";

      revealedIds.forEach((cardId) => {
        const card = oracleCards.find((item) => item.id === cardId);
        const entries = getCardHistory(cardId);
        const latest = entries[0];
        const formattedDate = latest ? formatDate(new Date(latest.date)) : "";

        const cardItem = document.createElement("button");
        cardItem.type = "button";
        cardItem.className = "oracle-revealed-card";

        const figure = document.createElement("div");
        figure.className = "oracle-revealed-figure";
        const image = document.createElement("img");
        image.src = getCardImage(cardId);
        image.alt = card?.name || "Carta revelada";
        figure.appendChild(image);

        const body = document.createElement("div");
        body.className = "oracle-revealed-body";
        const title = document.createElement("strong");
        title.textContent = card?.name || "Carta revelada";
        const paragraph = document.createElement("p");
        paragraph.textContent = summarizeEntry(latest);
        body.appendChild(title);
        body.appendChild(paragraph);
        if (formattedDate) {
          const dateLabel = document.createElement("span");
          dateLabel.textContent = `Respuesta del ${formattedDate}`;
          body.appendChild(dateLabel);
        }

        cardItem.appendChild(figure);
        cardItem.appendChild(body);
        cardItem.addEventListener("click", () => openOracleModal(cardId));
        oracleRevealed.appendChild(cardItem);
      });
    };

    const renderHistory = (cardId) => {
      const { visible: entries, total: totalEntries, sourceType } = getCardHistoryForDisplay(cardId);
      oracleHistoryList.innerHTML = "";

      if (!entries.length) {
        oracleHistory.style.display = "none";
        if (oracleHistoryNote) {
          oracleHistoryNote.textContent = "";
        }
        return;
      }

      oracleHistory.style.display = "block";
      if (oracleHistoryNote) {
        if (sourceType === "year") {
          const hiddenCount = Math.max(0, totalEntries - entries.length);
          oracleHistoryNote.textContent = hiddenCount > 0
            ? `Mostrando ${entries.length} respuestas (públicas o privadas) del último año. ${hiddenCount} registros más no se muestran aquí.`
            : "Mostrando hasta 4 respuestas (públicas o privadas) del último año.";
        } else {
          oracleHistoryNote.textContent =
            "No hay respuestas del último año. Mostrando hasta 4 respuestas previas registradas.";
        }
      }

      entries.forEach((entry) => {
        const item = document.createElement("div");
        item.className = "oracle-history-item";
        const isPastCycle = Number(entry.cycle) < Number(oracleState.cycle);

        const head = document.createElement("div");
        head.className = "oracle-history-head";
        const label = document.createElement("span");
        label.textContent = entry.type === "public"
          ? "Respuesta pública"
          : entry.type === "secret"
            ? "Respuesta secreta"
            : "Respuesta";
        const dateText = document.createElement("span");
        dateText.textContent = formatDate(new Date(entry.date));
        head.appendChild(label);
        head.appendChild(dateText);
        item.appendChild(head);

        const body = document.createElement("p");
        if (entry.type === "secret") {
          body.textContent = "Contenido secreto cifrado. Para visualizarlo debes digitar tu clave privada personal.";
          item.appendChild(body);
        } else {
          body.textContent = entry.text || "";
          item.appendChild(body);
        }

        const actions = document.createElement("div");
        actions.className = "oracle-history-item-actions";

        if (entry.type === "secret" && entry.id > 0) {
          const button = document.createElement("button");
          button.type = "button";
          button.className = "btn btn-outline btn-compact oracle-secret-history-btn";
          button.dataset.entryId = `${entry.id}`;
          button.textContent = "Visualizar respuesta secreta";
          actions.appendChild(button);
        }

        if (isPastCycle && entry.id > 0) {
          const deleteButton = document.createElement("button");
          deleteButton.type = "button";
          deleteButton.className = "oracle-history-delete-btn";
          deleteButton.dataset.entryId = `${entry.id}`;
          deleteButton.title = "Borrar respuesta de forma permanente";
          deleteButton.innerHTML = '<img src="/css/icons/icondelete.webp" alt="Borrar respuesta" />';
          actions.appendChild(deleteButton);
        }

        if (actions.childElementCount > 0) {
          item.appendChild(actions);
        }

        oracleHistoryList.appendChild(item);
      });
    };

    const closeModal = () => {
      oracleModalOverlay.classList.add("hidden");
      oracleModalOverlay.setAttribute("aria-hidden", "true");
      oracleConfirm.classList.add("hidden");
      resetPrivatePasswordUi();
      resetSecretUnlockUi();
      if (oracleSecretActions) {
        oracleSecretActions.classList.add("hidden");
      }
      if (oracleRevealSecretBtn) {
        delete oracleRevealSecretBtn.dataset.entryId;
      }
      pendingAction = null;
      pendingDeleteEntryId = null;
      selectedCard = null;
    };

    const openOracleModal = (cardId) => {
      selectedCard = oracleCards.find((card) => card.id === cardId);
      if (!selectedCard) return;

      if (!isViewingOwnProfile) {
        const entries = getCardHistory(cardId);
        const latest = entries[0];
        oracleCardName.textContent = selectedCard.name;
        oracleCardQuestion.textContent = selectedCard.question;
        oracleCardImage.src = getCardImage(selectedCard.id);
        oracleCardContext.textContent = selectedCard.context;

        oracleCardResponse.disabled = true;
        oracleCardResponse.placeholder = "Sin respuesta pública.";
        oracleCardResponse.value = latest?.text || "";
        oracleActionRow.style.display = "none";
        oracleConfirm.classList.add("hidden");
        resetPrivatePasswordUi();
        resetSecretUnlockUi();
        pendingDeleteEntryId = null;
        pendingAction = null;
        if (oracleSecretActions) oracleSecretActions.classList.add("hidden");

        oracleModalNote.textContent = latest?.date
          ? `Respuesta pública registrada el ${formatDate(new Date(latest.date))}.`
          : "Esta carta no tiene respuesta pública.";

        updateWordCounter();
        renderHistory(cardId);
        oracleModalOverlay.classList.remove("hidden");
        oracleModalOverlay.setAttribute("aria-hidden", "false");
        return;
      }

      const currentEntries = getCurrentCycleEntries(cardId);
      const answeredEntry = currentEntries.find((entry) => entry.type === "public" || entry.type === "secret");
      const hasAnswered = Boolean(answeredEntry);
      const hasHeart = currentEntries.some((entry) => entry.type === "heart");

      oracleCardName.textContent = selectedCard.name;
      oracleCardQuestion.textContent = selectedCard.question;
      oracleCardImage.src = getCardImage(selectedCard.id);
      oracleCardContext.textContent = selectedCard.context;

      oracleCardResponse.disabled = hasAnswered;
      oracleCardResponse.placeholder = "Escribe tu respuesta...";
      oracleCardResponse.value = "";
      oracleConfirm.classList.add("hidden");
      resetPrivatePasswordUi();
      resetSecretUnlockUi();
      pendingDeleteEntryId = null;
      pendingAction = null;
      if (oracleSecretActions) oracleSecretActions.classList.add("hidden");

      if (hasAnswered) {
        oracleActionRow.style.display = "none";
        if (answeredEntry?.type === "secret") {
          oracleModalNote.textContent = answeredEntry?.date
            ? `Respuesta secreta registrada el ${formatDate(new Date(answeredEntry.date))}. Para verla debes digitar tu clave privada.`
            : "Respuesta secreta registrada. Para verla debes digitar tu clave privada.";
          oracleCardResponse.placeholder = "Respuesta secreta cifrada en tu vault.";
          if (oracleSecretActions && oracleRevealSecretBtn && answeredEntry?.id > 0) {
            oracleRevealSecretBtn.dataset.entryId = `${answeredEntry.id}`;
            oracleSecretActions.classList.remove("hidden");
          }
        } else {
          oracleCardResponse.value = answeredEntry?.text || "";
          oracleModalNote.textContent = answeredEntry?.date
            ? `Respuesta registrada el ${formatDate(new Date(answeredEntry.date))}. Este texto es inmodificable.`
            : "Respuesta registrada. Este texto es inmodificable.";
        }
      } else {
        oracleActionRow.style.display = "flex";
        oracleModalNote.textContent = hasHeart
          ? "Esta carta quedó reposando en tu corazón. Puedes responder cuando lo desees durante este ciclo."
          : "Puedes responder ahora, en secreto o dejar la pregunta reposando en tu corazón.";
      }

      updateWordCounter();
      renderHistory(cardId);
      oracleModalOverlay.classList.remove("hidden");
      oracleModalOverlay.setAttribute("aria-hidden", "false");
    };

    const triggerConfirm = (action) => {
      pendingAction = action;
      pendingDeleteEntryId = null;
      resetSecretUnlockUi();
      if (action === "public") {
        oracleConfirmText.textContent = "¿Estás seguro de tu respuesta pública?";
        resetPrivatePasswordUi();
      } else if (action === "secret") {
        oracleConfirmText.textContent =
          "¿Estás seguro de tu respuesta secreta? Deberás digitar tu clave privada para cifrarla.";
        showPrivatePasswordUi();
      } else {
        oracleConfirmText.textContent =
          "¿Deseas dejar esta pregunta reposando en tu corazón?";
        resetPrivatePasswordUi();
      }
      oracleConfirm.classList.remove("hidden");
    };

    const extractSecretText = (raw) => {
      try {
        const parsed = JSON.parse(raw);
        if (parsed && typeof parsed === "object") {
          return String(parsed.text || parsed.response || "");
        }
      } catch {
        // No-op: if payload is not JSON, fallback to plaintext body.
      }
      return String(raw || "");
    };

    const revealSecretEntry = async (entryId, privatePassword, { renderIntoTextarea = true } = {}) => {
      const id = Number(entryId || 0);
      const entry = oracleEntriesById.get(id);
      if (!entry || entry.type !== "secret") {
        throw new Error("No se encontró la respuesta secreta.");
      }

      if (!String(privatePassword || "").trim()) {
        throw new Error("Debes digitar tu clave privada personal.");
      }

      const dekKey = await decryptDekFromPassword(String(privatePassword));
      const plaintext = await aesGcmDecryptText(
        dekKey,
        entry.ciphertextHex,
        entry.nonceHex,
        buildOracleAad(entry.cardId, entry.cycle)
      );
      const secretText = extractSecretText(plaintext);

      if (renderIntoTextarea) {
        oracleCardResponse.value = secretText;
        updateWordCounter();
        oracleModalNote.textContent = "Respuesta secreta descifrada localmente en tu navegador.";
      } else {
        window.alert(secretText || "La respuesta secreta está vacía.");
      }
    };

    const triggerDeleteHistoryConfirm = (entryId) => {
      const id = Number(entryId || 0);
      if (!Number.isFinite(id) || id <= 0) return;
      pendingDeleteEntryId = id;
      pendingAction = "delete_history";
      resetPrivatePasswordUi();
      resetSecretUnlockUi();
      oracleConfirmText.textContent =
        "Vas a borrar esta respuesta de forma permanente. Una vez elimines este recuerdo, no volverás a visualizarlo. ¿Deseas continuar?";
      oracleConfirm.classList.remove("hidden");
    };

    const submitOracleResponse = async (payload) => {
      const res = await apiFetch("/oracle/respond", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo registrar la respuesta del Oráculo.");
      }
      oracleState = normalizeOracleState(data);
    };

    const deleteOracleResponse = async (entryId) => {
      const responseId = Number(entryId || 0);
      if (!Number.isFinite(responseId) || responseId <= 0) {
        throw new Error("Respuesta inválida para borrar.");
      }

      const res = await apiFetch(`/oracle/responses/${responseId}`, {
        method: "DELETE",
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo borrar la respuesta.");
      }
      oracleState = normalizeOracleState(data);
    };

    const finalizeResponse = async () => {
      if (!selectedCard || !pendingAction || isSubmitting) return;

      if (pendingAction === "delete_history") {
        const responseId = Number(pendingDeleteEntryId || 0);
        if (!Number.isFinite(responseId) || responseId <= 0) {
          oracleConfirm.classList.add("hidden");
          pendingAction = null;
          pendingDeleteEntryId = null;
          return;
        }

        isSubmitting = true;
        oracleConfirmYes.disabled = true;
        oracleConfirmNo.disabled = true;

        try {
          await deleteOracleResponse(responseId);
          oracleConfirm.classList.add("hidden");
          pendingAction = null;
          pendingDeleteEntryId = null;
          renderAll();
          openOracleModal(selectedCard.id);
        } catch (err) {
          oracleModalNote.textContent = err?.message || "No se pudo borrar la respuesta.";
        } finally {
          isSubmitting = false;
          oracleConfirmYes.disabled = false;
          oracleConfirmNo.disabled = false;
        }
        return;
      }

      const responseText = oracleCardResponse.value.trim();
      if (pendingAction !== "heart" && !responseText) {
        oracleModalNote.textContent = "Escribe una respuesta antes de confirmar esta acción.";
        updateWordCounter();
        return;
      }

      if (pendingAction !== "heart") {
        const words = countWords(responseText);
        updateWordCounter();
        if (words > MAX_RESPONSE_WORDS) {
          oracleModalNote.textContent = `Tu respuesta supera el máximo permitido de ${MAX_RESPONSE_WORDS} palabras.`;
          return;
        }
      } else {
        updateWordCounter();
      }

      const payload = {
        card_id: selectedCard.id,
        response_type: pendingAction,
      };

      let privatePassword = "";
      if (pendingAction === "secret") {
        privatePassword = String(oraclePrivatePasswordInput?.value || "");
        if (!privatePassword.trim()) {
          setPrivatePasswordError("Digita tu clave privada personal");
          oraclePrivatePasswordInput?.focus();
          return;
        }
        setPrivatePasswordError("");
      }

      isSubmitting = true;
      oracleConfirmYes.disabled = true;
      oracleConfirmNo.disabled = true;
      let completed = false;

      try {
        if (pendingAction === "public") {
          payload.text_public = responseText;
        } else if (pendingAction === "secret") {
          const dekKey = await decryptDekFromPassword(privatePassword);
          const encoded = JSON.stringify({ text: responseText });
          const encrypted = await aesGcmEncryptText(
            dekKey,
            encoded,
            buildOracleAad(selectedCard.id, oracleState.cycle)
          );

          payload.ciphertext_hex = bufToHex(encrypted.ciphertext);
          payload.nonce_hex = bufToHex(encrypted.nonce.buffer);
        }

        await submitOracleResponse(payload);
        completed = true;
        closeModal();
        renderAll();
      } catch (err) {
        const message = err?.message || "No se pudo registrar la respuesta.";
        if (pendingAction === "secret") {
          setPrivatePasswordError(message);
        } else {
          oracleModalNote.textContent = message;
        }
      } finally {
        isSubmitting = false;
        oracleConfirmYes.disabled = false;
        oracleConfirmNo.disabled = false;
        if (completed) {
          pendingAction = null;
          pendingDeleteEntryId = null;
        }
      }
    };

    const renderAll = () => {
      const shuffled = shuffleCards(oracleCards);
      const { cooldownActive, cycleComplete, remainingMs } = updateCooldownStatus();
      renderOracleDeck(shuffled, cooldownActive, cycleComplete, remainingMs);
      renderRevealed();
    };

    const loadOracleState = async () => {
      try {
        oracleStatus.textContent = "Cargando cartas...";
        const profileId = Number(activeProfileUserId);
        const endpoint =
          !isViewingOwnProfile && Number.isFinite(profileId) && profileId > 0
            ? `/oracle/public/${encodeURIComponent(String(profileId))}`
            : "/oracle/state";
        const res = await apiFetch(endpoint);
        const data = await parseResponseJson(res);
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo cargar el estado del Oráculo.");
        }
        oracleState = normalizeOracleState(data);
        renderAll();
      } catch (err) {
        oracleStatus.textContent = "No se pudo cargar el Oráculo";
        oracleCooldown.textContent = err?.message || "Inténtalo de nuevo.";
        if (!isViewingOwnProfile && oracleRevealedEmpty) {
          oracleRevealed.innerHTML = "";
          oracleRevealedEmpty.textContent = err?.message || "Este módulo es privado.";
          oracleRevealedEmpty.style.display = "block";
        }
      }
    };

    oraclePublishBtn.addEventListener("click", () => triggerConfirm("public"));
    oracleSecretBtn.addEventListener("click", () => triggerConfirm("secret"));
    oracleHeartBtn.addEventListener("click", () => triggerConfirm("heart"));

    oracleConfirmYes.addEventListener("click", () => void finalizeResponse());
    oracleConfirmNo.addEventListener("click", () => {
      oracleConfirm.classList.add("hidden");
      resetPrivatePasswordUi();
      pendingDeleteEntryId = null;
      pendingAction = null;
    });

    if (oraclePrivatePasswordInput) {
      oraclePrivatePasswordInput.addEventListener("input", () => setPrivatePasswordError(""));
      oraclePrivatePasswordInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          void finalizeResponse();
        }
      });
    }

    if (oracleCardResponse) {
      oracleCardResponse.addEventListener("input", () => {
        updateWordCounter();
      });
    }

    if (oracleRevealSecretBtn) {
      oracleRevealSecretBtn.addEventListener("click", () => {
        const entryId = Number(oracleRevealSecretBtn.dataset.entryId || 0);
        if (!entryId) return;
        openSecretUnlockUi(entryId);
      });
    }

    if (oracleHistoryList) {
      oracleHistoryList.addEventListener("click", (event) => {
        const target = event.target instanceof Element ? event.target : null;
        const secretTrigger = target ? target.closest(".oracle-secret-history-btn") : null;
        if (secretTrigger) {
          const entryId = Number(secretTrigger.dataset.entryId || 0);
          if (!entryId) return;
          openSecretUnlockUi(entryId);
          return;
        }

        const deleteTrigger = target ? target.closest(".oracle-history-delete-btn") : null;
        if (deleteTrigger) {
          const entryId = Number(deleteTrigger.dataset.entryId || 0);
          if (!entryId) return;
          triggerDeleteHistoryConfirm(entryId);
        }
      });
    }

    if (oracleSecretUnlockConfirm) {
      oracleSecretUnlockConfirm.addEventListener("click", async () => {
        const password = String(oracleSecretUnlockPassword?.value || "");
        if (!password.trim()) {
          setSecretUnlockError("Digita tu clave privada personal");
          oracleSecretUnlockPassword?.focus();
          return;
        }

        try {
          await revealSecretEntry(pendingSecretRevealEntryId, password, { renderIntoTextarea: true });
          resetSecretUnlockUi();
        } catch (err) {
          setSecretUnlockError(err?.message || "No se pudo descifrar la respuesta secreta.");
        }
      });
    }

    if (oracleSecretUnlockCancel) {
      oracleSecretUnlockCancel.addEventListener("click", () => {
        resetSecretUnlockUi();
      });
    }

    if (oracleSecretUnlockPassword) {
      oracleSecretUnlockPassword.addEventListener("input", () => setSecretUnlockError(""));
      oracleSecretUnlockPassword.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          oracleSecretUnlockConfirm?.click();
        }
      });
    }

    closeOracleModal.addEventListener("click", closeModal);
    oracleModalOverlay.addEventListener("click", (event) => {
      if (event.target === oracleModalOverlay) closeModal();
    });

    updateWordCounter();
    (async () => {
      try {
        await resolveProfileContext();
      } catch (error) {
        console.error(error);
      } finally {
        void loadOracleState();
      }
    })();
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Oráculo</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user oracle-background">
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
      <details class="topbar-dropdown" id="profileDropdown">
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

      <details class="topbar-dropdown" id="menuDropdown">
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

      <!-- =========================
       *  PORTADA / COVER
       *  ========================= -->
      <section class="cover" id="cover">
        <div class="cover-media" id="coverMedia">
          <img id="coverImg" class="cover-img" src="/assets/cover-default.jpg" alt="Portada" />

          <div class="cover-actions cover-actions-purpose">
            <details class="cover-menu">
              <summary class="icon-btn" id="btnChangeCover" title="Editar imagen de portada">
                Editar imagen de portada
              </summary>
              <div class="cover-menu-panel">
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

          <div class="purpose-stack purpose-stack-modern" aria-label="Deseos de propósito">
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
                  Deseo de propósito sin definir
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

      <div class="oracle-body">
        <!-- =========================
         *  NAV / LINKS
         *  ========================= -->
        <nav class="profile-nav" aria-label="Navegación de perfil">
          <a class="nav-pill" href="/home_user.html" title="Home" data-profile-module="home">Home</a>
          <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
            <span class="nav-icon">⭐</span>
            <span><strong>5.000.000</strong> estrellas</span>
          </a>
          <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
          <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
          <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
          <a class="nav-pill" href="/calendar.html" title="Calendario" data-profile-module="calendar">Calendario</a>
          <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
        <a class="nav-pill" href="/messages.html" title="Mensajes">Mensajes</a>
        </nav>

        <!-- =========================
         *  ORACULO
         *  ========================= -->
        <section class="oracle-shell" aria-label="Oráculo">
          <header class="oracle-head">
            <div>
              <h2 class="oracle-title">El Oráculo</h2>
              <p class="oracle-subtitle">
                Selecciona una carta para comprender tu presente. Solo una carta cada 3 días.
              </p>
            </div>
          </header>

          <section class="panel oracle-intro" aria-label="¿Qué es el Oráculo?">
            <div class="panel-head">
              <h3 class="panel-title">¿Qué es el Oráculo?</h3>
            </div>
            <p class="panel-text">
              El Oráculo es una herramienta de reflexión de Kiadez.com. Eliges una carta, no para adivinar tu futuro,
              sino para comprender tu presente. Actualmente el Oráculo está compuesto de 30 cartas y solo puedes
              seleccionar una sola cada 3 días. La carta te planteará una pregunta, que puedes responder inmediatamente
              o dejar reposando en tu corazón. Si eres juicioso y disciplinado, responderás la pregunta que te propone
              la carta hasta 4 veces a lo largo de un solo año. Eso te permitirá reconocer cuánto has progresado en el
              camino de conocerte a ti mismo.
            </p>
          </section>

          <section class="panel oracle-deck" aria-label="Cartas no reveladas">
            <div class="oracle-deck-head">
              <div>
                <h3>Cartas no reveladas</h3>
                <p class="oracle-status" id="oracleStatus">Selecciona una carta</p>
              </div>
              <div class="oracle-deck-note" id="oracleCooldown"></div>
            </div>
            <div class="oracle-grid" id="oracleDeck"></div>
            <div class="oracle-empty hidden" id="oracleDeckEmpty">
              En 3 días podrás elegir una nueva carta.
            </div>
          </section>

          <section class="panel oracle-revealed" aria-label="Cartas reveladas">
            <div class="panel-head">
              <h3 class="panel-title">Cartas reveladas</h3>
              <span class="panel-badge">Respuestas registradas</span>
            </div>
            <div class="oracle-revealed-grid" id="oracleRevealed"></div>
            <div class="oracle-empty" id="oracleRevealedEmpty">
              Aún no has revelado cartas. Cuando selecciones una, aparecerá aquí.
            </div>
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
            <li><a href="/downloadapp.html">Descarga la app</a></li>
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
              <li><a href="/?lang=pt">Português</a></li>
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

  <!-- =========================
   *  MODAL: CARTA SELECCIONADA
   *  ========================= -->
  <div class="modal-overlay hidden" id="oracleModalOverlay" aria-hidden="true">
    <div class="modal modal-wide oracle-modal" role="dialog" aria-modal="true" aria-label="Carta seleccionada">
      <div class="modal-head">
        <div>
          <h3 id="oracleCardName">Nombre de la carta</h3>
          <p class="oracle-card-question" id="oracleCardQuestion"></p>
        </div>
        <button class="modal-close" type="button" id="closeOracleModal">✕</button>
      </div>

      <div class="modal-body">
        <div class="oracle-modal-top">
          <div class="oracle-card-figure">
            <img id="oracleCardImage" src="/css/oracle/Oracle9.png" alt="Carta del Oráculo" />
          </div>
          <div class="oracle-card-context">
            <h4>Contexto</h4>
            <p id="oracleCardContext"></p>
          </div>
        </div>

        <textarea class="modal-textarea" id="oracleCardResponse" rows="6"
          placeholder="Escribe tu respuesta..."></textarea>
        <p class="oracle-word-counter" id="oracleWordCounter">0/500 palabras</p>
        <div class="oracle-modal-note" id="oracleModalNote"></div>
        <div class="oracle-action-row hidden" id="oracleSecretActions">
          <button class="btn btn-outline btn-compact" type="button" id="oracleRevealSecretBtn">
            Digitar clave privada para visualizar respuesta secreta
          </button>
        </div>
        <div class="oracle-secret-unlock hidden" id="oracleSecretUnlock">
          <p class="oracle-secret-unlock-text">
            Digita tu clave privada personal para visualizar esta respuesta secreta.
          </p>
          <input
            class="oracle-private-password-input"
            id="oracleSecretUnlockPassword"
            type="password"
            placeholder="Digita tu clave privada personal"
            autocomplete="current-password"
          />
          <p class="oracle-private-password-error" id="oracleSecretUnlockError"></p>
          <div class="oracle-confirm-actions">
            <button class="btn btn-primary btn-compact" type="button" id="oracleSecretUnlockConfirm">
              Visualizar
            </button>
            <button class="btn btn-outline btn-compact" type="button" id="oracleSecretUnlockCancel">
              Cancelar
            </button>
          </div>
        </div>

        <div class="oracle-action-row" id="oracleActionRow">
          <button class="btn btn-primary btn-compact" type="button" id="oraclePublishBtn">Responder ahora y
            publicar</button>
          <button class="btn btn-outline btn-compact" type="button" id="oracleSecretBtn">Responder en secreto</button>
          <button class="btn btn-outline btn-compact" type="button" id="oracleHeartBtn">Dejar esta pregunta reposando
            en mi corazón</button>
        </div>

        <div class="oracle-confirm hidden" id="oracleConfirm">
          <p id="oracleConfirmText"></p>
          <div class="oracle-private-password hidden" id="oraclePrivatePasswordWrap">
            <input
              class="oracle-private-password-input"
              id="oraclePrivatePassword"
              type="password"
              placeholder="Digita tu clave privada personal"
              autocomplete="current-password"
            />
            <p class="oracle-private-password-error" id="oraclePrivatePasswordError"></p>
          </div>
          <div class="oracle-confirm-actions">
            <button class="btn btn-primary btn-compact" type="button" id="oracleConfirmYes">Sí</button>
            <button class="btn btn-outline btn-compact" type="button" id="oracleConfirmNo">No</button>
          </div>
        </div>

        <div class="oracle-history" id="oracleHistory">
          <h4>Respuestas anteriores</h4>
          <p class="oracle-history-note" id="oracleHistoryNote"></p>
          <div class="oracle-history-list" id="oracleHistoryList"></div>
        </div>
      </div>
    </div>
  </div>
