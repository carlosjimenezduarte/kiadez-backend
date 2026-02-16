<script>
  import { onMount } from 'svelte';
  import { initPurposeCoverModule } from '../lib/purposeCover';
  import { logout } from '../lib/logout';

  onMount(() => {
    initPurposeCoverModule();

    // POSTS
    const API = 'http://127.0.0.1:8000';
    const postModalOverlay = document.getElementById('postModalOverlay');
    const openPostModal = document.getElementById('openPostModal');
    const menuPublishBtn = document.getElementById('menuPublishBtn');
    const menuDropdown = document.getElementById('menuDropdown');
    const homeTopbarBtn = document.getElementById('homeTopbarBtn');
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
    const homeAvatarButton = document.getElementById('homeAvatarButton');
    const homeProfileName = document.getElementById('homeProfileName');
    const homeUsernameLink = document.getElementById('homeUsernameLink');
    const homeUsernameValue = document.getElementById('homeUsernameValue');
    const homeUsernameEditBtn = document.getElementById('homeUsernameEditBtn');
    const homeUsernameCooldown = document.getElementById('homeUsernameCooldown');
    const homeUsernameModalOverlay = document.getElementById('homeUsernameModalOverlay');
    const closeHomeUsernameModal = document.getElementById('closeHomeUsernameModal');
    const cancelHomeUsernameModal = document.getElementById('cancelHomeUsernameModal');
    const saveHomeUsernameBtn = document.getElementById('saveHomeUsernameBtn');
    const homeUsernameInput = document.getElementById('homeUsernameInput');
    const homeUsernamePreview = document.getElementById('homeUsernamePreview');
    const homeUsernameModalStatus = document.getElementById('homeUsernameModalStatus');
    const homeUsernameConfirmWrap = document.getElementById('homeUsernameConfirmWrap');
    const homeUsernameConfirmText = document.getElementById('homeUsernameConfirmText');
    const confirmHomeUsernameBtn = document.getElementById('confirmHomeUsernameBtn');
    const cancelHomeUsernameConfirmBtn = document.getElementById('cancelHomeUsernameConfirmBtn');
    const homePublicWishList = document.getElementById('homePublicWishList');
    const homePublicWishCount = document.getElementById('homePublicWishCount');
    const homePublicWishStatus = document.getElementById('homePublicWishStatus');
    const homeFulfilledWishList = document.getElementById('homeFulfilledWishList');
    const homeFulfilledWishCount = document.getElementById('homeFulfilledWishCount');
    const homeFulfilledWishStatus = document.getElementById('homeFulfilledWishStatus');
    const homePrivateWishCount = document.getElementById('homePrivateWishCount');
    const homePrivateWishTotal = document.getElementById('homePrivateWishTotal');
    const homePrivateWishStatus = document.getElementById('homePrivateWishStatus');
    const homeAboutTextValue = document.getElementById('homeAboutTextValue');
    const homeAboutEmptyState = document.getElementById('homeAboutEmptyState');
    const homeAboutEditBtn = document.getElementById('homeAboutEditBtn');
    const homeAboutModalOverlay = document.getElementById('homeAboutModalOverlay');
    const closeHomeAboutModal = document.getElementById('closeHomeAboutModal');
    const cancelHomeAboutModal = document.getElementById('cancelHomeAboutModal');
    const saveHomeAboutBtn = document.getElementById('saveHomeAboutBtn');
    const homeAboutInput = document.getElementById('homeAboutInput');
    const homeAboutWordCounter = document.getElementById('homeAboutWordCounter');
    const homeAboutModalStatus = document.getElementById('homeAboutModalStatus');
    const profilePhotoPostOverlay = document.getElementById('profilePhotoPostModalOverlay');
    const closeProfilePhotoPostModal = document.getElementById('closeProfilePhotoPostModal');
    const cancelProfilePhotoPostModal = document.getElementById('cancelProfilePhotoPostModal');
    const profilePhotoPostImage = document.getElementById('profilePhotoPostImage');
    const profilePhotoPostAuthor = document.getElementById('profilePhotoPostAuthor');
    const profilePhotoPostMeta = document.getElementById('profilePhotoPostMeta');
    const profilePhotoStarPost = document.getElementById('profilePhotoStarPost');
    const profilePhotoCommentPost = document.getElementById('profilePhotoCommentPost');
    const profilePhotoSharePost = document.getElementById('profilePhotoSharePost');
    const profilePhotoPostStatus = document.getElementById('profilePhotoPostStatus');
    const homeAvatarImages = Array.from(document.querySelectorAll('[data-home-avatar]'));

    let selectedFile = null;
    let selectedFileURL = null;
    let selectedCommentPostId = null;
    let selectedDeletePostId = null;
    let selectedReportPostId = null;
    let currentFeedPosts = [];
    let profilePhotoMediaId = null;
    let profilePhotoPost = null;
    let profilePhotoPostId = null;
    let currentAboutDisplayName = (homeProfileName?.textContent || 'Usuario Kiadez').trim();
    let currentUsername = '';
    let pendingUsername = '';

    const HOME_ABOUT_MAX_WORDS = 50;
    const USERNAME_MIN_LENGTH = 4;
    const USERNAME_MAX_LENGTH = 30;
    const USERNAME_PATTERN = /^[a-z0-9._]{4,30}$/;
    const PROFILE_PHOTO_POST_STORAGE_KEY = 'home_profile_photo_post_id';
    const PROFILE_PHOTO_POST_TEXT = 'Actualice mi foto de perfil.';
    const DEFAULT_AVATAR_SRC = '/assets/avatar-default.jpg';

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

    const setHomeAboutModalStatus = (message, isError = false) => {
      if (!homeAboutModalStatus) return;
      homeAboutModalStatus.textContent = message || '';
      homeAboutModalStatus.classList.toggle('is-error', Boolean(isError));
    };

    const setProfilePhotoPostStatus = (message, isError = false) => {
      if (!profilePhotoPostStatus) return;
      profilePhotoPostStatus.textContent = message || '';
      profilePhotoPostStatus.classList.toggle('is-error', Boolean(isError));
    };

    const setHomeUsernameModalStatus = (message, isError = false) => {
      if (!homeUsernameModalStatus) return;
      homeUsernameModalStatus.textContent = message || '';
      homeUsernameModalStatus.classList.toggle('is-error', Boolean(isError));
    };

    const setHomePublicWishStatus = (message, isError = false) => {
      if (!homePublicWishStatus) return;
      homePublicWishStatus.textContent = message || '';
      homePublicWishStatus.classList.toggle('is-error', Boolean(isError));
    };

    const setHomeFulfilledWishStatus = (message, isError = false) => {
      if (!homeFulfilledWishStatus) return;
      homeFulfilledWishStatus.textContent = message || '';
      homeFulfilledWishStatus.classList.toggle('is-error', Boolean(isError));
    };

    const setHomePrivateWishStatus = (message, isError = false) => {
      if (!homePrivateWishStatus) return;
      homePrivateWishStatus.textContent = message || '';
      homePrivateWishStatus.classList.toggle('is-error', Boolean(isError));
    };

    const countWords = (value) => {
      if (!value) return 0;
      return value
        .trim()
        .split(/\s+/)
        .filter(Boolean).length;
    };

    const normalizeUsername = (value) => {
      let normalized = (value || '').trim().toLowerCase();
      while (normalized.startsWith('@')) normalized = normalized.slice(1);
      return normalized;
    };

    const formatIsoDate = (isoDate) => {
      if (!isoDate) return '';
      const dateValue = new Date(isoDate);
      if (Number.isNaN(dateValue.getTime())) return '';
      return dateValue.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    };

    const setHomeCanonicalLinks = (profilePath) => {
      const normalizedPath = profilePath || '/home_user.html';
      document.querySelectorAll('a[data-home-link="true"]').forEach((link) => {
        link.href = normalizedPath;
      });

      if (window.location.pathname !== '/home_user.html') return;
      const currentUrl = new URL(window.location.href);
      const targetUrl = new URL(normalizedPath, window.location.origin);
      if (currentUrl.search !== targetUrl.search) {
        window.history.replaceState({}, '', `${currentUrl.pathname}${targetUrl.search}`);
      }
    };

    const setHomeAvatarSource = (url) => {
      const avatarUrl = (url || '').trim() || DEFAULT_AVATAR_SRC;
      homeAvatarImages.forEach((img) => {
        img.src = avatarUrl;
      });
      if (profilePhotoPostImage && !profilePhotoPost) {
        profilePhotoPostImage.src = avatarUrl;
      }
    };

    const setProfilePhotoPostId = (postId) => {
      const normalized = Number(postId);
      profilePhotoPostId = Number.isFinite(normalized) && normalized > 0 ? normalized : null;
      if (profilePhotoPostId) {
        localStorage.setItem(PROFILE_PHOTO_POST_STORAGE_KEY, String(profilePhotoPostId));
      } else {
        localStorage.removeItem(PROFILE_PHOTO_POST_STORAGE_KEY);
      }
    };

    const updateHomeAboutWordCounter = () => {
      if (!homeAboutWordCounter) return;
      const words = countWords(homeAboutInput?.value || '');
      homeAboutWordCounter.textContent = `${words} / ${HOME_ABOUT_MAX_WORDS} palabras`;
      homeAboutWordCounter.classList.toggle('is-error', words > HOME_ABOUT_MAX_WORDS);
    };

    setProfilePhotoPostId(localStorage.getItem(PROFILE_PHOTO_POST_STORAGE_KEY));

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

    const applyHomeAbout = (about) => {
      const displayName = (about?.display_name || '').trim() || (homeProfileName?.textContent || '').trim() || 'Usuario Kiadez';
      const aboutText = (about?.about_text || '').trim();
      currentAboutDisplayName = displayName;
      if (homeProfileName) homeProfileName.textContent = displayName;
      if (profilePhotoPostAuthor) profilePhotoPostAuthor.textContent = displayName;

      if (homeAboutTextValue) {
        homeAboutTextValue.textContent = aboutText;
        homeAboutTextValue.classList.toggle('hidden', !aboutText);
      }
      if (homeAboutEmptyState) {
        homeAboutEmptyState.classList.toggle('hidden', Boolean(aboutText));
      }
    };

    const loadHomeAbout = async () => {
      try {
        const res = await apiFetch('/biography/about');
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo cargar "Acerca de mi".');
        applyHomeAbout(data);
      } catch (error) {
        console.error(error);
      }
    };

    const openHomeAboutModalPanel = () => {
      if (homeAboutInput) {
        homeAboutInput.value = (homeAboutTextValue?.textContent || '').trim();
      }
      updateHomeAboutWordCounter();
      setHomeAboutModalStatus('');
      homeAboutModalOverlay?.classList.remove('hidden');
      homeAboutModalOverlay?.setAttribute('aria-hidden', 'false');
    };

    const closeHomeAboutModalPanel = () => {
      homeAboutModalOverlay?.classList.add('hidden');
      homeAboutModalOverlay?.setAttribute('aria-hidden', 'true');
      setHomeAboutModalStatus('');
    };

    const renderProfilePhotoPost = (post) => {
      profilePhotoPost = post || null;
      if (profilePhotoPostImage) {
        const imageUrl = post?.media_url || homeAvatarImages[0]?.src || DEFAULT_AVATAR_SRC;
        profilePhotoPostImage.src = imageUrl;
      }
      if (profilePhotoPostMeta) {
        if (!post) {
          profilePhotoPostMeta.textContent = '· Publicacion pendiente';
        } else {
          profilePhotoPostMeta.textContent = `· ${relativeTime(post.created_at)} · ${post.visibility === 'private' ? 'Privado' : 'Publico'}`;
        }
      }
      if (profilePhotoStarPost) {
        const starredByMe = Boolean(post?.starred_by_me);
        const starCount = Number(post?.star_count || 0);
        profilePhotoStarPost.disabled = !post || starredByMe;
        profilePhotoStarPost.textContent = starredByMe
          ? `⭐ Estrella donada (${starCount})`
          : `⭐ Donar estrella (${starCount})`;
      }
      if (profilePhotoCommentPost) {
        profilePhotoCommentPost.disabled = !post;
        profilePhotoCommentPost.textContent = `💬 Comentar (${Number(post?.comment_count || 0)})`;
      }
      if (profilePhotoSharePost) {
        profilePhotoSharePost.disabled = !post;
        profilePhotoSharePost.textContent = `🔁 Compartir (${Number(post?.share_count || 0)})`;
      }
      setProfilePhotoPostStatus('');
    };

    const syncProfilePhotoPostFromFeed = () => {
      if (!Array.isArray(currentFeedPosts) || currentFeedPosts.length === 0) {
        renderProfilePhotoPost(null);
        return;
      }

      let foundPost = null;
      if (profilePhotoPostId) {
        foundPost = currentFeedPosts.find((post) => post.id === profilePhotoPostId) || null;
      }
      if (!foundPost && profilePhotoMediaId) {
        foundPost = currentFeedPosts.find(
          (post) => post.is_mine && post.media_id === profilePhotoMediaId && post.media_kind === 'image'
        ) || null;
        if (foundPost) setProfilePhotoPostId(foundPost.id);
      }
      if (!foundPost && profilePhotoPostId) {
        setProfilePhotoPostId(null);
      }
      renderProfilePhotoPost(foundPost);
    };

    const loadProfilePhoto = async () => {
      try {
        const res = await apiFetch('/media/profile-photo');
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo cargar la foto de perfil.');
        profilePhotoMediaId = data.media_id || null;
        setHomeAvatarSource(data.url || DEFAULT_AVATAR_SRC);
      } catch (error) {
        console.error(error);
      }
    };

    const applyUsernameState = (state) => {
      const username = normalizeUsername(state?.username || '');
      currentUsername = username;
      const hasUsername = Boolean(username);
      const profilePath = state?.profile_url || (hasUsername ? `/home_user.html?u=${encodeURIComponent(username)}` : '/home_user.html');
      if (homeUsernameValue) homeUsernameValue.textContent = hasUsername ? `@${username}` : '@elige-tu-usuario';
      if (homeUsernameLink) {
        homeUsernameLink.href = profilePath;
        homeUsernameLink.classList.toggle('is-empty', !hasUsername);
      }
      if (homeUsernameEditBtn) {
        const canUpdate = Boolean(state?.can_update);
        homeUsernameEditBtn.disabled = !canUpdate;
        homeUsernameEditBtn.classList.toggle('is-disabled', !canUpdate);
      }
      if (homeUsernameCooldown) {
        const canUpdate = Boolean(state?.can_update);
        if (canUpdate) {
          homeUsernameCooldown.textContent = 'Puedes cambiar tu nombre de usuario ahora.';
        } else if (state?.cooldown_until) {
          homeUsernameCooldown.textContent = `Podrás cambiarlo nuevamente el ${formatIsoDate(state.cooldown_until)}.`;
        } else {
          homeUsernameCooldown.textContent = 'Nombre de usuario bloqueado temporalmente.';
        }
      }
      setHomeCanonicalLinks(profilePath);
    };

    const loadUsernameState = async () => {
      try {
        const res = await apiFetch('/auth/username');
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo cargar tu nombre de usuario.');
        applyUsernameState(data);
      } catch (error) {
        console.error(error);
      }
    };

    const updateUsernamePreview = () => {
      if (!homeUsernamePreview) return;
      const normalized = normalizeUsername(homeUsernameInput?.value || '');
      homeUsernamePreview.textContent = normalized
        ? `Enlace: ${window.location.origin}/home_user.html?u=${normalized}`
        : 'Enlace: /home_user.html';
    };

    const openHomeUsernameModalPanel = () => {
      if (homeUsernameInput) homeUsernameInput.value = currentUsername;
      pendingUsername = '';
      setHomeUsernameModalStatus('');
      homeUsernameConfirmWrap?.classList.add('hidden');
      updateUsernamePreview();
      homeUsernameModalOverlay?.classList.remove('hidden');
      homeUsernameModalOverlay?.setAttribute('aria-hidden', 'false');
    };

    const closeHomeUsernameModalPanel = () => {
      homeUsernameModalOverlay?.classList.add('hidden');
      homeUsernameModalOverlay?.setAttribute('aria-hidden', 'true');
      pendingUsername = '';
      setHomeUsernameModalStatus('');
      homeUsernameConfirmWrap?.classList.add('hidden');
    };

    const validateUsernameInput = (username) => {
      if (!username) return 'Digita un nombre de usuario.';
      if (username.length < USERNAME_MIN_LENGTH || username.length > USERNAME_MAX_LENGTH) {
        return `El nombre de usuario debe tener entre ${USERNAME_MIN_LENGTH} y ${USERNAME_MAX_LENGTH} caracteres.`;
      }
      if (!USERNAME_PATTERN.test(username)) {
        return 'Usa solo letras minúsculas, números, punto o guión bajo.';
      }
      return '';
    };

    const handleHomeUsernameOverlayClick = (event) => {
      if (event.target === homeUsernameModalOverlay) closeHomeUsernameModalPanel();
    };

    const handleHomeUsernameInput = () => {
      if (!homeUsernameInput) return;
      homeUsernameInput.value = normalizeUsername(homeUsernameInput.value);
      updateUsernamePreview();
      setHomeUsernameModalStatus('');
      homeUsernameConfirmWrap?.classList.add('hidden');
      pendingUsername = '';
    };

    const handlePrepareUsernameChange = async () => {
      const candidate = normalizeUsername(homeUsernameInput?.value || '');
      if (homeUsernameInput) homeUsernameInput.value = candidate;
      const validationError = validateUsernameInput(candidate);
      if (validationError) {
        setHomeUsernameModalStatus(validationError, true);
        return;
      }

      const oldLabel = saveHomeUsernameBtn?.textContent || 'Aceptar';
      if (saveHomeUsernameBtn) {
        saveHomeUsernameBtn.disabled = true;
        saveHomeUsernameBtn.textContent = 'Validando...';
      }

      try {
        const res = await apiFetch(`/auth/username/check?username=${encodeURIComponent(candidate)}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo validar el nombre de usuario.');
        if (!data.available) {
          setHomeUsernameModalStatus(data.detail || 'Ese nombre de usuario no está disponible.', true);
          homeUsernameConfirmWrap?.classList.add('hidden');
          pendingUsername = '';
          return;
        }

        pendingUsername = candidate;
        if (homeUsernameConfirmText) {
          homeUsernameConfirmText.textContent = `¿Estás seguro de que deseas este nombre de usuario: @${candidate}?`;
        }
        homeUsernameConfirmWrap?.classList.remove('hidden');
        setHomeUsernameModalStatus('');
      } catch (error) {
        setHomeUsernameModalStatus(error.message || 'No se pudo validar el nombre de usuario.', true);
      } finally {
        if (saveHomeUsernameBtn) {
          saveHomeUsernameBtn.disabled = false;
          saveHomeUsernameBtn.textContent = oldLabel;
        }
      }
    };

    const handleCancelUsernameConfirmation = () => {
      pendingUsername = '';
      homeUsernameConfirmWrap?.classList.add('hidden');
      setHomeUsernameModalStatus('');
    };

    const handleConfirmUsernameChange = async () => {
      if (!pendingUsername) {
        setHomeUsernameModalStatus('Primero valida un nombre de usuario disponible.', true);
        return;
      }

      const oldLabel = confirmHomeUsernameBtn?.textContent || 'Sí';
      if (confirmHomeUsernameBtn) {
        confirmHomeUsernameBtn.disabled = true;
        confirmHomeUsernameBtn.textContent = 'Guardando...';
      }

      try {
        const res = await apiFetch('/auth/username', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: pendingUsername })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo actualizar el nombre de usuario.');
        applyUsernameState(data.state || null);
        closeHomeUsernameModalPanel();
        setPostsStatus(`Tu nombre de usuario ahora es @${data?.state?.username || pendingUsername}.`);
      } catch (error) {
        setHomeUsernameModalStatus(error.message || 'No se pudo actualizar el nombre de usuario.', true);
      } finally {
        if (confirmHomeUsernameBtn) {
          confirmHomeUsernameBtn.disabled = false;
          confirmHomeUsernameBtn.textContent = oldLabel;
        }
      }
    };

    const renderHomePublicWishes = (items, activeCount = 0, activeLimit = 50) => {
      if (!homePublicWishList) return;
      const wishes = Array.isArray(items) ? [...items] : [];
      wishes.sort((a, b) => {
        const aTs = Date.parse(a?.created_at || '');
        const bTs = Date.parse(b?.created_at || '');
        const aSafe = Number.isNaN(aTs) ? 0 : aTs;
        const bSafe = Number.isNaN(bTs) ? 0 : bTs;
        return bSafe - aSafe;
      });

      const topSeven = wishes.slice(0, 7);
      if (homePublicWishCount) {
        const safeActiveCount = Math.max(0, Number(activeCount || 0));
        const safeActiveLimit = Math.max(1, Number(activeLimit || 50));
        homePublicWishCount.textContent = `${safeActiveCount} / ${safeActiveLimit}`;
      }

      if (topSeven.length === 0) {
        homePublicWishList.innerHTML = `
          <li class="wish-item wish-item-home-public wish-item-empty">
            <span class="wish-dot"></span>
            <span class="wish-item-label">Aún no tienes deseos públicos activos.</span>
          </li>
        `;
        return;
      }

      homePublicWishList.innerHTML = topSeven
        .map((wish) => {
          const wishText = escapeHtml(wish?.wish_text || 'Deseo sin descripción');
          const mediaUrl = (wish?.media_url || '').trim();
          const mediaHtml = mediaUrl
            ? `<img class="wish-item-thumb" src="${escapeHtml(mediaUrl)}" alt="Imagen del deseo público" loading="lazy" />`
            : '<span class="wish-dot"></span>';

          return `
            <li class="wish-item wish-item-home-public">
              ${mediaHtml}
              <span class="wish-item-label">${wishText}</span>
            </li>
          `;
        })
        .join('');
    };

    const loadHomePublicWishes = async () => {
      try {
        const res = await apiFetch('/public-wishes/personal');
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudieron cargar tus deseos públicos.');
        renderHomePublicWishes(data?.items || [], data?.active_count || 0, data?.active_limit || 50);
        setHomePublicWishStatus('');
      } catch (error) {
        renderHomePublicWishes([], 0, 50);
        setHomePublicWishStatus(error.message || 'No se pudieron cargar tus deseos públicos.', true);
      }
    };

    const renderHomeFulfilledWishes = (items, total = 0) => {
      if (!homeFulfilledWishList) return;
      const wishes = Array.isArray(items) ? [...items] : [];
      wishes.sort((a, b) => {
        const aTs = Date.parse(a?.fulfilled_at || a?.updated_at || a?.created_at || '');
        const bTs = Date.parse(b?.fulfilled_at || b?.updated_at || b?.created_at || '');
        const aSafe = Number.isNaN(aTs) ? 0 : aTs;
        const bSafe = Number.isNaN(bTs) ? 0 : bTs;
        if (bSafe !== aSafe) return bSafe - aSafe;
        return Number(b?.id || 0) - Number(a?.id || 0);
      });

      const topSeven = wishes.slice(0, 7);
      if (homeFulfilledWishCount) {
        const safeTotal = Math.max(0, Number(total || wishes.length));
        homeFulfilledWishCount.textContent = safeTotal > 7
          ? `${topSeven.length} de ${safeTotal}`
          : `${topSeven.length} recientes`;
      }

      if (topSeven.length === 0) {
        homeFulfilledWishList.innerHTML = `
          <li class="wish-item wish-item-home-public wish-item-empty">
            <span class="wish-dot"></span>
            <span class="wish-item-label">Aún no tienes deseos cumplidos.</span>
          </li>
        `;
        return;
      }

      homeFulfilledWishList.innerHTML = topSeven
        .map((wish) => {
          const wishText = escapeHtml(wish?.wish_text || 'Deseo cumplido sin descripción');
          const mediaUrl = (wish?.fulfilled_evidence_media_url || wish?.media_url || '').trim();
          const mediaHtml = mediaUrl
            ? `<img class="wish-item-thumb" src="${escapeHtml(mediaUrl)}" alt="Imagen del deseo cumplido" loading="lazy" />`
            : '<span class="wish-dot"></span>';

          return `
            <li class="wish-item wish-item-home-public">
              ${mediaHtml}
              <span class="wish-item-label">${wishText}</span>
            </li>
          `;
        })
        .join('');
    };

    const loadHomeFulfilledWishes = async () => {
      try {
        const res = await apiFetch('/public-wishes/personal/fulfilled?limit=7&offset=0');
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudieron cargar tus deseos cumplidos.');
        renderHomeFulfilledWishes(data?.items || [], data?.total || 0);
        setHomeFulfilledWishStatus('');
      } catch (error) {
        renderHomeFulfilledWishes([], 0);
        setHomeFulfilledWishStatus(error.message || 'No se pudieron cargar tus deseos cumplidos.', true);
      }
    };

    const renderHomePrivateWishSummary = (activeCount = 0, activeLimit = 50) => {
      const safeActiveCount = Math.max(0, Number(activeCount || 0));
      const safeActiveLimit = Math.max(1, Number(activeLimit || 50));
      const summary = `${safeActiveCount} / ${safeActiveLimit}`;

      if (homePrivateWishCount) {
        homePrivateWishCount.textContent = summary;
      }
      if (homePrivateWishTotal) {
        homePrivateWishTotal.textContent = summary;
      }
    };

    const loadHomePrivateWishes = async () => {
      try {
        const res = await apiFetch('/private-wishes/personal');
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudieron cargar tus deseos privados.');
        renderHomePrivateWishSummary(data?.active_count || 0, data?.active_limit || 50);
        setHomePrivateWishStatus('');
      } catch (error) {
        renderHomePrivateWishSummary(0, 50);
        setHomePrivateWishStatus(error.message || 'No se pudieron cargar tus deseos privados.', true);
      }
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
        currentFeedPosts = Array.isArray(data) ? data : [];
        renderPosts(data);
        syncProfilePhotoPostFromFeed();
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

    const handleMenuPublishClick = () => {
      openPost();
      menuDropdown?.removeAttribute('open');
    };

    const handleTopbarHomeClick = () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
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

    const uploadMediaFile = async (file, visibilityValue) => {
      if (!file) return null;
      const presignRes = await apiFetch('/media/presign/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          content_type: file.type,
          size_bytes: file.size,
          visibility: visibilityValue
        })
      });
      const presignData = await presignRes.json();
      if (!presignRes.ok) {
        throw new Error(presignData.detail || 'No se pudo preparar la carga de media.');
      }

      const uploadRes = await fetch(presignData.upload_url, {
        method: 'PUT',
        headers: presignData.required_headers || { 'Content-Type': file.type },
        body: file
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

      const mediaKind = file.type.startsWith('video/') ? 'video' : 'image';
      return { media_id: presignData.media_id, media_kind: mediaKind };
    };

    const uploadMediaIfNeeded = async (visibilityValue) => {
      if (!selectedFile) return null;
      return uploadMediaFile(selectedFile, visibilityValue);
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

    const createPost = async ({ text, visibility = 'public', media_id = null, media_kind = null }) => {
      const res = await apiFetch('/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text || null,
          visibility: (visibility || 'public').toLowerCase(),
          media_id: media_id ?? null,
          media_kind: media_kind ?? null
        })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'No se pudo crear la publicacion.');
      }
      return data;
    };

    const ensureProfilePhotoPost = async () => {
      if (!profilePhotoMediaId) {
        renderProfilePhotoPost(null);
        setProfilePhotoPostStatus('Primero debes cargar una foto de perfil.', true);
        return false;
      }

      if (!Array.isArray(currentFeedPosts) || currentFeedPosts.length === 0) {
        await loadFeed();
      } else {
        syncProfilePhotoPostFromFeed();
      }
      if (profilePhotoPost?.id) return true;

      const created = await createPost({
        text: PROFILE_PHOTO_POST_TEXT,
        visibility: 'public',
        media_id: profilePhotoMediaId,
        media_kind: 'image'
      });
      setProfilePhotoPostId(created.id);
      await loadFeed();
      syncProfilePhotoPostFromFeed();
      return Boolean(profilePhotoPost?.id);
    };

    const openProfilePhotoPost = async () => {
      profilePhotoPostOverlay?.classList.remove('hidden');
      profilePhotoPostOverlay?.setAttribute('aria-hidden', 'false');
      try {
        await ensureProfilePhotoPost();
      } catch (error) {
        setProfilePhotoPostStatus(error.message || 'No se pudo abrir la publicacion de la foto de perfil.', true);
      }
    };

    const closeProfilePhotoPost = () => {
      profilePhotoPostOverlay?.classList.add('hidden');
      profilePhotoPostOverlay?.setAttribute('aria-hidden', 'true');
      setProfilePhotoPostStatus('');
    };

    const handleProfilePhotoPostOverlayClick = (event) => {
      if (event.target === profilePhotoPostOverlay) closeProfilePhotoPost();
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

    const openCommentsForPost = async (postId, title = null) => {
      selectedCommentPostId = postId;
      if (commentsTitle) {
        commentsTitle.textContent = title || `Comentarios de la publicacion #${postId}`;
      }
      commentsOverlay?.classList.remove('hidden');
      commentsOverlay?.setAttribute('aria-hidden', 'false');
      await loadComments();
    };

    const donateStarToPost = async (postId, setStatus = setPostsStatus) => {
      try {
        const res = await apiFetch(`/posts/${postId}/stars`, { method: 'POST' });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo donar la estrella.');
        setStatus('Estrella donada. Esta accion es irreversible.');
        await Promise.all([loadFeed(), loadMyStats()]);
        syncProfilePhotoPostFromFeed();
      } catch (error) {
        setStatus(error.message || 'No se pudo donar la estrella.', true);
      }
    };

    const sharePost = async (postId, setStatus = setPostsStatus) => {
      try {
        await apiFetch(`/posts/${postId}/share`, { method: 'POST' });
        const shareUrlObject = new URL('/home_user.html', window.location.origin);
        if (currentUsername) {
          shareUrlObject.searchParams.set('u', currentUsername);
        }
        shareUrlObject.searchParams.set('post', String(postId));
        const shareUrl = shareUrlObject.toString();
        if (navigator.share) {
          await navigator.share({ title: 'Kiadez', text: 'Mira esta publicacion', url: shareUrl });
        } else if (navigator.clipboard?.writeText) {
          await navigator.clipboard.writeText(shareUrl);
        }
        setStatus('Publicacion compartida.');
        await loadFeed();
        syncProfilePhotoPostFromFeed();
      } catch (error) {
        setStatus(error.message || 'No se pudo compartir.', true);
      }
    };

    const handleOpenHomeAboutModal = () => {
      openHomeAboutModalPanel();
    };

    const handleHomeAboutOverlayClick = (event) => {
      if (event.target === homeAboutModalOverlay) closeHomeAboutModalPanel();
    };

    const handleSaveHomeAbout = async () => {
      const aboutText = (homeAboutInput?.value || '').trim();
      const wordCount = countWords(aboutText);
      if (wordCount > HOME_ABOUT_MAX_WORDS) {
        setHomeAboutModalStatus(`Puedes escribir maximo ${HOME_ABOUT_MAX_WORDS} palabras.`, true);
        return;
      }

      const oldLabel = saveHomeAboutBtn?.textContent || 'Guardar';
      if (saveHomeAboutBtn) {
        saveHomeAboutBtn.disabled = true;
        saveHomeAboutBtn.textContent = 'Guardando...';
      }

      try {
        const res = await apiFetch('/biography/about', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            display_name: (currentAboutDisplayName || homeProfileName?.textContent || 'Usuario Kiadez').trim(),
            about_text: aboutText || null
          })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo guardar "Acerca de mi".');
        applyHomeAbout(data);
        closeHomeAboutModalPanel();
        setPostsStatus('"Acerca de mi" actualizado.');
      } catch (error) {
        setHomeAboutModalStatus(error.message || 'No se pudo guardar "Acerca de mi".', true);
      } finally {
        if (saveHomeAboutBtn) {
          saveHomeAboutBtn.disabled = false;
          saveHomeAboutBtn.textContent = oldLabel;
        }
      }
    };

    const handleProfilePhotoStar = async () => {
      if (!profilePhotoPost?.id) return;
      await donateStarToPost(profilePhotoPost.id, setProfilePhotoPostStatus);
    };

    const handleProfilePhotoComment = async () => {
      if (!profilePhotoPost?.id) return;
      await openCommentsForPost(profilePhotoPost.id, 'Comentarios de tu foto de perfil');
    };

    const handleProfilePhotoShare = async () => {
      if (!profilePhotoPost?.id) return;
      await sharePost(profilePhotoPost.id, setProfilePhotoPostStatus);
    };

    const handlePostsClick = async (event) => {
      const button = event.target.closest('[data-action][data-post-id]');
      if (!button) return;
      const action = button.dataset.action;
      const postId = Number(button.dataset.postId);
      if (!postId) return;

      if (action === 'star-post') {
        await donateStarToPost(postId);
        return;
      }

      if (action === 'comment-post') {
        await openCommentsForPost(postId);
        return;
      }

      if (action === 'share-post') {
        await sharePost(postId);
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
    menuPublishBtn?.addEventListener('click', handleMenuPublishClick);
    homeTopbarBtn?.addEventListener('click', handleTopbarHomeClick);
    homeAvatarButton?.addEventListener('click', openProfilePhotoPost);
    homeUsernameEditBtn?.addEventListener('click', openHomeUsernameModalPanel);
    closeHomeUsernameModal?.addEventListener('click', closeHomeUsernameModalPanel);
    cancelHomeUsernameModal?.addEventListener('click', closeHomeUsernameModalPanel);
    saveHomeUsernameBtn?.addEventListener('click', handlePrepareUsernameChange);
    homeUsernameInput?.addEventListener('input', handleHomeUsernameInput);
    homeUsernameModalOverlay?.addEventListener('click', handleHomeUsernameOverlayClick);
    confirmHomeUsernameBtn?.addEventListener('click', handleConfirmUsernameChange);
    cancelHomeUsernameConfirmBtn?.addEventListener('click', handleCancelUsernameConfirmation);
    closeProfilePhotoPostModal?.addEventListener('click', closeProfilePhotoPost);
    cancelProfilePhotoPostModal?.addEventListener('click', closeProfilePhotoPost);
    profilePhotoPostOverlay?.addEventListener('click', handleProfilePhotoPostOverlayClick);
    profilePhotoStarPost?.addEventListener('click', handleProfilePhotoStar);
    profilePhotoCommentPost?.addEventListener('click', handleProfilePhotoComment);
    profilePhotoSharePost?.addEventListener('click', handleProfilePhotoShare);
    homeAboutEditBtn?.addEventListener('click', handleOpenHomeAboutModal);
    closeHomeAboutModal?.addEventListener('click', closeHomeAboutModalPanel);
    cancelHomeAboutModal?.addEventListener('click', closeHomeAboutModalPanel);
    saveHomeAboutBtn?.addEventListener('click', handleSaveHomeAbout);
    homeAboutInput?.addEventListener('input', updateHomeAboutWordCounter);
    homeAboutModalOverlay?.addEventListener('click', handleHomeAboutOverlayClick);
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

    void (async () => {
      await Promise.all([
        loadHomeAbout(),
        loadProfilePhoto(),
        loadUsernameState(),
        loadHomePublicWishes(),
        loadHomeFulfilledWishes(),
        loadHomePrivateWishes(),
        loadMyStats()
      ]);
      await loadFeed();
      syncProfilePhotoPostFromFeed();
    })();

    return () => {
      if (selectedFileURL) URL.revokeObjectURL(selectedFileURL);

      openPostModal?.removeEventListener('click', openPost);
      menuPublishBtn?.removeEventListener('click', handleMenuPublishClick);
      homeTopbarBtn?.removeEventListener('click', handleTopbarHomeClick);
      homeAvatarButton?.removeEventListener('click', openProfilePhotoPost);
      homeUsernameEditBtn?.removeEventListener('click', openHomeUsernameModalPanel);
      closeHomeUsernameModal?.removeEventListener('click', closeHomeUsernameModalPanel);
      cancelHomeUsernameModal?.removeEventListener('click', closeHomeUsernameModalPanel);
      saveHomeUsernameBtn?.removeEventListener('click', handlePrepareUsernameChange);
      homeUsernameInput?.removeEventListener('input', handleHomeUsernameInput);
      homeUsernameModalOverlay?.removeEventListener('click', handleHomeUsernameOverlayClick);
      confirmHomeUsernameBtn?.removeEventListener('click', handleConfirmUsernameChange);
      cancelHomeUsernameConfirmBtn?.removeEventListener('click', handleCancelUsernameConfirmation);
      closeProfilePhotoPostModal?.removeEventListener('click', closeProfilePhotoPost);
      cancelProfilePhotoPostModal?.removeEventListener('click', closeProfilePhotoPost);
      profilePhotoPostOverlay?.removeEventListener('click', handleProfilePhotoPostOverlayClick);
      profilePhotoStarPost?.removeEventListener('click', handleProfilePhotoStar);
      profilePhotoCommentPost?.removeEventListener('click', handleProfilePhotoComment);
      profilePhotoSharePost?.removeEventListener('click', handleProfilePhotoShare);
      homeAboutEditBtn?.removeEventListener('click', handleOpenHomeAboutModal);
      closeHomeAboutModal?.removeEventListener('click', closeHomeAboutModalPanel);
      cancelHomeAboutModal?.removeEventListener('click', closeHomeAboutModalPanel);
      saveHomeAboutBtn?.removeEventListener('click', handleSaveHomeAbout);
      homeAboutInput?.removeEventListener('input', updateHomeAboutWordCounter);
      homeAboutModalOverlay?.removeEventListener('click', handleHomeAboutOverlayClick);
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
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input type="search" placeholder="Buscar en Kiadez" aria-label="Buscar" />
      </form>
    </div>

    <div class="feed-topbar-zone feed-topbar-center">
      <button class="topbar-btn is-active" id="homeTopbarBtn" type="button">🏠 Home</button>
      <a class="topbar-btn" href="/gallery.html">🖼️ Galería</a>
      <a class="topbar-btn" href="/my-public-whishes.html">🌐 Deseos públicos</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 Deseos privados</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html">✅ Deseos cumplidos</a>
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown" id="profileDropdown">
        <summary class="topbar-avatar-btn" aria-label="Perfil del usuario">
          <img src="/assets/avatar-default.jpg" alt="Perfil de Carlos Jiménez Duarte" data-home-avatar />
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/privacy-and-settings.html" role="menuitem">Configuración y privacidad</a>
          <button type="button" role="menuitem" on:click={logout}>Cerrar sesión</button>
        </div>
      </details>

      <button class="topbar-icon" type="button" aria-label="Notificaciones">
        🔔
        <span class="topbar-badge">3</span>
      </button>

      <details class="topbar-dropdown" id="menuDropdown">
        <summary class="topbar-menu-btn" aria-label="Abrir menú">
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">Menú</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <button class="dropdown-action" id="menuPublishBtn" type="button" role="menuitem">
            Publicar
          </button>
          <a href="/home_user.html" role="menuitem" data-home-link="true">Mi Home</a>
          <a href="/achievements.html" role="menuitem">Logros recientes</a>
          <a href="/gallery.html" role="menuitem">Galería</a>
          <a href="/calendar.html" role="menuitem">Calendario</a>
          <a href="/my-biography.html" role="menuitem">Mi Biografía</a>
        </div>
      </details>
    </div>
  </header>

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
        <a class="nav-pill" href="/home_user.html" title="Home" data-home-link="true">Home</a>
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
              <button class="profile-avatar-btn" id="homeAvatarButton" type="button" title="Ver foto de perfil como publicación">
                <img class="avatar profile-avatar-image" src="/assets/avatar-default.jpg" alt="Foto de perfil" data-home-avatar />
              </button>
              <div class="profile-meta">
                <h2 class="profile-name" id="homeProfileName">Carlos Jiménez Duarte</h2>
                <p class="profile-rank">Rango 2 · Aprendiz</p>
                <div class="home-username-row">
                  <a class="home-username-link is-empty" id="homeUsernameLink" href="/home_user.html" data-home-link="true">
                    <span id="homeUsernameValue">@elige-tu-usuario</span>
                  </a>
                  <button class="infobox-edit-btn home-username-edit-btn" id="homeUsernameEditBtn" type="button" title="Modificar nombre de usuario">
                    <img src="/css/icons/iconedit.webp" alt="Editar usuario" />
                  </button>
                </div>
                <p class="home-username-cooldown" id="homeUsernameCooldown"></p>
              </div>
            </div>
          </article>

          <article class="panel">
            <div class="panel-head home-about-head">
              <h3 class="panel-title">Acerca de mí</h3>
              <button class="infobox-edit-btn home-about-edit-btn" id="homeAboutEditBtn" type="button" title="Modificar acerca de mí">
                <img src="/css/icons/iconedit.webp" alt="Editar" />
              </button>
            </div>
            <p class="panel-muted hidden" id="homeAboutEmptyState">
              Cuéntale a la comunidad quién eres en pocas palabras.
            </p>
            <p class="panel-text home-about-text" id="homeAboutTextValue">
              Aficionado a los videojuegos, los libros, los perros y la buena comida.
              Mi filosofía es que: la sabiduría suprema consiste en tener sueños lo suficientemente grandes
              para no perderlos de vista mientras se persiguen.
            </p>
          </article>

          <article class="panel">
            <div class="panel-head">
              <h3 class="panel-title">Mis deseos cumplidos</h3>
              <span class="panel-badge" id="homeFulfilledWishCount">0 recientes</span>
            </div>

            <ul class="wish-list" id="homeFulfilledWishList">
              <li class="wish-item wish-item-home-public wish-item-empty">
                <span class="wish-dot"></span>
                <span class="wish-item-label">Cargando tus deseos cumplidos...</span>
              </li>
            </ul>
            <p class="home-public-wish-status" id="homeFulfilledWishStatus" aria-live="polite"></p>

            <a href="/my-fulfilled-whises.html" class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn">Ver más</a>
          </article>

          <article class="panel">
            <div class="panel-head">
              <h3 class="panel-title">Mis deseos públicos</h3>
              <span class="panel-badge" id="homePublicWishCount">0 / 50</span>
            </div>

            <ul class="wish-list" id="homePublicWishList">
              <li class="wish-item wish-item-home-public wish-item-empty">
                <span class="wish-dot"></span>
                <span class="wish-item-label">Cargando tus deseos públicos...</span>
              </li>
            </ul>
            <p class="home-public-wish-status" id="homePublicWishStatus" aria-live="polite"></p>

            <a href="/my-public-whishes.html" class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn">Ver más</a>
          </article>

          <article class="panel">
            <div class="panel-head">
              <h3 class="panel-title">Deseos privados</h3>
              <span class="panel-badge" id="homePrivateWishCount">0 / 50</span>
            </div>

            <div class="secret-meter">
              <div class="secret-number" id="homePrivateWishTotal">0 / 50</div>
              <div class="secret-sub">Solo tú puedes ver esta cifra</div>
            </div>
            <p class="home-public-wish-status" id="homePrivateWishStatus" aria-live="polite"></p>

            <a href="/my-private-whishes.html" class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn">Ir a Deseos privados</a>
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
              <img class="avatar avatar-sm" src="/assets/avatar-default.jpg" alt="Avatar" data-home-avatar />
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
        <img class="avatar avatar-sm" src="/assets/avatar-default.jpg" alt="Avatar" data-home-avatar />
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

<div class="modal-overlay hidden" id="profilePhotoPostModalOverlay" aria-hidden="true">
  <div class="modal modal-wide profile-photo-post-modal" role="dialog" aria-modal="true" aria-label="Publicación de foto de perfil">
    <div class="modal-head">
      <h3>Foto de perfil publicada</h3>
      <button class="modal-close" type="button" id="closeProfilePhotoPostModal">✕</button>
    </div>
    <div class="modal-body">
      <article class="panel post profile-photo-post-card">
        <div class="post-head">
          <div>
            <strong id="profilePhotoPostAuthor">Carlos Jiménez Duarte</strong>
            <span class="post-meta" id="profilePhotoPostMeta">· Publicación pendiente</span>
          </div>
        </div>
        <p class="post-text">Actualice mi foto de perfil.</p>
        <div class="post-media">
          <img id="profilePhotoPostImage" src="/assets/avatar-default.jpg" alt="Foto de perfil publicada" />
        </div>
        <p class="post-warning">La donación de estrella es irreversible.</p>
        <div class="post-actions">
          <button class="post-btn" type="button" id="profilePhotoStarPost">⭐ Donar estrella (0)</button>
          <button class="post-btn" type="button" id="profilePhotoCommentPost">💬 Comentar (0)</button>
          <button class="post-btn" type="button" id="profilePhotoSharePost">🔁 Compartir (0)</button>
        </div>
      </article>
      <p class="profile-photo-post-status" id="profilePhotoPostStatus" aria-live="polite"></p>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelProfilePhotoPostModal">Cerrar</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="homeUsernameModalOverlay" aria-hidden="true">
  <div class="modal home-username-modal" role="dialog" aria-modal="true" aria-label="Modificar nombre de usuario">
    <div class="modal-head">
      <h3>Modificar nombre de usuario</h3>
      <button class="modal-close" type="button" id="closeHomeUsernameModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="panel-muted">Elige un nombre de usuario único. Solo podrás cambiarlo una vez por mes.</p>
      <label class="modal-label" for="homeUsernameInput">Nombre de usuario</label>
      <div class="home-username-input-wrap">
        <span class="home-username-prefix">@</span>
        <input
          class="modal-input home-username-input"
          id="homeUsernameInput"
          type="text"
          minlength="4"
          maxlength="30"
          autocomplete="off"
          placeholder="carlosjimenezduarte"
        />
      </div>
      <p class="home-username-preview" id="homeUsernamePreview">Enlace: /home_user.html</p>
      <p class="infobox-photo-status" id="homeUsernameModalStatus" aria-live="polite"></p>
      <div class="home-username-confirm-wrap hidden" id="homeUsernameConfirmWrap">
        <p class="modal-label-center" id="homeUsernameConfirmText">
          ¿Estás seguro de que deseas este nombre de usuario?
        </p>
        <div class="home-username-confirm-actions">
          <button class="btn btn-primary btn-compact" type="button" id="confirmHomeUsernameBtn">Sí</button>
          <button class="btn btn-outline btn-compact" type="button" id="cancelHomeUsernameConfirmBtn">Cancelar</button>
        </div>
      </div>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelHomeUsernameModal">Cancelar</button>
      <button class="btn btn-primary btn-compact" type="button" id="saveHomeUsernameBtn">Aceptar</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="homeAboutModalOverlay" aria-hidden="true">
  <div class="modal home-about-modal" role="dialog" aria-modal="true" aria-label="Modificar acerca de mí">
    <div class="modal-head">
      <h3>Modificar "Acerca de mí"</h3>
      <button class="modal-close" type="button" id="closeHomeAboutModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="panel-muted">Describe quién eres en un máximo de 50 palabras.</p>
      <textarea class="modal-textarea home-about-textarea" id="homeAboutInput" rows="5" placeholder="Escribe aquí..."></textarea>
      <p class="home-about-word-count" id="homeAboutWordCounter">0 / 50 palabras</p>
      <p class="infobox-photo-status" id="homeAboutModalStatus" aria-live="polite"></p>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelHomeAboutModal">Cancelar</button>
      <button class="btn btn-primary btn-compact" type="button" id="saveHomeAboutBtn">Guardar</button>
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
