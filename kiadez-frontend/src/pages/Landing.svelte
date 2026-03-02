<script>
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";

  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

  function handleSubmit(event) {
    event.preventDefault();
    alert(tr("Aquí conectamos con Kiadez API.", "This is where we connect to the Kiadez API.", "C'est ici que nous nous connectons à l'API Kiadez."));
  }
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
        <h2 class="auth-title">{tr("Iniciar sesión en Kiadez", "Sign in to Kiadez", "Se connecter à Kiadez")}</h2>

        <form id="auth-form" on:submit={handleSubmit}>
          <input type="email" placeholder={tr("Correo electrónico", "Email address", "Adresse e-mail")} required />
          <input type="password" placeholder={tr("Contraseña", "Password", "Mot de passe")} required />

          <button type="submit" class="btn btn-primary">
            {tr("Iniciar sesión", "Sign in", "Se connecter")}
          </button>

          <a href="/forgot-password.html" class="auth-link">
            {tr("¿Olvidaste tu contraseña?", "Forgot your password?", "Mot de passe oublié ?")}
          </a>

          <div class="auth-divider"></div>
          <a href="register.html" class="btn btn-outline">
            {tr("Registrarse en Kiadez", "Create an account", "Créer un compte")}
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
        {tr("Una red social pensada para cumplir los deseos", "A social network designed to fulfill wishes", "Un réseau social conçu pour accomplir les souhaits")}
      </p>

      <blockquote class="hero-quote">
        {tr(
          "La sabiduría suprema consiste en tener sueños lo suficientemente grandes para no perderlos de vista mientras se persiguen.",
          "Supreme wisdom is having dreams so big that you never lose sight of them while pursuing them."
        )}
        <br />
        <br />
        <span>— William Faulkner</span>
      </blockquote>
    </section>
  </main>

  <AuthFooter />
</div>
