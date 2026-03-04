let toastHost = null;

const ensureToastHost = () => {
  if (toastHost && document.body.contains(toastHost)) return toastHost;

  toastHost = document.createElement("div");
  toastHost.className = "kiadez-feedback-toast-host";
  toastHost.setAttribute("aria-live", "polite");
  toastHost.setAttribute("aria-atomic", "true");
  document.body.appendChild(toastHost);
  return toastHost;
};

const normalizeMessage = (message, fallback = "Acción completada.") => {
  const text = String(message || "").trim();
  return text || fallback;
};

export const showUiToast = (message, { type = "info", durationMs = 3600 } = {}) => {
  if (typeof window === "undefined" || typeof document === "undefined") return;

  const host = ensureToastHost();
  const toast = document.createElement("article");
  const variant = String(type || "info").toLowerCase();

  toast.className = `kiadez-feedback-toast is-${variant}`;
  toast.setAttribute("role", variant === "error" ? "alert" : "status");
  toast.textContent = normalizeMessage(message, "Listo.");
  host.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.add("is-visible");
  });

  const hide = () => {
    toast.classList.remove("is-visible");
    setTimeout(() => {
      toast.remove();
    }, 180);
  };

  const timeout = Number(durationMs);
  const finalDuration = Number.isFinite(timeout) && timeout > 500 ? timeout : 3600;
  window.setTimeout(hide, finalDuration);
};

export const showUiAlert = (message, options = {}) => {
  const type = options?.type || "info";
  showUiToast(message, { ...options, type });
};

const createDialog = ({
  title = "Confirmación",
  message = "",
  confirmLabel = "Confirmar",
  cancelLabel = "Cancelar",
  danger = false,
  withInput = false,
  inputPlaceholder = "",
  inputValue = "",
}) =>
  new Promise((resolve) => {
    if (typeof window === "undefined" || typeof document === "undefined") {
      resolve(withInput ? null : false);
      return;
    }

    const overlay = document.createElement("div");
    overlay.className = "modal-overlay kiadez-feedback-overlay";
    overlay.setAttribute("aria-hidden", "false");

    const modal = document.createElement("div");
    modal.className = "modal kiadez-feedback-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-label", normalizeMessage(title, "Confirmación"));

    const head = document.createElement("div");
    head.className = "modal-head";
    const titleEl = document.createElement("h3");
    titleEl.textContent = normalizeMessage(title, "Confirmación");
    const closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "modal-close";
    closeBtn.setAttribute("aria-label", "Cerrar");
    closeBtn.textContent = "✕";
    head.appendChild(titleEl);
    head.appendChild(closeBtn);

    const body = document.createElement("div");
    body.className = "modal-body";
    const text = document.createElement("p");
    text.className = "panel-text";
    text.textContent = normalizeMessage(message, "");
    body.appendChild(text);

    let input = null;
    if (withInput) {
      input = document.createElement("input");
      input.type = "text";
      input.className = "modal-input kiadez-feedback-input";
      input.placeholder = String(inputPlaceholder || "");
      input.value = String(inputValue || "");
      body.appendChild(input);
    }

    const actions = document.createElement("div");
    actions.className = "modal-actions";
    const cancelBtn = document.createElement("button");
    cancelBtn.type = "button";
    cancelBtn.className = "btn btn-outline btn-compact";
    cancelBtn.textContent = normalizeMessage(cancelLabel, "Cancelar");

    const confirmBtn = document.createElement("button");
    confirmBtn.type = "button";
    confirmBtn.className = danger
      ? "btn btn-primary btn-compact kiadez-feedback-danger-btn"
      : "btn btn-primary btn-compact";
    confirmBtn.textContent = normalizeMessage(confirmLabel, "Confirmar");

    actions.appendChild(cancelBtn);
    actions.appendChild(confirmBtn);

    modal.appendChild(head);
    modal.appendChild(body);
    modal.appendChild(actions);
    overlay.appendChild(modal);
    document.body.appendChild(overlay);

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    let resolved = false;
    const finish = (value) => {
      if (resolved) return;
      resolved = true;
      document.removeEventListener("keydown", onKeyDown, true);
      document.body.style.overflow = previousOverflow;
      overlay.remove();
      resolve(value);
    };

    const cancel = () => finish(withInput ? null : false);
    const confirm = () => {
      if (withInput) {
        finish(String(input?.value || ""));
        return;
      }
      finish(true);
    };

    const onKeyDown = (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        cancel();
        return;
      }
      if (event.key === "Enter") {
        event.preventDefault();
        confirm();
      }
    };

    closeBtn.addEventListener("click", cancel);
    cancelBtn.addEventListener("click", cancel);
    confirmBtn.addEventListener("click", confirm);
    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) cancel();
    });
    document.addEventListener("keydown", onKeyDown, true);

    if (input) {
      requestAnimationFrame(() => input?.focus());
    } else {
      requestAnimationFrame(() => confirmBtn.focus());
    }
  });

export const showUiConfirm = async (
  message,
  { title = "Confirmación", confirmLabel = "Confirmar", cancelLabel = "Cancelar", danger = false } = {}
) => {
  const result = await createDialog({
    title,
    message,
    confirmLabel,
    cancelLabel,
    danger,
    withInput: false,
  });
  return Boolean(result);
};

export const showUiPrompt = async (
  message,
  {
    title = "Ingresa un valor",
    placeholder = "",
    defaultValue = "",
    confirmLabel = "Aceptar",
    cancelLabel = "Cancelar",
  } = {}
) => {
  const result = await createDialog({
    title,
    message,
    confirmLabel,
    cancelLabel,
    withInput: true,
    inputPlaceholder: placeholder,
    inputValue: defaultValue,
  });
  if (result === null) return null;
  return String(result || "");
};

