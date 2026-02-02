<script>
  import { onMount } from "svelte";

  onMount(() => {
    const API = "http://127.0.0.1:8000";
    
            const form = document.getElementById("auth-form");
    
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
    
                localStorage.setItem("access_token", data.access_token);
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
    
            form.addEventListener("submit", async (e) => {
                e.preventDefault();
    
                const email = form.email.value;
                const password = form.password.value;
    
                try {
                    const token = await login(email, password);
                    const hasVault = await checkVault(token);
    
                    if (hasVault) {
                        window.location.href = "/life-proposal.html";
                    } else {
                        window.location.href = "/create-private-key.html";
                    }
                } catch (err) {
                    alert(err.message);
                    console.error(err);
                }
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

    </div>
