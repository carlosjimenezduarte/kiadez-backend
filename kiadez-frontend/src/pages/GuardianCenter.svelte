<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";

  const API = "http://127.0.0.1:8000";
  const GUARDIAN_REQUIRED_RANK = 3;

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
    }
  };

  const getActiveModule = () => modules.find((item) => item.key === activeModuleKey) || modules[0];

  const formatStatusLabel = (status) => {
    const value = String(status || "").toLowerCase();
    if (value === "open") return "Abierta";
    if (value === "in_progress") return "Compromiso sellado";
    if (value === "closed") return "Denegada";
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
      window.alert(`Mensaje enviado a ${data?.recipient_handle || ownerMessageToHandle}.`);
      closeOwnerMessageModal();
    } catch (err) {
      actionError = err?.message || "No se pudo enviar el mensaje.";
    } finally {
      actionLoading = false;
    }
  };

  onMount(() => {
    document.body.dataset.visitor = "false";

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
      } catch (err) {
        loadError = err?.message || "No se pudo cargar el Centro del Guardián.";
      } finally {
        isLoading = false;
      }
    })();
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
              {#if activeModuleKey === "wish_management"}
                <span class="guardian-center-module-pill">En vivo</span>
              {:else}
                <span class="guardian-center-module-pill">Próximamente</span>
              {/if}
            </div>

            {#if activeModuleKey === "wish_management"}
              <p class="panel-muted guardian-center-module-note">
                Solicitudes generadas desde “Yo puedo cumplir ese deseo”. Usa el botón “Ver deseo” para ir al deseo exacto.
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
                        <div class="guardian-wish-card-status">{formatStatusLabel(req.status)}</div>
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
              <div class="guardian-center-empty">No hay publicaciones denunciadas por ahora.</div>
            {:else if activeModuleKey === "reported_profiles"}
              <div class="guardian-center-empty">No hay perfiles denunciados por ahora.</div>
            {:else if activeModuleKey === "messaging"}
              <div class="guardian-center-empty">
                Aquí aparecerán conversaciones y coordinación entre Guardianes y usuarios.
              </div>
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
    <div class="modal wish-modal guardian-center-modal guardian-center-mail-modal" role="dialog" aria-modal="true" aria-label="Mensaje al dueño del deseo">
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
