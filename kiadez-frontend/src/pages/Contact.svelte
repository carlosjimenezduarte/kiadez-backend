<script>
  import { supportApi } from '../lib/api.js';

  let name = '';
  let email = '';
  let message = '';
  let status = '';
  let error = '';

  async function handleSubmit(event) {
    event.preventDefault();
    status = 'Sending message...';
    error = '';

    try {
      const res = await supportApi.contact({ name, email, message });
      status = res?.message || 'Thank you, we have received your message.';
      name = '';
      email = '';
      message = '';
    } catch (err) {
      error = err.message || 'Could not send the message.';
      status = '';
    }
  }
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Contact</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background">
  <main class="auth-center">
    <div class="auth-card">
      <h2 class="auth-title">Contact</h2>
      <p class="panel-muted">We want to hear from you. Write to us and we will reply soon.</p>

      <form id="auth-form" on:submit|preventDefault={handleSubmit}>
        <input type="text" bind:value={name} placeholder="Name" required />
        <input type="email" bind:value={email} placeholder="Email address" required />
        <textarea class="modal-textarea" bind:value={message} rows="4" placeholder="Your message" required></textarea>
        <button type="submit" class="btn btn-primary">Send message</button>
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
