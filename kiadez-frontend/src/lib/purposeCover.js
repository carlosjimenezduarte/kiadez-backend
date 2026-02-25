import { clearDekSession, getDekSessionHex, setDekSessionHex } from "./dekSession";

const API = "http://127.0.0.1:8000";
const AAD_PURPOSE = new TextEncoder().encode("kiadez-life-purpose-v1");
const AAD_VAULT = new TextEncoder().encode("kiadez-vault-v1");
const AAD_PRIVATE_WISH = new TextEncoder().encode("kiadez-private-wish-v1");
const PRIVATE_MEDIA_AAD_PREFIX = "kiadez-private-media-v1:";
const PURPOSE_PREFIX = "Deseo ";
const PURPOSE_SECRET_TEXT = "Deseo marcado como secreto";
const PURPOSE_UNDEFINED_TEXT = "Deseo de propósito sin definir";
const PURPOSE_REVEAL_PREFIX = "Este deseo será revelado";
const COVER_DEFAULT_IMAGE = "/assets/cover-default.jpg";

const DEFAULT_PURPOSE_TEXT = {
  1: "Deseo #1: Secreto",
  2: "Deseo construir el Reino de Combray",
  3: "Deseo estar unido a Jesús"
};

const getAccessToken = () =>
  localStorage.getItem("access_token") ||
  localStorage.getItem("kiadez_access_token") ||
  "";

const parseResponseJson = async (response) => {
  try {
    return await response.json();
  } catch {
    return {};
  }
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
  const status = slot?.status || "active";

  // A fulfilled slot is considered "vacant" so the user can define a new purpose explicitly.
  if (String(status) === "fulfilled") {
    return {
      slot_number: slotNumber,
      is_private: false,
      status: "fulfilled",
      reveal_at: null,
      icon_key: null,
      text_public: null,
      text_input: "",
      ciphertext_hex: null,
      nonce_hex: null,
    };
  }
  return {
    slot_number: slotNumber,
    is_private: Boolean(slot?.is_private),
    status,
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

  const coverSelectExisting = coverMenu.querySelector("#coverSelectExisting");
  if (coverSelectExisting) {
    coverSelectExisting.remove();
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

  return {
    coverMedia,
    coverImg,
    coverMenu,
    coverFile,
    coverUploadBtn: document.getElementById("coverUpload"),
    coverMoveBtn: document.getElementById("coverMove"),
    coverSaveActions: document.getElementById("coverSaveActions"),
    coverSaveBtn: document.getElementById("coverSaveBtn"),
    coverCancelBtn: document.getElementById("coverCancelBtn")
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
    coverUploadBtn,
    coverMoveBtn,
    coverSaveActions,
    coverSaveBtn,
    coverCancelBtn
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
  let coverSavedSrc = COVER_DEFAULT_IMAGE;
  let coverSavedMediaId = null;
  let coverActiveMediaId = null;
  let coverSavedOffsetX = 0;
  let coverSavedOffsetY = 0;
  let coverPendingUploadFile = null;
  let coverPreviewObjectUrl = "";
  let coverSaving = false;
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

  const revokeCoverPreviewUrl = () => {
    if (!coverPreviewObjectUrl) return;
    try {
      URL.revokeObjectURL(coverPreviewObjectUrl);
    } catch {
      // no-op
    }
    coverPreviewObjectUrl = "";
  };

  const resetCoverPendingMedia = () => {
    coverPendingUploadFile = null;
    revokeCoverPreviewUrl();
  };

  const uploadCoverImageFile = async (file) => {
    const token = getAccessToken();
    if (!token) throw new Error("No hay sesión activa.");

    const formData = new FormData();
    formData.append("visibility", "public");
    formData.append("file", file);

    const response = await fetch(`${API}/media/upload/direct`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });
    const data = await parseResponseJson(response);
    if (!response.ok) {
      throw new Error(data?.detail || "No se pudo subir la portada.");
    }
    const mediaId = Number(data?.media_id || 0) || null;
    if (!mediaId) {
      throw new Error("No se recibió media_id para la portada.");
    }
    return {
      media_id: mediaId,
      url: String(data?.url || "").trim() || null,
    };
  };

  const loadCoverFromApi = async () => {
    const token = getAccessToken();
    if (!token) return;
    try {
      const response = await fetch(`${API}/media/cover-photo`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await parseResponseJson(response);
      if (!response.ok) return;

      coverSavedMediaId = Number(data?.media_id || 0) || null;
      coverActiveMediaId = coverSavedMediaId;
      coverSavedSrc = String(data?.url || "").trim() || COVER_DEFAULT_IMAGE;
      coverSavedOffsetX = Number(data?.offset_x || 0) || 0;
      coverSavedOffsetY = Number(data?.offset_y || 0) || 0;
      coverOffsetX = coverSavedOffsetX;
      coverOffsetY = coverSavedOffsetY;
      coverDirty = false;
      resetCoverPendingMedia();
      coverImg.src = coverSavedSrc;
      recalcCoverBounds();
      updateCoverTransform(coverOffsetX, coverOffsetY);
    } catch {
      // no-op: keep default cover if API is unavailable.
    }
  };

  const commitCoverState = async () => {
    if (coverSaving) return;
    const token = getAccessToken();
    if (!token) {
      window.location.href = "/login.html";
      return;
    }
    coverSaving = true;
    if (coverSaveBtn) coverSaveBtn.disabled = true;
    if (coverCancelBtn) coverCancelBtn.disabled = true;
    try {
      let mediaIdToSave = coverActiveMediaId;
      if (coverPendingUploadFile) {
        const uploaded = await uploadCoverImageFile(coverPendingUploadFile);
        mediaIdToSave = uploaded.media_id;
        coverActiveMediaId = uploaded.media_id;
        if (uploaded.url) {
          coverImg.src = uploaded.url;
        }
      }

      const response = await fetch(`${API}/media/cover-photo`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          media_id: mediaIdToSave,
          offset_x: Math.round(coverOffsetX),
          offset_y: Math.round(coverOffsetY),
        }),
      });
      const data = await parseResponseJson(response);
      if (!response.ok) {
        throw new Error(data?.detail || "No se pudo guardar la portada.");
      }

      coverSavedMediaId = Number(data?.media_id || 0) || null;
      coverActiveMediaId = coverSavedMediaId;
      coverSavedSrc = String(data?.url || "").trim() || coverImg.src || COVER_DEFAULT_IMAGE;
      coverSavedOffsetX = Number(data?.offset_x || 0) || 0;
      coverSavedOffsetY = Number(data?.offset_y || 0) || 0;
      coverOffsetX = coverSavedOffsetX;
      coverOffsetY = coverSavedOffsetY;
      coverDirty = false;
      resetCoverPendingMedia();
      setCoverMoveState(false);
      hideCoverActions();
      if (coverSavedSrc) {
        coverImg.src = coverSavedSrc;
      }
      recalcCoverBounds();
      updateCoverTransform(coverOffsetX, coverOffsetY);
      window.dispatchEvent(new CustomEvent("kiadez:cover-photo-updated", { detail: data }));
    } catch (error) {
      window.alert(error?.message || "No se pudo guardar la portada.");
    } finally {
      coverSaving = false;
      if (coverSaveBtn) coverSaveBtn.disabled = false;
      if (coverCancelBtn) coverCancelBtn.disabled = false;
    }
  };

  const revertCoverState = () => {
    coverOffsetX = coverSavedOffsetX;
    coverOffsetY = coverSavedOffsetY;
    coverActiveMediaId = coverSavedMediaId;
    if (coverSavedSrc) coverImg.src = coverSavedSrc;
    coverDirty = false;
    resetCoverPendingMedia();
    setCoverMoveState(false);
    hideCoverActions();
    updateCoverTransform(coverOffsetX, coverOffsetY);
  };

  const handleCoverUpload = () => coverFile?.click();
  const handleCoverFileChange = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    resetCoverPendingMedia();
    coverPendingUploadFile = file;
    coverPreviewObjectUrl = URL.createObjectURL(file);
    coverImg.src = coverPreviewObjectUrl;
    coverOffsetX = 0;
    coverOffsetY = 0;
    markCoverDirty();
    closeCoverMenu();
    setCoverMoveState(true);
    recalcCoverBounds();
    event.target.value = "";
  };

  const handleToggleMove = () => {
    setCoverMoveState(!coverMoveEnabled);
    markCoverDirty();
    closeCoverMenu();
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
  coverSaveBtn?.addEventListener("click", () => void commitCoverState());
  coverCancelBtn?.addEventListener("click", revertCoverState);
  coverMedia.addEventListener("mousedown", handleCoverMouseDown);
  window.addEventListener("mousemove", handleCoverMouseMove);
  window.addEventListener("mouseup", handleCoverMouseUp);
  coverImg.addEventListener("load", handleCoverImageLoad);
  window.addEventListener("resize", recalcCoverBounds);

  void loadCoverFromApi();
  hideCoverActions();

  return () => {
    revokeCoverPreviewUrl();
  };
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

  if (!document.getElementById("purposeFulfillOverlay")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeFulfillOverlay" aria-hidden="true">
        <div class="modal wish-modal fulfill-wish-modal purpose-fulfill-modal" role="dialog" aria-modal="true" aria-label="Subir evidencia">
          <div class="modal-head">
            <h3>¡Sube la evidencia!</h3>
            <button class="modal-close" type="button" id="purposeFulfillClose">✕</button>
          </div>
          <div class="modal-body">
            <p class="panel-muted"><strong>¿Dónde quieres publicarlo?</strong></p>
            <div class="purpose-publish-choice" role="group" aria-label="Seleccionar dónde publicar">
              <button class="purpose-publish-btn is-selected" type="button" data-publish="private" aria-pressed="true">
                <span class="purpose-publish-emoji" aria-hidden="true">🔒</span>
                <span>Privado</span>
              </button>
              <button class="purpose-publish-btn" type="button" data-publish="public" aria-pressed="false">
                <span class="purpose-publish-emoji" aria-hidden="true">🌐</span>
                <span>Público</span>
              </button>
            </div>

            <div class="purpose-private-key" id="purposeFulfillKeyRow">
              <label class="modal-label" for="purposeFulfillPassword">Clave privada personal</label>
              <input class="modal-input" id="purposeFulfillPassword" type="password" autocomplete="off" placeholder="Clave privada personal" />
              <p class="panel-muted purpose-private-key-note">
                Digita tu clave privada personal para confirmar tu decisión.
              </p>
            </div>

            <input id="purposeFulfillEvidence" type="file" accept="image/*" class="hidden" />
            <div class="wish-image-preview" id="purposeFulfillEvidencePreview" aria-live="polite">
              <label class="wish-image-btn" for="purposeFulfillEvidence" aria-label="Sube la evidencia visual">+</label>
              <div class="wish-preview-content">
                <span class="wish-preview-placeholder">Sube la evidencia visual.</span>
                <span class="wish-preview-name">PNG, WEBP, JPEG, etc.</span>
              </div>
            </div>

            <p class="panel-muted">
              <strong>¿Declaras bajo verdad de juramento que este deseo se ha cumplido?</strong>
            </p>
            <p class="purpose-fulfill-error" id="purposeFulfillError" aria-live="polite"></p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-primary btn-compact" type="button" id="purposeFulfillConfirm">
              Juro bajo verdad de juramento que este deseo se ha cumplido
            </button>
          </div>
          <div class="modal-actions">
            <button class="btn btn-outline btn-compact" type="button" id="purposeFulfillCancel">Cancelar</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeVaultOverlay")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeVaultOverlay" aria-hidden="true">
        <div class="modal wish-modal purpose-vault-modal" role="dialog" aria-modal="true" aria-label="Desbloquear clave privada">
          <div class="modal-body">
            <img class="private-security-hero" src="/css/cpp-key.webp" alt="Clave privada" />
            <h2 class="private-security-title">Digita tu contraseña privada personal:</h2>

            <div class="private-security-input-row">
              <label class="modal-label hidden" for="purposeVaultPassword">Contraseña privada</label>
              <input class="modal-input private-security-input" id="purposeVaultPassword" type="password" autocomplete="off" inputmode="text" placeholder="••••••••••••••" />
              <button class="private-security-btn private-security-unlock" type="button" id="purposeVaultUnlock" aria-label="Ingresar" title="Ingresar">
                <img src="/css/icons/icondoor.webp" alt="Ingresar" />
              </button>
            </div>

            <p class="private-security-error" id="purposeVaultError" role="alert"></p>

            <div class="private-security-actions">
              <button class="private-security-btn" type="button" aria-label="Modificar contraseña privada personal"
                id="purposeVaultChangePassword" title="Modificar contraseña privada personal">
                <img src="/css/icons/iconedit.webp" alt="Cambiar contraseña" />
              </button>
              <button class="private-security-btn" type="button" aria-label="Reiniciar contraseña"
                id="purposeVaultResetPassword" title="Reiniciar contraseña">
                <img src="/css/icons/icondelete.webp" alt="Reiniciar contraseña" />
              </button>
            </div>

            <p class="private-security-note">
              Tu clave secreta personal protege toda la información privada que declares en esta red social: deseos,
              propósitos y datos confidenciales. Sin esta clave, no se habilitan cambios en tu propósito de vida.
            </p>
          </div>

          <div class="modal-actions purpose-vault-actions">
            <button class="btn btn-outline btn-compact" type="button" id="purposeVaultCancel">Cancelar</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeVaultChangePasswordModal")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeVaultChangePasswordModal" aria-hidden="true">
        <div class="modal wish-modal private-change-password-modal" role="dialog" aria-modal="true" aria-label="Modificar contraseña privada personal">
          <div class="modal-head">
            <h3>Modificar contraseña privada personal</h3>
            <button class="modal-close" type="button" id="purposeVaultChangePasswordCancel">✕</button>
          </div>
          <div class="modal-body">
            <label class="modal-label" for="purposeVaultCurrentPassword">Digita tu actual contraseña privada personal</label>
            <input class="modal-input" id="purposeVaultCurrentPassword" type="password" autocomplete="off" />

            <label class="modal-label" for="purposeVaultNewPassword">Digita tu nueva contraseña privada personal</label>
            <input class="modal-input" id="purposeVaultNewPassword" type="password" autocomplete="off" />

            <label class="modal-label" for="purposeVaultConfirmPassword">Confirma tu nueva contraseña privada actual</label>
            <input class="modal-input" id="purposeVaultConfirmPassword" type="password" autocomplete="off" />

            <p class="private-security-error" id="purposeVaultChangePasswordError" role="alert"></p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-primary btn-compact" type="button" id="purposeVaultChangePasswordConfirm">Confirmar</button>
            <button class="btn btn-outline btn-compact" type="button" id="purposeVaultChangePasswordCancelFooter">Cancelar</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeVaultResetPasswordModal")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeVaultResetPasswordModal" aria-hidden="true">
        <div class="modal wish-modal private-reset-modal" role="dialog" aria-modal="true" aria-label="Restaurar contraseña privada personal">
          <div class="modal-head">
            <h3>Restaurar contraseña privada personal</h3>
            <button class="modal-close" type="button" id="purposeVaultResetPasswordCancel">✕</button>
          </div>
          <div class="modal-body">
            <p class="private-reset-text">
              Estás a punto de reiniciar tu clave secreta personal porque la has olvidado.
            </p>
            <p class="private-reset-text">
              Esta acción eliminará de forma permanente todos tus deseos privados y tu información cifrada.
            </p>
            <p class="private-reset-text private-reset-question">
              ¿Estás seguro de que deseas continuar?
            </p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-primary btn-compact" type="button" id="purposeVaultResetPasswordConfirm">Sí, continuar</button>
            <button class="btn btn-outline btn-compact" type="button" id="purposeVaultResetPasswordCancelFooter">Cancelar</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeVaultResetPasswordFinalModal")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeVaultResetPasswordFinalModal" aria-hidden="true">
        <div class="modal wish-modal private-reset-modal" role="dialog" aria-modal="true" aria-label="Confirmación final de eliminación">
          <div class="modal-head">
            <h3>Confirmación final</h3>
            <button class="modal-close" type="button" id="purposeVaultResetPasswordFinalCancel">✕</button>
          </div>
          <div class="modal-body">
            <p class="private-reset-text">
              Para confirmar la eliminación de tu clave secreta personal, escribe la siguiente palabra exactamente como se muestra:
            </p>
            <p class="private-reset-text private-reset-keyword" id="purposeVaultResetKeywordLabel">ELIMINAR</p>
            <input class="modal-input" id="purposeVaultResetPasswordKeyword" type="text" autocomplete="off" />

            <p class="private-security-error" id="purposeVaultResetPasswordError" role="alert"></p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-primary btn-compact" type="button" id="purposeVaultResetPasswordFinalConfirm">Eliminar clave</button>
            <button class="btn btn-outline btn-compact" type="button" id="purposeVaultResetPasswordFinalCancelFooter">Cancelar</button>
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

  const purposeFulfillBySlot = new Map(
    Array.from(purposeFulfillBtns || []).map((btn) => [Number(btn.dataset.slot || 0), btn])
  );

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
  const purposeFulfillOverlay = document.getElementById("purposeFulfillOverlay");
  const purposeFulfillClose = document.getElementById("purposeFulfillClose");
  const purposeFulfillCancel = document.getElementById("purposeFulfillCancel");
  const purposeFulfillConfirm = document.getElementById("purposeFulfillConfirm");
  const purposeFulfillEvidence = document.getElementById("purposeFulfillEvidence");
  const purposeFulfillEvidencePreview = document.getElementById("purposeFulfillEvidencePreview");
  const purposeFulfillKeyRow = document.getElementById("purposeFulfillKeyRow");
  const purposeFulfillPassword = document.getElementById("purposeFulfillPassword");
  const purposeFulfillError = document.getElementById("purposeFulfillError");
  const purposePublishChoice = purposeFulfillOverlay?.querySelector(".purpose-publish-choice");
  const purposeVaultOverlay = document.getElementById("purposeVaultOverlay");
  const purposeVaultPassword = document.getElementById("purposeVaultPassword");
  const purposeVaultUnlock = document.getElementById("purposeVaultUnlock");
  const purposeVaultCancel = document.getElementById("purposeVaultCancel");
  const purposeVaultError = document.getElementById("purposeVaultError");
  const purposeVaultChangePasswordBtn = document.getElementById("purposeVaultChangePassword");
  const purposeVaultResetPasswordBtn = document.getElementById("purposeVaultResetPassword");
  const purposeVaultChangePasswordModal = document.getElementById("purposeVaultChangePasswordModal");
  const purposeVaultChangePasswordCancel = document.getElementById("purposeVaultChangePasswordCancel");
  const purposeVaultChangePasswordCancelFooter = document.getElementById("purposeVaultChangePasswordCancelFooter");
  const purposeVaultCurrentPassword = document.getElementById("purposeVaultCurrentPassword");
  const purposeVaultNewPassword = document.getElementById("purposeVaultNewPassword");
  const purposeVaultConfirmPassword = document.getElementById("purposeVaultConfirmPassword");
  const purposeVaultChangePasswordConfirm = document.getElementById("purposeVaultChangePasswordConfirm");
  const purposeVaultChangePasswordError = document.getElementById("purposeVaultChangePasswordError");
  const purposeVaultResetPasswordModal = document.getElementById("purposeVaultResetPasswordModal");
  const purposeVaultResetPasswordCancel = document.getElementById("purposeVaultResetPasswordCancel");
  const purposeVaultResetPasswordCancelFooter = document.getElementById("purposeVaultResetPasswordCancelFooter");
  const purposeVaultResetPasswordConfirm = document.getElementById("purposeVaultResetPasswordConfirm");
  const purposeVaultResetPasswordFinalModal = document.getElementById("purposeVaultResetPasswordFinalModal");
  const purposeVaultResetPasswordFinalCancel = document.getElementById("purposeVaultResetPasswordFinalCancel");
  const purposeVaultResetPasswordFinalCancelFooter = document.getElementById("purposeVaultResetPasswordFinalCancelFooter");
  const purposeVaultResetKeywordLabel = document.getElementById("purposeVaultResetKeywordLabel");
  const purposeVaultResetPasswordKeyword = document.getElementById("purposeVaultResetPasswordKeyword");
  const purposeVaultResetPasswordFinalConfirm = document.getElementById("purposeVaultResetPasswordFinalConfirm");
  const purposeVaultResetPasswordError = document.getElementById("purposeVaultResetPasswordError");

  enhancePrefixInputs(lifeProposalOverlay);

  let purposeSlots = [];
  let activePurposeUnlockSlot = null;
  let activePurposeFulfillSlot = null;
  let purposePublishTo = "private";
  let purposeFulfillEvidenceUrl = null;
  let purposeFulfillEvidenceImage = null;
  let purposeFulfillBusy = false;
  let pendingConfirmGroup = null;
  let purposeVaultResetKeywords = null;

  const setPurposeStatus = (groupEl, text) => {
    const statusEl = groupEl.querySelector(".purpose-status");
    if (statusEl) statusEl.textContent = text;
  };

  const getPurposePresentation = (slot) => {
    if (!slot) return { text: "", showUnlock: false };
    if (String(slot.status || "active") === "fulfilled") {
      return { text: PURPOSE_UNDEFINED_TEXT, showUnlock: false };
    }
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
      const fulfillBtn = purposeFulfillBySlot.get(slotNumber);
      if (!pill) return;

      if (!slot) {
        pill.classList.remove("is-undefined");
        pill.textContent = defaultPurposeTextBySlot[slotNumber];
        unlockBtn?.classList.add("hidden");
        if (fulfillBtn) {
          fulfillBtn.classList.remove("is-marked");
          fulfillBtn.classList.remove("is-vanished");
          fulfillBtn.disabled = true;
          fulfillBtn.setAttribute("title", "Primero define este propósito para poder marcarlo como cumplido.");
        }
        return;
      }

      const isFulfilled = String(slot.status || "active") === "fulfilled";
      pill.classList.toggle("is-undefined", isFulfilled);
      const view = getPurposePresentation(slot);
      pill.textContent = view.text || defaultPurposeTextBySlot[slotNumber];
      unlockBtn?.classList.toggle("hidden", !view.showUnlock);

      if (fulfillBtn) {
        const hasContent = Boolean(slot.text_public || slot.text_input || slot.ciphertext_hex);
        fulfillBtn.classList.toggle("is-marked", isFulfilled);
        fulfillBtn.classList.toggle("is-vanished", isFulfilled);
        fulfillBtn.disabled = !hasContent || isFulfilled;
        if (isFulfilled) {
          fulfillBtn.setAttribute("title", "Propósito cumplido. Define uno nuevo desde 'Editar mi propósito de vida'.");
        } else if (!hasContent) {
          fulfillBtn.setAttribute("title", "Primero define este propósito para poder marcarlo como cumplido.");
        } else {
          fulfillBtn.setAttribute("title", `Marcar deseo ${slotNumber} como cumplido`);
        }
      }
    });
  };

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
      throw new Error("No hay sesión activa.");
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`
    };
    const res = await fetch(`${API}${path}`, { ...options, headers });
    if (res.status === 401) {
      throw new Error("Sesión expirada. Inicia sesión nuevamente.");
    }
    return res;
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

  const loadPurposeSlots = async () => {
    const remoteSlots = await fetchPurposeSlotsFromApi();
    purposeSlots = remoteSlots;
    renderPurposeSlots(purposeSlots);
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
    const fallbackSlots = Array.isArray(purposeSlots) ? purposeSlots : [];
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

  const setPurposeVaultError = (message) => {
    if (!purposeVaultError) return;
    purposeVaultError.textContent = message || "";
    purposeVaultError.classList.toggle("is-visible", Boolean(message));
  };

  const closePurposeVaultModal = () => {
    if (!purposeVaultOverlay) return;
    purposeVaultOverlay.classList.add("hidden");
    purposeVaultOverlay.setAttribute("aria-hidden", "true");
    if (purposeVaultPassword) purposeVaultPassword.value = "";
    setPurposeVaultError("");
    updateModalScrollLock();
  };

  const openPurposeVaultModal = (message = "") => {
    if (!purposeVaultOverlay) return;
    purposeVaultOverlay.classList.remove("hidden");
    purposeVaultOverlay.setAttribute("aria-hidden", "false");
    setPurposeVaultError(message);
    if (purposeVaultPassword && !message) {
      purposeVaultPassword.value = "";
    }
    setTimeout(() => purposeVaultPassword?.focus(), 0);
    updateModalScrollLock();
  };

  const setPurposeVaultChangePasswordError = (message) => {
    if (!purposeVaultChangePasswordError) return;
    purposeVaultChangePasswordError.textContent = message || "";
    purposeVaultChangePasswordError.classList.toggle("is-visible", Boolean(message));
  };

  const setPurposeVaultResetPasswordError = (message) => {
    if (!purposeVaultResetPasswordError) return;
    purposeVaultResetPasswordError.textContent = message || "";
    purposeVaultResetPasswordError.classList.toggle("is-visible", Boolean(message));
  };

  const closePurposeVaultChangePasswordModal = () => {
    if (!purposeVaultChangePasswordModal) return;
    purposeVaultChangePasswordModal.classList.add("hidden");
    purposeVaultChangePasswordModal.setAttribute("aria-hidden", "true");
    if (purposeVaultCurrentPassword) purposeVaultCurrentPassword.value = "";
    if (purposeVaultNewPassword) purposeVaultNewPassword.value = "";
    if (purposeVaultConfirmPassword) purposeVaultConfirmPassword.value = "";
    setPurposeVaultChangePasswordError("");
    updateModalScrollLock();
  };

  const openPurposeVaultChangePasswordModal = () => {
    if (!purposeVaultChangePasswordModal) return;
    setPurposeVaultChangePasswordError("");
    purposeVaultChangePasswordModal.classList.remove("hidden");
    purposeVaultChangePasswordModal.setAttribute("aria-hidden", "false");
    setTimeout(() => purposeVaultCurrentPassword?.focus(), 0);
    updateModalScrollLock();
  };

  const closePurposeVaultResetPasswordModal = () => {
    if (!purposeVaultResetPasswordModal) return;
    purposeVaultResetPasswordModal.classList.add("hidden");
    purposeVaultResetPasswordModal.setAttribute("aria-hidden", "true");
    updateModalScrollLock();
  };

  const openPurposeVaultResetPasswordModal = () => {
    if (!purposeVaultResetPasswordModal) return;
    void loadPurposeVaultResetKeywords();
    purposeVaultResetPasswordModal.classList.remove("hidden");
    purposeVaultResetPasswordModal.setAttribute("aria-hidden", "false");
    updateModalScrollLock();
  };

  const closePurposeVaultResetPasswordFinalModal = () => {
    if (!purposeVaultResetPasswordFinalModal) return;
    purposeVaultResetPasswordFinalModal.classList.add("hidden");
    purposeVaultResetPasswordFinalModal.setAttribute("aria-hidden", "true");
    if (purposeVaultResetPasswordKeyword) purposeVaultResetPasswordKeyword.value = "";
    setPurposeVaultResetPasswordError("");
    updateModalScrollLock();
  };

  const openPurposeVaultResetPasswordFinalModal = () => {
    if (!purposeVaultResetPasswordFinalModal) return;
    void loadPurposeVaultResetKeywords();
    setPurposeVaultResetPasswordError("");
    if (purposeVaultResetPasswordKeyword) purposeVaultResetPasswordKeyword.value = "";
    purposeVaultResetPasswordFinalModal.classList.remove("hidden");
    purposeVaultResetPasswordFinalModal.setAttribute("aria-hidden", "false");
    setTimeout(() => purposeVaultResetPasswordKeyword?.focus(), 0);
    updateModalScrollLock();
  };

  const loadPurposeVaultResetKeywords = async () => {
    try {
      const res = await apiFetch("/vault/reset-keywords");
      const data = await parseResponseJson(res);
      if (!res.ok) return;
      purposeVaultResetKeywords = data?.keywords || null;
      if (purposeVaultResetKeywordLabel && purposeVaultResetKeywords?.es) {
        purposeVaultResetKeywordLabel.textContent = String(purposeVaultResetKeywords.es);
      }
    } catch {
      // No bloquea el flujo; dejamos palabra por defecto.
    }
  };

  const handlePurposeVaultChangePassword = async () => {
    const current = purposeVaultCurrentPassword?.value || "";
    const next = purposeVaultNewPassword?.value || "";
    const next2 = purposeVaultConfirmPassword?.value || "";

    setPurposeVaultChangePasswordError("");

    if (!current.trim()) {
      setPurposeVaultChangePasswordError("Debes digitar tu contraseña privada actual.");
      return;
    }
    if (!next.trim() || next.length < 8) {
      setPurposeVaultChangePasswordError("Tu nueva clave debe tener al menos 8 caracteres.");
      return;
    }
    if (next !== next2) {
      setPurposeVaultChangePasswordError("La confirmación no coincide con tu nueva clave.");
      return;
    }

    const token = getAccessToken();
    if (!token) {
      window.location.href = "/login.html";
      return;
    }

    try {
      const dekRaw = await decryptDekRawFromPassword(current, token);

      const iters = 310000;
      const salt = crypto.getRandomValues(new Uint8Array(16));
      const kek = await pbkdf2Key(next, salt.buffer, iters);
      const nonce = crypto.getRandomValues(new Uint8Array(12));
      const wrappedDek = await crypto.subtle.encrypt(
        { name: "AES-GCM", iv: nonce, additionalData: AAD_VAULT },
        kek,
        dekRaw
      );

      const rewrapRes = await apiFetch("/vault/rewrap", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          kdf_name: "pbkdf2_sha256",
          kdf_iters: iters,
          kdf_salt_hex: bufToHex(salt.buffer),
          wrapped_dek_nonce_hex: bufToHex(nonce.buffer),
          wrapped_dek_hex: bufToHex(wrappedDek),
        }),
      });
      const rewrapData = await parseResponseJson(rewrapRes);
      if (!rewrapRes.ok) {
        throw new Error(rewrapData.detail || "No se pudo actualizar tu clave privada.");
      }

      closePurposeVaultChangePasswordModal();
      closePurposeVaultModal();
      openLifeProposalModal();
    } catch (err) {
      setPurposeVaultChangePasswordError(
        err?.message || "No se pudo modificar la contraseña privada."
      );
    }
  };

  const handlePurposeVaultReset = async () => {
    setPurposeVaultResetPasswordError("");
    const typed = (purposeVaultResetPasswordKeyword?.value || "").trim();
    if (!typed) {
      setPurposeVaultResetPasswordError("Debes escribir la palabra de confirmación.");
      return;
    }

    const allowed = purposeVaultResetKeywords
      ? Object.values(purposeVaultResetKeywords).map((value) => String(value).toUpperCase())
      : ["ELIMINAR", "DELETE", "SUPPRIMER"];

    if (!allowed.includes(typed.toUpperCase())) {
      setPurposeVaultResetPasswordError("La palabra de confirmación no coincide.");
      return;
    }

    try {
      const res = await apiFetch("/vault/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ confirm_keyword: typed }),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo restaurar tu clave privada.");
      }

      clearDekSession();

      closePurposeVaultResetPasswordFinalModal();
      closePurposeVaultResetPasswordModal();
      closePurposeVaultModal();
      window.location.href = "/create-private-key.html";
    } catch (err) {
      setPurposeVaultResetPasswordError(
        err?.message || "No se pudo restaurar tu clave privada."
      );
    }
  };

  const ensureVaultReadyForPurposeEditor = async () => {
    const token = getAccessToken();
    if (!token) {
      window.location.href = "/login.html";
      return false;
    }

    const sessionDek = getDekSessionHex();
    if (sessionDek && String(sessionDek).trim()) {
      return true;
    }

    const statusRes = await fetch(`${API}/vault/status`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const statusData = await parseResponseJson(statusRes);
    if (!statusRes.ok) {
      throw new Error(statusData.detail || "No se pudo verificar el estado de tu clave privada.");
    }
    if (!statusData?.has_vault) {
      window.location.href = "/create-private-key.html";
      return false;
    }

    openPurposeVaultModal();
    return false;
  };

  const unlockVaultForPurposeEditor = async () => {
    const password = (purposeVaultPassword?.value || "").trim();
    if (!password) {
      setPurposeVaultError("Debes digitar tu clave privada personal.");
      return;
    }

    const token = getAccessToken();
    if (!token) {
      window.location.href = "/login.html";
      return;
    }

    setPurposeVaultError("");
    try {
      await decryptDekFromPassword(password, token);
      closePurposeVaultModal();
      openLifeProposalModal();
    } catch (err) {
      if (err?.name === "OperationError" || String(err?.message || "").includes("OperationError")) {
        setPurposeVaultError("Contraseña incorrecta. Inténtalo de nuevo.");
      } else {
        setPurposeVaultError(err?.message || "No se pudo desbloquear tu clave privada personal.");
      }
    }
  };

  const handleEditPurposeClick = async () => {
    try {
      const ready = await ensureVaultReadyForPurposeEditor();
      if (ready) openLifeProposalModal();
    } catch (err) {
      openPurposeVaultModal(err?.message || "No se pudo validar la clave privada personal.");
    }
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

  const setPurposeFulfillError = (message) => {
    if (!purposeFulfillError) return;
    purposeFulfillError.textContent = message || "";
    purposeFulfillError.classList.toggle("is-visible", Boolean(message));
  };

  const syncPurposePublishChoice = () => {
    if (!purposePublishChoice) return;
    purposePublishChoice.querySelectorAll(".purpose-publish-btn").forEach((btn) => {
      const isSelected = btn.dataset.publish === purposePublishTo;
      btn.classList.toggle("is-selected", isSelected);
      btn.setAttribute("aria-pressed", isSelected ? "true" : "false");
    });
    if (purposeFulfillKeyRow) {
      const showKey = purposePublishTo === "private";
      purposeFulfillKeyRow.classList.toggle("hidden", !showKey);
      if (!showKey && purposeFulfillPassword) purposeFulfillPassword.value = "";
    }
  };

  const closePurposeFulfillModal = () => {
    if (!purposeFulfillOverlay) return;
    purposeFulfillOverlay.classList.add("hidden");
    purposeFulfillOverlay.setAttribute("aria-hidden", "true");
    if (purposeFulfillEvidence) purposeFulfillEvidence.value = "";
    if (purposeFulfillPassword) purposeFulfillPassword.value = "";
    setPurposeFulfillError("");
    activePurposeFulfillSlot = null;
    purposePublishTo = "private";
    syncPurposePublishChoice();
    if (purposeFulfillEvidenceUrl) {
      URL.revokeObjectURL(purposeFulfillEvidenceUrl);
      purposeFulfillEvidenceUrl = null;
    }
    if (purposeFulfillEvidenceImage) {
      purposeFulfillEvidenceImage.remove();
      purposeFulfillEvidenceImage = null;
    }
    if (purposeFulfillEvidencePreview) {
      purposeFulfillEvidencePreview.classList.remove("has-image");
      const placeholder = purposeFulfillEvidencePreview.querySelector(".wish-preview-placeholder");
      const nameEl = purposeFulfillEvidencePreview.querySelector(".wish-preview-name");
      if (placeholder) placeholder.textContent = "Sube la evidencia visual.";
      if (nameEl) nameEl.textContent = "PNG, WEBP, JPEG, etc.";
    }
    updateModalScrollLock();
  };

  const openPurposeFulfillModal = (slotNumber) => {
    if (!purposeFulfillOverlay) return;
    const slotMap = getPurposeSlotMap(purposeSlots);
    const slotData = slotMap.get(slotNumber);
    if (!slotData) {
      window.alert("Primero define este propósito antes de marcarlo como cumplido.");
      return;
    }
    if (String(slotData.status || "active") === "fulfilled") return;

    activePurposeFulfillSlot = slotNumber;
    purposePublishTo = "private";
    syncPurposePublishChoice();
    setPurposeFulfillError("");
    if (purposeFulfillEvidence) purposeFulfillEvidence.value = "";
    if (purposeFulfillPassword) purposeFulfillPassword.value = "";

    if (purposeFulfillEvidenceUrl) {
      URL.revokeObjectURL(purposeFulfillEvidenceUrl);
      purposeFulfillEvidenceUrl = null;
    }
    if (purposeFulfillEvidenceImage) {
      purposeFulfillEvidenceImage.remove();
      purposeFulfillEvidenceImage = null;
    }
    if (purposeFulfillEvidencePreview) {
      purposeFulfillEvidencePreview.classList.remove("has-image");
      const placeholder = purposeFulfillEvidencePreview.querySelector(".wish-preview-placeholder");
      const nameEl = purposeFulfillEvidencePreview.querySelector(".wish-preview-name");
      if (placeholder) placeholder.textContent = "Sube la evidencia visual.";
      if (nameEl) nameEl.textContent = "PNG, WEBP, JPEG, etc.";
    }

    purposeFulfillOverlay.classList.remove("hidden");
    purposeFulfillOverlay.setAttribute("aria-hidden", "false");
    updateModalScrollLock();
    if (purposeFulfillPassword) purposeFulfillPassword.focus();
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

  const decryptDekRawFromPassword = async (privatePassword, token) => {
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
    setDekSessionHex(bufToHex(dekRaw));
    return dekRaw;
  };

  const decryptDekFromPassword = async (privatePassword, token) => {
    const dekRaw = await decryptDekRawFromPassword(privatePassword, token);
    return crypto.subtle.importKey("raw", dekRaw, { name: "AES-GCM" }, false, ["encrypt", "decrypt"]);
  };

  const importDekFromSession = async () => {
    const dekHex = getDekSessionHex();
    if (!dekHex) {
      throw new Error("Digita tu clave privada personal para confirmar tu decisión.");
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

  const aesGcmEncryptText = async (key, text, aadBuf) => {
    const nonce = crypto.getRandomValues(new Uint8Array(12));
    const ciphertext = await crypto.subtle.encrypt(
      { name: "AES-GCM", iv: nonce, additionalData: aadBuf },
      key,
      new TextEncoder().encode(text)
    );
    return { nonce, ciphertext };
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
      closePurposeUnlockModal();
    } catch (err) {
      purposeUnlockError.textContent = err?.message || "No se pudo desbloquear el deseo.";
      purposeUnlockError.classList.add("is-visible");
    }
  };

  const resolveImageContentType = (file) => {
    if (file?.type && file.type.startsWith("image/")) return file.type;
    const name = String(file?.name || "").toLowerCase();
    if (name.endsWith(".webp")) return "image/webp";
    if (name.endsWith(".png")) return "image/png";
    if (name.endsWith(".jpg") || name.endsWith(".jpeg")) return "image/jpeg";
    if (name.endsWith(".gif")) return "image/gif";
    return "";
  };

  const presignEncryptedUpload = async (file) => {
    const contentType = resolveImageContentType(file);
    if (!contentType) {
      throw new Error("Tipo de imagen no reconocido. Usa WEBP, PNG o JPEG.");
    }

    // AES-GCM adds 16 bytes tag; we also prefix 12 bytes nonce => +28 bytes total.
    const sizeBytes = Number(file.size || 0) + 28;

    const res = await apiFetch("/media/presign/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        filename: file.name,
        content_type: contentType,
        size_bytes: sizeBytes,
        visibility: "private",
        obfuscate_owner: true,
      }),
    });
    const data = await parseResponseJson(res);
    if (!res.ok) {
      throw new Error(data.detail || "No se pudo preparar la carga cifrada.");
    }
    return { ...data, contentType };
  };

  const uploadEncryptedMediaFile = async (file) => {
    if (!file) return null;

    const dekKey = await importDekFromSession();
    const presign = await presignEncryptedUpload(file);
    const mediaId = Number(presign.media_id || 0);
    if (!Number.isFinite(mediaId) || mediaId <= 0) {
      throw new Error("No se pudo preparar la carga (media_id inválido).");
    }

    const aad = new TextEncoder().encode(`${PRIVATE_MEDIA_AAD_PREFIX}${mediaId}`);
    const nonce = crypto.getRandomValues(new Uint8Array(12));
    const plaintextBuf = await file.arrayBuffer();
    const encryptedBuf = await crypto.subtle.encrypt(
      { name: "AES-GCM", iv: nonce, additionalData: aad },
      dekKey,
      plaintextBuf
    );

    const combined = new Uint8Array(nonce.byteLength + encryptedBuf.byteLength);
    combined.set(nonce, 0);
    combined.set(new Uint8Array(encryptedBuf), nonce.byteLength);

    const formData = new FormData();
    formData.append("media_id", `${mediaId}`);
    formData.append(
      "file",
      new Blob([combined], { type: presign.contentType }),
      file.name
    );

    const uploadRes = await apiFetch("/media/upload/proxy", {
      method: "POST",
      body: formData,
    });
    const uploadData = await parseResponseJson(uploadRes);
    if (!uploadRes.ok) {
      throw new Error(uploadData.detail || "No se pudo subir la imagen cifrada.");
    }

    return {
      media_id: mediaId,
      mime_type: presign.contentType,
      original_filename: file.name,
    };
  };

  const uploadPublicMediaFile = async (file) => {
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
      throw new Error(data.detail || "No se pudo subir la imagen.");
    }
    return data;
  };

  const updatePurposeFulfillEvidencePreview = (file) => {
    if (!purposeFulfillEvidencePreview) return;

    const previewPlaceholder = purposeFulfillEvidencePreview.querySelector(".wish-preview-placeholder");
    const previewName = purposeFulfillEvidencePreview.querySelector(".wish-preview-name");

    if (purposeFulfillEvidenceUrl) {
      URL.revokeObjectURL(purposeFulfillEvidenceUrl);
      purposeFulfillEvidenceUrl = null;
    }

    if (!file) {
      purposeFulfillEvidencePreview.classList.remove("has-image");
      if (purposeFulfillEvidenceImage) {
        purposeFulfillEvidenceImage.remove();
        purposeFulfillEvidenceImage = null;
      }
      if (previewPlaceholder) previewPlaceholder.textContent = "Sube la evidencia visual.";
      if (previewName) previewName.textContent = "PNG, WEBP, JPEG, etc.";
      return;
    }

    purposeFulfillEvidenceUrl = URL.createObjectURL(file);
    purposeFulfillEvidencePreview.classList.add("has-image");
    if (!purposeFulfillEvidenceImage) {
      purposeFulfillEvidenceImage = document.createElement("img");
      purposeFulfillEvidenceImage.className = "wish-preview-image";
      purposeFulfillEvidenceImage.alt = "Evidencia seleccionada";
      purposeFulfillEvidencePreview.insertBefore(
        purposeFulfillEvidenceImage,
        purposeFulfillEvidencePreview.firstChild
      );
    }
    purposeFulfillEvidenceImage.src = purposeFulfillEvidenceUrl;
    if (previewPlaceholder) previewPlaceholder.textContent = "";
    if (previewName) previewName.textContent = file.name || "Evidencia seleccionada";
  };

  const resolvePurposePlainText = async (slotData) => {
    if (!slotData) return "";
    if (!slotData.is_private) {
      return slotData.text_public || slotData.text_input || "";
    }
    if (slotData.text_input) return slotData.text_input;
    if (slotData.ciphertext_hex && slotData.nonce_hex) {
      const dekKey = await importDekFromSession();
      return await aesGcmDecryptText(dekKey, slotData.ciphertext_hex, slotData.nonce_hex, AAD_PURPOSE);
    }
    return "";
  };

  const fulfillPurposeSlot = async () => {
    if (!activePurposeFulfillSlot) return;
    if (purposeFulfillBusy) return;
    if (!purposeFulfillConfirm) return;

    const slotNumber = Number(activePurposeFulfillSlot || 0);
    if (!slotNumber) return;

    const slotMap = getPurposeSlotMap(purposeSlots);
    const slotData = slotMap.get(slotNumber);
    if (!slotData) {
      setPurposeFulfillError("No se encontró el propósito. Intenta recargar la página.");
      return;
    }

    purposeFulfillBusy = true;
    purposeFulfillConfirm.disabled = true;
    setPurposeFulfillError("");

    try {
      let dekKey = null;
      if (purposePublishTo === "private") {
        const password = (purposeFulfillPassword?.value || "").trim();
        if (!password) {
          throw new Error("Digita tu clave privada personal para confirmar tu decisión.");
        }
        const token = getAccessToken();
        if (!token) {
          throw new Error("No hay sesión activa.");
        }
        try {
          dekKey = await decryptDekFromPassword(password, token);
        } catch (err) {
          if (err?.name === "OperationError" || String(err?.message || "").includes("OperationError")) {
            throw new Error("Clave privada personal incorrecta.");
          }
          throw err;
        }
        if (purposeFulfillPassword) purposeFulfillPassword.value = "";
      }

      const wishText = (await resolvePurposePlainText(slotData)).trim();
      if (!wishText) {
        throw new Error("Primero define el texto de este propósito para poder publicarlo.");
      }

      const file = purposeFulfillEvidence && purposeFulfillEvidence.files ? purposeFulfillEvidence.files[0] : null;
      const evidence = file
        ? (purposePublishTo === "public" ? await uploadPublicMediaFile(file) : await uploadEncryptedMediaFile(file))
        : null;
      const evidenceMediaId = Number(evidence?.media_id || 0) || null;

      if (purposePublishTo === "public") {
        const res = await apiFetch("/life-purpose/fulfill", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            slot_number: slotNumber,
            publish_to: "public",
            evidence_media_id: evidenceMediaId,
            wish_text: wishText,
            wish_type: "Espiritual",
          }),
        });
        const data = await parseResponseJson(res);
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo publicar el deseo.");
        }

        purposeSlots = purposeSlots.map((slot) => {
          if (Number(slot.slot_number) !== slotNumber) return slot;
          return {
            ...slot,
            is_private: false,
            reveal_at: null,
            icon_key: null,
            text_public: null,
            text_input: "",
            ciphertext_hex: null,
            nonce_hex: null,
            status: "fulfilled"
          };
        });
      } else {
        const dekKey = await importDekFromSession();
        const privatePayload = {
          wish_text: wishText,
          wish_type: "Espiritual",
          from_life_purpose: true,
          life_purpose_slot_number: slotNumber,
          life_purpose_icon_key: slotData.icon_key || null,
        };
        const { nonce, ciphertext } = await aesGcmEncryptText(
          dekKey,
          JSON.stringify(privatePayload),
          AAD_PRIVATE_WISH
        );

        const res = await apiFetch("/life-purpose/fulfill", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            slot_number: slotNumber,
            publish_to: "private",
            evidence_media_id: evidenceMediaId,
            ciphertext_hex: bufToHex(ciphertext),
            nonce_hex: bufToHex(nonce.buffer),
          }),
        });
        const data = await parseResponseJson(res);
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo publicar el deseo.");
        }

        purposeSlots = purposeSlots.map((slot) => {
          if (Number(slot.slot_number) !== slotNumber) return slot;
          return {
            ...slot,
            is_private: false,
            reveal_at: null,
            icon_key: null,
            text_public: null,
            text_input: "",
            ciphertext_hex: null,
            nonce_hex: null,
            status: "fulfilled"
          };
        });
      }

      const publishedScope = purposePublishTo;
      renderPurposeSlots(purposeSlots);
      closePurposeFulfillModal();

      window.dispatchEvent(new CustomEvent("kiadez:fulfilled-wishes-changed", {
        detail: { scope: publishedScope }
      }));
    } catch (err) {
      setPurposeFulfillError(err?.message || "No se pudo publicar el deseo.");
    } finally {
      purposeFulfillBusy = false;
      purposeFulfillConfirm.disabled = false;
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

    try {
      const res = await apiFetch("/life-purpose/save", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ slots }),
      });
      const payload = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(payload?.detail || "No se pudieron guardar los propósitos.");
      }

      purposeSlots = localSlots
        .map((slot) => normalizePurposeSlot(slot, Number(slot.slot_number)))
        .sort((a, b) => a.slot_number - b.slot_number);
      renderPurposeSlots(purposeSlots);
      closeLifeProposalModal();
    } catch (err) {
      const message = err?.message || "No se pudieron guardar los propósitos.";
      groups.forEach((groupEl) => {
        setPurposeStatus(groupEl, message);
      });
    }
  });

  btnEditPurposes?.addEventListener("click", () => {
    void handleEditPurposeClick();
  });
  lifeProposalClose?.addEventListener("click", closeLifeProposalModal);
  lifeProposalCloseFooter?.addEventListener("click", closeLifeProposalModal);
  lifeProposalOverlay?.addEventListener("click", (event) => {
    if (event.target === lifeProposalOverlay) closeLifeProposalModal();
  });

  purposeVaultCancel?.addEventListener("click", closePurposeVaultModal);
  purposeVaultOverlay?.addEventListener("click", (event) => {
    if (event.target === purposeVaultOverlay) closePurposeVaultModal();
  });
  purposeVaultUnlock?.addEventListener("click", () => void unlockVaultForPurposeEditor());
  purposeVaultPassword?.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      void unlockVaultForPurposeEditor();
    }
  });
  purposeVaultChangePasswordBtn?.addEventListener("click", openPurposeVaultChangePasswordModal);
  purposeVaultResetPasswordBtn?.addEventListener("click", openPurposeVaultResetPasswordModal);

  purposeVaultChangePasswordCancel?.addEventListener("click", closePurposeVaultChangePasswordModal);
  purposeVaultChangePasswordCancelFooter?.addEventListener("click", closePurposeVaultChangePasswordModal);
  purposeVaultChangePasswordModal?.addEventListener("click", (event) => {
    if (event.target === purposeVaultChangePasswordModal) closePurposeVaultChangePasswordModal();
  });
  purposeVaultChangePasswordConfirm?.addEventListener("click", () => void handlePurposeVaultChangePassword());
  [purposeVaultCurrentPassword, purposeVaultNewPassword, purposeVaultConfirmPassword].forEach((input) => {
    input?.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        void handlePurposeVaultChangePassword();
      }
    });
  });

  purposeVaultResetPasswordCancel?.addEventListener("click", closePurposeVaultResetPasswordModal);
  purposeVaultResetPasswordCancelFooter?.addEventListener("click", closePurposeVaultResetPasswordModal);
  purposeVaultResetPasswordModal?.addEventListener("click", (event) => {
    if (event.target === purposeVaultResetPasswordModal) closePurposeVaultResetPasswordModal();
  });
  purposeVaultResetPasswordConfirm?.addEventListener("click", () => {
    closePurposeVaultResetPasswordModal();
    openPurposeVaultResetPasswordFinalModal();
  });

  purposeVaultResetPasswordFinalCancel?.addEventListener("click", closePurposeVaultResetPasswordFinalModal);
  purposeVaultResetPasswordFinalCancelFooter?.addEventListener("click", closePurposeVaultResetPasswordFinalModal);
  purposeVaultResetPasswordFinalModal?.addEventListener("click", (event) => {
    if (event.target === purposeVaultResetPasswordFinalModal) closePurposeVaultResetPasswordFinalModal();
  });
  purposeVaultResetPasswordFinalConfirm?.addEventListener("click", () => void handlePurposeVaultReset());
  purposeVaultResetPasswordKeyword?.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      void handlePurposeVaultReset();
    }
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

  purposeFulfillClose?.addEventListener("click", closePurposeFulfillModal);
  purposeFulfillCancel?.addEventListener("click", closePurposeFulfillModal);
  purposeFulfillOverlay?.addEventListener("click", (event) => {
    if (event.target === purposeFulfillOverlay) closePurposeFulfillModal();
  });
  purposePublishChoice?.addEventListener("click", (event) => {
    const btn = event.target.closest(".purpose-publish-btn");
    if (!btn) return;
    const next = btn.dataset.publish;
    if (next !== "private" && next !== "public") return;
    purposePublishTo = next;
    setPurposeFulfillError("");
    syncPurposePublishChoice();
    if (purposePublishTo === "private" && purposeFulfillPassword) {
      purposeFulfillPassword.focus();
    }
  });
  purposeFulfillEvidence?.addEventListener("change", () => {
    const file = purposeFulfillEvidence.files && purposeFulfillEvidence.files[0];
    updatePurposeFulfillEvidencePreview(file || null);
  });
  purposeFulfillConfirm?.addEventListener("click", () => void fulfillPurposeSlot());

  purposeFulfillBtns.forEach((btn) => {
    if (btn.dataset.bound === "true") return;
    btn.dataset.bound = "true";
    btn.addEventListener("click", () => {
      const slotNumber = Number(btn.dataset.slot || "0");
      if (!slotNumber) return;
      openPurposeFulfillModal(slotNumber);
    });
  });

  void loadPurposeSlots();

  return () => {};
};
