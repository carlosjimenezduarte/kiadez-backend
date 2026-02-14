// Frontend-only logout: clears local tokens + sensitive session state, then redirects to login.
// Note: signature supports being used directly as an event handler (Svelte passes the event object).
export function logout({ redirectTo = "/login.html" } = {}) {
  try {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("kiadez_access_token");

    // Remove cached purpose content (can include sensitive plaintext in some flows).
    localStorage.removeItem("kiadez_user_purpose");
  } catch {
    // Ignore storage errors.
  }

  try {
    // DEK is session-scoped; remove it on logout.
    sessionStorage.removeItem("dek_hex");
  } catch {
    // Ignore storage errors.
  }

  window.location.href = redirectTo;
}

