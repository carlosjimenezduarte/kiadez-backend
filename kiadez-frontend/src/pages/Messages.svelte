<script>
  import { onMount } from "svelte";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";
  import { logout } from "../lib/logout";

  const API = "http://127.0.0.1:8000";
  const GUARDIAN_REQUIRED_RANK = 3;
  const SUBJECT_MAX_LENGTH = 180;
  const BODY_MAX_LENGTH = 10000;

  let isLoading = true;
  let loadError = "";

  let viewerUserId = null;
  let guardianRank = 0;
  let isGuardian = false;

  let visibleThreads = [];
  let selectedThreadId = "";

  let showComposeModal = false;
  let composeTo = "";
  let composeSubject = "";
  let composeBody = "";
  let composeError = "";
  let composeToError = false;
  let composeSubjectError = false;
  let composeBodyError = false;
  let composeLoading = false;

  let replyBody = "";
  let replyError = "";
  let replyBodyError = false;
  let replyLoading = false;

  const getAccessToken = () => localStorage.getItem("access_token") || "";

  const parseResponseJson = async (response) => {
    try {
      return await response.json();
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

    const response = await fetch(`${API}${path}`, {
      ...options,
      headers: {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login.html";
      throw new Error("Tu sesión expiró. Inicia sesión nuevamente.");
    }

    return response;
  };

  const normalizeUsername = (value) => {
    let normalized = String(value || "").trim().toLowerCase();
    while (normalized.startsWith("@")) normalized = normalized.slice(1);
    return normalized;
  };

  const parseRecipientInput = (value) => {
    const raw = String(value || "").trim();
    if (!raw) return { userId: null, username: "" };

    const normalized = normalizeUsername(raw);
    const idMatch = normalized.match(/^id(\d+)$/i);
    if (idMatch) {
      return { userId: Number(idMatch[1]), username: "" };
    }

    return { userId: null, username: normalized };
  };

  const sortThreads = (threads) =>
    [...threads].sort((a, b) => {
      const timeA = new Date(a?.updated_at || a?.created_at || 0).getTime();
      const timeB = new Date(b?.updated_at || b?.created_at || 0).getTime();
      return timeB - timeA;
    });

  const formatDateTime = (value) => {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleString("es-CO", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const formatShortDate = (value) => {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleDateString("es-CO", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  const setComposeError = (message) => {
    composeError = String(message || "").trim();
  };

  const setReplyError = (message) => {
    replyError = String(message || "").trim();
  };

  const resetComposeForm = () => {
    composeTo = "";
    composeSubject = "";
    composeBody = "";
    composeError = "";
    composeToError = false;
    composeSubjectError = false;
    composeBodyError = false;
  };

  const openComposeModal = () => {
    if (!isGuardian) return;
    resetComposeForm();
    showComposeModal = true;
  };

  const closeComposeModal = () => {
    if (composeLoading) return;
    showComposeModal = false;
    resetComposeForm();
  };

  const selectThread = (threadId) => {
    selectedThreadId = String(threadId || "");
    replyBody = "";
    replyError = "";
    replyBodyError = false;
  };

  const getThreadCounterpart = (thread) => {
    const myUserId = Number(viewerUserId || 0);
    if (!myUserId || !thread) {
      return {
        user_id: null,
        name: "Usuario",
        handle: "@usuario",
      };
    }

    if (myUserId === Number(thread.guardian_user_id || 0)) {
      return {
        user_id: Number(thread.recipient_user_id || 0),
        name: String(thread.recipient_name || "Usuario").trim() || "Usuario",
        handle: String(thread.recipient_handle || "@usuario").trim() || "@usuario",
      };
    }

    return {
      user_id: Number(thread.guardian_user_id || 0),
      name: String(thread.guardian_name || "Usuario").trim() || "Usuario",
      handle: String(thread.guardian_handle || "@usuario").trim() || "@usuario",
    };
  };

  const getLastMessage = (thread) => {
    if (!thread || !Array.isArray(thread.messages) || !thread.messages.length) return null;
    return thread.messages[thread.messages.length - 1];
  };

  const canReplyThread = (thread) => Boolean(thread?.can_reply);

  const loadViewerContext = async () => {
    const meResponse = await apiFetch("/auth/me");
    const meData = await parseResponseJson(meResponse);
    if (!meResponse.ok) {
      throw new Error(meData?.detail || "No se pudo cargar tu perfil.");
    }

    const myUserId = Number(meData?.user_number || 0);
    if (!myUserId) {
      throw new Error("No se pudo identificar tu usuario.");
    }

    viewerUserId = myUserId;
    guardianRank = Number(meData?.guardian_rank || 0) || 0;
    isGuardian = guardianRank >= GUARDIAN_REQUIRED_RANK;
  };

  const loadThreads = async ({ preferredThreadId = "" } = {}) => {
    const response = await apiFetch("/messages/threads");
    const data = await parseResponseJson(response);
    if (!response.ok) {
      throw new Error(data?.detail || "No se pudo cargar tu bandeja de mensajería.");
    }

    const items = Array.isArray(data?.items) ? data.items : [];
    visibleThreads = sortThreads(items);

    if (!visibleThreads.length) {
      selectedThreadId = "";
      return;
    }

    const preferred = String(preferredThreadId || "").trim();
    if (preferred && visibleThreads.some((thread) => String(thread.id) === preferred)) {
      selectedThreadId = preferred;
      return;
    }

    if (visibleThreads.some((thread) => String(thread.id) === selectedThreadId)) {
      return;
    }

    selectedThreadId = String(visibleThreads[0].id);
  };

  const submitCompose = async () => {
    if (composeLoading) return;

    composeToError = !String(composeTo || "").trim();
    composeSubjectError = !String(composeSubject || "").trim();
    composeBodyError = !String(composeBody || "").trim();

    if (!isGuardian) {
      setComposeError("Solo los Guardianes pueden iniciar mensajes.");
      return;
    }

    if (composeToError || composeSubjectError || composeBodyError) {
      setComposeError("Debes completar Para, Asunto y Mensaje.");
      return;
    }

    const recipient = parseRecipientInput(composeTo);
    if (!recipient.userId && !recipient.username) {
      composeToError = true;
      setComposeError("Debes escribir un @id, @usuario o @allusers válido.");
      return;
    }

    composeLoading = true;
    setComposeError("");

    try {
      const payload = {
        subject: String(composeSubject || "").trim(),
        body: String(composeBody || "").trim(),
      };

      if (recipient.userId) {
        payload.to_user_id = Number(recipient.userId);
      } else {
        payload.to_username = recipient.username;
      }

      const response = await apiFetch("/messages/threads", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(data?.detail || "No se pudo enviar el mensaje.");
      }

      await loadThreads({ preferredThreadId: String(data?.id || "") });
      closeComposeModal();
    } catch (error) {
      setComposeError(error?.message || "No se pudo enviar el mensaje.");
    } finally {
      composeLoading = false;
    }
  };

  const submitReply = async () => {
    if (replyLoading) return;

    const active = visibleThreads.find((thread) => String(thread.id) === selectedThreadId) || null;
    if (!active) {
      setReplyError("Selecciona una conversación para responder.");
      return;
    }

    if (!canReplyThread(active)) {
      setReplyError("No tienes permisos para responder en esta conversación.");
      return;
    }

    replyBodyError = !String(replyBody || "").trim();
    if (replyBodyError) {
      setReplyError("Debes escribir una respuesta antes de enviar.");
      return;
    }

    replyLoading = true;
    setReplyError("");

    try {
      const response = await apiFetch(
        `/messages/threads/${encodeURIComponent(String(active.id))}/reply`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            body: String(replyBody || "").trim(),
          }),
        }
      );
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(data?.detail || "No se pudo enviar la respuesta.");
      }

      await loadThreads({ preferredThreadId: String(active.id) });
      replyBody = "";
      replyBodyError = false;
    } catch (error) {
      setReplyError(error?.message || "No se pudo enviar la respuesta.");
    } finally {
      replyLoading = false;
    }
  };

  $: activeThread =
    visibleThreads.find((thread) => String(thread.id) === selectedThreadId) ||
    visibleThreads[0] ||
    null;

  onMount(() => {
    const cleanupCover = initPurposeCoverModule();
    void syncProfileStarsTotal("messagesStarsTotal");

    (async () => {
      isLoading = true;
      loadError = "";
      try {
        await loadViewerContext();
        await loadThreads();
      } catch (error) {
        loadError = error?.message || "No se pudo cargar la bandeja de mensajería.";
      } finally {
        isLoading = false;
      }
    })();

    return () => {
      if (typeof cleanupCover === "function") cleanupCover();
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Mensajería</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background messages-page">
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
          <a href="/messages.html" role="menuitem">Mensajes</a>
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="/assets/cover-default.jpg" alt="Portada" />

        <div class="cover-actions">
          <button class="icon-btn" id="btnChangeCover" type="button" title="Cambiar portada">
            Cambiar portada
          </button>
          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button" title="Editar mi propósito de vida">
            Editar mi propósito de vida
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="purpose-triangle" aria-label="Deseos de propósito">
          <button class="purpose-pill purpose-top" type="button" id="purpose1">
            Deseo #1: Secreto
          </button>

          <button class="purpose-pill purpose-left" type="button" id="purpose2">
            Deseo construir el Reino de Combray
          </button>

          <button class="purpose-pill purpose-right" type="button" id="purpose3">
            Deseo estar unido a Jesús
          </button>
        </div>

        <div class="cover-hint" id="coverHint">
          Arrastra la portada para encuadrarla
        </div>
      </div>
    </section>

    <div class="home-body messages-body">
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
          <span class="nav-icon">⭐</span>
          <span><strong id="messagesStarsTotal">0</strong> estrellas</span>
        </a>
        <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
        <a class="nav-pill is-active" href="/messages.html" title="Mensajes">Mensajes</a>
      </nav>

      <section class="panel messages-shell" aria-label="Mensajería interna">
        <div class="panel-head messages-head">
          <div>
            <h2 class="panel-title">Mensajería interna</h2>
            <p class="panel-muted messages-subtitle">
              Solo los Guardianes pueden iniciar conversaciones. Los usuarios pueden responder dentro del hilo recibido.
            </p>
          </div>
          {#if isGuardian}
            <button class="btn btn-primary btn-compact messages-compose-trigger" type="button" on:click={openComposeModal}>
              💬 Nuevo mensaje
            </button>
          {/if}
        </div>

        {#if loadError}
          <p class="messages-status is-error">{loadError}</p>
        {:else if isLoading}
          <p class="messages-status">Cargando tu bandeja de mensajería...</p>
        {:else if !visibleThreads.length}
          <article class="messages-empty" aria-live="polite">
            {#if isGuardian}
              <p>
                Tu bandeja está vacía. Cuando envíes un mensaje o recibas respuesta, la conversación aparecerá aquí.
              </p>
              <button class="btn btn-outline btn-compact" type="button" on:click={openComposeModal}>
                Abrir redactor
              </button>
            {:else}
              <p>
                Estas en la zona de mensajería, si algún día algún Guardián decide comunicarse contigo, recibirás un mensaje aquí.
              </p>
            {/if}
          </article>
        {:else}
          <div class="messages-layout">
            <aside class="messages-thread-list" aria-label="Conversaciones">
              {#each visibleThreads as thread (thread.id)}
                {@const counterpart = getThreadCounterpart(thread)}
                {@const lastMessage = getLastMessage(thread)}
                <button
                  class={`messages-thread-item${selectedThreadId === String(thread.id) ? " is-active" : ""}`}
                  type="button"
                  on:click={() => selectThread(thread.id)}
                >
                  <div class="messages-thread-head">
                    <strong class="messages-thread-name">{counterpart.name}</strong>
                    <time class="messages-thread-date">{formatShortDate(thread.updated_at)}</time>
                  </div>
                  <div class="messages-thread-handle">{counterpart.handle}</div>
                  <div class="messages-thread-subject">{thread.subject}</div>
                  <div class="messages-thread-preview">
                    {lastMessage ? lastMessage.body : "Sin mensajes"}
                  </div>
                </button>
              {/each}
            </aside>

            {#if activeThread}
              {@const activeCounterpart = getThreadCounterpart(activeThread)}
              <section class="messages-conversation" aria-label="Conversación seleccionada">
                <header class="messages-conversation-head">
                  <div>
                    <h3 class="messages-conversation-title">{activeThread.subject}</h3>
                    <p class="messages-conversation-meta">
                      Conversación con {activeCounterpart.name} <span>{activeCounterpart.handle}</span>
                    </p>
                  </div>
                  {#if activeThread.is_guardian_center_origin}
                    <span class="panel-badge">Centro del Guardián</span>
                  {:else if isGuardian}
                    <span class="panel-badge">Guardián · Rango {guardianRank}</span>
                  {:else}
                    <span class="panel-badge">Respuesta habilitada</span>
                  {/if}
                </header>

                <div class="messages-bubble-list" aria-live="polite">
                  {#each activeThread.messages as message (message.id)}
                    {@const isMine = Number(message.sender_user_id || 0) === Number(viewerUserId || 0)}
                    <article class={`messages-bubble${isMine ? " is-mine" : ""}`}>
                      <div class="messages-bubble-meta">
                        <span>{isMine ? "Tú" : `${message.sender_name} · ${message.sender_handle}`}</span>
                        <time>{formatDateTime(message.created_at)}</time>
                      </div>
                      <p class="messages-bubble-body">{message.body}</p>
                    </article>
                  {/each}
                </div>

                {#if canReplyThread(activeThread)}
                  <form
                    class="messages-reply-form"
                    on:submit|preventDefault={submitReply}
                  >
                    <label class="modal-label" for="messagesReplyBody">Responder</label>
                    <textarea
                      id="messagesReplyBody"
                      class="modal-textarea messages-reply-input"
                      class:is-error={replyBodyError}
                      rows="4"
                      maxlength={BODY_MAX_LENGTH}
                      bind:value={replyBody}
                      on:input={() => {
                        replyBodyError = false;
                        setReplyError("");
                      }}
                      placeholder="Escribe tu respuesta"
                    ></textarea>
                    {#if replyError}
                      <p class="messages-status is-error">{replyError}</p>
                    {/if}
                    <div class="messages-reply-actions">
                      <button class="btn btn-primary btn-compact" type="submit" disabled={replyLoading}>
                        {replyLoading ? "Enviando..." : "Enviar respuesta"}
                      </button>
                    </div>
                  </form>
                {:else}
                  <p class="messages-status">No tienes permisos para responder en esta conversación.</p>
                {/if}
              </section>
            {/if}
          </div>
        {/if}
      </section>
    </div>
  </main>

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

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showComposeModal}
    aria-hidden={!showComposeModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !composeLoading) closeComposeModal();
    }}
  >
    <div class="modal wish-modal guardian-center-modal guardian-center-mail-modal messages-compose-modal" role="dialog" aria-modal="true" aria-label="Nuevo mensaje de Guardián">
      <div class="modal-head guardian-center-modal-head">
        <h3>Nuevo mensaje de Guardián</h3>
      </div>
      <div class="modal-body">
        <label class="modal-label" for="composeTo">Para</label>
        <input
          id="composeTo"
          class="modal-input"
          class:is-error={composeToError}
          type="text"
          maxlength="120"
          bind:value={composeTo}
          placeholder="@id123, @usuario o @allusers"
          on:input={() => {
            composeToError = false;
            setComposeError("");
          }}
        />
        <p class="panel-muted">
          Puedes usar <strong>@allusers</strong> para enviar un mensaje masivo (solo cuentas autorizadas).
        </p>

        <label class="modal-label" for="composeSubject">Asunto</label>
        <input
          id="composeSubject"
          class="modal-input"
          class:is-error={composeSubjectError}
          type="text"
          maxlength={SUBJECT_MAX_LENGTH}
          bind:value={composeSubject}
          on:input={() => {
            composeSubjectError = false;
            setComposeError("");
          }}
        />

        <label class="modal-label" for="composeBody">Mensaje</label>
        <textarea
          id="composeBody"
          class="modal-textarea guardian-center-mail-textarea"
          class:is-error={composeBodyError}
          rows="6"
          maxlength={BODY_MAX_LENGTH}
          bind:value={composeBody}
          on:input={() => {
            composeBodyError = false;
            setComposeError("");
          }}
        ></textarea>

        {#if composeError}
          <div class="wish-error is-visible">{composeError}</div>
        {/if}
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" disabled={composeLoading} on:click={submitCompose}>
          {composeLoading ? "Enviando..." : "Enviar mensaje"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={composeLoading} on:click={closeComposeModal}>
          Cancelar
        </button>
      </div>
    </div>
  </div>
</div>
