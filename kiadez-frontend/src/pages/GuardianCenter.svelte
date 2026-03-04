<script>
  import { onMount } from "svelte";
  import GuardianMessagingCenter from "../lib/GuardianMessagingCenter.svelte";
  import { logout } from "../lib/logout";
  import { showUiAlert } from "../lib/uiFeedback";

  const API = import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") || "http://localhost:8000";
  const GUARDIAN_REQUIRED_RANK = 3;
  const GUARDIAN_MAX_RANK = 8;

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
      window.location.href = "/login.html";
      throw new Error("Sesión expirada.");
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
      title: "Publicaciones denunciadas",
      note: "Revisar reportes y tomar acciones.",
    },
    {
      key: "reported_profiles",
      icon: "🧾",
      title: "Perfiles denunciados",
      note: "Validar perfiles y resolver apelaciones.",
    },
    {
      key: "wish_management",
      icon: "🪄",
      title: "Gestión de deseos",
      note: "Solicitudes: “Yo puedo cumplir este deseo”.",
    },
    {
      key: "rank_management",
      icon: "🛡️",
      title: "Gestión de Rangos",
      note: "Buscar por @id y subir nivel de Guardián sin saltos.",
    },
    {
      key: "messaging",
      icon: "💬",
      title: "Mensajería",
      note: "Conversaciones y coordinación con usuarios.",
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
    if (value === "open") return "Abierta";
    if (value === "in_progress") return "Compromiso sellado";
    if (value === "closed") {
      return request?.denied_at ? "Denegada" : "Deseo completado";
    }
    return value || "Desconocida";
  };

  const formatDateTime = (value) => {
    try {
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return "";
      return date.toLocaleString();
    } catch {
      return "";
    }
  };

  const formatReportStatusLabel = (item) => {
    const value = String(item?.status || "").toLowerCase();
    if (value === "open") return "Pendiente";
    if (value === "kept") return "Conservada";
    if (value === "deleted") return "Eliminada";
    return value || "Desconocida";
  };

  const formatReportReasonLabel = (reason, otherReason = "") => {
    const value = String(reason || "").toLowerCase();
    if (value === "violent") return "Contenido violento o perturbador";
    if (value === "divisive") return "Promueve confrontación o división excesiva";
    if (value === "sexual") return "Contenido sexual explícito o inapropiado";
    if (value === "other") {
      const note = String(otherReason || "").trim();
      return note ? `Otra razón: ${note}` : "Otra razón";
    }
    return value || "Razón no especificada";
  };

  const formatProfileReportStatusLabel = (item) => {
    const value = String(item?.status || "").toLowerCase();
    if (value === "open") return "Pendiente";
    if (value === "reviewed") return "Revisado";
    return value || "Desconocida";
  };

  const formatAccountModerationStatusLabel = (value) => {
    const status = String(value || "").toLowerCase();
    if (status === "suspended") return "Cuenta suspendida";
    if (status === "closed") return "Cuenta cerrada";
    return "Cuenta activa";
  };

  const formatProfileReportReasonLabel = (reason, otherReason = "") => {
    const value = String(reason || "").toLowerCase();
    if (value === "fake_or_illegal") return "Perfil falso o contenido ilegal";
    if (value === "external_manipulation")
      return "Manipulación hacia otros usuarios en la vida real a través de medios externos";
    if (value === "star_manipulation") return "Abuso de publicaciones para atraer estrellas";
    if (value === "abusive_or_coercive") return "Conducta abusiva o coercitiva";
    if (value === "wish_system_abuse") return "Uso indebido del sistema de deseos";
    if (value === "safety_risk") return "Riesgo para la seguridad de otros";
    if (value === "other") {
      const note = String(otherReason || "").trim();
      return note ? `Otro: ${note}` : "Otro";
    }
    return value || "Razón no especificada";
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
      rankLookupError = "Escribe un @id o @username para buscar.";
      return;
    }

    rankLookupLoading = true;
    try {
      const res = await apiFetch(
        `/guardian-center/rank-management/user?query=${encodeURIComponent(query)}`
      );
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo encontrar el usuario.");
      }
      rankLookupResult = data || null;
      if (!rankLookupResult?.user_id) {
        throw new Error("Respuesta inválida al cargar el usuario.");
      }
    } catch (err) {
      rankLookupError = err?.message || "No se pudo encontrar el usuario.";
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
        throw new Error(data.detail || "No se pudo promover el rango.");
      }

      const updatedTarget = data?.target || null;
      if (!updatedTarget?.user_id) {
        throw new Error("Respuesta inválida al promover el usuario.");
      }
      rankLookupResult = updatedTarget;
      if (updatedTarget.is_self) {
        guardianRank = Number(updatedTarget.guardian_rank || guardianRank) || guardianRank;
      }
      closePromoteRankModal();
    } catch (err) {
      rankPromoteError = err?.message || "No se pudo promover el rango.";
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
    ownerMessageSubject = "Confirmación previa antes de congelar tu deseo";
    ownerMessageBody =
      "Hay una persona interesada en cumplir este deseo. Antes de congelarlo y continuar el proceso interno de Kiadez, necesito confirmar contigo si alguien cercano ya lo está gestionando fuera de la red social.";
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
        throw new Error(data.detail || "No se pudieron cargar las solicitudes.");
      }
      wishRequestsItems = Array.isArray(data?.items) ? data.items : [];
      wishRequestsTotalPages = Math.max(1, Number(data?.total_pages || 1));
      wishRequestsPage = Math.max(1, Math.min(Number(data?.page || requestedPage), wishRequestsTotalPages));
    } catch (err) {
      wishRequestsError = err?.message || "No se pudieron cargar las solicitudes.";
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
        throw new Error(data.detail || "No se pudieron cargar las publicaciones denunciadas.");
      }
      reportedPostsItems = Array.isArray(data?.items) ? data.items : [];
      reportedPostsTotalPages = Math.max(1, Number(data?.total_pages || 1));
      reportedPostsPage = Math.max(1, Math.min(Number(data?.page || requestedPage), reportedPostsTotalPages));
    } catch (err) {
      reportedPostsError = err?.message || "No se pudieron cargar las publicaciones denunciadas.";
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
        throw new Error(data.detail || "No se pudieron cargar los perfiles denunciados.");
      }
      const nextItems = Array.isArray(data?.items) ? data.items : [];
      reportedProfilesItems = nextItems.map((item) => normalizeReportedProfileItem(item));
      reportedProfilesTotalPages = Math.max(1, Number(data?.total_pages || 1));
      reportedProfilesPage = Math.max(1, Math.min(Number(data?.page || requestedPage), reportedProfilesTotalPages));
    } catch (err) {
      reportedProfilesError = err?.message || "No se pudieron cargar los perfiles denunciados.";
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
        throw new Error(data.detail || "No se pudieron cargar las publicaciones denunciadas de este perfil.");
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
                err?.message || "No se pudieron cargar las publicaciones denunciadas de este perfil.",
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
        throw new Error(data.detail || "No se pudo sellar el compromiso.");
      }
      updateWishRequestItem(data);
      closeSealCommitmentModal();
    } catch (err) {
      actionError = err?.message || "No se pudo sellar el compromiso.";
    } finally {
      actionLoading = false;
    }
  };

  const denyRequest = async () => {
    if (!activeWishRequest?.id || actionLoading) return;

    denySubjectError = !String(denySubject || "").trim();
    denyBodyError = !String(denyBody || "").trim();
    if (denySubjectError || denyBodyError) {
      actionError = "Debes completar asunto y mensaje para denegar la petición.";
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
        throw new Error(data.detail || "No se pudo denegar la petición.");
      }
      updateWishRequestItem(data);
      closeDenyModal();
    } catch (err) {
      actionError = err?.message || "No se pudo denegar la petición.";
    } finally {
      actionLoading = false;
    }
  };

  const sendOwnerMessage = async () => {
    if (!activeWishRequest?.id || actionLoading) return;

    ownerMessageSubjectError = !String(ownerMessageSubject || "").trim();
    ownerMessageBodyError = !String(ownerMessageBody || "").trim();
    if (ownerMessageSubjectError || ownerMessageBodyError) {
      actionError = "Debes completar asunto y mensaje para enviar la notificación.";
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
        throw new Error(data.detail || "No se pudo enviar el mensaje.");
      }
      showUiAlert(`Mensaje enviado a ${data?.recipient_handle || ownerMessageToHandle}.`, { type: "success" });
      closeOwnerMessageModal();
    } catch (err) {
      actionError = err?.message || "No se pudo enviar el mensaje.";
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
        throw new Error(data.detail || "No se pudo eliminar la publicación denunciada.");
      }
      updateReportedPostItem(data);
      closeDeleteReportedPostModal();
    } catch (err) {
      reportedPostsActionError = err?.message || "No se pudo eliminar la publicación denunciada.";
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
        throw new Error(data.detail || "No se pudo conservar la publicación reportada.");
      }
      updateReportedPostItem(data);
      closeKeepReportedPostModal();
    } catch (err) {
      reportedPostsActionError = err?.message || "No se pudo conservar la publicación reportada.";
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
    runReportedProfileAccountAction("suspend-account", "No se pudo suspender la cuenta.");

  const enableReportedProfileAccount = async () =>
    runReportedProfileAccountAction("enable-account", "No se pudo habilitar la cuenta.");

  const closeReportedProfileAccount = async () =>
    runReportedProfileAccountAction("close-account", "No se pudo cerrar la cuenta.");

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
          throw new Error(data.detail || "No se pudo cargar tu perfil.");
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
        loadError = err?.message || "No se pudo cargar el Centro del Guardián.";
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
  <title>Kiadez — Centro del Guardián</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background settings-page guardian-center-page">
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
      <details class="topbar-dropdown" id="profileDropdown">
        <summary class="topbar-avatar-btn" aria-label="Perfil del usuario">
          <img src="/assets/avatar-default.jpg" alt="Perfil de usuario" />
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
          <a href="/home_user.html" role="menuitem">Mi Home</a>
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
    <div class="home-body settings-body guardian-center-body">
      <section class="panel guardian-center-panel" aria-label="Centro del Guardián">
        <div class="panel-head guardian-center-head">
          <div>
            <h2 class="panel-title">Centro del Guardián</h2>
            <p class="panel-muted guardian-center-subtitle">
              Escenario de autoridad para Guardianes. Aquí se gestionan reportes, solicitudes y coordinación.
            </p>
          </div>
          <span class="panel-badge">
            {#if isLoading}
              Cargando...
            {:else if isGuardian}
              Guardián · Rango {guardianRank}
            {:else}
              Acceso restringido
            {/if}
          </span>
        </div>

        {#if loadError}
          <div class="guardian-center-empty is-error">{loadError}</div>
        {:else if isLoading}
          <div class="guardian-center-empty">Cargando tu autorización...</div>
        {:else if !isGuardian}
          <div class="guardian-center-lock">
            <p class="guardian-center-lock-text">
              Este módulo está disponible solo para usuarios con rango de Guardián (Rango {GUARDIAN_REQUIRED_RANK}).
            </p>
            <div class="guardian-center-lock-actions">
              <a class="btn btn-outline btn-compact" href="/guardians-rank.html">Ver rangos</a>
              <a class="btn btn-primary btn-compact" href="/be-a-guardian.html">Ser Guardián</a>
            </div>
          </div>
        {:else}
          <div class="settings-actions guardian-center-actions" aria-label="Módulos del Guardián">
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
                <span class="guardian-center-cta" aria-hidden="true">Abrir</span>
              </button>
            {/each}
          </div>

          <div class="guardian-center-divider" aria-hidden="true"></div>

          {@const activeModule = getActiveModule()}
          <section class="guardian-center-module" aria-label={activeModule.title}>
            <div class="guardian-center-module-head">
              <h3 class="guardian-center-module-title">{activeModule.title}</h3>
              {#if activeModuleKey === "wish_management" || activeModuleKey === "reported_posts" || activeModuleKey === "reported_profiles" || activeModuleKey === "rank_management"}
                <span class="guardian-center-module-pill">En vivo</span>
              {:else}
                <span class="guardian-center-module-pill">Próximamente</span>
              {/if}
            </div>

            {#if activeModuleKey === "wish_management"}
              <p class="panel-muted guardian-center-module-note">
                Solicitudes generadas desde “Yo puedo cumplir ese deseo”. Usa el botón “Ver deseo” para ir al deseo exacto.
              </p>
            {:else if activeModuleKey === "reported_posts"}
              <p class="panel-muted guardian-center-module-note">
                Denuncias de publicaciones recibidas en tiempo real. Revisa el reporte y decide si se conserva o se elimina la publicación.
              </p>
            {:else if activeModuleKey === "reported_profiles"}
              <p class="panel-muted guardian-center-module-note">
                Denuncias de perfiles recibidas en tiempo real, con las publicaciones denunciadas asociadas a cada usuario.
              </p>
            {:else if activeModuleKey === "rank_management"}
              <p class="panel-muted guardian-center-module-note">
                Busca usuarios por <strong>@id</strong> o <strong>@username</strong>, revisa su rango actual y promuévelos al siguiente nivel sin saltos.
              </p>
            {:else}
              <p class="panel-muted guardian-center-module-note">
                Este módulo está listo en interfaz. Mañana lo conectamos con base de datos y lógica real.
              </p>
            {/if}

            {#if activeModuleKey === "wish_management"}
              {#if wishRequestsError}
                <div class="guardian-center-empty is-error">{wishRequestsError}</div>
              {:else if wishRequestsLoading}
                <div class="guardian-center-empty">Cargando solicitudes...</div>
              {:else if !wishRequestsItems.length}
                <div class="guardian-center-empty">No hay solicitudes por ahora.</div>
              {:else}
                <div class="guardian-wish-requests" aria-label="Solicitudes recibidas">
                  {#each wishRequestsItems as req (req.id)}
                    <article class="guardian-wish-card">
                      <header class="guardian-wish-card-head">
                        <div class="guardian-wish-card-title">{req.wish_text}</div>
                        <div class="guardian-wish-card-status">{formatStatusLabel(req)}</div>
                      </header>

                      <div class="guardian-wish-card-meta">
                        <span>Solicitud #{req.id}</span>
                        <span aria-hidden="true">·</span>
                        <span>{formatDateTime(req.created_at)}</span>
                        <span aria-hidden="true">·</span>
                        <span>Tipo: {req.wish_type}</span>
                        {#if req.commitment_code}
                          <span aria-hidden="true">·</span>
                          <span class="guardian-wish-commitment-code">{req.commitment_code}</span>
                        {/if}
                      </div>

                      <div class="guardian-wish-card-actions">
                        <a class="btn btn-outline btn-compact" href={req.wish_url} target="_blank" rel="noopener noreferrer">
                          Ver deseo
                        </a>
                        <a class="btn btn-outline btn-compact" href={req.requester.profile_url} target="_blank" rel="noopener noreferrer">
                          Ver solicitante
                        </a>
                        <a class="btn btn-outline btn-compact" href={req.wish_owner.profile_url} target="_blank" rel="noopener noreferrer">
                          Ver dueño del deseo
                        </a>
                        <button
                          class="btn btn-primary btn-compact"
                          type="button"
                          disabled={actionLoading || req.status === "closed" || Boolean(req.commitment_code)}
                          on:click={() => openSealCommitmentModal(req)}
                        >
                          {req.commitment_code ? "Compromiso sellado" : "Sellar compromiso"}
                        </button>
                        <button
                          class="btn btn-outline btn-compact guardian-btn-deny"
                          type="button"
                          disabled={actionLoading || req.status === "closed"}
                          on:click={() => openDenyModal(req)}
                        >
                          Denegar petición
                        </button>
                      </div>

                      <div class="guardian-wish-card-body">
                        <div class="guardian-wish-field">
                          <div class="guardian-wish-label">Solicitante</div>
                          <div class="guardian-wish-value">
                            {req.requester.full_name}
                            <span class="guardian-wish-handle">{req.requester.handle}</span>
                          </div>
                        </div>

                        <div class="guardian-wish-field">
                          <div class="guardian-wish-label">Dueño del deseo</div>
                          <div class="guardian-wish-value guardian-wish-owner-row">
                            {req.wish_owner.full_name}
                            <span class="guardian-wish-handle">{req.wish_owner.handle}</span>
                            <button
                              class="guardian-owner-message-btn"
                              type="button"
                              title="Enviar mensaje al dueño del deseo"
                              aria-label="Enviar mensaje al dueño del deseo"
                              disabled={actionLoading || req.status === "closed"}
                              on:click={() => openOwnerMessageModal(req)}
                            >
                              ✉️
                            </button>
                          </div>
                        </div>

                        {#if req.commitment_code}
                          <div class="guardian-wish-field guardian-wish-field-commitment">
                            <div class="guardian-wish-label">Código de compromiso</div>
                            <div class="guardian-wish-value">
                              <strong>{req.commitment_code}</strong>
                              {#if req.commitment_sealed_at}
                                <span class="guardian-wish-commitment-date">
                                  · Sellado: {formatDateTime(req.commitment_sealed_at)}
                                </span>
                              {/if}
                            </div>
                          </div>
                        {/if}

                        {#if req.guardian}
                          <div class="guardian-wish-field">
                            <div class="guardian-wish-label">Guardián asignado</div>
                            <div class="guardian-wish-value">
                              {req.guardian.full_name}
                              <span class="guardian-wish-handle">{req.guardian.handle}</span>
                            </div>
                          </div>
                        {/if}

                        <div class="guardian-wish-field">
                          <div class="guardian-wish-label">Motivo</div>
                          <div class="guardian-wish-value guardian-wish-reason">{req.reason}</div>
                        </div>

                        <div class="guardian-wish-field guardian-wish-contact">
                          <div class="guardian-wish-label">Contacto</div>
                          <div class="guardian-wish-value">
                            <div>{req.contact_phone}</div>
                            <div>{req.contact_email}</div>
                          </div>
                        </div>

                        <div class="guardian-wish-field">
                          <div class="guardian-wish-label">Evidencia</div>
                          <div class="guardian-wish-value">
                            {#if req.evidence_url}
                              {#if req.evidence_mime_type && req.evidence_mime_type.startsWith("image/")}
                                <a
                                  class="guardian-wish-evidence-link"
                                  href={req.evidence_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  aria-label="Abrir evidencia (imagen)"
                                >
                                  <img class="guardian-wish-evidence-img" src={req.evidence_url} alt="Evidencia adjunta" />
                                </a>
                              {:else if req.evidence_mime_type && req.evidence_mime_type.startsWith("video/")}
                                <video class="guardian-wish-evidence-video" src={req.evidence_url} controls preload="metadata"></video>
                              {:else}
                                <a class="btn btn-outline btn-compact" href={req.evidence_url} target="_blank" rel="noopener noreferrer">
                                  Ver evidencia
                                </a>
                              {/if}
                            {:else}
                              <span class="panel-muted">No disponible.</span>
                            {/if}
                          </div>
                        </div>
                      </div>
                    </article>
                  {/each}
                </div>

                <div class="guardian-wish-pagination" aria-label="Paginación de solicitudes">
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={wishRequestsLoading || wishRequestsPage <= 1}
                    on:click={() => loadWishRequests(wishRequestsPage - 1)}
                  >
                    Anterior
                  </button>
                  <span class="guardian-wish-page">{wishRequestsPage} / {wishRequestsTotalPages}</span>
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={wishRequestsLoading || wishRequestsPage >= wishRequestsTotalPages}
                    on:click={() => loadWishRequests(wishRequestsPage + 1)}
                  >
                    Siguiente
                  </button>
                </div>
              {/if}
            {:else if activeModuleKey === "reported_posts"}
              {#if reportedPostsError}
                <div class="guardian-center-empty is-error">{reportedPostsError}</div>
              {:else if reportedPostsLoading}
                <div class="guardian-center-empty">Cargando publicaciones denunciadas...</div>
              {:else if !reportedPostsItems.length}
                <div class="guardian-center-empty">No hay publicaciones denunciadas por ahora.</div>
              {:else}
                <div class="guardian-reported-posts" aria-label="Publicaciones denunciadas">
                  {#each reportedPostsItems as item (item.id)}
                    {@const statusLabel = formatReportStatusLabel(item)}
                    <article class="guardian-reported-card">
                      <header class="guardian-reported-head">
                        <div class="guardian-reported-title-wrap">
                          <div class="guardian-reported-title">Caso #{item.id}</div>
                          <div class="guardian-reported-meta">
                            <span>Reportes: {item.report_count}</span>
                            <span aria-hidden="true">·</span>
                            <span>Primero: {formatDateTime(item.first_reported_at)}</span>
                            <span aria-hidden="true">·</span>
                            <span>Último: {formatDateTime(item.last_reported_at)}</span>
                          </div>
                        </div>
                        <span class={`guardian-reported-status is-${String(item.status || "").toLowerCase()}`}>{statusLabel}</span>
                      </header>

                      <div class="guardian-reported-body">
                        <div class="guardian-reported-field">
                          <div class="guardian-wish-label">Autor de la publicación</div>
                          <div class="guardian-wish-value">
                            {item.post_author.full_name}
                            <span class="guardian-wish-handle">{item.post_author.handle}</span>
                          </div>
                        </div>

                        <div class="guardian-reported-field">
                          <div class="guardian-wish-label">Publicación reportada</div>
                          <div class="guardian-reported-text">
                            {#if item.post_text}
                              {item.post_text}
                            {:else}
                              <span class="panel-muted">Sin texto.</span>
                            {/if}
                          </div>
                          {#if item.post_media_url}
                            <div class="guardian-reported-media-wrap">
                              {#if item.post_media_kind && item.post_media_kind.startsWith("video")}
                                <video class="guardian-reported-media" src={item.post_media_url} controls preload="metadata"></video>
                              {:else}
                                <a href={item.post_media_url} target="_blank" rel="noopener noreferrer" class="guardian-reported-media-link">
                                  <img class="guardian-reported-media" src={item.post_media_url} alt="Media de la publicación denunciada" />
                                </a>
                              {/if}
                            </div>
                          {/if}
                        </div>

                        {#if item.reports?.length}
                          <div class="guardian-reported-field">
                            <div class="guardian-wish-label">Últimos reportes</div>
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
                            <div class="guardian-wish-label">Última decisión</div>
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
                          Ver perfil
                        </a>
                        <button
                          class="btn btn-primary btn-compact"
                          type="button"
                          disabled={reportedPostsActionLoading || item.status === "deleted" || !item.post_id}
                          on:click={() => openDeleteReportedPostModal(item)}
                        >
                          Eliminar publicación
                        </button>
                        <button
                          class="btn btn-outline btn-compact"
                          type="button"
                          disabled={reportedPostsActionLoading || item.status === "kept"}
                          on:click={() => openKeepReportedPostModal(item)}
                        >
                          Conservar publicación
                        </button>
                      </div>
                    </article>
                  {/each}
                </div>

                <div class="guardian-wish-pagination" aria-label="Paginación de publicaciones denunciadas">
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={reportedPostsLoading || reportedPostsPage <= 1}
                    on:click={() => loadReportedPosts(reportedPostsPage - 1)}
                  >
                    Anterior
                  </button>
                  <span class="guardian-wish-page">{reportedPostsPage} / {reportedPostsTotalPages}</span>
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={reportedPostsLoading || reportedPostsPage >= reportedPostsTotalPages}
                    on:click={() => loadReportedPosts(reportedPostsPage + 1)}
                  >
                    Siguiente
                  </button>
                </div>
              {/if}
            {:else if activeModuleKey === "reported_profiles"}
              {#if reportedProfilesError}
                <div class="guardian-center-empty is-error">{reportedProfilesError}</div>
              {:else if reportedProfilesLoading}
                <div class="guardian-center-empty">Cargando perfiles denunciados...</div>
              {:else if !reportedProfilesItems.length}
                <div class="guardian-center-empty">No hay perfiles denunciados por ahora.</div>
              {:else}
                <div class="guardian-reported-posts guardian-reported-profiles" aria-label="Perfiles denunciados">
                  {#each reportedProfilesItems as item (item.id)}
                    {@const statusLabel = formatProfileReportStatusLabel(item)}
                    {@const postsData = item.reported_posts || { items: [], page: 1, total_pages: 1, total: 0, range_start: 0, range_end: 0 }}
                    <article class="guardian-reported-card guardian-reported-profile-card">
                      <header class="guardian-reported-head">
                        <div class="guardian-reported-title-wrap">
                          <div class="guardian-reported-title">Caso de perfil #{item.id}</div>
                          <div class="guardian-reported-meta">
                            <span>Reportes: {item.report_count}</span>
                            <span aria-hidden="true">·</span>
                            <span>Primero: {formatDateTime(item.first_reported_at)}</span>
                            <span aria-hidden="true">·</span>
                            <span>Último: {formatDateTime(item.last_reported_at)}</span>
                          </div>
                        </div>
                        <span class={`guardian-reported-status is-${String(item.status || "").toLowerCase()}`}>{statusLabel}</span>
                      </header>

                      <div class="guardian-reported-body">
                        <div class="guardian-reported-field">
                          <div class="guardian-wish-label">Usuario denunciado</div>
                          <div class="guardian-wish-value">
                            {item.reported_user.full_name}
                            <span class="guardian-wish-handle">{item.reported_user.handle}</span>
                          </div>
                        </div>

                        <div class="guardian-reported-field">
                          <div class="guardian-wish-label">Estado de la cuenta</div>
                          <div class="guardian-wish-value">
                            <span class={`guardian-reported-status is-${String(item.account_moderation_status || "active").toLowerCase()}`}>
                              {formatAccountModerationStatusLabel(item.account_moderation_status)}
                            </span>
                            {#if item.account_moderated_by_guardian}
                              <span class="guardian-wish-handle">
                                · por {item.account_moderated_by_guardian.handle}
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
                            <div class="guardian-wish-label">Últimos reportes de perfil</div>
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
                            <div class="guardian-wish-label">Publicaciones denunciadas</div>
                            <span class="guardian-reported-profile-posts-counter">{Number(postsData.total || 0)} / {Number(postsData.total || 0)}</span>
                          </div>

                          {#if item.reported_posts_error}
                            <div class="guardian-center-empty is-error">{item.reported_posts_error}</div>
                          {:else if item.reported_posts_loading}
                            <div class="guardian-center-empty">Cargando publicaciones denunciadas del perfil...</div>
                          {:else if !postsData.items?.length}
                            <p class="panel-muted">0/0. Este usuario está limpio en publicaciones denunciadas.</p>
                          {:else}
                            <div class="guardian-reported-profile-post-list">
                              {#each postsData.items as postCase (postCase.id)}
                                <article class="guardian-reported-profile-post-item">
                                  <div class="guardian-reported-profile-post-main">
                                    <div class="guardian-reported-profile-post-title">
                                      Caso #{postCase.id} · Reportes: {postCase.report_count}
                                    </div>
                                    <div class="guardian-reported-profile-post-meta">
                                      Último reporte: {formatDateTime(postCase.last_reported_at)}
                                    </div>
                                    {#if postCase.post_text}
                                      <div class="guardian-reported-text">{postCase.post_text}</div>
                                    {/if}
                                  </div>
                                  <div class="guardian-reported-profile-post-actions">
                                    {#if postCase.post_url}
                                      <a class="btn btn-outline btn-compact" href={postCase.post_url} target="_blank" rel="noopener noreferrer">
                                        Ver publicación
                                      </a>
                                    {:else}
                                      <span class="panel-muted">Publicación no disponible.</span>
                                    {/if}
                                  </div>
                                </article>
                              {/each}
                            </div>
                          {/if}

                          {#if Number(postsData.total_pages || 1) > 1}
                            <div class="guardian-wish-pagination guardian-reported-profile-post-pagination" aria-label={`Paginación de publicaciones denunciadas del caso ${item.id}`}>
                              <button
                                class="btn btn-outline btn-compact"
                                type="button"
                                disabled={item.reported_posts_loading || Number(postsData.page || 1) <= 1}
                                on:click={() => loadReportedProfilePostsPage(item.id, Number(postsData.page || 1) - 1)}
                              >
                                Anterior
                              </button>
                              <span class="guardian-wish-page">{Number(postsData.page || 1)} / {Number(postsData.total_pages || 1)}</span>
                              <button
                                class="btn btn-outline btn-compact"
                                type="button"
                                disabled={item.reported_posts_loading || Number(postsData.page || 1) >= Number(postsData.total_pages || 1)}
                                on:click={() => loadReportedProfilePostsPage(item.id, Number(postsData.page || 1) + 1)}
                              >
                                Siguiente
                              </button>
                            </div>
                          {/if}
                        </div>

                        {#if item.resolved_by_guardian}
                          <div class="guardian-reported-field">
                            <div class="guardian-wish-label">Última revisión</div>
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
                          Suspender cuenta
                        </button>
                        <button
                          class="btn btn-outline btn-compact"
                          type="button"
                          disabled={reportedProfilesActionLoading || !item.can_enable_account}
                          on:click={() => openEnableReportedProfileModal(item)}
                        >
                          Habilitar cuenta
                        </button>
                        <button
                          class="btn btn-primary btn-compact"
                          type="button"
                          disabled={reportedProfilesActionLoading || !item.can_close_account}
                          on:click={() => openCloseReportedProfileModal(item)}
                        >
                          Cerrar cuenta
                        </button>
                        <a class="btn btn-outline btn-compact" href={item.reported_user.profile_url} target="_blank" rel="noopener noreferrer">
                          Ver perfil
                        </a>
                      </div>
                    </article>
                  {/each}
                </div>

                <div class="guardian-wish-pagination" aria-label="Paginación de perfiles denunciados">
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={reportedProfilesLoading || reportedProfilesPage <= 1}
                    on:click={() => loadReportedProfiles(reportedProfilesPage - 1)}
                  >
                    Anterior
                  </button>
                  <span class="guardian-wish-page">{reportedProfilesPage} / {reportedProfilesTotalPages}</span>
                  <button
                    class="btn btn-outline btn-compact"
                    type="button"
                    disabled={reportedProfilesLoading || reportedProfilesPage >= reportedProfilesTotalPages}
                    on:click={() => loadReportedProfiles(reportedProfilesPage + 1)}
                  >
                    Siguiente
                  </button>
                </div>
              {/if}
            {:else if activeModuleKey === "rank_management"}
              <section class="guardian-rank-manager" aria-label="Gestión de rangos">
                <form
                  class="guardian-rank-search"
                  on:submit|preventDefault={searchRankUser}
                >
                  <label class="modal-label guardian-rank-label" for="rankLookupQuery">
                    Usuario objetivo (@id o @username)
                  </label>
                  <div class="guardian-rank-search-row">
                    <input
                      id="rankLookupQuery"
                      class="modal-input guardian-rank-input"
                      type="text"
                      placeholder="@id12 o @carlosjduarte"
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
                      {rankLookupLoading ? "Buscando..." : "Buscar usuario"}
                    </button>
                  </div>
                  <p class="panel-muted guardian-rank-search-hint">
                    El ascenso siempre será de nivel en nivel hasta máximo Rango {GUARDIAN_MAX_RANK}.
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
                          <span>Rol: {rankLookupResult.role}</span>
                        </div>
                      </div>
                      <a
                        class="btn btn-outline btn-compact"
                        href={rankLookupResult.profile_url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        Ver perfil
                      </a>
                    </header>

                    <div class="guardian-rank-grid">
                      <div class="guardian-rank-slot">
                        <div class="guardian-wish-label">Rango actual</div>
                        <div class="guardian-rank-value">
                          Nivel {rankLookupResult.guardian_rank} · {rankLookupResult.guardian_rank_name}
                        </div>
                      </div>
                      <div class="guardian-rank-slot">
                        <div class="guardian-wish-label">Siguiente nivel</div>
                        <div class="guardian-rank-value">
                          {#if rankLookupResult.next_guardian_rank !== null && rankLookupResult.next_guardian_rank !== undefined}
                            Nivel {rankLookupResult.next_guardian_rank} · {rankLookupResult.next_guardian_rank_name}
                          {:else}
                            Rango máximo alcanzado
                          {/if}
                        </div>
                      </div>
                    </div>

                    {#if rankLookupResult.is_self}
                      <p class="panel-muted guardian-rank-self-note">
                        Este usuario corresponde a tu propia cuenta.
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
                          Promoviendo...
                        {:else if rankLookupResult.can_promote}
                          Subir al siguiente nivel
                        {:else}
                          Rango máximo alcanzado
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
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label="Sellar compromiso">
      <div class="modal-head guardian-center-modal-head">
        <h3>Sellar compromiso</h3>
      </div>
      <div class="modal-body">
        <p class="panel-muted">
          ¿Te aseguraste de seguir el protocolo previo para que esta gestión se complete de acuerdo a las políticas internas de Kiadez.com?
        </p>
        {#if actionError}
          <div class="wish-error is-visible">{actionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={actionLoading} on:click={sealCommitment}>
          {actionLoading ? "Procesando..." : "Sí"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={actionLoading} on:click={closeSealCommitmentModal}>
          No
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
    <div class="modal wish-modal guardian-center-modal guardian-center-mail-modal" role="dialog" aria-modal="true" aria-label="Denegar petición">
      <div class="modal-head guardian-center-modal-head">
        <h3>Denegar petición</h3>
      </div>
      <div class="modal-body">
        <label class="modal-label" for="denyToHandle">Para</label>
        <input id="denyToHandle" class="modal-input guardian-center-readonly" type="text" readonly value={denyToHandle} />

        <label class="modal-label" for="denySubject">Asunto</label>
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

        <label class="modal-label" for="denyBody">Mensaje</label>
        <textarea
          id="denyBody"
          class="modal-textarea guardian-center-mail-textarea"
          class:is-error={denyBodyError}
          rows="6"
          placeholder={`Explica aquí por qué la petición fue denegada.\n\nAtentamente,\nGuardián – Rango ${guardianRank}\nKiadez.com`}
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
          {actionLoading ? "Enviando..." : "Enviar denegación"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={actionLoading} on:click={closeDenyModal}>
          Cancelar
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
    <div class="modal wish-modal guardian-center-modal guardian-center-mail-modal guardian-center-owner-mail-modal" role="dialog" aria-modal="true" aria-label="Mensaje al dueño del deseo">
      <div class="modal-head guardian-center-modal-head">
        <h3>Mensaje al dueño del deseo</h3>
      </div>
      <div class="modal-body">
        <label class="modal-label" for="ownerMessageToHandle">Para</label>
        <input
          id="ownerMessageToHandle"
          class="modal-input guardian-center-readonly"
          type="text"
          readonly
          value={ownerMessageToHandle}
        />

        <label class="modal-label" for="ownerMessageSubject">Asunto</label>
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

        <label class="modal-label" for="ownerMessageBody">Mensaje</label>
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
          {actionLoading ? "Enviando..." : "Enviar mensaje"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={actionLoading} on:click={closeOwnerMessageModal}>
          Cancelar
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
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label="Eliminar publicación denunciada">
      <div class="modal-head guardian-center-modal-head">
        <h3>Eliminar publicación denunciada</h3>
      </div>
      <div class="modal-body">
        <p class="panel-muted">
          Esta acción eliminará la publicación reportada y dejará registro en el historial del usuario.
        </p>
        {#if activeReportedPost?.post_author}
          <p>
            Autor: <strong>{activeReportedPost.post_author.full_name}</strong>
            <span class="guardian-wish-handle">{activeReportedPost.post_author.handle}</span>
          </p>
        {/if}
        {#if reportedPostsActionError}
          <div class="wish-error is-visible">{reportedPostsActionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={reportedPostsActionLoading} on:click={deleteReportedPost}>
          {reportedPostsActionLoading ? "Procesando..." : "Eliminar"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={reportedPostsActionLoading} on:click={closeDeleteReportedPostModal}>
          Cancelar
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
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label="Conservar publicación reportada">
      <div class="modal-head guardian-center-modal-head">
        <h3>Conservar publicación reportada</h3>
      </div>
      <div class="modal-body">
        <p class="panel-muted">
          Marcarás este caso como revisado y la publicación permanecerá visible.
        </p>
        {#if activeReportedPost?.post_author}
          <p>
            Autor: <strong>{activeReportedPost.post_author.full_name}</strong>
            <span class="guardian-wish-handle">{activeReportedPost.post_author.handle}</span>
          </p>
        {/if}
        {#if reportedPostsActionError}
          <div class="wish-error is-visible">{reportedPostsActionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={reportedPostsActionLoading} on:click={keepReportedPost}>
          {reportedPostsActionLoading ? "Procesando..." : "Conservar"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={reportedPostsActionLoading} on:click={closeKeepReportedPostModal}>
          Cancelar
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
    <div class="modal wish-modal guardian-center-modal guardian-rank-promote-modal" role="dialog" aria-modal="true" aria-label="Confirmar ascenso de rango">
      <div class="modal-head guardian-center-modal-head">
        <h3>Confirmar ascenso de rango</h3>
      </div>
      <div class="modal-body">
        {#if rankLookupResult}
          <p>
            ¿Estás seguro que quieres subir a
            <strong> {rankLookupResult.full_name}</strong>
            ({rankLookupResult.handle})
            al
            <strong>
              nivel {rankLookupResult.next_guardian_rank} ({rankLookupResult.next_guardian_rank_name})
            </strong>
            ?
          </p>
          <p class="panel-muted">
            Rango actual: Nivel {rankLookupResult.guardian_rank} ({rankLookupResult.guardian_rank_name}).
          </p>
        {:else}
          <p class="panel-muted">No hay usuario seleccionado.</p>
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
          {rankPromoteLoading ? "Procesando..." : "Sí, subir nivel"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={rankPromoteLoading} on:click={closePromoteRankModal}>
          Cancelar
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
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label="Suspender cuenta reportada">
      <div class="modal-head guardian-center-modal-head">
        <h3>Suspender cuenta</h3>
      </div>
      <div class="modal-body">
        {#if activeReportedProfile}
          <p>
            ¿Estás seguro que quieres suspender la cuenta de
            <strong> {activeReportedProfile.reported_user?.full_name}</strong>
            ({activeReportedProfile.reported_user?.handle})?
          </p>
          <p class="panel-muted">
            La suspensión no expira por tiempo. Solo un Guardián podrá habilitarla manualmente.
          </p>
        {:else}
          <p class="panel-muted">No hay perfil seleccionado.</p>
        {/if}

        {#if reportedProfilesActionError}
          <div class="wish-error is-visible">{reportedProfilesActionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={suspendReportedProfileAccount}>
          {reportedProfilesActionLoading ? "Procesando..." : "Sí, suspender"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={closeSuspendReportedProfileModal}>
          Cancelar
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
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label="Habilitar cuenta reportada">
      <div class="modal-head guardian-center-modal-head">
        <h3>Habilitar cuenta</h3>
      </div>
      <div class="modal-body">
        {#if activeReportedProfile}
          <p>
            ¿Estas seguro que quieres habilitar cuenta?
          </p>
          <p class="panel-muted">
            Usuario: <strong>{activeReportedProfile.reported_user?.full_name}</strong>
            <span class="guardian-wish-handle">{activeReportedProfile.reported_user?.handle}</span>
          </p>
        {:else}
          <p class="panel-muted">No hay perfil seleccionado.</p>
        {/if}

        {#if reportedProfilesActionError}
          <div class="wish-error is-visible">{reportedProfilesActionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={enableReportedProfileAccount}>
          {reportedProfilesActionLoading ? "Procesando..." : "Sí, habilitar"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={closeEnableReportedProfileModal}>
          Cancelar
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
    <div class="modal wish-modal guardian-center-modal" role="dialog" aria-modal="true" aria-label="Cerrar cuenta reportada">
      <div class="modal-head guardian-center-modal-head">
        <h3>Cerrar cuenta</h3>
      </div>
      <div class="modal-body">
        {#if activeReportedProfile}
          <p>
            ¿Estas seguro que quieres cerrar cuenta de
            <strong> {activeReportedProfile.reported_user?.full_name}</strong>
            ({activeReportedProfile.reported_user?.handle})?
          </p>
          <p class="panel-muted">
            Esta decisión es definitiva. La cuenta quedará cerrada de forma permanente y no podrá habilitarse.
          </p>
        {:else}
          <p class="panel-muted">No hay perfil seleccionado.</p>
        {/if}

        {#if reportedProfilesActionError}
          <div class="wish-error is-visible">{reportedProfilesActionError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={closeReportedProfileAccount}>
          {reportedProfilesActionLoading ? "Procesando..." : "Sí, cerrar cuenta"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={reportedProfilesActionLoading} on:click={closeCloseReportedProfileModal}>
          Cancelar
        </button>
      </div>
    </div>
  </div>

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
