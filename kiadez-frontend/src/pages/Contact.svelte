<script>
  import { supportApi } from '../lib/api.js';

  let name = '';
  let email = '';
  let message = '';
  let status = '';
  let error = '';

  async function handleSubmit(event) {
    event.preventDefault();
    status = 'Enviando mensaje...';
    error = '';

    try {
      const res = await supportApi.contact({ name, email, message });
      status = res?.message || 'Gracias, hemos recibido tu mensaje.';
      name = '';
      email = '';
      message = '';
    } catch (err) {
      error = err.message || 'No se pudo enviar el mensaje.';
      status = '';
    }
  }
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Contacto</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background">
  <main class="auth-center">
    <div class="auth-card">
      <h2 class="auth-title">Contacto</h2>
      <p class="panel-muted">Queremos escucharte. Escríbenos y responderemos pronto.</p>

      <form id="auth-form" on:submit|preventDefault={handleSubmit}>
        <input type="text" bind:value={name} placeholder="Nombre" required />
        <input type="email" bind:value={email} placeholder="Correo electrónico" required />
        <textarea class="modal-textarea" bind:value={message} rows="4" placeholder="Tu mensaje" required></textarea>
        <button type="submit" class="btn btn-primary">Enviar mensaje</button>
      </form>

      {#if status}
        <p class="panel-muted">{status}</p>
      {/if}
      {#if error}
        <p class="panel-muted">{error}</p>
      {/if}

      <div class="auth-brand">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
        <span>Kiadez</span>
      </div>
    </div>
  </main>
</div>
