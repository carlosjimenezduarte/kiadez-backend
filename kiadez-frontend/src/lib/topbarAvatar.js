const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") ||
  "http://127.0.0.1:8000";

const DEFAULT_AVATAR_SRC = "/assets/avatar-default.jpg";
const AVATAR_CACHE_KEY = "kiadez_profile_avatar_url";

const getAccessToken = () =>
  localStorage.getItem("access_token") ||
  localStorage.getItem("kiadez_access_token") ||
  "";

const parseJsonSafe = async (response) => {
  try {
    return await response.json();
  } catch {
    return {};
  }
};

const applyAvatarToTopbar = (url) => {
  const avatarUrl = (url || "").trim() || DEFAULT_AVATAR_SRC;
  document.querySelectorAll(".topbar-avatar-btn img").forEach((img) => {
    img.src = avatarUrl;
  });
};

export async function syncTopbarAvatar() {
  const cached = localStorage.getItem(AVATAR_CACHE_KEY) || "";
  if (cached) {
    applyAvatarToTopbar(cached);
  }

  const token = getAccessToken();
  if (!token) return cached || null;

  try {
    const response = await fetch(`${API_BASE_URL}/media/profile-photo`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 401) {
      return cached || null;
    }

    const data = await parseJsonSafe(response);
    if (!response.ok) {
      return cached || null;
    }

    const avatarUrl = (data?.url || "").trim() || DEFAULT_AVATAR_SRC;
    applyAvatarToTopbar(avatarUrl);
    localStorage.setItem(AVATAR_CACHE_KEY, avatarUrl);
    return avatarUrl;
  } catch {
    return cached || null;
  }
}
