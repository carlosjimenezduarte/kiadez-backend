<script>
  import { onMount } from "svelte";
  import { getLocale } from "./i18n";

  const API = "http://127.0.0.1:8000";
  const GUARDIAN_REQUIRED_RANK = 3;
  const SUBJECT_MAX_LENGTH = 180;
  const BODY_MAX_LENGTH = 10000;
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

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
      throw new Error(tr("No hay sesión activa.", "No active session.", "Aucune session active."));
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
      throw new Error(
        tr(
          "Tu sesión expiró. Inicia sesión nuevamente.",
          "Your session expired. Sign in again.",
          "Ta session a expiré. Connecte-toi de nouveau."
        )
      );
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
    return date.toLocaleString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
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
    return date.toLocaleDateString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
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
        name: tr("Usuario", "User", "Utilisateur"),
        handle: tr("@usuario", "@user", "@utilisateur"),
      };
    }

    if (myUserId === Number(thread.guardian_user_id || 0)) {
      return {
        user_id: Number(thread.recipient_user_id || 0),
        name:
          String(
            thread.recipient_name || tr("Usuario", "User", "Utilisateur")
          ).trim() || tr("Usuario", "User", "Utilisateur"),
        handle:
          String(
            thread.recipient_handle || tr("@usuario", "@user", "@utilisateur")
          ).trim() || tr("@usuario", "@user", "@utilisateur"),
      };
    }

    return {
      user_id: Number(thread.guardian_user_id || 0),
      name:
        String(thread.guardian_name || tr("Usuario", "User", "Utilisateur"))
          .trim() || tr("Usuario", "User", "Utilisateur"),
      handle:
        String(thread.guardian_handle || tr("@usuario", "@user", "@utilisateur"))
          .trim() || tr("@usuario", "@user", "@utilisateur"),
    };
  };

  const getLastMessage = (thread) => {
    if (!thread || !Array.isArray(thread.messages) || !thread.messages.length)
      return null;
    return thread.messages[thread.messages.length - 1];
  };

  const canReplyThread = (thread) => Boolean(thread?.can_reply);

  const loadViewerContext = async () => {
    const meResponse = await apiFetch("/auth/me");
    const meData = await parseResponseJson(meResponse);
    if (!meResponse.ok) {
      throw new Error(
        meData?.detail ||
          tr(
            "No se pudo cargar tu perfil.",
            "Could not load your profile.",
            "Impossible de charger ton profil."
          )
      );
    }

    const myUserId = Number(meData?.user_number || 0);
    if (!myUserId) {
      throw new Error(
        tr(
          "No se pudo identificar tu usuario.",
          "Could not identify your user.",
          "Impossible d'identifier ton utilisateur."
        )
      );
    }

    viewerUserId = myUserId;
    guardianRank = Number(meData?.guardian_rank || 0) || 0;
    isGuardian = guardianRank >= GUARDIAN_REQUIRED_RANK;
  };

  const loadThreads = async ({ preferredThreadId = "" } = {}) => {
    const response = await apiFetch("/messages/threads");
    const data = await parseResponseJson(response);
    if (!response.ok) {
      throw new Error(
        data?.detail ||
          tr(
            "No se pudo cargar tu bandeja de mensajería.",
            "Could not load your message inbox.",
            "Impossible de charger ta boîte de messages."
          )
      );
    }

    const items = Array.isArray(data?.items) ? data.items : [];
    visibleThreads = sortThreads(items);

    if (!visibleThreads.length) {
      selectedThreadId = "";
      return;
    }

    const preferred = String(preferredThreadId || "").trim();
    if (
      preferred &&
      visibleThreads.some((thread) => String(thread.id) === preferred)
    ) {
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
      setComposeError(
        tr(
          "Solo los Guardianes pueden iniciar mensajes.",
          "Only Guardians can start messages.",
          "Seuls les Gardiens peuvent démarrer des messages."
        )
      );
      return;
    }

    if (composeToError || composeSubjectError || composeBodyError) {
      setComposeError(
        tr(
          "Debes completar Para, Asunto y Mensaje.",
          "You must complete To, Subject and Message.",
          "Tu dois compléter À, Objet et Message."
        )
      );
      return;
    }

    const recipient = parseRecipientInput(composeTo);
    if (!recipient.userId && !recipient.username) {
      composeToError = true;
      setComposeError(
        tr(
          "Debes escribir un @id, @usuario o @allusers válido.",
          "You must enter a valid @id, @user or @allusers.",
          "Tu dois saisir un @id, @utilisateur ou @allusers valide."
        )
      );
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
        throw new Error(
          data?.detail ||
            tr(
              "No se pudo enviar el mensaje.",
              "Could not send message.",
              "Impossible d'envoyer le message."
            )
        );
      }

      await loadThreads({ preferredThreadId: String(data?.id || "") });
      closeComposeModal();
    } catch (error) {
      setComposeError(
        error?.message ||
          tr(
            "No se pudo enviar el mensaje.",
            "Could not send message.",
            "Impossible d'envoyer le message."
          )
      );
    } finally {
      composeLoading = false;
    }
  };

  const submitReply = async () => {
    if (replyLoading) return;

    const active =
      visibleThreads.find((thread) => String(thread.id) === selectedThreadId) ||
      null;
    if (!active) {
      setReplyError(
        tr(
          "Selecciona una conversación para responder.",
          "Select a conversation to reply.",
          "Sélectionne une conversation pour répondre."
        )
      );
      return;
    }

    if (!canReplyThread(active)) {
      setReplyError(
        tr(
          "No tienes permisos para responder en esta conversación.",
          "You do not have permission to reply in this conversation.",
          "Tu n'as pas l'autorisation de répondre dans cette conversation."
        )
      );
      return;
    }

    replyBodyError = !String(replyBody || "").trim();
    if (replyBodyError) {
      setReplyError(
        tr(
          "Debes escribir una respuesta antes de enviar.",
          "You must write a reply before sending.",
          "Tu dois écrire une réponse avant d'envoyer."
        )
      );
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
        throw new Error(
          data?.detail ||
            tr(
              "No se pudo enviar la respuesta.",
              "Could not send reply.",
              "Impossible d'envoyer la réponse."
            )
        );
      }

      await loadThreads({ preferredThreadId: String(active.id) });
      replyBody = "";
      replyBodyError = false;
    } catch (error) {
      setReplyError(
        error?.message ||
          tr(
            "No se pudo enviar la respuesta.",
            "Could not send reply.",
            "Impossible d'envoyer la réponse."
          )
      );
    } finally {
      replyLoading = false;
    }
  };

  $: activeThread =
    visibleThreads.find((thread) => String(thread.id) === selectedThreadId) ||
    visibleThreads[0] ||
    null;

  onMount(() => {
    (async () => {
      isLoading = true;
      loadError = "";
      try {
        await loadViewerContext();
        await loadThreads();
      } catch (error) {
        loadError =
          error?.message ||
          tr(
            "No se pudo cargar la bandeja de mensajería.",
            "Could not load message inbox.",
            "Impossible de charger la boîte de messages."
          );
      } finally {
        isLoading = false;
      }
    })();
  });
</script>

<div class="messages-page guardian-center-messaging">
  <section
    class="messages-shell"
    aria-label={tr("Mensajería interna", "Internal messaging", "Messagerie interne")}
  >
    <div class="panel-head messages-head">
      <div>
        <h2 class="panel-title">
          {tr("Mensajería interna", "Internal messaging", "Messagerie interne")}
        </h2>
        <p class="panel-muted messages-subtitle">
          {tr(
            "Solo los Guardianes pueden iniciar conversaciones. Los usuarios pueden responder dentro del hilo recibido.",
            "Only Guardians can start conversations. Users can reply inside the received thread."
          )}
        </p>
      </div>
      {#if isGuardian}
        <button
          class="btn btn-primary btn-compact messages-compose-trigger"
          type="button"
          on:click={openComposeModal}
        >
          💬 {tr("Nuevo mensaje", "New message", "Nouveau message")}
        </button>
      {/if}
    </div>

    {#if loadError}
      <p class="messages-status is-error">{loadError}</p>
    {:else if isLoading}
      <p class="messages-status">
        {tr(
          "Cargando tu bandeja de mensajería...",
          "Loading your message inbox...",
          "Chargement de ta boîte de messages..."
        )}
      </p>
    {:else if !visibleThreads.length}
      <article class="messages-empty" aria-live="polite">
        {#if isGuardian}
          <p>
            {tr(
              "Tu bandeja está vacía. Cuando envíes un mensaje o recibas respuesta, la conversación aparecerá aquí.",
              "Your inbox is empty. When you send a message or receive a reply, the conversation will appear here."
            )}
          </p>
          <button class="btn btn-outline btn-compact" type="button" on:click={openComposeModal}>
            {tr("Abrir redactor", "Open composer", "Ouvrir le composeur")}
          </button>
        {:else}
          <p>
            {tr(
              "Estas en la zona de mensajería, si algún día algún Guardián decide comunicarse contigo, recibirás un mensaje aquí.",
              "You are in the messaging area. If a Guardian decides to contact you someday, you will receive a message here."
            )}
          </p>
        {/if}
      </article>
    {:else}
      <div class="messages-layout">
        <aside class="messages-thread-list" aria-label={tr("Conversaciones", "Conversations", "Conversations")}>
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
                {lastMessage ? lastMessage.body : tr("Sin mensajes", "No messages", "Aucun message")}
              </div>
            </button>
          {/each}
        </aside>

        {#if activeThread}
          {@const activeCounterpart = getThreadCounterpart(activeThread)}
          <section
            class="messages-conversation"
            aria-label={tr("Conversación seleccionada", "Selected conversation", "Conversation sélectionnée")}
          >
            <header class="messages-conversation-head">
              <div>
                <h3 class="messages-conversation-title">{activeThread.subject}</h3>
                <p class="messages-conversation-meta">
                  {tr("Conversación con", "Conversation with", "Conversation avec")}
                  {activeCounterpart.name} <span>{activeCounterpart.handle}</span>
                </p>
              </div>
              {#if activeThread.is_guardian_center_origin}
                <span class="panel-badge">{tr("Centro del Guardián", "Guardian Center", "Centre des Gardiens")}</span>
              {:else if isGuardian}
                <span class="panel-badge">{tr("Guardián · Rango", "Guardian · Rank", "Gardien · Rang")} {guardianRank}</span>
              {:else}
                <span class="panel-badge">{tr("Respuesta habilitada", "Reply enabled", "Réponse activée")}</span>
              {/if}
            </header>

            <div class="messages-bubble-list" aria-live="polite">
              {#each activeThread.messages as message (message.id)}
                {@const isMine = Number(message.sender_user_id || 0) === Number(viewerUserId || 0)}
                <article class={`messages-bubble${isMine ? " is-mine" : ""}`}>
                  <div class="messages-bubble-meta">
                    <span>{isMine ? tr("Tú", "You", "Toi") : `${message.sender_name} · ${message.sender_handle}`}</span>
                    <time>{formatDateTime(message.created_at)}</time>
                  </div>
                  <p class="messages-bubble-body">{message.body}</p>
                </article>
              {/each}
            </div>

            {#if canReplyThread(activeThread)}
              <form class="messages-reply-form" on:submit|preventDefault={submitReply}>
                <label class="modal-label" for="messagesReplyBodyCenter">{tr("Responder", "Reply", "Répondre")}</label>
                <textarea
                  id="messagesReplyBodyCenter"
                  class="modal-textarea messages-reply-input"
                  class:is-error={replyBodyError}
                  rows="4"
                  maxlength={BODY_MAX_LENGTH}
                  bind:value={replyBody}
                  on:input={() => {
                    replyBodyError = false;
                    setReplyError("");
                  }}
                  placeholder={tr("Escribe tu respuesta", "Write your reply", "Écris ta réponse")}
                ></textarea>
                {#if replyError}
                  <p class="messages-status is-error">{replyError}</p>
                {/if}
                <div class="messages-reply-actions">
                  <button class="btn btn-primary btn-compact" type="submit" disabled={replyLoading}>
                    {replyLoading ? tr("Enviando...", "Sending...", "Envoi...") : tr("Enviar respuesta", "Send reply", "Envoyer la réponse")}
                  </button>
                </div>
              </form>
            {:else}
              <p class="messages-status">
                {tr(
                  "No tienes permisos para responder en esta conversación.",
                  "You do not have permission to reply in this conversation.",
                  "Tu n'as pas l'autorisation de répondre dans cette conversation."
                )}
              </p>
            {/if}
          </section>
        {/if}
      </div>
    {/if}
  </section>

  <div
    class="modal-overlay guardian-center-modal-overlay"
    class:hidden={!showComposeModal}
    aria-hidden={!showComposeModal}
    on:click={(event) => {
      if (event.target === event.currentTarget && !composeLoading) closeComposeModal();
    }}
  >
    <div
      class="modal wish-modal guardian-center-modal guardian-center-mail-modal messages-compose-modal"
      role="dialog"
      aria-modal="true"
      aria-label={tr("Nuevo mensaje de Guardián", "New Guardian message", "Nouveau message Gardien")}
    >
      <div class="modal-head guardian-center-modal-head">
        <h3>{tr("Nuevo mensaje de Guardián", "New Guardian message", "Nouveau message Gardien")}</h3>
      </div>
      <div class="modal-body">
        <label class="modal-label" for="composeToGuardianCenter">
          {tr("Para", "To", "À")}
        </label>
        <input
          id="composeToGuardianCenter"
          class="modal-input"
          class:is-error={composeToError}
          type="text"
          maxlength="120"
          bind:value={composeTo}
          placeholder={tr("@id123, @usuario o @allusers", "@id123, @user or @allusers", "@id123, @utilisateur ou @allusers")}
          on:input={() => {
            composeToError = false;
            setComposeError("");
          }}
        />
        <p class="panel-muted">
          {@html tr(
            "Puedes usar <strong>@allusers</strong> para enviar un mensaje masivo (solo cuentas autorizadas).",
            "You can use <strong>@allusers</strong> to send a mass message (authorized accounts only)."
          )}
        </p>

        <label class="modal-label" for="composeSubjectGuardianCenter">
          {tr("Asunto", "Subject", "Objet")}
        </label>
        <input
          id="composeSubjectGuardianCenter"
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

        <label class="modal-label" for="composeBodyGuardianCenter">
          {tr("Mensaje", "Message", "Message")}
        </label>
        <textarea
          id="composeBodyGuardianCenter"
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
          {composeLoading ? tr("Enviando...", "Sending...", "Envoi...") : tr("Enviar mensaje", "Send message", "Envoyer le message")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" disabled={composeLoading} on:click={closeComposeModal}>
          {tr("Cancelar", "Cancel", "Annuler")}
        </button>
      </div>
    </div>
  </div>
</div>
