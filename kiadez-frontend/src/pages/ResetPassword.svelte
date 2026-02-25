<script>
  import { onMount } from 'svelte';
  import { authApi } from '../lib/api.js';

  const PASSWORD_MIN_LENGTH = 8;
  const PASSWORD_RE_UPPER = /[A-Z]/;
  const PASSWORD_RE_DIGIT = /[0-9]/;
  const PASSWORD_RE_SPECIAL = /[^a-zA-Z0-9]/;
  const PASSWORD_POLICY_MESSAGE =
    'La contraseña debe incluir mínimo 8 caracteres, 1 mayúscula, 1 número y 1 carácter especial.';

  let token = '';
  let password = '';
  let passwordConfirm = '';
  let status = '';
  let error = '';

  const passwordChecks = (value) => {
    const pw = String(value || '');
    return {
      length: pw.length >= PASSWORD_MIN_LENGTH,
      upper: PASSWORD_RE_UPPER.test(pw),
      digit: PASSWORD_RE_DIGIT.test(pw),
      special: PASSWORD_RE_SPECIAL.test(pw),
    };
  };

  const isPasswordValid = (value) => Object.values(passwordChecks(value)).every(Boolean);

  $: showPasswordPolicyHint = Boolean(password) && !isPasswordValid(password);

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
    if (!password.trim()) {
      error = 'Debes digitar tu nueva contraseña.';
      return;
    }
    if (!isPasswordValid(password)) {
      error = PASSWORD_POLICY_MESSAGE;
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
        window.location.href = '/login.html';
        return;
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
        <input type="password" bind:value={password} placeholder="Nueva contraseña" minlength="8" required />
        {#if showPasswordPolicyHint}
          <p class="auth-form-error" role="alert">{PASSWORD_POLICY_MESSAGE}</p>
        {/if}
        <input type="password" bind:value={passwordConfirm} placeholder="Confirmar contraseña" required />
        <button type="submit" class="btn btn-primary">Actualizar contraseña</button>
      </form>

      {#if status}
        <p class="panel-muted">{status}</p>
      {/if}
      {#if error}
        <p class="auth-form-error" role="alert">{error}</p>
      {/if}

      <a class="auth-link" href="/login.html">Volver al inicio de sesión</a>
    </div>
  </main>
</div>
