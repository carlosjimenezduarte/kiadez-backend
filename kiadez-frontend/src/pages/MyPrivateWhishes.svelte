<script>
  import { onMount } from "svelte";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { clearDekSession, getDekSessionHex, setDekSessionHex } from "../lib/dekSession";
  import { logout } from "../lib/logout";
  import { syncProfileStarsTotal } from "../lib/starsCounter";
  import { showUiAlert } from "../lib/uiFeedback";

  const PRIVATE_FULFILLED_VISIBLE_SLOTS = 10;
  const PLACEHOLDER_PRIVATE_FULFILLED_MESSAGE =
    "Aquí se publicará tu deseo privado cuando lo marques como cumplido.";
  const privateCompletedSlots = Array.from(
    { length: PRIVATE_FULFILLED_VISIBLE_SLOTS },
    (_, index) => index + 1
  );

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

  const formatFulfilledDate = (value) => {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleDateString("es-CO", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric"
    });
  };

  const getTypeIconSrc = (wishType) => personalTypeIconMap[wishType] || personalTypeIconMap["Espiritual"];

  const getWishTypeHint = (wishType) => {
    const normalized = String(wishType || "").trim();
    if (!normalized) return "Deseo personal";
    return `Deseo ${normalized.toLowerCase()}`;
  };

  const PURPOSE_ORIGIN_HINT = "Este deseo fue alguna vez un deseo de propósito de vida";

  const DEFAULT_PURPOSE_ICON_SRC = "/css/icons/iconelemental.webp";

  const purposeIconMap = {
    air: "/assets/air.png",
    earth: "/assets/earth.png",
    water: "/assets/water.png",
    fire: "/assets/fire.png",
  };

  const getPurposeIconLabel = (iconKey) => {
    if (iconKey === "air") return "Aire";
    if (iconKey === "earth") return "Tierra";
    if (iconKey === "water") return "Agua";
    if (iconKey === "fire") return "Fuego";
    return "Propósito";
  };

  const getPurposeIconSrc = (iconKey) => purposeIconMap[String(iconKey || "")] || "";
  const getLifePurposeIconSrc = (iconKey) => getPurposeIconSrc(iconKey) || DEFAULT_PURPOSE_ICON_SRC;
  const isFromLifePurpose = (wish) => Boolean(wish?.from_life_purpose || wish?.life_purpose_icon_key);

  let privateFulfilledItems = [];
  let privateFulfilledView = privateCompletedSlots.map((slot) => ({ slot, wish: null }));
  let privateFulfilledTotal = 0;
  let privateFulfilledError = "";
  let privateFulfilledLoading = false;
  let privateFulfilledPage = 1;
  let privateFulfilledTotalPages = 1;
  let privateFulfilledPageNumbers = [1];
  let privateFulfilledRangeStart = 0;
  let privateFulfilledRangeEnd = 0;

  $: privateFulfilledView = privateCompletedSlots.map((slot, index) => ({
    slot,
    wish: privateFulfilledItems[index] || null
  }));

  let privateLockRoot;
  let privateUiEpoch = 0;
  let privateFulfilledRequestId = 0;
  let loadPrivateFulfilledWishesFromApiRef = null;

  const goToPrivateFulfilledPage = (page) => {
    const next = Number(page);
    if (!Number.isFinite(next)) return;
    if (privateLockRoot?.classList.contains("private-locked")) return;

    const clamped = Math.max(1, Math.min(Math.trunc(next), privateFulfilledTotalPages || 1));
    if (clamped === privateFulfilledPage) return;

    privateFulfilledPage = clamped;
    if (typeof loadPrivateFulfilledWishesFromApiRef === "function") {
      void loadPrivateFulfilledWishesFromApiRef(privateUiEpoch, clamped);
    }
  };

  $: privateFulfilledTotalPages = Math.max(
    1,
    Math.ceil(privateFulfilledTotal / PRIVATE_FULFILLED_VISIBLE_SLOTS)
  );
  $: privateFulfilledPage = Math.min(privateFulfilledPage, privateFulfilledTotalPages);
  $: privateFulfilledPage = Math.max(privateFulfilledPage, 1);
  $: privateFulfilledPageNumbers = Array.from(
    { length: privateFulfilledTotalPages },
    (_, index) => index + 1
  );
  $: privateFulfilledRangeStart = privateFulfilledTotal
    ? (privateFulfilledPage - 1) * PRIVATE_FULFILLED_VISIBLE_SLOTS + 1
    : 0;
  $: privateFulfilledRangeEnd = privateFulfilledTotal
    ? Math.min(privateFulfilledPage * PRIVATE_FULFILLED_VISIBLE_SLOTS, privateFulfilledTotal)
    : 0;

  onMount(() => {
    document.body.dataset.visitor = "false";
    initPurposeCoverModule();
    void syncProfileStarsTotal("privateWishesStarsTotal");

    const API = import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") || "http://localhost:8000";
    const AAD_VAULT = new TextEncoder().encode("kiadez-vault-v1");
    const AAD_PRIVATE_WISH = new TextEncoder().encode("kiadez-private-wish-v1");
    const PRIVATE_MEDIA_AAD_PREFIX = "kiadez-private-media-v1:";

    const prefixInputs = document.querySelectorAll(".wish-prefix-input");
    const privateUnlockBtn = document.getElementById("private-security-unlock");
    const privatePasswordInput = document.getElementById("private-security-password");
    const privateSecurityError = document.getElementById("private-security-error");
    const privateCensorInterfaceBtn = document.getElementById("private-censor-interface");
    const privateChangePasswordBtn = document.getElementById("private-security-change-password");
    const privateChangePasswordModal = document.getElementById("private-change-password-modal");
    const privateChangePasswordCancel = document.getElementById("private-change-password-cancel");
    const privateChangePasswordCancelFooter = document.getElementById("private-change-password-cancel-footer");
    const privateCurrentPassword = document.getElementById("private-current-password");
    const privateNewPassword = document.getElementById("private-new-password");
    const privateConfirmPassword = document.getElementById("private-confirm-password");
    const privateChangePasswordConfirm = document.getElementById("private-change-password-confirm");
    const privateChangePasswordError = document.getElementById("private-change-password-error");
    const privateResetPasswordBtn = document.getElementById("private-security-reset-password");
    const privateResetPasswordModal = document.getElementById("private-reset-password-modal");
    const privateResetPasswordCancel = document.getElementById("private-reset-password-cancel");
    const privateResetPasswordCancelFooter = document.getElementById("private-reset-password-cancel-footer");
    const privateResetPasswordConfirm = document.getElementById("private-reset-password-confirm");
    const privateResetPasswordFinalModal = document.getElementById("private-reset-password-final-modal");
    const privateResetPasswordFinalCancel = document.getElementById("private-reset-password-final-cancel");
    const privateResetPasswordFinalCancelFooter = document.getElementById("private-reset-password-final-cancel-footer");
    const privateResetKeywordLabel = document.getElementById("private-reset-keyword-label");
    const privateResetKeywordInput = document.getElementById("private-reset-password-keyword");
    const privateResetKeywordConfirm = document.getElementById("private-reset-password-final-confirm");
    const privateResetKeywordError = document.getElementById("private-reset-password-error");
    const suffixInputs = document.querySelectorAll("[data-suffix]");

    const bufToHex = (buf) =>
      [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");

    const hexToBuf = (hex) => {
      const normalized = (hex || "").trim();
      if (!normalized) return new ArrayBuffer(0);
      const bytes = new Uint8Array(normalized.length / 2);
      for (let i = 0; i < bytes.length; i += 1) {
        bytes[i] = parseInt(normalized.substr(i * 2, 2), 16);
      }
      return bytes.buffer;
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
        window.location.href = "/login.html";
        throw new Error("No hay sesión activa.");
      }
      const headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`,
      };
      const res = await fetch(`${API}${path}`, { ...options, headers });
      if (res.status === 401) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login.html";
        throw new Error("Sesión expirada.");
      }
      return res;
    };

    const importDekFromSession = async () => {
      const dekHex = getDekSessionHex();
      if (!dekHex) {
        throw new Error("Debes desbloquear tu clave privada personal primero.");
      }
      const dekRaw = hexToBuf(dekHex);
      return crypto.subtle.importKey("raw", dekRaw, { name: "AES-GCM" }, false, ["encrypt", "decrypt"]);
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

    const aesGcmEncryptText = async (key, text, aadBuf) => {
      const nonce = crypto.getRandomValues(new Uint8Array(12));
      const ciphertext = await crypto.subtle.encrypt(
        { name: "AES-GCM", iv: nonce, additionalData: aadBuf },
        key,
        new TextEncoder().encode(text)
      );
      return { nonce, ciphertext };
    };

    const aesGcmDecryptText = async (key, ciphertextHex, nonceHex, aadBuf) => {
      const decrypted = await crypto.subtle.decrypt(
        { name: "AES-GCM", iv: new Uint8Array(hexToBuf(nonceHex)), additionalData: aadBuf },
        key,
        hexToBuf(ciphertextHex)
      );
      return new TextDecoder().decode(decrypted);
    };

    const decryptDekFromPassword = async (privatePassword) => {
      const vaultRes = await apiFetch("/vault/record");
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

    const decryptMediaToBlobUrl = async ({ media_id, mime_type }) => {
      if (!media_id) return null;
      const dekKey = await importDekFromSession();

      const res = await apiFetch(`/media/${media_id}/raw`);
      if (!res.ok) return null;
      const responseContentType = (res.headers.get("content-type") || "").split(";")[0].trim();
      const buf = await res.arrayBuffer();
      if (!buf || buf.byteLength < 12 + 16) return null;

      const bytes = new Uint8Array(buf);
      const nonce = bytes.slice(0, 12);
      const ciphertext = bytes.slice(12);
      const aad = new TextEncoder().encode(`${PRIVATE_MEDIA_AAD_PREFIX}${media_id}`);

      const decrypted = await crypto.subtle.decrypt(
        { name: "AES-GCM", iv: nonce, additionalData: aad },
        dekKey,
        ciphertext
      );

      const blob = new Blob([decrypted], { type: mime_type || responseContentType || "application/octet-stream" });
      return URL.createObjectURL(blob);
    };

    prefixInputs.forEach((input) => {
      const field = /** @type {HTMLInputElement | HTMLTextAreaElement} */ (input);
      const prefix = field.dataset.prefix || "Deseo ";
      const counterId = field.dataset.counter;
      const counterEl = counterId ? document.getElementById(counterId) : null;
      const maxLength = field.maxLength > 0 ? field.maxLength : null;

      const clampToMax = () => {
        if (maxLength && field.value.length > maxLength) {
          field.value = field.value.slice(0, maxLength);
        }
      };

      const updateCounter = () => {
        if (!counterEl) return;
        const current = field.value.length;
        const limit = maxLength || current;
        counterEl.textContent = `${current}/${limit}`;
      };

      if (!field.value.startsWith(prefix)) {
        field.value = `${prefix}${field.value}`;
      }
      clampToMax();
      updateCounter();

      const ensurePrefix = () => {
        if (!field.value.startsWith(prefix)) {
          const cleaned = field.value.replace(prefix, "");
          field.value = `${prefix}${cleaned}`;
        }
        if (field.value.length < prefix.length) {
          field.value = prefix;
        }
        clampToMax();
        updateCounter();
      };

      field.addEventListener("input", ensurePrefix);

      field.addEventListener("keydown", (event) => {
        const cursorStart = field.selectionStart || 0;
        if ((event.key === "Backspace" || event.key === "Delete") && cursorStart <= prefix.length) {
          event.preventDefault();
          field.setSelectionRange(prefix.length, prefix.length);
        }
      });
    });

    const setInlineError = (el, message) => {
      if (!el) return;
      el.textContent = message || "";
      el.classList.toggle("is-visible", Boolean(message));
    };

    // Replaced later once wish DOM nodes are available.
    let clearPrivateSensitiveUi = () => {};

    const censorPrivateInterface = ({ focusPassword = true } = {}) => {
      if (!privateLockRoot) return;
      privateUiEpoch += 1;

      // Ensure sensitive session data is not kept once the UI is censored.
      try {
        clearDekSession();
      } catch {
        // ignore
      }

      // Clear decrypted UI so the interface is safe even if overlays fail.
      try {
        clearPrivateSensitiveUi();
      } catch {
        // ignore
      }

      // Close any open modals (fixed overlays) that could leak info above the censor overlay.
      document.querySelectorAll(".modal-overlay:not(.hidden)").forEach((overlay) => {
        overlay.classList.add("hidden");
        overlay.setAttribute("aria-hidden", "true");
      });
      document.body.classList.remove("modal-open");

      // Close any dropdowns as well.
      document.querySelectorAll("details[open]").forEach((details) => {
        details.removeAttribute("open");
      });

      privateLockRoot.classList.add("private-locked");
      if (privatePasswordInput) privatePasswordInput.value = "";
      setInlineError(privateSecurityError, "");

      if (focusPassword) {
        setTimeout(() => privatePasswordInput?.focus(), 0);
      }
    };

    const attemptPrivateUnlock = async () => {
      if (!privatePasswordInput || !privateLockRoot) return;
      const value = privatePasswordInput.value || "";
      if (!value.trim()) {
        setInlineError(privateSecurityError, "Debes digitar tu clave privada personal.");
        return;
      }

      try {
        await decryptDekFromPassword(value);
        privateLockRoot.classList.remove("private-locked");
        privatePasswordInput.value = "";
        setInlineError(privateSecurityError, "");
        // Hydrate private wishes only after the DEK is available.
        privateUiEpoch += 1;
        const epoch = privateUiEpoch;
        privateFulfilledPage = 1;
        void loadPrivatePersonalWishesFromApi(epoch);
        void loadPrivateFulfilledWishesFromApi(epoch, 1);
      } catch (err) {
        setInlineError(
          privateSecurityError,
          err?.message || "Contraseña incorrecta. Inténtalo de nuevo."
        );
      }
    };

    if (privateUnlockBtn) {
      privateUnlockBtn.addEventListener("click", () => void attemptPrivateUnlock());
    }

    if (privatePasswordInput) {
      privatePasswordInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          void attemptPrivateUnlock();
        }
      });
    }

    if (privateCensorInterfaceBtn) {
      privateCensorInterfaceBtn.addEventListener("click", () => censorPrivateInterface());
    }

    // If the user leaves this page (or the browser restores it from bfcache), require the password again.
    window.addEventListener("pagehide", () => censorPrivateInterface({ focusPassword: false }));
    window.addEventListener("pageshow", () => censorPrivateInterface({ focusPassword: false }));

    const setChangePasswordModal = (isOpen) => {
      if (!privateChangePasswordModal) return;
      privateChangePasswordModal.classList.toggle("hidden", !isOpen);
      privateChangePasswordModal.setAttribute("aria-hidden", String(!isOpen));
      document.body.classList.toggle("modal-open", Boolean(isOpen));
    };

    if (privateChangePasswordBtn) {
      privateChangePasswordBtn.addEventListener("click", () => setChangePasswordModal(true));
    }

    if (privateChangePasswordCancel) {
      privateChangePasswordCancel.addEventListener("click", () => setChangePasswordModal(false));
    }

    if (privateChangePasswordCancelFooter) {
      privateChangePasswordCancelFooter.addEventListener("click", () => setChangePasswordModal(false));
    }

    const handleChangePrivatePassword = async () => {
      const current = privateCurrentPassword?.value || "";
      const next = privateNewPassword?.value || "";
      const next2 = privateConfirmPassword?.value || "";

      setInlineError(privateChangePasswordError, "");

      if (!current.trim()) {
        setInlineError(privateChangePasswordError, "Debes digitar tu contraseña privada actual.");
        return;
      }
      if (!next.trim() || next.length < 8) {
        setInlineError(privateChangePasswordError, "Tu nueva clave debe tener al menos 8 caracteres.");
        return;
      }
      if (next !== next2) {
        setInlineError(privateChangePasswordError, "La confirmación no coincide con tu nueva clave.");
        return;
      }

      try {
        const dekRaw = await decryptDekFromPassword(current);

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
        const rewrapData = await rewrapRes.json().catch(() => ({}));
        if (!rewrapRes.ok) {
          throw new Error(rewrapData.detail || "No se pudo actualizar tu clave privada.");
        }

        // Ya tenemos el DEK, así que podemos desbloquear la página inmediatamente.
        privateLockRoot?.classList.remove("private-locked");
        privatePasswordInput && (privatePasswordInput.value = "");

        privateCurrentPassword && (privateCurrentPassword.value = "");
        privateNewPassword && (privateNewPassword.value = "");
        privateConfirmPassword && (privateConfirmPassword.value = "");

        setChangePasswordModal(false);
        privateUiEpoch += 1;
        const epoch = privateUiEpoch;
        privateFulfilledPage = 1;
        void loadPrivatePersonalWishesFromApi(epoch);
        void loadPrivateFulfilledWishesFromApi(epoch, 1);
      } catch (err) {
        setInlineError(
          privateChangePasswordError,
          err?.message || "No se pudo modificar la contraseña privada."
        );
      }
    };

    if (privateChangePasswordConfirm) {
      privateChangePasswordConfirm.addEventListener("click", () => void handleChangePrivatePassword());
    }

    const setResetPasswordModal = (isOpen) => {
      if (!privateResetPasswordModal) return;
      privateResetPasswordModal.classList.toggle("hidden", !isOpen);
      privateResetPasswordModal.setAttribute("aria-hidden", String(!isOpen));
      document.body.classList.toggle("modal-open", Boolean(isOpen));
    };

    if (privateResetPasswordBtn) {
      privateResetPasswordBtn.addEventListener("click", () => setResetPasswordModal(true));
    }

    if (privateResetPasswordCancel) {
      privateResetPasswordCancel.addEventListener("click", () => setResetPasswordModal(false));
    }

    if (privateResetPasswordCancelFooter) {
      privateResetPasswordCancelFooter.addEventListener("click", () => setResetPasswordModal(false));
    }

    const setResetPasswordFinalModal = (isOpen) => {
      if (!privateResetPasswordFinalModal) return;
      privateResetPasswordFinalModal.classList.toggle("hidden", !isOpen);
      privateResetPasswordFinalModal.setAttribute("aria-hidden", String(!isOpen));
      document.body.classList.toggle("modal-open", Boolean(isOpen));
    };

    if (privateResetPasswordConfirm) {
      privateResetPasswordConfirm.addEventListener("click", () => {
        setResetPasswordModal(false);
        setResetPasswordFinalModal(true);
      });
    }

    if (privateResetPasswordFinalCancel) {
      privateResetPasswordFinalCancel.addEventListener("click", () => setResetPasswordFinalModal(false));
    }

    if (privateResetPasswordFinalCancelFooter) {
      privateResetPasswordFinalCancelFooter.addEventListener("click", () => setResetPasswordFinalModal(false));
    }

    let resetKeywords = null;
    const loadResetKeywords = async () => {
      try {
        const res = await apiFetch("/vault/reset-keywords");
        const data = await res.json().catch(() => ({}));
        if (!res.ok) return;
        resetKeywords = data?.keywords || null;
        if (privateResetKeywordLabel && resetKeywords && resetKeywords.es) {
          privateResetKeywordLabel.textContent = String(resetKeywords.es);
        }
      } catch {
        // no-op: si falla, dejamos el texto por defecto
      }
    };

    const handleResetVault = async () => {
      setInlineError(privateResetKeywordError, "");
      const typed = (privateResetKeywordInput?.value || "").trim();
      if (!typed) {
        setInlineError(privateResetKeywordError, "Debes escribir la palabra de confirmación.");
        return;
      }

      const allowed = resetKeywords
        ? Object.values(resetKeywords).map((v) => String(v).toUpperCase())
        : ["ELIMINAR", "DELETE", "SUPPRIMER"];

      if (!allowed.includes(typed.toUpperCase())) {
        setInlineError(privateResetKeywordError, "La palabra de confirmación no coincide.");
        return;
      }

      try {
        const res = await apiFetch("/vault/reset", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ confirm_keyword: typed }),
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          throw new Error(data.detail || "No se pudo restaurar tu clave privada.");
        }

        // Limpieza local para que la UI no quede en un estado inconsistente.
        clearDekSession();

        setResetPasswordFinalModal(false);
        setResetPasswordModal(false);
        window.location.href = "/create-private-key.html";
      } catch (err) {
        setInlineError(
          privateResetKeywordError,
          err?.message || "No se pudo restaurar tu clave privada."
        );
      }
    };

    if (privateResetKeywordConfirm) {
      privateResetKeywordConfirm.addEventListener("click", () => void handleResetVault());
    }

    // Al entrar a la página verificamos que exista vault; si ya está desbloqueado en esta sesión, quitamos el lock.
    (async () => {
      try {
        const stRes = await apiFetch("/vault/status");
        const st = await stRes.json().catch(() => ({}));
        if (!stRes.ok) return;
        if (!st?.has_vault) {
          window.location.href = "/create-private-key.html";
          return;
        }

        await loadResetKeywords();
      } catch (err) {
        console.error(err);
      }
    })();

    suffixInputs.forEach((input) => {
      const field = /** @type {HTMLInputElement | HTMLTextAreaElement} */ (input);
      const suffix = field.dataset.suffix || "";
      if (!suffix) return;

      const normalizeSuffix = () => {
        const current = field.value || "";
        const suffixIndex = current.indexOf(suffix);
        if (suffixIndex === -1) {
          field.value = `${current}${suffix}`;
          return;
        }
        const editablePart = current.slice(0, suffixIndex);
        field.value = `${editablePart}${suffix}`;
      };

      const clampCaret = () => {
        const current = field.value || "";
        const suffixIndex = current.indexOf(suffix);
        if (suffixIndex === -1) return;
        const maxPos = suffixIndex;
        const cursorStart = field.selectionStart ?? 0;
        const cursorEnd = field.selectionEnd ?? 0;
        if (cursorStart > maxPos || cursorEnd > maxPos) {
          field.setSelectionRange(maxPos, maxPos);
        }
      };

      normalizeSuffix();

      field.addEventListener("input", () => {
        normalizeSuffix();
        clampCaret();
      });

      field.addEventListener("keydown", (event) => {
        const current = field.value || "";
        const suffixIndex = current.indexOf(suffix);
        if (suffixIndex === -1) return;
        const maxPos = suffixIndex;
        const cursorStart = field.selectionStart ?? 0;
        const cursorEnd = field.selectionEnd ?? 0;

        if ((event.key === "Backspace" || event.key === "Delete") && cursorStart >= maxPos) {
          event.preventDefault();
          field.setSelectionRange(maxPos, maxPos);
        }

        if (cursorEnd > maxPos) {
          event.preventDefault();
          field.setSelectionRange(maxPos, maxPos);
        }
      });

      field.addEventListener("click", clampCaret);
      field.addEventListener("focus", clampCaret);
      field.addEventListener("mouseup", clampCaret);
    });

    const lampSlotTemplate = document.getElementById("private-wish-lamp-slot-template");
    const personalWishList = document.getElementById("private-personal-wish-list");
    const personalWishAdd = document.getElementById("private-personal-wish-add");
    const personalWishCount = document.getElementById("private-personal-wish-count");
    const personalWishModal = document.getElementById("private-personal-wish-modal");
    const closePersonalWishModal = document.getElementById("private-close-personal-wish-modal");
    const deleteWishModal = document.getElementById("private-delete-wish-modal");
    const confirmDeleteWish = document.getElementById("private-confirm-delete-wish");
    const cancelDeleteWish = document.getElementById("private-cancel-delete-wish");
    const fulfillWishModal = document.getElementById("private-fulfill-wish-modal");
    const cancelFulfillWish = document.getElementById("private-cancel-fulfill-wish");
    const confirmFulfillWish = document.getElementById("private-confirm-fulfill-wish");
    const fulfillEvidence = document.getElementById("private-fulfill-evidence");
    const fulfillEvidencePreview = document.getElementById("private-fulfill-evidence-preview");
    const icanConfirmModal = document.getElementById("private-ican-confirm-modal");
    const icanConfirmYes = document.getElementById("private-ican-confirm-yes");
    const icanConfirmNo = document.getElementById("private-ican-confirm-no");
    const guardianContactModal = document.getElementById("private-guardian-contact-modal");
    const cancelGuardianModal = document.getElementById("private-cancel-guardian-modal");
    const personalWishText = document.getElementById("private-personal-wish-text");
    const personalWishError = document.getElementById("private-personal-wish-error");
    const confirmPersonalWish = document.getElementById("private-confirm-personal-wish");
    const personalWishMedia = document.getElementById("private-personal-wish-media");
    const personalWishPreview = document.getElementById("private-personal-wish-preview");
    const personalWishFileName = document.getElementById("private-personal-wish-file-name");
    const personalWishTypeIcon = document.getElementById("private-personal-wish-type-icon");
    const personalWishTypeInputs = document.querySelectorAll('input[name="private-personal-wish-type"]');
    const personalWishTypeHint = document.getElementById("private-personal-wish-type-hint");
    const personalMax = 50;
    const personalMin = 7;
    let personalTotal = 0;
    let personalPreviewUrl = null;
    let personalPreviewImage = null;
    let activePersonalSlot = null;
    let activeDeleteSlot = null;
    let activeFulfillSlot = null;
    let activeIcanSlot = null;
    let fulfillEvidenceUrl = null;
    let fulfillEvidenceImage = null;

    const parsePositiveId = (value) => {
      const id = Number(value || 0);
      return Number.isFinite(id) && id > 0 ? id : null;
    };

    const fetchPrivatePersonalWishList = async () => {
      const res = await apiFetch("/private-wishes/personal");
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudieron cargar tus deseos privados.");
      }
      return data;
    };

    const fetchPrivateFulfilledPersonalWishList = async (
      limit = PRIVATE_FULFILLED_VISIBLE_SLOTS,
      offset = 0
    ) => {
      const res = await apiFetch(`/private-wishes/personal/fulfilled?limit=${limit}&offset=${offset}`);
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudieron cargar tus deseos privados cumplidos.");
      }
      return data;
    };

    const createPrivatePersonalWish = async (payload) => {
      const res = await apiFetch("/private-wishes/personal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo crear el deseo privado.");
      }
      return data;
    };

    const updatePrivatePersonalWish = async (wishId, payload) => {
      const res = await apiFetch(`/private-wishes/personal/${wishId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo actualizar el deseo privado.");
      }
      return data;
    };

    const deletePrivatePersonalWish = async (wishId) => {
      const res = await apiFetch(`/private-wishes/personal/${wishId}`, { method: "DELETE" });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo borrar el deseo privado.");
      }
      return data;
    };

    const fulfillPrivatePersonalWish = async (wishId, evidenceMediaId = null) => {
      const res = await apiFetch(`/private-wishes/personal/${wishId}/fulfill`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ evidence_media_id: evidenceMediaId || null }),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || "No se pudo marcar el deseo como cumplido.");
      }
      return data;
    };

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
      if (fulfillEvidence) fulfillEvidence.value = "";
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

    if (closePersonalWishModal) {
      closePersonalWishModal.addEventListener("click", closePersonalWishModalFn);
    }

    if (personalWishModal) {
      personalWishModal.addEventListener("click", (event) => {
        if (event.target === personalWishModal) closePersonalWishModalFn();
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

      const previewPlaceholder = fulfillEvidencePreview.querySelector(".wish-preview-placeholder");
      const previewName = fulfillEvidencePreview.querySelector(".wish-preview-name");

      if (!file) {
        fulfillEvidencePreview.classList.remove("has-image");
        if (fulfillEvidenceImage) {
          fulfillEvidenceImage.remove();
          fulfillEvidenceImage = null;
        }
        if (previewPlaceholder) {
          previewPlaceholder.textContent = "Sube la evidencia visual.";
        }
        if (previewName) {
          previewName.textContent = "PNG, WEBP, JPEG, etc.";
        }
        return;
      }

      fulfillEvidenceUrl = URL.createObjectURL(file);
      fulfillEvidencePreview.classList.add("has-image");
      if (!fulfillEvidenceImage) {
        fulfillEvidenceImage = document.createElement("img");
        fulfillEvidenceImage.className = "wish-preview-image";
        fulfillEvidenceImage.alt = "Evidencia seleccionada";
        fulfillEvidencePreview.insertBefore(fulfillEvidenceImage, fulfillEvidencePreview.firstChild);
      }
      fulfillEvidenceImage.src = fulfillEvidenceUrl;
      if (previewPlaceholder) {
        previewPlaceholder.textContent = "Imagen seleccionada";
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

    if (personalWishAdd) {
      personalWishAdd.addEventListener("click", () => {
        addLampSlot();
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

    const setPersonalWishError = (show, message) => {
      if (!personalWishError) return;
      if (message) {
        personalWishError.textContent = message;
      }
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

    const resetSlotToEmpty = (slot) => {
      if (!slot || !lampSlotTemplate) return;
      if (slot.dataset.imageUrl && slot.dataset.imageObjectUrl === "true") {
        URL.revokeObjectURL(slot.dataset.imageUrl);
      }
      delete slot.dataset.imageUrl;
      delete slot.dataset.imageObjectUrl;
      delete slot.dataset.imageMimeType;
      delete slot.dataset.imageFilename;
      delete slot.dataset.description;
      delete slot.dataset.type;
      delete slot.dataset.goal;
      delete slot.dataset.current;
      delete slot.dataset.template;
      delete slot.dataset.wishId;
      delete slot.dataset.mediaId;
      slot.classList.remove("is-choosing", "is-filled");
      slot.classList.add("is-empty");
      slot.innerHTML = "";
      slot.appendChild(lampSlotTemplate.content.cloneNode(true));
    };

    const renderPersonalWishSlot = (slot, description, imageUrl, type) => {
      if (!slot) return;
      if (slot.dataset.imageUrl && slot.dataset.imageUrl !== imageUrl && slot.dataset.imageObjectUrl === "true") {
        URL.revokeObjectURL(slot.dataset.imageUrl);
      }
      delete slot.dataset.imageUrl;
      delete slot.dataset.imageObjectUrl;

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
      actions.appendChild(createWishActionBtn("/css/icons/iconedit.webp", "Editar deseo", "edit"));
      actions.appendChild(createWishActionBtn("/css/icons/iconfulfill.webp", "Marcar como cumplido", "fulfill"));
      actions.appendChild(createWishActionBtn("/css/icons/icondelete.webp", "Borrar deseo", "delete"));
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
        slot.dataset.imageObjectUrl = imageUrl.startsWith("blob:") ? "true" : "false";
      } else {
        body.classList.add("single");
      }

      row.appendChild(body);
      slot.appendChild(row);
    };

    const decryptPrivateWishPayload = async (wish) => {
      if (!wish?.ciphertext_hex || !wish?.nonce_hex) return null;
      const dekKey = await importDekFromSession();
      const plainText = await aesGcmDecryptText(dekKey, wish.ciphertext_hex, wish.nonce_hex, AAD_PRIVATE_WISH);
      try {
        return JSON.parse(plainText);
      } catch {
        return { wish_text: plainText };
      }
    };

    const applyPrivateWishRecordToSlot = async (slot, wish, epoch) => {
      if (!slot || !wish) return;
      if (epoch !== privateUiEpoch) return;

      const wishId = parsePositiveId(wish.id);
      const mediaId = parsePositiveId(wish.media_id);
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

      let wishText = "";
      let wishType = "Espiritual";
      let imageMimeType = "";
      let imageFilename = "";

      try {
        const payload = await decryptPrivateWishPayload(wish);
        if (epoch !== privateUiEpoch) return;
        if (payload && typeof payload === "object") {
          wishText = String(payload.wish_text || payload.text || "");
          wishType = String(payload.wish_type || payload.type || "Espiritual");
          const image = payload.image && typeof payload.image === "object" ? payload.image : null;
          imageMimeType = String(image?.mime_type || payload.image_mime_type || "");
          imageFilename = String(image?.filename || payload.image_filename || "");
        }
      } catch (err) {
        console.error(err);
      }

      let imageUrl = null;
      if (mediaId) {
        if (epoch !== privateUiEpoch) return;
        try {
          imageUrl = await decryptMediaToBlobUrl({
            media_id: mediaId,
            mime_type: imageMimeType,
          });
        } catch (err) {
          console.error(err);
        }
      }

      if (epoch !== privateUiEpoch) {
        if (imageUrl && String(imageUrl).startsWith("blob:")) {
          URL.revokeObjectURL(imageUrl);
        }
        return;
      }

      if (imageMimeType) slot.dataset.imageMimeType = imageMimeType;
      else delete slot.dataset.imageMimeType;
      if (imageFilename) slot.dataset.imageFilename = imageFilename;
      else delete slot.dataset.imageFilename;

      renderPersonalWishSlot(slot, wishText || "", imageUrl || null, wishType || "Espiritual");
    };

    const clearPersonalSlots = () => {
      if (!personalWishList) return;
      personalWishList.querySelectorAll(".wish-slot").forEach((slot) => {
        if (slot.dataset?.imageUrl && slot.dataset.imageObjectUrl === "true") {
          URL.revokeObjectURL(slot.dataset.imageUrl);
        }
      });
      personalWishList.innerHTML = "";
      personalTotal = 0;
      if (personalWishAdd) {
        personalWishAdd.disabled = false;
      }
      if (personalWishCount) {
        personalWishCount.textContent = "0";
      }
    };

    const hydratePersonalSlots = async (items, epoch) => {
      if (!personalWishList) return;
      const records = Array.isArray(items) ? items : [];
      clearPersonalSlots();
      if (epoch !== privateUiEpoch) return;

      const totalSlots = Math.max(personalMin, Math.min(personalMax, records.length));
      for (let i = 0; i < totalSlots; i += 1) {
        addLampSlot();
      }

      const slots = Array.from(personalWishList.querySelectorAll(".wish-slot"));
      for (let i = 0; i < records.length; i += 1) {
        const slot = slots[i];
        const wish = records[i];
        if (!slot) continue;
        try {
          if (epoch !== privateUiEpoch || privateLockRoot?.classList.contains("private-locked")) break;
          await applyPrivateWishRecordToSlot(slot, wish, epoch);
        } catch (err) {
          console.error(err);
        }
      }
    };

    const loadPrivatePersonalWishesFromApi = async (epoch = privateUiEpoch) => {
      try {
        await importDekFromSession();
        const data = await fetchPrivatePersonalWishList();
        if (epoch !== privateUiEpoch) return;
        await hydratePersonalSlots(data?.items || [], epoch);
      } catch (error) {
        console.error(error);
      }
    };

    const revokePrivateFulfilledBlobUrls = () => {
      const items = Array.isArray(privateFulfilledItems) ? privateFulfilledItems : [];
      items.forEach((item) => {
        const url = item?.image_url || "";
        if (url && String(url).startsWith("blob:")) {
          URL.revokeObjectURL(url);
        }
      });
    };

    const loadPrivateFulfilledWishesFromApi = async (epoch = privateUiEpoch) => {
      const requestId = (privateFulfilledRequestId += 1);
      const requestedPage = Math.max(1, Math.trunc(Number(privateFulfilledPage || 1)));
      const offset = (requestedPage - 1) * PRIVATE_FULFILLED_VISIBLE_SLOTS;
      privateFulfilledPage = requestedPage;
      privateFulfilledLoading = true;
      privateFulfilledError = "";

      const newBlobUrls = [];

      const isStale = () =>
        requestId !== privateFulfilledRequestId ||
        epoch !== privateUiEpoch ||
        privateLockRoot?.classList.contains("private-locked");

      try {
        await importDekFromSession();
        const data = await fetchPrivateFulfilledPersonalWishList(PRIVATE_FULFILLED_VISIBLE_SLOTS, offset);
        if (isStale()) {
          newBlobUrls.forEach((url) => URL.revokeObjectURL(url));
          return;
        }

        const rawItems = Array.isArray(data?.items) ? data.items : [];
        const total = Number(data?.total) || rawItems.length;
        const hydrated = [];

        for (let i = 0; i < rawItems.length; i += 1) {
          if (isStale()) break;
          const wish = rawItems[i];

	          let wishText = "";
	          let wishType = "Espiritual";
	          let originalMimeType = "";
	          let lifePurposeIconKey = null;
	          let fromLifePurpose = false;

	          try {
	            const payload = await decryptPrivateWishPayload(wish);
	            if (isStale()) break;
	            if (payload && typeof payload === "object") {
	              wishText = String(payload.wish_text || payload.text || "");
	              wishType = String(payload.wish_type || payload.type || "Espiritual");
	              lifePurposeIconKey = payload.life_purpose_icon_key || payload.purpose_icon_key || null;
	              fromLifePurpose = Boolean(
	                payload.from_life_purpose ||
	                  payload.life_purpose_slot_number ||
	                  payload.life_purpose_icon_key ||
	                  payload.purpose_icon_key
	              );
	              const image = payload.image && typeof payload.image === "object" ? payload.image : null;
	              originalMimeType = String(image?.mime_type || payload.image_mime_type || "");
	            }
	          } catch (err) {
	            console.error(err);
	          }

          const evidenceId = parsePositiveId(wish.fulfilled_evidence_media_id);
          const originalId = parsePositiveId(wish.media_id);
          const imageMediaId = evidenceId || originalId || null;

          let imageUrl = null;
          if (imageMediaId) {
            try {
              imageUrl = await decryptMediaToBlobUrl({
                media_id: imageMediaId,
                mime_type: evidenceId ? "" : originalMimeType,
              });
              if (imageUrl && String(imageUrl).startsWith("blob:")) {
                newBlobUrls.push(imageUrl);
              }
            } catch (err) {
              console.error(err);
            }
          }

	          hydrated.push({
	            id: wish.id,
	            wish_text: wishText,
	            wish_type: wishType,
	            from_life_purpose: fromLifePurpose,
	            life_purpose_icon_key: lifePurposeIconKey,
	            fulfilled_at: wish.fulfilled_at,
	            image_url: imageUrl,
	          });
	        }

        if (isStale()) {
          newBlobUrls.forEach((url) => URL.revokeObjectURL(url));
          return;
        }

        revokePrivateFulfilledBlobUrls();
        privateFulfilledItems = hydrated;
        privateFulfilledTotal = total;
      } catch (error) {
        newBlobUrls.forEach((url) => URL.revokeObjectURL(url));
        if (isStale()) return;
        privateFulfilledItems = [];
        privateFulfilledTotal = 0;
        privateFulfilledError =
          error instanceof Error
            ? error.message
            : "No se pudieron cargar tus deseos privados cumplidos.";
      } finally {
        if (epoch === privateUiEpoch && requestId === privateFulfilledRequestId) {
          privateFulfilledLoading = false;
        }
      }
	    };
	
	    loadPrivateFulfilledWishesFromApiRef = loadPrivateFulfilledWishesFromApi;

	    window.addEventListener("kiadez:fulfilled-wishes-changed", (event) => {
	      const scope = event?.detail?.scope;
	      if (scope !== "private") return;
	      if (privateLockRoot?.classList.contains("private-locked")) return;
	      privateFulfilledPage = 1;
	      privateUiEpoch += 1;
	      const epoch = privateUiEpoch;
	      void loadPrivateFulfilledWishesFromApi(epoch);
	    });
	
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

    clearPrivateSensitiveUi = () => {
      // Remove any decrypted data + blob URLs from the DOM.
      clearPersonalSlots();
      for (let i = 0; i < personalMin; i += 1) {
        addLampSlot();
      }

      revokePrivateFulfilledBlobUrls();
      privateFulfilledRequestId += 1;
      privateFulfilledItems = [];
      privateFulfilledTotal = 0;
      privateFulfilledError = "";
      privateFulfilledLoading = false;
      privateFulfilledPage = 1;

      resetPersonalWishForm();
      updateFulfillEvidencePreview(null);
      if (fulfillEvidence) fulfillEvidence.value = "";

      activePersonalSlot = null;
      activeDeleteSlot = null;
      activeFulfillSlot = null;
      activeIcanSlot = null;
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

    personalWishTypeInputs.forEach((input) => {
      input.addEventListener("change", () => {
        if (input.checked) {
          syncPersonalTypeIcon(input.value);
          syncPersonalTypeHint(input.value);
        }
      });
    });

    const checkedInput = Array.from(personalWishTypeInputs).find((input) => input.checked);
    if (checkedInput) {
      syncPersonalTypeIcon(checkedInput.value);
      syncPersonalTypeHint(checkedInput.value);
    }

    const handleConfirmPersonalWish = async () => {
      if (!activePersonalSlot) return;
      if (!personalWishText) return;
      if (!isPersonalWishValid()) {
        setPersonalWishError(true, "No has descrito tu deseo.");
        return;
      }

      const epoch = privateUiEpoch;
      const description = personalWishText.value.trim();
      const file = personalWishMedia && personalWishMedia.files ? personalWishMedia.files[0] : null;
      const selectedType = Array.from(personalWishTypeInputs).find((input) => input.checked)?.value || "Espiritual";

      const wishId = parsePositiveId(activePersonalSlot.dataset.wishId);
      const currentMediaId = parsePositiveId(activePersonalSlot.dataset.mediaId);
      const currentMimeType = activePersonalSlot.dataset.imageMimeType || "";
      const currentFilename = activePersonalSlot.dataset.imageFilename || "";

      try {
        setPersonalWishError(false);

        const uploaded = file ? await uploadEncryptedMediaFile(file) : null;
        if (epoch !== privateUiEpoch) return;
        const mediaId = uploaded?.media_id || currentMediaId || null;
        const mimeType = uploaded?.mime_type || currentMimeType || "";
        const filename = uploaded?.original_filename || currentFilename || "";

        const dekKey = await importDekFromSession();
        if (epoch !== privateUiEpoch) return;
        const payloadPlain = {
          v: 1,
          wish_text: description,
          wish_type: selectedType,
          image: mediaId
            ? {
                mime_type: mimeType || null,
                filename: filename || null,
              }
            : null,
        };

        const { nonce, ciphertext } = await aesGcmEncryptText(dekKey, JSON.stringify(payloadPlain), AAD_PRIVATE_WISH);
        if (epoch !== privateUiEpoch) return;

        const apiPayload = {
          ciphertext_hex: bufToHex(ciphertext),
          nonce_hex: bufToHex(nonce.buffer),
          media_id: mediaId || null,
        };

        const savedWish = wishId
          ? await updatePrivatePersonalWish(wishId, apiPayload)
          : await createPrivatePersonalWish(apiPayload);
        if (epoch !== privateUiEpoch) return;

        if (savedWish?.id) {
          activePersonalSlot.dataset.wishId = `${savedWish.id}`;
        }
        if (mediaId) {
          activePersonalSlot.dataset.mediaId = `${mediaId}`;
        } else {
          delete activePersonalSlot.dataset.mediaId;
        }
        if (mimeType) activePersonalSlot.dataset.imageMimeType = mimeType;
        else delete activePersonalSlot.dataset.imageMimeType;
        if (filename) activePersonalSlot.dataset.imageFilename = filename;
        else delete activePersonalSlot.dataset.imageFilename;

        // Render immediately using local plaintext + local preview (if any). On refresh it'll decrypt from API.
        const imageUrl = file ? URL.createObjectURL(file) : activePersonalSlot.dataset.imageUrl || null;
        if (epoch !== privateUiEpoch) {
          if (imageUrl && String(imageUrl).startsWith("blob:")) {
            URL.revokeObjectURL(imageUrl);
          }
          return;
        }
        renderPersonalWishSlot(activePersonalSlot, description, imageUrl, selectedType);

        closePersonalWishModalFn();
        resetPersonalWishForm();
        activePersonalSlot = null;
      } catch (error) {
        console.error(error);
        if (epoch !== privateUiEpoch || privateLockRoot?.classList.contains("private-locked")) return;
        setPersonalWishError(true, error?.message || "No se pudo guardar tu deseo privado.");
      }
    };

    if (confirmPersonalWish) {
      confirmPersonalWish.addEventListener("click", handleConfirmPersonalWish);
    }

    if (confirmDeleteWish) {
      confirmDeleteWish.addEventListener("click", async () => {
        const epoch = privateUiEpoch;
        if (activeDeleteSlot) {
          const wishId = parsePositiveId(activeDeleteSlot.dataset.wishId);
          if (wishId) {
            try {
              await deletePrivatePersonalWish(wishId);
              if (epoch !== privateUiEpoch) return;
            } catch (error) {
              console.error(error);
              if (epoch !== privateUiEpoch || privateLockRoot?.classList.contains("private-locked")) return;
              showUiAlert(error?.message || "No se pudo borrar el deseo privado.", { type: "error" });
              return;
            }
          }
          if (epoch !== privateUiEpoch) return;
          resetSlotToEmpty(activeDeleteSlot);
        }
        if (epoch !== privateUiEpoch) return;
        closeDeleteWishModalFn();
      });
    }

    const handleConfirmFulfillWish = async () => {
      if (!activeFulfillSlot) return;
      const epoch = privateUiEpoch;
      const wishId = parsePositiveId(activeFulfillSlot.dataset.wishId);
      if (!wishId) {
        showUiAlert("Primero debes guardar el deseo antes de marcarlo como cumplido.", { type: "error" });
        return;
      }

      try {
        const file = fulfillEvidence && fulfillEvidence.files ? fulfillEvidence.files[0] : null;
        const uploadedEvidence = file ? await uploadEncryptedMediaFile(file) : null;
        if (epoch !== privateUiEpoch) return;
        await fulfillPrivatePersonalWish(wishId, uploadedEvidence?.media_id || null);
        if (epoch !== privateUiEpoch) return;

        resetSlotToEmpty(activeFulfillSlot);
        closeFulfillWishModalFn();
        privateFulfilledPage = 1;
        void loadPrivateFulfilledWishesFromApi(epoch, 1);
      } catch (error) {
        console.error(error);
        if (epoch !== privateUiEpoch || privateLockRoot?.classList.contains("private-locked")) return;
        showUiAlert(error?.message || "No se pudo marcar el deseo como cumplido.", { type: "error" });
      }
    };

    if (confirmFulfillWish) {
      confirmFulfillWish.addEventListener("click", () => void handleConfirmFulfillWish());
    }

    if (personalWishList) {
      personalWishList.addEventListener("click", (event) => {
        const lampBtn = event.target.closest(".wish-lamp-btn");
        const actionBtn = event.target.closest(".wish-icon-btn");

        if (lampBtn) {
          const slot = lampBtn.closest(".wish-slot");
          if (!slot) return;
          activePersonalSlot = slot;
          openPersonalWishModal();
          return;
        }

        if (actionBtn) {
          const slot = actionBtn.closest(".wish-slot");
          if (!slot) return;
          if (actionBtn.dataset.action === "delete") {
            openDeleteWishModal(slot);
          } else if (actionBtn.dataset.action === "edit") {
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
          } else if (actionBtn.dataset.action === "fulfill") {
            openFulfillWishModal(slot);
          }
          return;
        }
      });
    }
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Mis deseos privados</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="private-wishes-page private-locked" bind:this={privateLockRoot}>
  <div class="page-background page-background-user private-wishes-background">
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
      <a class="topbar-btn is-active" href="/my-private-whishes.html">🔒 Deseos privados</a>
        <a class="topbar-btn" href="/my-fulfilled-whises.html">✅ Deseos cumplidos</a>
      </div>

      <div class="feed-topbar-zone feed-topbar-right">
        <details class="topbar-dropdown" id="profileDropdown">
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

        <details class="topbar-dropdown" id="menuDropdown">
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

    <main class="user-home">
      <!-- =========================
       *  PORTADA / COVER
       *  ========================= -->
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

      <div class="private-wishes-body private-wishes-content">
        <div class="private-wishes-surface">
        <!-- =========================
         *  NAV / LINKS
         *  ========================= -->
        <nav class="profile-nav" aria-label="Navegación de perfil">
          <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
          <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
            <span class="nav-icon">⭐</span>
            <span><strong id="privateWishesStarsTotal">0</strong> estrellas</span>
          </a>
          <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
          <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
          <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
          <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
          <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
        <a class="nav-pill" href="/messages.html" title="Mensajes">Mensajes</a>
        </nav>

        <!-- =========================
         *  MIS DESEOS PRIVADOS
         *  ========================= -->
        <section class="private-wishes-shell" aria-label="Mis deseos privados">
          <header class="private-wishes-head">
            <div>
              <h2 class="private-wishes-title">Mis deseos privados</h2>
            </div>

            <div class="private-wishes-tags">
              <button class="btn btn-outline btn-compact private-censor-btn" type="button" id="private-censor-interface" title="Censurar interfaz de deseos privados">
                <span class="private-censor-icon" aria-hidden="true">🔒</span>
                <span>Censurar interfaz de deseos privados</span>
              </button>
            </div>
          </header>

          <!-- =========================
           *  LISTAS DE DESEOS
           *  ========================= -->
          <section class="wish-lists-grid" aria-label="Listas de deseos">
            <article class="panel wish-list-panel">
              <div class="panel-head">
                <h3 class="panel-title">Deseos privados</h3>
                <span class="panel-badge"><span id="private-personal-wish-count">7</span> / 50</span>
              </div>

              <ol class="wish-slot-list" id="private-personal-wish-list" data-total="50" aria-label="Deseos personales">
              </ol>
              <div class="wish-add-row">
                <button class="wish-add-btn" id="private-personal-wish-add" type="button" title="Agregar deseo">
                  <span class="wish-add-plus">+</span>
                </button>
              </div>
            </article>

            <div class="fulfilled-wishes-page">
              <article class="panel wish-list-panel">
                <div class="panel-head">
                  <h3 class="panel-title">Deseos privados cumplidos</h3>
                  <span class="panel-badge">
                    {privateFulfilledItems.length} / {PRIVATE_FULFILLED_VISIBLE_SLOTS}
                  </span>
                </div>
                <ol
                  class="wish-slot-list wish-slot-list-fulfilled"
                  aria-label="Deseos privados cumplidos"
                  style={`counter-reset: wish ${Math.max(0, privateFulfilledRangeStart - 1)};`}
                >
                  {#each privateFulfilledView as item}
                    <li class="wish-slot is-filled" data-slot={item.slot}>
                      {#if item.wish}
                        {@const fulfilledImageUrl = item.wish.image_url || null}
                        <div class="wish-slot-row">
                          <div class={`wish-slot-body${fulfilledImageUrl ? "" : " single"}`}>
                            <div class="wish-slot-left">
                              <div class="wish-slot-header">
                                <button
                                  class="wish-category-hint"
                                  type="button"
                                  data-hint={isFromLifePurpose(item.wish) ? PURPOSE_ORIGIN_HINT : getWishTypeHint(item.wish.wish_type)}
                                  aria-label={isFromLifePurpose(item.wish) ? PURPOSE_ORIGIN_HINT : getWishTypeHint(item.wish.wish_type)}
	                                >
	                                  <img
	                                    class={`wish-slot-category-icon${isFromLifePurpose(item.wish) ? " is-purpose-icon" : ""}`}
	                                    src={isFromLifePurpose(item.wish) ? getLifePurposeIconSrc(item.wish.life_purpose_icon_key) : getTypeIconSrc(item.wish.wish_type)}
	                                    alt={isFromLifePurpose(item.wish) ? getPurposeIconLabel(item.wish.life_purpose_icon_key) : getWishTypeHint(item.wish.wish_type)}
	                                    loading="lazy"
	                                  />
	                                </button>
	                                <br />
	                                <div class="wish-slot-title">{item.wish.wish_text}</div>
	                                <div class="wish-slot-meta wish-slot-meta-fulfilled">
	                                  {#if item.wish.fulfilled_at}
                                    <span class="wish-type-pill wish-fulfilled-date-pill">
                                      Cumplido el {formatFulfilledDate(item.wish.fulfilled_at)}
                                    </span>
                                  {/if}
                                </div>
                              </div>
                            </div>

                            {#if fulfilledImageUrl}
                              <div class="wish-slot-image-wrap">
                                <img
                                  class="wish-slot-image wish-slot-image-fulfilled"
                                  src={fulfilledImageUrl}
                                  alt="Evidencia del deseo privado cumplido"
                                  loading="lazy"
                                />
                              </div>
                            {/if}
                          </div>
                        </div>
                      {:else}
                        <div class="wish-slot-row wish-slot-row-fulfilled">
                          <p class="wish-slot-fulfilled-message">{PLACEHOLDER_PRIVATE_FULFILLED_MESSAGE}</p>
                        </div>
                      {/if}
                    </li>
                  {/each}
                </ol>
                {#if privateFulfilledTotal > 0 && privateFulfilledTotal >= PRIVATE_FULFILLED_VISIBLE_SLOTS}
                  <nav class="wish-pagination" aria-label="Paginación de deseos privados cumplidos">
                    <button
                      class="wish-page-btn is-arrow"
                      type="button"
                      aria-label="Página anterior"
                      on:click={() => goToPrivateFulfilledPage(privateFulfilledPage - 1)}
                      disabled={privateFulfilledPage <= 1}
                    >
                      &lt;&lt;
                    </button>
                    {#each privateFulfilledPageNumbers as page}
                      <button
                        class={`wish-page-btn${page === privateFulfilledPage ? " is-active" : ""}`}
                        type="button"
                        aria-current={page === privateFulfilledPage ? "page" : undefined}
                        on:click={() => goToPrivateFulfilledPage(page)}
                      >
                        {page}
                      </button>
                    {/each}
                    <button
                      class="wish-page-btn is-arrow"
                      type="button"
                      aria-label="Página siguiente"
                      on:click={() => goToPrivateFulfilledPage(privateFulfilledPage + 1)}
                      disabled={privateFulfilledPage >= privateFulfilledTotalPages}
                    >
                      &gt;&gt;
                    </button>
                  </nav>
                {/if}
                {#if privateFulfilledLoading}
                  <p class="wish-fulfilled-status">Cargando deseos cumplidos...</p>
                {:else if privateFulfilledError}
                  <p class="wish-fulfilled-status is-error">{privateFulfilledError}</p>
                {:else if privateFulfilledTotal > 0 && privateFulfilledTotal >= PRIVATE_FULFILLED_VISIBLE_SLOTS}
                  <p class="wish-fulfilled-status">
                    Mostrando {privateFulfilledRangeStart}-{privateFulfilledRangeEnd} de {privateFulfilledTotal} deseos cumplidos.
                  </p>
                {/if}
              </article>
            </div>
          </section>

          <template id="private-wish-lamp-slot-template">
            <div class="wish-slot-row wish-slot-row-empty">
              <button class="wish-add-btn wish-lamp-btn" type="button" title="Agregar deseo">
                <img class="wish-lamp-icon" src="/css/icons/iconlamp.webp" alt="Agregar deseo" />
              </button>
            </div>
          </template>

          <div class="modal-overlay hidden" id="private-personal-wish-modal" aria-hidden="true">
            <div class="modal modal-wide personal-wish-modal" role="dialog" aria-modal="true"
              aria-label="Configurar deseo personal">
              <div class="modal-head">
                <h3>Configurar deseo personal</h3>
                <button class="modal-close" type="button" id="private-close-personal-wish-modal">✕</button>
              </div>
              <div class="modal-body personal-wish-body">
                <div class="wish-modal-grid">
                  <div class="wish-modal-col">
                    <div class="wish-config-icon personal-wish-hero">
                      <img src="/css/icons/iconpersonal.webp" alt="Deseo personal" />
                    </div>
                    <h2 class="modal-label modal-label-center">Descripción del deseo</h2>
                    <label class="modal-label hidden" for="private-personal-wish-text">Descripción del deseo</label>
                    <textarea class="modal-textarea wish-prefix-input wish-textarea-compact" id="private-personal-wish-text"
                      rows="3" maxlength="80" data-prefix="Deseo " data-counter="private-personal-wish-counter"></textarea>
                    <div class="wish-counter" id="private-personal-wish-counter" aria-live="polite">0/80</div>
                    <div class="wish-error" id="private-personal-wish-error" role="alert">No has descrito tu deseo</div>
                    <div class="wish-warning">
                      <span class="wish-warning-icon">!</span>
                      <span id="private-personal-wish-type-hint">
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
                        <img id="private-personal-wish-type-icon" src="/css/icons/Espiritual.webp" alt="Espiritual" />
                      </div>
                      <h2 class="modal-label modal-label-center">Tipo de deseo</h2>
                      <div class="wish-type-grid">
                        <label class="wish-type-option">
                          <input type="radio" name="private-personal-wish-type" value="Espiritual" checked />
                          <span class="wish-type-visual">
                            <span>Espiritual</span>
                          </span>
                        </label>
                        <label class="wish-type-option">
                          <input type="radio" name="private-personal-wish-type" value="Material" />
                          <span class="wish-type-visual">
                            <span>Material</span>
                          </span>
                        </label>
                        <label class="wish-type-option">
                          <input type="radio" name="private-personal-wish-type" value="Monetario" />
                          <span class="wish-type-visual">
                            <span>Monetario</span>
                          </span>
                        </label>
                        <label class="wish-type-option">
                          <input type="radio" name="private-personal-wish-type" value="Profesional" />
                          <span class="wish-type-visual">
                            <span>Profesional</span>
                          </span>
                        </label>
                        <label class="wish-type-option">
                          <input type="radio" name="private-personal-wish-type" value="Salud y cuerpo" />
                          <span class="wish-type-visual">
                            <span>Salud y cuerpo</span>
                          </span>
                        </label>
                        <label class="wish-type-option">
                          <input type="radio" name="private-personal-wish-type" value="Relacional" />
                          <span class="wish-type-visual">
                            <span>Relacional</span>
                          </span>
                        </label>
                        <label class="wish-type-option">
                          <input type="radio" name="private-personal-wish-type" value="Vivencial" />
                          <span class="wish-type-visual">
                            <span>Vivencial</span>
                          </span>
                        </label>
                      </div>
                    </fieldset>
                  </div>

                  <div class="wish-modal-col">
                    <h2 class="modal-label modal-label-center">Agregar imagen</h2>
                    <label class="modal-label hidden" for="private-personal-wish-media">Agregar imagen</label>
                    <input class="modal-input hidden" id="private-personal-wish-media" type="file" accept="image/*" />
                    <div class="wish-image-preview" id="private-personal-wish-preview" aria-live="polite">
                      <label class="wish-image-btn" for="private-personal-wish-media" aria-label="Seleccionar imagen">+</label>
                      <div class="wish-preview-content">
                        <span class="wish-preview-placeholder">Seleccionar imagen</span>
                        <span class="wish-preview-name" id="private-personal-wish-file-name">Sin imagen seleccionada</span>
                      </div>
                    </div>
                    <div class="wish-config-icon personal-wish-hero">
                      <img src="/css/icons/iconsave.webp" alt="guardar" />
                    </div>
                    <div class="wish-form-actions wish-form-actions-center">
                      <br>
                      <button class="btn btn-primary btn-compact btn-icon" type="button" id="private-confirm-personal-wish">
                        ¡Confirmar mi deseo!
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-overlay hidden" id="private-delete-wish-modal" aria-hidden="true">
            <div class="modal wish-modal delete-wish-modal" role="dialog" aria-modal="true" aria-label="Borrar deseo">
              <div class="modal-head">
                <h3>¿Estás seguro de que deseas borrar este deseo?</h3>
              </div>
              <div class="modal-actions">
                <button class="btn btn-primary btn-compact" type="button" id="private-confirm-delete-wish">Sí</button>
                <button class="btn btn-outline btn-compact" type="button" id="private-cancel-delete-wish">No</button>
              </div>
            </div>
          </div>

          <div class="modal-overlay hidden" id="private-fulfill-wish-modal" aria-hidden="true">
            <div class="modal wish-modal fulfill-wish-modal" role="dialog" aria-modal="true"
              aria-label="Subir evidencia">
              <div class="modal-head">
                <h3>¡Sube la evidencia!</h3>
              </div>
              <div class="modal-body">
                <input id="private-fulfill-evidence" type="file" accept="image/*" class="hidden" />
                <div class="wish-image-preview" id="private-fulfill-evidence-preview" aria-live="polite">
                  <label class="wish-image-btn" for="private-fulfill-evidence" aria-label="Sube la evidencia visual">+</label>
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
                <button class="btn btn-primary btn-compact" type="button" id="private-confirm-fulfill-wish">
                  Juro bajo verdad de juramento que este deseo se ha cumplido
                </button>
              </div>
              <div class="modal-actions">
                <button class="btn btn-outline btn-compact" type="button" id="private-cancel-fulfill-wish">Cancelar</button>
              </div>
            </div>
          </div>

          <div class="modal-overlay hidden" id="private-ican-confirm-modal" aria-hidden="true">
            <div class="modal wish-modal ican-confirm-modal" role="dialog" aria-modal="true"
              aria-label="Conceder deseo">
              <div class="modal-head">
                <h3>Yo puedo conceder ese deseo</h3>
              </div>
              <div class="modal-body">
                <p class="panel-muted">¿Estás seguro de que deseas cumplir este deseo?</p>
              </div>
              <div class="modal-actions">
                <button class="btn btn-primary btn-compact" type="button" id="private-ican-confirm-yes">Sí</button>
                <button class="btn btn-outline btn-compact" type="button" id="private-ican-confirm-no">No</button>
              </div>
            </div>
          </div>

          <div class="modal-overlay hidden" id="private-guardian-contact-modal" aria-hidden="true">
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
                <label class="modal-label hidden" for="private-guardian-reason-visitor">Describe por qué deseas conceder ese
                  deseo</label>
                <textarea class="modal-textarea" id="private-guardian-reason-visitor" rows="3"></textarea>

                <h2 class="guardian-section-title">Número telefónico</h2>
                <label class="modal-label hidden" for="private-guardian-phone-visitor">Número telefónico</label>
                <input class="modal-input" id="private-guardian-phone-visitor" type="tel" inputmode="tel"
                  placeholder="+57 300 000 0000" />

                <h2 class="guardian-section-title">E-mail</h2>
                <label class="modal-label hidden" for="private-guardian-email-visitor">E-mail</label>
                <input class="modal-input" id="private-guardian-email-visitor" type="email" placeholder="correo@ejemplo.com" />

                <h2 class="guardian-section-title">Evidencia</h2>
                <div class="upload-row">
                  <label class="upload-btn" for="private-guardian-evidence-visitor">Adjuntar imagen o video</label>
                  <input id="private-guardian-evidence-visitor" type="file" accept="image/*,video/*" class="hidden" />
                  <div class="upload-hint">Envíanos una evidencia de tu buena intención</div>
                </div>
              </div>
              <div class="modal-actions">
                <button class="btn btn-primary btn-compact" type="button">Enviar</button>
                <button class="btn btn-outline btn-compact" type="button" id="private-cancel-guardian-modal">Cancelar</button>
              </div>
            </div>
          </div>

        </section>
        </div>

        <!-- =========================
         *  SEGURIDAD / PRIVATE LOCK
         *  ========================= -->
        <section class="private-security-overlay" aria-label="Seguridad de deseos privados">
          <div class="private-security-card" role="dialog" aria-modal="true" aria-live="polite">
            <img class="private-security-hero" src="/css/cpp-key.webp" alt="Clave privada" />

            <h2 class="private-security-title">Digita tu contraseña privada personal:</h2>

            <div class="private-security-input-row">
              <label class="modal-label hidden" for="private-security-password">Contraseña privada</label>
              <input class="modal-input private-security-input" id="private-security-password" type="password"
                autocomplete="off" inputmode="text" placeholder="••••••••••••••" />
              <button class="private-security-btn private-security-unlock" type="button" id="private-security-unlock"
                aria-label="Ingresar" title="Ingresar">
                <img src="/css/icons/icondoor.webp" alt="Ingresar" />
              </button>
            </div>

            <p class="private-security-error" id="private-security-error" role="alert">
              Contraseña incorrecta. Inténtalo de nuevo.
            </p>

            <div class="private-security-actions">
              <button class="private-security-btn" type="button" aria-label="Modificar contraseña privada personal"
                id="private-security-change-password" title="Modificar contraseña privada personal">
                <img src="/css/icons/iconedit.webp" alt="Cambiar contraseña" />
              </button>
              <button class="private-security-btn" type="button" aria-label="Reiniciar contraseña"
                id="private-security-reset-password" title="Reiniciar contraseña">
                <img src="/css/icons/icondelete.webp" alt="Reiniciar contraseña" />
              </button>
            </div>

            <p class="private-security-note">
              Tu clave secreta personal protege toda la información privada que declares en esta red social: deseos,
              propósitos y datos confidenciales. Si la pierdes, no podrás recuperar el acceso a esa información. En caso
              de olvido, podrás reiniciar la clave, pero esto implicará la eliminación definitiva de todos tus deseos
              privados y datos confidenciales, los cuales deberán configurarse nuevamente. Sin esta clave, nadie puede
              acceder a tu información privada: ni el Guardián Supremo Absoluto ni las bases de datos de la red social
              tienen visibilidad sobre lo que has decidido mantener en secreto. Se recomienda guardar tu clave secreta
              —de forma digital o física— en un lugar seguro.
            </p>
          </div>
        </section>
      </div>
    </main>

    <div class="modal-overlay hidden" id="private-change-password-modal" aria-hidden="true">
      <div class="modal wish-modal private-change-password-modal" role="dialog" aria-modal="true" aria-label="Modificar contraseña privada personal">
        <div class="modal-head">
          <h3>Modificar contraseña privada personal</h3>
          <button class="modal-close" type="button" id="private-change-password-cancel">✕</button>
        </div>
        <div class="modal-body">
          <label class="modal-label" for="private-current-password">Digita tu actual contraseña privada personal</label>
          <input class="modal-input" id="private-current-password" type="password" autocomplete="off" />

          <label class="modal-label" for="private-new-password">Digita tu nueva contraseña privada personal</label>
          <input class="modal-input" id="private-new-password" type="password" autocomplete="off" />

          <label class="modal-label" for="private-confirm-password">Confirma tu nueva contraseña privada actual</label>
          <input class="modal-input" id="private-confirm-password" type="password" autocomplete="off" />

          <p class="private-security-error" id="private-change-password-error" role="alert"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-primary btn-compact" type="button" id="private-change-password-confirm">Confirmar</button>
          <button class="btn btn-outline btn-compact" type="button" id="private-change-password-cancel-footer">Cancelar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="private-reset-password-modal" aria-hidden="true">
      <div class="modal wish-modal private-reset-modal" role="dialog" aria-modal="true" aria-label="Restaurar contraseña privada personal">
        <div class="modal-head">
          <h3>Restaurar contraseña privada personal</h3>
          <button class="modal-close" type="button" id="private-reset-password-cancel">✕</button>
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
          <button class="btn btn-primary btn-compact" type="button" id="private-reset-password-confirm">Sí, continuar</button>
          <button class="btn btn-outline btn-compact" type="button" id="private-reset-password-cancel-footer">Cancelar</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay hidden" id="private-reset-password-final-modal" aria-hidden="true">
      <div class="modal wish-modal private-reset-modal" role="dialog" aria-modal="true" aria-label="Confirmación final de eliminación">
        <div class="modal-head">
          <h3>Confirmación final</h3>
          <button class="modal-close" type="button" id="private-reset-password-final-cancel">✕</button>
        </div>
        <div class="modal-body">
          <p class="private-reset-text">
            Para confirmar la eliminación de tu clave secreta personal, escribe la siguiente palabra exactamente como se muestra:
          </p>
          <p class="private-reset-text private-reset-keyword" id="private-reset-keyword-label">ELIMINAR</p>
          <input class="modal-input" id="private-reset-password-keyword" type="text" autocomplete="off" />

          <p class="private-security-error" id="private-reset-password-error" role="alert"></p>
        </div>
        <div class="modal-actions">
          <button class="btn btn-primary btn-compact" type="button" id="private-reset-password-final-confirm">Eliminar clave</button>
          <button class="btn btn-outline btn-compact" type="button" id="private-reset-password-final-cancel-footer">Cancelar</button>
        </div>
      </div>
    </div>

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
            <li><a href="/downloadapp.html">Descarga la app</a></li>
              <li><a href="/guardians-rank.html">Rangos de Guardianes</a></li>
              <li><a href="/be-a-guardian.html">Ser Guardián</a></li>
              <li><a href="/contact.html">Contacto</a></li>
            </ul>
          </div>

          <div class="footer-column">
            <h4>Idiomas</h4>
            <ul>
              <li><a href="/?lang=es">Español</a></li>
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
</div>
