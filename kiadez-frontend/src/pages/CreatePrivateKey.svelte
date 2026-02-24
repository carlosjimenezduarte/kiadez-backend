<script>
  import { onMount } from "svelte";
  import { setDekSessionHex } from "../lib/dekSession";

  const API = "http://127.0.0.1:8000";
  const AAD_VAULT = new TextEncoder().encode("kiadez-vault-v1");

  let statusMessage = "";
  let submitLabel = "Crear clave privada";
  let isSubmitting = false;
  let ppw = "";
  let ppw2 = "";
  let ppwVisible = false;
  let ppw2Visible = false;

  const PASSWORD_POLICY_MESSAGE =
    "Debe incluir 8+ caracteres, 1 mayúscula, 1 número y 1 símbolo.";

  const passwordMeetsPolicy = (value) => {
    const password = String(value || "");
    if (password.length < 8) return false;
    if (!/[A-Z]/.test(password)) return false;
    if (!/[0-9]/.test(password)) return false;
    if (!/[^a-zA-Z0-9]/.test(password)) return false;
    return true;
  };

  let passwordWarningText = "";

  $: {
    const password = String(ppw || "");
    const confirm = String(ppw2 || "");

    if (password && !passwordMeetsPolicy(password)) {
      passwordWarningText = PASSWORD_POLICY_MESSAGE;
    } else if (passwordMeetsPolicy(password) && confirm && password !== confirm) {
      if (confirm.length >= password.length) {
        passwordWarningText = "Las claves privadas deben coincidir.";
      } else {
        passwordWarningText = "";
      }
    } else {
      passwordWarningText = "";
    }
  }

  let feedbackModalOpen = false;
  let feedbackTitle = "Aviso";
  let feedbackMessage = "";
  let feedbackActionLabel = "Aceptar";
  let feedbackNextUrl = null;

  function openFeedbackModal({ title = "Aviso", message, actionLabel = "Aceptar", nextUrl = null }) {
    feedbackTitle = title;
    feedbackMessage = message;
    feedbackActionLabel = actionLabel;
    feedbackNextUrl = nextUrl;
    feedbackModalOpen = true;
  }

  function closeFeedbackModal() {
    feedbackModalOpen = false;
    const nextUrl = feedbackNextUrl;
    feedbackNextUrl = null;
    if (nextUrl) {
      window.location.href = nextUrl;
    }
  }

  function bufToHex(buf) {
    return [...new Uint8Array(buf)]
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
  }

  function showStatus(msg) {
    statusMessage = msg;
  }

  function getAccessToken() {
    return localStorage.getItem("access_token") || "";
  }

  async function pbkdf2Key(password, saltBuf, iters) {
    const enc = new TextEncoder();
    const baseKey = await crypto.subtle.importKey(
      "raw",
      enc.encode(password),
      "PBKDF2",
      false,
      ["deriveKey"]
    );

    return crypto.subtle.deriveKey(
      {
        name: "PBKDF2",
        salt: saltBuf,
        iterations: iters,
        hash: "SHA-256",
      },
      baseKey,
      { name: "AES-GCM", length: 256 },
      false,
      ["encrypt", "decrypt"]
    );
  }

  async function aesGcmEncrypt(key, rawBytesBuf, aadBytes) {
    const nonce = crypto.getRandomValues(new Uint8Array(12));
    const ciphertext = await crypto.subtle.encrypt(
      { name: "AES-GCM", iv: nonce, additionalData: aadBytes },
      key,
      rawBytesBuf
    );
    return { nonce: nonce.buffer, ciphertext };
  }

  async function checkVaultStatus() {
    const token = getAccessToken();
    if (!token) {
      showStatus("No hay sesión activa. Inicia sesión de nuevo.");
      return { has_vault: false, ok: false };
    }

    try {
      const res = await fetch(`${API}/vault/status`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (!res.ok) {
        showStatus(data.detail || "No se pudo consultar el estado del vault.");
        return { has_vault: false, ok: false };
      }
      return { has_vault: !!data.has_vault, ok: true };
    } catch (e) {
      showStatus("No se pudo conectar con el servidor.");
      return { has_vault: false, ok: false };
    }
  }

  async function checkLifePurposeConfigured() {
    const token = getAccessToken();
    if (!token) {
      return { configured: false, ok: false };
    }

    try {
      const res = await fetch(`${API}/life-purpose/mine`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      if (!res.ok) {
        showStatus(data.detail || "No se pudo consultar tu propósito de vida.");
        return { configured: false, ok: false };
      }

      const slots = Array.isArray(data?.slots) ? data.slots : [];
      const slotNumbers = new Set(
        slots
          .map((slot) => Number(slot?.slot_number))
          .filter((n) => Number.isFinite(n) && n >= 1 && n <= 3)
      );
      return { configured: slotNumbers.size >= 3, ok: true };
    } catch (e) {
      showStatus("No se pudo conectar con el servidor.");
      return { configured: false, ok: false };
    }
  }

  async function createVault(privatePassword) {
    const iters = 310000;
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const kek = await pbkdf2Key(privatePassword, salt.buffer, iters);
    const dekRaw = crypto.getRandomValues(new Uint8Array(32)).buffer;
    const { nonce, ciphertext } = await aesGcmEncrypt(kek, dekRaw, AAD_VAULT);

    const token = getAccessToken();
    const res = await fetch(`${API}/vault/setup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        kdf_name: "pbkdf2_sha256",
        kdf_iters: iters,
        kdf_salt_hex: bufToHex(salt.buffer),
        wrapped_dek_nonce_hex: bufToHex(nonce),
        wrapped_dek_hex: bufToHex(ciphertext),
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "No se pudo crear vault.");
    }

    setDekSessionHex(bufToHex(dekRaw));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const token = getAccessToken();
    if (!token) {
      openFeedbackModal({
        title: "Sesión requerida",
        message: "No hay sesión activa. Inicia sesión de nuevo.",
        actionLabel: "Ir a login",
        nextUrl: "/login.html",
      });
      return;
    }

    const st = await checkVaultStatus();
    if (st.ok && st.has_vault) {
      const purposeState = await checkLifePurposeConfigured();
      window.location.href = purposeState.configured ? "/home_user.html" : "/life-proposal.html";
      return;
    }

    if (!passwordMeetsPolicy(ppw)) {
      openFeedbackModal({
        title: "Clave inválida",
        message: PASSWORD_POLICY_MESSAGE,
      });
      return;
    }

    if (ppw !== ppw2) {
      openFeedbackModal({
        title: "Claves no coinciden",
        message: "Verifica que ambas claves privadas sean exactamente iguales.",
      });
      return;
    }

    isSubmitting = true;
    try {
      await createVault(ppw);
      openFeedbackModal({
        title: "Clave privada creada",
        message: "Tu clave privada se configuró correctamente.",
        actionLabel: "Continuar",
        nextUrl: "/life-proposal.html",
      });
    } catch (err) {
      console.error(err);
      openFeedbackModal({
        title: "No se pudo guardar",
        message: err.message || "No se pudo crear la clave privada.",
      });
    } finally {
      isSubmitting = false;
    }
  }

  onMount(async () => {
    const st = await checkVaultStatus();
    if (st.ok && st.has_vault) {
      const purposeState = await checkLifePurposeConfigured();
      if (purposeState.configured) {
        showStatus("Ya tienes clave privada y propósito configurados. Puedes continuar a tu Home.");
        submitLabel = "Ir a mi Home";
      } else {
        showStatus("Ya tienes una clave privada configurada. Próximo paso: tu propósito de vida.");
        submitLabel = "Continuar";
      }
    }
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Kiadez — Crea tu clave privada</title>
    <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-backgroundcpp">
        <main class="auth-center">
            <div class="auth-card auth-card--wide">
                <h2 class="auth-title">Crea tu clave privada personal</h2>

                <div class="auth-message">
                    <p>
                        Esta clave protege tus <strong>deseos privados</strong> y tu <strong>propósito secreto</strong>.
                    </p>
                    <br>
                    <br>
                    <p class="muted">
                        Esta clave no pertenece a Kiadez: te pertenece a ti.<br>
                        Más adelante podrás definir custodios o mecanismos de recuperación consciente.
                        <br>
                        <br>
                        Por favor, guarda muy bien esta clave o memórizala como un tesoro personal.
                    </p>
                    <br>
                    {#if statusMessage}
                      <p class="muted">{statusMessage}</p>
                    {/if}
                </div>

                <form id="vault-form" on:submit={handleSubmit}>
                    <div class="password-field">
                      <input
                        type={ppwVisible ? "text" : "password"}
                        name="ppw"
                        placeholder="Clave privada personal"
                        bind:value={ppw}
                        required
                      />
                      <button
                        class="password-toggle"
                        class:is-visible={ppwVisible}
                        type="button"
                        aria-label={ppwVisible ? "Ocultar contraseña" : "Mostrar contraseña"}
                        aria-pressed={ppwVisible ? "true" : "false"}
                        title={ppwVisible ? "Ocultar contraseña" : "Mostrar contraseña"}
                        on:click={() => (ppwVisible = !ppwVisible)}
                      >
                        <svg class="password-toggle-icon password-toggle-icon-show" viewBox="0 0 24 24" aria-hidden="true">
                          <path d="M2.2 12c1.7-4.2 5.6-7 9.8-7s8.1 2.8 9.8 7c-1.7 4.2-5.6 7-9.8 7s-8.1-2.8-9.8-7z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" />
                          <circle cx="12" cy="12" r="3.2" fill="none" stroke="currentColor" stroke-width="1.8" />
                        </svg>
                        <svg class="password-toggle-icon password-toggle-icon-hide" viewBox="0 0 24 24" aria-hidden="true">
                          <path d="M2.2 12c1.7-4.2 5.6-7 9.8-7s8.1 2.8 9.8 7c-1.7 4.2-5.6 7-9.8 7s-8.1-2.8-9.8-7z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" />
                          <circle cx="12" cy="12" r="3.2" fill="none" stroke="currentColor" stroke-width="1.8" />
                          <path d="M4 4l16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                        </svg>
                      </button>
                    </div>

                    <div class="password-field">
                      <input
                        type={ppw2Visible ? "text" : "password"}
                        name="ppw2"
                        placeholder="Confirmar clave privada"
                        bind:value={ppw2}
                        required
                      />
                      <button
                        class="password-toggle"
                        class:is-visible={ppw2Visible}
                        type="button"
                        aria-label={ppw2Visible ? "Ocultar contraseña" : "Mostrar contraseña"}
                        aria-pressed={ppw2Visible ? "true" : "false"}
                        title={ppw2Visible ? "Ocultar contraseña" : "Mostrar contraseña"}
                        on:click={() => (ppw2Visible = !ppw2Visible)}
                      >
                        <svg class="password-toggle-icon password-toggle-icon-show" viewBox="0 0 24 24" aria-hidden="true">
                          <path d="M2.2 12c1.7-4.2 5.6-7 9.8-7s8.1 2.8 9.8 7c-1.7 4.2-5.6 7-9.8 7s-8.1-2.8-9.8-7z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" />
                          <circle cx="12" cy="12" r="3.2" fill="none" stroke="currentColor" stroke-width="1.8" />
                        </svg>
                        <svg class="password-toggle-icon password-toggle-icon-hide" viewBox="0 0 24 24" aria-hidden="true">
                          <path d="M2.2 12c1.7-4.2 5.6-7 9.8-7s8.1 2.8 9.8 7c-1.7 4.2-5.6 7-9.8 7s-8.1-2.8-9.8-7z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" />
                          <circle cx="12" cy="12" r="3.2" fill="none" stroke="currentColor" stroke-width="1.8" />
                          <path d="M4 4l16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                        </svg>
                      </button>
                    </div>

                    <p class={"form-warning" + (passwordWarningText ? "" : " is-hidden")} aria-live="polite">
                      <span class="form-warning-reserve">
                        Debe incluir 8+ caracteres, 1 mayúscula, 1 número y 1 símbolo.
                      </span>
                      <span class="form-warning-live">{passwordWarningText}</span>
                    </p>


                    <button type="submit" class="btn btn-primary" id="submit-btn" disabled={isSubmitting}>
                        {isSubmitting ? "Creando..." : submitLabel}
                    </button>

                    <br><br>
                    <a href="/login.html" class="btn btn-outline">Volver</a>
                </form>

                <div class="auth-brand">
                    <img src="/css/logo-kiadez.webp" alt="Kiadez" />
                    <span>Kiadez</span>
                </div>
            </div>
        </main>

        <footer class="kiadez-footer">
            <div class="footer-bottom">© 2026 Kiadez — Una red social para cumplir deseos.</div>
        </footer>
    </div>

{#if feedbackModalOpen}
  <div class="modal-overlay" id="privateKeyFeedbackOverlay" aria-hidden="false">
    <div class="modal" role="dialog" aria-modal="true" aria-label={feedbackTitle}>
      <div class="modal-head">
        <h3>{feedbackTitle}</h3>
        <button class="modal-close" type="button" on:click={closeFeedbackModal}>✕</button>
      </div>
      <div class="modal-body">
        <p class="modal-label-center">{feedbackMessage}</p>
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" on:click={closeFeedbackModal}>
          {feedbackActionLabel}
        </button>
      </div>
    </div>
  </div>
{/if}
