const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export function getAccessToken() {
  return localStorage.getItem('discipline_access_token');
}

export function getRefreshToken() {
  return localStorage.getItem('discipline_refresh_token');
}

export function setTokens(access, refresh) {
  if (access) localStorage.setItem('discipline_access_token', access);
  if (refresh) localStorage.setItem('discipline_refresh_token', refresh);
}

export function clearTokens() {
  localStorage.removeItem('discipline_access_token');
  localStorage.removeItem('discipline_refresh_token');
}

async function request(path, { method = 'GET', body, auth = true } = {}) {
  const headers = { 'Content-Type': 'application/json' };

  if (auth) {
    const token = getAccessToken();
    if (token) headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const message =
      errorData?.detail ||
      errorData?.message ||
      Object.values(errorData || {})?.[0]?.[0] ||
      `Request failed with status ${response.status}`;

    const error = new Error(message);
    error.status = response.status;
    error.data = errorData;
    throw error;
  }

  return response.json();
}

export async function login(username, password) {
  return request('/api/auth/token/', {
    method: 'POST',
    body: { username, password },
    auth: false,
  });
}

export async function signup(username, password) {
  return request('/api/auth/signup/', {
    method: 'POST',
    body: { username, password },
    auth: false,
  });
}

export async function refreshAccessToken() {
  const refresh = getRefreshToken();
  if (!refresh) throw new Error('No refresh token available');

  return request('/api/auth/token/refresh/', {
    method: 'POST',
    body: { refresh },
    auth: false,
  });
}

async function authedRequest(path, options = {}) {
  try {
    return await request(path, { ...options, auth: true });
  } catch (error) {
    if (error.status !== 401) throw error;

    const tokenData = await refreshAccessToken();
    setTokens(tokenData.access, tokenData.refresh);

    return request(path, { ...options, auth: true });
  }
}

export async function getPlayerMe() {
  return authedRequest('/api/player/me/');
}

export async function getQuests() {
  return authedRequest('/api/quests/');
}

export async function completeQuest(questId) {
  return authedRequest('/api/quests/complete/', {
    method: 'POST',
    body: { quest_id: questId },
  });
}
