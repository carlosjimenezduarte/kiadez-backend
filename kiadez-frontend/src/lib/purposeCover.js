const API = "http://127.0.0.1:8000";
const AAD_PURPOSE = new TextEncoder().encode("kiadez-life-purpose-v1");
const AAD_VAULT = new TextEncoder().encode("kiadez-vault-v1");
const PURPOSE_PREFIX = "Deseo ";
const PURPOSE_SECRET_TEXT = "Deseo marcado como secreto";
const PURPOSE_REVEAL_PREFIX = "Este deseo será revelado";
const PURPOSE_STORAGE_VERSION = 2;
const LS = {
  purpose: "kiadez_user_purpose",
  coverImg: "kiadez_user_cover_img",
  coverPos: "kiadez_user_cover_pos"
};
const COVER_PRESETS = [
  "/assets/cover-default.jpg",
  "/assets/post-1.jpg",
  "/assets/post-2.jpg"
];

const DEFAULT_PURPOSE_TEXT = {
  1: "Deseo #1: Secreto",
  2: "Deseo construir el Reino de Combray",
  3: "Deseo estar unido a Jesús"
};

const bufToHex = (buf) =>
  [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");

const hexToBuf = (hex) => {
  const bytes = new Uint8Array((hex || "").length / 2);
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
  if (iconKey === "air") return "Aire";
  if (iconKey === "earth") return "Tierra";
  if (iconKey === "water") return "Agua";
  if (iconKey === "fire") return "Fuego";
  return "Icono";
};

const getIconSrc = (iconKey) => `assets/${iconKey}.png`;

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
  const raw = localStorage.getItem(LS.purpose);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
};

const storePurposeValues = (slots) => {
  const slotMap = getPurposeSlotMap(slots);
  const normalizedSlots = [1, 2, 3]
    .map((slotNumber) => {
      const slot = slotMap.get(slotNumber);
      if (!slot) return null;
      return normalizePurposeSlot(slot, slotNumber);
    })
    .filter(Boolean);

  localStorage.setItem(LS.purpose, JSON.stringify({
    version: PURPOSE_STORAGE_VERSION,
    slots: normalizedSlots
  }));
};

const setLifeInputValue = (input, value) => {
  if (!input) return;
  const normalized = normalizePurposeText(value || "");
  input.value = normalized || PURPOSE_PREFIX;
  input.dispatchEvent(new Event("input", { bubbles: true }));
};

const updateModalScrollLock = () => {
  const hasOpenModal = document.querySelector(".modal-overlay:not(.hidden)");
  document.body.classList.toggle("modal-open", Boolean(hasOpenModal));
};

const readCoverPosition = () => {
  const raw = localStorage.getItem(LS.coverPos);
  if (!raw) return { x: 0, y: 0 };
  try {
    const parsed = JSON.parse(raw);
    return {
      x: Number(parsed?.x) || 0,
      y: Number(parsed?.y) || 0
    };
  } catch {
    return { x: 0, y: 0 };
  }
};

const storeCoverState = (src, x, y) => {
  if (src) localStorage.setItem(LS.coverImg, src);
  localStorage.setItem(LS.coverPos, JSON.stringify({ x, y }));
};

const ensureCoverSelectModal = () => {
  if (document.getElementById("coverSelectModal")) return;

  document.body.insertAdjacentHTML("beforeend", `
    <div class="modal-overlay hidden" id="coverSelectModal" aria-hidden="true">
      <div class="modal wish-modal cover-select-modal" role="dialog" aria-modal="true" aria-label="Seleccionar imagen de portada">
        <div class="modal-head">
          <h3>Seleccionar imagen</h3>
        </div>
        <div class="modal-body">
          <div class="cover-select-grid">
            ${COVER_PRESETS.map((src, idx) => `
              <button class="cover-select-item" type="button" data-cover-src="${src}">
                <img src="${src}" alt="Portada ${idx + 1}" />
              </button>
            `).join("")}
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="coverSelectCancel">Cancelar</button>
        </div>
      </div>
    </div>
  `);
};

const ensureCoverLayout = () => {
  const coverMedia = document.getElementById("coverMedia");
  const coverImg = document.getElementById("coverImg");
  const coverActions = coverMedia?.querySelector(".cover-actions");
  if (!coverMedia || !coverImg || !coverActions) return null;

  let coverMenu = coverActions.querySelector(".cover-menu");
  if (!coverMenu) {
    const legacyBtn = coverActions.querySelector("#btnChangeCover");
    const menuEl = document.createElement("details");
    menuEl.className = "cover-menu";
    menuEl.innerHTML = `
      <summary class="icon-btn" id="btnChangeCover" title="Editar imagen de portada">Editar imagen de portada</summary>
      <div class="cover-menu-panel">
        <button class="cover-menu-item" type="button" id="coverSelectExisting">Seleccionar imagen</button>
        <button class="cover-menu-item" type="button" id="coverUpload">Subir imagen</button>
        <button class="cover-menu-item" type="button" id="coverMove">Mover imagen</button>
      </div>
    `;
    if (legacyBtn) {
      legacyBtn.replaceWith(menuEl);
    } else {
      coverActions.prepend(menuEl);
    }
    coverMenu = menuEl;
  }

  const coverSummary = coverMenu.querySelector("#btnChangeCover");
  if (coverSummary) {
    coverSummary.textContent = "Editar imagen de portada";
    coverSummary.title = "Editar imagen de portada";
  }

  if (!coverMenu.querySelector("#coverSelectExisting")) {
    const panel = coverMenu.querySelector(".cover-menu-panel");
    panel?.insertAdjacentHTML("afterbegin", `
      <button class="cover-menu-item" type="button" id="coverSelectExisting">Seleccionar imagen</button>
    `);
  }
  if (!coverMenu.querySelector("#coverUpload")) {
    const panel = coverMenu.querySelector(".cover-menu-panel");
    panel?.insertAdjacentHTML("beforeend", `
      <button class="cover-menu-item" type="button" id="coverUpload">Subir imagen</button>
    `);
  }
  if (!coverMenu.querySelector("#coverMove")) {
    const panel = coverMenu.querySelector(".cover-menu-panel");
    panel?.insertAdjacentHTML("beforeend", `
      <button class="cover-menu-item" type="button" id="coverMove">Mover imagen</button>
    `);
  }

  let coverFile = document.getElementById("coverFile");
  if (!coverFile) {
    coverFile = document.createElement("input");
    coverFile.id = "coverFile";
    coverFile.type = "file";
    coverFile.accept = "image/*";
    coverFile.className = "hidden";
    coverActions.appendChild(coverFile);
  }

  let coverSaveActions = document.getElementById("coverSaveActions");
  if (!coverSaveActions) {
    coverSaveActions = document.createElement("div");
    coverSaveActions.id = "coverSaveActions";
    coverSaveActions.className = "cover-save-actions hidden";
    coverSaveActions.innerHTML = `
      <button class="btn btn-primary btn-compact" type="button" id="coverSaveBtn">Guardar cambios</button>
      <button class="btn btn-outline btn-compact" type="button" id="coverCancelBtn">Cancelar</button>
    `;
    coverMedia.appendChild(coverSaveActions);
  }

  ensureCoverSelectModal();
  return {
    coverMedia,
    coverImg,
    coverMenu,
    coverFile,
    coverSelectExisting: document.getElementById("coverSelectExisting"),
    coverUploadBtn: document.getElementById("coverUpload"),
    coverMoveBtn: document.getElementById("coverMove"),
    coverSaveActions: document.getElementById("coverSaveActions"),
    coverSaveBtn: document.getElementById("coverSaveBtn"),
    coverCancelBtn: document.getElementById("coverCancelBtn"),
    coverSelectModal: document.getElementById("coverSelectModal"),
    coverSelectCancel: document.getElementById("coverSelectCancel")
  };
};

const initCoverEditor = () => {
  const refs = ensureCoverLayout();
  if (!refs) return () => {};

  const {
    coverMedia,
    coverImg,
    coverMenu,
    coverFile,
    coverSelectExisting,
    coverUploadBtn,
    coverMoveBtn,
    coverSaveActions,
    coverSaveBtn,
    coverCancelBtn,
    coverSelectModal,
    coverSelectCancel
  } = refs;

  if (coverMedia.dataset.coverEditorBound === "true") return () => {};
  coverMedia.dataset.coverEditorBound = "true";

  let coverMoveEnabled = false;
  let coverDragActive = false;
  let coverStartX = 0;
  let coverStartY = 0;
  let coverOffsetX = 0;
  let coverOffsetY = 0;
  let coverMaxOffsetX = 0;
  let coverMaxOffsetY = 0;
  let coverSavedSrc = "";
  let coverSavedOffsetX = 0;
  let coverSavedOffsetY = 0;
  let coverDirty = false;

  const closeCoverMenu = () => {
    if (coverMenu && coverMenu.hasAttribute("open")) {
      coverMenu.removeAttribute("open");
    }
  };

  const showCoverActions = () => {
    coverSaveActions?.classList.remove("hidden");
  };

  const hideCoverActions = () => {
    coverSaveActions?.classList.add("hidden");
  };

  const updateCoverTransform = (x, y) => {
    const clampedX = Math.min(coverMaxOffsetX, Math.max(-coverMaxOffsetX, x));
    const clampedY = Math.min(coverMaxOffsetY, Math.max(-coverMaxOffsetY, y));
    coverImg.style.transform = "none";
    coverImg.style.objectPosition = `calc(50% + ${clampedX}px) calc(50% + ${clampedY}px)`;
    return { x: clampedX, y: clampedY };
  };

  const recalcCoverBounds = () => {
    if (!coverImg.naturalWidth || !coverImg.naturalHeight) return;
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

  const setCoverMoveState = (enabled) => {
    coverMoveEnabled = enabled;
    coverMedia.classList.toggle("is-move-mode", enabled);
    coverMoveBtn?.classList.toggle("is-active", enabled);
    updateCoverTransform(coverOffsetX, coverOffsetY);
  };

  const markCoverDirty = () => {
    coverDirty = true;
    showCoverActions();
  };

  const commitCoverState = () => {
    coverSavedSrc = coverImg.src;
    coverSavedOffsetX = coverOffsetX;
    coverSavedOffsetY = coverOffsetY;
    coverDirty = false;
    setCoverMoveState(false);
    hideCoverActions();
    storeCoverState(coverSavedSrc, coverSavedOffsetX, coverSavedOffsetY);
  };

  const revertCoverState = () => {
    coverOffsetX = coverSavedOffsetX;
    coverOffsetY = coverSavedOffsetY;
    if (coverSavedSrc) coverImg.src = coverSavedSrc;
    coverDirty = false;
    setCoverMoveState(false);
    hideCoverActions();
    updateCoverTransform(coverOffsetX, coverOffsetY);
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

  const loadCoverFromStorage = () => {
    const savedImg = localStorage.getItem(LS.coverImg);
    const savedPos = readCoverPosition();
    coverOffsetX = savedPos.x;
    coverOffsetY = savedPos.y;
    coverSavedOffsetX = savedPos.x;
    coverSavedOffsetY = savedPos.y;
    if (savedImg) {
      coverSavedSrc = savedImg;
      coverImg.src = savedImg;
      return;
    }
    coverSavedSrc = coverImg.src;
    updateCoverTransform(coverOffsetX, coverOffsetY);
  };

  const handleCoverUpload = () => coverFile?.click();
  const handleCoverFileChange = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result !== "string") return;
      coverImg.src = reader.result;
      coverOffsetX = 0;
      coverOffsetY = 0;
      markCoverDirty();
      closeCoverMenu();
      setCoverMoveState(true);
      recalcCoverBounds();
    };
    reader.readAsDataURL(file);
    event.target.value = "";
  };

  const handleToggleMove = () => {
    setCoverMoveState(!coverMoveEnabled);
    markCoverDirty();
    closeCoverMenu();
  };

  const handleOpenSelect = () => {
    openCoverSelectModal();
    closeCoverMenu();
  };

  const handleSelectModalClick = (event) => {
    if (event.target === coverSelectModal) {
      closeCoverSelectModal();
      return;
    }
    const button = event.target.closest(".cover-select-item");
    if (!button) return;
    const src = button.dataset.coverSrc;
    if (!src) return;
    coverImg.src = src;
    coverOffsetX = 0;
    coverOffsetY = 0;
    markCoverDirty();
    closeCoverSelectModal();
    setCoverMoveState(true);
    recalcCoverBounds();
  };

  const handleCoverMouseDown = (event) => {
    if (!coverMoveEnabled) return;
    if (event.target.closest(".cover-actions")) return;
    if (event.target.closest(".cover-save-actions")) return;
    coverDragActive = true;
    coverStartX = event.clientX;
    coverStartY = event.clientY;
    coverMedia.classList.add("is-dragging");
  };

  const handleCoverMouseMove = (event) => {
    if (!coverDragActive) return;
    const dx = event.clientX - coverStartX;
    const dy = event.clientY - coverStartY;
    updateCoverTransform(coverOffsetX + dx, coverOffsetY + dy);
  };

  const handleCoverMouseUp = (event) => {
    if (!coverDragActive) return;
    const dx = event.clientX - coverStartX;
    const dy = event.clientY - coverStartY;
    const clamped = updateCoverTransform(coverOffsetX + dx, coverOffsetY + dy);
    coverOffsetX = clamped.x;
    coverOffsetY = clamped.y;
    coverDragActive = false;
    coverMedia.classList.remove("is-dragging");
  };

  const handleCoverImageLoad = () => {
    recalcCoverBounds();
    if (!coverDirty) {
      coverSavedOffsetX = coverOffsetX;
      coverSavedOffsetY = coverOffsetY;
    }
  };

  coverUploadBtn?.addEventListener("click", handleCoverUpload);
  coverFile?.addEventListener("change", handleCoverFileChange);
  coverMoveBtn?.addEventListener("click", handleToggleMove);
  coverSelectExisting?.addEventListener("click", handleOpenSelect);
  coverSelectCancel?.addEventListener("click", closeCoverSelectModal);
  coverSelectModal?.addEventListener("click", handleSelectModalClick);
  coverSaveBtn?.addEventListener("click", commitCoverState);
  coverCancelBtn?.addEventListener("click", revertCoverState);
  coverMedia.addEventListener("mousedown", handleCoverMouseDown);
  window.addEventListener("mousemove", handleCoverMouseMove);
  window.addEventListener("mouseup", handleCoverMouseUp);
  coverImg.addEventListener("load", handleCoverImageLoad);
  window.addEventListener("resize", recalcCoverBounds);

  loadCoverFromStorage();
  hideCoverActions();

  return () => {};
};

const ensurePurposeModals = () => {
  if (!document.getElementById("lifeProposalOverlay")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="lifeProposalOverlay" aria-hidden="true">
        <div class="modal modal-wide life-proposal-modal" role="dialog" aria-modal="true" aria-label="Propósito de vida">
          <div class="modal-head">
            <h3>Propósito de vida</h3>
            <button class="modal-close" type="button" id="lifeProposalClose">✕</button>
          </div>
          <div class="modal-body life-proposal-body">
            <div class="auth-card auth-card--wide auth-card--life life-proposal-card">
              <h2 class="auth-title">Tu propósito de vida</h2>
              <div class="auth-message">
                <p>
                  Escribe tres deseos que orienten tu camino.
                  <br>
                  Son brújula, no presión.
                </p>
                <p class="muted">
                  Estos propósitos se guardan cifrados con tu clave privada personal.
                </p>
              </div>
              <form id="life-form">
                <div class="purpose-group" data-purpose="1">
                  <textarea id="p1" class="wish-prefix-input" data-prefix="Deseo " rows="1" maxlength="80" placeholder="Deseo 1" required>Deseo </textarea>
                  <div class="purpose-actions" role="group" aria-label="Acciones para propósito 1">
                    <button type="button" class="purpose-action" data-action="confirm" title="Confirmar deseo de propósito" aria-label="Confirmar deseo de propósito">
                      <img src="/css/icons/iconsave.webp" alt="Guardar propósito">
                    </button>
                    <button type="button" class="purpose-action" data-action="secret" title="Convertir en secreto" aria-label="Convertir en secreto">
                      <img src="/css/icons/iconkey.webp" alt="Marcar como secreto">
                    </button>
                    <button type="button" class="purpose-action" data-action="reveal" title="Revelar en fecha" aria-label="Revelar en fecha">
                      <img src="/css/icons/iconcalendar.webp" alt="Programar fecha">
                    </button>
                    <button type="button" class="purpose-action" data-action="icon" title="Elegir icono" aria-label="Elegir icono">
                      <img src="/css/icons/iconelemental.webp" alt="Elegir icono">
                    </button>
                  </div>
                  <input type="date" class="purpose-date" aria-label="Fecha de revelacion para proposito 1">
                  <div class="purpose-icon-panel" aria-label="Selector de iconos">
                    <button type="button" class="purpose-icon" data-icon="air" title="Aire"><img src="assets/air.png" alt="Aire"></button>
                    <button type="button" class="purpose-icon" data-icon="earth" title="Tierra"><img src="assets/earth.png" alt="Tierra"></button>
                    <button type="button" class="purpose-icon" data-icon="water" title="Agua"><img src="assets/water.png" alt="Agua"></button>
                    <button type="button" class="purpose-icon" data-icon="fire" title="Fuego"><img src="assets/fire.png" alt="Fuego"></button>
                  </div>
                  <div class="purpose-status" aria-live="polite">Estado: público por defecto.</div>
                </div>
                <div class="purpose-group" data-purpose="2">
                  <textarea id="p2" class="wish-prefix-input" data-prefix="Deseo " rows="1" maxlength="80" placeholder="Deseo 2" required>Deseo </textarea>
                  <div class="purpose-actions" role="group" aria-label="Acciones para propósito 2">
                    <button type="button" class="purpose-action" data-action="confirm" title="Confirmar deseo de propósito" aria-label="Confirmar deseo de propósito">
                      <img src="/css/icons/iconsave.webp" alt="Guardar propósito">
                    </button>
                    <button type="button" class="purpose-action" data-action="secret" title="Convertir en secreto" aria-label="Convertir en secreto">
                      <img src="/css/icons/iconkey.webp" alt="Marcar como secreto">
                    </button>
                    <button type="button" class="purpose-action" data-action="reveal" title="Revelar en fecha" aria-label="Revelar en fecha">
                      <img src="/css/icons/iconcalendar.webp" alt="Programar fecha">
                    </button>
                    <button type="button" class="purpose-action" data-action="icon" title="Elegir icono" aria-label="Elegir icono">
                      <img src="/css/icons/iconelemental.webp" alt="Elegir icono">
                    </button>
                  </div>
                  <input type="date" class="purpose-date" aria-label="Fecha de revelacion para proposito 2">
                  <div class="purpose-icon-panel" aria-label="Selector de iconos">
                    <button type="button" class="purpose-icon" data-icon="air" title="Aire"><img src="assets/air.png" alt="Aire"></button>
                    <button type="button" class="purpose-icon" data-icon="earth" title="Tierra"><img src="assets/earth.png" alt="Tierra"></button>
                    <button type="button" class="purpose-icon" data-icon="water" title="Agua"><img src="assets/water.png" alt="Agua"></button>
                    <button type="button" class="purpose-icon" data-icon="fire" title="Fuego"><img src="assets/fire.png" alt="Fuego"></button>
                  </div>
                  <div class="purpose-status" aria-live="polite">Estado: público por defecto.</div>
                </div>
                <div class="purpose-group" data-purpose="3">
                  <textarea id="p3" class="wish-prefix-input" data-prefix="Deseo " rows="1" maxlength="80" placeholder="Deseo 3" required>Deseo </textarea>
                  <div class="purpose-actions" role="group" aria-label="Acciones para propósito 3">
                    <button type="button" class="purpose-action" data-action="confirm" title="Confirmar deseo de propósito" aria-label="Confirmar deseo de propósito">
                      <img src="/css/icons/iconsave.webp" alt="Guardar propósito">
                    </button>
                    <button type="button" class="purpose-action" data-action="secret" title="Convertir en secreto" aria-label="Convertir en secreto">
                      <img src="/css/icons/iconkey.webp" alt="Marcar como secreto">
                    </button>
                    <button type="button" class="purpose-action" data-action="reveal" title="Revelar en fecha" aria-label="Revelar en fecha">
                      <img src="/css/icons/iconcalendar.webp" alt="Programar fecha">
                    </button>
                    <button type="button" class="purpose-action" data-action="icon" title="Elegir icono" aria-label="Elegir icono">
                      <img src="/css/icons/iconelemental.webp" alt="Elegir icono">
                    </button>
                  </div>
                  <input type="date" class="purpose-date" aria-label="Fecha de revelacion para proposito 3">
                  <div class="purpose-icon-panel" aria-label="Selector de iconos">
                    <button type="button" class="purpose-icon" data-icon="air" title="Aire"><img src="assets/air.png" alt="Aire"></button>
                    <button type="button" class="purpose-icon" data-icon="earth" title="Tierra"><img src="assets/earth.png" alt="Tierra"></button>
                    <button type="button" class="purpose-icon" data-icon="water" title="Agua"><img src="assets/water.png" alt="Agua"></button>
                    <button type="button" class="purpose-icon" data-icon="fire" title="Fuego"><img src="assets/fire.png" alt="Fuego"></button>
                  </div>
                  <div class="purpose-status" aria-live="polite">Estado: público por defecto.</div>
                </div>
                <button type="submit" class="btn btn-primary">Guardar propósito</button>
                <button type="button" class="btn btn-outline" id="lifeProposalCloseFooter">Volver</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("lifeConfirmOverlay")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="lifeConfirmOverlay" aria-hidden="true">
        <div class="modal" role="dialog" aria-modal="true" aria-label="Confirmar propósito público">
          <div class="modal-head">
            <h3>Confirmar propósito</h3>
            <button class="modal-close" type="button" id="lifeConfirmClose">✕</button>
          </div>
          <div class="modal-body">
            <p class="modal-label-center" id="lifeConfirmText">¿Confirmar este deseo como público?</p>
            <p class="modal-label-center muted">Se guardará como público.</p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-outline btn-compact" type="button" id="lifeConfirmCancel">Cancelar</button>
            <button class="btn btn-primary btn-compact" type="button" id="lifeConfirmOk">Confirmar</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeUnlockOverlay")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeUnlockOverlay" aria-hidden="true">
        <div class="modal wish-modal purpose-unlock-modal" role="dialog" aria-modal="true" aria-label="Desbloquear deseo secreto">
          <div class="modal-head">
            <h3>Desbloquear deseo secreto</h3>
            <button class="modal-close" type="button" id="purposeUnlockClose">✕</button>
          </div>
          <div class="modal-body">
            <p class="modal-label-center" id="purposeUnlockText">Si confirmas tu clave privada, este deseo se volverá público.</p>
            <label class="modal-label hidden" for="purposeUnlockPassword">Clave privada personal</label>
            <input class="modal-input" id="purposeUnlockPassword" type="password" autocomplete="off" placeholder="Clave privada personal" />
            <p class="purpose-unlock-error" id="purposeUnlockError" aria-live="polite"></p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-outline btn-compact" type="button" id="purposeUnlockCancel">Cancelar</button>
            <button class="btn btn-primary btn-compact" type="button" id="purposeUnlockConfirm">Desbloquear</button>
          </div>
        </div>
      </div>
    `);
  }
};

const enhancePrefixInputs = (scopeEl) => {
  const inputs = scopeEl.querySelectorAll(".wish-prefix-input");
  inputs.forEach((input) => {
    const prefix = input.dataset.prefix || "Deseo ";
    const maxLength = input.maxLength > 0 ? input.maxLength : null;
    const clampToMax = () => {
      if (maxLength && input.value.length > maxLength) {
        input.value = input.value.slice(0, maxLength);
      }
    };
    if (!input.value.startsWith(prefix)) {
      input.value = `${prefix}${input.value}`;
    }
    clampToMax();
    const ensurePrefix = () => {
      if (!input.value.startsWith(prefix)) {
        const cleaned = input.value.replace(prefix, "");
        input.value = `${prefix}${cleaned}`;
      }
      if (input.value.length < prefix.length) {
        input.value = prefix;
      }
      clampToMax();
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
};

const ensurePurposeLayout = () => {
  const coverMedia = document.getElementById("coverMedia");
  if (!coverMedia) return null;

  const coverActions = coverMedia.querySelector(".cover-actions");
  const btnEditPurposes = document.getElementById("btnEditPurposes");
  if (coverActions && btnEditPurposes) {
    coverActions.classList.add("cover-actions-purpose");
    btnEditPurposes.classList.add("cover-purpose-btn");
    btnEditPurposes.textContent = "Editar mi propósito de vida";
    btnEditPurposes.title = "Editar mi propósito de vida";
  }

  let root = coverMedia.querySelector(".purpose-stack-modern");
  if (!root) {
    const legacyRoot = coverMedia.querySelector(".purpose-stack, .purpose-triangle");
    const legacyP1 = document.getElementById("purpose1");
    const legacyP2 = document.getElementById("purpose2");
    const legacyP3 = document.getElementById("purpose3");
    const currentText = {
      1: legacyP1?.textContent?.trim() || DEFAULT_PURPOSE_TEXT[1],
      2: legacyP2?.textContent?.trim() || DEFAULT_PURPOSE_TEXT[2],
      3: legacyP3?.textContent?.trim() || DEFAULT_PURPOSE_TEXT[3]
    };

    const stack = document.createElement("div");
    stack.className = "purpose-stack purpose-stack-modern";
    stack.setAttribute("aria-label", "Deseos de propósito");
    stack.innerHTML = `
      <div class="purpose-list">
        ${[1, 2, 3].map((slot) => `
          <div class="purpose-pill-row">
            <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="${slot}" title="Marcar deseo ${slot} como cumplido">
              <img src="/css/icons/iconfulfill.webp" alt="Marcar deseo cumplido" />
            </button>
            <button class="purpose-pill" type="button" id="purpose${slot}">${currentText[slot]}</button>
            <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock${slot}" data-slot="${slot}" title="Desbloquear deseo ${slot}">
              <img src="/css/icons/iconkey.webp" alt="Desbloquear deseo secreto" />
            </button>
          </div>
        `).join("")}
      </div>
    `;

    if (legacyRoot) {
      legacyRoot.replaceWith(stack);
    } else {
      coverMedia.appendChild(stack);
    }
    root = stack;
  }

  return {
    btnEditPurposes: document.getElementById("btnEditPurposes"),
    purposePills: {
      1: document.getElementById("purpose1"),
      2: document.getElementById("purpose2"),
      3: document.getElementById("purpose3")
    },
    purposeUnlocks: {
      1: document.getElementById("purposeUnlock1"),
      2: document.getElementById("purposeUnlock2"),
      3: document.getElementById("purposeUnlock3")
    },
    purposeFulfillBtns: root.querySelectorAll(".purpose-fulfill-btn")
  };
};

const getAccessToken = () => localStorage.getItem("access_token") || "";

export const initPurposeCoverModule = () => {
  const cleanupCoverEditor = initCoverEditor();
  ensurePurposeModals();
  const layout = ensurePurposeLayout();
  if (!layout) return cleanupCoverEditor;

  const {
    btnEditPurposes,
    purposePills,
    purposeUnlocks,
    purposeFulfillBtns
  } = layout;

  const defaultPurposeTextBySlot = {
    1: purposePills[1]?.textContent?.trim() || DEFAULT_PURPOSE_TEXT[1],
    2: purposePills[2]?.textContent?.trim() || DEFAULT_PURPOSE_TEXT[2],
    3: purposePills[3]?.textContent?.trim() || DEFAULT_PURPOSE_TEXT[3]
  };

  const lifeProposalOverlay = document.getElementById("lifeProposalOverlay");
  const lifeProposalClose = document.getElementById("lifeProposalClose");
  const lifeProposalCloseFooter = document.getElementById("lifeProposalCloseFooter");
  const lifeConfirmOverlay = document.getElementById("lifeConfirmOverlay");
  const lifeConfirmClose = document.getElementById("lifeConfirmClose");
  const lifeConfirmCancel = document.getElementById("lifeConfirmCancel");
  const lifeConfirmOk = document.getElementById("lifeConfirmOk");
  const lifeConfirmText = document.getElementById("lifeConfirmText");
  const purposeUnlockOverlay = document.getElementById("purposeUnlockOverlay");
  const purposeUnlockClose = document.getElementById("purposeUnlockClose");
  const purposeUnlockCancel = document.getElementById("purposeUnlockCancel");
  const purposeUnlockConfirm = document.getElementById("purposeUnlockConfirm");
  const purposeUnlockPassword = document.getElementById("purposeUnlockPassword");
  const purposeUnlockError = document.getElementById("purposeUnlockError");
  const purposeUnlockText = document.getElementById("purposeUnlockText");

  enhancePrefixInputs(lifeProposalOverlay);

  let purposeSlots = [];
  let activePurposeUnlockSlot = null;
  let pendingConfirmGroup = null;

  const setPurposeStatus = (groupEl, text) => {
    const statusEl = groupEl.querySelector(".purpose-status");
    if (statusEl) statusEl.textContent = text;
  };

  const getPurposePresentation = (slot) => {
    if (!slot) return { text: "", showUnlock: false };
    if (slot.reveal_at && isRevealPending(slot.reveal_at)) {
      return {
        text: `${PURPOSE_REVEAL_PREFIX} ${formatRevealDate(slot.reveal_at)}`,
        showUnlock: false
      };
    }
    if (slot.is_private) return { text: PURPOSE_SECRET_TEXT, showUnlock: true };
    return { text: slot.text_public || slot.text_input || "", showUnlock: false };
  };

  const renderPurposeSlots = (slots) => {
    const slotMap = getPurposeSlotMap(slots);
    [1, 2, 3].forEach((slotNumber) => {
      const slot = slotMap.get(slotNumber);
      const pill = purposePills[slotNumber];
      const unlockBtn = purposeUnlocks[slotNumber];
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
            text_input: remoteSlot.text_public || localSlot?.text_input || ""
          }, slotNumber);
        }
        if (localSlot) return normalizePurposeSlot(localSlot, slotNumber);
        return null;
      })
      .filter(Boolean);
  };

  const fetchPurposeSlotsFromApi = async () => {
    const token = getAccessToken();
    if (!token) return [];
    try {
      const res = await fetch(`${API}/life-purpose/mine`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) return [];
      const data = await res.json();
      if (!Array.isArray(data?.slots)) return [];
      return data.slots
        .map((slot, index) => normalizePurposeSlot(slot, index + 1))
        .filter((slot) => slot.slot_number >= 1 && slot.slot_number <= 3);
    } catch (err) {
      console.error(err);
      return [];
    }
  };

  const loadPurposeFromStorage = async () => {
    const storedSlots = normalizePurposeState(readPurposeStorage());
    if (storedSlots.length) {
      purposeSlots = storedSlots;
      renderPurposeSlots(purposeSlots);
    }

    const remoteSlots = await fetchPurposeSlotsFromApi();
    if (!remoteSlots.length) return;

    purposeSlots = mergePurposeSlots(remoteSlots, storedSlots);
    renderPurposeSlots(purposeSlots);
    storePurposeValues(purposeSlots);
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
        iconActionBtn.title = `Icono: ${iconLabel}`;
      } else {
        iconActionBtn.innerHTML = "<img src=\"/css/icons/iconelemental.webp\" alt=\"Elegir icono\">";
        iconActionBtn.title = "Elegir icono";
      }
    }

    if (!slotData) {
      setPurposeStatus(groupEl, "Estado: público por defecto.");
      return;
    }
    if (slotData.reveal_at && isRevealPending(slotData.reveal_at)) {
      setPurposeStatus(groupEl, `Estado: se revelará el día ${formatRevealDate(slotData.reveal_at)}.`);
      return;
    }
    if (isPrivate) {
      setPurposeStatus(groupEl, "Estado: marcado como secreto.");
      return;
    }
    setPurposeStatus(groupEl, "Estado: confirmado (publico).");
  };

  const openLifeProposalModal = () => {
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
    lifeProposalOverlay.classList.add("hidden");
    lifeProposalOverlay.setAttribute("aria-hidden", "true");
    updateModalScrollLock();
  };

  const closeConfirmModal = () => {
    lifeConfirmOverlay.classList.add("hidden");
    lifeConfirmOverlay.setAttribute("aria-hidden", "true");
    pendingConfirmGroup = null;
    updateModalScrollLock();
  };

  const openConfirmModal = (groupEl) => {
    pendingConfirmGroup = groupEl;
    const number = groupEl?.dataset?.purpose;
    lifeConfirmText.textContent = number
      ? `¿Confirmar el propósito ${number} como público?`
      : "¿Confirmar este deseo como público?";
    lifeConfirmOverlay.classList.remove("hidden");
    lifeConfirmOverlay.setAttribute("aria-hidden", "false");
    updateModalScrollLock();
  };

  const closePurposeUnlockModal = () => {
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
    purposeUnlockText.textContent = `Si confirmas tu clave privada, el deseo ${slotNumber} se volverá público.`;
    purposeUnlockError.textContent = "";
    purposeUnlockError.classList.remove("is-visible");
    purposeUnlockPassword.value = "";
    purposeUnlockOverlay.classList.remove("hidden");
    purposeUnlockOverlay.setAttribute("aria-hidden", "false");
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
      { name: "PBKDF2", salt: saltBuf, iterations: iters, hash: "SHA-256" },
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
      throw new Error(vaultData.detail || "No se pudo leer el vault.");
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
    sessionStorage.setItem("dek_hex", bufToHex(dekRaw));
    return crypto.subtle.importKey("raw", dekRaw, { name: "AES-GCM" }, false, ["encrypt", "decrypt"]);
  };

  const importDekFromSession = async () => {
    const dekHex = sessionStorage.getItem("dek_hex");
    if (!dekHex) {
      throw new Error("Vault no desbloqueado. Crea tu clave privada o desbloquéala primero.");
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
      purposeUnlockError.textContent = "Debes digitar tu clave privada personal.";
      purposeUnlockError.classList.add("is-visible");
      return;
    }

    const slotMap = getPurposeSlotMap(purposeSlots);
    const slotData = slotMap.get(activePurposeUnlockSlot);
    if (!slotData?.ciphertext_hex || !slotData?.nonce_hex) {
      purposeUnlockError.textContent = "No hay datos cifrados para este deseo.";
      purposeUnlockError.classList.add("is-visible");
      return;
    }

    const token = getAccessToken();
    if (!token) {
      purposeUnlockError.textContent = "No hay sesión activa.";
      purposeUnlockError.classList.add("is-visible");
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
        throw new Error(revealData.detail || "No se pudo revelar el deseo.");
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
      purposeUnlockError.textContent = err?.message || "No se pudo desbloquear el deseo.";
      purposeUnlockError.classList.add("is-visible");
    }
  };

  const lifeForm = lifeProposalOverlay.querySelector("#life-form");

  lifeConfirmClose?.addEventListener("click", closeConfirmModal);
  lifeConfirmCancel?.addEventListener("click", closeConfirmModal);
  lifeConfirmOverlay?.addEventListener("click", (event) => {
    if (event.target === lifeConfirmOverlay) closeConfirmModal();
  });
  lifeConfirmOk?.addEventListener("click", () => {
    if (!pendingConfirmGroup) return closeConfirmModal();
    pendingConfirmGroup.dataset.isPrivate = "false";
    setPurposeStatus(pendingConfirmGroup, "Estado: confirmado (publico).");
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

      if (action === "confirm") return openConfirmModal(groupEl);
      if (action === "secret") {
        groupEl.dataset.isPrivate = "true";
        setPurposeStatus(groupEl, "Estado: marcado como secreto.");
        return;
      }
      if (action === "reveal") {
        const dateInput = groupEl.querySelector(".purpose-date");
        if (!dateInput) return;
        if (typeof dateInput.showPicker === "function") dateInput.showPicker();
        else {
          dateInput.focus();
          dateInput.click();
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
        actionBtn.title = `Icono: ${label}`;
      }
      setPurposeStatus(groupEl, `Estado: icono asociado: ${label}.`);
      panel.classList.remove("is-open");
    });
  });

  lifeProposalOverlay.querySelectorAll(".purpose-date").forEach((dateInput) => {
    dateInput.addEventListener("change", () => {
      const groupEl = dateInput.closest(".purpose-group");
      groupEl.dataset.revealAt = dateInput.value || "";
      if (!dateInput.value) return;
      setPurposeStatus(groupEl, `Estado: se revelará el día ${formatRevealDate(dateInput.value)}.`);
    });
  });

  lifeForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const groups = [...lifeProposalOverlay.querySelectorAll(".purpose-group")];
    const values = groups.map((groupEl) => {
      const textarea = groupEl.querySelector("textarea");
      return normalizePurposeText(textarea?.value || "");
    });
    if (values.some((value) => !value)) {
      groups.forEach((groupEl, index) => {
        if (!values[index]) setPurposeStatus(groupEl, "Completa este propósito antes de guardar.");
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
            setPurposeStatus(groupEl, err.message || "No se pudo desbloquear el vault.");
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
        const nonce = crypto.getRandomValues(new Uint8Array(12));
        const ptBuf = new TextEncoder().encode(text).buffer;
        const ct = await crypto.subtle.encrypt(
          { name: "AES-GCM", iv: nonce, additionalData: AAD_PURPOSE },
          dekKey,
          ptBuf
        );
        const encrypted = { nonce_hex: bufToHex(nonce.buffer), ciphertext_hex: bufToHex(ct) };
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

    purposeSlots = localSlots
      .map((slot) => normalizePurposeSlot(slot, Number(slot.slot_number)))
      .sort((a, b) => a.slot_number - b.slot_number);
    renderPurposeSlots(purposeSlots);
    storePurposeValues(purposeSlots);

    try {
      await fetch(`${API}/life-purpose/save`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify({ slots })
      });
    } catch (err) {
      console.error(err);
    }

    closeLifeProposalModal();
  });

  btnEditPurposes?.addEventListener("click", openLifeProposalModal);
  lifeProposalClose?.addEventListener("click", closeLifeProposalModal);
  lifeProposalCloseFooter?.addEventListener("click", closeLifeProposalModal);
  lifeProposalOverlay?.addEventListener("click", (event) => {
    if (event.target === lifeProposalOverlay) closeLifeProposalModal();
  });

  [purposeUnlocks[1], purposeUnlocks[2], purposeUnlocks[3]].forEach((unlockBtn) => {
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
      btn.setAttribute("title", "Deseo marcado como cumplido (demo)");
    });
  });

  void loadPurposeFromStorage();

  return () => {};
};
