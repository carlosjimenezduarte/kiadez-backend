<script>
  import { authApi } from "../lib/api.js";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { t } from "../lib/i18n";

  let email = "";
  let status = "";
  let error = "";

  async function handleSubmit(event) {
    event.preventDefault();
    status = t("auth.forgot_password.status_sending");
    error = "";

    try {
      await authApi.requestPasswordReset({ email });
      status = t("auth.forgot_password.status_sent");
      email = "";
    } catch {
      error = t("auth.forgot_password.error_send");
      status = "";
    }
  }
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{t("auth.forgot_password.meta_title")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background">
  <main class="auth-center">
    <div class="auth-card">
      <h2 class="auth-title">{t("auth.forgot_password.title")}</h2>
      <p class="panel-muted">{t("auth.forgot_password.description")}</p>

      <form id="auth-form" on:submit|preventDefault={handleSubmit}>
        <input type="email" bind:value={email} placeholder={t("auth.forgot_password.email_placeholder")} required />
        <button type="submit" class="btn btn-primary">{t("auth.forgot_password.submit")}</button>
      </form>

      {#if status}
        <p class="panel-muted">{status}</p>
      {/if}
      {#if error}
        <p class="panel-muted">{error}</p>
      {/if}

      <a class="auth-link" href="/login.html">{t("auth.forgot_password.back_to_login")}</a>
    </div>
  </main>

  <AuthFooter />
</div>
