<script>
  import { onMount } from "svelte";

  onMount(() => {
    const API = "http://127.0.0.1:8000";
            const AAD_VAULT = new TextEncoder().encode("kiadez-vault-v1");
    
            // ===== Utilidades =====
            function bufToHex(buf) {
                return [...new Uint8Array(buf)]
                    .map(b => b.toString(16).padStart(2, "0"))
                    .join("");
            }
    
            function showStatus(msg) {
                const el = document.getElementById("status-label");
                el.style.display = "block";
                el.textContent = msg;
            }
    
            function getAccessToken() {
                return localStorage.getItem("access_token") || "";
            }
    
            // ===== Crypto: PBKDF2 -> AES-GCM key (KEK) =====
            async function pbkdf2Key(password, saltBuf, iters) {
                const enc = new TextEncoder();
                const baseKey = await crypto.subtle.importKey(
                    "raw",
                    enc.encode(password),
                    "PBKDF2",
                    false,
                    ["deriveKey"]
                );
    
                return crypto.subtle.deriveKey(
                    {
                        name: "PBKDF2",
                        salt: saltBuf,
                        iterations: iters,
                        hash: "SHA-256",
                    },
                    baseKey,
                    { name: "AES-GCM", length: 256 },
                    false,
                    ["encrypt", "decrypt"]
                );
            }
    
            // ===== Crypto: AES-GCM encrypt =====
            async function aesGcmEncrypt(key, rawBytesBuf, aadBytes) {
                const nonce = crypto.getRandomValues(new Uint8Array(12));
                const ciphertext = await crypto.subtle.encrypt(
                    { name: "AES-GCM", iv: nonce, additionalData: aadBytes },
                    key,
                    rawBytesBuf
                );
                return { nonce: nonce.buffer, ciphertext };
            }
    
            // ===== Precheck: ¿ya existe vault? =====
            async function checkVaultStatus() {
                const token = getAccessToken();
                if (!token) {
                    showStatus("No hay sesión activa. Inicia sesión de nuevo.");
                    return { has_vault: false, ok: false };
                }
    
                try {
                    const res = await fetch(`${API}/vault/status`, {
                        headers: { "Authorization": `Bearer ${token}` }
                    });
                    const data = await res.json();
                    if (!res.ok) {
                        showStatus(data.detail || "No se pudo consultar el estado del vault.");
                        return { has_vault: false, ok: false };
                    }
                    return { has_vault: !!data.has_vault, ok: true };
                } catch (e) {
                    showStatus("No se pudo conectar con el servidor.");
                    return { has_vault: false, ok: false };
                }
            }
    
            // ===== Crear Vault (ZK): genera DEK, wrap con KEK y guarda SOLO lo envuelto =====
            async function createVault(privatePassword) {
                const iters = 310000;
                const salt = crypto.getRandomValues(new Uint8Array(16));
    
                // KEK derivada de CPP
                const kek = await pbkdf2Key(privatePassword, salt.buffer, iters);
    
                // DEK random (32 bytes)
                const dekRaw = crypto.getRandomValues(new Uint8Array(32)).buffer;
    
                // Wrap DEK con KEK (AES-GCM)
                const { nonce, ciphertext } = await aesGcmEncrypt(kek, dekRaw, AAD_VAULT);
    
                // POST al backend (solo ciphertext + params)
                const token = getAccessToken();
                const res = await fetch(`${API}/vault/setup`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        kdf_name: "pbkdf2_sha256",
                        kdf_iters: iters,
                        kdf_salt_hex: bufToHex(salt.buffer),
                        wrapped_dek_nonce_hex: bufToHex(nonce),
                        wrapped_dek_hex: bufToHex(ciphertext),
                    }),
                });
    
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || "No se pudo crear vault.");
    
                // Guardamos la DEK en memoria de sesión (NO en localStorage)
                sessionStorage.setItem("dek_hex", bufToHex(dekRaw));
    
                return true;
            }
    
            // ===== UX / Flujo =====
            const form = document.getElementById("vault-form");
            const btn = document.getElementById("submit-btn");
    
            (async () => {
                const st = await checkVaultStatus();
                if (st.ok && st.has_vault) {
                    showStatus("Ya tienes una clave privada configurada. Próximo paso: tu propósito de vida.");
                    btn.textContent = "Continuar";
                }
            })();
    
            form.addEventListener("submit", async (e) => {
                e.preventDefault();
    
                const token = getAccessToken();
                if (!token) {
                    alert("No hay sesión activa. Inicia sesión de nuevo.");
                    window.location.href = "/login.html";
                    return;
                }
    
                // Si ya existe vault, solo avanzamos (no recreamos)
                const st = await checkVaultStatus();
                if (st.ok && st.has_vault) {
                    window.location.href = "/life-proposal.html";
                    return;
                }
    
                const ppw = form.ppw.value;
                const ppw2 = form.ppw2.value;
    
                if (ppw !== ppw2) {
                    alert("Las claves no coinciden.");
                    return;
                }
    
                // opcional: regla mínima de UX (sin duplicar la política del backend)
                if (ppw.length < 8) {
                    alert("Tu clave privada debe tener al menos 8 caracteres.");
                    return;
                }
    
                btn.disabled = true;
                const oldText = btn.textContent;
                btn.textContent = "Creando...";
    
                try {
                    await createVault(ppw);
                    alert("Clave privada creada. Vamos a tu propósito de vida.");
                    window.location.href = "/life-proposal.html";
                } catch (err) {
                    console.error(err);
                    alert(err.message || "No se pudo crear la clave privada.");
                } finally {
                    btn.disabled = false;
                    btn.textContent = oldText;
                }
            });
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Kiadez — Crea tu clave privada</title>
    <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-backgroundcpp">
        <main class="auth-center">
            <div class="auth-card auth-card--wide">
                <h2 class="auth-title">Crea tu clave privada personal</h2>

                <div class="auth-message">
                    <p>
                        Esta clave protege tus <strong>deseos privados</strong> y tu <strong>propósito secreto</strong>.
                    </p>
                    <br>
                    <br>
                    <p class="muted">
                        Esta clave no pertenece a Kiadez: te pertenece a ti.<br>
                        Más adelante podrás definir custodios o mecanismos de recuperación consciente.
                        <br>
                        <br>
                        Por favor, guarda muy bien esta clave o memórizala como un tesoro personal.
                    </p>
                    <br>
                    <p class="muted" id="status-label" style="display:none;"></p>
                </div>

                <form id="vault-form">
                    <input type="password" name="ppw" placeholder="Clave privada personal" required />
                    <input type="password" name="ppw2" placeholder="Confirmar clave privada" required />


                    <button type="submit" class="btn btn-primary" id="submit-btn">
                        Crear clave privada
                    </button>

                    <br><br>
                    <a href="/login.html" class="btn btn-outline">Volver</a>
                </form>

                <div class="auth-brand">
                    <img src="/css/logo-kiadez.webp" alt="Kiadez" />
                    <span>Kiadez</span>
                </div>
            </div>
        </main>

        <footer class="kiadez-footer">
            <div class="footer-bottom">© 2026 Kiadez — Una red social para cumplir deseos.</div>
        </footer>
    </div>
