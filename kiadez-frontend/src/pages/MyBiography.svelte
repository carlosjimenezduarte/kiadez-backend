<script>
  import { onMount } from "svelte";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";

  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

  onMount(() => {
    initPurposeCoverModule();
    void syncProfileStarsTotal("biographyStarsTotal");

    const API = "http://127.0.0.1:8000";
    const profilePhoto = document.getElementById("profilePhoto");
    const profilePhotoTrigger = document.getElementById("profilePhotoTrigger");
    const profilePhotoMenu = document.getElementById("profilePhotoMenu");
    const bioPhotoUpload = document.getElementById("bioPhotoUpload");
    const bioPhotoFile = document.getElementById("bioPhotoFile");
    const bioPhotoStatus = document.getElementById("bioPhotoStatus");
    const emblemImage = document.getElementById("emblemImage");
    const emblemTrigger = document.getElementById("emblemTrigger");
    const emblemMenu = document.getElementById("emblemMenu");
    const emblemUpload = document.getElementById("emblemUpload");
    const emblemFile = document.getElementById("emblemFile");
    const emblemStatus = document.getElementById("emblemStatus");
    const personalInfoEditBtn = document.getElementById("personalInfoEditBtn");
    const personalInfoModalOverlay = document.getElementById("personalInfoModalOverlay");
    const closePersonalInfoModal = document.getElementById("closePersonalInfoModal");
    const cancelPersonalInfoModal = document.getElementById("cancelPersonalInfoModal");
    const savePersonalInfoBtn = document.getElementById("savePersonalInfoBtn");
    const personalInfoModalStatus = document.getElementById("personalInfoModalStatus");
    const physicalTraitsEditBtn = document.getElementById("physicalTraitsEditBtn");
    const physicalTraitsModalOverlay = document.getElementById("physicalTraitsModalOverlay");
    const closePhysicalTraitsModal = document.getElementById("closePhysicalTraitsModal");
    const cancelPhysicalTraitsModal = document.getElementById("cancelPhysicalTraitsModal");
    const savePhysicalTraitsBtn = document.getElementById("savePhysicalTraitsBtn");
    const physicalTraitsModalStatus = document.getElementById("physicalTraitsModalStatus");
    const educationEditBtn = document.getElementById("educationEditBtn");
    const educationModalOverlay = document.getElementById("educationModalOverlay");
    const closeEducationModal = document.getElementById("closeEducationModal");
    const cancelEducationModal = document.getElementById("cancelEducationModal");
    const saveEducationBtn = document.getElementById("saveEducationBtn");
    const educationModalStatus = document.getElementById("educationModalStatus");
    const curiositiesEditBtn = document.getElementById("curiositiesEditBtn");
    const curiositiesModalOverlay = document.getElementById("curiositiesModalOverlay");
    const closeCuriositiesModal = document.getElementById("closeCuriositiesModal");
    const cancelCuriositiesModal = document.getElementById("cancelCuriositiesModal");
    const saveCuriositiesBtn = document.getElementById("saveCuriositiesBtn");
    const curiositiesModalStatus = document.getElementById("curiositiesModalStatus");
    const professionalInfoEditBtn = document.getElementById("professionalInfoEditBtn");
    const professionalInfoModalOverlay = document.getElementById("professionalInfoModalOverlay");
    const closeProfessionalInfoModal = document.getElementById("closeProfessionalInfoModal");
    const cancelProfessionalInfoModal = document.getElementById("cancelProfessionalInfoModal");
    const saveProfessionalInfoBtn = document.getElementById("saveProfessionalInfoBtn");
    const professionalInfoModalStatus = document.getElementById("professionalInfoModalStatus");
    const aboutEditBtn = document.getElementById("aboutEditBtn");
    const aboutModalOverlay = document.getElementById("aboutModalOverlay");
    const closeAboutModal = document.getElementById("closeAboutModal");
    const cancelAboutModal = document.getElementById("cancelAboutModal");
    const saveAboutBtn = document.getElementById("saveAboutBtn");
    const aboutModalStatus = document.getElementById("aboutModalStatus");
    const aboutDisplayNameInput = document.getElementById("aboutDisplayNameInput");
    const aboutTextInput = document.getElementById("aboutTextInput");
    const aboutWordCounter = document.getElementById("aboutWordCounter");
    const aboutDisplayNameValue = document.getElementById("aboutDisplayNameValue");
    const aboutTextValue = document.getElementById("aboutTextValue");
    const aboutEmptyState = document.getElementById("aboutEmptyState");
    const dreamEditBtn = document.getElementById("dreamEditBtn");
    const dreamModalOverlay = document.getElementById("dreamModalOverlay");
    const closeDreamModal = document.getElementById("closeDreamModal");
    const cancelDreamModal = document.getElementById("cancelDreamModal");
    const saveDreamBtn = document.getElementById("saveDreamBtn");
    const dreamModalStatus = document.getElementById("dreamModalStatus");
    const dreamTitleInput = document.getElementById("dreamTitleInput");
    const dreamTextInput = document.getElementById("dreamTextInput");
    const dreamWordCounter = document.getElementById("dreamWordCounter");
    const dreamTitleValue = document.getElementById("dreamTitleValue");
    const dreamTextValue = document.getElementById("dreamTextValue");
    const dreamEmptyState = document.getElementById("dreamEmptyState");
    const proAchievementsEditBtn = document.getElementById("proAchievementsEditBtn");
    const proAchievementsModalOverlay = document.getElementById("proAchievementsModalOverlay");
    const closeProAchievementsModal = document.getElementById("closeProAchievementsModal");
    const cancelProAchievementsModal = document.getElementById("cancelProAchievementsModal");
    const saveProAchievementsBtn = document.getElementById("saveProAchievementsBtn");
    const proAchievementsModalStatus = document.getElementById("proAchievementsModalStatus");
    const proAchievementsTitleInput = document.getElementById("proAchievementsTitleInput");
    const proAchievementsTextInput = document.getElementById("proAchievementsTextInput");
    const proAchievementsWordCounter = document.getElementById("proAchievementsWordCounter");
    const proAchievementsTitleValue = document.getElementById("proAchievementsTitleValue");
    const proAchievementsTextValue = document.getElementById("proAchievementsTextValue");
    const proAchievementsEmptyState = document.getElementById("proAchievementsEmptyState");
    const lifeAchievementsEditBtn = document.getElementById("lifeAchievementsEditBtn");
    const lifeAchievementsModalOverlay = document.getElementById("lifeAchievementsModalOverlay");
    const closeLifeAchievementsModal = document.getElementById("closeLifeAchievementsModal");
    const cancelLifeAchievementsModal = document.getElementById("cancelLifeAchievementsModal");
    const saveLifeAchievementsBtn = document.getElementById("saveLifeAchievementsBtn");
    const lifeAchievementsModalStatus = document.getElementById("lifeAchievementsModalStatus");
    const lifeAchievementsTitleInput = document.getElementById("lifeAchievementsTitleInput");
    const lifeAchievementsTextInput = document.getElementById("lifeAchievementsTextInput");
    const lifeAchievementsWordCounter = document.getElementById("lifeAchievementsWordCounter");
    const lifeAchievementsTitleValue = document.getElementById("lifeAchievementsTitleValue");
    const lifeAchievementsTextValue = document.getElementById("lifeAchievementsTextValue");
    const lifeAchievementsEmptyState = document.getElementById("lifeAchievementsEmptyState");
    const quotesEditBtn = document.getElementById("quotesEditBtn");
    const quotesModalOverlay = document.getElementById("quotesModalOverlay");
    const closeQuotesModal = document.getElementById("closeQuotesModal");
    const cancelQuotesModal = document.getElementById("cancelQuotesModal");
    const saveQuotesBtn = document.getElementById("saveQuotesBtn");
    const quotesModalStatus = document.getElementById("quotesModalStatus");
    const quotesTitleInput = document.getElementById("quotesTitleInput");
    const quotesTextInput = document.getElementById("quotesTextInput");
    const quotesWordCounter = document.getElementById("quotesWordCounter");
    const quotesTitleValue = document.getElementById("quotesTitleValue");
    const quotesTextValue = document.getElementById("quotesTextValue");
    const quotesEmptyState = document.getElementById("quotesEmptyState");
    const distinctionsEditBtn = document.getElementById("distinctionsEditBtn");
    const distinctionsModalOverlay = document.getElementById("distinctionsModalOverlay");
    const closeDistinctionsModal = document.getElementById("closeDistinctionsModal");
    const cancelDistinctionsModal = document.getElementById("cancelDistinctionsModal");
    const saveDistinctionsBtn = document.getElementById("saveDistinctionsBtn");
    const distinctionsModalStatus = document.getElementById("distinctionsModalStatus");
    const distinctionsRows = document.getElementById("distinctionsRows");
    const distinctionsForm = document.getElementById("distinctionsForm");
    const tocAboutLabel = document.querySelector('[data-toc="about"]');
    const tocDreamLabel = document.querySelector('[data-toc="dream"]');
    const tocProLabel = document.querySelector('[data-toc="pro"]');
    const tocLifeLabel = document.querySelector('[data-toc="life"]');
    const tocQuotesLabel = document.querySelector('[data-toc="quotes"]');
    const tocUserName = document.getElementById("tocUserName");
    const infoName = document.getElementById("infoName");

    const personalBirthNameInput = document.getElementById("personalBirthNameInput");
    const personalBirthDateInput = document.getElementById("personalBirthDateInput");
    const personalBirthCityInput = document.getElementById("personalBirthCityInput");
    const personalBirthRegionInput = document.getElementById("personalBirthRegionInput");
    const personalBirthCountryInput = document.getElementById("personalBirthCountryInput");
    const personalResidenceInput = document.getElementById("personalResidenceInput");
    const personalNationalityInput = document.getElementById("personalNationalityInput");
    const personalNativeLanguageInput = document.getElementById("personalNativeLanguageInput");
    const personalPseudonymsInput = document.getElementById("personalPseudonymsInput");

    const personalInfoBirthNameValue = document.getElementById("personalInfoBirthNameValue");
    const personalInfoBirthValue = document.getElementById("personalInfoBirthValue");
    const personalInfoResidenceValue = document.getElementById("personalInfoResidenceValue");
    const personalInfoNationalityValue = document.getElementById("personalInfoNationalityValue");
    const personalInfoNativeLanguageValue = document.getElementById("personalInfoNativeLanguageValue");
    const personalInfoPseudonymsValue = document.getElementById("personalInfoPseudonymsValue");
    const physicalHeightInput = document.getElementById("physicalHeightInput");
    const physicalWeightInput = document.getElementById("physicalWeightInput");
    const physicalEyesInput = document.getElementById("physicalEyesInput");
    const physicalHairInput = document.getElementById("physicalHairInput");
    const physicalTraitsHeightValue = document.getElementById("physicalTraitsHeightValue");
    const physicalTraitsWeightValue = document.getElementById("physicalTraitsWeightValue");
    const physicalTraitsEyesValue = document.getElementById("physicalTraitsEyesValue");
    const physicalTraitsHairValue = document.getElementById("physicalTraitsHairValue");
    const educationSlot1Input = document.getElementById("educationSlot1Input");
    const educationSlot2Input = document.getElementById("educationSlot2Input");
    const educationSlot3Input = document.getElementById("educationSlot3Input");
    const educationSlot4Input = document.getElementById("educationSlot4Input");
    const educationSlot1Value = document.getElementById("educationSlot1Value");
    const educationSlot2Value = document.getElementById("educationSlot2Value");
    const educationSlot3Value = document.getElementById("educationSlot3Value");
    const educationSlot4Value = document.getElementById("educationSlot4Value");
    const curiosityHeroInput = document.getElementById("curiosityHeroInput");
    const curiositySongInput = document.getElementById("curiositySongInput");
    const curiosityFoodInput = document.getElementById("curiosityFoodInput");
    const curiosityGamesInput = document.getElementById("curiosityGamesInput");
    const curiosityBookInput = document.getElementById("curiosityBookInput");
    const curiosityHobbiesInput = document.getElementById("curiosityHobbiesInput");
    const curiosityMottoInput = document.getElementById("curiosityMottoInput");
    const curiositiesHeroValue = document.getElementById("curiositiesHeroValue");
    const curiositiesSongValue = document.getElementById("curiositiesSongValue");
    const curiositiesFoodValue = document.getElementById("curiositiesFoodValue");
    const curiositiesGamesValue = document.getElementById("curiositiesGamesValue");
    const curiositiesBookValue = document.getElementById("curiositiesBookValue");
    const curiositiesHobbiesValue = document.getElementById("curiositiesHobbiesValue");
    const curiositiesMottoValue = document.getElementById("curiositiesMottoValue");
    const professionalOccupationInput = document.getElementById("professionalOccupationInput");
    const professionalActiveYearsInput = document.getElementById("professionalActiveYearsInput");
    const professionalOccupationValue = document.getElementById("professionalOccupationValue");
    const professionalActiveYearsValue = document.getElementById("professionalActiveYearsValue");
    const wishesFulfilledValue = document.getElementById("wishesFulfilledValue");
    const cooperativeWishesFulfilledValue = document.getElementById("cooperativeWishesFulfilledValue");
    const wishesGrantedValue = document.getElementById("wishesGrantedValue");
    const activityRankRow = document.getElementById("activityRankRow");
    const activityRankValue = document.getElementById("activityRankValue");

    const defaultProfilePhotoSrc = profilePhoto?.getAttribute("src") || "/css/logo-kiadez.webp";
    const defaultEmblemSrc = emblemImage?.getAttribute("src") || "/css/logo-kiadez.webp";
    const ABOUT_MAX_WORDS = 1200;
    const DREAM_MAX_WORDS = 1200;
    const PRO_ACHIEVEMENTS_MAX_WORDS = 500;
    const LIFE_ACHIEVEMENTS_MAX_WORDS = 500;
    const FAVORITE_QUOTES_MAX_WORDS = 500;
    const DISTINCTIONS_MAX_SLOTS = 10;
    const GUARDIAN_MIN_RANK = 3;
    const GUARDIAN_RANK_NAMES = Object.freeze({
      0: tr("Sin rango", "No rank", "Sans rang"),
      1: tr("Aspirante", "Aspirant", "Aspirant"),
      2: tr("Aprendiz", "Apprentice", "Apprenti"),
      3: tr("Guardián", "Guardian", "Gardien"),
      4: tr("Guardián Consagrado", "Consecrated Guardian", "Gardien Consacré"),
      5: tr("Guardián Mayor", "Senior Guardian", "Gardien Majeur"),
      6: tr("Guardián del Logos", "Guardian of the Logos", "Gardien du Logos"),
      7: tr("Guardián del Umbral", "Guardian of the Threshold", "Gardien du Seuil"),
      8: tr("Guardián de Guardianes", "Guardian of Guardians", "Gardien des Gardiens"),
    });
    const defaultAboutDisplayName = (aboutDisplayNameValue?.textContent || infoName?.textContent || tr("Usuario Kiadez", "Kiadez User", "Utilisateur Kiadez")).trim();
    const defaultDreamTitle = (dreamTitleValue?.textContent || tr("Sobre su mayor sueño", "About their greatest dream", "À propos de son plus grand rêve")).trim();
    const defaultProAchievementsTitle = (
      proAchievementsTitleValue?.textContent || tr("Logros profesionales", "Professional achievements", "Réalisations professionnelles")
    ).trim();
    const defaultLifeAchievementsTitle = (
      lifeAchievementsTitleValue?.textContent || tr("Logros alcanzados", "Life achievements", "Réalisations de vie")
    ).trim();
    const defaultQuotesTitle = (quotesTitleValue?.textContent || tr("Frases favoritas", "Favorite quotes", "Citations favorites")).trim();
    let currentPersonalInfo = null;
    let currentPhysicalTraits = null;
    let currentEducation = null;
    let currentCuriosities = null;
    let currentProfessionalInfo = null;
    let currentAbout = null;
    let currentDream = null;
    let currentProAchievements = null;
    let currentLifeAchievements = null;
    let currentFavoriteQuotes = null;
    let currentDistinctions = null;
    let viewerUserId = null;
    let viewerUsername = "";
    let viewerGuardianRank = 0;
    let activeProfileUserId = null;
    let activeProfileUsername = "";
    let isViewingOwnProfile = true;
    let profileContextResolved = false;

    const getAccessToken = () => localStorage.getItem("access_token") || "";

    const setBioPhotoStatus = (message, isError = false) => {
      if (!bioPhotoStatus) return;
      bioPhotoStatus.textContent = message || "";
      bioPhotoStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setEmblemStatus = (message, isError = false) => {
      if (!emblemStatus) return;
      emblemStatus.textContent = message || "";
      emblemStatus.classList.toggle("is-error", Boolean(isError));
    };

    const apiFetch = async (path, options = {}) => {
      const token = getAccessToken();
      if (!token) throw new Error(tr("No hay sesión activa.", "No active session.", "Aucune session active."));
      const headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`,
      };
      const res = await fetch(`${API}${path}`, { ...options, headers });
      if (res.status === 401) {
        throw new Error(tr("Sesión expirada. Inicia sesión nuevamente.", "Session expired. Sign in again.", "Session expirée. Connecte-toi de nouveau."));
      }
      return res;
    };

    const setPersonalInfoModalStatus = (message, isError = false) => {
      if (!personalInfoModalStatus) return;
      personalInfoModalStatus.textContent = message || "";
      personalInfoModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setPhysicalTraitsModalStatus = (message, isError = false) => {
      if (!physicalTraitsModalStatus) return;
      physicalTraitsModalStatus.textContent = message || "";
      physicalTraitsModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setEducationModalStatus = (message, isError = false) => {
      if (!educationModalStatus) return;
      educationModalStatus.textContent = message || "";
      educationModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setCuriositiesModalStatus = (message, isError = false) => {
      if (!curiositiesModalStatus) return;
      curiositiesModalStatus.textContent = message || "";
      curiositiesModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setProfessionalInfoModalStatus = (message, isError = false) => {
      if (!professionalInfoModalStatus) return;
      professionalInfoModalStatus.textContent = message || "";
      professionalInfoModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setAboutModalStatus = (message, isError = false) => {
      if (!aboutModalStatus) return;
      aboutModalStatus.textContent = message || "";
      aboutModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setDreamModalStatus = (message, isError = false) => {
      if (!dreamModalStatus) return;
      dreamModalStatus.textContent = message || "";
      dreamModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setProAchievementsModalStatus = (message, isError = false) => {
      if (!proAchievementsModalStatus) return;
      proAchievementsModalStatus.textContent = message || "";
      proAchievementsModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setLifeAchievementsModalStatus = (message, isError = false) => {
      if (!lifeAchievementsModalStatus) return;
      lifeAchievementsModalStatus.textContent = message || "";
      lifeAchievementsModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setQuotesModalStatus = (message, isError = false) => {
      if (!quotesModalStatus) return;
      quotesModalStatus.textContent = message || "";
      quotesModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const setDistinctionsModalStatus = (message, isError = false) => {
      if (!distinctionsModalStatus) return;
      distinctionsModalStatus.textContent = message || "";
      distinctionsModalStatus.classList.toggle("is-error", Boolean(isError));
    };

    const parsePositiveId = (value) => {
      const normalized = Number(value);
      if (!Number.isFinite(normalized) || normalized <= 0) return null;
      return Math.trunc(normalized);
    };

    const normalizeGuardianRank = (value) => {
      const normalized = Number(value);
      if (!Number.isFinite(normalized)) return 0;
      return Math.max(0, Math.trunc(normalized));
    };

    const normalizeUsername = (value) => {
      let normalized = String(value || "").trim().toLowerCase();
      while (normalized.startsWith("@")) normalized = normalized.slice(1);
      return normalized;
    };

    const isViewerGuardian = () => Number(viewerGuardianRank || 0) >= GUARDIAN_MIN_RANK;

    const buildDistinctionsEndpoint = ({ includeTarget = false } = {}) => {
      if (!includeTarget || isViewingOwnProfile) {
        return "/biography/distinctions";
      }
      const profileId = parsePositiveId(activeProfileUserId);
      if (!profileId) {
        throw new Error(tr("No se pudo identificar el perfil a editar.", "Could not identify the profile to edit.", "Impossible d'identifier le profil à modifier."));
      }
      return `/biography/distinctions/${encodeURIComponent(String(profileId))}`;
    };

    const fetchViewerIdentity = async () => {
      const res = await apiFetch("/auth/me");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo cargar tu sesión.", "Could not load your session.", "Impossible de charger ta session."));
      }
      return data;
    };

    const fetchFollowProfile = async ({ userId = null, username = "" } = {}) => {
      const safeUserId = parsePositiveId(userId);
      const safeUsername = normalizeUsername(username);
      if (!safeUserId && !safeUsername) return null;
      const query = safeUserId
        ? `user_id=${encodeURIComponent(String(safeUserId))}`
        : `username=${encodeURIComponent(safeUsername)}`;
      const res = await apiFetch(`/follows/profile?${query}`);
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo cargar el perfil solicitado.", "Could not load the requested profile.", "Impossible de charger le profil demandé."));
      }
      return data;
    };

    const buildProfileFullName = (payload = {}) => {
      const fullName = String(payload?.full_name || "").trim();
      if (fullName) return fullName;
      const firstName = String(payload?.first_name || "").trim();
      const lastName = String(payload?.last_name || "").trim();
      return `${firstName} ${lastName}`.trim();
    };

    const applyInfoName = (value) => {
      if (!infoName) return;
      const normalizedName = String(value || "").trim() || tr("Usuario Kiadez", "Kiadez User", "Utilisateur Kiadez");
      infoName.textContent = normalizedName;
      infoName.classList.toggle("is-long", normalizedName.length > 26);
      infoName.classList.toggle("is-very-long", normalizedName.length > 36);
    };

    const applyDistinctionsEditorVisibility = () => {
      const canEdit = isViewerGuardian();
      if (distinctionsEditBtn) {
        distinctionsEditBtn.classList.toggle("hidden", !canEdit);
        distinctionsEditBtn.disabled = !canEdit;
      }
    };

    const applyActivityRankToView = (rankValue) => {
      const rank = normalizeGuardianRank(rankValue);
      const rankName = GUARDIAN_RANK_NAMES[rank] || tr(`Rango ${rank}`, `Rank ${rank}`, `Rank ${rank}`);
      if (activityRankValue) {
        activityRankValue.textContent = rank > 0 ? tr(`Rango ${rank} · ${rankName}`, `Rank ${rank} · ${rankName}`, `Rank ${rank} · ${rankName}`) : "";
      }
      if (activityRankRow) {
        activityRankRow.classList.toggle("hidden", rank <= 0);
      }
    };

    const ensureDistinctionsForm = () => {
      if (!distinctionsForm) return;
      if (distinctionsForm.childElementCount > 0) return;

      distinctionsForm.innerHTML = Array.from({ length: DISTINCTIONS_MAX_SLOTS }, (_, index) => {
        const slotNumber = index + 1;
        return `
          <div class="distinction-slot-card">
            <p class="distinction-slot-title">${tr("Distinción", "Distinction", "Distinction")} ${slotNumber}</p>
            <label class="modal-label" for="distinctionTypeInput${slotNumber}">${tr("Tipo de distinción", "Distinction type", "Type de distinction")}</label>
            <input class="modal-input" id="distinctionTypeInput${slotNumber}" type="text" maxlength="120" />
            <label class="modal-label" for="distinctionDescriptionInput${slotNumber}">${tr("Descripción", "Description", "Description")}</label>
            <input class="modal-input" id="distinctionDescriptionInput${slotNumber}" type="text" maxlength="500" />
          </div>
        `;
      }).join("");
    };

    const getDistinctionTypeInput = (slotNumber) => document.getElementById(`distinctionTypeInput${slotNumber}`);
    const getDistinctionDescriptionInput = (slotNumber) => document.getElementById(`distinctionDescriptionInput${slotNumber}`);

    const resolveBiographyProfileContext = async () => {
      if (profileContextResolved) return;

      const me = await fetchViewerIdentity();
      viewerUserId = parsePositiveId(me?.user_number || me?.user_id);
      viewerGuardianRank = normalizeGuardianRank(me?.guardian_rank);
      viewerUsername = normalizeUsername(me?.username || "");
      activeProfileUserId = viewerUserId;
      activeProfileUsername = viewerUsername;
      isViewingOwnProfile = true;
      applyActivityRankToView(viewerGuardianRank);
      const meFullName = buildProfileFullName(me);
      if (meFullName) {
        applyInfoName(meFullName);
      }

      if (viewerUserId || viewerUsername) {
        try {
          const viewerProfile = await fetchFollowProfile({ userId: viewerUserId, username: viewerUsername });
          const viewerFullName = buildProfileFullName(viewerProfile);
          if (viewerFullName) {
            applyInfoName(viewerFullName);
          }
          viewerGuardianRank = normalizeGuardianRank(viewerProfile?.guardian_rank);
          applyActivityRankToView(viewerGuardianRank);
        } catch {
          // Keep the best-effort name from /auth/me.
        }
      }

      const params = new URLSearchParams(window.location.search);
      const requestedUserId = parsePositiveId(params.get("id"));
      const requestedUsername = normalizeUsername(params.get("u"));
      const wantsOtherProfile = Boolean(requestedUserId || requestedUsername);

      if (wantsOtherProfile) {
        const isSelfById = requestedUserId && viewerUserId && requestedUserId === viewerUserId;
        const isSelfByUsername = requestedUsername && viewerUsername && requestedUsername === viewerUsername;

        if (!isSelfById && !isSelfByUsername) {
          const profile = await fetchFollowProfile({
            userId: requestedUserId,
            username: requestedUserId ? "" : requestedUsername,
          });
          const targetUserId = parsePositiveId(profile?.user_id);
          if (targetUserId) {
            activeProfileUserId = targetUserId;
            activeProfileUsername = normalizeUsername(profile?.username || "");
            isViewingOwnProfile = Boolean(viewerUserId && targetUserId === viewerUserId);
            const fullName = String(profile?.full_name || "").trim();
            if (fullName) applyInfoName(fullName);
            applyActivityRankToView(profile?.guardian_rank);
          }
        }
      }

      profileContextResolved = true;
      applyDistinctionsEditorVisibility();
    };

    const countWords = (value) => {
      if (!value) return 0;
      return value
        .trim()
        .split(/\s+/)
        .filter(Boolean).length;
    };

    const setTextOrFallback = (element, value) => {
      if (!element) return;
      const cleanValue = (value || "").trim();
      element.textContent = cleanValue || "Prefiero no decirlo";
    };

    const setTextOrEmpty = (element, value) => {
      if (!element) return;
      element.textContent = (value || "").trim();
    };

    const applyPersonalInfoToView = (info) => {
      setTextOrFallback(personalInfoBirthNameValue, info?.birth_name);
      setTextOrFallback(personalInfoBirthValue, info?.birth_display);
      setTextOrFallback(personalInfoResidenceValue, info?.residence);
      setTextOrFallback(personalInfoNationalityValue, info?.nationality);
      setTextOrFallback(personalInfoNativeLanguageValue, info?.native_language);
      setTextOrFallback(personalInfoPseudonymsValue, info?.pseudonyms);
    };

    const applyPhysicalTraitsToView = (traits) => {
      setTextOrFallback(physicalTraitsHeightValue, traits?.height);
      setTextOrFallback(physicalTraitsWeightValue, traits?.weight);
      setTextOrFallback(physicalTraitsEyesValue, traits?.eyes);
      setTextOrFallback(physicalTraitsHairValue, traits?.hair);
    };

    const applyEducationToView = (education) => {
      setTextOrEmpty(educationSlot1Value, education?.slot1);
      setTextOrEmpty(educationSlot2Value, education?.slot2);
      setTextOrEmpty(educationSlot3Value, education?.slot3);
      setTextOrEmpty(educationSlot4Value, education?.slot4);
    };

    const applyCuriositiesToView = (curiosities) => {
      setTextOrFallback(curiositiesHeroValue, curiosities?.favorite_superhero);
      setTextOrFallback(curiositiesSongValue, curiosities?.favorite_song);
      setTextOrFallback(curiositiesFoodValue, curiosities?.favorite_food);
      setTextOrFallback(curiositiesGamesValue, curiosities?.videogames);
      setTextOrFallback(curiositiesBookValue, curiosities?.favorite_book);
      setTextOrFallback(curiositiesHobbiesValue, curiosities?.other_hobbies);
      setTextOrFallback(curiositiesMottoValue, curiosities?.motto);
    };

    const applyProfessionalInfoToView = (professionalInfo) => {
      setTextOrFallback(professionalOccupationValue, professionalInfo?.occupation);
      setTextOrFallback(professionalActiveYearsValue, professionalInfo?.active_years);
    };

    const normalizeDistinctionSlots = (value) => {
      const slots = Array.isArray(value?.slots) ? value.slots : [];
      return Array.from({ length: DISTINCTIONS_MAX_SLOTS }, (_, index) => {
        const slot = slots[index] || {};
        return {
          slot_number: index + 1,
          distinction_type: String(slot?.distinction_type || "").trim(),
          description: String(slot?.description || "").trim(),
        };
      });
    };

    const renderDistinctionsRows = (slots) => {
      if (!distinctionsRows) return;
      distinctionsRows.innerHTML = "";

      const normalizedSlots = Array.isArray(slots) ? slots : [];
      const visibleSlots = normalizedSlots.filter((slot) => slot.distinction_type || slot.description);
      if (!visibleSlots.length) return;

      visibleSlots.forEach((slot) => {
        const row = document.createElement("tr");
        const header = document.createElement("th");
        header.textContent = slot.distinction_type || `${tr("Distinción", "Distinction", "Distinction")} ${slot.slot_number}`;
        const detail = document.createElement("td");
        detail.textContent = slot.description || "";
        row.appendChild(header);
        row.appendChild(detail);
        distinctionsRows.appendChild(row);
      });
    };

    const applyDistinctionsToView = (distinctions) => {
      const slots = normalizeDistinctionSlots(distinctions);
      currentDistinctions = { slots };
      renderDistinctionsRows(slots);
    };

    const fillDistinctionsForm = (distinctions) => {
      ensureDistinctionsForm();
      const slots = normalizeDistinctionSlots(distinctions);
      for (let slotNumber = 1; slotNumber <= DISTINCTIONS_MAX_SLOTS; slotNumber += 1) {
        const slot = slots[slotNumber - 1];
        const typeInput = getDistinctionTypeInput(slotNumber);
        const descriptionInput = getDistinctionDescriptionInput(slotNumber);
        if (typeInput) typeInput.value = slot?.distinction_type || "";
        if (descriptionInput) descriptionInput.value = slot?.description || "";
      }
      setDistinctionsModalStatus("");
    };

    const buildDistinctionsPayload = () => {
      const slots = [];
      for (let slotNumber = 1; slotNumber <= DISTINCTIONS_MAX_SLOTS; slotNumber += 1) {
        const typeInput = getDistinctionTypeInput(slotNumber);
        const descriptionInput = getDistinctionDescriptionInput(slotNumber);
        slots.push({
          distinction_type: typeInput?.value?.trim() || null,
          description: descriptionInput?.value?.trim() || null,
        });
      }
      return { slots };
    };

    const normalizeActivityCount = (value) => {
      const numeric = Number(value);
      if (!Number.isFinite(numeric)) return "0";
      return String(Math.max(0, Math.trunc(numeric)));
    };

    const applyActivityStatsToView = (stats) => {
      if (wishesFulfilledValue) {
        wishesFulfilledValue.textContent = normalizeActivityCount(stats?.wishes_fulfilled);
      }
      if (cooperativeWishesFulfilledValue) {
        cooperativeWishesFulfilledValue.textContent = normalizeActivityCount(stats?.cooperative_wishes_fulfilled);
      }
      if (wishesGrantedValue) {
        wishesGrantedValue.textContent = normalizeActivityCount(stats?.wishes_granted);
      }
    };

    const applyAboutToView = (about) => {
      const displayName = (about?.display_name || "").trim() || defaultAboutDisplayName;
      const aboutText = (about?.about_text || "").trim();

      if (aboutDisplayNameValue) aboutDisplayNameValue.textContent = displayName;
      if (tocAboutLabel) tocAboutLabel.textContent = displayName;
      if (tocUserName) tocUserName.textContent = displayName;

      if (aboutTextValue) {
        aboutTextValue.textContent = aboutText;
        aboutTextValue.classList.toggle("hidden", !aboutText);
      }
      if (aboutEmptyState) {
        aboutEmptyState.classList.toggle("hidden", Boolean(aboutText));
      }
    };

    const applyDreamToView = (dream) => {
      const dreamTitle = (dream?.dream_title || "").trim() || defaultDreamTitle;
      const dreamText = (dream?.dream_text || "").trim();

      if (dreamTitleValue) dreamTitleValue.textContent = dreamTitle;
      if (tocDreamLabel) tocDreamLabel.textContent = dreamTitle;

      if (dreamTextValue) {
        dreamTextValue.textContent = dreamText;
        dreamTextValue.classList.toggle("hidden", !dreamText);
      }
      if (dreamEmptyState) {
        dreamEmptyState.classList.toggle("hidden", Boolean(dreamText));
      }
    };

    const applyProAchievementsToView = (section) => {
      const sectionTitle = (section?.section_title || "").trim() || defaultProAchievementsTitle;
      const sectionText = (section?.section_text || "").trim();

      if (proAchievementsTitleValue) proAchievementsTitleValue.textContent = sectionTitle;
      if (tocProLabel) tocProLabel.textContent = sectionTitle;

      if (proAchievementsTextValue) {
        proAchievementsTextValue.textContent = sectionText;
        proAchievementsTextValue.classList.toggle("hidden", !sectionText);
      }
      if (proAchievementsEmptyState) {
        proAchievementsEmptyState.classList.toggle("hidden", Boolean(sectionText));
      }
    };

    const applyLifeAchievementsToView = (section) => {
      const sectionTitle = (section?.section_title || "").trim() || defaultLifeAchievementsTitle;
      const sectionText = (section?.section_text || "").trim();

      if (lifeAchievementsTitleValue) lifeAchievementsTitleValue.textContent = sectionTitle;
      if (tocLifeLabel) tocLifeLabel.textContent = sectionTitle;

      if (lifeAchievementsTextValue) {
        lifeAchievementsTextValue.textContent = sectionText;
        lifeAchievementsTextValue.classList.toggle("hidden", !sectionText);
      }
      if (lifeAchievementsEmptyState) {
        lifeAchievementsEmptyState.classList.toggle("hidden", Boolean(sectionText));
      }
    };

    const applyQuotesToView = (section) => {
      const sectionTitle = (section?.section_title || "").trim() || defaultQuotesTitle;
      const sectionText = (section?.section_text || "").trim();

      if (quotesTitleValue) quotesTitleValue.textContent = sectionTitle;
      if (tocQuotesLabel) tocQuotesLabel.textContent = sectionTitle;

      if (quotesTextValue) {
        quotesTextValue.textContent = sectionText;
        quotesTextValue.classList.toggle("hidden", !sectionText);
      }
      if (quotesEmptyState) {
        quotesEmptyState.classList.toggle("hidden", Boolean(sectionText));
      }
    };

    const updateAboutWordCounter = () => {
      if (!aboutWordCounter) return;
      const totalWords = countWords(aboutTextInput?.value || "");
      aboutWordCounter.textContent = `${totalWords} / ${ABOUT_MAX_WORDS} palabras`;
      aboutWordCounter.classList.toggle("is-error", totalWords > ABOUT_MAX_WORDS);
    };

    const updateDreamWordCounter = () => {
      if (!dreamWordCounter) return;
      const totalWords = countWords(dreamTextInput?.value || "");
      dreamWordCounter.textContent = `${totalWords} / ${DREAM_MAX_WORDS} palabras`;
      dreamWordCounter.classList.toggle("is-error", totalWords > DREAM_MAX_WORDS);
    };

    const updateProAchievementsWordCounter = () => {
      if (!proAchievementsWordCounter) return;
      const totalWords = countWords(proAchievementsTextInput?.value || "");
      proAchievementsWordCounter.textContent = `${totalWords} / ${PRO_ACHIEVEMENTS_MAX_WORDS} palabras`;
      proAchievementsWordCounter.classList.toggle("is-error", totalWords > PRO_ACHIEVEMENTS_MAX_WORDS);
    };

    const updateLifeAchievementsWordCounter = () => {
      if (!lifeAchievementsWordCounter) return;
      const totalWords = countWords(lifeAchievementsTextInput?.value || "");
      lifeAchievementsWordCounter.textContent = `${totalWords} / ${LIFE_ACHIEVEMENTS_MAX_WORDS} palabras`;
      lifeAchievementsWordCounter.classList.toggle("is-error", totalWords > LIFE_ACHIEVEMENTS_MAX_WORDS);
    };

    const updateQuotesWordCounter = () => {
      if (!quotesWordCounter) return;
      const totalWords = countWords(quotesTextInput?.value || "");
      quotesWordCounter.textContent = `${totalWords} / ${FAVORITE_QUOTES_MAX_WORDS} palabras`;
      quotesWordCounter.classList.toggle("is-error", totalWords > FAVORITE_QUOTES_MAX_WORDS);
    };

    const fillPersonalInfoForm = (info) => {
      if (personalBirthNameInput) personalBirthNameInput.value = info?.birth_name || "";
      if (personalBirthDateInput) personalBirthDateInput.value = info?.birth_date || "";
      if (personalBirthCityInput) personalBirthCityInput.value = info?.birth_city || "";
      if (personalBirthRegionInput) personalBirthRegionInput.value = info?.birth_region || "";
      if (personalBirthCountryInput) personalBirthCountryInput.value = info?.birth_country || "";
      if (personalResidenceInput) personalResidenceInput.value = info?.residence || "";
      if (personalNationalityInput) personalNationalityInput.value = info?.nationality || "";
      if (personalNativeLanguageInput) personalNativeLanguageInput.value = info?.native_language || "";
      if (personalPseudonymsInput) personalPseudonymsInput.value = info?.pseudonyms || "";
      setPersonalInfoModalStatus("");
    };

    const fillPhysicalTraitsForm = (traits) => {
      if (physicalHeightInput) physicalHeightInput.value = traits?.height || "";
      if (physicalWeightInput) physicalWeightInput.value = traits?.weight || "";
      if (physicalEyesInput) physicalEyesInput.value = traits?.eyes || "";
      if (physicalHairInput) physicalHairInput.value = traits?.hair || "";
      setPhysicalTraitsModalStatus("");
    };

    const fillEducationForm = (education) => {
      if (educationSlot1Input) educationSlot1Input.value = education?.slot1 || "";
      if (educationSlot2Input) educationSlot2Input.value = education?.slot2 || "";
      if (educationSlot3Input) educationSlot3Input.value = education?.slot3 || "";
      if (educationSlot4Input) educationSlot4Input.value = education?.slot4 || "";
      setEducationModalStatus("");
    };

    const fillCuriositiesForm = (curiosities) => {
      if (curiosityHeroInput) curiosityHeroInput.value = curiosities?.favorite_superhero || "";
      if (curiositySongInput) curiositySongInput.value = curiosities?.favorite_song || "";
      if (curiosityFoodInput) curiosityFoodInput.value = curiosities?.favorite_food || "";
      if (curiosityGamesInput) curiosityGamesInput.value = curiosities?.videogames || "";
      if (curiosityBookInput) curiosityBookInput.value = curiosities?.favorite_book || "";
      if (curiosityHobbiesInput) curiosityHobbiesInput.value = curiosities?.other_hobbies || "";
      if (curiosityMottoInput) curiosityMottoInput.value = curiosities?.motto || "";
      setCuriositiesModalStatus("");
    };

    const fillProfessionalInfoForm = (professionalInfo) => {
      if (professionalOccupationInput) professionalOccupationInput.value = professionalInfo?.occupation || "";
      if (professionalActiveYearsInput) professionalActiveYearsInput.value = professionalInfo?.active_years || "";
      setProfessionalInfoModalStatus("");
    };

    const fillAboutForm = (about) => {
      if (aboutDisplayNameInput) {
        aboutDisplayNameInput.value = (about?.display_name || "").trim() || defaultAboutDisplayName;
      }
      if (aboutTextInput) {
        aboutTextInput.value = about?.about_text || "";
      }
      updateAboutWordCounter();
      setAboutModalStatus("");
    };

    const fillDreamForm = (dream) => {
      if (dreamTitleInput) {
        dreamTitleInput.value = (dream?.dream_title || "").trim() || defaultDreamTitle;
      }
      if (dreamTextInput) {
        dreamTextInput.value = dream?.dream_text || "";
      }
      updateDreamWordCounter();
      setDreamModalStatus("");
    };

    const fillProAchievementsForm = (section) => {
      if (proAchievementsTitleInput) {
        proAchievementsTitleInput.value = (section?.section_title || "").trim() || defaultProAchievementsTitle;
      }
      if (proAchievementsTextInput) {
        proAchievementsTextInput.value = section?.section_text || "";
      }
      updateProAchievementsWordCounter();
      setProAchievementsModalStatus("");
    };

    const fillLifeAchievementsForm = (section) => {
      if (lifeAchievementsTitleInput) {
        lifeAchievementsTitleInput.value = (section?.section_title || "").trim() || defaultLifeAchievementsTitle;
      }
      if (lifeAchievementsTextInput) {
        lifeAchievementsTextInput.value = section?.section_text || "";
      }
      updateLifeAchievementsWordCounter();
      setLifeAchievementsModalStatus("");
    };

    const fillQuotesForm = (section) => {
      if (quotesTitleInput) {
        quotesTitleInput.value = (section?.section_title || "").trim() || defaultQuotesTitle;
      }
      if (quotesTextInput) {
        quotesTextInput.value = section?.section_text || "";
      }
      updateQuotesWordCounter();
      setQuotesModalStatus("");
    };

    const openPersonalInfoModal = () => {
      personalInfoModalOverlay?.classList.remove("hidden");
      personalInfoModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const openPhysicalTraitsModal = () => {
      physicalTraitsModalOverlay?.classList.remove("hidden");
      physicalTraitsModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const openEducationModal = () => {
      educationModalOverlay?.classList.remove("hidden");
      educationModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const openCuriositiesModal = () => {
      curiositiesModalOverlay?.classList.remove("hidden");
      curiositiesModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const openProfessionalInfoModal = () => {
      professionalInfoModalOverlay?.classList.remove("hidden");
      professionalInfoModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const openAboutModal = () => {
      aboutModalOverlay?.classList.remove("hidden");
      aboutModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const openDreamModal = () => {
      dreamModalOverlay?.classList.remove("hidden");
      dreamModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const openProAchievementsModal = () => {
      proAchievementsModalOverlay?.classList.remove("hidden");
      proAchievementsModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const openLifeAchievementsModal = () => {
      lifeAchievementsModalOverlay?.classList.remove("hidden");
      lifeAchievementsModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const openQuotesModal = () => {
      quotesModalOverlay?.classList.remove("hidden");
      quotesModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const openDistinctionsModal = () => {
      distinctionsModalOverlay?.classList.remove("hidden");
      distinctionsModalOverlay?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const closePersonalInfoModalFn = () => {
      personalInfoModalOverlay?.classList.add("hidden");
      personalInfoModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const closePhysicalTraitsModalFn = () => {
      physicalTraitsModalOverlay?.classList.add("hidden");
      physicalTraitsModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const closeEducationModalFn = () => {
      educationModalOverlay?.classList.add("hidden");
      educationModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const closeCuriositiesModalFn = () => {
      curiositiesModalOverlay?.classList.add("hidden");
      curiositiesModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const closeProfessionalInfoModalFn = () => {
      professionalInfoModalOverlay?.classList.add("hidden");
      professionalInfoModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const closeAboutModalFn = () => {
      aboutModalOverlay?.classList.add("hidden");
      aboutModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const closeDreamModalFn = () => {
      dreamModalOverlay?.classList.add("hidden");
      dreamModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const closeProAchievementsModalFn = () => {
      proAchievementsModalOverlay?.classList.add("hidden");
      proAchievementsModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const closeLifeAchievementsModalFn = () => {
      lifeAchievementsModalOverlay?.classList.add("hidden");
      lifeAchievementsModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const closeQuotesModalFn = () => {
      quotesModalOverlay?.classList.add("hidden");
      quotesModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const closeDistinctionsModalFn = () => {
      distinctionsModalOverlay?.classList.add("hidden");
      distinctionsModalOverlay?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const loadPersonalInfo = async () => {
      const res = await apiFetch("/biography/personal-info");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(
          data.detail || tr("No se pudo cargar la información personal.", "Could not load personal information.", "Impossible de charger les informations personnelles.")
        );
      }
      currentPersonalInfo = data;
      applyPersonalInfoToView(data);
      return data;
    };

    const loadPhysicalTraits = async () => {
      const res = await apiFetch("/biography/physical-traits");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(
          data.detail || tr("No se pudieron cargar las características físicas.", "Could not load physical traits.", "Impossible de charger les caractéristiques physiques.")
        );
      }
      currentPhysicalTraits = data;
      applyPhysicalTraitsToView(data);
      return data;
    };

    const loadEducation = async () => {
      const res = await apiFetch("/biography/education");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo cargar Educación.", "Could not load education.", "Impossible de charger l'éducation."));
      }
      currentEducation = data;
      applyEducationToView(data);
      return data;
    };

    const loadCuriosities = async () => {
      const res = await apiFetch("/biography/curiosities");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudieron cargar las curiosidades.", "Could not load curiosities.", "Impossible de charger les curiosités."));
      }
      currentCuriosities = data;
      applyCuriositiesToView(data);
      return data;
    };

    const loadProfessionalInfo = async () => {
      const res = await apiFetch("/biography/professional-info");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(
          data.detail || tr("No se pudo cargar la información profesional.", "Could not load professional information.", "Impossible de charger les informations professionnelles.")
        );
      }
      currentProfessionalInfo = data;
      applyProfessionalInfoToView(data);
      return data;
    };

    const loadAbout = async () => {
      const res = await apiFetch("/biography/about");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo cargar tu biografía.", "Could not load your biography.", "Impossible de charger ta biographie."));
      }
      currentAbout = data;
      applyAboutToView(data);
      return data;
    };

    const loadDream = async () => {
      const res = await apiFetch("/biography/dream");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo cargar tu mayor sueño.", "Could not load your greatest dream.", "Impossible de charger ton plus grand rêve."));
      }
      currentDream = data;
      applyDreamToView(data);
      return data;
    };

    const loadProAchievements = async () => {
      const res = await apiFetch("/biography/professional-achievements");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudieron cargar tus logros profesionales.", "Could not load your professional achievements.", "Impossible de charger tes réalisations professionnelles."));
      }
      currentProAchievements = data;
      applyProAchievementsToView(data);
      return data;
    };

    const loadLifeAchievements = async () => {
      const res = await apiFetch("/biography/life-achievements");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudieron cargar tus logros alcanzados.", "Could not load your life achievements.", "Impossible de charger tes réalisations de vie."));
      }
      currentLifeAchievements = data;
      applyLifeAchievementsToView(data);
      return data;
    };

    const loadFavoriteQuotes = async () => {
      const res = await apiFetch("/biography/favorite-quotes");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudieron cargar tus frases favoritas.", "Could not load your favorite quotes.", "Impossible de charger tes citations favorites."));
      }
      currentFavoriteQuotes = data;
      applyQuotesToView(data);
      return data;
    };

    const loadDistinctions = async () => {
      const endpoint = buildDistinctionsEndpoint({ includeTarget: true });
      const res = await apiFetch(endpoint);
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudieron cargar las distinciones.", "Could not load distinctions.", "Impossible de charger les distinctions."));
      }
      currentDistinctions = data;
      applyDistinctionsToView(data);
      return data;
    };

    const loadActivityStats = async ({ userId = null } = {}) => {
      const requestedUserId = parsePositiveId(userId);
      const query = requestedUserId ? `?user_id=${encodeURIComponent(String(requestedUserId))}` : "";
      const res = await apiFetch(`/biography/activity-stats${query}`);
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo cargar la actividad de Kiadez.", "Could not load Kiadez activity.", "Impossible de charger l'activité Kiadez."));
      }
      applyActivityStatsToView(data);
      return data;
    };

    const buildPersonalInfoPayload = () => ({
      birth_name: personalBirthNameInput?.value?.trim() || null,
      birth_date: personalBirthDateInput?.value || null,
      birth_city: personalBirthCityInput?.value?.trim() || null,
      birth_region: personalBirthRegionInput?.value?.trim() || null,
      birth_country: personalBirthCountryInput?.value?.trim() || null,
      residence: personalResidenceInput?.value?.trim() || null,
      nationality: personalNationalityInput?.value?.trim() || null,
      native_language: personalNativeLanguageInput?.value?.trim() || null,
      pseudonyms: personalPseudonymsInput?.value?.trim() || null,
    });

    const buildPhysicalTraitsPayload = () => ({
      height: physicalHeightInput?.value?.trim() || null,
      weight: physicalWeightInput?.value?.trim() || null,
      eyes: physicalEyesInput?.value?.trim() || null,
      hair: physicalHairInput?.value?.trim() || null,
    });

    const buildEducationPayload = () => ({
      slot1: educationSlot1Input?.value?.trim() || null,
      slot2: educationSlot2Input?.value?.trim() || null,
      slot3: educationSlot3Input?.value?.trim() || null,
      slot4: educationSlot4Input?.value?.trim() || null,
    });

    const buildCuriositiesPayload = () => ({
      favorite_superhero: curiosityHeroInput?.value?.trim() || null,
      favorite_song: curiositySongInput?.value?.trim() || null,
      favorite_food: curiosityFoodInput?.value?.trim() || null,
      videogames: curiosityGamesInput?.value?.trim() || null,
      favorite_book: curiosityBookInput?.value?.trim() || null,
      other_hobbies: curiosityHobbiesInput?.value?.trim() || null,
      motto: curiosityMottoInput?.value?.trim() || null,
    });

    const buildProfessionalInfoPayload = () => ({
      occupation: professionalOccupationInput?.value?.trim() || null,
      active_years: professionalActiveYearsInput?.value?.trim() || null,
    });

    const buildAboutPayload = () => ({
      display_name: aboutDisplayNameInput?.value?.trim() || null,
      about_text: aboutTextInput?.value?.trim() || null,
    });

    const buildDreamPayload = () => ({
      dream_title: dreamTitleInput?.value?.trim() || null,
      dream_text: dreamTextInput?.value?.trim() || null,
    });

    const buildProAchievementsPayload = () => ({
      section_title: proAchievementsTitleInput?.value?.trim() || null,
      section_text: proAchievementsTextInput?.value?.trim() || null,
    });

    const buildLifeAchievementsPayload = () => ({
      section_title: lifeAchievementsTitleInput?.value?.trim() || null,
      section_text: lifeAchievementsTextInput?.value?.trim() || null,
    });

    const buildQuotesPayload = () => ({
      section_title: quotesTitleInput?.value?.trim() || null,
      section_text: quotesTextInput?.value?.trim() || null,
    });

    const openPhotoMenu = () => {
      profilePhotoMenu?.classList.remove("hidden");
    };

    const closePhotoMenu = () => {
      profilePhotoMenu?.classList.add("hidden");
    };

    const openEmblemMenu = () => {
      emblemMenu?.classList.remove("hidden");
    };

    const closeEmblemMenu = () => {
      emblemMenu?.classList.add("hidden");
    };

    const assignProfilePhoto = async (mediaId) => {
      const res = await apiFetch("/media/profile-photo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ media_id: mediaId }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo asignar la foto de perfil.", "Could not assign the profile photo.", "Impossible d'assigner la photo de profil."));
      }
      if (profilePhoto && data.url) {
        profilePhoto.src = data.url;
      }
      return data;
    };

    const loadCurrentProfilePhoto = async () => {
      try {
        const res = await apiFetch("/media/profile-photo");
        const data = await res.json();
        if (!res.ok) return;
        if (profilePhoto) {
          profilePhoto.src = data.url || defaultProfilePhotoSrc;
        }
      } catch {
        if (profilePhoto) {
          profilePhoto.src = defaultProfilePhotoSrc;
        }
      }
    };

    const assignEmblem = async (mediaId) => {
      const res = await apiFetch("/media/emblem", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ media_id: mediaId }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo asignar el emblema.", "Could not assign the emblem.", "Impossible d'assigner l'emblème."));
      }
      if (emblemImage && data.url) {
        emblemImage.src = data.url;
      }
      return data;
    };

    const loadCurrentEmblem = async () => {
      try {
        const res = await apiFetch("/media/emblem");
        const data = await res.json();
        if (!res.ok) return;
        if (emblemImage) {
          emblemImage.src = data.url || defaultEmblemSrc;
        }
      } catch {
        if (emblemImage) {
          emblemImage.src = defaultEmblemSrc;
        }
      }
    };

    const uploadProfilePhotoFromFile = async (file) => {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("visibility", "public");

      const uploadRes = await apiFetch("/media/upload/direct", {
        method: "POST",
        body: formData,
      });
      const uploadData = await uploadRes.json();
      if (!uploadRes.ok) {
        throw new Error(uploadData.detail || tr("No se pudo subir la imagen.", "Could not upload the image.", "Impossible de téléverser l'image."));
      }
      return uploadData;
    };

    const uploadEmblemFromFile = async (file) => {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("visibility", "public");

      const uploadRes = await apiFetch("/media/upload/direct", {
        method: "POST",
        body: formData,
      });
      const uploadData = await uploadRes.json();
      if (!uploadRes.ok) {
        throw new Error(uploadData.detail || tr("No se pudo subir la imagen.", "Could not upload the image.", "Impossible de téléverser l'image."));
      }

      await assignEmblem(uploadData.media_id);
    };

    const handlePhotoTriggerClick = (event) => {
      event.preventDefault();
      if (profilePhotoMenu?.classList.contains("hidden")) {
        openPhotoMenu();
      } else {
        closePhotoMenu();
      }
    };

    const handleEmblemTriggerClick = (event) => {
      event.preventDefault();
      if (emblemMenu?.classList.contains("hidden")) {
        openEmblemMenu();
      } else {
        closeEmblemMenu();
      }
    };

    const handleUploadClick = () => {
      closePhotoMenu();
      bioPhotoFile?.click();
    };

    const handlePhotoFileChange = async (event) => {
      const file = event?.target?.files?.[0];
      if (!file) return;
      if (!file.type.startsWith("image/")) {
        setBioPhotoStatus(tr("Solo se permiten imágenes.", "Only images are allowed.", "Seules les images sont autorisées."), true);
        return;
      }
      setBioPhotoStatus(tr("Subiendo imagen...", "Uploading image...", "Téléversement de l'image..."));
      try {
        const uploadData = await uploadProfilePhotoFromFile(file);
        await assignProfilePhoto(uploadData.media_id);
        setBioPhotoStatus(tr("Foto de perfil actualizada.", "Profile photo updated.", "Photo de profil mise à jour."));
      } catch (error) {
        setBioPhotoStatus(error.message || tr("No se pudo subir la imagen.", "Could not upload the image.", "Impossible de téléverser l'image."), true);
      } finally {
        event.target.value = "";
      }
    };

    const handleEmblemUploadClick = () => {
      closeEmblemMenu();
      emblemFile?.click();
    };

    const handleEmblemFileChange = async (event) => {
      const file = event?.target?.files?.[0];
      if (!file) return;
      if (!file.type.startsWith("image/")) {
        setEmblemStatus(tr("Solo se permiten imágenes.", "Only images are allowed.", "Seules les images sont autorisées."), true);
        return;
      }
      setEmblemStatus(tr("Subiendo imagen...", "Uploading image...", "Téléversement de l'image..."));
      try {
        await uploadEmblemFromFile(file);
        setEmblemStatus(tr("Emblema actualizado.", "Emblem updated.", "Emblème mis à jour."));
      } catch (error) {
        setEmblemStatus(error.message || tr("No se pudo subir la imagen.", "Could not upload the image.", "Impossible de téléverser l'image."), true);
      } finally {
        event.target.value = "";
      }
    };


    const handlePageClick = (event) => {
      if (profilePhotoMenu && !profilePhotoMenu.classList.contains("hidden")) {
        const clickedInsideMenu = event.target.closest("#profilePhotoMenu");
        const clickedTrigger = event.target.closest("#profilePhotoTrigger");
        if (!clickedInsideMenu && !clickedTrigger) {
          closePhotoMenu();
        }
      }

      if (emblemMenu && !emblemMenu.classList.contains("hidden")) {
        const clickedInsideMenu = event.target.closest("#emblemMenu");
        const clickedTrigger = event.target.closest("#emblemTrigger");
        if (!clickedInsideMenu && !clickedTrigger) {
          closeEmblemMenu();
        }
      }
    };

    const handlePersonalInfoOverlayClick = (event) => {
      if (event.target === personalInfoModalOverlay) {
        closePersonalInfoModalFn();
      }
    };

    const handlePhysicalTraitsOverlayClick = (event) => {
      if (event.target === physicalTraitsModalOverlay) {
        closePhysicalTraitsModalFn();
      }
    };

    const handleEducationOverlayClick = (event) => {
      if (event.target === educationModalOverlay) {
        closeEducationModalFn();
      }
    };

    const handleCuriositiesOverlayClick = (event) => {
      if (event.target === curiositiesModalOverlay) {
        closeCuriositiesModalFn();
      }
    };

    const handleProfessionalInfoOverlayClick = (event) => {
      if (event.target === professionalInfoModalOverlay) {
        closeProfessionalInfoModalFn();
      }
    };

    const handleAboutOverlayClick = (event) => {
      if (event.target === aboutModalOverlay) {
        closeAboutModalFn();
      }
    };

    const handleDreamOverlayClick = (event) => {
      if (event.target === dreamModalOverlay) {
        closeDreamModalFn();
      }
    };

    const handleProAchievementsOverlayClick = (event) => {
      if (event.target === proAchievementsModalOverlay) {
        closeProAchievementsModalFn();
      }
    };

    const handleLifeAchievementsOverlayClick = (event) => {
      if (event.target === lifeAchievementsModalOverlay) {
        closeLifeAchievementsModalFn();
      }
    };

    const handleQuotesOverlayClick = (event) => {
      if (event.target === quotesModalOverlay) {
        closeQuotesModalFn();
      }
    };

    const handleDistinctionsOverlayClick = (event) => {
      if (event.target === distinctionsModalOverlay) {
        closeDistinctionsModalFn();
      }
    };

    const handleOpenPersonalInfoModal = async () => {
      setPersonalInfoModalStatus(tr("Cargando datos...", "Loading data...", "Chargement des données..."));
      try {
        if (!currentPersonalInfo) {
          await loadPersonalInfo();
        }
        fillPersonalInfoForm(currentPersonalInfo);
        openPersonalInfoModal();
      } catch (error) {
        setPersonalInfoModalStatus(error.message || tr("No se pudo cargar la información.", "Could not load information.", "Impossible de charger les informations."), true);
      }
    };

    const handleOpenPhysicalTraitsModal = async () => {
      setPhysicalTraitsModalStatus(tr("Cargando datos...", "Loading data...", "Chargement des données..."));
      try {
        if (!currentPhysicalTraits) {
          await loadPhysicalTraits();
        }
        fillPhysicalTraitsForm(currentPhysicalTraits);
        openPhysicalTraitsModal();
      } catch (error) {
        setPhysicalTraitsModalStatus(error.message || tr("No se pudieron cargar los datos.", "Could not load data.", "Impossible de charger les données."), true);
      }
    };

    const handleOpenEducationModal = async () => {
      setEducationModalStatus(tr("Cargando datos...", "Loading data...", "Chargement des données..."));
      try {
        if (!currentEducation) {
          await loadEducation();
        }
        fillEducationForm(currentEducation);
        openEducationModal();
      } catch (error) {
        setEducationModalStatus(error.message || tr("No se pudo cargar Educación.", "Could not load education.", "Impossible de charger l'éducation."), true);
      }
    };

    const handleOpenCuriositiesModal = async () => {
      setCuriositiesModalStatus(tr("Cargando datos...", "Loading data...", "Chargement des données..."));
      try {
        if (!currentCuriosities) {
          await loadCuriosities();
        }
        fillCuriositiesForm(currentCuriosities);
        openCuriositiesModal();
      } catch (error) {
        setCuriositiesModalStatus(error.message || tr("No se pudieron cargar las curiosidades.", "Could not load curiosities.", "Impossible de charger les curiosités."), true);
      }
    };

    const handleOpenProfessionalInfoModal = async () => {
      setProfessionalInfoModalStatus(tr("Cargando datos...", "Loading data...", "Chargement des données..."));
      try {
        if (!currentProfessionalInfo) {
          await loadProfessionalInfo();
        }
        fillProfessionalInfoForm(currentProfessionalInfo);
        openProfessionalInfoModal();
      } catch (error) {
        setProfessionalInfoModalStatus(
          error.message || tr("No se pudo cargar la información profesional.", "Could not load professional information.", "Impossible de charger les informations professionnelles."),
          true
        );
      }
    };

    const handleOpenAboutModal = async () => {
      setAboutModalStatus(tr("Cargando datos...", "Loading data...", "Chargement des données..."));
      try {
        if (!currentAbout) {
          await loadAbout();
        }
        fillAboutForm(currentAbout);
        openAboutModal();
      } catch (error) {
        setAboutModalStatus(error.message || tr("No se pudo cargar tu biografía.", "Could not load your biography.", "Impossible de charger ta biographie."), true);
      }
    };

    const handleOpenDreamModal = async () => {
      setDreamModalStatus(tr("Cargando datos...", "Loading data...", "Chargement des données..."));
      try {
        if (!currentDream) {
          await loadDream();
        }
        fillDreamForm(currentDream);
        openDreamModal();
      } catch (error) {
        setDreamModalStatus(
          error.message || tr("No se pudo cargar tu mayor sueño.", "Could not load your greatest dream.", "Impossible de charger ton plus grand rêve."),
          true
        );
      }
    };

    const handleOpenProAchievementsModal = async () => {
      setProAchievementsModalStatus(tr("Cargando datos...", "Loading data...", "Chargement des données..."));
      try {
        if (!currentProAchievements) {
          await loadProAchievements();
        }
        fillProAchievementsForm(currentProAchievements);
        openProAchievementsModal();
      } catch (error) {
        setProAchievementsModalStatus(
          error.message || tr("No se pudieron cargar tus logros profesionales.", "Could not load your professional achievements.", "Impossible de charger tes réalisations professionnelles."),
          true
        );
      }
    };

    const handleOpenLifeAchievementsModal = async () => {
      setLifeAchievementsModalStatus(tr("Cargando datos...", "Loading data...", "Chargement des données..."));
      try {
        if (!currentLifeAchievements) {
          await loadLifeAchievements();
        }
        fillLifeAchievementsForm(currentLifeAchievements);
        openLifeAchievementsModal();
      } catch (error) {
        setLifeAchievementsModalStatus(
          error.message || tr("No se pudieron cargar tus logros alcanzados.", "Could not load your life achievements.", "Impossible de charger tes réalisations de vie."),
          true
        );
      }
    };

    const handleOpenQuotesModal = async () => {
      setQuotesModalStatus(tr("Cargando datos...", "Loading data...", "Chargement des données..."));
      try {
        if (!currentFavoriteQuotes) {
          await loadFavoriteQuotes();
        }
        fillQuotesForm(currentFavoriteQuotes);
        openQuotesModal();
      } catch (error) {
        setQuotesModalStatus(
          error.message || tr("No se pudieron cargar tus frases favoritas.", "Could not load your favorite quotes.", "Impossible de charger tes citations favorites."),
          true
        );
      }
    };

    const handleOpenDistinctionsModal = async () => {
      if (!isViewerGuardian()) {
        setDistinctionsModalStatus(
          tr(
            "Esta sección solo puede ser actualizada por los Guardianes de Kiadez.com.",
            "This section can only be updated by Kiadez.com Guardians."
          ),
          true
        );
        return;
      }

      setDistinctionsModalStatus(tr("Cargando distinciones...", "Loading distinctions...", "Chargement des distinctions..."));
      try {
        if (!currentDistinctions) {
          await loadDistinctions();
        }
        fillDistinctionsForm(currentDistinctions);
        openDistinctionsModal();
      } catch (error) {
        setDistinctionsModalStatus(error.message || tr("No se pudieron cargar las distinciones.", "Could not load distinctions.", "Impossible de charger les distinctions."), true);
      }
    };

    const handleSavePersonalInfo = async () => {
      setPersonalInfoModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildPersonalInfoPayload();
        const res = await apiFetch("/biography/personal-info", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(
            data.detail || tr("No se pudo guardar la información personal.", "Could not save personal information.", "Impossible d'enregistrer les informations personnelles.")
          );
        }
        currentPersonalInfo = data;
        applyPersonalInfoToView(data);
        closePersonalInfoModalFn();
      } catch (error) {
        setPersonalInfoModalStatus(error.message || tr("No se pudo guardar la información.", "Could not save information.", "Impossible d'enregistrer les informations."), true);
      }
    };

    const handleSavePhysicalTraits = async () => {
      setPhysicalTraitsModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildPhysicalTraitsPayload();
        const res = await apiFetch("/biography/physical-traits", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(
            data.detail || tr("No se pudieron guardar las características físicas.", "Could not save physical traits.", "Impossible d'enregistrer les caractéristiques physiques.")
          );
        }
        currentPhysicalTraits = data;
        applyPhysicalTraitsToView(data);
        closePhysicalTraitsModalFn();
      } catch (error) {
        setPhysicalTraitsModalStatus(error.message || tr("No se pudieron guardar los datos.", "Could not save data.", "Impossible d'enregistrer les données."), true);
      }
    };

    const handleSaveEducation = async () => {
      setEducationModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildEducationPayload();
        const res = await apiFetch("/biography/education", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || tr("No se pudo guardar Educación.", "Could not save education.", "Impossible d'enregistrer l'éducation."));
        }
        currentEducation = data;
        applyEducationToView(data);
        closeEducationModalFn();
      } catch (error) {
        setEducationModalStatus(error.message || tr("No se pudo guardar Educación.", "Could not save education.", "Impossible d'enregistrer l'éducation."), true);
      }
    };

    const handleSaveCuriosities = async () => {
      setCuriositiesModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildCuriositiesPayload();
        const res = await apiFetch("/biography/curiosities", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || tr("No se pudo guardar Curiosidades.", "Could not save curiosities.", "Impossible d'enregistrer les curiosités."));
        }
        currentCuriosities = data;
        applyCuriositiesToView(data);
        closeCuriositiesModalFn();
      } catch (error) {
        setCuriositiesModalStatus(error.message || tr("No se pudo guardar Curiosidades.", "Could not save curiosities.", "Impossible d'enregistrer les curiosités."), true);
      }
    };

    const handleSaveProfessionalInfo = async () => {
      setProfessionalInfoModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildProfessionalInfoPayload();
        const res = await apiFetch("/biography/professional-info", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(
            data.detail || tr("No se pudo guardar la información profesional.", "Could not save professional information.", "Impossible d'enregistrer les informations professionnelles.")
          );
        }
        currentProfessionalInfo = data;
        applyProfessionalInfoToView(data);
        closeProfessionalInfoModalFn();
      } catch (error) {
        setProfessionalInfoModalStatus(
          error.message || tr("No se pudo guardar la información profesional.", "Could not save professional information.", "Impossible d'enregistrer les informations professionnelles."),
          true
        );
      }
    };

    const handleAboutInputChange = () => {
      updateAboutWordCounter();
      if (aboutModalStatus?.classList.contains("is-error")) {
        setAboutModalStatus("");
      }
    };

    const handleDreamInputChange = () => {
      updateDreamWordCounter();
      if (dreamModalStatus?.classList.contains("is-error")) {
        setDreamModalStatus("");
      }
    };

    const handleProAchievementsInputChange = () => {
      updateProAchievementsWordCounter();
      if (proAchievementsModalStatus?.classList.contains("is-error")) {
        setProAchievementsModalStatus("");
      }
    };

    const handleLifeAchievementsInputChange = () => {
      updateLifeAchievementsWordCounter();
      if (lifeAchievementsModalStatus?.classList.contains("is-error")) {
        setLifeAchievementsModalStatus("");
      }
    };

    const handleQuotesInputChange = () => {
      updateQuotesWordCounter();
      if (quotesModalStatus?.classList.contains("is-error")) {
        setQuotesModalStatus("");
      }
    };

    const handleSaveAbout = async () => {
      updateAboutWordCounter();
      const totalWords = countWords(aboutTextInput?.value || "");
      if (totalWords > ABOUT_MAX_WORDS) {
        setAboutModalStatus(
          tr(
            `La biografía permite máximo ${ABOUT_MAX_WORDS} palabras.`,
            `Biography allows a maximum of ${ABOUT_MAX_WORDS} words.`
          ),
          true
        );
        return;
      }

      setAboutModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildAboutPayload();
        const res = await apiFetch("/biography/about", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || tr("No se pudo guardar tu biografía.", "Could not save your biography.", "Impossible d'enregistrer ta biographie."));
        }
        currentAbout = data;
        applyAboutToView(data);
        closeAboutModalFn();
      } catch (error) {
        setAboutModalStatus(error.message || tr("No se pudo guardar tu biografía.", "Could not save your biography.", "Impossible d'enregistrer ta biographie."), true);
      }
    };

    const handleSaveDream = async () => {
      updateDreamWordCounter();
      const totalWords = countWords(dreamTextInput?.value || "");
      if (totalWords > DREAM_MAX_WORDS) {
        setDreamModalStatus(
          tr(
            `El mayor sueño permite máximo ${DREAM_MAX_WORDS} palabras.`,
            `Greatest dream allows a maximum of ${DREAM_MAX_WORDS} words.`
          ),
          true
        );
        return;
      }

      setDreamModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildDreamPayload();
        const res = await apiFetch("/biography/dream", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(
            data.detail || tr("No se pudo guardar tu mayor sueño.", "Could not save your greatest dream.", "Impossible d'enregistrer ton plus grand rêve.")
          );
        }
        currentDream = data;
        applyDreamToView(data);
        closeDreamModalFn();
      } catch (error) {
        setDreamModalStatus(
          error.message || tr("No se pudo guardar tu mayor sueño.", "Could not save your greatest dream.", "Impossible d'enregistrer ton plus grand rêve."),
          true
        );
      }
    };

    const handleSaveProAchievements = async () => {
      updateProAchievementsWordCounter();
      const totalWords = countWords(proAchievementsTextInput?.value || "");
      if (totalWords > PRO_ACHIEVEMENTS_MAX_WORDS) {
        setProAchievementsModalStatus(
          tr(
            `Los logros profesionales permiten máximo ${PRO_ACHIEVEMENTS_MAX_WORDS} palabras.`,
            `Professional achievements allow a maximum of ${PRO_ACHIEVEMENTS_MAX_WORDS} words.`
          ),
          true
        );
        return;
      }

      setProAchievementsModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildProAchievementsPayload();
        const res = await apiFetch("/biography/professional-achievements", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(
            data.detail || tr("No se pudieron guardar tus logros profesionales.", "Could not save your professional achievements.", "Impossible d'enregistrer tes réalisations professionnelles.")
          );
        }
        currentProAchievements = data;
        applyProAchievementsToView(data);
        closeProAchievementsModalFn();
      } catch (error) {
        setProAchievementsModalStatus(
          error.message || tr("No se pudieron guardar tus logros profesionales.", "Could not save your professional achievements.", "Impossible d'enregistrer tes réalisations professionnelles."),
          true
        );
      }
    };

    const handleSaveLifeAchievements = async () => {
      updateLifeAchievementsWordCounter();
      const totalWords = countWords(lifeAchievementsTextInput?.value || "");
      if (totalWords > LIFE_ACHIEVEMENTS_MAX_WORDS) {
        setLifeAchievementsModalStatus(
          tr(
            `Los logros alcanzados permiten máximo ${LIFE_ACHIEVEMENTS_MAX_WORDS} palabras.`,
            `Life achievements allow a maximum of ${LIFE_ACHIEVEMENTS_MAX_WORDS} words.`
          ),
          true
        );
        return;
      }

      setLifeAchievementsModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildLifeAchievementsPayload();
        const res = await apiFetch("/biography/life-achievements", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(
            data.detail || tr("No se pudieron guardar tus logros alcanzados.", "Could not save your life achievements.", "Impossible d'enregistrer tes réalisations de vie.")
          );
        }
        currentLifeAchievements = data;
        applyLifeAchievementsToView(data);
        closeLifeAchievementsModalFn();
      } catch (error) {
        setLifeAchievementsModalStatus(
          error.message || tr("No se pudieron guardar tus logros alcanzados.", "Could not save your life achievements.", "Impossible d'enregistrer tes réalisations de vie."),
          true
        );
      }
    };

    const handleSaveQuotes = async () => {
      updateQuotesWordCounter();
      const totalWords = countWords(quotesTextInput?.value || "");
      if (totalWords > FAVORITE_QUOTES_MAX_WORDS) {
        setQuotesModalStatus(
          tr(
            `Las frases favoritas permiten máximo ${FAVORITE_QUOTES_MAX_WORDS} palabras.`,
            `Favorite quotes allow a maximum of ${FAVORITE_QUOTES_MAX_WORDS} words.`
          ),
          true
        );
        return;
      }

      setQuotesModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildQuotesPayload();
        const res = await apiFetch("/biography/favorite-quotes", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || tr("No se pudieron guardar tus frases favoritas.", "Could not save your favorite quotes.", "Impossible d'enregistrer tes citations favorites."));
        }
        currentFavoriteQuotes = data;
        applyQuotesToView(data);
        closeQuotesModalFn();
      } catch (error) {
        setQuotesModalStatus(
          error.message || tr("No se pudieron guardar tus frases favoritas.", "Could not save your favorite quotes.", "Impossible d'enregistrer tes citations favorites."),
          true
        );
      }
    };

    const handleSaveDistinctions = async () => {
      if (!isViewerGuardian()) {
        setDistinctionsModalStatus(
          tr(
            "Esta sección solo puede ser actualizada por los Guardianes de Kiadez.com.",
            "This section can only be updated by Kiadez.com Guardians."
          ),
          true
        );
        return;
      }

      setDistinctionsModalStatus(tr("Guardando...", "Saving...", "Enregistrement..."));
      try {
        const payload = buildDistinctionsPayload();
        const endpoint = buildDistinctionsEndpoint({ includeTarget: true });
        const res = await apiFetch(endpoint, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || tr("No se pudieron guardar las distinciones.", "Could not save distinctions.", "Impossible d'enregistrer les distinctions."));
        }
        currentDistinctions = data;
        applyDistinctionsToView(data);
        closeDistinctionsModalFn();
      } catch (error) {
        setDistinctionsModalStatus(error.message || tr("No se pudieron guardar las distinciones.", "Could not save distinctions.", "Impossible d'enregistrer les distinctions."), true);
      }
    };

    personalInfoEditBtn?.addEventListener("click", handleOpenPersonalInfoModal);
    closePersonalInfoModal?.addEventListener("click", closePersonalInfoModalFn);
    cancelPersonalInfoModal?.addEventListener("click", closePersonalInfoModalFn);
    savePersonalInfoBtn?.addEventListener("click", handleSavePersonalInfo);
    personalInfoModalOverlay?.addEventListener("click", handlePersonalInfoOverlayClick);
    physicalTraitsEditBtn?.addEventListener("click", handleOpenPhysicalTraitsModal);
    closePhysicalTraitsModal?.addEventListener("click", closePhysicalTraitsModalFn);
    cancelPhysicalTraitsModal?.addEventListener("click", closePhysicalTraitsModalFn);
    savePhysicalTraitsBtn?.addEventListener("click", handleSavePhysicalTraits);
    physicalTraitsModalOverlay?.addEventListener("click", handlePhysicalTraitsOverlayClick);
    educationEditBtn?.addEventListener("click", handleOpenEducationModal);
    closeEducationModal?.addEventListener("click", closeEducationModalFn);
    cancelEducationModal?.addEventListener("click", closeEducationModalFn);
    saveEducationBtn?.addEventListener("click", handleSaveEducation);
    educationModalOverlay?.addEventListener("click", handleEducationOverlayClick);
    curiositiesEditBtn?.addEventListener("click", handleOpenCuriositiesModal);
    closeCuriositiesModal?.addEventListener("click", closeCuriositiesModalFn);
    cancelCuriositiesModal?.addEventListener("click", closeCuriositiesModalFn);
    saveCuriositiesBtn?.addEventListener("click", handleSaveCuriosities);
    curiositiesModalOverlay?.addEventListener("click", handleCuriositiesOverlayClick);
    professionalInfoEditBtn?.addEventListener("click", handleOpenProfessionalInfoModal);
    closeProfessionalInfoModal?.addEventListener("click", closeProfessionalInfoModalFn);
    cancelProfessionalInfoModal?.addEventListener("click", closeProfessionalInfoModalFn);
    saveProfessionalInfoBtn?.addEventListener("click", handleSaveProfessionalInfo);
    professionalInfoModalOverlay?.addEventListener("click", handleProfessionalInfoOverlayClick);
    aboutEditBtn?.addEventListener("click", handleOpenAboutModal);
    closeAboutModal?.addEventListener("click", closeAboutModalFn);
    cancelAboutModal?.addEventListener("click", closeAboutModalFn);
    saveAboutBtn?.addEventListener("click", handleSaveAbout);
    aboutModalOverlay?.addEventListener("click", handleAboutOverlayClick);
    aboutTextInput?.addEventListener("input", handleAboutInputChange);
    dreamEditBtn?.addEventListener("click", handleOpenDreamModal);
    closeDreamModal?.addEventListener("click", closeDreamModalFn);
    cancelDreamModal?.addEventListener("click", closeDreamModalFn);
    saveDreamBtn?.addEventListener("click", handleSaveDream);
    dreamModalOverlay?.addEventListener("click", handleDreamOverlayClick);
    dreamTextInput?.addEventListener("input", handleDreamInputChange);
    proAchievementsEditBtn?.addEventListener("click", handleOpenProAchievementsModal);
    closeProAchievementsModal?.addEventListener("click", closeProAchievementsModalFn);
    cancelProAchievementsModal?.addEventListener("click", closeProAchievementsModalFn);
    saveProAchievementsBtn?.addEventListener("click", handleSaveProAchievements);
    proAchievementsModalOverlay?.addEventListener("click", handleProAchievementsOverlayClick);
    proAchievementsTextInput?.addEventListener("input", handleProAchievementsInputChange);
    lifeAchievementsEditBtn?.addEventListener("click", handleOpenLifeAchievementsModal);
    closeLifeAchievementsModal?.addEventListener("click", closeLifeAchievementsModalFn);
    cancelLifeAchievementsModal?.addEventListener("click", closeLifeAchievementsModalFn);
    saveLifeAchievementsBtn?.addEventListener("click", handleSaveLifeAchievements);
    lifeAchievementsModalOverlay?.addEventListener("click", handleLifeAchievementsOverlayClick);
    lifeAchievementsTextInput?.addEventListener("input", handleLifeAchievementsInputChange);
    quotesEditBtn?.addEventListener("click", handleOpenQuotesModal);
    closeQuotesModal?.addEventListener("click", closeQuotesModalFn);
    cancelQuotesModal?.addEventListener("click", closeQuotesModalFn);
    saveQuotesBtn?.addEventListener("click", handleSaveQuotes);
    quotesModalOverlay?.addEventListener("click", handleQuotesOverlayClick);
    quotesTextInput?.addEventListener("input", handleQuotesInputChange);
    distinctionsEditBtn?.addEventListener("click", handleOpenDistinctionsModal);
    closeDistinctionsModal?.addEventListener("click", closeDistinctionsModalFn);
    cancelDistinctionsModal?.addEventListener("click", closeDistinctionsModalFn);
    saveDistinctionsBtn?.addEventListener("click", handleSaveDistinctions);
    distinctionsModalOverlay?.addEventListener("click", handleDistinctionsOverlayClick);
    profilePhotoTrigger?.addEventListener("click", handlePhotoTriggerClick);
    bioPhotoUpload?.addEventListener("click", handleUploadClick);
    bioPhotoFile?.addEventListener("change", handlePhotoFileChange);
    emblemTrigger?.addEventListener("click", handleEmblemTriggerClick);
    emblemUpload?.addEventListener("click", handleEmblemUploadClick);
    emblemFile?.addEventListener("change", handleEmblemFileChange);
    document.addEventListener("click", handlePageClick);
    ensureDistinctionsForm();
    applyDistinctionsEditorVisibility();

    void loadCurrentProfilePhoto();
    void loadCurrentEmblem();
    void loadPersonalInfo().catch((error) => {
      setPersonalInfoModalStatus(
        error.message || tr("No se pudo cargar la información personal.", "Could not load personal information.", "Impossible de charger les informations personnelles."),
        true
      );
    });
    void loadPhysicalTraits().catch(() => {});
    void loadEducation().catch(() => {});
    void loadCuriosities().catch(() => {});
    void loadProfessionalInfo().catch(() => {});
    void loadAbout().catch(() => {});
    void loadDream().catch(() => {});
    void loadProAchievements().catch(() => {});
    void loadLifeAchievements().catch(() => {});
    void loadFavoriteQuotes().catch(() => {});
    void (async () => {
      try {
        await resolveBiographyProfileContext();
      } catch (error) {
        setDistinctionsModalStatus(
          error?.message || tr("No se pudo cargar el contexto del perfil.", "Could not load the profile context.", "Impossible de charger le contexte du profil."),
          true
        );
      }
      void loadActivityStats({ userId: activeProfileUserId }).catch(() => {});
      void loadDistinctions().catch((error) => {
        applyDistinctionsToView({ slots: [] });
        setDistinctionsModalStatus(
          error?.message || tr("No se pudieron cargar las distinciones.", "Could not load distinctions.", "Impossible de charger les distinctions."),
          true
        );
      });
    })();

    return () => {
      personalInfoEditBtn?.removeEventListener("click", handleOpenPersonalInfoModal);
      closePersonalInfoModal?.removeEventListener("click", closePersonalInfoModalFn);
      cancelPersonalInfoModal?.removeEventListener("click", closePersonalInfoModalFn);
      savePersonalInfoBtn?.removeEventListener("click", handleSavePersonalInfo);
      personalInfoModalOverlay?.removeEventListener("click", handlePersonalInfoOverlayClick);
      physicalTraitsEditBtn?.removeEventListener("click", handleOpenPhysicalTraitsModal);
      closePhysicalTraitsModal?.removeEventListener("click", closePhysicalTraitsModalFn);
      cancelPhysicalTraitsModal?.removeEventListener("click", closePhysicalTraitsModalFn);
      savePhysicalTraitsBtn?.removeEventListener("click", handleSavePhysicalTraits);
      physicalTraitsModalOverlay?.removeEventListener("click", handlePhysicalTraitsOverlayClick);
      educationEditBtn?.removeEventListener("click", handleOpenEducationModal);
      closeEducationModal?.removeEventListener("click", closeEducationModalFn);
      cancelEducationModal?.removeEventListener("click", closeEducationModalFn);
      saveEducationBtn?.removeEventListener("click", handleSaveEducation);
      educationModalOverlay?.removeEventListener("click", handleEducationOverlayClick);
      curiositiesEditBtn?.removeEventListener("click", handleOpenCuriositiesModal);
      closeCuriositiesModal?.removeEventListener("click", closeCuriositiesModalFn);
      cancelCuriositiesModal?.removeEventListener("click", closeCuriositiesModalFn);
      saveCuriositiesBtn?.removeEventListener("click", handleSaveCuriosities);
      curiositiesModalOverlay?.removeEventListener("click", handleCuriositiesOverlayClick);
      professionalInfoEditBtn?.removeEventListener("click", handleOpenProfessionalInfoModal);
      closeProfessionalInfoModal?.removeEventListener("click", closeProfessionalInfoModalFn);
      cancelProfessionalInfoModal?.removeEventListener("click", closeProfessionalInfoModalFn);
      saveProfessionalInfoBtn?.removeEventListener("click", handleSaveProfessionalInfo);
      professionalInfoModalOverlay?.removeEventListener("click", handleProfessionalInfoOverlayClick);
      aboutEditBtn?.removeEventListener("click", handleOpenAboutModal);
      closeAboutModal?.removeEventListener("click", closeAboutModalFn);
      cancelAboutModal?.removeEventListener("click", closeAboutModalFn);
      saveAboutBtn?.removeEventListener("click", handleSaveAbout);
      aboutModalOverlay?.removeEventListener("click", handleAboutOverlayClick);
      aboutTextInput?.removeEventListener("input", handleAboutInputChange);
      dreamEditBtn?.removeEventListener("click", handleOpenDreamModal);
      closeDreamModal?.removeEventListener("click", closeDreamModalFn);
      cancelDreamModal?.removeEventListener("click", closeDreamModalFn);
      saveDreamBtn?.removeEventListener("click", handleSaveDream);
      dreamModalOverlay?.removeEventListener("click", handleDreamOverlayClick);
      dreamTextInput?.removeEventListener("input", handleDreamInputChange);
      proAchievementsEditBtn?.removeEventListener("click", handleOpenProAchievementsModal);
      closeProAchievementsModal?.removeEventListener("click", closeProAchievementsModalFn);
      cancelProAchievementsModal?.removeEventListener("click", closeProAchievementsModalFn);
      saveProAchievementsBtn?.removeEventListener("click", handleSaveProAchievements);
      proAchievementsModalOverlay?.removeEventListener("click", handleProAchievementsOverlayClick);
      proAchievementsTextInput?.removeEventListener("input", handleProAchievementsInputChange);
      lifeAchievementsEditBtn?.removeEventListener("click", handleOpenLifeAchievementsModal);
      closeLifeAchievementsModal?.removeEventListener("click", closeLifeAchievementsModalFn);
      cancelLifeAchievementsModal?.removeEventListener("click", closeLifeAchievementsModalFn);
      saveLifeAchievementsBtn?.removeEventListener("click", handleSaveLifeAchievements);
      lifeAchievementsModalOverlay?.removeEventListener("click", handleLifeAchievementsOverlayClick);
      lifeAchievementsTextInput?.removeEventListener("input", handleLifeAchievementsInputChange);
      quotesEditBtn?.removeEventListener("click", handleOpenQuotesModal);
      closeQuotesModal?.removeEventListener("click", closeQuotesModalFn);
      cancelQuotesModal?.removeEventListener("click", closeQuotesModalFn);
      saveQuotesBtn?.removeEventListener("click", handleSaveQuotes);
      quotesModalOverlay?.removeEventListener("click", handleQuotesOverlayClick);
      quotesTextInput?.removeEventListener("input", handleQuotesInputChange);
      distinctionsEditBtn?.removeEventListener("click", handleOpenDistinctionsModal);
      closeDistinctionsModal?.removeEventListener("click", closeDistinctionsModalFn);
      cancelDistinctionsModal?.removeEventListener("click", closeDistinctionsModalFn);
      saveDistinctionsBtn?.removeEventListener("click", handleSaveDistinctions);
      distinctionsModalOverlay?.removeEventListener("click", handleDistinctionsOverlayClick);
      profilePhotoTrigger?.removeEventListener("click", handlePhotoTriggerClick);
      bioPhotoUpload?.removeEventListener("click", handleUploadClick);
      bioPhotoFile?.removeEventListener("change", handlePhotoFileChange);
      emblemTrigger?.removeEventListener("click", handleEmblemTriggerClick);
      emblemUpload?.removeEventListener("click", handleEmblemUploadClick);
      emblemFile?.removeEventListener("change", handleEmblemFileChange);
      document.removeEventListener("click", handlePageClick);
    };
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{tr("Kiadez — Mi biografía", "Kiadez — My biography", "Kiadez — Ma biographie")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-bio biography-background">
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
        <a class="topbar-btn" href="/home_user.html">🏠 {tr("Home", "Home", "Accueil")}</a>
        <a class="topbar-btn" href="/gallery.html">🖼️ {tr("Galería", "Gallery", "Galerie")}</a>
        <a class="topbar-btn" href="/my-public-whishes.html">🌐 {tr("Deseos públicos", "Public wishes", "Souhaits publics")}</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 {tr("Deseos privados", "Private wishes", "Souhaits privés")}</a>
        <a class="topbar-btn" href="/my-fulfilled-whises.html">✅ {tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</a>
      </div>

      <div class="feed-topbar-zone feed-topbar-right">
        <details class="topbar-dropdown" id="biographyProfileDropdown">
          <summary class="topbar-avatar-btn" aria-label={tr("Perfil del usuario", "User profile", "Profil utilisateur")}>
            <img src="/assets/avatar-default.jpg" alt={tr("Perfil de Carlos Jiménez Duarte", "Carlos Jiménez Duarte profile", "Profil de Carlos Jiménez Duarte")} />
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

        <details class="topbar-dropdown" id="biographyMenuDropdown">
          <summary class="topbar-menu-btn" aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}>
            <span class="topbar-menu-icon" aria-hidden="true">☰</span>
            <span class="topbar-menu-label">{tr("Menú", "Menu", "Navigation")}</span>
          </summary>
          <div class="dropdown-menu" role="menu">
            <a href="/home_user.html" role="menuitem">{tr("Mi Home", "My Home", "Mon Home")}</a>
            <a href="/achievements.html" role="menuitem">{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
            <a href="/gallery.html" role="menuitem">{tr("Galería", "Gallery", "Galerie")}</a>
            <a href="/calendar.html" role="menuitem">{tr("Calendario", "Calendar", "Calendrier")}</a>
            <a href="/my-biography.html" role="menuitem">{tr("Mi Biografía", "My Biography", "Ma biographie")}</a>
          <a href="/messages.html" role="menuitem">{tr("Mensajes", "Messages", "Messagerie")}</a>
          </div>
        </details>
      </div>
    </header>

    <main class="user-home user-home--bio">

      <!-- PORTADA (MISMA DE HOME) -->
      <section class="cover" id="cover">
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

      <div class="biography-body">
      <!-- NAV (YA LO TIENES IGUAL) -->
      <nav class="profile-nav" aria-label={tr("Navegación de perfil", "Profile navigation", "Navigation du profil")}>
        <a class="nav-pill" href="/home_user.html" title={tr("Home", "Home", "Accueil")}>{tr("Home", "Home", "Accueil")}</a>
        <a class="nav-pill" href="/star-pool-found.html" title={tr("Estrellas", "Stars", "Étoiles")}>
          <span class="nav-icon">⭐</span>
          <span><strong id="biographyStarsTotal">0</strong> {tr("estrellas", "stars", "étoiles")}</span>
        </a>

        <a class="nav-pill" href="/followers.html" title={tr("Seguidores", "Followers", "Abonnés")}>{tr("Seguidores", "Followers", "Abonnés")}</a>
        <a class="nav-pill" href="/achievements.html" title={tr("Logros recientes", "Recent achievements", "Réalisations récentes")}>{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
        <a class="nav-pill" href="/gallery.html" title={tr("Galería", "Gallery", "Galerie")}>{tr("Galería", "Gallery", "Galerie")}</a>
        <a class="nav-pill" href="/calendar.html" title={tr("Calendario", "Calendar", "Calendrier")}>{tr("Calendario", "Calendar", "Calendrier")}</a>
        <a class="nav-pill" href="/my-biography.html" title={tr("Mi biografía", "My biography", "Ma biographie")}>{tr("Mi biografía", "My biography", "Ma biographie")}</a>
        <a class="nav-pill" href="/messages.html" title={tr("Mensajes", "Messages", "Messagerie")}>{tr("Mensajes", "Messages", "Messagerie")}</a>
      </nav>
      <!-- ======= CUERPO (3 columnas) ======= -->
      <section class="bio-shell">

        <section class="bio-grid">

          <!-- ========== IZQUIERDA: TOC ========== -->
          <aside class="bio-card bio-toc" aria-label={tr("Tabla de contenidos", "Table of contents", "Table des matières")}>
            <h2 class="bio-side-title" id="tocUserName">Carlos Jiménez Duarte</h2>

            <ol class="bio-toc-list" id="tocList">
              <li><a href="#sec-about" data-toc="about">Carlos Jiménez Duarte</a></li>
              <li><a href="#sec-dream" data-toc="dream">{tr("Sobre su mayor sueño", "About their greatest dream", "À propos de son plus grand rêve")}</a></li>
              <li><a href="#sec-pro" data-toc="pro">{tr("Logros profesionales", "Professional achievements", "Réalisations professionnelles")}</a></li>
              <li><a href="#sec-life" data-toc="life">{tr("Logros alcanzados", "Life achievements", "Réalisations de vie")}</a></li>
              <li><a href="#sec-quotes" data-toc="quotes">{tr("Frases favoritas", "Favorite quotes", "Citations favorites")}</a></li>
            </ol>

            <p class="bio-side-note">
              {tr("Esta tabla se sincroniza con tus títulos del centro.", "This table syncs with your center titles.", "Cette table se synchronise avec tes titres au centre.")}
            </p>
          </aside>

          <!-- ========== CENTRO: CONTENIDO ========== -->
          <section class="bio-center" aria-label={tr("Biografía editable", "Editable biography", "Biographie modifiable")}>

            <!-- Sección 1 -->
            <article class="bio-card bio-section bio-about-section" id="sec-about" data-section="about">
              <header class="bio-section-header">
                <h2 class="bio-section-title" id="aboutDisplayNameValue">Carlos Jiménez Duarte</h2>
                <button class="infobox-edit-btn bio-about-edit-btn" id="aboutEditBtn" type="button" title={tr("Modificar biografía", "Edit biography", "Modifier la biographie")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Modificar biografía", "Edit biography", "Modifier la biographie")} />
                </button>
              </header>

              <div class="bio-about-view">
                <div id="aboutEmptyState">
                  <p class="bio-about-empty-message">
                    {tr(
                      "Todavía no has redactado tu biografía. ¿Qué esperas para hacerlo ahora?",
                      "You have not written your biography yet. What are you waiting for?"
                    )}
                  </p>
                </div>
                <p class="bio-about-text hidden" id="aboutTextValue"></p>
              </div>
            </article>

            <!-- Sección 2 -->
            <article class="bio-card bio-section bio-dream-section" id="sec-dream" data-section="dream">
              <header class="bio-section-header">
                <h2 class="bio-section-title" id="dreamTitleValue">{tr("Sobre su mayor sueño", "About their greatest dream", "À propos de son plus grand rêve")}</h2>
                <button class="infobox-edit-btn bio-about-edit-btn" id="dreamEditBtn" type="button" title={tr("Modificar mayor sueño", "Edit greatest dream", "Modifier le plus grand rêve")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Modificar mayor sueño", "Edit greatest dream", "Modifier le plus grand rêve")} />
                </button>
              </header>

              <div class="bio-about-view">
                <div id="dreamEmptyState">
                  <p class="bio-about-empty-message">
                    {tr(
                      "Todavía no has descrito tu mayor sueño. ¿Te gustaría compartir con el mundo que es lo que palpita en tu corazón?",
                      "You have not described your greatest dream yet. Would you like to share what beats in your heart with the world?"
                    )}
                  </p>
                </div>
                <p class="bio-about-text hidden" id="dreamTextValue"></p>
              </div>
            </article>

            <!-- Sección 3 -->
            <article class="bio-card bio-section bio-pro-achievements-section" id="sec-pro" data-section="pro">
              <header class="bio-section-header">
                <h2 class="bio-section-title" id="proAchievementsTitleValue">{tr("Logros profesionales", "Professional achievements", "Réalisations professionnelles")}</h2>
                <button class="infobox-edit-btn bio-about-edit-btn" id="proAchievementsEditBtn" type="button" title={tr("Modificar logros profesionales", "Edit professional achievements", "Modifier les réalisations professionnelles")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Modificar logros profesionales", "Edit professional achievements", "Modifier les réalisations professionnelles")} />
                </button>
              </header>

              <div class="bio-about-view">
                <div id="proAchievementsEmptyState">
                  <p class="bio-about-empty-message">
                    {tr(
                      "¿Cuáles son aquellos logros de los que más te han hecho sentir realizado en este mundo? Incluso lo más humilde es significativo.",
                      "Which achievements have made you feel most fulfilled in this world? Even the humblest ones are meaningful."
                    )}
                  </p>
                </div>
                <p class="bio-about-text hidden" id="proAchievementsTextValue"></p>
              </div>
            </article>

            <!-- Sección 4 -->
            <article class="bio-card bio-section bio-life-achievements-section" id="sec-life" data-section="life">
              <header class="bio-section-header">
                <h2 class="bio-section-title" id="lifeAchievementsTitleValue">{tr("Logros alcanzados", "Life achievements", "Réalisations de vie")}</h2>
                <button class="infobox-edit-btn bio-about-edit-btn" id="lifeAchievementsEditBtn" type="button" title={tr("Modificar logros alcanzados", "Edit life achievements", "Modifier les réalisations de vie")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Modificar logros alcanzados", "Edit life achievements", "Modifier les réalisations de vie")} />
                </button>
              </header>

              <div class="bio-about-view">
                <div id="lifeAchievementsEmptyState">
                  <p class="bio-about-empty-message">
                    {tr(
                      "¿Qué es aquello tan significativo para ti cómo para ser considerado como parte de tu legado? ¿Cuáles son los meritos por los que te gustaría ser recordado? Deja tu constancia aquí.",
                      "What is so significant to you that it should be considered part of your legacy? Which merits would you like to be remembered for? Leave your record here."
                    )}
                  </p>
                </div>
                <p class="bio-about-text hidden" id="lifeAchievementsTextValue"></p>
              </div>
            </article>

            <!-- Sección 5 -->
            <article class="bio-card bio-section bio-quotes-section" id="sec-quotes" data-section="quotes">
              <header class="bio-section-header">
                <h2 class="bio-section-title" id="quotesTitleValue">{tr("Frases favoritas", "Favorite quotes", "Citations favorites")}</h2>
                <button class="infobox-edit-btn bio-about-edit-btn" id="quotesEditBtn" type="button" title={tr("Modificar frases favoritas", "Edit favorite quotes", "Modifier les citations favorites")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Modificar frases favoritas", "Edit favorite quotes", "Modifier les citations favorites")} />
                </button>
              </header>

              <div class="bio-about-view">
                <div id="quotesEmptyState">
                  <p class="bio-about-empty-message">
                    {tr(
                      "¡Esta es una oportunidad fantástica para dar constancia de tu filosofía de vida en las frases que más te gustan!",
                      "This is a fantastic opportunity to record your life philosophy in the quotes you love most."
                    )}
                  </p>
                </div>
                <p class="bio-about-text hidden" id="quotesTextValue"></p>
              </div>
            </article>

          </section>

          <!-- ========== DERECHA: INFOBOX ========== -->
          <aside class="bio-card bio-infobox" aria-label={tr("Ficha del usuario", "User profile card", "Fiche utilisateur")}>

            <div class="infobox-head">
              <h2 class="infobox-title" id="infoName">Carlos Jiménez Duarte</h2>
            </div>

            <figure class="infobox-photo">
              <div class="infobox-photo-wrap">
                <button class="infobox-photo-trigger" id="profilePhotoTrigger" type="button"
                  title={tr("Gestionar foto de perfil", "Manage profile photo", "Gérer la photo de profil")}>
                  <img id="profilePhoto" src="/css/logo-kiadez.webp" alt={tr("Foto del usuario", "User photo", "Photo de l'utilisateur")} />
                </button>

                <div class="infobox-photo-menu hidden" id="profilePhotoMenu">
                  <button type="button" id="bioPhotoUpload">{tr("Subir imagen", "Upload image", "Téléverser une image")}</button>
                </div>

                <input id="bioPhotoFile" type="file" accept="image/*" class="hidden" />
              </div>
            </figure>
            <p class="infobox-photo-status" id="bioPhotoStatus" aria-live="polite"></p>

            <!-- Sección -->
            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">{tr("Información personal", "Personal information", "Informations personnelles")}</span>
                <button class="infobox-edit-btn" id="personalInfoEditBtn" type="button" title={tr("Editar información personal", "Edit personal information", "Modifier les informations personnelles")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Editar información personal", "Edit personal information", "Modifier les informations personnelles")} />
                </button>
              </div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="birthname">
                  <th>{tr("Nombre de nacimiento", "Birth name", "Nom de naissance")}</th>
                  <td><span id="personalInfoBirthNameValue">Carlos Jiménez Duarte</span></td>
                </tr>
                <tr data-field="birth">
                  <th>{tr("Nacimiento", "Birth", "Naissance")}</th>
                  <td><span id="personalInfoBirthValue">{tr("5 de mayo de 1986 (39 años); Barrancabermeja, Santander, Colombia", "May 5, 1986 (39 years old); Barrancabermeja, Santander, Colombia", "5 mai 1986 (39 ans) ; Barrancabermeja, Santander, Colombie")}</span></td>
                </tr>
                <tr data-field="residence">
                  <th>{tr("Residencia", "Residence", "Résidence")}</th>
                  <td><span id="personalInfoResidenceValue">{tr("Medellín, Antioquia", "Medellin, Antioquia", "Medellín, Antioquia")}</span></td>
                </tr>
                <tr data-field="nationality">
                  <th>{tr("Nacionalidad", "Nationality", "Nationalité")}</th>
                  <td><span id="personalInfoNationalityValue">{tr("Colombiana", "Colombian", "Colombienne")}</span></td>
                </tr>
                <tr data-field="lang">
                  <th>{tr("Lengua materna", "Native language", "Langue maternelle")}</th>
                  <td><span id="personalInfoNativeLanguageValue">{tr("Español", "Spanish", "Espagnol")}</span></td>
                </tr>
                <tr data-field="pseudonyms">
                  <th>{tr("Seudónimos", "Pseudonyms", "Pseudonymes")}</th>
                  <td><span id="personalInfoPseudonymsValue">Melquíades, Kiadez, Saint Martin</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">{tr("Características físicas", "Physical traits", "Caractéristiques physiques")}</span>
                <button class="infobox-edit-btn" id="physicalTraitsEditBtn" type="button" title={tr("Editar características físicas", "Edit physical traits", "Modifier les caractéristiques physiques")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Editar características físicas", "Edit physical traits", "Modifier les caractéristiques physiques")} />
                </button>
              </div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="height">
                  <th>{tr("Altura", "Height", "Taille")}</th>
                  <td><span id="physicalTraitsHeightValue">1,80 m</span></td>
                </tr>
                <tr data-field="weight">
                  <th>{tr("Peso", "Weight", "Poids")}</th>
                  <td><span id="physicalTraitsWeightValue">76 kg</span></td>
                </tr>
                <tr data-field="eyes">
                  <th>{tr("Ojos", "Eyes", "Yeux")}</th>
                  <td><span id="physicalTraitsEyesValue">{tr("Castaño", "Brown", "Marron")}</span></td>
                </tr>
                <tr data-field="hair">
                  <th>{tr("Cabello", "Hair", "Cheveux")}</th>
                  <td><span id="physicalTraitsHairValue">{tr("Castaño", "Brown", "Marron")}</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">{tr("Educación", "Education", "Éducation")}</span>
                <button class="infobox-edit-btn" id="educationEditBtn" type="button" title={tr("Editar educación", "Edit education", "Modifier l'éducation")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Editar educación", "Edit education", "Modifier l'éducation")} />
                </button>
              </div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="education">
                  <th>{tr("Educado en", "Educated at", "Éduqué à")}</th>
                  <td>
                    <div class="education-slots">
                      <div class="education-slot" id="educationSlot1Value">{tr("Colegio Calasanz", "Calasanz School", "Collège Calasanz")}</div>
                      <div class="education-slot" id="educationSlot2Value">{tr("Universidad Pontificia Bolivariana", "Pontifical Bolivarian University", "Université Pontificale Bolivarienne")}</div>
                      <div class="education-slot" id="educationSlot3Value">{tr("Politécnico Grancolombiano", "Grancolombiano Polytechnic", "Polytechnique Grancolombiano")}</div>
                      <div class="education-slot" id="educationSlot4Value"></div>
                    </div>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">{tr("Información profesional", "Professional information", "Informations professionnelles")}</span>
                <button class="infobox-edit-btn" id="professionalInfoEditBtn" type="button" title={tr("Editar información profesional", "Edit professional information", "Modifier les informations professionnelles")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Editar información profesional", "Edit professional information", "Modifier les informations professionnelles")} />
                </button>
              </div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="occupation">
                  <th>{tr("Ocupación", "Occupation", "Profession")}</th>
                  <td><span id="professionalOccupationValue">{tr("Escritor, Ingeniero de Software, Artista Plástico Aficionado", "Writer, Software Engineer, Amateur Visual Artist", "Écrivain, Ingénieur logiciel, Artiste plastique amateur")}</span></td>
                </tr>
                <tr data-field="active">
                  <th>{tr("Años activo", "Active years", "Années d'activité")}</th>
                  <td><span id="professionalActiveYearsValue">{tr("2003 — presente", "2003 — present", "2003 — présent")}</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">{tr("Distinciones", "Distinctions", "Distinctions")}</span>
                <button class="infobox-edit-btn hidden" id="distinctionsEditBtn" type="button" title={tr("Editar distinciones", "Edit distinctions", "Modifier les distinctions")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Editar distinciones", "Edit distinctions", "Modifier les distinctions")} />
                </button>
              </div>
              <p class="infobox-guardian-note">
                {tr(
                  "Esta sección solo puede ser actualizada por los Guardianes de Kiadez.com.",
                  "This section can only be updated by Kiadez.com Guardians."
                )}
              </p>
              <table class="infobox-table">
                <tbody id="distinctionsRows"></tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">{tr("Curiosidades", "Curiosities", "Curiosités")}</span>
                <button class="infobox-edit-btn" id="curiositiesEditBtn" type="button" title={tr("Editar curiosidades", "Edit curiosities", "Modifier les curiosités")}>
                  <img src="/css/icons/iconedit.webp" alt={tr("Editar curiosidades", "Edit curiosities", "Modifier les curiosités")} />
                </button>
              </div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="hero">
                  <th>{tr("Superhéroe favorito", "Favorite superhero", "Super-héros préféré")}</th>
                  <td><span id="curiositiesHeroValue">Batman</span></td>
                </tr>
                <tr data-field="song">
                  <th>{tr("Canción favorita", "Favorite song", "Chanson préférée")}</th>
                  <td><span id="curiositiesSongValue">Dreamer — Ozzy Osbourne</span></td>
                </tr>
                <tr data-field="food">
                  <th>{tr("Comida favorita", "Favorite food", "Nourriture préférée")}</th>
                  <td><span id="curiositiesFoodValue">{tr("Comida mexicana", "Mexican food", "Cuisine mexicaine")}</span></td>
                </tr>
                <tr data-field="games">
                  <th>{tr("Videojuegos", "Video games", "Jeux vidéo")}</th>
                  <td><span id="curiositiesGamesValue">Dofus, Prince of Persia 2, Batman Arkham Knight</span></td>
                </tr>
                <tr data-field="book">
                  <th>{tr("Libro favorito", "Favorite book", "Livre préféré")}</th>
                  <td><span id="curiositiesBookValue">{tr("Las Mil y Una Noches", "One Thousand and One Nights", "Les Mille et Une Nuits")}</span></td>
                </tr>
                <tr data-field="hobbies">
                  <th>{tr("Otros pasatiempos", "Other hobbies", "Autres passe-temps")}</th>
                  <td><span id="curiositiesHobbiesValue">{tr("Sacar a Willow a paseo, reír, ver series, soñar en grande", "Walking Willow, laughing, watching shows, dreaming big", "Promener Willow, rire, regarder des séries, rêver en grand")}</span></td>
                </tr>
                <tr data-field="motto">
                  <th>{tr("Lema", "Motto", "Devise")}</th>
                  <td><span id="curiositiesMottoValue">{tr("A Dios sea la gloria", "Glory be to God", "Gloire à Dieu")}</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">{tr("Actividad en Kiadez.com", "Activity on Kiadez.com", "Activité sur Kiadez.com")}</div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="wishes_done">
                  <th>{tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</th>
                  <td><span id="wishesFulfilledValue" data-value>0</span><span class="infobox-hidden" data-hidden hidden>{tr("Prefiero no decirlo", "I prefer not to say", "Je préfère ne pas le dire")}</span>
                  </td>
                </tr>
                <tr data-field="cooperative_wishes_done">
                  <th>{tr("Deseos cooperativos cumplidos", "Fulfilled cooperative wishes", "Souhaits coopératifs accomplis")}</th>
                  <td><span id="cooperativeWishesFulfilledValue" data-value>0</span><span class="infobox-hidden" data-hidden hidden>{tr("Prefiero no decirlo", "I prefer not to say", "Je préfère ne pas le dire")}</span>
                  </td>
                </tr>
                <tr data-field="wishes_granted">
                  <th>{tr("Deseos concedidos", "Granted wishes", "Souhaits accordés")}</th>
                  <td><span id="wishesGrantedValue" data-value>0</span><span class="infobox-hidden" data-hidden hidden>{tr("Prefiero no decirlo", "I prefer not to say", "Je préfère ne pas le dire")}</span>
                  </td>
                </tr>
                <tr data-field="rank" id="activityRankRow" class="hidden">
                  <th>{tr("Rango", "Rank", "Rang")}</th>
                  <td><span id="activityRankValue" data-value></span><span class="infobox-hidden" data-hidden hidden>{tr("Prefiero no decirlo", "I prefer not to say", "Je préfère ne pas le dire")}</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">{tr("Emblema", "Emblem", "Emblème")}</div>
              <div class="infobox-emblem">
                <div class="infobox-photo-wrap infobox-emblem-wrap">
                  <button class="infobox-photo-trigger infobox-emblem-trigger" id="emblemTrigger" type="button" title={tr("Gestionar emblema", "Manage emblem", "Gérer l'emblème")}>
                    <img id="emblemImage" src="/css/logo-kiadez.webp" alt={tr("Emblema", "Emblem", "Emblème")} />
                  </button>
                  <div class="infobox-photo-menu hidden" id="emblemMenu">
                    <button type="button" id="emblemUpload">{tr("Subir imagen", "Upload image", "Téléverser une image")}</button>
                  </div>
                  <input id="emblemFile" type="file" accept="image/*" class="hidden" />
                </div>
              </div>
              <p class="infobox-photo-status" id="emblemStatus" aria-live="polite"></p>
            </div>

            <!-- Panel de privacidad (aparece en modo edición) -->
            <div class="infobox-privacy-panel" id="privacyPanel" hidden>
              <p class="bio-side-note" style="margin:0 0 10px;">
                {tr(
                  "Activa/desactiva qué campos aparecen públicos. Si lo apagas, se muestra “Prefiero no decirlo”.",
                  'Toggle which fields are public. If you disable them, “I prefer not to say” is shown.'
                )}
              </p>
              <div class="privacy-grid" id="privacyGrid"></div>
            </div>

          </aside>

        </section>

      </section>
      </div>

    </main>

    <div class="modal-overlay hidden" id="aboutModalOverlay" aria-hidden="true">
      <div class="modal about-modal" role="dialog" aria-modal="true" aria-label={tr("Editar biografía", "Edit biography", "Modifier la biographie")}>
        <div class="modal-head">
          <h3>{tr("Editar biografía", "Edit biography", "Modifier la biographie")}</h3>
          <button class="modal-close" type="button" id="closeAboutModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="about-modal-name">
            <label class="modal-label" for="aboutDisplayNameInput">{tr("Nombre público", "Public name", "Nom public")}</label>
            <input class="modal-input about-modal-name-input" id="aboutDisplayNameInput" type="text" maxlength="200" />
          </div>

          <p class="bio-prompt about-modal-prompt">
            {tr(
              "Describe quién eres. Se sugiere hacerlo en tercera persona. Aprovecha este espacio: es tu Wikipedia personal. Lo que escribas aquí será lo mismo que podrían leer tus seres queridos dentro de 100 años.",
              "Describe who you are. It is recommended to write in the third person. Use this space well: it is your personal Wikipedia. What you write here could be read by your loved ones 100 years from now."
            )}
          </p>

          <div class="about-modal-editor">
            <textarea class="bio-textarea about-modal-textarea" id="aboutTextInput" placeholder={tr("Escribe aquí...", "Write here...", "Écris ici...")}></textarea>
            <div class="bio-meta">
              <span id="aboutWordCounter">{tr("0 / 1200 palabras", "0 / 1200 words", "0 / 1200 mots")}</span>
            </div>
          </div>

          <p class="infobox-photo-status" id="aboutModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelAboutModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveAboutBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="dreamModalOverlay" aria-hidden="true">
      <div class="modal about-modal dream-modal" role="dialog" aria-modal="true" aria-label={tr("Editar mayor sueño", "Edit greatest dream", "Modifier le plus grand rêve")}>
        <div class="modal-head">
          <h3>{tr("Editar mayor sueño", "Edit greatest dream", "Modifier le plus grand rêve")}</h3>
          <button class="modal-close" type="button" id="closeDreamModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="about-modal-name">
            <label class="modal-label" for="dreamTitleInput">{tr("Título de sección", "Section title", "Titre de section")}</label>
            <input class="modal-input about-modal-name-input" id="dreamTitleInput" type="text" maxlength="200" />
          </div>

          <p class="bio-prompt about-modal-prompt">
            {tr(
              "Describe aquí cuál es ese sueño que te gustaría ver realidad: aquello que, contra todo pronóstico, te gustaría ver realizado. O, si lo sientes, lo que te gustaría alcanzar en una nueva vida. Simplemente sueña y cree.",
              "Describe here the dream you would most like to see become real: what, against all odds, you want fulfilled. Or, if you feel it, what you would like to reach in a new life. Simply dream and believe."
            )}
          </p>

          <div class="about-modal-editor">
            <textarea class="bio-textarea about-modal-textarea" id="dreamTextInput" placeholder={tr("Escribe aquí...", "Write here...", "Écris ici...")}></textarea>
            <div class="bio-meta">
              <span id="dreamWordCounter">{tr("0 / 1200 palabras", "0 / 1200 words", "0 / 1200 mots")}</span>
            </div>
          </div>

          <p class="infobox-photo-status" id="dreamModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelDreamModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveDreamBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="proAchievementsModalOverlay" aria-hidden="true">
      <div class="modal about-modal pro-achievements-modal" role="dialog" aria-modal="true" aria-label={tr("Editar logros profesionales", "Edit professional achievements", "Modifier les réalisations professionnelles")}>
        <div class="modal-head">
          <h3>{tr("Editar logros profesionales", "Edit professional achievements", "Modifier les réalisations professionnelles")}</h3>
          <button class="modal-close" type="button" id="closeProAchievementsModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="about-modal-name">
            <label class="modal-label" for="proAchievementsTitleInput">{tr("Título de sección", "Section title", "Titre de section")}</label>
            <input class="modal-input about-modal-name-input" id="proAchievementsTitleInput" type="text" maxlength="200" />
          </div>

          <p class="bio-prompt about-modal-prompt">
            {tr(
              "Describe aquí los logros personales o académicos más importantes que consideras has conseguido hasta ahora. Esto te servirá como tu propia versión de LinkedIn. (Recomendado en viñetas.)",
              "Describe here the most important personal or academic achievements you believe you have reached so far. This will serve as your own LinkedIn-style section. (Bullet points are recommended.)"
            )}
          </p>

          <div class="about-modal-editor">
            <textarea class="bio-textarea about-modal-textarea" id="proAchievementsTextInput" placeholder={tr("Escribe aquí...", "Write here...", "Écris ici...")}></textarea>
            <div class="bio-meta">
              <span id="proAchievementsWordCounter">{tr("0 / 500 palabras", "0 / 500 words", "0 / 500 mots")}</span>
            </div>
          </div>

          <p class="infobox-photo-status" id="proAchievementsModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelProAchievementsModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveProAchievementsBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="lifeAchievementsModalOverlay" aria-hidden="true">
      <div class="modal about-modal life-achievements-modal" role="dialog" aria-modal="true" aria-label={tr("Editar logros alcanzados", "Edit life achievements", "Modifier les réalisations de vie")}>
        <div class="modal-head">
          <h3>{tr("Editar logros alcanzados", "Edit life achievements", "Modifier les réalisations de vie")}</h3>
          <button class="modal-close" type="button" id="closeLifeAchievementsModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="about-modal-name">
            <label class="modal-label" for="lifeAchievementsTitleInput">{tr("Título de sección", "Section title", "Titre de section")}</label>
            <input class="modal-input about-modal-name-input" id="lifeAchievementsTitleInput" type="text" maxlength="200" />
          </div>

          <p class="bio-prompt about-modal-prompt">
            {tr(
              "Describe aquí los logros personales que te hacen sentir orgulloso; aquello que sabes define tu existencia. (Recomendado en viñetas.)",
              "Describe here the personal achievements that make you feel proud; what you know defines your existence. (Bullet points are recommended.)"
            )}
          </p>

          <div class="about-modal-editor">
            <textarea class="bio-textarea about-modal-textarea" id="lifeAchievementsTextInput" placeholder={tr("Escribe aquí...", "Write here...", "Écris ici...")}></textarea>
            <div class="bio-meta">
              <span id="lifeAchievementsWordCounter">{tr("0 / 500 palabras", "0 / 500 words", "0 / 500 mots")}</span>
            </div>
          </div>

          <p class="infobox-photo-status" id="lifeAchievementsModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelLifeAchievementsModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveLifeAchievementsBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="quotesModalOverlay" aria-hidden="true">
      <div class="modal about-modal quotes-modal" role="dialog" aria-modal="true" aria-label={tr("Editar frases favoritas", "Edit favorite quotes", "Modifier les citations favorites")}>
        <div class="modal-head">
          <h3>{tr("Editar frases favoritas", "Edit favorite quotes", "Modifier les citations favorites")}</h3>
          <button class="modal-close" type="button" id="closeQuotesModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="about-modal-name">
            <label class="modal-label" for="quotesTitleInput">{tr("Título de sección", "Section title", "Titre de section")}</label>
            <input class="modal-input about-modal-name-input" id="quotesTitleInput" type="text" maxlength="200" />
          </div>

          <p class="bio-prompt about-modal-prompt">
            {tr(
              "Describe tu filosofía de vida en 3 o 4 frases. Cuando ya no estés en este mundo, las personas podrían recordarte por estas banderas personales.",
              "Describe your life philosophy in 3 or 4 quotes. When you are no longer in this world, people may remember you through these personal banners."
            )}
          </p>

          <div class="about-modal-editor">
            <textarea class="bio-textarea about-modal-textarea" id="quotesTextInput" placeholder={tr("Escribe aquí...", "Write here...", "Écris ici...")}></textarea>
            <div class="bio-meta">
              <span id="quotesWordCounter">{tr("0 / 500 palabras", "0 / 500 words", "0 / 500 mots")}</span>
            </div>
          </div>

          <p class="infobox-photo-status" id="quotesModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelQuotesModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveQuotesBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="distinctionsModalOverlay" aria-hidden="true">
      <div class="modal about-modal distinctions-modal" role="dialog" aria-modal="true" aria-label={tr("Editar distinciones", "Edit distinctions", "Modifier les distinctions")}>
        <div class="modal-head">
          <h3>{tr("Editar distinciones", "Edit distinctions", "Modifier les distinctions")}</h3>
          <button class="modal-close" type="button" id="closeDistinctionsModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="distinctions-grid" id="distinctionsForm"></div>
          <p class="infobox-photo-status" id="distinctionsModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelDistinctionsModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveDistinctionsBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="personalInfoModalOverlay" aria-hidden="true">
      <div class="modal personal-info-modal" role="dialog" aria-modal="true" aria-label={tr("Editar información personal", "Edit personal information", "Modifier les informations personnelles")}>
        <div class="modal-head">
          <h3>{tr("Editar información personal", "Edit personal information", "Modifier les informations personnelles")}</h3>
          <button class="modal-close" type="button" id="closePersonalInfoModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="personal-info-grid">
            <div class="personal-info-col">
              <div class="personal-info-field">
                <label class="modal-label" for="personalBirthNameInput">{tr("Nombre de nacimiento", "Birth name", "Nom de naissance")}</label>
                <input class="modal-input" id="personalBirthNameInput" type="text" maxlength="200" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalBirthDateInput">{tr("Nacimiento", "Birth", "Naissance")}</label>
                <input class="modal-input" id="personalBirthDateInput" type="date" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalBirthCityInput">{tr("Ciudad de nacimiento", "Birth city", "Ville de naissance")}</label>
                <input class="modal-input" id="personalBirthCityInput" type="text" maxlength="120" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalBirthRegionInput">{tr("Región / Estado de nacimiento", "Birth region / state", "Région / État de naissance")}</label>
                <input class="modal-input" id="personalBirthRegionInput" type="text" maxlength="120" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalBirthCountryInput">{tr("País de nacimiento", "Birth country", "Pays de naissance")}</label>
                <input class="modal-input" id="personalBirthCountryInput" type="text" maxlength="120" />
              </div>
            </div>

            <div class="personal-info-col">
              <div class="personal-info-field">
                <label class="modal-label" for="personalResidenceInput">{tr("Residencia", "Residence", "Résidence")}</label>
                <input class="modal-input" id="personalResidenceInput" type="text" maxlength="255" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalNationalityInput">{tr("Nacionalidad", "Nationality", "Nationalité")}</label>
                <input class="modal-input" id="personalNationalityInput" type="text" maxlength="120" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalNativeLanguageInput">{tr("Lengua materna", "Native language", "Langue maternelle")}</label>
                <input class="modal-input" id="personalNativeLanguageInput" type="text" maxlength="120" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalPseudonymsInput">{tr("Seudónimos", "Pseudonyms", "Pseudonymes")}</label>
                <input class="modal-input" id="personalPseudonymsInput" type="text" maxlength="300" />
              </div>
            </div>
          </div>

          <p class="infobox-photo-status" id="personalInfoModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelPersonalInfoModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="savePersonalInfoBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="physicalTraitsModalOverlay" aria-hidden="true">
      <div class="modal physical-traits-modal" role="dialog" aria-modal="true" aria-label={tr("Editar características físicas", "Edit physical traits", "Modifier les caractéristiques physiques")}>
        <div class="modal-head">
          <h3>{tr("Editar características físicas", "Edit physical traits", "Modifier les caractéristiques physiques")}</h3>
          <button class="modal-close" type="button" id="closePhysicalTraitsModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="physical-traits-grid">
            <div class="physical-traits-col">
              <div class="physical-traits-field">
                <label class="modal-label" for="physicalHeightInput">{tr("Altura", "Height", "Taille")}</label>
                <input class="modal-input" id="physicalHeightInput" type="text" maxlength="40" placeholder={tr("Ej: 1,80 m", "Ex: 5'11\\\"", "Ex : 5'11\\\"")} />
              </div>

              <div class="physical-traits-field">
                <label class="modal-label" for="physicalWeightInput">{tr("Peso", "Weight", "Poids")}</label>
                <input class="modal-input" id="physicalWeightInput" type="text" maxlength="40" placeholder={tr("Ej: 76 kg", "Ex: 168 lb", "Ex : 168 lb")} />
              </div>
            </div>

            <div class="physical-traits-col">
              <div class="physical-traits-field">
                <label class="modal-label" for="physicalEyesInput">{tr("Ojos", "Eyes", "Yeux")}</label>
                <input class="modal-input" id="physicalEyesInput" type="text" maxlength="80" placeholder={tr("Ej: Castaño", "Ex: Brown", "Ex : Marron")} />
              </div>

              <div class="physical-traits-field">
                <label class="modal-label" for="physicalHairInput">{tr("Cabello", "Hair", "Cheveux")}</label>
                <input class="modal-input" id="physicalHairInput" type="text" maxlength="80" placeholder={tr("Ej: Castaño", "Ex: Brown", "Ex : Marron")} />
              </div>
            </div>
          </div>

          <p class="infobox-photo-status" id="physicalTraitsModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelPhysicalTraitsModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="savePhysicalTraitsBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="educationModalOverlay" aria-hidden="true">
      <div class="modal education-modal" role="dialog" aria-modal="true" aria-label={tr("Editar educación", "Edit education", "Modifier l'éducation")}>
        <div class="modal-head">
          <h3>{tr("Editar educación", "Edit education", "Modifier l'éducation")}</h3>
          <button class="modal-close" type="button" id="closeEducationModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="education-grid">
            <div class="education-col">
              <div class="education-field">
                <label class="modal-label" for="educationSlot1Input">{tr("Institución académica 1", "Academic institution 1", "Institution académique 1")}</label>
                <input class="modal-input" id="educationSlot1Input" type="text" maxlength="255" placeholder={tr("Ej: Colegio...", "Ex: School...", "Ex : École...")} />
              </div>
              <div class="education-field">
                <label class="modal-label" for="educationSlot2Input">{tr("Institución académica 2", "Academic institution 2", "Institution académique 2")}</label>
                <input class="modal-input" id="educationSlot2Input" type="text" maxlength="255" placeholder={tr("Ej: Universidad...", "Ex: University...", "Ex : Université...")} />
              </div>
            </div>
            <div class="education-col">
              <div class="education-field">
                <label class="modal-label" for="educationSlot3Input">{tr("Institución académica 3", "Academic institution 3", "Institution académique 3")}</label>
                <input class="modal-input" id="educationSlot3Input" type="text" maxlength="255" placeholder={tr("Ej: Instituto...", "Ex: Institute...", "Ex : Institut...")} />
              </div>
              <div class="education-field">
                <label class="modal-label" for="educationSlot4Input">{tr("Institución académica 4", "Academic institution 4", "Institution académique 4")}</label>
                <input class="modal-input" id="educationSlot4Input" type="text" maxlength="255" placeholder={tr("Ej: Academia...", "Ex: Academy...", "Ex : Académie...")} />
              </div>
            </div>
          </div>

          <p class="infobox-photo-status" id="educationModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelEducationModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveEducationBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="curiositiesModalOverlay" aria-hidden="true">
      <div class="modal curiosities-modal" role="dialog" aria-modal="true" aria-label={tr("Editar curiosidades", "Edit curiosities", "Modifier les curiosités")}>
        <div class="modal-head">
          <h3>{tr("Editar curiosidades", "Edit curiosities", "Modifier les curiosités")}</h3>
          <button class="modal-close" type="button" id="closeCuriositiesModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="curiosities-grid">
            <div class="curiosities-col">
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityHeroInput">{tr("Superhéroe favorito", "Favorite superhero", "Super-héros préféré")}</label>
                <input class="modal-input" id="curiosityHeroInput" type="text" maxlength="120" />
              </div>
              <div class="curiosities-field">
                <label class="modal-label" for="curiositySongInput">{tr("Canción favorita", "Favorite song", "Chanson préférée")}</label>
                <input class="modal-input" id="curiositySongInput" type="text" maxlength="255" />
              </div>
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityFoodInput">{tr("Comida favorita", "Favorite food", "Nourriture préférée")}</label>
                <input class="modal-input" id="curiosityFoodInput" type="text" maxlength="160" />
              </div>
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityGamesInput">{tr("Videojuegos", "Video games", "Jeux vidéo")}</label>
                <input class="modal-input" id="curiosityGamesInput" type="text" maxlength="500" />
              </div>
            </div>
            <div class="curiosities-col">
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityBookInput">{tr("Libro favorito", "Favorite book", "Livre préféré")}</label>
                <input class="modal-input" id="curiosityBookInput" type="text" maxlength="255" />
              </div>
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityHobbiesInput">{tr("Otros pasatiempos", "Other hobbies", "Autres passe-temps")}</label>
                <input class="modal-input" id="curiosityHobbiesInput" type="text" maxlength="500" />
              </div>
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityMottoInput">{tr("Lema", "Motto", "Devise")}</label>
                <input class="modal-input" id="curiosityMottoInput" type="text" maxlength="255" />
              </div>
            </div>
          </div>
          <p class="infobox-photo-status" id="curiositiesModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelCuriositiesModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveCuriositiesBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="professionalInfoModalOverlay" aria-hidden="true">
      <div class="modal professional-info-modal" role="dialog" aria-modal="true" aria-label={tr("Editar información profesional", "Edit professional information", "Modifier les informations professionnelles")}>
        <div class="modal-head">
          <h3>{tr("Editar información profesional", "Edit professional information", "Modifier les informations professionnelles")}</h3>
          <button class="modal-close" type="button" id="closeProfessionalInfoModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="professional-info-grid">
            <div class="professional-info-field">
              <label class="modal-label" for="professionalOccupationInput">{tr("Ocupación", "Occupation", "Profession")}</label>
              <input class="modal-input" id="professionalOccupationInput" type="text" maxlength="500" />
            </div>
            <div class="professional-info-field">
              <label class="modal-label" for="professionalActiveYearsInput">{tr("Años activo", "Active years", "Années d'activité")}</label>
              <input class="modal-input" id="professionalActiveYearsInput" type="text" maxlength="120" />
            </div>
          </div>
          <p class="infobox-photo-status" id="professionalInfoModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelProfessionalInfoModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveProfessionalInfoBtn">{tr("Guardar", "Save", "Enregistrer")}</button>
        </div>
      </div>
    </div>

      <AuthFooter />


  </div>
