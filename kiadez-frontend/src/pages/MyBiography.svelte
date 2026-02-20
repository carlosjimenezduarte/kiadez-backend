<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";

  onMount(() => {
    initPurposeCoverModule();
    void syncProfileStarsTotal("biographyStarsTotal");

    const API = "http://127.0.0.1:8000";
    const profilePhoto = document.getElementById("profilePhoto");
    const profilePhotoTrigger = document.getElementById("profilePhotoTrigger");
    const profilePhotoMenu = document.getElementById("profilePhotoMenu");
    const bioPhotoSelectExisting = document.getElementById("bioPhotoSelectExisting");
    const bioPhotoUpload = document.getElementById("bioPhotoUpload");
    const bioPhotoFile = document.getElementById("bioPhotoFile");
    const bioPhotoStatus = document.getElementById("bioPhotoStatus");
    const bioPhotoSelectModal = document.getElementById("bioPhotoSelectModal");
    const bioPhotoSelectGrid = document.getElementById("bioPhotoSelectGrid");
    const bioPhotoSelectCancel = document.getElementById("bioPhotoSelectCancel");
    const emblemImage = document.getElementById("emblemImage");
    const emblemTrigger = document.getElementById("emblemTrigger");
    const emblemMenu = document.getElementById("emblemMenu");
    const emblemSelectExisting = document.getElementById("emblemSelectExisting");
    const emblemUpload = document.getElementById("emblemUpload");
    const emblemFile = document.getElementById("emblemFile");
    const emblemStatus = document.getElementById("emblemStatus");
    const emblemSelectModal = document.getElementById("emblemSelectModal");
    const emblemSelectGrid = document.getElementById("emblemSelectGrid");
    const emblemSelectCancel = document.getElementById("emblemSelectCancel");
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
    const wishesGrantedValue = document.getElementById("wishesGrantedValue");

    const defaultProfilePhotoSrc = profilePhoto?.getAttribute("src") || "/css/logo-kiadez.webp";
    const defaultEmblemSrc = emblemImage?.getAttribute("src") || "/css/logo-kiadez.webp";
    const ABOUT_MAX_WORDS = 1200;
    const DREAM_MAX_WORDS = 1200;
    const PRO_ACHIEVEMENTS_MAX_WORDS = 500;
    const LIFE_ACHIEVEMENTS_MAX_WORDS = 500;
    const FAVORITE_QUOTES_MAX_WORDS = 500;
    const DISTINCTIONS_MAX_SLOTS = 10;
    const GUARDIAN_MIN_RANK = 3;
    const defaultAboutDisplayName = (aboutDisplayNameValue?.textContent || infoName?.textContent || "Usuario Kiadez").trim();
    const defaultDreamTitle = (dreamTitleValue?.textContent || "Sobre su mayor sueño").trim();
    const defaultProAchievementsTitle = (proAchievementsTitleValue?.textContent || "Logros profesionales").trim();
    const defaultLifeAchievementsTitle = (lifeAchievementsTitleValue?.textContent || "Logros alcanzados").trim();
    const defaultQuotesTitle = (quotesTitleValue?.textContent || "Frases favoritas").trim();
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
      if (!token) throw new Error("No hay sesión activa.");
      const headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`,
      };
      const res = await fetch(`${API}${path}`, { ...options, headers });
      if (res.status === 401) {
        throw new Error("Sesión expirada. Inicia sesión nuevamente.");
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
        throw new Error("No se pudo identificar el perfil a editar.");
      }
      return `/biography/distinctions/${encodeURIComponent(String(profileId))}`;
    };

    const fetchViewerIdentity = async () => {
      const res = await apiFetch("/auth/me");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo cargar tu sesión.");
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
        throw new Error(data.detail || "No se pudo cargar el perfil solicitado.");
      }
      return data;
    };

    const applyDistinctionsEditorVisibility = () => {
      const canEdit = isViewerGuardian();
      if (distinctionsEditBtn) {
        distinctionsEditBtn.classList.toggle("hidden", !canEdit);
        distinctionsEditBtn.disabled = !canEdit;
      }
    };

    const ensureDistinctionsForm = () => {
      if (!distinctionsForm) return;
      if (distinctionsForm.childElementCount > 0) return;

      distinctionsForm.innerHTML = Array.from({ length: DISTINCTIONS_MAX_SLOTS }, (_, index) => {
        const slotNumber = index + 1;
        return `
          <div class="distinction-slot-card">
            <p class="distinction-slot-title">Distinción ${slotNumber}</p>
            <label class="modal-label" for="distinctionTypeInput${slotNumber}">Tipo de distinción</label>
            <input class="modal-input" id="distinctionTypeInput${slotNumber}" type="text" maxlength="120" />
            <label class="modal-label" for="distinctionDescriptionInput${slotNumber}">Descripción</label>
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
      viewerGuardianRank = Number(me?.guardian_rank || 0) || 0;
      viewerUsername = normalizeUsername(me?.username || "");
      activeProfileUserId = viewerUserId;
      activeProfileUsername = viewerUsername;
      isViewingOwnProfile = true;

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
            if (fullName && infoName) infoName.textContent = fullName;
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
        header.textContent = slot.distinction_type || `Distinción ${slot.slot_number}`;
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

    const applyActivityStatsToView = (stats) => {
      if (!wishesGrantedValue) return;
      const totalGranted = Number(stats?.wishes_granted);
      wishesGrantedValue.textContent = Number.isFinite(totalGranted) ? String(Math.max(0, Math.trunc(totalGranted))) : "0";
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
        throw new Error(data.detail || "No se pudo cargar la información personal.");
      }
      currentPersonalInfo = data;
      applyPersonalInfoToView(data);
      return data;
    };

    const loadPhysicalTraits = async () => {
      const res = await apiFetch("/biography/physical-traits");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudieron cargar las características físicas.");
      }
      currentPhysicalTraits = data;
      applyPhysicalTraitsToView(data);
      return data;
    };

    const loadEducation = async () => {
      const res = await apiFetch("/biography/education");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo cargar Educación.");
      }
      currentEducation = data;
      applyEducationToView(data);
      return data;
    };

    const loadCuriosities = async () => {
      const res = await apiFetch("/biography/curiosities");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudieron cargar las curiosidades.");
      }
      currentCuriosities = data;
      applyCuriositiesToView(data);
      return data;
    };

    const loadProfessionalInfo = async () => {
      const res = await apiFetch("/biography/professional-info");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo cargar la información profesional.");
      }
      currentProfessionalInfo = data;
      applyProfessionalInfoToView(data);
      return data;
    };

    const loadAbout = async () => {
      const res = await apiFetch("/biography/about");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo cargar tu biografía.");
      }
      currentAbout = data;
      applyAboutToView(data);
      return data;
    };

    const loadDream = async () => {
      const res = await apiFetch("/biography/dream");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo cargar tu mayor sueño.");
      }
      currentDream = data;
      applyDreamToView(data);
      return data;
    };

    const loadProAchievements = async () => {
      const res = await apiFetch("/biography/professional-achievements");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudieron cargar tus logros profesionales.");
      }
      currentProAchievements = data;
      applyProAchievementsToView(data);
      return data;
    };

    const loadLifeAchievements = async () => {
      const res = await apiFetch("/biography/life-achievements");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudieron cargar tus logros alcanzados.");
      }
      currentLifeAchievements = data;
      applyLifeAchievementsToView(data);
      return data;
    };

    const loadFavoriteQuotes = async () => {
      const res = await apiFetch("/biography/favorite-quotes");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudieron cargar tus frases favoritas.");
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
        throw new Error(data.detail || "No se pudieron cargar las distinciones.");
      }
      currentDistinctions = data;
      applyDistinctionsToView(data);
      return data;
    };

    const loadActivityStats = async () => {
      const res = await apiFetch("/biography/activity-stats");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo cargar la actividad de Kiadez.");
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

    const openPhotoSelectModal = () => {
      bioPhotoSelectModal?.classList.remove("hidden");
      bioPhotoSelectModal?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const closePhotoSelectModal = () => {
      bioPhotoSelectModal?.classList.add("hidden");
      bioPhotoSelectModal?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const openEmblemSelectModal = () => {
      emblemSelectModal?.classList.remove("hidden");
      emblemSelectModal?.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
    };

    const closeEmblemSelectModal = () => {
      emblemSelectModal?.classList.add("hidden");
      emblemSelectModal?.setAttribute("aria-hidden", "true");
      if (!document.querySelector(".modal-overlay:not(.hidden)")) {
        document.body.classList.remove("modal-open");
      }
    };

    const renderSelectableImages = (items) => {
      if (!bioPhotoSelectGrid) return;
      if (!items.length) {
        bioPhotoSelectGrid.innerHTML = `
          <p class="infobox-photo-empty">No tienes imágenes disponibles aún.</p>
        `;
        return;
      }
      bioPhotoSelectGrid.innerHTML = items
        .map(
          (item) => `
          <button class="cover-select-item" type="button" data-media-id="${item.media_id}" data-media-url="${item.url}">
            <img src="${item.url}" alt="Imagen subida ${item.media_id}" />
          </button>
        `
        )
        .join("");
    };

    const renderSelectableEmblemImages = (items) => {
      if (!emblemSelectGrid) return;
      if (!items.length) {
        emblemSelectGrid.innerHTML = `
          <p class="infobox-photo-empty">No tienes imágenes disponibles aún.</p>
        `;
        return;
      }
      emblemSelectGrid.innerHTML = items
        .map(
          (item) => `
          <button class="cover-select-item" type="button" data-media-id="${item.media_id}" data-media-url="${item.url}">
            <img src="${item.url}" alt="Imagen subida ${item.media_id}" />
          </button>
        `
        )
        .join("");
    };

    const assignProfilePhoto = async (mediaId) => {
      const res = await apiFetch("/media/profile-photo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ media_id: mediaId }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo asignar la foto de perfil.");
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
        throw new Error(data.detail || "No se pudo asignar el emblema.");
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

    const loadSelectableImages = async () => {
      const res = await apiFetch("/media/mine/images?limit=60");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "No se pudieron cargar tus imágenes.");
      }
      return Array.isArray(data.items) ? data.items : [];
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
        throw new Error(uploadData.detail || "No se pudo subir la imagen.");
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
        throw new Error(uploadData.detail || "No se pudo subir la imagen.");
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

    const handleOpenExisting = () => {
      closePhotoMenu();
      window.location.href = "/gallery.html";
    };

    const handleEmblemTriggerClick = (event) => {
      event.preventDefault();
      if (emblemMenu?.classList.contains("hidden")) {
        openEmblemMenu();
      } else {
        closeEmblemMenu();
      }
    };

    const handleOpenExistingEmblem = async () => {
      closeEmblemMenu();
      setEmblemStatus("Cargando imágenes...");
      openEmblemSelectModal();
      try {
        const items = await loadSelectableImages();
        renderSelectableEmblemImages(items);
        setEmblemStatus("");
      } catch (error) {
        renderSelectableEmblemImages([]);
        setEmblemStatus(error.message || "No se pudieron cargar imágenes.", true);
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
        setBioPhotoStatus("Solo se permiten imágenes.", true);
        return;
      }
      setBioPhotoStatus("Subiendo imagen a tu galería...");
      try {
        await uploadProfilePhotoFromFile(file);
        setBioPhotoStatus("Imagen subida. Para usarla como foto de perfil, ve a Home.");
      } catch (error) {
        setBioPhotoStatus(error.message || "No se pudo subir la imagen.", true);
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
        setEmblemStatus("Solo se permiten imágenes.", true);
        return;
      }
      setEmblemStatus("Subiendo imagen...");
      try {
        await uploadEmblemFromFile(file);
        setEmblemStatus("Emblema actualizado.");
      } catch (error) {
        setEmblemStatus(error.message || "No se pudo subir la imagen.", true);
      } finally {
        event.target.value = "";
      }
    };

    const handleSelectGridClick = () => {};

    const handleEmblemSelectGridClick = async (event) => {
      const button = event.target.closest("[data-media-id]");
      if (!button) return;
      const mediaId = Number(button.dataset.mediaId || "0");
      if (!mediaId) return;
      setEmblemStatus("Asignando imagen...");
      try {
        await assignEmblem(mediaId);
        setEmblemStatus("Emblema actualizado.");
        closeEmblemSelectModal();
      } catch (error) {
        setEmblemStatus(error.message || "No se pudo asignar la imagen.", true);
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

    const handleModalOverlayClick = (event) => {
      if (event.target === bioPhotoSelectModal) {
        closePhotoSelectModal();
      }
    };

    const handleEmblemModalOverlayClick = (event) => {
      if (event.target === emblemSelectModal) {
        closeEmblemSelectModal();
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
      setPersonalInfoModalStatus("Cargando datos...");
      try {
        if (!currentPersonalInfo) {
          await loadPersonalInfo();
        }
        fillPersonalInfoForm(currentPersonalInfo);
        openPersonalInfoModal();
      } catch (error) {
        setPersonalInfoModalStatus(error.message || "No se pudo cargar la información.", true);
      }
    };

    const handleOpenPhysicalTraitsModal = async () => {
      setPhysicalTraitsModalStatus("Cargando datos...");
      try {
        if (!currentPhysicalTraits) {
          await loadPhysicalTraits();
        }
        fillPhysicalTraitsForm(currentPhysicalTraits);
        openPhysicalTraitsModal();
      } catch (error) {
        setPhysicalTraitsModalStatus(error.message || "No se pudieron cargar los datos.", true);
      }
    };

    const handleOpenEducationModal = async () => {
      setEducationModalStatus("Cargando datos...");
      try {
        if (!currentEducation) {
          await loadEducation();
        }
        fillEducationForm(currentEducation);
        openEducationModal();
      } catch (error) {
        setEducationModalStatus(error.message || "No se pudo cargar Educación.", true);
      }
    };

    const handleOpenCuriositiesModal = async () => {
      setCuriositiesModalStatus("Cargando datos...");
      try {
        if (!currentCuriosities) {
          await loadCuriosities();
        }
        fillCuriositiesForm(currentCuriosities);
        openCuriositiesModal();
      } catch (error) {
        setCuriositiesModalStatus(error.message || "No se pudieron cargar las curiosidades.", true);
      }
    };

    const handleOpenProfessionalInfoModal = async () => {
      setProfessionalInfoModalStatus("Cargando datos...");
      try {
        if (!currentProfessionalInfo) {
          await loadProfessionalInfo();
        }
        fillProfessionalInfoForm(currentProfessionalInfo);
        openProfessionalInfoModal();
      } catch (error) {
        setProfessionalInfoModalStatus(error.message || "No se pudo cargar la información profesional.", true);
      }
    };

    const handleOpenAboutModal = async () => {
      setAboutModalStatus("Cargando datos...");
      try {
        if (!currentAbout) {
          await loadAbout();
        }
        fillAboutForm(currentAbout);
        openAboutModal();
      } catch (error) {
        setAboutModalStatus(error.message || "No se pudo cargar tu biografía.", true);
      }
    };

    const handleOpenDreamModal = async () => {
      setDreamModalStatus("Cargando datos...");
      try {
        if (!currentDream) {
          await loadDream();
        }
        fillDreamForm(currentDream);
        openDreamModal();
      } catch (error) {
        setDreamModalStatus(error.message || "No se pudo cargar tu mayor sueño.", true);
      }
    };

    const handleOpenProAchievementsModal = async () => {
      setProAchievementsModalStatus("Cargando datos...");
      try {
        if (!currentProAchievements) {
          await loadProAchievements();
        }
        fillProAchievementsForm(currentProAchievements);
        openProAchievementsModal();
      } catch (error) {
        setProAchievementsModalStatus(error.message || "No se pudieron cargar tus logros profesionales.", true);
      }
    };

    const handleOpenLifeAchievementsModal = async () => {
      setLifeAchievementsModalStatus("Cargando datos...");
      try {
        if (!currentLifeAchievements) {
          await loadLifeAchievements();
        }
        fillLifeAchievementsForm(currentLifeAchievements);
        openLifeAchievementsModal();
      } catch (error) {
        setLifeAchievementsModalStatus(error.message || "No se pudieron cargar tus logros alcanzados.", true);
      }
    };

    const handleOpenQuotesModal = async () => {
      setQuotesModalStatus("Cargando datos...");
      try {
        if (!currentFavoriteQuotes) {
          await loadFavoriteQuotes();
        }
        fillQuotesForm(currentFavoriteQuotes);
        openQuotesModal();
      } catch (error) {
        setQuotesModalStatus(error.message || "No se pudieron cargar tus frases favoritas.", true);
      }
    };

    const handleOpenDistinctionsModal = async () => {
      if (!isViewerGuardian()) {
        setDistinctionsModalStatus("Esta sección solo puede ser actualizada por los Guardianes de Kiadez.com.", true);
        return;
      }

      setDistinctionsModalStatus("Cargando distinciones...");
      try {
        if (!currentDistinctions) {
          await loadDistinctions();
        }
        fillDistinctionsForm(currentDistinctions);
        openDistinctionsModal();
      } catch (error) {
        setDistinctionsModalStatus(error.message || "No se pudieron cargar las distinciones.", true);
      }
    };

    const handleSavePersonalInfo = async () => {
      setPersonalInfoModalStatus("Guardando...");
      try {
        const payload = buildPersonalInfoPayload();
        const res = await apiFetch("/biography/personal-info", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo guardar la información personal.");
        }
        currentPersonalInfo = data;
        applyPersonalInfoToView(data);
        closePersonalInfoModalFn();
      } catch (error) {
        setPersonalInfoModalStatus(error.message || "No se pudo guardar la información.", true);
      }
    };

    const handleSavePhysicalTraits = async () => {
      setPhysicalTraitsModalStatus("Guardando...");
      try {
        const payload = buildPhysicalTraitsPayload();
        const res = await apiFetch("/biography/physical-traits", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "No se pudieron guardar las características físicas.");
        }
        currentPhysicalTraits = data;
        applyPhysicalTraitsToView(data);
        closePhysicalTraitsModalFn();
      } catch (error) {
        setPhysicalTraitsModalStatus(error.message || "No se pudieron guardar los datos.", true);
      }
    };

    const handleSaveEducation = async () => {
      setEducationModalStatus("Guardando...");
      try {
        const payload = buildEducationPayload();
        const res = await apiFetch("/biography/education", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo guardar Educación.");
        }
        currentEducation = data;
        applyEducationToView(data);
        closeEducationModalFn();
      } catch (error) {
        setEducationModalStatus(error.message || "No se pudo guardar Educación.", true);
      }
    };

    const handleSaveCuriosities = async () => {
      setCuriositiesModalStatus("Guardando...");
      try {
        const payload = buildCuriositiesPayload();
        const res = await apiFetch("/biography/curiosities", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo guardar Curiosidades.");
        }
        currentCuriosities = data;
        applyCuriositiesToView(data);
        closeCuriositiesModalFn();
      } catch (error) {
        setCuriositiesModalStatus(error.message || "No se pudo guardar Curiosidades.", true);
      }
    };

    const handleSaveProfessionalInfo = async () => {
      setProfessionalInfoModalStatus("Guardando...");
      try {
        const payload = buildProfessionalInfoPayload();
        const res = await apiFetch("/biography/professional-info", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo guardar la información profesional.");
        }
        currentProfessionalInfo = data;
        applyProfessionalInfoToView(data);
        closeProfessionalInfoModalFn();
      } catch (error) {
        setProfessionalInfoModalStatus(error.message || "No se pudo guardar la información profesional.", true);
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
        setAboutModalStatus(`La biografía permite máximo ${ABOUT_MAX_WORDS} palabras.`, true);
        return;
      }

      setAboutModalStatus("Guardando...");
      try {
        const payload = buildAboutPayload();
        const res = await apiFetch("/biography/about", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo guardar tu biografía.");
        }
        currentAbout = data;
        applyAboutToView(data);
        closeAboutModalFn();
      } catch (error) {
        setAboutModalStatus(error.message || "No se pudo guardar tu biografía.", true);
      }
    };

    const handleSaveDream = async () => {
      updateDreamWordCounter();
      const totalWords = countWords(dreamTextInput?.value || "");
      if (totalWords > DREAM_MAX_WORDS) {
        setDreamModalStatus(`El mayor sueño permite máximo ${DREAM_MAX_WORDS} palabras.`, true);
        return;
      }

      setDreamModalStatus("Guardando...");
      try {
        const payload = buildDreamPayload();
        const res = await apiFetch("/biography/dream", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo guardar tu mayor sueño.");
        }
        currentDream = data;
        applyDreamToView(data);
        closeDreamModalFn();
      } catch (error) {
        setDreamModalStatus(error.message || "No se pudo guardar tu mayor sueño.", true);
      }
    };

    const handleSaveProAchievements = async () => {
      updateProAchievementsWordCounter();
      const totalWords = countWords(proAchievementsTextInput?.value || "");
      if (totalWords > PRO_ACHIEVEMENTS_MAX_WORDS) {
        setProAchievementsModalStatus(
          `Los logros profesionales permiten máximo ${PRO_ACHIEVEMENTS_MAX_WORDS} palabras.`,
          true
        );
        return;
      }

      setProAchievementsModalStatus("Guardando...");
      try {
        const payload = buildProAchievementsPayload();
        const res = await apiFetch("/biography/professional-achievements", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "No se pudieron guardar tus logros profesionales.");
        }
        currentProAchievements = data;
        applyProAchievementsToView(data);
        closeProAchievementsModalFn();
      } catch (error) {
        setProAchievementsModalStatus(error.message || "No se pudieron guardar tus logros profesionales.", true);
      }
    };

    const handleSaveLifeAchievements = async () => {
      updateLifeAchievementsWordCounter();
      const totalWords = countWords(lifeAchievementsTextInput?.value || "");
      if (totalWords > LIFE_ACHIEVEMENTS_MAX_WORDS) {
        setLifeAchievementsModalStatus(
          `Los logros alcanzados permiten máximo ${LIFE_ACHIEVEMENTS_MAX_WORDS} palabras.`,
          true
        );
        return;
      }

      setLifeAchievementsModalStatus("Guardando...");
      try {
        const payload = buildLifeAchievementsPayload();
        const res = await apiFetch("/biography/life-achievements", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "No se pudieron guardar tus logros alcanzados.");
        }
        currentLifeAchievements = data;
        applyLifeAchievementsToView(data);
        closeLifeAchievementsModalFn();
      } catch (error) {
        setLifeAchievementsModalStatus(error.message || "No se pudieron guardar tus logros alcanzados.", true);
      }
    };

    const handleSaveQuotes = async () => {
      updateQuotesWordCounter();
      const totalWords = countWords(quotesTextInput?.value || "");
      if (totalWords > FAVORITE_QUOTES_MAX_WORDS) {
        setQuotesModalStatus(
          `Las frases favoritas permiten máximo ${FAVORITE_QUOTES_MAX_WORDS} palabras.`,
          true
        );
        return;
      }

      setQuotesModalStatus("Guardando...");
      try {
        const payload = buildQuotesPayload();
        const res = await apiFetch("/biography/favorite-quotes", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "No se pudieron guardar tus frases favoritas.");
        }
        currentFavoriteQuotes = data;
        applyQuotesToView(data);
        closeQuotesModalFn();
      } catch (error) {
        setQuotesModalStatus(error.message || "No se pudieron guardar tus frases favoritas.", true);
      }
    };

    const handleSaveDistinctions = async () => {
      if (!isViewerGuardian()) {
        setDistinctionsModalStatus("Esta sección solo puede ser actualizada por los Guardianes de Kiadez.com.", true);
        return;
      }

      setDistinctionsModalStatus("Guardando...");
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
          throw new Error(data.detail || "No se pudieron guardar las distinciones.");
        }
        currentDistinctions = data;
        applyDistinctionsToView(data);
        closeDistinctionsModalFn();
      } catch (error) {
        setDistinctionsModalStatus(error.message || "No se pudieron guardar las distinciones.", true);
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
    bioPhotoSelectExisting?.addEventListener("click", handleOpenExisting);
    bioPhotoUpload?.addEventListener("click", handleUploadClick);
    bioPhotoFile?.addEventListener("change", handlePhotoFileChange);
    bioPhotoSelectCancel?.addEventListener("click", closePhotoSelectModal);
    bioPhotoSelectModal?.addEventListener("click", handleModalOverlayClick);
    emblemTrigger?.addEventListener("click", handleEmblemTriggerClick);
    emblemSelectExisting?.addEventListener("click", handleOpenExistingEmblem);
    emblemUpload?.addEventListener("click", handleEmblemUploadClick);
    emblemFile?.addEventListener("change", handleEmblemFileChange);
    emblemSelectGrid?.addEventListener("click", handleEmblemSelectGridClick);
    emblemSelectCancel?.addEventListener("click", closeEmblemSelectModal);
    emblemSelectModal?.addEventListener("click", handleEmblemModalOverlayClick);
    document.addEventListener("click", handlePageClick);
    ensureDistinctionsForm();
    applyDistinctionsEditorVisibility();

    void loadCurrentProfilePhoto();
    void loadCurrentEmblem();
    void loadPersonalInfo().catch((error) => {
      setPersonalInfoModalStatus(error.message || "No se pudo cargar la información personal.", true);
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
    void loadActivityStats().catch(() => {});
    void (async () => {
      try {
        await resolveBiographyProfileContext();
      } catch (error) {
        setDistinctionsModalStatus(error?.message || "No se pudo cargar el contexto del perfil.", true);
      }
      void loadDistinctions().catch((error) => {
        applyDistinctionsToView({ slots: [] });
        setDistinctionsModalStatus(error?.message || "No se pudieron cargar las distinciones.", true);
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
      bioPhotoSelectExisting?.removeEventListener("click", handleOpenExisting);
      bioPhotoUpload?.removeEventListener("click", handleUploadClick);
      bioPhotoFile?.removeEventListener("change", handlePhotoFileChange);
      bioPhotoSelectCancel?.removeEventListener("click", closePhotoSelectModal);
      bioPhotoSelectModal?.removeEventListener("click", handleModalOverlayClick);
      emblemTrigger?.removeEventListener("click", handleEmblemTriggerClick);
      emblemSelectExisting?.removeEventListener("click", handleOpenExistingEmblem);
      emblemUpload?.removeEventListener("click", handleEmblemUploadClick);
      emblemFile?.removeEventListener("change", handleEmblemFileChange);
      emblemSelectGrid?.removeEventListener("click", handleEmblemSelectGridClick);
      emblemSelectCancel?.removeEventListener("click", closeEmblemSelectModal);
      emblemSelectModal?.removeEventListener("click", handleEmblemModalOverlayClick);
      document.removeEventListener("click", handlePageClick);
    };
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Mi biografía</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-bio biography-background">
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
        <a class="topbar-btn" href="/home_user.html">🏠 Home</a>
        <a class="topbar-btn" href="/gallery.html">🖼️ Galería</a>
        <a class="topbar-btn" href="/my-public-whishes.html">🌐 Deseos públicos</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 Deseos privados</a>
        <a class="topbar-btn" href="/my-fulfilled-whises.html">✅ Deseos cumplidos</a>
      </div>

      <div class="feed-topbar-zone feed-topbar-right">
        <details class="topbar-dropdown" id="biographyProfileDropdown">
          <summary class="topbar-avatar-btn" aria-label="Perfil del usuario">
            <img src="/assets/avatar-default.jpg" alt="Perfil de Carlos Jiménez Duarte" />
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

        <details class="topbar-dropdown" id="biographyMenuDropdown">
          <summary class="topbar-menu-btn" aria-label="Abrir menú">
            <span class="topbar-menu-icon" aria-hidden="true">☰</span>
            <span class="topbar-menu-label">Menú</span>
          </summary>
          <div class="dropdown-menu" role="menu">
            <a href="/home_user.html" role="menuitem">Mi Home</a>
            <a href="/achievements.html" role="menuitem">Logros recientes</a>
            <a href="/gallery.html" role="menuitem">Galería</a>
            <a href="/calendar.html" role="menuitem">Calendario</a>
            <a href="/my-biography.html" role="menuitem">Mi Biografía</a>
          <a href="/messages.html" role="menuitem">Mensajes</a>
          </div>
        </details>
      </div>
    </header>

    <main class="user-home user-home--bio">

      <!-- PORTADA (MISMA DE HOME) -->
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

      <div class="biography-body">
      <!-- NAV (YA LO TIENES IGUAL) -->
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
          <span class="nav-icon">⭐</span>
          <span><strong id="biographyStarsTotal">0</strong> estrellas</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
        <a class="nav-pill" href="/messages.html" title="Mensajes">Mensajes</a>
      </nav>
      <!-- ======= CUERPO (3 columnas) ======= -->
      <section class="bio-shell">

        <section class="bio-grid">

          <!-- ========== IZQUIERDA: TOC ========== -->
          <aside class="bio-card bio-toc" aria-label="Tabla de contenidos">
            <h2 class="bio-side-title" id="tocUserName">Carlos Jiménez Duarte</h2>

            <ol class="bio-toc-list" id="tocList">
              <li><a href="#sec-about" data-toc="about">Carlos Jiménez Duarte</a></li>
              <li><a href="#sec-dream" data-toc="dream">Sobre su mayor sueño</a></li>
              <li><a href="#sec-pro" data-toc="pro">Logros profesionales</a></li>
              <li><a href="#sec-life" data-toc="life">Logros alcanzados</a></li>
              <li><a href="#sec-quotes" data-toc="quotes">Frases favoritas</a></li>
            </ol>

            <p class="bio-side-note">
              Esta tabla se sincroniza con tus títulos del centro.
            </p>
          </aside>

          <!-- ========== CENTRO: CONTENIDO ========== -->
          <section class="bio-center" aria-label="Biografía editable">

            <!-- Sección 1 -->
            <article class="bio-card bio-section bio-about-section" id="sec-about" data-section="about">
              <header class="bio-section-header">
                <h2 class="bio-section-title" id="aboutDisplayNameValue">Carlos Jiménez Duarte</h2>
                <button class="infobox-edit-btn bio-about-edit-btn" id="aboutEditBtn" type="button" title="Modificar biografía">
                  <img src="/css/icons/iconedit.webp" alt="Modificar biografía" />
                </button>
              </header>

              <div class="bio-about-view">
                <div id="aboutEmptyState">
                  <p class="bio-about-empty-message">
                    Todavía no has redactado tu biografía. ¿Qué esperas para hacerlo ahora?
                  </p>
                </div>
                <p class="bio-about-text hidden" id="aboutTextValue"></p>
              </div>
            </article>

            <!-- Sección 2 -->
            <article class="bio-card bio-section bio-dream-section" id="sec-dream" data-section="dream">
              <header class="bio-section-header">
                <h2 class="bio-section-title" id="dreamTitleValue">Sobre su mayor sueño</h2>
                <button class="infobox-edit-btn bio-about-edit-btn" id="dreamEditBtn" type="button" title="Modificar mayor sueño">
                  <img src="/css/icons/iconedit.webp" alt="Modificar mayor sueño" />
                </button>
              </header>

              <div class="bio-about-view">
                <div id="dreamEmptyState">
                  <p class="bio-about-empty-message">
                    Todavía no has descrito tu mayor sueño. ¿Te gustaría compartir con el mundo que es lo que palpita en tu corazón?
                  </p>
                </div>
                <p class="bio-about-text hidden" id="dreamTextValue"></p>
              </div>
            </article>

            <!-- Sección 3 -->
            <article class="bio-card bio-section bio-pro-achievements-section" id="sec-pro" data-section="pro">
              <header class="bio-section-header">
                <h2 class="bio-section-title" id="proAchievementsTitleValue">Logros profesionales</h2>
                <button class="infobox-edit-btn bio-about-edit-btn" id="proAchievementsEditBtn" type="button" title="Modificar logros profesionales">
                  <img src="/css/icons/iconedit.webp" alt="Modificar logros profesionales" />
                </button>
              </header>

              <div class="bio-about-view">
                <div id="proAchievementsEmptyState">
                  <p class="bio-about-empty-message">
                    ¿Cuáles son aquellos logros de los que más te han hecho sentir realizado en este mundo? Incluso lo más humilde es significativo.
                  </p>
                </div>
                <p class="bio-about-text hidden" id="proAchievementsTextValue"></p>
              </div>
            </article>

            <!-- Sección 4 -->
            <article class="bio-card bio-section bio-life-achievements-section" id="sec-life" data-section="life">
              <header class="bio-section-header">
                <h2 class="bio-section-title" id="lifeAchievementsTitleValue">Logros alcanzados</h2>
                <button class="infobox-edit-btn bio-about-edit-btn" id="lifeAchievementsEditBtn" type="button" title="Modificar logros alcanzados">
                  <img src="/css/icons/iconedit.webp" alt="Modificar logros alcanzados" />
                </button>
              </header>

              <div class="bio-about-view">
                <div id="lifeAchievementsEmptyState">
                  <p class="bio-about-empty-message">
                    ¿Qué es aquello tan significativo para ti cómo para ser considerado como parte de tu legado? ¿Cuáles son los meritos por los que te gustaría ser recordado? Deja tu constancia aquí.
                  </p>
                </div>
                <p class="bio-about-text hidden" id="lifeAchievementsTextValue"></p>
              </div>
            </article>

            <!-- Sección 5 -->
            <article class="bio-card bio-section bio-quotes-section" id="sec-quotes" data-section="quotes">
              <header class="bio-section-header">
                <h2 class="bio-section-title" id="quotesTitleValue">Frases favoritas</h2>
                <button class="infobox-edit-btn bio-about-edit-btn" id="quotesEditBtn" type="button" title="Modificar frases favoritas">
                  <img src="/css/icons/iconedit.webp" alt="Modificar frases favoritas" />
                </button>
              </header>

              <div class="bio-about-view">
                <div id="quotesEmptyState">
                  <p class="bio-about-empty-message">
                    ¡Esta es una oportunidad fantástica para dar constancia de tu filosofía de vida en las frases que más te gustan!
                  </p>
                </div>
                <p class="bio-about-text hidden" id="quotesTextValue"></p>
              </div>
            </article>

          </section>

          <!-- ========== DERECHA: INFOBOX ========== -->
          <aside class="bio-card bio-infobox" aria-label="Ficha del usuario">

            <div class="infobox-head">
              <h2 class="infobox-title" id="infoName">Carlos Jiménez</h2>
            </div>

            <figure class="infobox-photo">
              <div class="infobox-photo-wrap">
                <button class="infobox-photo-trigger" id="profilePhotoTrigger" type="button"
                  title="Gestionar imágenes de galería">
                  <img id="profilePhoto" src="/css/logo-kiadez.webp" alt="Foto del usuario" />
                </button>

                <div class="infobox-photo-menu hidden" id="profilePhotoMenu">
                  <button type="button" id="bioPhotoSelectExisting">Abrir galería</button>
                  <button type="button" id="bioPhotoUpload">Subir a galería</button>
                </div>

                <input id="bioPhotoFile" type="file" accept="image/*" class="hidden" />
              </div>
              <figcaption id="photoCaption">Jiménez en 2025.</figcaption>
            </figure>
            <p class="infobox-photo-status" id="bioPhotoStatus" aria-live="polite"></p>

            <!-- Sección -->
            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">Información personal</span>
                <button class="infobox-edit-btn" id="personalInfoEditBtn" type="button" title="Editar información personal">
                  <img src="/css/icons/iconedit.webp" alt="Editar información personal" />
                </button>
              </div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="birthname">
                  <th>Nombre de nacimiento</th>
                  <td><span id="personalInfoBirthNameValue">Carlos Jiménez Duarte</span></td>
                </tr>
                <tr data-field="birth">
                  <th>Nacimiento</th>
                  <td><span id="personalInfoBirthValue">5 de mayo de 1986 (39 años); Barrancabermeja, Santander, Colombia</span></td>
                </tr>
                <tr data-field="residence">
                  <th>Residencia</th>
                  <td><span id="personalInfoResidenceValue">Medellín, Antioquia</span></td>
                </tr>
                <tr data-field="nationality">
                  <th>Nacionalidad</th>
                  <td><span id="personalInfoNationalityValue">Colombiana</span></td>
                </tr>
                <tr data-field="lang">
                  <th>Lengua materna</th>
                  <td><span id="personalInfoNativeLanguageValue">Español</span></td>
                </tr>
                <tr data-field="pseudonyms">
                  <th>Seudónimos</th>
                  <td><span id="personalInfoPseudonymsValue">Melquíades, Kiadez, Saint Martin</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">Características físicas</span>
                <button class="infobox-edit-btn" id="physicalTraitsEditBtn" type="button" title="Editar características físicas">
                  <img src="/css/icons/iconedit.webp" alt="Editar características físicas" />
                </button>
              </div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="height">
                  <th>Altura</th>
                  <td><span id="physicalTraitsHeightValue">1,80 m</span></td>
                </tr>
                <tr data-field="weight">
                  <th>Peso</th>
                  <td><span id="physicalTraitsWeightValue">76 kg</span></td>
                </tr>
                <tr data-field="eyes">
                  <th>Ojos</th>
                  <td><span id="physicalTraitsEyesValue">Castaño</span></td>
                </tr>
                <tr data-field="hair">
                  <th>Cabello</th>
                  <td><span id="physicalTraitsHairValue">Castaño</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">Educación</span>
                <button class="infobox-edit-btn" id="educationEditBtn" type="button" title="Editar educación">
                  <img src="/css/icons/iconedit.webp" alt="Editar educación" />
                </button>
              </div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="education">
                  <th>Educado en</th>
                  <td>
                    <div class="education-slots">
                      <div class="education-slot" id="educationSlot1Value">Colegio Calasanz</div>
                      <div class="education-slot" id="educationSlot2Value">Universidad Pontificia Bolivariana</div>
                      <div class="education-slot" id="educationSlot3Value">Politécnico Grancolombiano</div>
                      <div class="education-slot" id="educationSlot4Value"></div>
                    </div>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">Información profesional</span>
                <button class="infobox-edit-btn" id="professionalInfoEditBtn" type="button" title="Editar información profesional">
                  <img src="/css/icons/iconedit.webp" alt="Editar información profesional" />
                </button>
              </div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="occupation">
                  <th>Ocupación</th>
                  <td><span id="professionalOccupationValue">Escritor, Ingeniero de Software, Artista Plástico Aficionado</span></td>
                </tr>
                <tr data-field="active">
                  <th>Años activo</th>
                  <td><span id="professionalActiveYearsValue">2003 — presente</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">Distinciones</span>
                <button class="infobox-edit-btn hidden" id="distinctionsEditBtn" type="button" title="Editar distinciones">
                  <img src="/css/icons/iconedit.webp" alt="Editar distinciones" />
                </button>
              </div>
              <p class="infobox-guardian-note">
                Esta sección solo puede ser actualizada por los Guardianes de Kiadez.com.
              </p>
              <table class="infobox-table">
                <tbody id="distinctionsRows"></tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title is-editable">
                <span class="infobox-section-title-text">Curiosidades</span>
                <button class="infobox-edit-btn" id="curiositiesEditBtn" type="button" title="Editar curiosidades">
                  <img src="/css/icons/iconedit.webp" alt="Editar curiosidades" />
                </button>
              </div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="hero">
                  <th>Superhéroe favorito</th>
                  <td><span id="curiositiesHeroValue">Batman</span></td>
                </tr>
                <tr data-field="song">
                  <th>Canción favorita</th>
                  <td><span id="curiositiesSongValue">Dreamer — Ozzy Osbourne</span></td>
                </tr>
                <tr data-field="food">
                  <th>Comida favorita</th>
                  <td><span id="curiositiesFoodValue">Comida mexicana</span></td>
                </tr>
                <tr data-field="games">
                  <th>Videojuegos</th>
                  <td><span id="curiositiesGamesValue">Dofus, Prince of Persia 2, Batman Arkham Knight</span></td>
                </tr>
                <tr data-field="book">
                  <th>Libro favorito</th>
                  <td><span id="curiositiesBookValue">Las Mil y Una Noches</span></td>
                </tr>
                <tr data-field="hobbies">
                  <th>Otros pasatiempos</th>
                  <td><span id="curiositiesHobbiesValue">Sacar a Willow a paseo, reír, ver series, soñar en grande</span></td>
                </tr>
                <tr data-field="motto">
                  <th>Lema</th>
                  <td><span id="curiositiesMottoValue">A Dios sea la gloria</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">Actividad en Kiadez.com</div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="wishes_done">
                  <th>Deseos cumplidos</th>
                  <td><span data-value>20</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span>
                  </td>
                </tr>
                <tr data-field="wishes_granted">
                  <th>Deseos concedidos</th>
                  <td><span id="wishesGrantedValue" data-value>0</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span>
                  </td>
                </tr>
                <tr data-field="rank">
                  <th>Rango</th>
                  <td><span data-value>Guardián Rango 3</span><span class="infobox-hidden" data-hidden hidden>Prefiero
                      no
                      decirlo</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">Emblema</div>
              <div class="infobox-emblem">
                <div class="infobox-photo-wrap infobox-emblem-wrap">
                  <button class="infobox-photo-trigger infobox-emblem-trigger" id="emblemTrigger" type="button" title="Gestionar emblema">
                    <img id="emblemImage" src="/css/logo-kiadez.webp" alt="Emblema" />
                  </button>
                  <div class="infobox-photo-menu hidden" id="emblemMenu">
                    <button type="button" id="emblemSelectExisting">Seleccionar imagen</button>
                    <button type="button" id="emblemUpload">Subir imagen</button>
                  </div>
                  <input id="emblemFile" type="file" accept="image/*" class="hidden" />
                </div>
              </div>
              <p class="infobox-photo-status" id="emblemStatus" aria-live="polite"></p>
            </div>

            <!-- Panel de privacidad (aparece en modo edición) -->
            <div class="infobox-privacy-panel" id="privacyPanel" hidden>
              <p class="bio-side-note" style="margin:0 0 10px;">
                Activa/desactiva qué campos aparecen públicos. Si lo apagas, se muestra “Prefiero no decirlo”.
              </p>
              <div class="privacy-grid" id="privacyGrid"></div>
            </div>

          </aside>

        </section>

      </section>
      </div>

    </main>

    <div class="modal-overlay hidden" id="bioPhotoSelectModal" aria-hidden="true">
      <div class="modal wish-modal cover-select-modal" role="dialog" aria-modal="true"
        aria-label="Seleccionar imagen de perfil">
        <div class="modal-head">
          <h3>Seleccionar imagen</h3>
        </div>
        <div class="modal-body">
          <div class="cover-select-grid" id="bioPhotoSelectGrid"></div>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="bioPhotoSelectCancel">Cancelar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="emblemSelectModal" aria-hidden="true">
      <div class="modal wish-modal cover-select-modal" role="dialog" aria-modal="true"
        aria-label="Seleccionar emblema">
        <div class="modal-head">
          <h3>Seleccionar imagen</h3>
        </div>
        <div class="modal-body">
          <div class="cover-select-grid" id="emblemSelectGrid"></div>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="emblemSelectCancel">Cancelar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="aboutModalOverlay" aria-hidden="true">
      <div class="modal about-modal" role="dialog" aria-modal="true" aria-label="Editar biografía">
        <div class="modal-head">
          <h3>Editar biografía</h3>
          <button class="modal-close" type="button" id="closeAboutModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="about-modal-name">
            <label class="modal-label" for="aboutDisplayNameInput">Nombre público</label>
            <input class="modal-input about-modal-name-input" id="aboutDisplayNameInput" type="text" maxlength="200" />
          </div>

          <p class="bio-prompt about-modal-prompt">
            Describe quién eres. Se sugiere hacerlo en tercera persona. Aprovecha este espacio: es tu Wikipedia personal.
            Lo que escribas aquí será lo mismo que podrían leer tus seres queridos dentro de 100 años.
          </p>

          <div class="about-modal-editor">
            <textarea class="bio-textarea about-modal-textarea" id="aboutTextInput" placeholder="Escribe aquí..."></textarea>
            <div class="bio-meta">
              <span id="aboutWordCounter">0 / 1200 palabras</span>
            </div>
          </div>

          <p class="infobox-photo-status" id="aboutModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelAboutModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveAboutBtn">Guardar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="dreamModalOverlay" aria-hidden="true">
      <div class="modal about-modal dream-modal" role="dialog" aria-modal="true" aria-label="Editar mayor sueño">
        <div class="modal-head">
          <h3>Editar mayor sueño</h3>
          <button class="modal-close" type="button" id="closeDreamModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="about-modal-name">
            <label class="modal-label" for="dreamTitleInput">Título de sección</label>
            <input class="modal-input about-modal-name-input" id="dreamTitleInput" type="text" maxlength="200" />
          </div>

          <p class="bio-prompt about-modal-prompt">
            Describe aquí cuál es ese sueño que te gustaría ver realidad: aquello que, contra todo pronóstico, te gustaría ver realizado. O, si lo sientes, lo que te gustaría alcanzar en una nueva vida. Simplemente sueña y cree.
          </p>

          <div class="about-modal-editor">
            <textarea class="bio-textarea about-modal-textarea" id="dreamTextInput" placeholder="Escribe aquí..."></textarea>
            <div class="bio-meta">
              <span id="dreamWordCounter">0 / 1200 palabras</span>
            </div>
          </div>

          <p class="infobox-photo-status" id="dreamModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelDreamModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveDreamBtn">Guardar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="proAchievementsModalOverlay" aria-hidden="true">
      <div class="modal about-modal pro-achievements-modal" role="dialog" aria-modal="true" aria-label="Editar logros profesionales">
        <div class="modal-head">
          <h3>Editar logros profesionales</h3>
          <button class="modal-close" type="button" id="closeProAchievementsModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="about-modal-name">
            <label class="modal-label" for="proAchievementsTitleInput">Título de sección</label>
            <input class="modal-input about-modal-name-input" id="proAchievementsTitleInput" type="text" maxlength="200" />
          </div>

          <p class="bio-prompt about-modal-prompt">
            Describe aquí los logros personales o académicos más importantes que consideras has conseguido hasta ahora.
            Esto te servirá como tu propia versión de LinkedIn. (Recomendado en viñetas.)
          </p>

          <div class="about-modal-editor">
            <textarea class="bio-textarea about-modal-textarea" id="proAchievementsTextInput" placeholder="Escribe aquí..."></textarea>
            <div class="bio-meta">
              <span id="proAchievementsWordCounter">0 / 500 palabras</span>
            </div>
          </div>

          <p class="infobox-photo-status" id="proAchievementsModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelProAchievementsModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveProAchievementsBtn">Guardar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="lifeAchievementsModalOverlay" aria-hidden="true">
      <div class="modal about-modal life-achievements-modal" role="dialog" aria-modal="true" aria-label="Editar logros alcanzados">
        <div class="modal-head">
          <h3>Editar logros alcanzados</h3>
          <button class="modal-close" type="button" id="closeLifeAchievementsModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="about-modal-name">
            <label class="modal-label" for="lifeAchievementsTitleInput">Título de sección</label>
            <input class="modal-input about-modal-name-input" id="lifeAchievementsTitleInput" type="text" maxlength="200" />
          </div>

          <p class="bio-prompt about-modal-prompt">
            Describe aquí los logros personales que te hacen sentir orgulloso; aquello que sabes define tu existencia.
            (Recomendado en viñetas.)
          </p>

          <div class="about-modal-editor">
            <textarea class="bio-textarea about-modal-textarea" id="lifeAchievementsTextInput" placeholder="Escribe aquí..."></textarea>
            <div class="bio-meta">
              <span id="lifeAchievementsWordCounter">0 / 500 palabras</span>
            </div>
          </div>

          <p class="infobox-photo-status" id="lifeAchievementsModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelLifeAchievementsModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveLifeAchievementsBtn">Guardar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="quotesModalOverlay" aria-hidden="true">
      <div class="modal about-modal quotes-modal" role="dialog" aria-modal="true" aria-label="Editar frases favoritas">
        <div class="modal-head">
          <h3>Editar frases favoritas</h3>
          <button class="modal-close" type="button" id="closeQuotesModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="about-modal-name">
            <label class="modal-label" for="quotesTitleInput">Título de sección</label>
            <input class="modal-input about-modal-name-input" id="quotesTitleInput" type="text" maxlength="200" />
          </div>

          <p class="bio-prompt about-modal-prompt">
            Describe tu filosofía de vida en 3 o 4 frases. Cuando ya no estés en este mundo, las personas
            podrían recordarte por estas banderas personales.
          </p>

          <div class="about-modal-editor">
            <textarea class="bio-textarea about-modal-textarea" id="quotesTextInput" placeholder="Escribe aquí..."></textarea>
            <div class="bio-meta">
              <span id="quotesWordCounter">0 / 500 palabras</span>
            </div>
          </div>

          <p class="infobox-photo-status" id="quotesModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelQuotesModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveQuotesBtn">Guardar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="distinctionsModalOverlay" aria-hidden="true">
      <div class="modal about-modal distinctions-modal" role="dialog" aria-modal="true" aria-label="Editar distinciones">
        <div class="modal-head">
          <h3>Editar distinciones</h3>
          <button class="modal-close" type="button" id="closeDistinctionsModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="distinctions-grid" id="distinctionsForm"></div>
          <p class="infobox-photo-status" id="distinctionsModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelDistinctionsModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveDistinctionsBtn">Guardar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="personalInfoModalOverlay" aria-hidden="true">
      <div class="modal personal-info-modal" role="dialog" aria-modal="true" aria-label="Editar información personal">
        <div class="modal-head">
          <h3>Editar información personal</h3>
          <button class="modal-close" type="button" id="closePersonalInfoModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="personal-info-grid">
            <div class="personal-info-col">
              <div class="personal-info-field">
                <label class="modal-label" for="personalBirthNameInput">Nombre de nacimiento</label>
                <input class="modal-input" id="personalBirthNameInput" type="text" maxlength="200" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalBirthDateInput">Nacimiento</label>
                <input class="modal-input" id="personalBirthDateInput" type="date" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalBirthCityInput">Ciudad de nacimiento</label>
                <input class="modal-input" id="personalBirthCityInput" type="text" maxlength="120" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalBirthRegionInput">Región / Estado de nacimiento</label>
                <input class="modal-input" id="personalBirthRegionInput" type="text" maxlength="120" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalBirthCountryInput">País de nacimiento</label>
                <input class="modal-input" id="personalBirthCountryInput" type="text" maxlength="120" />
              </div>
            </div>

            <div class="personal-info-col">
              <div class="personal-info-field">
                <label class="modal-label" for="personalResidenceInput">Residencia</label>
                <input class="modal-input" id="personalResidenceInput" type="text" maxlength="255" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalNationalityInput">Nacionalidad</label>
                <input class="modal-input" id="personalNationalityInput" type="text" maxlength="120" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalNativeLanguageInput">Lengua materna</label>
                <input class="modal-input" id="personalNativeLanguageInput" type="text" maxlength="120" />
              </div>

              <div class="personal-info-field">
                <label class="modal-label" for="personalPseudonymsInput">Seudónimos</label>
                <input class="modal-input" id="personalPseudonymsInput" type="text" maxlength="300" />
              </div>
            </div>
          </div>

          <p class="infobox-photo-status" id="personalInfoModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelPersonalInfoModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="savePersonalInfoBtn">Guardar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="physicalTraitsModalOverlay" aria-hidden="true">
      <div class="modal physical-traits-modal" role="dialog" aria-modal="true" aria-label="Editar características físicas">
        <div class="modal-head">
          <h3>Editar características físicas</h3>
          <button class="modal-close" type="button" id="closePhysicalTraitsModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="physical-traits-grid">
            <div class="physical-traits-col">
              <div class="physical-traits-field">
                <label class="modal-label" for="physicalHeightInput">Altura</label>
                <input class="modal-input" id="physicalHeightInput" type="text" maxlength="40" placeholder="Ej: 1,80 m" />
              </div>

              <div class="physical-traits-field">
                <label class="modal-label" for="physicalWeightInput">Peso</label>
                <input class="modal-input" id="physicalWeightInput" type="text" maxlength="40" placeholder="Ej: 76 kg" />
              </div>
            </div>

            <div class="physical-traits-col">
              <div class="physical-traits-field">
                <label class="modal-label" for="physicalEyesInput">Ojos</label>
                <input class="modal-input" id="physicalEyesInput" type="text" maxlength="80" placeholder="Ej: Castaño" />
              </div>

              <div class="physical-traits-field">
                <label class="modal-label" for="physicalHairInput">Cabello</label>
                <input class="modal-input" id="physicalHairInput" type="text" maxlength="80" placeholder="Ej: Castaño" />
              </div>
            </div>
          </div>

          <p class="infobox-photo-status" id="physicalTraitsModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelPhysicalTraitsModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="savePhysicalTraitsBtn">Guardar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="educationModalOverlay" aria-hidden="true">
      <div class="modal education-modal" role="dialog" aria-modal="true" aria-label="Editar educación">
        <div class="modal-head">
          <h3>Editar educación</h3>
          <button class="modal-close" type="button" id="closeEducationModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="education-grid">
            <div class="education-col">
              <div class="education-field">
                <label class="modal-label" for="educationSlot1Input">Institución académica 1</label>
                <input class="modal-input" id="educationSlot1Input" type="text" maxlength="255" placeholder="Ej: Colegio..." />
              </div>
              <div class="education-field">
                <label class="modal-label" for="educationSlot2Input">Institución académica 2</label>
                <input class="modal-input" id="educationSlot2Input" type="text" maxlength="255" placeholder="Ej: Universidad..." />
              </div>
            </div>
            <div class="education-col">
              <div class="education-field">
                <label class="modal-label" for="educationSlot3Input">Institución académica 3</label>
                <input class="modal-input" id="educationSlot3Input" type="text" maxlength="255" placeholder="Ej: Instituto..." />
              </div>
              <div class="education-field">
                <label class="modal-label" for="educationSlot4Input">Institución académica 4</label>
                <input class="modal-input" id="educationSlot4Input" type="text" maxlength="255" placeholder="Ej: Academia..." />
              </div>
            </div>
          </div>

          <p class="infobox-photo-status" id="educationModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelEducationModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveEducationBtn">Guardar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="curiositiesModalOverlay" aria-hidden="true">
      <div class="modal curiosities-modal" role="dialog" aria-modal="true" aria-label="Editar curiosidades">
        <div class="modal-head">
          <h3>Editar curiosidades</h3>
          <button class="modal-close" type="button" id="closeCuriositiesModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="curiosities-grid">
            <div class="curiosities-col">
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityHeroInput">Superhéroe favorito</label>
                <input class="modal-input" id="curiosityHeroInput" type="text" maxlength="120" />
              </div>
              <div class="curiosities-field">
                <label class="modal-label" for="curiositySongInput">Canción favorita</label>
                <input class="modal-input" id="curiositySongInput" type="text" maxlength="255" />
              </div>
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityFoodInput">Comida favorita</label>
                <input class="modal-input" id="curiosityFoodInput" type="text" maxlength="160" />
              </div>
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityGamesInput">Videojuegos</label>
                <input class="modal-input" id="curiosityGamesInput" type="text" maxlength="500" />
              </div>
            </div>
            <div class="curiosities-col">
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityBookInput">Libro favorito</label>
                <input class="modal-input" id="curiosityBookInput" type="text" maxlength="255" />
              </div>
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityHobbiesInput">Otros pasatiempos</label>
                <input class="modal-input" id="curiosityHobbiesInput" type="text" maxlength="500" />
              </div>
              <div class="curiosities-field">
                <label class="modal-label" for="curiosityMottoInput">Lema</label>
                <input class="modal-input" id="curiosityMottoInput" type="text" maxlength="255" />
              </div>
            </div>
          </div>
          <p class="infobox-photo-status" id="curiositiesModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelCuriositiesModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveCuriositiesBtn">Guardar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="professionalInfoModalOverlay" aria-hidden="true">
      <div class="modal professional-info-modal" role="dialog" aria-modal="true" aria-label="Editar información profesional">
        <div class="modal-head">
          <h3>Editar información profesional</h3>
          <button class="modal-close" type="button" id="closeProfessionalInfoModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="professional-info-grid">
            <div class="professional-info-field">
              <label class="modal-label" for="professionalOccupationInput">Ocupación</label>
              <input class="modal-input" id="professionalOccupationInput" type="text" maxlength="500" />
            </div>
            <div class="professional-info-field">
              <label class="modal-label" for="professionalActiveYearsInput">Años activo</label>
              <input class="modal-input" id="professionalActiveYearsInput" type="text" maxlength="120" />
            </div>
          </div>
          <p class="infobox-photo-status" id="professionalInfoModalStatus" aria-live="polite"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="cancelProfessionalInfoModal">Cancelar</button>
          <button class="btn btn-primary btn-compact" type="button" id="saveProfessionalInfoBtn">Guardar</button>
        </div>
      </div>
    </div>

      <!-- FOOTER reutilizado -->
      <footer class="kiadez-footer">
        <div class="footer-main">

          <div class="footer-column footer-origin">
            <p class="footer-poem">
              Kiadez fue llamado por una estrella a subir el Monte Manjaro.<br>
              No para dominar, sino para orientar.<br>
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
