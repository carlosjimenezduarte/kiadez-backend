<script>
  import { onMount } from "svelte";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { t } from "../lib/i18n";

  const API_BASE = "http://127.0.0.1:8000";
  const RESEND_COOLDOWN_SECONDS = 20;
  const VERIFICATION_POLL_MS = 3000;

  let email = "";
  let resendLoading = false;
  let resendCountdown = 0;

  let pollTimerId = null;
  let resendTimerId = null;

  const resendLabel = () => {
    if (resendLoading) return t("auth.check_email.alerts.resend_loading");
    if (resendCountdown > 0) {
      return t("auth.check_email.resend_with_seconds", { seconds: resendCountdown });
    }
    return t("auth.check_email.resend");
  };

  const clearTimers = () => {
    if (pollTimerId) {
      clearInterval(pollTimerId);
      pollTimerId = null;
    }
    if (resendTimerId) {
      clearInterval(resendTimerId);
      resendTimerId = null;
    }
  };

  const startResendCooldown = () => {
    resendCountdown = RESEND_COOLDOWN_SECONDS;
    if (resendTimerId) clearInterval(resendTimerId);
    resendTimerId = setInterval(() => {
      resendCountdown = Math.max(0, resendCountdown - 1);
      if (resendCountdown === 0 && resendTimerId) {
        clearInterval(resendTimerId);
        resendTimerId = null;
      }
    }, 1000);
  };

  const checkVerification = async () => {
    if (!email) return;

    try {
      const res = await fetch(`${API_BASE}/auth/verification-status?email=${encodeURIComponent(email)}`);
      const data = await res.json();

      if (data.verified === true) {
        clearTimers();
        window.location.href = `login.html?email=${encodeURIComponent(email)}`;
      }
    } catch (err) {
      console.warn("Verification status request failed:", err);
    }
  };

  const resendVerificationEmail = async () => {
    if (!email) {
      alert(t("auth.check_email.alerts.missing_email"));
      return;
    }
    if (resendLoading || resendCountdown > 0) return;

    resendLoading = true;
    try {
      const response = await fetch(`${API_BASE}/auth/resend-verification`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      if (!response.ok) throw new Error("resend_failed");
      alert(t("auth.check_email.alerts.resend_done"));
    } catch {
      alert(t("auth.check_email.alerts.resend_failed"));
    } finally {
      resendLoading = false;
      startResendCooldown();
    }
  };

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    email = params.get("email") || "";

    pollTimerId = setInterval(() => {
      void checkVerification();
    }, VERIFICATION_POLL_MS);
    void checkVerification();

    return () => {
      clearTimers();
    };
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{t("auth.check_email.meta_title")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background">
  <main class="auth-center">
    <div class="auth-card auth-card--wide">
      <h2 class="auth-title">{t("auth.check_email.title")}</h2>

      <div class="auth-message">
        <p>{t("auth.check_email.intro")}</p>
        <br />
        <p class="muted">{t("auth.check_email.hint")}</p>
        <br />
      </div>

      <div class="auth-actions">
        <button class="btn btn-primary" id="resend-btn" type="button" disabled={resendLoading || resendCountdown > 0} on:click={resendVerificationEmail}>
          {resendLabel()}
        </button>
        <br />

        <a href="/index.html" class="btn btn-outline">
          {t("auth.check_email.back_to_login")}
        </a>
        <br />
        <br />
      </div>

      <div class="auth-divider"></div>

      <p class="auth-help muted">
        {t("auth.check_email.help")}
      </p>

      <div class="auth-brand">
        <img src="/css/logo-kiadez.webp" alt={t("common.brand")} />
        <span>{t("common.brand")}</span>
      </div>
    </div>
  </main>

  <AuthFooter compact={true} />
</div>
