<script>
  import { onMount } from 'svelte';
  import { authApi } from '../lib/api.js';

  let token = '';
  let password = '';
  let passwordConfirm = '';
  let status = '';
  let error = '';

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    token = params.get('token') || '';
  });

  async function handleSubmit(event) {
    event.preventDefault();
    error = '';
    status = '';

    if (!token) {
      error = 'Token inválido.';
      return;
    }
    if (password !== passwordConfirm) {
      error = 'Las contraseñas no coinciden.';
      return;
    }

    status = 'Actualizando contraseña...';
    try {
      const res = await authApi.confirmPasswordReset({
        token,
        new_password: password,
      });
      if (res?.reset) {
        status = 'Contraseña actualizada. Ya puedes iniciar sesión.';
        password = '';
        passwordConfirm = '';
      } else {
        status = '';
        error = 'No se pudo actualizar la contraseña.';
      }
    } catch (err) {
      status = '';
      error = err.message || 'No se pudo actualizar la contraseña.';
    }
  }
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Restablecer contraseña</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background">
  <main class="auth-center">
    <div class="auth-card">
      <h2 class="auth-title">Restablecer contraseña</h2>
      <p class="panel-muted">Crea una nueva contraseña para tu cuenta.</p>

      <form id="auth-form" on:submit|preventDefault={handleSubmit}>
        <input type="password" bind:value={password} placeholder="Nueva contraseña" required />
        <input type="password" bind:value={passwordConfirm} placeholder="Confirmar contraseña" required />
        <button type="submit" class="btn btn-primary">Actualizar contraseña</button>
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
