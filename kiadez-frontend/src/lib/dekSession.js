const SESSION_KEY = "kiadez_dek_session_v1";
const LEGACY_SESSION_KEY = "dek_hex";
const DEFAULT_TTL_MS = 45 * 60 * 1000;

const normalizeHex = (value) => String(value || "").trim().toLowerCase();

const isValidHex = (value) => /^[0-9a-f]+$/.test(value) && value.length % 2 === 0;

const decodeBase64Url = (value) => {
  const normalized = String(value || "").replace(/-/g, "+").replace(/_/g, "/");
  const padded = normalized + "=".repeat((4 - (normalized.length % 4 || 4)) % 4);
  return atob(padded);
};

const getAccessToken = () =>
  localStorage.getItem("access_token") ||
  localStorage.getItem("kiadez_access_token") ||
  "";

const getCurrentUserSub = () => {
  const token = getAccessToken();
  if (!token || !token.includes(".")) return "";
  try {
    const payloadPart = token.split(".")[1] || "";
    const payloadJson = decodeBase64Url(payloadPart);
    const payload = JSON.parse(payloadJson);
    return String(payload?.sub || "").trim();
  } catch {
    return "";
  }
};

const persistState = (state) => {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(state));
};

const clearLegacyKey = () => {
  try {
    sessionStorage.removeItem(LEGACY_SESSION_KEY);
  } catch {
    // no-op
  }
};

const loadStructuredState = () => {
  try {
    const raw = sessionStorage.getItem(SESSION_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    const dekHex = normalizeHex(parsed?.dek_hex);
    const expiresAt = Number(parsed?.expires_at || 0);
    if (!dekHex || !isValidHex(dekHex) || !Number.isFinite(expiresAt) || expiresAt <= 0) {
      return null;
    }
    return {
      dek_hex: dekHex,
      user_sub: String(parsed?.user_sub || "").trim() || "",
      expires_at: expiresAt,
      updated_at: Number(parsed?.updated_at || 0) || 0,
    };
  } catch {
    return null;
  }
};

const migrateLegacyIfNeeded = () => {
  const legacy = normalizeHex(sessionStorage.getItem(LEGACY_SESSION_KEY));
  if (!legacy || !isValidHex(legacy)) return null;
  setDekSessionHex(legacy);
  clearLegacyKey();
  return loadStructuredState();
};

export const clearDekSession = () => {
  try {
    sessionStorage.removeItem(SESSION_KEY);
  } catch {
    // no-op
  }
  clearLegacyKey();
};

export const setDekSessionHex = (dekHex, { ttlMs = DEFAULT_TTL_MS } = {}) => {
  const normalized = normalizeHex(dekHex);
  const ttl = Number(ttlMs);
  if (!normalized || !isValidHex(normalized) || !Number.isFinite(ttl) || ttl <= 0) {
    return false;
  }
  const now = Date.now();
  const state = {
    dek_hex: normalized,
    user_sub: getCurrentUserSub(),
    expires_at: now + ttl,
    updated_at: now,
  };
  persistState(state);
  clearLegacyKey();
  return true;
};

export const getDekSessionHex = ({ renewTtl = true } = {}) => {
  let state = loadStructuredState();
  if (!state) {
    state = migrateLegacyIfNeeded();
  }
  if (!state) return "";

  const now = Date.now();
  if (state.expires_at <= now) {
    clearDekSession();
    return "";
  }

  const currentSub = getCurrentUserSub();
  if (state.user_sub && currentSub && state.user_sub !== currentSub) {
    clearDekSession();
    return "";
  }

  if (renewTtl) {
    state.expires_at = now + DEFAULT_TTL_MS;
    state.updated_at = now;
    persistState(state);
  }
  return state.dek_hex;
};
