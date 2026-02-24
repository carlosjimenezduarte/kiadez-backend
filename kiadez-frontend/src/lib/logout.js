import { clearDekSession } from "./dekSession";

// Frontend-only logout: clears local tokens + sensitive session state, then redirects to login.
// Note: signature supports being used directly as an event handler (Svelte passes the event object).
export function logout({ redirectTo = "/login.html" } = {}) {
  try {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("kiadez_access_token");

  } catch {
    // Ignore storage errors.
  }

  try {
    clearDekSession();
  } catch {
    // Ignore storage errors.
  }

  window.location.href = redirectTo;
}
