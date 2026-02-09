<script>
  import { onMount } from "svelte";

  onMount(() => {
    document.body.dataset.visitor = "false";

    const prefixInputs = document.querySelectorAll(".wish-prefix-input");
    const suffixInputs = document.querySelectorAll("[data-suffix]");

    prefixInputs.forEach((input) => {
      const prefix = input.dataset.prefix || "Deseo ";
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
    const toggleVisitorView = document.getElementById("toggleVisitorView");
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
    const coverMedia = document.getElementById("coverMedia");
    const coverImg = document.getElementById("coverImg");
    const coverFile = document.getElementById("coverFile");
    const coverUploadBtn = document.getElementById("coverUpload");
    const coverMoveBtn = document.getElementById("coverMove");
    const coverMenu = document.querySelector(".cover-menu");
    const coverSelectExisting = document.getElementById("coverSelectExisting");
    const coverSelectModal = document.getElementById("coverSelectModal");
    const coverSelectCancel = document.getElementById("coverSelectCancel");
    const coverSaveActions = document.getElementById("coverSaveActions");
    const coverSaveBtn = document.getElementById("coverSaveBtn");
    const coverCancelBtn = document.getElementById("coverCancelBtn");
    const confirmCooperativeWish = document.getElementById("confirmCooperativeWish");
    const icanConfirmModal = document.getElementById("icanConfirmModal");
    const icanConfirmYes = document.getElementById("icanConfirmYes");
    const icanConfirmNo = document.getElementById("icanConfirmNo");
    const guardianContactModal = document.getElementById("guardianContactModal");
    const cancelGuardianModal = document.getElementById("cancelGuardianModal");
    const cooperativeParticipateModal = document.getElementById("cooperativeParticipateModal");
    const cooperativeParticipateDescription = document.getElementById("cooperativeParticipateDescription");
    const cooperativeParticipateQuote = document.getElementById("cooperativeParticipateQuote");
    const cancelCooperativeParticipate = document.getElementById("cancelCooperativeParticipate");
    const confirmCooperativeParticipate = document.getElementById("confirmCooperativeParticipate");
    const cooperativeSecurityModal = document.getElementById("cooperativeSecurityModal");
    const cooperativeSecurityCodeInput = document.getElementById("cooperativeSecurityCodeInput");
    const cooperativeSecurityError = document.getElementById("cooperativeSecurityError");
    const confirmCooperativeSecurity = document.getElementById("confirmCooperativeSecurity");
    const cancelCooperativeSecurity = document.getElementById("cancelCooperativeSecurity");
    const cooperativeCharacter = document.getElementById("cooperativeCharacter");
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
    let activeIcanSlot = null;
    let activeCooperativeSlot = null;
    let cooperativePreviewUrl = null;
    let cooperativePreviewImage = null;
    let activeParticipateSource = null;
    let activeParticipateMode = "create";
    let activeParticipateSlot = null;
    let activeSecuritySlot = null;
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
    let isVisitorView = false;
    let fulfillEvidenceUrl = null;

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

    const updateModalScrollLock = () => {
      const hasOpenModal = document.querySelector(".modal-overlay:not(.hidden)");
      document.body.classList.toggle("modal-open", Boolean(hasOpenModal));
    };

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
      cooperativeWishModal.classList.remove("hidden");
      cooperativeWishModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
      if (cooperativeWishSecurityCode) {
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

    const openFulfillWishModal = (slot) => {
      if (!fulfillWishModal) return;
      activeFulfillSlot = slot;
      fulfillWishModal.classList.remove("hidden");
      fulfillWishModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
      updateFulfillEvidencePreview(null);
    };

    const closeFulfillWishModalFn = () => {
      if (!fulfillWishModal) return;
      fulfillWishModal.classList.add("hidden");
      fulfillWishModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
      activeFulfillSlot = null;
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

    const openGuardianContactModal = () => {
      if (!guardianContactModal) return;
      guardianContactModal.classList.remove("hidden");
      guardianContactModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeGuardianContactModalFn = () => {
      if (!guardianContactModal) return;
      guardianContactModal.classList.add("hidden");
      guardianContactModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
    };

    const openCooperativeParticipateModal = (slot, mode = "create") => {
      if (!cooperativeParticipateModal) return;
      activeParticipateMode = mode;
      activeParticipateSource = slot;
      const description = mode === "edit"
        ? slot?.dataset?.rootDescription || ""
        : slot?.dataset?.description || "";
      const template = mode === "edit"
        ? slot?.dataset?.template || ""
        : slot?.dataset?.template || "";
      if (cooperativeParticipateDescription) {
        cooperativeParticipateDescription.textContent = description;
      }
      if (cooperativeParticipateQuote) {
        cooperativeParticipateQuote.textContent = template ? `“${template}”` : "";
      }
      if (cooperativeCharacter) {
        cooperativeCharacter.value = mode === "edit" ? slot?.dataset?.participationText || "" : "";
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
    };

    const openCooperativeSecurityModal = (slot) => {
      if (!cooperativeSecurityModal) return;
      activeSecuritySlot = slot;
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

    const closeCooperativeSecurityModal = () => {
      if (!cooperativeSecurityModal) return;
      cooperativeSecurityModal.classList.add("hidden");
      cooperativeSecurityModal.setAttribute("aria-hidden", "true");
      activeSecuritySlot = null;
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

    const guardianOptions = document.querySelectorAll(".guardian-option");
    if (guardianOptions.length) {
      guardianOptions.forEach((option) => {
        option.addEventListener("click", () => {
          guardianOptions.forEach((btn) => btn.classList.remove("is-selected"));
          option.classList.add("is-selected");
          guardianOptions.forEach((btn) => btn.setAttribute("aria-pressed", "false"));
          option.setAttribute("aria-pressed", "true");
        });
      });
    }

    const updateFulfillEvidencePreview = (file) => {
      if (!fulfillEvidencePreview) return;

      if (fulfillEvidenceUrl) {
        URL.revokeObjectURL(fulfillEvidenceUrl);
        fulfillEvidenceUrl = null;
      }

      fulfillEvidencePreview.innerHTML = "";

      if (!file) {
        fulfillEvidencePreview.innerHTML = `
          <label class="wish-image-btn" for="fulfillEvidence" aria-label="Sube la evidencia visual">+</label>
          <div class="wish-preview-content">
            <span class="wish-preview-placeholder">Sube la evidencia visual.</span>
            <span class="wish-preview-name">PNG, WEBP, JPEG, etc.</span>
          </div>
        `;
        return;
      }

      fulfillEvidenceUrl = URL.createObjectURL(file);
      const img = document.createElement("img");
      img.src = fulfillEvidenceUrl;
      img.alt = "Evidencia seleccionada";
      img.className = "wish-evidence-image";
      fulfillEvidencePreview.appendChild(img);
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
          previewPlaceholder.textContent = "Seleccionar imagen";
        }
        if (cooperativeWishFileName) {
          cooperativeWishFileName.textContent = "Sin imagen seleccionada";
        }
        return;
      }

      cooperativePreviewUrl = URL.createObjectURL(file);
      cooperativeWishPreview.classList.add("has-image");
      if (!cooperativePreviewImage) {
        cooperativePreviewImage = document.createElement("img");
        cooperativePreviewImage.className = "wish-preview-image";
        cooperativePreviewImage.alt = "Vista previa de la imagen seleccionada";
        cooperativeWishPreview.insertBefore(cooperativePreviewImage, cooperativeWishPreview.firstChild);
      }
      cooperativePreviewImage.src = cooperativePreviewUrl;
      if (previewPlaceholder) {
        previewPlaceholder.textContent = "Imagen seleccionada";
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
        cooperativePreviewImage.alt = "Vista previa de la imagen seleccionada";
        cooperativeWishPreview.insertBefore(cooperativePreviewImage, cooperativeWishPreview.firstChild);
      }
      cooperativePreviewImage.src = url;
      if (previewPlaceholder) {
        previewPlaceholder.textContent = "Imagen seleccionada";
      }
      if (cooperativeWishFileName) {
        cooperativeWishFileName.textContent = label || "Imagen actual";
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
          previewPlaceholder.textContent = "Seleccionar imagen";
        }
        if (personalWishFileName) {
          personalWishFileName.textContent = "Sin imagen seleccionada";
        }
        return;
      }

      personalPreviewUrl = URL.createObjectURL(file);
      personalWishPreview.classList.add("has-image");
      if (!personalPreviewImage) {
        personalPreviewImage = document.createElement("img");
        personalPreviewImage.className = "wish-preview-image";
        personalPreviewImage.alt = "Vista previa de la imagen seleccionada";
        personalWishPreview.insertBefore(personalPreviewImage, personalWishPreview.firstChild);
      }
      personalPreviewImage.src = personalPreviewUrl;
      if (previewPlaceholder) {
        previewPlaceholder.textContent = "Imagen seleccionada";
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
        personalPreviewImage.alt = "Vista previa de la imagen seleccionada";
        personalWishPreview.insertBefore(personalPreviewImage, personalWishPreview.firstChild);
      }
      personalPreviewImage.src = url;
      if (previewPlaceholder) {
        previewPlaceholder.textContent = "Imagen seleccionada";
      }
      if (personalWishFileName) {
        personalWishFileName.textContent = label || "Imagen actual";
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

    const setPersonalWishError = (show) => {
      if (!personalWishError) return;
      personalWishError.classList.toggle("is-visible", show);
    };

    if (personalWishText) {
      personalWishText.addEventListener("input", () => {
        setPersonalWishError(!isPersonalWishValid());
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
      icon.setAttribute("aria-label", "Yo puedo cumplir ese deseo");
      icon.title = "Yo puedo cumplir ese deseo";
      const img = document.createElement("img");
      img.src = "/css/icons/iconican.webp";
      img.alt = "Yo puedo cumplir ese deseo";
      icon.appendChild(img);
      return icon;
    };

    const createVisitorCooperativeIcon = () => {
      const icon = document.createElement("div");
      icon.className = "wish-icon-btn wish-icon-static";
      icon.dataset.action = "help-coop";
      icon.setAttribute("aria-label", "Yo puedo ayudar a cumplir este deseo");
      icon.title = "Yo puedo ayudar a cumplir este deseo";
      const img = document.createElement("img");
      img.src = "/css/icons/iconcooperative2.webp";
      img.alt = "Yo puedo ayudar a cumplir este deseo";
      icon.appendChild(img);
      return icon;
    };

    const resetSlotToEmpty = (slot) => {
      if (!slot || !lampSlotTemplate) return;
      if (slot.dataset.imageUrl) {
        URL.revokeObjectURL(slot.dataset.imageUrl);
        delete slot.dataset.imageUrl;
      }
      delete slot.dataset.description;
      delete slot.dataset.type;
      delete slot.dataset.goal;
      delete slot.dataset.current;
      delete slot.dataset.template;
      slot.classList.remove("is-choosing", "is-filled");
      slot.classList.add("is-empty");
      slot.innerHTML = "";
      slot.appendChild(lampSlotTemplate.content.cloneNode(true));
    };

    const renderPersonalWishSlot = (slot, description, imageUrl, type) => {
      if (!slot) return;
      if (slot.dataset.imageUrl) {
        URL.revokeObjectURL(slot.dataset.imageUrl);
        delete slot.dataset.imageUrl;
      }

      slot.classList.remove("is-empty", "is-choosing");
      slot.classList.add("is-filled");
      slot.innerHTML = "";
      slot.dataset.description = description;
      if (type) {
        slot.dataset.type = type;
      }

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
      if (isVisitorView) {
        actions.appendChild(createVisitorIcon());
      } else {
        actions.appendChild(createWishActionBtn("/css/icons/iconedit.webp", "Editar deseo", "edit"));
        actions.appendChild(createWishActionBtn("/css/icons/iconfulfill.webp", "Marcar como cumplido", "fulfill"));
        actions.appendChild(createWishActionBtn("/css/icons/icondelete.webp", "Borrar deseo", "delete"));
      }
      leftCol.appendChild(actions);
      body.appendChild(leftCol);

      if (imageUrl) {
        const imageWrap = document.createElement("div");
        imageWrap.className = "wish-slot-image-wrap";
        const img = document.createElement("img");
        img.className = "wish-slot-image";
        img.src = imageUrl;
        img.alt = "Imagen del deseo";
        imageWrap.appendChild(img);
        body.appendChild(imageWrap);
        slot.dataset.imageUrl = imageUrl;
      } else {
        body.classList.add("single");
      }

      row.appendChild(body);
      slot.appendChild(row);
    };

    const renderCooperativeWishSlot = (slot, description, imageUrl, type, current, goal, template, securityCode) => {
      if (!slot) return;
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
      if (!isVisitorView) {
        const securityField = document.createElement("div");
        securityField.className = "wish-security-field";
        const securityLabel = document.createElement("span");
        securityLabel.className = "wish-security-label";
        securityLabel.textContent = "Código de seguridad";
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
      if (isVisitorView) {
        actions.appendChild(createVisitorCooperativeIcon());
      } else {
        actions.appendChild(createWishActionBtn("/css/icons/iconedit.webp", "Editar deseo", "edit"));
        const fulfillBtn = createWishActionBtn("/css/icons/iconfulfill.webp", "Marcar como cumplido", "fulfill");
        fulfillBtn.classList.add("wish-icon-disabled");
        actions.appendChild(fulfillBtn);
        actions.appendChild(createWishActionBtn("/css/icons/icondelete.webp", "Borrar deseo", "delete"));
      }
      leftCol.appendChild(actions);

      body.appendChild(leftCol);

      if (imageUrl) {
        const imageWrap = document.createElement("div");
        imageWrap.className = "wish-slot-image-wrap";
        const img = document.createElement("img");
        img.className = "wish-slot-image";
        img.src = imageUrl;
        img.alt = "Imagen del deseo";
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
      slot.dataset.rootUser = rootUser || "Carlos Jiménez Duarte";
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
      icon.alt = "Yo puedo ayudar a cumplir este deseo";
      iconWrap.appendChild(icon);

      const descWrap = document.createElement("div");
      descWrap.className = "wish-slot-description";
      const title = document.createElement("div");
      title.className = "wish-slot-title";
      title.textContent = participationText;
      const typePill = document.createElement("span");
      typePill.className = "wish-type-pill";
      typePill.textContent = "Cooperativo";
      descWrap.appendChild(title);
      descWrap.appendChild(typePill);
      if (!isVisitorView) {
        const securityField = document.createElement("div");
        securityField.className = "wish-security-field";
        const securityLabel = document.createElement("span");
        securityLabel.className = "wish-security-label";
        securityLabel.textContent = "Código de seguridad";
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
      actions.appendChild(createWishActionBtn("/css/icons/iconedit.webp", "Editar deseo", "help-edit"));
      actions.appendChild(createWishActionBtn("/css/icons/iconfulfill.webp", "Marcar como cumplido", "fulfill"));
      actions.appendChild(createWishActionBtn("/css/icons/icondelete.webp", "Borrar deseo", "delete"));

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
        img.alt = "Imagen del deseo raíz";
        imageWrap.appendChild(img);
        rightCol.appendChild(imageWrap);
      }

      const rootLink = document.createElement("a");
      rootLink.className = "wish-root-link";
      rootLink.href = "#";
      rootLink.textContent = rootUser || "Carlos Jiménez Duarte";

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
        const prefix = personalWishText.dataset.prefix || "Deseo ";
        personalWishText.value = prefix;
        personalWishText.dispatchEvent(new Event("input", { bubbles: true }));
      }
      if (personalWishMedia) {
        personalWishMedia.value = "";
      }
      updatePersonalPreview(null);
      setPersonalWishError(false);
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
      "Espiritual": "Deseos relacionados con el sentido de vida, la conciencia, la fe, la paz interior y el crecimiento espiritual. Ejemplo: perseverar en el hábito de la meditación, leer libros sobre espiritualidad, asistir a misa.",
      "Material": "Deseos vinculados a bienes, objetos o condiciones tangibles que mejoran la calidad de vida. Pueden involucrar recursos externos y, en algunos casos, la ayuda o participación de otras personas. Ejemplo: tener una cafetera nueva, un nuevo auto, una nueva computadora.",
      "Monetario": "Deseos relacionados exclusivamente con metas económicas personales. No pueden ser concedidos por otras personas y funcionan como objetivos de ahorro, disciplina y logro individual. Solo el propio usuario puede cumplirlos.",
      "Profesional": "Deseos asociados al desarrollo laboral, académico o creativo. Incluyen proyectos, estudios, reconocimiento, impacto profesional y crecimiento en la vocación personal. Ejemplo: estudiar arquitectura y graduarme de la Universidad Politécnico de Milán.",
      "Salud y cuerpo": "Deseos enfocados en el bienestar físico, la energía vital, la recuperación y la relación consciente con el cuerpo. No sustituyen atención médica ni tratamientos profesionales. Ejemplo: mantener la disciplina de ejercitar tu cuerpo a diario, correr 1 km diario, alimentarte bien.",
      "Relacional": "Deseos relacionados con vínculos humanos: familia, pareja, amistades y comunidad. Incluyen encuentros, reconciliaciones, fortalecimiento de relaciones y construcción de lazos significativos. Ejemplo: tomarse una cerveza con Lars Ulrich, ir a un concierto con tu hermano, disfrutar de un día en familia en el Restaurante La Matriarca.",
      "Vivencial": "Deseos orientados a experiencias, momentos únicos y vivencias significativas. No se definen por la posesión, sino por el hecho de vivir algo que deje huella en la memoria y la conciencia. Ejemplo: lanzarse en paracaídas, visitar Las Islas Maldivas, viajar en helicóptero."
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
      });
    }

    const handleConfirmPersonalWish = () => {
      if (!activePersonalSlot) return;
      if (!personalWishText) return;
      if (!isPersonalWishValid()) {
        setPersonalWishError(true);
        return;
      }

      const description = personalWishText.value.trim();
      const file = personalWishMedia && personalWishMedia.files ? personalWishMedia.files[0] : null;
      const imageUrl = file ? URL.createObjectURL(file) : activePersonalSlot.dataset.imageUrl || null;
      const selectedType = Array.from(personalWishTypeInputs).find((input) => input.checked)?.value || "Espiritual";

      renderPersonalWishSlot(activePersonalSlot, description, imageUrl, selectedType);
      closePersonalWishModalFn();
      resetPersonalWishForm();
      activePersonalSlot = null;
    };

    if (confirmPersonalWish) {
      confirmPersonalWish.addEventListener("click", handleConfirmPersonalWish);
    }

    if (confirmCooperativeWish) {
      confirmCooperativeWish.addEventListener("click", () => {
        if (!cooperativeWishList || !activeCooperativeSlot) return;
        const description = cooperativeWishText ? cooperativeWishText.value.trim() : "";
        if (!description) return;

        const selectedType = Array.from(cooperativeWishTypeInputs).find((input) => input.checked)?.value || "Espiritual";
        const goal = cooperativeWishCount ? Number(cooperativeWishCount.value) || 0 : 0;
        const template = cooperativeWishTemplate ? cooperativeWishTemplate.value : "";
        const securityCodeRaw = cooperativeWishSecurityCode ? cooperativeWishSecurityCode.value : "";
        const securityCode = securityCodeRaw.replace(/\D/g, "").slice(0, 6);
        const file = cooperativeWishMedia && cooperativeWishMedia.files ? cooperativeWishMedia.files[0] : null;
        const imageUrl = file ? URL.createObjectURL(file) : activeCooperativeSlot?.dataset.imageUrl || null;

        const slot = activeCooperativeSlot;
        slot.dataset.securityCode = securityCode;
        renderCooperativeWishSlot(slot, description, imageUrl, selectedType, 0, goal, template, securityCode);
        activeCooperativeSlot = null;
        closeCooperativeWishModalFn();
      });
    }

    if (confirmCooperativeParticipate) {
      confirmCooperativeParticipate.addEventListener("click", () => {
        if (!cooperativeWishList || !activeParticipateSource) return;
        const rootDescription = activeParticipateSource.dataset.description || "";
        const rootTemplate = activeParticipateSource.dataset.template || "";
        const rootImageUrl = activeParticipateSource.dataset.imageUrl || null;
        const rootUser = "Carlos Jiménez Duarte";
        const extraText = cooperativeCharacter ? cooperativeCharacter.value.trim() : "";
        const participationText = rootTemplate
          ? rootTemplate.replace(/\*[^*]*\*/, extraText || "…")
          : extraText;

        const slot = activeParticipateMode === "edit" && activeParticipateSlot
          ? activeParticipateSlot
          : document.createElement("li");

        if (!activeParticipateSlot) {
          slot.className = "wish-slot is-filled is-cooperative is-participation";
          cooperativeWishList.appendChild(slot);
        }

        renderParticipationWishSlot(slot, participationText, rootDescription, rootImageUrl, rootUser, rootTemplate);
        activeParticipateSlot = null;
        closeCooperativeParticipateModalFn();
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
        const expected = activeSecuritySlot.dataset.securityCode || "";
        const entered = cooperativeSecurityCodeInput ? cooperativeSecurityCodeInput.value.trim() : "";
        const isValid = expected && entered === expected;
        if (!isValid) {
          if (cooperativeSecurityError) {
            cooperativeSecurityError.classList.add("is-visible");
          }
          return;
        }
        if (cooperativeSecurityError) {
          cooperativeSecurityError.classList.remove("is-visible");
        }
        const slot = activeSecuritySlot;
        closeCooperativeSecurityModal();
        openCooperativeParticipateModal(slot);
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

    const openCoverSelectModal = () => {
      if (!coverSelectModal) return;
      coverSelectModal.classList.remove("hidden");
      coverSelectModal.setAttribute("aria-hidden", "false");
      updateModalScrollLock();
    };

    const closeCoverSelectModal = () => {
      if (!coverSelectModal) return;
      coverSelectModal.classList.add("hidden");
      coverSelectModal.setAttribute("aria-hidden", "true");
      updateModalScrollLock();
    };

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

    if (coverSelectExisting) {
      coverSelectExisting.addEventListener("click", () => {
        openCoverSelectModal();
        closeCoverMenu();
      });
    }

    if (coverSelectCancel) {
      coverSelectCancel.addEventListener("click", closeCoverSelectModal);
    }

    if (coverSelectModal) {
      coverSelectModal.addEventListener("click", (event) => {
        if (event.target === coverSelectModal) closeCoverSelectModal();
      });
    }

    if (coverSelectModal && coverImg) {
      coverSelectModal.addEventListener("click", (event) => {
        const button = event.target.closest(".cover-select-item");
        if (!button) return;
        const src = button.dataset.coverSrc;
        if (!src) return;
        if (coverPendingUrl) {
          URL.revokeObjectURL(coverPendingUrl);
          coverPendingUrl = null;
        }
        coverImg.src = src;
        coverOffsetX = 0;
        coverOffsetY = 0;
        markCoverDirty();
        closeCoverSelectModal();
        setCoverMoveState(true);
        recalcCoverBounds();
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
      confirmDeleteWish.addEventListener("click", () => {
        if (activeDeleteSlot) {
          if (activeDeleteSlot.classList.contains("is-cooperative")) {
            if (activeDeleteSlot.dataset.imageUrl) {
              URL.revokeObjectURL(activeDeleteSlot.dataset.imageUrl);
            }
            activeDeleteSlot.remove();
          } else {
            resetSlotToEmpty(activeDeleteSlot);
          }
        }
        closeDeleteWishModalFn();
      });
    }

    const rerenderPersonalSlots = () => {
      if (!personalWishList) return;
      const slots = Array.from(personalWishList.querySelectorAll(".wish-slot.is-filled"));
      slots.forEach((slot) => {
        const description = slot.dataset.description || "";
        const type = slot.dataset.type || "Espiritual";
        const imageUrl = slot.dataset.imageUrl || null;
        renderPersonalWishSlot(slot, description, imageUrl, type);
      });
    };

    const rerenderCooperativeSlots = () => {
      if (!cooperativeWishList) return;
      const slots = Array.from(cooperativeWishList.querySelectorAll(".wish-slot.is-filled"));
      slots.forEach((slot) => {
        if (slot.classList.contains("is-participation")) {
          const participationText = slot.dataset.participationText || "";
          const rootDescription = slot.dataset.rootDescription || "";
          const rootImageUrl = slot.dataset.rootImageUrl || null;
          const rootUser = slot.dataset.rootUser || "Carlos Jiménez Duarte";
          const template = slot.dataset.template || "";
          renderParticipationWishSlot(slot, participationText, rootDescription, rootImageUrl, rootUser, template);
          return;
        }
        const description = slot.dataset.description || "";
        const type = slot.dataset.type || "Espiritual";
        const imageUrl = slot.dataset.imageUrl || null;
        const current = Number(slot.dataset.current || 0);
        const goal = Number(slot.dataset.goal || 0);
        const template = slot.dataset.template || "";
        const securityCode = slot.dataset.securityCode || "";
        renderCooperativeWishSlot(slot, description, imageUrl, type, current, goal, template, securityCode);
      });
    };

    if (toggleVisitorView) {
      toggleVisitorView.addEventListener("click", () => {
        isVisitorView = !isVisitorView;
        toggleVisitorView.textContent = isVisitorView ? "Ver como propietario" : "Ver como visitante";
        rerenderPersonalSlots();
        rerenderCooperativeSlots();
      });
    }

    if (personalWishList) {
      personalWishList.addEventListener("click", (event) => {
        const lampBtn = event.target.closest(".wish-lamp-btn");
        const cancelBtn = event.target.closest(".wish-choice-cancel");
        const choiceBtn = event.target.closest(".wish-choice-btn");
        const actionBtn = event.target.closest(".wish-icon-btn");

        if (lampBtn) {
          const slot = lampBtn.closest(".wish-slot");
          if (!slot) return;
          activePersonalSlot = slot;
          openPersonalWishModal();
          return;
        }

        if (cancelBtn) {
          const slot = cancelBtn.closest(".wish-slot");
          if (!slot) return;
          resetSlotToEmpty(slot);
          activePersonalSlot = null;
          return;
        }

        if (choiceBtn) {
          const slot = choiceBtn.closest(".wish-slot");
          if (choiceBtn.dataset.choice === "personal") {
            activePersonalSlot = slot;
            openPersonalWishModal();
          } else if (choiceBtn.dataset.choice === "cooperative") {
            activePersonalSlot = null;
            openCooperativeWishModal();
          }
          return;
        }

        if (actionBtn) {
          if (isVisitorView && !["ican", "help-coop"].includes(actionBtn.dataset.action)) return;
          const slot = actionBtn.closest(".wish-slot");
          if (!slot) return;
          if (actionBtn.dataset.action === "delete") {
            openDeleteWishModal(slot);
          } else if (actionBtn.dataset.action === "edit") {
            if (slot.classList.contains("is-cooperative")) {
              activeCooperativeSlot = slot;
              const existingDescription = slot.dataset.description || "";
              const prefix = cooperativeWishText ? cooperativeWishText.dataset.prefix || "Deseo " : "Deseo ";
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
              setCooperativePreviewFromUrl(slot.dataset.imageUrl || null, "Imagen actual");
              openCooperativeWishModal();
            } else {
              activePersonalSlot = slot;
              const existingDescription = slot.dataset.description || "";
              const prefix = personalWishText ? personalWishText.dataset.prefix || "Deseo " : "Deseo ";
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

              setPersonalPreviewFromUrl(slot.dataset.imageUrl || null, "Imagen actual");
              openPersonalWishModal();
            }
          } else if (actionBtn.dataset.action === "fulfill") {
            openFulfillWishModal(slot);
          } else if (actionBtn.dataset.action === "ican") {
            openIcanConfirmModal(slot);
          } else if (actionBtn.dataset.action === "help-coop") {
            if (isVisitorView) {
              openCooperativeSecurityModal(slot);
            } else {
              openCooperativeParticipateModal(slot);
            }
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
          const slot = lampBtn.closest(".wish-slot");
          if (!slot || slot.classList.contains("is-choosing")) return;
          activeCooperativeSlot = slot;
          openCooperativeWishModal();
          return;
        }
        if (!actionBtn) return;
        if (isVisitorView && !["help-coop"].includes(actionBtn.dataset.action)) return;
        const slot = actionBtn.closest(".wish-slot");
        if (!slot) return;

        if (actionBtn.dataset.action === "delete") {
          openDeleteWishModal(slot);
        } else if (actionBtn.dataset.action === "edit") {
          activeCooperativeSlot = slot;
          const existingDescription = slot.dataset.description || "";
          const prefix = cooperativeWishText ? cooperativeWishText.dataset.prefix || "Deseo " : "Deseo ";
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
          setCooperativePreviewFromUrl(slot.dataset.imageUrl || null, "Imagen actual");
          openCooperativeWishModal();
        } else if (actionBtn.dataset.action === "help-edit") {
          activeParticipateSlot = slot;
          openCooperativeParticipateModal(slot, "edit");
        } else if (actionBtn.dataset.action === "help-coop") {
          if (isVisitorView) {
            openCooperativeSecurityModal(slot);
          } else {
            openCooperativeParticipateModal(slot);
          }
        }
      });
    }
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Mis deseos públicos</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user public-wishes-background">
  <main class="user-home">
    <!-- =========================
     *  PORTADA / COVER
     *  ========================= -->
    <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="/assets/cover-default.jpg" alt="Portada" />

        <div class="cover-actions">
          <details class="cover-menu">
            <summary class="icon-btn" id="btnChangeCover" title="Editar imagen de portada">
              Editar imagen de portada
            </summary>
            <div class="cover-menu-panel">
              <button class="cover-menu-item" type="button" id="coverSelectExisting">
                Seleccionar imagen
              </button>
              <button class="cover-menu-item" type="button" id="coverUpload">
                Subir imagen
              </button>
              <button class="cover-menu-item" type="button" id="coverMove">
                Mover imagen
              </button>
            </div>
          </details>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="cover-save-actions hidden" id="coverSaveActions">
          <button class="btn btn-primary btn-compact" type="button" id="coverSaveBtn">
            Guardar cambios
          </button>
          <button class="btn btn-outline btn-compact" type="button" id="coverCancelBtn">
            Cancelar
          </button>
        </div>

        <div class="purpose-stack" aria-label="Deseos de propósito">
          <div class="purpose-list">
            <button class="purpose-pill" type="button" id="purpose1">
            Deseo #1: Secreto
            </button>

            <button class="purpose-pill" type="button" id="purpose2">
            Deseo construir el Reino de Combray
            </button>

            <button class="purpose-pill" type="button" id="purpose3">
            Deseo estar unido a Jesús
            </button>
          </div>

          <button class="icon-btn purpose-edit-btn" id="btnEditPurposes" type="button" title="Modificar deseo">
            <img src="/css/icons/iconedit.webp" alt="Modificar deseo" />
          </button>
        </div>
      </div>
    </section>

    <div class="modal-overlay hidden" id="coverSelectModal" aria-hidden="true">
      <div class="modal wish-modal cover-select-modal" role="dialog" aria-modal="true"
        aria-label="Seleccionar imagen de portada">
        <div class="modal-head">
          <h3>Seleccionar imagen</h3>
        </div>
        <div class="modal-body">
          <div class="cover-select-grid">
            <button class="cover-select-item" type="button" data-cover-src="/assets/cover-default.jpg">
              <img src="/assets/cover-default.jpg" alt="Portada 1" />
            </button>
            <button class="cover-select-item" type="button" data-cover-src="/assets/post-1.jpg">
              <img src="/assets/post-1.jpg" alt="Portada 2" />
            </button>
            <button class="cover-select-item" type="button" data-cover-src="/assets/post-2.jpg">
              <img src="/assets/post-2.jpg" alt="Portada 3" />
            </button>
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="coverSelectCancel">Cancelar</button>
        </div>
      </div>
    </div>

    <div class="public-wishes-body">
      <!-- =========================
       *  NAV / LINKS
       *  ========================= -->
      <nav class="profile-nav" aria-label="Navegación de perfil">
        <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="#" title="Estrellas">
          <span class="nav-icon">⭐</span>
          <span><strong>5.000.000</strong> estrellas</span>
        </a>
        <a class="nav-pill" href="#" title="Seguidores">Seguidores</a>
        <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
        <a class="nav-pill" href="#" title="Galería">Galería</a>
        <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
        <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
      </nav>

      <!-- =========================
       *  MIS DESEOS PUBLICOS
       *  ========================= -->
      <section class="public-wishes-shell" aria-label="Mis deseos públicos">
        <header class="public-wishes-head">
          <div>
            <h2 class="public-wishes-title">Mis deseos públicos</h2>
          </div>
        </header>

        <!-- =========================
         *  LISTAS DE DESEOS
         *  ========================= -->
        <section class="wish-lists-grid" aria-label="Listas de deseos">
          <article class="panel wish-list-panel">
            <div class="panel-head">
              <h3 class="panel-title">Deseos personales</h3>
              <div class="panel-actions">
                <button class="btn btn-outline btn-compact" type="button" id="toggleVisitorView">
                  Ver como visitante
                </button>
              </div>
              <span class="panel-badge"><span id="personalWishCount">7</span> / 50</span>
            </div>

            <ol class="wish-slot-list" id="personalWishList" data-total="50" aria-label="Deseos personales">
            </ol>
            <div class="wish-add-row">
              <button class="wish-add-btn" id="personalWishAdd" type="button" title="Agregar deseo">
                <span class="wish-add-plus">+</span>
              </button>
            </div>
          </article>

          <article class="panel wish-list-panel">
            <div class="panel-head">
              <h3 class="panel-title">Deseos cooperativos</h3>
              <span class="panel-badge"><span id="cooperativeWishCountLabel">0</span> / 20</span>
            </div>
            <p class="panel-muted">
              Zona vacía hasta que el usuario configura un deseo cooperativo.
            </p>
            <ol class="wish-slot-list" id="cooperativeWishList" data-total="0" aria-label="Deseos cooperativos">
            </ol>
            <div class="wish-add-row">
              <button class="wish-add-btn" id="cooperativeWishAdd" type="button" title="Agregar deseo cooperativo">
                <span class="wish-add-plus">+</span>
              </button>
            </div>
          </article>
        </section>

        <template id="wishLampSlotTemplate">
          <div class="wish-slot-row wish-slot-row-empty">
            <button class="wish-add-btn wish-lamp-btn" type="button" title="Agregar deseo">
              <img class="wish-lamp-icon" src="/css/icons/iconlamp.webp" alt="Agregar deseo" />
            </button>
          </div>
        </template>

        <template id="wishChoiceInlineTemplate">
          <div class="wish-slot-row wish-slot-row-choice">
            <div class="wish-choice-inline">
              <button class="wish-choice-card wish-choice-btn" type="button" data-choice="personal">
                <span class="wish-config-icon">
                  <img src="/css/icons/iconpersonal.webp" alt="Deseo personal" />
                </span>
                <span>¿Es un deseo individual?</span>
              </button>
              <button class="wish-choice-card wish-choice-btn" type="button" data-choice="cooperative">
                <span class="wish-config-icon">
                  <img src="/css/icons/iconcooperative.webp" alt="Deseo cooperativo" />
                </span>
                <span>¿Es un deseo cooperativo?</span>
              </button>
              <button class="wish-choice-card wish-choice-cancel" type="button" aria-label="Cancelar">
                <span class="wish-choice-cancel-icon">✕</span>
              </button>
            </div>
          </div>
        </template>

        <div class="modal-overlay hidden" id="personalWishModal" aria-hidden="true">
          <div class="modal modal-wide personal-wish-modal" role="dialog" aria-modal="true"
            aria-label="Configurar deseo personal">
            <div class="modal-head">
              <h3>Configurar deseo personal</h3>
              <button class="modal-close" type="button" id="closePersonalWishModal">✕</button>
            </div>
            <div class="modal-body personal-wish-body">
              <div class="wish-modal-grid">
                <div class="wish-modal-col">
                  <div class="wish-config-icon personal-wish-hero">
                    <img src="/css/icons/iconpersonal.webp" alt="Deseo personal" />
                  </div>
                  <h2 class="modal-label modal-label-center">Descripción del deseo</h2>
                  <label class="modal-label hidden" for="personalWishText">Descripción del deseo</label>
                  <textarea class="modal-textarea wish-prefix-input wish-textarea-compact" id="personalWishText"
                    rows="3" maxlength="80" data-prefix="Deseo " data-counter="personalWishCounter"></textarea>
                  <div class="wish-counter" id="personalWishCounter" aria-live="polite">0/80</div>
                  <div class="wish-error" id="personalWishError" role="alert">No has descrito tu deseo</div>
                  <div class="wish-warning">
                    <span class="wish-warning-icon">!</span>
                    <span id="personalWishTypeHint">
                      Deseos relacionados con el sentido de vida, la conciencia, la fe, la paz interior y el
                      crecimiento
                      espiritual. Ejemplo: perseverar en el hábito de la meditación, leer libros sobre espiritualidad,
                      asistir a misa.
                    </span>
                  </div>
                </div>

                <div class="wish-modal-col">
                  <fieldset class="wish-type-fieldset">
                    <div class="wish-type-selected">
                      <img id="personalWishTypeIcon" src="/css/icons/Espiritual.webp" alt="Espiritual" />
                    </div>
                    <h2 class="modal-label modal-label-center">Tipo de deseo</h2>
                    <div class="wish-type-grid">
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Espiritual" checked />
                        <span class="wish-type-visual">
                          <span>Espiritual</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Material" />
                        <span class="wish-type-visual">
                          <span>Material</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Monetario" />
                        <span class="wish-type-visual">
                          <span>Monetario</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Profesional" />
                        <span class="wish-type-visual">
                          <span>Profesional</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Salud y cuerpo" />
                        <span class="wish-type-visual">
                          <span>Salud y cuerpo</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Relacional" />
                        <span class="wish-type-visual">
                          <span>Relacional</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="personalWishType" value="Vivencial" />
                        <span class="wish-type-visual">
                          <span>Vivencial</span>
                        </span>
                      </label>
                    </div>
                  </fieldset>
                </div>

                <div class="wish-modal-col">
                  <h2 class="modal-label modal-label-center">Agregar imagen</h2>
                  <label class="modal-label hidden" for="personalWishMedia">Agregar imagen</label>
                  <input class="modal-input hidden" id="personalWishMedia" type="file" accept="image/*" />
                  <div class="wish-image-preview" id="personalWishPreview" aria-live="polite">
                    <label class="wish-image-btn" for="personalWishMedia" aria-label="Seleccionar imagen">+</label>
                    <div class="wish-preview-content">
                      <span class="wish-preview-placeholder">Seleccionar imagen</span>
                      <span class="wish-preview-name" id="personalWishFileName">Sin imagen seleccionada</span>
                    </div>
                  </div>
                  <div class="wish-config-icon personal-wish-hero">
                    <img src="/css/icons/iconsave.webp" alt="guardar" />
                  </div>
                  <div class="wish-form-actions wish-form-actions-center">
                    <br>
                    <button class="btn btn-primary btn-compact btn-icon" type="button" id="confirmPersonalWish">
                      ¡Confirmar mi deseo!
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-overlay hidden" id="cooperativeWishModal" aria-hidden="true">
          <div class="modal modal-wide cooperative-wish-modal" role="dialog" aria-modal="true"
            aria-label="Configurar deseo cooperativo">
            <div class="modal-head">
              <h3>Configurar deseo cooperativo</h3>
              <button class="modal-close" type="button" id="closeCooperativeWishModal">✕</button>
            </div>
            <div class="modal-body cooperative-wish-body">
              <div class="wish-modal-grid">
                <div class="wish-modal-col">
                  <div class="wish-config-icon personal-wish-hero">
                    <img src="/css/icons/iconcooperative.webp" alt="Deseo cooperativo" />
                  </div>
                  <h2 class="modal-label modal-label-center">Descripción del deseo</h2>
                  <label class="modal-label hidden" for="cooperativeWishText">Descripción del deseo
                    cooperativo</label>
                  <h5 class="modal-label modal-label-center"><i>Ejemplo: Deseo nivelar a 50 personajes del videojuego
                      Dofus, del servidor Tal Kasha, a nivel 200 en Anutropia.</i></h5>
                  <textarea class="modal-textarea wish-prefix-input wish-textarea-compact" id="cooperativeWishText"
                    rows="3" maxlength="120" data-prefix="Deseo ">Deseo </textarea>
                  <div class="wish-warning">
                    <span class="wish-warning-icon">!</span>
                    <span id="cooperativeWishTypeHint">
                      Deseos relacionados con el sentido de vida, la conciencia, la fe, la paz interior y el
                      crecimiento espiritual. Ejemplo: perseverar en el hábito de la meditación, leer libros sobre
                      espiritualidad, asistir a misa.
                    </span>
                  </div>
                  <label class="modal-label" for="cooperativeWishSecurityCode">Código de seguridad</label>
                  <input class="modal-input" id="cooperativeWishSecurityCode" type="text" inputmode="numeric"
                    maxlength="6" placeholder="000000" />
                </div>

                <div class="wish-modal-col">
                  <fieldset class="wish-type-fieldset">
                    <div class="wish-type-selected">
                      <img id="cooperativeWishTypeIcon" src="/css/icons/Espiritual.webp" alt="Espiritual" />
                    </div>
                    <h2 class="modal-label modal-label-center">Tipo de deseo</h2>
                    <div class="wish-type-grid">
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Espiritual" checked />
                        <span class="wish-type-visual">
                          <span>Espiritual</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Material" />
                        <span class="wish-type-visual">
                          <span>Material</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Profesional" />
                        <span class="wish-type-visual">
                          <span>Profesional</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Salud y cuerpo" />
                        <span class="wish-type-visual">
                          <span>Salud y cuerpo</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Relacional" />
                        <span class="wish-type-visual">
                          <span>Relacional</span>
                        </span>
                      </label>
                      <label class="wish-type-option">
                        <input type="radio" name="cooperativeWishType" value="Vivencial" />
                        <span class="wish-type-visual">
                          <span>Vivencial</span>
                        </span>
                      </label>
                    </div>
                  </fieldset>
                </div>

                <div class="wish-modal-col">
                  <h2 class="modal-label modal-label-center">Configuración cooperativa</h2>

                  <h3 class="modal-label modal-label-center">Número máximo de personas
                    participantes</h3>
                  <input class="modal-input" id="cooperativeWishCount" type="number" min="1" value="50" />

                  <h3 class="modal-label modal-label-center">Dale al usuario una idea de cómo apropiarse de este
                    deseo</h3>
                  <h5 class="modal-label modal-label-center"><i>Ejemplo:Deseo que el Team Guardian nivele, en el
                      servidor Tal Kasha, a mi personaje llamado... *este espacio libro sera rellenado por el
                      usuario*</i></h5>
                  <textarea class="modal-textarea" id="cooperativeWishTemplate" rows="4"
                    data-suffix="*este espacio libre será rellenado por el usuario.*">Deseo *este espacio libre será rellenado por el usuario.*</textarea>
                </div>

                <div class="wish-modal-col">
                  <h2 class="modal-label modal-label-center">Agregar imagen</h2>
                  <label class="modal-label hidden" for="cooperativeWishMedia">Agregar imagen</label>
                  <input class="modal-input hidden" id="cooperativeWishMedia" type="file" accept="image/*" />
                  <div class="wish-image-preview" id="cooperativeWishPreview" aria-live="polite">
                    <label class="wish-image-btn" for="cooperativeWishMedia" aria-label="Seleccionar imagen">+</label>
                    <div class="wish-preview-content">
                      <span class="wish-preview-placeholder">Seleccionar imagen</span>
                      <span class="wish-preview-name" id="cooperativeWishFileName">Sin imagen seleccionada</span>
                    </div>
                  </div>
                  <div class="wish-config-icon personal-wish-hero">
                    <img src="/css/icons/iconsave.webp" alt="guardar" />
                  </div>
                  <div class="wish-form-actions wish-form-actions-center">
                    <br>
                    <button class="btn btn-primary btn-compact btn-icon" type="button" id="confirmCooperativeWish">
                      ¡Confirmar deseo cooperativo!
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-overlay hidden" id="deleteWishModal" aria-hidden="true">
          <div class="modal wish-modal delete-wish-modal" role="dialog" aria-modal="true" aria-label="Borrar deseo">
            <div class="modal-head">
              <h3>¿Estás seguro de que deseas borrar este deseo?</h3>
            </div>
            <div class="modal-actions">
              <button class="btn btn-primary btn-compact" type="button" id="confirmDeleteWish">Sí</button>
              <button class="btn btn-outline btn-compact" type="button" id="cancelDeleteWish">No</button>
            </div>
          </div>
        </div>

        <div class="modal-overlay hidden" id="fulfillWishModal" aria-hidden="true">
          <div class="modal wish-modal fulfill-wish-modal" role="dialog" aria-modal="true"
            aria-label="Subir evidencia">
            <div class="modal-head">
              <h3>¡Sube la evidencia!</h3>
            </div>
            <div class="modal-body">
              <input id="fulfillEvidence" type="file" accept="image/*" class="hidden" />
              <div class="wish-evidence-preview" id="fulfillEvidencePreview" aria-live="polite">
                <label class="wish-image-btn" for="fulfillEvidence" aria-label="Sube la evidencia visual">+</label>
                <div class="wish-preview-content">
                  <span class="wish-preview-placeholder">Sube la evidencia visual.</span>
                  <span class="wish-preview-name">PNG, WEBP, JPEG, etc.</span>
                </div>
              </div>
              <p class="panel-muted">
                <strong>¿Declaras bajo verdad de juramento que este deseo se ha cumplido?</strong>
              </p>
            </div>
            <div class="modal-actions">
              <button class="btn btn-primary btn-compact" type="button">
                Juro bajo verdad de juramento que este deseo se ha cumplido
              </button>
            </div>
            <div class="modal-actions">
              <button class="btn btn-outline btn-compact" type="button" id="cancelFulfillWish">Cancelar</button>
            </div>
          </div>
        </div>

        <div class="modal-overlay hidden" id="icanConfirmModal" aria-hidden="true">
          <div class="modal wish-modal ican-confirm-modal" role="dialog" aria-modal="true"
            aria-label="Conceder deseo">
            <div class="modal-head">
              <h3>Yo puedo conceder ese deseo</h3>
            </div>
            <div class="modal-body">
              <p class="panel-muted">¿Estás seguro de que deseas cumplir este deseo?</p>
            </div>
            <div class="modal-actions">
              <button class="btn btn-primary btn-compact" type="button" id="icanConfirmYes">Sí</button>
              <button class="btn btn-outline btn-compact" type="button" id="icanConfirmNo">No</button>
            </div>
          </div>
        </div>

        <div class="modal-overlay hidden" id="guardianContactModal" aria-hidden="true">
          <div class="modal wish-modal guardian-contact-modal" role="dialog" aria-modal="true"
            aria-label="Contactar a un Guardián">
            <div class="modal-head">
              <h3>Contactar a un Guardián</h3>
            </div>
            <div class="modal-body">
              <h2 class="guardian-section-title">Selecciona a un Guardián</h2>
              <div class="guardian-row guardian-select">
                <button class="guardian-option" type="button" aria-pressed="false">
                  <img class="guardian-avatar" src="/css/icons/Guardian1.png" alt="Guardián 1" />
                </button>
                <button class="guardian-option" type="button" aria-pressed="false">
                  <img class="guardian-avatar" src="/css/icons/Guardian2.png" alt="Guardián 2" />
                </button>
                <button class="guardian-option" type="button" aria-pressed="false">
                  <img class="guardian-avatar" src="/css/icons/Guardian3.png" alt="Guardián 3" />
                </button>
                <button class="guardian-option" type="button" aria-pressed="false">
                  <img class="guardian-avatar" src="/css/icons/Guardian4.png" alt="Guardián 4" />
                </button>
              </div>

              <h2 class="guardian-section-title">Describe por qué deseas conceder ese deseo</h2>
              <label class="modal-label hidden" for="guardianReasonVisitor">Describe por qué deseas conceder ese
                deseo</label>
              <textarea class="modal-textarea" id="guardianReasonVisitor" rows="3"></textarea>

              <h2 class="guardian-section-title">Número telefónico</h2>
              <label class="modal-label hidden" for="guardianPhoneVisitor">Número telefónico</label>
              <input class="modal-input" id="guardianPhoneVisitor" type="tel" inputmode="tel"
                placeholder="+57 300 000 0000" />

              <h2 class="guardian-section-title">E-mail</h2>
              <label class="modal-label hidden" for="guardianEmailVisitor">E-mail</label>
              <input class="modal-input" id="guardianEmailVisitor" type="email" placeholder="correo@ejemplo.com" />

              <h2 class="guardian-section-title">Evidencia</h2>
              <div class="upload-row">
                <label class="upload-btn" for="guardianEvidenceVisitor">Adjuntar imagen o video</label>
                <input id="guardianEvidenceVisitor" type="file" accept="image/*,video/*" class="hidden" />
                <div class="upload-hint">Envíanos una evidencia de tu buena intención</div>
              </div>
            </div>
            <div class="modal-actions">
              <button class="btn btn-primary btn-compact" type="button">Enviar</button>
              <button class="btn btn-outline btn-compact" type="button" id="cancelGuardianModal">Cancelar</button>
            </div>
          </div>
        </div>

        <div class="modal-overlay hidden" id="cooperativeSecurityModal" aria-hidden="true">
          <div class="modal wish-modal cooperative-participate-modal" role="dialog" aria-modal="true"
            aria-label="Confirmación de deseo cooperativo">
            <div class="modal-head">
              <h3>Confirmación de deseo cooperativo</h3>
            </div>
            <div class="modal-body">
              <p class="panel-muted">
                Escribe el código de seguridad que estableció el creador de este deseo cooperativo
              </p>
              <label class="modal-label hidden" for="cooperativeSecurityCodeInput">Código de seguridad</label>
              <input class="modal-input" id="cooperativeSecurityCodeInput" type="text" inputmode="numeric"
                maxlength="6" placeholder="000000" />
              <div class="wish-error" id="cooperativeSecurityError" role="alert">
                El código de seguridad no coincide.
              </div>
            </div>
            <div class="modal-actions">
              <button class="btn btn-primary btn-compact" type="button" id="confirmCooperativeSecurity">Confirmar</button>
              <button class="btn btn-outline btn-compact" type="button" id="cancelCooperativeSecurity">Cancelar</button>
            </div>
          </div>
        </div>

        <div class="modal-overlay hidden" id="cooperativeParticipateModal" aria-hidden="true">
          <div class="modal wish-modal cooperative-participate-modal" role="dialog" aria-modal="true"
            aria-label="Gestión de participación en el deseo cooperativo">
            <div class="modal-head">
              <h3>Gestión de participación en el deseo cooperativo</h3>
            </div>
            <div class="modal-body">
              <p class="panel-muted" id="cooperativeParticipateDescription"></p>
              <p class="panel-muted">¿Seguro que quieres ayudar a cumplir este deseo?</p>
              <div class="wish-quote" id="cooperativeParticipateQuote"></div>
              <label class="modal-label" for="cooperativeCharacter">Termina de redactar la naturaleza de este deseo,
                para que sea tuyo</label>
              <input class="modal-input" id="cooperativeCharacter" type="text" placeholder="Ej: Zenejim" />
            </div>
            <div class="modal-actions">
              <button class="btn btn-primary btn-compact" type="button" id="confirmCooperativeParticipate">
                Ayudar a cumplir este deseo
              </button>
              <button class="btn btn-outline btn-compact" type="button"
                id="cancelCooperativeParticipate">Cancelar</button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>

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
            <li><a href="#">Qué es Kiadez</a></li>
            <li><a href="#">Rangos de Guardianes</a></li>
            <li><a href="#">Ser Guardián</a></li>
            <li><a href="#">Contacto</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>Idiomas</h4>
          <ul>
            <li><a href="#">Español</a></li>
            <li><a href="#">English</a></li>
            <li><a href="#">Français</a></li>
            <li><a href="#">Português</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>Información legal</h4>
          <ul>
            <li><a href="#">Términos y condiciones</a></li>
            <li><a href="#">Privacidad</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      © 2026 Kiadez — Una red social para cumplir deseos.
    </div>
  </footer>
</div>
