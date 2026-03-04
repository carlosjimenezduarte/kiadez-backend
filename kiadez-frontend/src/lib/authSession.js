const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") ||
  "http://localhost:8000";

const ACCESS_TOKEN_KEYS = ["kiadez_access_token", "access_token"];
const REFRESH_TOKEN_KEY = "refresh_token";

let refreshPromise = null;
let interceptorInstalled = false;

function getAccessToken() {
  for (const key of ACCESS_TOKEN_KEYS) {
    const token = localStorage.getItem(key);
    if (token && token.trim()) return token.trim();
  }
  return "";
}

function setAccessToken(token) {
  const value = String(token || "").trim();
  if (!value) return;
  for (const key of ACCESS_TOKEN_KEYS) {
    localStorage.setItem(key, value);
  }
}

function getRefreshToken() {
  const token = localStorage.getItem(REFRESH_TOKEN_KEY);
  return token && token.trim() ? token.trim() : "";
}

function setRefreshToken(token) {
  const value = String(token || "").trim();
  if (!value) return;
  localStorage.setItem(REFRESH_TOKEN_KEY, value);
}

function clearStoredSession() {
  for (const key of ACCESS_TOKEN_KEYS) {
    localStorage.removeItem(key);
  }
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

function getRequestUrl(input) {
  if (typeof input === "string") return input;
  if (input instanceof URL) return input.toString();
  if (input instanceof Request) return input.url;
  return "";
}

function isApiRequest(url) {
  try {
    const absolute = new URL(url, window.location.origin).toString();
    return absolute === API_BASE_URL || absolute.startsWith(`${API_BASE_URL}/`);
  } catch {
    return false;
  }
}

function isRefreshEndpoint(url) {
  try {
    const parsed = new URL(url, window.location.origin);
    const api = new URL(API_BASE_URL, window.location.origin);
    return parsed.origin === api.origin && parsed.pathname === "/auth/refresh";
  } catch {
    return false;
  }
}

function hasAuthorizationHeader(input, init) {
  const initHeaders = new Headers(init?.headers || undefined);
  if (initHeaders.has("Authorization")) return true;
  if (input instanceof Request) {
    const reqHeaders = new Headers(input.headers || undefined);
    return reqHeaders.has("Authorization");
  }
  return false;
}

async function refreshAccessToken(originalFetch) {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return false;

  if (!refreshPromise) {
    refreshPromise = (async () => {
      try {
        const response = await originalFetch(`${API_BASE_URL}/auth/refresh`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });

        if (!response.ok) {
          clearStoredSession();
          return false;
        }

        let payload = {};
        try {
          payload = await response.json();
        } catch {
          payload = {};
        }

        const newAccess = String(payload?.access_token || "").trim();
        const newRefresh = String(payload?.refresh_token || "").trim();
        if (!newAccess || !newRefresh) {
          clearStoredSession();
          return false;
        }

        setAccessToken(newAccess);
        setRefreshToken(newRefresh);
        return true;
      } catch {
        clearStoredSession();
        return false;
      } finally {
        refreshPromise = null;
      }
    })();
  }

  return refreshPromise;
}

function withUpdatedAuthorization(input, init, accessToken) {
  const nextToken = String(accessToken || "").trim();
  if (!nextToken) return { input, init };

  if (input instanceof Request) {
    const headers = new Headers(input.headers || undefined);
    headers.set("Authorization", `Bearer ${nextToken}`);
    return { input: new Request(input, { headers }), init: undefined };
  }

  const nextInit = { ...(init || {}) };
  const headers = new Headers(nextInit.headers || undefined);
  headers.set("Authorization", `Bearer ${nextToken}`);
  nextInit.headers = headers;
  return { input, init: nextInit };
}

export function installAuthSessionInterceptor() {
  if (interceptorInstalled || typeof window === "undefined") return;
  interceptorInstalled = true;

  const originalFetch = window.fetch.bind(window);

  window.fetch = async (input, init) => {
    const url = getRequestUrl(input);
    if (!url || !isApiRequest(url) || isRefreshEndpoint(url)) {
      return originalFetch(input, init);
    }

    const requiresAuth = hasAuthorizationHeader(input, init);
    const retryInput = input instanceof Request ? input.clone() : input;

    const response = await originalFetch(input, init);
    if (response.status !== 401 || !requiresAuth) {
      return response;
    }

    const refreshed = await refreshAccessToken(originalFetch);
    if (!refreshed) return response;

    const freshAccessToken = getAccessToken();
    if (!freshAccessToken) return response;

    const retried = withUpdatedAuthorization(retryInput, init, freshAccessToken);
    return originalFetch(retried.input, retried.init);
  };
}
