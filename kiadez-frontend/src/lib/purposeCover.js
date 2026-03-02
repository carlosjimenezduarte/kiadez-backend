import { clearDekSession, getDekSessionHex, setDekSessionHex } from "./dekSession";
import { getLocale } from "./i18n";

const API = "http://127.0.0.1:8000";
const AAD_PURPOSE = new TextEncoder().encode("kiadez-life-purpose-v1");
const AAD_VAULT = new TextEncoder().encode("kiadez-vault-v1");
const AAD_PRIVATE_WISH = new TextEncoder().encode("kiadez-private-wish-v1");
const PRIVATE_MEDIA_AAD_PREFIX = "kiadez-private-media-v1:";

const normalizeLocaleCode = (value) => {
  const raw = String(value || "").trim().toLowerCase();
  if (!raw) return null;
  if (raw.startsWith("es")) return "es";
  if (raw.startsWith("en")) return "en";
  if (raw.startsWith("fr")) return "fr";
  return null;
};

const localeFromUrl = () => {
  if (typeof window === "undefined") return null;
  try {
    const params = new URLSearchParams(window.location.search);
    return normalizeLocaleCode(params.get("lang"));
  } catch {
    return null;
  }
};

const localeFromStorage = () => {
  if (typeof window === "undefined") return null;
  try {
    return normalizeLocaleCode(window.localStorage.getItem("kiadez_locale"));
  } catch {
    return null;
  }
};

const resolvePurposeLocale = () => {
  const urlLocale = localeFromUrl();
  if (urlLocale) return urlLocale;

  const storageLocale = localeFromStorage();
  if (storageLocale === "es" || storageLocale === "fr") return storageLocale;

  const i18nLocale = normalizeLocaleCode(getLocale());
  if (i18nLocale === "es" || i18nLocale === "fr") return i18nLocale;
  return "es";
};

const locale = resolvePurposeLocale();
const isEn = locale === "en";
const isFr = locale === "fr";
const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);
const PURPOSE_PREFIX = tr("Deseo ", "Wish ", "Souhait ");
const LEGACY_PURPOSE_PREFIXES = ["Wish ", "Deseo ", "Souhait "];
const PURPOSE_SECRET_TEXT = tr(
  "Deseo marcado como secreto",
  "Wish marked as secret",
  "Souhait marqué comme secret",
);
const PURPOSE_UNDEFINED_TEXT = tr(
  "Deseo de propósito sin definir",
  "Undefined purpose wish",
  "Souhait de finalité non défini",
);
const PURPOSE_REVEAL_PREFIX = tr(
  "Este deseo se revelará",
  "This wish will be revealed",
  "Ce souhait sera révélé",
);
const COVER_DEFAULT_IMAGE = "/assets/cover-default.jpg";
const TXT_EDIT_COVER = tr(
  "Editar imagen de portada",
  "Edit cover image",
  "Modifier l'image de couverture",
);
const TXT_UPLOAD_IMAGE = tr("Subir imagen", "Upload image", "Téléverser une image");
const TXT_MOVE_IMAGE = tr("Mover imagen", "Move image", "Déplacer l'image");
const TXT_SAVE_CHANGES = tr("Guardar cambios", "Save changes", "Enregistrer les modifications");
const TXT_CANCEL = tr("Cancelar", "Cancel", "Annuler");
const TXT_EDIT_LIFE_PURPOSE = tr(
  "Editar mi propósito de vida",
  "Edit my life purpose",
  "Modifier mon objectif de vie",
);
const TXT_PURPOSE_WISHES = tr(
  "Deseos de propósito",
  "Purpose wishes",
  "Souhaits de finalité",
);
const TXT_MARK_FULFILLED = tr(
  "Marcar deseo {slot} como cumplido",
  "Mark wish {slot} as fulfilled",
  "Marquer le souhait {slot} comme accompli",
);
const TXT_UNLOCK_WISH = tr(
  "Desbloquear deseo {slot}",
  "Unlock wish {slot}",
  "Déverrouiller le souhait {slot}",
);
const TXT_DEFINE_FIRST = tr(
  "Define primero este deseo antes de marcarlo como cumplido.",
  "Define this purpose first before marking it as fulfilled.",
  "Définis d'abord ce souhait avant de le marquer comme accompli.",
);
const TXT_PURPOSE_FULFILLED_HINT = tr(
  "Deseo cumplido. Define uno nuevo desde Editar mi propósito de vida.",
  "Purpose fulfilled. Define a new one from Edit my life purpose.",
  "Souhait accompli. Définis-en un nouveau depuis Modifier mon objectif de vie.",
);
const TXT_STATUS_PUBLIC_DEFAULT = tr(
  "Estado: público por defecto.",
  "Status: public by default.",
  "Statut : public par défaut.",
);
const TXT_STATUS_SECRET = tr(
  "Estado: marcado como secreto.",
  "Status: marked as secret.",
  "Statut : marqué comme secret.",
);
const TXT_STATUS_CONFIRMED_PUBLIC = tr(
  "Estado: confirmado (público).",
  "Status: confirmed (public).",
  "Statut : confirmé (public).",
);
const TXT_STATUS_ICON_ASSOCIATED = tr(
  "Estado: ícono asociado: {label}.",
  "Status: icon associated: {label}.",
  "Statut : icône associée : {label}.",
);
const TXT_ICON_SELECTED = tr(
  "Ícono: {label}",
  "Icon: {label}",
  "Icône : {label}",
);
const TXT_STATUS_REVEAL_ON = tr(
  "Estado: se revelará el {date}.",
  "Status: will be revealed on {date}.",
  "Statut : sera révélé le {date}.",
);
const TXT_COMPLETE_BEFORE_SAVING = tr(
  "Completa este propósito antes de guardar.",
  "Complete this purpose before saving.",
  "Complète cet objectif avant d'enregistrer.",
);
const TXT_SAVE_PURPOSE = tr(
  "Guardar propósito",
  "Save purpose",
  "Enregistrer l'objectif",
);
const TXT_BACK = tr("Volver", "Back", "Retour");
const TXT_CONFIRM = tr("Confirmar", "Confirm", "Confirmer");
const TXT_UNLOCK = tr("Desbloquear", "Unlock", "Déverrouiller");
const TXT_PRIVATE = tr("Privado", "Private", "Privé");
const TXT_PUBLIC = tr("Público", "Public", "Public");
const TXT_UPLOAD_VISUAL_EVIDENCE = tr(
  "Sube evidencia visual.",
  "Upload visual evidence.",
  "Téléverse une preuve visuelle.",
);
const TXT_CHOOSE_ICON = tr("Elegir ícono", "Choose icon", "Choisir l'icône");
const TXT_MARK_FULFILLED_WISH = tr(
  "Marcar deseo cumplido",
  "Mark fulfilled wish",
  "Marquer le souhait comme accompli",
);
const TXT_UNLOCK_SECRET_WISH = tr(
  "Desbloquear deseo secreto",
  "Unlock secret wish",
  "Déverrouiller le souhait secret",
);
const TXT_SELECTED_EVIDENCE = tr(
  "Evidencia seleccionada",
  "Selected evidence",
  "Preuve sélectionnée",
);
const TXT_PNG_TYPES = "PNG, WEBP, JPEG, etc.";
const TXT_ERR_NO_ACTIVE_SESSION = tr(
  "No hay sesión activa.",
  "There is no active session.",
  "Aucune session active.",
);
const TXT_ERR_SESSION_EXPIRED = tr(
  "Sesión expirada. Inicia sesión de nuevo.",
  "Session expired. Sign in again.",
  "Session expirée. Connecte-toi de nouveau.",
);
const TXT_ERR_COULD_NOT_UPLOAD_COVER = tr(
  "No se pudo subir la portada.",
  "Could not upload the cover.",
  "Impossible de téléverser la couverture.",
);
const TXT_ERR_COULD_NOT_SAVE_COVER = tr(
  "No se pudo guardar la portada.",
  "Could not save the cover.",
  "Impossible d'enregistrer la couverture.",
);
const TXT_ERR_COULD_NOT_READ_VAULT = tr(
  "No se pudo leer la bóveda.",
  "Could not read the vault.",
  "Impossible de lire le coffre.",
);
const TXT_ERR_ENTER_PRIVATE_KEY = tr(
  "Debes ingresar tu clave privada personal.",
  "You must enter your personal private key.",
  "Tu dois saisir ta clé privée personnelle.",
);
const TXT_ERR_INVALID_PRIVATE_KEY = tr(
  "Clave privada incorrecta. Intenta nuevamente.",
  "Incorrect password. Try again.",
  "Mot de passe incorrect. Réessaie.",
);
const TXT_ERR_NO_ENCRYPTED_DATA = tr(
  "No hay datos cifrados para este deseo.",
  "There is no encrypted data for this wish.",
  "Il n'y a pas de données chiffrées pour ce souhait.",
);
const TXT_ERR_COULD_NOT_REVEAL_WISH = tr(
  "No se pudo revelar el deseo.",
  "Could not reveal the wish.",
  "Impossible de révéler le souhait.",
);
const TXT_ERR_COULD_NOT_UNLOCK_WISH = tr(
  "No se pudo desbloquear el deseo.",
  "Could not unlock the wish.",
  "Impossible de déverrouiller le souhait.",
);
const TXT_ERR_PURPOSE_NOT_FOUND = tr(
  "No se encontró el propósito. Intenta recargar la página.",
  "Purpose not found. Try reloading the page.",
  "Objectif introuvable. Essaie de recharger la page.",
);
const TXT_ERR_DEFINE_TEXT_FIRST = tr(
  "Define primero el texto de este propósito antes de publicarlo.",
  "Define this purpose text first before publishing it.",
  "Définis d'abord le texte de cet objectif avant de le publier.",
);
const TXT_ERR_COULD_NOT_PUBLISH_WISH = tr(
  "No se pudo publicar el deseo.",
  "Could not publish the wish.",
  "Impossible de publier le souhait.",
);
const TXT_ERR_COULD_NOT_VERIFY_VAULT = tr(
  "No se pudo verificar el estado de tu clave privada.",
  "Could not verify your private key status.",
  "Impossible de vérifier l'état de ta clé privée.",
);
const TXT_ERR_COULD_NOT_VALIDATE_PRIVATE_KEY = tr(
  "No se pudo validar la clave privada personal.",
  "Could not validate the personal private key.",
  "Impossible de valider la clé privée personnelle.",
);
const TXT_ERR_CONFIRM_WORD_REQUIRED = tr(
  "Debes escribir la palabra de confirmación.",
  "You must write the confirmation word.",
  "Tu dois écrire le mot de confirmation.",
);
const TXT_ERR_CONFIRM_WORD_MISMATCH = tr(
  "La palabra de confirmación no coincide.",
  "Confirmation word does not match.",
  "Le mot de confirmation ne correspond pas.",
);
const TXT_ERR_COULD_NOT_RESTORE_PRIVATE_KEY = tr(
  "No se pudo restaurar tu clave privada.",
  "Could not restore your private key.",
  "Impossible de restaurer ta clé privée.",
);
const TXT_ERR_COULD_NOT_CHANGE_PRIVATE_PASSWORD = tr(
  "No se pudo cambiar la clave privada.",
  "Could not change the private password.",
  "Impossible de changer le mot de passe privé.",
);
const TXT_ERR_CURRENT_PRIVATE_REQUIRED = tr(
  "Debes ingresar tu clave privada actual.",
  "You must enter your current private password.",
  "Tu dois saisir ton mot de passe privé actuel.",
);
const TXT_ERR_NEW_PRIVATE_MIN = tr(
  "Tu nueva clave debe tener al menos 8 caracteres.",
  "Your new key must be at least 8 characters long.",
  "Ta nouvelle clé doit contenir au moins 8 caractères.",
);
const TXT_ERR_NEW_PRIVATE_CONFIRM = tr(
  "La confirmación no coincide con tu nueva clave.",
  "Confirmation does not match your new key.",
  "La confirmation ne correspond pas à ta nouvelle clé.",
);
const TXT_ERR_COULD_NOT_UPDATE_PRIVATE_KEY = tr(
  "No se pudo actualizar tu clave privada.",
  "Could not update your private key.",
  "Impossible de mettre à jour ta clé privée.",
);
const TXT_ERR_COULD_NOT_UNLOCK_VAULT = tr(
  "No se pudo desbloquear tu clave privada personal.",
  "Could not unlock your personal private key.",
  "Impossible de déverrouiller ta clé privée personnelle.",
);
const TXT_ERR_COULD_NOT_UNLOCK_VAULT_GENERIC = tr(
  "No se pudo desbloquear la bóveda.",
  "Could not unlock the vault.",
  "Impossible de déverrouiller le coffre.",
);
const TXT_ERR_COULD_NOT_SAVE_PURPOSES = tr(
  "No se pudieron guardar los propósitos.",
  "Could not save purposes.",
  "Impossible d'enregistrer les objectifs.",
);

const DEFAULT_PURPOSE_TEXT = {
  1: tr("Deseo #1: Secreto", "Wish #1: Secret", "Souhait n°1 : Secret"),
  2: tr(
    "Deseo construir el Reino de Combray",
    "I wish to build the Kingdom of Combray",
    "Je souhaite construire le Royaume de Combray",
  ),
  3: tr(
    "Deseo estar unido a Jesús",
    "I wish to be united with Jesus",
    "Je souhaite être uni à Jésus",
  ),
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
  const legacyPrefix = LEGACY_PURPOSE_PREFIXES.find((prefix) =>
    trimmed.startsWith(prefix),
  );
  if (legacyPrefix) {
    const rest = trimmed.slice(legacyPrefix.length).trim();
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
      <summary class="icon-btn" id="btnChangeCover" title="${TXT_EDIT_COVER}">${TXT_EDIT_COVER}</summary>
      <div class="cover-menu-panel">
        <button class="cover-menu-item" type="button" id="coverUpload">${TXT_UPLOAD_IMAGE}</button>
        <button class="cover-menu-item" type="button" id="coverMove">${TXT_MOVE_IMAGE}</button>
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
    coverSummary.textContent = TXT_EDIT_COVER;
    coverSummary.title = TXT_EDIT_COVER;
  }

  const coverSelectExisting = coverMenu.querySelector("#coverSelectExisting");
  if (coverSelectExisting) {
    coverSelectExisting.remove();
  }
  if (!coverMenu.querySelector("#coverUpload")) {
    const panel = coverMenu.querySelector(".cover-menu-panel");
    panel?.insertAdjacentHTML("beforeend", `
      <button class="cover-menu-item" type="button" id="coverUpload">${TXT_UPLOAD_IMAGE}</button>
    `);
  }
  if (!coverMenu.querySelector("#coverMove")) {
    const panel = coverMenu.querySelector(".cover-menu-panel");
    panel?.insertAdjacentHTML("beforeend", `
      <button class="cover-menu-item" type="button" id="coverMove">${TXT_MOVE_IMAGE}</button>
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
      <button class="btn btn-primary btn-compact" type="button" id="coverSaveBtn">${TXT_SAVE_CHANGES}</button>
      <button class="btn btn-outline btn-compact" type="button" id="coverCancelBtn">${TXT_CANCEL}</button>
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
    if (!token) throw new Error(TXT_ERR_NO_ACTIVE_SESSION);

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
      throw new Error(data?.detail || TXT_ERR_COULD_NOT_UPLOAD_COVER);
    }
    const mediaId = Number(data?.media_id || 0) || null;
    if (!mediaId) {
      throw new Error("No media_id was received for the cover.");
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
        throw new Error(data?.detail || TXT_ERR_COULD_NOT_SAVE_COVER);
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
      window.alert(error?.message || TXT_ERR_COULD_NOT_SAVE_COVER);
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
        <div class="modal modal-wide life-proposal-modal" role="dialog" aria-modal="true" aria-label="${tr("Propósito de vida", "Life purpose", "Objectif de vie")}">
          <div class="modal-head">
            <h3>${tr("Propósito de vida", "Life purpose", "Objectif de vie")}</h3>
            <button class="modal-close" type="button" id="lifeProposalClose">✕</button>
          </div>
          <div class="modal-body life-proposal-body">
            <div class="auth-card auth-card--wide auth-card--life life-proposal-card">
              <h2 class="auth-title">${tr("Tu propósito de vida", "Your life purpose", "Ton objectif de vie")}</h2>
              <div class="auth-message">
                <p>
                  ${tr("Escribe tres deseos que orienten tu camino.", "Write three wishes that guide your path.", "Écris trois souhaits qui orientent ton chemin.")}
                  <br>
                  ${tr("Son una brújula, no una presión.", "They are a compass, not pressure.", "Ils sont une boussole, pas une pression.")}
                </p>
                <p class="muted">
                  ${tr("Estos propósitos se almacenan cifrados con tu clave privada personal.", "These purposes are stored encrypted with your personal private key.", "Ces objectifs sont stockés chiffrés avec ta clé privée personnelle.")}
                </p>
              </div>
              <form id="life-form">
                ${[1, 2, 3].map((slot) => `
                  <div class="purpose-group" data-purpose="${slot}">
                    <textarea id="p${slot}" class="wish-prefix-input" data-prefix="${PURPOSE_PREFIX}" rows="1" maxlength="80" placeholder="${tr("Deseo " + slot, "Wish " + slot, "Souhait " + slot)}" required>${PURPOSE_PREFIX}</textarea>
                    <div class="purpose-actions" role="group" aria-label="${tr("Acciones para el propósito " + slot, "Actions for purpose " + slot, "Actions pour l'objectif " + slot)}">
                      <button type="button" class="purpose-action" data-action="confirm" title="${tr("Confirmar deseo de propósito", "Confirm purpose wish", "Confirmer le souhait")}" aria-label="${tr("Confirmar deseo de propósito", "Confirm purpose wish", "Confirmer le souhait")}">
                        <img src="/css/icons/iconsave.webp" alt="${tr("Guardar propósito", "Save purpose", "Enregistrer l'objectif")}">
                      </button>
                      <button type="button" class="purpose-action" data-action="secret" title="${tr("Marcar como secreto", "Mark as secret", "Marquer comme secret")}" aria-label="${tr("Marcar como secreto", "Mark as secret", "Marquer comme secret")}">
                        <img src="/css/icons/iconkey.webp" alt="${tr("Marcar como secreto", "Mark as secret", "Marquer comme secret")}">
                      </button>
                      <button type="button" class="purpose-action" data-action="reveal" title="${tr("Revelar en fecha", "Reveal on date", "Révéler à la date")}" aria-label="${tr("Revelar en fecha", "Reveal on date", "Révéler à la date")}">
                        <img src="/css/icons/iconcalendar.webp" alt="${tr("Programar fecha", "Schedule date", "Planifier la date")}">
                      </button>
                      <button type="button" class="purpose-action" data-action="icon" title="${tr("Elegir ícono", "Choose icon", "Choisir l'icône")}" aria-label="${tr("Elegir ícono", "Choose icon", "Choisir l'icône")}">
                        <img src="/css/icons/iconelemental.webp" alt="${tr("Elegir ícono", "Choose icon", "Choisir l'icône")}">
                      </button>
                    </div>
                    <input type="date" class="purpose-date" aria-label="${tr("Fecha de revelación para propósito " + slot, "Reveal date for purpose " + slot, "Date de révélation pour l'objectif " + slot)}">
                    <div class="purpose-icon-panel" aria-label="${tr("Selector de íconos", "Icon selector", "Sélecteur d'icônes")}">
                      <button type="button" class="purpose-icon" data-icon="air" title="${tr("Aire", "Air", "Air")}"><img src="assets/air.png" alt="${tr("Aire", "Air", "Air")}"></button>
                      <button type="button" class="purpose-icon" data-icon="earth" title="${tr("Tierra", "Earth", "Terre")}"><img src="assets/earth.png" alt="${tr("Tierra", "Earth", "Terre")}"></button>
                      <button type="button" class="purpose-icon" data-icon="water" title="${tr("Agua", "Water", "Eau")}"><img src="assets/water.png" alt="${tr("Agua", "Water", "Eau")}"></button>
                      <button type="button" class="purpose-icon" data-icon="fire" title="${tr("Fuego", "Fire", "Feu")}"><img src="assets/fire.png" alt="${tr("Fuego", "Fire", "Feu")}"></button>
                    </div>
                    <div class="purpose-status" aria-live="polite">${TXT_STATUS_PUBLIC_DEFAULT}</div>
                  </div>
                `).join("")}
                <button type="submit" class="btn btn-primary">${TXT_SAVE_PURPOSE}</button>
                <button type="button" class="btn btn-outline" id="lifeProposalCloseFooter">${TXT_BACK}</button>
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
        <div class="modal" role="dialog" aria-modal="true" aria-label="${tr("Confirmar propósito público", "Confirm public purpose", "Confirmer l'objectif public")}">
          <div class="modal-head">
            <h3>${tr("Confirmar propósito", "Confirm purpose", "Confirmer l'objectif")}</h3>
            <button class="modal-close" type="button" id="lifeConfirmClose">✕</button>
          </div>
          <div class="modal-body">
            <p class="modal-label-center" id="lifeConfirmText">${tr("¿Confirmas este deseo como público?", "Confirm this wish as public?", "Confirmer ce souhait comme public ?")}</p>
            <p class="modal-label-center muted">${tr("Se guardará como público.", "It will be saved as public.", "Il sera enregistré comme public.")}</p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-outline btn-compact" type="button" id="lifeConfirmCancel">${TXT_CANCEL}</button>
            <button class="btn btn-primary btn-compact" type="button" id="lifeConfirmOk">${TXT_CONFIRM}</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeUnlockOverlay")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeUnlockOverlay" aria-hidden="true">
        <div class="modal wish-modal purpose-unlock-modal" role="dialog" aria-modal="true" aria-label="${tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller le souhait secret")}">
          <div class="modal-head">
            <h3>${tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller le souhait secret")}</h3>
            <button class="modal-close" type="button" id="purposeUnlockClose">✕</button>
          </div>
          <div class="modal-body">
            <p class="modal-label-center" id="purposeUnlockText">${tr("Si confirmas tu clave privada, este deseo se volverá público.", "If you confirm your private key, this wish will become public.", "Si tu confirmes ta clé privée, ce souhait deviendra public.")}</p>
            <label class="modal-label hidden" for="purposeUnlockPassword">${tr("Clave privada personal", "Personal private key", "Clé privée personnelle")}</label>
            <input class="modal-input" id="purposeUnlockPassword" type="password" autocomplete="off" placeholder="${tr("Clave privada personal", "Personal private key", "Clé privée personnelle")}" />
            <p class="purpose-unlock-error" id="purposeUnlockError" aria-live="polite"></p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-outline btn-compact" type="button" id="purposeUnlockCancel">${TXT_CANCEL}</button>
            <button class="btn btn-primary btn-compact" type="button" id="purposeUnlockConfirm">${TXT_UNLOCK}</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeFulfillOverlay")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeFulfillOverlay" aria-hidden="true">
        <div class="modal wish-modal fulfill-wish-modal purpose-fulfill-modal" role="dialog" aria-modal="true" aria-label="${tr("Subir evidencia", "Upload evidence", "Téléverser une preuve")}">
          <div class="modal-head">
            <h3>${tr("¡Sube evidencia!", "Upload evidence!", "Téléverse une preuve !")}</h3>
            <button class="modal-close" type="button" id="purposeFulfillClose">✕</button>
          </div>
          <div class="modal-body">
            <p class="panel-muted"><strong>${tr("¿Dónde quieres publicarlo?", "Where do you want to publish it?", "Où veux-tu le publier ?")}</strong></p>
            <div class="purpose-publish-choice" role="group" aria-label="${tr("Selecciona dónde publicar", "Select where to publish", "Sélectionne où publier")}">
              <button class="purpose-publish-btn is-selected" type="button" data-publish="private" aria-pressed="true">
                <span class="purpose-publish-emoji" aria-hidden="true">🔒</span>
                <span>${TXT_PRIVATE}</span>
              </button>
              <button class="purpose-publish-btn" type="button" data-publish="public" aria-pressed="false">
                <span class="purpose-publish-emoji" aria-hidden="true">🌐</span>
                <span>${TXT_PUBLIC}</span>
              </button>
            </div>

            <div class="purpose-private-key" id="purposeFulfillKeyRow">
              <label class="modal-label" for="purposeFulfillPassword">${tr("Clave privada personal", "Personal private key", "Clé privée personnelle")}</label>
              <input class="modal-input" id="purposeFulfillPassword" type="password" autocomplete="off" placeholder="${tr("Clave privada personal", "Personal private key", "Clé privée personnelle")}" />
              <p class="panel-muted purpose-private-key-note">
                ${tr("Ingresa tu clave privada personal para confirmar tu decisión.", "Enter your personal private key to confirm your decision.", "Saisis ta clé privée personnelle pour confirmer ta décision.")}
              </p>
            </div>

            <input id="purposeFulfillEvidence" type="file" accept="image/*" class="hidden" />
            <div class="wish-image-preview" id="purposeFulfillEvidencePreview" aria-live="polite">
              <label class="wish-image-btn" for="purposeFulfillEvidence" aria-label="${TXT_UPLOAD_VISUAL_EVIDENCE}">+</label>
              <div class="wish-preview-content">
                <span class="wish-preview-placeholder">${TXT_UPLOAD_VISUAL_EVIDENCE}</span>
                <span class="wish-preview-name">${TXT_PNG_TYPES}</span>
              </div>
            </div>

            <p class="panel-muted">
              <strong>${tr("¿Juras bajo juramento que este deseo ha sido cumplido?", "Do you swear under oath that this wish has been fulfilled?", "Jures-tu sous serment que ce souhait a été accompli ?")}</strong>
            </p>
            <p class="purpose-fulfill-error" id="purposeFulfillError" aria-live="polite"></p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-primary btn-compact" type="button" id="purposeFulfillConfirm">
              ${tr("Juro bajo juramento que este deseo ha sido cumplido", "I swear under oath that this wish has been fulfilled", "Je jure sous serment que ce souhait a été accompli")}
            </button>
          </div>
          <div class="modal-actions">
            <button class="btn btn-outline btn-compact" type="button" id="purposeFulfillCancel">${TXT_CANCEL}</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeVaultOverlay")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeVaultOverlay" aria-hidden="true">
        <div class="modal wish-modal purpose-vault-modal" role="dialog" aria-modal="true" aria-label="${tr("Desbloquear clave privada", "Unlock private key", "Déverrouiller la clé privée")}">
          <div class="modal-body">
            <img class="private-security-hero" src="/css/cpp-key.webp" alt="${tr("Clave privada personal", "Personal private key", "Clé privée personnelle")}" />
            <h2 class="private-security-title">${tr("Ingresa tu clave privada personal:", "Enter your personal private password:", "Saisis ton mot de passe privé personnel :")}</h2>

            <div class="private-security-input-row">
              <label class="modal-label hidden" for="purposeVaultPassword">${tr("Clave privada personal", "Private password", "Mot de passe privé")}</label>
              <input class="modal-input private-security-input" id="purposeVaultPassword" type="password" autocomplete="off" inputmode="text" placeholder="••••••••••••••" />
              <button class="private-security-btn private-security-unlock" type="button" id="purposeVaultUnlock" aria-label="${tr("Ingresar", "Enter", "Entrer")}" title="${tr("Ingresar", "Enter", "Entrer")}">
                <img src="/css/icons/icondoor.webp" alt="${tr("Ingresar", "Enter", "Entrer")}" />
              </button>
            </div>

            <p class="private-security-error" id="purposeVaultError" role="alert"></p>

            <div class="private-security-actions">
              <button class="private-security-btn" type="button" aria-label="${tr("Cambiar clave privada personal", "Change personal private password", "Changer le mot de passe privé personnel")}"
                id="purposeVaultChangePassword" title="${tr("Cambiar clave privada personal", "Change personal private password", "Changer le mot de passe privé personnel")}">
                <img src="/css/icons/iconedit.webp" alt="${tr("Cambiar contraseña", "Change password", "Changer le mot de passe")}" />
              </button>
              <button class="private-security-btn" type="button" aria-label="${tr("Restablecer clave privada", "Reset password", "Réinitialiser le mot de passe")}"
                id="purposeVaultResetPassword" title="${tr("Restablecer clave privada", "Reset password", "Réinitialiser le mot de passe")}">
                <img src="/css/icons/icondelete.webp" alt="${tr("Restablecer contraseña", "Reset password", "Réinitialiser le mot de passe")}" />
              </button>
            </div>

            <p class="private-security-note">
              ${tr(
                "Tu clave secreta personal protege toda la información privada que declares en esta red social: deseos, propósitos y datos confidenciales. Sin esta clave, no se habilitan cambios de tu propósito de vida.",
                "Your personal secret key protects all private information you declare in this social network: wishes, purposes, and confidential data. Without this key, changes to your life purpose are not enabled.",
                "Ta clé secrète personnelle protège toutes les informations privées que tu déclares dans ce réseau social : souhaits, objectifs et données confidentielles. Sans cette clé, les changements de ton objectif de vie ne sont pas activés."
              )}
            </p>
          </div>

          <div class="modal-actions purpose-vault-actions">
            <button class="btn btn-outline btn-compact" type="button" id="purposeVaultCancel">${TXT_CANCEL}</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeVaultChangePasswordModal")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeVaultChangePasswordModal" aria-hidden="true">
        <div class="modal wish-modal private-change-password-modal" role="dialog" aria-modal="true" aria-label="${tr("Cambiar clave privada personal", "Change personal private password", "Changer le mot de passe privé personnel")}">
          <div class="modal-head">
            <h3>${tr("Cambiar clave privada personal", "Change personal private password", "Changer le mot de passe privé personnel")}</h3>
            <button class="modal-close" type="button" id="purposeVaultChangePasswordCancel">✕</button>
          </div>
          <div class="modal-body">
            <label class="modal-label" for="purposeVaultCurrentPassword">${tr("Ingresa tu clave privada personal actual", "Enter your current personal private password", "Saisis ton mot de passe privé personnel actuel")}</label>
            <input class="modal-input" id="purposeVaultCurrentPassword" type="password" autocomplete="off" />

            <label class="modal-label" for="purposeVaultNewPassword">${tr("Ingresa tu nueva clave privada personal", "Enter your new personal private password", "Saisis ton nouveau mot de passe privé personnel")}</label>
            <input class="modal-input" id="purposeVaultNewPassword" type="password" autocomplete="off" />

            <label class="modal-label" for="purposeVaultConfirmPassword">${tr("Confirma tu nueva clave privada personal", "Confirm your new personal private password", "Confirme ton nouveau mot de passe privé personnel")}</label>
            <input class="modal-input" id="purposeVaultConfirmPassword" type="password" autocomplete="off" />

            <p class="private-security-error" id="purposeVaultChangePasswordError" role="alert"></p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-primary btn-compact" type="button" id="purposeVaultChangePasswordConfirm">${TXT_CONFIRM}</button>
            <button class="btn btn-outline btn-compact" type="button" id="purposeVaultChangePasswordCancelFooter">${TXT_CANCEL}</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeVaultResetPasswordModal")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeVaultResetPasswordModal" aria-hidden="true">
        <div class="modal wish-modal private-reset-modal" role="dialog" aria-modal="true" aria-label="${tr("Restaurar clave privada personal", "Restore personal private password", "Restaurer le mot de passe privé personnel")}">
          <div class="modal-head">
            <h3>${tr("Restaurar clave privada personal", "Restore personal private password", "Restaurer le mot de passe privé personnel")}</h3>
            <button class="modal-close" type="button" id="purposeVaultResetPasswordCancel">✕</button>
          </div>
          <div class="modal-body">
            <p class="private-reset-text">
              ${tr("Estás a punto de restablecer tu clave secreta personal porque la olvidaste.", "You are about to reset your personal secret key because you forgot it.", "Tu es sur le point de réinitialiser ta clé secrète personnelle parce que tu l'as oubliée.")}
            </p>
            <p class="private-reset-text">
              ${tr("Esta acción eliminará de forma permanente todos tus deseos privados y la información cifrada.", "This action will permanently delete all your private wishes and encrypted information.", "Cette action supprimera définitivement tous tes souhaits privés et les informations chiffrées.")}
            </p>
            <p class="private-reset-text private-reset-question">
              ${tr("¿Seguro que deseas continuar?", "Are you sure you want to continue?", "Es-tu sûr de vouloir continuer ?")}
            </p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-primary btn-compact" type="button" id="purposeVaultResetPasswordConfirm">${tr("Sí, continuar", "Yes, continue", "Oui, continuer")}</button>
            <button class="btn btn-outline btn-compact" type="button" id="purposeVaultResetPasswordCancelFooter">${TXT_CANCEL}</button>
          </div>
        </div>
      </div>
    `);
  }

  if (!document.getElementById("purposeVaultResetPasswordFinalModal")) {
    document.body.insertAdjacentHTML("beforeend", `
      <div class="modal-overlay hidden" id="purposeVaultResetPasswordFinalModal" aria-hidden="true">
        <div class="modal wish-modal private-reset-modal" role="dialog" aria-modal="true" aria-label="${tr("Confirmación final de eliminación", "Final deletion confirmation", "Confirmation finale de suppression")}">
          <div class="modal-head">
            <h3>${tr("Confirmación final", "Final confirmation", "Confirmation finale")}</h3>
            <button class="modal-close" type="button" id="purposeVaultResetPasswordFinalCancel">✕</button>
          </div>
          <div class="modal-body">
            <p class="private-reset-text">
              ${tr("Para confirmar la eliminación de tu clave secreta personal, escribe la siguiente palabra exactamente como aparece:", "To confirm deletion of your personal secret key, type the following word exactly as shown:", "Pour confirmer la suppression de ta clé secrète personnelle, écris le mot suivant exactement comme affiché :")}
            </p>
            <p class="private-reset-text private-reset-keyword" id="purposeVaultResetKeywordLabel">${tr("ELIMINAR", "DELETE", "SUPPRIMER")}</p>
            <input class="modal-input" id="purposeVaultResetPasswordKeyword" type="text" autocomplete="off" />

            <p class="private-security-error" id="purposeVaultResetPasswordError" role="alert"></p>
          </div>
          <div class="modal-actions">
            <button class="btn btn-primary btn-compact" type="button" id="purposeVaultResetPasswordFinalConfirm">${tr("Eliminar clave", "Delete key", "Supprimer la clé")}</button>
            <button class="btn btn-outline btn-compact" type="button" id="purposeVaultResetPasswordFinalCancelFooter">${TXT_CANCEL}</button>
          </div>
        </div>
      </div>
    `);
  }
};

const enhancePrefixInputs = (scopeEl) => {
  const inputs = scopeEl.querySelectorAll(".wish-prefix-input");
  inputs.forEach((input) => {
    const prefix = input.dataset.prefix || PURPOSE_PREFIX;
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
    btnEditPurposes.textContent = TXT_EDIT_LIFE_PURPOSE;
    btnEditPurposes.title = TXT_EDIT_LIFE_PURPOSE;
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
    stack.setAttribute("aria-label", TXT_PURPOSE_WISHES);
    stack.innerHTML = `
      <div class="purpose-list">
        ${[1, 2, 3].map((slot) => `
          <div class="purpose-pill-row">
            <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="${slot}" title="${TXT_MARK_FULFILLED.replace("{slot}", String(slot))}">
              <img src="/css/icons/iconfulfill.webp" alt="${TXT_MARK_FULFILLED_WISH}" />
            </button>
            <button class="purpose-pill" type="button" id="purpose${slot}">${currentText[slot]}</button>
            <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock${slot}" data-slot="${slot}" title="${TXT_UNLOCK_WISH.replace("{slot}", String(slot))}">
              <img src="/css/icons/iconkey.webp" alt="${TXT_UNLOCK_SECRET_WISH}" />
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
          fulfillBtn.setAttribute("title", TXT_DEFINE_FIRST);
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
          fulfillBtn.setAttribute("title", TXT_PURPOSE_FULFILLED_HINT);
        } else if (!hasContent) {
          fulfillBtn.setAttribute("title", TXT_DEFINE_FIRST);
        } else {
          fulfillBtn.setAttribute("title", TXT_MARK_FULFILLED.replace("{slot}", String(slotNumber)));
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
      throw new Error(TXT_ERR_NO_ACTIVE_SESSION);
    }

    const headers = {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`
    };
    const res = await fetch(`${API}${path}`, { ...options, headers });
    if (res.status === 401) {
      throw new Error(TXT_ERR_SESSION_EXPIRED);
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
        iconActionBtn.title = TXT_ICON_SELECTED.replace("{label}", iconLabel);
      } else {
        iconActionBtn.innerHTML = `<img src="/css/icons/iconelemental.webp" alt="${TXT_CHOOSE_ICON}">`;
        iconActionBtn.title = TXT_CHOOSE_ICON;
      }
    }

    if (!slotData) {
      setPurposeStatus(groupEl, TXT_STATUS_PUBLIC_DEFAULT);
      return;
    }
    if (slotData.reveal_at && isRevealPending(slotData.reveal_at)) {
      setPurposeStatus(
        groupEl,
        TXT_STATUS_REVEAL_ON.replace("{date}", formatRevealDate(slotData.reveal_at)),
      );
      return;
    }
    if (isPrivate) {
      setPurposeStatus(groupEl, TXT_STATUS_SECRET);
      return;
    }
    setPurposeStatus(groupEl, TXT_STATUS_CONFIRMED_PUBLIC);
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
      ? tr(
          `¿Confirmas el propósito ${number} como público?`,
          `Confirm purpose ${number} as public?`,
          `Confirmer l'objectif ${number} comme public ?`,
        )
      : tr(
          "¿Confirmas este deseo como público?",
          "Confirm this wish as public?",
          "Confirmer ce souhait comme public ?",
        );
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
      setPurposeVaultChangePasswordError(TXT_ERR_CURRENT_PRIVATE_REQUIRED);
      return;
    }
    if (!next.trim() || next.length < 8) {
      setPurposeVaultChangePasswordError(TXT_ERR_NEW_PRIVATE_MIN);
      return;
    }
    if (next !== next2) {
      setPurposeVaultChangePasswordError(TXT_ERR_NEW_PRIVATE_CONFIRM);
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
        throw new Error(rewrapData.detail || TXT_ERR_COULD_NOT_UPDATE_PRIVATE_KEY);
      }

      closePurposeVaultChangePasswordModal();
      closePurposeVaultModal();
      openLifeProposalModal();
    } catch (err) {
      setPurposeVaultChangePasswordError(
        err?.message || TXT_ERR_COULD_NOT_CHANGE_PRIVATE_PASSWORD
      );
    }
  };

  const handlePurposeVaultReset = async () => {
    setPurposeVaultResetPasswordError("");
    const typed = (purposeVaultResetPasswordKeyword?.value || "").trim();
    if (!typed) {
      setPurposeVaultResetPasswordError(TXT_ERR_CONFIRM_WORD_REQUIRED);
      return;
    }

    const allowed = purposeVaultResetKeywords
      ? Object.values(purposeVaultResetKeywords).map((value) => String(value).toUpperCase())
      : ["ELIMINAR", "DELETE", "SUPPRIMER"];

    if (!allowed.includes(typed.toUpperCase())) {
      setPurposeVaultResetPasswordError(TXT_ERR_CONFIRM_WORD_MISMATCH);
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
        throw new Error(data.detail || TXT_ERR_COULD_NOT_RESTORE_PRIVATE_KEY);
      }

      clearDekSession();

      closePurposeVaultResetPasswordFinalModal();
      closePurposeVaultResetPasswordModal();
      closePurposeVaultModal();
      window.location.href = "/create-private-key.html";
    } catch (err) {
      setPurposeVaultResetPasswordError(
        err?.message || TXT_ERR_COULD_NOT_RESTORE_PRIVATE_KEY
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
      throw new Error(statusData.detail || TXT_ERR_COULD_NOT_VERIFY_VAULT);
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
      setPurposeVaultError(TXT_ERR_ENTER_PRIVATE_KEY);
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
        setPurposeVaultError(TXT_ERR_INVALID_PRIVATE_KEY);
      } else {
        setPurposeVaultError(err?.message || TXT_ERR_COULD_NOT_UNLOCK_VAULT);
      }
    }
  };

  const handleEditPurposeClick = async () => {
    try {
      const ready = await ensureVaultReadyForPurposeEditor();
      if (ready) openLifeProposalModal();
    } catch (err) {
      openPurposeVaultModal(err?.message || TXT_ERR_COULD_NOT_VALIDATE_PRIVATE_KEY);
    }
  };

  const openPurposeUnlockModal = (slotNumber) => {
    const slotMap = getPurposeSlotMap(purposeSlots);
    const slotData = slotMap.get(slotNumber);
    if (!slotData || !slotData.is_private || isRevealPending(slotData.reveal_at)) return;
    activePurposeUnlockSlot = slotNumber;
    purposeUnlockText.textContent = tr(
      `Si confirmas tu clave privada, el deseo ${slotNumber} se volverá público.`,
      `If you confirm your private key, wish ${slotNumber} will become public.`,
      `Si tu confirmes ta clé privée, le souhait ${slotNumber} deviendra public.`,
    );
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
      if (placeholder) placeholder.textContent = TXT_UPLOAD_VISUAL_EVIDENCE;
      if (nameEl) nameEl.textContent = TXT_PNG_TYPES;
    }
    updateModalScrollLock();
  };

  const openPurposeFulfillModal = (slotNumber) => {
    if (!purposeFulfillOverlay) return;
    const slotMap = getPurposeSlotMap(purposeSlots);
    const slotData = slotMap.get(slotNumber);
    if (!slotData) {
      window.alert(TXT_DEFINE_FIRST);
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
      if (placeholder) placeholder.textContent = TXT_UPLOAD_VISUAL_EVIDENCE;
      if (nameEl) nameEl.textContent = TXT_PNG_TYPES;
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
      throw new Error(vaultData.detail || TXT_ERR_COULD_NOT_READ_VAULT);
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
      throw new Error(TXT_ERR_ENTER_PRIVATE_KEY);
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
      purposeUnlockError.textContent = TXT_ERR_ENTER_PRIVATE_KEY;
      purposeUnlockError.classList.add("is-visible");
      return;
    }

    const slotMap = getPurposeSlotMap(purposeSlots);
    const slotData = slotMap.get(activePurposeUnlockSlot);
    if (!slotData?.ciphertext_hex || !slotData?.nonce_hex) {
      purposeUnlockError.textContent = TXT_ERR_NO_ENCRYPTED_DATA;
      purposeUnlockError.classList.add("is-visible");
      return;
    }

    const token = getAccessToken();
    if (!token) {
      purposeUnlockError.textContent = TXT_ERR_NO_ACTIVE_SESSION;
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
        throw new Error(revealData.detail || TXT_ERR_COULD_NOT_REVEAL_WISH);
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
      purposeUnlockError.textContent = err?.message || TXT_ERR_COULD_NOT_UNLOCK_WISH;
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
      throw new Error(
        data.detail ||
          tr(
            "No se pudo preparar la carga cifrada.",
            "Could not prepare encrypted payload.",
            "Impossible de préparer la charge chiffrée.",
          ),
      );
    }
    return { ...data, contentType };
  };

  const uploadEncryptedMediaFile = async (file) => {
    if (!file) return null;

    const dekKey = await importDekFromSession();
    const presign = await presignEncryptedUpload(file);
    const mediaId = Number(presign.media_id || 0);
    if (!Number.isFinite(mediaId) || mediaId <= 0) {
      throw new Error(
        tr(
          "No se pudo preparar la carga (media_id inválido).",
          "Could not prepare payload (invalid media_id).",
          "Impossible de préparer la charge (media_id invalide).",
        ),
      );
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
      throw new Error(
        uploadData.detail ||
          tr(
            "No se pudo subir la imagen cifrada.",
            "Could not upload encrypted image.",
            "Impossible de téléverser l'image chiffrée.",
          ),
      );
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
      throw new Error(
        data.detail ||
          tr(
            "No se pudo subir la imagen.",
            "Could not upload image.",
            "Impossible de téléverser l'image.",
          ),
      );
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
      if (previewPlaceholder) previewPlaceholder.textContent = TXT_UPLOAD_VISUAL_EVIDENCE;
      if (previewName) previewName.textContent = TXT_PNG_TYPES;
      return;
    }

    purposeFulfillEvidenceUrl = URL.createObjectURL(file);
    purposeFulfillEvidencePreview.classList.add("has-image");
    if (!purposeFulfillEvidenceImage) {
      purposeFulfillEvidenceImage = document.createElement("img");
      purposeFulfillEvidenceImage.className = "wish-preview-image";
      purposeFulfillEvidenceImage.alt = TXT_SELECTED_EVIDENCE;
      purposeFulfillEvidencePreview.insertBefore(
        purposeFulfillEvidenceImage,
        purposeFulfillEvidencePreview.firstChild
      );
    }
    purposeFulfillEvidenceImage.src = purposeFulfillEvidenceUrl;
    if (previewPlaceholder) previewPlaceholder.textContent = "";
    if (previewName) previewName.textContent = file.name || TXT_SELECTED_EVIDENCE;
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
      setPurposeFulfillError(TXT_ERR_PURPOSE_NOT_FOUND);
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
          throw new Error(TXT_ERR_ENTER_PRIVATE_KEY);
        }
        const token = getAccessToken();
        if (!token) {
          throw new Error(TXT_ERR_NO_ACTIVE_SESSION);
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
        throw new Error(TXT_ERR_DEFINE_TEXT_FIRST);
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
          throw new Error(data.detail || TXT_ERR_COULD_NOT_PUBLISH_WISH);
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
          throw new Error(data.detail || TXT_ERR_COULD_NOT_PUBLISH_WISH);
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
      setPurposeFulfillError(err?.message || TXT_ERR_COULD_NOT_PUBLISH_WISH);
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
    setPurposeStatus(pendingConfirmGroup, TXT_STATUS_CONFIRMED_PUBLIC);
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
        setPurposeStatus(groupEl, TXT_STATUS_SECRET);
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
        actionBtn.title = tr(`Ícono: ${label}`, `Icon: ${label}`, `Icône : ${label}`);
      }
      setPurposeStatus(
        groupEl,
        TXT_STATUS_ICON_ASSOCIATED.replace("{label}", label),
      );
      panel.classList.remove("is-open");
    });
  });

  lifeProposalOverlay.querySelectorAll(".purpose-date").forEach((dateInput) => {
    dateInput.addEventListener("change", () => {
      const groupEl = dateInput.closest(".purpose-group");
      groupEl.dataset.revealAt = dateInput.value || "";
      if (!dateInput.value) return;
      setPurposeStatus(
        groupEl,
        TXT_STATUS_REVEAL_ON.replace("{date}", formatRevealDate(dateInput.value)),
      );
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
        if (!values[index]) setPurposeStatus(groupEl, TXT_COMPLETE_BEFORE_SAVING);
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
            setPurposeStatus(groupEl, err.message || TXT_ERR_COULD_NOT_UNLOCK_VAULT_GENERIC);
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
        throw new Error(payload?.detail || TXT_ERR_COULD_NOT_SAVE_PURPOSES);
      }

      purposeSlots = localSlots
        .map((slot) => normalizePurposeSlot(slot, Number(slot.slot_number)))
        .sort((a, b) => a.slot_number - b.slot_number);
      renderPurposeSlots(purposeSlots);
      closeLifeProposalModal();
    } catch (err) {
      const localizedMessage = err?.message || TXT_ERR_COULD_NOT_SAVE_PURPOSES;
      groups.forEach((groupEl) => {
        setPurposeStatus(groupEl, localizedMessage);
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
