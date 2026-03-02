<script>
  import { onMount } from 'svelte';
  import { initPurposeCoverModule } from '../lib/purposeCover';
  import { logout } from '../lib/logout';
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";

  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

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
    const editPostOverlay = document.getElementById('editPostModalOverlay');
    const closeEditPostModal = document.getElementById('closeEditPostModal');
    const cancelEditPost = document.getElementById('cancelEditPost');
    const saveEditPost = document.getElementById('saveEditPost');
    const editPostTextInput = document.getElementById('editPostText');
    const editPostModalStatus = document.getElementById('editPostModalStatus');

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
    const homeAvatarFile = document.getElementById('homeAvatarFile');
    const homeProfileName = document.getElementById('homeProfileName');
    const homeProfileRank = document.getElementById('homeProfileRank');
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
	    const homeCalendarDots = document.getElementById('homeCalendarDots');
	    const homeCalendarMonthName = document.getElementById('homeCalendarMonthName');
	    const homeCalendarMonthProgress = document.getElementById('homeCalendarMonthProgress');
	    const homeCalendarStatus = document.getElementById('homeCalendarStatus');
	    const homeOracleCardImage = document.getElementById('homeOracleCardImage');
	    const homeOracleSummary = document.getElementById('homeOracleSummary');
	    const homeOracleStatus = document.getElementById('homeOracleStatus');
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
    let selectedEditPostId = null;
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
    let homeAvatarProfilePhotoBusy = false;
    let currentAboutDisplayName = (homeProfileName?.textContent || tr('', '', '')).trim();
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
	    const PROFILE_PHOTO_POST_TEXT = tr('', '', '');
	    const DEFAULT_AVATAR_SRC = '/assets/avatar-default.jpg';
	    const DEFAULT_COVER_SRC = '/assets/cover-default.jpg';
	    const ORACLE_BACK_CARD_IMAGE = '/css/oracle/carta.webp';
    const HASHTAG_PATTERN = /(^|[^A-Za-z0-9_])#([A-Za-z0-9_]{2,50})/g;
    const GUARDIAN_RANK_NAMES = Object.freeze({
      0: tr('', '', ''),
      1: tr('', '', ''),
      2: tr('', '', ''),
      3: tr('', '', ''),
      4: tr('', '', ''),
      5: tr('', '', ''),
      6: tr('', '', ''),
      7: tr('', '', ''),
      8: tr('', '', '')
    });
    const MONTH_LABELS = [
      tr('', '', ''),
      tr('', '', ''),
	      tr('', '', ''),
	      tr('', '', ''),
	      tr('', '', ''),
	      tr('', '', ''),
	      tr('', '', ''),
	      tr('', '', ''),
	      tr('', '', ''),
	      tr('', '', ''),
	      tr('', '', ''),
	      tr('', '', '')
	    ];
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

    const normalizeGuardianRank = (value) => {
      const parsed = Number(value);
      if (!Number.isFinite(parsed)) return 0;
      return Math.max(0, Math.trunc(parsed));
    };

    const formatGuardianRankLabel = (value) => {
      const rank = normalizeGuardianRank(value);
      const rankName = GUARDIAN_RANK_NAMES[rank] || tr(`Rango ${rank}`, `Rank ${rank}`, `Rank ${rank}`);
      return tr(`Rango ${rank} · ${rankName}`, `Rank ${rank} · ${rankName}`, `Rank ${rank} · ${rankName}`);
    };

    const applyHomeProfileRank = (value) => {
      if (!homeProfileRank) return;
      const rank = normalizeGuardianRank(value);
      if (rank <= 0) {
        homeProfileRank.textContent = "";
        homeProfileRank.classList.add("hidden");
        return;
      }
      homeProfileRank.classList.remove("hidden");
      homeProfileRank.textContent = formatGuardianRankLabel(rank);
    };

	    const escapeHtml = (value) =>
	      (value || '')
	        .replaceAll('&', '&amp;')
	        .replaceAll('<', '&lt;')
	        .replaceAll('>', '&gt;')
	        .replaceAll('"', '&quot;')
	        .replaceAll("'", '&#39;');

	    const normalizeHashtag = (value) =>
	      String(value || '')
	        .trim()
	        .toLowerCase()
	        .replace(/^#+/, '')
	        .replace(/[^a-z0-9_]/g, '');

	    const buildFeedHashtagHref = (value) => {
	      const normalized = normalizeHashtag(value);
	      if (!normalized) return '/feed.html';
	      return `/feed.html?search=%23${encodeURIComponent(normalized)}`;
	    };

	    const renderPlainTextWithHashtags = (value) => {
	      const text = String(value || '');
	      if (!text) return '';

	      HASHTAG_PATTERN.lastIndex = 0;
	      let cursor = 0;
	      let html = '';
	      let match;
	      while ((match = HASHTAG_PATTERN.exec(text)) !== null) {
	        const full = String(match[0] || '');
	        const prefix = full.startsWith('#') ? '' : full[0];
	        const tag = String(match[2] || '').trim();
	        if (!tag) continue;

	        const token = `#${tag}`;
	        const tokenStart = Number(match.index) + prefix.length;
	        if (tokenStart < cursor) continue;

	        html += escapeHtml(text.slice(cursor, Number(match.index)));
	        html += escapeHtml(prefix);
	        html += `<a class="post-hashtag-link" href="${escapeHtml(buildFeedHashtagHref(tag))}">${escapeHtml(token)}</a>`;
	        cursor = tokenStart + token.length;
	      }

	      html += escapeHtml(text.slice(cursor));
	      return html;
	    };

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
      if (status === 'requested') return tr('', '', '');
      if (status === 'pending') return tr('', '', '');
      if (status === 'approved') return tr('', '', '');
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

	    const setMinorProtectedCollapsedState = (collapsed) => {
	      minorProtectedCollapsed = Boolean(collapsed);
	      if (minorProtectedBody) {
	        minorProtectedBody.classList.toggle('hidden', minorProtectedCollapsed);
	      }
	      if (toggleMinorProtectedPanelBtn) {
	        toggleMinorProtectedPanelBtn.textContent = minorProtectedCollapsed
            ? tr('', '', '')
            : tr('', '', '');
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

	      setMinorProtectedCollapsedState(minorProtectedCollapsed);
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
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
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
        setMinorAccreditationModalStatus(
          tr('Debes indicar el teléfono del adulto responsable.', "You must enter the responsible adult's phone number."),
          true
        );
        return;
      }
      if (!guardianEmail) {
        setMinorAccreditationModalStatus(
          tr('Debes indicar el correo del adulto responsable.', "You must enter the responsible adult's email."),
          true
        );
        return;
      }

      const oldLabel = submitMinorAccreditationBtn?.textContent || tr('', '', '');
      if (submitMinorAccreditationBtn) {
        submitMinorAccreditationBtn.disabled = true;
        submitMinorAccreditationBtn.textContent = tr('', '', '');
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
          throw new Error(data.detail || tr('', '', ''));
        }

        await loadMinorAccreditationStatus();
        setMinorAccreditationModalStatus(
          data.message ||
            tr(
              'Solicitud enviada. Revisa con el adulto responsable el correo de validación.',
              'Request sent. Ask the responsible adult to check the validation email.'
            ),
          false
        );
      } catch (error) {
        setMinorAccreditationModalStatus(
          error.message || tr('', '', ''),
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

	    const setHomeCalendarStatus = (message, isError = false) => {
	      if (!homeCalendarStatus) return;
	      homeCalendarStatus.textContent = message || '';
	      homeCalendarStatus.classList.toggle('is-error', Boolean(isError));
	    };

	    const setHomeOracleStatus = (message, isError = false) => {
	      if (!homeOracleStatus) return;
	      homeOracleStatus.textContent = message || '';
	      homeOracleStatus.classList.toggle('is-error', Boolean(isError));
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
      return dateValue.toLocaleDateString(isEn ? 'en-US' : isFr ? 'fr-FR' : 'es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    };

    const toIsoDateUtc = (value) => {
      if (!value) return '';
      if (typeof value === 'string') {
        const normalized = value.trim();
        if (/^\d{4}-\d{2}-\d{2}$/.test(normalized)) return normalized;
        const parsed = new Date(normalized);
        if (Number.isNaN(parsed.getTime())) return '';
        return parsed.toISOString().slice(0, 10);
      }
      if (value instanceof Date) {
        if (Number.isNaN(value.getTime())) return '';
        return value.toISOString().slice(0, 10);
      }
      return '';
    };

    const formatHomeCalendarDayLabel = (isoDate) => {
      const normalized = toIsoDateUtc(isoDate);
      if (!normalized) return '';
      try {
        const dateValue = new Date(`${normalized}T00:00:00Z`);
        return new Intl.DateTimeFormat(isEn ? 'en-US' : isFr ? 'fr-FR' : 'es-CO', {
          day: 'numeric',
          month: 'long',
          year: 'numeric',
          timeZone: 'UTC'
        }).format(dateValue);
      } catch {
        return normalized;
      }
    };

    const buildHomeCalendarMonth = ({ year, monthIndex, items, todayIsoDate }) => {
      const safeYear = Number.isFinite(Number(year)) ? Number(year) : new Date().getUTCFullYear();
      const safeMonthIndex = Math.max(0, Math.min(11, Number(monthIndex || 0)));
      const totalDays = new Date(Date.UTC(safeYear, safeMonthIndex + 1, 0)).getUTCDate();
      const firstWeekday = (new Date(Date.UTC(safeYear, safeMonthIndex, 1)).getUTCDay() + 6) % 7;
      const itemMap = new Map(
        (Array.isArray(items) ? items : []).map((item) => [toIsoDateUtc(item?.date_utc), item])
      );

      let activeDays = 0;
      const days = [];
      for (let day = 1; day <= totalDays; day += 1) {
        const isoDate = `${safeYear}-${String(safeMonthIndex + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const item = itemMap.get(isoDate);
        const posts = Math.max(0, Number(item?.posts || 0));
        const hasPosts = posts > 0;
        if (hasPosts) activeDays += 1;

        days.push({
          date_utc: isoDate,
          posts,
          hasPosts,
          isToday: isoDate === todayIsoDate
        });
      }

      return {
        name: MONTH_LABELS[safeMonthIndex] || tr('', '', ''),
        activeDays,
        totalDays,
        padding: Array.from({ length: firstWeekday }, (_, idx) => `pad-${safeYear}-${safeMonthIndex + 1}-${idx}`),
        days
      };
    };

    const renderHomeCalendarMonth = (monthData) => {
      if (!homeCalendarDots) return;

      const monthName = String(monthData?.name || tr('', '', ''));
      const activeDays = Math.max(0, Number(monthData?.activeDays || 0));
      const totalDays = Math.max(0, Number(monthData?.totalDays || 0));
      const padding = Array.isArray(monthData?.padding) ? monthData.padding : [];
      const days = Array.isArray(monthData?.days) ? monthData.days : [];

      if (homeCalendarMonthName) homeCalendarMonthName.textContent = monthName;
      if (homeCalendarMonthProgress) homeCalendarMonthProgress.textContent = `${activeDays} / ${totalDays}`;

      const dotsHtml = [
        ...padding.map(
          (padKey) => `<span class="month-dot is-pad" aria-hidden="true" data-key="${escapeHtml(String(padKey))}"></span>`
        ),
        ...days.map((day) => {
          const posts = Math.max(0, Number(day?.posts || 0));
          const hasPosts = posts > 0;
          const postsLabel = posts === 1
            ? tr('', '', '')
            : tr(`${posts} publicaciones`, `${posts} posts`, `${posts} posts`);
          const dayLabel = formatHomeCalendarDayLabel(day?.date_utc) || String(day?.date_utc || '');
          const title = `${dayLabel} · ${postsLabel}`;
          const stateClass = hasPosts ? 'is-active' : 'is-idle';
          const todayClass = day?.isToday ? ' is-today' : '';
          return `<button class="month-dot-btn ${stateClass}${todayClass}" type="button" disabled title="${escapeHtml(title)}" aria-label="${escapeHtml(title)}"></button>`;
        })
      ];
      homeCalendarDots.innerHTML = dotsHtml.join('');
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

	    const truncateText = (value, maxLength = 220) => {
	      const normalized = String(value || '').replace(/\s+/g, ' ').trim();
	      if (!normalized) return '';
	      if (normalized.length <= maxLength) return normalized;
	      return `${normalized.slice(0, Math.max(1, maxLength - 1)).trimEnd()}...`;
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

	    const applyCoverState = (payload) => {
	      const coverImage = document.getElementById('coverImg');
	      if (!coverImage) return;
	      const coverUrl = String(payload?.url || '').trim() || DEFAULT_COVER_SRC;
	      const offsetX = Number(payload?.offset_x || 0) || 0;
	      const offsetY = Number(payload?.offset_y || 0) || 0;
	      coverImage.src = coverUrl;
	      coverImage.style.objectPosition = `calc(50% + ${offsetX}px) calc(50% + ${offsetY}px)`;
	    };

	    const loadHomeCover = async (userId = null) => {
	      const profileId = Number(userId);
	      const endpoint = !isViewingOwnProfile && Number.isFinite(profileId) && profileId > 0
	        ? `/media/cover-photo/user/${encodeURIComponent(String(profileId))}`
	        : '/media/cover-photo';
	      try {
	        const res = await apiFetch(endpoint);
	        const data = await res.json();
	        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
	        applyCoverState(data);
	      } catch (error) {
	        console.error(error);
	        applyCoverState({ url: DEFAULT_COVER_SRC, offset_x: 0, offset_y: 0 });
	      }
	    };

	    const setProfilePhotoPostId = (postId) => {
	      const normalized = Number(postId);
	      profilePhotoPostId = Number.isFinite(normalized) && normalized > 0 ? normalized : null;
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
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        applyProfilePrivacyVisibility(data);
      } catch (error) {
        console.error(error);
        applyProfilePrivacyVisibility(DEFAULT_PROFILE_PRIVACY_VISIBILITY);
      }
    };

    const updateHomeAboutWordCounter = () => {
      if (!homeAboutWordCounter) return;
      const words = countWords(homeAboutInput?.value || '');
      homeAboutWordCounter.textContent = isEn || isFr
        ? `${words} / ${HOME_ABOUT_MAX_WORDS} words`
        : `${words} / ${HOME_ABOUT_MAX_WORDS} palabras`;
      homeAboutWordCounter.classList.toggle('is-error', words > HOME_ABOUT_MAX_WORDS);
    };

	    minorProtectedCollapsed = false;

    const relativeTime = (isoDate) => {
      const ts = Date.parse(isoDate);
      if (Number.isNaN(ts)) return tr('', '', '');
      const minutes = Math.floor((Date.now() - ts) / 60000);
      if (minutes < 1) return tr('', '', '');
      if (minutes < 60) return isEn || isFr ? `${minutes} min ago` : `hace ${minutes} min`;
      const hours = Math.floor(minutes / 60);
      if (hours < 24) return isEn || isFr ? `${hours} h ago` : `hace ${hours} h`;
      const days = Math.floor(hours / 24);
      return isEn || isFr ? `${days} day${days > 1 ? 's' : ''} ago` : `hace ${days} dia${days > 1 ? 's' : ''}`;
    };

    const apiFetch = async (path, options = {}) => {
      const token = getAccessToken();
      if (!token) {
        window.location.href = '/login.html';
	        throw new Error(tr('', '', ''));
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
	        throw new Error(tr('', '', ''));
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
        throw new Error(data.detail || tr('', '', ''));
      }
      const userId = Number(data?.user_number);
      const guardianRank = normalizeGuardianRank(data?.guardian_rank);
      return {
        user_id: Number.isFinite(userId) && userId > 0 ? userId : null,
        username: normalizeUsername(data?.username || ''),
        guardian_rank: guardianRank
      };
    };

    const fetchFollowProfile = async ({ userId = null, username = null } = {}) => {
      const idValue = Number(userId);
      const usernameValue = normalizeUsername(username || '');
      if (Number.isFinite(idValue) && idValue > 0) {
        const res = await apiFetch(`/follows/profile?user_id=${encodeURIComponent(String(idValue))}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        return data;
      }
      if (usernameValue) {
        const res = await apiFetch(`/follows/profile?username=${encodeURIComponent(usernameValue)}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        return data;
      }
      throw new Error(tr('', '', ''));
    };

    const applyForeignProfileHeader = (profile) => {
      const profileId = Number(profile?.user_id);
      activeProfileUserId = Number.isFinite(profileId) && profileId > 0 ? profileId : null;
      activeProfileUsername = normalizeUsername(profile?.username || '');
      activeProfileUrl = String(profile?.profile_url || '').trim() || '/home_user.html';

      const handleText =
        String(profile?.handle || '').trim() ||
	        (activeProfileUsername ? `@${activeProfileUsername}` : activeProfileUserId ? `@id${activeProfileUserId}` : tr('', '', ''));

      if (homeUsernameValue) homeUsernameValue.textContent = handleText;
      if (homeUsernameLink) {
        homeUsernameLink.href = activeProfileUrl;
        homeUsernameLink.classList.toggle('is-empty', false);
      }
      if (homeUsernameCooldown) homeUsernameCooldown.textContent = '';
      applyHomeProfileRank(profile?.guardian_rank);

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
        applyHomeProfileRank(me.guardian_rank);
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
      const displayName =
        (about?.display_name || '').trim() ||
        (homeProfileName?.textContent || '').trim() ||
        tr('', '', '');
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
          ? tr('', '', '')
          : tr('', '', '');
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
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        applyHomeAbout(data);
      } catch (error) {
        console.error(error);
        if (homeAboutTextValue) {
          homeAboutTextValue.textContent = '';
          homeAboutTextValue.classList.add('hidden');
        }
        if (homeAboutEmptyState) {
          const reason = String(error?.message || '').trim();
	          if (
            !isViewingOwnProfile
            && (reason.toLowerCase().includes('oculta por privacidad') || reason.toLowerCase().includes('hidden by privacy'))
          ) {
            homeAboutEmptyState.textContent = tr(
              'Este usuario decidió ocultar su sección "Acerca de mí".',
              'This user chose to hide their "About me" section.'
            );
          } else {
            homeAboutEmptyState.textContent = isViewingOwnProfile
              ? tr('', '', '')
              : tr('', '', '');
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

      if (!hasMany) {
        if (profilePhotoPrevBtn) profilePhotoPrevBtn.disabled = true;
        if (profilePhotoNextBtn) profilePhotoNextBtn.disabled = true;
        return;
      }

      const safeIndex = Math.max(0, Math.min(total - 1, Number(profilePhotoHistoryIndex) || 0));
      profilePhotoHistoryIndex = safeIndex;

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
          profilePhotoPostMeta.textContent = tr('', '', '');
        } else {
          profilePhotoPostMeta.textContent = `· ${relativeTime(post.created_at)} · ${
            post.visibility === 'private' ? tr('', '', '') : tr('', '', '')
          }`;
        }
      }
      if (profilePhotoStarPost) {
        const starredByMe = Boolean(post?.starred_by_me);
        const isMine = Boolean(post?.is_mine);
        const starCount = Number(post?.star_count || 0);
        profilePhotoStarPost.disabled = !post || starredByMe || isMine;
        profilePhotoStarPost.textContent = starredByMe
          ? `⭐ ${tr('', '', '')} (${starCount})`
          : `⭐ ${tr('', '', '')} (${starCount})`;
      }
      if (profilePhotoCommentPost) {
        profilePhotoCommentPost.disabled = !post;
        profilePhotoCommentPost.textContent = `💬 ${tr('', '', '')} (${Number(post?.comment_count || 0)})`;
      }
      if (profilePhotoSharePost) {
        profilePhotoSharePost.disabled = !post;
        profilePhotoSharePost.textContent = `🔁 ${tr('', '', '')} (${Number(post?.share_count || 0)})`;
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
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        profilePhotoMediaId = data.media_id || null;
        setHomeAvatarSource(data.url || DEFAULT_AVATAR_SRC);
      } catch (error) {
        console.error(error);
      }
    };

    const closeHomeAvatarDropdown = () => {
      homeAvatarDropdown?.removeAttribute('open');
    };

    const refreshHomeAvatarMenuOptions = () => {
      const hasProfilePhoto = Boolean(profilePhotoMediaId);
      homeAvatarViewBtn?.classList.toggle('hidden', !hasProfilePhoto);
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
      if (homeUsernameValue) {
        homeUsernameValue.textContent = hasUsername ? `@${username}` : tr('', '', '');
      }
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
          homeUsernameCooldown.textContent = tr('', '', '');
        } else if (state?.cooldown_until) {
          homeUsernameCooldown.textContent = tr(
            `Podrás cambiarlo nuevamente el ${formatIsoDate(state.cooldown_until)}.`,
            `You can change it again on ${formatIsoDate(state.cooldown_until)}.`
          );
        } else {
          homeUsernameCooldown.textContent = tr('', '', '');
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
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        applyUsernameState(data);
      } catch (error) {
        console.error(error);
      }
    };

    const updateUsernamePreview = () => {
      if (!homeUsernamePreview) return;
      const normalized = normalizeUsername(homeUsernameInput?.value || '');
      homeUsernamePreview.textContent = normalized
        ? tr(
          `Enlace: ${window.location.origin}/home_user.html?u=${normalized}`,
          `Link: ${window.location.origin}/home_user.html?u=${normalized}`
        )
        : tr('', '', '');
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
      if (!username) return tr('', '', '');
      if (username.length < USERNAME_MIN_LENGTH || username.length > USERNAME_MAX_LENGTH) {
        return tr(
          `El nombre de usuario debe tener entre ${USERNAME_MIN_LENGTH} y ${USERNAME_MAX_LENGTH} caracteres.`,
          `Username must be between ${USERNAME_MIN_LENGTH} and ${USERNAME_MAX_LENGTH} characters.`
        );
      }
      if (!USERNAME_PATTERN.test(username)) {
        return tr(
          'Usa solo letras minúsculas, números, punto o guión bajo.',
          'Use only lowercase letters, numbers, dot, or underscore.'
        );
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

      const oldLabel = saveHomeUsernameBtn?.textContent || tr('', '', '');
      if (saveHomeUsernameBtn) {
        saveHomeUsernameBtn.disabled = true;
        saveHomeUsernameBtn.textContent = tr('', '', '');
      }

      try {
        const res = await apiFetch(`/auth/username/check?username=${encodeURIComponent(candidate)}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        if (!data.available) {
          setHomeUsernameModalStatus(
            data.detail || tr('', '', ''),
            true
          );
          homeUsernameConfirmWrap?.classList.add('hidden');
          pendingUsername = '';
          return;
        }

        pendingUsername = candidate;
        if (homeUsernameConfirmText) {
          homeUsernameConfirmText.textContent = tr(
            `¿Estás seguro de que deseas este nombre de usuario: @${candidate}?`,
            `Are you sure you want this username: @${candidate}?`
          );
        }
        homeUsernameConfirmWrap?.classList.remove('hidden');
        setHomeUsernameModalStatus('');
      } catch (error) {
        setHomeUsernameModalStatus(error.message || tr('', '', ''), true);
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
        setHomeUsernameModalStatus(
          tr('', '', ''),
          true
        );
        return;
      }

      const oldLabel = confirmHomeUsernameBtn?.textContent || tr('', '', '');
      if (confirmHomeUsernameBtn) {
        confirmHomeUsernameBtn.disabled = true;
        confirmHomeUsernameBtn.textContent = tr('', '', '');
      }

      try {
        const res = await apiFetch('/auth/username', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: pendingUsername })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        applyUsernameState(data.state || null);
        closeHomeUsernameModalPanel();
        setPostsStatus(
          tr(
            `Tu nombre de usuario ahora es @${data?.state?.username || pendingUsername}.`,
            `Your username is now @${data?.state?.username || pendingUsername}.`
          )
        );
      } catch (error) {
        setHomeUsernameModalStatus(error.message || tr('', '', ''), true);
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
            <span class="wish-item-label">${escapeHtml(tr('', '', ''))}</span>
          </li>
        `;
        return;
      }

      homePublicWishList.innerHTML = topSeven
        .map((wish) => {
          const wishText = escapeHtml(wish?.wish_text || tr('', '', ''));
          const mediaUrl = (wish?.media_url || '').trim();
          const mediaHtml = mediaUrl
            ? `<img class="wish-item-thumb" src="${escapeHtml(mediaUrl)}" alt="${escapeHtml(tr('', '', ''))}" loading="lazy" />`
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
          const wishText = escapeHtml(
            wish?.wish_text || tr('', '', '')
          );
          const mediaUrl = (wish?.media_url || '').trim();
          const mediaHtml = mediaUrl
            ? `<img class="wish-item-thumb" src="${escapeHtml(mediaUrl)}" alt="${escapeHtml(tr('', '', ''))}" loading="lazy" />`
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
	        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
	        renderHomePublicWishes(data?.items || [], data?.active_count || 0, data?.active_limit || 50);
	        setHomePublicWishStatus('');
      } catch (error) {
        renderHomePublicWishes([], 0, 50);
        setHomePublicWishStatus(error.message || tr('', '', ''), true);
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
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        renderHomeCooperativeWishes(data?.items || [], data?.active_count || 0, data?.active_limit || 20);
        setHomeCooperativeWishStatus('');
      } catch (error) {
        hasActiveCooperativeWishes = false;
        updateHomeCooperativePanelVisibility();
        renderHomeCooperativeWishes([], 0, 20);
        setHomeCooperativeWishStatus(error.message || tr('', '', ''), true);
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
          ? isEn
            ? `${topSeven.length} of ${safeTotal}`
            : `${topSeven.length} de ${safeTotal}`
          : isEn
            ? `${topSeven.length} recent`
            : `${topSeven.length} recientes`;
      }

      if (topSeven.length === 0) {
        homeFulfilledWishList.innerHTML = `
          <li class="wish-item wish-item-home-public wish-item-empty">
            <span class="wish-dot"></span>
            <span class="wish-item-label">${escapeHtml(tr('', '', ''))}</span>
          </li>
        `;
        return;
      }

      homeFulfilledWishList.innerHTML = topSeven
        .map((wish) => {
          const wishText = escapeHtml(wish?.wish_text || tr('', '', ''));
          const mediaUrl = (wish?.fulfilled_evidence_media_url || wish?.media_url || '').trim();
          const mediaHtml = mediaUrl
            ? `<img class="wish-item-thumb" src="${escapeHtml(mediaUrl)}" alt="${escapeHtml(tr('', '', ''))}" loading="lazy" />`
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
	        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
	        renderHomeFulfilledWishes(data?.items || [], data?.total || 0);
	        setHomeFulfilledWishStatus('');
      } catch (error) {
        renderHomeFulfilledWishes([], 0);
        setHomeFulfilledWishStatus(error.message || tr('', '', ''), true);
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
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        renderHomePrivateWishSummary(data?.active_count || 0, data?.active_limit || 50);
        setHomePrivateWishStatus('');
      } catch (error) {
        renderHomePrivateWishSummary(0, 50);
        setHomePrivateWishStatus(error.message || tr('', '', ''), true);
      }
    };

	    const loadHomeCalendar = async () => {
	      if (!homeCalendarDots) return;

      const fallbackTodayIso = new Date().toISOString().slice(0, 10);
      const fallbackYear = Number(fallbackTodayIso.slice(0, 4));
      const fallbackMonthIndex = Math.max(0, Math.min(11, Number(fallbackTodayIso.slice(5, 7)) - 1));
      const renderFallbackCalendar = () => {
        const fallbackMonth = buildHomeCalendarMonth({
          year: fallbackYear,
          monthIndex: fallbackMonthIndex,
          items: [],
          todayIsoDate: fallbackTodayIso
        });
        renderHomeCalendarMonth(fallbackMonth);
      };

      if (!isViewingOwnProfile && !activeProfilePrivacyVisibility.public_profile_show_calendar) {
        renderFallbackCalendar();
        setHomeCalendarStatus('');
        return;
      }

      setHomeCalendarStatus(tr('', '', ''));
      renderFallbackCalendar();

      try {
        const profileId = Number(activeProfileUserId);
        if (!isViewingOwnProfile && (!Number.isFinite(profileId) || profileId <= 0)) {
          throw new Error(tr('', '', ''));
        }

        const requestYear = new Date().getUTCFullYear();
        const endpoint = !isViewingOwnProfile
          ? `/calendar/user/${encodeURIComponent(String(profileId))}?year=${encodeURIComponent(String(requestYear))}`
          : `/calendar/mine?year=${encodeURIComponent(String(requestYear))}`;

        const res = await apiFetch(endpoint);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));

        const todayIso = toIsoDateUtc(data?.today_utc) || fallbackTodayIso;
        const monthYear = Number(todayIso.slice(0, 4)) || requestYear;
        const monthIndex = Math.max(0, Math.min(11, Number(todayIso.slice(5, 7)) - 1));
        const monthData = buildHomeCalendarMonth({
          year: monthYear,
          monthIndex,
          items: Array.isArray(data?.items) ? data.items : [],
          todayIsoDate: todayIso
        });

        renderHomeCalendarMonth(monthData);
        setHomeCalendarStatus('');
      } catch (error) {
        renderFallbackCalendar();
        setHomeCalendarStatus(error?.message || tr('', '', ''), true);
	      }
	    };

	    const getOracleCardImage = (cardId) => `/css/oracle/Oracle${cardId}.webp`;

	    const applyHomeOracleNoSelectionState = (summaryText) => {
	      if (homeOracleCardImage) {
	        homeOracleCardImage.src = ORACLE_BACK_CARD_IMAGE;
	        homeOracleCardImage.alt = tr('', '', '');
	      }
	      if (homeOracleSummary) {
	        homeOracleSummary.textContent =
	          summaryText || tr(
            'Conoce El Oráculo y elige tu primera carta para reflexionar sobre tu presente.',
            'Discover the Oracle and choose your first card to reflect on your present.'
          );
	      }
	    };

	    const loadHomeOracle = async () => {
	      if (!homeOracleCardImage) return;

		      if (!isViewingOwnProfile && !activeProfilePrivacyVisibility.public_profile_show_oracle) {
		        applyHomeOracleNoSelectionState(tr('', '', ''));
		        setHomeOracleStatus('');
		        return;
		      }

		      setHomeOracleStatus(tr('', '', ''));
	      applyHomeOracleNoSelectionState('');

	      try {
	        const profileId = Number(activeProfileUserId);
	        if (!isViewingOwnProfile && (!Number.isFinite(profileId) || profileId <= 0)) {
		          throw new Error(tr('', '', ''));
	        }

	        const endpoint = isViewingOwnProfile
	          ? '/oracle/state'
	          : `/oracle/public/${encodeURIComponent(String(profileId))}`;
	        const res = await apiFetch(endpoint);
	        const data = await res.json();
		        if (!res.ok) throw new Error(data.detail || tr('', '', ''));

	        const responses = Array.isArray(data?.responses) ? data.responses : [];
	        const latest = responses.find((entry) => {
	          const cardId = Number(entry?.card_id || 0);
	          return Number.isFinite(cardId) && cardId >= 1 && cardId <= 30;
	        });

	        if (!latest) {
	          applyHomeOracleNoSelectionState(
	            isViewingOwnProfile
		              ? tr(
                    'Conoce El Oráculo y elige tu primera carta para reflexionar sobre tu presente.',
                    'Discover the Oracle and choose your first card to reflect on your present.'
                  )
		              : tr('', '', '')
		          );
	          setHomeOracleStatus('');
	          return;
	        }

	        const cardId = Number(latest?.card_id || 0);
	        const responseType = String(latest?.response_type || '').trim().toLowerCase();
	        const textPublic = String(latest?.text_public || '').trim();

	        homeOracleCardImage.src = getOracleCardImage(cardId);
		        homeOracleCardImage.alt = tr(
              `Carta más reciente elegida en El Oráculo (${cardId})`,
              `Most recent card chosen in the Oracle (${cardId})`
            );

	        if (responseType === 'public' && textPublic) {
	          if (homeOracleSummary) homeOracleSummary.textContent = truncateText(textPublic);
	        } else if (responseType === 'secret' && isViewingOwnProfile) {
		          if (homeOracleSummary) {
                homeOracleSummary.textContent = tr(
                  'Tu respuesta a esta carta está guardada en secreto en tu Vault.',
                  'Your response to this card is stored in secret in your Vault.'
                );
              }
		        } else if (responseType === 'heart' && isViewingOwnProfile) {
		          if (homeOracleSummary) {
                homeOracleSummary.textContent = tr(
                  'Elegiste dejar esta carta reposando en tu corazón.',
                  'You chose to let this card rest in your heart.'
                );
              }
		        } else {
		          if (homeOracleSummary) {
                homeOracleSummary.textContent = tr(
                  'Esta es la carta más reciente que se eligió en El Oráculo.',
                  'This is the most recent card chosen in the Oracle.'
                );
              }
		        }

	        setHomeOracleStatus('');
	      } catch (error) {
	        applyHomeOracleNoSelectionState(
	          isViewingOwnProfile
		            ? tr(
                  'Conoce El Oráculo y elige tu primera carta para reflexionar sobre tu presente.',
                  'Discover the Oracle and choose your first card to reflect on your present.'
                )
		            : tr('', '', '')
		        );
		        setHomeOracleStatus(error?.message || tr('', '', ''), true);
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
            album_name: String(post?.album_name || '').trim() || tr(`Álbum ${albumId}`, `Album ${albumId}`, `Album ${albumId}`),
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

	    const renderPostTextHtml = (post) => {
	      const text = String(post?.text || '');
	      if (!text) return '';

      const mentions = Array.isArray(post?.mentions)
        ? post.mentions
            .filter((item) => Number.isFinite(Number(item?.start_index)) && Number.isFinite(Number(item?.end_index)))
            .map((item) => ({
              start_index: Number(item.start_index),
              end_index: Number(item.end_index),
              profile_url: String(item?.profile_url || '').trim(),
              is_active: Boolean(item?.is_active)
            }))
            .sort((a, b) => a.start_index - b.start_index || a.end_index - b.end_index)
        : [];

	      if (!mentions.length) return renderPlainTextWithHashtags(text);

      let cursor = 0;
      let html = '';
      for (const mention of mentions) {
        const start = Math.max(0, mention.start_index);
        const end = Math.min(text.length, Math.max(start, mention.end_index));
        if (start < cursor || end <= start) continue;

	        html += renderPlainTextWithHashtags(text.slice(cursor, start));
	        const fragment = text.slice(start, end);
	        if (mention.is_active && mention.profile_url) {
	          html += `<a class="post-mention-link" href="${escapeHtml(mention.profile_url)}">${escapeHtml(fragment)}</a>`;
	        } else {
	          html += escapeHtml(fragment);
	        }
	        cursor = end;
	      }
	      html += renderPlainTextWithHashtags(text.slice(cursor));
	      return html;
	    };

	    const renderPosts = (posts) => {
	      if (!postsList) return;
	      const displayPosts = buildDisplayPosts(posts);

      if (!Array.isArray(displayPosts) || displayPosts.length === 0) {
        postsList.innerHTML = `
          <article class="panel post post-empty">
            <p class="post-text">${escapeHtml(tr('', '', ''))}</p>
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
                  : `<img src="${escapeHtml(albumPost.media_url || '')}" alt="${escapeHtml(tr('', '', ''))}" loading="lazy" />`;
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
              <div class="post-album-grid" aria-label="${escapeHtml(tr('', '', ''))}">
                ${previewHtml}
              </div>
            `;
          } else {
            mediaHtml = post.media_url
              ? post.media_kind === 'video'
                ? `<div class="post-media"><video src="${post.media_url}" controls></video></div>`
                : `<div class="post-media"><img src="${post.media_url}" alt="${escapeHtml(tr('', '', ''))}" /></div>`
              : '';
          }

          const starDisabled = post.starred_by_me || post.is_mine ? 'disabled' : '';
          const starLabel = post.starred_by_me
            ? `⭐ ${tr('', '', '')} (${post.star_count})`
            : `⭐ ${tr('', '', '')} (${post.star_count})`;
          const reportBtn = post.is_mine
            ? ''
            : `<button class="post-head-btn" type="button" data-action="report-post" data-post-id="${post.id}" title="${escapeHtml(tr('', '', ''))}">🚩</button>`;
          const editBtn = post.is_mine
            ? `<button class="post-head-btn" type="button" data-action="edit-post" data-post-id="${post.id}" title="${escapeHtml(tr('', '', ''))}">📝</button>`
            : '';
          const deleteBtn = post.is_mine
            ? `<button class="post-head-btn" type="button" data-action="delete-post" data-post-id="${post.id}" title="${escapeHtml(tr('', '', ''))}">🗑</button>`
            : '';
          const albumMeta = isAlbumGroup
            ? `<p class="post-album-meta">${escapeHtml(post.album_name || tr('', '', ''))} · ${Number(post.album_total_items || 0)} ${escapeHtml(tr('', '', ''))}</p>`
            : '';
		          const openAlbumBtn = isAlbumGroup
		            ? `<button class="post-btn" type="button" data-action="open-album-gallery" data-album-id="${Number(post.album_id || 0)}">🖼️ ${escapeHtml(tr('', '', ''))} (${Number(post.album_total_items || 0)})</button>`
		            : '';
		          const authorProfileUrl = escapeHtml(String(post?.__author_profile_url || buildAuthorProfileUrl(post?.author)));
		          const authorName = escapeHtml(post?.author?.name || tr('', '', ''));
		          const authorAvatarUrl = escapeHtml(String(post?.__author_avatar_url || DEFAULT_AVATAR_SRC).trim() || DEFAULT_AVATAR_SRC);

	          return `
	            <article class="panel post" data-post-id="${post.id}">
	              <div class="post-head">
	                <div class="post-head-author">
	                  <a class="post-author-avatar-link" href="${authorProfileUrl}">
		                    <img class="post-author-avatar" src="${authorAvatarUrl}" alt="${escapeHtml(tr('', '', ''))} ${authorName}" loading="lazy" />
	                  </a>
	                  <div class="post-head-main">
	                    <a class="post-author-link" href="${authorProfileUrl}">${authorName}</a>
		                    <span class="post-meta">· ${relativeTime(post.created_at)} · ${post.visibility === 'private' ? tr('', '', '') : tr('', '', '')}</span>
	                  </div>
	                </div>
	                <div class="post-head-actions">
	                  ${reportBtn}
	                  ${editBtn}
	                  ${deleteBtn}
	                </div>
              </div>
              ${albumMeta}
              ${post.text ? `<p class="post-text">${renderPostTextHtml(post)}</p>` : ''}
              ${mediaHtml}
              <div class="post-actions">
                <button class="post-btn" type="button" data-action="star-post" data-post-id="${post.id}" ${starDisabled}>${starLabel}</button>
	                <button class="post-btn" type="button" data-action="comment-post" data-post-id="${post.id}">💬 ${escapeHtml(tr('', '', ''))} (${post.comment_count})</button>
	                <button class="post-btn" type="button" data-action="share-post" data-post-id="${post.id}">🔁 ${escapeHtml(tr('', '', ''))} (${post.share_count})</button>
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
            starsTotalLabel.textContent = Number(data.my_received_stars_total || 0).toLocaleString(isEn ? 'en-US' : isFr ? 'fr-FR' : 'es-CO');
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
          starsTotalLabel.textContent = Number(data.received_stars_total || 0).toLocaleString(isEn ? 'en-US' : isFr ? 'fr-FR' : 'es-CO');
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
	          setPostsStatus(data.detail || tr('', '', ''), true);
	          return;
	        }
	        const sourcePosts = Array.isArray(data) ? data : [];
	        const uniqueAuthorIds = Array.from(
	          new Set(
	            sourcePosts
	              .map((post) => Number(post?.author?.id || 0))
	              .filter((id) => Number.isFinite(id) && id > 0)
	          )
	        );
	        const profilesByAuthorId = new Map();
	        await Promise.all(
	          uniqueAuthorIds.map(async (authorId) => {
	            try {
	              const profile = await fetchFollowProfile({ userId: authorId });
	              profilesByAuthorId.set(authorId, profile);
	            } catch {
	              profilesByAuthorId.set(authorId, null);
	            }
	          })
	        );
	        const enrichedPosts = sourcePosts.map((post) => {
	          const authorId = Number(post?.author?.id || 0);
	          const profile = profilesByAuthorId.get(authorId);
	          const authorAvatarUrl = String(profile?.avatar_url || '').trim() || DEFAULT_AVATAR_SRC;
	          const authorProfileUrl = String(profile?.profile_url || '').trim() || buildAuthorProfileUrl(post?.author);
	          return {
	            ...post,
	            __author_avatar_url: authorAvatarUrl,
	            __author_profile_url: authorProfileUrl
	          };
	        });
	        currentFeedPosts = enrichedPosts;
	        renderPosts(enrichedPosts);
	        if (isViewingOwnProfile) syncProfilePhotoPostFromFeed();
	        setPostsStatus('');
	      } catch (error) {
	        setPostsStatus(tr('', '', ''), true);
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
      if (uploadHint) uploadHint.textContent = tr('', '', '');
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
        postPreview.innerHTML = `<img src="${selectedFileURL}" alt="${escapeHtml(tr('', '', ''))}" />`;
      } else if (file.type.startsWith('video/')) {
        postPreview.innerHTML = `<video src="${selectedFileURL}" controls></video>`;
      } else {
        selectedFile = null;
        postPreview.innerHTML = '';
        postPreview.classList.add('hidden');
        setPostsStatus(tr('', '', ''), true);
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
          throw new Error(uploadData.detail || tr('', '', ''));
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
        throw new Error(presignData.detail || tr('', '', ''));
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
        throw new Error(proxyData.detail || tr('', '', ''));
      }

      return { media_id: presignData.media_id, media_kind: 'video' };
    };

    const uploadProfilePhotoFilePresigned = async (file) => {
      if (!file) return null;
      if (!file.type?.startsWith('image/')) {
        throw new Error(tr('', '', ''));
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
        throw new Error(presignData.detail || tr('', '', ''));
      }

      try {
        const uploadRes = await fetch(presignData.upload_url, {
          method: 'PUT',
          headers: presignData.required_headers || { 'Content-Type': file.type },
          body: file
        });
        if (!uploadRes.ok) {
          throw new Error(tr('', '', ''));
        }
      } catch (error) {
        const message = (error?.message || '').toLowerCase();
        if (message.includes('failed to fetch') || message.includes('cors')) {
          throw new Error(
            tr(
              'La subida directa al bucket fue bloqueada por CORS. Debes habilitar CORS en tu bucket de media para permitir PUT desde tu frontend.',
              'Direct upload to the bucket was blocked by CORS. You must enable CORS on your media bucket to allow PUT requests from your frontend.'
            )
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
        throw new Error(confirmData.detail || tr('', '', ''));
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
        setPostsStatus(tr('', '', ''), true);
        return;
      }

      const oldLabel = publishPost?.textContent || tr('', '', '');
      if (publishPost) {
        publishPost.disabled = true;
        publishPost.textContent = tr('', '', '');
      }

      try {
        let visibilityValue = (postVisibility?.value || 'public').toLowerCase();
        if (minorAccreditationState?.is_minor_protected && visibilityValue === 'public') {
          visibilityValue = 'private';
          if (postVisibility) postVisibility.value = 'private';
          setPostsStatus(
            tr(
              'Tu cuenta está en modo protegido. Esta publicación se guardará en privado.',
              'Your account is in protected mode. This post will be saved as private.'
            )
          );
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
          throw new Error(data.detail || tr('', '', ''));
        }

        setPostsStatus(tr('', '', ''));
        closePost();
        await Promise.all([loadFeed(), loadMyStats(), loadHomeCalendar()]);
      } catch (error) {
        setPostsStatus(error.message || tr('', '', ''), true);
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
        throw new Error(data.detail || tr('', '', ''));
      }
      return data;
    };

    const ensureProfilePhotoPost = async () => {
      if (!profilePhotoMediaId) {
        renderProfilePhotoPost(null);
        setProfilePhotoPostStatus(tr('', '', ''), true);
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
      await loadHomeCalendar();
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
        setProfilePhotoPostStatus(
          error.message || tr('', '', ''),
          true
        );
      }
    };

    const setProfilePhotoFromMediaId = async (mediaId) => {
      if (!isViewingOwnProfile) {
        throw new Error(tr('', '', ''));
      }
      const normalized = Number(mediaId);
      if (!Number.isFinite(normalized) || normalized <= 0) {
        throw new Error(tr('', '', ''));
      }
      const res = await apiFetch('/media/profile-photo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ media_id: normalized })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr('', '', ''));
      }
      profilePhotoMediaId = data.media_id || null;
      setProfilePhotoPostId(null);
      setHomeAvatarSource(data.url || DEFAULT_AVATAR_SRC);
      renderProfilePhotoPost(null);
      return data;
    };

    const handleHomeAvatarButtonClick = () => {
      if (!isViewingOwnProfile) return;
      refreshHomeAvatarMenuOptions();
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
        setPostsStatus(tr('', '', ''), true);
        if (homeAvatarFile) homeAvatarFile.value = '';
        return;
      }

      homeAvatarProfilePhotoBusy = true;
      setPostsStatus(tr('', '', ''));
      try {
        const uploaded = await uploadProfilePhotoFilePresigned(file);
        await setProfilePhotoFromMediaId(uploaded?.media_id);
        setPostsStatus(tr('', '', ''));
        void ensureProfilePhotoPost().catch((error) => console.error(error));
      } catch (error) {
        setPostsStatus(error.message || tr('', '', ''), true);
      } finally {
        homeAvatarProfilePhotoBusy = false;
        if (homeAvatarFile) homeAvatarFile.value = '';
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

    const setEditPostModalStatus = (message, isError = false) => {
      if (!editPostModalStatus) return;
      editPostModalStatus.textContent = message || '';
      editPostModalStatus.classList.toggle('is-error', Boolean(isError));
    };

    const closeEditModal = () => {
      editPostOverlay?.classList.add('hidden');
      editPostOverlay?.setAttribute('aria-hidden', 'true');
      selectedEditPostId = null;
      if (editPostTextInput) editPostTextInput.value = '';
      setEditPostModalStatus('');
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
      if (commentsStatus) commentsStatus.textContent = tr('', '', '');
      try {
        const res = await apiFetch(`/posts/${selectedCommentPostId}/comments?limit=200`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        if (!Array.isArray(data) || data.length === 0) {
          commentsList.innerHTML = `<p class="post-comments-empty">${escapeHtml(tr('', '', ''))}</p>`;
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
        if (commentsStatus) commentsStatus.textContent = error.message || tr('', '', '');
      }
    };

    const openCommentsForPost = async (postId, title = null) => {
      selectedCommentPostId = postId;
      if (commentsTitle) {
        commentsTitle.textContent = title || tr(
          `Comentarios de la publicación #${postId}`,
          `Comments on post #${postId}`
        );
      }
      commentsOverlay?.classList.remove('hidden');
      commentsOverlay?.setAttribute('aria-hidden', 'false');
      await loadComments();
    };

    const donateStarToPost = async (postId, setStatus = setPostsStatus) => {
      const post = Array.isArray(currentFeedPosts)
        ? currentFeedPosts.find((item) => Number(item?.id) === Number(postId))
        : null;
      if (post?.is_mine) {
        setStatus(tr('', '', ''), true);
        return;
      }
      if (post?.starred_by_me) {
        setStatus(tr('', '', ''), true);
        return;
      }
      try {
        const res = await apiFetch(`/posts/${postId}/stars`, { method: 'POST' });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        setStatus(tr('', '', ''));
        await Promise.all([loadFeed(), loadMyStats()]);
        if (isViewingOwnProfile) syncProfilePhotoPostFromFeed();
      } catch (error) {
        setStatus(error.message || tr('', '', ''), true);
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
          await navigator.share({ title: 'Kiadez', text: tr('', '', ''), url: shareUrl });
        } else if (navigator.clipboard?.writeText) {
          await navigator.clipboard.writeText(shareUrl);
        }
        setStatus(tr('', '', ''));
        await loadFeed();
        if (isViewingOwnProfile) syncProfilePhotoPostFromFeed();
      } catch (error) {
        setStatus(error.message || tr('', '', ''), true);
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
        setHomeAboutModalStatus(
          tr(
            `Puedes escribir máximo ${HOME_ABOUT_MAX_WORDS} palabras.`,
            `You can write up to ${HOME_ABOUT_MAX_WORDS} words.`
          ),
          true
        );
        return;
      }

      const oldLabel = saveHomeAboutBtn?.textContent || tr('', '', '');
      if (saveHomeAboutBtn) {
        saveHomeAboutBtn.disabled = true;
        saveHomeAboutBtn.textContent = tr('', '', '');
      }

      try {
        const res = await apiFetch('/biography/about', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            display_name: (currentAboutDisplayName || homeProfileName?.textContent || tr('', '', '')).trim(),
            about_text: aboutText || null
          })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        applyHomeAbout(data);
        closeHomeAboutModalPanel();
        setPostsStatus(tr('', '', ''));
      } catch (error) {
        setHomeAboutModalStatus(error.message || tr('', '', ''), true);
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
      await openCommentsForPost(
        profilePhotoPost.id,
        tr('', '', '')
      );
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

    const handleOpenEditPostModal = (postId) => {
      const normalizedPostId = Number(postId || 0);
      if (!normalizedPostId) return;
      const post = Array.isArray(currentFeedPosts)
        ? currentFeedPosts.find((item) => Number(item?.id) === normalizedPostId)
        : null;
      if (!post || !post.is_mine) return;

      selectedEditPostId = normalizedPostId;
      if (editPostTextInput) editPostTextInput.value = String(post.text || '');
      setEditPostModalStatus('');
      editPostOverlay?.classList.remove('hidden');
      editPostOverlay?.setAttribute('aria-hidden', 'false');
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

      if (action === 'edit-post') {
        handleOpenEditPostModal(postId);
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
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        setPostsStatus(
          tr(
            `Publicación eliminada. Se restaron ${data.removed_stars || 0} estrellas asociadas.`,
            `Post deleted. ${data.removed_stars || 0} associated stars were removed.`
          )
        );
        closeDeleteModal();
        await Promise.all([loadFeed(), loadMyStats(), loadHomeCalendar()]);
      } catch (error) {
        setPostsStatus(error.message || tr('', '', ''), true);
      }
    };

    const handleSaveEditedPost = async () => {
      if (!selectedEditPostId) return;
      const text = (editPostTextInput?.value || '').trim();
      if (!text) {
        setEditPostModalStatus(tr('', '', ''), true);
        return;
      }

      const oldLabel = saveEditPost?.textContent || tr('', '', '');
      if (saveEditPost) {
        saveEditPost.disabled = true;
        saveEditPost.textContent = tr('', '', '');
      }
      setEditPostModalStatus('');

      try {
        const res = await apiFetch(`/posts/${selectedEditPostId}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));

        closeEditModal();
        setPostsStatus(tr('', '', ''));
        await Promise.all([loadFeed(), loadMyStats(), loadHomeCalendar()]);
      } catch (error) {
        setEditPostModalStatus(error.message || tr('', '', ''), true);
      } finally {
        if (saveEditPost) {
          saveEditPost.disabled = false;
          saveEditPost.textContent = oldLabel;
        }
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
        setPostsStatus(tr('', '', ''), true);
        return;
      }
      const otherReason = (reportReasonOther?.value || '').trim();
      if (reason === 'other' && !otherReason) {
        setPostsStatus(
          tr('', '', ''),
          true
        );
        return;
      }

      try {
        const res = await apiFetch(`/posts/${selectedReportPostId}/reports`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reason, other_reason: otherReason || null })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        setPostsStatus(tr('', '', ''));
        closeReportModal();
      } catch (error) {
        setPostsStatus(error.message || tr('', '', ''), true);
      }
    };

    const handleOpenProfileReportModal = () => {
      if (isViewingOwnProfile) return;
      const targetUserId = Number(activeProfileUserId);
      if (!Number.isFinite(targetUserId) || targetUserId <= 0) {
        setPostsStatus(tr('', '', ''), true);
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
        setReportProfileModalStatus(tr('', '', ''), true);
        return;
      }
      const otherReason = (reportProfileReasonOther?.value || '').trim();
      if (reason === 'other' && !otherReason) {
        setReportProfileModalStatus(
          tr('', '', ''),
          true
        );
        return;
      }

      const oldLabel = submitReportProfile?.textContent || tr('', '', '');
      if (submitReportProfile) {
        submitReportProfile.disabled = true;
        submitReportProfile.textContent = tr('', '', '');
      }
      setReportProfileModalStatus('');

      try {
        const res = await apiFetch(`/follows/profile/${encodeURIComponent(String(selectedReportProfileUserId))}/reports`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reason, other_reason: otherReason || null })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        setPostsStatus(tr('', '', ''));
        closeReportProfileModalPanel();
      } catch (error) {
        setReportProfileModalStatus(error.message || tr('', '', ''), true);
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
        if (commentsStatus) commentsStatus.textContent = tr('', '', '');
        return;
      }
      try {
        const res = await apiFetch(`/posts/${selectedCommentPostId}/comments`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || tr('', '', ''));
        if (commentInput) commentInput.value = '';
        if (commentsStatus) commentsStatus.textContent = '';
        await Promise.all([loadComments(), loadFeed()]);
      } catch (error) {
        if (commentsStatus) commentsStatus.textContent = error.message || tr('', '', '');
      }
    };

    openPostModal?.addEventListener('click', openPost);
    menuPublishBtn?.addEventListener('click', handleMenuPublishClick);
    homeTopbarBtn?.addEventListener('click', handleTopbarHomeClick);
    homeAvatarButton?.addEventListener('click', handleHomeAvatarButtonClick);
    homeAvatarViewBtn?.addEventListener('click', handleHomeAvatarViewClick);
    homeAvatarUploadBtn?.addEventListener('click', handleHomeAvatarUploadClick);
    homeAvatarFile?.addEventListener('change', handleHomeAvatarFileChange);
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

    closeEditPostModal?.addEventListener('click', closeEditModal);
    cancelEditPost?.addEventListener('click', closeEditModal);
    saveEditPost?.addEventListener('click', handleSaveEditedPost);
    editPostOverlay?.addEventListener('click', (event) => {
      if (event.target === editPostOverlay) closeEditModal();
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
        setPostsStatus(error.message || tr('', '', ''), true);
      }

	      if (isViewingOwnProfile) {
		        await Promise.all([
		          loadMinorAccreditationStatus(),
		          loadHomeAbout(),
		          loadHomeCover(),
		          loadProfilePhoto(),
		          loadUsernameState(),
		          loadHomePublicWishes(),
	          loadHomeCooperativeWishes(),
	          loadHomeFulfilledWishes(),
	          loadHomePrivateWishes(),
	          loadHomeCalendar(),
	          loadHomeOracle(),
	          loadMyStats()
	        ]);
        await loadFeed();
        syncProfilePhotoPostFromFeed();
        return;
      }

		      await loadForeignProfilePrivacyVisibility();
				      await Promise.all([
				        loadHomeAbout(activeProfileUserId),
			        loadHomeCover(activeProfileUserId),
				        loadHomePublicWishes(),
			        loadHomeCooperativeWishes(),
			        loadHomeFulfilledWishes(),
	          loadHomeCalendar(),
	          loadHomeOracle(),
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
      closeEditPostModal?.removeEventListener('click', closeEditModal);
      cancelEditPost?.removeEventListener('click', closeEditModal);
      saveEditPost?.removeEventListener('click', handleSaveEditedPost);

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
  <title>{tr("Kiadez — Inicio", "Kiadez — Home", "Kiadez — Accueil")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background home-user-page">
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input type="search" placeholder={tr("Buscar en Kiadez", "Search on Kiadez", "Rechercher sur Kiadez")} aria-label={tr("Buscar", "Search", "Rechercher")} />
      </form>
    </div>

    <div class="feed-topbar-zone feed-topbar-center">
	      <button class="topbar-btn is-active" id="homeTopbarBtn" type="button">🏠 {tr("Home", "Home", "Accueil")}</button>
	      <a class="topbar-btn" href="/gallery.html" data-profile-module="gallery">🖼️ {tr("Galería", "Gallery", "Galerie")}</a>
	      <a class="topbar-btn" href="/my-public-whishes.html" data-profile-module="public_wishes">🌐 {tr("Deseos públicos", "Public wishes", "Souhaits publics")}</a>
	      <a class="topbar-btn" href="/my-private-whishes.html">🔒 {tr("Deseos privados", "Private wishes", "Souhaits privés")}</a>
	      <a class="topbar-btn" href="/my-fulfilled-whises.html" data-profile-module="fulfilled_wishes">✅ {tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</a>
	    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown" id="profileDropdown">
        <summary class="topbar-avatar-btn" aria-label={tr("Perfil del usuario", "User profile", "Profil utilisateur")}>
          <img src="/assets/avatar-default.jpg" alt={tr("Foto de perfil del usuario", "User profile photo", "Photo de profil utilisateur")} data-viewer-avatar />
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/privacy-and-settings.html" role="menuitem">{tr("Configuración y privacidad", "Settings and privacy", "Paramètres et confidentialité")}</a>
          <button type="button" role="menuitem" on:click={logout}>{tr("Cerrar sesión", "Sign out", "Se déconnecter")}</button>
        </div>
      </details>

      <button class="topbar-icon" type="button" aria-label={tr("Notificaciones", "Notifications", "Alertes")}>
        🔔
        <span class="topbar-badge">3</span>
      </button>

      <details class="topbar-dropdown" id="menuDropdown">
        <summary class="topbar-menu-btn" aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}>
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">{tr("Menú", "Menu", "Navigation")}</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <button class="dropdown-action" id="menuPublishBtn" type="button" role="menuitem">
            {tr("Publicar", "Publish", "Publier")}
          </button>
          <a href="/home_user.html" role="menuitem" data-my-home-link="true">{tr("Mi Home", "My Home", "Mon Home")}</a>
          <a href="/achievements.html" role="menuitem" data-profile-module="achievements">{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
          <a href="/gallery.html" role="menuitem" data-profile-module="gallery">{tr("Galería", "Gallery", "Galerie")}</a>
	          <a href="/calendar.html" role="menuitem" data-profile-module="calendar">{tr("Calendario", "Calendar", "Calendrier")}</a>
          <a href="/my-biography.html" role="menuitem" data-profile-module="biography">{tr("Mi Biografía", "My Biography", "Ma biographie")}</a>
          <a href="/messages.html" role="menuitem">{tr("Mensajes", "Messages", "Messagerie")}</a>
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <section class="cover" id="cover" data-profile-module="cover_purposes">
      <div class="cover-media" id="coverMedia">
	        <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt={tr("Portada", "Cover", "Couverture")} />

        <div class="cover-actions">
          <button class="icon-btn" id="btnChangeCover" type="button" title={tr("Cambiar portada", "Change cover", "Changer la couverture")}>
            {tr("Cambiar portada", "Change cover", "Changer la couverture")}
          </button>
          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button" title={tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier mon objectif de vie")}>
            {tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier mon objectif de vie")}
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

	        <div class="purpose-triangle" aria-label={tr("Deseos de propósito", "Purpose wishes", "Souhaits de finalité")}>
	          <button class="purpose-pill purpose-top" type="button" id="purpose1">
	            {tr("Deseo #1: Secreto", "Wish #1: Secret", "Souhait #1 : Secret")}
	          </button>

	          <button class="purpose-pill purpose-left" type="button" id="purpose2">
	            {tr("Deseo construir el Reino de Combray", "I wish to build the Kingdom of Combray", "Je souhaite construire le Royaume de Combray")}
	          </button>

	          <button class="purpose-pill purpose-right" type="button" id="purpose3">
	            {tr("Deseo estar unido a Jesús", "I wish to be united with Jesus", "Je souhaite être uni à Jésus")}
	          </button>
	        </div>

        <div class="cover-hint" id="coverHint">
          {tr("Arrastra la portada para encuadrarla", "Drag the cover to frame it", "Fais glisser la couverture pour la cadrer")}
        </div>
      </div>
    </section>

    <div class="home-body">
      <nav class="profile-nav" aria-label={tr("Navegación de perfil", "Profile navigation", "Navigation du profil")}>
        <a class="nav-pill" href="/home_user.html" title={tr("Home", "Home", "Accueil")} data-profile-link="true">{tr("Home", "Home", "Accueil")}</a>
        <a class="nav-pill" href="/star-pool-found.html" title={tr("Estrellas", "Stars", "Étoiles")} data-profile-module="stars">
          <span class="nav-icon">⭐</span>
          <span><strong id="homeStarsTotal">0</strong> {tr("estrellas", "stars", "étoiles")}</span>
        </a>

        <a class="nav-pill" href="/followers.html" title={tr("Seguidores", "Followers", "Abonnés")} data-profile-module="followers">{tr("Seguidores", "Followers", "Abonnés")}</a>
        <a class="nav-pill" href="/achievements.html" title={tr("Logros recientes", "Recent achievements", "Réalisations récentes")} data-profile-module="achievements">{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
        <a class="nav-pill" href="/gallery.html" title={tr("Galería", "Gallery", "Galerie")} data-profile-module="gallery">{tr("Galería", "Gallery", "Galerie")}</a>
	        <a class="nav-pill" href="/calendar.html" title={tr("Calendario", "Calendar", "Calendrier")} data-profile-module="calendar">{tr("Calendario", "Calendar", "Calendrier")}</a>
        <a class="nav-pill" href="/my-biography.html" title={tr("Mi biografía", "My biography", "Ma biographie")} data-profile-module="biography">{tr("Mi biografía", "My biography", "Ma biographie")}</a>
        <a class="nav-pill" href="/messages.html" title={tr("Mensajes", "Messages", "Messagerie")}>{tr("Mensajes", "Messages", "Messagerie")}</a>
      </nav>

      <section class="profile-grid">
        <aside class="left-col">
          <article class="panel profile-card">
            <div class="profile-row">
              <details class="topbar-dropdown profile-avatar-dropdown" id="homeAvatarDropdown">
	                <summary class="profile-avatar-btn" id="homeAvatarButton" aria-label={tr("Foto de perfil", "Profile photo", "Photo de profil")} title={tr("Foto de perfil", "Profile photo", "Photo de profil")}>
	                  <img class="avatar profile-avatar-image" src="/assets/avatar-default.jpg" alt={tr("Foto de perfil", "Profile photo", "Photo de profil")} data-profile-avatar />
	                </summary>
	                <div class="dropdown-menu" role="menu">
	                  <button class="dropdown-action hidden" id="homeAvatarViewBtn" type="button" role="menuitem">
	                    {tr("Ver imagen de perfil", "View profile image", "Voir la photo de profil")}
	                  </button>
	                  <button class="dropdown-action" id="homeAvatarUploadBtn" type="button" role="menuitem">
	                    {tr("Subir imagen de perfil", "Upload profile image", "Téléverser la photo de profil")}
	                  </button>
	                </div>
              </details>
              <input id="homeAvatarFile" type="file" accept="image/*" class="hidden" />
              <div class="profile-meta">
                <h2 class="profile-name" id="homeProfileName">Carlos Jiménez Duarte</h2>
                <p class="profile-rank hidden" id="homeProfileRank"></p>
                <div class="home-username-row">
                  <a class="home-username-link is-empty" id="homeUsernameLink" href="/home_user.html" data-profile-link="true">
	                    <span id="homeUsernameValue">{tr("@elige-tu-usuario", "@choose-your-username", "@choisis-ton-nom-utilisateur")}</span>
	                  </a>
	                  <button class="infobox-edit-btn home-username-edit-btn" id="homeUsernameEditBtn" type="button" title={tr("Modificar nombre de usuario", "Edit username", "Modifier le nom d'utilisateur")}>
	                    <img src="/css/icons/iconedit.webp" alt={tr("Editar usuario", "Edit user", "Modifier l'utilisateur")} />
	                  </button>
	                  <button class="post-head-btn home-username-report-btn hidden" id="homeUsernameReportBtn" type="button" title={tr("Denunciar perfil", "Report profile", "Signaler le profil")} aria-label={tr("Denunciar perfil", "Report profile", "Signaler le profil")}>
	                    🚩
	                  </button>
                </div>
                <p class="home-username-cooldown" id="homeUsernameCooldown"></p>
              </div>
            </div>
          </article>

          <article class="panel" id="homeAboutPanel">
            <div class="panel-head home-about-head">
              <h3 class="panel-title">{tr("Acerca de mí", "About me", "À propos de moi")}</h3>
	              <button class="infobox-edit-btn home-about-edit-btn" id="homeAboutEditBtn" type="button" title={tr("Modificar acerca de mí", "Edit about me", "Modifier À propos de moi")}>
	                <img src="/css/icons/iconedit.webp" alt={tr("Editar", "Edit", "Modifier")} />
	              </button>
            </div>
            <p class="panel-muted" id="homeAboutEmptyState">
              {tr('', '', '')}
            </p>
            <p class="panel-text home-about-text hidden" id="homeAboutTextValue"></p>
          </article>

          <article class="panel" id="homeFulfilledPanel">
            <div class="panel-head">
              <h3 class="panel-title">{tr("Mis deseos cumplidos", "My fulfilled wishes", "Mes souhaits accomplis")}</h3>
              <span class="panel-badge" id="homeFulfilledWishCount">{tr("0 recientes", "0 recent", "0 récents")}</span>
            </div>

            <ul class="wish-list" id="homeFulfilledWishList">
              <li class="wish-item wish-item-home-public wish-item-empty">
                <span class="wish-dot"></span>
                <span class="wish-item-label">{tr("Cargando tus deseos cumplidos...", "Loading your fulfilled wishes...", "Chargement de tes souhaits accomplis...")}</span>
              </li>
            </ul>
            <p class="home-public-wish-status" id="homeFulfilledWishStatus" aria-live="polite"></p>

	            <a href="/my-fulfilled-whises.html" class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn" data-profile-module="fulfilled_wishes">{tr("Ver más", "See more", "Voir plus")}</a>
          </article>

          <article class="panel" id="homePublicPanel">
            <div class="panel-head">
              <h3 class="panel-title">{tr("Mis deseos públicos", "My public wishes", "Mes souhaits publics")}</h3>
              <span class="panel-badge" id="homePublicWishCount">0 / 50</span>
            </div>

            <ul class="wish-list" id="homePublicWishList">
              <li class="wish-item wish-item-home-public wish-item-empty">
                <span class="wish-dot"></span>
                <span class="wish-item-label">{tr("Cargando tus deseos públicos...", "Loading your public wishes...", "Chargement de tes souhaits publics...")}</span>
              </li>
            </ul>
            <p class="home-public-wish-status" id="homePublicWishStatus" aria-live="polite"></p>

	            <a href="/my-public-whishes.html" class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn" data-profile-module="public_wishes">{tr("Ver más", "See more", "Voir plus")}</a>
          </article>

          <article class="panel hidden" id="homeCooperativePanel">
            <div class="panel-head">
              <h3 class="panel-title">{tr("Deseos cooperativos", "Cooperative wishes", "Souhaits coopératifs")}</h3>
              <span class="panel-badge" id="homeCooperativeWishCount">0 / 20</span>
            </div>

            <ul class="wish-list" id="homeCooperativeWishList"></ul>
            <p class="home-public-wish-status" id="homeCooperativeWishStatus" aria-live="polite"></p>

	            <a
                href="/my-public-whishes.html#cooperative-wishes"
                class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn"
                data-profile-module="public_wishes_cooperative"
              >
                {tr("Ver más", "See more", "Voir plus")}
              </a>
          </article>

          <article class="panel">
            <div class="panel-head">
              <h3 class="panel-title">{tr("Deseos privados", "Private wishes", "Souhaits privés")}</h3>
              <span class="panel-badge" id="homePrivateWishCount">0 / 50</span>
            </div>

            <div class="secret-meter">
              <div class="secret-number" id="homePrivateWishTotal">0 / 50</div>
              <div class="secret-sub">{tr("Solo tú puedes ver esta cifra", "Only you can see this value", "Seul toi peux voir cette valeur")}</div>
            </div>
            <p class="home-public-wish-status" id="homePrivateWishStatus" aria-live="polite"></p>

            <a href="/my-private-whishes.html" class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn">{tr("Ir a Deseos privados", "Go to private wishes", "Aller aux souhaits privés")}</a>
          </article>

          <article class="panel" id="homeCalendarPanel">
            <div class="panel-head">
              <h3 class="panel-title">{tr("Calendario", "Calendar", "Calendrier")}</h3>
              <span class="panel-badge">{tr("Mes actual", "Current month", "Mois en cours")}</span>
            </div>

            <div class="home-calendar-shell" aria-label={tr("Actividad mensual de publicaciones", "Monthly posting activity", "Activité mensuelle de publication")}>
              <article class="month-card home-calendar-month-card">
                <div class="month-name">
                  <span id="homeCalendarMonthName">{tr("Mes actual", "Current month", "Mois en cours")}</span>
                  <span class="month-status" id="homeCalendarMonthProgress">0 / 0</span>
                </div>
                <div class="month-dots home-calendar-dots" id="homeCalendarDots"></div>
              </article>
            </div>
            <p class="home-public-wish-status" id="homeCalendarStatus" aria-live="polite"></p>

	            <a href="/calendar.html" class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn" data-profile-module="calendar">{tr("Ver más", "See more", "Voir plus")}</a>
          </article>

	          <article class="panel" id="homeOraclePanel">
	            <div class="panel-head">
	              <h3 class="panel-title">{tr("Oráculo", "Oracle", "Oracle")}</h3>
	              <span class="panel-badge">{tr("Última carta", "Latest card", "Dernière carte")}</span>
	            </div>

	            <div class="oracle-card">
	              <img id="homeOracleCardImage" src="/css/oracle/carta.webp" alt={tr("Carta del Oráculo en reverso", "Oracle card back", "Dos de carte Oracle")} />
	            </div>
	            <p class="panel-muted" id="homeOracleSummary">
	              {tr("Conoce El Oráculo y elige tu primera carta para reflexionar sobre tu presente.", "Discover the Oracle and choose your first card to reflect on your present.", "Découvre l'Oracle et choisis ta première carte pour réfléchir à ton présent.")}
	            </p>
	            <p class="home-public-wish-status" id="homeOracleStatus" aria-live="polite"></p>

		            <a href="/oracle.html" class="btn btn-outline btn-compact btn-inline home-public-wish-more-btn" data-profile-module="oracle">{tr("Visitar el Oráculo", "Visit Oracle", "Visiter l'Oracle")}</a>
	          </article>
	        </aside>

	        <section class="right-col">
	          <article class="panel composer">
	            <div class="composer-row">
		              <img class="avatar avatar-sm composer-avatar" src="/assets/avatar-default.jpg" alt={tr("Avatar", "Avatar", "Avatar")} data-viewer-avatar />
	              <button class="composer-input" id="openPostModal" type="button">
	                {tr("¿Qué estás pensando?", "What are you thinking?", "À quoi penses-tu ?")}
	              </button>
	            </div>
	          </article>

          <article class="panel minor-protected-panel hidden" id="minorProtectedPanel">
            <div class="panel-head minor-protected-head">
              <h3 class="panel-title">{tr("Cuenta en modo protegido", "Account in protected mode", "Compte en mode protégé")}</h3>
              <button class="btn btn-outline btn-compact minor-protected-toggle" id="toggleMinorProtectedPanel" type="button">
                {tr("Reducir", "Collapse", "Réduire")}
              </button>
            </div>
            <div class="minor-protected-body" id="minorProtectedBody">
              <p class="panel-muted">
                {tr(
                  "Según la fecha de nacimiento registrada, tu perfil requiere validación de un padre, madre o tutor legal para habilitar funciones públicas. Puedes usar la plataforma con normalidad, pero tu contenido permanecerá privado hasta completar este proceso.",
                  "Based on your registered birth date, your profile requires validation by a parent or legal guardian to enable public features. You can use the platform normally, but your content will remain private until this process is completed."
                )}
              </p>
              <p class="panel-muted minor-protected-state" id="minorProtectedStateLabel"></p>
              <div class="minor-protected-actions">
                <button class="btn btn-primary btn-compact" id="openMinorAccreditationModal" type="button">
                  {tr("Acreditar cuenta", "Accredit account", "Accréditer le compte")}
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

  <AuthFooter />
</div>

<div class="modal-overlay hidden" id="postModalOverlay" aria-hidden="true">
  <div class="modal modal-wide" role="dialog" aria-modal="true" aria-label={tr("Crear publicación", "Create post", "Créer une publication")}>
    <div class="modal-head">
      <h3>{tr("Crear publicación", "Create post", "Créer une publication")}</h3>
      <button class="modal-close" type="button" id="closePostModal">✕</button>
    </div>

	    <div class="modal-body">
	      <div class="post-modal-top">
		        <img class="avatar avatar-sm composer-avatar" src="/assets/avatar-default.jpg" alt={tr("Avatar", "Avatar", "Avatar")} data-viewer-avatar />
	        <div>
          <div class="post-modal-name"><strong>Carlos Jiménez Duarte</strong></div>
          <select class="modal-select" id="postVisibility">
            <option value="public">{tr("Público", "Public", "Public")}</option>
            <option value="private">{tr("Privado", "Private", "Privé")}</option>
          </select>
        </div>
      </div>

      <textarea class="modal-textarea" id="postText" rows="5" placeholder={tr("Escribe algo...", "Write something...", "Écris quelque chose...")}></textarea>

      <div class="upload-row">
        <label class="upload-btn" for="postFile">{tr("Adjuntar imagen o video", "Attach image or video", "Joindre image ou vidéo")}</label>
        <input id="postFile" type="file" accept="image/*,video/*" class="hidden" />
        <div class="upload-hint" id="uploadHint">{tr("Sin archivo adjunto", "No file attached", "Aucun fichier joint")}</div>
      </div>

      <div class="preview hidden" id="postPreview"></div>
    </div>

    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelPost">{tr("Cancelar", "Cancel", "Annuler")}</button>
      <button class="btn btn-primary btn-compact" type="button" id="publishPost">{tr("Publicar", "Publish", "Publier")}</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="minorAccreditationModalOverlay" aria-hidden="true">
  <div class="modal minor-accreditation-modal" role="dialog" aria-modal="true" aria-label={tr("Acreditar cuenta", "Accredit account", "Accréditer le compte")}>
    <div class="modal-head">
      <h3>{tr("Acreditar cuenta", "Accredit account", "Accréditer le compte")}</h3>
      <button class="modal-close" type="button" id="closeMinorAccreditationModal">✕</button>
    </div>

    <div class="modal-body">
      <p class="panel-muted">
        {tr(
          "Registra los datos del padre, madre o tutor legal para enviar la solicitud de validación.",
          "Register the parent or legal guardian details to send the validation request."
        )}
      </p>

      <label class="modal-label" for="minorGuardianPhoneInput">{tr("Teléfono del padre, madre o tutor legal", "Phone of parent or legal guardian", "Téléphone du parent ou tuteur légal")}</label>
      <input
        class="modal-input"
        id="minorGuardianPhoneInput"
        type="tel"
        maxlength="40"
        placeholder="+57 321 6852619"
      />

      <label class="modal-label" for="minorGuardianEmailInput">{tr("Correo electrónico del adulto responsable", "Responsible adult email", "E-mail de l'adulte responsable")}</label>
      <input
        class="modal-input"
        id="minorGuardianEmailInput"
        type="email"
        maxlength="255"
        placeholder="ejemplo@correo.com"
      />

      <label class="modal-label" for="minorRelationshipSelect">{tr("Parentesco", "Relationship", "Relation")}</label>
      <select class="modal-select" id="minorRelationshipSelect">
        <option value="padre">{tr("Padre", "Father", "Père")}</option>
        <option value="madre">{tr("Madre", "Mother", "Mère")}</option>
        <option value="tutor_legal">{tr("Tutor legal", "Legal guardian", "Tuteur légal")}</option>
        <option value="adulto_responsable">{tr("Adulto responsable", "Responsible adult", "Adulte responsable")}</option>
      </select>

      <p class="minor-accreditation-modal-status" id="minorAccreditationModalStatus" aria-live="polite"></p>
    </div>

    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelMinorAccreditationModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
      <button class="btn btn-primary btn-compact" type="button" id="submitMinorAccreditation">{tr("Enviar solicitud", "Send request", "Envoyer la demande")}</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="profilePhotoPostModalOverlay" aria-hidden="true">
  <div class="modal modal-wide profile-photo-post-modal" role="dialog" aria-modal="true" aria-label={tr("Publicación de foto de perfil", "Profile photo post", "Publication de photo de profil")}>
    <div class="modal-head">
      <h3>{tr("Foto de perfil", "Profile photo", "Photo de profil")}</h3>
      <button class="modal-close" type="button" id="closeProfilePhotoPostModal">✕</button>
    </div>
    <div class="modal-body">
      <article class="panel post profile-photo-post-card">
        <div class="post-head">
          <div>
            <strong id="profilePhotoPostAuthor">Carlos Jiménez Duarte</strong>
	            <span class="post-meta" id="profilePhotoPostMeta">{tr("· Publicación pendiente", "· Pending post", "· Publication en attente")}</span>
	          </div>
	        </div>
	        <p class="post-text">{tr("Actualicé mi foto de perfil.", "I updated my profile photo.", "J'ai mis à jour ma photo de profil.")}</p>
        <div class="post-media profile-photo-media">
          <button
            class="profile-photo-nav profile-photo-nav-prev hidden"
            type="button"
            id="profilePhotoPrevBtn"
            aria-label={tr("Foto de perfil anterior", "Previous profile photo", "Photo de profil précédente")}
            title={tr("Foto anterior", "Previous photo", "Photo précédente")}
          >
            ‹
          </button>
	          <img id="profilePhotoPostImage" src="/assets/avatar-default.jpg" alt={tr("Foto de perfil", "Profile photo", "Photo de profil")} />
          <button
            class="profile-photo-nav profile-photo-nav-next hidden"
            type="button"
            id="profilePhotoNextBtn"
            aria-label={tr("Foto de perfil siguiente", "Next profile photo", "Photo de profil suivante")}
            title={tr("Foto siguiente", "Next photo", "Photo suivante")}
          >
            ›
          </button>
        </div>
        <div class="post-actions">
          <button class="post-btn" type="button" id="profilePhotoStarPost">⭐ {tr("Donar estrella", "Donate star", "Donner une étoile")} (0)</button>
          <button class="post-btn" type="button" id="profilePhotoCommentPost">💬 {tr("Comentar", "Comment", "Commenter")} (0)</button>
          <button class="post-btn" type="button" id="profilePhotoSharePost">🔁 {tr("Compartir", "Share", "Partager")} (0)</button>
        </div>
      </article>
      <p class="profile-photo-post-status" id="profilePhotoPostStatus" aria-live="polite"></p>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelProfilePhotoPostModal">{tr("Cerrar", "Close", "Fermer")}</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="homeUsernameModalOverlay" aria-hidden="true">
  <div class="modal home-username-modal" role="dialog" aria-modal="true" aria-label={tr("Modificar nombre de usuario", "Edit username", "Modifier le nom d'utilisateur")}>
    <div class="modal-head">
      <h3>{tr("Modificar nombre de usuario", "Edit username", "Modifier le nom d'utilisateur")}</h3>
      <button class="modal-close" type="button" id="closeHomeUsernameModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="panel-muted">{tr("Elige un nombre de usuario único. Solo podrás cambiarlo una vez por mes.", "Choose a unique username. You can change it only once per month.", "Choisis un nom d'utilisateur unique. Tu ne peux le modifier qu'une fois par mois.")}</p>
      <label class="modal-label" for="homeUsernameInput">{tr("Nombre de usuario", "Username", "Nom d'utilisateur")}</label>
      <div class="home-username-input-wrap">
        <span class="home-username-prefix">@</span>
        <input
          class="modal-input home-username-input"
          id="homeUsernameInput"
          type="text"
          minlength="4"
          maxlength="30"
          autocomplete="off"
          placeholder={tr("tunombredeusuario", "yourusername", "tonnomutilisateur")}
        />
      </div>
      <p class="home-username-preview" id="homeUsernamePreview">{tr("Enlace: /home_user.html", "Link: /home_user.html", "Lien : /home_user.html")}</p>
      <p class="infobox-photo-status" id="homeUsernameModalStatus" aria-live="polite"></p>
      <div class="home-username-confirm-wrap hidden" id="homeUsernameConfirmWrap">
        <p class="modal-label-center" id="homeUsernameConfirmText">
          {tr("¿Estás seguro de que deseas este nombre de usuario?", "Are you sure you want this username?", "Es-tu sûr de vouloir ce nom d'utilisateur ?")}
        </p>
        <div class="home-username-confirm-actions">
          <button class="btn btn-primary btn-compact" type="button" id="confirmHomeUsernameBtn">{tr("Sí", "Yes", "Oui")}</button>
          <button class="btn btn-outline btn-compact" type="button" id="cancelHomeUsernameConfirmBtn">{tr("Cancelar", "Cancel", "Annuler")}</button>
        </div>
      </div>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelHomeUsernameModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
      <button class="btn btn-primary btn-compact" type="button" id="saveHomeUsernameBtn">{tr("Aceptar", "Accept", "Accepter")}</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="homeAboutModalOverlay" aria-hidden="true">
  <div class="modal home-about-modal" role="dialog" aria-modal="true" aria-label={tr("Modificar acerca de mí", "Edit about me", "Modifier À propos de moi")}>
    <div class="modal-head">
      <h3>{tr('', '', '')}</h3>
      <button class="modal-close" type="button" id="closeHomeAboutModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="panel-muted">{tr("Describe quién eres en un máximo de 50 palabras.", "Describe who you are in up to 50 words.", "Décris qui tu es en 50 mots maximum.")}</p>
      <textarea class="modal-textarea home-about-textarea" id="homeAboutInput" rows="5" placeholder={tr("Escribe aquí...", "Write here...", "Écris ici...")}></textarea>
      <p class="home-about-word-count" id="homeAboutWordCounter">{tr("0 / 50 palabras", "0 / 50 words", "0 / 50 mots")}</p>
      <p class="infobox-photo-status" id="homeAboutModalStatus" aria-live="polite"></p>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelHomeAboutModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
      <button class="btn btn-primary btn-compact" type="button" id="saveHomeAboutBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="deletePostModalOverlay" aria-hidden="true">
  <div class="modal wish-modal delete-wish-modal" role="dialog" aria-modal="true" aria-label={tr("Eliminar publicación", "Delete post", "Supprimer la publication")}>
    <div class="modal-head">
      <h3>{tr("Eliminar publicación", "Delete post", "Supprimer la publication")}</h3>
      <button class="modal-close" type="button" id="closeDeletePostModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="modal-label-center">
        {tr(
          "Esta acción eliminará la publicación y restará permanentemente las estrellas asociadas a ella.",
          "This action will delete the post and permanently deduct the associated stars."
        )}
      </p>
      <p class="modal-label-center muted">{tr("Esta acción no se puede deshacer.", "This action cannot be undone.", "Cette action est irréversible.")}</p>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelDeletePost">{tr("Cancelar", "Cancel", "Annuler")}</button>
      <button class="btn btn-primary btn-compact" type="button" id="confirmDeletePost">{tr("Eliminar", "Delete", "Supprimer")}</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="editPostModalOverlay" aria-hidden="true">
  <div class="modal wish-modal fulfill-wish-modal" role="dialog" aria-modal="true" aria-label={tr("Editar publicación", "Edit post", "Modifier la publication")}>
    <div class="modal-head">
      <h3>{tr("Editar publicación", "Edit post", "Modifier la publication")}</h3>
      <button class="modal-close" type="button" id="closeEditPostModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="modal-label-center">
        {tr("Puedes corregir ortografía o gramática del texto publicado.", "You can correct spelling or grammar in the published text.", "Tu peux corriger l'orthographe ou la grammaire du texte publié.")}
      </p>
      <label class="modal-label" for="editPostText">{tr("Texto", "Text", "Texte")}</label>
      <textarea class="modal-textarea" id="editPostText" rows="5" maxlength="2000" placeholder={tr("Escribe el texto actualizado", "Write the updated text", "Écris le texte mis à jour")}></textarea>
      <p class="infobox-photo-status" id="editPostModalStatus" aria-live="polite"></p>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelEditPost">{tr("Cancelar", "Cancel", "Annuler")}</button>
      <button class="btn btn-primary btn-compact" type="button" id="saveEditPost">{tr("Guardar cambios", "Save changes", "Enregistrer les modifications")}</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="reportPostModalOverlay" aria-hidden="true">
  <div class="modal wish-modal fulfill-wish-modal report-post-modal" role="dialog" aria-modal="true" aria-label={tr("Reportar publicación", "Report post", "Signaler la publication")}>
    <div class="modal-head">
      <h3>{tr("Reportar publicación", "Report post", "Signaler la publication")}</h3>
      <button class="modal-close" type="button" id="closeReportPostModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="modal-label-center">
        {tr("Selecciona la razón por la cual deseas reportar esta publicación.", "Select the reason why you want to report this post.", "Sélectionne la raison pour laquelle tu veux signaler cette publication.")}
      </p>
      <div class="report-reasons">
        <label class="report-option"><input type="radio" name="postReportReason" value="violent" checked /> {tr("Contenido violento o perturbador", "Violent or disturbing content", "Contenu violent ou perturbant")}</label>
        <label class="report-option"><input type="radio" name="postReportReason" value="divisive" /> {tr("Contenido que promueve confrontación o división excesiva", "Content that promotes confrontation or excessive division", "Contenu qui favorise la confrontation ou une division excessive")}</label>
        <label class="report-option"><input type="radio" name="postReportReason" value="sexual" /> {tr("Contenido sexual explícito o inapropiado", "Explicit or inappropriate sexual content", "Contenu sexuel explicite ou inapproprié")}</label>
        <label class="report-option"><input type="radio" name="postReportReason" value="other" /> {tr("Otra razón", "Other reason", "Autre raison")}</label>
      </div>
      <div id="reportReasonOtherWrap" class="report-other-wrap hidden">
        <label class="modal-label" for="reportReasonOther">{tr("Describe la razón", "Describe the reason", "Décris la raison")}</label>
        <textarea class="modal-textarea" id="reportReasonOther" rows="3" placeholder={tr("Escribe tu razón", "Write your reason", "Écris ta raison")}></textarea>
      </div>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelReportPost">{tr("Cancelar", "Cancel", "Annuler")}</button>
      <button class="btn btn-primary btn-compact" type="button" id="submitReportPost">{tr("Enviar reporte", "Send report", "Envoyer le signalement")}</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="reportProfileModalOverlay" aria-hidden="true">
  <div class="modal wish-modal fulfill-wish-modal" role="dialog" aria-modal="true" aria-label={tr("Reportar perfil", "Report profile", "Signaler le profil")}>
    <div class="modal-head">
      <h3>{tr("Reportar perfil", "Report profile", "Signaler le profil")}</h3>
      <button class="modal-close" type="button" id="closeReportProfileModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="modal-label-center">
        {tr("Selecciona la razón por la cual deseas reportar este perfil.", "Select the reason why you want to report this profile.", "Sélectionne la raison pour laquelle tu veux signaler ce profil.")}
      </p>
      <div class="report-reasons">
        <label class="report-option"><input type="radio" name="profileReportReason" value="fake_or_illegal" checked /> {tr("Perfil falso o contenido ilegal", "Fake profile or illegal content", "Profil faux ou contenu illégal")}</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="external_manipulation" /> {tr("Manipulación hacia otros usuarios en la vida real a través de medios externos a esta plataforma", "Manipulation of other users in real life through means external to this platform", "Manipulation d'autres utilisateurs dans la vie réelle via des moyens externes à cette plateforme")}</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="star_manipulation" /> {tr("Abuso de publicaciones para atraer estrellas", "Abusive posting to attract stars", "Publications abusives pour attirer des étoiles")}</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="abusive_or_coercive" /> {tr("Conducta abusiva o coercitiva", "Abusive or coercive behavior", "Comportement abusif ou coercitif")}</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="wish_system_abuse" /> {tr("Uso indebido del sistema de deseos", "Misuse of the wishes system", "Mauvaise utilisation du système des souhaits")}</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="safety_risk" /> {tr("Riesgo para la seguridad de otros", "Risk to the safety of others", "Risque pour la sécurité des autres")}</label>
        <label class="report-option"><input type="radio" name="profileReportReason" value="other" /> {tr("Otro (Especificar)", "Other (Specify)", "Autre (préciser)")}</label>
      </div>
      <div id="reportProfileReasonOtherWrap" class="report-other-wrap hidden">
        <label class="modal-label" for="reportProfileReasonOther">{tr("Describe la razón", "Describe the reason", "Décris la raison")}</label>
        <textarea class="modal-textarea" id="reportProfileReasonOther" rows="3" placeholder={tr("Escribe tu razón", "Write your reason", "Écris ta raison")}></textarea>
      </div>
      <p class="infobox-photo-status" id="reportProfileModalStatus" aria-live="polite"></p>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelReportProfile">{tr("Cancelar", "Cancel", "Annuler")}</button>
      <button class="btn btn-primary btn-compact" type="button" id="submitReportProfile">{tr("Enviar reporte", "Send report", "Envoyer le signalement")}</button>
    </div>
  </div>
</div>

<div class="modal-overlay hidden" id="postCommentsModalOverlay" aria-hidden="true">
  <div class="modal modal-wide" role="dialog" aria-modal="true" aria-label={tr("Comentarios de publicación", "Post comments", "Commentaires de publication")}>
    <div class="modal-head">
      <h3 id="postCommentsTitle">{tr("Comentarios", "Comments", "Commentaires")}</h3>
      <button class="modal-close" type="button" id="closePostCommentsModal">✕</button>
    </div>
    <div class="modal-body">
      <p class="posts-status" id="postCommentsStatus"></p>
      <div class="post-comments-list" id="postCommentsList"></div>
      <label class="modal-label" for="postCommentInput">{tr("Agregar comentario", "Add comment", "Ajouter un commentaire")}</label>
      <textarea class="modal-textarea" id="postCommentInput" rows="3" maxlength="1200" placeholder={tr("Escribe un comentario", "Write a comment", "Écrire un commentaire")}></textarea>
    </div>
    <div class="modal-actions">
      <button class="btn btn-outline btn-compact" type="button" id="cancelPostCommentsModal">{tr("Cerrar", "Close", "Fermer")}</button>
      <button class="btn btn-primary btn-compact" type="button" id="sendPostComment">{tr("Comentar", "Comment", "Commenter")}</button>
    </div>
  </div>
</div>
