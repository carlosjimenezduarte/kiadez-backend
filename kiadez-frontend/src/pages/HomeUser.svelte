<script>
  import { onMount } from 'svelte';
  import { initPurposeCoverModule } from '../lib/purposeCover';

  onMount(() => {
    // COVER: upload + drag to position
    const coverMedia = document.getElementById('coverMedia');
    const coverImg = document.getElementById('coverImg');
    const coverFile = document.getElementById('coverFile');
    const btnChangeCover = document.getElementById('btnChangeCover');
    const coverHint = document.getElementById('coverHint');

    let isDraggingCover = false;
    let startX = 0;
    let startY = 0;
    let currentX = 0;
    let currentY = 0;

    const applyCoverTransform = () => {
      if (coverImg) {
        coverImg.style.transform = `translate(${currentX}px, ${currentY}px)`;
      }
    };

    const handleChangeCover = () => coverFile?.click();
    const handleCoverFileChange = (event) => {
      const file = event?.target?.files?.[0];
      if (!file || !coverImg) return;

      const url = URL.createObjectURL(file);
      coverImg.src = url;
      currentX = 0;
      currentY = 0;
      applyCoverTransform();
    };

    const handleCoverMouseDown = (event) => {
      const isButton = event.target.closest('.cover-actions');
      const isPill = event.target.closest('.purpose-pill');
      if (isButton || isPill) return;

      isDraggingCover = true;
      startX = event.clientX - currentX;
      startY = event.clientY - currentY;
      coverMedia?.classList.add('is-dragging');
      coverHint?.classList.add('hidden');
    };

    const handleCoverMouseMove = (event) => {
      if (!isDraggingCover) return;
      currentX = event.clientX - startX;
      currentY = event.clientY - startY;
      applyCoverTransform();
    };

    const handleCoverMouseUp = () => {
      if (!isDraggingCover) return;
      isDraggingCover = false;
      coverMedia?.classList.remove('is-dragging');
    };

    btnChangeCover?.addEventListener('click', handleChangeCover);
    coverFile?.addEventListener('change', handleCoverFileChange);
    coverMedia?.addEventListener('mousedown', handleCoverMouseDown);
    window.addEventListener('mousemove', handleCoverMouseMove);
    window.addEventListener('mouseup', handleCoverMouseUp);

    initPurposeCoverModule();

    // POSTS
    const API = 'http://127.0.0.1:8000';
    const postModalOverlay = document.getElementById('postModalOverlay');
    const openPostModal = document.getElementById('openPostModal');
    const closePostModal = document.getElementById('closePostModal');
    const cancelPost = document.getElementById('cancelPost');
    const postFile = document.getElementById('postFile');
    const uploadHint = document.getElementById('uploadHint');
    const postPreview = document.getElementById('postPreview');
    const publishPost = document.getElementById('publishPost');
    const postText = document.getElementById('postText');
    const postVisibility = document.getElementById('postVisibility');
    const postsList = document.getElementById('homePostsList');
    const postsStatus = document.getElementById('postsStatus');
    const starsTotalLabel = document.getElementById('homeStarsTotal');

    const deletePostOverlay = document.getElementById('deletePostModalOverlay');
    const closeDeletePostModal = document.getElementById('closeDeletePostModal');
    const cancelDeletePost = document.getElementById('cancelDeletePost');
    const confirmDeletePost = document.getElementById('confirmDeletePost');

    const reportPostOverlay = document.getElementById('reportPostModalOverlay');
    const closeReportPostModal = document.getElementById('closeReportPostModal');
    const cancelReportPost = document.getElementById('cancelReportPost');
    const submitReportPost = document.getElementById('submitReportPost');
    const reportReasonOtherWrap = document.getElementById('reportReasonOtherWrap');
    const reportReasonOther = document.getElementById('reportReasonOther');

    const commentsOverlay = document.getElementById('postCommentsModalOverlay');
    const closeCommentsModal = document.getElementById('closePostCommentsModal');
    const cancelCommentsModal = document.getElementById('cancelPostCommentsModal');
    const commentsList = document.getElementById('postCommentsList');
    const commentsStatus = document.getElementById('postCommentsStatus');
    const commentInput = document.getElementById('postCommentInput');
    const sendComment = document.getElementById('sendPostComment');
    const commentsTitle = document.getElementById('postCommentsTitle');

    let selectedFile = null;
    let selectedFileURL = null;
    let selectedCommentPostId = null;
    let selectedDeletePostId = null;
    let selectedReportPostId = null;

    const getAccessToken = () => localStorage.getItem('access_token') || '';

    const escapeHtml = (value) =>
      (value || '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');

    const setPostsStatus = (message, isError = false) => {
      if (!postsStatus) return;
      postsStatus.textContent = message || '';
      postsStatus.classList.toggle('posts-status-error', Boolean(isError));
    };

    const relativeTime = (isoDate) => {
      const ts = Date.parse(isoDate);
      if (Number.isNaN(ts)) return 'ahora';
      const minutes = Math.floor((Date.now() - ts) / 60000);
      if (minutes < 1) return 'ahora';
      if (minutes < 60) return `hace ${minutes} min`;
      const hours = Math.floor(minutes / 60);
      if (hours < 24) return `hace ${hours} h`;
      const days = Math.floor(hours / 24);
      return `hace ${days} dia${days > 1 ? 's' : ''}`;
    };

    const apiFetch = async (path, options = {}) => {
      const token = getAccessToken();
      if (!token) {
        window.location.href = '/login.html';
        throw new Error('No hay sesion activa');
      }
      const headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`
      };
      const res = await fetch(`${API}${path}`, { ...options, headers });
      if (res.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login.html';
        throw new Error('Sesion expirada');
      }
      return res;
    };

    const renderPosts = (posts) => {
      if (!postsList) return;
      if (!Array.isArray(posts) || posts.length === 0) {
        postsList.innerHTML = `
          <article class="panel post post-empty">
            <p class="post-text">Aun no hay publicaciones. Crea la primera desde el boton "Que estas pensando?".</p>
          </article>
        `;
        return;
      }

      postsList.innerHTML = posts
        .map((post) => {
          const mediaHtml = post.media_url
            ? post.media_kind === 'video'
              ? `<div class="post-media"><video src="${post.media_url}" controls></video></div>`
              : `<div class="post-media"><img src="${post.media_url}" alt="Media de la publicacion" /></div>`
            : '';
          const starDisabled = post.starred_by_me ? 'disabled' : '';
          const starLabel = post.starred_by_me
            ? `⭐ Estrella donada (${post.star_count})`
            : `⭐ Donar estrella (${post.star_count})`;
          const reportBtn = post.is_mine
            ? ''
            : `<button class="post-head-btn" type="button" data-action="report-post" data-post-id="${post.id}" title="Reportar publicacion">🚩</button>`;
          const deleteBtn = post.is_mine
            ? `<button class="post-head-btn" type="button" data-action="delete-post" data-post-id="${post.id}" title="Eliminar publicacion">🗑</button>`
            : '';

          return `
            <article class="panel post" data-post-id="${post.id}">
              <div class="post-head">
                <div>
                  <strong>${escapeHtml(post.author.name)}</strong>
                  <span class="post-meta">· ${relativeTime(post.created_at)} · ${post.visibility === 'private' ? 'Privado' : 'Publico'}</span>
                </div>
                <div class="post-head-actions">
                  ${reportBtn}
                  ${deleteBtn}
                </div>
              </div>
              ${post.text ? `<p class="post-text">${escapeHtml(post.text)}</p>` : ''}
              ${mediaHtml}
              <p class="post-warning">La donacion de estrella es irreversible.</p>
              <div class="post-actions">
                <button class="post-btn" type="button" data-action="star-post" data-post-id="${post.id}" ${starDisabled}>${starLabel}</button>
                <button class="post-btn" type="button" data-action="comment-post" data-post-id="${post.id}">💬 Comentar (${post.comment_count})</button>
                <button class="post-btn" type="button" data-action="share-post" data-post-id="${post.id}">🔁 Compartir (${post.share_count})</button>
              </div>
            </article>
          `;
        })
        .join('');
    };

    const loadMyStats = async () => {
      try {
        const res = await apiFetch('/posts/me/stats');
        const data = await res.json();
        if (res.ok && starsTotalLabel) {
          starsTotalLabel.textContent = Number(data.my_received_stars_total || 0).toLocaleString('es-CO');
        }
      } catch (error) {
        console.error(error);
      }
    };

    const loadFeed = async () => {
      try {
        const res = await apiFetch('/posts/feed?limit=40');
        const data = await res.json();
        if (!res.ok) {
          setPostsStatus(data.detail || 'No se pudo cargar el feed.', true);
          return;
        }
        renderPosts(data);
        setPostsStatus('');
      } catch (error) {
        setPostsStatus('No se pudo conectar con el servidor de publicaciones.', true);
      }
    };

    const openPost = () => {
      postModalOverlay?.classList.remove('hidden');
      postModalOverlay?.setAttribute('aria-hidden', 'false');
    };

    const closePost = () => {
      postModalOverlay?.classList.add('hidden');
      postModalOverlay?.setAttribute('aria-hidden', 'true');
      if (uploadHint) uploadHint.textContent = 'Sin archivo adjunto';
      if (postPreview) {
        postPreview.innerHTML = '';
        postPreview.classList.add('hidden');
      }
      if (selectedFileURL) {
        URL.revokeObjectURL(selectedFileURL);
        selectedFileURL = null;
      }
      selectedFile = null;
      if (postFile) postFile.value = '';
      if (postText) postText.value = '';
      if (postVisibility) postVisibility.value = 'public';
    };

    const handlePostOverlayClick = (event) => {
      if (event.target === postModalOverlay) closePost();
    };

    const handlePostFileChange = (event) => {
      const file = event?.target?.files?.[0];
      selectedFile = file || null;
      if (!file) return;
      if (uploadHint) uploadHint.textContent = file.name;

      if (selectedFileURL) URL.revokeObjectURL(selectedFileURL);
      selectedFileURL = URL.createObjectURL(file);
      if (!postPreview) return;
      postPreview.classList.remove('hidden');

      if (file.type.startsWith('image/')) {
        postPreview.innerHTML = `<img src="${selectedFileURL}" alt="Previsualizacion" />`;
      } else if (file.type.startsWith('video/')) {
        postPreview.innerHTML = `<video src="${selectedFileURL}" controls></video>`;
      } else {
        selectedFile = null;
        postPreview.innerHTML = '';
        postPreview.classList.add('hidden');
        setPostsStatus('Solo se permiten archivos de imagen o video.', true);
      }
    };

    const uploadMediaIfNeeded = async (visibilityValue) => {
      if (!selectedFile) return null;

      const presignRes = await apiFetch('/media/presign/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: selectedFile.name,
          content_type: selectedFile.type,
          size_bytes: selectedFile.size,
          visibility: visibilityValue
        })
      });
      const presignData = await presignRes.json();
      if (!presignRes.ok) {
        throw new Error(presignData.detail || 'No se pudo preparar la carga de media.');
      }

      const uploadRes = await fetch(presignData.upload_url, {
        method: 'PUT',
        headers: presignData.required_headers || { 'Content-Type': selectedFile.type },
        body: selectedFile
      });
      if (!uploadRes.ok) {
        throw new Error('No se pudo subir el archivo.');
      }

      const confirmRes = await apiFetch('/media/confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ media_id: presignData.media_id })
      });
      const confirmData = await confirmRes.json();
      if (!confirmRes.ok) {
        throw new Error(confirmData.detail || 'No se pudo confirmar la media.');
      }

      const mediaKind = selectedFile.type.startsWith('video/') ? 'video' : 'image';
      return { media_id: presignData.media_id, media_kind: mediaKind };
    };

    const handlePublishPost = async () => {
      const text = (postText?.value || '').trim();
      if (!text && !selectedFile) {
        setPostsStatus('Debes escribir texto o adjuntar imagen/video.', true);
        return;
      }

      const oldLabel = publishPost?.textContent || 'Publicar';
      if (publishPost) {
        publishPost.disabled = true;
        publishPost.textContent = 'Publicando...';
      }

      try {
        const visibilityValue = (postVisibility?.value || 'public').toLowerCase();
        const mediaData = await uploadMediaIfNeeded(visibilityValue);
        const payload = {
          text: text || null,
          visibility: visibilityValue,
          media_id: mediaData?.media_id ?? null,
          media_kind: mediaData?.media_kind ?? null
        };

        const res = await apiFetch('/posts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || 'No se pudo crear la publicacion.');
        }

        setPostsStatus('Publicacion creada correctamente.');
        closePost();
        await Promise.all([loadFeed(), loadMyStats()]);
      } catch (error) {
        setPostsStatus(error.message || 'No se pudo publicar.', true);
      } finally {
        if (publishPost) {
          publishPost.disabled = false;
          publishPost.textContent = oldLabel;
        }
      }
    };

    const closeDeleteModal = () => {
      deletePostOverlay?.classList.add('hidden');
      deletePostOverlay?.setAttribute('aria-hidden', 'true');
      selectedDeletePostId = null;
    };

    const closeReportModal = () => {
      reportPostOverlay?.classList.add('hidden');
      reportPostOverlay?.setAttribute('aria-hidden', 'true');
      selectedReportPostId = null;
      if (reportReasonOther) reportReasonOther.value = '';
      if (reportReasonOtherWrap) reportReasonOtherWrap.classList.add('hidden');
      const defaultOption = document.querySelector('input[name="postReportReason"][value="violent"]');
      if (defaultOption) defaultOption.checked = true;
    };

    const closeComments = () => {
      commentsOverlay?.classList.add('hidden');
      commentsOverlay?.setAttribute('aria-hidden', 'true');
      selectedCommentPostId = null;
      if (commentInput) commentInput.value = '';
      if (commentsList) commentsList.innerHTML = '';
    };

    const loadComments = async () => {
      if (!selectedCommentPostId || !commentsList) return;
      commentsList.innerHTML = '';
      if (commentsStatus) commentsStatus.textContent = 'Cargando comentarios...';
      try {
        const res = await apiFetch(`/posts/${selectedCommentPostId}/comments?limit=200`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo cargar comentarios.');
        if (!Array.isArray(data) || data.length === 0) {
          commentsList.innerHTML = '<p class="post-comments-empty">Aun no hay comentarios.</p>';
        } else {
          commentsList.innerHTML = data
            .map(
              (comment) => `
                <article class="post-comment-item">
                  <div class="post-comment-head">
                    <strong>${escapeHtml(comment.author.name)}</strong>
                    <span>${relativeTime(comment.created_at)}</span>
                  </div>
                  <p>${escapeHtml(comment.text)}</p>
                </article>
              `
            )
            .join('');
        }
        if (commentsStatus) commentsStatus.textContent = '';
      } catch (error) {
        if (commentsStatus) commentsStatus.textContent = error.message || 'No se pudieron cargar comentarios.';
      }
    };

    const handlePostsClick = async (event) => {
      const button = event.target.closest('[data-action][data-post-id]');
      if (!button) return;
      const action = button.dataset.action;
      const postId = Number(button.dataset.postId);
      if (!postId) return;

      if (action === 'star-post') {
        try {
          const res = await apiFetch(`/posts/${postId}/stars`, { method: 'POST' });
          const data = await res.json();
          if (!res.ok) throw new Error(data.detail || 'No se pudo donar la estrella.');
          setPostsStatus('Estrella donada. Esta accion es irreversible.');
          await Promise.all([loadFeed(), loadMyStats()]);
        } catch (error) {
          setPostsStatus(error.message || 'No se pudo donar la estrella.', true);
        }
        return;
      }

      if (action === 'comment-post') {
        selectedCommentPostId = postId;
        if (commentsTitle) commentsTitle.textContent = `Comentarios de la publicacion #${postId}`;
        commentsOverlay?.classList.remove('hidden');
        commentsOverlay?.setAttribute('aria-hidden', 'false');
        await loadComments();
        return;
      }

      if (action === 'share-post') {
        try {
          await apiFetch(`/posts/${postId}/share`, { method: 'POST' });
          const shareUrl = `${window.location.origin}/home_user.html?post=${postId}`;
          if (navigator.share) {
            await navigator.share({ title: 'Kiadez', text: 'Mira esta publicacion', url: shareUrl });
          } else if (navigator.clipboard?.writeText) {
            await navigator.clipboard.writeText(shareUrl);
          }
          setPostsStatus('Publicacion compartida.');
          await loadFeed();
        } catch (error) {
          setPostsStatus(error.message || 'No se pudo compartir.', true);
        }
        return;
      }

      if (action === 'delete-post') {
        selectedDeletePostId = postId;
        deletePostOverlay?.classList.remove('hidden');
        deletePostOverlay?.setAttribute('aria-hidden', 'false');
        return;
      }

      if (action === 'report-post') {
        selectedReportPostId = postId;
        reportPostOverlay?.classList.remove('hidden');
        reportPostOverlay?.setAttribute('aria-hidden', 'false');
      }
    };

    const handleConfirmDeletePost = async () => {
      if (!selectedDeletePostId) return;
      try {
        const res = await apiFetch(`/posts/${selectedDeletePostId}`, { method: 'DELETE' });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo eliminar la publicacion.');
        setPostsStatus(`Publicacion eliminada. Se restaron ${data.removed_stars || 0} estrellas asociadas.`);
        closeDeleteModal();
        await Promise.all([loadFeed(), loadMyStats()]);
      } catch (error) {
        setPostsStatus(error.message || 'No se pudo eliminar la publicacion.', true);
      }
    };

    const handleReportReasonChange = (event) => {
      const selected = event.target?.value || '';
      if (!reportReasonOtherWrap) return;
      if (selected === 'other') reportReasonOtherWrap.classList.remove('hidden');
      else reportReasonOtherWrap.classList.add('hidden');
    };

    const handleSubmitReport = async () => {
      if (!selectedReportPostId) return;
      const selected = document.querySelector('input[name="postReportReason"]:checked');
      const reason = selected?.value;
      if (!reason) {
        setPostsStatus('Debes elegir una razon de reporte.', true);
        return;
      }
      const otherReason = (reportReasonOther?.value || '').trim();
      if (reason === 'other' && !otherReason) {
        setPostsStatus('Debes escribir la razon cuando eliges "Otra razon".', true);
        return;
      }

      try {
        const res = await apiFetch(`/posts/${selectedReportPostId}/reports`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reason, other_reason: otherReason || null })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo enviar el reporte.');
        setPostsStatus('Reporte enviado correctamente.');
        closeReportModal();
      } catch (error) {
        setPostsStatus(error.message || 'No se pudo enviar el reporte.', true);
      }
    };

    const handleSendComment = async () => {
      if (!selectedCommentPostId) return;
      const text = (commentInput?.value || '').trim();
      if (!text) {
        if (commentsStatus) commentsStatus.textContent = 'Escribe un comentario antes de enviar.';
        return;
      }
      try {
        const res = await apiFetch(`/posts/${selectedCommentPostId}/comments`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo crear el comentario.');
        if (commentInput) commentInput.value = '';
        if (commentsStatus) commentsStatus.textContent = '';
        await Promise.all([loadComments(), loadFeed()]);
      } catch (error) {
        if (commentsStatus) commentsStatus.textContent = error.message || 'No se pudo guardar el comentario.';
      }
    };

    openPostModal?.addEventListener('click', openPost);
    closePostModal?.addEventListener('click', closePost);
    cancelPost?.addEventListener('click', closePost);
    postModalOverlay?.addEventListener('click', handlePostOverlayClick);
    postFile?.addEventListener('change', handlePostFileChange);
    publishPost?.addEventListener('click', handlePublishPost);
    postsList?.addEventListener('click', handlePostsClick);

    closeDeletePostModal?.addEventListener('click', closeDeleteModal);
    cancelDeletePost?.addEventListener('click', closeDeleteModal);
    confirmDeletePost?.addEventListener('click', handleConfirmDeletePost);
    deletePostOverlay?.addEventListener('click', (event) => {
      if (event.target === deletePostOverlay) closeDeleteModal();
    });

    closeReportPostModal?.addEventListener('click', closeReportModal);
    cancelReportPost?.addEventListener('click', closeReportModal);
    submitReportPost?.addEventListener('click', handleSubmitReport);
    reportPostOverlay?.addEventListener('click', (event) => {
      if (event.target === reportPostOverlay) closeReportModal();
    });
    document
      .querySelectorAll('input[name="postReportReason"]')
      .forEach((input) => input.addEventListener('change', handleReportReasonChange));

    closeCommentsModal?.addEventListener('click', closeComments);
    cancelCommentsModal?.addEventListener('click', closeComments);
    sendComment?.addEventListener('click', handleSendComment);
    commentsOverlay?.addEventListener('click', (event) => {
      if (event.target === commentsOverlay) closeComments();
    });

    void Promise.all([loadFeed(), loadMyStats()]);

    return () => {
      if (selectedFileURL) URL.revokeObjectURL(selectedFileURL);

      btnChangeCover?.removeEventListener('click', handleChangeCover);
      coverFile?.removeEventListener('change', handleCoverFileChange);
      coverMedia?.removeEventListener('mousedown', handleCoverMouseDown);
      window.removeEventListener('mousemove', handleCoverMouseMove);
      window.removeEventListener('mouseup', handleCoverMouseUp);

      openPostModal?.removeEventListener('click', openPost);
      closePostModal?.removeEventListener('click', closePost);
      cancelPost?.removeEventListener('click', closePost);
      postModalOverlay?.removeEventListener('click', handlePostOverlayClick);
      postFile?.removeEventListener('change', handlePostFileChange);
      publishPost?.removeEventListener('click', handlePublishPost);
      postsList?.removeEventListener('click', handlePostsClick);

      closeDeletePostModal?.removeEventListener('click', closeDeleteModal);
      cancelDeletePost?.removeEventListener('click', closeDeleteModal);
      confirmDeletePost?.removeEventListener('click', handleConfirmDeletePost);

      closeReportPostModal?.removeEventListener('click', closeReportModal);
      cancelReportPost?.removeEventListener('click', closeReportModal);
      submitReportPost?.removeEventListener('click', handleSubmitReport);
      document
        .querySelectorAll('input[name="postReportReason"]')
        .forEach((input) => input.removeEventListener('change', handleReportReasonChange));

      closeCommentsModal?.removeEventListener('click', closeComments);
      cancelCommentsModal?.removeEventListener('click', closeComments);
      sendComment?.removeEventListener('click', handleSendComment);
    };

  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Inicio</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background">
  <main class="user-home">
    <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt="Portada" />

        <div class="cover-actions">
          <button class="icon-btn" id="btnChangeCover" type="button" title="Cambiar portada">
            Cambiar portada
          </button>
          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button" title="Editar mi propósito de vida">
            Editar mi propósito de vida
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="purpose-triangle" aria-label="Deseos de propósito">
          <button class="purpose-pill purpose-top" type="button" id="purpose1">
            Deseo #1: Secreto
          </button>

          <button class="purpose-pill purpose-left" type="button" id="purpose2">
            Deseo construir el Reino de Combray
          </button>

          <button class="purpose-pill purpose-right" type="button" id="purpose3">
            Deseo estar unido a Jesús
          </button>
        </div>

        <div class="cover-hint" id="coverHint">
          Arrastra la portada para encuadrarla
        </div>
      </div>
    </section>

    <div class="home-body">
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
          <span class="nav-icon">⭐</span>
          <span><strong id="homeStarsTotal">0</strong> estrellas</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
      </nav>

      <section class="profile-grid">
        <aside class="left-col">
          <article class="panel profile-card">
            <div class="profile-row">
              <img class="avatar" src="assets/avatar-default.jpg" alt="Foto de perfil" />
              <div class="profile-meta">
                <h2 class="profile-name">Carlos Jiménez Duarte</h2>
                <p class="profile-rank">Rango 2 · Aprendiz</p>

                <div class="profile-actions">
                  <button class="btn btn-outline btn-compact" type="button">Editar perfil</button>
                  <button class="btn btn-primary btn-compact" type="button">Ver mi perfil público</button>
                </div>
              </div>
            </div>
          </article>

          <article class="panel">
            <a href="/fulfilled-wishes.html" class="panel-title-link">Mis deseos cumplidos</a>
            <p class="panel-muted">
              Accede a tu historial de deseos completados y a los detalles de cada logro.
            </p>
          </article>

          <article class="panel">
            <h3 class="panel-title">Acerca de mí</h3>
            <p class="panel-text">
              Aficionado a los videojuegos, los libros, los perros y la buena comida.
              Mi filosofía es que: la sabiduría suprema consiste en tener sueños lo suficientemente grandes
              para no perderlos de vista mientras se persiguen.
            </p>
          </article>

          <article class="panel">
            <div class="panel-head">
              <h3 class="panel-title">Mis deseos públicos</h3>
              <span class="panel-badge">7 / 50</span>
            </div>

            <ul class="wish-list">
              <li class="wish-item"><span class="wish-dot"></span> Comprar mi PC Gamer</li>
              <li class="wish-item"><span class="wish-dot"></span> Comprar mi escritorio gamer</li>
              <li class="wish-item"><span class="wish-dot"></span> Recuperar los Dofus vendidos</li>
              <li class="wish-item"><span class="wish-dot"></span> Publicar Kiadez oficialmente</li>
              <li class="wish-item"><span class="wish-dot"></span> Alcanzar el primer millón de usuarios</li>
              <li class="wish-item"><span class="wish-dot"></span> Montar el Santuario del Logos</li>
              <li class="wish-item"><span class="wish-dot"></span> Viajar con propósito (Monte Manjaro)</li>
            </ul>

            <a href="/my-public-whishes.html" class="btn btn-outline btn-compact btn-inline">Ver más</a>
          </article>

          <article class="panel">
            <div class="panel-head">
              <h3 class="panel-title">Mis deseos secretos</h3>
              <span class="panel-badge">20 / 50</span>
            </div>

            <div class="secret-meter">
              <div class="secret-number">20/50</div>
              <div class="secret-sub">Solo tú puedes ver esta cifra</div>
            </div>
          </article>

          <article class="panel">
            <div class="panel-head">
              <h3 class="panel-title">Calendario</h3>
              <span class="panel-badge">Actividad</span>
            </div>

            <div class="heatmap" aria-label="Actividad del usuario (mock)">
              <div class="heat-col">
                <span class="heat-cell lv0"></span><span class="heat-cell lv1"></span><span class="heat-cell lv2"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv0"></span><span class="heat-cell lv1"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv1"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv2"></span><span class="heat-cell lv3"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv0"></span><span class="heat-cell lv2"></span><span class="heat-cell lv2"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv3"></span><span class="heat-cell lv2"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv1"></span><span class="heat-cell lv2"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv1"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv2"></span><span class="heat-cell lv3"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv1"></span><span class="heat-cell lv2"></span><span class="heat-cell lv3"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv0"></span><span class="heat-cell lv0"></span><span class="heat-cell lv1"></span><span class="heat-cell lv1"></span><span class="heat-cell lv2"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv1"></span><span class="heat-cell lv2"></span><span class="heat-cell lv1"></span><span class="heat-cell lv3"></span><span class="heat-cell lv2"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv0"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv1"></span><span class="heat-cell lv2"></span><span class="heat-cell lv3"></span><span class="heat-cell lv2"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv2"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv0"></span><span class="heat-cell lv1"></span><span class="heat-cell lv2"></span><span class="heat-cell lv1"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv1"></span><span class="heat-cell lv2"></span><span class="heat-cell lv3"></span><span class="heat-cell lv2"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv0"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv0"></span><span class="heat-cell lv1"></span><span class="heat-cell lv2"></span><span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv1"></span><span class="heat-cell lv2"></span>
              </div>
              <div class="heat-col">
                <span class="heat-cell lv1"></span><span class="heat-cell lv0"></span><span class="heat-cell lv1"></span><span class="heat-cell lv2"></span><span class="heat-cell lv3"></span><span class="heat-cell lv2"></span><span class="heat-cell lv1"></span>
              </div>
            </div>

            <a href="/calendar.html" class="btn btn-outline btn-compact btn-inline">Ver calendario</a>
          </article>

          <article class="panel">
            <div class="panel-head">
              <h3 class="panel-title">Oráculo</h3>
              <span class="panel-badge">Última carta</span>
            </div>

            <div class="oracle-card">
              <img src="assets/oracle-default.jpg" alt="Última carta del Oráculo" />
            </div>

            <a href="/oracle.html" class="btn btn-outline btn-compact btn-inline">Abrir Oráculo</a>
          </article>
        </aside>

        <section class="right-col">
          <article class="panel composer">
            <div class="composer-row">
              <img class="avatar avatar-sm" src="assets/avatar-default.jpg" alt="Avatar" />
              <button class="composer-input" id="openPostModal" type="button">
                ¿Qué estás pensando?
              </button>
            </div>

            <div class="composer-actions">
              <button class="mini-action" type="button" data-kind="text">Texto</button>
              <button class="mini-action" type="button" data-kind="image">Imagen</button>
              <button class="mini-action" type="button" data-kind="video">Video</button>
            </div>
          </article>

          <p class="posts-status" id="postsStatus"></p>
          <div class="posts-list" id="homePostsList"></div>
        </section>
      </section>
    </div>
  </main>

  <footer class="kiadez-footer">
    <div class="footer-main">
      <div class="footer-column footer-origin">
        <p class="footer-poem">
          Kiadez fue llamado por una estrella a subir el Monte Manjaro.<br />
          No para dominar, sino para orientar.<br />
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

<div class="modal-overlay hidden" id="postModalOverlay" aria-hidden="true">
  <div class="modal modal-wide" role="dialog" aria-modal="true" aria-label="Crear publicación">
    <div class="modal-head">
      <h3>Crear publicación</h3>
      <button class="modal-close" type="button" id="closePostModal">✕</button>
    </div>

    <div class="modal-body">
      <div class="post-modal-top">
        <img class="avatar avatar-sm" src="assets/avatar-default.jpg" alt="Avatar" />
        <div>
          <div class="post-modal-name"><strong>Carlos Jiménez Duarte</strong></div>
          <select class="modal-select" id="postVisibility">
            <option value="public">Público</option>
            <option value="private">Privado</option>
          </select>
        </div>
      </div>

      <textarea class="modal-textarea" id="postText" rows="5" placeholder="Escribe algo..."></textarea>

      <div class="upload-row">
        <label class="upload-btn" for="postFile">Adjuntar imagen o video</label>
        <input id="postFile" type="file" accept="image/*,video/*" class="hidden" />
        <div class="upload-hint" id="uploadHint">Sin archivo adjunto</div>
      </div>

      <div class="preview hidden" id="postPreview"></div>
    </div>

    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelPost">Cancelar</button>
      <button class="btn btn-primary btn-compact" type="button" id="publishPost">Publicar</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="deletePostModalOverlay" aria-hidden="true">
  <div class="modal wish-modal delete-wish-modal" role="dialog" aria-modal="true" aria-label="Eliminar publicación">
    <div class="modal-head">
      <h3>Eliminar publicación</h3>
      <button class="modal-close" type="button" id="closeDeletePostModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="modal-label-center">
        Esta acción eliminará la publicación y restará permanentemente las estrellas asociadas a ella.
      </p>
      <p class="modal-label-center muted">Esta acción no se puede deshacer.</p>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelDeletePost">Cancelar</button>
      <button class="btn btn-primary btn-compact" type="button" id="confirmDeletePost">Eliminar</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="reportPostModalOverlay" aria-hidden="true">
  <div class="modal wish-modal fulfill-wish-modal" role="dialog" aria-modal="true" aria-label="Reportar publicación">
    <div class="modal-head">
      <h3>Reportar publicación</h3>
      <button class="modal-close" type="button" id="closeReportPostModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="modal-label-center">
        Selecciona la razón por la cual deseas reportar esta publicación.
      </p>
      <div class="report-reasons">
        <label class="report-option"><input type="radio" name="postReportReason" value="violent" checked /> Contenido violento o perturbador</label>
        <label class="report-option"><input type="radio" name="postReportReason" value="divisive" /> Contenido que promueve confrontación o división excesiva</label>
        <label class="report-option"><input type="radio" name="postReportReason" value="sexual" /> Contenido sexual explícito o inapropiado</label>
        <label class="report-option"><input type="radio" name="postReportReason" value="other" /> Otra razón</label>
      </div>
      <div id="reportReasonOtherWrap" class="report-other-wrap hidden">
        <label class="modal-label" for="reportReasonOther">Describe la razón</label>
        <textarea class="modal-textarea" id="reportReasonOther" rows="3" placeholder="Escribe tu razón"></textarea>
      </div>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelReportPost">Cancelar</button>
      <button class="btn btn-primary btn-compact" type="button" id="submitReportPost">Enviar reporte</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="postCommentsModalOverlay" aria-hidden="true">
  <div class="modal modal-wide" role="dialog" aria-modal="true" aria-label="Comentarios de publicación">
    <div class="modal-head">
      <h3 id="postCommentsTitle">Comentarios</h3>
      <button class="modal-close" type="button" id="closePostCommentsModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="posts-status" id="postCommentsStatus"></p>
      <div class="post-comments-list" id="postCommentsList"></div>
      <label class="modal-label" for="postCommentInput">Agregar comentario</label>
      <textarea class="modal-textarea" id="postCommentInput" rows="3" maxlength="1200" placeholder="Escribe un comentario"></textarea>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelPostCommentsModal">Cerrar</button>
      <button class="btn btn-primary btn-compact" type="button" id="sendPostComment">Comentar</button>
    </div>
  </div>
</div>
