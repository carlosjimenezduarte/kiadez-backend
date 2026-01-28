<script>
  import { authApi } from '../lib/api.js';

  let email = '';
  let status = '';
  let error = '';

  async function handleSubmit(event) {
    event.preventDefault();
    status = 'Enviando enlace...';
    error = '';

    try {
      const res = await authApi.requestPasswordReset({ email });
      status = res?.message || 'Si el correo existe, enviaremos un enlace de recuperación.';
      email = '';
    } catch (err) {
      error = err.message || 'No se pudo enviar el enlace.';
      status = '';
    }
  }
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Recuperar contraseña</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background">
  <main class="auth-center">
    <div class="auth-card">
      <h2 class="auth-title">Recuperar contraseña</h2>
      <p class="panel-muted">Escribe tu correo y te enviaremos un enlace seguro.</p>

      <form id="auth-form" on:submit|preventDefault={handleSubmit}>
        <input type="email" bind:value={email} placeholder="Correo electrónico" required />
        <button type="submit" class="btn btn-primary">Enviar enlace</button>
      </form>

      {#if status}
        <p class="panel-muted">{status}</p>
      {/if}
      {#if error}
        <p class="panel-muted">{error}</p>
      {/if}

      <a class="auth-link" href="/login.html">Volver al inicio de sesión</a>
    </div>
  </main>
</div>
