<script>
  import { onMount } from "svelte";
  import { getDekSessionHex } from "../lib/dekSession";

  onMount(() => {
    const API = "http://127.0.0.1:8000";
        const token = localStorage.getItem("access_token") || "";
        if (!token) {
          window.location.href = "/login.html";
          return;
        }

        void (async () => {
          try {
            const res = await fetch(`${API}/life-purpose/mine`, {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            });
            const data = await res.json();
            if (!res.ok) return;
            const slots = Array.isArray(data?.slots) ? data.slots : [];
            const slotNumbers = new Set(
              slots
                .map((slot) => Number(slot?.slot_number))
                .filter((n) => Number.isFinite(n) && n >= 1 && n <= 3)
            );
            if (slotNumbers.size >= 3) {
              window.location.href = "/home_user.html";
            }
          } catch (error) {
            console.error("Could not validate life purpose onboarding", error);
          }
        })();

        const AAD_PURPOSE = new TextEncoder().encode("kiadez-life-purpose-v1");
    
        function bufToHex(buf) {
          return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
        }
        function hexToBuf(hex) {
          const bytes = new Uint8Array(hex.length / 2);
          for (let i = 0; i < bytes.length; i++) bytes[i] = parseInt(hex.substr(i * 2, 2), 16);
          return bytes.buffer;
        }
    
        async function importDekFromSession() {
          const dekHex = getDekSessionHex();
          if (!dekHex) {
            throw new Error("Vault not unlocked. Create your private key or unlock it first.");
          }
          const dekRaw = hexToBuf(dekHex);
          return crypto.subtle.importKey(
            "raw",
            dekRaw,
            { name: "AES-GCM" },
            false,
            ["encrypt", "decrypt"]
          );
        }
    
        async function aesGcmEncrypt(key, plaintext, aadBuf) {
          const nonce = crypto.getRandomValues(new Uint8Array(12));
          const ptBuf = new TextEncoder().encode(plaintext).buffer;
    
          const ct = await crypto.subtle.encrypt(
            { name: "AES-GCM", iv: nonce, additionalData: aadBuf },
            key,
            ptBuf
          );
    
          return { nonce_hex: bufToHex(nonce.buffer), ciphertext_hex: bufToHex(ct) };
        }
    
        function setPurposeStatus(groupEl, text) {
          const statusEl = groupEl.querySelector(".purpose-status");
          if (statusEl) statusEl.textContent = text;
        }
    
        function getIconLabel(iconKey) {
          if (iconKey === "air") return "Air";
          if (iconKey === "earth") return "Earth";
          if (iconKey === "water") return "Water";
          if (iconKey === "fire") return "Fire";
          return "Icon";
        }
    
        function getIconSrc(iconKey) {
          return `assets/${iconKey}.png`;
        }

        const prefixInputs = document.querySelectorAll(".wish-prefix-input");
        prefixInputs.forEach((input) => {
          const field = /** @type {HTMLTextAreaElement} */ (input);
          const prefix = field.dataset.prefix || "Wish ";
          const maxLength = field.maxLength > 0 ? field.maxLength : null;

          const clampToMax = () => {
            if (maxLength && field.value.length > maxLength) {
              field.value = field.value.slice(0, maxLength);
            }
          };

          const ensurePrefix = () => {
            if (!field.value.startsWith(prefix)) {
              const cleaned = field.value.replace(prefix, "");
              field.value = `${prefix}${cleaned}`;
            }
            if (field.value.length < prefix.length) {
              field.value = prefix;
            }
            clampToMax();
          };

          ensurePrefix();

          field.addEventListener("focus", () => {
            if (field.value === prefix) {
              field.setSelectionRange(prefix.length, prefix.length);
            }
          });

          field.addEventListener("input", ensurePrefix);

          field.addEventListener("keydown", (event) => {
            const cursorStart = field.selectionStart || 0;
            if ((event.key === "Backspace" || event.key === "Delete") && cursorStart <= prefix.length) {
              event.preventDefault();
              field.setSelectionRange(prefix.length, prefix.length);
            }
          });
        });

        const confirmOverlay = document.getElementById("lifeConfirmOverlay");
        const confirmClose = document.getElementById("lifeConfirmClose");
        const confirmCancel = document.getElementById("lifeConfirmCancel");
        const confirmOk = document.getElementById("lifeConfirmOk");
        const confirmText = document.getElementById("lifeConfirmText");
        let pendingConfirmGroup = null;

        const openConfirmModal = (groupEl) => {
          pendingConfirmGroup = groupEl;
          if (confirmText) {
            const number = groupEl?.dataset?.purpose;
            confirmText.textContent = number
              ? `Confirm purpose ${number} as public?`
              : "Confirm this wish as public?";
          }
          confirmOverlay?.classList.remove("hidden");
          confirmOverlay?.setAttribute("aria-hidden", "false");
        };

        const closeConfirmModal = () => {
          confirmOverlay?.classList.add("hidden");
          confirmOverlay?.setAttribute("aria-hidden", "true");
          pendingConfirmGroup = null;
        };

        confirmClose?.addEventListener("click", closeConfirmModal);
        confirmCancel?.addEventListener("click", closeConfirmModal);
        confirmOverlay?.addEventListener("click", (event) => {
          if (event.target === confirmOverlay) closeConfirmModal();
        });

        confirmOk?.addEventListener("click", () => {
          if (!pendingConfirmGroup) {
            closeConfirmModal();
            return;
          }
          pendingConfirmGroup.dataset.isPrivate = "false";
          setPurposeStatus(pendingConfirmGroup, "Status: confirmed (public).");
          closeConfirmModal();
        });

        document.querySelectorAll(".purpose-group").forEach((groupEl) => {
          if (!groupEl.dataset.isPrivate) groupEl.dataset.isPrivate = "false";
        });
    
        document.querySelectorAll(".purpose-actions").forEach((actionRow) => {
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
              setPurposeStatus(groupEl, "Status: marked as secret.");
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
    
        document.querySelectorAll(".purpose-icon-panel").forEach((panel) => {
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
              actionBtn.title = `Icon: ${label}`;
            }
    
            setPurposeStatus(groupEl, `Status: associated icon: ${label}.`);
            panel.classList.remove("is-open");
          });
        });
    
        document.querySelectorAll(".purpose-date").forEach((dateInput) => {
          dateInput.addEventListener("change", () => {
            const groupEl = dateInput.closest(".purpose-group");
            groupEl.dataset.revealAt = dateInput.value || "";
            if (!dateInput.value) return;
            const formatted = dateInput.value.split("-").reverse().join("/");
            setPurposeStatus(groupEl, `Status: will be revealed on ${formatted}.`);
          });
        });
    
        document.getElementById("life-form").addEventListener("submit", async (e) => {
          e.preventDefault();
    
          const groups = [...document.querySelectorAll(".purpose-group")];
          const needsDek = groups.some((groupEl) => groupEl.dataset.isPrivate === "true");
    
          let dekKey = null;
          if (needsDek) {
            try {
              dekKey = await importDekFromSession();
            } catch (err) {
              alert(err.message);
              return;
            }
          }
    
          const slots = [];
          for (const groupEl of groups) {
            const textarea = groupEl.querySelector("textarea");
            const text = textarea.value.trim();
            if (!text) {
              alert("Complete all three purposes.");
              return;
            }
    
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
            } else {
              slots.push({
                slot_number: slotNumber,
                is_private: false,
                text_public: text,
                reveal_at: revealAt,
                icon_key: iconKey
              });
            }
          }
    
          const payload = { slots };
    
          try {
            const res = await fetch(`${API}/life-purpose/save`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`
              },
              body: JSON.stringify(payload)
            });
    
            const data = await res.json();
    
            if (!res.ok) {
              alert(data.detail || "Could not save the purpose.");
              return;
            }
    
            window.location.href = "/home_user.html";
    
          } catch (err) {
            console.error(err);
            alert("Server connection error.");
          }
        });
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Life purpose</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-backgroundlogin">

    <main class="auth-center">
      <div class="auth-card auth-card--wide auth-card--life">

        <h2 class="auth-title">Your life purpose</h2>

        <div class="auth-message">
          <p>
            Write three wishes to guide your path.
            <br>
            They are a compass, not pressure.
          </p>
          <p class="muted">
            These purposes are stored encrypted with your personal private key.
          </p>
        </div>

        <form id="life-form">
          <div class="purpose-group" data-purpose="1">
            <textarea id="p1" class="wish-prefix-input" data-prefix="Wish " rows="1" maxlength="80" placeholder="Wish 1" required>Wish </textarea>
            <div class="purpose-actions" role="group" aria-label="Actions for purpose 1">
              <button type="button" class="purpose-action" data-action="confirm" title="Confirm purpose wish" aria-label="Confirm purpose wish">
                <img src="/css/icons/iconsave.webp" alt="Save purpose">
              </button>
              <button type="button" class="purpose-action" data-action="secret" title="Mark as secret" aria-label="Mark as secret">
                <img src="/css/icons/iconkey.webp" alt="Mark as secret">
              </button>
              <button type="button" class="purpose-action" data-action="reveal" title="Reveal on date" aria-label="Reveal on date">
                <img src="/css/icons/iconcalendar.webp" alt="Schedule date">
              </button>
              <button type="button" class="purpose-action" data-action="icon" title="Choose icon" aria-label="Choose icon">
                <img src="/css/icons/iconelemental.webp" alt="Choose icon">
              </button>
            </div>
            <input type="date" class="purpose-date" aria-label="Reveal date for purpose 1">
            <div class="purpose-icon-panel" aria-label="Icon selector">
              <button type="button" class="purpose-icon" data-icon="air" title="Air">
                <img src="assets/air.png" alt="Air">
              </button>
              <button type="button" class="purpose-icon" data-icon="earth" title="Earth">
                <img src="assets/earth.png" alt="Earth">
              </button>
              <button type="button" class="purpose-icon" data-icon="water" title="Water">
                <img src="assets/water.png" alt="Water">
              </button>
              <button type="button" class="purpose-icon" data-icon="fire" title="Fire">
                <img src="assets/fire.png" alt="Fire">
              </button>
            </div>
            <div class="purpose-status" aria-live="polite">Status: public by default.</div>
          </div>

          <div class="purpose-group" data-purpose="2">
            <textarea id="p2" class="wish-prefix-input" data-prefix="Wish " rows="1" maxlength="80" placeholder="Wish 2" required>Wish </textarea>
            <div class="purpose-actions" role="group" aria-label="Actions for purpose 2">
              <button type="button" class="purpose-action" data-action="confirm" title="Confirm purpose wish" aria-label="Confirm purpose wish">
                <img src="/css/icons/iconsave.webp" alt="Save purpose">
              </button>
              <button type="button" class="purpose-action" data-action="secret" title="Mark as secret" aria-label="Mark as secret">
                <img src="/css/icons/iconkey.webp" alt="Mark as secret">
              </button>
              <button type="button" class="purpose-action" data-action="reveal" title="Reveal on date" aria-label="Reveal on date">
                <img src="/css/icons/iconcalendar.webp" alt="Schedule date">
              </button>
              <button type="button" class="purpose-action" data-action="icon" title="Choose icon" aria-label="Choose icon">
                <img src="/css/icons/iconelemental.webp" alt="Choose icon">
              </button>
            </div>
            <input type="date" class="purpose-date" aria-label="Reveal date for purpose 2">
            <div class="purpose-icon-panel" aria-label="Icon selector">
              <button type="button" class="purpose-icon" data-icon="air" title="Air">
                <img src="assets/air.png" alt="Air">
              </button>
              <button type="button" class="purpose-icon" data-icon="earth" title="Earth">
                <img src="assets/earth.png" alt="Earth">
              </button>
              <button type="button" class="purpose-icon" data-icon="water" title="Water">
                <img src="assets/water.png" alt="Water">
              </button>
              <button type="button" class="purpose-icon" data-icon="fire" title="Fire">
                <img src="assets/fire.png" alt="Fire">
              </button>
            </div>
            <div class="purpose-status" aria-live="polite">Status: public by default.</div>
          </div>

          <div class="purpose-group" data-purpose="3">
            <textarea id="p3" class="wish-prefix-input" data-prefix="Wish " rows="1" maxlength="80" placeholder="Wish 3" required>Wish </textarea>
            <div class="purpose-actions" role="group" aria-label="Actions for purpose 3">
              <button type="button" class="purpose-action" data-action="confirm" title="Confirm purpose wish" aria-label="Confirm purpose wish">
                <img src="/css/icons/iconsave.webp" alt="Save purpose">
              </button>
              <button type="button" class="purpose-action" data-action="secret" title="Mark as secret" aria-label="Mark as secret">
                <img src="/css/icons/iconkey.webp" alt="Mark as secret">
              </button>
              <button type="button" class="purpose-action" data-action="reveal" title="Reveal on date" aria-label="Reveal on date">
                <img src="/css/icons/iconcalendar.webp" alt="Schedule date">
              </button>
              <button type="button" class="purpose-action" data-action="icon" title="Choose icon" aria-label="Choose icon">
                <img src="/css/icons/iconelemental.webp" alt="Choose icon">
              </button>
            </div>
            <input type="date" class="purpose-date" aria-label="Reveal date for purpose 3">
            <div class="purpose-icon-panel" aria-label="Icon selector">
              <button type="button" class="purpose-icon" data-icon="air" title="Air">
                <img src="assets/air.png" alt="Air">
              </button>
              <button type="button" class="purpose-icon" data-icon="earth" title="Earth">
                <img src="assets/earth.png" alt="Earth">
              </button>
              <button type="button" class="purpose-icon" data-icon="water" title="Water">
                <img src="assets/water.png" alt="Water">
              </button>
              <button type="button" class="purpose-icon" data-icon="fire" title="Fire">
                <img src="assets/fire.png" alt="Fire">
              </button>
            </div>
            <div class="purpose-status" aria-live="polite">Status: public by default.</div>
          </div>

          <button type="submit" class="btn btn-primary">Save purpose</button>
          <a href="/create-private-key.html" class="btn btn-outline">Back</a>
        </form>

        <div class="auth-brand">
          <img src="/css/logo-kiadez.webp" alt="Kiadez" />
          <span>Kiadez</span>
        </div>

      </div>
    </main>

    <div class="modal-overlay hidden" id="lifeConfirmOverlay" aria-hidden="true">
      <div class="modal" role="dialog" aria-modal="true" aria-label="Confirm public purpose">
        <div class="modal-head">
          <h3>Confirm purpose</h3>
          <button class="modal-close" type="button" id="lifeConfirmClose">✕</button>
        </div>

        <div class="modal-body">
          <p class="modal-label-center" id="lifeConfirmText">
            Confirm this wish as public?
          </p>
          <p class="modal-label-center muted">
            It will be saved as public.
          </p>
        </div>

        <div class="modal-actions">
          <button class="btn btn-outline btn-compact" type="button" id="lifeConfirmCancel">Cancel</button>
          <button class="btn btn-primary btn-compact" type="button" id="lifeConfirmOk">Confirm</button>
        </div>
      </div>
    </div>

    <footer class="kiadez-footer">
      <div class="footer-bottom">
        © 2026 Kiadez — A social network to fulfill wishes.
      </div>
    </footer>

  </div>
