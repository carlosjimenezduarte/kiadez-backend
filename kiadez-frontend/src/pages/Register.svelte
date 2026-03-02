<script>
  import { onMount } from "svelte";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { t } from "../lib/i18n";

  onMount(() => {
    const form = document.getElementById("register-form");
    if (!form) return undefined;

    const passwordInput = form.querySelector('input[name="password"]');
    const passwordConfirmInput = form.querySelector('input[name="password_confirm"]');
    const passwordToggle = document.getElementById("registerPasswordToggle");
    const passwordConfirmToggle = document.getElementById("registerPasswordConfirmToggle");
    const passwordWarning = document.getElementById("password-warning");
    const passwordWarningLive = passwordWarning?.querySelector?.(".form-warning-live");

    const PASSWORD_POLICY_MESSAGE = t("auth.register.password.policy");

    const passwordMeetsPolicy = (value) => {
      const password = String(value || "");
      if (password.length < 8) return false;
      if (!/[A-Z]/.test(password)) return false;
      if (!/[0-9]/.test(password)) return false;
      if (!/[^a-zA-Z0-9]/.test(password)) return false;
      return true;
    };

    const setPasswordWarning = (message) => {
      if (!passwordWarning) return;
      const text = (message || "").trim();
      if (passwordWarningLive) passwordWarningLive.textContent = text;
      passwordWarning.classList.toggle("is-hidden", !text);
    };

    const updatePasswordWarning = () => {
      const password = passwordInput?.value || "";
      const confirm = passwordConfirmInput?.value || "";

      if (password && !passwordMeetsPolicy(password)) {
        setPasswordWarning(PASSWORD_POLICY_MESSAGE);
        return;
      }

      if (passwordMeetsPolicy(password) && confirm && password !== confirm) {
        if (confirm.length >= password.length) {
          setPasswordWarning(t("auth.register.password.mismatch"));
        } else {
          setPasswordWarning("");
        }
        return;
      }

      setPasswordWarning("");
    };

    const applyPasswordToggleState = (input, button) => {
      if (!input || !button) return;
      const isVisible = input.type === "text";
      button.classList.toggle("is-visible", isVisible);
      button.setAttribute("aria-pressed", isVisible ? "true" : "false");
      button.setAttribute("aria-label", isVisible ? t("auth.register.password.hide") : t("auth.register.password.show"));
      button.title = isVisible ? t("auth.register.password.hide") : t("auth.register.password.show");
    };

    const togglePasswordVisibility = (input, button) => {
      if (!input || !button) return;
      input.type = input.type === "password" ? "text" : "password";
      applyPasswordToggleState(input, button);
      input.focus();
    };

    const handlePasswordToggleClick = () => togglePasswordVisibility(passwordInput, passwordToggle);
    const handlePasswordConfirmToggleClick = () =>
      togglePasswordVisibility(passwordConfirmInput, passwordConfirmToggle);

    const handleSubmit = async (event) => {
      event.preventDefault();

      const data = new FormData(form);
      const password = String(data.get("password") || "");
      const passwordConfirm = String(data.get("password_confirm") || "");

      updatePasswordWarning();
      if (!passwordMeetsPolicy(password)) {
        setPasswordWarning(PASSWORD_POLICY_MESSAGE);
        passwordInput?.focus();
        return;
      }
      if (password !== passwordConfirm) {
        setPasswordWarning(t("auth.register.password.mismatch"));
        passwordConfirmInput?.focus();
        return;
      }

      const payload = {
        first_name: data.get("first_name"),
        last_name: data.get("last_name"),
        email: data.get("email"),
        birth_date: data.get("birth_date"),
        gender: data.get("gender"),
        password,
      };

      try {
        const response = await fetch("http://127.0.0.1:8000/auth/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();
        if (!response.ok) {
          alert(result.detail || t("auth.register.alerts.register_error"));
          return;
        }

        window.location.href = `check-email.html?email=${encodeURIComponent(String(payload.email || ""))}`;
      } catch (error) {
        console.error(error);
        alert(t("auth.register.alerts.server_error"));
      }
    };

    passwordInput?.addEventListener("input", updatePasswordWarning);
    passwordConfirmInput?.addEventListener("input", updatePasswordWarning);
    passwordToggle?.addEventListener("click", handlePasswordToggleClick);
    passwordConfirmToggle?.addEventListener("click", handlePasswordConfirmToggleClick);
    form.addEventListener("submit", handleSubmit);

    applyPasswordToggleState(passwordInput, passwordToggle);
    applyPasswordToggleState(passwordConfirmInput, passwordConfirmToggle);

    return () => {
      passwordInput?.removeEventListener("input", updatePasswordWarning);
      passwordConfirmInput?.removeEventListener("input", updatePasswordWarning);
      passwordToggle?.removeEventListener("click", handlePasswordToggleClick);
      passwordConfirmToggle?.removeEventListener("click", handlePasswordConfirmToggleClick);
      form.removeEventListener("submit", handleSubmit);
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <title>{t("auth.register.meta_title")}</title>
  <link rel="stylesheet" href="/css/register.css" />
</svelte:head>

<div class="page-background">
  <main class="hero">
    <section class="hero-left">
      <div class="auth-card">
        <h2 class="auth-title">{t("auth.register.title")}</h2>

        <form id="register-form">
          <input type="text" name="first_name" placeholder={t("auth.register.first_name_placeholder")} required />
          <input type="text" name="last_name" placeholder={t("auth.register.last_name_placeholder")} required />
          <input type="email" name="email" placeholder={t("auth.register.email_placeholder")} required />

          <input type="date" name="birth_date" id="birthdate" required />

          <select name="gender" required>
            <option value="">{t("auth.register.gender_placeholder")}</option>
            <option value="male">{t("auth.register.gender_male")}</option>
            <option value="female">{t("auth.register.gender_female")}</option>
          </select>

          <div class="password-field">
            <input
              id="registerPassword"
              type="password"
              name="password"
              placeholder={t("auth.register.password_placeholder")}
              required
            />
            <button
              class="password-toggle"
              id="registerPasswordToggle"
              type="button"
              aria-label={t("auth.register.password.show")}
              aria-pressed="false"
              title={t("auth.register.password.show")}
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
              id="registerPasswordConfirm"
              type="password"
              name="password_confirm"
              placeholder={t("auth.register.password_confirm_placeholder")}
              required
            />
            <button
              class="password-toggle"
              id="registerPasswordConfirmToggle"
              type="button"
              aria-label={t("auth.register.password.show")}
              aria-pressed="false"
              title={t("auth.register.password.show")}
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

          <p id="password-warning" class="form-warning is-hidden" aria-live="polite">
            <span class="form-warning-reserve">
              {t("auth.register.password.policy")}
            </span>
            <span class="form-warning-live"></span>
          </p>

          <p id="age-warning" class="age-warning hidden">
            {t("auth.register.age_warning")}
          </p>

          <button type="submit" class="btn btn-primary">
            {t("auth.register.submit")}
          </button>
        </form>

        <a href="/index.html" class="auth-link">
          {t("auth.register.already_have_account")}
        </a>

        <div class="auth-brand">
          <img src="/css/logo-kiadez.webp" alt={t("common.brand")} />
          <span>{t("common.brand")}</span>
        </div>
      </div>
    </section>

    <section class="hero-right">
      <h1 class="hero-title">{t("common.brand")}</h1>

      <p class="hero-subtitle">
        {t("auth.register.hero_subtitle")}
      </p>

      <blockquote class="hero-quote">
        {t("auth.register.hero_quote")}
      </blockquote>
    </section>
  </main>

  <AuthFooter />
</div>
