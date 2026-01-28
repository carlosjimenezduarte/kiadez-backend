const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, '') ||
  'http://127.0.0.1:8000';

const TOKEN_KEY = 'kiadez_access_token';

export function setAccessToken(token) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

export function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function clearAccessToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request(path, { method = 'GET', token, body, headers } = {}) {
  const fetchHeaders = {
    ...(body ? { 'Content-Type': 'application/json' } : {}),
    ...(headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const res = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: fetchHeaders,
    body: body ? JSON.stringify(body) : undefined,
  });

  const isJson = res.headers.get('content-type')?.includes('application/json');
  const payload = isJson ? await res.json() : null;

  if (!res.ok) {
    const message = payload?.detail || payload?.message || res.statusText;
    throw new Error(message);
  }

  return payload;
}

export const authApi = {
  register(data) {
    return request('/auth/register', { method: 'POST', body: data });
  },
  login(data) {
    return request('/auth/login', { method: 'POST', body: data });
  },
  verify2fa({ temp_token, code }) {
    return request('/auth/2fa/verify', {
      method: 'POST',
      headers: { Authorization: `Bearer ${temp_token}` },
      body: { code },
    });
  },
  requestPasswordReset({ email }) {
    return request('/auth/password-reset/request', {
      method: 'POST',
      body: { email },
    });
  },
  confirmPasswordReset({ token, new_password }) {
    return request('/auth/password-reset/confirm', {
      method: 'POST',
      body: { token, new_password },
    });
  },
};

export const supportApi = {
  contact({ name, email, message }) {
    return request('/support/contact', {
      method: 'POST',
      body: { name, email, message },
    });
  },
};

export const mediaApi = {
  presignUpload({ filename, content_type, size_bytes, visibility }) {
    return request('/media/presign/upload', {
      method: 'POST',
      token: getAccessToken(),
      body: { filename, content_type, size_bytes, visibility },
    });
  },
  confirmUpload({ media_id, title, text, published_at, duration_seconds, width, height }) {
    return request('/media/confirm', {
      method: 'POST',
      token: getAccessToken(),
      body: {
        media_id,
        title,
        text,
        published_at,
        duration_seconds,
        width,
        height,
      },
    });
  },
  getMediaUrl(mediaId) {
    return request(`/media/${mediaId}`, { token: getAccessToken() });
  },
  deleteMedia(mediaId) {
    return request(`/media/${mediaId}`, {
      method: 'DELETE',
      token: getAccessToken(),
    });
  },
};

export async function uploadToPresignedUrl({ upload_url, file, content_type }) {
  const res = await fetch(upload_url, {
    method: 'PUT',
    headers: {
      'Content-Type': content_type,
    },
    body: file,
  });

  if (!res.ok) {
    throw new Error('Error subiendo archivo a storage.');
  }

  return res;
}
