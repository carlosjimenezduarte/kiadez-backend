<script>
  import { onMount } from "svelte";
  import { authApi } from "../lib/api.js";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { t } from "../lib/i18n";

  const PASSWORD_MIN_LENGTH = 8;
  const PASSWORD_RE_UPPER = /[A-Z]/;
  const PASSWORD_RE_DIGIT = /[0-9]/;
  const PASSWORD_RE_SPECIAL = /[^a-zA-Z0-9]/;

  let token = "";
  let password = "";
  let passwordConfirm = "";
  let status = "";
  let error = "";

  const passwordChecks = (value) => {
    const pw = String(value || "");
    return {
      length: pw.length >= PASSWORD_MIN_LENGTH,
      upper: PASSWORD_RE_UPPER.test(pw),
      digit: PASSWORD_RE_DIGIT.test(pw),
      special: PASSWORD_RE_SPECIAL.test(pw),
    };
  };

  const isPasswordValid = (value) => Object.values(passwordChecks(value)).every(Boolean);
  $: showPasswordPolicyHint = Boolean(password) && !isPasswordValid(password);

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    token = params.get("token") || "";
  });

  async function handleSubmit(event) {
    event.preventDefault();
    error = "";
    status = "";

    if (!token) {
      error = t("auth.reset_password.errors.token_invalid");
      return;
    }
    if (!password.trim()) {
      error = t("auth.reset_password.errors.password_required");
      return;
    }
    if (!isPasswordValid(password)) {
      error = t("auth.reset_password.errors.password_policy");
      return;
    }
    if (password !== passwordConfirm) {
      error = t("auth.reset_password.errors.password_mismatch");
      return;
    }

    status = t("auth.reset_password.status_updating");
    try {
      const res = await authApi.confirmPasswordReset({
        token,
        new_password: password,
      });
      if (res?.reset) {
        window.location.href = "/login.html";
        return;
      }
      status = "";
      error = t("auth.reset_password.errors.update_failed");
    } catch {
      status = "";
      error = t("auth.reset_password.errors.update_failed");
    }
  }
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{t("auth.reset_password.meta_title")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background">
  <main class="auth-center">
    <div class="auth-card">
      <h2 class="auth-title">{t("auth.reset_password.title")}</h2>
      <p class="panel-muted">{t("auth.reset_password.description")}</p>

      <form id="auth-form" on:submit|preventDefault={handleSubmit}>
        <input
          type="password"
          bind:value={password}
          placeholder={t("auth.reset_password.password_placeholder")}
          minlength="8"
          required
        />
        {#if showPasswordPolicyHint}
          <p class="auth-form-error" role="alert">{t("auth.reset_password.errors.password_policy")}</p>
        {/if}
        <input
          type="password"
          bind:value={passwordConfirm}
          placeholder={t("auth.reset_password.password_confirm_placeholder")}
          required
        />
        <button type="submit" class="btn btn-primary">{t("auth.reset_password.submit")}</button>
      </form>

      {#if status}
        <p class="panel-muted">{status}</p>
      {/if}
      {#if error}
        <p class="auth-form-error" role="alert">{error}</p>
      {/if}

      <a class="auth-link" href="/login.html">{t("auth.reset_password.back_to_login")}</a>
    </div>
  </main>

  <AuthFooter compact={true} />
</div>
