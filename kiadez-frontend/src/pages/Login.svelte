<script>
  import { onMount } from "svelte";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { t } from "../lib/i18n";

  onMount(() => {
    const API = "http://127.0.0.1:8000";
    const form = document.getElementById("auth-form");
    const authErrorEl = document.getElementById("auth-error");
    if (!form || !authErrorEl) return undefined;

    const twofaOverlay = document.getElementById("twofaLoginOverlay");
    const twofaCodeInput = document.getElementById("twofa-login-code");
    const twofaConfirmBtn = document.getElementById("twofa-login-confirm");
    const twofaCancelBtn = document.getElementById("twofa-login-cancel");
    const twofaCancelFooterBtn = document.getElementById("twofa-login-cancel-footer");
    const twofaErrorEl = document.getElementById("twofa-login-error");

    let pending2FATempToken = "";

    const setAuthError = (message) => {
      const text = String(message || "");
      authErrorEl.textContent = text;
      authErrorEl.classList.toggle("hidden", !text);
    };

    const setTwofaError = (message) => {
      if (!twofaErrorEl) return;
      const text = String(message || "");
      twofaErrorEl.textContent = text;
      twofaErrorEl.classList.toggle("hidden", !text);
    };

    const setTwofaModalOpen = (isOpen) => {
      if (!twofaOverlay) return;
      const open = Boolean(isOpen);
      twofaOverlay.classList.toggle("hidden", !open);
      twofaOverlay.setAttribute("aria-hidden", String(!open));

      if (open) {
        setTwofaError("");
        if (twofaCodeInput) {
          twofaCodeInput.value = "";
          setTimeout(() => twofaCodeInput?.focus(), 0);
        }
      } else {
        pending2FATempToken = "";
        if (twofaCodeInput) twofaCodeInput.value = "";
        setTwofaError("");
      }
    };

    const persistTokens = (data) => {
      if (data?.access_token) {
        localStorage.setItem("access_token", data.access_token);
      }
      if (data?.refresh_token) {
        localStorage.setItem("refresh_token", data.refresh_token);
      }
    };

    const login = async (email, password) => {
      const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      if (!res.ok) {
        const error = new Error(data.detail || t("auth.login.errors.start_session"));
        error.status = res.status;
        throw error;
      }

      if (data?.["2fa_required"]) {
        return {
          twofa_required: true,
          temp_token: data?.temp_token || "",
        };
      }

      persistTokens(data);
      return {
        twofa_required: false,
        access_token: data.access_token,
      };
    };

    const verify2fa = async (tempToken, code) => {
      const res = await fetch(`${API}/auth/2fa/verify`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${tempToken}`,
        },
        body: JSON.stringify({ code }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || t("auth.login.errors.twofa_incorrect"));
      }

      persistTokens(data);
      return data.access_token;
    };

    const checkVault = async (token) => {
      const res = await fetch(`${API}/vault/status`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || t("auth.login.errors.vault_check"));
      }

      return data.has_vault;
    };

    const checkLifePurposeConfigured = async (token) => {
      const res = await fetch(`${API}/life-purpose/mine`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || t("auth.login.errors.life_purpose_check"));
      }

      const slots = Array.isArray(data?.slots) ? data.slots : [];
      const slotNumbers = new Set(
        slots
          .map((slot) => Number(slot?.slot_number))
          .filter((n) => Number.isFinite(n) && n >= 1 && n <= 3)
      );
      return slotNumbers.size >= 3;
    };

    const continueAfterLogin = async (token) => {
      const hasVault = await checkVault(token);
      if (!hasVault) {
        window.location.href = "/create-private-key.html";
        return;
      }

      const hasLifePurpose = await checkLifePurposeConfigured(token);
      if (hasLifePurpose) {
        window.location.href = "/home_user.html";
        return;
      }

      window.location.href = "/life-proposal.html";
    };

    const handleSubmit = async (event) => {
      event.preventDefault();
      setAuthError("");

      const email = form.email.value;
      const password = form.password.value;

      try {
        const result = await login(email, password);
        if (result?.twofa_required) {
          pending2FATempToken = result?.temp_token || "";
          setTwofaModalOpen(true);
          return;
        }

        const token = result?.access_token;
        await continueAfterLogin(token);
      } catch (err) {
        const errorMessage = String(err?.message || "");
        const invalidCredentials =
          Number(err?.status) === 401 || /credenciales|credentials/i.test(errorMessage);
        if (invalidCredentials) {
          setAuthError(t("auth.login.errors.invalid_credentials"));
        } else {
          setAuthError(errorMessage || t("auth.login.errors.generic"));
        }
        console.error(err);
      }
    };

    const handleEmailInput = () => setAuthError("");
    const handlePasswordInput = () => setAuthError("");

    const handleTwofaConfirm = async () => {
      setTwofaError("");
      const code = (twofaCodeInput?.value || "").trim();
      if (!/^[0-9]{6}$/.test(code)) {
        setTwofaError(t("auth.login.twofa.invalid_code"));
        return;
      }

      try {
        if (twofaConfirmBtn) twofaConfirmBtn.disabled = true;
        const token = await verify2fa(pending2FATempToken, code);
        setTwofaModalOpen(false);
        await continueAfterLogin(token);
      } catch (err) {
        setTwofaError(err.message || t("auth.login.errors.twofa_incorrect"));
        console.error(err);
      } finally {
        if (twofaConfirmBtn) twofaConfirmBtn.disabled = false;
      }
    };

    const handleTwofaKeydown = (event) => {
      if (event.key !== "Enter") return;
      event.preventDefault();
      void handleTwofaConfirm();
    };

    const handleTwofaConfirmClick = () => {
      void handleTwofaConfirm();
    };

    const handleTwofaCancel = () => {
      setTwofaModalOpen(false);
    };

    const handleTwofaOverlayClick = (event) => {
      if (event.target === twofaOverlay) setTwofaModalOpen(false);
    };

    form.addEventListener("submit", handleSubmit);
    form.email?.addEventListener("input", handleEmailInput);
    form.password?.addEventListener("input", handlePasswordInput);
    twofaConfirmBtn?.addEventListener("click", handleTwofaConfirmClick);
    twofaCodeInput?.addEventListener("keydown", handleTwofaKeydown);
    twofaCancelBtn?.addEventListener("click", handleTwofaCancel);
    twofaCancelFooterBtn?.addEventListener("click", handleTwofaCancel);
    twofaOverlay?.addEventListener("click", handleTwofaOverlayClick);

    const params = new URLSearchParams(window.location.search);
    const emailParam = params.get("email");
    if (emailParam) {
      const emailInput = form.querySelector('input[name="email"]');
      if (emailInput) emailInput.value = emailParam;
    }

    return () => {
      form.removeEventListener("submit", handleSubmit);
      form.email?.removeEventListener("input", handleEmailInput);
      form.password?.removeEventListener("input", handlePasswordInput);
      twofaConfirmBtn?.removeEventListener("click", handleTwofaConfirmClick);
      twofaCodeInput?.removeEventListener("keydown", handleTwofaKeydown);
      twofaCancelBtn?.removeEventListener("click", handleTwofaCancel);
      twofaCancelFooterBtn?.removeEventListener("click", handleTwofaCancel);
      twofaOverlay?.removeEventListener("click", handleTwofaOverlayClick);
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{t("auth.login.meta_title")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-backgroundlogin">
  <main class="auth-center">
    <div class="auth-card auth-card--wide">
      <h2 class="auth-title">{t("auth.login.title")}</h2>

      <form id="auth-form">
        <input type="email" name="email" placeholder={t("auth.login.email_placeholder")} required />
        <input type="password" name="password" placeholder={t("auth.login.password_placeholder")} required />
        <p id="auth-error" class="auth-form-error hidden" role="alert"></p>

        <button type="submit" class="btn btn-primary">
          {t("auth.login.submit")}
        </button>

        <a href="/forgot-password.html" class="auth-link">
          {t("auth.login.forgot_password")}
        </a>

        <div class="auth-divider"></div>

        <a href="/register.html" class="btn btn-outline">
          {t("auth.login.create_account")}
        </a>
      </form>

      <div class="auth-brand">
        <img src="/css/logo-kiadez.webp" alt={t("common.brand")} />
        <span>{t("common.brand")}</span>
      </div>
    </div>
  </main>

  <AuthFooter />

  <div class="modal-overlay hidden" id="twofaLoginOverlay" aria-hidden="true">
    <div class="modal twofa-login-modal" role="dialog" aria-modal="true" aria-label={t("auth.login.twofa.modal_aria")}>
      <div class="modal-head">
        <h3>{t("auth.login.twofa.title")}</h3>
        <button class="modal-close" type="button" id="twofa-login-cancel" aria-label={t("auth.login.twofa.close_aria")}>✕</button>
      </div>
      <div class="modal-body">
        <p class="panel-text">
          {t("auth.login.twofa.description")}
        </p>
        <input
          class="modal-input"
          id="twofa-login-code"
          type="text"
          inputmode="numeric"
          autocomplete="one-time-code"
          placeholder={t("auth.login.twofa.input_placeholder")}
          maxlength="6"
        />
        <p class="settings-form-error hidden" id="twofa-login-error" role="alert"></p>
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" id="twofa-login-confirm">{t("auth.login.twofa.confirm")}</button>
        <button class="btn btn-outline btn-compact" type="button" id="twofa-login-cancel-footer">{t("auth.login.twofa.cancel")}</button>
      </div>
    </div>
  </div>
</div>
