<script>
  import { onMount } from "svelte";

  onMount(() => {
    const form = document.getElementById("register-form");
    if (!form) return;

    const passwordInput = form.querySelector('input[name="password"]');
    const passwordConfirmInput = form.querySelector('input[name="password_confirm"]');
    const passwordToggle = document.getElementById("registerPasswordToggle");
    const passwordConfirmToggle = document.getElementById("registerPasswordConfirmToggle");
    const passwordWarning = document.getElementById("password-warning");
    const passwordWarningLive = passwordWarning?.querySelector?.(".form-warning-live");

    const PASSWORD_POLICY_MESSAGE =
      "Debe incluir 8+ caracteres, 1 mayúscula, 1 número y 1 símbolo.";

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
          setPasswordWarning("Las contraseñas deben coincidir.");
        } else {
          setPasswordWarning("");
        }
        return;
      }

      setPasswordWarning("");
    };

    passwordInput?.addEventListener("input", updatePasswordWarning);
    passwordConfirmInput?.addEventListener("input", updatePasswordWarning);

    const applyPasswordToggleState = (input, button) => {
      if (!input || !button) return;
      const isVisible = input.type === "text";
      button.classList.toggle("is-visible", isVisible);
      button.setAttribute("aria-pressed", isVisible ? "true" : "false");
      button.setAttribute("aria-label", isVisible ? "Ocultar contraseña" : "Mostrar contraseña");
      button.title = isVisible ? "Ocultar contraseña" : "Mostrar contraseña";
    };

    const togglePasswordVisibility = (input, button) => {
      if (!input || !button) return;
      input.type = input.type === "password" ? "text" : "password";
      applyPasswordToggleState(input, button);
      input.focus();
    };

    const handlePasswordToggleClick = () => togglePasswordVisibility(passwordInput, passwordToggle);
    const handlePasswordConfirmToggleClick = () => togglePasswordVisibility(passwordConfirmInput, passwordConfirmToggle);

    passwordToggle?.addEventListener("click", handlePasswordToggleClick);
    passwordConfirmToggle?.addEventListener("click", handlePasswordConfirmToggleClick);

    applyPasswordToggleState(passwordInput, passwordToggle);
    applyPasswordToggleState(passwordConfirmInput, passwordConfirmToggle);
    
    const handleSubmit = async (e) => {
      e.preventDefault();
    
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
        setPasswordWarning("Las contraseñas deben coincidir.");
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
          alert(result.detail || "Error al registrar usuario.");
          return;
        }
    
        // ✅ Registro exitoso → lo mandamos a check-email
        window.location.href = `check-email.html?email=${encodeURIComponent(payload.email)}`;
    
    
      } catch (error) {
        console.error(error);
        alert("No se pudo conectar con el servidor.");
      }
    };

    form.addEventListener("submit", handleSubmit);

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
    <title>Kiadez — Registro</title>
    <link rel="stylesheet" href="/css/register.css" />
</svelte:head>

<div class="page-background">

        <main class="hero">

            <!-- FORMULARIO -->
            <section class="hero-left">

                <div class="auth-card">
                    <h2 class="auth-title">Crear cuenta en Kiadez</h2>

                    <form id="register-form">

                        <input type="text" name="first_name" placeholder="Nombre" required />
                        <input type="text" name="last_name" placeholder="Apellido" required />
                        <input type="email" name="email" placeholder="Correo electrónico" required />



                        <input type="date" name="birth_date" id="birthdate" required />

                        <select name="gender" required>
                            <option value="">Género</option>
                            <option value="male">Hombre</option>
                            <option value="female">Mujer</option>
                        </select>

                        <div class="password-field">
                          <input id="registerPassword" type="password" name="password" placeholder="Contraseña" required />
                          <button
                            class="password-toggle"
                            id="registerPasswordToggle"
                            type="button"
                            aria-label="Mostrar contraseña"
                            aria-pressed="false"
                            title="Mostrar contraseña"
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
                          <input id="registerPasswordConfirm" type="password" name="password_confirm" placeholder="Confirmar contraseña" required />
                          <button
                            class="password-toggle"
                            id="registerPasswordConfirmToggle"
                            type="button"
                            aria-label="Mostrar contraseña"
                            aria-pressed="false"
                            title="Mostrar contraseña"
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
                            Debe incluir 8+ caracteres, 1 mayúscula, 1 número y 1 símbolo.
                          </span>
                          <span class="form-warning-live"></span>
                        </p>

                        <p id="age-warning" class="age-warning hidden">
                            Si eres menor de edad, tu cuenta tendrá restricciones hasta que un padre o tutor la
                            autorice.
                        </p>

                        <button type="submit" class="btn btn-primary">
                            Crear cuenta
                        </button>

                    </form>

                    <a href="/index.html" class="auth-link">
                        ¿Ya tienes cuenta? Inicia sesión
                    </a>

                    <div class="auth-brand">
                        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
                        <span>Kiadez</span>
                    </div>
                </div>

            </section>

            <!-- VISIÓN -->
            <section class="hero-right">
                <h1 class="hero-title">Kiadez</h1>

                <p class="hero-subtitle">
                    El primer paso para cumplir tus deseos
                </p>

                <blockquote class="hero-quote">
                    Todo gran viaje comienza cuando alguien se atreve a decir “sí”.
                </blockquote>
            </section>

        </main>

        <!-- FOOTER (idéntico al Home) -->
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
                        <h4>Sobre nuestra red social</h4>
                        <ul>
                            <li><a href="/what-is-kiadez.html">Qué es Kiadez</a></li>
                            <li><a href="/guardians-rank.html">Rangos de Guardianes</a></li>
                            <li><a href="/be-a-guardian.html">Ser Guardián</a></li>
                            <li><a href="/contact.html">Contacto</a></li>

                        </ul>
                    </div>

                    <div class="footer-column">
                        <h4>Idiomas</h4>
                        <ul>
                            <li><a href="/?lang=es">Español</a></li>
                            <li><a href="/?lang=en">English</a></li>
                            <li><a href="/?lang=fr">Français</a></li>
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

    </div>
