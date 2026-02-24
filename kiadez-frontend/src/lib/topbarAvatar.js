const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") ||
  "http://127.0.0.1:8000";

const DEFAULT_AVATAR_SRC = "/assets/avatar-default.jpg";

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
  applyAvatarToTopbar(DEFAULT_AVATAR_SRC);

  const token = getAccessToken();
  if (!token) return null;

  try {
    const response = await fetch(`${API_BASE_URL}/media/profile-photo`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 401) {
      return null;
    }

    const data = await parseJsonSafe(response);
    if (!response.ok) {
      return null;
    }

    const avatarUrl = (data?.url || "").trim() || DEFAULT_AVATAR_SRC;
    applyAvatarToTopbar(avatarUrl);
    return avatarUrl;
  } catch {
    return null;
  }
}
