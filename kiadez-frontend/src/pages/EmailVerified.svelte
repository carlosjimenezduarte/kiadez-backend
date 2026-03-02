<script>
  import { onMount } from "svelte";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { t } from "../lib/i18n";

  let success = true;
  let linkHref = "/login.html";
  let linkText = t("auth.email_verified.login_button");
  let redirectLabel = t("auth.email_verified.redirecting_short");

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    const status = params.get("status");
    const email = params.get("email") || "";

    let timerId = null;

    if (status === "ok") {
      const target = email ? `login.html?email=${encodeURIComponent(email)}` : "/login.html";
      linkHref = target;

      let seconds = 2;
      redirectLabel = t("auth.email_verified.redirecting", { seconds });
      timerId = setInterval(() => {
        seconds -= 1;
        if (seconds >= 0) {
          redirectLabel = t("auth.email_verified.redirecting", { seconds });
          return;
        }
        clearInterval(timerId);
        timerId = null;
        window.location.href = target;
      }, 600);
    } else {
      success = false;
      linkHref = "/check-email.html";
      linkText = t("auth.email_verified.back_to_check_email");
      redirectLabel = t("auth.email_verified.invalid_detail");
    }

    return () => {
      if (timerId) clearInterval(timerId);
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{t("auth.email_verified.meta_title")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-backgroundlogin">
  <main class="auth-center">
    <div class="auth-card auth-card--wide">
      <h2 class="auth-title">{t("auth.email_verified.title")}</h2>

      <div class="auth-message">
        {#if success}
          <p>{t("auth.email_verified.success_intro")}</p>
        {:else}
          <p>{t("auth.email_verified.invalid_intro")}</p>
        {/if}
        <p class="muted">{redirectLabel}</p>
      </div>

      <div class="auth-actions">
        <a id="login-link" href={linkHref} class="btn btn-primary">
          {linkText}
        </a>
      </div>

      <div class="auth-brand">
        <img src="/css/logo-kiadez.webp" alt={t("common.brand")} />
        <span>{t("common.brand")}</span>
      </div>
    </div>
  </main>

  <AuthFooter compact={true} />
</div>
