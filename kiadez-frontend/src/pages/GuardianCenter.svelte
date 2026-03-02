<script>
  import { onMount } from "svelte";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import GuardianMessagingCenter from "../lib/GuardianMessagingCenter.svelte";
  import { getLocale } from "../lib/i18n";
  import { logout } from "../lib/logout";

  const API = "http://127.0.0.1:8000";
  const GUARDIAN_REQUIRED_RANK = 3;
  const GUARDIAN_MAX_RANK = 8;
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

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
      window.location.href = "/login.html";
      throw new Error(tr("No hay sesión activa.", "No active session.", "Aucune session active."));
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    };
    const res = await fetch(`${API}${path}`, { ...options, headers });
    if (res.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login.html";
      throw new Error(tr("Sesión expirada.", "Session expired.", "Session expirée."));
    }
    return res;
  };

  let guardianRank = 0;
  let isGuardian = false;
  let isLoading = true;
  let loadError = "";

  let wishRequestsLoading = false;
  let wishRequestsError = "";
  let wishRequestsPage = 1;
  let wishRequestsTotalPages = 1;
  let wishRequestsItems = [];
  const WISH_REQUESTS_PAGE_SIZE = 10;
  let activeWishRequest = null;
  let actionError = "";
  let actionLoading = false;

  let reportedPostsLoading = false;
  let reportedPostsError = "";
  let reportedPostsPage = 1;
  let reportedPostsTotalPages = 1;
  let reportedPostsItems = [];
  const REPORTED_POSTS_PAGE_SIZE = 10;
  let activeReportedPost = null;
  let reportedPostsActionError = "";
  let reportedPostsActionLoading = false;
  let showDeleteReportedPostModal = false;
  let showKeepReportedPostModal = false;
  let reportedProfilesLoading = false;
  let reportedProfilesError = "";
  let reportedProfilesPage = 1;
  let reportedProfilesTotalPages = 1;
  let reportedProfilesItems = [];
  let activeReportedProfile = null;
  let reportedProfilesActionError = "";
  let reportedProfilesActionLoading = false;
  let showSuspendReportedProfileModal = false;
  let showEnableReportedProfileModal = false;
  let showCloseReportedProfileModal = false;
  const REPORTED_PROFILES_PAGE_SIZE = 10;

  let showSealCommitmentModal = false;
  let showDenyModal = false;
  let showOwnerMessageModal = false;

  let denyToHandle = "";
  let denySubject = "";
  let denyBody = "";
  let denySubjectError = false;
  let denyBodyError = false;

  let ownerMessageToHandle = "";
  let ownerMessageSubject = "";
  let ownerMessageBody = "";
  let ownerMessageSubjectError = false;
  let ownerMessageBodyError = false;

  let rankLookupQuery = "";
  let rankLookupLoading = false;
  let rankLookupError = "";
  let rankLookupResult = null;
  let showPromoteRankModal = false;
  let rankPromoteLoading = false;
  let rankPromoteError = "";

  const modules = [
    {
      key: "reported_posts",
      icon: "🚩",
      title: tr("Publicaciones denunciadas", "Reported posts", "Publications signalées"),
      note: tr("Revisar reportes y tomar acciones.", "Review reports and take actions.", "Examiner les signalements et agir."),
    },
    {
      key: "reported_profiles",
      icon: "🧾",
      title: tr("Perfiles denunciados", "Reported profiles", "Profils signalés"),
      note: tr("Validar perfiles y resolver apelaciones.", "Validate profiles and resolve appeals.", "Valider les profils et résoudre les appels."),
    },
    {
      key: "wish_management",
      icon: "🪄",
      title: tr("Gestión de deseos", "Wish management", "Gestion des souhaits"),
      note: tr("Solicitudes: “Yo puedo cumplir este deseo”.", "Requests: “I can fulfill this wish.”", "Demandes : « Je peux accomplir ce souhait. »"),
    },
    {
      key: "rank_management",
      icon: "🛡️",
      title: tr("Gestión de rangos", "Rank management", "Gestion des rangs"),
      note: tr("Buscar por @id y subir nivel de Guardián sin saltos.", "Search by @id and promote Guardian rank without skipping levels.", "Rechercher par @id et promouvoir le rang de Gardien sans sauter de niveau."),
    },
    {
      key: "messaging",
      icon: "💬",
      title: tr("Mensajería", "Messaging", "Messagerie"),
      note: tr("Conversaciones y coordinación con usuarios.", "Conversations and coordination with users.", "Conversations et coordination avec les utilisateurs."),
    },
  ];

  let activeModuleKey = modules[0].key;

  const setActiveModule = (key) => {
    activeModuleKey = String(key || modules[0].key);
    if (activeModuleKey === "wish_management" && isGuardian) {
      void loadWishRequests(1);
      return;
    }
    if (activeModuleKey === "reported_posts" && isGuardian) {
      void loadReportedPosts(1);
      return;
    }
    if (activeModuleKey === "reported_profiles" && isGuardian) {
      void loadReportedProfiles(1);
      return;
    }
    if (activeModuleKey === "rank_management" && isGuardian) {
      rankLookupError = "";
    }
  };

  const getActiveModule = () => modules.find((item) => item.key === activeModuleKey) || modules[0];

  const formatStatusLabel = (request) => {
    const value = String(request?.status || "").toLowerCase();
    if (value === "open") return tr("Abierta", "Open", "Ouvrir");
    if (value === "in_progress") return tr("Compromiso sellado", "Commitment sealed", "Engagement scellé");
    if (value === "closed") {
      return request?.denied_at ? tr("Denegada", "Denied", "Refusé") : tr("Deseo completado", "Wish completed", "Souhait accompli");
    }
    return value || tr("Desconocida", "Unknown", "Inconnu");
  };

  const formatDateTime = (value) => {
    try {
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return "";
      return date.toLocaleString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO");
    } catch {
      return "";
    }
  };

  const formatReportStatusLabel = (item) => {
    const value = String(item?.status || "").toLowerCase();
    if (value === "open") return tr("Pendiente", "Pending", "En attente");
    if (value === "kept") return tr("Conservada", "Kept", "Conservé");
    if (value === "deleted") return tr("Eliminada", "Deleted", "Supprimé");
    return value || tr("Desconocida", "Unknown", "Inconnu");
  };

  const formatReportReasonLabel = (reason, otherReason = "") => {
    const value = String(reason || "").toLowerCase();
    if (value === "violent") return tr("Contenido violento o perturbador", "Violent or disturbing content", "Contenu violent ou perturbant");
    if (value === "divisive") return tr("Promueve confrontación o división excesiva", "Promotes confrontation or excessive division", "Encourage la confrontation ou une division excessive");
    if (value === "sexual") return tr("Contenido sexual explícito o inapropiado", "Explicit or inappropriate sexual content", "Contenu sexuel explicite ou inapproprié");
    if (value === "other") {
      const note = String(otherReason || "").trim();
      return note ? tr(`Otra razón: ${note}`, `Other reason: ${note}`, `Other reason: ${note}`) : tr("Otra razón", "Other reason", "Autre motif");
    }
    return value || tr("Razón no especificada", "Unspecified reason", "Raison non précisée");
  };

  const formatProfileReportStatusLabel = (item) => {
    const value = String(item?.status || "").toLowerCase();
    if (value === "open") return tr("Pendiente", "Pending", "En attente");
    if (value === "reviewed") return tr("Revisado", "Reviewed", "Révisé");
    return value || tr("Desconocida", "Unknown", "Inconnu");
  };

  const formatAccountModerationStatusLabel = (value) => {
    const status = String(value || "").toLowerCase();
    if (status === "suspended") return tr("Cuenta suspendida", "Account suspended", "Compte suspendu");
    if (status === "closed") return tr("Cuenta cerrada", "Account closed", "Compte fermé");
    return tr("Cuenta activa", "Active account", "Compte actif");
  };

  const formatProfileReportReasonLabel = (reason, otherReason = "") => {
    const value = String(reason || "").toLowerCase();
    if (value === "fake_or_illegal") return tr("Perfil falso o contenido ilegal", "Fake profile or illegal content", "Faux profil ou contenu illégal");
    if (value === "external_manipulation")
      return tr(
        "Manipulation toward other users in real life through external channels",
        "Manipulation of other users in real life through external means"
      );
    if (value === "star_manipulation") return tr("Abuso de publicaciones para atraer estrellas", "Post abuse to attract stars", "Abus de publication pour attirer des étoiles");
    if (value === "abusive_or_coercive") return tr("Conducta abusiva o coercitiva", "Abusive or coercive behavior", "Comportement abusif ou coercitif");
    if (value === "wish_system_abuse") return tr("Uso indebido del sistema de deseos", "Misuse of the wish system", "Mauvaise utilisation du système de souhaits");
    if (value === "safety_risk") return tr("Riesgo para la seguridad de otros", "Safety risk for others", "Risque de sécurité pour les autres");
    if (value === "other") {
      const note = String(otherReason || "").trim();
      return note ? tr(`Otro: ${note}`, `Other: ${note}`, `Other: ${note}`) : tr("Otro", "Other", "Autre");
    }
    return value || tr("Razón no especificada", "Unspecified reason", "Raison non précisée");
  };

  const toCensoredHandle = (userId) => {
    const id = Number(userId || 0);
    if (!Number.isFinite(id) || id <= 0) return "@id";
    return `@id${id}`;
  };

  const updateWishRequestItem = (updatedRequest) => {
    if (!updatedRequest || !updatedRequest.id) return;
    const targetId = Number(updatedRequest.id);
    wishRequestsItems = wishRequestsItems.map((item) =>
      Number(item?.id) === targetId ? { ...item, ...updatedRequest } : item
    );
  };

  const updateReportedPostItem = (updatedItem) => {
    if (!updatedItem || !updatedItem.id) return;
    const targetId = Number(updatedItem.id);
    reportedPostsItems = reportedPostsItems.map((item) =>
      Number(item?.id) === targetId ? { ...item, ...updatedItem } : item
    );
  };

  const closeSealCommitmentModal = () => {
    showSealCommitmentModal = false;
    activeWishRequest = null;
    actionError = "";
  };

  const closeDenyModal = () => {
    showDenyModal = false;
    activeWishRequest = null;
    actionError = "";
    denyToHandle = "";
    denySubject = "";
    denyBody = "";
    denySubjectError = false;
    denyBodyError = false;
  };

  const closeOwnerMessageModal = () => {
    showOwnerMessageModal = false;
    activeWishRequest = null;
    actionError = "";
    ownerMessageToHandle = "";
    ownerMessageSubject = "";
    ownerMessageBody = "";
    ownerMessageSubjectError = false;
    ownerMessageBodyError = false;
  };

  const closeDeleteReportedPostModal = () => {
    showDeleteReportedPostModal = false;
    activeReportedPost = null;
    reportedPostsActionError = "";
  };

  const closeKeepReportedPostModal = () => {
    showKeepReportedPostModal = false;
    activeReportedPost = null;
    reportedPostsActionError = "";
  };

  const closePromoteRankModal = () => {
    showPromoteRankModal = false;
    rankPromoteError = "";
  };

  const closeSuspendReportedProfileModal = () => {
    showSuspendReportedProfileModal = false;
    activeReportedProfile = null;
    reportedProfilesActionError = "";
  };

  const closeEnableReportedProfileModal = () => {
    showEnableReportedProfileModal = false;
    activeReportedProfile = null;
    reportedProfilesActionError = "";
  };

  const closeCloseReportedProfileModal = () => {
    showCloseReportedProfileModal = false;
    activeReportedProfile = null;
    reportedProfilesActionError = "";
  };

  const openPromoteRankModal = () => {
    if (!rankLookupResult?.can_promote || rankPromoteLoading) return;
    rankPromoteError = "";
    showPromoteRankModal = true;
  };

  const searchRankUser = async () => {
    const query = String(rankLookupQuery || "").trim();
    rankLookupError = "";
    rankLookupResult = null;
    if (!query) {
      rankLookupError = tr("Escribe un @id o @username para buscar.", "Type an @id or @username to search.", "Saisis un @id ou @username pour rechercher.");
      return;
    }

    rankLookupLoading = true;
    try {
      const res = await apiFetch(
        `/guardian-center/rank-management/user?query=${encodeURIComponent(query)}`
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo encontrar el usuario.", "Could not find the user.", "Impossible de trouver l'utilisateur."));
      }
      rankLookupResult = data || null;
      if (!rankLookupResult?.user_id) {
        throw new Error(tr("Respuesta inválida al cargar el usuario.", "Invalid response while loading the user.", "Réponse invalide lors du chargement de l'utilisateur."));
      }
    } catch (err) {
      rankLookupError = err?.message || tr("No se pudo encontrar el usuario.", "Could not find the user.", "Impossible de trouver l'utilisateur.");
      rankLookupResult = null;
    } finally {
      rankLookupLoading = false;
    }
  };

  const promoteRankUser = async () => {
    const targetUserId = Number(rankLookupResult?.user_id || 0);
    if (!Number.isFinite(targetUserId) || targetUserId <= 0) return;
    if (!rankLookupResult?.can_promote || rankPromoteLoading) return;

    rankPromoteLoading = true;
    rankPromoteError = "";
    try {
      const res = await apiFetch(
        `/guardian-center/rank-management/users/${encodeURIComponent(String(targetUserId))}/promote`,
        { method: "POST" }
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo promover el rango.", "Could not promote the rank.", "Impossible de promouvoir le rang."));
      }

      const updatedTarget = data?.target || null;
      if (!updatedTarget?.user_id) {
        throw new Error(tr("Respuesta inválida al promover el usuario.", "Invalid response while promoting the user.", "Réponse invalide lors de la promotion de l'utilisateur."));
      }
      rankLookupResult = updatedTarget;
      if (updatedTarget.is_self) {
        guardianRank = Number(updatedTarget.guardian_rank || guardianRank) || guardianRank;
      }
      closePromoteRankModal();
    } catch (err) {
      rankPromoteError = err?.message || tr("No se pudo promover el rango.", "Could not promote the rank.", "Impossible de promouvoir le rang.");
    } finally {
      rankPromoteLoading = false;
    }
  };

  const openSealCommitmentModal = (req) => {
    activeWishRequest = req || null;
    actionError = "";
    showSealCommitmentModal = true;
  };

  const openDenyModal = (req) => {
    activeWishRequest = req || null;
    actionError = "";
    denyToHandle = toCensoredHandle(req?.requester?.user_id);
    denySubject = "";
    denyBody = "";
    denySubjectError = false;
    denyBodyError = false;
    showDenyModal = true;
  };

  const openOwnerMessageModal = (req) => {
    activeWishRequest = req || null;
    actionError = "";
    ownerMessageToHandle = toCensoredHandle(req?.wish_owner?.user_id);
    ownerMessageSubject = tr(
      "Prior confirmation before freezing your wish",
      "Prior confirmation before freezing your wish"
    );
    ownerMessageBody =
      tr(
        "There is someone interested in fulfilling this wish. Before freezing it and continuing Kiadez internal process, I need to confirm with you whether someone close is already managing it outside the social network.",
        "Someone is interested in fulfilling this wish. Before freezing it and continuing Kiadez's internal process, I need to confirm with you whether someone close to you is already handling it outside the social network."
      );
    ownerMessageSubjectError = false;
    ownerMessageBodyError = false;
    showOwnerMessageModal = true;
  };

  const openDeleteReportedPostModal = (item) => {
    activeReportedPost = item || null;
    reportedPostsActionError = "";
    showDeleteReportedPostModal = true;
  };

  const openKeepReportedPostModal = (item) => {
    activeReportedPost = item || null;
    reportedPostsActionError = "";
    showKeepReportedPostModal = true;
  };

  const openSuspendReportedProfileModal = (item) => {
    if (reportedProfilesActionLoading) return;
    activeReportedProfile = item || null;
    reportedProfilesActionError = "";
    showSuspendReportedProfileModal = true;
  };

  const openEnableReportedProfileModal = (item) => {
    if (reportedProfilesActionLoading) return;
    activeReportedProfile = item || null;
    reportedProfilesActionError = "";
    showEnableReportedProfileModal = true;
  };

  const openCloseReportedProfileModal = (item) => {
    if (reportedProfilesActionLoading) return;
    activeReportedProfile = item || null;
    reportedProfilesActionError = "";
    showCloseReportedProfileModal = true;
  };

  const loadWishRequests = async (page = 1) => {
    wishRequestsLoading = true;
    wishRequestsError = "";
    const requestedPage = Math.max(1, Number(page || 1));

    try {
      const res = await apiFetch(
        `/guardian-center/wish-requests?page=${encodeURIComponent(String(requestedPage))}&page_size=${encodeURIComponent(String(WISH_REQUESTS_PAGE_SIZE))}`
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudieron cargar las solicitudes.", "Could not load requests.", "Impossible de charger les demandes."));
      }
      wishRequestsItems = Array.isArray(data?.items) ? data.items : [];
      wishRequestsTotalPages = Math.max(1, Number(data?.total_pages || 1));
      wishRequestsPage = Math.max(1, Math.min(Number(data?.page || requestedPage), wishRequestsTotalPages));
    } catch (err) {
      wishRequestsError = err?.message || tr("No se pudieron cargar las solicitudes.", "Could not load requests.", "Impossible de charger les demandes.");
      wishRequestsItems = [];
      wishRequestsPage = 1;
      wishRequestsTotalPages = 1;
    } finally {
      wishRequestsLoading = false;
    }
  };

  const loadReportedPosts = async (page = 1) => {
    reportedPostsLoading = true;
    reportedPostsError = "";
    const requestedPage = Math.max(1, Number(page || 1));

    try {
      const res = await apiFetch(
        `/guardian-center/reported-posts?page=${encodeURIComponent(String(requestedPage))}&page_size=${encodeURIComponent(String(REPORTED_POSTS_PAGE_SIZE))}`
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudieron cargar las publicaciones denunciadas.", "Could not load reported posts.", "Impossible de charger les publications signalées."));
      }
      reportedPostsItems = Array.isArray(data?.items) ? data.items : [];
      reportedPostsTotalPages = Math.max(1, Number(data?.total_pages || 1));
      reportedPostsPage = Math.max(1, Math.min(Number(data?.page || requestedPage), reportedPostsTotalPages));
    } catch (err) {
      reportedPostsError = err?.message || tr("No se pudieron cargar las publicaciones denunciadas.", "Could not load reported posts.", "Impossible de charger les publications signalées.");
      reportedPostsItems = [];
      reportedPostsPage = 1;
      reportedPostsTotalPages = 1;
    } finally {
      reportedPostsLoading = false;
    }
  };

  const normalizeReportedProfileItem = (item) => ({
    ...(item || {}),
    reported_posts_loading: false,
    reported_posts_error: "",
  });

  const updateReportedProfileItem = (updatedItem) => {
    if (!updatedItem || !updatedItem.id) return;
    const targetId = Number(updatedItem.id);
    reportedProfilesItems = reportedProfilesItems.map((item) =>
      Number(item?.id) === targetId
        ? {
            ...normalizeReportedProfileItem(item),
            ...normalizeReportedProfileItem(updatedItem),
          }
        : item
    );
  };

  const loadReportedProfiles = async (page = 1) => {
    reportedProfilesLoading = true;
    reportedProfilesError = "";
    const requestedPage = Math.max(1, Number(page || 1));

    try {
      const res = await apiFetch(
        `/guardian-center/reported-profiles?page=${encodeURIComponent(String(requestedPage))}&page_size=${encodeURIComponent(String(REPORTED_PROFILES_PAGE_SIZE))}`
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudieron cargar los perfiles denunciados.", "Could not load reported profiles.", "Impossible de charger les profils signalés."));
      }
      const nextItems = Array.isArray(data?.items) ? data.items : [];
      reportedProfilesItems = nextItems.map((item) => normalizeReportedProfileItem(item));
      reportedProfilesTotalPages = Math.max(1, Number(data?.total_pages || 1));
      reportedProfilesPage = Math.max(1, Math.min(Number(data?.page || requestedPage), reportedProfilesTotalPages));
    } catch (err) {
      reportedProfilesError = err?.message || tr("No se pudieron cargar los perfiles denunciados.", "Could not load reported profiles.", "Impossible de charger les profils signalés.");
      reportedProfilesItems = [];
      reportedProfilesPage = 1;
      reportedProfilesTotalPages = 1;
    } finally {
      reportedProfilesLoading = false;
    }
  };

  const loadReportedProfilePostsPage = async (caseId, page = 1) => {
    const targetCaseId = Number(caseId || 0);
    if (!Number.isFinite(targetCaseId) || targetCaseId <= 0) return;
    const requestedPage = Math.max(1, Number(page || 1));

    reportedProfilesItems = reportedProfilesItems.map((item) =>
      Number(item?.id) === targetCaseId
        ? { ...item, reported_posts_loading: true, reported_posts_error: "" }
        : item
    );

    try {
      const res = await apiFetch(
        `/guardian-center/reported-profiles/${encodeURIComponent(String(targetCaseId))}/reported-posts?page=${encodeURIComponent(String(requestedPage))}&page_size=10`
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(
          data.detail || tr("No se pudieron cargar las publicaciones denunciadas de este perfil.", "Could not load reported posts for this profile.", "Impossible de charger les publications signalées pour ce profil.")
        );
      }
      const normalizedPosts = {
        items: Array.isArray(data?.items) ? data.items : [],
        page: Math.max(1, Number(data?.page || requestedPage)),
        page_size: Math.max(1, Number(data?.page_size || 10)),
        total: Math.max(0, Number(data?.total || 0)),
        total_pages: Math.max(1, Number(data?.total_pages || 1)),
        range_start: Math.max(0, Number(data?.range_start || 0)),
        range_end: Math.max(0, Number(data?.range_end || 0)),
      };

      reportedProfilesItems = reportedProfilesItems.map((item) =>
        Number(item?.id) === targetCaseId
          ? {
              ...item,
              reported_posts: normalizedPosts,
              reported_posts_loading: false,
              reported_posts_error: "",
            }
          : item
      );
    } catch (err) {
      reportedProfilesItems = reportedProfilesItems.map((item) =>
        Number(item?.id) === targetCaseId
          ? {
              ...item,
              reported_posts_loading: false,
              reported_posts_error:
                err?.message || tr("No se pudieron cargar las publicaciones denunciadas de este perfil.", "Could not load reported posts for this profile.", "Impossible de charger les publications signalées pour ce profil."),
            }
          : item
      );
    }
  };

  const sealCommitment = async () => {
    if (!activeWishRequest?.id || actionLoading) return;
    actionLoading = true;
    actionError = "";
    try {
      const res = await apiFetch(`/guardian-center/wish-requests/${encodeURIComponent(String(activeWishRequest.id))}/seal-commitment`, {
        method: "POST",
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo sellar el compromiso.", "Could not seal the commitment.", "Impossible de sceller l'engagement."));
      }
      updateWishRequestItem(data);
      closeSealCommitmentModal();
    } catch (err) {
      actionError = err?.message || tr("No se pudo sellar el compromiso.", "Could not seal the commitment.", "Impossible de sceller l'engagement.");
    } finally {
      actionLoading = false;
    }
  };

  const denyRequest = async () => {
    if (!activeWishRequest?.id || actionLoading) return;

    denySubjectError = !String(denySubject || "").trim();
    denyBodyError = !String(denyBody || "").trim();
    if (denySubjectError || denyBodyError) {
      actionError = tr("Debes completar asunto y mensaje para denegar la petición.", "You must complete subject and message to deny the request.", "Tu dois complete subject and message to deny the request.");
      return;
    }

    actionLoading = true;
    actionError = "";
    try {
      const res = await apiFetch(`/guardian-center/wish-requests/${encodeURIComponent(String(activeWishRequest.id))}/deny`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          subject: String(denySubject || "").trim(),
          body: String(denyBody || "").trim(),
        }),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo denegar la petición.", "Could not deny the request.", "Impossible de refuser la demande."));
      }
      updateWishRequestItem(data);
      closeDenyModal();
    } catch (err) {
      actionError = err?.message || tr("No se pudo denegar la petición.", "Could not deny the request.", "Impossible de refuser la demande.");
    } finally {
      actionLoading = false;
    }
  };

  const sendOwnerMessage = async () => {
    if (!activeWishRequest?.id || actionLoading) return;

    ownerMessageSubjectError = !String(ownerMessageSubject || "").trim();
    ownerMessageBodyError = !String(ownerMessageBody || "").trim();
    if (ownerMessageSubjectError || ownerMessageBodyError) {
      actionError = tr(
        "You must complete subject and message to send the notification.",
        "You must complete subject and message to send the notification."
      );
      return;
    }

    actionLoading = true;
    actionError = "";
    try {
      const res = await apiFetch(
        `/guardian-center/wish-requests/${encodeURIComponent(String(activeWishRequest.id))}/message-owner`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            subject: String(ownerMessageSubject || "").trim(),
            body: String(ownerMessageBody || "").trim(),
          }),
        }
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo enviar el mensaje.", "Could not send the message.", "Impossible d'envoyer le message."));
      }
      window.alert(
        tr(
          `Mensaje enviado a ${data?.recipient_handle || ownerMessageToHandle}.`,
          `Message sent to ${data?.recipient_handle || ownerMessageToHandle}.`
        )
      );
      closeOwnerMessageModal();
    } catch (err) {
      actionError = err?.message || tr("No se pudo enviar el mensaje.", "Could not send the message.", "Impossible d'envoyer le message.");
    } finally {
      actionLoading = false;
    }
  };

  const deleteReportedPost = async () => {
    if (!activeReportedPost?.id || reportedPostsActionLoading) return;
    reportedPostsActionLoading = true;
    reportedPostsActionError = "";
    try {
      const res = await apiFetch(
        `/guardian-center/reported-posts/${encodeURIComponent(String(activeReportedPost.id))}/delete-post`,
        { method: "POST" }
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo eliminar la publicación denunciada.", "Could not delete the reported post.", "Impossible de supprimer la publication signalée."));
      }
      updateReportedPostItem(data);
      closeDeleteReportedPostModal();
    } catch (err) {
      reportedPostsActionError = err?.message || tr("No se pudo eliminar la publicación denunciada.", "Could not delete the reported post.", "Impossible de supprimer la publication signalée.");
    } finally {
      reportedPostsActionLoading = false;
    }
  };

  const keepReportedPost = async () => {
    if (!activeReportedPost?.id || reportedPostsActionLoading) return;
    reportedPostsActionLoading = true;
    reportedPostsActionError = "";
    try {
      const res = await apiFetch(
        `/guardian-center/reported-posts/${encodeURIComponent(String(activeReportedPost.id))}/keep-post`,
        { method: "POST" }
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo conservar la publicación reportada.", "Could not keep the reported post.", "Impossible de conserver la publication signalée."));
      }
      updateReportedPostItem(data);
      closeKeepReportedPostModal();
    } catch (err) {
      reportedPostsActionError = err?.message || tr("No se pudo conservar la publicación reportada.", "Could not keep the reported post.", "Impossible de conserver la publication signalée.");
    } finally {
      reportedPostsActionLoading = false;
    }
  };

  const runReportedProfileAccountAction = async (actionSuffix, fallbackError) => {
    if (!activeReportedProfile?.id || reportedProfilesActionLoading) return;
    const caseId = Number(activeReportedProfile.id || 0);
    if (!Number.isFinite(caseId) || caseId <= 0) return;

    reportedProfilesActionLoading = true;
    reportedProfilesActionError = "";
    try {
      const res = await apiFetch(
        `/guardian-center/reported-profiles/${encodeURIComponent(String(caseId))}/${actionSuffix}`,
        { method: "POST" }
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || fallbackError);
      }
      updateReportedProfileItem(data);
      closeSuspendReportedProfileModal();
      closeEnableReportedProfileModal();
      closeCloseReportedProfileModal();
    } catch (err) {
      reportedProfilesActionError = err?.message || fallbackError;
    } finally {
      reportedProfilesActionLoading = false;
    }
  };

  const suspendReportedProfileAccount = async () =>
    runReportedProfileAccountAction("suspend-account", tr("No se pudo suspender la cuenta.", "Could not suspend the account.", "Impossible de suspend the account."));

  const enableReportedProfileAccount = async () =>
    runReportedProfileAccountAction("enable-account", tr("No se pudo habilitar la cuenta.", "Could not enable the account.", "Impossible de enable the account."));

  const closeReportedProfileAccount = async () =>
    runReportedProfileAccountAction("close-account", tr("No se pudo cerrar la cuenta.", "Could not close the account.", "Impossible de close the account."));

  onMount(() => {
    document.body.dataset.visitor = "false";
    const pollingMs = 15000;
    const poller = window.setInterval(() => {
      if (!isGuardian || isLoading) return;
      if (activeModuleKey === "reported_posts") {
        if (reportedPostsLoading || reportedPostsActionLoading) return;
        void loadReportedPosts(reportedPostsPage);
        return;
      }
      if (activeModuleKey === "reported_profiles") {
        if (reportedProfilesLoading) return;
        void loadReportedProfiles(reportedProfilesPage);
      }
    }, pollingMs);

    (async () => {
      isLoading = true;
      loadError = "";
      guardianRank = 0;
      isGuardian = false;
      try {
        const res = await apiFetch("/auth/me");
        const data = await parseResponseJson(res);
        if (!res.ok) {
          throw new Error(data.detail || tr("No se pudo cargar tu perfil.", "Could not load your profile.", "Impossible de charger ton profil."));
        }
        guardianRank = Number(data?.guardian_rank || 0) || 0;
        isGuardian = guardianRank >= GUARDIAN_REQUIRED_RANK;
        if (isGuardian) {
          if (activeModuleKey === "reported_posts") {
            await loadReportedPosts(1);
          } else if (activeModuleKey === "reported_profiles") {
            await loadReportedProfiles(1);
          } else if (activeModuleKey === "wish_management") {
            await loadWishRequests(1);
          }
        }
      } catch (err) {
        loadError = err?.message || tr("No se pudo cargar el Centro del Guardián.", "Could not load the Guardian Center.", "Impossible de load the Guardian Center.");
      } finally {
        isLoading = false;
      }
    })();

    return () => {
      window.clearInterval(poller);
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{tr("Kiadez — Centro del Guardián", "Kiadez — Guardian Center", "Kiadez — Centre des Gardiens")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background settings-page guardian-center-page">
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input type="search" placeholder={tr("Buscar en Kiadez", "Search in Kiadez", "Rechercher dans Kiadez")} aria-label={tr("Buscar", "Search", "Rechercher")} />
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
      <details class="topbar-dropdown" id="profileDropdown">
        <summary class="topbar-avatar-btn" aria-label={tr("Perfil del usuario", "User profile", "Profil utilisateur")}>
          <img src="/assets/avatar-default.jpg" alt={tr("Perfil de usuario", "User profile", "Profil utilisateur")} />
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

      <details class="topbar-dropdown" id="menuDropdown">
        <summary class="topbar-menu-btn" aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}>
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">{tr("Menú", "Menu", "Navigation")}</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem">{tr("Mi Home", "My Home", "Mon accueil")}</a>
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
    <div class="home-body settings-body guardian-center-body">
      <section class="panel guardian-center-panel" aria-label={tr("Centro del Guardián", "Guardian Center", "Centre des Gardiens")}>
        <div class="panel-head guardian-center-head">
          <div>
            <h2 class="panel-title">{tr("Centro del Guardián", "Guardian Center", "Centre des Gardiens")}</h2>
            <p class="panel-muted guardian-center-subtitle">
              {tr(
                "Authority scenario for Guardians. Reports, requests, and coordination are managed here.",
                "Authority workspace for Guardians. Reports, requests, and coordination are managed here."
              )}
            </p>
          </div>
          <span class="panel-badge">
            {#if isLoading}
              {tr("Cargando...", "Loading...", "Chargement...")}
            {:else if isGuardian}
              {tr("Guardián · Rango", "Guardian · Rank", "Gardien · Rang")} {guardianRank}
            {:else}
              {tr("Acceso restringido", "Restricted access", "Accès restreint")}
            {/if}
          </span>
        </div>

        {#if loadError}
          <div class="guardian-center-empty is-error">{loadError}</div>
        {:else if isLoading}
          <div class="guardian-center-empty">{tr("Cargando tu autorización...", "Loading your authorization...", "Chargement de ton autorisation...")}</div>
        {:else if !isGuardian}
          <div class="guardian-center-lock">
            <p class="guardian-center-lock-text">
              {tr(
                "This module is available only for users with Guardian rank (Rank",
                "This module is available only for users with Guardian rank (Rank"
              )} {GUARDIAN_REQUIRED_RANK}).
            </p>
            <div class="guardian-center-lock-actions">
              <a class="btn btn-outline btn-compact" href="/guardians-rank.html">{tr("Ver rangos", "View ranks", "Voir les rangs")}</a>
              <a class="btn btn-primary btn-compact" href="/be-a-guardian.html">{tr("Ser Guardián", "Become a Guardian", "Devenir Gardien")}</a>
            </div>
          </div>
        {:else}
          <div class="settings-actions guardian-center-actions" aria-label={tr("Módulos del Guardián", "Guardian modules", "Modules du Gardien")}>
            {#each modules as module (module.key)}
              <button
                type="button"
                class={`settings-action guardian-center-action${activeModuleKey === module.key ? " is-active" : ""}`}
                aria-pressed={activeModuleKey === module.key}
                on:click={() => setActiveModule(module.key)}
              >
                <span class="settings-action-icon" aria-hidden="true">{module.icon}</span>
                <span class="settings-action-meta">
                  <span class="settings-action-label">{module.title}</span>
                  <span class="settings-action-note">{module.note}</span>
                </span>
                <span class="guardian-center-cta" aria-hidden="true">{tr("Abrir", "Open", "Ouvrir")}</span>
              </button>
            {/each}
          </div>

          <div class="guardian-center-divider" aria-hidden="true"></div>

          {@const activeModule = getActiveModule()}
          <section class="guardian-center-module" aria-label={activeModule.title}>
            <div class="guardian-center-module-head">
              <h3 class="guardian-center-module-title">{activeModule.title}</h3>
              {#if activeModuleKey === "wish_management" || activeModuleKey === "reported_posts" || activeModuleKey === "reported_profiles" || activeModuleKey === "rank_management" || activeModuleKey === "messaging"}
                <span class="guardian-center-module-pill">{tr("En vivo", "Live", "En direct")}</span>
              {:else}
                <span class="guardian-center-module-pill">{tr("Próximamente", "Coming soon", "Bientôt disponible")}</span>
              {/if}
            </div>

            {#if activeModuleKey === "wish_management"}
              <p class="panel-muted guardian-center-module-note">
                {tr(
                  "Requests generated from I can fulfill this wish. Use the View wish button to go to the exact wish.",
                  "Requests created from “I can fulfill this wish”. Use the “View wish” button to open the exact wish."
                )}
              </p>
            {:else if activeModuleKey === "reported_posts"}
              <p class="panel-muted guardian-center-module-note">
                {tr(
                  "Post reports received in real time. Review the report and decide whether the post is kept or deleted.",
                  "Post reports received in real time. Review the report and decide whether the post is kept or deleted."
                )}
              </p>
            {:else if activeModuleKey === "reported_profiles"}
              <p class="panel-muted guardian-center-module-note">
                {tr(
                  "Denuncias de perfiles recibidas en tiempo real, con las publicaciones denunciadas asociadas a cada usuario.",
                  "Profile reports received in real time, with reported posts associated with each user."
                )}
              </p>
            {:else if activeModuleKey === "rank_management"}
              <p class="panel-muted guardian-center-module-note">
                {tr(
                  "Busca usuarios por",
                  "Search users by"
                )} <strong>@id</strong> {tr("o", "or", "ou")} <strong>@username</strong>, {tr("revisa su rango actual y promuévelos al siguiente nivel sin saltos.", "review their current rank and promote them to the next level without skipping.", "vérifie leur rang actuel et promeus-les au niveau suivant sans sauter d'étapes.")}
              </p>
            {:else if activeModuleKey === "messaging"}
              <p class="panel-muted guardian-center-module-note">
                {tr(
                  "Centro de mensajería interno para iniciar conversaciones y responder dentro de cada hilo.",
                  "Internal messaging center to start conversations and reply inside each thread.",
                  "Centre de messagerie interne pour démarrer des conversations et répondre dans chaque fil."
                )}
              </p>
            {:else}
              <p class="panel-muted guardian-center-module-note">
                {tr(
                  "This module interface is ready. Tomorrow we will connect it to the database and real logic.",
                  "This module is ready at UI level. We will connect it to the database and real logic next."
                )}
              </p>
            {/if}

            {#if activeModuleKey === "wish_management"}
              {#if wishRequestsError}
                <div class="guardian-center-empty is-error">{wishRequestsError}</div>
              {:else if wishRequestsLoading}
                <div class="guardian-center-empty">{tr("Cargando solicitudes...", "Loading requests...", "Chargement des demandes...")}</div>
              {:else if !wishRequestsItems.length}
                <div class="guardian-center-empty">{tr("No hay solicitudes por ahora.", "There are no requests for now.", "Il n'y a aucune demande pour le moment.")}</div>
              {:else}
                <div class="guardian-wish-requests" aria-label={tr("Solicitudes recibidas", "Received requests", "Demandes reçues")}>
                  {#each wishRequestsItems as req (req.id)}
                    <article class="guardian-wish-card">
                      <header class="guardian-wish-card-head">
                        <div class="guardian-wish-card-title">{req.wish_text}</div>
                        <div class="guardian-wish-card-status">{formatStatusLabel(req)}</div>
                      </header>

                      <div class="guardian-wish-card-meta">
                        <span>{tr("Solicitud", "Request", "Demande")} #{req.id}</span>
                        <span aria-hidden="true">·</span>
                        <span>{formatDateTime(req.created_at)}</span>
                        <span aria-hidden="true">·</span>
                        <span>{tr("Tipo", "Type", "Type")}: {req.wish_type}</span>
                        {#if req.commitment_code}
                          <span aria-hidden="true">·</span>
                          <span class="guardian-wish-commitment-code">{req.commitment_code}</span>
                        {/if}
                      </div>

                      <div class="guardian-wish-card-actions">
                        <a class="btn btn-outline btn-compact" href={req.wish_url} target="_blank" rel="noopener noreferrer">
                          {tr("Ver deseo", "View wish", "Voir le souhait")}
                        </a>
                        <a class="btn btn-outline btn-compact" href={req.requester.profile_url} target="_blank" rel="noopener noreferrer">
                          {tr("Ver solicitante", "View requester", "Voir le demandeur")}
                        </a>
                        <a class="btn btn-outline btn-compact" href={req.wish_owner.profile_url} target="_blank" rel="noopener noreferrer">
                          {tr("Ver dueño del deseo", "View wish owner", "Voir le propriétaire du souhait")}
                        </a>
                        <button
                          class="btn btn-primary btn-compact"
                          type="button"
                          disabled={actionLoading || req.status === "closed" || Boolean(req.commitment_code)}
                          on:click={() => openSealCommitmentModal(req)}
                        >
                          {req.commitment_code ? tr("Compromiso sellado", "Commitment sealed", "Engagement scellé") : tr("Sellar compromiso", "Seal commitment", "Sceller l'engagement")}
                        </button>
                        <button
                          class="btn btn-outline btn-compact guardian-btn-deny"
                          type="button"
                          disabled={actionLoading || req.status === "closed"}
                          on:click={() => openDenyModal(req)}
                        >
                          {tr("Denegar petición", "Deny request", "Refuser la demande")}
                        </button>
                      </div>

                      <div class="guardian-wish-card-body">
                        <div class="guardian-wish-field">
                          <div class="guardian-wish-label">{tr("Solicitante", "Requester", "Demandeur")}</div>
                          <div class="guardian-wish-value">
                            {req.requester.full_name}
                            <span class="guardian-wish-handle">{req.requester.handle}</span>
                          </div>
                        </div>

                        <div class="guardian-wish-field">
                          <div class="guardian-wish-label">{tr("Dueño del deseo", "Wish owner", "Propriétaire du souhait")}</div>
                          <div class="guardian-wish-value guardian-wish-owner-row">
                            {req.wish_owner.full_name}
                            <span class="guardian-wish-handle">{req.wish_owner.handle}</span>
                            <button
                              class="guardian-owner-message-btn"
                              type="button"
                              title={tr("Enviar mensaje al dueño del deseo", "Send message to wish owner", "Envoyer un message au propriétaire du souhait")}
                              aria-label={tr("Enviar mensaje al dueño del deseo", "Send message to wish owner", "Envoyer un message au propriétaire du souhait")}
                              disabled={actionLoading || req.status === "closed"}
                              on:click={() => openOwnerMessageModal(req)}
                            >
                              ✉️
                            </button>
                          </div>
                        </div>

                        {#if req.commitment_code}
                          <div class="guardian-wish-field guardian-wish-field-commitment">
                            <div class="guardian-wish-label">{tr("Código de compromiso", "Commitment code", "Code d'engagement")}</div>
                            <div class="guardian-wish-value">
                              <strong>{req.commitment_code}</strong>
                              {#if req.commitment_sealed_at}
                                <span class="guardian-wish-commitment-date">
                                  · {tr("Sellado", "Sealed", "Scellé")}: {formatDateTime(req.commitment_sealed_at)}
                                </span>
                              {/if}
                            </div>
                          </div>
                        {/if}

                        {#if req.guardian}
                          <div class="guardian-wish-field">
                            <div class="guardian-wish-label">{tr("Guardián asignado", "Assigned guardian", "Gardien assigné")}</div>
                            <div class="guardian-wish-value">
                              {req.guardian.full_name}
                              <span class="guardian-wish-handle">{req.guardian.handle}</span>
                            </div>
                          </div>
                        {/if}

                        <div class="guardian-wish-field">
                          <div class="guardian-wish-label">{tr("Motivo", "Reason", "Motif")}</div>
                          <div class="guardian-wish-value guardian-wish-reason">{req.reason}</div>
                        </div>

                        <div class="guardian-wish-field guardian-wish-contact">
                          <div class="guardian-wish-label">{tr("Contacto", "Contact", "Contact")}</div>
                          <div class="guardian-wish-value">
                            <div>{req.contact_phone}</div>
                            <div>{req.contact_email}</div>
                          </div>
                        </div>

                        <div class="guardian-wish-field">
                          <div class="guardian-wish-label">{tr("Evidencia", "Evidence", "Preuve")}</div>
                          <div class="guardian-wish-value">
                            {#if req.evidence_url}
                              {#if req.evidence_mime_type && req.evidence_mime_type.startsWith("image/")}
                                <a
                                  class="guardian-wish-evidence-link"
                                  href={req.evidence_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  aria-label={tr("Abrir evidencia (imagen)", "Open evidence (image)", "Ouvrir la preuve (image)")}
                                >
                                  <img class="guardian-wish-evidence-img" src={req.evidence_url} alt={tr("Evidencia adjunta", "Attached evidence", "Preuve jointe")} />
                                </a>
                              {:else if req.evidence_mime_type && req.evidence_mime_type.startsWith("video/")}
                                <video class="guardian-wish-evidence-video" src={req.evidence_url} controls preload="metadata">
                                  <track kind="captions" srclang={isEn ? "en" : isFr ? "fr" : "es"} label={tr("Subtítulos", "Captions", "Sous-titres")} />
                                </video>
                              {:else}
                                <a class="btn btn-outline btn-compact" href={req.evidence_url} target="_blank" rel="noopener noreferrer">
                                  {tr("Ver evidencia", "View evidence", "Voir la preuve")}
                                </a>
                              {/if}
                            {:else}
                              <span class="panel-muted">{tr("No disponible.", "Not available.", "Non disponible.")}</span>
                            {/if}
                          </div>
                        </div>
                      </div>
                    </article>
                  {/each}
                </div>

                <div class="guardian-wish-pagination" aria-label={tr("Paginación de solicitudes", "Request pagination", "Pagination des demandes")}>
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={wishRequestsLoading || wishRequestsPage <= 1}
                    on:click={() => loadWishRequests(wishRequestsPage - 1)}
                  >
                    {tr("Anterior", "Previous", "Précédent")}
                  </button>
                  <span class="guardian-wish-page">{wishRequestsPage} / {wishRequestsTotalPages}</span>
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={wishRequestsLoading || wishRequestsPage >= wishRequestsTotalPages}
                    on:click={() => loadWishRequests(wishRequestsPage + 1)}
                  >
                    {tr("Siguiente", "Next", "Suivant")}
                  </button>
                </div>
              {/if}
            {:else if activeModuleKey === "reported_posts"}
              {#if reportedPostsError}
                <div class="guardian-center-empty is-error">{reportedPostsError}</div>
              {:else if reportedPostsLoading}
                <div class="guardian-center-empty">{tr("Cargando publicaciones denunciadas...", "Loading reported posts...", "Chargement des publications signalées...")}</div>
              {:else if !reportedPostsItems.length}
                <div class="guardian-center-empty">{tr("No hay publicaciones denunciadas por ahora.", "There are no reported posts for now.", "Il n'y a aucune publication signalée pour le moment.")}</div>
              {:else}
                <div class="guardian-reported-posts" aria-label={tr("Publicaciones denunciadas", "Reported posts", "Publications signalées")}>
                  {#each reportedPostsItems as item (item.id)}
                    {@const statusLabel = formatReportStatusLabel(item)}
                    <article class="guardian-reported-card">
                      <header class="guardian-reported-head">
                        <div class="guardian-reported-title-wrap">
                          <div class="guardian-reported-title">{tr("Caso", "Case", "Cas")} #{item.id}</div>
                          <div class="guardian-reported-meta">
                            <span>{tr("Reportes", "Reports", "Signalements")}: {item.report_count}</span>
                            <span aria-hidden="true">·</span>
                            <span>{tr("Primero", "First", "Premier")}: {formatDateTime(item.first_reported_at)}</span>
                            <span aria-hidden="true">·</span>
                            <span>{tr("Último", "Latest", "Récents")}: {formatDateTime(item.last_reported_at)}</span>
                          </div>
                        </div>
                        <span class={`guardian-reported-status is-${String(item.status || "").toLowerCase()}`}>{statusLabel}</span>
                      </header>

                      <div class="guardian-reported-body">
                        <div class="guardian-reported-field">
                          <div class="guardian-wish-label">{tr("Autor de la publicación", "Post author", "Auteur de la publication")}</div>
                          <div class="guardian-wish-value">
                            {item.post_author.full_name}
                            <span class="guardian-wish-handle">{item.post_author.handle}</span>
                          </div>
                        </div>

                        <div class="guardian-reported-field">
                          <div class="guardian-wish-label">{tr("Publicación reportada", "Reported post", "Publication signalée")}</div>
                          <div class="guardian-reported-text">
                            {#if item.post_text}
                              {item.post_text}
                            {:else}
                              <span class="panel-muted">{tr("Sin texto.", "No text.", "Aucun texte.")}</span>
                            {/if}
                          </div>
                          {#if item.post_media_url}
                            <div class="guardian-reported-media-wrap">
                              {#if item.post_media_kind && item.post_media_kind.startsWith("video")}
                                <video class="guardian-reported-media" src={item.post_media_url} controls preload="metadata">
                                  <track kind="captions" srclang={isEn ? "en" : isFr ? "fr" : "es"} label={tr("Subtítulos", "Captions", "Sous-titres")} />
                                </video>
                              {:else}
                                <a href={item.post_media_url} target="_blank" rel="noopener noreferrer" class="guardian-reported-media-link">
                                  <img class="guardian-reported-media" src={item.post_media_url} alt={tr("Media de la publicación denunciada", "Reported post media", "Média de la publication signalée")} />
                                </a>
                              {/if}
                            </div>
                          {/if}
                        </div>

                        {#if item.reports?.length}
                          <div class="guardian-reported-field">
                            <div class="guardian-wish-label">{tr("Últimos reportes", "Latest reports", "Derniers signalements")}</div>
                            <div class="guardian-reported-reasons">
                              {#each item.reports as rep (rep.id)}
                                <div class="guardian-reported-reason-item">
                                  <span class="guardian-wish-handle">{rep.reporter_handle}</span>
                                  <span>{formatReportReasonLabel(rep.reason, rep.other_reason)}</span>
                                  <span class="panel-muted">{formatDateTime(rep.created_at)}</span>
                                </div>
                              {/each}
                            </div>
                          </div>
                        {/if}

                        {#if item.resolved_by_guardian}
                          <div class="guardian-reported-field">
                            <div class="guardian-wish-label">{tr("Última decisión", "Latest decision", "Dernière décision")}</div>
                            <div class="guardian-wish-value">
                              {item.resolved_by_guardian.full_name}
                              <span class="guardian-wish-handle">{item.resolved_by_guardian.handle}</span>
                              {#if item.resolved_at}
                                <span class="guardian-wish-commitment-date">· {formatDateTime(item.resolved_at)}</span>
                              {/if}
                            </div>
                          </div>
                        {/if}
                      </div>

                      <div class="guardian-reported-actions">
                        <a class="btn btn-outline btn-compact" href={item.post_author.profile_url} target="_blank" rel="noopener noreferrer">
                          {tr("Ver perfil", "View profile", "Voir le profil")}
                        </a>
                        <button
                          class="btn btn-primary btn-compact"
                          type="button"
                          disabled={reportedPostsActionLoading || item.status === "deleted" || !item.post_id}
                          on:click={() => openDeleteReportedPostModal(item)}
                        >
                          {tr("Eliminar publicación", "Delete post", "Supprimer la publication")}
                        </button>
                        <button
                          class="btn btn-outline btn-compact"
                          type="button"
                          disabled={reportedPostsActionLoading || item.status === "kept"}
                          on:click={() => openKeepReportedPostModal(item)}
                        >
                          {tr("Conservar publicación", "Keep post", "Conserver la publication")}
                        </button>
                      </div>
                    </article>
                  {/each}
                </div>

                <div class="guardian-wish-pagination" aria-label={tr("Paginación de publicaciones denunciadas", "Reported posts pagination", "Pagination des publications signalées")}>
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={reportedPostsLoading || reportedPostsPage <= 1}
                    on:click={() => loadReportedPosts(reportedPostsPage - 1)}
                  >
                    {tr("Anterior", "Previous", "Précédent")}
                  </button>
                  <span class="guardian-wish-page">{reportedPostsPage} / {reportedPostsTotalPages}</span>
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={reportedPostsLoading || reportedPostsPage >= reportedPostsTotalPages}
                    on:click={() => loadReportedPosts(reportedPostsPage + 1)}
                  >
                    {tr("Siguiente", "Next", "Suivant")}
                  </button>
                </div>
              {/if}
            {:else if activeModuleKey === "reported_profiles"}
              {#if reportedProfilesError}
                <div class="guardian-center-empty is-error">{reportedProfilesError}</div>
              {:else if reportedProfilesLoading}
                <div class="guardian-center-empty">{tr("Cargando perfiles denunciados...", "Loading reported profiles...", "Chargement des profils signalés...")}</div>
              {:else if !reportedProfilesItems.length}
                <div class="guardian-center-empty">{tr("No hay perfiles denunciados por ahora.", "There are no reported profiles for now.", "Il n'y a aucun profil signalé pour le moment.")}</div>
              {:else}
                <div class="guardian-reported-posts guardian-reported-profiles" aria-label={tr("Perfiles denunciados", "Reported profiles", "Profils signalés")}>
                  {#each reportedProfilesItems as item (item.id)}
                    {@const statusLabel = formatProfileReportStatusLabel(item)}
                    {@const postsData = item.reported_posts || { items: [], page: 1, total_pages: 1, total: 0, range_start: 0, range_end: 0 }}
                    <article class="guardian-reported-card guardian-reported-profile-card">
                      <header class="guardian-reported-head">
                        <div class="guardian-reported-title-wrap">
                          <div class="guardian-reported-title">{tr("Caso de perfil", "Profile case", "Cas de profil")} #{item.id}</div>
                          <div class="guardian-reported-meta">
                            <span>{tr("Reportes", "Reports", "Signalements")}: {item.report_count}</span>
                            <span aria-hidden="true">·</span>
                            <span>{tr("Primero", "First", "Premier")}: {formatDateTime(item.first_reported_at)}</span>
                            <span aria-hidden="true">·</span>
                            <span>{tr("Último", "Latest", "Récents")}: {formatDateTime(item.last_reported_at)}</span>
                          </div>
                        </div>
                        <span class={`guardian-reported-status is-${String(item.status || "").toLowerCase()}`}>{statusLabel}</span>
                      </header>

                      <div class="guardian-reported-body">
                        <div class="guardian-reported-field">
                          <div class="guardian-wish-label">{tr("Usuario denunciado", "Reported user", "Utilisateur signalé")}</div>
                          <div class="guardian-wish-value">
                            {item.reported_user.full_name}
                            <span class="guardian-wish-handle">{item.reported_user.handle}</span>
                          </div>
                        </div>

                        <div class="guardian-reported-field">
                          <div class="guardian-wish-label">{tr("Estado de la cuenta", "Account status", "Statut du compte")}</div>
                          <div class="guardian-wish-value">
                            <span class={`guardian-reported-status is-${String(item.account_moderation_status || "active").toLowerCase()}`}>
                              {formatAccountModerationStatusLabel(item.account_moderation_status)}
                            </span>
                            {#if item.account_moderated_by_guardian}
                              <span class="guardian-wish-handle">
                                · {tr("por", "by", "par")} {item.account_moderated_by_guardian.handle}
                              </span>
                            {/if}
                            {#if item.account_moderated_at}
                              <span class="guardian-wish-commitment-date">
                                · {formatDateTime(item.account_moderated_at)}
                              </span>
                            {/if}
                          </div>
                        </div>

                        {#if item.reports?.length}
                          <div class="guardian-reported-field">
                            <div class="guardian-wish-label">{tr("Últimos reportes de perfil", "Latest profile reports", "Derniers signalements de profil")}</div>
                            <div class="guardian-reported-reasons">
                              {#each item.reports as rep (rep.id)}
                                <div class="guardian-reported-reason-item">
                                  <span class="guardian-wish-handle">{rep.reporter_handle}</span>
                                  <span>{formatProfileReportReasonLabel(rep.reason, rep.other_reason)}</span>
                                  <span class="panel-muted">{formatDateTime(rep.created_at)}</span>
                                </div>
                              {/each}
                            </div>
                          </div>
                        {/if}

                        <div class="guardian-reported-field guardian-reported-profile-posts">
                          <div class="guardian-reported-profile-posts-head">
                            <div class="guardian-wish-label">{tr("Publicaciones denunciadas", "Reported posts", "Publications signalées")}</div>
                            <span class="guardian-reported-profile-posts-counter">{Number(postsData.total || 0)} / {Number(postsData.total || 0)}</span>
                          </div>

                          {#if item.reported_posts_error}
                            <div class="guardian-center-empty is-error">{item.reported_posts_error}</div>
                          {:else if item.reported_posts_loading}
                            <div class="guardian-center-empty">{tr("Cargando publicaciones denunciadas del perfil...", "Loading reported posts for this profile...", "Chargement des publications signalées pour ce profil...")}</div>
                          {:else if !postsData.items?.length}
                            <p class="panel-muted">{tr("0/0. Este usuario está limpio en publicaciones denunciadas.", "0/0. This user has no reported posts.", "0/0. Cet utilisateur n'a aucune publication signalée.")}</p>
                          {:else}
                            <div class="guardian-reported-profile-post-list">
                              {#each postsData.items as postCase (postCase.id)}
                                <article class="guardian-reported-profile-post-item">
                                  <div class="guardian-reported-profile-post-main">
                                    <div class="guardian-reported-profile-post-title">
                                      {tr("Caso", "Case", "Cas")} #{postCase.id} · {tr("Reportes", "Reports", "Signalements")}: {postCase.report_count}
                                    </div>
                                    <div class="guardian-reported-profile-post-meta">
                                      {tr("Último reporte", "Latest report", "Dernier signalement")}: {formatDateTime(postCase.last_reported_at)}
                                    </div>
                                    {#if postCase.post_text}
                                      <div class="guardian-reported-text">{postCase.post_text}</div>
                                    {/if}
                                  </div>
                                  <div class="guardian-reported-profile-post-actions">
                                    {#if postCase.post_url}
                                      <a class="btn btn-outline btn-compact" href={postCase.post_url} target="_blank" rel="noopener noreferrer">
                                        {tr("Ver publicación", "View post", "Voir la publication")}
                                      </a>
                                    {:else}
                                      <span class="panel-muted">{tr("Publicación no disponible.", "Post unavailable.", "Publication indisponible.")}</span>
                                    {/if}
                                  </div>
                                </article>
                              {/each}
                            </div>
                          {/if}

                          {#if Number(postsData.total_pages || 1) > 1}
                            <div class="guardian-wish-pagination guardian-reported-profile-post-pagination" aria-label={tr(`Paginación de publicaciones denunciadas del caso ${item.id}`, `Reported posts pagination for case ${item.id}`, `Reported posts pagination for case ${item.id}`)}>
                              <button
                                class="btn btn-outline btn-compact"
                                type="button"
                                disabled={item.reported_posts_loading || Number(postsData.page || 1) <= 1}
                                on:click={() => loadReportedProfilePostsPage(item.id, Number(postsData.page || 1) - 1)}
                              >
                                {tr("Anterior", "Previous", "Précédent")}
                              </button>
                              <span class="guardian-wish-page">{Number(postsData.page || 1)} / {Number(postsData.total_pages || 1)}</span>
                              <button
                                class="btn btn-outline btn-compact"
                                type="button"
                                disabled={item.reported_posts_loading || Number(postsData.page || 1) >= Number(postsData.total_pages || 1)}
                                on:click={() => loadReportedProfilePostsPage(item.id, Number(postsData.page || 1) + 1)}
                              >
                                {tr("Siguiente", "Next", "Suivant")}
                              </button>
                            </div>
                          {/if}
                        </div>

                        {#if item.resolved_by_guardian}
                          <div class="guardian-reported-field">
                            <div class="guardian-wish-label">{tr("Última revisión", "Latest review", "Dernière révision")}</div>
                            <div class="guardian-wish-value">
                              {item.resolved_by_guardian.full_name}
                              <span class="guardian-wish-handle">{item.resolved_by_guardian.handle}</span>
                              {#if item.resolved_at}
                                <span class="guardian-wish-commitment-date">· {formatDateTime(item.resolved_at)}</span>
                              {/if}
                            </div>
                          </div>
                        {/if}
                      </div>

                      <div class="guardian-reported-actions">
                        <button
                          class="btn btn-outline btn-compact"
                          type="button"
                          disabled={reportedProfilesActionLoading || !item.can_suspend_account}
                          on:click={() => openSuspendReportedProfileModal(item)}
                        >
                          {tr("Suspender cuenta", "Suspend account", "Suspendre le compte")}
                        </button>
                        <button
                          class="btn btn-outline btn-compact"
                          type="button"
                          disabled={reportedProfilesActionLoading || !item.can_enable_account}
                          on:click={() => openEnableReportedProfileModal(item)}
                        >
                          {tr("Habilitar cuenta", "Enable account", "Activer le compte")}
                        </button>
                        <button
                          class="btn btn-primary btn-compact"
                          type="button"
                          disabled={reportedProfilesActionLoading || !item.can_close_account}
                          on:click={() => openCloseReportedProfileModal(item)}
                        >
                          {tr("Cerrar cuenta", "Close account", "Fermer le compte")}
                        </button>
                        <a class="btn btn-outline btn-compact" href={item.reported_user.profile_url} target="_blank" rel="noopener noreferrer">
                          {tr("Ver perfil", "View profile", "Voir le profil")}
                        </a>
                      </div>
                    </article>
                  {/each}
                </div>

                <div class="guardian-wish-pagination" aria-label={tr("Paginación de perfiles denunciados", "Reported profiles pagination", "Pagination des profils signalés")}>
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={reportedProfilesLoading || reportedProfilesPage <= 1}
                    on:click={() => loadReportedProfiles(reportedProfilesPage - 1)}
                  >
                    {tr("Anterior", "Previous", "Précédent")}
                  </button>
                  <span class="guardian-wish-page">{reportedProfilesPage} / {reportedProfilesTotalPages}</span>
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={reportedProfilesLoading || reportedProfilesPage >= reportedProfilesTotalPages}
                    on:click={() => loadReportedProfiles(reportedProfilesPage + 1)}
                  >
                    {tr("Siguiente", "Next", "Suivant")}
                  </button>
                </div>
              {/if}
            {:else if activeModuleKey === "rank_management"}
              <section class="guardian-rank-manager" aria-label={tr("Gestión de rangos", "Rank management", "Gestion des rangs")}>
                <form
                  class="guardian-rank-search"
                  on:submit|preventDefault={searchRankUser}
                >
                  <label class="modal-label guardian-rank-label" for="rankLookupQuery">
                    {tr("Usuario objetivo (@id o @username)", "Target user (@id or @username)", "Utilisateur cible (@id ou @username)")}
                  </label>
                  <div class="guardian-rank-search-row">
                    <input
                      id="rankLookupQuery"
                      class="modal-input guardian-rank-input"
                      type="text"
                      placeholder={tr("@id12 o @carlosjduarte", "@id12 or @carlosjduarte", "@id12 ou @carlosjduarte")}
                      maxlength="80"
                      bind:value={rankLookupQuery}
                      on:input={() => {
                        rankLookupError = "";
                      }}
                    />
                    <button
                      class="btn btn-primary btn-compact"
                      type="submit"
                      disabled={rankLookupLoading}
                    >
                      {rankLookupLoading ? tr("Buscando...", "Searching...", "Recherche...") : tr("Buscar usuario", "Search user", "Rechercher un utilisateur")}
                    </button>
                  </div>
                  <p class="panel-muted guardian-rank-search-hint">
                    {tr("El ascenso siempre será de nivel en nivel hasta máximo Rango", "Promotion always goes level by level up to maximum Rank", "La promotion se fait toujours niveau par niveau jusqu'au rang maximum")} {GUARDIAN_MAX_RANK}.
                  </p>
                </form>

                {#if rankLookupError}
                  <div class="guardian-center-empty is-error">{rankLookupError}</div>
                {/if}

                {#if rankLookupResult}
                  <article class="guardian-rank-card">
                    <header class="guardian-rank-card-head">
                      <div>
                        <h4 class="guardian-rank-card-title">{rankLookupResult.full_name}</h4>
                        <div class="guardian-rank-card-meta">
                          <span>{rankLookupResult.handle}</span>
                          <span aria-hidden="true">·</span>
                          <span>{tr("Rol", "Role", "Rôle")}: {rankLookupResult.role}</span>
                        </div>
                      </div>
                      <a
                        class="btn btn-outline btn-compact"
                        href={rankLookupResult.profile_url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {tr("Ver perfil", "View profile", "Voir le profil")}
                      </a>
                    </header>

                    <div class="guardian-rank-grid">
                      <div class="guardian-rank-slot">
                        <div class="guardian-wish-label">{tr("Rango actual", "Current rank", "Rang actuel")}</div>
                        <div class="guardian-rank-value">
                          {tr("Nivel", "Level", "Niveau")} {rankLookupResult.guardian_rank} · {rankLookupResult.guardian_rank_name}
                        </div>
                      </div>
                      <div class="guardian-rank-slot">
                        <div class="guardian-wish-label">{tr("Siguiente nivel", "Next level", "Niveau suivant")}</div>
                        <div class="guardian-rank-value">
                          {#if rankLookupResult.next_guardian_rank !== null && rankLookupResult.next_guardian_rank !== undefined}
                            {tr("Nivel", "Level", "Niveau")} {rankLookupResult.next_guardian_rank} · {rankLookupResult.next_guardian_rank_name}
                          {:else}
                            {tr("Rango máximo alcanzado", "Maximum rank reached", "Rang maximum atteint")}
                          {/if}
                        </div>
                      </div>
                    </div>

                    {#if rankLookupResult.is_self}
                      <p class="panel-muted guardian-rank-self-note">
                        {tr("Este usuario corresponde a tu propia cuenta.", "This user matches your own account.", "Cet utilisateur correspond à ton propre compte.")}
                      </p>
                    {/if}

                    <div class="guardian-rank-actions">
                      <button
                        class="btn btn-primary btn-compact"
                        type="button"
                        disabled={!rankLookupResult.can_promote || rankPromoteLoading}
                        on:click={openPromoteRankModal}
                      >
                        {#if rankPromoteLoading}
                          {tr("Promoviendo...", "Promoting...", "Promotion...")}
                        {:else if rankLookupResult.can_promote}
                          {tr("Subir al siguiente nivel", "Promote to next level", "Promouvoir au niveau suivant")}
                        {:else}
                          {tr("Rango máximo alcanzado", "Maximum rank reached", "Rang maximum atteint")}
                        {/if}
                      </button>
                    </div>
                  </article>
                {/if}
              </section>
            {:else if activeModuleKey === "messaging"}
              <GuardianMessagingCenter />
            {/if}
          </section>
        {/if}
      </section>
    </div>
  </main>

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showSealCommitmentModal}
    aria-hidden={!showSealCommitmentModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !actionLoading) closeSealCommitmentModal();
    }}
  >
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label={tr("Sellar compromiso", "Seal commitment", "Sceller l'engagement")}>
      <div class="modal-head guardian-center-modal-head">
        <h3>{tr("Sellar compromiso", "Seal commitment", "Sceller l'engagement")}</h3>
      </div>
      <div class="modal-body">
        <p class="panel-muted">
          {tr(
            "Did you make sure to follow the prior protocol so this process is completed according to Kiadez.com internal policies?",
            "Did you ensure the prior protocol was followed so this process aligns with Kiadez.com's internal policies?"
          )}
        </p>
        {#if actionError}
          <div class="wish-error is-visible">{actionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={actionLoading} on:click={sealCommitment}>
          {actionLoading ? tr("Procesando...", "Processing...", "Traitement...") : tr("Sí", "Yes", "Oui")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={actionLoading} on:click={closeSealCommitmentModal}>
          {tr("No", "No", "Non")}
        </button>
      </div>
    </div>
  </div>

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showDenyModal}
    aria-hidden={!showDenyModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !actionLoading) closeDenyModal();
    }}
  >
    <div class="modal wish-modal guardian-center-modal guardian-center-mail-modal" role="dialog" aria-modal="true" aria-label={tr("Denegar petición", "Deny request", "Refuser la demande")}>
      <div class="modal-head guardian-center-modal-head">
        <h3>{tr("Denegar petición", "Deny request", "Refuser la demande")}</h3>
      </div>
      <div class="modal-body">
        <label class="modal-label" for="denyToHandle">{tr("Para", "To", "À")}</label>
        <input id="denyToHandle" class="modal-input guardian-center-readonly" type="text" readonly value={denyToHandle} />

        <label class="modal-label" for="denySubject">{tr("Asunto", "Subject", "Objet")}</label>
        <input
          id="denySubject"
          class="modal-input"
          class:is-error={denySubjectError}
          type="text"
          maxlength="180"
          bind:value={denySubject}
          on:input={() => {
            denySubjectError = false;
            actionError = "";
          }}
        />

        <label class="modal-label" for="denyBody">{tr("Mensaje", "Message", "Message")}</label>
        <textarea
          id="denyBody"
          class="modal-textarea guardian-center-mail-textarea"
          class:is-error={denyBodyError}
          rows="6"
          placeholder={tr(
            `Explain here why the request was denied.\n\nRegards,\nGuardian – Rank ${guardianRank}\nKiadez.com`,
            `Explain here why the request was denied.\n\nSincerely,\nGuardian – Rank ${guardianRank}\nKiadez.com`
          )}
          bind:value={denyBody}
          on:input={() => {
            denyBodyError = false;
            actionError = "";
          }}
        ></textarea>

        {#if actionError}
          <div class="wish-error is-visible">{actionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={actionLoading} on:click={denyRequest}>
          {actionLoading ? tr("Enviando...", "Sending...", "Envoi...") : tr("Enviar denegación", "Send denial", "Envoyer un refus")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={actionLoading} on:click={closeDenyModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
      </div>
    </div>
  </div>

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showOwnerMessageModal}
    aria-hidden={!showOwnerMessageModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !actionLoading) closeOwnerMessageModal();
    }}
  >
    <div class="modal wish-modal guardian-center-modal guardian-center-mail-modal" role="dialog" aria-modal="true" aria-label={tr("Mensaje al dueño del deseo", "Message to wish owner", "Message au propriétaire du souhait")}>
      <div class="modal-head guardian-center-modal-head">
        <h3>{tr("Mensaje al dueño del deseo", "Message to wish owner", "Message au propriétaire du souhait")}</h3>
      </div>
      <div class="modal-body">
        <label class="modal-label" for="ownerMessageToHandle">{tr("Para", "To", "À")}</label>
        <input
          id="ownerMessageToHandle"
          class="modal-input guardian-center-readonly"
          type="text"
          readonly
          value={ownerMessageToHandle}
        />

        <label class="modal-label" for="ownerMessageSubject">{tr("Asunto", "Subject", "Objet")}</label>
        <input
          id="ownerMessageSubject"
          class="modal-input"
          class:is-error={ownerMessageSubjectError}
          type="text"
          maxlength="180"
          bind:value={ownerMessageSubject}
          on:input={() => {
            ownerMessageSubjectError = false;
            actionError = "";
          }}
        />

        <label class="modal-label" for="ownerMessageBody">{tr("Mensaje", "Message", "Message")}</label>
        <textarea
          id="ownerMessageBody"
          class="modal-textarea guardian-center-mail-textarea"
          class:is-error={ownerMessageBodyError}
          rows="6"
          bind:value={ownerMessageBody}
          on:input={() => {
            ownerMessageBodyError = false;
            actionError = "";
          }}
        ></textarea>

        {#if actionError}
          <div class="wish-error is-visible">{actionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={actionLoading} on:click={sendOwnerMessage}>
          {actionLoading ? tr("Enviando...", "Sending...", "Envoi...") : tr("Enviar mensaje", "Send message", "Envoyer un message")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={actionLoading} on:click={closeOwnerMessageModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
      </div>
    </div>
  </div>

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showDeleteReportedPostModal}
    aria-hidden={!showDeleteReportedPostModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !reportedPostsActionLoading) closeDeleteReportedPostModal();
    }}
  >
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label={tr("Eliminar publicación denunciada", "Delete reported post", "Supprimer la publication signalée")}>
      <div class="modal-head guardian-center-modal-head">
        <h3>{tr("Eliminar publicación denunciada", "Delete reported post", "Supprimer la publication signalée")}</h3>
      </div>
      <div class="modal-body">
        <p class="panel-muted">
          {tr(
            "This action will delete the reported post and leave a record in the user history.",
            "This action will delete the reported post and leave a record in the user's history."
          )}
        </p>
        {#if activeReportedPost?.post_author}
          <p>
            {tr("Autor", "Author", "Auteur")}: <strong>{activeReportedPost.post_author.full_name}</strong>
            <span class="guardian-wish-handle">{activeReportedPost.post_author.handle}</span>
          </p>
        {/if}
        {#if reportedPostsActionError}
          <div class="wish-error is-visible">{reportedPostsActionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={reportedPostsActionLoading} on:click={deleteReportedPost}>
          {reportedPostsActionLoading ? tr("Procesando...", "Processing...", "Traitement...") : tr("Eliminar", "Delete", "Supprimer")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={reportedPostsActionLoading} on:click={closeDeleteReportedPostModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
      </div>
    </div>
  </div>

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showKeepReportedPostModal}
    aria-hidden={!showKeepReportedPostModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !reportedPostsActionLoading) closeKeepReportedPostModal();
    }}
  >
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label={tr("Conservar publicación reportada", "Keep reported post", "Conserver la publication signalée")}>
      <div class="modal-head guardian-center-modal-head">
        <h3>{tr("Conservar publicación reportada", "Keep reported post", "Conserver la publication signalée")}</h3>
      </div>
      <div class="modal-body">
        <p class="panel-muted">
          {tr(
            "You will mark this case as reviewed and the post will remain visible.",
            "You will mark this case as reviewed and the post will remain visible."
          )}
        </p>
        {#if activeReportedPost?.post_author}
          <p>
            {tr("Autor", "Author", "Auteur")}: <strong>{activeReportedPost.post_author.full_name}</strong>
            <span class="guardian-wish-handle">{activeReportedPost.post_author.handle}</span>
          </p>
        {/if}
        {#if reportedPostsActionError}
          <div class="wish-error is-visible">{reportedPostsActionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={reportedPostsActionLoading} on:click={keepReportedPost}>
          {reportedPostsActionLoading ? tr("Procesando...", "Processing...", "Traitement...") : tr("Conservar", "Keep", "Conserver")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={reportedPostsActionLoading} on:click={closeKeepReportedPostModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
      </div>
    </div>
  </div>

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showPromoteRankModal}
    aria-hidden={!showPromoteRankModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !rankPromoteLoading) closePromoteRankModal();
    }}
  >
    <div class="modal wish-modal guardian-center-modal guardian-rank-promote-modal" role="dialog" aria-modal="true" aria-label={tr("Confirmar ascenso de rango", "Confirm rank promotion", "Confirmer la promotion de rang")}>
      <div class="modal-head guardian-center-modal-head">
        <h3>{tr("Confirmar ascenso de rango", "Confirm rank promotion", "Confirmer la promotion de rang")}</h3>
      </div>
      <div class="modal-body">
        {#if rankLookupResult}
          <p>
            {tr("¿Estás seguro que quieres subir a", "Are you sure you want to promote", "Es-tu sûr de vouloir promouvoir")}
            <strong> {rankLookupResult.full_name}</strong>
            ({rankLookupResult.handle})
            {tr("to", "to", "à")}
            <strong>
              {tr("nivel", "level", "niveau")} {rankLookupResult.next_guardian_rank} ({rankLookupResult.next_guardian_rank_name})
            </strong>
            ?
          </p>
          <p class="panel-muted">
            {tr("Rango actual", "Current rank", "Rang actuel")}: {tr("Nivel", "Level", "Niveau")} {rankLookupResult.guardian_rank} ({rankLookupResult.guardian_rank_name}).
          </p>
        {:else}
          <p class="panel-muted">{tr("No hay usuario seleccionado.", "No selected user.", "Aucun utilisateur sélectionné.")}</p>
        {/if}

        {#if rankPromoteError}
          <div class="wish-error is-visible">{rankPromoteError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button
          class="btn btn-primary btn-compact"
          type="button"
          disabled={rankPromoteLoading || !rankLookupResult?.can_promote}
          on:click={promoteRankUser}
        >
          {rankPromoteLoading ? tr("Procesando...", "Processing...", "Traitement...") : tr("Sí, subir nivel", "Yes, promote level", "Oui, promouvoir le niveau")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={rankPromoteLoading} on:click={closePromoteRankModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
      </div>
    </div>
  </div>

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showSuspendReportedProfileModal}
    aria-hidden={!showSuspendReportedProfileModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !reportedProfilesActionLoading) closeSuspendReportedProfileModal();
    }}
  >
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label={tr("Suspender cuenta reportada", "Suspend reported account", "Suspendre le compte signalé")}>
      <div class="modal-head guardian-center-modal-head">
        <h3>{tr("Suspender cuenta", "Suspend account", "Suspendre le compte")}</h3>
      </div>
      <div class="modal-body">
        {#if activeReportedProfile}
          <p>
            {tr("¿Estás seguro que quieres suspender la cuenta de", "Are you sure you want to suspend the account of", "Es-tu sûr de vouloir suspendre le compte de")}
            <strong> {activeReportedProfile.reported_user?.full_name}</strong>
            ({activeReportedProfile.reported_user?.handle})?
          </p>
          <p class="panel-muted">
            {tr(
              "Suspension does not expire over time. Only a Guardian can enable it manually.",
              "Suspension does not expire over time. Only a Guardian can enable it manually."
            )}
          </p>
        {:else}
          <p class="panel-muted">{tr("No hay perfil seleccionado.", "No selected profile.", "Aucun profil sélectionné.")}</p>
        {/if}

        {#if reportedProfilesActionError}
          <div class="wish-error is-visible">{reportedProfilesActionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={suspendReportedProfileAccount}>
          {reportedProfilesActionLoading ? tr("Procesando...", "Processing...", "Traitement...") : tr("Sí, suspender", "Yes, suspend", "Oui, suspendre")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={closeSuspendReportedProfileModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
      </div>
    </div>
  </div>

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showEnableReportedProfileModal}
    aria-hidden={!showEnableReportedProfileModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !reportedProfilesActionLoading) closeEnableReportedProfileModal();
    }}
  >
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label={tr("Habilitar cuenta reportada", "Enable reported account", "Activer le compte signalé")}>
      <div class="modal-head guardian-center-modal-head">
        <h3>{tr("Habilitar cuenta", "Enable account", "Activer le compte")}</h3>
      </div>
      <div class="modal-body">
        {#if activeReportedProfile}
          <p>
            {tr("¿Estas seguro que quieres habilitar cuenta?", "Are you sure you want to enable the account?", "Es-tu sûr de vouloir activer le compte ?")}
          </p>
          <p class="panel-muted">
            {tr("Usuario", "User", "Utilisateur")}: <strong>{activeReportedProfile.reported_user?.full_name}</strong>
            <span class="guardian-wish-handle">{activeReportedProfile.reported_user?.handle}</span>
          </p>
        {:else}
          <p class="panel-muted">{tr("No hay perfil seleccionado.", "No selected profile.", "Aucun profil sélectionné.")}</p>
        {/if}

        {#if reportedProfilesActionError}
          <div class="wish-error is-visible">{reportedProfilesActionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={enableReportedProfileAccount}>
          {reportedProfilesActionLoading ? tr("Procesando...", "Processing...", "Traitement...") : tr("Sí, habilitar", "Yes, enable", "Oui, activer")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={closeEnableReportedProfileModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
      </div>
    </div>
  </div>

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showCloseReportedProfileModal}
    aria-hidden={!showCloseReportedProfileModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !reportedProfilesActionLoading) closeCloseReportedProfileModal();
    }}
  >
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label={tr("Cerrar cuenta reportada", "Close reported account", "Fermer le compte signalé")}>
      <div class="modal-head guardian-center-modal-head">
        <h3>{tr("Cerrar cuenta", "Close account", "Fermer le compte")}</h3>
      </div>
      <div class="modal-body">
        {#if activeReportedProfile}
          <p>
            {tr("¿Estas seguro que quieres cerrar cuenta de", "Are you sure you want to close the account of", "Es-tu sûr de vouloir fermer le compte de")}
            <strong> {activeReportedProfile.reported_user?.full_name}</strong>
            ({activeReportedProfile.reported_user?.handle})?
          </p>
          <p class="panel-muted">
            {tr(
              "This decision is final. The account will be permanently closed and cannot be enabled again.",
              "This decision is final. The account will be permanently closed and cannot be enabled again."
            )}
          </p>
        {:else}
          <p class="panel-muted">{tr("No hay perfil seleccionado.", "No selected profile.", "Aucun profil sélectionné.")}</p>
        {/if}

        {#if reportedProfilesActionError}
          <div class="wish-error is-visible">{reportedProfilesActionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={closeReportedProfileAccount}>
          {reportedProfilesActionLoading ? tr("Procesando...", "Processing...", "Traitement...") : tr("Sí, cerrar cuenta", "Yes, close account", "Oui, fermer le compte")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={closeCloseReportedProfileModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
      </div>
    </div>
  </div>
  <AuthFooter />
</div>
