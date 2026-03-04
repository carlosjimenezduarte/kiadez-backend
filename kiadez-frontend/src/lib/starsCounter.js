const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") ||
  "http://localhost:8000";

const parseJsonSafe = async (response) => {
  try {
    return await response.json();
  } catch {
    return {};
  }
};

const getAccessToken = () =>
  localStorage.getItem("access_token") ||
  localStorage.getItem("kiadez_access_token") ||
  "";

export async function syncProfileStarsTotal(elementId, { onError } = {}) {
  const label = document.getElementById(elementId);
  if (!label) return null;

  const token = getAccessToken();
  if (!token) return null;

  try {
    const response = await fetch(`${API_BASE_URL}/posts/me/stats`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      return null;
    }

    const data = await parseJsonSafe(response);
    if (!response.ok) {
      throw new Error(data.detail || "No se pudieron cargar tus estrellas.");
    }

    const stars = Number(data.my_received_stars_total || 0);
    label.textContent = stars.toLocaleString("es-CO");
    return stars;
  } catch (error) {
    if (typeof onError === "function") {
      onError(error);
    }
    return null;
  }
}
