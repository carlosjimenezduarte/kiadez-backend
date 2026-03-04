import { clearDekSession } from "./dekSession";

// Frontend-only logout: clears local tokens + sensitive session state, then redirects to login.
// Accepts either an event object (on:click={logout}) or an options object ({ redirectTo }).
export function logout(arg) {
  const redirectTo =
    arg &&
    typeof arg === "object" &&
    "redirectTo" in arg &&
    typeof arg.redirectTo === "string" &&
    arg.redirectTo.trim()
      ? arg.redirectTo
      : "/login.html";

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
