<script>
  import { onMount, tick } from "svelte";
  import { logout } from "../lib/logout";

  const API = "http://127.0.0.1:8000";
  const PASSWORD_MIN_LENGTH = 8;
  const PASSWORD_RE_UPPER = /[A-Z]/;
  const PASSWORD_RE_DIGIT = /[0-9]/;
  const PASSWORD_RE_SPECIAL = /[^a-zA-Z0-9]/;

  let changePasswordModalOpen = false;
  let changeEmailModalOpen = false;
  let changePasswordMode = "change"; // change | reset
  let changePasswordStatus = "";
  let changePasswordError = "";
  let emailChangeStatus = "";
  let emailChangeError = "";
  let resetStatus = "";
  let resetError = "";
  let isChangingPassword = false;
  let isChangingEmail = false;
  let isSendingReset = false;

  let meEmail = "";

  let currentPassword = "";
  let emailCurrentPassword = "";
  let newPassword = "";
  let newPasswordConfirm = "";
  let newEmail = "";

  let showCurrentPassword = false;
  let showNewPassword = false;
  let showNewPasswordConfirm = false;
  let showEmailCurrentPassword = false;

  let currentPasswordInput;
  let emailCurrentPasswordInput;

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

  const PRIVACY_TOGGLES = [
    {
      key: "public_profile_show_about",
      label: "Acerca de mí",
      description: "Controla si otras personas pueden ver tu módulo de presentación personal.",
    },
    {
      key: "public_profile_show_biography",
      label: "Mi biografía",
      description: "Controla la visibilidad de tu módulo de biografía pública en el perfil.",
    },
    {
      key: "public_profile_show_fulfilled_wishes",
      label: "Mis deseos cumplidos",
      description: "Permite o bloquea la visibilidad externa de tus deseos ya cumplidos.",
    },
    {
      key: "public_profile_show_public_wishes",
      label: "Mis deseos públicos",
      description: "Permite o bloquea la visibilidad externa de tu listado de deseos públicos.",
    },
    {
      key: "public_profile_show_cooperative_wishes",
      label: "Deseos cooperativos",
      description: "Controla si otros usuarios pueden ver e interactuar con tus deseos cooperativos.",
    },
    {
      key: "public_profile_show_followers",
      label: "Seguidores",
      description: "Decide si otros usuarios pueden ver el conteo de seguidores de tu perfil.",
    },
    {
      key: "public_profile_show_gallery",
      label: "Galería",
      description: "Controla si el acceso a tu módulo de galería aparece visible en tu perfil.",
    },
    {
      key: "public_profile_show_recent_achievements",
      label: "Logros recientes",
      description: "Controla si el acceso a tus logros aparece visible para otros usuarios.",
    },
    {
      key: "public_profile_show_stars",
      label: "Estrellas",
      description: "Controla la visibilidad del módulo de estrellas dentro de tu perfil público.",
    },
    {
      key: "public_profile_show_cover_purposes",
      label: "Portada y propósitos",
      description: "Controla si tu portada y tus propósitos de vida se muestran en tu perfil público.",
    },
    {
      key: "public_profile_show_calendar",
      label: "Calendario",
      description: "Controla si tu calendario y actividad temporal son visibles para otros.",
    },
    {
      key: "public_profile_show_oracle",
      label: "Oráculo",
      description: "Controla si otras personas pueden consultar tu oráculo en tu perfil.",
    },
    {
      key: "public_profile_show_personal_posts",
      label: "Publicaciones personales",
      description: "Si lo apagas, tus publicaciones no serán visibles para otros usuarios.",
    },
  ];

  const DEFAULT_PRIVACY_SETTINGS = {
    public_profile_show_about: true,
    public_profile_show_biography: true,
    public_profile_show_fulfilled_wishes: true,
    public_profile_show_public_wishes: true,
    public_profile_show_cooperative_wishes: true,
    public_profile_show_followers: true,
    public_profile_show_gallery: true,
    public_profile_show_recent_achievements: true,
    public_profile_show_stars: true,
    public_profile_show_cover_purposes: true,
    public_profile_show_calendar: true,
    public_profile_show_oracle: true,
    public_profile_show_personal_posts: true,
  };

  const ACCOUNT_CLOSE_REASON_OTHER = "other";
  const ACCOUNT_CLOSE_OPTIONS = [
    { value: "no_support", label: "No encontré el acompañamiento que esperaba en este momento" },
    { value: "prefer_private_space", label: "Prefiero mantener mis deseos en un espacio más privado" },
    { value: "personal_pause", label: "Deseo tomar una pausa personal" },
    { value: "misaligned_platform", label: "No me siento alineado actualmente con la dinámica de la plataforma" },
    { value: "goals_reached", label: "He alcanzado mis objetivos por ahora" },
    { value: ACCOUNT_CLOSE_REASON_OTHER, label: "Otro (especificar)" },
  ];

  let privacyModalOpen = false;
  let privacyLoading = false;
  let privacySaving = false;
  let privacyError = "";
  let privacyStatus = "";
  let privacySettings = { ...DEFAULT_PRIVACY_SETTINGS };

  let closeAccountModalOpen = false;
  let closeAccountReason = ACCOUNT_CLOSE_OPTIONS[0].value;
  let closeAccountOtherReason = "";
  let closeAccountPassword = "";
  let closeAccountLoading = false;
  let closeAccountError = "";
  let closeAccountStatus = "";
  let closeAccountDone = false;
  let closeAccountDeadlineLabel = "";
  let showCloseAccountPassword = false;

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

  const resetChangeEmailState = () => {
    emailChangeStatus = "";
    emailChangeError = "";
    isChangingEmail = false;

    emailCurrentPassword = "";
    newEmail = "";
    showEmailCurrentPassword = false;
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

  const openChangeEmailModal = async () => {
    resetChangeEmailState();
    changeEmailModalOpen = true;
    void loadMeEmail();

    await tick();
    emailCurrentPasswordInput?.focus();
  };

  const closeChangeEmailModal = () => {
    changeEmailModalOpen = false;
    resetChangeEmailState();
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

  const handleChangeEmail = async () => {
    emailChangeError = "";
    emailChangeStatus = "";

    const current = String(emailCurrentPassword || "").trim();
    const nextEmail = String(newEmail || "").trim().toLowerCase();
    const currentEmail = String(meEmail || "").trim().toLowerCase();

    if (!current) {
      emailChangeError = "Debes digitar tu contraseña actual.";
      return;
    }

    if (!nextEmail) {
      emailChangeError = "Debes digitar el nuevo correo.";
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(nextEmail)) {
      emailChangeError = "Digita un correo electrónico válido.";
      return;
    }

    if (currentEmail && nextEmail === currentEmail) {
      emailChangeError = "El nuevo correo debe ser distinto al actual.";
      return;
    }

    isChangingEmail = true;
    try {
      const res = await apiFetch("/auth/email/change", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          current_password: current,
          new_email: nextEmail,
        }),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo actualizar el correo.");
      }

      meEmail = String(data?.email || nextEmail);
      newEmail = "";
      emailCurrentPassword = "";
      showEmailCurrentPassword = false;
      emailChangeStatus = data?.message || "Correo actualizado correctamente.";
    } catch (err) {
      emailChangeError = err?.message || "No se pudo actualizar el correo.";
    } finally {
      isChangingEmail = false;
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

  const normalizePrivacySettings = (payload) => ({
    public_profile_show_about: Boolean(payload?.public_profile_show_about ?? true),
    public_profile_show_biography: Boolean(payload?.public_profile_show_biography ?? true),
    public_profile_show_fulfilled_wishes: Boolean(payload?.public_profile_show_fulfilled_wishes ?? true),
    public_profile_show_public_wishes: Boolean(payload?.public_profile_show_public_wishes ?? true),
    public_profile_show_cooperative_wishes: Boolean(payload?.public_profile_show_cooperative_wishes ?? true),
    public_profile_show_followers: Boolean(payload?.public_profile_show_followers ?? true),
    public_profile_show_gallery: Boolean(payload?.public_profile_show_gallery ?? true),
    public_profile_show_recent_achievements: Boolean(payload?.public_profile_show_recent_achievements ?? true),
    public_profile_show_stars: Boolean(payload?.public_profile_show_stars ?? true),
    public_profile_show_cover_purposes: Boolean(payload?.public_profile_show_cover_purposes ?? true),
    public_profile_show_calendar: Boolean(payload?.public_profile_show_calendar ?? true),
    public_profile_show_oracle: Boolean(payload?.public_profile_show_oracle ?? true),
    public_profile_show_personal_posts: Boolean(payload?.public_profile_show_personal_posts ?? true),
  });

  const loadPrivacySettings = async () => {
    privacyLoading = true;
    privacyError = "";
    try {
      const res = await apiFetch("/privacy/mine");
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo cargar tu configuración de privacidad.");
      }
      privacySettings = normalizePrivacySettings(data);
    } catch (err) {
      privacyError = err?.message || "No se pudo cargar tu configuración de privacidad.";
      privacySettings = { ...DEFAULT_PRIVACY_SETTINGS };
    } finally {
      privacyLoading = false;
    }
  };

  const openPrivacyModal = async () => {
    privacyStatus = "";
    privacyError = "";
    privacyModalOpen = true;
    await loadPrivacySettings();
  };

  const closePrivacyModal = () => {
    privacyModalOpen = false;
    privacyStatus = "";
    privacyError = "";
  };

  const togglePrivacy = (key) => {
    if (privacyLoading || privacySaving) return;
    if (!(key in privacySettings)) return;
    privacyStatus = "";
    privacyError = "";
    privacySettings = {
      ...privacySettings,
      [key]: !Boolean(privacySettings[key]),
    };
  };

  const handleSavePrivacy = async () => {
    if (privacyLoading || privacySaving) return;
    privacySaving = true;
    privacyError = "";
    privacyStatus = "";

    try {
      const res = await apiFetch("/privacy/mine", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(privacySettings),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo guardar tu configuración de privacidad.");
      }
      privacySettings = normalizePrivacySettings(data);
      privacyStatus = "Privacidad actualizada correctamente.";
    } catch (err) {
      privacyError = err?.message || "No se pudo guardar tu configuración de privacidad.";
    } finally {
      privacySaving = false;
    }
  };

  const resetCloseAccountState = () => {
    closeAccountReason = ACCOUNT_CLOSE_OPTIONS[0].value;
    closeAccountOtherReason = "";
    closeAccountPassword = "";
    closeAccountLoading = false;
    closeAccountError = "";
    closeAccountStatus = "";
    closeAccountDone = false;
    closeAccountDeadlineLabel = "";
    showCloseAccountPassword = false;
  };

  const openCloseAccountModal = () => {
    resetCloseAccountState();
    closeAccountModalOpen = true;
  };

  const closeCloseAccountModal = () => {
    if (closeAccountLoading) return;
    closeAccountModalOpen = false;
    resetCloseAccountState();
  };

  const handleConfirmCloseAccount = async () => {
    if (closeAccountLoading || closeAccountDone) return;
    closeAccountError = "";
    closeAccountStatus = "";

    const reason = String(closeAccountReason || "").trim();
    const currentPassword = String(closeAccountPassword || "");
    const otherReason = String(closeAccountOtherReason || "").trim();

    if (!reason) {
      closeAccountError = "Selecciona un motivo para cerrar la cuenta.";
      return;
    }
    if (reason === ACCOUNT_CLOSE_REASON_OTHER && !otherReason) {
      closeAccountError = "Describe el motivo en la opción “Otro”.";
      return;
    }
    if (!currentPassword.trim()) {
      closeAccountError = "Digita tu contraseña para confirmar el cierre de cuenta.";
      return;
    }

    closeAccountLoading = true;
    try {
      const res = await apiFetch("/auth/account/close", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          reason,
          current_password: currentPassword,
          other_reason: reason === ACCOUNT_CLOSE_REASON_OTHER ? otherReason : null,
        }),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo cerrar la cuenta.");
      }

      const deadlineDate = new Date(data?.restore_deadline_at || "");
      closeAccountDeadlineLabel = Number.isNaN(deadlineDate.getTime()) ? "" : deadlineDate.toLocaleString();
      closeAccountStatus = data?.message || "";
      closeAccountDone = true;
      closeAccountPassword = "";
      closeAccountOtherReason = "";
      showCloseAccountPassword = false;
    } catch (err) {
      closeAccountError = err?.message || "No se pudo cerrar la cuenta.";
    } finally {
      closeAccountLoading = false;
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
          <a href="/messages.html" role="menuitem">Mensajes</a>
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

          <button class="settings-action" type="button" on:click={openChangeEmailModal}>
            <span class="settings-action-icon" aria-hidden="true">📧</span>
            <span class="settings-action-label">Modificar correo electrónico</span>
          </button>

          <button class="settings-action" type="button" on:click={openTwoFAModal}>
            <span class="settings-action-icon" aria-hidden="true">🛡️</span>
            <span class="settings-action-label">Habilitar autenticación 2FA</span>
          </button>

          <button class="settings-action" type="button" on:click={openPrivacyModal}>
            <span class="settings-action-icon" aria-hidden="true">🔒</span>
            <span class="settings-action-label">Privacidad</span>
          </button>

          <button class="settings-action is-danger" type="button" on:click={openCloseAccountModal}>
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
    class="modal-overlay"
    class:hidden={!closeAccountModalOpen}
    aria-hidden={!closeAccountModalOpen}
    on:click={(event) => {
      if (event.target?.classList?.contains("modal-overlay") && !closeAccountDone) closeCloseAccountModal();
    }}
  >
    <div class="modal settings-close-account-modal" role="dialog" aria-modal="true" aria-label="Cerrar cuenta">
      <div class="modal-head">
        <h3>Cerrar cuenta</h3>
        {#if !closeAccountDone}
          <button class="modal-close" type="button" on:click={closeCloseAccountModal}>✕</button>
        {/if}
      </div>

      <div class="modal-body">
        {#if closeAccountDone}
          <p class="panel-text settings-close-account-summary">
            {closeAccountStatus || "Tu cuenta fue cerrada correctamente."}
          </p>
          {#if closeAccountDeadlineLabel}
            <p class="panel-muted">
              Puedes restaurarla hasta el <strong>{closeAccountDeadlineLabel}</strong> iniciando sesión con tu clave o recuperándola.
            </p>
          {/if}
        {:else}
          <p class="panel-text settings-close-account-intro">
            Selecciona el motivo principal por el cual deseas cerrar tu cuenta.
          </p>

          <fieldset class="settings-close-account-reasons">
            <legend class="settings-close-account-legend">Motivo del cierre</legend>
            {#each ACCOUNT_CLOSE_OPTIONS as option}
              <label class="settings-close-account-option">
                <input
                  type="radio"
                  name="close-account-reason"
                  value={option.value}
                  checked={closeAccountReason === option.value}
                  disabled={closeAccountLoading}
                  on:change={() => {
                    closeAccountReason = option.value;
                    closeAccountError = "";
                  }}
                />
                <span>{option.label}</span>
              </label>
            {/each}
          </fieldset>

          {#if closeAccountReason === ACCOUNT_CLOSE_REASON_OTHER}
            <label class="modal-label" for="close-account-other-reason">Especifica el motivo</label>
            <textarea
              id="close-account-other-reason"
              class="modal-textarea"
              rows="3"
              maxlength="1600"
              bind:value={closeAccountOtherReason}
              disabled={closeAccountLoading}
            ></textarea>
          {/if}

          <div class="settings-close-account-warning">
            Al cerrar la cuenta, tu información quedará inhabilitada para el sistema público. Además, eliminaremos tus deseos públicos y privados,
            publicaciones, reacciones y comentarios.
          </div>

          <label class="modal-label" for="close-account-password">Digita tu contraseña para confirmar</label>
          <div class="settings-password-row">
            <input
              id="close-account-password"
              class="modal-input"
              type={showCloseAccountPassword ? "text" : "password"}
              bind:value={closeAccountPassword}
              autocomplete="current-password"
              disabled={closeAccountLoading}
            />
            <button
              class="settings-password-toggle"
              type="button"
              aria-label={showCloseAccountPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
              on:click={() => (showCloseAccountPassword = !showCloseAccountPassword)}
            >
              👁️
            </button>
          </div>

          <p class="panel-muted settings-close-account-window">
            Después de confirmar, tendrás 30 días para volver con esa misma contraseña o recuperándola si la olvidas. Si no regresas en ese plazo,
            la cuenta se eliminará permanentemente.
          </p>

          {#if closeAccountError}
            <p class="settings-form-error" role="alert">{closeAccountError}</p>
          {/if}
        {/if}
      </div>

      <div class="modal-actions">
        {#if closeAccountDone}
          <button class="btn btn-primary btn-compact" type="button" on:click={() => logout()}>
            Ir al inicio de sesión
          </button>
        {:else}
          <button class="btn btn-primary btn-compact settings-close-account-confirm" type="button" on:click={handleConfirmCloseAccount} disabled={closeAccountLoading}>
            {closeAccountLoading ? "Cerrando..." : "Confirmar cierre de cuenta"}
          </button>
          <button class="btn btn-outline btn-compact" type="button" on:click={closeCloseAccountModal} disabled={closeAccountLoading}>
            Cancelar
          </button>
        {/if}
      </div>
    </div>
  </div>

  <div
    class="modal-overlay"
    class:hidden={!privacyModalOpen}
    aria-hidden={!privacyModalOpen}
    on:click={(event) => {
      if (event.target?.classList?.contains("modal-overlay")) closePrivacyModal();
    }}
  >
    <div class="modal settings-privacy-modal" role="dialog" aria-modal="true" aria-label="Privacidad del perfil público">
      <div class="modal-head">
        <h3>Privacidad del perfil público</h3>
        <button class="modal-close" type="button" on:click={closePrivacyModal}>✕</button>
      </div>

      <div class="modal-body">
        <p class="panel-text settings-privacy-intro">
          Decide qué partes de tu perfil estarán visibles para otros usuarios. Estos cambios no afectan lo que tú puedes ver dentro de Kiadez.
        </p>

        {#if privacyLoading}
          <p class="panel-muted">Cargando configuración de privacidad...</p>
        {:else}
          <div class="settings-privacy-grid">
            {#each PRIVACY_TOGGLES as toggle}
              <div class="privacy-item settings-privacy-item">
                <div class="settings-privacy-main">
                  <span class="privacy-label">{toggle.label}</span>
                  <p class="settings-privacy-help">{toggle.description}</p>
                </div>
                <label class="switch" aria-label={`Alternar visibilidad de ${toggle.label}`}>
                  <input
                    type="checkbox"
                    checked={Boolean(privacySettings[toggle.key])}
                    disabled={privacySaving}
                    on:change={() => togglePrivacy(toggle.key)}
                  />
                  <span class="slider"></span>
                </label>
              </div>
            {/each}
          </div>
        {/if}

        {#if privacyError}
          <p class="settings-form-error" role="alert">{privacyError}</p>
        {/if}
        {#if privacyStatus}
          <p class="settings-form-success" role="status">{privacyStatus}</p>
        {/if}
      </div>

      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" on:click={handleSavePrivacy} disabled={privacyLoading || privacySaving}>
          {privacySaving ? "Guardando..." : "Guardar"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" on:click={closePrivacyModal}>
          Cerrar
        </button>
      </div>
    </div>
  </div>

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
          <p class="panel-text settings-change-intro">
            Para actualizar tu contraseña, primero confirma tu contraseña de inicio de sesión.
          </p>

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

          <div class="settings-change-section">
            <h4 class="settings-change-section-title">Cambiar contraseña</h4>

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

            <div class="settings-change-section-actions">
              <button class="btn btn-primary btn-compact" type="button" on:click={handleChangePassword} disabled={isChangingPassword}>
                {isChangingPassword ? "Confirmando..." : "Actualizar contraseña"}
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
          </div>
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
          <button class="btn btn-outline btn-compact" type="button" on:click={closeChangePasswordModal}>
            Cerrar
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
    class:hidden={!changeEmailModalOpen}
    aria-hidden={!changeEmailModalOpen}
    on:click={(event) => {
      if (event.target?.classList?.contains("modal-overlay")) closeChangeEmailModal();
    }}
  >
    <div
      class="modal settings-change-password-modal"
      role="dialog"
      aria-modal="true"
      aria-label="Modificar correo electrónico"
    >
      <div class="modal-head">
        <h3>Modificar correo electrónico</h3>
        <button class="modal-close" type="button" on:click={closeChangeEmailModal}>✕</button>
      </div>

      <div class="modal-body">
        <p class="panel-text settings-change-intro">
          Para actualizar tu correo, primero confirma tu contraseña de inicio de sesión.
        </p>

        <label class="modal-label" for="settings-email-current-password">
          Digita tu contraseña actual
        </label>
        <div class="settings-password-row">
          <input
            class="modal-input"
            id="settings-email-current-password"
            bind:this={emailCurrentPasswordInput}
            type={showEmailCurrentPassword ? "text" : "password"}
            bind:value={emailCurrentPassword}
            autocomplete="current-password"
          />
          <button
            class="settings-password-toggle"
            type="button"
            aria-label={showEmailCurrentPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
            on:click={() => (showEmailCurrentPassword = !showEmailCurrentPassword)}
          >
            👁️
          </button>
        </div>

        <div class="settings-change-section">
          <h4 class="settings-change-section-title">Cambiar correo electrónico</h4>

          {#if meEmail}
            <p class="panel-muted settings-change-current-email">
              Correo actual: <strong>{meEmail}</strong>
            </p>
          {/if}

          <label class="modal-label" for="settings-new-email">
            Digita tu nuevo correo electrónico
          </label>
          <input
            class="modal-input"
            id="settings-new-email"
            type="email"
            bind:value={newEmail}
            autocomplete="email"
            placeholder="nuevo-correo@ejemplo.com"
          />

          <div class="settings-change-section-actions">
            <button class="btn btn-primary btn-compact" type="button" on:click={handleChangeEmail} disabled={isChangingEmail}>
              {isChangingEmail ? "Actualizando..." : "Actualizar correo"}
            </button>
          </div>

          {#if emailChangeError}
            <p class="settings-form-error" role="alert">{emailChangeError}</p>
          {/if}
          {#if emailChangeStatus}
            <p class="settings-form-success" role="status">{emailChangeStatus}</p>
          {/if}
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" on:click={closeChangeEmailModal}>
          Cerrar
        </button>
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
