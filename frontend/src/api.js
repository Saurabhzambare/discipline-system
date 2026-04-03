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

export async function getDailyLineup(date) {
  const query = date ? `?date=${encodeURIComponent(date)}` : '';
  return authedRequest(`/api/quests/daily/${query}`);
}

export async function completeLineupItem(itemId) {
  return authedRequest('/api/quests/daily/complete/', {
    method: 'POST',
    body: { item_id: itemId },
  });
}

export async function getSwapAlternatives(itemId) {
  return authedRequest(`/api/quests/swap-alternatives/?item_id=${encodeURIComponent(itemId)}`);
}

export async function swapQuest(itemId, newQuestId) {
  return authedRequest('/api/quests/swap/', {
    method: 'POST',
    body: { item_id: itemId, new_quest_id: newQuestId },
  });
}

export async function setDailyIntention(date, intention) {
  return authedRequest('/api/quests/intention/', {
    method: 'POST',
    body: { date, intention },
  });
}

export async function submitQuestFeedback(itemId, feedback) {
  return authedRequest('/api/quests/feedback/', {
    method: 'POST',
    body: { item_id: itemId, feedback },
  });
}

export async function getDailyCompletionSummary(date) {
  const query = date ? `?date=${encodeURIComponent(date)}` : '';
  return authedRequest(`/api/quests/summary/${query}`);
}

export async function getSocialPosts() {
  return authedRequest('/api/social/posts/');
}

export async function getSocialPost(postId) {
  return authedRequest(`/api/social/posts/${postId}/`);
}

export async function googleAuth(credential) {
  return request('/api/auth/google/', {
    method: 'POST',
    body: { credential },
    auth: false,
  });
}

export async function createSocialPost({ content, visibility, group_id, post_type } = {}) {
  return authedRequest('/api/social/posts/', {
    method: 'POST',
    body: {
      content,
      visibility,
      post_type: post_type || 'update',
      ...(group_id != null ? { group_id } : {}),
    },
  });
}

export async function updateSocialPost(postId, { content, visibility }) {
  return authedRequest(`/api/social/posts/${postId}/`, {
    method: 'PATCH',
    body: { content, visibility },
  });
}

export async function deleteSocialPost(postId) {
  return authedRequest(`/api/social/posts/${postId}/`, { method: 'DELETE' });
}

export async function searchPlayers(q) {
  return authedRequest(`/api/social/players/search/?q=${encodeURIComponent(q)}`);
}

export async function getNotifications() {
  return authedRequest('/api/social/notifications/');
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

// ── Friends ──────────────────────────────────────────────────────────────────

export async function getFriends() {
  return authedRequest('/api/social/friends/');
}

export async function getFriendRequests(direction) {
  const query = direction ? `?direction=${direction}` : '';
  return authedRequest(`/api/social/friends/requests/${query}`);
}

export async function sendFriendRequest(toPlayerId) {
  return authedRequest('/api/social/friends/requests/', {
    method: 'POST',
    body: { to_player_id: toPlayerId },
  });
}

export async function acceptFriendRequest(requestId) {
  return authedRequest(`/api/social/friends/requests/${requestId}/accept/`, {
    method: 'POST',
  });
}

export async function declineFriendRequest(requestId) {
  return authedRequest(`/api/social/friends/requests/${requestId}/decline/`, {
    method: 'POST',
  });
}

export async function cancelFriendRequest(requestId) {
  return authedRequest(`/api/social/friends/requests/${requestId}/cancel/`, {
    method: 'POST',
  });
}

export async function removeFriend(playerId) {
  return authedRequest(`/api/social/friends/${playerId}/`, {
    method: 'DELETE',
  });
}

export async function getPublicProfile(identifier) {
  return authedRequest(`/api/social/profiles/${identifier}/`);
}

// ── Groups ────────────────────────────────────────────────────────────────────

export async function getGroups() {
  return authedRequest('/api/social/groups/');
}

export async function createGroup({ name, description, is_private }) {
  return authedRequest('/api/social/groups/', {
    method: 'POST',
    body: { name, description, is_private },
  });
}

export async function joinGroup(groupId) {
  return authedRequest(`/api/social/groups/${groupId}/join/`, { method: 'POST' });
}

export async function leaveGroup(groupId) {
  return authedRequest(`/api/social/groups/${groupId}/leave/`, { method: 'POST' });
}

export async function getGroupMembers(groupId) {
  return authedRequest(`/api/social/groups/${groupId}/members/`);
}

export async function getGroupFeed(groupId) {
  return authedRequest(`/api/social/groups/${groupId}/feed/`);
}

// ── PATH DISCOVERY ────────────────────────────────────────────────────────────

export async function startQuiz() {
  return authedRequest('/api/paths/quiz/start/', { method: 'POST' });
}

export async function submitQuizAnswer(quizId, questionNumber, answer) {
  return authedRequest('/api/paths/quiz/answer/', {
    method: 'POST',
    body: { quiz_id: quizId, question_number: questionNumber, answer },
  });
}

export async function completeQuiz(quizId) {
  return authedRequest('/api/paths/quiz/complete/', {
    method: 'POST',
    body: { quiz_id: quizId },
  });
}

export async function selectPath(pathCode) {
  return authedRequest('/api/paths/select/', {
    method: 'POST',
    body: { path_code: pathCode },
  });
}

export async function getActivePaths() {
  return authedRequest('/api/paths/active/');
}

export async function retakeQuiz() {
  return authedRequest('/api/paths/retake/', { method: 'POST' });
}

export async function getOnboardingStatus() {
  return authedRequest('/api/paths/onboarding/status/');
}

export async function saveFitnessWarriorOnboarding(payload) {
  return authedRequest('/api/paths/onboarding/fitness-warrior/', {
    method: 'POST',
    body: payload,
  });
}

export async function saveMindsetSageOnboarding(payload) {
  return authedRequest('/api/paths/onboarding/mindset-sage/', {
    method: 'POST',
    body: payload,
  });
}

export async function saveHealthAlchemistOnboarding(payload) {
  return authedRequest('/api/paths/onboarding/health-alchemist/', {
    method: 'POST',
    body: payload,
  });
}

export async function getAlchemistSetupGuide() {
  return authedRequest('/api/paths/onboarding/health-alchemist/setup-guide/');
}

export async function saveDisciplineKnightOnboarding(payload) {
  return authedRequest('/api/paths/onboarding/discipline-knight/', {
    method: 'POST',
    body: payload,
  });
}

export async function submitDisciplineCode(rules) {
  return authedRequest('/api/paths/onboarding/discipline-code/', {
    method: 'POST',
    body: { rules },
  });
}

export async function saveGrindVisionaryOnboarding(payload) {
  return authedRequest('/api/paths/onboarding/grind-visionary/', {
    method: 'POST',
    body: payload,
  });
}

export async function completeOnboarding(pathCode) {
  return authedRequest('/api/paths/onboarding/complete/', {
    method: 'POST',
    body: { path_code: pathCode },
  });
}
