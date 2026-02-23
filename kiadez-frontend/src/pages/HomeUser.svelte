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
    const minorProtectedPanel = document.getElementById('minorProtectedPanel');
    const minorProtectedBody = document.getElementById('minorProtectedBody');
    const minorProtectedStateLabel = document.getElementById('minorProtectedStateLabel');
    const toggleMinorProtectedPanelBtn = document.getElementById('toggleMinorProtectedPanel');
    const openMinorAccreditationModalBtn = document.getElementById('openMinorAccreditationModal');
    const minorAccreditationModalOverlay = document.getElementById('minorAccreditationModalOverlay');
    const closeMinorAccreditationModalBtn = document.getElementById('closeMinorAccreditationModal');
    const cancelMinorAccreditationModalBtn = document.getElementById('cancelMinorAccreditationModal');
    const submitMinorAccreditationBtn = document.getElementById('submitMinorAccreditation');
    const minorGuardianPhoneInput = document.getElementById('minorGuardianPhoneInput');
    const minorGuardianEmailInput = document.getElementById('minorGuardianEmailInput');
    const minorRelationshipSelect = document.getElementById('minorRelationshipSelect');
    const minorAccreditationModalStatus = document.getElementById('minorAccreditationModalStatus');
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
    const reportProfileOverlay = document.getElementById('reportProfileModalOverlay');
    const closeReportProfileModal = document.getElementById('closeReportProfileModal');
    const cancelReportProfile = document.getElementById('cancelReportProfile');
    const submitReportProfile = document.getElementById('submitReportProfile');
    const reportProfileReasonOtherWrap = document.getElementById('reportProfileReasonOtherWrap');
    const reportProfileReasonOther = document.getElementById('reportProfileReasonOther');
    const reportProfileModalStatus = document.getElementById('reportProfileModalStatus');

    const commentsOverlay = document.getElementById('postCommentsModalOverlay');
    const closeCommentsModal = document.getElementById('closePostCommentsModal');
    const cancelCommentsModal = document.getElementById('cancelPostCommentsModal');
    const commentsList = document.getElementById('postCommentsList');
    const commentsStatus = document.getElementById('postCommentsStatus');
    const commentInput = document.getElementById('postCommentInput');
    const sendComment = document.getElementById('sendPostComment');
    const commentsTitle = document.getElementById('postCommentsTitle');
    const homeAvatarDropdown = document.getElementById('homeAvatarDropdown');
    const homeAvatarButton = document.getElementById('homeAvatarButton');
    const homeAvatarViewBtn = document.getElementById('homeAvatarViewBtn');
    const homeAvatarUploadBtn = document.getElementById('homeAvatarUploadBtn');
    const homeAvatarGalleryBtn = document.getElementById('homeAvatarGalleryBtn');
    const homeAvatarFile = document.getElementById('homeAvatarFile');
    const homeAvatarGalleryModalOverlay = document.getElementById('homeAvatarGalleryModalOverlay');
    const closeHomeAvatarGalleryModal = document.getElementById('closeHomeAvatarGalleryModal');
    const cancelHomeAvatarGalleryModal = document.getElementById('cancelHomeAvatarGalleryModal');
    const homeAvatarGalleryGrid = document.getElementById('homeAvatarGalleryGrid');
    const homeAvatarGalleryStatus = document.getElementById('homeAvatarGalleryStatus');
    const homeProfileName = document.getElementById('homeProfileName');
    const homeUsernameLink = document.getElementById('homeUsernameLink');
    const homeUsernameValue = document.getElementById('homeUsernameValue');
    const homeUsernameEditBtn = document.getElementById('homeUsernameEditBtn');
    const homeUsernameReportBtn = document.getElementById('homeUsernameReportBtn');
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
    const homeCooperativeWishList = document.getElementById('homeCooperativeWishList');
    const homeCooperativeWishCount = document.getElementById('homeCooperativeWishCount');
    const homeCooperativeWishStatus = document.getElementById('homeCooperativeWishStatus');
    const homeFulfilledWishList = document.getElementById('homeFulfilledWishList');
    const homeFulfilledWishCount = document.getElementById('homeFulfilledWishCount');
    const homeFulfilledWishStatus = document.getElementById('homeFulfilledWishStatus');
	    const homePrivateWishCount = document.getElementById('homePrivateWishCount');
	    const homePrivateWishTotal = document.getElementById('homePrivateWishTotal');
	    const homePrivateWishStatus = document.getElementById('homePrivateWishStatus');
	    const btnChangeCover = document.getElementById('btnChangeCover');
	    const btnEditPurposes = document.getElementById('btnEditPurposes');
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
    const homeAboutPanel = document.getElementById('homeAboutPanel');
    const homeFulfilledPanel = document.getElementById('homeFulfilledPanel');
    const homePublicPanel = document.getElementById('homePublicPanel');
    const homeCooperativePanel = document.getElementById('homeCooperativePanel');
    const homeCalendarPanel = document.getElementById('homeCalendarPanel');
    const homeOraclePanel = document.getElementById('homeOraclePanel');
    const homeCoverSection = document.getElementById('cover');
    const profilePhotoPostOverlay = document.getElementById('profilePhotoPostModalOverlay');
    const closeProfilePhotoPostModal = document.getElementById('closeProfilePhotoPostModal');
    const cancelProfilePhotoPostModal = document.getElementById('cancelProfilePhotoPostModal');
    const profilePhotoPrevBtn = document.getElementById('profilePhotoPrevBtn');
    const profilePhotoNextBtn = document.getElementById('profilePhotoNextBtn');
    const profilePhotoNavLabel = document.getElementById('profilePhotoNavLabel');
    const profilePhotoPostImage = document.getElementById('profilePhotoPostImage');
    const profilePhotoPostAuthor = document.getElementById('profilePhotoPostAuthor');
    const profilePhotoPostMeta = document.getElementById('profilePhotoPostMeta');
    const profilePhotoStarPost = document.getElementById('profilePhotoStarPost');
    const profilePhotoCommentPost = document.getElementById('profilePhotoCommentPost');
    const profilePhotoSharePost = document.getElementById('profilePhotoSharePost');
    const profilePhotoPostStatus = document.getElementById('profilePhotoPostStatus');
    const viewerAvatarImages = Array.from(document.querySelectorAll('[data-viewer-avatar]'));
    const profileAvatarImages = Array.from(document.querySelectorAll('[data-profile-avatar]'));

    let selectedFile = null;
    let selectedFileURL = null;
    let selectedCommentPostId = null;
    let selectedDeletePostId = null;
    let selectedReportPostId = null;
    let selectedReportProfileUserId = null;
    let currentFeedPosts = [];
    let profilePhotoMediaId = null;
    let profilePhotoPost = null;
    let profilePhotoPostId = null;
    let profilePhotoViewerPostId = null;
    let profilePhotoHistory = [];
    let profilePhotoHistoryIndex = 0;
    let homeAvatarGalleryHasImages = false;
    let homeAvatarProfilePhotoBusy = false;
    let currentAboutDisplayName = (homeProfileName?.textContent || 'Usuario Kiadez').trim();
    let currentUsername = '';
    let pendingUsername = '';
    let viewerUserId = null;
    let viewerUsername = '';
    let activeProfileUserId = null;
    let activeProfileUsername = '';
    let activeProfileUrl = '/home_user.html';
    let isViewingOwnProfile = true;
    let hasActiveCooperativeWishes = false;
    let minorAccreditationState = null;
    let minorProtectedCollapsed = false;

    const HOME_ABOUT_MAX_WORDS = 50;
    const USERNAME_MIN_LENGTH = 4;
    const USERNAME_MAX_LENGTH = 30;
    const USERNAME_PATTERN = /^[a-z0-9._]{4,30}$/;
    const PROFILE_PHOTO_POST_STORAGE_KEY = 'home_profile_photo_post_id';
    const PROFILE_PHOTO_POST_TEXT = 'Actualice mi foto de perfil.';
    const DEFAULT_AVATAR_SRC = '/assets/avatar-default.jpg';
    const MINOR_PROTECTED_COLLAPSED_KEY = 'home_minor_protected_collapsed';
    const DEFAULT_PROFILE_PRIVACY_VISIBILITY = {
      public_profile_show_about: true,
      public_profile_show_fulfilled_wishes: true,
      public_profile_show_public_wishes: true,
      public_profile_show_calendar: true,
      public_profile_show_oracle: true,
      public_profile_show_personal_posts: true,
      public_profile_show_cooperative_wishes: true,
      public_profile_show_followers: true,
      public_profile_show_gallery: true,
      public_profile_show_recent_achievements: true,
      public_profile_show_stars: true,
      public_profile_show_cover_purposes: true,
      public_profile_show_biography: true,
    };
    let activeProfilePrivacyVisibility = { ...DEFAULT_PROFILE_PRIVACY_VISIBILITY };

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

    const setMinorAccreditationModalStatus = (message, isError = false) => {
      if (!minorAccreditationModalStatus) return;
      minorAccreditationModalStatus.textContent = message || '';
      minorAccreditationModalStatus.classList.toggle('is-error', Boolean(isError));
    };

    const minorStatusLabel = (status) => {
      if (status === 'requested') return 'Solicitud enviada a adulto responsable';
      if (status === 'pending') return 'Acreditación pendiente';
      if (status === 'approved') return 'Cuenta acreditada';
      return '';
    };

    const syncPostVisibilityMinorGuard = () => {
      if (!postVisibility) return;
      const publicOption = postVisibility.querySelector('option[value="public"]');
      const isProtected = Boolean(minorAccreditationState?.is_minor_protected);
      if (publicOption) {
        publicOption.disabled = isProtected;
      }
      if (isProtected && postVisibility.value === 'public') {
        postVisibility.value = 'private';
      }
    };

    const setMinorProtectedCollapsedState = (collapsed, { persist = true } = {}) => {
      minorProtectedCollapsed = Boolean(collapsed);
      if (minorProtectedBody) {
        minorProtectedBody.classList.toggle('hidden', minorProtectedCollapsed);
      }
      if (toggleMinorProtectedPanelBtn) {
        toggleMinorProtectedPanelBtn.textContent = minorProtectedCollapsed ? 'Expandir' : 'Reducir';
      }
      if (persist) {
        try {
          localStorage.setItem(MINOR_PROTECTED_COLLAPSED_KEY, minorProtectedCollapsed ? '1' : '0');
        } catch (error) {
          console.warn(error);
        }
      }
    };

    const applyMinorProtectedPanelState = () => {
      const isProtected = Boolean(minorAccreditationState?.is_minor_protected);
      const shouldShow = isViewingOwnProfile && isProtected;
      minorProtectedPanel?.classList.toggle('hidden', !shouldShow);

      if (!shouldShow) {
        syncPostVisibilityMinorGuard();
        return;
      }

      if (minorProtectedStateLabel) {
        minorProtectedStateLabel.textContent = minorStatusLabel(minorAccreditationState?.status);
      }
      if (minorGuardianPhoneInput) {
        minorGuardianPhoneInput.value = String(minorAccreditationState?.guardian_phone || '').trim();
      }
      if (minorGuardianEmailInput) {
        minorGuardianEmailInput.value = String(minorAccreditationState?.guardian_email || '').trim();
      }
      if (minorRelationshipSelect) {
        minorRelationshipSelect.value = String(minorAccreditationState?.relationship || 'padre');
      }

      setMinorProtectedCollapsedState(minorProtectedCollapsed, { persist: false });
      syncPostVisibilityMinorGuard();
    };

    const loadMinorAccreditationStatus = async () => {
      if (!isViewingOwnProfile) {
        minorAccreditationState = null;
        applyMinorProtectedPanelState();
        return;
      }

      try {
        const res = await apiFetch('/auth/minor-accreditation/status');
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo cargar el estado de acreditación.');
        minorAccreditationState = data || null;
      } catch (error) {
        console.error(error);
        minorAccreditationState = null;
      }

      applyMinorProtectedPanelState();
    };

    const openMinorAccreditationModal = () => {
      if (!minorAccreditationState?.is_minor_protected) return;
      setMinorAccreditationModalStatus('');
      minorAccreditationModalOverlay?.classList.remove('hidden');
      minorAccreditationModalOverlay?.setAttribute('aria-hidden', 'false');
    };

    const closeMinorAccreditationModal = () => {
      minorAccreditationModalOverlay?.classList.add('hidden');
      minorAccreditationModalOverlay?.setAttribute('aria-hidden', 'true');
      setMinorAccreditationModalStatus('');
    };

    const submitMinorAccreditation = async () => {
      const guardianPhone = String(minorGuardianPhoneInput?.value || '').trim();
      const guardianEmail = String(minorGuardianEmailInput?.value || '').trim();
      const relationship = String(minorRelationshipSelect?.value || 'padre').trim().toLowerCase();

      if (!guardianPhone) {
        setMinorAccreditationModalStatus('Debes indicar el teléfono del adulto responsable.', true);
        return;
      }
      if (!guardianEmail) {
        setMinorAccreditationModalStatus('Debes indicar el correo del adulto responsable.', true);
        return;
      }

      const oldLabel = submitMinorAccreditationBtn?.textContent || 'Enviar solicitud';
      if (submitMinorAccreditationBtn) {
        submitMinorAccreditationBtn.disabled = true;
        submitMinorAccreditationBtn.textContent = 'Enviando...';
      }
      setMinorAccreditationModalStatus('');

      try {
        const res = await apiFetch('/auth/minor-accreditation/request', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            guardian_phone: guardianPhone,
            guardian_email: guardianEmail,
            relationship,
          }),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || 'No se pudo enviar la solicitud de acreditación.');
        }

        await loadMinorAccreditationStatus();
        setMinorAccreditationModalStatus(
          data.message || 'Solicitud enviada. Revisa con el adulto responsable el correo de validación.',
          false
        );
      } catch (error) {
        setMinorAccreditationModalStatus(
          error.message || 'No se pudo enviar la solicitud de acreditación.',
          true
        );
      } finally {
        if (submitMinorAccreditationBtn) {
          submitMinorAccreditationBtn.disabled = false;
          submitMinorAccreditationBtn.textContent = oldLabel;
        }
      }
    };

    const handleMinorProtectedToggle = () => {
      setMinorProtectedCollapsedState(!minorProtectedCollapsed);
    };

    const handleMinorAccreditationOverlayClick = (event) => {
      if (event.target === minorAccreditationModalOverlay) {
        closeMinorAccreditationModal();
      }
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

    const setHomeCooperativeWishStatus = (message, isError = false) => {
      if (!homeCooperativeWishStatus) return;
      homeCooperativeWishStatus.textContent = message || '';
      homeCooperativeWishStatus.classList.toggle('is-error', Boolean(isError));
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

    const setReportProfileModalStatus = (message, isError = false) => {
      if (!reportProfileModalStatus) return;
      reportProfileModalStatus.textContent = message || '';
      reportProfileModalStatus.classList.toggle('is-error', Boolean(isError));
    };

    const updateHomeCooperativePanelVisibility = () => {
      const canShowCooperative = Boolean(activeProfilePrivacyVisibility.public_profile_show_cooperative_wishes);
      const isVisible = canShowCooperative && hasActiveCooperativeWishes;
      homeCooperativePanel?.classList.toggle('hidden', !isVisible);
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

	    const buildViewerHomeUrl = () => {
	      if (viewerUsername) return `/home_user.html?u=${encodeURIComponent(viewerUsername)}`;
	      if (viewerUserId) return `/home_user.html?id=${encodeURIComponent(String(viewerUserId))}`;
	      return '/home_user.html';
	    };

	    const buildAuthorProfileUrl = (author) => {
	      const authorId = Number(author?.id || 0);
	      if (Number.isFinite(authorId) && authorId > 0) {
	        return `/home_user.html?id=${encodeURIComponent(String(authorId))}`;
	      }
	      return '/home_user.html';
	    };

	    const buildProfileQueryParams = () => {
	      if (activeProfileUsername) {
	        return { key: 'u', value: activeProfileUsername };
	      }
	      if (activeProfileUserId) {
	        return { key: 'id', value: String(activeProfileUserId) };
	      }
	      return null;
	    };

    const buildProfileModuleUrl = (path) => {
      const raw = String(path || '').trim();
      if (!raw) return '';
      try {
        const url = new URL(raw, window.location.origin);
        const qp = buildProfileQueryParams();
        url.searchParams.delete('u');
        url.searchParams.delete('id');
        if (qp) url.searchParams.set(qp.key, qp.value);
        return `${url.pathname}${url.search}${url.hash}`;
      } catch {
        return raw;
      }
    };

    const PROFILE_MODULE_ROUTES = {
      home: '/home_user.html',
      public_wishes: '/my-public-whishes.html',
      public_wishes_cooperative: '/my-public-whishes.html#cooperative-wishes',
      fulfilled_wishes: '/my-fulfilled-whises.html',
      followers: '/followers.html',
      achievements: '/achievements.html',
      gallery: '/gallery.html',
      stars: '/star-pool-found.html',
      calendar: '/calendar.html',
      oracle: '/oracle.html',
      biography: '/my-biography.html'
	    };

	    const syncProfileModuleLinks = () => {
	      document.querySelectorAll('a[data-profile-module]').forEach((link) => {
	        const key = String(link.getAttribute('data-profile-module') || '').trim();
	        const basePath = PROFILE_MODULE_ROUTES[key] || link.getAttribute('href') || '';
	        const nextHref = buildProfileModuleUrl(basePath);
	        if (nextHref) link.href = nextHref;
	      });
	    };

    const setMyHomeLinks = (profilePath) => {
      const normalizedPath = profilePath || '/home_user.html';
      document.querySelectorAll('a[data-my-home-link="true"]').forEach((link) => {
        link.href = normalizedPath;
      });
    };

    const setProfileCanonicalLinks = (profilePath) => {
      const normalizedPath = profilePath || '/home_user.html';
      document.querySelectorAll('a[data-profile-link="true"]').forEach((link) => {
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
      const shouldUpdateViewer = isViewingOwnProfile;
      if (shouldUpdateViewer) {
        viewerAvatarImages.forEach((img) => {
          img.src = avatarUrl;
        });
      }
      profileAvatarImages.forEach((img) => {
        img.src = avatarUrl;
      });
      if (isViewingOwnProfile && profilePhotoPostImage && !profilePhotoPost) {
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

    const normalizeProfilePrivacyVisibility = (value) => ({
      public_profile_show_about: Boolean(value?.public_profile_show_about ?? true),
      public_profile_show_fulfilled_wishes: Boolean(value?.public_profile_show_fulfilled_wishes ?? true),
      public_profile_show_public_wishes: Boolean(value?.public_profile_show_public_wishes ?? true),
      public_profile_show_calendar: Boolean(value?.public_profile_show_calendar ?? true),
      public_profile_show_oracle: Boolean(value?.public_profile_show_oracle ?? true),
      public_profile_show_personal_posts: Boolean(value?.public_profile_show_personal_posts ?? true),
      public_profile_show_cooperative_wishes: Boolean(value?.public_profile_show_cooperative_wishes ?? true),
      public_profile_show_followers: Boolean(value?.public_profile_show_followers ?? true),
      public_profile_show_gallery: Boolean(value?.public_profile_show_gallery ?? true),
      public_profile_show_recent_achievements: Boolean(value?.public_profile_show_recent_achievements ?? true),
      public_profile_show_stars: Boolean(value?.public_profile_show_stars ?? true),
      public_profile_show_cover_purposes: Boolean(value?.public_profile_show_cover_purposes ?? true),
      public_profile_show_biography: Boolean(value?.public_profile_show_biography ?? true),
    });

    const setProfileModuleVisibility = (moduleKey, visible) => {
      document.querySelectorAll(`[data-profile-module="${moduleKey}"]`).forEach((node) => {
        node.classList.toggle('hidden', !visible);
      });
    };

    const applyProfilePrivacyVisibility = (value, { isOwner = false } = {}) => {
      if (isOwner) {
        activeProfilePrivacyVisibility = { ...DEFAULT_PROFILE_PRIVACY_VISIBILITY };
      } else {
        activeProfilePrivacyVisibility = normalizeProfilePrivacyVisibility(value);
      }

      const visibility = activeProfilePrivacyVisibility;
      homeAboutPanel?.classList.toggle('hidden', !visibility.public_profile_show_about);
      homeFulfilledPanel?.classList.toggle('hidden', !visibility.public_profile_show_fulfilled_wishes);
      homePublicPanel?.classList.toggle('hidden', !visibility.public_profile_show_public_wishes);
      updateHomeCooperativePanelVisibility();
      homeCalendarPanel?.classList.toggle('hidden', !visibility.public_profile_show_calendar);
      homeOraclePanel?.classList.toggle('hidden', !visibility.public_profile_show_oracle);
      homeCoverSection?.classList.toggle('hidden', !visibility.public_profile_show_cover_purposes);

      setProfileModuleVisibility('fulfilled_wishes', visibility.public_profile_show_fulfilled_wishes);
      setProfileModuleVisibility('public_wishes', visibility.public_profile_show_public_wishes);
      setProfileModuleVisibility('public_wishes_cooperative', visibility.public_profile_show_cooperative_wishes);
      setProfileModuleVisibility('followers', visibility.public_profile_show_followers);
      setProfileModuleVisibility('achievements', visibility.public_profile_show_recent_achievements);
      setProfileModuleVisibility('gallery', visibility.public_profile_show_gallery);
      setProfileModuleVisibility('stars', visibility.public_profile_show_stars);
      setProfileModuleVisibility('calendar', visibility.public_profile_show_calendar);
      setProfileModuleVisibility('oracle', visibility.public_profile_show_oracle);
      setProfileModuleVisibility('biography', visibility.public_profile_show_biography);
    };

    const loadForeignProfilePrivacyVisibility = async () => {
      if (isViewingOwnProfile) {
        applyProfilePrivacyVisibility(DEFAULT_PROFILE_PRIVACY_VISIBILITY, { isOwner: true });
        return;
      }

      const profileId = Number(activeProfileUserId);
      if (!Number.isFinite(profileId) || profileId <= 0) {
        applyProfilePrivacyVisibility(DEFAULT_PROFILE_PRIVACY_VISIBILITY);
        return;
      }

      try {
        const res = await apiFetch(`/privacy/user/${encodeURIComponent(String(profileId))}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo cargar la privacidad del perfil.');
        applyProfilePrivacyVisibility(data);
      } catch (error) {
        console.error(error);
        applyProfilePrivacyVisibility(DEFAULT_PROFILE_PRIVACY_VISIBILITY);
      }
    };

    const updateHomeAboutWordCounter = () => {
      if (!homeAboutWordCounter) return;
      const words = countWords(homeAboutInput?.value || '');
      homeAboutWordCounter.textContent = `${words} / ${HOME_ABOUT_MAX_WORDS} palabras`;
      homeAboutWordCounter.classList.toggle('is-error', words > HOME_ABOUT_MAX_WORDS);
    };

    setProfilePhotoPostId(localStorage.getItem(PROFILE_PHOTO_POST_STORAGE_KEY));
    try {
      minorProtectedCollapsed = localStorage.getItem(MINOR_PROTECTED_COLLAPSED_KEY) === '1';
    } catch (error) {
      console.warn(error);
      minorProtectedCollapsed = false;
    }

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

    const applyReadOnlyProfileMode = () => {
      // When viewing someone else's profile, hide any "my account" panels and editing actions.
      homeUsernameEditBtn?.classList.add('hidden');
      homeUsernameReportBtn?.classList.remove('hidden');
      homeUsernameCooldown?.classList.add('hidden');
      homeAboutEditBtn?.classList.add('hidden');
      homeAvatarUploadBtn?.classList.add('hidden');
	      homeAvatarGalleryBtn?.classList.add('hidden');
	      homeAvatarViewBtn?.classList.add('hidden');
	      menuPublishBtn?.classList.add('hidden');
	      btnChangeCover?.classList.add('hidden');
	      btnEditPurposes?.classList.add('hidden');

      homeAvatarDropdown?.removeAttribute('open');

      homePrivateWishCount?.closest('article.panel')?.classList.add('hidden');

	      openPostModal?.closest('.composer')?.classList.add('hidden');
      minorProtectedPanel?.classList.add('hidden');
	    };

    const fetchViewerIdentity = async () => {
      const res = await apiFetch('/auth/me');
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'No se pudo cargar tu perfil.');
      }
      const userId = Number(data?.user_number);
      return {
        user_id: Number.isFinite(userId) && userId > 0 ? userId : null,
        username: normalizeUsername(data?.username || ''),
      };
    };

    const fetchFollowProfile = async ({ userId = null, username = null } = {}) => {
      const idValue = Number(userId);
      const usernameValue = normalizeUsername(username || '');
      if (Number.isFinite(idValue) && idValue > 0) {
        const res = await apiFetch(`/follows/profile?user_id=${encodeURIComponent(String(idValue))}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo cargar el perfil.');
        return data;
      }
      if (usernameValue) {
        const res = await apiFetch(`/follows/profile?username=${encodeURIComponent(usernameValue)}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo cargar el perfil.');
        return data;
      }
      throw new Error('Parámetros inválidos para cargar perfil.');
    };

    const applyForeignProfileHeader = (profile) => {
      const profileId = Number(profile?.user_id);
      activeProfileUserId = Number.isFinite(profileId) && profileId > 0 ? profileId : null;
      activeProfileUsername = normalizeUsername(profile?.username || '');
      activeProfileUrl = String(profile?.profile_url || '').trim() || '/home_user.html';

      const handleText =
        String(profile?.handle || '').trim() ||
        (activeProfileUsername ? `@${activeProfileUsername}` : activeProfileUserId ? `@id${activeProfileUserId}` : '@usuario');

      if (homeUsernameValue) homeUsernameValue.textContent = handleText;
      if (homeUsernameLink) {
        homeUsernameLink.href = activeProfileUrl;
        homeUsernameLink.classList.toggle('is-empty', false);
      }
      if (homeUsernameCooldown) homeUsernameCooldown.textContent = '';

      const fullName = String(profile?.full_name || '').trim();
      if (fullName && homeProfileName) homeProfileName.textContent = fullName;

	      setProfileCanonicalLinks(activeProfileUrl);
	      setMyHomeLinks(buildViewerHomeUrl());
	      syncProfileModuleLinks();
	      setHomeAvatarSource(String(profile?.avatar_url || '').trim() || DEFAULT_AVATAR_SRC);
	    };

    const resolveProfileContext = async () => {
      const params = new URLSearchParams(window.location.search);
      const requestedIdRaw = params.get('id');
      const requestedId = Number(requestedIdRaw);
      const requestedUserId =
        Number.isFinite(requestedId) && requestedId > 0 ? requestedId : null;
      const requestedUsername = normalizeUsername(params.get('u') || '');

      try {
        const me = await fetchViewerIdentity();
        viewerUserId = me.user_id;
        viewerUsername = me.username;
      } catch (error) {
        console.error(error);
      }

	      activeProfileUserId = viewerUserId;
	      activeProfileUsername = viewerUsername;
	      activeProfileUrl = '/home_user.html';
	      isViewingOwnProfile = true;
	      homeUsernameReportBtn?.classList.add('hidden');
	      setMyHomeLinks(buildViewerHomeUrl());
	      syncProfileModuleLinks();

      const wantsOtherProfile = Boolean(requestedUserId || requestedUsername);
      if (!wantsOtherProfile) return null;

      const isSelfById = requestedUserId && viewerUserId && requestedUserId === viewerUserId;
      const isSelfByUsername = requestedUsername && viewerUsername && requestedUsername === viewerUsername;
      if (isSelfById || isSelfByUsername) return null;

      const profile = await fetchFollowProfile({
        userId: requestedUserId,
        username: requestedUserId ? null : requestedUsername,
      });

      isViewingOwnProfile = false;
      applyReadOnlyProfileMode();
      applyForeignProfileHeader(profile);
      return profile;
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
        homeAboutEmptyState.textContent = isViewingOwnProfile
          ? 'Cuéntale a la comunidad quién eres en pocas palabras.'
          : 'Este usuario aún no ha compartido su sección "Acerca de mí".';
        homeAboutEmptyState.classList.toggle('hidden', Boolean(aboutText));
      }
    };

    const loadHomeAbout = async (userId = null) => {
      if (!isViewingOwnProfile && !activeProfilePrivacyVisibility.public_profile_show_about) {
        return;
      }
      try {
        const endpoint =
          Number.isFinite(Number(userId)) && Number(userId) > 0
            ? `/biography/about/${encodeURIComponent(String(Number(userId)))}`
            : '/biography/about';
        const res = await apiFetch(endpoint);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo cargar "Acerca de mi".');
        applyHomeAbout(data);
      } catch (error) {
        console.error(error);
        if (homeAboutTextValue) {
          homeAboutTextValue.textContent = '';
          homeAboutTextValue.classList.add('hidden');
        }
        if (homeAboutEmptyState) {
          const reason = String(error?.message || '').trim();
          if (!isViewingOwnProfile && reason.toLowerCase().includes('oculta por privacidad')) {
            homeAboutEmptyState.textContent = 'Este usuario decidió ocultar su sección "Acerca de mí".';
          } else {
            homeAboutEmptyState.textContent = isViewingOwnProfile
              ? 'No se pudo cargar tu sección "Acerca de mí".'
              : 'No se pudo cargar la sección "Acerca de mí" de este perfil.';
          }
          homeAboutEmptyState.classList.remove('hidden');
        }
      }
    };

    const openHomeAboutModalPanel = () => {
      if (!isViewingOwnProfile) return;
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

    const collectProfilePhotoHistoryFromFeed = (posts) => {
      const items = Array.isArray(posts) ? posts : [];
      // Profile photo publications are the ones this page creates automatically.
      return items.filter((post) => {
        if (!post?.is_mine) return false;
        if (post?.media_kind !== 'image') return false;
        if (!post?.media_id) return false;
        const text = (post?.text || '').trim();
        return text === PROFILE_PHOTO_POST_TEXT;
      });
    };

    const updateProfilePhotoNavigation = () => {
      const total = Array.isArray(profilePhotoHistory) ? profilePhotoHistory.length : 0;
      const hasMany = total > 1;
      profilePhotoPrevBtn?.classList.toggle('hidden', !hasMany);
      profilePhotoNextBtn?.classList.toggle('hidden', !hasMany);
      profilePhotoNavLabel?.classList.toggle('hidden', !hasMany);

      if (!hasMany) {
        if (profilePhotoNavLabel) profilePhotoNavLabel.textContent = '';
        if (profilePhotoPrevBtn) profilePhotoPrevBtn.disabled = true;
        if (profilePhotoNextBtn) profilePhotoNextBtn.disabled = true;
        return;
      }

      const safeIndex = Math.max(0, Math.min(total - 1, Number(profilePhotoHistoryIndex) || 0));
      profilePhotoHistoryIndex = safeIndex;
      if (profilePhotoNavLabel) profilePhotoNavLabel.textContent = `${safeIndex + 1} / ${total}`;

      // Feed is sorted newest -> oldest; "Anterior" goes to older photos.
      if (profilePhotoPrevBtn) profilePhotoPrevBtn.disabled = safeIndex >= total - 1;
      if (profilePhotoNextBtn) profilePhotoNextBtn.disabled = safeIndex <= 0;
    };

    const renderProfilePhotoPost = (post) => {
      profilePhotoPost = post || null;
      if (profilePhotoPostImage) {
        const imageUrl = post?.media_url || profileAvatarImages[0]?.src || DEFAULT_AVATAR_SRC;
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
        profilePhotoHistory = [];
        profilePhotoHistoryIndex = 0;
        updateProfilePhotoNavigation();
        return;
      }

      // 1) Keep a stable reference to the *current* profile photo post (by id or by media id).
      let currentProfilePost = null;
      if (profilePhotoPostId) {
        currentProfilePost =
          currentFeedPosts.find((post) => post.id === profilePhotoPostId && post.is_mine) || null;
      }
      if (!currentProfilePost && profilePhotoMediaId) {
        currentProfilePost = currentFeedPosts.find(
          (post) => post.is_mine && post.media_id === profilePhotoMediaId && post.media_kind === 'image'
        ) || null;
        if (currentProfilePost) setProfilePhotoPostId(currentProfilePost.id);
      }
      if (!currentProfilePost && profilePhotoPostId) setProfilePhotoPostId(null);

      // 2) Build the profile photo history (newest -> oldest).
      profilePhotoHistory = collectProfilePhotoHistoryFromFeed(currentFeedPosts);

      // 3) Render the viewer-selected post (if any), otherwise render current profile photo post.
      let viewerPost = null;
      if (profilePhotoViewerPostId) {
        viewerPost = profilePhotoHistory.find((post) => post.id === profilePhotoViewerPostId) || null;
      }
      if (!viewerPost) {
        viewerPost = currentProfilePost;
        profilePhotoViewerPostId = viewerPost?.id || null;
      }

      // Keep the index in sync for the navigation UI.
      if (profilePhotoViewerPostId) {
        const idx = profilePhotoHistory.findIndex((post) => post.id === profilePhotoViewerPostId);
        if (idx >= 0) profilePhotoHistoryIndex = idx;
      } else if (viewerPost?.id) {
        const idx = profilePhotoHistory.findIndex((post) => post.id === viewerPost.id);
        profilePhotoHistoryIndex = idx >= 0 ? idx : 0;
      } else {
        profilePhotoHistoryIndex = 0;
      }

      renderProfilePhotoPost(viewerPost);
      updateProfilePhotoNavigation();
    };

    const loadProfilePhoto = async () => {
      if (!isViewingOwnProfile) return;
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

    const setHomeAvatarGalleryStatus = (message, isError = false) => {
      if (!homeAvatarGalleryStatus) return;
      homeAvatarGalleryStatus.textContent = message || '';
      homeAvatarGalleryStatus.classList.toggle('posts-status-error', Boolean(isError));
    };

    const closeHomeAvatarDropdown = () => {
      homeAvatarDropdown?.removeAttribute('open');
    };

    const closeHomeAvatarGalleryModalPanel = () => {
      homeAvatarGalleryModalOverlay?.classList.add('hidden');
      homeAvatarGalleryModalOverlay?.setAttribute('aria-hidden', 'true');
      setHomeAvatarGalleryStatus('');
      if (homeAvatarGalleryGrid) homeAvatarGalleryGrid.innerHTML = '';
    };

    const handleHomeAvatarGalleryOverlayClick = (event) => {
      if (event.target === homeAvatarGalleryModalOverlay) closeHomeAvatarGalleryModalPanel();
    };

    const fetchMyImageOptions = async (limit = 24) => {
      const res = await apiFetch(`/media/mine/images?limit=${limit}`);
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'No se pudo cargar tu galería.');
      }
      const items = Array.isArray(data.items) ? data.items : [];
      return items;
    };

    const refreshHomeAvatarMenuOptions = async () => {
      const hasProfilePhoto = Boolean(profilePhotoMediaId);
      homeAvatarViewBtn?.classList.toggle('hidden', !hasProfilePhoto);
      if (!homeAvatarGalleryBtn) return;

      try {
        const items = await fetchMyImageOptions(1);
        homeAvatarGalleryHasImages = items.length > 0;
      } catch (error) {
        homeAvatarGalleryHasImages = false;
      }

      homeAvatarGalleryBtn.classList.toggle('hidden', !homeAvatarGalleryHasImages);
    };

    const applyUsernameState = (state) => {
      const username = normalizeUsername(state?.username || '');
      currentUsername = username;
      const hasUsername = Boolean(username);
      const profilePath = state?.profile_url || (hasUsername ? `/home_user.html?u=${encodeURIComponent(username)}` : '/home_user.html');
	      if (isViewingOwnProfile) {
	        activeProfileUsername = username;
	        activeProfileUrl = profilePath;
	        if (viewerUserId) activeProfileUserId = viewerUserId;
	        syncProfileModuleLinks();
	      }
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
      setProfileCanonicalLinks(profilePath);
      if (isViewingOwnProfile) setMyHomeLinks(profilePath);
    };

    const loadUsernameState = async () => {
      if (!isViewingOwnProfile) return;
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
      if (!isViewingOwnProfile) return;
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

    const renderHomeCooperativeWishes = (items, activeCount = 0, activeLimit = 20) => {
      if (!homeCooperativeWishList) return;
      const wishes = Array.isArray(items) ? [...items] : [];
      wishes.sort((a, b) => {
        const aTs = Date.parse(a?.created_at || '');
        const bTs = Date.parse(b?.created_at || '');
        const aSafe = Number.isNaN(aTs) ? 0 : aTs;
        const bSafe = Number.isNaN(bTs) ? 0 : bTs;
        return bSafe - aSafe;
      });

      const topSeven = wishes.slice(0, 7);
      const safeActiveCount = Math.max(0, Number(activeCount || 0));
      const safeActiveLimit = Math.max(1, Number(activeLimit || 20));

      hasActiveCooperativeWishes = safeActiveCount > 0 && topSeven.length > 0;
      updateHomeCooperativePanelVisibility();

      if (homeCooperativeWishCount) {
        homeCooperativeWishCount.textContent = `${safeActiveCount} / ${safeActiveLimit}`;
      }

      if (topSeven.length === 0) {
        homeCooperativeWishList.innerHTML = '';
        return;
      }

      homeCooperativeWishList.innerHTML = topSeven
        .map((wish) => {
          const wishText = escapeHtml(wish?.wish_text || 'Deseo cooperativo sin descripción');
          const mediaUrl = (wish?.media_url || '').trim();
          const mediaHtml = mediaUrl
            ? `<img class="wish-item-thumb" src="${escapeHtml(mediaUrl)}" alt="Imagen del deseo cooperativo" loading="lazy" />`
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
	      if (!isViewingOwnProfile && !activeProfilePrivacyVisibility.public_profile_show_public_wishes) {
	        setHomePublicWishStatus('');
	        return;
	      }
	      try {
	        const profileId = Number(activeProfileUserId);
	        const endpoint =
	          !isViewingOwnProfile && Number.isFinite(profileId) && profileId > 0
	            ? `/public-wishes/user/${encodeURIComponent(String(profileId))}/personal`
	            : '/public-wishes/personal';
	        const res = await apiFetch(endpoint);
	        const data = await res.json();
	        if (!res.ok) throw new Error(data.detail || 'No se pudieron cargar tus deseos públicos.');
	        renderHomePublicWishes(data?.items || [], data?.active_count || 0, data?.active_limit || 50);
	        setHomePublicWishStatus('');
      } catch (error) {
        renderHomePublicWishes([], 0, 50);
        setHomePublicWishStatus(error.message || 'No se pudieron cargar tus deseos públicos.', true);
      }
    };

    const loadHomeCooperativeWishes = async () => {
      if (!isViewingOwnProfile && !activeProfilePrivacyVisibility.public_profile_show_cooperative_wishes) {
        hasActiveCooperativeWishes = false;
        updateHomeCooperativePanelVisibility();
        setHomeCooperativeWishStatus('');
        return;
      }
      try {
        const profileId = Number(activeProfileUserId);
        const endpoint =
          !isViewingOwnProfile && Number.isFinite(profileId) && profileId > 0
            ? `/public-wishes/user/${encodeURIComponent(String(profileId))}/cooperative`
            : '/public-wishes/cooperative';
        const res = await apiFetch(endpoint);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudieron cargar tus deseos cooperativos.');
        renderHomeCooperativeWishes(data?.items || [], data?.active_count || 0, data?.active_limit || 20);
        setHomeCooperativeWishStatus('');
      } catch (error) {
        hasActiveCooperativeWishes = false;
        updateHomeCooperativePanelVisibility();
        renderHomeCooperativeWishes([], 0, 20);
        setHomeCooperativeWishStatus(error.message || 'No se pudieron cargar tus deseos cooperativos.', true);
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
	      if (!isViewingOwnProfile && !activeProfilePrivacyVisibility.public_profile_show_fulfilled_wishes) {
	        setHomeFulfilledWishStatus('');
	        return;
	      }
	      try {
	        const profileId = Number(activeProfileUserId);
	        const endpoint =
	          !isViewingOwnProfile && Number.isFinite(profileId) && profileId > 0
	            ? `/public-wishes/user/${encodeURIComponent(String(profileId))}/personal/fulfilled?limit=7&offset=0`
	            : '/public-wishes/personal/fulfilled?limit=7&offset=0';
	        const res = await apiFetch(endpoint);
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

    const buildDisplayPosts = (posts) => {
      const list = Array.isArray(posts) ? posts : [];
      const grouped = new Map();
      const display = [];

      for (const post of list) {
        const albumId = Number(post?.album_id || 0);
        if (!albumId) {
          display.push({ ...post, __kind: 'single' });
          continue;
        }

        const existing = grouped.get(albumId);
        if (!existing) {
          const albumGroup = {
            __kind: 'album',
            album_id: albumId,
            album_name: String(post?.album_name || '').trim() || `Álbum ${albumId}`,
            album_items: [post]
          };
          grouped.set(albumId, albumGroup);
          display.push(albumGroup);
          continue;
        }

        existing.album_items.push(post);
      }

      return display.map((item) => {
        if (item.__kind !== 'album') return item;

        const albumItems = Array.isArray(item.album_items) ? item.album_items : [];
        const coverPost = albumItems[0] || null;
        const previewItems = albumItems.slice(0, 4);
        const extraItems = Math.max(0, albumItems.length - previewItems.length);

        return {
          ...coverPost,
          __kind: 'album',
          album_id: item.album_id,
          album_name: item.album_name,
          album_items: albumItems,
          album_preview_items: previewItems,
          album_total_items: albumItems.length,
          album_extra_items: extraItems
        };
      });
    };

    const renderPosts = (posts) => {
      if (!postsList) return;
      const displayPosts = buildDisplayPosts(posts);

      if (!Array.isArray(displayPosts) || displayPosts.length === 0) {
        postsList.innerHTML = `
          <article class="panel post post-empty">
            <p class="post-text">Aun no hay publicaciones. Crea la primera desde el boton "Que estas pensando?".</p>
          </article>
        `;
        return;
      }

      postsList.innerHTML = displayPosts
        .map((post) => {
          const isAlbumGroup = post.__kind === 'album' && Number(post.album_total_items || 0) > 1;

          let mediaHtml = '';
          if (isAlbumGroup) {
            const previewItems = Array.isArray(post.album_preview_items) ? post.album_preview_items : [];
            const extraItems = Math.max(0, Number(post.album_extra_items || 0));
            const previewHtml = previewItems
              .map((albumPost, index) => {
                const mediaNode = albumPost.media_kind === 'video'
                  ? `<video src="${escapeHtml(albumPost.media_url || '')}" muted playsinline preload="metadata"></video>`
                  : `<img src="${escapeHtml(albumPost.media_url || '')}" alt="Archivo del álbum" loading="lazy" />`;
                const showExtra = index === 3 && extraItems > 0
                  ? `<span class="post-album-more">+${extraItems}</span>`
                  : '';
                return `
                  <div class="post-album-cell">
                    ${mediaNode}
                    ${showExtra}
                  </div>
                `;
              })
              .join('');

            mediaHtml = `
              <div class="post-album-grid" aria-label="Publicación agrupada de álbum">
                ${previewHtml}
              </div>
            `;
          } else {
            mediaHtml = post.media_url
              ? post.media_kind === 'video'
                ? `<div class="post-media"><video src="${post.media_url}" controls></video></div>`
                : `<div class="post-media"><img src="${post.media_url}" alt="Media de la publicacion" /></div>`
              : '';
          }

          const starDisabled = post.starred_by_me || post.is_mine ? 'disabled' : '';
          const starLabel = post.starred_by_me
            ? `⭐ Estrella donada (${post.star_count})`
            : `⭐ Donar estrella (${post.star_count})`;
          const reportBtn = post.is_mine
            ? ''
            : `<button class="post-head-btn" type="button" data-action="report-post" data-post-id="${post.id}" title="Reportar publicacion">🚩</button>`;
          const deleteBtn = post.is_mine
            ? `<button class="post-head-btn" type="button" data-action="delete-post" data-post-id="${post.id}" title="Eliminar publicacion">🗑</button>`
            : '';
          const albumMeta = isAlbumGroup
            ? `<p class="post-album-meta">${escapeHtml(post.album_name || "Álbum")} · ${Number(post.album_total_items || 0)} archivo(s)</p>`
            : '';
	          const openAlbumBtn = isAlbumGroup
	            ? `<button class="post-btn" type="button" data-action="open-album-gallery" data-album-id="${Number(post.album_id || 0)}">🖼️ Hojear álbum (${Number(post.album_total_items || 0)})</button>`
	            : '';
	          const authorProfileUrl = escapeHtml(buildAuthorProfileUrl(post?.author));
	          const authorName = escapeHtml(post?.author?.name || 'Usuario');

	          return `
	            <article class="panel post" data-post-id="${post.id}">
	              <div class="post-head">
	                <div>
	                  <a class="post-author-link" href="${authorProfileUrl}">${authorName}</a>
	                  <span class="post-meta">· ${relativeTime(post.created_at)} · ${post.visibility === 'private' ? 'Privado' : 'Publico'}</span>
	                </div>
	                <div class="post-head-actions">
                  ${reportBtn}
                  ${deleteBtn}
                </div>
              </div>
              ${albumMeta}
              ${post.text ? `<p class="post-text">${escapeHtml(post.text)}</p>` : ''}
              ${mediaHtml}
              <p class="post-warning">La donacion de estrella es irreversible.</p>
              <div class="post-actions">
                <button class="post-btn" type="button" data-action="star-post" data-post-id="${post.id}" ${starDisabled}>${starLabel}</button>
                <button class="post-btn" type="button" data-action="comment-post" data-post-id="${post.id}">💬 Comentar (${post.comment_count})</button>
                <button class="post-btn" type="button" data-action="share-post" data-post-id="${post.id}">🔁 Compartir (${post.share_count})</button>
                ${openAlbumBtn}
              </div>
            </article>
          `;
        })
        .join('');
    };

    const loadMyStats = async () => {
      try {
        if (!starsTotalLabel) return;
        if (isViewingOwnProfile) {
          const res = await apiFetch('/posts/me/stats');
          const data = await res.json();
          if (res.ok) {
            starsTotalLabel.textContent = Number(data.my_received_stars_total || 0).toLocaleString('es-CO');
          }
          return;
        }

        const profileId = Number(activeProfileUserId);
        if (!Number.isFinite(profileId) || profileId <= 0) {
          starsTotalLabel.textContent = '0';
          return;
        }

        const res = await apiFetch(`/follows/profile?user_id=${encodeURIComponent(String(profileId))}`);
        const data = await res.json();
        if (res.ok) {
          starsTotalLabel.textContent = Number(data.received_stars_total || 0).toLocaleString('es-CO');
        }
      } catch (error) {
        console.error(error);
      }
    };

    const loadFeed = async () => {
      try {
        const profileId = Number(activeProfileUserId);
        const endpoint = isViewingOwnProfile
          ? '/posts/mine?limit=40'
          : Number.isFinite(profileId) && profileId > 0
            ? `/posts/user/${encodeURIComponent(String(profileId))}?limit=40`
            : '/posts/mine?limit=40';

        const res = await apiFetch(endpoint);
        const data = await res.json();
        if (!res.ok) {
          setPostsStatus(data.detail || 'No se pudo cargar las publicaciones.', true);
          return;
        }
        currentFeedPosts = Array.isArray(data) ? data : [];
        renderPosts(data);
        if (isViewingOwnProfile) syncProfilePhotoPostFromFeed();
        setPostsStatus('');
      } catch (error) {
        setPostsStatus('No se pudo conectar con el servidor de publicaciones.', true);
      }
    };

    const openPost = () => {
      if (!isViewingOwnProfile) return;
      syncPostVisibilityMinorGuard();
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
      if (postVisibility) {
        postVisibility.value = minorAccreditationState?.is_minor_protected ? 'private' : 'public';
      }
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
      const mediaKind = file.type.startsWith('video/') ? 'video' : 'image';

      // Imagen: upload directo al backend (evita CORS del bucket).
      if (mediaKind === 'image') {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('visibility', (visibilityValue || 'private').toLowerCase());

        const uploadRes = await apiFetch('/media/upload/direct', {
          method: 'POST',
          body: formData
        });
        const uploadData = await uploadRes.json();
        if (!uploadRes.ok) {
          throw new Error(uploadData.detail || 'No se pudo subir la imagen.');
        }
        return { media_id: uploadData.media_id, media_kind: 'image' };
      }

      // Video (y otros): registro + subida por proxy (evita CORS del bucket).
      const presignRes = await apiFetch('/media/presign/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          content_type: file.type,
          size_bytes: file.size,
          visibility: (visibilityValue || 'private').toLowerCase()
        })
      });
      const presignData = await presignRes.json();
      if (!presignRes.ok) {
        throw new Error(presignData.detail || 'No se pudo preparar la carga de media.');
      }

      const proxyForm = new FormData();
      proxyForm.append('media_id', String(presignData.media_id));
      proxyForm.append('file', file);
      const proxyRes = await apiFetch('/media/upload/proxy', {
        method: 'POST',
        body: proxyForm
      });
      const proxyData = await proxyRes.json();
      if (!proxyRes.ok) {
        throw new Error(proxyData.detail || 'No se pudo subir el archivo.');
      }

      return { media_id: presignData.media_id, media_kind: 'video' };
    };

    const uploadProfilePhotoFilePresigned = async (file) => {
      if (!file) return null;
      if (!file.type?.startsWith('image/')) {
        throw new Error('Solo se permiten imágenes para la foto de perfil.');
      }

      const presignRes = await apiFetch('/media/presign/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: file.name,
          content_type: file.type,
          size_bytes: file.size,
          visibility: 'public'
        })
      });
      const presignData = await presignRes.json();
      if (!presignRes.ok) {
        throw new Error(presignData.detail || 'No se pudo preparar la carga de la foto de perfil.');
      }

      try {
        const uploadRes = await fetch(presignData.upload_url, {
          method: 'PUT',
          headers: presignData.required_headers || { 'Content-Type': file.type },
          body: file
        });
        if (!uploadRes.ok) {
          throw new Error('No se pudo subir la imagen al storage.');
        }
      } catch (error) {
        const message = (error?.message || '').toLowerCase();
        if (message.includes('failed to fetch') || message.includes('cors')) {
          throw new Error(
            'La subida directa al bucket fue bloqueada por CORS. Debes habilitar CORS en tu bucket de media para permitir PUT desde tu frontend.'
          );
        }
        throw error;
      }

      const confirmRes = await apiFetch('/media/confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ media_id: presignData.media_id })
      });
      const confirmData = await confirmRes.json();
      if (!confirmRes.ok) {
        throw new Error(confirmData.detail || 'No se pudo confirmar la foto de perfil.');
      }

      return { media_id: presignData.media_id, media_kind: 'image' };
    };

    const uploadMediaIfNeeded = async (visibilityValue) => {
      if (!selectedFile) return null;
      return uploadMediaFile(selectedFile, visibilityValue);
    };

    const handlePublishPost = async () => {
      if (!isViewingOwnProfile) return;
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
        let visibilityValue = (postVisibility?.value || 'public').toLowerCase();
        if (minorAccreditationState?.is_minor_protected && visibilityValue === 'public') {
          visibilityValue = 'private';
          if (postVisibility) postVisibility.value = 'private';
          setPostsStatus('Tu cuenta está en modo protegido. Esta publicación se guardará en privado.');
        }
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
          visibility: (
            minorAccreditationState?.is_minor_protected ? 'private' : (visibility || 'public')
          ).toLowerCase(),
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

      let currentProfilePost = null;
      if (profilePhotoPostId) {
        currentProfilePost =
          currentFeedPosts.find((post) => post.id === profilePhotoPostId && post.is_mine) || null;
      }
      if (!currentProfilePost && profilePhotoMediaId) {
        currentProfilePost = currentFeedPosts.find(
          (post) => post.is_mine && post.media_id === profilePhotoMediaId && post.media_kind === 'image'
        ) || null;
        if (currentProfilePost) setProfilePhotoPostId(currentProfilePost.id);
      }
      if (currentProfilePost) return true;

      const created = await createPost({
        text: PROFILE_PHOTO_POST_TEXT,
        visibility: 'public',
        media_id: profilePhotoMediaId,
        media_kind: 'image'
      });
      setProfilePhotoPostId(created.id);
      await loadFeed();
      syncProfilePhotoPostFromFeed();
      return Boolean(profilePhotoPostId);
    };

    const openProfilePhotoPost = async () => {
      if (!isViewingOwnProfile) return;
      profilePhotoViewerPostId = null;
      profilePhotoHistory = [];
      profilePhotoHistoryIndex = 0;
      updateProfilePhotoNavigation();
      profilePhotoPostOverlay?.classList.remove('hidden');
      profilePhotoPostOverlay?.setAttribute('aria-hidden', 'false');
      try {
        await ensureProfilePhotoPost();
        // Always open on the *current* profile photo.
        profilePhotoViewerPostId = profilePhotoPostId || null;
        syncProfilePhotoPostFromFeed();
      } catch (error) {
        setProfilePhotoPostStatus(error.message || 'No se pudo abrir la publicacion de la foto de perfil.', true);
      }
    };

    const setProfilePhotoFromMediaId = async (mediaId) => {
      if (!isViewingOwnProfile) {
        throw new Error('No autorizado para cambiar esta foto de perfil.');
      }
      const normalized = Number(mediaId);
      if (!Number.isFinite(normalized) || normalized <= 0) {
        throw new Error('Media inválida para foto de perfil.');
      }
      const res = await apiFetch('/media/profile-photo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ media_id: normalized })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'No se pudo actualizar la foto de perfil.');
      }
      profilePhotoMediaId = data.media_id || null;
      setProfilePhotoPostId(null);
      setHomeAvatarSource(data.url || DEFAULT_AVATAR_SRC);
      renderProfilePhotoPost(null);
      return data;
    };

    const handleHomeAvatarButtonClick = () => {
      if (!isViewingOwnProfile) return;
      void refreshHomeAvatarMenuOptions();
    };

    const handleHomeAvatarViewClick = () => {
      if (!isViewingOwnProfile) return;
      closeHomeAvatarDropdown();
      void openProfilePhotoPost();
    };

    const handleHomeAvatarUploadClick = () => {
      if (!isViewingOwnProfile) return;
      closeHomeAvatarDropdown();
      homeAvatarFile?.click();
    };

    const handleHomeAvatarFileChange = async (event) => {
      if (!isViewingOwnProfile) return;
      const file = event?.target?.files?.[0];
      if (!file) return;
      closeHomeAvatarDropdown();
      if (homeAvatarProfilePhotoBusy) return;
      if (!file.type?.startsWith('image/')) {
        setPostsStatus('Solo se permiten imágenes para la foto de perfil.', true);
        if (homeAvatarFile) homeAvatarFile.value = '';
        return;
      }

      homeAvatarProfilePhotoBusy = true;
      setPostsStatus('Subiendo foto de perfil...');
      try {
        const uploaded = await uploadProfilePhotoFilePresigned(file);
        await setProfilePhotoFromMediaId(uploaded?.media_id);
        setPostsStatus('Foto de perfil actualizada.');
        void ensureProfilePhotoPost().catch((error) => console.error(error));
      } catch (error) {
        setPostsStatus(error.message || 'No se pudo actualizar tu foto de perfil.', true);
      } finally {
        homeAvatarProfilePhotoBusy = false;
        if (homeAvatarFile) homeAvatarFile.value = '';
      }
    };

    const renderHomeAvatarGallery = (items) => {
      if (!homeAvatarGalleryGrid) return;
      if (!Array.isArray(items) || items.length === 0) {
        homeAvatarGalleryGrid.innerHTML = '';
        return;
      }

      homeAvatarGalleryGrid.innerHTML = items
        .map(
          (item) => `
            <button class="avatar-gallery-option" type="button" data-media-id="${Number(item.media_id) || ''}" title="Usar como foto de perfil">
              <img src="${escapeHtml(item.url)}" alt="Imagen de galería" loading="lazy" />
            </button>
          `
        )
        .join('');
    };

    const openHomeAvatarGalleryModalPanel = async () => {
      if (!isViewingOwnProfile) return;
      closeHomeAvatarDropdown();
      homeAvatarGalleryModalOverlay?.classList.remove('hidden');
      homeAvatarGalleryModalOverlay?.setAttribute('aria-hidden', 'false');
      setHomeAvatarGalleryStatus('Cargando imágenes...');
      if (homeAvatarGalleryGrid) homeAvatarGalleryGrid.innerHTML = '';

      try {
        const items = await fetchMyImageOptions(60);
        if (items.length === 0) {
          setHomeAvatarGalleryStatus('Aún no tienes imágenes en tu galería.', false);
          renderHomeAvatarGallery([]);
          return;
        }
        setHomeAvatarGalleryStatus('Selecciona una imagen para tu foto de perfil.');
        renderHomeAvatarGallery(items);
      } catch (error) {
        setHomeAvatarGalleryStatus(error.message || 'No se pudo cargar tu galería.', true);
      }
    };

    const handleHomeAvatarGalleryPick = async (event) => {
      if (!isViewingOwnProfile) return;
      const button = event.target?.closest?.('[data-media-id]');
      if (!button) return;
      const mediaId = Number(button.dataset.mediaId);
      if (!Number.isFinite(mediaId) || mediaId <= 0) return;
      if (homeAvatarProfilePhotoBusy) return;

      homeAvatarProfilePhotoBusy = true;
      setHomeAvatarGalleryStatus('Actualizando foto de perfil...');
      try {
        await setProfilePhotoFromMediaId(mediaId);
        closeHomeAvatarGalleryModalPanel();
        setPostsStatus('Foto de perfil actualizada.');
        void ensureProfilePhotoPost().catch((error) => console.error(error));
      } catch (error) {
        setHomeAvatarGalleryStatus(error.message || 'No se pudo actualizar tu foto de perfil.', true);
      } finally {
        homeAvatarProfilePhotoBusy = false;
      }
    };

    const closeProfilePhotoPost = () => {
      profilePhotoPostOverlay?.classList.add('hidden');
      profilePhotoPostOverlay?.setAttribute('aria-hidden', 'true');
      setProfilePhotoPostStatus('');
      profilePhotoViewerPostId = null;
      profilePhotoHistory = [];
      profilePhotoHistoryIndex = 0;
      updateProfilePhotoNavigation();
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

    const closeReportProfileModalPanel = () => {
      reportProfileOverlay?.classList.add('hidden');
      reportProfileOverlay?.setAttribute('aria-hidden', 'true');
      selectedReportProfileUserId = null;
      setReportProfileModalStatus('');
      if (reportProfileReasonOther) reportProfileReasonOther.value = '';
      if (reportProfileReasonOtherWrap) reportProfileReasonOtherWrap.classList.add('hidden');
      const defaultOption = document.querySelector('input[name="profileReportReason"][value="fake_or_illegal"]');
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
        if (isViewingOwnProfile) syncProfilePhotoPostFromFeed();
      } catch (error) {
        setStatus(error.message || 'No se pudo donar la estrella.', true);
      }
    };

    const sharePost = async (postId, setStatus = setPostsStatus) => {
      try {
        await apiFetch(`/posts/${postId}/share`, { method: 'POST' });
        const shareUrlObject = new URL('/home_user.html', window.location.origin);
        if (activeProfileUsername) {
          shareUrlObject.searchParams.set('u', activeProfileUsername);
        } else if (activeProfileUserId) {
          shareUrlObject.searchParams.set('id', String(activeProfileUserId));
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
        if (isViewingOwnProfile) syncProfilePhotoPostFromFeed();
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

    const setProfilePhotoViewerByIndex = (nextIndex) => {
      const total = Array.isArray(profilePhotoHistory) ? profilePhotoHistory.length : 0;
      if (total === 0) {
        profilePhotoViewerPostId = null;
        profilePhotoHistoryIndex = 0;
        renderProfilePhotoPost(null);
        updateProfilePhotoNavigation();
        return;
      }

      const safeIndex = Math.max(0, Math.min(total - 1, Number(nextIndex) || 0));
      profilePhotoHistoryIndex = safeIndex;
      const nextPost = profilePhotoHistory[safeIndex] || null;
      profilePhotoViewerPostId = nextPost?.id || null;
      renderProfilePhotoPost(nextPost);
      updateProfilePhotoNavigation();
    };

    const handleProfilePhotoPrevNav = () => {
      if (profilePhotoPrevBtn?.disabled) return;
      setProfilePhotoViewerByIndex(profilePhotoHistoryIndex + 1);
    };

    const handleProfilePhotoNextNav = () => {
      if (profilePhotoNextBtn?.disabled) return;
      setProfilePhotoViewerByIndex(profilePhotoHistoryIndex - 1);
    };

    const handlePostsClick = async (event) => {
      const button = event.target.closest('[data-action]');
      if (!button) return;
      const action = button.dataset.action;
      const albumId = Number(button.dataset.albumId);
      const postId = Number(button.dataset.postId);

      if (action === 'open-album-gallery') {
        if (!Number.isFinite(albumId) || albumId <= 0) return;
        window.location.href = `/gallery.html?album=${encodeURIComponent(String(albumId))}`;
        return;
      }

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

    const handleProfileReportReasonChange = (event) => {
      const selected = event.target?.value || '';
      if (!reportProfileReasonOtherWrap) return;
      if (selected === 'other') reportProfileReasonOtherWrap.classList.remove('hidden');
      else reportProfileReasonOtherWrap.classList.add('hidden');
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

    const handleOpenProfileReportModal = () => {
      if (isViewingOwnProfile) return;
      const targetUserId = Number(activeProfileUserId);
      if (!Number.isFinite(targetUserId) || targetUserId <= 0) {
        setPostsStatus('No se pudo identificar el usuario a denunciar.', true);
        return;
      }
      selectedReportProfileUserId = targetUserId;
      setReportProfileModalStatus('');
      reportProfileOverlay?.classList.remove('hidden');
      reportProfileOverlay?.setAttribute('aria-hidden', 'false');
    };

    const handleSubmitProfileReport = async () => {
      if (!selectedReportProfileUserId) return;
      const selected = document.querySelector('input[name="profileReportReason"]:checked');
      const reason = selected?.value;
      if (!reason) {
        setReportProfileModalStatus('Debes elegir una razón de reporte.', true);
        return;
      }
      const otherReason = (reportProfileReasonOther?.value || '').trim();
      if (reason === 'other' && !otherReason) {
        setReportProfileModalStatus('Debes escribir la razón cuando eliges "Otro".', true);
        return;
      }

      const oldLabel = submitReportProfile?.textContent || 'Enviar reporte';
      if (submitReportProfile) {
        submitReportProfile.disabled = true;
        submitReportProfile.textContent = 'Enviando...';
      }
      setReportProfileModalStatus('');

      try {
        const res = await apiFetch(`/follows/profile/${encodeURIComponent(String(selectedReportProfileUserId))}/reports`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reason, other_reason: otherReason || null })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'No se pudo enviar el reporte de perfil.');
        setPostsStatus('Reporte de perfil enviado correctamente.');
        closeReportProfileModalPanel();
      } catch (error) {
        setReportProfileModalStatus(error.message || 'No se pudo enviar el reporte de perfil.', true);
      } finally {
        if (submitReportProfile) {
          submitReportProfile.disabled = false;
          submitReportProfile.textContent = oldLabel;
        }
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
    homeAvatarButton?.addEventListener('click', handleHomeAvatarButtonClick);
    homeAvatarViewBtn?.addEventListener('click', handleHomeAvatarViewClick);
    homeAvatarUploadBtn?.addEventListener('click', handleHomeAvatarUploadClick);
    homeAvatarFile?.addEventListener('change', handleHomeAvatarFileChange);
    homeAvatarGalleryBtn?.addEventListener('click', openHomeAvatarGalleryModalPanel);
    closeHomeAvatarGalleryModal?.addEventListener('click', closeHomeAvatarGalleryModalPanel);
    cancelHomeAvatarGalleryModal?.addEventListener('click', closeHomeAvatarGalleryModalPanel);
    homeAvatarGalleryModalOverlay?.addEventListener('click', handleHomeAvatarGalleryOverlayClick);
    homeAvatarGalleryGrid?.addEventListener('click', handleHomeAvatarGalleryPick);
    homeUsernameEditBtn?.addEventListener('click', openHomeUsernameModalPanel);
    homeUsernameReportBtn?.addEventListener('click', handleOpenProfileReportModal);
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
    profilePhotoPrevBtn?.addEventListener('click', handleProfilePhotoPrevNav);
    profilePhotoNextBtn?.addEventListener('click', handleProfilePhotoNextNav);
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
    toggleMinorProtectedPanelBtn?.addEventListener('click', handleMinorProtectedToggle);
    openMinorAccreditationModalBtn?.addEventListener('click', openMinorAccreditationModal);
    closeMinorAccreditationModalBtn?.addEventListener('click', closeMinorAccreditationModal);
    cancelMinorAccreditationModalBtn?.addEventListener('click', closeMinorAccreditationModal);
    submitMinorAccreditationBtn?.addEventListener('click', submitMinorAccreditation);
    minorAccreditationModalOverlay?.addEventListener('click', handleMinorAccreditationOverlayClick);

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

    closeReportProfileModal?.addEventListener('click', closeReportProfileModalPanel);
    cancelReportProfile?.addEventListener('click', closeReportProfileModalPanel);
    submitReportProfile?.addEventListener('click', handleSubmitProfileReport);
    reportProfileOverlay?.addEventListener('click', (event) => {
      if (event.target === reportProfileOverlay) closeReportProfileModalPanel();
    });
    document
      .querySelectorAll('input[name="profileReportReason"]')
      .forEach((input) => input.addEventListener('change', handleProfileReportReasonChange));

    closeCommentsModal?.addEventListener('click', closeComments);
    cancelCommentsModal?.addEventListener('click', closeComments);
    sendComment?.addEventListener('click', handleSendComment);
    commentsOverlay?.addEventListener('click', (event) => {
      if (event.target === commentsOverlay) closeComments();
    });

    void (async () => {
      applyProfilePrivacyVisibility(DEFAULT_PROFILE_PRIVACY_VISIBILITY, { isOwner: true });
      try {
        await resolveProfileContext();
      } catch (error) {
        console.error(error);
        setPostsStatus(error.message || 'No se pudo cargar el perfil.', true);
      }

      if (isViewingOwnProfile) {
        await Promise.all([
          loadMinorAccreditationStatus(),
          loadHomeAbout(),
          loadProfilePhoto(),
          loadUsernameState(),
          loadHomePublicWishes(),
          loadHomeCooperativeWishes(),
          loadHomeFulfilledWishes(),
          loadHomePrivateWishes(),
          loadMyStats()
        ]);
        await loadFeed();
        syncProfilePhotoPostFromFeed();
        return;
      }

		      await loadForeignProfilePrivacyVisibility();
		      await Promise.all([
		        loadHomeAbout(activeProfileUserId),
		        loadHomePublicWishes(),
	        loadHomeCooperativeWishes(),
	        loadHomeFulfilledWishes(),
	        loadMyStats(),
	      ]);
	      await loadFeed();
	    })();

    return () => {
      if (selectedFileURL) URL.revokeObjectURL(selectedFileURL);

      openPostModal?.removeEventListener('click', openPost);
      menuPublishBtn?.removeEventListener('click', handleMenuPublishClick);
      homeTopbarBtn?.removeEventListener('click', handleTopbarHomeClick);
      homeAvatarButton?.removeEventListener('click', handleHomeAvatarButtonClick);
      homeAvatarViewBtn?.removeEventListener('click', handleHomeAvatarViewClick);
      homeAvatarUploadBtn?.removeEventListener('click', handleHomeAvatarUploadClick);
      homeAvatarFile?.removeEventListener('change', handleHomeAvatarFileChange);
      homeAvatarGalleryBtn?.removeEventListener('click', openHomeAvatarGalleryModalPanel);
      closeHomeAvatarGalleryModal?.removeEventListener('click', closeHomeAvatarGalleryModalPanel);
      cancelHomeAvatarGalleryModal?.removeEventListener('click', closeHomeAvatarGalleryModalPanel);
      homeAvatarGalleryModalOverlay?.removeEventListener('click', handleHomeAvatarGalleryOverlayClick);
      homeAvatarGalleryGrid?.removeEventListener('click', handleHomeAvatarGalleryPick);
      homeUsernameEditBtn?.removeEventListener('click', openHomeUsernameModalPanel);
      homeUsernameReportBtn?.removeEventListener('click', handleOpenProfileReportModal);
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
      profilePhotoPrevBtn?.removeEventListener('click', handleProfilePhotoPrevNav);
      profilePhotoNextBtn?.removeEventListener('click', handleProfilePhotoNextNav);
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
      toggleMinorProtectedPanelBtn?.removeEventListener('click', handleMinorProtectedToggle);
      openMinorAccreditationModalBtn?.removeEventListener('click', openMinorAccreditationModal);
      closeMinorAccreditationModalBtn?.removeEventListener('click', closeMinorAccreditationModal);
      cancelMinorAccreditationModalBtn?.removeEventListener('click', closeMinorAccreditationModal);
      submitMinorAccreditationBtn?.removeEventListener('click', submitMinorAccreditation);
      minorAccreditationModalOverlay?.removeEventListener('click', handleMinorAccreditationOverlayClick);

      closeDeletePostModal?.removeEventListener('click', closeDeleteModal);
      cancelDeletePost?.removeEventListener('click', closeDeleteModal);
      confirmDeletePost?.removeEventListener('click', handleConfirmDeletePost);

      closeReportPostModal?.removeEventListener('click', closeReportModal);
      cancelReportPost?.removeEventListener('click', closeReportModal);
      submitReportPost?.removeEventListener('click', handleSubmitReport);
      document
        .querySelectorAll('input[name="postReportReason"]')
        .forEach((input) => input.removeEventListener('change', handleReportReasonChange));

      closeReportProfileModal?.removeEventListener('click', closeReportProfileModalPanel);
      cancelReportProfile?.removeEventListener('click', closeReportProfileModalPanel);
      submitReportProfile?.removeEventListener('click', handleSubmitProfileReport);
      document
        .querySelectorAll('input[name="profileReportReason"]')
        .forEach((input) => input.removeEventListener('change', handleProfileReportReasonChange));

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
	      <a class="topbar-btn" href="/gallery.html" data-profile-module="gallery">🖼️ Galería</a>
	      <a class="topbar-btn" href="/my-public-whishes.html" data-profile-module="public_wishes">🌐 Deseos públicos</a>
	      <a class="topbar-btn" href="/my-private-whishes.html">🔒 Deseos privados</a>
	      <a class="topbar-btn" href="/my-fulfilled-whises.html" data-profile-module="fulfilled_wishes">✅ Deseos cumplidos</a>
	    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown" id="profileDropdown">
        <summary class="topbar-avatar-btn" aria-label="Perfil del usuario">
          <img src="/assets/avatar-default.jpg" alt="Perfil de Carlos Jiménez Duarte" data-viewer-avatar />
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
          <a href="/home_user.html" role="menuitem" data-my-home-link="true">Mi Home</a>
          <a href="/achievements.html" role="menuitem" data-profile-module="achievements">Logros recientes</a>
          <a href="/gallery.html" role="menuitem" data-profile-module="gallery">Galería</a>
	          <a href="/calendar.html" role="menuitem" data-profile-module="calendar">Calendario</a>
          <a href="/my-biography.html" role="menuitem" data-profile-module="biography">Mi Biografía</a>
          <a href="/messages.html" role="menuitem">Mensajes</a>
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <section class="cover" id="cover" data-profile-module="cover_purposes">
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
        <a class="nav-pill" href="/home_user.html" title="Home" data-profile-link="true">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas" data-profile-module="stars">
          <span class="nav-icon">⭐</span>
          <span><strong id="homeStarsTotal">0</strong> estrellas</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Seguidores" data-profile-module="followers">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes" data-profile-module="achievements">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería" data-profile-module="gallery">Galería</a>
	        <a class="nav-pill" href="/calendar.html" title="Calendario" data-profile-module="calendar">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía" data-profile-module="biography">Mi biografía</a>
        <a class="nav-pill" href="/messages.html" title="Mensajes">Mensajes</a>
      </nav>

      <section class="profile-grid">
        <aside class="left-col">
          <article class="panel profile-card">
            <div class="profile-row">
              <details class="topbar-dropdown profile-avatar-dropdown" id="homeAvatarDropdown">
                <summary class="profile-avatar-btn" id="homeAvatarButton" aria-label="Foto de perfil" title="Foto de perfil">
                  <img class="avatar profile-avatar-image" src="/assets/avatar-default.jpg" alt="Foto de perfil" data-profile-avatar />
                </summary>
                <div class="dropdown-menu" role="menu">
                  <button class="dropdown-action hidden" id="homeAvatarViewBtn" type="button" role="menuitem">
                    Ver imagen de perfil
                  </button>
                  <button class="dropdown-action" id="homeAvatarUploadBtn" type="button" role="menuitem">
                    Subir imagen de perfil
                  </button>
                  <button class="dropdown-action hidden" id="homeAvatarGalleryBtn" type="button" role="menuitem">
                    Elegir imagen de perfil
                  </button>
                </div>
              </details>
              <input id="homeAvatarFile" type="file" accept="image/*" class="hidden" />
              <div class="profile-meta">
                <h2 class="profile-name" id="homeProfileName">Carlos Jiménez Duarte</h2>
                <p class="profile-rank">Rango 2 · Aprendiz</p>
                <div class="home-username-row">
                  <a class="home-username-link is-empty" id="homeUsernameLink" href="/home_user.html" data-profile-link="true">
                    <span id="homeUsernameValue">@elige-tu-usuario</span>
                  </a>
                  <button class="infobox-edit-btn home-username-edit-btn" id="homeUsernameEditBtn" type="button" title="Modificar nombre de usuario">
                    <img src="/css/icons/iconedit.webp" alt="Editar usuario" />
                  </button>
                  <button class="post-head-btn home-username-report-btn hidden" id="homeUsernameReportBtn" type="button" title="Denunciar perfil" aria-label="Denunciar perfil">
                    🚩
                  </button>
                </div>
                <p class="home-username-cooldown" id="homeUsernameCooldown"></p>
              </div>
            </div>
          </article>

          <article class="panel" id="homeAboutPanel">
            <div class="panel-head home-about-head">
              <h3 class="panel-title">Acerca de mí</h3>
              <button class="infobox-edit-btn home-about-edit-btn" id="homeAboutEditBtn" type="button" title="Modificar acerca de mí">
                <img src="/css/icons/iconedit.webp" alt="Editar" />
              </button>
            </div>
            <p class="panel-muted" id="homeAboutEmptyState">
              Cargando sección "Acerca de mí"...
            </p>
            <p class="panel-text home-about-text hidden" id="homeAboutTextValue"></p>
          </article>

          <article class="panel" id="homeFulfilledPanel">
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

	            <a href="/my-fulfilled-whises.html" class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn" data-profile-module="fulfilled_wishes">Ver más</a>
          </article>

          <article class="panel" id="homePublicPanel">
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

	            <a href="/my-public-whishes.html" class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn" data-profile-module="public_wishes">Ver más</a>
          </article>

          <article class="panel hidden" id="homeCooperativePanel">
            <div class="panel-head">
              <h3 class="panel-title">Deseos cooperativos</h3>
              <span class="panel-badge" id="homeCooperativeWishCount">0 / 20</span>
            </div>

            <ul class="wish-list" id="homeCooperativeWishList"></ul>
            <p class="home-public-wish-status" id="homeCooperativeWishStatus" aria-live="polite"></p>

	            <a
                href="/my-public-whishes.html#cooperative-wishes"
                class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn"
                data-profile-module="public_wishes_cooperative"
              >
                Ver más
              </a>
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

          <article class="panel" id="homeCalendarPanel">
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

	            <a href="/calendar.html" class="btn btn-outline btn-compact btn-inline" data-profile-module="calendar">Ver calendario</a>
          </article>

          <article class="panel" id="homeOraclePanel">
            <div class="panel-head">
              <h3 class="panel-title">Oráculo</h3>
              <span class="panel-badge">Última carta</span>
            </div>

            <div class="oracle-card">
              <img src="assets/oracle-default.jpg" alt="Última carta del Oráculo" />
            </div>

	            <a href="/oracle.html" class="btn btn-outline btn-compact btn-inline" data-profile-module="oracle">Abrir Oráculo</a>
          </article>
        </aside>

        <section class="right-col">
          <article class="panel composer">
            <div class="composer-row">
              <img class="avatar avatar-sm" src="/assets/avatar-default.jpg" alt="Avatar" data-viewer-avatar />
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

          <article class="panel minor-protected-panel hidden" id="minorProtectedPanel">
            <div class="panel-head minor-protected-head">
              <h3 class="panel-title">Cuenta en modo protegido</h3>
              <button class="btn btn-outline btn-compact minor-protected-toggle" id="toggleMinorProtectedPanel" type="button">
                Reducir
              </button>
            </div>
            <div class="minor-protected-body" id="minorProtectedBody">
              <p class="panel-muted">
                Según la fecha de nacimiento registrada, tu perfil requiere validación de un padre, madre o tutor legal para habilitar funciones públicas.
                Puedes usar la plataforma con normalidad, pero tu contenido permanecerá privado hasta completar este proceso.
              </p>
              <p class="panel-muted minor-protected-state" id="minorProtectedStateLabel"></p>
              <div class="minor-protected-actions">
                <button class="btn btn-primary btn-compact" id="openMinorAccreditationModal" type="button">
                  Acreditar cuenta
                </button>
              </div>
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
            <li><a href="/mygamerules.html">Mis reglas de juego</a></li>
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
        <img class="avatar avatar-sm" src="/assets/avatar-default.jpg" alt="Avatar" data-viewer-avatar />
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

<div class="modal-overlay hidden" id="minorAccreditationModalOverlay" aria-hidden="true">
  <div class="modal minor-accreditation-modal" role="dialog" aria-modal="true" aria-label="Acreditar cuenta">
    <div class="modal-head">
      <h3>Acreditar cuenta</h3>
      <button class="modal-close" type="button" id="closeMinorAccreditationModal">✕</button>
    </div>

    <div class="modal-body">
      <p class="panel-muted">
        Registra los datos del padre, madre o tutor legal para enviar la solicitud de validación.
      </p>

      <label class="modal-label" for="minorGuardianPhoneInput">Teléfono del padre, madre o tutor legal</label>
      <input
        class="modal-input"
        id="minorGuardianPhoneInput"
        type="tel"
        maxlength="40"
        placeholder="+57 321 6852619"
      />

      <label class="modal-label" for="minorGuardianEmailInput">Correo electrónico del adulto responsable</label>
      <input
        class="modal-input"
        id="minorGuardianEmailInput"
        type="email"
        maxlength="255"
        placeholder="ejemplo@correo.com"
      />

      <label class="modal-label" for="minorRelationshipSelect">Parentesco</label>
      <select class="modal-select" id="minorRelationshipSelect">
        <option value="padre">Padre</option>
        <option value="madre">Madre</option>
        <option value="tutor_legal">Tutor legal</option>
        <option value="adulto_responsable">Adulto responsable</option>
      </select>

      <p class="minor-accreditation-modal-status" id="minorAccreditationModalStatus" aria-live="polite"></p>
    </div>

    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelMinorAccreditationModal">Cancelar</button>
      <button class="btn btn-primary btn-compact" type="button" id="submitMinorAccreditation">Enviar solicitud</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="profilePhotoPostModalOverlay" aria-hidden="true">
  <div class="modal modal-wide profile-photo-post-modal" role="dialog" aria-modal="true" aria-label="Publicación de foto de perfil">
    <div class="modal-head">
      <h3>Foto de perfil</h3>
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
        <div class="post-media profile-photo-media">
          <button
            class="profile-photo-nav profile-photo-nav-prev hidden"
            type="button"
            id="profilePhotoPrevBtn"
            aria-label="Foto de perfil anterior"
            title="Foto anterior"
          >
            ‹
          </button>
          <img id="profilePhotoPostImage" src="/assets/avatar-default.jpg" alt="Foto de perfil" />
          <button
            class="profile-photo-nav profile-photo-nav-next hidden"
            type="button"
            id="profilePhotoNextBtn"
            aria-label="Foto de perfil siguiente"
            title="Foto siguiente"
          >
            ›
          </button>
        </div>
        <p class="profile-photo-nav-label hidden" id="profilePhotoNavLabel"></p>
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

<div class="modal-overlay hidden" id="homeAvatarGalleryModalOverlay" aria-hidden="true">
  <div class="modal modal-wide avatar-gallery-modal" role="dialog" aria-modal="true" aria-label="Seleccionar foto de perfil">
    <div class="modal-head">
      <h3>Elegir foto de perfil</h3>
      <button class="modal-close" type="button" id="closeHomeAvatarGalleryModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="panel-muted">Selecciona una imagen de tu galería para usarla como foto de perfil.</p>
      <p class="posts-status" id="homeAvatarGalleryStatus" aria-live="polite"></p>
      <div class="avatar-gallery-grid" id="homeAvatarGalleryGrid"></div>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelHomeAvatarGalleryModal">Cancelar</button>
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
          placeholder="tunombredeusuario"
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

<div class="modal-overlay hidden" id="reportProfileModalOverlay" aria-hidden="true">
  <div class="modal wish-modal fulfill-wish-modal" role="dialog" aria-modal="true" aria-label="Reportar perfil">
    <div class="modal-head">
      <h3>Reportar perfil</h3>
      <button class="modal-close" type="button" id="closeReportProfileModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="modal-label-center">
        Selecciona la razón por la cual deseas reportar este perfil.
      </p>
      <div class="report-reasons">
        <label class="report-option"><input type="radio" name="profileReportReason" value="fake_or_illegal" checked /> Perfil falso o contenido ilegal</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="external_manipulation" /> Manipulación hacia otros usuarios en la vida real a través de medios externos a esta plataforma</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="star_manipulation" /> Abuso de publicaciones para atraer estrellas</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="abusive_or_coercive" /> Conducta abusiva o coercitiva</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="wish_system_abuse" /> Uso indebido del sistema de deseos</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="safety_risk" /> Riesgo para la seguridad de otros</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="other" /> Otro (Especificar)</label>
      </div>
      <div id="reportProfileReasonOtherWrap" class="report-other-wrap hidden">
        <label class="modal-label" for="reportProfileReasonOther">Describe la razón</label>
        <textarea class="modal-textarea" id="reportProfileReasonOther" rows="3" placeholder="Escribe tu razón"></textarea>
      </div>
      <p class="infobox-photo-status" id="reportProfileModalStatus" aria-live="polite"></p>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelReportProfile">Cancelar</button>
      <button class="btn btn-primary btn-compact" type="button" id="submitReportProfile">Enviar reporte</button>
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
