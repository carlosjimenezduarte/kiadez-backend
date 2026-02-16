<script>
  import { onMount, tick } from "svelte";
  import { logout } from "../lib/logout";

  const API = "http://127.0.0.1:8000";
  const PASSWORD_MIN_LENGTH = 8;
  const PASSWORD_RE_UPPER = /[A-Z]/;
  const PASSWORD_RE_DIGIT = /[0-9]/;
  const PASSWORD_RE_SPECIAL = /[^a-zA-Z0-9]/;

  let changePasswordModalOpen = false;
  let changePasswordMode = "change"; // change | reset
  let changePasswordStatus = "";
  let changePasswordError = "";
  let resetStatus = "";
  let resetError = "";
  let isChangingPassword = false;
  let isSendingReset = false;

  let meEmail = "";

  let currentPassword = "";
  let newPassword = "";
  let newPasswordConfirm = "";

  let showCurrentPassword = false;
  let showNewPassword = false;
  let showNewPasswordConfirm = false;

  let currentPasswordInput;

  // -------------------------
  // 2FA
  // -------------------------

  let twofaModalOpen = false;
  let twofaStatusLoading = false;
  let twofaStatusError = "";
  let twofaStatus = null;

  let twofaSetupLoading = false;
  let twofaSetupError = "";
  let twofaQrCode = "";
  let twofaManualCode = "";
  let twofaIssuer = "";

  let twofaCode = "";
  let twofaConfirmLoading = false;
  let twofaConfirmError = "";
  let twofaConfirmStatus = "";

  let twofaDisableLoading = false;
  let twofaDisableError = "";
  let twofaDisableStatus = "";

  let twofaCodeInput;

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
      Authorization: `Bearer ${token}`
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

  const loadMeEmail = async () => {
    if (meEmail) return meEmail;
    const res = await apiFetch("/auth/me");
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(data.detail || "No se pudo cargar tu información.");
    }
    meEmail = String(data?.email || "");
    return meEmail;
  };

  const resetChangePasswordState = () => {
    changePasswordStatus = "";
    changePasswordError = "";
    resetStatus = "";
    resetError = "";
    isChangingPassword = false;
    isSendingReset = false;

    currentPassword = "";
    newPassword = "";
    newPasswordConfirm = "";

    showCurrentPassword = false;
    showNewPassword = false;
    showNewPasswordConfirm = false;
  };

  const openChangePasswordModal = async () => {
    resetChangePasswordState();
    changePasswordMode = "change";
    changePasswordModalOpen = true;

    // Best-effort: prefetch email so "Olvidé mi contraseña" can send the reset mail.
    void loadMeEmail();

    await tick();
    currentPasswordInput?.focus();
  };

  const closeChangePasswordModal = () => {
    changePasswordModalOpen = false;
    resetChangePasswordState();
  };

  const passwordChecks = (value) => {
    const pw = String(value || "");
    return {
      length: pw.length >= PASSWORD_MIN_LENGTH,
      upper: PASSWORD_RE_UPPER.test(pw),
      digit: PASSWORD_RE_DIGIT.test(pw),
      special: PASSWORD_RE_SPECIAL.test(pw),
    };
  };

  $: newPasswordRules = passwordChecks(newPassword);
  $: newPasswordIsValid = Object.values(newPasswordRules).every(Boolean);

  const handleChangePassword = async () => {
    changePasswordError = "";
    changePasswordStatus = "";

    const current = String(currentPassword || "");
    const next = String(newPassword || "");
    const next2 = String(newPasswordConfirm || "");

    if (!current.trim()) {
      changePasswordError = "Debes digitar tu contraseña actual.";
      return;
    }

    if (!next.trim()) {
      changePasswordError = "Debes digitar tu nueva contraseña.";
      return;
    }

    if (!newPasswordIsValid) {
      changePasswordError = "Tu nueva contraseña no cumple la normativa requerida.";
      return;
    }

    if (next !== next2) {
      changePasswordError = "La confirmación no coincide con tu nueva contraseña.";
      return;
    }

    isChangingPassword = true;
    try {
      const res = await apiFetch("/auth/password/change", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          current_password: current,
          new_password: next,
          new_password_confirm: next2,
        }),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo cambiar la contraseña.");
      }

      changePasswordStatus = "Contraseña actualizada correctamente.";
      currentPassword = "";
      newPassword = "";
      newPasswordConfirm = "";
      showCurrentPassword = false;
      showNewPassword = false;
      showNewPasswordConfirm = false;
    } catch (err) {
      changePasswordError = err?.message || "No se pudo cambiar la contraseña.";
    } finally {
      isChangingPassword = false;
    }
  };

  const handleSendPasswordReset = async () => {
    resetError = "";
    resetStatus = "";
    isSendingReset = true;

    try {
      const email = await loadMeEmail();
      if (!email) {
        throw new Error("No pudimos identificar tu correo. Intenta iniciar sesión nuevamente.");
      }

      const res = await fetch(`${API}/auth/password-reset/request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo enviar el enlace de recuperación.");
      }

      resetStatus = data?.message || "Si el correo existe, enviaremos un enlace de recuperación.";
    } catch (err) {
      resetError = err?.message || "No se pudo enviar el enlace de recuperación.";
    } finally {
      isSendingReset = false;
    }
  };

  const resetTwoFAState = () => {
    twofaStatusLoading = false;
    twofaStatusError = "";
    twofaStatus = null;

    twofaSetupLoading = false;
    twofaSetupError = "";
    twofaQrCode = "";
    twofaManualCode = "";
    twofaIssuer = "";

    twofaCode = "";
    twofaConfirmLoading = false;
    twofaConfirmError = "";
    twofaConfirmStatus = "";

    twofaDisableLoading = false;
    twofaDisableError = "";
    twofaDisableStatus = "";
  };

  const refreshTwoFAStatus = async () => {
    twofaStatusLoading = true;
    twofaStatusError = "";
    try {
      const res = await apiFetch("/auth/2fa/status");
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo cargar el estado de 2FA.");
      }
      twofaStatus = data || null;
    } catch (err) {
      twofaStatusError = err?.message || "No se pudo cargar el estado de 2FA.";
      twofaStatus = null;
    } finally {
      twofaStatusLoading = false;
    }
  };

  const openTwoFAModal = async () => {
    resetTwoFAState();
    twofaModalOpen = true;
    void refreshTwoFAStatus();
    await tick();
    twofaCodeInput?.focus();
  };

  const closeTwoFAModal = () => {
    twofaModalOpen = false;
    resetTwoFAState();
  };

  const copyTwoFAManualCode = async () => {
    if (!twofaManualCode) return;
    try {
      await navigator.clipboard.writeText(twofaManualCode);
      twofaConfirmStatus = "Código manual copiado al portapapeles.";
    } catch {
      twofaConfirmStatus = "No se pudo copiar automáticamente. Selecciona el código y cópialo.";
    }
  };

  const handleTwoFASetup = async () => {
    twofaSetupLoading = true;
    twofaSetupError = "";
    twofaConfirmError = "";
    twofaConfirmStatus = "";

    try {
      const res = await apiFetch("/auth/2fa/setup", { method: "POST" });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo generar el QR de 2FA.");
      }

      twofaQrCode = String(data?.qr_code || "");
      twofaManualCode = String(data?.manual_code || "");
      twofaIssuer = String(data?.issuer || "");
      twofaCode = "";

      await tick();
      twofaCodeInput?.focus();
    } catch (err) {
      twofaSetupError = err?.message || "No se pudo generar el QR de 2FA.";
      twofaQrCode = "";
      twofaManualCode = "";
      twofaIssuer = "";
    } finally {
      twofaSetupLoading = false;
    }
  };

  const handleTwoFAConfirm = async () => {
    twofaConfirmError = "";
    twofaConfirmStatus = "";

    const code = String(twofaCode || "").trim();
    if (!/^[0-9]{6}$/.test(code)) {
      twofaConfirmError = "Digita un código válido de 6 dígitos.";
      return;
    }

    twofaConfirmLoading = true;
    try {
      const res = await apiFetch("/auth/2fa/confirm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo activar 2FA.");
      }

      twofaConfirmStatus = "2FA habilitado correctamente. A partir de ahora se te pedirá un código al iniciar sesión.";
      twofaQrCode = "";
      twofaManualCode = "";
      twofaIssuer = "";
      twofaCode = "";
      void refreshTwoFAStatus();
    } catch (err) {
      twofaConfirmError = err?.message || "No se pudo activar 2FA.";
    } finally {
      twofaConfirmLoading = false;
    }
  };

  const handleTwoFADisable = async () => {
    twofaDisableError = "";
    twofaDisableStatus = "";
    twofaDisableLoading = true;

    try {
      const res = await apiFetch("/auth/2fa/disable", { method: "POST" });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo deshabilitar 2FA.");
      }
      if (data?.disabled) {
        twofaDisableStatus = "2FA deshabilitado.";
      } else {
        twofaDisableStatus = "2FA actualizado.";
      }
      twofaQrCode = "";
      twofaManualCode = "";
      twofaIssuer = "";
      twofaCode = "";
      void refreshTwoFAStatus();
    } catch (err) {
      twofaDisableError = err?.message || "No se pudo deshabilitar 2FA.";
    } finally {
      twofaDisableLoading = false;
    }
  };

  onMount(() => {
    document.body.dataset.visitor = "false";
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Configuración y privacidad</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background settings-page">
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
    <div class="home-body settings-body">
      <section class="panel settings-panel" aria-label="Configuración y privacidad">
        <div class="panel-head">
          <h2 class="panel-title">Configuración y privacidad</h2>
          <span class="panel-badge">Cuenta</span>
        </div>

        <div class="settings-actions">
          <button class="settings-action" type="button" on:click={openChangePasswordModal}>
            <span class="settings-action-icon" aria-hidden="true">🔑</span>
            <span class="settings-action-label">Cambiar contraseña</span>
          </button>

          <button class="settings-action" type="button" on:click={openTwoFAModal}>
            <span class="settings-action-icon" aria-hidden="true">🛡️</span>
            <span class="settings-action-label">Habilitar autenticación 2FA</span>
          </button>

          <button class="settings-action" type="button">
            <span class="settings-action-icon" aria-hidden="true">🔒</span>
            <span class="settings-action-label">Privacidad</span>
          </button>

          <button class="settings-action is-danger" type="button">
            <span class="settings-action-icon" aria-hidden="true">🗑️</span>
            <span class="settings-action-label">Cerrar cuenta</span>
          </button>
        </div>
      </section>
    </div>
  </main>

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

  <div
    class="modal-overlay"
    class:hidden={!changePasswordModalOpen}
    aria-hidden={!changePasswordModalOpen}
    on:click={(event) => {
      if (event.target?.classList?.contains("modal-overlay")) closeChangePasswordModal();
    }}
  >
    <div
      class="modal settings-change-password-modal"
      role="dialog"
      aria-modal="true"
      aria-label="Cambiar contraseña"
    >
      <div class="modal-head">
        <h3>{changePasswordMode === "change" ? "Cambiar contraseña" : "Recuperar contraseña"}</h3>
        <button class="modal-close" type="button" on:click={closeChangePasswordModal}>✕</button>
      </div>

      <div class="modal-body">
        {#if changePasswordMode === "change"}
          <label class="modal-label" for="settings-current-password">
            Digita tu contraseña actual
          </label>
          <div class="settings-password-row">
            <input
              class="modal-input"
              id="settings-current-password"
              bind:this={currentPasswordInput}
              type={showCurrentPassword ? "text" : "password"}
              bind:value={currentPassword}
              autocomplete="current-password"
            />
            <button
              class="settings-password-toggle"
              type="button"
              aria-label={showCurrentPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
              on:click={() => (showCurrentPassword = !showCurrentPassword)}
            >
              👁️
            </button>
          </div>

          <label class="modal-label" for="settings-new-password">
            Digita tu nueva contraseña
          </label>
          <div class="settings-password-row">
            <input
              class="modal-input"
              id="settings-new-password"
              type={showNewPassword ? "text" : "password"}
              bind:value={newPassword}
              autocomplete="new-password"
            />
            <button
              class="settings-password-toggle"
              type="button"
              aria-label={showNewPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
              on:click={() => (showNewPassword = !showNewPassword)}
            >
              👁️
            </button>
          </div>

          <div class="settings-password-rules" aria-label="Normativa de contraseña">
            <div class:ok={newPasswordRules.length} class="settings-password-rule">
              {newPasswordRules.length ? "✔" : "•"} Mínimo {PASSWORD_MIN_LENGTH} caracteres
            </div>
            <div class:ok={newPasswordRules.upper} class="settings-password-rule">
              {newPasswordRules.upper ? "✔" : "•"} Al menos 1 mayúscula
            </div>
            <div class:ok={newPasswordRules.digit} class="settings-password-rule">
              {newPasswordRules.digit ? "✔" : "•"} Al menos 1 número
            </div>
            <div class:ok={newPasswordRules.special} class="settings-password-rule">
              {newPasswordRules.special ? "✔" : "•"} Al menos 1 caracter especial
            </div>
          </div>

          <label class="modal-label" for="settings-new-password-confirm">
            Confirma tu nueva contraseña
          </label>
          <div class="settings-password-row">
            <input
              class="modal-input"
              id="settings-new-password-confirm"
              type={showNewPasswordConfirm ? "text" : "password"}
              bind:value={newPasswordConfirm}
              autocomplete="new-password"
            />
            <button
              class="settings-password-toggle"
              type="button"
              aria-label={showNewPasswordConfirm ? "Ocultar contraseña" : "Mostrar contraseña"}
              on:click={() => (showNewPasswordConfirm = !showNewPasswordConfirm)}
            >
              👁️
            </button>
          </div>

          <button
            class="settings-inline-link"
            type="button"
            on:click={() => {
              changePasswordMode = "reset";
              changePasswordError = "";
              changePasswordStatus = "";
            }}
          >
            ¿Olvidaste tu contraseña?
          </button>

          {#if changePasswordError}
            <p class="settings-form-error" role="alert">{changePasswordError}</p>
          {/if}
          {#if changePasswordStatus}
            <p class="settings-form-success" role="status">{changePasswordStatus}</p>
          {/if}
        {:else}
          <p class="panel-text settings-reset-text">
            Si ya no recuerdas tu contraseña, te enviaremos un enlace seguro para restablecerla.
          </p>

          {#if meEmail}
            <p class="panel-muted settings-reset-meta">
              Enviaremos el enlace a: <strong>{meEmail}</strong>
            </p>
          {/if}

          {#if resetError}
            <p class="settings-form-error" role="alert">{resetError}</p>
          {/if}
          {#if resetStatus}
            <p class="settings-form-success" role="status">{resetStatus}</p>
          {/if}
        {/if}
      </div>

      <div class="modal-actions">
        {#if changePasswordMode === "change"}
          <button class="btn btn-primary btn-compact" type="button" on:click={handleChangePassword} disabled={isChangingPassword}>
            {isChangingPassword ? "Confirmando..." : "Confirmar"}
          </button>
          <button class="btn btn-outline btn-compact" type="button" on:click={closeChangePasswordModal}>
            Cancelar
          </button>
        {:else}
          <button class="btn btn-primary btn-compact" type="button" on:click={handleSendPasswordReset} disabled={isSendingReset}>
            {isSendingReset ? "Enviando..." : "Enviar enlace"}
          </button>
          <button class="btn btn-outline btn-compact" type="button" on:click={() => (changePasswordMode = "change")}>
            Volver
          </button>
        {/if}
      </div>
    </div>
  </div>

  <div
    class="modal-overlay"
    class:hidden={!twofaModalOpen}
    aria-hidden={!twofaModalOpen}
    on:click={(event) => {
      if (event.target?.classList?.contains("modal-overlay")) closeTwoFAModal();
    }}
  >
    <div class="modal settings-twofa-modal" role="dialog" aria-modal="true" aria-label="Autenticación 2FA">
      <div class="modal-head">
        <h3>Autenticación 2FA</h3>
        <button class="modal-close" type="button" on:click={closeTwoFAModal}>✕</button>
      </div>

      <div class="modal-body">
        <p class="panel-text settings-twofa-intro">
          Protege tu cuenta con un segundo factor (TOTP). Al iniciar sesión, además de tu contraseña, se te pedirá un código de 6 dígitos.
        </p>

        {#if twofaStatusLoading}
          <p class="panel-muted">Cargando estado de 2FA...</p>
        {:else if twofaStatusError}
          <p class="settings-form-error" role="alert">{twofaStatusError}</p>
        {:else}
          <div class="settings-twofa-status">
            <span class="panel-badge">
              Estado: {twofaStatus?.is_enabled ? "Activo" : "Inactivo"}
            </span>
            {#if twofaStatus?.is_enabled && twofaStatus?.confirmed_at}
              <span class="panel-muted settings-twofa-date">
                Activado el {new Date(twofaStatus.confirmed_at).toLocaleDateString("es-CO")}
              </span>
            {/if}
          </div>
        {/if}

        {#if twofaDisableError}
          <p class="settings-form-error" role="alert">{twofaDisableError}</p>
        {/if}
        {#if twofaDisableStatus}
          <p class="settings-form-success" role="status">{twofaDisableStatus}</p>
        {/if}

        {#if twofaStatus?.is_enabled}
          <div class="settings-twofa-actions">
            <button class="btn btn-outline btn-compact" type="button" on:click={handleTwoFADisable} disabled={twofaDisableLoading}>
              {twofaDisableLoading ? "Deshabilitando..." : "Deshabilitar 2FA"}
            </button>
            <button
              class="btn btn-primary btn-compact"
              type="button"
              on:click={async () => {
                await handleTwoFADisable();
                if (!twofaDisableError) {
                  await handleTwoFASetup();
                }
              }}
              disabled={twofaDisableLoading || twofaSetupLoading}
            >
              {twofaSetupLoading ? "Generando..." : "Generar nuevo 2FA"}
            </button>
          </div>
        {:else}
          <div class="settings-twofa-actions">
            <button class="btn btn-primary btn-compact" type="button" on:click={handleTwoFASetup} disabled={twofaSetupLoading}>
              {twofaSetupLoading ? "Generando..." : twofaQrCode ? "Regenerar QR" : "Generar QR"}
            </button>
          </div>
        {/if}

        {#if twofaSetupError}
          <p class="settings-form-error" role="alert">{twofaSetupError}</p>
        {/if}

        {#if twofaQrCode}
          <div class="settings-twofa-setup">
            <div class="settings-twofa-qr">
              <img src={twofaQrCode} alt="QR de autenticación 2FA" />
            </div>

            <div class="settings-twofa-manual">
              <div class="panel-muted settings-twofa-manual-label">
                Código manual (para apps como KeePassXC):
              </div>
              <div class="settings-twofa-manual-row">
                <code class="settings-twofa-manual-code">{twofaManualCode}</code>
                <button class="btn btn-outline btn-compact settings-twofa-copy" type="button" on:click={copyTwoFAManualCode}>
                  Copiar
                </button>
              </div>
              {#if twofaIssuer}
                <div class="panel-muted settings-twofa-issuer">
                  Emisor: <strong>{twofaIssuer}</strong>
                </div>
              {/if}
            </div>
          </div>

          <label class="modal-label" for="settings-twofa-code">
            Digita el código de 6 dígitos de tu app autenticadora
          </label>
          <input
            class="modal-input"
            id="settings-twofa-code"
            bind:this={twofaCodeInput}
            type="text"
            inputmode="numeric"
            autocomplete="one-time-code"
            placeholder="123456"
            maxlength="6"
            bind:value={twofaCode}
            on:keydown={(event) => {
              if (event.key === "Enter") {
                event.preventDefault();
                void handleTwoFAConfirm();
              }
            }}
          />

          {#if twofaConfirmError}
            <p class="settings-form-error" role="alert">{twofaConfirmError}</p>
          {/if}
          {#if twofaConfirmStatus}
            <p class="settings-form-success" role="status">{twofaConfirmStatus}</p>
          {/if}
        {/if}
      </div>

      <div class="modal-actions">
        {#if twofaQrCode}
          <button class="btn btn-primary btn-compact" type="button" on:click={handleTwoFAConfirm} disabled={twofaConfirmLoading}>
            {twofaConfirmLoading ? "Confirmando..." : "Confirmar"}
          </button>
        {/if}
        <button class="btn btn-outline btn-compact" type="button" on:click={closeTwoFAModal}>
          Cerrar
        </button>
      </div>
    </div>
  </div>
</div>
