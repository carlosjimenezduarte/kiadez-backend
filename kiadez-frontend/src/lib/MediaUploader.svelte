<script>
  import {
    authApi,
    mediaApi,
    uploadToPresignedUrl,
    setAccessToken,
    getAccessToken,
    clearAccessToken,
  } from './api.js';

  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, '') ||
    'http://127.0.0.1:8000';

  const MAX_IMAGE_MB = 10;
  const MAX_VIDEO_MB = 100;

  let email = '';
  let password = '';
  let twofaCode = '';
  let tempToken = '';
  let needs2fa = false;
  let manualToken = '';
  let accessToken = getAccessToken();

  let authStatus = '';
  let authError = '';

  let file = null;
  let visibility = 'private';
  let title = '';
  let text = '';
  let publishedAt = '';
  let uploadStatus = '';
  let uploadError = '';
  let isUploading = false;
  let uploadedUrl = '';
  let uploadedMediaId = null;
  let uploadedKey = '';
  let expiresIn = null;

  function handleLogout() {
    clearAccessToken();
    accessToken = null;
    tempToken = '';
    needs2fa = false;
    authStatus = 'Logged out';
  }

  function applyManualToken() {
    if (!manualToken.trim()) return;
    setAccessToken(manualToken.trim());
    accessToken = manualToken.trim();
    manualToken = '';
    authStatus = 'Access token set';
    authError = '';
  }

  async function handleLogin() {
    authError = '';
    authStatus = 'Signing in...';
    needs2fa = false;

    try {
      const res = await authApi.login({ email, password });
      if (res?.['2fa_required']) {
        tempToken = res.temp_token;
        needs2fa = true;
        authStatus = '2FA required';
        return;
      }
      setAccessToken(res.access_token);
      accessToken = res.access_token;
      authStatus = 'Signed in';
    } catch (err) {
      authError = err.message || 'Login failed';
      authStatus = '';
    }
  }

  async function handleVerify2fa() {
    authError = '';
    authStatus = 'Verifying 2FA...';

    try {
      const res = await authApi.verify2fa({
        temp_token: tempToken,
        code: twofaCode,
      });
      setAccessToken(res.access_token);
      accessToken = res.access_token;
      needs2fa = false;
      tempToken = '';
      twofaCode = '';
      authStatus = 'Signed in with 2FA';
    } catch (err) {
      authError = err.message || '2FA failed';
      authStatus = '';
    }
  }

  function handleFileChange(event) {
    uploadError = '';
    uploadStatus = '';
    const selected = event.currentTarget?.files?.[0] || null;
    file = selected;
  }

  function validateFile(selectedFile) {
    if (!selectedFile) {
      return 'Select a file first.';
    }
    if (!selectedFile.type) {
      return 'File type missing. Try another file.';
    }
    if (!selectedFile.type.startsWith('image/') && !selectedFile.type.startsWith('video/')) {
      return 'Only images or videos are allowed.';
    }
    const sizeMb = selectedFile.size / (1024 * 1024);
    if (selectedFile.type.startsWith('image/') && sizeMb > MAX_IMAGE_MB) {
      return `Image too large. Max ${MAX_IMAGE_MB}MB.`;
    }
    if (selectedFile.type.startsWith('video/') && sizeMb > MAX_VIDEO_MB) {
      return `Video too large. Max ${MAX_VIDEO_MB}MB.`;
    }
    return null;
  }

  async function handleUpload() {
    uploadError = '';
    uploadStatus = '';
    uploadedUrl = '';
    uploadedMediaId = null;
    uploadedKey = '';
    expiresIn = null;

    if (!accessToken) {
      uploadError = 'Sign in or set an access token.';
      return;
    }

    const validationError = validateFile(file);
    if (validationError) {
      uploadError = validationError;
      return;
    }

    isUploading = true;
    uploadStatus = 'Requesting presigned URL...';

    try {
      const presign = await mediaApi.presignUpload({
        filename: file.name,
        content_type: file.type,
        size_bytes: file.size,
        visibility,
      });

      uploadStatus = 'Uploading to storage...';
      await uploadToPresignedUrl({
        upload_url: presign.upload_url,
        file,
        content_type: file.type,
      });

      uploadStatus = 'Confirming upload...';
      const confirm = await mediaApi.confirmUpload({
        media_id: presign.media_id,
        title: title || null,
        text: text || null,
        published_at: publishedAt ? new Date(publishedAt).toISOString() : null,
      });

      uploadedUrl = confirm.url;
      uploadedMediaId = confirm.media_id;
      uploadedKey = presign.object_key;
      expiresIn = confirm.expires_in;
      uploadStatus = 'Upload complete';
    } catch (err) {
      uploadError = err.message || 'Upload failed';
      uploadStatus = '';
    } finally {
      isUploading = false;
    }
  }

  async function refreshUrl() {
    uploadError = '';
    uploadStatus = 'Refreshing URL...';
    if (!uploadedMediaId) {
      uploadError = 'No media id to refresh.';
      uploadStatus = '';
      return;
    }
    try {
      const res = await mediaApi.getMediaUrl(uploadedMediaId);
      uploadedUrl = res.url;
      expiresIn = res.expires_in;
      uploadStatus = 'URL refreshed';
    } catch (err) {
      uploadError = err.message || 'Failed to refresh';
      uploadStatus = '';
    }
  }
</script>

<div class="card">
  <div class="card-head">
    <div>
      <p class="eyebrow">Auth</p>
      <h2>Sign in for uploads</h2>
      <p class="muted">API base: {API_BASE_URL}</p>
    </div>
    {#if accessToken}
      <button class="ghost" type="button" on:click={handleLogout}>Log out</button>
    {/if}
  </div>

  {#if !accessToken}
    <form class="grid" on:submit|preventDefault={handleLogin}>
      <label>
        <span>Email</span>
        <input type="email" bind:value={email} placeholder="you@kiadez.com" required />
      </label>
      <label>
        <span>Password</span>
        <input type="password" bind:value={password} placeholder="Your password" required />
      </label>
      <button type="submit">Sign in</button>
    </form>

    {#if needs2fa}
      <form class="grid" on:submit|preventDefault={handleVerify2fa}>
        <label>
          <span>2FA code</span>
          <input type="text" bind:value={twofaCode} minlength="6" maxlength="6" placeholder="123456" required />
        </label>
        <button type="submit">Verify 2FA</button>
      </form>
    {/if}

    <div class="divider">or</div>
    <div class="grid">
      <label>
        <span>Access token</span>
        <input type="password" bind:value={manualToken} placeholder="Paste access token" />
      </label>
      <button class="ghost" type="button" on:click={applyManualToken}>Use token</button>
    </div>
  {:else}
    <div class="status-row">
      <span class="pill">Token loaded</span>
      <span class="muted">Ready to upload</span>
    </div>
  {/if}

  {#if authStatus}
    <p class="status">{authStatus}</p>
  {/if}
  {#if authError}
    <p class="error">{authError}</p>
  {/if}
</div>

<div class="card">
  <div class="card-head">
    <div>
      <p class="eyebrow">Media</p>
      <h2>Direct upload</h2>
      <p class="muted">Images up to {MAX_IMAGE_MB}MB, video up to {MAX_VIDEO_MB}MB.</p>
    </div>
  </div>

  <div class="grid">
    <label class="file">
      <span>File</span>
      <input type="file" accept="image/*,video/*" on:change={handleFileChange} />
      {#if file}
        <small>{file.name} ({Math.round(file.size / 1024)} KB)</small>
      {/if}
    </label>

    <div class="radio">
      <span>Visibility</span>
      <label><input type="radio" bind:group={visibility} value="private" /> Private</label>
      <label><input type="radio" bind:group={visibility} value="public" /> Public</label>
    </div>
  </div>

  <div class="grid">
    <label>
      <span>Title</span>
      <input type="text" bind:value={title} placeholder="Optional title" />
    </label>
    <label>
      <span>Text</span>
      <textarea rows="3" bind:value={text} placeholder="Optional description"></textarea>
    </label>
    <label>
      <span>Publish at</span>
      <input type="datetime-local" bind:value={publishedAt} />
    </label>
  </div>

  <button class="primary" type="button" on:click={handleUpload} disabled={isUploading}>
    {isUploading ? 'Uploading...' : 'Upload now'}
  </button>

  {#if uploadStatus}
    <p class="status">{uploadStatus}</p>
  {/if}
  {#if uploadError}
    <p class="error">{uploadError}</p>
  {/if}

  {#if uploadedUrl}
    <div class="result">
      <div>
        <p class="eyebrow">Result</p>
        <h3>Signed URL ready</h3>
        <p class="muted">Media ID: {uploadedMediaId}</p>
        <p class="muted">Key: {uploadedKey}</p>
        <p class="muted">Expires in: {expiresIn}s</p>
      </div>
      <div class="url-box">
        <a href={uploadedUrl} target="_blank" rel="noreferrer">Open file</a>
        <button class="ghost" type="button" on:click={refreshUrl}>Refresh URL</button>
      </div>
    </div>
  {/if}
</div>

<style>
  .card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08);
  }

  .card + .card {
    margin-top: 24px;
  }

  .card-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 16px;
  }

  .eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.2em;
    font-size: 0.7rem;
    color: var(--accent);
    margin: 0;
  }

  h2 {
    margin: 6px 0 4px;
    font-size: 1.5rem;
  }

  .muted {
    color: var(--muted);
    font-size: 0.9rem;
  }

  .grid {
    display: grid;
    gap: 16px;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    margin-bottom: 16px;
  }

  label span {
    display: block;
    font-size: 0.85rem;
    margin-bottom: 6px;
    color: var(--muted);
  }

  input,
  textarea {
    width: 100%;
    padding: 12px 14px;
    border-radius: 14px;
    border: 1px solid transparent;
    background: #f7f5f1;
    color: var(--ink);
    font-family: inherit;
    font-size: 0.95rem;
  }

  input:focus,
  textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(242, 157, 76, 0.2);
  }

  button {
    border: none;
    border-radius: 999px;
    padding: 12px 18px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .primary {
    background: var(--accent);
    color: #1c1b19;
    box-shadow: 0 12px 30px rgba(242, 157, 76, 0.3);
  }

  .primary:hover {
    transform: translateY(-1px);
  }

  .ghost {
    background: transparent;
    color: var(--ink);
    border: 1px solid var(--line);
  }

  .divider {
    text-align: center;
    font-size: 0.8rem;
    color: var(--muted);
    margin: 12px 0;
  }

  .status {
    margin: 8px 0 0;
    font-size: 0.9rem;
    color: var(--accent);
  }

  .error {
    margin: 8px 0 0;
    font-size: 0.9rem;
    color: #c44536;
  }

  .status-row {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .pill {
    background: #efe7dc;
    color: #7a4d1b;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }

  .radio label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    margin-bottom: 6px;
  }

  .result {
    margin-top: 20px;
    padding: 16px;
    border-radius: 18px;
    background: linear-gradient(140deg, #f7f4ed, #fff);
    border: 1px solid var(--line);
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: space-between;
  }

  .url-box {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .url-box a {
    color: var(--ink);
    text-decoration: none;
    font-weight: 600;
  }

  .file small {
    display: block;
    margin-top: 8px;
    color: var(--muted);
    font-size: 0.8rem;
  }
</style>
