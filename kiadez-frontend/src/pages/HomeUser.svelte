<script>
  import { onMount } from 'svelte';

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

    // PURPOSE MODAL
    const purposeModalOverlay = document.getElementById('purposeModalOverlay');
    const btnEditPurposes = document.getElementById('btnEditPurposes');
    const closePurposeModal = document.getElementById('closePurposeModal');
    const cancelPurposeModal = document.getElementById('cancelPurposeModal');
    const savePurposeModal = document.getElementById('savePurposeModal');

    const p1 = document.getElementById('purpose1');
    const p2 = document.getElementById('purpose2');
    const p3 = document.getElementById('purpose3');

    const purposeInput1 = document.getElementById('purposeInput1');
    const purposeInput2 = document.getElementById('purposeInput2');
    const purposeInput3 = document.getElementById('purposeInput3');

    const openPurposeModal = () => {
      if (purposeInput1 && p1) purposeInput1.value = p1.textContent.trim();
      if (purposeInput2 && p2) purposeInput2.value = p2.textContent.trim();
      if (purposeInput3 && p3) purposeInput3.value = p3.textContent.trim();

      purposeModalOverlay?.classList.remove('hidden');
      purposeModalOverlay?.setAttribute('aria-hidden', 'false');
    };

    const closePurpose = () => {
      purposeModalOverlay?.classList.add('hidden');
      purposeModalOverlay?.setAttribute('aria-hidden', 'true');
    };

    const handleSavePurpose = () => {
      if (p1 && purposeInput1?.value?.trim()) p1.textContent = purposeInput1.value.trim();
      if (p2 && purposeInput2?.value?.trim()) p2.textContent = purposeInput2.value.trim();
      if (p3 && purposeInput3?.value?.trim()) p3.textContent = purposeInput3.value.trim();
      closePurpose();
    };

    const handlePurposeOverlayClick = (event) => {
      if (event.target === purposeModalOverlay) closePurpose();
    };

    btnEditPurposes?.addEventListener('click', openPurposeModal);
    closePurposeModal?.addEventListener('click', closePurpose);
    cancelPurposeModal?.addEventListener('click', closePurpose);
    savePurposeModal?.addEventListener('click', handleSavePurpose);
    purposeModalOverlay?.addEventListener('click', handlePurposeOverlayClick);

    // POST MODAL
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
      if (postFile) postFile.value = '';
      if (postText) postText.value = '';
      if (postVisibility) postVisibility.value = 'public';
    };

    const handlePostOverlayClick = (event) => {
      if (event.target === postModalOverlay) closePost();
    };

    const handlePostFileChange = (event) => {
      const file = event?.target?.files?.[0];
      if (!file) return;
      if (uploadHint) uploadHint.textContent = file.name;

      const url = URL.createObjectURL(file);
      if (!postPreview) return;
      postPreview.classList.remove('hidden');

      if (file.type.startsWith('image/')) {
        postPreview.innerHTML = `<img src="${url}" alt="Previsualización" />`;
      } else if (file.type.startsWith('video/')) {
        postPreview.innerHTML = `<video src="${url}" controls></video>`;
      } else {
        postPreview.innerHTML = '';
        postPreview.classList.add('hidden');
      }
    };

    const handlePublishPost = () => {
      alert('Publicación creada (mock). En backend luego la guardamos en DB.');
      closePost();
    };

    openPostModal?.addEventListener('click', openPost);
    closePostModal?.addEventListener('click', closePost);
    cancelPost?.addEventListener('click', closePost);
    postModalOverlay?.addEventListener('click', handlePostOverlayClick);
    postFile?.addEventListener('change', handlePostFileChange);
    publishPost?.addEventListener('click', handlePublishPost);

    return () => {
      btnChangeCover?.removeEventListener('click', handleChangeCover);
      coverFile?.removeEventListener('change', handleCoverFileChange);
      coverMedia?.removeEventListener('mousedown', handleCoverMouseDown);
      window.removeEventListener('mousemove', handleCoverMouseMove);
      window.removeEventListener('mouseup', handleCoverMouseUp);

      btnEditPurposes?.removeEventListener('click', openPurposeModal);
      closePurposeModal?.removeEventListener('click', closePurpose);
      cancelPurposeModal?.removeEventListener('click', closePurpose);
      savePurposeModal?.removeEventListener('click', handleSavePurpose);
      purposeModalOverlay?.removeEventListener('click', handlePurposeOverlayClick);

      openPostModal?.removeEventListener('click', openPost);
      closePostModal?.removeEventListener('click', closePost);
      cancelPost?.removeEventListener('click', closePost);
      postModalOverlay?.removeEventListener('click', handlePostOverlayClick);
      postFile?.removeEventListener('change', handlePostFileChange);
      publishPost?.removeEventListener('click', handlePublishPost);
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
          <button class="icon-btn" id="btnEditPurposes" type="button" title="Editar deseos de propósito">
            Editar propósito
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
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
          <span class="nav-icon">⭐</span>
          <span><strong>5.000.000</strong> estrellas</span>
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

          <article class="panel post">
            <div class="post-head">
              <div>
                <strong>Carlos Jiménez Duarte</strong>
                <span class="post-meta">· hace 2 horas · Público</span>
              </div>
            </div>

            <p class="post-text">
              Las mejores cosas llegan sin ser esperadas. #propósito #constancia #vida
            </p>

            <div class="post-actions">
              <button class="post-btn" type="button">⭐ Estrella</button>
              <button class="post-btn" type="button">💬 Comentar</button>
              <button class="post-btn" type="button">🔁 Compartir</button>
            </div>
          </article>

          <article class="panel post">
            <div class="post-head">
              <div>
                <strong>Carlos Jiménez Duarte</strong>
                <span class="post-meta">· ayer · Público</span>
              </div>
            </div>

            <p class="post-text">
              Hoy estuve desarrollando el mockup de mi red social.
            </p>

            <div class="post-media">
              <img src="assets/post-1.jpg" alt="Post con imagen" />
            </div>

            <div class="post-actions">
              <button class="post-btn" type="button">⭐ Estrella</button>
              <button class="post-btn" type="button">💬 Comentar</button>
              <button class="post-btn" type="button">🔁 Compartir</button>
            </div>
          </article>

          <article class="panel post">
            <div class="post-head">
              <div>
                <strong>Carlos Jiménez Duarte</strong>
                <span class="post-meta">· hace 3 días · Público</span>
              </div>
            </div>

            <p class="post-text">
              Oh, my God, I’m sharing my soda with Lars Ulrich 😄
            </p>

            <div class="post-media">
              <img src="assets/post-2.jpg" alt="Post con imagen" />
            </div>

            <div class="post-actions">
              <button class="post-btn" type="button">⭐ Estrella</button>
              <button class="post-btn" type="button">💬 Comentar</button>
              <button class="post-btn" type="button">🔁 Compartir</button>
            </div>
          </article>

          <article class="panel post">
            <div class="post-head">
              <div>
                <strong>Carlos Jiménez Duarte</strong>
                <span class="post-meta">· hace 1 semana · Público</span>
              </div>
            </div>

            <p class="post-text">
              Los paseos con Willow siempre me relajan.
            </p>

            <div class="post-media">
              <img src="assets/post-3.jpg" alt="Post con imagen" />
            </div>

            <div class="post-actions">
              <button class="post-btn" type="button">⭐ Estrella</button>
              <button class="post-btn" type="button">💬 Comentar</button>
              <button class="post-btn" type="button">🔁 Compartir</button>
            </div>
          </article>
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

<div class="modal-overlay hidden" id="purposeModalOverlay" aria-hidden="true">
  <div class="modal" role="dialog" aria-modal="true" aria-label="Editar deseos de propósito">
    <div class="modal-head">
      <h3>Editar deseos de propósito</h3>
      <button class="modal-close" type="button" id="closePurposeModal">✕</button>
    </div>

    <div class="modal-body">
      <label class="modal-label" for="purposeInput1">Deseo 1</label>
      <input class="modal-input" id="purposeInput1" type="text" />

      <label class="modal-label" for="purposeInput2">Deseo 2</label>
      <input class="modal-input" id="purposeInput2" type="text" />

      <label class="modal-label" for="purposeInput3">Deseo 3</label>
      <input class="modal-input" id="purposeInput3" type="text" />
    </div>

    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelPurposeModal">Cancelar</button>
      <button class="btn btn-primary btn-compact" type="button" id="savePurposeModal">Guardar</button>
    </div>
  </div>
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
