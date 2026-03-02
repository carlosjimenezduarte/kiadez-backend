<script>
  import { onMount, tick } from "svelte";
  import { logout } from "../lib/logout";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { buildLangHref, getLocale, setLocale } from "../lib/i18n";

  const API = "http://127.0.0.1:8000";
  const PASSWORD_MIN_LENGTH = 8;
  const PASSWORD_RE_UPPER = /[A-Z]/;
  const PASSWORD_RE_DIGIT = /[0-9]/;
  const PASSWORD_RE_SPECIAL = /[^a-zA-Z0-9]/;
  const SUPPORTED_LOCALES = ["es", "en", "fr"];
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

  let changePasswordModalOpen = false;
  let changeEmailModalOpen = false;
  let changeNameModalOpen = false;
  let changePasswordMode = "change"; // change | reset
  let changePasswordStatus = "";
  let changePasswordError = "";
  let emailChangeStatus = "";
  let emailChangeError = "";
  let nameChangeStatus = "";
  let nameChangeError = "";
  let resetStatus = "";
  let resetError = "";
  let isChangingPassword = false;
  let isChangingEmail = false;
  let isChangingName = false;
  let isSendingReset = false;

  let meEmail = "";
  let profileFirstName = "";
  let profileLastName = "";

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
  let firstNameInput;

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
      label: tr("Acerca de mí", "About me", "À propos de moi"),
      description: tr(
        "Controla si otras personas pueden ver tu módulo de presentación personal.",
        "Controls whether other people can view your personal introduction module."
      ),
    },
    {
      key: "public_profile_show_biography",
      label: tr("Mi biografía", "My biography", "Ma biographie"),
      description: tr(
        "Controla la visibilidad de tu módulo de biografía pública en el perfil.",
        "Controls visibility of your public biography module on your profile."
      ),
    },
    {
      key: "public_profile_show_fulfilled_wishes",
      label: tr("Mis deseos cumplidos", "My fulfilled wishes", "Mes souhaits accomplis"),
      description: tr(
        "Permite o bloquea la visibilidad externa de tus deseos ya cumplidos.",
        "Allows or blocks external visibility of your fulfilled wishes."
      ),
    },
    {
      key: "public_profile_show_public_wishes",
      label: tr("Mis deseos públicos", "My public wishes", "Mes souhaits publics"),
      description: tr(
        "Permite o bloquea la visibilidad externa de tu listado de deseos públicos.",
        "Allows or blocks external visibility of your public wishes list."
      ),
    },
    {
      key: "public_profile_show_cooperative_wishes",
      label: tr("Deseos cooperativos", "Cooperative wishes", "Souhaits coopératifs"),
      description: tr(
        "Controla si otros usuarios pueden ver e interactuar con tus deseos cooperativos.",
        "Controls whether other users can view and interact with your cooperative wishes."
      ),
    },
    {
      key: "public_profile_show_followers",
      label: tr("Seguidores", "Followers", "Abonnés"),
      description: tr(
        "Decide si otros usuarios pueden ver el conteo de seguidores de tu perfil.",
        "Decides whether other users can see your follower count."
      ),
    },
    {
      key: "public_profile_show_gallery",
      label: tr("Galería", "Gallery", "Galerie"),
      description: tr(
        "Controla si el acceso a tu módulo de galería aparece visible en tu perfil.",
        "Controls whether access to your gallery module is visible on your profile."
      ),
    },
    {
      key: "public_profile_show_recent_achievements",
      label: tr("Logros recientes", "Recent achievements", "Réalisations récentes"),
      description: tr(
        "Controla si el acceso a tus logros aparece visible para otros usuarios.",
        "Controls whether access to your achievements appears visible to other users."
      ),
    },
    {
      key: "public_profile_show_stars",
      label: tr("Estrellas", "Stars", "Étoiles"),
      description: tr(
        "Controla la visibilidad del módulo de estrellas dentro de tu perfil público.",
        "Controls visibility of the stars module in your public profile."
      ),
    },
    {
      key: "public_profile_show_cover_purposes",
      label: tr("Portada y propósitos", "Cover and purposes", "Couverture et finalités"),
      description: tr(
        "Controla si tu portada y tus propósitos de vida se muestran en tu perfil público.",
        "Controls whether your cover and life purposes are shown on your public profile."
      ),
    },
    {
      key: "public_profile_show_calendar",
      label: tr("Calendario", "Calendar", "Calendrier"),
      description: tr(
        "Controla si tu calendario y actividad temporal son visibles para otros.",
        "Controls whether your calendar and timeline activity are visible to others."
      ),
    },
    {
      key: "public_profile_show_oracle",
      label: tr("Oráculo", "Oracle", "Oracle"),
      description: tr(
        "Controla si otras personas pueden consultar tu oráculo en tu perfil.",
        "Controls whether others can consult your oracle on your profile."
      ),
    },
    {
      key: "public_profile_show_personal_posts",
      label: tr("Publicaciones personales", "Personal posts", "Publications personnelles"),
      description: tr(
        "Si lo apagas, tus publicaciones no serán visibles para otros usuarios.",
        "If disabled, your posts will not be visible to other users."
      ),
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
    {
      value: "no_support",
      label: tr(
        "No encontré el acompañamiento que esperaba en este momento",
        "I did not find the support I expected at this moment"
      )
    },
    {
      value: "prefer_private_space",
      label: tr(
        "Prefiero mantener mis deseos en un espacio más privado",
        "I prefer to keep my wishes in a more private space"
      )
    },
    {
      value: "personal_pause",
      label: tr("Deseo tomar una pausa personal", "I want to take a personal pause", "Je veux faire une pause personnelle")
    },
    {
      value: "misaligned_platform",
      label: tr(
        "No me siento alineado actualmente con la dinámica de la plataforma",
        "I currently do not feel aligned with the platform dynamics"
      )
    },
    {
      value: "goals_reached",
      label: tr("He alcanzado mis objetivos por ahora", "I have reached my goals for now", "J'ai atteint mes objectifs pour le moment")
    },
    { value: ACCOUNT_CLOSE_REASON_OTHER, label: tr("Otro (especificar)", "Other (specify)", "Autre (préciser)") },
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
  let languageModalOpen = false;

  const openLanguageModal = () => {
    languageModalOpen = true;
  };

  const closeLanguageModal = () => {
    languageModalOpen = false;
  };

  const applyLocale = (nextLocale) => {
    const normalized = String(nextLocale || "").trim().toLowerCase();
    if (!SUPPORTED_LOCALES.includes(normalized)) return;
    if (normalized === locale) {
      languageModalOpen = false;
      return;
    }
    setLocale(normalized);
    window.location.href = buildLangHref(normalized);
  };

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
      "Accept-Language": locale,
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`
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

  const loadMeEmail = async () => {
    if (meEmail) return meEmail;
    const res = await apiFetch("/auth/me");
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(data.detail || tr("No se pudo cargar tu información.", "Could not load your account information.", "Impossible de charger les informations de ton compte."));
    }
    meEmail = String(data?.email || "");
    return meEmail;
  };

  const normalizeHumanName = (value) => String(value || "").trim().replace(/\s+/g, " ");

  const loadProfileName = async () => {
    const res = await apiFetch("/auth/profile/name");
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(data.detail || tr("No se pudo cargar tu nombre actual.", "Could not load your current name.", "Impossible de charger ton nom actuel."));
    }
    profileFirstName = normalizeHumanName(data?.first_name || "");
    profileLastName = normalizeHumanName(data?.last_name || "");
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

  const resetChangeNameState = () => {
    nameChangeStatus = "";
    nameChangeError = "";
    isChangingName = false;
  };

  const openChangeNameModal = async () => {
    resetChangeNameState();
    changeNameModalOpen = true;
    try {
      await loadProfileName();
    } catch (err) {
      nameChangeError = err?.message || tr("No se pudo cargar tu nombre actual.", "Could not load your current name.", "Impossible de charger ton nom actuel.");
    }

    await tick();
    firstNameInput?.focus();
  };

  const closeChangeNameModal = () => {
    changeNameModalOpen = false;
    resetChangeNameState();
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
      changePasswordError = tr("Debes digitar tu contraseña actual.", "You must enter your current password.", "Tu dois saisir ton mot de passe actuel.");
      return;
    }

    if (!next.trim()) {
      changePasswordError = tr("Debes digitar tu nueva contraseña.", "You must enter your new password.", "Tu dois saisir ton nouveau mot de passe.");
      return;
    }

    if (!newPasswordIsValid) {
      changePasswordError = tr(
        "Tu nueva contraseña no cumple la normativa requerida.",
        "Your new password does not meet the required policy."
      );
      return;
    }

    if (next !== next2) {
      changePasswordError = tr(
        "La confirmación no coincide con tu nueva contraseña.",
        "Confirmation does not match your new password."
      );
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
        throw new Error(data.detail || tr("No se pudo cambiar la contraseña.", "Could not change password.", "Impossible de changer le mot de passe."));
      }

      changePasswordStatus = tr("Contraseña actualizada correctamente.", "Password updated successfully.", "Mot de passe mis à jour avec succès.");
      currentPassword = "";
      newPassword = "";
      newPasswordConfirm = "";
      showCurrentPassword = false;
      showNewPassword = false;
      showNewPasswordConfirm = false;
    } catch (err) {
      changePasswordError = err?.message || tr("No se pudo cambiar la contraseña.", "Could not change password.", "Impossible de changer le mot de passe.");
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
        throw new Error(
          tr(
            "No pudimos identificar tu correo. Intenta iniciar sesión nuevamente.",
            "We could not identify your email. Please sign in again."
          )
        );
      }

      const res = await fetch(`${API}/auth/password-reset/request`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept-Language": locale,
        },
        body: JSON.stringify({ email }),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo enviar el enlace de recuperación.", "Could not send recovery link.", "Impossible d'envoyer le lien de récupération."));
      }

      resetStatus = data?.message || tr(
        "Si el correo existe, enviaremos un enlace de recuperación.",
        "If the email exists, we will send a recovery link."
      );
    } catch (err) {
      resetError = err?.message || tr("No se pudo enviar el enlace de recuperación.", "Could not send recovery link.", "Impossible d'envoyer le lien de récupération.");
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
      emailChangeError = tr("Debes digitar tu contraseña actual.", "You must enter your current password.", "Tu dois saisir ton mot de passe actuel.");
      return;
    }

    if (!nextEmail) {
      emailChangeError = tr("Debes digitar el nuevo correo.", "You must enter the new email.", "Tu dois saisir le nouvel e-mail.");
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(nextEmail)) {
      emailChangeError = tr("Digita un correo electrónico válido.", "Enter a valid email address.", "Saisis une adresse e-mail valide.");
      return;
    }

    if (currentEmail && nextEmail === currentEmail) {
      emailChangeError = tr("El nuevo correo debe ser distinto al actual.", "The new email must be different from the current one.", "Le nouvel e-mail doit être différent de l'actuel.");
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
        throw new Error(data.detail || tr("No se pudo actualizar el correo.", "Could not update email.", "Impossible de mettre à jour l'e-mail."));
      }

      meEmail = String(data?.email || nextEmail);
      newEmail = "";
      emailCurrentPassword = "";
      showEmailCurrentPassword = false;
      emailChangeStatus = data?.message || tr("Correo actualizado correctamente.", "Email updated successfully.", "E-mail mis à jour avec succès.");
    } catch (err) {
      emailChangeError = err?.message || tr("No se pudo actualizar el correo.", "Could not update email.", "Impossible de mettre à jour l'e-mail.");
    } finally {
      isChangingEmail = false;
    }
  };

  const handleChangeName = async () => {
    nameChangeError = "";
    nameChangeStatus = "";

    const firstName = normalizeHumanName(profileFirstName);
    const lastName = normalizeHumanName(profileLastName);

    if (!firstName) {
      nameChangeError = tr("Debes digitar al menos un nombre.", "You must enter at least one first name.", "Tu dois saisir au moins un prénom.");
      return;
    }

    if (!lastName) {
      nameChangeError = tr("Debes digitar al menos un apellido.", "You must enter at least one last name.", "Tu dois saisir au moins un nom.");
      return;
    }

    isChangingName = true;
    try {
      const res = await apiFetch("/auth/profile/name", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
        }),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo actualizar tu nombre.", "Could not update your name.", "Impossible de mettre à jour ton nom."));
      }

      profileFirstName = normalizeHumanName(data?.first_name || firstName);
      profileLastName = normalizeHumanName(data?.last_name || lastName);
      nameChangeStatus = tr("Nombre y apellido actualizados correctamente.", "First and last name updated successfully.", "Prénom et nom mis à jour avec succès.");
    } catch (err) {
      nameChangeError = err?.message || tr("No se pudo actualizar tu nombre.", "Could not update your name.", "Impossible de mettre à jour ton nom.");
    } finally {
      isChangingName = false;
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
        throw new Error(data.detail || tr("No se pudo cargar el estado de 2FA.", "Could not load 2FA status.", "Impossible de charger l'état 2FA."));
      }
      twofaStatus = data || null;
    } catch (err) {
      twofaStatusError = err?.message || tr("No se pudo cargar el estado de 2FA.", "Could not load 2FA status.", "Impossible de charger l'état 2FA.");
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
      twofaConfirmStatus = tr("Código manual copiado al portapapeles.", "Manual code copied to clipboard.", "Code manuel copié dans le presse-papiers.");
    } catch {
      twofaConfirmStatus = tr(
        "No se pudo copiar automáticamente. Selecciona el código y cópialo.",
        "Could not copy automatically. Select the code and copy it."
      );
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
        throw new Error(data.detail || tr("No se pudo generar el QR de 2FA.", "Could not generate 2FA QR.", "Impossible de générer le QR 2FA."));
      }

      twofaQrCode = String(data?.qr_code || "");
      twofaManualCode = String(data?.manual_code || "");
      twofaIssuer = String(data?.issuer || "");
      twofaCode = "";

      await tick();
      twofaCodeInput?.focus();
    } catch (err) {
      twofaSetupError = err?.message || tr("No se pudo generar el QR de 2FA.", "Could not generate 2FA QR.", "Impossible de générer le QR 2FA.");
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
      twofaConfirmError = tr("Digita un código válido de 6 dígitos.", "Enter a valid 6-digit code.", "Saisis un code valide à 6 chiffres.");
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
        throw new Error(data.detail || tr("No se pudo activar 2FA.", "Could not enable 2FA.", "Impossible d'activer la 2FA."));
      }

      twofaConfirmStatus = tr(
        "2FA habilitado correctamente. A partir de ahora se te pedirá un código al iniciar sesión.",
        "2FA enabled successfully. You will now be asked for a code when signing in."
      );
      twofaQrCode = "";
      twofaManualCode = "";
      twofaIssuer = "";
      twofaCode = "";
      void refreshTwoFAStatus();
    } catch (err) {
      twofaConfirmError = err?.message || tr("No se pudo activar 2FA.", "Could not enable 2FA.", "Impossible d'activer la 2FA.");
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
        throw new Error(data.detail || tr("No se pudo deshabilitar 2FA.", "Could not disable 2FA.", "Impossible de désactiver la 2FA."));
      }
      if (data?.disabled) {
        twofaDisableStatus = tr("2FA deshabilitado.", "2FA disabled.", "2FA désactivée.");
      } else {
        twofaDisableStatus = tr("2FA actualizado.", "2FA updated.", "2FA mise à jour.");
      }
      twofaQrCode = "";
      twofaManualCode = "";
      twofaIssuer = "";
      twofaCode = "";
      void refreshTwoFAStatus();
    } catch (err) {
      twofaDisableError = err?.message || tr("No se pudo deshabilitar 2FA.", "Could not disable 2FA.", "Impossible de désactiver la 2FA.");
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
        throw new Error(data.detail || tr("No se pudo cargar tu configuración de privacidad.", "Could not load your privacy settings.", "Impossible de charger tes paramètres de confidentialité."));
      }
      privacySettings = normalizePrivacySettings(data);
    } catch (err) {
      privacyError = err?.message || tr("No se pudo cargar tu configuración de privacidad.", "Could not load your privacy settings.", "Impossible de charger tes paramètres de confidentialité.");
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
        throw new Error(data.detail || tr("No se pudo guardar tu configuración de privacidad.", "Could not save your privacy settings.", "Impossible d'enregistrer tes paramètres de confidentialité."));
      }
      privacySettings = normalizePrivacySettings(data);
      privacyStatus = tr("Privacidad actualizada correctamente.", "Privacy updated successfully.", "Confidentialité mise à jour avec succès.");
    } catch (err) {
      privacyError = err?.message || tr("No se pudo guardar tu configuración de privacidad.", "Could not save your privacy settings.", "Impossible d'enregistrer tes paramètres de confidentialité.");
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
      closeAccountError = tr("Selecciona un motivo para cerrar la cuenta.", "Select a reason to close the account.", "Sélectionne une raison pour fermer le compte.");
      return;
    }
    if (reason === ACCOUNT_CLOSE_REASON_OTHER && !otherReason) {
      closeAccountError = tr("Describe el motivo en la opción “Otro”.", "Describe the reason in the “Other” option.", "Décris la raison dans l'option « Autre ».");
      return;
    }
    if (!currentPassword.trim()) {
      closeAccountError = tr("Digita tu contraseña para confirmar el cierre de cuenta.", "Enter your password to confirm account closure.", "Saisis ton mot de passe pour confirmer la fermeture du compte.");
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
        throw new Error(data.detail || tr("No se pudo cerrar la cuenta.", "Could not close account.", "Impossible de fermer le compte."));
      }

      const deadlineDate = new Date(data?.restore_deadline_at || "");
      closeAccountDeadlineLabel = Number.isNaN(deadlineDate.getTime())
        ? ""
        : deadlineDate.toLocaleString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO");
      closeAccountStatus = data?.message || "";
      closeAccountDone = true;
      closeAccountPassword = "";
      closeAccountOtherReason = "";
      showCloseAccountPassword = false;
    } catch (err) {
      closeAccountError = err?.message || tr("No se pudo cerrar la cuenta.", "Could not close account.", "Impossible de fermer le compte.");
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
  <title>{tr("Kiadez — Configuración y privacidad", "Kiadez — Settings and privacy", "Kiadez — Paramètres et confidentialité")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background settings-page">
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input type="search" placeholder={tr("Buscar en Kiadez", "Search on Kiadez", "Rechercher sur Kiadez")} aria-label={tr("Buscar", "Search", "Rechercher")} />
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
          <img src="/assets/avatar-default.jpg" alt={tr("Foto de perfil del usuario", "User profile photo", "Photo de profil utilisateur")} />
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
          <a href="/home_user.html" role="menuitem">{tr("Mi Home", "My Home", "Mon Home")}</a>
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
    <div class="home-body settings-body">
      <section class="panel settings-panel" aria-label={tr("Configuración y privacidad", "Settings and privacy", "Paramètres et confidentialité")}>
        <div class="panel-head">
          <h2 class="panel-title">{tr("Configuración y privacidad", "Settings and privacy", "Paramètres et confidentialité")}</h2>
          <span class="panel-badge">{tr("Cuenta", "Account", "Compte")}</span>
        </div>

        <div class="settings-actions">
          <button class="settings-action" type="button" on:click={openChangePasswordModal}>
            <span class="settings-action-icon" aria-hidden="true">🔑</span>
            <span class="settings-action-label">{tr("Cambiar contraseña", "Change password", "Changer le mot de passe")}</span>
          </button>

          <button class="settings-action" type="button" on:click={openChangeEmailModal}>
            <span class="settings-action-icon" aria-hidden="true">📧</span>
            <span class="settings-action-label">{tr("Modificar correo electrónico", "Change email address", "Changer l'adresse e-mail")}</span>
          </button>

          <button class="settings-action" type="button" on:click={openChangeNameModal}>
            <span class="settings-action-icon" aria-hidden="true">🪪</span>
            <span class="settings-action-label">{tr("Modificar nombre y apellido", "Edit first and last name", "Modifier prénom et nom")}</span>
          </button>

          <button class="settings-action" type="button" on:click={openLanguageModal}>
            <span class="settings-action-icon" aria-hidden="true">🌍</span>
            <span class="settings-action-label">{tr("Idioma de la plataforma", "Platform language", "Langue de la plateforme")}</span>
          </button>

          <button class="settings-action" type="button" on:click={openTwoFAModal}>
            <span class="settings-action-icon" aria-hidden="true">🛡️</span>
            <span class="settings-action-label">{tr("Habilitar autenticación 2FA", "Enable 2FA authentication", "Activer l'authentification 2FA")}</span>
          </button>

          <button class="settings-action" type="button" on:click={openPrivacyModal}>
            <span class="settings-action-icon" aria-hidden="true">🔒</span>
            <span class="settings-action-label">{tr("Privacidad", "Privacy", "Confidentialité")}</span>
          </button>

          <button class="settings-action is-danger" type="button" on:click={openCloseAccountModal}>
            <span class="settings-action-icon" aria-hidden="true">🗑️</span>
            <span class="settings-action-label">{tr("Cerrar cuenta", "Close account", "Fermer le compte")}</span>
          </button>
        </div>
      </section>
    </div>
  </main>
  <AuthFooter />

  <div
    class="modal-overlay"
    class:hidden={!changeNameModalOpen}
    aria-hidden={!changeNameModalOpen}
    on:click={(event) => {
      if (event.target?.classList?.contains("modal-overlay")) closeChangeNameModal();
    }}
  >
    <div
      class="modal settings-change-password-modal"
      role="dialog"
      aria-modal="true"
      aria-label={tr("Modificar nombre y apellido", "Edit first and last name", "Modifier prénom et nom")}
    >
      <div class="modal-head">
        <h3>{tr("Modificar nombre y apellido", "Edit first and last name", "Modifier prénom et nom")}</h3>
        <button class="modal-close" type="button" on:click={closeChangeNameModal}>✕</button>
      </div>

      <div class="modal-body">
        <p class="panel-text settings-change-intro">
          {tr(
            "Ajusta tu nombre visible como prefieras: puedes corregir apellidos, quitar un segundo nombre o agregar nuevos nombres.",
            "Adjust your visible name as you prefer: you can correct last names, remove a middle name, or add new given names.",
            "Ajuste ton nom visible comme tu veux : tu peux corriger des noms de famille, retirer un deuxième prénom ou ajouter de nouveaux prénoms."
          )}
        </p>

        <label class="modal-label" for="settings-first-name">
          {tr("Nombre(s)", "First name(s)", "Prénom(s)")}
        </label>
        <input
          class="modal-input"
          id="settings-first-name"
          bind:this={firstNameInput}
          type="text"
          bind:value={profileFirstName}
          autocomplete="given-name"
          maxlength="100"
          placeholder={tr("Ej: Carlos Andrés", "Ex: Carlos Andrew", "Ex. : Carlos André")}
        />

        <label class="modal-label" for="settings-last-name">
          {tr("Apellido(s)", "Last name(s)", "Nom(s)")}
        </label>
        <input
          class="modal-input"
          id="settings-last-name"
          type="text"
          bind:value={profileLastName}
          autocomplete="family-name"
          maxlength="100"
          placeholder={tr("Ej: Jiménez Duarte", "Ex: Johnson Smith", "Ex. : Dupont Martin")}
        />

        {#if nameChangeError}
          <p class="settings-form-error" role="alert">{nameChangeError}</p>
        {/if}
        {#if nameChangeStatus}
          <p class="settings-form-success" role="status">{nameChangeStatus}</p>
        {/if}
      </div>

      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" on:click={handleChangeName} disabled={isChangingName}>
          {isChangingName ? tr("Actualizando...", "Updating...", "Mise à jour...") : tr("Actualizar nombre", "Update name", "Mettre à jour le nom")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" on:click={closeChangeNameModal}>
          {tr("Cerrar", "Close", "Fermer")}
        </button>
      </div>
    </div>
  </div>

  <div
    class="modal-overlay"
    class:hidden={!languageModalOpen}
    aria-hidden={!languageModalOpen}
    on:click={(event) => {
      if (event.target?.classList?.contains("modal-overlay")) closeLanguageModal();
    }}
  >
    <div class="modal settings-language-modal" role="dialog" aria-modal="true" aria-label={tr("Idioma de la plataforma", "Platform language", "Langue de la plateforme")}>
      <div class="modal-head">
        <h3>{tr("Idioma de la plataforma", "Platform language", "Langue de la plateforme")}</h3>
        <button class="modal-close" type="button" on:click={closeLanguageModal}>✕</button>
      </div>

      <div class="modal-body">
        <p class="panel-text settings-close-account-intro">
          {tr(
            "Selecciona el idioma de tu interfaz. Al confirmar, recargaremos esta vista para aplicar el cambio completo.",
            "Select your interface language. When you confirm, we will reload this view to apply the change completely.",
            "Sélectionne la langue de ton interface. Lors de la confirmation, nous rechargerons cette vue pour appliquer complètement le changement."
          )}
        </p>

        <fieldset class="settings-close-account-reasons">
          <legend class="settings-close-account-legend">{tr("Idiomas disponibles", "Available languages", "Langues disponibles")}</legend>

          <label class="settings-close-account-option">
            <input type="radio" name="settings-language" checked={locale === "es"} on:change={() => applyLocale("es")} />
            <span>Español</span>
          </label>

          <label class="settings-close-account-option">
            <input type="radio" name="settings-language" checked={locale === "en"} on:change={() => applyLocale("en")} />
            <span>English</span>
          </label>

          <label class="settings-close-account-option">
            <input type="radio" name="settings-language" checked={locale === "fr"} on:change={() => applyLocale("fr")} />
            <span>Français</span>
          </label>
        </fieldset>
      </div>

      <div class="modal-actions">
        <button class="btn btn-outline btn-compact" type="button" on:click={closeLanguageModal}>
          {tr("Cerrar", "Close", "Fermer")}
        </button>
      </div>
    </div>
  </div>

  <div
    class="modal-overlay"
    class:hidden={!closeAccountModalOpen}
    aria-hidden={!closeAccountModalOpen}
    on:click={(event) => {
      if (event.target?.classList?.contains("modal-overlay") && !closeAccountDone) closeCloseAccountModal();
    }}
  >
    <div class="modal settings-close-account-modal" role="dialog" aria-modal="true" aria-label={tr("Cerrar cuenta", "Close account", "Fermer le compte")}>
      <div class="modal-head">
        <h3>{tr("Cerrar cuenta", "Close account", "Fermer le compte")}</h3>
        {#if !closeAccountDone}
          <button class="modal-close" type="button" on:click={closeCloseAccountModal}>✕</button>
        {/if}
      </div>

      <div class="modal-body">
        {#if closeAccountDone}
          <p class="panel-text settings-close-account-summary">
            {closeAccountStatus || tr("Tu cuenta fue cerrada correctamente.", "Your account was closed successfully.", "Ton compte a été fermé avec succès.")}
          </p>
          {#if closeAccountDeadlineLabel}
            <p class="panel-muted">
              {tr("Puedes restaurarla hasta el", "You can restore it until", "Tu peux le restaurer jusqu'à")} <strong>{closeAccountDeadlineLabel}</strong> {tr("iniciando sesión con tu clave o recuperándola.", "by signing in with your password or recovering it.", "en te connectant avec ton mot de passe ou en le récupérant.")}
            </p>
          {/if}
        {:else}
          <p class="panel-text settings-close-account-intro">
            {tr("Selecciona el motivo principal por el cual deseas cerrar tu cuenta.", "Select the main reason why you want to close your account.", "Sélectionne la raison principale pour laquelle tu veux fermer ton compte.")}
          </p>

          <fieldset class="settings-close-account-reasons">
            <legend class="settings-close-account-legend">{tr("Motivo del cierre", "Reason for closure", "Raison de fermeture")}</legend>
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
            <label class="modal-label" for="close-account-other-reason">{tr("Especifica el motivo", "Specify the reason", "Précise la raison")}</label>
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
            {tr(
              "Al cerrar la cuenta, tu información quedará inhabilitada para el sistema público. Además, eliminaremos tus deseos públicos y privados, publicaciones, reacciones y comentarios.",
              "When closing your account, your information will be disabled for the public system. In addition, we will remove your public and private wishes, posts, reactions, and comments."
            )}
          </div>

          <label class="modal-label" for="close-account-password">{tr("Digita tu contraseña para confirmar", "Enter your password to confirm", "Saisis ton mot de passe pour confirmer")}</label>
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
              aria-label={showCloseAccountPassword ? tr("Ocultar contraseña", "Hide password", "Masquer le mot de passe") : tr("Mostrar contraseña", "Show password", "Afficher le mot de passe")}
              on:click={() => (showCloseAccountPassword = !showCloseAccountPassword)}
            >
              👁️
            </button>
          </div>

          <p class="panel-muted settings-close-account-window">
            {tr(
              "Después de confirmar, tendrás 30 días para volver con esa misma contraseña o recuperándola si la olvidas. Si no regresas en ese plazo, la cuenta se eliminará permanentemente.",
              "After confirming, you will have 30 days to return with that same password or recover it if you forget it. If you do not return within that period, the account will be permanently deleted."
            )}
          </p>

          {#if closeAccountError}
            <p class="settings-form-error" role="alert">{closeAccountError}</p>
          {/if}
        {/if}
      </div>

      <div class="modal-actions">
        {#if closeAccountDone}
          <button class="btn btn-primary btn-compact" type="button" on:click={() => logout()}>
            {tr("Ir al inicio de sesión", "Go to sign in", "Aller à la connexion")}
          </button>
        {:else}
          <button class="btn btn-primary btn-compact settings-close-account-confirm" type="button" on:click={handleConfirmCloseAccount} disabled={closeAccountLoading}>
            {closeAccountLoading ? tr("Cerrando...", "Closing...", "Fermeture...") : tr("Confirmar cierre de cuenta", "Confirm account closure", "Confirmer la fermeture du compte")}
          </button>
          <button class="btn btn-outline btn-compact" type="button" on:click={closeCloseAccountModal} disabled={closeAccountLoading}>
            {tr("Cancelar", "Cancel", "Annuler")}
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
    <div class="modal settings-privacy-modal" role="dialog" aria-modal="true" aria-label={tr("Privacidad del perfil público", "Public profile privacy", "Confidentialité du profil public")}>
      <div class="modal-head">
        <h3>{tr("Privacidad del perfil público", "Public profile privacy", "Confidentialité du profil public")}</h3>
        <button class="modal-close" type="button" on:click={closePrivacyModal}>✕</button>
      </div>

      <div class="modal-body">
        <p class="panel-text settings-privacy-intro">
          {tr(
            "Decide qué partes de tu perfil estarán visibles para otros usuarios. Estos cambios no afectan lo que tú puedes ver dentro de Kiadez.",
            "Decide which parts of your profile will be visible to other users. These changes do not affect what you can see inside Kiadez."
          )}
        </p>

        {#if privacyLoading}
          <p class="panel-muted">{tr("Cargando configuración de privacidad...", "Loading privacy settings...", "Chargement des paramètres de confidentialité...")}</p>
        {:else}
          <div class="settings-privacy-grid">
            {#each PRIVACY_TOGGLES as toggle}
              <div class="privacy-item settings-privacy-item">
                <div class="settings-privacy-main">
                  <span class="privacy-label">{toggle.label}</span>
                  <p class="settings-privacy-help">{toggle.description}</p>
                </div>
                <label class="switch" aria-label={`${tr("Alternar visibilidad de", "Toggle visibility of", "Basculer la visibilité de")} ${toggle.label}`}>
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
          {privacySaving ? tr("Guardando...", "Saving...", "Enregistrement...") : tr("Guardar", "Save", "Enregistrer")}
        </button>
        <button class="btn btn-outline btn-compact" type="button" on:click={closePrivacyModal}>
          {tr("Cerrar", "Close", "Fermer")}
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
      aria-label={tr("Cambiar contraseña", "Change password", "Changer le mot de passe")}
    >
      <div class="modal-head">
        <h3>{changePasswordMode === "change" ? tr("Cambiar contraseña", "Change password", "Changer le mot de passe") : tr("Recuperar contraseña", "Recover password", "Récupérer le mot de passe")}</h3>
        <button class="modal-close" type="button" on:click={closeChangePasswordModal}>✕</button>
      </div>

      <div class="modal-body">
        {#if changePasswordMode === "change"}
          <p class="panel-text settings-change-intro">
            {tr(
              "Para actualizar tu contraseña, primero confirma tu contraseña de inicio de sesión.",
              "To update your password, first confirm your sign-in password."
            )}
          </p>

          <label class="modal-label" for="settings-current-password">
            {tr("Digita tu contraseña actual", "Enter your current password", "Saisis ton mot de passe actuel")}
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
              aria-label={showCurrentPassword ? tr("Ocultar contraseña", "Hide password", "Masquer le mot de passe") : tr("Mostrar contraseña", "Show password", "Afficher le mot de passe")}
              on:click={() => (showCurrentPassword = !showCurrentPassword)}
            >
              👁️
            </button>
          </div>

          <div class="settings-change-section">
            <h4 class="settings-change-section-title">{tr("Cambiar contraseña", "Change password", "Changer le mot de passe")}</h4>

            <label class="modal-label" for="settings-new-password">
              {tr("Digita tu nueva contraseña", "Enter your new password", "Saisis ton nouveau mot de passe")}
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
                aria-label={showNewPassword ? tr("Ocultar contraseña", "Hide password", "Masquer le mot de passe") : tr("Mostrar contraseña", "Show password", "Afficher le mot de passe")}
                on:click={() => (showNewPassword = !showNewPassword)}
              >
                👁️
              </button>
            </div>

            <div class="settings-password-rules" aria-label={tr("Normativa de contraseña", "Password policy", "Politique de mot de passe")}>
              <div class:ok={newPasswordRules.length} class="settings-password-rule">
                {newPasswordRules.length ? "✔" : "•"} {tr("Mínimo", "Minimum", "Minimum")} {PASSWORD_MIN_LENGTH} {tr("caracteres", "characters", "caractères")}
              </div>
              <div class:ok={newPasswordRules.upper} class="settings-password-rule">
                {newPasswordRules.upper ? "✔" : "•"} {tr("Al menos 1 mayúscula", "At least 1 uppercase letter", "Au moins 1 majuscule")}
              </div>
              <div class:ok={newPasswordRules.digit} class="settings-password-rule">
                {newPasswordRules.digit ? "✔" : "•"} {tr("Al menos 1 número", "At least 1 number", "Au moins 1 chiffre")}
              </div>
              <div class:ok={newPasswordRules.special} class="settings-password-rule">
                {newPasswordRules.special ? "✔" : "•"} {tr("Al menos 1 caracter especial", "At least 1 special character", "Au moins 1 caractère spécial")}
              </div>
            </div>

            <label class="modal-label" for="settings-new-password-confirm">
              {tr("Confirma tu nueva contraseña", "Confirm your new password", "Confirme ton nouveau mot de passe")}
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
                aria-label={showNewPasswordConfirm ? tr("Ocultar contraseña", "Hide password", "Masquer le mot de passe") : tr("Mostrar contraseña", "Show password", "Afficher le mot de passe")}
                on:click={() => (showNewPasswordConfirm = !showNewPasswordConfirm)}
              >
                👁️
              </button>
            </div>

            <div class="settings-change-section-actions">
              <button class="btn btn-primary btn-compact" type="button" on:click={handleChangePassword} disabled={isChangingPassword}>
                {isChangingPassword ? tr("Confirmando...", "Confirming...", "Confirmation...") : tr("Actualizar contraseña", "Update password", "Mettre à jour le mot de passe")}
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
              {tr("¿Olvidaste tu contraseña?", "Forgot your password?", "Mot de passe oublié ?")}
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
            {tr(
              "Si ya no recuerdas tu contraseña, te enviaremos un enlace seguro para restablecerla.",
              "If you no longer remember your password, we will send you a secure link to reset it."
            )}
          </p>

          {#if meEmail}
            <p class="panel-muted settings-reset-meta">
              {tr("Enviaremos el enlace a:", "We will send the link to:", "Nous enverrons le lien à :")} <strong>{meEmail}</strong>
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
            {tr("Cerrar", "Close", "Fermer")}
          </button>
        {:else}
          <button class="btn btn-primary btn-compact" type="button" on:click={handleSendPasswordReset} disabled={isSendingReset}>
            {isSendingReset ? tr("Enviando...", "Sending...", "Envoi...") : tr("Enviar enlace", "Send link", "Envoyer le lien")}
          </button>
          <button class="btn btn-outline btn-compact" type="button" on:click={() => (changePasswordMode = "change")}>
            {tr("Volver", "Back", "Retour")}
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
      aria-label={tr("Modificar correo electrónico", "Change email address", "Changer l'adresse e-mail")}
    >
      <div class="modal-head">
        <h3>{tr("Modificar correo electrónico", "Change email address", "Changer l'adresse e-mail")}</h3>
        <button class="modal-close" type="button" on:click={closeChangeEmailModal}>✕</button>
      </div>

      <div class="modal-body">
        <p class="panel-text settings-change-intro">
          {tr(
            "Para actualizar tu correo, primero confirma tu contraseña de inicio de sesión.",
            "To update your email, first confirm your sign-in password."
          )}
        </p>

        <label class="modal-label" for="settings-email-current-password">
          {tr("Digita tu contraseña actual", "Enter your current password", "Saisis ton mot de passe actuel")}
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
            aria-label={showEmailCurrentPassword ? tr("Ocultar contraseña", "Hide password", "Masquer le mot de passe") : tr("Mostrar contraseña", "Show password", "Afficher le mot de passe")}
            on:click={() => (showEmailCurrentPassword = !showEmailCurrentPassword)}
          >
            👁️
          </button>
        </div>

        <div class="settings-change-section">
          <h4 class="settings-change-section-title">{tr("Cambiar correo electrónico", "Change email address", "Changer l'adresse e-mail")}</h4>

          {#if meEmail}
            <p class="panel-muted settings-change-current-email">
              {tr("Correo actual:", "Current email:", "E-mail actuel :")} <strong>{meEmail}</strong>
            </p>
          {/if}

          <label class="modal-label" for="settings-new-email">
            {tr("Digita tu nuevo correo electrónico", "Enter your new email address", "Saisis ta nouvelle adresse e-mail")}
          </label>
          <input
            class="modal-input"
            id="settings-new-email"
            type="email"
            bind:value={newEmail}
            autocomplete="email"
            placeholder={tr("nuevo-correo@ejemplo.com", "new-email@example.com", "nouvel-email@exemple.com")}
          />

          <div class="settings-change-section-actions">
            <button class="btn btn-primary btn-compact" type="button" on:click={handleChangeEmail} disabled={isChangingEmail}>
              {isChangingEmail ? tr("Actualizando...", "Updating...", "Mise à jour...") : tr("Actualizar correo", "Update email", "Mettre à jour l'e-mail")}
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
          {tr("Cerrar", "Close", "Fermer")}
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
    <div class="modal settings-twofa-modal" role="dialog" aria-modal="true" aria-label={tr("Autenticación 2FA", "2FA authentication", "Authentification 2FA")}>
      <div class="modal-head">
        <h3>{tr("Autenticación 2FA", "2FA authentication", "Authentification 2FA")}</h3>
        <button class="modal-close" type="button" on:click={closeTwoFAModal}>✕</button>
      </div>

      <div class="modal-body">
        <p class="panel-text settings-twofa-intro">
          {tr(
            "Protege tu cuenta con un segundo factor (TOTP). Al iniciar sesión, además de tu contraseña, se te pedirá un código de 6 dígitos.",
            "Protect your account with a second factor (TOTP). When signing in, in addition to your password, you will be asked for a 6-digit code."
          )}
        </p>

        {#if twofaStatusLoading}
          <p class="panel-muted">{tr("Cargando estado de 2FA...", "Loading 2FA status...", "Chargement de l'état 2FA...")}</p>
        {:else if twofaStatusError}
          <p class="settings-form-error" role="alert">{twofaStatusError}</p>
        {:else}
          <div class="settings-twofa-status">
            <span class="panel-badge">
              {tr("Estado:", "Status:", "Statut :")} {twofaStatus?.is_enabled ? tr("Activo", "Active", "Actif") : tr("Inactivo", "Inactive", "Inactif")}
            </span>
            {#if twofaStatus?.is_enabled && twofaStatus?.confirmed_at}
              <span class="panel-muted settings-twofa-date">
                {tr("Activado el", "Enabled on", "Activé le")} {new Date(twofaStatus.confirmed_at).toLocaleDateString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO")}
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
              {twofaDisableLoading ? tr("Deshabilitando...", "Disabling...", "Désactivation...") : tr("Deshabilitar 2FA", "Disable 2FA", "Désactiver la 2FA")}
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
              {twofaSetupLoading ? tr("Generando...", "Generating...", "Génération...") : tr("Generar nuevo 2FA", "Generate new 2FA", "Générer une nouvelle 2FA")}
            </button>
          </div>
        {:else}
          <div class="settings-twofa-actions">
            <button class="btn btn-primary btn-compact" type="button" on:click={handleTwoFASetup} disabled={twofaSetupLoading}>
              {twofaSetupLoading ? tr("Generando...", "Generating...", "Génération...") : twofaQrCode ? tr("Regenerar QR", "Regenerate QR", "Régénérer le QR") : tr("Generar QR", "Generate QR", "Générer le QR")}
            </button>
          </div>
        {/if}

        {#if twofaSetupError}
          <p class="settings-form-error" role="alert">{twofaSetupError}</p>
        {/if}

        {#if twofaQrCode}
          <div class="settings-twofa-setup">
            <div class="settings-twofa-qr">
              <img src={twofaQrCode} alt={tr("QR de autenticación 2FA", "2FA authentication QR", "QR d'authentification 2FA")} />
            </div>

            <div class="settings-twofa-manual">
              <div class="panel-muted settings-twofa-manual-label">
                {tr("Código manual (para apps como KeePassXC):", "Manual code (for apps like KeePassXC):", "Code manuel (pour des apps comme KeePassXC) :")}
              </div>
              <div class="settings-twofa-manual-row">
                <code class="settings-twofa-manual-code">{twofaManualCode}</code>
                <button class="btn btn-outline btn-compact settings-twofa-copy" type="button" on:click={copyTwoFAManualCode}>
                  {tr("Copiar", "Copy", "Copier")}
                </button>
              </div>
              {#if twofaIssuer}
                <div class="panel-muted settings-twofa-issuer">
                  {tr("Emisor:", "Issuer:", "Émetteur :")} <strong>{twofaIssuer}</strong>
                </div>
              {/if}
            </div>
          </div>

          <label class="modal-label" for="settings-twofa-code">
            {tr("Digita el código de 6 dígitos de tu app autenticadora", "Enter the 6-digit code from your authenticator app", "Saisis le code à 6 chiffres de ton application d'authentification")}
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
            {twofaConfirmLoading ? tr("Confirmando...", "Confirming...", "Confirmation...") : tr("Confirmar", "Confirm", "Confirmer")}
          </button>
        {/if}
        <button class="btn btn-outline btn-compact" type="button" on:click={closeTwoFAModal}>
          {tr("Cerrar", "Close", "Fermer")}
        </button>
      </div>
    </div>
  </div>
</div>
