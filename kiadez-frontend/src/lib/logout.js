import { clearDekSession } from "./dekSession";

// Frontend-only logout: clears local tokens + sensitive session state, then redirects to login.
// Supports both direct usage as event handler (`on:click={logout}`) and manual invocation
// (`logout({ redirectTo: "/somewhere" })`).
/**
 * @param {{ redirectTo?: string } | Event | undefined} arg
 */
export function logout(arg) {
  let redirectTo = "/login.html";

  if (
    arg &&
    typeof arg === "object" &&
    "redirectTo" in arg &&
    typeof arg.redirectTo === "string" &&
    arg.redirectTo.trim()
  ) {
    redirectTo = arg.redirectTo;
  }

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
