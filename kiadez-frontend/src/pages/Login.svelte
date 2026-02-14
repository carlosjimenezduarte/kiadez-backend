<script>
  import { onMount } from "svelte";

  onMount(() => {
    const API = "http://127.0.0.1:8000";
    const DEV_LOGIN_SECRET = (import.meta.env.VITE_DEV_LOGIN_SECRET || "").trim();
    const isLocalHost =
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1";
    const isDevUI = Boolean(import.meta.env.DEV) || isLocalHost;
    
            const form = document.getElementById("auth-form");
            const demoLoginBox = document.getElementById("dev-login-box");
            const demoCarlosBtn = document.getElementById("demo-login-carlos");
            const demoDavidBtn = document.getElementById("demo-login-david");

            if (!isDevUI) {
                demoLoginBox?.remove();
            }

            function persistTokens(data) {
                if (data?.access_token) {
                    localStorage.setItem("access_token", data.access_token);
                }
                if (data?.refresh_token) {
                    localStorage.setItem("refresh_token", data.refresh_token);
                }
            }

            const twofaOverlay = document.getElementById("twofaLoginOverlay");
            const twofaCodeInput = document.getElementById("twofa-login-code");
            const twofaConfirmBtn = document.getElementById("twofa-login-confirm");
            const twofaCancelBtn = document.getElementById("twofa-login-cancel");
            const twofaCancelFooterBtn = document.getElementById("twofa-login-cancel-footer");
            const twofaErrorEl = document.getElementById("twofa-login-error");

            let pending2FATempToken = "";

            function setTwofaError(message) {
                if (!twofaErrorEl) return;
                const text = String(message || "");
                twofaErrorEl.textContent = text;
                twofaErrorEl.classList.toggle("hidden", !text);
            }

            function setTwofaModalOpen(isOpen) {
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
            }
    
            async function login(email, password) {
                const res = await fetch(`${API}/auth/login`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email, password }),
                });
    
                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || "Error al iniciar sesión");
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
            }

            async function verify2fa(tempToken, code) {
                const res = await fetch(`${API}/auth/2fa/verify`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${tempToken}`,
                    },
                    body: JSON.stringify({ code }),
                });

                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || "Código 2FA incorrecto");
                }

                persistTokens(data);
                return data.access_token;
            }

            async function devLoginAs(email) {
                const headers = {
                    "Content-Type": "application/json",
                };
                if (DEV_LOGIN_SECRET) {
                    headers["X-Dev-Secret"] = DEV_LOGIN_SECRET;
                }

                const res = await fetch(`${API}/dev/login-as`, {
                    method: "POST",
                    headers,
                    body: JSON.stringify({ email }),
                });

                const data = await res.json();
                if (!res.ok) {
                    if (res.status === 404) {
                        throw new Error("Dev login no está habilitado en backend.");
                    }
                    throw new Error(data.detail || "No se pudo iniciar sesión demo");
                }

                persistTokens(data);
                return data.access_token;
            }
    
            async function checkVault(token) {
                const res = await fetch(`${API}/vault/status`, {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                });
    
                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || "No se pudo verificar el vault");
                }
    
                return data.has_vault;
            }

            async function checkLifePurposeConfigured(token) {
                const res = await fetch(`${API}/life-purpose/mine`, {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                });

                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || "No se pudo verificar tu propósito de vida");
                }

                const slots = Array.isArray(data?.slots) ? data.slots : [];
                const slotNumbers = new Set(
                  slots
                    .map((slot) => Number(slot?.slot_number))
                    .filter((n) => Number.isFinite(n) && n >= 1 && n <= 3)
                );
                return slotNumbers.size >= 3;
            }

            async function continueAfterLogin(token) {
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
            }
    
            form.addEventListener("submit", async (e) => {
                e.preventDefault();
    
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
                    alert(err.message);
                    console.error(err);
                }
            });

            demoCarlosBtn?.addEventListener("click", async () => {
                try {
                    const token = await devLoginAs("carlos.demo@example.com");
                    await continueAfterLogin(token);
                } catch (err) {
                    alert(err.message);
                    console.error(err);
                }
            });

            demoDavidBtn?.addEventListener("click", async () => {
                try {
                    const token = await devLoginAs("david.demo@example.com");
                    await continueAfterLogin(token);
                } catch (err) {
                    alert(err.message);
                    console.error(err);
                }
            });

            const handleTwofaConfirm = async () => {
                setTwofaError("");
                const code = (twofaCodeInput?.value || "").trim();
                if (!/^[0-9]{6}$/.test(code)) {
                    setTwofaError("Digita un código válido de 6 dígitos.");
                    return;
                }

                try {
                    if (twofaConfirmBtn) twofaConfirmBtn.disabled = true;
                    const token = await verify2fa(pending2FATempToken, code);
                    setTwofaModalOpen(false);
                    await continueAfterLogin(token);
                } catch (err) {
                    setTwofaError(err.message || "Código 2FA incorrecto");
                    console.error(err);
                } finally {
                    if (twofaConfirmBtn) twofaConfirmBtn.disabled = false;
                }
            };

            twofaConfirmBtn?.addEventListener("click", () => void handleTwofaConfirm());
            twofaCodeInput?.addEventListener("keydown", (event) => {
                if (event.key === "Enter") {
                    event.preventDefault();
                    void handleTwofaConfirm();
                }
            });

            twofaCancelBtn?.addEventListener("click", () => setTwofaModalOpen(false));
            twofaCancelFooterBtn?.addEventListener("click", () => setTwofaModalOpen(false));
            twofaOverlay?.addEventListener("click", (event) => {
                if (event.target === twofaOverlay) setTwofaModalOpen(false);
            });
    
            // Prefill email si viene por URL
            const params = new URLSearchParams(window.location.search);
            const emailParam = params.get("email");
            if (emailParam) {
                document.querySelector('input[name="email"]').value = emailParam;
            }
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Kiadez — Iniciar sesión</title>
    <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-backgroundlogin">

        <main class="auth-center">
            <div class="auth-card auth-card--wide">

                <h2 class="auth-title">Bienvenido de vuelta</h2>

                <form id="auth-form">
                    <input type="email" name="email" placeholder="Correo electrónico" required />
                    <input type="password" name="password" placeholder="Contraseña" required />

                    <button type="submit" class="btn btn-primary">
                        Entrar a Kiadez
                    </button>

                    <a href="/forgot-password.html" class="auth-link">
                        ¿Olvidaste tu contraseña?
                    </a>

                    <div class="auth-divider"></div>

                    <a href="/register.html" class="btn btn-outline">
                        Crear una cuenta nueva
                    </a>

                    <div class="auth-divider"></div>

                    <div class="dev-login-box" id="dev-login-box" aria-label="Acceso demo para desarrollo">
                        <p class="dev-login-title">Acceso demo</p>
                        <div class="dev-login-grid">
                            <button type="button" class="btn btn-outline" id="demo-login-carlos">
                                Entrar como Carlos
                            </button>
                            <button type="button" class="btn btn-outline" id="demo-login-david">
                                Entrar como David
                            </button>
                        </div>
                    </div>
                </form>

                <div class="auth-brand">
                    <img src="/css/logo-kiadez.webp" alt="Kiadez" />
                    <span>Kiadez</span>
                </div>

            </div>
        </main>

        <footer class="kiadez-footer">
            <div class="footer-main">
                <div class="footer-column footer-origin">
                    <p class="footer-poem">
                        Kiadez fue llamado por una estrella a subir el Monte Manjaro.<br>
                        No para dominar, sino para orientar.<br>
                        Su luz no deslumbra: acompaña.
                    </p>
                </div>

                <div class="footer-columns">
                    <div class="footer-column">
                        <h4>Sobre Kiadez</h4>
                        <ul>
                            <li><a href="/what-is-kiadez.html">Qué es Kiadez</a></li>
                            <li><a href="/guardians-rank.html">Rangos de Guardianes</a></li>
                            <li><a href="/contact.html">Contacto</a></li>
                        </ul>
                    </div>

                    <div class="footer-column">
                        <h4>Legal</h4>
                        <ul>
                            <li><a href="/terms.html">Términos</a></li>
                            <li><a href="/privacy.html">Privacidad</a></li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="footer-bottom">
                © 2026 Kiadez — Una red social para cumplir deseos.
            </div>
        </footer>

        <div class="modal-overlay hidden" id="twofaLoginOverlay" aria-hidden="true">
            <div class="modal twofa-login-modal" role="dialog" aria-modal="true" aria-label="Verificación 2FA">
                <div class="modal-head">
                    <h3>Verificación 2FA</h3>
                    <button class="modal-close" type="button" id="twofa-login-cancel">✕</button>
                </div>
                <div class="modal-body">
                    <p class="panel-text">
                        Digita el código de 6 dígitos de tu app autenticadora para completar el inicio de sesión.
                    </p>
                    <input class="modal-input" id="twofa-login-code" type="text" inputmode="numeric" autocomplete="one-time-code"
                        placeholder="123456" maxlength="6" />
                    <p class="settings-form-error hidden" id="twofa-login-error" role="alert"></p>
                </div>
                <div class="modal-actions">
                    <button class="btn btn-primary btn-compact" type="button" id="twofa-login-confirm">Confirmar</button>
                    <button class="btn btn-outline btn-compact" type="button" id="twofa-login-cancel-footer">Cancelar</button>
                </div>
            </div>
        </div>

    </div>
