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

function buildErrorMessage(errorData, status) {
  if (!errorData) return `Request failed with status ${status}`;

  if (typeof errorData.detail === 'string') return errorData.detail;
  if (typeof errorData.message === 'string') return errorData.message;

  const firstEntry = Object.values(errorData)[0];
  if (Array.isArray(firstEntry) && firstEntry.length > 0) return String(firstEntry[0]);
  if (typeof firstEntry === 'string') return firstEntry;

  return `Request failed with status ${status}`;
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
    const error = new Error(buildErrorMessage(errorData, response.status));
    error.status = response.status;
    error.data = errorData;
    throw error;
  }

  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('application/json')) {
    return null;
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

  if (!refresh) {
    const error = new Error('Your session has expired. Please log in again.');
    error.status = 401;
    throw error;
  }

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

    try {
      const tokenData = await refreshAccessToken();
      setTokens(tokenData.access, tokenData.refresh);
    } catch {
      clearTokens();
      const authError = new Error('Your session has expired. Please log in again.');
      authError.status = 401;
      throw authError;
    }

    return request(path, { ...options, auth: true });
  }
}

export async function getPlayerMe() {
  return authedRequest('/api/player/me/');
}

export async function updatePlayerPath(path) {
  return authedRequest('/api/player/path/', {
    method: 'PATCH',
    body: { path },
  });
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

export async function getSocialPosts() {
  return authedRequest('/api/social/posts/');
}

export async function getSocialPost(postId) {
  return authedRequest(`/api/social/posts/${postId}/`);
}

export async function createSocialPost({ content, visibility }) {
  return authedRequest('/api/social/posts/', {
    method: 'POST',
    body: {
      content,
      visibility,
      post_type: 'update',
    },
  });
}

export async function getPostComments(postId) {
  return authedRequest(`/api/social/posts/${postId}/comments/`);
}

export async function createPostComment(postId, content) {
  return authedRequest(`/api/social/posts/${postId}/comments/`, {
    method: 'POST',
    body: { content },
  });
}

export async function updatePostComment(postId, commentId, content) {
  return authedRequest(`/api/social/posts/${postId}/comments/${commentId}/`, {
    method: 'PATCH',
    body: { content },
  });
}

export async function deletePostComment(postId, commentId) {
  return authedRequest(`/api/social/posts/${postId}/comments/${commentId}/`, {
    method: 'DELETE',
  });
}

export async function setPostReaction(postId, reactionType) {
  return authedRequest(`/api/social/posts/${postId}/reaction/`, {
    method: 'PUT',
    body: { reaction_type: reactionType },
  });
}

export async function removePostReaction(postId) {
  return authedRequest(`/api/social/posts/${postId}/reaction/`, {
    method: 'DELETE',
  });
}
