<script>
  import { onMount } from "svelte";

  onMount(() => {
    const API_BASE = "http://127.0.0.1:8000";
    
            const params = new URLSearchParams(window.location.search);
            const email = params.get("email") || "";
    
            const resendBtn = document.getElementById("resend-btn");
    
            // Reenviar real (con cooldown)
            resendBtn.addEventListener("click", async () => {
                if (!email) {
                    alert("No se encontró el correo en la URL.");
                    return;
                }
    
                resendBtn.disabled = true;
                const originalText = resendBtn.textContent;
                resendBtn.textContent = "Enviando...";
    
                try {
                    const res = await fetch(`${API_BASE}/auth/resend-verification`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ email }),
                    });
    
                    const data = await res.json();
                    alert(data.message || "Listo.");
                } catch (e) {
                    alert("No se pudo reenviar. Intenta de nuevo.");
                } finally {
                    let t = 20;
                    const timer = setInterval(() => {
                        resendBtn.textContent = `Reenviar correo (${t})`;
                        t--;
                        if (t < 0) {
                            clearInterval(timer);
                            resendBtn.disabled = false;
                            resendBtn.textContent = originalText;
                        }
                    }, 1000);
                }
            });
    
            // Polling: cada 3s preguntamos si ya está verificado
            let pollTimer = null;
    
            async function checkVerification() {
                if (!email) return;
    
                try {
                    const res = await fetch(`${API_BASE}/auth/verification-status?email=${encodeURIComponent(email)}`);
                    const data = await res.json();
    
                    if (data.verified === true) {
                        clearInterval(pollTimer);
                        window.location.href = `login.html?email=${encodeURIComponent(email)}`;
                    }
                } catch (err) {
                    console.warn("No se pudo consultar verificación:", err);
                }
            }
    
            pollTimer = setInterval(checkVerification, 3000);
            checkVerification();
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Kiadez — Revisa tu correo</title>
    <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background">

        <main class="auth-center">
            <div class="auth-card auth-card--wide">

                <h2 class="auth-title">Revisa tu correo</h2>

                <div class="auth-message">
                    <p>
                        Te enviamos un enlace de verificación para activar tu cuenta.
                    </p>
                    <br>

                    <p class="muted">
                        Abre tu bandeja de entrada (y revisa spam si no lo ves).
                    </p>
                    <br>

                </div>

                <div class="auth-actions">
                    <!-- Esto lo conectamos después: reenviar -->
                    <button class="btn btn-primary" id="resend-btn" type="button">
                        Reenviar correo
                    </button>
                    <br>

                    <a href="/index.html" class="btn btn-outline">
                        Volver al inicio de sesión
                    </a>
                    <br>
                    <br>
                </div>



                <div class="auth-divider"></div>

                <p class="auth-help muted">
                    Si cerraste la ventana o perdiste el enlace, puedes reenviar el correo desde aquí.
                </p>

                <div class="auth-brand">
                    <img src="logo.png" alt="Kiadez" />
                    <span>Kiadez</span>
                </div>

            </div>
        </main>

        <footer class="kiadez-footer">
            <div class="footer-bottom">
                © 2026 Kiadez — Una red social para cumplir deseos.
            </div>
        </footer>

    </div>
