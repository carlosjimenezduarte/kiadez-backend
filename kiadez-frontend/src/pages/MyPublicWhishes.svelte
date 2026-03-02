<script>
  import { onMount } from "svelte";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";
  import { getDekSessionHex, setDekSessionHex } from "../lib/dekSession";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { logout } from "../lib/logout";
  import { syncProfileStarsTotal } from "../lib/starsCounter";

  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

  onMount(() => {
    document.body.dataset.visitor = "false";
    void syncProfileStarsTotal("myPublicWishesStarsTotal");
    initPurposeCoverModule();

    const prefixInputs = document.querySelectorAll(".wish-prefix-input");
    const suffixInputs = document.querySelectorAll("[data-suffix]");

    prefixInputs.forEach((input) => {
      const prefix = input.dataset.prefix || tr("Deseo ", "Wish ", "Souhait ");
      const counterId = input.dataset.counter;
      const counterEl = counterId ? document.getElementById(counterId) : null;
      const maxLength = input.maxLength > 0 ? input.maxLength : null;

      const clampToMax = () => {
        if (maxLength && input.value.length > maxLength) {
          input.value = input.value.slice(0, maxLength);
        }
      };

      const updateCounter = () => {
        if (!counterEl) return;
        const current = input.value.length;
        const limit = maxLength || current;
        counterEl.textContent = `${current}/${limit}`;
      };

      if (!input.value.startsWith(prefix)) {
        input.value = `${prefix}${input.value}`;
      }
      clampToMax();
      updateCounter();

      const ensurePrefix = () => {
        if (!input.value.startsWith(prefix)) {
          const cleaned = input.value.replace(prefix, "");
          input.value = `${prefix}${cleaned}`;
        }
        if (input.value.length < prefix.length) {
          input.value = prefix;
        }
        clampToMax();
        updateCounter();
      };

      input.addEventListener("input", ensurePrefix);

      input.addEventListener("keydown", (event) => {
        const cursorStart = input.selectionStart || 0;
        if ((event.key === "Backspace" || event.key === "Delete") && cursorStart <= prefix.length) {
          event.preventDefault();
          input.setSelectionRange(prefix.length, prefix.length);
        }
      });
    });

    suffixInputs.forEach((input) => {
      const suffix = input.dataset.suffix || "";
      if (!suffix) return;

      const normalizeSuffix = () => {
        const current = input.value || "";
        const suffixIndex = current.indexOf(suffix);
        if (suffixIndex === -1) {
          input.value = `${current}${suffix}`;
          return;
        }
        const editablePart = current.slice(0, suffixIndex);
        input.value = `${editablePart}${suffix}`;
      };

      const clampCaret = () => {
        const current = input.value || "";
        const suffixIndex = current.indexOf(suffix);
        if (suffixIndex === -1) return;
        const maxPos = suffixIndex;
        const cursorStart = input.selectionStart ?? 0;
        const cursorEnd = input.selectionEnd ?? 0;
        if (cursorStart > maxPos || cursorEnd > maxPos) {
          input.setSelectionRange(maxPos, maxPos);
        }
      };

      normalizeSuffix();

      input.addEventListener("input", () => {
        normalizeSuffix();
        clampCaret();
      });

      input.addEventListener("keydown", (event) => {
        const current = input.value || "";
        const suffixIndex = current.indexOf(suffix);
        if (suffixIndex === -1) return;
        const maxPos = suffixIndex;
        const cursorStart = input.selectionStart ?? 0;
        const cursorEnd = input.selectionEnd ?? 0;

        if ((event.key === "Backspace" || event.key === "Delete") && cursorStart >= maxPos) {
          event.preventDefault();
          input.setSelectionRange(maxPos, maxPos);
        }

        if (cursorEnd > maxPos) {
          event.preventDefault();
          input.setSelectionRange(maxPos, maxPos);
        }
      });

      input.addEventListener("click", clampCaret);
      input.addEventListener("focus", clampCaret);
      input.addEventListener("mouseup", clampCaret);
    });

    const lampSlotTemplate = document.getElementById("wishLampSlotTemplate");
    const choiceInlineTemplate = document.getElementById("wishChoiceInlineTemplate");
    const personalWishList = document.getElementById("personalWishList");
    const personalWishAdd = document.getElementById("personalWishAdd");
    const personalWishCount = document.getElementById("personalWishCount");
    const cooperativeWishList = document.getElementById("cooperativeWishList");
    const cooperativeWishAdd = document.getElementById("cooperativeWishAdd");
    const cooperativeWishCountLabel = document.getElementById("cooperativeWishCountLabel");
    const personalWishModal = document.getElementById("personalWishModal");
    const closePersonalWishModal = document.getElementById("closePersonalWishModal");
    const cooperativeWishModal = document.getElementById("cooperativeWishModal");
    const closeCooperativeWishModal = document.getElementById("closeCooperativeWishModal");
    const deleteWishModal = document.getElementById("deleteWishModal");
    const confirmDeleteWish = document.getElementById("confirmDeleteWish");
    const cancelDeleteWish = document.getElementById("cancelDeleteWish");
    const fulfillWishModal = document.getElementById("fulfillWishModal");
    const cancelFulfillWish = document.getElementById("cancelFulfillWish");
    const confirmFulfillWish = document.getElementById("confirmFulfillWish");
    const fulfillEvidence = document.getElementById("fulfillEvidence");
    const fulfillEvidencePreview = document.getElementById("fulfillEvidencePreview");
    const cooperativeWishTypeIcon = document.getElementById("cooperativeWishTypeIcon");
    const cooperativeWishTypeInputs = document.querySelectorAll('input[name="cooperativeWishType"]');
    const cooperativeWishTypeHint = document.getElementById("cooperativeWishTypeHint");
    const cooperativeWishMedia = document.getElementById("cooperativeWishMedia");
    const cooperativeWishPreview = document.getElementById("cooperativeWishPreview");
    const cooperativeWishFileName = document.getElementById("cooperativeWishFileName");
    const cooperativeWishTemplate = document.getElementById("cooperativeWishTemplate");
    const cooperativeWishText = document.getElementById("cooperativeWishText");
    const cooperativeWishCount = document.getElementById("cooperativeWishCount");
    const cooperativeWishSecurityCode = document.getElementById("cooperativeWishSecurityCode");
    const cooperativeWishError = document.getElementById("cooperativeWishError");
    const disableLegacyPurposeCover = true;
    const getLegacyElement = (id) => (disableLegacyPurposeCover ? null : document.getElementById(id));
    const getLegacyQuery = (selector) => (disableLegacyPurposeCover ? null : document.querySelector(selector));
    const getLegacyQueryAll = (selector) => (disableLegacyPurposeCover ? [] : document.querySelectorAll(selector));
    const coverMedia = getLegacyElement("coverMedia");
    const coverImg = getLegacyElement("coverImg");
    const coverFile = getLegacyElement("coverFile");
    const coverChangeBtn = getLegacyElement("btnChangeCover");
    const coverUploadBtn = getLegacyElement("coverUpload");
    const coverMoveBtn = getLegacyElement("coverMove");
    const coverMenu = getLegacyQuery(".cover-menu");
    const coverSaveActions = getLegacyElement("coverSaveActions");
    const coverSaveBtn = getLegacyElement("coverSaveBtn");
    const coverCancelBtn = getLegacyElement("coverCancelBtn");
    const btnEditPurposes = getLegacyElement("btnEditPurposes");
    const lifeProposalOverlay = getLegacyElement("lifeProposalOverlay");
    const lifeProposalClose = getLegacyElement("lifeProposalClose");
    const lifeProposalCloseFooter = getLegacyElement("lifeProposalCloseFooter");
    const lifeConfirmOverlay = getLegacyElement("lifeConfirmOverlay");
    const lifeConfirmClose = getLegacyElement("lifeConfirmClose");
    const lifeConfirmCancel = getLegacyElement("lifeConfirmCancel");
    const lifeConfirmOk = getLegacyElement("lifeConfirmOk");
    const lifeConfirmText = getLegacyElement("lifeConfirmText");
    const purpose1 = getLegacyElement("purpose1");
    const purpose2 = getLegacyElement("purpose2");
    const purpose3 = getLegacyElement("purpose3");
    const purposeUnlock1 = getLegacyElement("purposeUnlock1");
    const purposeUnlock2 = getLegacyElement("purposeUnlock2");
    const purposeUnlock3 = getLegacyElement("purposeUnlock3");
    const purposeUnlockOverlay = getLegacyElement("purposeUnlockOverlay");
    const purposeUnlockClose = getLegacyElement("purposeUnlockClose");
    const purposeUnlockCancel = getLegacyElement("purposeUnlockCancel");
    const purposeUnlockConfirm = getLegacyElement("purposeUnlockConfirm");
    const purposeUnlockPassword = getLegacyElement("purposeUnlockPassword");
    const purposeUnlockError = getLegacyElement("purposeUnlockError");
    const purposeUnlockText = getLegacyElement("purposeUnlockText");
    const purposeFulfillBtns = getLegacyQueryAll(".purpose-fulfill-btn");
    const confirmCooperativeWish = document.getElementById("confirmCooperativeWish");
    const icanConfirmModal = document.getElementById("icanConfirmModal");
    const icanConfirmYes = document.getElementById("icanConfirmYes");
    const icanConfirmNo = document.getElementById("icanConfirmNo");
    const guardianContactModal = document.getElementById("guardianContactModal");
    const cancelGuardianModal = document.getElementById("cancelGuardianModal");
    const guardianSelect = document.getElementById("guardianSelect");
    const guardianPrevPage = document.getElementById("guardianPrevPage");
    const guardianNextPage = document.getElementById("guardianNextPage");
    const guardianPageLabel = document.getElementById("guardianPageLabel");
    const guardianStatus = document.getElementById("guardianStatus");
    const guardianReasonVisitor = document.getElementById("guardianReasonVisitor");
    const guardianReasonError = document.getElementById("guardianReasonError");
    const guardianPhoneVisitor = document.getElementById("guardianPhoneVisitor");
    const guardianPhoneError = document.getElementById("guardianPhoneError");
    const guardianEmailVisitor = document.getElementById("guardianEmailVisitor");
    const guardianEmailError = document.getElementById("guardianEmailError");
    const guardianEvidenceRow = document.getElementById("guardianEvidenceRow");
    const guardianEvidenceInput = document.getElementById("guardianEvidenceVisitor");
    const guardianEvidencePreview = document.getElementById("guardianEvidencePreview");
    const guardianEvidenceThumb = document.getElementById("guardianEvidenceThumb");
    const guardianEvidenceName = document.getElementById("guardianEvidenceName");
    const guardianEvidenceError = document.getElementById("guardianEvidenceError");
    const guardianSendBtn = document.getElementById("guardianSendBtn");
    const guardianRequestContext = document.getElementById("guardianRequestContext");
    const freezeWishConfirmModal = document.getElementById("freezeWishConfirmModal");
    const freezeWishConfirmYes = document.getElementById("freezeWishConfirmYes");
    const freezeWishConfirmNo = document.getElementById("freezeWishConfirmNo");
    const unfreezeWishReasonModal = document.getElementById("unfreezeWishReasonModal");
    const unfreezeReasonModalClose = document.getElementById("unfreezeReasonModalClose");
    const unfreezeReasonErrorBtn = document.getElementById("unfreezeReasonErrorBtn");
    const unfreezeReasonUnexpectedBtn = document.getElementById("unfreezeReasonUnexpectedBtn");
    const unfreezeReasonCancel = document.getElementById("unfreezeReasonCancel");
    const unfreezeWishUnexpectedModal = document.getElementById("unfreezeWishUnexpectedModal");
    const unfreezeUnexpectedModalClose = document.getElementById("unfreezeUnexpectedModalClose");
    const unfreezeUnexpectedText = document.getElementById("unfreezeUnexpectedText");
    const unfreezeUnexpectedWordCount = document.getElementById("unfreezeUnexpectedWordCount");
    const unfreezeUnexpectedError = document.getElementById("unfreezeUnexpectedError");
    const unfreezeUnexpectedSubmit = document.getElementById("unfreezeUnexpectedSubmit");
    const unfreezeUnexpectedCancel = document.getElementById("unfreezeUnexpectedCancel");
    const guardianFulfillModal = document.getElementById("guardianFulfillModal");
    const guardianFulfillClose = document.getElementById("guardianFulfillClose");
    const guardianFulfillCancel = document.getElementById("guardianFulfillCancel");
    const guardianFulfillSubmit = document.getElementById("guardianFulfillSubmit");
    const guardianFulfillEvidence = document.getElementById("guardianFulfillEvidence");
    const guardianFulfillEvidencePreview = document.getElementById("guardianFulfillEvidencePreview");
    const guardianFulfillCommitmentCode = document.getElementById("guardianFulfillCommitmentCode");
    const guardianFulfillCodeError = document.getElementById("guardianFulfillCodeError");
    const guardianFulfillAttributionSecret = document.getElementById("guardianFulfillAttributionSecret");
    const guardianFulfillAttributionPublic = document.getElementById("guardianFulfillAttributionPublic");
    const guardianFulfillAttributionError = document.getElementById("guardianFulfillAttributionError");
    const cooperativeParticipateModal = document.getElementById("cooperativeParticipateModal");
    const cooperativeParticipateDescription = document.getElementById("cooperativeParticipateDescription");
    const cooperativeParticipateQuote = document.getElementById("cooperativeParticipateQuote");
    const cooperativeParticipateTitle = document.getElementById("cooperativeParticipateTitle");
    const cooperativeParticipatePrompt = document.getElementById("cooperativeParticipatePrompt");
    const cooperativeParticipateCta = document.getElementById("confirmCooperativeParticipate");
    const cancelCooperativeParticipate = document.getElementById("cancelCooperativeParticipate");
    const confirmCooperativeParticipate = document.getElementById("confirmCooperativeParticipate");
    const cooperativeSecurityModal = document.getElementById("cooperativeSecurityModal");
    const cooperativeSecurityCodeInput = document.getElementById("cooperativeSecurityCodeInput");
    const cooperativeSecurityError = document.getElementById("cooperativeSecurityError");
    const confirmCooperativeSecurity = document.getElementById("confirmCooperativeSecurity");
    const cancelCooperativeSecurity = document.getElementById("cancelCooperativeSecurity");
    const cooperativeCharacter = document.getElementById("cooperativeCharacter");
    const cooperativeCancelParticipationModal = document.getElementById("cooperativeCancelParticipationModal");
    const cooperativeCancelParticipationYes = document.getElementById("cooperativeCancelParticipationYes");
    const cooperativeCancelParticipationNo = document.getElementById("cooperativeCancelParticipationNo");
    const cooperativeOwnerReviewModal = document.getElementById("cooperativeOwnerReviewModal");
    const cooperativeOwnerReviewClose = document.getElementById("cooperativeOwnerReviewClose");
    const cooperativeOwnerReviewCancel = document.getElementById("cooperativeOwnerReviewCancel");
    const cooperativeOwnerReviewProceed = document.getElementById("cooperativeOwnerReviewProceed");
    const cooperativeOwnerReviewList = document.getElementById("cooperativeOwnerReviewList");
    const cooperativeOwnerReviewStatus = document.getElementById("cooperativeOwnerReviewStatus");
    const cooperativeFeedbackModal = document.getElementById("cooperativeFeedbackModal");
    const cooperativeFeedbackTitle = document.getElementById("cooperativeFeedbackTitle");
    const cooperativeFeedbackMessage = document.getElementById("cooperativeFeedbackMessage");
    const cooperativeFeedbackClose = document.getElementById("cooperativeFeedbackClose");
    const personalWishText = document.getElementById("personalWishText");
    const personalWishError = document.getElementById("personalWishError");
    const confirmPersonalWish = document.getElementById("confirmPersonalWish");
    const personalWishMedia = document.getElementById("personalWishMedia");
    const personalWishPreview = document.getElementById("personalWishPreview");
    const personalWishFileName = document.getElementById("personalWishFileName");
    const personalWishTypeIcon = document.getElementById("personalWishTypeIcon");
    const personalWishTypeInputs = document.querySelectorAll('input[name="personalWishType"]');
    const personalWishTypeHint = document.getElementById("personalWishTypeHint");
    const personalMax = 50;
    const personalMin = 7;
    let personalTotal = 0;
    const cooperativeMax = 20;
    const cooperativeMin = 3;
    let cooperativeTotal = 0;
    let personalPreviewUrl = null;
    let personalPreviewImage = null;
    let activePersonalSlot = null;
    let activeDeleteSlot = null;
    let activeFulfillSlot = null;
    let activeFulfillContext = "personal";
    let activeIcanSlot = null;
    let activeCooperativeSlot = null;
    let activeCooperativeCancelSlot = null;
    let activeCooperativeOwnerReviewSlot = null;
    let cooperativePreviewUrl = null;
    let cooperativePreviewImage = null;
    let activeParticipateSource = null;
    let activeParticipateMode = "create";
    let activeParticipateSlot = null;
    let activeSecuritySlot = null;
    let activeSecurityCode = "";
    let cooperativeOwnerReviewSubmitting = false;
    let coverMoveEnabled = false;
    let coverDragActive = false;
    let coverStartX = 0;
    let coverStartY = 0;
    let coverOffsetX = 0;
    let coverOffsetY = 0;
    let coverMaxOffsetX = 0;
    let coverMaxOffsetY = 0;
    let coverDirty = false;
    let coverSavedSrc = "";
	    let coverSavedOffsetX = 0;
	    let coverSavedOffsetY = 0;
	    let coverPendingUrl = null;
	    let isViewingOwnProfile = true;
	    let viewerUserId = null;
	    let viewerUsername = "";
	    let viewerGuardianRank = 0;
	    let viewerIsGuardian = false;
	    let activeProfileUserId = null;
	    let activeProfileUsername = "";
	    let activeProfileFullName = "";
	    let highlightWishId = null;
	    let fulfillEvidenceUrl = null;
	    let fulfillEvidenceImage = null;
    const GUARDIANS_PAGE_SIZE = 4;
    const COOPERATIVE_PARTICIPANTS_LIMIT = 10;
    const GUARDIAN_REQUIRED_RANK = 3;
	    const GUARDIAN_AVATAR_PLACEHOLDERS = [
	      "/css/icons/Guardian1.png",
	      "/css/icons/Guardian2.png",
	      "/css/icons/Guardian3.png",
	      "/css/icons/Guardian4.png",
	    ];
	    let guardiansPage = 1;
	    let guardiansTotalPages = 1;
	    let guardiansItems = [];
	    let guardiansLoading = false;
	    let guardiansError = "";
	    let selectedGuardianUserId = null;
	    let guardianRequestWishId = null;
	    let guardianRequestWishText = "";
	    let guardianEvidenceUrl = null;
	    let guardianEvidenceMedia = null;
	    let guardianSubmitting = false;
	    let activeGuardianFreezeSlot = null;
	    let guardianFreezeSubmitting = false;
	    let activeGuardianFulfillSlot = null;
	    let guardianFulfillSubmitting = false;
	    let guardianFulfillEvidenceUrl = null;
	    let guardianFulfillEvidenceImage = null;
	    let guardianFulfillAttributionMode = null;

    const addLampSlot = () => {
      if (!lampSlotTemplate || !personalWishList) return;
      if (personalTotal >= personalMax) return;

      const li = document.createElement("li");
      li.className = "wish-slot is-empty";
      li.appendChild(lampSlotTemplate.content.cloneNode(true));
      personalWishList.appendChild(li);
      personalTotal += 1;

      if (personalWishCount) {
        personalWishCount.textContent = `${personalTotal}`;
      }

      if (personalWishAdd) {
        personalWishAdd.disabled = personalTotal >= personalMax;
      }
    };

    for (let i = 0; i < personalMin; i += 1) {
      addLampSlot();
    }

    const addCooperativeSlot = () => {
      if (!lampSlotTemplate || !cooperativeWishList) return;
      if (cooperativeTotal >= cooperativeMax) return;

      const li = document.createElement("li");
      li.className = "wish-slot is-empty";
      li.appendChild(lampSlotTemplate.content.cloneNode(true));
      cooperativeWishList.appendChild(li);
      cooperativeTotal += 1;

      if (cooperativeWishCountLabel) {
        cooperativeWishCountLabel.textContent = `${cooperativeTotal}`;
      }

      if (cooperativeWishAdd) {
        cooperativeWishAdd.disabled = cooperativeTotal >= cooperativeMax;
      }
    };

    for (let i = 0; i < cooperativeMin; i += 1) {
      addCooperativeSlot();
    }

    const findCooperativeEditorSlot = () => {
      if (!cooperativeWishList) return null;
      const slots = Array.from(cooperativeWishList.querySelectorAll(".wish-slot"));
      const emptySlot = slots.find((slot) => slot.classList.contains("is-empty"));
      if (emptySlot) return emptySlot;
      if (cooperativeTotal >= cooperativeMax) return null;
      addCooperativeSlot();
      const updatedSlots = Array.from(cooperativeWishList.querySelectorAll(".wish-slot"));
      return updatedSlots[updatedSlots.length - 1] || null;
    };

    const updateModalScrollLock = () => {
      const hasOpenModal = document.querySelector(".modal-overlay:not(.hidden)");
      document.body.classList.toggle("modal-open", Boolean(hasOpenModal));
    };

    const PURPOSE_PREFIX = tr("Deseo ", "Wish ", "Souhait ");
    const PURPOSE_SECRET_TEXT = tr("Deseo marcado como secreto", "Wish marked as secret", "Souhait marqué comme secret");
    const PURPOSE_REVEAL_PREFIX = tr("Este deseo será revelado", "This wish will be revealed", "Ce souhait sera révélé");
    const PURPOSE_STORAGE_VERSION = 2;
    const API = "http://127.0.0.1:8000";
    const AAD_PURPOSE = new TextEncoder().encode("kiadez-life-purpose-v1");
    const AAD_VAULT = new TextEncoder().encode("kiadez-vault-v1");

    const purposePillBySlot = {
      1: purpose1,
      2: purpose2,
      3: purpose3
    };
    const purposeUnlockBySlot = {
      1: purposeUnlock1,
      2: purposeUnlock2,
      3: purposeUnlock3
    };
    const defaultPurposeTextBySlot = {
      1: purpose1?.textContent?.trim() || tr("Deseo #1: Secreto", "Wish #1: Secret", "Souhait n°1 : Secret"),
      2: purpose2?.textContent?.trim() || tr("Deseo de propósito sin definir", "Undefined purpose wish", "Souhait de mission non défini"),
      3: purpose3?.textContent?.trim() || tr("Deseo estar unido a Jesús", "I wish to be united with Jesus", "Je souhaite être uni à Jésus")
    };
    let purposeSlots = [];
    let activePurposeUnlockSlot = null;

    const bufToHex = (buf) => {
      return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
    };

    const hexToBuf = (hex) => {
      const bytes = new Uint8Array(hex.length / 2);
      for (let i = 0; i < bytes.length; i += 1) {
        bytes[i] = parseInt(hex.substr(i * 2, 2), 16);
      }
      return bytes.buffer;
    };

    const getTodayAtMidnight = () => {
      const now = new Date();
      now.setHours(0, 0, 0, 0);
      return now;
    };

    const formatRevealDate = (isoDate) => {
      const parts = (isoDate || "").split("-");
      if (parts.length !== 3) return isoDate || "";
      return `${parts[2]}/${parts[1]}/${parts[0]}`;
    };

    const isRevealPending = (isoDate) => {
      if (!isoDate) return false;
      const revealDate = new Date(`${isoDate}T00:00:00`);
      return revealDate.getTime() > getTodayAtMidnight().getTime();
    };

    const normalizePurposeText = (value) => {
      const trimmed = (value || "").trim();
      if (!trimmed) return "";
      if (trimmed === PURPOSE_PREFIX.trim()) return "";
      if (trimmed.startsWith(PURPOSE_PREFIX)) {
        const rest = trimmed.slice(PURPOSE_PREFIX.length).trim();
        return rest ? `${PURPOSE_PREFIX}${rest}` : "";
      }
      return `${PURPOSE_PREFIX}${trimmed}`;
    };

    const getIconLabel = (iconKey) => {
      if (iconKey === "air") return tr("Aire", "Air", "Air");
      if (iconKey === "earth") return tr("Tierra", "Earth", "Terre");
      if (iconKey === "water") return tr("Agua", "Water", "Eau");
      if (iconKey === "fire") return tr("Fuego", "Fire", "Feu");
      return tr("Icono", "Icon", "Icône");
    };

    const getIconSrc = (iconKey) => `assets/${iconKey}.png`;

    const setPurposeStatus = (groupEl, text) => {
      const statusEl = groupEl.querySelector(".purpose-status");
      if (statusEl) statusEl.textContent = text;
    };

    const getPurposeSlotMap = (slots) => new Map(
      (slots || []).map((slot) => [Number(slot.slot_number), slot])
    );

    const normalizePurposeSlot = (slot, fallbackSlotNumber) => {
      const slotNumber = Number(slot?.slot_number || fallbackSlotNumber);
      return {
        slot_number: slotNumber,
        is_private: Boolean(slot?.is_private),
        status: slot?.status || "active",
        reveal_at: slot?.reveal_at || null,
        icon_key: slot?.icon_key || null,
        text_public: slot?.text_public || null,
        text_input: slot?.text_input || slot?.text_public || "",
        ciphertext_hex: slot?.ciphertext_hex || null,
        nonce_hex: slot?.nonce_hex || null
      };
    };

    const normalizePurposeState = (raw) => {
      if (!raw) return [];
      if (Array.isArray(raw.slots)) {
        return raw.slots
          .map((slot, index) => normalizePurposeSlot(slot, index + 1))
          .filter((slot) => slot.slot_number >= 1 && slot.slot_number <= 3);
      }

      const legacyValues = [raw.one, raw.two, raw.three];
      return legacyValues
        .map((value, index) => {
          const normalizedText = normalizePurposeText(value || "");
          if (!normalizedText) return null;
          return normalizePurposeSlot({
            slot_number: index + 1,
            is_private: false,
            text_public: normalizedText,
            text_input: normalizedText
          }, index + 1);
        })
        .filter(Boolean);
    };

    const readPurposeStorage = () => {
      return null;
    };

    const storePurposeValues = (slots) => {
      return slots;
    };

    const getPurposePresentation = (slot) => {
      if (!slot) {
        return { text: "", showUnlock: false };
      }

      if (slot.reveal_at && isRevealPending(slot.reveal_at)) {
        return {
          text: `${PURPOSE_REVEAL_PREFIX} ${formatRevealDate(slot.reveal_at)}`,
          showUnlock: false
        };
      }

      if (slot.is_private) {
        return {
          text: PURPOSE_SECRET_TEXT,
          showUnlock: true
        };
      }

      return {
        text: slot.text_public || slot.text_input || "",
        showUnlock: false
      };
    };

    const renderPurposeSlots = (slots) => {
      const slotMap = getPurposeSlotMap(slots);
      [1, 2, 3].forEach((slotNumber) => {
        const slot = slotMap.get(slotNumber);
        const pill = purposePillBySlot[slotNumber];
        const unlockBtn = purposeUnlockBySlot[slotNumber];
        if (!pill) return;

        if (!slot) {
          pill.textContent = defaultPurposeTextBySlot[slotNumber];
          unlockBtn?.classList.add("hidden");
          return;
        }

        const view = getPurposePresentation(slot);
        pill.textContent = view.text || defaultPurposeTextBySlot[slotNumber];
        unlockBtn?.classList.toggle("hidden", !view.showUnlock);
      });
    };

    const mergePurposeSlots = (remoteSlots, localSlots) => {
      const remoteMap = getPurposeSlotMap(remoteSlots);
      const localMap = getPurposeSlotMap(localSlots);
      return [1, 2, 3]
        .map((slotNumber) => {
          const remoteSlot = remoteMap.get(slotNumber);
          const localSlot = localMap.get(slotNumber);
          if (remoteSlot) {
            return normalizePurposeSlot({
              ...remoteSlot,
              // La vista debe reflejar fielmente la base de datos:
              // no arrastrar textos antiguos guardados localmente.
              text_input: remoteSlot.text_public || ""
            }, slotNumber);
          }
          if (localSlot) {
            return normalizePurposeSlot(localSlot, slotNumber);
          }
          return null;
        })
        .filter(Boolean);
    };

    const getAccessToken = () => localStorage.getItem("access_token") || "";

    const parseResponseJson = async (res) => {
      try {
        return await res.json();
      } catch {
        return {};
      }
    };

	    const apiFetch = async (path, options = {}) => {
	      const token = getAccessToken();
	      if (!token) {
	        throw new Error(tr("No hay sesión activa.", "No active session.", "Aucune session active."));
	      }

      const headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`
      };
      const res = await fetch(`${API}${path}`, { ...options, headers });
      if (res.status === 401) {
        throw new Error(tr("Sesión expirada. Inicia sesión nuevamente.", "Session expired. Please sign in again.", "Session expirée. Connecte-toi de nouveau."));
      }
	      return res;
	    };

	    const normalizeUsername = (value) => {
	      let normalized = String(value || "").trim().toLowerCase();
	      while (normalized.startsWith("@")) normalized = normalized.slice(1);
	      return normalized;
	    };

	    const fetchViewerIdentity = async () => {
	      const res = await apiFetch("/auth/me");
	      const data = await parseResponseJson(res);
	      if (!res.ok) {
	        throw new Error(data.detail || tr("No se pudo cargar tu perfil.", "Could not load your profile.", "Impossible de charger ton profil."));
	      }
	      const userId = Number(data?.user_number);
	      const guardianRank = Number(data?.guardian_rank || 0) || 0;
	      return {
	        user_id: Number.isFinite(userId) && userId > 0 ? userId : null,
	        username: normalizeUsername(data?.username || ""),
	        guardian_rank: guardianRank,
	      };
	    };

	    const fetchFollowProfile = async ({ userId = null, username = null } = {}) => {
	      const idValue = Number(userId);
	      const usernameValue = normalizeUsername(username || "");
	      if (Number.isFinite(idValue) && idValue > 0) {
	        const res = await apiFetch(`/follows/profile?user_id=${encodeURIComponent(String(idValue))}`);
	        const data = await parseResponseJson(res);
	        if (!res.ok) throw new Error(data.detail || tr("No se pudo cargar el perfil.", "Could not load the profile.", "Impossible de charger le profil."));
	        return data;
	      }
	      if (usernameValue) {
	        const res = await apiFetch(`/follows/profile?username=${encodeURIComponent(usernameValue)}`);
	        const data = await parseResponseJson(res);
	        if (!res.ok) throw new Error(data.detail || tr("No se pudo cargar el perfil.", "Could not load the profile.", "Impossible de charger le profil."));
	        return data;
	      }
	      throw new Error(tr("Parámetros inválidos para cargar perfil.", "Invalid parameters to load profile.", "Paramètres invalides pour charger le profil."));
	    };

	    const buildViewerHomeUrl = () => {
	      if (viewerUsername) return `/home_user.html?u=${encodeURIComponent(viewerUsername)}`;
	      if (viewerUserId) return `/home_user.html?id=${encodeURIComponent(String(viewerUserId))}`;
	      return "/home_user.html";
	    };

	    const buildProfileQueryParams = () => {
	      if (activeProfileUsername) {
	        return { key: "u", value: activeProfileUsername };
	      }
	      if (activeProfileUserId) {
	        return { key: "id", value: String(activeProfileUserId) };
	      }
	      return null;
	    };

	    const buildProfileModuleUrl = (path) => {
	      const raw = String(path || "").trim();
	      if (!raw) return "";
	      try {
	        const url = new URL(raw, window.location.origin);
	        const qp = buildProfileQueryParams();
	        url.searchParams.delete("u");
	        url.searchParams.delete("id");
	        if (qp) url.searchParams.set(qp.key, qp.value);
	        return `${url.pathname}${url.search}`;
	      } catch {
	        return raw;
	      }
	    };

	    const PROFILE_MODULE_ROUTES = {
	      home: "/home_user.html",
	      public_wishes: "/my-public-whishes.html",
	      fulfilled_wishes: "/my-fulfilled-whises.html",
	      calendar: "/calendar.html",
	      oracle: "/oracle.html",
	    };

	    const syncProfileModuleLinks = () => {
	      document.querySelectorAll("a[data-profile-module]").forEach((link) => {
	        const key = String(link.getAttribute("data-profile-module") || "").trim();
	        const basePath = PROFILE_MODULE_ROUTES[key] || link.getAttribute("href") || "";
	        const nextHref = buildProfileModuleUrl(basePath);
	        if (nextHref) link.href = nextHref;
	      });
	    };

	    const applyProfileHeader = () => {
	      const title = document.querySelector(".public-wishes-title");
	      if (title) {
	        title.textContent = isViewingOwnProfile
	          ? tr("Mis deseos públicos", "My public wishes", "Mes souhaits publics")
	          : `${tr("Deseos públicos de", "Public wishes of", "Souhaits publics de")} ${activeProfileFullName || tr("usuario", "user", "utilisateur")}`;
	      }
	      document.title = isViewingOwnProfile
	        ? tr("Kiadez — Mis deseos públicos", "Kiadez — My public wishes", "Kiadez — Mes souhaits publics")
	        : `Kiadez — ${tr("Deseos públicos de", "Public wishes of", "Souhaits publics de")} ${activeProfileFullName || tr("usuario", "user", "utilisateur")}`;
	    };

	    const applyForeignViewMode = () => {
	      document.body.dataset.visitor = "true";
	      if (personalWishAdd) personalWishAdd.classList.add("hidden");
	      if (cooperativeWishAdd) cooperativeWishAdd.classList.add("hidden");
	      document.querySelectorAll(".wish-add-row").forEach((row) => row.classList.add("hidden"));
	    };

	    const resolveProfileContext = async () => {
	      const params = new URLSearchParams(window.location.search);
	      highlightWishId = parsePositiveId(params.get("wish"));
	      const requestedIdRaw = params.get("id");
	      const requestedId = Number(requestedIdRaw);
	      const requestedUserId =
	        Number.isFinite(requestedId) && requestedId > 0 ? requestedId : null;
	      const requestedUsername = normalizeUsername(params.get("u") || "");

	      const me = await fetchViewerIdentity();
	      viewerUserId = me.user_id;
	      viewerUsername = me.username;
	      viewerGuardianRank = Number(me.guardian_rank || 0) || 0;
	      viewerIsGuardian = viewerGuardianRank >= GUARDIAN_REQUIRED_RANK;

	      activeProfileUserId = viewerUserId;
	      activeProfileUsername = viewerUsername;
	      activeProfileFullName = "";
	      isViewingOwnProfile = true;
	      document.body.dataset.visitor = "false";

	      const wantsOtherProfile = Boolean(requestedUserId || requestedUsername);
	      if (wantsOtherProfile) {
	        const isSelfById = requestedUserId && viewerUserId && requestedUserId === viewerUserId;
	        const isSelfByUsername = requestedUsername && viewerUsername && requestedUsername === viewerUsername;
	        if (!isSelfById && !isSelfByUsername) {
	          const profile = await fetchFollowProfile({
	            userId: requestedUserId,
	            username: requestedUserId ? null : requestedUsername,
	          });
	          activeProfileUserId = Number(profile?.user_id) || requestedUserId;
	          activeProfileUsername = normalizeUsername(profile?.username || requestedUsername);
	          activeProfileFullName = String(profile?.full_name || "").trim();
	          isViewingOwnProfile = Boolean(viewerUserId && activeProfileUserId === viewerUserId);
	          if (!isViewingOwnProfile) {
	            applyForeignViewMode();
	          }
	        }
	      }

	      applyProfileHeader();
	      syncProfileModuleLinks();
	    };

	    const uploadWishImage = async (file) => {
	      if (!isViewingOwnProfile) {
	        throw new Error(tr("No autorizado.", "Not authorized.", "Non autorisé."));
	      }
	      if (!file) return null;
	      const formData = new FormData();
	      formData.append("visibility", "public");
      formData.append("file", file);
      const res = await apiFetch("/media/upload/direct", {
        method: "POST",
        body: formData
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo subir la imagen.", "Could not upload the image.", "Impossible de téléverser l'image."));
      }
	      return data;
	    };

	    const uploadPublicImageMedia = async (file) => {
	      if (!file) return null;
	      const formData = new FormData();
	      formData.append("visibility", "public");
	      formData.append("file", file);
	      const res = await apiFetch("/media/upload/direct", {
	        method: "POST",
	        body: formData
	      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo subir la imagen.", "Could not upload the image.", "Impossible de téléverser l'image."));
      }
	      return data;
	    };

	    const uploadGuardianEvidenceFile = async (file) => {
	      if (!file) return null;
	      const mime = String(file.type || "").toLowerCase();

	      if (mime.startsWith("image/")) {
	        const formData = new FormData();
	        formData.append("visibility", "private");
	        formData.append("file", file);
	        const res = await apiFetch("/media/upload/direct", {
	          method: "POST",
	          body: formData
	        });
        const data = await parseResponseJson(res);
        if (!res.ok) {
          throw new Error(data.detail || tr("No se pudo subir la evidencia.", "Could not upload the evidence.", "Impossible de téléverser la preuve."));
        }
	        return { media_id: data.media_id };
	      }

	      if (!mime.startsWith("video/")) {
	        throw new Error(tr("Solo se permiten archivos de imagen o video.", "Only image or video files are allowed.", "Seuls les fichiers image ou vidéo sont autorisés."));
	      }

	      const presignRes = await apiFetch("/media/presign/upload", {
	        method: "POST",
	        headers: { "Content-Type": "application/json" },
	        body: JSON.stringify({
	          filename: file.name,
	          content_type: file.type,
	          size_bytes: file.size,
	          visibility: "private"
	        })
	      });
	      const presignData = await parseResponseJson(presignRes);
	      if (!presignRes.ok) {
	        throw new Error(presignData.detail || tr("No se pudo preparar la carga del video.", "Could not prepare video upload.", "Impossible de préparer l'envoi vidéo."));
	      }

	      const mediaId = Number(presignData?.media_id || 0);
	      if (!Number.isFinite(mediaId) || mediaId <= 0) {
	        throw new Error(tr("No se pudo preparar la carga (media_id inválido).", "Could not prepare upload (invalid media_id).", "Impossible de préparer l'envoi (media_id invalide)."));
	      }

	      const proxyForm = new FormData();
	      proxyForm.append("media_id", String(mediaId));
	      proxyForm.append("file", file);
	      const proxyRes = await apiFetch("/media/upload/proxy", {
	        method: "POST",
	        body: proxyForm
	      });
	      const proxyData = await parseResponseJson(proxyRes);
	      if (!proxyRes.ok) {
	        throw new Error(proxyData.detail || tr("No se pudo subir el video.", "Could not upload the video.", "Impossible de upload the video."));
	      }

	      return { media_id: mediaId };
	    };

	    const fetchPersonalWishList = async () => {
	      const profileId = Number(activeProfileUserId);
	      const endpoint =
	        !isViewingOwnProfile && Number.isFinite(profileId) && profileId > 0
	          ? `/public-wishes/user/${encodeURIComponent(String(profileId))}/personal`
	          : "/public-wishes/personal";
	      const res = await apiFetch(endpoint);
	      const data = await parseResponseJson(res);
	      if (!res.ok) {
	        throw new Error(data.detail || tr("No se pudieron cargar tus deseos personales.", "Could not load your personal wishes.", "Impossible de load your personal wishes."));
	      }
	      return data;
	    };

	    const createPersonalWish = async (payload) => {
	      if (!isViewingOwnProfile) {
	        throw new Error(tr("No autorizado.", "Not authorized.", "Non autorisé."));
	      }
	      const res = await apiFetch("/public-wishes/personal", {
	        method: "POST",
	        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo crear el deseo personal.", "Could not create the personal wish.", "Impossible de create the personal wish."));
      }
      return data;
    };

	    const updatePersonalWishRecord = async (wishId, payload) => {
	      if (!isViewingOwnProfile) {
	        throw new Error(tr("No autorizado.", "Not authorized.", "Non autorisé."));
	      }
	      const res = await apiFetch(`/public-wishes/personal/${wishId}`, {
	        method: "PUT",
	        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo actualizar el deseo personal.", "Could not update the personal wish.", "Impossible de update the personal wish."));
      }
      return data;
    };

	    const deletePersonalWishRecord = async (wishId) => {
	      if (!isViewingOwnProfile) {
	        throw new Error(tr("No autorizado.", "Not authorized.", "Non autorisé."));
	      }
	      const res = await apiFetch(`/public-wishes/personal/${wishId}`, {
	        method: "DELETE"
	      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo borrar el deseo personal.", "Could not delete the personal wish.", "Impossible de supprimer le souhait personnel."));
      }
      return data;
    };

	    const fulfillPersonalWishRecord = async (wishId, evidenceMediaId = null) => {
	      if (!isViewingOwnProfile) {
	        throw new Error(tr("No autorizado.", "Not authorized.", "Non autorisé."));
	      }
	      const res = await apiFetch(`/public-wishes/personal/${wishId}/fulfill`, {
	        method: "POST",
	        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ evidence_media_id: evidenceMediaId || null })
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo marcar el deseo como cumplido.", "Could not mark the wish as fulfilled.", "Impossible de marquer le souhait comme accompli."));
      }
      return data;
    };

	    const freezePersonalWishRecord = async (wishId) => {
	      if (!viewerIsGuardian) {
	        throw new Error(tr("Acceso restringido (rango de Guardián requerido).", "Restricted access (Guardian rank required).", "Accès restreint (rang Gardien requis)."));
	      }
	      const res = await apiFetch(`/public-wishes/personal/${wishId}/freeze`, {
	        method: "POST"
	      });
	      const data = await parseResponseJson(res);
	      if (!res.ok) {
	        throw new Error(data.detail || tr("No se pudo congelar el deseo.", "Could not freeze the wish.", "Impossible de geler le souhait."));
	      }
	      return data;
	    };

	    const fulfillPersonalWishFromGuardianRecord = async (wishId, payload) => {
	      if (!viewerIsGuardian) {
	        throw new Error(tr("Acceso restringido (rango de Guardián requerido).", "Restricted access (Guardian rank required).", "Accès restreint (rang Gardien requis)."));
	      }
	      const res = await apiFetch(`/public-wishes/personal/${wishId}/guardian-fulfill`, {
	        method: "POST",
	        headers: { "Content-Type": "application/json" },
	        body: JSON.stringify(payload)
	      });
	      const data = await parseResponseJson(res);
	      if (!res.ok) {
	        throw new Error(data.detail || tr("No se pudo marcar el deseo como cumplido.", "Could not mark the wish as fulfilled.", "Impossible de marquer le souhait comme accompli."));
	      }
	      return data;
	    };

	    const unfreezePersonalWishRecord = async (wishId, payload) => {
	      if (!viewerIsGuardian) {
	        throw new Error(tr("Acceso restringido (rango de Guardián requerido).", "Restricted access (Guardian rank required).", "Accès restreint (rang Gardien requis)."));
	      }
	      const res = await apiFetch(`/public-wishes/personal/${wishId}/unfreeze`, {
	        method: "POST",
	        headers: { "Content-Type": "application/json" },
	        body: JSON.stringify(payload)
	      });
	      const data = await parseResponseJson(res);
	      if (!res.ok) {
	        throw new Error(data.detail || tr("No se pudo descongelar el deseo.", "Could not unfreeze the wish.", "Impossible de débloquer le souhait."));
	      }
	      return data;
	    };

	    const fetchCooperativeWishList = async () => {
	      const profileId = Number(activeProfileUserId);
	      const endpoint =
	        !isViewingOwnProfile && Number.isFinite(profileId) && profileId > 0
	          ? `/public-wishes/user/${encodeURIComponent(String(profileId))}/cooperative`
	          : "/public-wishes/cooperative";
	      const res = await apiFetch(endpoint);
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudieron cargar los deseos cooperativos.", "Could not load the cooperative wishes.", "Impossible de load the cooperative wishes."));
      }
	      return data;
	    };

	    const createCooperativeWish = async (payload) => {
	      if (!isViewingOwnProfile) {
	        throw new Error(tr("No autorizado.", "Not authorized.", "Non autorisé."));
	      }
	      const res = await apiFetch("/public-wishes/cooperative", {
	        method: "POST",
	        headers: { "Content-Type": "application/json" },
	        body: JSON.stringify(payload)
	      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo crear el deseo cooperativo.", "Could not create the cooperative wish.", "Impossible de create the cooperative wish."));
      }
	      return data;
	    };

	    const updateCooperativeWishRecord = async (wishId, payload) => {
	      if (!isViewingOwnProfile) {
	        throw new Error(tr("No autorizado.", "Not authorized.", "Non autorisé."));
	      }
	      const res = await apiFetch(`/public-wishes/cooperative/${wishId}`, {
	        method: "PUT",
	        headers: { "Content-Type": "application/json" },
	        body: JSON.stringify(payload)
	      });
		      const data = await parseResponseJson(res);
		      if (!res.ok) {
		        throw new Error(data.detail || tr("No se pudo actualizar el deseo cooperativo.", "Could not update the cooperative wish.", "Impossible de update the cooperative wish."));
		      }
	      return data;
	    };

	    const deleteCooperativeWishRecord = async (wishId) => {
	      if (!isViewingOwnProfile) {
	        throw new Error(tr("No autorizado.", "Not authorized.", "Non autorisé."));
	      }
	      const res = await apiFetch(`/public-wishes/cooperative/${wishId}`, {
	        method: "DELETE"
	      });
		      const data = await parseResponseJson(res);
		      if (!res.ok) {
		        throw new Error(data.detail || tr("No se pudo borrar el deseo cooperativo.", "Could not delete the cooperative wish.", "Impossible de supprimer le souhait coopératif."));
		      }
	      return data;
	    };

	    const participateInCooperativeWishRecord = async (wishId, payload) => {
	      const res = await apiFetch(`/public-wishes/cooperative/${wishId}/participate`, {
	        method: "POST",
	        headers: { "Content-Type": "application/json" },
	        body: JSON.stringify(payload)
	      });
		      const data = await parseResponseJson(res);
		      if (!res.ok) {
		        throw new Error(data.detail || tr("No se pudo registrar tu participación.", "Could not register your participation.", "Impossible d'enregistrer ta participation."));
		      }
	      return data;
	    };

	    const cancelCooperativeParticipationRecord = async (wishId) => {
	      const res = await apiFetch(`/public-wishes/cooperative/${wishId}/participation/mine`, {
	        method: "DELETE",
	      });
		      const data = await parseResponseJson(res);
		      if (!res.ok) {
		        throw new Error(data.detail || tr("No se pudo cancelar tu participación.", "Could not cancel your participation.", "Impossible d'annuler ta participation."));
		      }
	      return data;
	    };

	    const completeCooperativeParticipationRecord = async (wishId, payload) => {
	      const res = await apiFetch(`/public-wishes/cooperative/${wishId}/participation/complete`, {
	        method: "POST",
	        headers: { "Content-Type": "application/json" },
	        body: JSON.stringify(payload),
	      });
		      const data = await parseResponseJson(res);
		      if (!res.ok) {
		        throw new Error(data.detail || tr("No se pudo registrar la evidencia de tu participación.", "Could not register evidence for your participation.", "Impossible de register evidence for your participation."));
		      }
	      return data;
	    };

	    const validateCooperativeParticipationRecord = async (wishId, participationId) => {
	      const res = await apiFetch(
	        `/public-wishes/cooperative/${wishId}/participation/${participationId}/validate`,
	        { method: "POST" }
	      );
		      const data = await parseResponseJson(res);
		      if (!res.ok) {
		        throw new Error(data.detail || tr("No se pudo validar la participación.", "Could not validate the participation.", "Impossible de valider la participation."));
		      }
	      return data;
	    };

	    const fulfillCooperativeWishRecord = async (wishId, payload) => {
	      if (!isViewingOwnProfile) {
	        throw new Error(tr("No autorizado.", "Not authorized.", "Non autorisé."));
	      }
	      const res = await apiFetch(`/public-wishes/cooperative/${wishId}/fulfill`, {
	        method: "POST",
	        headers: { "Content-Type": "application/json" },
	        body: JSON.stringify(payload),
	      });
		      const data = await parseResponseJson(res);
		      if (!res.ok) {
		        throw new Error(data.detail || tr("No se pudo marcar el deseo cooperativo como cumplido.", "Could not mark the cooperative wish as fulfilled.", "Impossible de mark the cooperative wish as fulfilled."));
		      }
	      return data;
	    };

    const fetchPurposeSlotsFromApi = async () => {
      const token = getAccessToken();
      if (!token) return null;
      try {
        const res = await fetch(`${API}/life-purpose/mine?t=${Date.now()}`, {
          headers: { Authorization: `Bearer ${token}` },
          cache: "no-store"
        });
        if (!res.ok) return null;
        const data = await res.json();
        if (!Array.isArray(data?.slots)) return [];
        return data.slots
          .map((slot, index) => normalizePurposeSlot(slot, index + 1))
          .filter((slot) => slot.slot_number >= 1 && slot.slot_number <= 3);
      } catch (err) {
        console.error(err);
        return null;
      }
    };

    const loadPurposeFromStorage = async () => {
      const remoteSlots = await fetchPurposeSlotsFromApi();
      if (remoteSlots === null) {
        purposeSlots = [];
        renderPurposeSlots(purposeSlots);
        return;
      }

      // Si la API respondió, se toma como fuente de verdad.
      purposeSlots = mergePurposeSlots(remoteSlots, []);
      renderPurposeSlots(purposeSlots);
      storePurposeValues(purposeSlots);
    };

    const setLifeInputValue = (input, value) => {
      if (!input) return;
      const normalized = normalizePurposeText(value || "");
      input.value = normalized || PURPOSE_PREFIX;
      input.dispatchEvent(new Event("input", { bubbles: true }));
    };

    const applyPurposeStateToForm = (groupEl, slotData) => {
      if (!groupEl) return;

      const isPrivate = slotData?.is_private === true;
      const revealAt = slotData?.reveal_at || "";
      const iconKey = slotData?.icon_key || "";

      groupEl.dataset.isPrivate = isPrivate ? "true" : "false";
      groupEl.dataset.revealAt = revealAt;
      if (iconKey) {
        groupEl.dataset.iconKey = iconKey;
      } else {
        delete groupEl.dataset.iconKey;
      }

      const dateInput = groupEl.querySelector(".purpose-date");
      if (dateInput) dateInput.value = revealAt;

      const iconPanel = groupEl.querySelector(".purpose-icon-panel");
      iconPanel?.querySelectorAll(".purpose-icon").forEach((iconBtn) => {
        iconBtn.classList.toggle("is-selected", iconBtn.dataset.icon === iconKey);
      });

      const iconActionBtn = groupEl.querySelector(".purpose-action[data-action=\"icon\"]");
      if (iconActionBtn) {
        if (iconKey) {
          const iconLabel = getIconLabel(iconKey);
          iconActionBtn.innerHTML = `<img src="${getIconSrc(iconKey)}" alt="${iconLabel}">`;
          iconActionBtn.title = `${tr("Icono", "Icon", "Icône")}: ${iconLabel}`;
        } else {
          iconActionBtn.innerHTML = `<img src="/css/icons/iconelemental.webp" alt="${tr("Elegir icono", "Choose icon", "Choisir une icône")}">`;
          iconActionBtn.title = tr("Elegir icono", "Choose icon", "Choisir une icône");
        }
      }

      if (!slotData) {
        setPurposeStatus(groupEl, tr("Estado: público por defecto.", "Status: public by default.", "Statut : public par défaut."));
        return;
      }

      if (slotData.reveal_at && isRevealPending(slotData.reveal_at)) {
        setPurposeStatus(
          groupEl,
          tr("Estado: se revelará el día", "Status: it will be revealed on", "Statut : il sera révélé le") + ` ${formatRevealDate(slotData.reveal_at)}.`
        );
        return;
      }

      if (isPrivate) {
        setPurposeStatus(groupEl, tr("Estado: marcado como secreto.", "Status: marked as secret.", "Statut : marqué comme secret."));
        return;
      }

      setPurposeStatus(groupEl, tr("Estado: confirmado (publico).", "Status: confirmed (public).", "Statut : confirmé (public)."));
    };

    const openLifeProposalModal = () => {
      if (!lifeProposalOverlay) return;

      const fallbackSlots = purposeSlots.length
        ? purposeSlots
        : normalizePurposeState(readPurposeStorage());
      const fallbackMap = getPurposeSlotMap(fallbackSlots);

      const input1 = lifeProposalOverlay.querySelector("#p1");
      const input2 = lifeProposalOverlay.querySelector("#p2");
      const input3 = lifeProposalOverlay.querySelector("#p3");

      setLifeInputValue(input1, fallbackMap.get(1)?.text_input || fallbackMap.get(1)?.text_public || "");
      setLifeInputValue(input2, fallbackMap.get(2)?.text_input || fallbackMap.get(2)?.text_public || "");
      setLifeInputValue(input3, fallbackMap.get(3)?.text_input || fallbackMap.get(3)?.text_public || "");

      lifeProposalOverlay.querySelectorAll(".purpose-group").forEach((groupEl) => {
        const slotNumber = Number(groupEl.dataset.purpose || "0");
        applyPurposeStateToForm(groupEl, fallbackMap.get(slotNumber));
      });

      lifeProposalOverlay.classList.remove("hidden");
      lifeProposalOverlay.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeLifeProposalModal = () => {
      if (!lifeProposalOverlay) return;
      lifeProposalOverlay.classList.add("hidden");
      lifeProposalOverlay.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
    };

    const closePurposeUnlockModal = () => {
      if (!purposeUnlockOverlay) return;
      purposeUnlockOverlay.classList.add("hidden");
      purposeUnlockOverlay.setAttribute("aria-hidden", "true");
      if (purposeUnlockPassword) purposeUnlockPassword.value = "";
      if (purposeUnlockError) {
        purposeUnlockError.textContent = "";
        purposeUnlockError.classList.remove("is-visible");
      }
      activePurposeUnlockSlot = null;
      updateModalScrollLock();
    };

    const openPurposeUnlockModal = (slotNumber) => {
      const slotMap = getPurposeSlotMap(purposeSlots);
      const slotData = slotMap.get(slotNumber);
      if (!slotData || !slotData.is_private || isRevealPending(slotData.reveal_at)) return;

      activePurposeUnlockSlot = slotNumber;
      if (purposeUnlockText) {
        purposeUnlockText.textContent = tr(
          `Si confirmas tu clave privada, el deseo ${slotNumber} se volverá público.`,
          `If you confirm your private key, wish ${slotNumber} will become public.`
        );
      }
      if (purposeUnlockError) {
        purposeUnlockError.textContent = "";
        purposeUnlockError.classList.remove("is-visible");
      }
      if (purposeUnlockPassword) purposeUnlockPassword.value = "";

      purposeUnlockOverlay?.classList.remove("hidden");
      purposeUnlockOverlay?.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const pbkdf2Key = async (password, saltBuf, iters) => {
      const baseKey = await crypto.subtle.importKey(
        "raw",
        new TextEncoder().encode(password),
        "PBKDF2",
        false,
        ["deriveKey"]
      );
      return crypto.subtle.deriveKey(
        {
          name: "PBKDF2",
          salt: saltBuf,
          iterations: iters,
          hash: "SHA-256"
        },
        baseKey,
        { name: "AES-GCM", length: 256 },
        false,
        ["encrypt", "decrypt"]
      );
    };

    const decryptDekFromPassword = async (privatePassword, token) => {
      const vaultRes = await fetch(`${API}/vault/record`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const vaultData = await vaultRes.json();
      if (!vaultRes.ok) {
        throw new Error(vaultData.detail || tr("No se pudo leer el vault.", "Could not read the vault.", "Impossible de lire le coffre."));
      }

      const kdfSalt = hexToBuf(vaultData.kdf_salt_b64 || "");
      const wrappedDekNonce = new Uint8Array(hexToBuf(vaultData.wrapped_dek_nonce_b64 || ""));
      const wrappedDek = hexToBuf(vaultData.wrapped_dek_b64 || "");
      const iters = Number(vaultData.kdf_iters || 310000);
      const kek = await pbkdf2Key(privatePassword, kdfSalt, iters);
      const dekRaw = await crypto.subtle.decrypt(
        { name: "AES-GCM", iv: wrappedDekNonce, additionalData: AAD_VAULT },
        kek,
        wrappedDek
      );
      setDekSessionHex(bufToHex(dekRaw));
      return crypto.subtle.importKey("raw", dekRaw, { name: "AES-GCM" }, false, ["encrypt", "decrypt"]);
    };

    const importDekFromSession = async () => {
      const dekHex = getDekSessionHex();
      if (!dekHex) {
        throw new Error(tr("Vault no desbloqueado. Crea tu clave privada o desbloquéala primero.", "Vault not unlocked. Create your private key or unlock it first.", "Coffre non déverrouillé. Crée ta clé privée ou déverrouille-la d'abord."));
      }
      const dekRaw = hexToBuf(dekHex);
      return crypto.subtle.importKey("raw", dekRaw, { name: "AES-GCM" }, false, ["encrypt", "decrypt"]);
    };

    const aesGcmDecryptText = async (key, ciphertextHex, nonceHex, aadBuf) => {
      const decrypted = await crypto.subtle.decrypt(
        { name: "AES-GCM", iv: new Uint8Array(hexToBuf(nonceHex)), additionalData: aadBuf },
        key,
        hexToBuf(ciphertextHex)
      );
      return new TextDecoder().decode(decrypted);
    };

    const revealPurposeFromPrivateKey = async () => {
      if (!activePurposeUnlockSlot) return;
      const password = purposeUnlockPassword?.value || "";
      if (!password.trim()) {
        if (purposeUnlockError) {
          purposeUnlockError.textContent = tr("Debes digitar tu clave privada personal.", "You must enter your personal private key.", "Tu dois saisir ta clé privée personnelle.");
          purposeUnlockError.classList.add("is-visible");
        }
        return;
      }

      const slotMap = getPurposeSlotMap(purposeSlots);
      const slotData = slotMap.get(activePurposeUnlockSlot);
      if (!slotData?.ciphertext_hex || !slotData?.nonce_hex) {
        if (purposeUnlockError) {
          purposeUnlockError.textContent = tr("No hay datos cifrados para este deseo.", "There is no encrypted data for this wish.", "Il n'y a pas de données chiffrées pour ce souhait.");
          purposeUnlockError.classList.add("is-visible");
        }
        return;
      }

      const token = getAccessToken();
      if (!token) {
        if (purposeUnlockError) {
          purposeUnlockError.textContent = tr("No hay sesión activa.", "No active session.", "Aucune session active.");
          purposeUnlockError.classList.add("is-visible");
        }
        return;
      }

      try {
        const dekKey = await decryptDekFromPassword(password, token);
        const plainText = await aesGcmDecryptText(
          dekKey,
          slotData.ciphertext_hex,
          slotData.nonce_hex,
          AAD_PURPOSE
        );

        const revealRes = await fetch(`${API}/life-purpose/reveal`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            slot_number: activePurposeUnlockSlot,
            text_public: plainText
          })
        });
        const revealData = await revealRes.json().catch(() => ({}));
        if (!revealRes.ok) {
          throw new Error(revealData.detail || tr("No se pudo revelar el deseo.", "Could not reveal the wish.", "Impossible de reveal the wish."));
        }

        purposeSlots = purposeSlots.map((slot) => {
          if (Number(slot.slot_number) !== Number(activePurposeUnlockSlot)) return slot;
          return {
            ...slot,
            is_private: false,
            text_public: plainText,
            text_input: plainText,
            ciphertext_hex: null,
            nonce_hex: null,
            status: "active"
          };
        });
        renderPurposeSlots(purposeSlots);
        storePurposeValues(purposeSlots);
        closePurposeUnlockModal();
      } catch (err) {
        if (purposeUnlockError) {
          purposeUnlockError.textContent = err?.message || tr("No se pudo desbloquear el deseo.", "Could not unlock the wish.", "Impossible de unlock the wish.");
          purposeUnlockError.classList.add("is-visible");
        }
      }
    };

    lifeProposalClose?.addEventListener("click", closeLifeProposalModal);
    lifeProposalCloseFooter?.addEventListener("click", closeLifeProposalModal);
    lifeProposalOverlay?.addEventListener("click", (event) => {
      if (event.target === lifeProposalOverlay) closeLifeProposalModal();
    });

    [purposeUnlock1, purposeUnlock2, purposeUnlock3].forEach((unlockBtn) => {
      unlockBtn?.addEventListener("click", () => {
        const slotNumber = Number(unlockBtn.dataset.slot || "0");
        if (!slotNumber) return;
        openPurposeUnlockModal(slotNumber);
      });
    });

    purposeUnlockClose?.addEventListener("click", closePurposeUnlockModal);
    purposeUnlockCancel?.addEventListener("click", closePurposeUnlockModal);
    purposeUnlockOverlay?.addEventListener("click", (event) => {
      if (event.target === purposeUnlockOverlay) closePurposeUnlockModal();
    });
    purposeUnlockConfirm?.addEventListener("click", revealPurposeFromPrivateKey);
    purposeUnlockPassword?.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        revealPurposeFromPrivateKey();
      }
    });

    purposeFulfillBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        btn.classList.add("is-marked");
        btn.setAttribute("title", tr("Deseo marcado como cumplido (demo)", "Wish marked as fulfilled (demo)", "Souhait marqué comme accompli (démo)"));
      });
    });

    const openPersonalWishModal = () => {
      if (!personalWishModal) return;
      personalWishModal.classList.remove("hidden");
      personalWishModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
      if (personalWishError) {
        personalWishError.classList.remove("is-visible");
      }
    };

    const closePersonalWishModalFn = () => {
      if (!personalWishModal) return;
      personalWishModal.classList.add("hidden");
      personalWishModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
    };

    const openCooperativeWishModal = () => {
      if (!cooperativeWishModal) return;
      const isEditing = Boolean(activeCooperativeSlot?.classList?.contains("is-filled"));
      if (!isEditing) {
        resetCooperativeWishForm();
      }
      setCooperativeWishError(false);
      cooperativeWishModal.classList.remove("hidden");
      cooperativeWishModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
      if (cooperativeWishSecurityCode && isEditing) {
        cooperativeWishSecurityCode.value = activeCooperativeSlot?.dataset?.securityCode || "";
      }
    };

    const closeCooperativeWishModalFn = () => {
      if (!cooperativeWishModal) return;
      cooperativeWishModal.classList.add("hidden");
      cooperativeWishModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
    };

    const openDeleteWishModal = (slot) => {
      if (!deleteWishModal) return;
      activeDeleteSlot = slot;
      deleteWishModal.classList.remove("hidden");
      deleteWishModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeDeleteWishModalFn = () => {
      if (!deleteWishModal) return;
      deleteWishModal.classList.add("hidden");
      deleteWishModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
      activeDeleteSlot = null;
    };

    const openFulfillWishModal = (slot, context = "personal") => {
      if (!fulfillWishModal) return;
      activeFulfillSlot = slot;
      activeFulfillContext = context || "personal";
      fulfillWishModal.classList.remove("hidden");
      fulfillWishModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
      if (fulfillEvidence) fulfillEvidence.value = "";
      updateFulfillEvidencePreview(null);
    };

    const closeFulfillWishModalFn = () => {
      if (!fulfillWishModal) return;
      fulfillWishModal.classList.add("hidden");
      fulfillWishModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
      if (fulfillEvidence) fulfillEvidence.value = "";
      updateFulfillEvidencePreview(null);
      activeFulfillSlot = null;
      activeFulfillContext = "personal";
    };

    const openIcanConfirmModal = (slot) => {
      if (!icanConfirmModal) return;
      activeIcanSlot = slot;
      icanConfirmModal.classList.remove("hidden");
      icanConfirmModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeIcanConfirmModalFn = () => {
      if (!icanConfirmModal) return;
      icanConfirmModal.classList.add("hidden");
      icanConfirmModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
      activeIcanSlot = null;
    };

	    const renderGuardianSelect = () => {
	      if (!guardianSelect) return;

	      guardianSelect.innerHTML = "";

	      const setStatus = (message) => {
	        if (!guardianStatus) return;
	        const normalized = String(message || "").trim();
	        guardianStatus.textContent = normalized;
	        guardianStatus.classList.toggle("hidden", !normalized);
	      };

	      if (guardiansLoading) {
	        setStatus(tr("Cargando guardianes...", "Loading guardians...", "Chargement des Gardiens..."));
	      } else if (guardiansError) {
	        setStatus(guardiansError);
	      } else if (!guardiansItems.length) {
	        setStatus(tr("Aún no hay guardianes disponibles.", "No guardians are available yet.", "Aucun Gardien n'est encore disponible."));
	      } else {
	        setStatus(tr("Pulsa un avatar para visitar el perfil del Guardián.", "Tap an avatar to view the Guardian profile.", "Appuie sur un avatar pour voir le profil du Gardien."));
	      }

	      const availableGuardianIds = guardiansItems
	        .map((guardian) => parsePositiveId(guardian?.user_id))
	        .filter(Boolean);
	      const firstGuardianId = availableGuardianIds[0] || null;
	      if (!selectedGuardianUserId && firstGuardianId) {
	        selectedGuardianUserId = firstGuardianId;
	      }
	      if (selectedGuardianUserId && !availableGuardianIds.includes(selectedGuardianUserId)) {
	        selectedGuardianUserId = firstGuardianId;
	      }

	      guardiansItems.slice(0, GUARDIANS_PAGE_SIZE).forEach((guardian, index) => {
	        const profileUrl = String(guardian?.profile_url || "").trim();
	        if (!profileUrl) return;

	        const guardianUserId = parsePositiveId(guardian?.user_id);
	        if (!guardianUserId) return;

	        const fullName = String(guardian?.full_name || tr("Guardián", "Guardian", "Gardien")).trim() || tr("Guardián", "Guardian", "Gardien");
	        const handle = String(guardian?.handle || "").trim();
	        const imgSrc = GUARDIAN_AVATAR_PLACEHOLDERS[index] || GUARDIAN_AVATAR_PLACEHOLDERS[0];

	        const link = document.createElement("a");
	        link.className = "guardian-option";
	        link.href = profileUrl;
	        link.target = "_blank";
	        link.rel = "noopener noreferrer";
	        link.title = handle ? `${fullName} (${handle})` : fullName;
	        link.setAttribute("aria-label", `Visitar perfil de ${fullName}`);
	        link.dataset.guardianUserId = `${guardianUserId}`;
	        if (selectedGuardianUserId && guardianUserId === selectedGuardianUserId) {
	          link.classList.add("is-selected");
	          link.setAttribute("aria-current", "true");
	        }

	        const img = document.createElement("img");
	        img.className = "guardian-avatar";
	        img.src = imgSrc;
	        img.alt = fullName;
	        link.appendChild(img);

	        guardianSelect.appendChild(link);
	      });

	      if (guardianPageLabel) {
	        const safeTotalPages = Math.max(1, Number(guardiansTotalPages || 1));
	        const safePage = Math.max(1, Math.min(Number(guardiansPage || 1), safeTotalPages));
	        guardianPageLabel.textContent = `${safePage} / ${safeTotalPages}`;
	      }

	      if (guardianPrevPage) {
	        guardianPrevPage.disabled = guardiansLoading || guardiansPage <= 1;
	      }
	      if (guardianNextPage) {
	        guardianNextPage.disabled = guardiansLoading || guardiansPage >= guardiansTotalPages;
	      }
	    };

	    const loadGuardiansPage = async (page = 1) => {
	      const requestedPage = Math.max(1, Number(page || 1));
	      guardiansLoading = true;
	      guardiansError = "";
	      guardiansItems = [];
	      guardiansPage = requestedPage;
	      renderGuardianSelect();

	      try {
	        const res = await apiFetch(
	          `/follows/guardians?page=${encodeURIComponent(String(requestedPage))}&page_size=${encodeURIComponent(String(GUARDIANS_PAGE_SIZE))}`
	        );
        const data = await parseResponseJson(res);
        if (!res.ok) {
          throw new Error(data.detail || tr("No se pudieron cargar los guardianes.", "Could not load guardians.", "Impossible de charger les Gardiens."));
        }
	        guardiansItems = Array.isArray(data?.items) ? data.items : [];
	        guardiansTotalPages = Math.max(1, Number(data?.total_pages || 1));
	        guardiansPage = Math.max(1, Math.min(Number(data?.page || requestedPage), guardiansTotalPages));
      } catch (error) {
        console.error(error);
        guardiansError = error?.message || tr("No se pudieron cargar los guardianes.", "Could not load guardians.", "Impossible de charger les Gardiens.");
      } finally {
        guardiansLoading = false;
        renderGuardianSelect();
	      }
	    };

	    const updateGuardianEvidencePreview = (file) => {
	      if (!guardianEvidencePreview || !guardianEvidenceThumb) return;

	      if (guardianEvidenceUrl) {
	        URL.revokeObjectURL(guardianEvidenceUrl);
	        guardianEvidenceUrl = null;
	      }

	      guardianEvidencePreview.classList.add("hidden");
	      if (guardianEvidenceMedia) {
	        guardianEvidenceMedia.remove();
	        guardianEvidenceMedia = null;
	      }
	      guardianEvidenceThumb.innerHTML = "";
	      if (guardianEvidenceName) guardianEvidenceName.textContent = "";

	      if (!file) return;

	      guardianEvidenceUrl = URL.createObjectURL(file);
	      const mime = String(file.type || "").toLowerCase();

	      if (mime.startsWith("video/")) {
	        const video = document.createElement("video");
	        video.src = guardianEvidenceUrl;
        video.controls = true;
        video.muted = true;
        video.playsInline = true;
        video.preload = "metadata";
        video.setAttribute("aria-label", tr("Evidencia seleccionada (video)", "Selected evidence (video)", "Preuve sélectionnée (vidéo)"));
        guardianEvidenceMedia = video;
      } else if (mime.startsWith("image/")) {
        const img = document.createElement("img");
        img.src = guardianEvidenceUrl;
        img.alt = tr("Evidencia seleccionada", "Selected evidence", "Preuve sélectionnée");
        guardianEvidenceMedia = img;
      } else {
        const fallback = document.createElement("div");
        fallback.textContent = tr("Archivo adjunto", "Attached file", "Fichier joint");
        guardianEvidenceMedia = fallback;
      }

	      if (guardianEvidenceMedia) {
	        guardianEvidenceMedia.className = "guardian-evidence-media";
	        guardianEvidenceThumb.appendChild(guardianEvidenceMedia);
	      }

	      if (guardianEvidenceName) guardianEvidenceName.textContent = file.name || "";
	      guardianEvidencePreview.classList.remove("hidden");
	    };

	    const setGuardianFieldError = (fieldEl, errorEl, show, message = "") => {
	      if (fieldEl) fieldEl.classList.toggle("is-error", Boolean(show));
	      if (!errorEl) return;
	      if (show && message) errorEl.textContent = message;
	      errorEl.classList.toggle("is-visible", Boolean(show));
	    };

	    const clearGuardianFormErrors = () => {
	      setGuardianFieldError(guardianReasonVisitor, guardianReasonError, false);
	      setGuardianFieldError(guardianPhoneVisitor, guardianPhoneError, false);
	      setGuardianFieldError(guardianEmailVisitor, guardianEmailError, false);
	      setGuardianFieldError(null, guardianEvidenceError, false);
	      guardianEvidenceRow?.classList.remove("is-error");
	    };

	    const clearGuardianFormValues = () => {
	      if (guardianReasonVisitor) guardianReasonVisitor.value = "";
	      if (guardianPhoneVisitor) guardianPhoneVisitor.value = "";
	      if (guardianEmailVisitor) guardianEmailVisitor.value = "";
	      if (guardianEvidenceInput) guardianEvidenceInput.value = "";
	      updateGuardianEvidencePreview(null);
	    };

	    const syncGuardianRequestContext = () => {
      if (!guardianRequestContext) return;
      const wishId = parsePositiveId(guardianRequestWishId);
      const text = String(guardianRequestWishText || "").trim();
      const prefix = wishId ? `${tr("Deseo", "Wish", "Souhait")} #${wishId}` : tr("Deseo", "Wish", "Souhait");
      const label = text ? `${prefix}: ${text}` : (wishId ? prefix : "");
      guardianRequestContext.textContent = label;
      guardianRequestContext.classList.toggle("hidden", !label);
	    };

	    const validateGuardianWishRequest = () => {
	      clearGuardianFormErrors();

	      const wishId = parsePositiveId(guardianRequestWishId);
	      if (!wishId) {
	        window.alert(tr("No se pudo identificar el deseo. Cierra y vuelve a intentarlo.", "Could not identify the wish. Close and try again.", "Impossible d'identifier le souhait. Ferme et réessaie."));
	        return null;
	      }

	      const guardianId = parsePositiveId(selectedGuardianUserId);
	      if (!guardianId) {
	        window.alert(tr("Aún no hay guardianes disponibles para recibir esta solicitud.", "No guardians are available yet to receive this request.", "Aucun Gardien n'est encore disponible pour recevoir cette demande."));
	        return null;
	      }

	      const reason = String(guardianReasonVisitor?.value || "").trim();
	      const phone = String(guardianPhoneVisitor?.value || "").trim();
	      const email = String(guardianEmailVisitor?.value || "").trim();
	      const evidenceFile = guardianEvidenceInput?.files?.[0] || null;

	      let firstInvalid = null;

	      if (!reason) {
	        setGuardianFieldError(guardianReasonVisitor, guardianReasonError, true, tr("Debes describir el motivo.", "You must describe the reason.", "Tu dois décrire la raison."));
	        firstInvalid = firstInvalid || guardianReasonVisitor;
	      }

	      if (!phone) {
	        setGuardianFieldError(guardianPhoneVisitor, guardianPhoneError, true, tr("Debes indicar tu número telefónico.", "You must provide your phone number.", "Tu dois fournir ton numéro de téléphone."));
	        firstInvalid = firstInvalid || guardianPhoneVisitor;
	      }

	      const emailOk = guardianEmailVisitor ? guardianEmailVisitor.checkValidity() : Boolean(email);
	      if (!email || !emailOk) {
	        setGuardianFieldError(guardianEmailVisitor, guardianEmailError, true, tr("Debes indicar un e-mail válido.", "You must provide a valid e-mail.", "Tu dois fournir un e-mail valide."));
	        firstInvalid = firstInvalid || guardianEmailVisitor;
	      }

	      if (!evidenceFile) {
	        setGuardianFieldError(null, guardianEvidenceError, true, tr("Debes adjuntar una evidencia (imagen o video).", "You must attach evidence (image or video).", "Tu dois attach evidence (image or video)."));
	        guardianEvidenceRow?.classList.add("is-error");
	        firstInvalid = firstInvalid || guardianEvidenceInput;
	      }

	      if (firstInvalid?.focus) firstInvalid.focus();
	      if (firstInvalid) return null;

	      return { wishId, guardianId, reason, phone, email, evidenceFile };
	    };

	    const submitGuardianWishRequest = async () => {
	      if (guardianSubmitting) return;
	      const validated = validateGuardianWishRequest();
	      if (!validated) return;

	      guardianSubmitting = true;
	      const oldLabel = guardianSendBtn?.textContent || tr("Enviar", "Send", "Envoyer");
	      if (guardianSendBtn) {
	        guardianSendBtn.disabled = true;
	        guardianSendBtn.textContent = tr("Enviando...", "Sending...", "Envoi...");
	      }

	      try {
	        const uploaded = await uploadGuardianEvidenceFile(validated.evidenceFile);
	        const evidenceMediaId = Number(uploaded?.media_id || 0);
	        if (!Number.isFinite(evidenceMediaId) || evidenceMediaId <= 0) {
	          throw new Error(tr("No se pudo subir la evidencia (media_id inválido).", "Could not upload evidence (invalid media_id).", "Impossible de upload evidence (invalid media_id)."));
	        }

	        const res = await apiFetch("/guardian-center/wish-requests", {
	          method: "POST",
	          headers: { "Content-Type": "application/json" },
	          body: JSON.stringify({
	            public_wish_id: validated.wishId,
	            guardian_user_id: validated.guardianId,
	            reason: validated.reason,
	            phone: validated.phone,
	            email: validated.email,
	            evidence_media_id: evidenceMediaId
	          })
	        });
	        const data = await parseResponseJson(res);
	        if (!res.ok) {
	          throw new Error(data.detail || tr("No se pudo enviar la solicitud.", "Could not send the request.", "Impossible d'envoyer la demande."));
	        }

	        window.alert(tr("Solicitud enviada. Un Guardián la recibirá en el Centro del Guardián.", "Request sent. A Guardian will receive it in the Guardian Center.", "Demande envoyée. Un Gardien la recevra dans le Centre des Gardiens."));
	        closeGuardianContactModalFn();
      } catch (error) {
        console.error(error);
        window.alert(error?.message || tr("No se pudo enviar la solicitud.", "Could not send the request.", "Impossible d'envoyer la demande."));
      } finally {
	        guardianSubmitting = false;
	        if (guardianSendBtn) {
	          guardianSendBtn.disabled = false;
	          guardianSendBtn.textContent = oldLabel;
	        }
	      }
	    };

    const openGuardianContactModal = () => {
      if (!guardianContactModal) return;
      guardianContactModal.classList.remove("hidden");
      guardianContactModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
	      clearGuardianFormErrors();
	      clearGuardianFormValues();
	      syncGuardianRequestContext();
	      void loadGuardiansPage(1);
    };

    const closeGuardianContactModalFn = () => {
      if (!guardianContactModal) return;
      guardianContactModal.classList.add("hidden");
      guardianContactModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
	      clearGuardianFormErrors();
	      clearGuardianFormValues();
	      selectedGuardianUserId = null;
	      guardianRequestWishId = null;
	      guardianRequestWishText = "";
	      syncGuardianRequestContext();
    };

    const openFreezeWishConfirmModal = (slot) => {
      if (!freezeWishConfirmModal || !slot) return;
      activeGuardianFreezeSlot = slot;
      freezeWishConfirmModal.classList.remove("hidden");
      freezeWishConfirmModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeFreezeWishConfirmModalFn = () => {
      if (!freezeWishConfirmModal) return;
      freezeWishConfirmModal.classList.add("hidden");
      freezeWishConfirmModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
      activeGuardianFreezeSlot = null;
    };

    const openUnfreezeWishReasonModal = (slot) => {
      if (!unfreezeWishReasonModal || !slot) return;
      activeGuardianFreezeSlot = slot;
      unfreezeWishReasonModal.classList.remove("hidden");
      unfreezeWishReasonModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeUnfreezeWishReasonModalFn = ({ keepActiveSlot = false } = {}) => {
      if (!unfreezeWishReasonModal) return;
      unfreezeWishReasonModal.classList.add("hidden");
      unfreezeWishReasonModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
      if (!keepActiveSlot) {
        activeGuardianFreezeSlot = null;
      }
    };

    const openUnfreezeUnexpectedModal = () => {
      if (!unfreezeWishUnexpectedModal) return;
      closeUnfreezeWishReasonModalFn({ keepActiveSlot: true });
      if (unfreezeUnexpectedText) {
        unfreezeUnexpectedText.value = "";
      }
      setUnfreezeUnexpectedError(false);
      syncUnexpectedWordCount();
      unfreezeWishUnexpectedModal.classList.remove("hidden");
      unfreezeWishUnexpectedModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeUnfreezeUnexpectedModalFn = ({ keepActiveSlot = false } = {}) => {
      if (!unfreezeWishUnexpectedModal) return;
      unfreezeWishUnexpectedModal.classList.add("hidden");
      unfreezeWishUnexpectedModal.setAttribute("aria-hidden", "true");
      setUnfreezeUnexpectedError(false);
      if (unfreezeUnexpectedText) {
        unfreezeUnexpectedText.value = "";
      }
      syncUnexpectedWordCount();
      updateModalScrollLock();
      if (!keepActiveSlot) {
        activeGuardianFreezeSlot = null;
      }
    };

    const setGuardianFulfillCodeError = (show, message = "") => {
      if (!guardianFulfillCodeError) return;
      if (show && message) guardianFulfillCodeError.textContent = message;
      guardianFulfillCodeError.classList.toggle("is-visible", Boolean(show));
    };

    const setGuardianFulfillAttributionError = (show, message = "") => {
      if (!guardianFulfillAttributionError) return;
      if (show && message) guardianFulfillAttributionError.textContent = message;
      guardianFulfillAttributionError.classList.toggle("is-visible", Boolean(show));
    };

    const syncGuardianFulfillAttributionButtons = () => {
      if (guardianFulfillAttributionSecret) {
        guardianFulfillAttributionSecret.classList.toggle(
          "is-selected",
          guardianFulfillAttributionMode === "secret"
        );
      }
      if (guardianFulfillAttributionPublic) {
        guardianFulfillAttributionPublic.classList.toggle(
          "is-selected",
          guardianFulfillAttributionMode === "public"
        );
      }
    };

    const setGuardianFulfillAttributionMode = (mode) => {
      guardianFulfillAttributionMode = mode === "public" ? "public" : (mode === "secret" ? "secret" : null);
      syncGuardianFulfillAttributionButtons();
      if (guardianFulfillAttributionMode) {
        setGuardianFulfillAttributionError(false);
      }
    };

    const updateGuardianFulfillEvidencePreview = (file) => {
      if (!guardianFulfillEvidencePreview) return;
      const previewPlaceholder = guardianFulfillEvidencePreview.querySelector(".wish-preview-placeholder");
      const previewName = guardianFulfillEvidencePreview.querySelector(".wish-preview-name");

      if (guardianFulfillEvidenceUrl) {
        URL.revokeObjectURL(guardianFulfillEvidenceUrl);
        guardianFulfillEvidenceUrl = null;
      }

      if (!file) {
        guardianFulfillEvidencePreview.classList.remove("has-image");
        if (guardianFulfillEvidenceImage) {
          guardianFulfillEvidenceImage.remove();
          guardianFulfillEvidenceImage = null;
        }
        if (previewPlaceholder) previewPlaceholder.textContent = tr("Sube la evidencia visual.", "Upload visual evidence.", "Téléverser une preuve visuelle.");
        if (previewName) previewName.textContent = tr("PNG, WEBP, JPEG, etc.", "PNG, WEBP, JPEG, etc.", "PNG, WEBP, JPEG, etc.");
        return;
      }

      guardianFulfillEvidenceUrl = URL.createObjectURL(file);
      guardianFulfillEvidencePreview.classList.add("has-image");
      if (!guardianFulfillEvidenceImage) {
        guardianFulfillEvidenceImage = document.createElement("img");
        guardianFulfillEvidenceImage.className = "wish-preview-image";
        guardianFulfillEvidenceImage.alt = tr("Evidencia seleccionada", "Selected evidence", "Preuve sélectionnée");
        guardianFulfillEvidencePreview.insertBefore(
          guardianFulfillEvidenceImage,
          guardianFulfillEvidencePreview.firstChild
        );
      }
      guardianFulfillEvidenceImage.src = guardianFulfillEvidenceUrl;
      if (previewPlaceholder) previewPlaceholder.textContent = tr("Imagen seleccionada", "Selected image", "Image sélectionnée");
      if (previewName) previewName.textContent = file.name;
    };

    const openGuardianFulfillWishModal = (slot) => {
      if (!guardianFulfillModal || !slot) return;
      activeGuardianFulfillSlot = slot;
      guardianFulfillModal.classList.remove("hidden");
      guardianFulfillModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
      if (guardianFulfillEvidence) guardianFulfillEvidence.value = "";
      if (guardianFulfillCommitmentCode) guardianFulfillCommitmentCode.value = "";
      setGuardianFulfillCodeError(false);
      setGuardianFulfillAttributionError(false);
      setGuardianFulfillAttributionMode(null);
      updateGuardianFulfillEvidencePreview(null);
    };

    const closeGuardianFulfillWishModalFn = () => {
      if (!guardianFulfillModal) return;
      guardianFulfillModal.classList.add("hidden");
      guardianFulfillModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
      if (guardianFulfillEvidence) guardianFulfillEvidence.value = "";
      if (guardianFulfillCommitmentCode) guardianFulfillCommitmentCode.value = "";
      setGuardianFulfillCodeError(false);
      setGuardianFulfillAttributionError(false);
      setGuardianFulfillAttributionMode(null);
      updateGuardianFulfillEvidencePreview(null);
      activeGuardianFulfillSlot = null;
    };

    const submitGuardianFulfillWish = async () => {
      if (guardianFulfillSubmitting) return;
      const slot = activeGuardianFulfillSlot;
      const wishId = parsePositiveId(slot?.dataset?.wishId);
      if (!slot || !wishId) {
        closeGuardianFulfillWishModalFn();
        return;
      }

      const frozenBy = parsePositiveId(slot?.dataset?.frozenByUserId);
      if (!viewerUserId || !frozenBy || frozenBy !== viewerUserId) {
        window.alert(
          tr(
            "Solo el guardián que congeló este deseo puede marcarlo como cumplido.",
            "Only the guardian who froze this wish can mark it as fulfilled."
          )
        );
        closeGuardianFulfillWishModalFn();
        return;
      }

      const commitmentCode = String(guardianFulfillCommitmentCode?.value || "").trim().toUpperCase();
      let hasError = false;
      if (!commitmentCode) {
        setGuardianFulfillCodeError(true, tr("Debes indicar el código de compromiso.", "You must enter the commitment code.", "Tu dois saisir le code d'engagement."));
        hasError = true;
      }
      if (!guardianFulfillAttributionMode) {
        setGuardianFulfillAttributionError(
          true,
          tr("Debes seleccionar cómo se publicará esta concesión.", "You must choose how this granting will be published.", "Tu dois choose how this granting will be published.")
        );
        hasError = true;
      }
      if (hasError) return;

      guardianFulfillSubmitting = true;
      const oldLabel =
        guardianFulfillSubmit?.textContent || tr("Confirmar y publicar deseo cumplido", "Confirm and publish fulfilled wish", "Confirmer et publier le souhait accompli");
      if (guardianFulfillSubmit) {
        guardianFulfillSubmit.disabled = true;
        guardianFulfillSubmit.textContent = tr("Procesando...", "Processing...", "Traitement...");
      }

      try {
        const evidenceFile = guardianFulfillEvidence?.files?.[0] || null;
        const uploadedEvidence = evidenceFile ? await uploadPublicImageMedia(evidenceFile) : null;
        await fulfillPersonalWishFromGuardianRecord(wishId, {
          commitment_code: commitmentCode,
          attribution_mode: guardianFulfillAttributionMode,
          evidence_media_id: uploadedEvidence?.media_id || null,
        });
        closeGuardianFulfillWishModalFn();
        await loadPersonalWishesFromApi();
        window.dispatchEvent(new CustomEvent("kiadez:fulfilled-wishes-changed", { detail: { scope: "public" } }));
        window.alert(tr("Deseo marcado como cumplido.", "Wish marked as fulfilled.", "Souhait marqué comme accompli."));
      } catch (error) {
        console.error(error);
        window.alert(error?.message || tr("No se pudo marcar el deseo como cumplido.", "Could not mark the wish as fulfilled.", "Impossible de marquer le souhait comme accompli."));
      } finally {
        guardianFulfillSubmitting = false;
        if (guardianFulfillSubmit) {
          guardianFulfillSubmit.disabled = false;
          guardianFulfillSubmit.textContent = oldLabel;
        }
      }
    };

    const applyGuardianWishResultToActiveSlot = (wishRecord) => {
      const slot = activeGuardianFreezeSlot;
      if (!slot || !wishRecord) return;
      applyPersonalWishRecordToSlot(slot, wishRecord);
    };

    const submitFreezeFromGuardianModal = async () => {
      if (guardianFreezeSubmitting) return;
      const slot = activeGuardianFreezeSlot;
      const wishId = parsePositiveId(slot?.dataset?.wishId);
      if (!slot || !wishId) {
        closeFreezeWishConfirmModalFn();
        return;
      }

      guardianFreezeSubmitting = true;
      const oldLabel = freezeWishConfirmYes?.textContent || tr("Sí", "Yes", "Oui");
      if (freezeWishConfirmYes) {
        freezeWishConfirmYes.disabled = true;
        freezeWishConfirmYes.textContent = tr("Procesando...", "Processing...", "Traitement...");
      }

      try {
        const updatedWish = await freezePersonalWishRecord(wishId);
        applyGuardianWishResultToActiveSlot(updatedWish);
        closeFreezeWishConfirmModalFn();
      } catch (error) {
        console.error(error);
        window.alert(error?.message || tr("No se pudo congelar el deseo.", "Could not freeze the wish.", "Impossible de geler le souhait."));
      } finally {
        guardianFreezeSubmitting = false;
        if (freezeWishConfirmYes) {
          freezeWishConfirmYes.disabled = false;
          freezeWishConfirmYes.textContent = oldLabel;
        }
      }
    };

    const submitUnfreezeFromGuardianModal = async ({ reasonType, reasonText = null } = {}) => {
      if (guardianFreezeSubmitting) return false;
      const slot = activeGuardianFreezeSlot;
      const wishId = parsePositiveId(slot?.dataset?.wishId);
      if (!slot || !wishId) {
        closeUnfreezeWishReasonModalFn();
        closeUnfreezeUnexpectedModalFn();
        return false;
      }

      guardianFreezeSubmitting = true;
      const oldUnexpectedLabel = unfreezeUnexpectedSubmit?.textContent || tr("Descongelar deseo", "Unfreeze wish", "Débloquer le souhait");
      const oldErrorLabel = unfreezeReasonErrorBtn?.textContent || tr("Deseo congelado por error", "Wish frozen by mistake", "Souhait gelé par erreur");
      const oldUnexpectedBtnLabel = unfreezeReasonUnexpectedBtn?.textContent || tr("Se presentó un imprevisto", "An unexpected issue occurred", "Un problème inattendu s'est produit");

      if (unfreezeUnexpectedSubmit) {
        unfreezeUnexpectedSubmit.disabled = true;
        unfreezeUnexpectedSubmit.textContent = tr("Procesando...", "Processing...", "Traitement...");
      }
      if (unfreezeReasonErrorBtn) {
        unfreezeReasonErrorBtn.disabled = true;
        unfreezeReasonErrorBtn.textContent = tr("Procesando...", "Processing...", "Traitement...");
      }
      if (unfreezeReasonUnexpectedBtn) {
        unfreezeReasonUnexpectedBtn.disabled = true;
      }

      try {
        const updatedWish = await unfreezePersonalWishRecord(wishId, {
          reason_type: reasonType,
          reason_text: reasonText,
        });
        applyGuardianWishResultToActiveSlot(updatedWish);
        closeUnfreezeWishReasonModalFn();
        closeUnfreezeUnexpectedModalFn();
        return true;
      } catch (error) {
        console.error(error);
        window.alert(error?.message || tr("No se pudo descongelar el deseo.", "Could not unfreeze the wish.", "Impossible de débloquer le souhait."));
        return false;
      } finally {
        guardianFreezeSubmitting = false;
        if (unfreezeUnexpectedSubmit) {
          unfreezeUnexpectedSubmit.disabled = false;
          unfreezeUnexpectedSubmit.textContent = oldUnexpectedLabel;
        }
        if (unfreezeReasonErrorBtn) {
          unfreezeReasonErrorBtn.disabled = false;
          unfreezeReasonErrorBtn.textContent = oldErrorLabel;
        }
        if (unfreezeReasonUnexpectedBtn) {
          unfreezeReasonUnexpectedBtn.disabled = false;
          unfreezeReasonUnexpectedBtn.textContent = oldUnexpectedBtnLabel;
        }
      }
    };

    const openCooperativeParticipateModal = (slot, mode = "create") => {
      if (!cooperativeParticipateModal) return;
      activeParticipateMode = mode === "edit" ? "edit" : "create";
      activeParticipateSource = slot;
      const description = slot?.dataset?.rootDescription || slot?.dataset?.description || "";
      const template = slot?.dataset?.template || "";
      const existingParticipation =
        slot?.dataset?.viewerParticipationText ||
        slot?.dataset?.participationText ||
        "";
      const isEditMode = activeParticipateMode === "edit";
      if (cooperativeParticipateTitle) {
        cooperativeParticipateTitle.textContent = isEditMode
          ? tr("Editar mi participación en el deseo cooperativo", "Edit my participation in the cooperative wish", "Modifier ma participation au souhait coopératif")
          : tr("Gestión de participación en el deseo cooperativo", "Cooperative wish participation management", "Gestion de participation aux souhaits coopératifs");
      }
      if (cooperativeParticipatePrompt) {
        cooperativeParticipatePrompt.textContent = isEditMode
          ? tr("Ajusta tu texto de participación.", "Adjust your participation text.", "Ajuste le texte de ta participation.")
          : tr("¿Seguro que quieres ayudar a cumplir este deseo?", "Are you sure you want to help fulfill this wish?", "Es-tu sûr de vouloir aider à accomplir ce souhait ?");
      }
      if (cooperativeParticipateCta) {
        cooperativeParticipateCta.textContent = isEditMode
          ? tr("Guardar cambios de mi participación", "Save changes to my participation", "Enregistrer les modifications de ma participation")
          : tr("Ayudar a cumplir este deseo", "Help fulfill this wish", "Aider à accomplir ce souhait");
      }
      if (cooperativeParticipateDescription) {
        cooperativeParticipateDescription.textContent = description;
      }
      if (cooperativeParticipateQuote) {
        cooperativeParticipateQuote.textContent = template ? `“${template}”` : "";
      }
      if (cooperativeCharacter) {
        cooperativeCharacter.value = isEditMode ? existingParticipation : "";
      }
      cooperativeParticipateModal.classList.remove("hidden");
      cooperativeParticipateModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeCooperativeParticipateModalFn = () => {
      if (!cooperativeParticipateModal) return;
      cooperativeParticipateModal.classList.add("hidden");
      cooperativeParticipateModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
      activeParticipateSource = null;
      activeParticipateSlot = null;
      activeParticipateMode = "create";
      activeSecurityCode = "";
    };

    const openCooperativeSecurityModal = (slot) => {
      if (!cooperativeSecurityModal) return;
      activeSecuritySlot = slot;
      activeSecurityCode = "";
      cooperativeSecurityModal.classList.remove("hidden");
      cooperativeSecurityModal.setAttribute("aria-hidden", "false");
      if (cooperativeSecurityCodeInput) {
        cooperativeSecurityCodeInput.value = "";
      }
      if (cooperativeSecurityError) {
        cooperativeSecurityError.classList.remove("is-visible");
      }
      updateModalScrollLock();
    };

    const closeCooperativeSecurityModal = ({ clearCode = true } = {}) => {
      if (!cooperativeSecurityModal) return;
      cooperativeSecurityModal.classList.add("hidden");
      cooperativeSecurityModal.setAttribute("aria-hidden", "true");
      activeSecuritySlot = null;
      if (clearCode) {
        activeSecurityCode = "";
      }
      updateModalScrollLock();
    };

    const openCooperativeCancelParticipationModal = (slot) => {
      if (!cooperativeCancelParticipationModal || !slot) return;
      activeCooperativeCancelSlot = slot;
      cooperativeCancelParticipationModal.classList.remove("hidden");
      cooperativeCancelParticipationModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeCooperativeCancelParticipationModal = () => {
      if (!cooperativeCancelParticipationModal) return;
      cooperativeCancelParticipationModal.classList.add("hidden");
      cooperativeCancelParticipationModal.setAttribute("aria-hidden", "true");
      activeCooperativeCancelSlot = null;
      updateModalScrollLock();
    };

    const getCooperativeOwnerReviewItemsFromSlot = (slot) => {
      const raw = String(slot?.dataset?.ownerReviewItems || "").trim();
      if (!raw) return [];
      try {
        const parsed = JSON.parse(raw);
        return Array.isArray(parsed) ? parsed : [];
      } catch {
        return [];
      }
    };

    const renderCooperativeOwnerReviewModal = () => {
      if (!cooperativeOwnerReviewList || !cooperativeOwnerReviewStatus) return;
      const slot = activeCooperativeOwnerReviewSlot;
      const items = getCooperativeOwnerReviewItemsFromSlot(slot);
      const ownerCanMarkFulfilled = slot?.dataset?.ownerCanMarkFulfilled === "true";
      const pendingCount = Number(slot?.dataset?.ownerPendingValidationCount || 0);

      cooperativeOwnerReviewList.innerHTML = "";
      if (!items.length) {
        cooperativeOwnerReviewStatus.textContent = tr(
          "Aún no hay evidencias de participantes para revisar.",
          "There is no participant evidence to review yet."
        );
      } else if (pendingCount > 0) {
        cooperativeOwnerReviewStatus.textContent = tr(
          `Debes validar ${pendingCount} evidencia(s) antes de cerrar el deseo.`,
          `You must validate ${pendingCount} evidence item(s) before closing the wish.`
        );
      } else {
        cooperativeOwnerReviewStatus.textContent = tr(
          "Todas las evidencias fueron validadas. Ya puedes cerrar el deseo.",
          "All evidence has been validated. You can now close the wish."
        );
      }

      items.forEach((item) => {
        const card = document.createElement("article");
        card.className = "cooperative-review-item";

        const head = document.createElement("div");
        head.className = "cooperative-review-head";

        const avatar = document.createElement("img");
        avatar.className = "cooperative-review-avatar";
        avatar.src = item?.participant_profile_photo_url || "/assets/avatar-default.jpg";
        avatar.alt = item?.participant_handle || tr("Participante", "Participant", "Participant·e");
        head.appendChild(avatar);

        const meta = document.createElement("div");
        meta.className = "cooperative-review-meta";
        const handle = document.createElement("a");
        handle.className = "cooperative-review-handle";
        handle.href = item?.participant_profile_url || "#";
        handle.textContent = item?.participant_handle || tr("@usuario", "@user", "@utilisateur");
        if (handle.href === "#") {
          handle.removeAttribute("href");
        }
        const text = document.createElement("p");
        text.className = "cooperative-review-text";
        text.textContent = item?.participation_text || "";
        meta.appendChild(handle);
        meta.appendChild(text);
        head.appendChild(meta);

        card.appendChild(head);

        const evidenceWrap = document.createElement("div");
        evidenceWrap.className = "cooperative-review-evidence-wrap";
        const evidence = document.createElement("img");
        evidence.className = "cooperative-review-evidence";
        evidence.src = item?.evidence_media_url || "/assets/avatar-default.jpg";
        evidence.alt = tr("Evidencia de participación", "Participation evidence", "Preuve de participation");
        evidenceWrap.appendChild(evidence);
        card.appendChild(evidenceWrap);

        const actions = document.createElement("div");
        actions.className = "cooperative-review-actions";
        const validateBtn = document.createElement("button");
        validateBtn.type = "button";
        validateBtn.className = `cooperative-review-validate-btn${item?.is_validated ? " is-validated" : ""}`;
        validateBtn.dataset.participationId = `${Number(item?.participation_id || 0)}`;
        validateBtn.textContent = item?.is_validated ? tr("✅ Validado", "✅ Validated", "✅ Validé") : tr("✅ Validar", "✅ Validate", "✅ Valider");
        validateBtn.disabled = cooperativeOwnerReviewSubmitting || Boolean(item?.is_validated);
        actions.appendChild(validateBtn);
        card.appendChild(actions);

        cooperativeOwnerReviewList.appendChild(card);
      });

      if (cooperativeOwnerReviewProceed) {
        cooperativeOwnerReviewProceed.disabled = !ownerCanMarkFulfilled || cooperativeOwnerReviewSubmitting;
      }
    };

    const openCooperativeOwnerReviewModal = (slot) => {
      if (!cooperativeOwnerReviewModal || !slot) return;
      activeCooperativeOwnerReviewSlot = slot;
      cooperativeOwnerReviewModal.classList.remove("hidden");
      cooperativeOwnerReviewModal.setAttribute("aria-hidden", "false");
      renderCooperativeOwnerReviewModal();
      updateModalScrollLock();
    };

    const closeCooperativeOwnerReviewModal = () => {
      if (!cooperativeOwnerReviewModal) return;
      cooperativeOwnerReviewModal.classList.add("hidden");
      cooperativeOwnerReviewModal.setAttribute("aria-hidden", "true");
      activeCooperativeOwnerReviewSlot = null;
      cooperativeOwnerReviewSubmitting = false;
      updateModalScrollLock();
    };

    const validateParticipantEvidenceFromOwner = async (participationId) => {
      if (cooperativeOwnerReviewSubmitting) return;
      const slot = activeCooperativeOwnerReviewSlot;
      const wishId = parsePositiveId(slot?.dataset?.wishId);
      if (!slot || !wishId || !participationId) return;

      cooperativeOwnerReviewSubmitting = true;
      try {
        const updatedWish = await validateCooperativeParticipationRecord(wishId, participationId);
        applyCooperativeWishRecordToSlot(slot, updatedWish);
        renderCooperativeOwnerReviewModal();
      } catch (error) {
        openCooperativeFeedbackModal({
          title: tr("No se pudo validar", "Could not validate", "Impossible de valider"),
          message: error?.message || tr("No se pudo validar la participación.", "Could not validate the participation.", "Impossible de valider la participation."),
        });
      } finally {
        cooperativeOwnerReviewSubmitting = false;
        renderCooperativeOwnerReviewModal();
      }
    };

    const continueOwnerCooperativeFulfillFlow = () => {
      const slot = activeCooperativeOwnerReviewSlot;
      if (!slot) return;
      const ownerCanMarkFulfilled = slot.dataset.ownerCanMarkFulfilled === "true";
      if (!ownerCanMarkFulfilled) {
        openCooperativeFeedbackModal({
          title: tr("Validación pendiente", "Validation pending", "Validation en attente"),
          message: tr("Primero debes validar todas las evidencias de participación.", "You must validate all participation evidence first.", "Tu dois validate all participation evidence first."),
        });
        return;
      }
      closeCooperativeOwnerReviewModal();
      openFulfillWishModal(slot, "cooperative-final");
    };

    const openCooperativeFeedbackModal = ({
      title = tr("Información", "Information", "Informations"),
      message = "",
    } = {}) => {
      if (!cooperativeFeedbackModal) return;
      if (cooperativeFeedbackTitle) {
        cooperativeFeedbackTitle.textContent = String(title || tr("Información", "Information", "Informations")).trim() || tr("Información", "Information", "Informations");
      }
      if (cooperativeFeedbackMessage) {
        cooperativeFeedbackMessage.textContent = String(message || "").trim();
      }
      cooperativeFeedbackModal.classList.remove("hidden");
      cooperativeFeedbackModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeCooperativeFeedbackModal = () => {
      if (!cooperativeFeedbackModal) return;
      cooperativeFeedbackModal.classList.add("hidden");
      cooperativeFeedbackModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
    };

    if (closePersonalWishModal) {
      closePersonalWishModal.addEventListener("click", closePersonalWishModalFn);
    }

    if (personalWishModal) {
      personalWishModal.addEventListener("click", (event) => {
        if (event.target === personalWishModal) closePersonalWishModalFn();
      });
    }

    if (closeCooperativeWishModal) {
      closeCooperativeWishModal.addEventListener("click", closeCooperativeWishModalFn);
    }

    if (cooperativeWishModal) {
      cooperativeWishModal.addEventListener("click", (event) => {
        if (event.target === cooperativeWishModal) closeCooperativeWishModalFn();
      });
    }

    const initLifeProposalModal = () => {
      if (!lifeProposalOverlay) return;

      const aesGcmEncrypt = async (key, plaintext, aadBuf) => {
        const nonce = crypto.getRandomValues(new Uint8Array(12));
        const ptBuf = new TextEncoder().encode(plaintext).buffer;
        const ct = await crypto.subtle.encrypt(
          { name: "AES-GCM", iv: nonce, additionalData: aadBuf },
          key,
          ptBuf
        );
        return { nonce_hex: bufToHex(nonce.buffer), ciphertext_hex: bufToHex(ct) };
      };

      let pendingConfirmGroup = null;

      const openConfirmModal = (groupEl) => {
        pendingConfirmGroup = groupEl;
        if (lifeConfirmText) {
          const number = groupEl?.dataset?.purpose;
          lifeConfirmText.textContent = number
            ? tr(`¿Confirmar el propósito ${number} como público?`, `Confirm purpose ${number} as public?`, `Confirm purpose ${number} as public?`)
            : tr("¿Confirmar este deseo como público?", "Confirm this wish as public?", "Confirmer ce souhait comme public ?");
        }
        lifeConfirmOverlay?.classList.remove("hidden");
        lifeConfirmOverlay?.setAttribute("aria-hidden", "false");
        updateModalScrollLock();
      };

      const closeConfirmModal = () => {
        lifeConfirmOverlay?.classList.add("hidden");
        lifeConfirmOverlay?.setAttribute("aria-hidden", "true");
        pendingConfirmGroup = null;
        updateModalScrollLock();
      };

      lifeConfirmClose?.addEventListener("click", closeConfirmModal);
      lifeConfirmCancel?.addEventListener("click", closeConfirmModal);
      lifeConfirmOverlay?.addEventListener("click", (event) => {
        if (event.target === lifeConfirmOverlay) closeConfirmModal();
      });

      lifeConfirmOk?.addEventListener("click", () => {
        if (!pendingConfirmGroup) {
          closeConfirmModal();
          return;
        }
        pendingConfirmGroup.dataset.isPrivate = "false";
        setPurposeStatus(pendingConfirmGroup, tr("Estado: confirmado (publico).", "Status: confirmed (public).", "Statut : confirmé (public)."));
        closeConfirmModal();
      });

      lifeProposalOverlay.querySelectorAll(".purpose-group").forEach((groupEl) => {
        if (!groupEl.dataset.isPrivate) groupEl.dataset.isPrivate = "false";
      });

      lifeProposalOverlay.querySelectorAll(".purpose-actions").forEach((actionRow) => {
        actionRow.addEventListener("click", (event) => {
          const btn = event.target.closest(".purpose-action");
          if (!btn) return;

          const groupEl = btn.closest(".purpose-group");
          const action = btn.dataset.action;

          if (action === "confirm") {
            openConfirmModal(groupEl);
            return;
          }

          if (action === "secret") {
            groupEl.dataset.isPrivate = "true";
            setPurposeStatus(groupEl, tr("Estado: marcado como secreto.", "Status: marked as secret.", "Statut : marqué comme secret."));
            return;
          }

          if (action === "reveal") {
            const dateInput = groupEl.querySelector(".purpose-date");
            if (dateInput) {
              if (typeof dateInput.showPicker === "function") {
                dateInput.showPicker();
              } else {
                dateInput.focus();
                dateInput.click();
              }
            }
            return;
          }

          if (action === "icon") {
            const panel = groupEl.querySelector(".purpose-icon-panel");
            if (panel) panel.classList.toggle("is-open");
          }
        });
      });

      lifeProposalOverlay.querySelectorAll(".purpose-icon-panel").forEach((panel) => {
        panel.addEventListener("click", (event) => {
          const iconBtn = event.target.closest(".purpose-icon");
          if (!iconBtn) return;

          const groupEl = panel.closest(".purpose-group");
          const iconKey = iconBtn.dataset.icon;
          const label = getIconLabel(iconKey);
          groupEl.dataset.iconKey = iconKey;

          panel.querySelectorAll(".purpose-icon").forEach((btn) => {
            btn.classList.toggle("is-selected", btn === iconBtn);
          });

          const actionBtn = groupEl.querySelector(".purpose-action[data-action=\"icon\"]");
          if (actionBtn) {
            actionBtn.innerHTML = `<img src="${getIconSrc(iconKey)}" alt="${label}">`;
            actionBtn.title = `${tr("Icono", "Icon", "Icône")}: ${label}`;
          }

          setPurposeStatus(groupEl, `${tr("Estado: icono asociado", "Status: icon linked", "Statut : icône liée")}: ${label}.`);
          panel.classList.remove("is-open");
        });
      });

      lifeProposalOverlay.querySelectorAll(".purpose-date").forEach((dateInput) => {
        dateInput.addEventListener("change", () => {
          const groupEl = dateInput.closest(".purpose-group");
          groupEl.dataset.revealAt = dateInput.value || "";
          if (!dateInput.value) return;
          const formatted = dateInput.value.split("-").reverse().join("/");
          setPurposeStatus(groupEl, `${tr("Estado: se revelara el dia", "Status: it will be revealed on", "Statut : il sera révélé le")} ${formatted}.`);
        });
      });

      const lifeForm = lifeProposalOverlay.querySelector("#life-form");
      lifeForm?.addEventListener("submit", async (event) => {
        event.preventDefault();

        const groups = [...lifeProposalOverlay.querySelectorAll(".purpose-group")];
        const values = groups.map((groupEl) => {
          const textarea = groupEl.querySelector("textarea");
          return normalizePurposeText(textarea?.value || "");
        });
        if (values.some((value) => !value)) {
          groups.forEach((groupEl, index) => {
            if (!values[index]) {
              setPurposeStatus(groupEl, tr("Completa este propósito antes de guardar.", "Complete this purpose before saving.", "Complète cette mission avant d'enregistrer."));
            }
          });
          return;
        }

        const needsDek = groups.some((groupEl) => groupEl.dataset.isPrivate === "true");

        let dekKey = null;
        if (needsDek) {
          try {
            dekKey = await importDekFromSession();
          } catch (err) {
            groups.forEach((groupEl) => {
              if (groupEl.dataset.isPrivate === "true") {
                setPurposeStatus(groupEl, err.message || tr("No se pudo desbloquear el vault.", "Could not unlock the vault.", "Impossible de unlock the vault."));
              }
            });
            return;
          }
        }

        const slots = [];
        const localSlots = [];
        for (const [index, groupEl] of groups.entries()) {
          const text = values[index];
          const slotNumber = Number(groupEl.dataset.purpose);
          const isPrivate = groupEl.dataset.isPrivate === "true";
          const revealAt = groupEl.dataset.revealAt || null;
          const iconKey = groupEl.dataset.iconKey || null;

          if (isPrivate) {
            const encrypted = await aesGcmEncrypt(dekKey, text, AAD_PURPOSE);
            slots.push({
              slot_number: slotNumber,
              is_private: true,
              ciphertext_hex: encrypted.ciphertext_hex,
              nonce_hex: encrypted.nonce_hex,
              reveal_at: revealAt,
              icon_key: iconKey
            });
            localSlots.push({
              slot_number: slotNumber,
              is_private: true,
              reveal_at: revealAt,
              icon_key: iconKey,
              text_input: text,
              text_public: null,
              ciphertext_hex: encrypted.ciphertext_hex,
              nonce_hex: encrypted.nonce_hex,
              status: "active"
            });
          } else {
            slots.push({
              slot_number: slotNumber,
              is_private: false,
              text_public: text,
              reveal_at: revealAt,
              icon_key: iconKey
            });
            localSlots.push({
              slot_number: slotNumber,
              is_private: false,
              reveal_at: revealAt,
              icon_key: iconKey,
              text_input: text,
              text_public: text,
              ciphertext_hex: null,
              nonce_hex: null,
              status: "active"
            });
          }
        }

        const payload = { slots };
        purposeSlots = localSlots
          .map((slot) => normalizePurposeSlot(slot, Number(slot.slot_number)))
          .sort((a, b) => a.slot_number - b.slot_number);
        renderPurposeSlots(purposeSlots);
        storePurposeValues(purposeSlots);

        try {
          const res = await fetch(`${API}/life-purpose/save`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            },
            body: JSON.stringify(payload)
          });

        } catch (err) {
          console.error(err);
        }
        closeLifeProposalModal();
      });
    };

    if (!disableLegacyPurposeCover) {
      initLifeProposalModal();
      void loadPurposeFromStorage();
    }

    if (cancelDeleteWish) {
      cancelDeleteWish.addEventListener("click", closeDeleteWishModalFn);
    }

    if (deleteWishModal) {
      deleteWishModal.addEventListener("click", (event) => {
        if (event.target === deleteWishModal) closeDeleteWishModalFn();
      });
    }

    if (cancelFulfillWish) {
      cancelFulfillWish.addEventListener("click", closeFulfillWishModalFn);
    }

    if (confirmFulfillWish) {
      confirmFulfillWish.addEventListener("click", async () => {
        const slot = activeFulfillSlot;
        if (!slot) return;

        const context = activeFulfillContext || (slot.classList.contains("is-cooperative") ? "cooperative-participation" : "personal");
        const wishId = parsePositiveId(slot.dataset.wishId);
        if (!wishId) {
          closeFulfillWishModalFn();
          return;
        }

        try {
          const evidenceFile = fulfillEvidence?.files?.[0] || null;
          if (!evidenceFile && context !== "personal") {
            openCooperativeFeedbackModal({
              title: tr("Evidencia requerida", "Evidence required", "Preuve requise"),
              message: tr("Debes subir una evidencia para continuar.", "You must upload evidence to continue.", "Tu dois upload evidence to continue."),
            });
            return;
          }

          const evidenceUploader = context === "personal" ? uploadWishImage : uploadPublicImageMedia;
          const uploadedEvidence = evidenceFile ? await evidenceUploader(evidenceFile) : null;
          const evidenceMediaId = parsePositiveId(uploadedEvidence?.media_id);

          if (context === "personal") {
            await fulfillPersonalWishRecord(wishId, evidenceMediaId || null);
            resetSlotToEmpty(slot);
            closeFulfillWishModalFn();
            window.dispatchEvent(new CustomEvent("kiadez:fulfilled-wishes-changed", { detail: { scope: "public" } }));
            return;
          }

          if (!evidenceMediaId) {
            throw new Error(tr("No se pudo subir la evidencia.", "Could not upload the evidence.", "Impossible de téléverser la preuve."));
          }

          if (context === "cooperative-participation") {
            const updatedWish = await completeCooperativeParticipationRecord(wishId, {
              evidence_media_id: evidenceMediaId,
              oath_accepted: true,
            });
            applyCooperativeWishRecordToSlot(slot, updatedWish);
            closeFulfillWishModalFn();
            openCooperativeFeedbackModal({
              title: tr("Participación actualizada", "Participation updated", "Participation mise à jour"),
              message: tr("Tu evidencia de participación fue enviada.", "Your participation evidence was sent.", "La preuve de ta participation a été envoyée."),
            });
            return;
          }

          if (context === "cooperative-final") {
            await fulfillCooperativeWishRecord(wishId, {
              evidence_media_id: evidenceMediaId,
              oath_accepted: true,
            });
            closeFulfillWishModalFn();
            await loadCooperativeWishesFromApi();
            openCooperativeFeedbackModal({
              title: tr("Deseo cooperativo cumplido", "Cooperative wish fulfilled", "Souhait coopératif accompli"),
              message: tr("El deseo cooperativo fue marcado como cumplido.", "The cooperative wish was marked as fulfilled.", "Le souhait coopératif a été marqué comme accompli."),
            });
            window.dispatchEvent(new CustomEvent("kiadez:fulfilled-wishes-changed", { detail: { scope: "public-cooperative" } }));
            return;
          }
        } catch (error) {
          console.error(error);
          openCooperativeFeedbackModal({
            title: tr("No se pudo completar la acción", "Could not complete the action", "Impossible de terminer l'action"),
            message: error?.message || tr("No se pudo marcar el deseo como cumplido.", "Could not mark the wish as fulfilled.", "Impossible de marquer le souhait comme accompli."),
          });
        }
      });
    }

    if (fulfillWishModal) {
      fulfillWishModal.addEventListener("click", (event) => {
        if (event.target === fulfillWishModal) closeFulfillWishModalFn();
      });
    }

    if (icanConfirmNo) {
      icanConfirmNo.addEventListener("click", closeIcanConfirmModalFn);
    }

    if (icanConfirmYes) {
      icanConfirmYes.addEventListener("click", () => {
	        guardianRequestWishId = parsePositiveId(activeIcanSlot?.dataset?.wishId);
	        guardianRequestWishText = String(activeIcanSlot?.dataset?.description || "").trim();
        closeIcanConfirmModalFn();
        openGuardianContactModal();
      });
    }

    if (icanConfirmModal) {
      icanConfirmModal.addEventListener("click", (event) => {
        if (event.target === icanConfirmModal) closeIcanConfirmModalFn();
      });
    }

    if (cancelGuardianModal) {
      cancelGuardianModal.addEventListener("click", closeGuardianContactModalFn);
    }

    if (guardianContactModal) {
      guardianContactModal.addEventListener("click", (event) => {
        if (event.target === guardianContactModal) closeGuardianContactModalFn();
      });
    }

    if (freezeWishConfirmNo) {
      freezeWishConfirmNo.addEventListener("click", closeFreezeWishConfirmModalFn);
    }

    if (freezeWishConfirmYes) {
      freezeWishConfirmYes.addEventListener("click", () => {
        void submitFreezeFromGuardianModal();
      });
    }

    if (freezeWishConfirmModal) {
      freezeWishConfirmModal.addEventListener("click", (event) => {
        if (event.target === freezeWishConfirmModal) closeFreezeWishConfirmModalFn();
      });
    }

    if (unfreezeReasonModalClose) {
      unfreezeReasonModalClose.addEventListener("click", closeUnfreezeWishReasonModalFn);
    }

    if (unfreezeReasonCancel) {
      unfreezeReasonCancel.addEventListener("click", closeUnfreezeWishReasonModalFn);
    }

    if (unfreezeReasonErrorBtn) {
      unfreezeReasonErrorBtn.addEventListener("click", () => {
        void submitUnfreezeFromGuardianModal({ reasonType: "error", reasonText: null });
      });
    }

    if (unfreezeReasonUnexpectedBtn) {
      unfreezeReasonUnexpectedBtn.addEventListener("click", () => {
        openUnfreezeUnexpectedModal();
      });
    }

    if (unfreezeWishReasonModal) {
      unfreezeWishReasonModal.addEventListener("click", (event) => {
        if (event.target === unfreezeWishReasonModal) closeUnfreezeWishReasonModalFn();
      });
    }

    if (unfreezeUnexpectedModalClose) {
      unfreezeUnexpectedModalClose.addEventListener("click", closeUnfreezeUnexpectedModalFn);
    }

    if (unfreezeUnexpectedCancel) {
      unfreezeUnexpectedCancel.addEventListener("click", closeUnfreezeUnexpectedModalFn);
    }

    if (unfreezeWishUnexpectedModal) {
      unfreezeWishUnexpectedModal.addEventListener("click", (event) => {
        if (event.target === unfreezeWishUnexpectedModal) closeUnfreezeUnexpectedModalFn();
      });
    }

    if (unfreezeUnexpectedText) {
      unfreezeUnexpectedText.addEventListener("input", () => {
        setUnfreezeUnexpectedError(false);
        syncUnexpectedWordCount();
      });
    }

    if (unfreezeUnexpectedSubmit) {
      unfreezeUnexpectedSubmit.addEventListener("click", () => {
        const text = String(unfreezeUnexpectedText?.value || "").trim();
        const words = countWords(text);
        if (!text) {
          setUnfreezeUnexpectedError(true, tr("Debes describir el imprevisto para descongelar el deseo.", "You must describe the issue to unfreeze the wish.", "Tu dois décrire le problème pour débloquer le souhait."));
          unfreezeUnexpectedText?.focus();
          return;
        }
        if (words > 100) {
          setUnfreezeUnexpectedError(true, tr("La explicación no puede superar 100 palabras.", "The explanation cannot exceed 100 words.", "L'explication ne peut pas dépasser 100 mots."));
          unfreezeUnexpectedText?.focus();
          return;
        }
        void submitUnfreezeFromGuardianModal({ reasonType: "unexpected", reasonText: text });
      });
    }

    if (guardianFulfillClose) {
      guardianFulfillClose.addEventListener("click", closeGuardianFulfillWishModalFn);
    }

    if (guardianFulfillCancel) {
      guardianFulfillCancel.addEventListener("click", closeGuardianFulfillWishModalFn);
    }

    if (guardianFulfillModal) {
      guardianFulfillModal.addEventListener("click", (event) => {
        if (event.target === guardianFulfillModal) closeGuardianFulfillWishModalFn();
      });
    }

    if (guardianFulfillEvidence) {
      guardianFulfillEvidence.addEventListener("change", () => {
        const file = guardianFulfillEvidence.files && guardianFulfillEvidence.files[0];
        updateGuardianFulfillEvidencePreview(file || null);
      });
    }

    if (guardianFulfillCommitmentCode) {
      guardianFulfillCommitmentCode.addEventListener("input", () => {
        guardianFulfillCommitmentCode.value = guardianFulfillCommitmentCode.value.toUpperCase().replace(/\s+/g, "");
        if (String(guardianFulfillCommitmentCode.value || "").trim()) {
          setGuardianFulfillCodeError(false);
        }
      });
    }

    if (guardianFulfillAttributionSecret) {
      guardianFulfillAttributionSecret.addEventListener("click", () => {
        setGuardianFulfillAttributionMode("secret");
      });
    }

    if (guardianFulfillAttributionPublic) {
      guardianFulfillAttributionPublic.addEventListener("click", () => {
        setGuardianFulfillAttributionMode("public");
      });
    }

    if (guardianFulfillSubmit) {
      guardianFulfillSubmit.addEventListener("click", () => {
        void submitGuardianFulfillWish();
      });
    }

	    if (guardianEvidenceInput) {
	      guardianEvidenceInput.addEventListener("change", () => {
	        const file = guardianEvidenceInput.files && guardianEvidenceInput.files[0];
	        updateGuardianEvidencePreview(file || null);
	        if (file) setGuardianFieldError(null, guardianEvidenceError, false);
	        if (file) guardianEvidenceRow?.classList.remove("is-error");
	      });
	    }

	    if (guardianReasonVisitor) {
	      guardianReasonVisitor.addEventListener("input", () => {
	        if (String(guardianReasonVisitor.value || "").trim()) {
	          setGuardianFieldError(guardianReasonVisitor, guardianReasonError, false);
	        }
	      });
	    }

	    if (guardianPhoneVisitor) {
	      guardianPhoneVisitor.addEventListener("input", () => {
	        if (String(guardianPhoneVisitor.value || "").trim()) {
	          setGuardianFieldError(guardianPhoneVisitor, guardianPhoneError, false);
	        }
	      });
	    }

	    if (guardianEmailVisitor) {
	      guardianEmailVisitor.addEventListener("input", () => {
	        const email = String(guardianEmailVisitor.value || "").trim();
	        if (email && guardianEmailVisitor.checkValidity()) {
	          setGuardianFieldError(guardianEmailVisitor, guardianEmailError, false);
	        }
	      });
	    }

	    if (guardianSelect) {
	      guardianSelect.addEventListener("click", (event) => {
	        const option = event.target.closest(".guardian-option");
	        if (!option || !guardianSelect.contains(option)) return;
	        const nextId = parsePositiveId(option.dataset.guardianUserId);
	        if (!nextId) return;
	        selectedGuardianUserId = nextId;
	        guardianSelect.querySelectorAll(".guardian-option").forEach((el) => {
	          const id = parsePositiveId(el.dataset.guardianUserId);
	          const isSelected = Boolean(id && id === selectedGuardianUserId);
	          el.classList.toggle("is-selected", isSelected);
	          if (isSelected) {
	            el.setAttribute("aria-current", "true");
	          } else {
	            el.removeAttribute("aria-current");
	          }
	        });
	      });
	    }

	    if (guardianSendBtn) {
	      guardianSendBtn.addEventListener("click", () => {
	        void submitGuardianWishRequest();
	      });
	    }

    if (cancelCooperativeParticipate) {
      cancelCooperativeParticipate.addEventListener("click", closeCooperativeParticipateModalFn);
    }

    if (cooperativeParticipateModal) {
      cooperativeParticipateModal.addEventListener("click", (event) => {
        if (event.target === cooperativeParticipateModal) closeCooperativeParticipateModalFn();
      });
    }

    if (cooperativeSecurityModal) {
      cooperativeSecurityModal.addEventListener("click", (event) => {
        if (event.target === cooperativeSecurityModal) closeCooperativeSecurityModal();
      });
    }

    if (cooperativeCancelParticipationNo) {
      cooperativeCancelParticipationNo.addEventListener("click", closeCooperativeCancelParticipationModal);
    }

    if (cooperativeCancelParticipationYes) {
      cooperativeCancelParticipationYes.addEventListener("click", async () => {
        const slot = activeCooperativeCancelSlot;
        const wishId = parsePositiveId(slot?.dataset?.wishId);
        if (!slot || !wishId) {
          closeCooperativeCancelParticipationModal();
          return;
        }

        const oldLabel = cooperativeCancelParticipationYes.textContent || tr("Sí", "Yes", "Oui");
        cooperativeCancelParticipationYes.disabled = true;
        cooperativeCancelParticipationYes.textContent = tr("Procesando...", "Processing...", "Traitement...");
        try {
          const updatedWish = await cancelCooperativeParticipationRecord(wishId);
          applyCooperativeWishRecordToSlot(slot, updatedWish);
          closeCooperativeCancelParticipationModal();
          window.alert(tr("Tu participación fue cancelada.", "Your participation was canceled.", "Ta participation a été annulée."));
        } catch (error) {
          window.alert(error?.message || tr("No se pudo cancelar tu participación.", "Could not cancel your participation.", "Impossible d'annuler ta participation."));
        } finally {
          cooperativeCancelParticipationYes.disabled = false;
          cooperativeCancelParticipationYes.textContent = oldLabel;
        }
      });
    }

    if (cooperativeCancelParticipationModal) {
      cooperativeCancelParticipationModal.addEventListener("click", (event) => {
        if (event.target === cooperativeCancelParticipationModal) closeCooperativeCancelParticipationModal();
      });
    }

    if (cooperativeOwnerReviewClose) {
      cooperativeOwnerReviewClose.addEventListener("click", closeCooperativeOwnerReviewModal);
    }

    if (cooperativeOwnerReviewCancel) {
      cooperativeOwnerReviewCancel.addEventListener("click", closeCooperativeOwnerReviewModal);
    }

    if (cooperativeOwnerReviewProceed) {
      cooperativeOwnerReviewProceed.addEventListener("click", continueOwnerCooperativeFulfillFlow);
    }

    if (cooperativeOwnerReviewList) {
      cooperativeOwnerReviewList.addEventListener("click", (event) => {
        const validateBtn = event.target.closest(".cooperative-review-validate-btn");
        if (!validateBtn) return;
        const participationId = parsePositiveId(validateBtn.dataset.participationId);
        if (!participationId) return;
        void validateParticipantEvidenceFromOwner(participationId);
      });
    }

    if (cooperativeOwnerReviewModal) {
      cooperativeOwnerReviewModal.addEventListener("click", (event) => {
        if (event.target === cooperativeOwnerReviewModal) closeCooperativeOwnerReviewModal();
      });
    }

    if (cooperativeFeedbackClose) {
      cooperativeFeedbackClose.addEventListener("click", closeCooperativeFeedbackModal);
    }

    if (cooperativeFeedbackModal) {
      cooperativeFeedbackModal.addEventListener("click", (event) => {
        if (event.target === cooperativeFeedbackModal) closeCooperativeFeedbackModal();
      });
    }

	    if (guardianPrevPage) {
	      guardianPrevPage.addEventListener("click", () => {
	        if (guardiansLoading) return;
	        if (guardiansPage <= 1) return;
	        void loadGuardiansPage(guardiansPage - 1);
	      });
	    }

	    if (guardianNextPage) {
	      guardianNextPage.addEventListener("click", () => {
	        if (guardiansLoading) return;
	        if (guardiansPage >= guardiansTotalPages) return;
	        void loadGuardiansPage(guardiansPage + 1);
	      });
	    }

    const updateFulfillEvidencePreview = (file) => {
      if (!fulfillEvidencePreview) return;
      const previewPlaceholder = fulfillEvidencePreview.querySelector(".wish-preview-placeholder");
      const previewName = fulfillEvidencePreview.querySelector(".wish-preview-name");

      if (fulfillEvidenceUrl) {
        URL.revokeObjectURL(fulfillEvidenceUrl);
        fulfillEvidenceUrl = null;
      }

      if (!file) {
        fulfillEvidencePreview.classList.remove("has-image");
        if (fulfillEvidenceImage) {
          fulfillEvidenceImage.remove();
          fulfillEvidenceImage = null;
        }
        if (previewPlaceholder) {
          previewPlaceholder.textContent = tr("Sube la evidencia visual.", "Upload visual evidence.", "Téléverser une preuve visuelle.");
        }
        if (previewName) {
          previewName.textContent = tr("PNG, WEBP, JPEG, etc.", "PNG, WEBP, JPEG, etc.", "PNG, WEBP, JPEG, etc.");
        }
        return;
      }

      fulfillEvidenceUrl = URL.createObjectURL(file);
      fulfillEvidencePreview.classList.add("has-image");
      if (!fulfillEvidenceImage) {
        fulfillEvidenceImage = document.createElement("img");
        fulfillEvidenceImage.className = "wish-preview-image";
        fulfillEvidenceImage.alt = tr("Evidencia seleccionada", "Selected evidence", "Preuve sélectionnée");
        fulfillEvidencePreview.insertBefore(fulfillEvidenceImage, fulfillEvidencePreview.firstChild);
      }
      fulfillEvidenceImage.src = fulfillEvidenceUrl;
      if (previewPlaceholder) {
        previewPlaceholder.textContent = tr("Imagen seleccionada", "Selected image", "Image sélectionnée");
      }
      if (previewName) {
        previewName.textContent = file.name;
      }
    };

    if (fulfillEvidence) {
      fulfillEvidence.addEventListener("change", () => {
        const file = fulfillEvidence.files && fulfillEvidence.files[0];
        updateFulfillEvidencePreview(file || null);
      });
    }

    const updateCooperativePreview = (file) => {
      if (!cooperativeWishPreview) return;
      const previewPlaceholder = cooperativeWishPreview.querySelector(".wish-preview-placeholder");

      if (cooperativePreviewUrl) {
        URL.revokeObjectURL(cooperativePreviewUrl);
        cooperativePreviewUrl = null;
      }

      if (!file) {
        cooperativeWishPreview.classList.remove("has-image");
        if (cooperativePreviewImage) {
          cooperativePreviewImage.remove();
          cooperativePreviewImage = null;
        }
        if (previewPlaceholder) {
          previewPlaceholder.textContent = tr("Seleccionar imagen", "Select image", "Sélectionner une image");
        }
        if (cooperativeWishFileName) {
          cooperativeWishFileName.textContent = tr("Sin imagen seleccionada", "No image selected", "Aucune image sélectionnée");
        }
        return;
      }

      cooperativePreviewUrl = URL.createObjectURL(file);
      cooperativeWishPreview.classList.add("has-image");
      if (!cooperativePreviewImage) {
        cooperativePreviewImage = document.createElement("img");
        cooperativePreviewImage.className = "wish-preview-image";
        cooperativePreviewImage.alt = tr("Vista previa de la imagen seleccionada", "Selected image preview", "Aperçu de l'image sélectionnée");
        cooperativeWishPreview.insertBefore(cooperativePreviewImage, cooperativeWishPreview.firstChild);
      }
      cooperativePreviewImage.src = cooperativePreviewUrl;
      if (previewPlaceholder) {
        previewPlaceholder.textContent = tr("Imagen seleccionada", "Selected image", "Image sélectionnée");
      }
      if (cooperativeWishFileName) {
        cooperativeWishFileName.textContent = file.name;
      }
    };

    const setCooperativePreviewFromUrl = (url, label) => {
      if (!cooperativeWishPreview) return;
      const previewPlaceholder = cooperativeWishPreview.querySelector(".wish-preview-placeholder");

      if (cooperativePreviewUrl) {
        URL.revokeObjectURL(cooperativePreviewUrl);
        cooperativePreviewUrl = null;
      }

      if (!url) {
        updateCooperativePreview(null);
        return;
      }

      cooperativeWishPreview.classList.add("has-image");
      if (!cooperativePreviewImage) {
        cooperativePreviewImage = document.createElement("img");
        cooperativePreviewImage.className = "wish-preview-image";
        cooperativePreviewImage.alt = tr("Vista previa de la imagen seleccionada", "Selected image preview", "Aperçu de l'image sélectionnée");
        cooperativeWishPreview.insertBefore(cooperativePreviewImage, cooperativeWishPreview.firstChild);
      }
      cooperativePreviewImage.src = url;
      if (previewPlaceholder) {
        previewPlaceholder.textContent = tr("Imagen seleccionada", "Selected image", "Image sélectionnée");
      }
      if (cooperativeWishFileName) {
        cooperativeWishFileName.textContent = label || tr("Imagen actual", "Current image", "Image actuelle");
      }
    };

    if (cooperativeWishMedia) {
      cooperativeWishMedia.addEventListener("change", () => {
        const file = cooperativeWishMedia.files && cooperativeWishMedia.files[0];
        updateCooperativePreview(file || null);
      });
    }

    if (personalWishAdd) {
      personalWishAdd.addEventListener("click", () => {
        addLampSlot();
      });
    }

    if (cooperativeWishAdd) {
      cooperativeWishAdd.addEventListener("click", () => {
        addCooperativeSlot();
      });
    }

    const updatePersonalPreview = (file) => {
      if (!personalWishPreview) return;
      const previewPlaceholder = personalWishPreview.querySelector(".wish-preview-placeholder");

      if (personalPreviewUrl) {
        URL.revokeObjectURL(personalPreviewUrl);
        personalPreviewUrl = null;
      }

      if (!file) {
        personalWishPreview.classList.remove("has-image");
        if (personalPreviewImage) {
          personalPreviewImage.remove();
          personalPreviewImage = null;
        }
        if (previewPlaceholder) {
          previewPlaceholder.textContent = tr("Seleccionar imagen", "Select image", "Sélectionner une image");
        }
        if (personalWishFileName) {
          personalWishFileName.textContent = tr("Sin imagen seleccionada", "No image selected", "Aucune image sélectionnée");
        }
        return;
      }

      personalPreviewUrl = URL.createObjectURL(file);
      personalWishPreview.classList.add("has-image");
      if (!personalPreviewImage) {
        personalPreviewImage = document.createElement("img");
        personalPreviewImage.className = "wish-preview-image";
        personalPreviewImage.alt = tr("Vista previa de la imagen seleccionada", "Selected image preview", "Aperçu de l'image sélectionnée");
        personalWishPreview.insertBefore(personalPreviewImage, personalWishPreview.firstChild);
      }
      personalPreviewImage.src = personalPreviewUrl;
      if (previewPlaceholder) {
        previewPlaceholder.textContent = tr("Imagen seleccionada", "Selected image", "Image sélectionnée");
      }
      if (personalWishFileName) {
        personalWishFileName.textContent = file.name;
      }
    };

    const setPersonalPreviewFromUrl = (url, label) => {
      if (!personalWishPreview) return;
      const previewPlaceholder = personalWishPreview.querySelector(".wish-preview-placeholder");

      if (personalPreviewUrl) {
        URL.revokeObjectURL(personalPreviewUrl);
        personalPreviewUrl = null;
      }

      if (!url) {
        updatePersonalPreview(null);
        return;
      }

      personalWishPreview.classList.add("has-image");
      if (!personalPreviewImage) {
        personalPreviewImage = document.createElement("img");
        personalPreviewImage.className = "wish-preview-image";
        personalPreviewImage.alt = tr("Vista previa de la imagen seleccionada", "Selected image preview", "Aperçu de l'image sélectionnée");
        personalWishPreview.insertBefore(personalPreviewImage, personalWishPreview.firstChild);
      }
      personalPreviewImage.src = url;
      if (previewPlaceholder) {
        previewPlaceholder.textContent = tr("Imagen seleccionada", "Selected image", "Image sélectionnée");
      }
      if (personalWishFileName) {
        personalWishFileName.textContent = label || tr("Imagen actual", "Current image", "Image actuelle");
      }
    };

    if (personalWishMedia) {
      personalWishMedia.addEventListener("change", () => {
        const file = personalWishMedia.files && personalWishMedia.files[0];
        updatePersonalPreview(file || null);
      });
    }

    const getPersonalWishDescription = () => {
      if (!personalWishText) return "";
      const prefix = personalWishText.dataset.prefix || "";
      const value = personalWishText.value || "";
      if (prefix && value.startsWith(prefix)) {
        return value.slice(prefix.length).trim();
      }
      return value.trim();
    };

    const isPersonalWishValid = () => getPersonalWishDescription().length > 0;
    const getCooperativeWishDescription = () => {
      if (!cooperativeWishText) return "";
      const prefix = cooperativeWishText.dataset.prefix || "";
      const value = cooperativeWishText.value || "";
      if (prefix && value.startsWith(prefix)) {
        return value.slice(prefix.length).trim();
      }
      return value.trim();
    };
    const isCooperativeWishValid = () => getCooperativeWishDescription().length > 0;

    const defaultPersonalWishErrorText = personalWishError?.textContent || tr("No has descrito tu deseo", "You have not described your wish", "Tu n'as pas décrit ton souhait");
    const defaultCooperativeWishErrorText =
      cooperativeWishError?.textContent || tr("No has descrito tu deseo cooperativo.", "You have not described your cooperative wish.", "Tu n'as pas décrit ton souhait coopératif.");

    const setPersonalWishError = (show, message = "") => {
      if (!personalWishError) return;
      personalWishError.textContent = show
        ? (message || defaultPersonalWishErrorText)
        : defaultPersonalWishErrorText;
      personalWishError.classList.toggle("is-visible", show);
    };

    const setCooperativeWishError = (show, message = "") => {
      if (!cooperativeWishError) return;
      cooperativeWishError.textContent = show
        ? (message || defaultCooperativeWishErrorText)
        : defaultCooperativeWishErrorText;
      cooperativeWishError.classList.toggle("is-visible", show);
    };

    if (personalWishText) {
      personalWishText.addEventListener("input", () => {
        setPersonalWishError(!isPersonalWishValid());
      });
    }

    if (cooperativeWishText) {
      cooperativeWishText.addEventListener("input", () => {
        if (isCooperativeWishValid()) setCooperativeWishError(false);
      });
    }

    const createWishActionBtn = (src, label, action) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "wish-icon-btn";
      button.title = label;
      if (action) {
        button.dataset.action = action;
        button.setAttribute("aria-label", label);
      }
      const img = document.createElement("img");
      img.src = src;
      img.alt = label;
      button.appendChild(img);
      return button;
    };

    const createVisitorIcon = () => {
      const icon = document.createElement("div");
      icon.className = "wish-icon-btn wish-icon-static";
      icon.dataset.action = "ican";
      icon.setAttribute("aria-label", tr("Yo puedo cumplir ese deseo", "I can fulfill this wish", "Je peux accomplir ce souhait"));
      icon.title = tr("Yo puedo cumplir ese deseo", "I can fulfill this wish", "Je peux accomplir ce souhait");
      const img = document.createElement("img");
      img.src = "/css/icons/iconican.webp";
      img.alt = tr("Yo puedo cumplir ese deseo", "I can fulfill this wish", "Je peux accomplir ce souhait");
      icon.appendChild(img);
      return icon;
    };

	    const createFreezeWishBtn = (mode = "freeze") => {
	      const isUnfreeze = mode === "unfreeze";
	      const title = isUnfreeze ? tr("Descongelar deseo", "Unfreeze wish", "Débloquer le souhait") : tr("Congelar deseo", "Freeze wish", "Geler le souhait");
	      const iconSrc = isUnfreeze ? "/css/icons/unfrezee.webp" : "/css/icons/freeze.webp";
	      const btn = document.createElement("button");
	      btn.type = "button";
	      btn.className = `wish-icon-btn wish-freeze-btn${isUnfreeze ? " is-unfreeze" : ""}`;
	      btn.dataset.action = isUnfreeze ? "guardian-unfreeze" : "guardian-freeze";
	      btn.setAttribute("aria-label", title);
	      btn.title = title;

	      const img = document.createElement("img");
	      img.src = iconSrc;
	      img.alt = title;
	      btn.appendChild(img);
	      return btn;
	    };

    const createVisitorCooperativeIcon = (hasParticipation = false) => {
      const title = hasParticipation
        ? tr("Editar mi participación en este deseo", "Edit my participation in this wish", "Modifier ma participation à ce souhait")
        : tr("Yo puedo ayudar a cumplir este deseo", "I can help fulfill this wish", "Je peux aider à accomplir ce souhait");
      const icon = document.createElement("div");
      icon.className = "wish-icon-btn wish-icon-static";
      icon.dataset.action = "help-coop";
      icon.setAttribute("aria-label", title);
      icon.title = title;
      const img = document.createElement("img");
      img.src = "/css/icons/iconcooperative2.webp";
      img.alt = title;
      icon.appendChild(img);
      return icon;
    };

    const resetSlotToEmpty = (slot) => {
      if (!slot || !lampSlotTemplate) return;
      if (slot.dataset.imageUrl && slot.dataset.imageObjectUrl === "true") {
        URL.revokeObjectURL(slot.dataset.imageUrl);
      }
      delete slot.dataset.imageUrl;
      delete slot.dataset.imageObjectUrl;
      delete slot.dataset.description;
      delete slot.dataset.type;
      delete slot.dataset.goal;
      delete slot.dataset.current;
      delete slot.dataset.template;
      delete slot.dataset.securityCode;
      delete slot.dataset.viewerParticipationText;
      delete slot.dataset.viewerParticipationStatus;
      delete slot.dataset.viewerParticipationHasEvidence;
      delete slot.dataset.viewerParticipationValidatedAt;
      delete slot.dataset.ownerPendingValidationCount;
      delete slot.dataset.ownerCanMarkFulfilled;
      delete slot.dataset.ownerReviewItems;
      delete slot.dataset.isFulfilled;
      delete slot.dataset.participationText;
      delete slot.dataset.rootDescription;
      delete slot.dataset.rootImageUrl;
      delete slot.dataset.rootUser;
      delete slot.dataset.wishId;
      delete slot.dataset.mediaId;
      delete slot.dataset.frozen;
      delete slot.dataset.frozenByUserId;
      delete slot.dataset.frozenByGuardianName;
      delete slot.dataset.frozenByGuardianProfileUrl;
      slot.classList.remove("is-choosing", "is-filled", "is-frozen", "is-frozen-opaque", "is-frozen-soft");
      slot.classList.add("is-empty");
      slot.innerHTML = "";
      slot.appendChild(lampSlotTemplate.content.cloneNode(true));
    };

    const renderPersonalWishSlot = (slot, description, imageUrl, type) => {
      if (!slot) return;
      if (slot.dataset.imageUrl && slot.dataset.imageObjectUrl === "true") {
        URL.revokeObjectURL(slot.dataset.imageUrl);
      }
      delete slot.dataset.imageUrl;
      delete slot.dataset.imageObjectUrl;

      slot.classList.remove("is-empty", "is-choosing", "is-frozen", "is-frozen-opaque", "is-frozen-soft");
      slot.classList.add("is-filled");
      slot.innerHTML = "";
      slot.dataset.description = description;
      if (type) {
        slot.dataset.type = type;
      }

	      const wishId = parsePositiveId(slot?.dataset?.wishId);
	      const isFrozen = Boolean(wishId && slot?.dataset?.frozen === "true");
	      const frozenByUserId = parsePositiveId(slot?.dataset?.frozenByUserId);
	      const isFrozenByMe = Boolean(isFrozen && viewerUserId && frozenByUserId === viewerUserId);

      const row = document.createElement("div");
      row.className = "wish-slot-row";

      const body = document.createElement("div");
      body.className = "wish-slot-body";

      const leftCol = document.createElement("div");
      leftCol.className = "wish-slot-left";

      const header = document.createElement("div");
      header.className = "wish-slot-header";

      const selectedType = type || Array.from(personalWishTypeInputs).find((input) => input.checked)?.value || "Espiritual";
      const categoryIconSrc = personalTypeIconMap[selectedType] || personalTypeIconMap["Espiritual"];
      const categoryIcon = document.createElement("img");
      categoryIcon.className = "wish-slot-category-icon";
      categoryIcon.src = categoryIconSrc;
      categoryIcon.alt = selectedType;
      header.appendChild(categoryIcon);

      const title = document.createElement("div");
      title.className = "wish-slot-title";
      title.textContent = description;
      header.appendChild(document.createElement("br"));
      header.appendChild(title);

      leftCol.appendChild(header);

      const actions = document.createElement("div");
      actions.className = "wish-slot-actions wish-slot-actions-inline";
      const canUseGuardianActions = Boolean(viewerIsGuardian && wishId);
      if (!isViewingOwnProfile) {
        actions.appendChild(createVisitorIcon());
      }
      if (isViewingOwnProfile) {
        actions.appendChild(createWishActionBtn("/css/icons/iconedit.webp", tr("Editar deseo", "Edit wish", "Modifier le souhait"), "edit"));
        actions.appendChild(createWishActionBtn("/css/icons/iconfulfill.webp", tr("Marcar como cumplido", "Mark as fulfilled", "Marquer comme accompli"), "fulfill"));
        actions.appendChild(createWishActionBtn("/css/icons/icondelete.webp", tr("Borrar deseo", "Delete wish", "Supprimer le souhait"), "delete"));
      }
      if (canUseGuardianActions && !isFrozen) {
        actions.appendChild(createFreezeWishBtn("freeze"));
      }
      leftCol.appendChild(actions);
      body.appendChild(leftCol);

      if (imageUrl) {
        const imageWrap = document.createElement("div");
        imageWrap.className = "wish-slot-image-wrap";
        const img = document.createElement("img");
        img.className = "wish-slot-image";
        img.src = imageUrl;
        img.alt = tr("Imagen del deseo", "Wish image", "Image du souhait");
        imageWrap.appendChild(img);
        body.appendChild(imageWrap);
        slot.dataset.imageUrl = imageUrl;
        slot.dataset.imageObjectUrl = imageUrl.startsWith("blob:") ? "true" : "false";
      } else {
        body.classList.add("single");
      }

	      row.appendChild(body);
	      slot.appendChild(row);

	      if (isFrozen) {
	        const softMode = isViewingOwnProfile || isFrozenByMe;
	        const canManageFrozenWish = Boolean(viewerIsGuardian && isFrozenByMe && wishId);
	        slot.classList.add("is-frozen", softMode ? "is-frozen-soft" : "is-frozen-opaque");

	        const overlay = document.createElement("div");
	        overlay.className = `wish-freeze-overlay ${softMode ? "is-soft" : "is-opaque"}${canManageFrozenWish ? " is-interactive" : ""}`;
	        overlay.setAttribute("aria-label", FROZEN_WISH_MESSAGE);

	        const card = document.createElement("div");
	        card.className = "wish-freeze-card";
	        if (!canManageFrozenWish) {
	          card.textContent = FROZEN_WISH_MESSAGE;
	        } else {
	          const content = document.createElement("div");
	          content.className = "wish-freeze-card-content";

	          const text = document.createElement("span");
	          text.className = "wish-freeze-card-message";
	          text.textContent = FROZEN_WISH_MESSAGE;
	          content.appendChild(text);

	          const overlayActions = document.createElement("div");
	          overlayActions.className = "wish-freeze-overlay-actions";
	          overlayActions.appendChild(createFreezeWishBtn("unfreeze"));
		          overlayActions.appendChild(
		            createWishActionBtn(
		              "/css/icons/iconfulfill.webp",
		              tr("Marcar deseo como cumplido (Guardián)", "Mark wish as fulfilled (Guardian)", "Marquer le souhait comme accompli (Gardien)"),
		              "guardian-fulfill"
		            )
		          );
	          content.appendChild(overlayActions);
	          card.appendChild(content);
	        }
	        overlay.appendChild(card);

	        slot.appendChild(overlay);
	      }
    };

    const parsePositiveId = (value) => {
      const id = Number(value || 0);
      return Number.isFinite(id) && id > 0 ? id : null;
    };

    const FROZEN_WISH_MESSAGE = tr(
      "Este deseo está siendo auditado por un guardián y posiblemente se cumpla pronto.",
      "This wish is being audited by a guardian and may be fulfilled soon."
    );

    const countWords = (text) => {
      return String(text || "")
        .trim()
        .split(/\s+/)
        .filter(Boolean).length;
    };

    const setUnfreezeUnexpectedError = (show, message = "") => {
      if (!unfreezeUnexpectedError) return;
      if (show && message) {
        unfreezeUnexpectedError.textContent = message;
      }
      unfreezeUnexpectedError.classList.toggle("is-visible", Boolean(show));
    };

    const syncUnexpectedWordCount = () => {
      if (!unfreezeUnexpectedWordCount || !unfreezeUnexpectedText) return;
      const words = countWords(unfreezeUnexpectedText.value);
      unfreezeUnexpectedWordCount.textContent = tr(`${words} / 100 palabras`, `${words} / 100 words`, `${words} / 100 words`);
      unfreezeUnexpectedWordCount.classList.toggle("is-error", words > 100);
    };

    const applyFrozenDatasetToSlotFromRecord = (slot, wish) => {
      if (!slot) return;
      const isFrozen = Boolean(wish?.is_frozen);
      if (!isFrozen) {
        delete slot.dataset.frozen;
        delete slot.dataset.frozenByUserId;
        delete slot.dataset.frozenByGuardianName;
        delete slot.dataset.frozenByGuardianProfileUrl;
        return;
      }

      slot.dataset.frozen = "true";
      const frozenBy = parsePositiveId(wish?.frozen_by_guardian_id);
      if (frozenBy) {
        slot.dataset.frozenByUserId = `${frozenBy}`;
      } else {
        delete slot.dataset.frozenByUserId;
      }

      const guardianName = String(wish?.frozen_by_guardian_full_name || "").trim();
      if (guardianName) {
        slot.dataset.frozenByGuardianName = guardianName;
      } else {
        delete slot.dataset.frozenByGuardianName;
      }

      const guardianProfileUrl = String(wish?.frozen_by_guardian_profile_url || "").trim();
      if (guardianProfileUrl) {
        slot.dataset.frozenByGuardianProfileUrl = guardianProfileUrl;
      } else {
        delete slot.dataset.frozenByGuardianProfileUrl;
      }
    };

    const applyPersonalWishRecordToSlot = (slot, wish) => {
      if (!slot || !wish) return;
      const wishId = parsePositiveId(wish.id);
      const mediaId = parsePositiveId(wish.media_id);
      if (wishId) {
        slot.dataset.wishId = `${wishId}`;
      } else {
        delete slot.dataset.wishId;
      }
      applyFrozenDatasetToSlotFromRecord(slot, wish);
      if (mediaId) {
        slot.dataset.mediaId = `${mediaId}`;
      } else {
        delete slot.dataset.mediaId;
      }
      renderPersonalWishSlot(slot, wish.wish_text || "", wish.media_url || null, wish.wish_type || "Espiritual");
    };

    const clearPersonalSlots = () => {
      if (!personalWishList) return;
      personalWishList.innerHTML = "";
      personalTotal = 0;
      if (personalWishAdd) {
        personalWishAdd.disabled = false;
      }
    };

    const hydratePersonalSlots = (items) => {
      if (!personalWishList) return;
      const records = Array.isArray(items) ? items : [];
      clearPersonalSlots();
      const totalSlots = Math.max(personalMin, Math.min(personalMax, records.length));
      for (let i = 0; i < totalSlots; i += 1) {
        addLampSlot();
      }
      const slots = Array.from(personalWishList.querySelectorAll(".wish-slot"));
      records.forEach((wish, index) => {
        const slot = slots[index];
        if (!slot) return;
        applyPersonalWishRecordToSlot(slot, wish);
      });

	      if (highlightWishId) {
	        const targetWishId = highlightWishId;
	        requestAnimationFrame(() => {
	          const allSlots = Array.from(personalWishList.querySelectorAll(".wish-slot"));
	          const targetSlot = allSlots.find((slotEl) => parsePositiveId(slotEl?.dataset?.wishId) === targetWishId);
	          highlightWishId = null;
	          if (!targetSlot) return;
	          targetSlot.classList.add("wish-slot-highlight");
	          try {
	            targetSlot.scrollIntoView({ behavior: "smooth", block: "center" });
	          } catch {
	            targetSlot.scrollIntoView();
	          }
	          window.setTimeout(() => {
	            targetSlot.classList.remove("wish-slot-highlight");
	          }, 3500);
	        });
	      }
    };

    const loadPersonalWishesFromApi = async () => {
      try {
        const data = await fetchPersonalWishList();
        hydratePersonalSlots(data?.items || []);
      } catch (error) {
        console.error(error);
      }
    };

    const applyCooperativeWishRecordToSlot = (slot, wish) => {
      if (!slot || !wish) return;
      const wishId = parsePositiveId(wish.id);
      const mediaId = parsePositiveId(wish.media_id);
      const ownerSecurityCode = String(wish.security_code || "").trim();
      const viewerParticipationText = String(wish.viewer_participation_text || "").trim();
      const viewerParticipationStatus = String(wish.viewer_participation_status || "").trim();
      const viewerParticipationValidatedAt = String(wish.viewer_participation_validated_at || "").trim();
      const ownerReviewItems = Array.isArray(wish.owner_review_items) ? wish.owner_review_items : [];
      const ownerPendingValidationCount = Number(wish.owner_pending_validation_count || 0);
      const ownerCanMarkFulfilled = Boolean(wish.owner_can_mark_fulfilled);
      const isFulfilled = Boolean(wish.is_fulfilled);

      if (wishId) {
        slot.dataset.wishId = `${wishId}`;
      } else {
        delete slot.dataset.wishId;
      }
      if (mediaId) {
        slot.dataset.mediaId = `${mediaId}`;
      } else {
        delete slot.dataset.mediaId;
      }
      if (ownerSecurityCode) {
        slot.dataset.securityCode = ownerSecurityCode;
      } else {
        delete slot.dataset.securityCode;
      }
      if (viewerParticipationText) {
        slot.dataset.viewerParticipationText = viewerParticipationText;
      } else {
        delete slot.dataset.viewerParticipationText;
      }
      if (viewerParticipationStatus) {
        slot.dataset.viewerParticipationStatus = viewerParticipationStatus;
      } else {
        delete slot.dataset.viewerParticipationStatus;
      }
      slot.dataset.viewerParticipationHasEvidence = wish.viewer_participation_has_evidence ? "true" : "false";
      if (viewerParticipationValidatedAt) {
        slot.dataset.viewerParticipationValidatedAt = viewerParticipationValidatedAt;
      } else {
        delete slot.dataset.viewerParticipationValidatedAt;
      }
      slot.dataset.ownerPendingValidationCount = `${Number.isFinite(ownerPendingValidationCount) ? ownerPendingValidationCount : 0}`;
      slot.dataset.ownerCanMarkFulfilled = ownerCanMarkFulfilled ? "true" : "false";
      slot.dataset.ownerReviewItems = JSON.stringify(ownerReviewItems);
      slot.dataset.isFulfilled = isFulfilled ? "true" : "false";

      renderCooperativeWishSlot(slot, wish);
    };

    const clearCooperativeSlots = () => {
      if (!cooperativeWishList) return;
      cooperativeWishList.innerHTML = "";
      cooperativeTotal = 0;
      if (cooperativeWishAdd) {
        cooperativeWishAdd.disabled = false;
      }
    };

    const hydrateCooperativeSlots = (items) => {
      if (!cooperativeWishList) return;
      const records = Array.isArray(items) ? items : [];
      clearCooperativeSlots();
      const totalSlots = Math.max(cooperativeMin, Math.min(cooperativeMax, records.length));
      for (let i = 0; i < totalSlots; i += 1) {
        addCooperativeSlot();
      }
      const slots = Array.from(cooperativeWishList.querySelectorAll(".wish-slot"));
      records.forEach((wish, index) => {
        const slot = slots[index];
        if (!slot) return;
        applyCooperativeWishRecordToSlot(slot, wish);
      });
    };

    const loadCooperativeWishesFromApi = async () => {
      try {
        const data = await fetchCooperativeWishList();
        hydrateCooperativeSlots(data?.items || []);
      } catch (error) {
        console.error(error);
      }
    };

    const renderCooperativeWishSlot = (slot, wish) => {
      if (!slot) return;
      const description = String(wish?.wish_text || "").trim();
      const imageUrl = String(wish?.media_url || "").trim() || null;
      const type = String(wish?.wish_type || slot?.dataset?.type || "Espiritual");
      const current = Number(wish?.participants_current || slot?.dataset?.current || 0);
      const goal = Number(wish?.participants_goal || slot?.dataset?.goal || 0);
      const template = String(wish?.template_text || slot?.dataset?.template || "");
      const securityCode = String(wish?.security_code || slot?.dataset?.securityCode || "").trim();
      const viewerParticipationText = String(
        wish?.viewer_participation_text || slot?.dataset?.viewerParticipationText || ""
      ).trim();
      const viewerParticipationStatus = String(
        wish?.viewer_participation_status || slot?.dataset?.viewerParticipationStatus || ""
      ).trim();
      const viewerParticipationHasEvidence = Boolean(
        wish?.viewer_participation_has_evidence || slot?.dataset?.viewerParticipationHasEvidence === "true"
      );
      const viewerParticipationValidated = Boolean(
        wish?.viewer_participation_validated_at || slot?.dataset?.viewerParticipationValidatedAt
      );
      const ownerReviewItems = Array.isArray(wish?.owner_review_items)
        ? wish.owner_review_items
        : getCooperativeOwnerReviewItemsFromSlot(slot);
      const hasOwnerEvidenceItems = ownerReviewItems.length > 0;

      if (slot.dataset.imageUrl && slot.dataset.imageUrl !== imageUrl) {
        URL.revokeObjectURL(slot.dataset.imageUrl);
        delete slot.dataset.imageUrl;
      }

      slot.classList.remove("is-empty", "is-choosing");
      slot.classList.add("is-filled", "is-cooperative");
      slot.innerHTML = "";
      slot.dataset.description = description;
      if (type) {
        slot.dataset.type = type;
      }
      if (goal !== undefined) {
        slot.dataset.goal = `${goal}`;
      }
      if (current !== undefined) {
        slot.dataset.current = `${current}`;
      }
      if (template) {
        slot.dataset.template = template;
      } else {
        delete slot.dataset.template;
      }
      if (securityCode) {
        slot.dataset.securityCode = securityCode;
      } else {
        delete slot.dataset.securityCode;
      }
      if (viewerParticipationText) {
        slot.dataset.viewerParticipationText = viewerParticipationText;
      } else {
        delete slot.dataset.viewerParticipationText;
      }

      const row = document.createElement("div");
      row.className = "wish-slot-row";

      const body = document.createElement("div");
      body.className = "wish-slot-body";

      const leftCol = document.createElement("div");
      leftCol.className = "wish-slot-left";

      const iconWrap = document.createElement("div");
      iconWrap.className = "wish-slot-icon";
      const selectedType = type || "Espiritual";
      const categoryIconSrc = personalTypeIconMap[selectedType] || personalTypeIconMap["Espiritual"];
      const categoryIcon = document.createElement("img");
      categoryIcon.className = "wish-slot-category-icon";
      categoryIcon.src = categoryIconSrc;
      categoryIcon.alt = selectedType;
      iconWrap.appendChild(categoryIcon);

      const descWrap = document.createElement("div");
      descWrap.className = "wish-slot-description wish-slot-description-coop";
      const title = document.createElement("div");
      title.className = "wish-slot-title";
      title.textContent = description;
      descWrap.appendChild(title);
      const hasViewerParticipation = Boolean((viewerParticipationText || "").trim());
      if (!isViewingOwnProfile && hasViewerParticipation) {
        const participationLine = document.createElement("div");
        participationLine.className = "wish-root-description";
        participationLine.textContent = `${tr("Tu participación", "Your participation", "Ta participation")}: ${viewerParticipationText}`;
        descWrap.appendChild(participationLine);

        if (viewerParticipationValidated) {
          const statusLine = document.createElement("div");
          statusLine.className = "wish-root-description";
          statusLine.textContent = tr(
            "✅ Tu participación fue validada por el creador del deseo.",
            "✅ Your participation was validated by the wish creator."
          );
          descWrap.appendChild(statusLine);
        } else if (viewerParticipationHasEvidence || viewerParticipationStatus === "completed") {
          const statusLine = document.createElement("div");
          statusLine.className = "wish-root-description";
          statusLine.textContent = tr(
            "⏳ Evidencia enviada. Esperando validación del creador.",
            "⏳ Evidence sent. Waiting for creator validation."
          );
          descWrap.appendChild(statusLine);
        }
      }
      if (isViewingOwnProfile) {
        const securityField = document.createElement("div");
        securityField.className = "wish-security-field";
        const securityLabel = document.createElement("span");
        securityLabel.className = "wish-security-label";
        securityLabel.textContent = tr("Código de seguridad", "Security code", "Code de sécurité");
        const securityInput = document.createElement("input");
        securityInput.className = "wish-security-input";
        securityInput.type = "text";
        securityInput.inputMode = "numeric";
        securityInput.maxLength = 6;
        securityInput.placeholder = "000000";
        securityInput.readOnly = true;
        securityInput.value = securityCode || slot.dataset.securityCode || "";
        securityField.appendChild(securityLabel);
        securityField.appendChild(securityInput);
        descWrap.appendChild(securityField);
      }

      const counter = document.createElement("div");
      counter.className = "wish-slot-counter";
      const safeCurrent = Number.isFinite(current) ? current : 0;
      const safeGoal = Number.isFinite(goal) ? goal : 0;
      const counterText = safeCurrent >= safeGoal && safeGoal > 0 ? `${safeGoal} = ${safeGoal}` : `${safeCurrent} < ${safeGoal}`;
      counter.textContent = counterText;

      leftCol.appendChild(iconWrap);
      leftCol.appendChild(descWrap);
      leftCol.appendChild(counter);

      const actions = document.createElement("div");
      actions.className = "wish-slot-actions wish-slot-actions-inline";
      if (!isViewingOwnProfile) {
        if (!hasViewerParticipation) {
          actions.appendChild(createVisitorCooperativeIcon(false));
        } else {
          const disableManageActions = viewerParticipationValidated;

          const editParticipationBtn = createWishActionBtn(
            "/css/icons/iconedit.webp",
            tr("Editar mi participación", "Edit my participation", "Modifier ma participation"),
            "help-edit"
          );
          if (disableManageActions) editParticipationBtn.classList.add("wish-icon-disabled");
          actions.appendChild(editParticipationBtn);

          const cancelParticipationBtn = createWishActionBtn(
            "/css/icons/icondelete.webp",
            tr("Cancelar mi participación", "Cancel my participation", "Annuler ma participation"),
            "help-cancel"
          );
          if (disableManageActions) cancelParticipationBtn.classList.add("wish-icon-disabled");
          actions.appendChild(cancelParticipationBtn);

          const completeParticipationTitle = viewerParticipationHasEvidence
            ? tr("Actualizar evidencia de mi participación", "Update my participation evidence", "Mettre à jour la preuve de ma participation")
            : tr("Marcar mi participación como cumplida", "Mark my participation as fulfilled", "Marquer ma participation comme accomplie");
          const completeParticipationBtn = createWishActionBtn(
            "/css/icons/iconfulfill.webp",
            completeParticipationTitle,
            "help-complete"
          );
          if (disableManageActions) completeParticipationBtn.classList.add("wish-icon-disabled");
          actions.appendChild(completeParticipationBtn);
        }
      } else {
        actions.appendChild(createWishActionBtn("/css/icons/iconedit.webp", tr("Editar deseo", "Edit wish", "Modifier le souhait"), "edit"));
        const fulfillBtn = createWishActionBtn("/css/icons/iconfulfill.webp", tr("Marcar como cumplido", "Mark as fulfilled", "Marquer comme accompli"), "fulfill");
        if (!hasOwnerEvidenceItems) {
          fulfillBtn.classList.add("wish-icon-disabled");
          fulfillBtn.title = tr("Aún no hay evidencias de participantes para validar.", "There is no participant evidence to validate yet.", "Il n'y a pas encore de preuve de participation à valider.");
        }
        actions.appendChild(fulfillBtn);
        actions.appendChild(createWishActionBtn("/css/icons/icondelete.webp", tr("Borrar deseo", "Delete wish", "Supprimer le souhait"), "delete"));
      }
      leftCol.appendChild(actions);

      body.appendChild(leftCol);

      if (imageUrl) {
        const imageWrap = document.createElement("div");
        imageWrap.className = "wish-slot-image-wrap";
        const img = document.createElement("img");
        img.className = "wish-slot-image";
        img.src = imageUrl;
        img.alt = tr("Imagen del deseo", "Wish image", "Image du souhait");
        imageWrap.appendChild(img);
        body.appendChild(imageWrap);
        slot.dataset.imageUrl = imageUrl;
      } else {
        body.classList.add("single");
      }

      row.appendChild(body);
      slot.appendChild(row);
    };

    const renderParticipationWishSlot = (slot, participationText, rootDescription, rootImageUrl, rootUser, template) => {
      if (!slot) return;
      slot.classList.remove("is-empty", "is-choosing");
      slot.classList.add("is-filled", "is-cooperative", "is-participation");
      slot.innerHTML = "";
      slot.dataset.participationText = participationText;
      slot.dataset.rootDescription = rootDescription || "";
      slot.dataset.rootUser = rootUser || tr("Usuario", "User", "Utilisateur");
      if (template) {
        slot.dataset.template = template;
      }
      if (rootImageUrl) {
        slot.dataset.rootImageUrl = rootImageUrl;
      }

      const row = document.createElement("div");
      row.className = "wish-slot-row";

      const body = document.createElement("div");
      body.className = "wish-slot-body";

      const leftCol = document.createElement("div");
      leftCol.className = "wish-slot-left";

      const iconWrap = document.createElement("div");
      iconWrap.className = "wish-slot-icon";
      const icon = document.createElement("img");
      icon.className = "wish-slot-category-icon";
      icon.src = "/css/icons/iconcooperative2.webp";
      icon.alt = tr("Yo puedo ayudar a cumplir este deseo", "I can help fulfill this wish", "Je peux aider à accomplir ce souhait");
      iconWrap.appendChild(icon);

      const descWrap = document.createElement("div");
      descWrap.className = "wish-slot-description";
      const title = document.createElement("div");
      title.className = "wish-slot-title";
      title.textContent = participationText;
      const typePill = document.createElement("span");
      typePill.className = "wish-type-pill";
      typePill.textContent = tr("Cooperativo", "Cooperative", "Coopératif");
      descWrap.appendChild(title);
      descWrap.appendChild(typePill);
      if (isViewingOwnProfile) {
        const securityField = document.createElement("div");
        securityField.className = "wish-security-field";
        const securityLabel = document.createElement("span");
        securityLabel.className = "wish-security-label";
        securityLabel.textContent = tr("Código de seguridad", "Security code", "Code de sécurité");
        const securityInput = document.createElement("input");
        securityInput.className = "wish-security-input";
        securityInput.type = "text";
        securityInput.inputMode = "numeric";
        securityInput.maxLength = 6;
        securityInput.placeholder = "000000";
        securityInput.readOnly = true;
        securityInput.value = slot.dataset.securityCode || "";
        securityField.appendChild(securityLabel);
        securityField.appendChild(securityInput);
        descWrap.appendChild(securityField);
      }

      const actions = document.createElement("div");
      actions.className = "wish-slot-actions wish-slot-actions-inline";
      actions.appendChild(createWishActionBtn("/css/icons/iconedit.webp", tr("Editar deseo", "Edit wish", "Modifier le souhait"), "help-edit"));
      actions.appendChild(createWishActionBtn("/css/icons/iconfulfill.webp", tr("Marcar como cumplido", "Mark as fulfilled", "Marquer comme accompli"), "fulfill"));
      actions.appendChild(createWishActionBtn("/css/icons/icondelete.webp", tr("Borrar deseo", "Delete wish", "Supprimer le souhait"), "delete"));

      leftCol.appendChild(iconWrap);
      leftCol.appendChild(descWrap);
      leftCol.appendChild(actions);

      body.appendChild(leftCol);

      const rightCol = document.createElement("div");
      rightCol.className = "wish-slot-right";

      if (rootImageUrl) {
        const imageWrap = document.createElement("div");
        imageWrap.className = "wish-slot-image-wrap";
        const img = document.createElement("img");
        img.className = "wish-slot-image";
        img.src = rootImageUrl;
        img.alt = tr("Imagen del deseo raíz", "Root wish image", "Image racine du souhait");
        imageWrap.appendChild(img);
        rightCol.appendChild(imageWrap);
      }

      const rootLink = document.createElement("a");
      rootLink.className = "wish-root-link";
      rootLink.href = "#";
      rootLink.textContent = rootUser || tr("Usuario", "User", "Utilisateur");

      const rootDesc = document.createElement("div");
      rootDesc.className = "wish-root-description";
      rootDesc.textContent = rootDescription || "";

      rightCol.appendChild(rootLink);
      rightCol.appendChild(rootDesc);
      body.appendChild(rightCol);

      row.appendChild(body);
      slot.appendChild(row);
    };

    const resetPersonalWishForm = () => {
      if (personalWishText) {
        const prefix = personalWishText.dataset.prefix || tr("Deseo ", "Wish ", "Souhait ");
        personalWishText.value = prefix;
        personalWishText.dispatchEvent(new Event("input", { bubbles: true }));
      }
      if (personalWishMedia) {
        personalWishMedia.value = "";
      }
      updatePersonalPreview(null);
      setPersonalWishError(false);
    };

    const resetCooperativeWishForm = () => {
      if (cooperativeWishText) {
        const prefix = cooperativeWishText.dataset.prefix || tr("Deseo ", "Wish ", "Souhait ");
        cooperativeWishText.value = prefix;
        cooperativeWishText.dispatchEvent(new Event("input", { bubbles: true }));
      }
      if (cooperativeWishCount) {
        cooperativeWishCount.value = `${COOPERATIVE_PARTICIPANTS_LIMIT}`;
      }
      if (cooperativeWishTemplate) {
        const suffix = cooperativeWishTemplate.dataset.suffix || "";
        cooperativeWishTemplate.value = suffix ? `${tr("Deseo", "Wish", "Souhait")} ${suffix}` : "";
        cooperativeWishTemplate.dispatchEvent(new Event("input", { bubbles: true }));
      }
      if (cooperativeWishSecurityCode) {
        cooperativeWishSecurityCode.value = "";
      }
      if (cooperativeWishMedia) {
        cooperativeWishMedia.value = "";
      }
      updateCooperativePreview(null);
      setCooperativeWishError(false);
    };

    const personalTypeIconMap = {
      "Espiritual": "/css/icons/Espiritual.webp",
      "Material": "/css/icons/Material.webp",
      "Monetario": "/css/icons/Monetario.webp",
      "Profesional": "/css/icons/Profesional.webp",
      "Salud y cuerpo": "/css/icons/Salud.webp",
      "Relacional": "/css/icons/Relacional.webp",
      "Vivencial": "/css/icons/Vivencial.webp"
    };

    const personalTypeHintMap = {
      "Espiritual": tr(
        "Deseos relacionados con el sentido de vida, la conciencia, la fe, la paz interior y el crecimiento espiritual. Ejemplo: perseverar en el hábito de la meditación, leer libros sobre espiritualidad, asistir a misa.",
        "Wishes related to life meaning, awareness, faith, inner peace, and spiritual growth. Example: keep a meditation habit, read spirituality books, attend mass."
      ),
      "Material": tr(
        "Deseos vinculados a bienes, objetos o condiciones tangibles que mejoran la calidad de vida. Pueden involucrar recursos externos y, en algunos casos, la ayuda o participación de otras personas. Ejemplo: tener una cafetera nueva, un nuevo auto, una nueva computadora.",
        "Wishes linked to goods, objects, or tangible conditions that improve quality of life. They may involve external resources and, in some cases, help from others. Example: a new coffee maker, a new car, a new computer."
      ),
      "Monetario": tr(
        "Deseos relacionados exclusivamente con metas económicas personales. No pueden ser concedidos por otras personas y funcionan como objetivos de ahorro, disciplina y logro individual. Solo el propio usuario puede cumplirlos.",
        "Wishes focused exclusively on personal financial goals. They cannot be granted by other people and work as savings, discipline, and individual achievement goals. Only the user can fulfill them."
      ),
      "Profesional": tr(
        "Deseos asociados al desarrollo laboral, académico o creativo. Incluyen proyectos, estudios, reconocimiento, impacto profesional y crecimiento en la vocación personal. Ejemplo: estudiar arquitectura y graduarme de la Universidad Politécnico de Milán.",
        "Wishes tied to career, academic, or creative development. They include projects, studies, recognition, professional impact, and growth in your personal vocation. Example: study architecture and graduate from Politecnico di Milano."
      ),
      "Salud y cuerpo": tr(
        "Deseos enfocados en el bienestar físico, la energía vital, la recuperación y la relación consciente con el cuerpo. No sustituyen atención médica ni tratamientos profesionales. Ejemplo: mantener la disciplina de ejercitar tu cuerpo a diario, correr 1 km diario, alimentarte bien.",
        "Wishes focused on physical well-being, vitality, recovery, and conscious care of the body. They do not replace medical care or professional treatment. Example: keep a daily workout habit, run 1 km each day, eat well."
      ),
      "Relacional": tr(
        "Deseos relacionados con vínculos humanos: familia, pareja, amistades y comunidad. Incluyen encuentros, reconciliaciones, fortalecimiento de relaciones y construcción de lazos significativos. Ejemplo: tomarse una cerveza con Lars Ulrich, ir a un concierto con tu hermano, disfrutar de un día en familia en el Restaurante La Matriarca.",
        "Wishes related to human bonds: family, partner, friends, and community. They include reunions, reconciliation, stronger relationships, and meaningful connections. Example: have a beer with Lars Ulrich, attend a concert with your brother, enjoy a family day at La Matriarca restaurant."
      ),
      "Vivencial": tr(
        "Deseos orientados a experiencias, momentos únicos y vivencias significativas. No se definen por la posesión, sino por el hecho de vivir algo que deje huella en la memoria y la conciencia. Ejemplo: lanzarse en paracaídas, visitar Las Islas Maldivas, viajar en helicóptero.",
        "Wishes focused on experiences, unique moments, and meaningful memories. They are not defined by ownership, but by living something that leaves a mark on memory and awareness. Example: skydive, visit the Maldives, fly in a helicopter."
      )
    };

    const syncPersonalTypeIcon = (value) => {
      if (!personalWishTypeIcon) return;
      const src = personalTypeIconMap[value] || personalTypeIconMap["Espiritual"];
      personalWishTypeIcon.src = src;
      personalWishTypeIcon.alt = value;
    };

    const syncPersonalTypeHint = (value) => {
      if (!personalWishTypeHint) return;
      const hint = personalTypeHintMap[value] || personalTypeHintMap["Espiritual"];
      personalWishTypeHint.textContent = hint;
    };

    const syncCooperativeTypeIcon = (value) => {
      if (!cooperativeWishTypeIcon) return;
      const src = personalTypeIconMap[value] || personalTypeIconMap["Espiritual"];
      cooperativeWishTypeIcon.src = src;
      cooperativeWishTypeIcon.alt = value;
    };

    const syncCooperativeTypeHint = (value) => {
      if (!cooperativeWishTypeHint) return;
      const hint = personalTypeHintMap[value] || personalTypeHintMap["Espiritual"];
      cooperativeWishTypeHint.textContent = hint;
    };

    personalWishTypeInputs.forEach((input) => {
      input.addEventListener("change", () => {
        if (input.checked) {
          syncPersonalTypeIcon(input.value);
          syncPersonalTypeHint(input.value);
        }
      });
    });

    cooperativeWishTypeInputs.forEach((input) => {
      input.addEventListener("change", () => {
        if (input.checked) {
          syncCooperativeTypeIcon(input.value);
          syncCooperativeTypeHint(input.value);
        }
      });
    });

    const checkedInput = Array.from(personalWishTypeInputs).find((input) => input.checked);
    if (checkedInput) {
      syncPersonalTypeIcon(checkedInput.value);
      syncPersonalTypeHint(checkedInput.value);
    }

    const checkedCoopInput = Array.from(cooperativeWishTypeInputs).find((input) => input.checked);
    if (checkedCoopInput) {
      syncCooperativeTypeIcon(checkedCoopInput.value);
      syncCooperativeTypeHint(checkedCoopInput.value);
    }

    if (cooperativeWishSecurityCode) {
      cooperativeWishSecurityCode.addEventListener("input", () => {
        const cleaned = cooperativeWishSecurityCode.value.replace(/\D/g, "").slice(0, 6);
        if (cooperativeWishSecurityCode.value !== cleaned) {
          cooperativeWishSecurityCode.value = cleaned;
        }
        if (cleaned.length === 6) {
          setCooperativeWishError(false);
        }
      });
    }

    const handleConfirmPersonalWish = async () => {
      if (!activePersonalSlot) return;
      if (!personalWishText) return;
      if (!isPersonalWishValid()) {
        setPersonalWishError(true, tr("No has descrito tu deseo.", "You have not described your wish.", "Tu n'as pas décrit ton souhait."));
        return;
      }

      const description = personalWishText.value.trim();
      const file = personalWishMedia && personalWishMedia.files ? personalWishMedia.files[0] : null;
      const selectedType = Array.from(personalWishTypeInputs).find((input) => input.checked)?.value || "Espiritual";
      const wishId = parsePositiveId(activePersonalSlot.dataset.wishId);
      const currentMediaId = parsePositiveId(activePersonalSlot.dataset.mediaId);

      try {
        setPersonalWishError(false);
        const uploadedMedia = file ? await uploadWishImage(file) : null;
        const payload = {
          wish_text: description,
          wish_type: selectedType,
          media_id: uploadedMedia?.media_id || currentMediaId || null
        };

        const savedWish = wishId
          ? await updatePersonalWishRecord(wishId, payload)
          : await createPersonalWish(payload);

        applyPersonalWishRecordToSlot(activePersonalSlot, savedWish);
        closePersonalWishModalFn();
        resetPersonalWishForm();
        activePersonalSlot = null;
      } catch (error) {
        setPersonalWishError(true, error?.message || tr("No se pudo guardar tu deseo personal.", "Could not save your personal wish.", "Impossible de save your personal wish."));
      }
    };

    if (confirmPersonalWish) {
      confirmPersonalWish.addEventListener("click", handleConfirmPersonalWish);
    }

    const buildCooperativeParticipationText = ({ mode = "create", template = "", userInput = "" } = {}) => {
      const cleanedInput = String(userInput || "").trim();
      if (mode === "edit") {
        return cleanedInput;
      }
      const normalizedTemplate = String(template || "").trim();
      if (!normalizedTemplate) {
        return cleanedInput;
      }
      if (/\*[^*]*\*/.test(normalizedTemplate)) {
        return normalizedTemplate.replace(/\*[^*]*\*/, cleanedInput || "…");
      }
      return cleanedInput || normalizedTemplate;
    };

    const handleConfirmCooperativeWish = async () => {
      if (!cooperativeWishList || !activeCooperativeSlot) return;
      setCooperativeWishError(false);
      const description = cooperativeWishText ? cooperativeWishText.value.trim() : "";
      const prefix = cooperativeWishText ? (cooperativeWishText.dataset.prefix || "") : "";
      const cleanDescription = prefix && description.startsWith(prefix)
        ? description.slice(prefix.length).trim()
        : description;
      if (!cleanDescription) {
        setCooperativeWishError(true, tr("No has descrito tu deseo cooperativo.", "You have not described your cooperative wish.", "Tu n'as pas décrit ton souhait coopératif."));
        return;
      }

      const selectedType = Array.from(cooperativeWishTypeInputs).find((input) => input.checked)?.value || "Espiritual";
      const goalRaw = cooperativeWishCount ? Number(cooperativeWishCount.value) : 0;
      const goal = Number.isFinite(goalRaw)
        ? Math.max(1, Math.min(COOPERATIVE_PARTICIPANTS_LIMIT, Math.floor(goalRaw)))
        : 1;
      if (cooperativeWishCount) {
        cooperativeWishCount.value = `${goal}`;
      }
      const template = cooperativeWishTemplate ? cooperativeWishTemplate.value.trim() : "";
      const securityCodeRaw = cooperativeWishSecurityCode ? cooperativeWishSecurityCode.value : "";
      const securityCode = securityCodeRaw.replace(/\D/g, "").slice(0, 6);
      if (securityCode.length !== 6) {
        setCooperativeWishError(true, tr("El código de seguridad debe tener exactamente 6 dígitos.", "The security code must have exactly 6 digits.", "Le code de sécurité doit contenir exactement 6 chiffres."));
        return;
      }
      const file = cooperativeWishMedia && cooperativeWishMedia.files ? cooperativeWishMedia.files[0] : null;
      const wishId = parsePositiveId(activeCooperativeSlot.dataset.wishId);
      const currentMediaId = parsePositiveId(activeCooperativeSlot.dataset.mediaId);

      try {
        const uploadedMedia = file ? await uploadWishImage(file) : null;
        const payload = {
          wish_text: description,
          wish_type: selectedType,
          participants_goal: goal,
          template_text: template || null,
          security_code: securityCode,
          media_id: uploadedMedia?.media_id || currentMediaId || null
        };
        const savedWish = wishId
          ? await updateCooperativeWishRecord(wishId, payload)
          : await createCooperativeWish(payload);
        applyCooperativeWishRecordToSlot(activeCooperativeSlot, savedWish);
        closeCooperativeWishModalFn();
        resetCooperativeWishForm();
        activeCooperativeSlot = null;
      } catch (error) {
        setCooperativeWishError(true, error?.message || tr("No se pudo guardar el deseo cooperativo.", "Could not save the cooperative wish.", "Impossible de save the cooperative wish."));
      }
    };

    if (confirmCooperativeWish) {
      confirmCooperativeWish.addEventListener("click", () => {
        void handleConfirmCooperativeWish();
      });
    }

    if (confirmCooperativeParticipate) {
      confirmCooperativeParticipate.addEventListener("click", async () => {
        const sourceSlot = activeParticipateSource;
        const wishId = parsePositiveId(sourceSlot?.dataset?.wishId);
        if (!sourceSlot || !wishId) return;
        const isEditMode = activeParticipateMode === "edit";
        const enteredCode = String(activeSecurityCode || "").replace(/\D/g, "").slice(0, 6);
        if (!isEditMode && enteredCode.length !== 6) {
          closeCooperativeParticipateModalFn();
          openCooperativeSecurityModal(sourceSlot);
          if (cooperativeSecurityError) {
            cooperativeSecurityError.classList.add("is-visible");
          }
          return;
        }
        const rootTemplate = String(sourceSlot.dataset.template || "");
        const extraText = cooperativeCharacter ? cooperativeCharacter.value : "";
        const participationText = buildCooperativeParticipationText({
          mode: activeParticipateMode,
          template: rootTemplate,
          userInput: extraText,
        });
        if (!participationText) {
          window.alert(tr("Debes describir tu participación.", "You must describe your participation.", "Tu dois describe your participation."));
          return;
        }
        try {
          const updatedWish = await participateInCooperativeWishRecord(wishId, {
            security_code: isEditMode ? null : enteredCode,
            participation_text: participationText,
          });
          applyCooperativeWishRecordToSlot(sourceSlot, updatedWish);
          closeCooperativeParticipateModalFn();
        } catch (error) {
          window.alert(error?.message || tr("No se pudo registrar tu participación.", "Could not register your participation.", "Impossible d'enregistrer ta participation."));
        }
      });
    }

    if (cooperativeSecurityCodeInput) {
      cooperativeSecurityCodeInput.addEventListener("input", () => {
        const cleaned = cooperativeSecurityCodeInput.value.replace(/\D/g, "").slice(0, 6);
        if (cooperativeSecurityCodeInput.value !== cleaned) {
          cooperativeSecurityCodeInput.value = cleaned;
        }
      });
    }

    if (confirmCooperativeSecurity) {
      confirmCooperativeSecurity.addEventListener("click", () => {
        if (!activeSecuritySlot) return;
        const enteredRaw = cooperativeSecurityCodeInput ? cooperativeSecurityCodeInput.value : "";
        const entered = enteredRaw.replace(/\D/g, "").slice(0, 6);
        if (cooperativeSecurityCodeInput && cooperativeSecurityCodeInput.value !== entered) {
          cooperativeSecurityCodeInput.value = entered;
        }
        if (entered.length !== 6) {
          if (cooperativeSecurityError) {
            cooperativeSecurityError.classList.add("is-visible");
          }
          return;
        }
        activeSecurityCode = entered;
        if (cooperativeSecurityError) {
          cooperativeSecurityError.classList.remove("is-visible");
        }
        const slot = activeSecuritySlot;
        const mode = slot?.dataset?.viewerParticipationText ? "edit" : "create";
        closeCooperativeSecurityModal({ clearCode: false });
        openCooperativeParticipateModal(slot, mode);
      });
    }

    if (cancelCooperativeSecurity) {
      cancelCooperativeSecurity.addEventListener("click", closeCooperativeSecurityModal);
    }

    const closeCoverMenu = () => {
      if (coverMenu && coverMenu.hasAttribute("open")) {
        coverMenu.removeAttribute("open");
      }
    };

    const markCoverDirty = () => {
      coverDirty = true;
      if (coverSaveActions) {
        coverSaveActions.classList.remove("hidden");
      }
    };

    const hideCoverActions = () => {
      if (coverSaveActions) {
        coverSaveActions.classList.add("hidden");
      }
    };

    const setCoverMoveState = (enabled) => {
      coverMoveEnabled = enabled;
      if (coverMedia) {
        coverMedia.classList.toggle("is-move-mode", coverMoveEnabled);
      }
      if (coverMoveBtn) {
        coverMoveBtn.classList.toggle("is-active", coverMoveEnabled);
      }
      updateCoverTransform(coverOffsetX, coverOffsetY);
    };

    const commitCoverState = () => {
      if (!coverImg) return;
      coverSavedSrc = coverImg.src;
      coverSavedOffsetX = coverOffsetX;
      coverSavedOffsetY = coverOffsetY;
      coverDirty = false;
      coverPendingUrl = null;
      setCoverMoveState(false);
      hideCoverActions();
    };

    const revertCoverState = () => {
      if (!coverImg) return;
      if (coverPendingUrl) {
        URL.revokeObjectURL(coverPendingUrl);
        coverPendingUrl = null;
      }
      coverOffsetX = coverSavedOffsetX;
      coverOffsetY = coverSavedOffsetY;
      if (coverSavedSrc) {
        coverImg.src = coverSavedSrc;
      }
      coverDirty = false;
      setCoverMoveState(false);
      hideCoverActions();
    };

    const updateCoverTransform = (x, y) => {
      if (!coverImg || !coverMedia) return { x, y };
      const clampedX = Math.min(coverMaxOffsetX, Math.max(-coverMaxOffsetX, x));
      const clampedY = Math.min(coverMaxOffsetY, Math.max(-coverMaxOffsetY, y));
      coverImg.style.transform = "none";
      coverImg.style.objectPosition = `calc(50% + ${clampedX}px) calc(50% + ${clampedY}px)`;
      return { x: clampedX, y: clampedY };
    };

    const recalcCoverBounds = () => {
      if (!coverImg || !coverMedia || !coverImg.naturalWidth || !coverImg.naturalHeight) return;
      const rect = coverMedia.getBoundingClientRect();
      const scale = Math.max(rect.width / coverImg.naturalWidth, rect.height / coverImg.naturalHeight);
      const renderedWidth = coverImg.naturalWidth * scale;
      const renderedHeight = coverImg.naturalHeight * scale;
      coverMaxOffsetX = Math.max(0, (renderedWidth - rect.width) / 2);
      coverMaxOffsetY = Math.max(0, (renderedHeight - rect.height) / 2);
      const clamped = updateCoverTransform(coverOffsetX, coverOffsetY);
      coverOffsetX = clamped.x;
      coverOffsetY = clamped.y;
    };

    if (coverChangeBtn && coverFile) {
      coverChangeBtn.addEventListener("click", () => coverFile.click());
    }

    if (coverUploadBtn && coverFile) {
      coverUploadBtn.addEventListener("click", () => coverFile.click());
    }

    if (coverFile && coverImg) {
      coverFile.addEventListener("change", (event) => {
        const file = event.target.files && event.target.files[0];
        if (!file) return;
        if (coverPendingUrl) {
          URL.revokeObjectURL(coverPendingUrl);
        }
        const url = URL.createObjectURL(file);
        coverPendingUrl = url;
        coverImg.src = url;
        coverOffsetX = 0;
        coverOffsetY = 0;
        markCoverDirty();
        closeCoverMenu();
        setCoverMoveState(true);
        recalcCoverBounds();
      });
    }

    if (coverMoveBtn && coverMedia) {
      coverMoveBtn.addEventListener("click", () => {
        setCoverMoveState(!coverMoveEnabled);
        markCoverDirty();
        closeCoverMenu();
      });
    }

    if (coverSaveBtn) {
      coverSaveBtn.addEventListener("click", commitCoverState);
    }

    if (coverCancelBtn) {
      coverCancelBtn.addEventListener("click", revertCoverState);
    }

    if (coverMedia && coverImg) {
      coverMedia.addEventListener("mousedown", (event) => {
        if (!coverMoveEnabled) return;
        if (event.target.closest(".cover-actions")) return;
        coverDragActive = true;
        coverStartX = event.clientX;
        coverStartY = event.clientY;
        coverMedia.classList.add("is-dragging");
      });

      window.addEventListener("mousemove", (event) => {
        if (!coverDragActive) return;
        const dx = event.clientX - coverStartX;
        const dy = event.clientY - coverStartY;
        const nextX = coverOffsetX + dx;
        const nextY = coverOffsetY + dy;
        updateCoverTransform(nextX, nextY);
      });

      window.addEventListener("mouseup", (event) => {
        if (!coverDragActive) return;
        const dx = event.clientX - coverStartX;
        const dy = event.clientY - coverStartY;
        const nextX = coverOffsetX + dx;
        const nextY = coverOffsetY + dy;
        const clamped = updateCoverTransform(nextX, nextY);
        coverOffsetX = clamped.x;
        coverOffsetY = clamped.y;
        coverDragActive = false;
        coverMedia.classList.remove("is-dragging");
      });
    }

    if (coverImg) {
      coverImg.addEventListener("load", () => {
        if (!coverSavedSrc) {
          coverSavedSrc = coverImg.src;
          coverSavedOffsetX = coverOffsetX;
          coverSavedOffsetY = coverOffsetY;
        }
        recalcCoverBounds();
      });
    }
    window.addEventListener("resize", recalcCoverBounds);

    if (confirmDeleteWish) {
      confirmDeleteWish.addEventListener("click", async () => {
        if (activeDeleteSlot) {
          if (activeDeleteSlot.classList.contains("is-cooperative")) {
            const wishId = parsePositiveId(activeDeleteSlot.dataset.wishId);
            if (wishId) {
              try {
                await deleteCooperativeWishRecord(wishId);
              } catch (error) {
                console.error(error);
                window.alert(error?.message || tr("No se pudo borrar el deseo cooperativo.", "Could not delete the cooperative wish.", "Impossible de supprimer le souhait coopératif."));
                return;
              }
            }
            resetSlotToEmpty(activeDeleteSlot);
          } else {
            const wishId = parsePositiveId(activeDeleteSlot.dataset.wishId);
            if (wishId) {
              try {
                await deletePersonalWishRecord(wishId);
              } catch (error) {
                console.error(error);
                window.alert(error?.message || tr("No se pudo borrar el deseo personal.", "Could not delete the personal wish.", "Impossible de supprimer le souhait personnel."));
                return;
              }
            }
            resetSlotToEmpty(activeDeleteSlot);
          }
        }
        closeDeleteWishModalFn();
      });
    }

	    if (personalWishList) {
	      personalWishList.addEventListener("click", (event) => {
	        const lampBtn = event.target.closest(".wish-lamp-btn");
	        const cancelBtn = event.target.closest(".wish-choice-cancel");
	        const choiceBtn = event.target.closest(".wish-choice-btn");
	        const actionBtn = event.target.closest(".wish-icon-btn");

	        if (lampBtn) {
	          if (!isViewingOwnProfile) return;
	          const slot = lampBtn.closest(".wish-slot");
	          if (!slot) return;
	          activePersonalSlot = slot;
	          openPersonalWishModal();
	          return;
	        }

	        if (cancelBtn) {
	          if (!isViewingOwnProfile) return;
	          const slot = cancelBtn.closest(".wish-slot");
	          if (!slot) return;
	          resetSlotToEmpty(slot);
	          activePersonalSlot = null;
	          return;
	        }

	        if (choiceBtn) {
	          if (!isViewingOwnProfile) return;
	          const slot = choiceBtn.closest(".wish-slot");
          if (choiceBtn.dataset.choice === "personal") {
            activePersonalSlot = slot;
            openPersonalWishModal();
          } else if (choiceBtn.dataset.choice === "cooperative") {
            activePersonalSlot = null;
            activeCooperativeSlot = findCooperativeEditorSlot();
            if (!activeCooperativeSlot) {
              window.alert(tr(`Ya alcanzaste el máximo de ${cooperativeMax} deseos cooperativos.`, `You have already reached the maximum of ${cooperativeMax} cooperative wishes.`, `You have already reached the maximum of ${cooperativeMax} cooperative wishes.`));
              return;
            }
            openCooperativeWishModal();
          }
          return;
        }

        if (actionBtn) {
          if (
            !isViewingOwnProfile &&
            ![
              "ican",
              "help-coop",
              "help-edit",
              "help-cancel",
              "help-complete",
              "guardian-freeze",
              "guardian-unfreeze",
              "guardian-fulfill",
            ].includes(
              actionBtn.dataset.action
            )
          ) return;
          const slot = actionBtn.closest(".wish-slot");
          if (!slot) return;
          if (actionBtn.dataset.action === "delete") {
            openDeleteWishModal(slot);
          } else if (actionBtn.dataset.action === "edit") {
            if (slot.classList.contains("is-cooperative")) {
              activeCooperativeSlot = slot;
              const existingDescription = slot.dataset.description || "";
              const prefix = cooperativeWishText
                ? cooperativeWishText.dataset.prefix || tr("Deseo ", "Wish ", "Souhait ")
                : tr("Deseo ", "Wish ", "Souhait ");
              if (cooperativeWishText) {
                cooperativeWishText.value = existingDescription
                  ? `${prefix}${existingDescription.replace(prefix, "").trim()}`
                  : prefix;
              }
              if (cooperativeWishCount) {
                cooperativeWishCount.value = slot.dataset.goal || cooperativeWishCount.value;
              }
              if (cooperativeWishTemplate) {
                cooperativeWishTemplate.value = slot.dataset.template || cooperativeWishTemplate.value;
                cooperativeWishTemplate.dispatchEvent(new Event("input", { bubbles: true }));
              }
              if (cooperativeWishSecurityCode) {
                cooperativeWishSecurityCode.value = slot.dataset.securityCode || "";
              }
              const typeValue = slot.dataset.type;
              if (typeValue) {
                const typeInput = Array.from(cooperativeWishTypeInputs).find((input) => input.value === typeValue);
                if (typeInput) {
                  typeInput.checked = true;
                  syncCooperativeTypeIcon(typeValue);
                  syncCooperativeTypeHint(typeValue);
                }
              }
              setCooperativePreviewFromUrl(slot.dataset.imageUrl || null, tr("Imagen actual", "Current image", "Image actuelle"));
              openCooperativeWishModal();
            } else {
              activePersonalSlot = slot;
              const existingDescription = slot.dataset.description || "";
              const prefix = personalWishText
                ? personalWishText.dataset.prefix || tr("Deseo ", "Wish ", "Souhait ")
                : tr("Deseo ", "Wish ", "Souhait ");
              if (personalWishText) {
                personalWishText.value = existingDescription
                  ? `${prefix}${existingDescription.replace(prefix, "").trim()}`
                  : prefix;
                personalWishText.dispatchEvent(new Event("input", { bubbles: true }));
              }

              const typeValue = slot.dataset.type;
              if (typeValue) {
                const typeInput = Array.from(personalWishTypeInputs).find((input) => input.value === typeValue);
                if (typeInput) {
                  typeInput.checked = true;
                  syncPersonalTypeIcon(typeValue);
                  syncPersonalTypeHint(typeValue);
                }
              }

              setPersonalPreviewFromUrl(slot.dataset.imageUrl || null, tr("Imagen actual", "Current image", "Image actuelle"));
              openPersonalWishModal();
            }
          } else if (actionBtn.dataset.action === "fulfill") {
            openFulfillWishModal(slot);
          } else if (actionBtn.dataset.action === "ican") {
            openIcanConfirmModal(slot);
          } else if (actionBtn.dataset.action === "guardian-freeze") {
            if (!viewerIsGuardian) return;
            const wishId = parsePositiveId(slot.dataset.wishId);
            if (!wishId) return;
            openFreezeWishConfirmModal(slot);
          } else if (actionBtn.dataset.action === "guardian-unfreeze") {
            if (!viewerIsGuardian) return;
            const wishId = parsePositiveId(slot.dataset.wishId);
            if (!wishId) return;
            const frozenBy = parsePositiveId(slot.dataset.frozenByUserId);
            if (!viewerUserId || !frozenBy || frozenBy !== viewerUserId) {
              window.alert(
                tr(
                  "Solo el guardián que congeló este deseo puede descongelarlo.",
                  "Only the guardian who froze this wish can unfreeze it."
                )
              );
              return;
            }
            openUnfreezeWishReasonModal(slot);
          } else if (actionBtn.dataset.action === "guardian-fulfill") {
            if (!viewerIsGuardian) return;
            const wishId = parsePositiveId(slot.dataset.wishId);
            if (!wishId) return;
            const frozenBy = parsePositiveId(slot.dataset.frozenByUserId);
            if (!viewerUserId || !frozenBy || frozenBy !== viewerUserId) {
              window.alert(
                tr(
                  "Solo el guardián que congeló este deseo puede marcarlo como cumplido.",
                  "Only the guardian who froze this wish can mark it as fulfilled."
                )
              );
              return;
            }
            openGuardianFulfillWishModal(slot);
          } else if (actionBtn.dataset.action === "help-coop") {
            if (!isViewingOwnProfile) {
              openCooperativeSecurityModal(slot);
            } else {
              openCooperativeParticipateModal(slot);
            }
          } else if (actionBtn.dataset.action === "help-edit") {
            openCooperativeParticipateModal(slot, "edit");
          } else if (actionBtn.dataset.action === "help-cancel") {
            openCooperativeCancelParticipationModal(slot);
          } else if (actionBtn.dataset.action === "help-complete") {
            openFulfillWishModal(slot, "cooperative-participation");
          }
          return;
        }

        if (!lampBtn) return;
      });
    }

    if (cooperativeWishList) {
      cooperativeWishList.addEventListener("click", (event) => {
        const lampBtn = event.target.closest(".wish-lamp-btn");
        const actionBtn = event.target.closest(".wish-icon-btn");
        if (lampBtn) {
          if (!isViewingOwnProfile) return;
          const slot = lampBtn.closest(".wish-slot");
          if (!slot || slot.classList.contains("is-choosing")) return;
          activeCooperativeSlot = slot;
          openCooperativeWishModal();
          return;
        }
        if (!actionBtn) return;
        if (!isViewingOwnProfile && !["help-coop", "help-edit", "help-cancel", "help-complete"].includes(actionBtn.dataset.action)) return;
        const slot = actionBtn.closest(".wish-slot");
        if (!slot) return;

        if (actionBtn.dataset.action === "delete") {
          openDeleteWishModal(slot);
        } else if (actionBtn.dataset.action === "edit") {
          activeCooperativeSlot = slot;
          const existingDescription = slot.dataset.description || "";
          const prefix = cooperativeWishText
            ? cooperativeWishText.dataset.prefix || tr("Deseo ", "Wish ", "Souhait ")
            : tr("Deseo ", "Wish ", "Souhait ");
          if (cooperativeWishText) {
            cooperativeWishText.value = existingDescription
              ? `${prefix}${existingDescription.replace(prefix, "").trim()}`
              : prefix;
          }
          if (cooperativeWishCount) {
            cooperativeWishCount.value = slot.dataset.goal || cooperativeWishCount.value;
          }
          if (cooperativeWishTemplate) {
            cooperativeWishTemplate.value = slot.dataset.template || cooperativeWishTemplate.value;
            cooperativeWishTemplate.dispatchEvent(new Event("input", { bubbles: true }));
          }
          if (cooperativeWishSecurityCode) {
            cooperativeWishSecurityCode.value = slot.dataset.securityCode || "";
          }
          const typeValue = slot.dataset.type;
          if (typeValue) {
            const typeInput = Array.from(cooperativeWishTypeInputs).find((input) => input.value === typeValue);
            if (typeInput) {
              typeInput.checked = true;
              syncCooperativeTypeIcon(typeValue);
              syncCooperativeTypeHint(typeValue);
            }
          }
          setCooperativePreviewFromUrl(slot.dataset.imageUrl || null, tr("Imagen actual", "Current image", "Image actuelle"));
          openCooperativeWishModal();
        } else if (actionBtn.dataset.action === "fulfill") {
          if (!isViewingOwnProfile) return;
          openCooperativeOwnerReviewModal(slot);
        } else if (actionBtn.dataset.action === "help-edit") {
          activeParticipateSlot = slot;
          openCooperativeParticipateModal(slot, "edit");
        } else if (actionBtn.dataset.action === "help-cancel") {
          openCooperativeCancelParticipationModal(slot);
        } else if (actionBtn.dataset.action === "help-complete") {
          openFulfillWishModal(slot, "cooperative-participation");
        } else if (actionBtn.dataset.action === "help-coop") {
          if (!isViewingOwnProfile) {
            openCooperativeSecurityModal(slot);
          } else {
            openCooperativeParticipateModal(slot);
          }
        }
      });
    }

    const scrollToCooperativeSectionIfRequested = () => {
      if (window.location.hash !== "#cooperative-wishes") return;
      const cooperativeSection = document.getElementById("cooperative-wishes");
      if (!cooperativeSection) return;
      requestAnimationFrame(() => {
        cooperativeSection.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    };

	    void (async () => {
	      try {
	        await resolveProfileContext();
	      } catch (error) {
	        console.error(error);
	      }
	      await Promise.all([
	        loadPersonalWishesFromApi(),
	        loadCooperativeWishesFromApi(),
	      ]);
        scrollToCooperativeSectionIfRequested();
	    })();
	  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{tr("Kiadez — Mis deseos públicos", "Kiadez — My public wishes", "Kiadez — Mes souhaits publics")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user public-wishes-background">
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input type="search" placeholder={tr("Buscar en Kiadez", "Search in Kiadez", "Rechercher dans Kiadez")} aria-label={tr("Buscar", "Search", "Rechercher")} />
      </form>
    </div>

		    <div class="feed-topbar-zone feed-topbar-center">
		      <a class="topbar-btn" href="/home_user.html" data-profile-module="home">🏠 Home</a>
		      <a class="topbar-btn" href="/gallery.html">🖼️ {tr("Galería", "Gallery", "Galerie")}</a>
		      <a class="topbar-btn is-active" href="/my-public-whishes.html" data-profile-module="public_wishes">🌐 {tr("Deseos públicos", "Public wishes", "Souhaits publics")}</a>
		      <a class="topbar-btn" href="/my-private-whishes.html">🔒 {tr("Deseos privados", "Private wishes", "Souhaits privés")}</a>
		      <a class="topbar-btn" href="/my-fulfilled-whises.html" data-profile-module="fulfilled_wishes">✅ {tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</a>
		    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown" id="profileDropdown">
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

      <details class="topbar-dropdown" id="menuDropdown">
        <summary class="topbar-menu-btn" aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}>
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">{tr("Menú", "Menu", "Navigation")}</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem">{tr("Mi Home", "My Home", "Mon accueil")}</a>
          <a href="/achievements.html" role="menuitem">{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
          <a href="/gallery.html" role="menuitem">{tr("Galería", "Gallery", "Galerie")}</a>
          <a href="/calendar.html" role="menuitem" data-profile-module="calendar">{tr("Calendario", "Calendar", "Calendrier")}</a>
          <a href="/my-biography.html" role="menuitem">{tr("Mi Biografía", "My Biography", "Ma biographie")}</a>
          <a href="/messages.html" role="menuitem">{tr("Mensajes", "Messages", "Messagerie")}</a>
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <!-- =========================
     *  PORTADA / COVER
     *  ========================= -->
	    <section class="cover" id="cover">
	      <div class="cover-media" id="coverMedia">
	        <img id="coverImg" class="cover-img" src="/assets/cover-default.jpg" alt={tr("Portada", "Cover", "Couverture")} />

        <div class="cover-actions">
	          <details class="cover-menu">
	            <summary class="icon-btn" id="btnChangeCover" title={tr("Editar imagen de portada", "Edit cover image", "Modifier l'image de couverture")}>
	              {tr("Editar imagen de portada", "Edit cover image", "Modifier l'image de couverture")}
	            </summary>
	            <div class="cover-menu-panel">
	              <button class="cover-menu-item" type="button" id="coverUpload">
	                {tr("Subir imagen", "Upload image", "Téléverser une image")}
	              </button>
	              <button class="cover-menu-item" type="button" id="coverMove">
	                {tr("Mover imagen", "Move image", "Déplacer l'image")}
	              </button>
	            </div>
	          </details>
	          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button"
	            title={tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier ma mission de vie")}>
	            {tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier ma mission de vie")}
	          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

	        <div class="cover-save-actions hidden" id="coverSaveActions">
	          <button class="btn btn-primary btn-compact" type="button" id="coverSaveBtn">
	            {tr("Guardar cambios", "Save changes", "Enregistrer les modifications")}
	          </button>
	          <button class="btn btn-outline btn-compact" type="button" id="coverCancelBtn">
	            {tr("Cancelar", "Cancel", "Annuler")}
	          </button>
	        </div>

	        <div class="purpose-stack" aria-label={tr("Deseos de propósito", "Purpose wishes", "Souhaits de mission")}>
          <div class="purpose-list">
            <div class="purpose-pill-row">
	              <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="1"
	                title={tr("Marcar deseo 1 como cumplido", "Mark wish 1 as fulfilled", "Marquer le souhait 1 comme accompli")}>
	                <img src="/css/icons/iconfulfill.webp" alt={tr("Marcar deseo cumplido", "Mark wish as fulfilled", "Marquer le souhait comme accompli")} />
	              </button>
	              <button class="purpose-pill" type="button" id="purpose1">
	                {tr("Deseo #1: Secreto", "Wish #1: Secret", "Souhait n°1 : Secret")}
	              </button>
	              <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock1"
	                data-slot="1" title={tr("Desbloquear deseo 1", "Unlock wish 1", "Déverrouiller le souhait 1")}>
	                <img src="/css/icons/iconkey.webp" alt={tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller le souhait secret")} />
	              </button>
            </div>

            <div class="purpose-pill-row">
	              <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="2"
	                title={tr("Marcar deseo 2 como cumplido", "Mark wish 2 as fulfilled", "Marquer le souhait 2 comme accompli")}>
	                <img src="/css/icons/iconfulfill.webp" alt={tr("Marcar deseo cumplido", "Mark wish as fulfilled", "Marquer le souhait comme accompli")} />
	              </button>
	              <button class="purpose-pill" type="button" id="purpose2">
	                {tr("Deseo de propósito sin definir", "Undefined purpose wish", "Souhait de mission non défini")}
	              </button>
	              <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock2"
	                data-slot="2" title={tr("Desbloquear deseo 2", "Unlock wish 2", "Déverrouiller le souhait 2")}>
	                <img src="/css/icons/iconkey.webp" alt={tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller le souhait secret")} />
	              </button>
            </div>

            <div class="purpose-pill-row">
	              <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="3"
	                title={tr("Marcar deseo 3 como cumplido", "Mark wish 3 as fulfilled", "Marquer le souhait 3 comme accompli")}>
	                <img src="/css/icons/iconfulfill.webp" alt={tr("Marcar deseo cumplido", "Mark wish as fulfilled", "Marquer le souhait comme accompli")} />
	              </button>
	              <button class="purpose-pill" type="button" id="purpose3">
	                {tr("Deseo estar unido a Jesús", "I wish to be united with Jesus", "Je souhaite être uni à Jésus")}
	              </button>
	              <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock3"
	                data-slot="3" title={tr("Desbloquear deseo 3", "Unlock wish 3", "Déverrouiller le souhait 3")}>
	                <img src="/css/icons/iconkey.webp" alt={tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller le souhait secret")} />
	              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

	    <div class="modal-overlay hidden" id="lifeProposalOverlay" aria-hidden="true">
	      <div class="modal modal-wide life-proposal-modal" role="dialog" aria-modal="true"
	        aria-label={tr("Propósito de vida", "Life purpose", "Mission de vie")}>
	        <div class="modal-head">
	          <h3>{tr("Propósito de vida", "Life purpose", "Mission de vie")}</h3>
	          <button class="modal-close" type="button" id="lifeProposalClose">✕</button>
	        </div>

        <div class="modal-body life-proposal-body">
	          <div class="auth-card auth-card--wide auth-card--life life-proposal-card">
	            <h2 class="auth-title">{tr("Tu propósito de vida", "Your life purpose", "Ta mission de vie")}</h2>

            <div class="auth-message">
	              <p>
	                {tr("Escribe tres deseos que orienten tu camino.", "Write three wishes that guide your path.", "Écris trois souhaits qui guident ton chemin.")}
	                <br>
	                {tr("Son brújula, no presión.", "They are a compass, not pressure.", "Ils sont une boussole, pas une pression.")}
	              </p>
	              <p class="muted">
	                {tr("Estos propósitos se guardan cifrados con tu clave privada personal.", "These purposes are stored encrypted with your personal private key.", "Ces missions sont stockées chiffrées avec ta clé privée personnelle.")}
	              </p>
	            </div>

            <form id="life-form">
              <div class="purpose-group" data-purpose="1">
	                <textarea id="p1" class="wish-prefix-input" data-prefix={tr("Deseo ", "Wish ", "Souhait ")} rows="1" maxlength="80"
	                  placeholder={tr("Deseo 1", "Wish 1", "Souhait 1")} required>{tr("Deseo ", "Wish ", "Souhait ")}</textarea>
	                <div class="purpose-actions" role="group" aria-label={tr("Acciones para propósito 1", "Actions for purpose 1", "Actions pour la mission 1")}>
	                  <button type="button" class="purpose-action" data-action="confirm"
	                    title={tr("Confirmar deseo de propósito", "Confirm purpose wish", "Confirmer le souhait de mission")} aria-label={tr("Confirmar deseo de propósito", "Confirm purpose wish", "Confirmer le souhait de mission")}>
	                    <img src="/css/icons/iconsave.webp" alt={tr("Guardar propósito", "Save purpose", "Enregistrer la mission")}>
	                  </button>
	                  <button type="button" class="purpose-action" data-action="secret" title={tr("Convertir en secreto", "Convert to secret", "Convertir en secret")}
	                    aria-label={tr("Convertir en secreto", "Convert to secret", "Convertir en secret")}>
	                    <img src="/css/icons/iconkey.webp" alt={tr("Marcar como secreto", "Mark as secret", "Marquer comme secret")}>
	                  </button>
	                  <button type="button" class="purpose-action" data-action="reveal" title={tr("Revelar en fecha", "Reveal on date", "Révéler à la date")}
	                    aria-label={tr("Revelar en fecha", "Reveal on date", "Révéler à la date")}>
	                    <img src="/css/icons/iconcalendar.webp" alt={tr("Programar fecha", "Schedule date", "Date planifiée")}>
	                  </button>
	                  <button type="button" class="purpose-action" data-action="icon" title={tr("Elegir icono", "Choose icon", "Choisir une icône")}
	                    aria-label={tr("Elegir icono", "Choose icon", "Choisir une icône")}>
	                    <img src="/css/icons/iconelemental.webp" alt={tr("Elegir icono", "Choose icon", "Choisir une icône")}>
	                  </button>
	                </div>
	                <input type="date" class="purpose-date" aria-label={tr("Fecha de revelación para propósito 1", "Reveal date for purpose 1", "Date de révélation pour la mission 1")}>
	                <div class="purpose-icon-panel" aria-label={tr("Selector de iconos", "Icon selector", "Sélecteur d'icône")}>
	                  <button type="button" class="purpose-icon" data-icon="air" title={tr("Aire", "Air", "Air")}>
	                    <img src="assets/air.png" alt={tr("Aire", "Air", "Air")}>
	                  </button>
	                  <button type="button" class="purpose-icon" data-icon="earth" title={tr("Tierra", "Earth", "Terre")}>
	                    <img src="assets/earth.png" alt={tr("Tierra", "Earth", "Terre")}>
	                  </button>
	                  <button type="button" class="purpose-icon" data-icon="water" title={tr("Agua", "Water", "Eau")}>
	                    <img src="assets/water.png" alt={tr("Agua", "Water", "Eau")}>
	                  </button>
	                  <button type="button" class="purpose-icon" data-icon="fire" title={tr("Fuego", "Fire", "Feu")}>
	                    <img src="assets/fire.png" alt={tr("Fuego", "Fire", "Feu")}>
	                  </button>
	                </div>
	                <div class="purpose-status" aria-live="polite">{tr("Estado: público por defecto.", "Status: public by default.", "Statut : public par défaut.")}</div>
	              </div>

	              <div class="purpose-group" data-purpose="2">
	                <textarea id="p2" class="wish-prefix-input" data-prefix={tr("Deseo ", "Wish ", "Souhait ")} rows="1" maxlength="80"
	                  placeholder={tr("Deseo 2", "Wish 2", "Souhait 2")} required>{tr("Deseo ", "Wish ", "Souhait ")}</textarea>
	                <div class="purpose-actions" role="group" aria-label={tr("Acciones para propósito 2", "Actions for purpose 2", "Actions pour la mission 2")}>
	                  <button type="button" class="purpose-action" data-action="confirm"
	                    title={tr("Confirmar deseo de propósito", "Confirm purpose wish", "Confirmer le souhait de mission")} aria-label={tr("Confirmar deseo de propósito", "Confirm purpose wish", "Confirmer le souhait de mission")}>
	                    <img src="/css/icons/iconsave.webp" alt={tr("Guardar propósito", "Save purpose", "Enregistrer la mission")}>
	                  </button>
	                  <button type="button" class="purpose-action" data-action="secret" title={tr("Convertir en secreto", "Convert to secret", "Convertir en secret")}
	                    aria-label={tr("Convertir en secreto", "Convert to secret", "Convertir en secret")}>
	                    <img src="/css/icons/iconkey.webp" alt={tr("Marcar como secreto", "Mark as secret", "Marquer comme secret")}>
	                  </button>
	                  <button type="button" class="purpose-action" data-action="reveal" title={tr("Revelar en fecha", "Reveal on date", "Révéler à la date")}
	                    aria-label={tr("Revelar en fecha", "Reveal on date", "Révéler à la date")}>
	                    <img src="/css/icons/iconcalendar.webp" alt={tr("Programar fecha", "Schedule date", "Date planifiée")}>
	                  </button>
	                  <button type="button" class="purpose-action" data-action="icon" title={tr("Elegir icono", "Choose icon", "Choisir une icône")}
	                    aria-label={tr("Elegir icono", "Choose icon", "Choisir une icône")}>
	                    <img src="/css/icons/iconelemental.webp" alt={tr("Elegir icono", "Choose icon", "Choisir une icône")}>
	                  </button>
	                </div>
	                <input type="date" class="purpose-date" aria-label={tr("Fecha de revelación para propósito 2", "Reveal date for purpose 2", "Date de révélation pour la mission 2")}>
	                <div class="purpose-icon-panel" aria-label={tr("Selector de iconos", "Icon selector", "Sélecteur d'icône")}>
	                  <button type="button" class="purpose-icon" data-icon="air" title={tr("Aire", "Air", "Air")}>
	                    <img src="assets/air.png" alt={tr("Aire", "Air", "Air")}>
	                  </button>
	                  <button type="button" class="purpose-icon" data-icon="earth" title={tr("Tierra", "Earth", "Terre")}>
	                    <img src="assets/earth.png" alt={tr("Tierra", "Earth", "Terre")}>
	                  </button>
	                  <button type="button" class="purpose-icon" data-icon="water" title={tr("Agua", "Water", "Eau")}>
	                    <img src="assets/water.png" alt={tr("Agua", "Water", "Eau")}>
	                  </button>
	                  <button type="button" class="purpose-icon" data-icon="fire" title={tr("Fuego", "Fire", "Feu")}>
	                    <img src="assets/fire.png" alt={tr("Fuego", "Fire", "Feu")}>
	                  </button>
	                </div>
	                <div class="purpose-status" aria-live="polite">{tr("Estado: público por defecto.", "Status: public by default.", "Statut : public par défaut.")}</div>
	              </div>

	              <div class="purpose-group" data-purpose="3">
	                <textarea id="p3" class="wish-prefix-input" data-prefix={tr("Deseo ", "Wish ", "Souhait ")} rows="1" maxlength="80"
	                  placeholder={tr("Deseo 3", "Wish 3", "Souhait 3")} required>{tr("Deseo ", "Wish ", "Souhait ")}</textarea>
	                <div class="purpose-actions" role="group" aria-label={tr("Acciones para propósito 3", "Actions for purpose 3", "Actions pour la mission 3")}>
	                  <button type="button" class="purpose-action" data-action="confirm"
	                    title={tr("Confirmar deseo de propósito", "Confirm purpose wish", "Confirmer le souhait de mission")} aria-label={tr("Confirmar deseo de propósito", "Confirm purpose wish", "Confirmer le souhait de mission")}>
	                    <img src="/css/icons/iconsave.webp" alt={tr("Guardar propósito", "Save purpose", "Enregistrer la mission")}>
	                  </button>
	                  <button type="button" class="purpose-action" data-action="secret" title={tr("Convertir en secreto", "Convert to secret", "Convertir en secret")}
	                    aria-label={tr("Convertir en secreto", "Convert to secret", "Convertir en secret")}>
	                    <img src="/css/icons/iconkey.webp" alt={tr("Marcar como secreto", "Mark as secret", "Marquer comme secret")}>
	                  </button>
	                  <button type="button" class="purpose-action" data-action="reveal" title={tr("Revelar en fecha", "Reveal on date", "Révéler à la date")}
	                    aria-label={tr("Revelar en fecha", "Reveal on date", "Révéler à la date")}>
	                    <img src="/css/icons/iconcalendar.webp" alt={tr("Programar fecha", "Schedule date", "Date planifiée")}>
	                  </button>
	                  <button type="button" class="purpose-action" data-action="icon" title={tr("Elegir icono", "Choose icon", "Choisir une icône")}
	                    aria-label={tr("Elegir icono", "Choose icon", "Choisir une icône")}>
	                    <img src="/css/icons/iconelemental.webp" alt={tr("Elegir icono", "Choose icon", "Choisir une icône")}>
	                  </button>
	                </div>
	                <input type="date" class="purpose-date" aria-label={tr("Fecha de revelación para propósito 3", "Reveal date for purpose 3", "Date de révélation pour la mission 3")}>
	                <div class="purpose-icon-panel" aria-label={tr("Selector de iconos", "Icon selector", "Sélecteur d'icône")}>
	                  <button type="button" class="purpose-icon" data-icon="air" title={tr("Aire", "Air", "Air")}>
	                    <img src="assets/air.png" alt={tr("Aire", "Air", "Air")}>
	                  </button>
	                  <button type="button" class="purpose-icon" data-icon="earth" title={tr("Tierra", "Earth", "Terre")}>
	                    <img src="assets/earth.png" alt={tr("Tierra", "Earth", "Terre")}>
	                  </button>
	                  <button type="button" class="purpose-icon" data-icon="water" title={tr("Agua", "Water", "Eau")}>
	                    <img src="assets/water.png" alt={tr("Agua", "Water", "Eau")}>
	                  </button>
	                  <button type="button" class="purpose-icon" data-icon="fire" title={tr("Fuego", "Fire", "Feu")}>
	                    <img src="assets/fire.png" alt={tr("Fuego", "Fire", "Feu")}>
	                  </button>
	                </div>
	                <div class="purpose-status" aria-live="polite">{tr("Estado: público por defecto.", "Status: public by default.", "Statut : public par défaut.")}</div>
	              </div>

	              <button type="submit" class="btn btn-primary">{tr("Guardar propósito", "Save purpose", "Enregistrer la mission")}</button>
	              <button type="button" class="btn btn-outline" id="lifeProposalCloseFooter">{tr("Volver", "Back", "Retour")}</button>
            </form>

            <div class="auth-brand">
              <img src="/css/logo-kiadez.webp" alt="Kiadez" />
              <span>Kiadez</span>
            </div>
          </div>
        </div>
      </div>
    </div>

	    <div class="modal-overlay hidden" id="lifeConfirmOverlay" aria-hidden="true">
	      <div class="modal" role="dialog" aria-modal="true" aria-label={tr("Confirmar propósito público", "Confirm public purpose", "Confirmer la mission publique")}>
	        <div class="modal-head">
	          <h3>{tr("Confirmar propósito", "Confirm purpose", "Confirmer la mission")}</h3>
	          <button class="modal-close" type="button" id="lifeConfirmClose">✕</button>
	        </div>

	        <div class="modal-body">
	          <p class="modal-label-center" id="lifeConfirmText">
	            {tr("¿Confirmar este deseo como público?", "Confirm this wish as public?", "Confirmer ce souhait comme public ?")}
	          </p>
	          <p class="modal-label-center muted">
	            {tr("Se guardará como público.", "It will be saved as public.", "Il sera enregistré comme public.")}
	          </p>
        </div>

	        <div class="modal-actions">
	          <button class="btn btn-outline btn-compact" type="button" id="lifeConfirmCancel">{tr("Cancelar", "Cancel", "Annuler")}</button>
	          <button class="btn btn-primary btn-compact" type="button" id="lifeConfirmOk">{tr("Confirmar", "Confirm", "Confirmer")}</button>
	        </div>
	      </div>
	    </div>

	    <div class="modal-overlay hidden" id="purposeUnlockOverlay" aria-hidden="true">
	      <div class="modal wish-modal purpose-unlock-modal" role="dialog" aria-modal="true"
	        aria-label={tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller le souhait secret")}>
	        <div class="modal-head">
	          <h3>{tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller le souhait secret")}</h3>
	          <button class="modal-close" type="button" id="purposeUnlockClose">✕</button>
	        </div>
	        <div class="modal-body">
	          <p class="modal-label-center" id="purposeUnlockText">
	            {tr("Si confirmas tu clave privada, este deseo se volverá público.", "If you confirm your private key, this wish will become public.", "Si tu confirmes ta clé privée, ce souhait deviendra public.")}
	          </p>
	          <label class="modal-label hidden" for="purposeUnlockPassword">{tr("Clave privada personal", "Personal private key", "Clé privée personnelle")}</label>
	          <input class="modal-input" id="purposeUnlockPassword" type="password" autocomplete="off"
	            placeholder={tr("Clave privada personal", "Personal private key", "Clé privée personnelle")} />
          <p class="purpose-unlock-error" id="purposeUnlockError" aria-live="polite"></p>
        </div>
	        <div class="modal-actions">
	          <button class="btn btn-outline btn-compact" type="button" id="purposeUnlockCancel">{tr("Cancelar", "Cancel", "Annuler")}</button>
	          <button class="btn btn-primary btn-compact" type="button" id="purposeUnlockConfirm">{tr("Desbloquear", "Unlock", "Déverrouiller")}</button>
	        </div>
	      </div>
	    </div>

    <div class="public-wishes-body">
      <!-- =========================
       *  NAV / LINKS
       *  ========================= -->
		      <nav class="profile-nav" aria-label={tr("Navegación de perfil", "Profile navigation", "Navigation du profil")}>
		        <a class="nav-pill" href="/home_user.html" title="Home" data-profile-module="home">Home</a>
		        <a class="nav-pill" href="/star-pool-found.html" title={tr("Estrellas", "Stars", "Étoiles")}>
		          <span class="nav-icon">⭐</span>
		          <span><strong id="myPublicWishesStarsTotal">0</strong> {tr("estrellas", "stars", "étoiles")}</span>
		        </a>
		        <a class="nav-pill" href="/followers.html" title={tr("Seguidores", "Followers", "Abonnés")}>{tr("Seguidores", "Followers", "Abonnés")}</a>
		        <a class="nav-pill" href="/achievements.html" title={tr("Logros recientes", "Recent achievements", "Réalisations récentes")}>{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
		        <a class="nav-pill" href="/gallery.html" title={tr("Galería", "Gallery", "Galerie")}>{tr("Galería", "Gallery", "Galerie")}</a>
		        <a class="nav-pill" href="/calendar.html" title={tr("Calendario", "Calendar", "Calendrier")} data-profile-module="calendar">{tr("Calendario", "Calendar", "Calendrier")}</a>
		        <a class="nav-pill" href="/my-biography.html" title={tr("Mi biografía", "My biography", "Ma biographie")}>{tr("Mi biografía", "My biography", "Ma biographie")}</a>
	        <a class="nav-pill" href="/messages.html" title={tr("Mensajes", "Messages", "Messagerie")}>{tr("Mensajes", "Messages", "Messagerie")}</a>
		      </nav>

      <!-- =========================
       *  MIS DESEOS PUBLICOS
       *  ========================= -->
	      <section class="public-wishes-shell" aria-label={tr("Mis deseos públicos", "My public wishes", "Mes souhaits publics")}>
	        <header class="public-wishes-head">
	          <div>
	            <h2 class="public-wishes-title">{tr("Mis deseos públicos", "My public wishes", "Mes souhaits publics")}</h2>
	          </div>
	        </header>

        <!-- =========================
         *  LISTAS DE DESEOS
         *  ========================= -->
	        <section class="wish-lists-grid" aria-label={tr("Listas de deseos", "Wish lists", "Listes de souhaits")}>
	          <article class="panel wish-list-panel">
	            <div class="panel-head">
	              <h3 class="panel-title">{tr("Deseos personales", "Personal wishes", "Souhaits personnels")}</h3>
	              <span class="panel-badge"><span id="personalWishCount">7</span> / 50</span>
	            </div>

	            <ol class="wish-slot-list" id="personalWishList" data-total="50" aria-label={tr("Deseos personales", "Personal wishes", "Souhaits personnels")}>
	            </ol>
	            <div class="wish-add-row">
	              <button class="wish-add-btn" id="personalWishAdd" type="button" title={tr("Agregar deseo", "Add wish", "Ajouter un souhait")}>
	                <span class="wish-add-plus">+</span>
	              </button>
	            </div>
	          </article>

	          <article class="panel wish-list-panel" id="cooperative-wishes">
	            <div class="panel-head">
	              <h3 class="panel-title">{tr("Deseos cooperativos", "Cooperative wishes", "Souhaits coopératifs")}</h3>
	              <span class="panel-badge"><span id="cooperativeWishCountLabel">0</span> / 20</span>
	            </div>
	            <ol class="wish-slot-list" id="cooperativeWishList" data-total="0" aria-label={tr("Deseos cooperativos", "Cooperative wishes", "Souhaits coopératifs")}>
	            </ol>
	            <div class="wish-add-row">
	              <button class="wish-add-btn" id="cooperativeWishAdd" type="button" title={tr("Agregar deseo cooperativo", "Add cooperative wish", "Ajouter un souhait coopératif")}>
	                <span class="wish-add-plus">+</span>
	              </button>
	            </div>
          </article>
        </section>

	        <template id="wishLampSlotTemplate">
	          <div class="wish-slot-row wish-slot-row-empty">
	            <button class="wish-add-btn wish-lamp-btn" type="button" title={tr("Agregar deseo", "Add wish", "Ajouter un souhait")}>
	              <img class="wish-lamp-icon" src="/css/icons/iconlamp.webp" alt={tr("Agregar deseo", "Add wish", "Ajouter un souhait")} />
	            </button>
	          </div>
	        </template>

        <template id="wishChoiceInlineTemplate">
          <div class="wish-slot-row wish-slot-row-choice">
            <div class="wish-choice-inline">
	              <button class="wish-choice-card wish-choice-btn" type="button" data-choice="personal">
	                <span class="wish-config-icon">
	                  <img src="/css/icons/iconpersonal.webp" alt={tr("Deseo personal", "Personal wish", "Souhait personnel")} />
	                </span>
	                <span>{tr("¿Es un deseo individual?", "Is it an individual wish?", "Est-ce un souhait individuel ?")}</span>
	              </button>
	              <button class="wish-choice-card wish-choice-btn" type="button" data-choice="cooperative">
	                <span class="wish-config-icon">
	                  <img src="/css/icons/iconcooperative.webp" alt={tr("Deseo cooperativo", "Cooperative wish", "Souhait coopératif")} />
	                </span>
	                <span>{tr("¿Es un deseo cooperativo?", "Is it a cooperative wish?", "Est-ce un souhait coopératif ?")}</span>
	              </button>
	              <button class="wish-choice-card wish-choice-cancel" type="button" aria-label={tr("Cancelar", "Cancel", "Annuler")}>
	                <span class="wish-choice-cancel-icon">✕</span>
	              </button>
            </div>
          </div>
        </template>

	        <div class="modal-overlay hidden" id="personalWishModal" aria-hidden="true">
	          <div class="modal modal-wide personal-wish-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Configurar deseo personal", "Set up personal wish", "Configurer un souhait personnel")}>
	            <div class="modal-head">
	              <h3>{tr("Configurar deseo personal", "Set up personal wish", "Configurer un souhait personnel")}</h3>
	              <button class="modal-close" type="button" id="closePersonalWishModal">✕</button>
	            </div>
	            <div class="modal-body personal-wish-body">
	              <div class="wish-modal-grid">
	                <div class="wish-modal-col">
	                  <div class="wish-config-icon personal-wish-hero">
	                    <img src="/css/icons/iconpersonal.webp" alt={tr("Deseo personal", "Personal wish", "Souhait personnel")} />
	                  </div>
	                  <h2 class="modal-label modal-label-center">{tr("Descripción del deseo", "Wish description", "Description du souhait")}</h2>
	                  <label class="modal-label hidden" for="personalWishText">{tr("Descripción del deseo", "Wish description", "Description du souhait")}</label>
	                  <textarea class="modal-textarea wish-prefix-input wish-textarea-compact" id="personalWishText"
	                    rows="3" maxlength="80" data-prefix={tr("Deseo ", "Wish ", "Souhait ")} data-counter="personalWishCounter"></textarea>
	                  <div class="wish-counter" id="personalWishCounter" aria-live="polite">0/80</div>
	                  <div class="wish-error" id="personalWishError" role="alert">{tr("No has descrito tu deseo", "You have not described your wish", "Tu n'as pas décrit ton souhait")}</div>
	                  <div class="wish-warning">
	                    <span class="wish-warning-icon">!</span>
	                    <span id="personalWishTypeHint">
	                      {tr(
	                        "Deseos relacionados con el sentido de vida, la conciencia, la fe, la paz interior y el crecimiento espiritual. Ejemplo: perseverar en el hábito de la meditación, leer libros sobre espiritualidad, asistir a misa.",
	                        "Wishes related to life meaning, awareness, faith, inner peace, and spiritual growth. Example: keep a meditation habit, read spirituality books, attend mass."
	                      )}
	                    </span>
	                  </div>
                </div>

                <div class="wish-modal-col">
                  <fieldset class="wish-type-fieldset">
                    <div class="wish-type-selected">
	                      <img id="personalWishTypeIcon" src="/css/icons/Espiritual.webp" alt={tr("Espiritual", "Spiritual", "Spirituel")} />
	                    </div>
	                    <h2 class="modal-label modal-label-center">{tr("Tipo de deseo", "Wish type", "Type de souhait")}</h2>
                    <div class="wish-type-grid">
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Espiritual" checked />
                        <span class="wish-type-visual">
	                          <span>{tr("Espiritual", "Spiritual", "Spirituel")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Material" />
                        <span class="wish-type-visual">
	                          <span>{tr("Material", "Material", "Matériel")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Monetario" />
                        <span class="wish-type-visual">
	                          <span>{tr("Monetario", "Financial", "Financier")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Profesional" />
                        <span class="wish-type-visual">
	                          <span>{tr("Profesional", "Professional", "Professionnel")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Salud y cuerpo" />
                        <span class="wish-type-visual">
	                          <span>{tr("Salud y cuerpo", "Health and body", "Santé et corps")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Relacional" />
                        <span class="wish-type-visual">
	                          <span>{tr("Relacional", "Relational", "Relationnel")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Vivencial" />
                        <span class="wish-type-visual">
	                          <span>{tr("Vivencial", "Experiential", "Expérientiel")}</span>
                        </span>
                      </label>
                    </div>
                  </fieldset>
                </div>

                <div class="wish-modal-col">
	                  <h2 class="modal-label modal-label-center">{tr("Agregar imagen", "Add image", "Ajouter une image")}</h2>
	                  <label class="modal-label hidden" for="personalWishMedia">{tr("Agregar imagen", "Add image", "Ajouter une image")}</label>
	                  <input class="modal-input hidden" id="personalWishMedia" type="file" accept="image/*" />
	                  <div class="wish-image-preview" id="personalWishPreview" aria-live="polite">
	                    <label class="wish-image-btn" for="personalWishMedia" aria-label={tr("Seleccionar imagen", "Select image", "Sélectionner une image")}>+</label>
	                    <div class="wish-preview-content">
	                      <span class="wish-preview-placeholder">{tr("Seleccionar imagen", "Select image", "Sélectionner une image")}</span>
	                      <span class="wish-preview-name" id="personalWishFileName">{tr("Sin imagen seleccionada", "No image selected", "Aucune image sélectionnée")}</span>
	                    </div>
	                  </div>
	                  <div class="wish-config-icon personal-wish-hero">
	                    <img src="/css/icons/iconsave.webp" alt={tr("guardar", "save", "enregistrer")} />
	                  </div>
	                  <div class="wish-form-actions wish-form-actions-center">
	                    <br>
	                    <button class="btn btn-primary btn-compact btn-icon" type="button" id="confirmPersonalWish">
	                      {tr("¡Confirmar mi deseo!", "Confirm my wish!", "Confirmer mon souhait !")}
	                    </button>
	                  </div>
	                </div>
	              </div>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="cooperativeWishModal" aria-hidden="true">
	          <div class="modal modal-wide cooperative-wish-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Configurar deseo cooperativo", "Set up cooperative wish", "Configurer un souhait coopératif")}>
	            <div class="modal-head">
	              <h3>{tr("Configurar deseo cooperativo", "Set up cooperative wish", "Configurer un souhait coopératif")}</h3>
	              <button class="modal-close" type="button" id="closeCooperativeWishModal">✕</button>
	            </div>
            <div class="modal-body cooperative-wish-body">
              <div class="wish-modal-grid">
	                <div class="wish-modal-col">
	                  <div class="wish-config-icon personal-wish-hero">
	                    <img src="/css/icons/iconcooperative.webp" alt={tr("Deseo cooperativo", "Cooperative wish", "Souhait coopératif")} />
	                  </div>
	                  <h2 class="modal-label modal-label-center">{tr("Descripción del deseo", "Wish description", "Description du souhait")}</h2>
	                  <label class="modal-label hidden" for="cooperativeWishText">{tr("Descripción del deseo cooperativo", "Cooperative wish description", "Description du souhait coopératif")}</label>
		                  <h5 class="modal-label modal-label-center"><i>{tr("Ejemplo: Deseo nivelar a 10 personajes del videojuego Dofus, del servidor Tal Kasha, a nivel 200 en Anutropia.", "Example: I wish to level up 10 characters in Dofus, on Tal Kasha server, to level 200 in Enutrosor.", "Exemple : je souhaite monter 10 personnages sur Dofus, serveur Tal Kasha, au niveau 200 à Enutrosor.")}</i></h5>
	                  <textarea class="modal-textarea wish-prefix-input wish-textarea-compact" id="cooperativeWishText"
	                    rows="3" maxlength="120" data-prefix={tr("Deseo ", "Wish ", "Souhait ")}>{tr("Deseo ", "Wish ", "Souhait ")}</textarea>
	                  <div class="wish-warning">
	                    <span class="wish-warning-icon">!</span>
	                    <span id="cooperativeWishTypeHint">
	                      {tr(
	                        "Deseos relacionados con el sentido de vida, la conciencia, la fe, la paz interior y el crecimiento espiritual. Ejemplo: perseverar en el hábito de la meditación, leer libros sobre espiritualidad, asistir a misa.",
	                        "Wishes related to life meaning, awareness, faith, inner peace, and spiritual growth. Example: keep a meditation habit, read spirituality books, attend mass."
	                      )}
	                    </span>
	                  </div>
	                  <label class="modal-label" for="cooperativeWishSecurityCode">{tr("Código de seguridad", "Security code", "Code de sécurité")}</label>
                  <input class="modal-input" id="cooperativeWishSecurityCode" type="text" inputmode="numeric"
                    maxlength="6" placeholder="000000" />
	                  <div class="wish-error" id="cooperativeWishError" role="alert">{tr("No has descrito tu deseo cooperativo.", "You have not described your cooperative wish.", "Tu n'as pas décrit ton souhait coopératif.")}</div>
                </div>

                <div class="wish-modal-col">
                  <fieldset class="wish-type-fieldset">
                    <div class="wish-type-selected">
	                      <img id="cooperativeWishTypeIcon" src="/css/icons/Espiritual.webp" alt={tr("Espiritual", "Spiritual", "Spirituel")} />
	                    </div>
	                    <h2 class="modal-label modal-label-center">{tr("Tipo de deseo", "Wish type", "Type de souhait")}</h2>
                    <div class="wish-type-grid">
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Espiritual" checked />
                        <span class="wish-type-visual">
	                          <span>{tr("Espiritual", "Spiritual", "Spirituel")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Material" />
                        <span class="wish-type-visual">
	                          <span>{tr("Material", "Material", "Matériel")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Profesional" />
                        <span class="wish-type-visual">
	                          <span>{tr("Profesional", "Professional", "Professionnel")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Salud y cuerpo" />
                        <span class="wish-type-visual">
	                          <span>{tr("Salud y cuerpo", "Health and body", "Santé et corps")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Relacional" />
                        <span class="wish-type-visual">
	                          <span>{tr("Relacional", "Relational", "Relationnel")}</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Vivencial" />
                        <span class="wish-type-visual">
	                          <span>{tr("Vivencial", "Experiential", "Expérientiel")}</span>
                        </span>
                      </label>
                    </div>
                  </fieldset>
                </div>

                <div class="wish-modal-col">
	                  <h2 class="modal-label modal-label-center">{tr("Configuración cooperativa", "Cooperative setup", "Configuration coopérative")}</h2>

	                  <h3 class="modal-label modal-label-center">{tr("Número máximo de personas participantes (máximo 10)", "Maximum number of participants (max 10)", "Nombre maximum de participants (max 10)")}</h3>
                  <input class="modal-input" id="cooperativeWishCount" type="number" min="1" max="10" value="10" />

	                  <h3 class="modal-label modal-label-center">{tr("Dale al usuario una idea de cómo apropiarse de este deseo", "Give the user an idea of how to personalize this wish", "Donne à l'utilisateur une idée de comment personnaliser ce souhait")}</h3>
                  <h5 class="modal-label modal-label-center"><i>Ejemplo:Deseo que el Team Guardian nivele, en el
                      servidor Tal Kasha, a mi personaje llamado... *este espacio libro sera rellenado por el
                      usuario*</i></h5>
	                  <textarea class="modal-textarea" id="cooperativeWishTemplate" rows="4"
	                    data-suffix={tr("*este espacio libre será rellenado por el usuario.*", "*this free space will be filled by the user.*", "*cet espace libre sera rempli par l'utilisateur.*")}>{tr("Deseo *este espacio libre será rellenado por el usuario.*", "Wish *this free space will be filled by the user.*", "Souhait *cet espace libre sera rempli par l'utilisateur.*")}</textarea>
	                </div>

	                <div class="wish-modal-col">
	                  <h2 class="modal-label modal-label-center">{tr("Agregar imagen", "Add image", "Ajouter une image")}</h2>
	                  <label class="modal-label hidden" for="cooperativeWishMedia">{tr("Agregar imagen", "Add image", "Ajouter une image")}</label>
	                  <input class="modal-input hidden" id="cooperativeWishMedia" type="file" accept="image/*" />
	                  <div class="wish-image-preview" id="cooperativeWishPreview" aria-live="polite">
	                    <label class="wish-image-btn" for="cooperativeWishMedia" aria-label={tr("Seleccionar imagen", "Select image", "Sélectionner une image")}>+</label>
	                    <div class="wish-preview-content">
	                      <span class="wish-preview-placeholder">{tr("Seleccionar imagen", "Select image", "Sélectionner une image")}</span>
	                      <span class="wish-preview-name" id="cooperativeWishFileName">{tr("Sin imagen seleccionada", "No image selected", "Aucune image sélectionnée")}</span>
	                    </div>
	                  </div>
	                  <div class="wish-config-icon personal-wish-hero">
	                    <img src="/css/icons/iconsave.webp" alt={tr("guardar", "save", "enregistrer")} />
	                  </div>
	                  <div class="wish-form-actions wish-form-actions-center">
	                    <br>
	                    <button class="btn btn-primary btn-compact btn-icon" type="button" id="confirmCooperativeWish">
	                      {tr("¡Confirmar deseo cooperativo!", "Confirm cooperative wish!", "Confirmer le souhait coopératif !")}
	                    </button>
	                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

	        <div class="modal-overlay hidden" id="deleteWishModal" aria-hidden="true">
	          <div class="modal wish-modal delete-wish-modal" role="dialog" aria-modal="true" aria-label={tr("Borrar deseo", "Delete wish", "Supprimer le souhait")}>
	            <div class="modal-head">
	              <h3>{tr("¿Estás seguro de que deseas borrar este deseo?", "Are you sure you want to delete this wish?", "Es-tu sûr de vouloir supprimer ce souhait ?")}</h3>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="confirmDeleteWish">{tr("Sí", "Yes", "Oui")}</button>
	              <button class="btn btn-outline btn-compact" type="button" id="cancelDeleteWish">{tr("No", "No", "Non")}</button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="fulfillWishModal" aria-hidden="true">
	          <div class="modal wish-modal fulfill-wish-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Subir evidencia", "Upload evidence", "Téléverser une preuve")}>
	            <div class="modal-head">
	              <h3>{tr("¡Sube la evidencia!", "Upload the evidence!", "Téléverse la preuve !")}</h3>
	            </div>
	            <div class="modal-body">
	              <input id="fulfillEvidence" type="file" accept="image/*" class="hidden" />
	              <div class="wish-image-preview" id="fulfillEvidencePreview" aria-live="polite">
	                <label class="wish-image-btn" for="fulfillEvidence" aria-label={tr("Sube la evidencia visual", "Upload visual evidence", "Téléverser une preuve visuelle")}>+</label>
	                <div class="wish-preview-content">
	                  <span class="wish-preview-placeholder">{tr("Sube la evidencia visual.", "Upload visual evidence.", "Téléverser une preuve visuelle.")}</span>
	                  <span class="wish-preview-name">PNG, WEBP, JPEG, etc.</span>
	                </div>
	              </div>
	              <p class="panel-muted">
	                <strong>{tr("¿Declaras bajo verdad de juramento que este deseo se ha cumplido?", "Do you swear that this wish has been fulfilled?", "Jures-tu que ce souhait a été accompli ?")}</strong>
	              </p>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="confirmFulfillWish">
	                {tr("Juro bajo verdad de juramento que este deseo se ha cumplido", "I swear that this wish has been fulfilled", "Je jure que ce souhait a été accompli")}
	              </button>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-outline btn-compact" type="button" id="cancelFulfillWish">{tr("Cancelar", "Cancel", "Annuler")}</button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="guardianFulfillModal" aria-hidden="true">
	          <div class="modal wish-modal fulfill-wish-modal guardian-fulfill-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Marcar deseo como cumplido (Guardián)", "Mark wish as fulfilled (Guardian)", "Marquer le souhait comme accompli (Gardien)")}>
	            <div class="modal-head">
	              <h3>{tr("¡Sube la evidencia!", "Upload the evidence!", "Téléverse la preuve !")}</h3>
	              <button class="modal-close" type="button" id="guardianFulfillClose">✕</button>
	            </div>
	            <div class="modal-body">
	              <label class="modal-label" for="guardianFulfillCommitmentCode">{tr("Espacio para el código de compromiso", "Commitment code field", "Champ du code d'engagement")}</label>
              <input
                class="modal-input guardian-fulfill-commitment-input"
                id="guardianFulfillCommitmentCode"
                type="text"
                maxlength="32"
                autocomplete="off"
                placeholder="KZ-204-00045"
              />
	              <div class="wish-error" id="guardianFulfillCodeError" role="alert">
	                {tr("Debes indicar el código de compromiso.", "You must enter the commitment code.", "Tu dois saisir le code d'engagement.")}
	              </div>

              <input id="guardianFulfillEvidence" type="file" accept="image/*" class="hidden" />
	              <div class="wish-image-preview" id="guardianFulfillEvidencePreview" aria-live="polite">
	                <label class="wish-image-btn" for="guardianFulfillEvidence" aria-label={tr("Sube la evidencia visual", "Upload visual evidence", "Téléverser une preuve visuelle")}>+</label>
	                <div class="wish-preview-content">
	                  <span class="wish-preview-placeholder">{tr("Sube la evidencia visual.", "Upload visual evidence.", "Téléverser une preuve visuelle.")}</span>
	                  <span class="wish-preview-name">PNG, WEBP, JPEG, etc.</span>
	                </div>
	              </div>

	              <p class="panel-muted">
	                <strong>{tr("¿Cómo deseas publicar la concesión de este deseo?", "How do you want to publish the granting of this wish?", "Comment veux-tu publier l'accomplissement de ce souhait ?")}</strong>
	              </p>
	              <div class="guardian-fulfill-attribution">
	                <button class="guardian-fulfill-attribution-btn" type="button" id="guardianFulfillAttributionSecret">
	                  {tr("Quien cumple el deseo decidió obrar desde lo secreto", "The person fulfilling the wish chose to act in secret", "La personne qui accomplit le souhait a choisi d'agir en secret")}
	                </button>
	                <button class="guardian-fulfill-attribution-btn" type="button" id="guardianFulfillAttributionPublic">
	                  {tr("Quien cumple el deseo desea atribuirse públicamente la concesión del deseo", "The person fulfilling the wish wants public attribution", "La personne qui accomplit le souhait veut une attribution publique")}
	                </button>
	              </div>
	              <div class="wish-error" id="guardianFulfillAttributionError" role="alert">
	                {tr("Debes seleccionar cómo se publicará esta concesión.", "You must select how this granting will be published.", "Tu dois select how this granting will be published.")}
	              </div>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="guardianFulfillSubmit">
	                {tr("Confirmar y publicar deseo cumplido", "Confirm and publish fulfilled wish", "Confirmer et publier le souhait accompli")}
	              </button>
	              <button class="btn btn-outline btn-compact" type="button" id="guardianFulfillCancel">{tr("Cancelar", "Cancel", "Annuler")}</button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="icanConfirmModal" aria-hidden="true">
	          <div class="modal wish-modal ican-confirm-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Conceder deseo", "Grant wish", "Accorder le souhait")}>
	            <div class="modal-head">
	              <h3>{tr("Yo puedo conceder ese deseo", "I can grant this wish", "Je peux accorder ce souhait")}</h3>
	            </div>
	            <div class="modal-body">
	              <p class="panel-muted">{tr("¿Estás seguro de que deseas cumplir este deseo?", "Are you sure you want to fulfill this wish?", "Es-tu sûr de vouloir accomplir ce souhait ?")}</p>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="icanConfirmYes">{tr("Sí", "Yes", "Oui")}</button>
	              <button class="btn btn-outline btn-compact" type="button" id="icanConfirmNo">{tr("No", "No", "Non")}</button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="freezeWishConfirmModal" aria-hidden="true">
	          <div class="modal wish-modal freeze-confirm-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Confirmar congelar deseo", "Confirm freeze wish", "Confirmer le gel du souhait")}>
	            <div class="modal-head">
	              <h3>{tr("¿Estás seguro de que deseas congelar este deseo?", "Are you sure you want to freeze this wish?", "Es-tu sûr de vouloir geler ce souhait ?")}</h3>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="freezeWishConfirmYes">{tr("Sí", "Yes", "Oui")}</button>
	              <button class="btn btn-outline btn-compact" type="button" id="freezeWishConfirmNo">{tr("No", "No", "Non")}</button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="unfreezeWishReasonModal" aria-hidden="true">
	          <div class="modal wish-modal unfreeze-reason-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Seleccionar motivo de descongelación", "Select unfreeze reason", "Sélectionner le motif de déblocage")}>
	            <div class="modal-head">
	              <h3>{tr("Descongelar deseo", "Unfreeze wish", "Débloquer le souhait")}</h3>
	              <button class="modal-close" type="button" id="unfreezeReasonModalClose">✕</button>
	            </div>
	            <div class="modal-body">
	              <p class="panel-muted">{tr("Selecciona el motivo para descongelar este deseo.", "Select the reason to unfreeze this wish.", "Sélectionne la raison de déblocage de ce souhait.")}</p>
	              <div class="unfreeze-reason-actions">
	                <button class="btn btn-outline" type="button" id="unfreezeReasonErrorBtn">
	                  {tr("Deseo congelado por error.", "Wish frozen by mistake.", "Souhait gelé par erreur.")}
	                </button>
	                <button class="btn btn-outline" type="button" id="unfreezeReasonUnexpectedBtn">
	                  {tr("Se presentó un imprevisto", "An unexpected issue occurred", "Un problème inattendu s'est produit")}
	                </button>
	              </div>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-outline btn-compact" type="button" id="unfreezeReasonCancel">{tr("Cancelar", "Cancel", "Annuler")}</button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="unfreezeWishUnexpectedModal" aria-hidden="true">
	          <div class="modal wish-modal unfreeze-unexpected-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Describir imprevisto", "Describe unexpected issue", "Décrire le problème inattendu")}>
	            <div class="modal-head">
	              <h3>{tr("Describe el imprevisto", "Describe the unexpected issue", "Décris le problème inattendu")}</h3>
	              <button class="modal-close" type="button" id="unfreezeUnexpectedModalClose">✕</button>
	            </div>
	            <div class="modal-body">
	              <p class="panel-muted">
	                {tr("Explica brevemente qué ocurrió. Máximo 100 palabras.", "Briefly explain what happened. Maximum 100 words.", "Explique brièvement ce qui s'est passé. Maximum 100 mots.")}
	              </p>
	              <label class="modal-label hidden" for="unfreezeUnexpectedText">{tr("Describe el imprevisto", "Describe the unexpected issue", "Décris le problème inattendu")}</label>
	              <textarea class="modal-textarea" id="unfreezeUnexpectedText" rows="4"
	                placeholder={tr("Describe aquí lo sucedido...", "Describe what happened here...", "Décris ce qui s'est passé ici...")}></textarea>
	              <p class="wish-word-count" id="unfreezeUnexpectedWordCount">{tr("0 / 100 palabras", "0 / 100 words", "0 / 100 mots")}</p>
	              <div class="wish-error" id="unfreezeUnexpectedError" role="alert">
	                {tr("Debes describir el imprevisto para descongelar el deseo.", "You must describe the issue to unfreeze the wish.", "Tu dois décrire le problème pour débloquer le souhait.")}
	              </div>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="unfreezeUnexpectedSubmit">
	                {tr("Descongelar deseo", "Unfreeze wish", "Débloquer le souhait")}
	              </button>
	              <button class="btn btn-outline btn-compact" type="button" id="unfreezeUnexpectedCancel">
	                {tr("Cancelar", "Cancel", "Annuler")}
	              </button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="guardianContactModal" aria-hidden="true">
	          <div class="modal wish-modal guardian-contact-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Contactar a un Guardián", "Contact a Guardian", "Contacter un Gardien")}>
	            <div class="modal-head">
	              <h3>{tr("Contactar a un Guardián", "Contact a Guardian", "Contacter un Gardien")}</h3>
	            </div>
	            <div class="modal-body">
	              <p class="panel-muted guardian-request-context hidden" id="guardianRequestContext"></p>
	              <h2 class="guardian-section-title">{tr("Selecciona a un Guardián", "Select a Guardian", "Sélectionner un Gardien")}</h2>
	              <div class="guardian-row guardian-select" id="guardianSelect"></div>
	              <div class="guardian-pagination">
	                <button class="btn btn-outline btn-compact" type="button" id="guardianPrevPage">{tr("Anterior", "Previous", "Précédent")}</button>
	                <span class="guardian-page" id="guardianPageLabel">1 / 1</span>
	                <button class="btn btn-outline btn-compact" type="button" id="guardianNextPage">{tr("Siguiente", "Next", "Suivant")}</button>
	              </div>
	              <p class="panel-muted guardian-status hidden" id="guardianStatus"></p>

	              <h2 class="guardian-section-title">{tr("Describe por qué deseas conceder ese deseo", "Describe why you want to grant this wish", "Décris pourquoi tu veux accorder ce souhait")}</h2>
	              <label class="modal-label hidden" for="guardianReasonVisitor">{tr("Describe por qué deseas conceder ese deseo", "Describe why you want to grant this wish", "Décris pourquoi tu veux accorder ce souhait")}</label>
	              <textarea class="modal-textarea" id="guardianReasonVisitor" rows="3"></textarea>
	              <div class="wish-error" id="guardianReasonError" role="alert">{tr("Debes describir el motivo.", "You must describe the reason.", "Tu dois décrire la raison.")}</div>

	              <h2 class="guardian-section-title">{tr("Número telefónico", "Phone number", "Numéro de téléphone")}</h2>
	              <label class="modal-label hidden" for="guardianPhoneVisitor">{tr("Número telefónico", "Phone number", "Numéro de téléphone")}</label>
	              <input class="modal-input" id="guardianPhoneVisitor" type="tel" inputmode="tel"
	                placeholder="+57 300 000 0000" />
	              <div class="wish-error" id="guardianPhoneError" role="alert">{tr("Debes indicar tu número telefónico.", "You must provide your phone number.", "Tu dois fournir ton numéro de téléphone.")}</div>

	              <h2 class="guardian-section-title">E-mail</h2>
	              <label class="modal-label hidden" for="guardianEmailVisitor">E-mail</label>
	              <input class="modal-input" id="guardianEmailVisitor" type="email" placeholder={tr("correo@ejemplo.com", "email@example.com", "courriel@exemple.com")} />
	              <div class="wish-error" id="guardianEmailError" role="alert">{tr("Debes indicar un e-mail válido.", "You must provide a valid e-mail.", "Tu dois fournir un e-mail valide.")}</div>

	              <h2 class="guardian-section-title">{tr("Evidencia", "Evidence", "Preuve")}</h2>
	              <div class="upload-row" id="guardianEvidenceRow">
	                <label class="upload-btn" for="guardianEvidenceVisitor">{tr("Adjuntar imagen o video", "Attach image or video", "Joindre une image ou une vidéo")}</label>
	                <input id="guardianEvidenceVisitor" type="file" accept="image/*,video/*" class="hidden" />
	                <div class="upload-hint">{tr("Envíanos una evidencia de tu buena intención", "Send us evidence of your good intention", "Envoie-nous une preuve de ta bonne intention")}</div>
	              </div>
	              <div class="guardian-evidence-preview hidden" id="guardianEvidencePreview" aria-live="polite">
	                <div class="guardian-evidence-thumb" id="guardianEvidenceThumb"></div>
	                <div class="guardian-evidence-meta">
	                  <span class="guardian-evidence-label">{tr("Evidencia seleccionada", "Selected evidence", "Preuve sélectionnée")}</span>
	                  <span class="guardian-evidence-name" id="guardianEvidenceName"></span>
	                </div>
	              </div>
	              <div class="wish-error" id="guardianEvidenceError" role="alert">{tr("Debes adjuntar una evidencia.", "You must attach evidence.", "Tu dois attach evidence.")}</div>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="guardianSendBtn">{tr("Enviar", "Send", "Envoyer")}</button>
	              <button class="btn btn-outline btn-compact" type="button" id="cancelGuardianModal">{tr("Cancelar", "Cancel", "Annuler")}</button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="cooperativeSecurityModal" aria-hidden="true">
	          <div class="modal wish-modal cooperative-participate-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Confirmación de deseo cooperativo", "Cooperative wish confirmation", "Confirmation de souhait coopératif")}>
	            <div class="modal-head">
	              <h3>{tr("Confirmación de deseo cooperativo", "Cooperative wish confirmation", "Confirmation de souhait coopératif")}</h3>
	            </div>
	            <div class="modal-body">
	              <p class="panel-muted">
	                {tr("Escribe el código de seguridad que estableció el creador de este deseo cooperativo", "Enter the security code set by the creator of this cooperative wish", "Saisis le code de sécurité défini par le créateur de ce souhait coopératif")}
	              </p>
	              <label class="modal-label hidden" for="cooperativeSecurityCodeInput">{tr("Código de seguridad", "Security code", "Code de sécurité")}</label>
	              <input class="modal-input" id="cooperativeSecurityCodeInput" type="text" inputmode="numeric"
	                maxlength="6" placeholder="000000" />
	              <div class="wish-error" id="cooperativeSecurityError" role="alert">
	                {tr("El código de seguridad no coincide.", "Security code does not match.", "Le code de sécurité ne correspond pas.")}
	              </div>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="confirmCooperativeSecurity">{tr("Confirmar", "Confirm", "Confirmer")}</button>
	              <button class="btn btn-outline btn-compact" type="button" id="cancelCooperativeSecurity">{tr("Cancelar", "Cancel", "Annuler")}</button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="cooperativeParticipateModal" aria-hidden="true">
	          <div class="modal wish-modal cooperative-participate-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Gestión de participación en el deseo cooperativo", "Cooperative wish participation management", "Gestion de participation aux souhaits coopératifs")}>
	            <div class="modal-head">
	              <h3 id="cooperativeParticipateTitle">{tr("Gestión de participación en el deseo cooperativo", "Cooperative wish participation management", "Gestion de participation aux souhaits coopératifs")}</h3>
	            </div>
	            <div class="modal-body">
	              <p class="panel-muted" id="cooperativeParticipateDescription"></p>
	              <p class="panel-muted" id="cooperativeParticipatePrompt">{tr("¿Seguro que quieres ayudar a cumplir este deseo?", "Are you sure you want to help fulfill this wish?", "Es-tu sûr de vouloir aider à accomplir ce souhait ?")}</p>
	              <div class="wish-quote" id="cooperativeParticipateQuote"></div>
	              <label class="modal-label" for="cooperativeCharacter">{tr("Termina de redactar la naturaleza de este deseo, para que sea tuyo", "Finish writing the nature of this wish so it becomes yours", "Termine d'écrire la nature de ce souhait pour qu'il devienne le tien")}</label>
	              <input class="modal-input" id="cooperativeCharacter" type="text" placeholder="Ej: Zenejim" />
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="confirmCooperativeParticipate">
	                {tr("Ayudar a cumplir este deseo", "Help fulfill this wish", "Aider à accomplir ce souhait")}
	              </button>
	              <button class="btn btn-outline btn-compact" type="button"
	                id="cancelCooperativeParticipate">{tr("Cancelar", "Cancel", "Annuler")}</button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="cooperativeCancelParticipationModal" aria-hidden="true">
	          <div class="modal wish-modal delete-wish-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Cancelar participación", "Cancel participation", "Annuler la participation")}>
	            <div class="modal-head">
	              <h3>{tr("¿Estás seguro de que ya no quieres participar en este deseo?", "Are you sure you no longer want to participate in this wish?", "Es-tu sûr de ne plus vouloir participer à ce souhait ?")}</h3>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="cooperativeCancelParticipationYes">{tr("Sí", "Yes", "Oui")}</button>
	              <button class="btn btn-outline btn-compact" type="button" id="cooperativeCancelParticipationNo">{tr("No", "No", "Non")}</button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="cooperativeOwnerReviewModal" aria-hidden="true">
	          <div class="modal wish-modal cooperative-owner-review-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Validar participaciones del deseo cooperativo", "Validate cooperative wish participations", "Valider les participations de souhait coopératif")}>
	            <div class="modal-head">
	              <h3>{tr("Validar participaciones con evidencia", "Validate participations with evidence", "Valider les participations avec preuves")}</h3>
	              <button class="modal-close" type="button" id="cooperativeOwnerReviewClose">✕</button>
	            </div>
	            <div class="modal-body">
	              <p class="panel-muted" id="cooperativeOwnerReviewStatus">
	                {tr("Revisa y valida cada evidencia antes de cerrar este deseo cooperativo.", "Review and validate each evidence item before closing this cooperative wish.", "Examine et valide chaque preuve avant de fermer ce souhait coopératif.")}
	              </p>
	              <div class="cooperative-owner-review-list" id="cooperativeOwnerReviewList"></div>
	            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="cooperativeOwnerReviewProceed">
	                {tr("Continuar para marcar deseo como cumplido", "Continue to mark wish as fulfilled", "Continuer pour marquer le souhait comme accompli")}
	              </button>
	              <button class="btn btn-outline btn-compact" type="button" id="cooperativeOwnerReviewCancel">
	                {tr("Cancelar", "Cancel", "Annuler")}
	              </button>
	            </div>
	          </div>
	        </div>

	        <div class="modal-overlay hidden" id="cooperativeFeedbackModal" aria-hidden="true">
	          <div class="modal wish-modal delete-wish-modal" role="dialog" aria-modal="true"
	            aria-label={tr("Mensaje informativo", "Informational message", "Message d'information")}>
	            <div class="modal-head">
	              <h3 id="cooperativeFeedbackTitle">{tr("Información", "Information", "Informations")}</h3>
	            </div>
            <div class="modal-body">
              <p class="panel-muted" id="cooperativeFeedbackMessage"></p>
            </div>
	            <div class="modal-actions">
	              <button class="btn btn-primary btn-compact" type="button" id="cooperativeFeedbackClose">{tr("Aceptar", "Accept", "Accepter")}</button>
	            </div>
	          </div>
	        </div>
	      </section>
	    </div>
	  </main>

	  <AuthFooter />
</div>
