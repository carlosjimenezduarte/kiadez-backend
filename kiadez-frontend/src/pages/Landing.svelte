<script>
  import { onMount } from "svelte";

  const API = import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") || "http://localhost:8000";

  let email = "";
  let password = "";
  let authError = "";
  let loginLoading = false;
  let restoringSession = false;

  let showTwofaModal = false;
  let twofaCode = "";
  let twofaError = "";
  let twofaLoading = false;
  let pending2FATempToken = "";

  const getStoredAccessToken = () =>
    localStorage.getItem("access_token") ||
    localStorage.getItem("kiadez_access_token") ||
    "";

  const clearStoredSession = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("kiadez_access_token");
  };

  const persistTokens = (data) => {
    if (data?.access_token) {
      localStorage.setItem("access_token", data.access_token);
    }
    if (data?.refresh_token) {
      localStorage.setItem("refresh_token", data.refresh_token);
    }
  };

  const readApiError = (payload, fallback = "Error inesperado.") => {
    const detail = payload?.detail;
    if (typeof detail === "string" && detail.trim()) return detail.trim();
    if (Array.isArray(detail) && detail.length > 0) {
      const first = detail[0];
      if (typeof first === "string" && first.trim()) return first.trim();
      if (first && typeof first === "object") {
        if (typeof first.msg === "string" && first.msg.trim()) return first.msg.trim();
        if (typeof first.message === "string" && first.message.trim()) return first.message.trim();
      }
    }
    if (detail && typeof detail === "object") {
      if (typeof detail.msg === "string" && detail.msg.trim()) return detail.msg.trim();
      if (typeof detail.message === "string" && detail.message.trim()) return detail.message.trim();
    }
    if (typeof payload?.message === "string" && payload.message.trim()) return payload.message.trim();
    return fallback;
  };

  const parseResponseJson = async (response) => {
    try {
      return await response.json();
    } catch {
      return {};
    }
  };

  const NETWORK_FAILURE_MESSAGE =
    "No se pudo conectar con el servidor (red, CORS o SSL).";

  const isFetchNetworkError = (error) =>
    error instanceof TypeError || /failed to fetch/i.test(String(error?.message || ""));

  const logNetworkError = (context, error) => {
    console.error(`[Landing] ${context}`, {
      apiBase: API,
      origin: typeof window !== "undefined" ? window.location.origin : "n/a",
      error,
    });
  };

  const checkVault = async (token) => {
    const res = await fetch(`${API}/vault/status`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(readApiError(data, "No se pudo verificar el vault."));
    }
    return Boolean(data?.has_vault);
  };

  const checkLifePurposeConfigured = async (token) => {
    const res = await fetch(`${API}/life-purpose/mine`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(readApiError(data, "No se pudo verificar tu propósito de vida."));
    }
    const slots = Array.isArray(data?.slots) ? data.slots : [];
    const configured = new Set(
      slots
        .map((slot) => Number(slot?.slot_number))
        .filter((n) => Number.isFinite(n) && n >= 1 && n <= 3)
    );
    return configured.size >= 3;
  };

  const continueAfterLogin = async (token) => {
    if (!token) throw new Error("No se recibió token de acceso.");

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

  const login = async (emailValue, passwordValue) => {
    let res;
    try {
      res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: String(emailValue || "").trim(),
          password: String(passwordValue || ""),
        }),
      });
    } catch (error) {
      logNetworkError("POST /auth/login failed", error);
      throw new Error(NETWORK_FAILURE_MESSAGE);
    }

    const data = await parseResponseJson(res);
    if (!res.ok) {
      const err = new Error(readApiError(data, "Error al iniciar sesión."));
      err.status = res.status;
      throw err;
    }

    if (data?.["2fa_required"]) {
      return {
        twofa_required: true,
        temp_token: String(data?.temp_token || "").trim(),
      };
    }

    persistTokens(data);
    return {
      twofa_required: false,
      access_token: String(data?.access_token || "").trim(),
    };
  };

  const verify2fa = async (tempToken, code) => {
    let res;
    try {
      res = await fetch(`${API}/auth/2fa/verify`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${tempToken}`,
        },
        body: JSON.stringify({ code }),
      });
    } catch (error) {
      logNetworkError("POST /auth/2fa/verify failed", error);
      throw new Error(NETWORK_FAILURE_MESSAGE);
    }

    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(readApiError(data, "Código 2FA incorrecto."));
    }
    persistTokens(data);
    return String(data?.access_token || "").trim();
  };

  const closeTwofaModal = () => {
    showTwofaModal = false;
    twofaCode = "";
    twofaError = "";
    twofaLoading = false;
    pending2FATempToken = "";
  };

  const handleTwofaConfirm = async () => {
    twofaError = "";
    const code = String(twofaCode || "").trim();
    if (!/^[0-9]{6}$/.test(code)) {
      twofaError = "Digita un código válido de 6 dígitos.";
      return;
    }

    try {
      twofaLoading = true;
      const token = await verify2fa(pending2FATempToken, code);
      closeTwofaModal();
      await continueAfterLogin(token);
    } catch (err) {
      if (isFetchNetworkError(err)) {
        twofaError = NETWORK_FAILURE_MESSAGE;
        logNetworkError("2FA confirmation failed", err);
      } else {
        twofaError = String(err?.message || "Código 2FA incorrecto.");
        console.error(err);
      }
    } finally {
      twofaLoading = false;
    }
  };

  const handleSubmit = async () => {
    authError = "";
    const normalizedEmail = String(email || "").trim();
    const normalizedPassword = String(password || "");

    if (!normalizedEmail || !normalizedPassword) {
      authError = "Completa correo electrónico y contraseña.";
      return;
    }

    try {
      loginLoading = true;
      const result = await login(normalizedEmail, normalizedPassword);
      if (result?.twofa_required) {
        pending2FATempToken = String(result?.temp_token || "").trim();
        showTwofaModal = true;
        return;
      }

      await continueAfterLogin(result?.access_token);
    } catch (err) {
      const message = String(err?.message || "");
      if (isFetchNetworkError(err)) {
        authError = NETWORK_FAILURE_MESSAGE;
        logNetworkError("Login submit failed", err);
      } else if (Number(err?.status) === 401 || /credenciales/i.test(message)) {
        authError = "Correo electrónico o contraseña inválida";
      } else {
        authError = message || "No se pudo iniciar sesión.";
      }
      if (!isFetchNetworkError(err)) {
        console.error(err);
      }
    } finally {
      loginLoading = false;
    }
  };

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    const emailParam = params.get("email");
    if (emailParam) {
      email = emailParam;
    }

    const token = getStoredAccessToken();
    if (!token) return;

    restoringSession = true;
    void continueAfterLogin(token)
      .catch(() => {
        clearStoredSession();
        restoringSession = false;
      });
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background">
  <main class="hero">
    <section class="hero-left">
      <div class="auth-card">
        <h2 class="auth-title">Iniciar sesión en Kiadez</h2>

        <form id="auth-form" on:submit|preventDefault={handleSubmit}>
          <input
            type="email"
            name="email"
            placeholder="Correo electrónico"
            autocomplete="email"
            bind:value={email}
            on:input={() => (authError = "")}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Contraseña"
            autocomplete="current-password"
            bind:value={password}
            on:input={() => (authError = "")}
            required
          />
          <p class={`auth-form-error ${authError ? "" : "hidden"}`} role="alert">{authError}</p>

          <button type="submit" class="btn btn-primary" disabled={loginLoading || restoringSession}>
            {#if restoringSession}
              Validando sesión...
            {:else if loginLoading}
              Iniciando sesión...
            {:else}
              Iniciar sesión
            {/if}
          </button>

          <a href="/forgot-password.html" class="auth-link">
            ¿Olvidaste tu contraseña?
          </a>

          <div class="auth-divider"></div>
          <a href="/register.html" class="btn btn-outline">
            Registrarse en Kiadez
          </a>
        </form>

        <div class="auth-brand">
          <img src="/css/logo-kiadez.webp" alt="Kiadez" />
          <span>Kiadez</span>
        </div>
      </div>
    </section>

    <section class="hero-right">
      <h1 class="hero-title">Kiadez</h1>

      <p class="hero-subtitle">
        Una red social pensada para cumplir los deseos
      </p>

      <blockquote class="hero-quote">
        La sabiduría suprema consiste en tener sueños lo suficientemente grandes
        para no perderlos de vista mientras se persiguen.
        <br />
        <br />
        <span>— William Faulkner</span>
      </blockquote>
    </section>
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
            <li><a href="/downloadapp.html">Descarga la app</a></li>
            <li><a href="/guardians-rank.html">Rangos de Guardianes</a></li>
            <li><a href="/be-a-guardian.html">Ser Guardián</a></li>
            <li><a href="/contact.html">Contacto</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>Idiomas</h4>
          <ul>
            <li><a href="/?lang=es">Español</a></li>
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

  <div class={`modal-overlay ${showTwofaModal ? "" : "hidden"}`} aria-hidden={!showTwofaModal}>
    <div class="modal twofa-login-modal" role="dialog" aria-modal="true" aria-label="Verificación 2FA">
      <div class="modal-head">
        <h3>Verificación 2FA</h3>
        <button class="modal-close" type="button" on:click={closeTwofaModal}>✕</button>
      </div>
      <div class="modal-body">
        <p class="panel-text">
          Digita el código de 6 dígitos de tu app autenticadora para completar el inicio de sesión.
        </p>
        <input
          class="modal-input"
          type="text"
          inputmode="numeric"
          autocomplete="one-time-code"
          placeholder="123456"
          maxlength="6"
          bind:value={twofaCode}
          on:keydown={(event) => {
            if (event.key === "Enter") {
              event.preventDefault();
              void handleTwofaConfirm();
            }
          }}
        />
        <p class={`settings-form-error ${twofaError ? "" : "hidden"}`} role="alert">{twofaError}</p>
      </div>
      <div class="modal-actions">
        <button class="btn btn-primary btn-compact" type="button" on:click={handleTwofaConfirm} disabled={twofaLoading}>
          {twofaLoading ? "Confirmando..." : "Confirmar"}
        </button>
        <button class="btn btn-outline btn-compact" type="button" on:click={closeTwofaModal} disabled={twofaLoading}>
          Cancelar
        </button>
      </div>
    </div>
  </div>
</div>
