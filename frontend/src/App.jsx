import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  acceptFriendRequest,
  cancelFriendRequest,
  clearTokens,
  completeQuest,
  createGroup,
  createPostComment,
  createSocialPost,
  declineFriendRequest,
  deletePostComment,
  deleteSocialPost,
  getAccessToken,
  getNotifications,
  getFriendRequests,
  getFriends,
  getGroupFeed,
  getGroupMembers,
  getGroups,
  getPlayerMe,
  getPublicProfile,
  getQuests,
  getSocialPost,
  getSocialPosts,
  googleAuth,
  joinGroup,
  leaveGroup,
  login,
  removePostReaction,
  removeFriend,
  sendFriendRequest,
  setPostReaction,
  setTokens,
  signup,
  updatePlayerPath,
  updatePostComment,
  updateSocialPost,
} from './api';
import { PathContext } from './contexts/PathContext';
import { PlayerContext } from './contexts/PlayerContext';
import { QuestContext } from './contexts/QuestContext';
import Layout from './components/Layout';
import PlayerProfileModal from './components/PlayerProfileModal';
import ComingSoonPage from './pages/ComingSoonPage';
import DashboardPage from './pages/DashboardPage';
import FeedPage from './pages/FeedPage';
import GroupsPage from './pages/GroupsPage';
import LoginPage from './pages/LoginPage';
import OnboardingPage from './pages/OnboardingPage';
import PreviewPage from './pages/PreviewPage';
import ProfilePage from './pages/ProfilePage';
import SignupPage from './pages/SignupPage';

const PUBLIC_ROUTES = ['/login', '/signup'];

function useRoute() {
  const [route, setRoute] = useState(window.location.pathname || '/');

  useEffect(() => {
    const onPopState = () => setRoute(window.location.pathname || '/');
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  const navigate = useCallback((path) => {
    if (window.location.pathname !== path) {
      window.history.pushState({}, '', path);
      setRoute(path);
    }
  }, []);

  return [route, navigate];
}

export default function App() {
  const [route, navigate] = useRoute();
  const [isAuthenticated, setIsAuthenticated] = useState(Boolean(getAccessToken()));
  const [player, setPlayer] = useState(null);
  const [quests, setQuests] = useState([]);
  const [feedPosts, setFeedPosts] = useState([]);
  const [loadingDashboard, setLoadingDashboard] = useState(false);
  const [loadingFeed, setLoadingFeed] = useState(false);
  const [dashboardError, setDashboardError] = useState('');
  const [feedError, setFeedError] = useState('');
  const [completingQuestId, setCompletingQuestId] = useState(null);
  const [savingPath, setSavingPath] = useState(false);
  const [flashMessage, setFlashMessage] = useState(null);
  const [friends, setFriends] = useState([]);
  const [incomingRequests, setIncomingRequests] = useState([]);
  const [outgoingRequests, setOutgoingRequests] = useState([]);
  const [loadingFriends, setLoadingFriends] = useState(false);
  const [friendsError, setFriendsError] = useState('');
  const [groups, setGroups] = useState([]);
  const [loadingGroups, setLoadingGroups] = useState(false);
  const [groupsError, setGroupsError] = useState('');
  const [levelUpInfo, setLevelUpInfo] = useState(null);
  const [viewingProfile, setViewingProfile] = useState(null);
  const [notifications, setNotifications] = useState([]);

  const selectedPath = useMemo(() => player?.path || '', [player?.path]);
  const selectedPathDisplay = useMemo(() => player?.path_display || '', [player?.path_display]);

  const handleAuthExpired = useCallback(
    (message = 'Session expired. Please log in again.') => {
      clearTokens();
      setIsAuthenticated(false);
      setPlayer(null);
      setQuests([]);
      setFeedPosts([]);
      setFlashMessage({ type: 'error', text: message });
      navigate('/login');
    },
    [navigate],
  );

  const withSocialAuth = useCallback(
    async (handler) => {
      try {
        return await handler();
      } catch (error) {
        if (error.status === 401) {
          handleAuthExpired(error.message);
        }
        throw error;
      }
    },
    [handleAuthExpired],
  );

  const loadDashboard = useCallback(async () => {
    setLoadingDashboard(true);
    setDashboardError('');

    try {
      const [playerData, questData] = await Promise.all([getPlayerMe(), getQuests()]);
      setPlayer(playerData);
      setQuests(questData);
    } catch (error) {
      if (error.status === 401) {
        handleAuthExpired(error.message);
        return;
      }
      setDashboardError(error.message || 'Could not load dashboard data.');
    } finally {
      setLoadingDashboard(false);
    }
  }, [handleAuthExpired]);

  const loadFeed = useCallback(
    async ({ showLoading = true, throwOnError = false } = {}) => {
      if (showLoading) {
        setLoadingFeed(true);
      }
      setFeedError('');

      try {
        const posts = await getSocialPosts();
        setFeedPosts(posts);
      } catch (error) {
        if (error.status === 401) {
          handleAuthExpired(error.message);
        }

        setFeedError(error.message || 'Could not load social feed.');

        if (throwOnError) {
          throw error;
        }
      } finally {
        if (showLoading) {
          setLoadingFeed(false);
        }
      }
    },
    [handleAuthExpired],
  );

  const loadFriends = useCallback(async () => {
    setLoadingFriends(true);
    setFriendsError('');
    try {
      const [friendsList, incoming, outgoing] = await Promise.all([
        getFriends(),
        getFriendRequests('incoming'),
        getFriendRequests('outgoing'),
      ]);
      setFriends(friendsList);
      setIncomingRequests(incoming);
      setOutgoingRequests(outgoing);
    } catch (error) {
      if (error.status === 401) { handleAuthExpired(error.message); return; }
      setFriendsError(error.message || 'Could not load friends.');
    } finally {
      setLoadingFriends(false);
    }
  }, [handleAuthExpired]);

  const handleSendFriendRequest = useCallback(async (username) => {
    const profile = await getPublicProfile(username);
    await sendFriendRequest(profile.id);
    await loadFriends();
    setFlashMessage({ type: 'success', text: `Friend request sent to ${username}.` });
  }, [loadFriends]);

  const handleAcceptRequest = useCallback(async (requestId) => {
    await acceptFriendRequest(requestId);
    await loadFriends();
    setFlashMessage({ type: 'success', text: 'Friend request accepted.' });
  }, [loadFriends]);

  const handleDeclineRequest = useCallback(async (requestId) => {
    await declineFriendRequest(requestId);
    await loadFriends();
  }, [loadFriends]);

  const handleCancelRequest = useCallback(async (requestId) => {
    await cancelFriendRequest(requestId);
    await loadFriends();
  }, [loadFriends]);

  const handleRemoveFriend = useCallback(async (playerId) => {
    await removeFriend(playerId);
    await loadFriends();
    setFlashMessage({ type: 'success', text: 'Friend removed.' });
  }, [loadFriends]);

  const loadGroups = useCallback(async () => {
    setLoadingGroups(true);
    setGroupsError('');
    try {
      const data = await getGroups();
      setGroups(data);
    } catch (error) {
      if (error.status === 401) { handleAuthExpired(error.message); return; }
      setGroupsError(error.message || 'Could not load groups.');
    } finally {
      setLoadingGroups(false);
    }
  }, [handleAuthExpired]);

  const handleCreateGroup = useCallback(async ({ name, description, is_private }) => {
    await createGroup({ name, description, is_private });
    await loadGroups();
    setFlashMessage({ type: 'success', text: `Group "${name}" created.` });
  }, [loadGroups]);

  const handleJoinGroup = useCallback(async (groupId) => {
    await joinGroup(groupId);
    await loadGroups();
    setFlashMessage({ type: 'success', text: 'Joined group.' });
  }, [loadGroups]);

  const handleLeaveGroup = useCallback(async (groupId) => {
    await leaveGroup(groupId);
    await loadGroups();
    setFlashMessage({ type: 'success', text: 'Left group.' });
  }, [loadGroups]);

  const loadNotifications = useCallback(async () => {
    try {
      const data = await getNotifications();
      setNotifications(data);
    } catch {
      // non-critical — silently ignore
    }
  }, []);

  const handleShareQuest = useCallback(
    async (quest, note) => {
      return withSocialAuth(async () => {
        const body = note
          ? `Just completed: "${quest.title}" — +${quest.exp_reward} EXP\n\n${note}`
          : `Just completed: "${quest.title}" — +${quest.exp_reward} EXP earned! 💪`;
        await createSocialPost({
          content: body,
          visibility: 'public',
          post_type: 'quest_completion',
        });
        setFlashMessage({ type: 'success', text: 'Quest shared to feed!' });
      });
    },
    [withSocialAuth],
  );

  const handleUpdatePost = useCallback(
    async (postId, { content, visibility }) => {
      return withSocialAuth(async () => {
        await updateSocialPost(postId, { content, visibility });
        await loadFeed({ showLoading: false });
      });
    },
    [loadFeed, withSocialAuth],
  );

  const handleDeletePost = useCallback(
    async (postId, onSuccess) => {
      return withSocialAuth(async () => {
        await deleteSocialPost(postId);
        if (onSuccess) {
          await onSuccess();
        } else {
          setFeedPosts((prev) => prev.filter((p) => p.id !== postId));
        }
        setFlashMessage({ type: 'success', text: 'Post deleted.' });
      });
    },
    [withSocialAuth],
  );

  const refreshPost = useCallback(
    async (postId) => {
      return withSocialAuth(async () => {
        const updatedPost = await getSocialPost(postId);
        setFeedPosts((previousPosts) =>
          previousPosts.map((post) => (post.id === postId ? updatedPost : post)),
        );
      });
    },
    [withSocialAuth],
  );

  const handleCreatePost = useCallback(
    async ({ content, visibility }) => {
      return withSocialAuth(async () => {
        await createSocialPost({ content, visibility });
        await loadFeed({ showLoading: false, throwOnError: true });
        setFlashMessage({ type: 'success', text: 'Post shared successfully.' });
      });
    },
    [loadFeed, withSocialAuth],
  );

  const handleAddComment = useCallback(
    async (postId, content) => {
      return withSocialAuth(async () => createPostComment(postId, content));
    },
    [withSocialAuth],
  );

  const handleUpdateComment = useCallback(
    async (postId, commentId, content) => {
      return withSocialAuth(async () => updatePostComment(postId, commentId, content));
    },
    [withSocialAuth],
  );

  const handleDeleteComment = useCallback(
    async (postId, commentId) => {
      return withSocialAuth(async () => deletePostComment(postId, commentId));
    },
    [withSocialAuth],
  );

  const handleSetReaction = useCallback(
    async (postId, reactionType) => {
      return withSocialAuth(async () => setPostReaction(postId, reactionType));
    },
    [withSocialAuth],
  );

  const handleRemoveReaction = useCallback(
    async (postId) => {
      return withSocialAuth(async () => removePostReaction(postId));
    },
    [withSocialAuth],
  );

  // Enforce onboarding for users who haven't chosen a path yet
  useEffect(() => {
    if (isAuthenticated && player && !player.path && route !== '/onboarding') {
      navigate('/onboarding');
    }
  }, [isAuthenticated, player, route, navigate]);

  useEffect(() => {
    const protectedRoute = !PUBLIC_ROUTES.includes(route);

    if (!isAuthenticated && protectedRoute) {
      navigate('/login');
      return;
    }

    if (isAuthenticated && (route === '/' || route === '/login' || route === '/signup')) {
      navigate('/dashboard');
      return;
    }

    if (isAuthenticated && !player) {
      getPlayerMe()
        .then((playerData) => setPlayer(playerData))
        .catch((error) => {
          if (error.status === 401) {
            handleAuthExpired(error.message);
          }
        });
    }

    if (isAuthenticated && (route === '/dashboard' || route === '/profile' || route === '/onboarding')) {
      loadDashboard();
    }

    if (isAuthenticated && route === '/profile') {
      loadFriends();
    }

    if (isAuthenticated && route === '/feed') {
      loadFeed();
    }

    if (isAuthenticated && route === '/groups') {
      loadGroups();
    }

    if (isAuthenticated) {
      loadNotifications();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [handleAuthExpired, isAuthenticated, loadDashboard, loadFeed, loadFriends, loadGroups, loadNotifications, navigate, route]);

  async function handleLogin(username, password) {
    const tokenData = await login(username, password);
    setTokens(tokenData.access, tokenData.refresh);
    setIsAuthenticated(true);
    setFlashMessage({ type: 'success', text: 'Welcome back, Hunter.' });
    navigate('/dashboard');
  }

  async function handleSignup(username, password) {
    await signup(username, password);
    setFlashMessage({ type: 'success', text: 'Account created. You can now sign in.' });
  }

  async function handleGoogleAuth(credential) {
    const data = await googleAuth(credential);
    setTokens(data.access, data.refresh);
    setIsAuthenticated(true);
    setFlashMessage({
      type: 'success',
      text: data.is_new ? 'Welcome, Hunter. Your account has been created.' : 'Welcome back, Hunter.',
    });
    navigate('/dashboard');
  }

  function handleLogout() {
    clearTokens();
    setIsAuthenticated(false);
    setPlayer(null);
    setQuests([]);
    setFeedPosts([]);
    setFlashMessage({ type: 'success', text: 'You have been logged out.' });
    navigate('/login');
  }

  async function handleSelectPath(path) {
    setSavingPath(true);
    setDashboardError('');

    try {
      const updatedPlayer = await updatePlayerPath(path);
      setPlayer(updatedPlayer);
      setFlashMessage({ type: 'success', text: `Path updated to ${updatedPlayer.path_display || path}.` });
    } catch (error) {
      if (error.status === 401) {
        handleAuthExpired(error.message);
        return;
      }
      setDashboardError(error.message || 'Could not update path.');
    } finally {
      setSavingPath(false);
    }
  }

  async function handleCompleteQuest(questId, note) {
    setCompletingQuestId(questId);
    const questForShare = quests.find((q) => q.id === questId);

    try {
      const response = await completeQuest(questId);

      setPlayer((previous) => {
        if (!previous) return previous;
        return {
          ...previous,
          exp: response.player_exp,
          level: response.new_level,
          streak: response.player_streak,
        };
      });

      setQuests((previous) =>
        previous.map((quest) =>
          quest.id === questId ? { ...quest, completed_today: true, assigned_completed_today: true } : quest,
        ),
      );

      // Auto-share to feed when note is provided (Feature B)
      if (note && questForShare) {
        try {
          await createSocialPost({
            content: `Just completed: "${questForShare.title}" — +${questForShare.exp_reward} EXP\n\n${note}`,
            visibility: 'public',
            post_type: 'quest_completion',
          });
        } catch {
          // share failure is non-critical
        }
      }

      if (response.leveled_up) {
        setLevelUpInfo({ newLevel: response.new_level });
      } else {
        setFlashMessage({
          type: 'success',
          text: note ? `Quest complete! +${response.exp_gained} EXP — shared to feed.` : `Quest complete! +${response.exp_gained} EXP.`,
        });
      }
    } catch (error) {
      if (error.status === 401) {
        handleAuthExpired(error.message);
        return;
      }
      setDashboardError(error.message || 'Quest completion failed.');
    } finally {
      setCompletingQuestId(null);
    }
  }

  let page;

  if (route === '/login') {
    page = <LoginPage onLogin={handleLogin} onGoogleAuth={handleGoogleAuth} onNavigate={navigate} />;
  } else if (route === '/signup') {
    page = <SignupPage onSignup={handleSignup} onGoogleAuth={handleGoogleAuth} onNavigate={navigate} />;
  } else if (route === '/onboarding') {
    page = (
      <OnboardingPage
        selectedPath={selectedPath}
        onSelectPath={handleSelectPath}
        onNavigate={navigate}
        savingPath={savingPath}
        isRequired={!player?.path}
      />
    );
  } else if (route === '/profile') {
    page = (
      <ProfilePage
        player={player}
        selectedPathDisplay={selectedPathDisplay}
        onNavigate={navigate}
        friends={friends}
        incomingRequests={incomingRequests}
        outgoingRequests={outgoingRequests}
        loadingFriends={loadingFriends}
        friendsError={friendsError}
        onSendFriendRequest={handleSendFriendRequest}
        onAcceptRequest={handleAcceptRequest}
        onDeclineRequest={handleDeclineRequest}
        onCancelRequest={handleCancelRequest}
        onRemoveFriend={handleRemoveFriend}
        onRefreshFriends={loadFriends}
      />
    );
  } else if (route === '/coming-soon') {
    page = <ComingSoonPage onNavigate={navigate} />;
  } else if (route === '/preview') {
    page = <PreviewPage />;
  } else if (route === '/groups') {
    page = (
      <GroupsPage
        groups={groups}
        loading={loadingGroups}
        error={groupsError}
        currentPlayerId={player?.id}
        onRefresh={loadGroups}
        onCreateGroup={handleCreateGroup}
        onJoinGroup={handleJoinGroup}
        onLeaveGroup={handleLeaveGroup}
        onAddComment={handleAddComment}
        onUpdateComment={handleUpdateComment}
        onDeleteComment={handleDeleteComment}
        onSetReaction={handleSetReaction}
        onRemoveReaction={handleRemoveReaction}
        onViewProfile={setViewingProfile}
        onUpdatePost={handleUpdatePost}
        onDeletePost={handleDeletePost}
      />
    );
  } else if (route === '/feed') {
    page = (
      <FeedPage
        posts={feedPosts}
        loading={loadingFeed}
        error={feedError}
        onRefresh={loadFeed}
        onCreatePost={handleCreatePost}
        currentPlayerId={player?.id}
        onRefreshPost={refreshPost}
        onAddComment={handleAddComment}
        onUpdateComment={handleUpdateComment}
        onDeleteComment={handleDeleteComment}
        onSetReaction={handleSetReaction}
        onRemoveReaction={handleRemoveReaction}
        onViewProfile={setViewingProfile}
        onUpdatePost={handleUpdatePost}
        onDeletePost={handleDeletePost}
        player={player}
        friends={friends}
        onNavigate={navigate}
      />
    );
  } else {
    page = (
      <DashboardPage
        player={player}
        quests={quests}
        loading={loadingDashboard}
        error={dashboardError}
        onRefresh={loadDashboard}
        onCompleteQuest={handleCompleteQuest}
        completingQuestId={completingQuestId}
        selectedPathDisplay={selectedPathDisplay}
        onNavigate={navigate}
        levelUpInfo={levelUpInfo}
        onDismissLevelUp={() => setLevelUpInfo(null)}
        onShareQuest={handleShareQuest}
      />
    );
  }

  return (
    <PlayerContext.Provider
      value={{
        player,
        setPlayer,
        loadingDashboard,
        dashboardError,
        levelUpInfo,
        setLevelUpInfo,
        loadDashboard,
        handleAuthExpired,
      }}
    >
      <QuestContext.Provider
        value={{
          quests,
          setQuests,
          completingQuestId,
          handleCompleteQuest,
        }}
      >
        <PathContext.Provider
          value={{
            selectedPath,
            selectedPathDisplay,
            savingPath,
            handleSelectPath,
          }}
        >
          <Layout
            onNavigate={navigate}
            isAuthenticated={isAuthenticated}
            onLogout={handleLogout}
            flashMessage={flashMessage}
            onDismissFlash={() => setFlashMessage(null)}
            route={route}
            playerName={player?.username}
            incomingRequestCount={incomingRequests.length}
            notifications={notifications}
          >
            {page}
            {viewingProfile && (
              <PlayerProfileModal
                username={viewingProfile}
                onClose={() => setViewingProfile(null)}
                onSendRequest={handleSendFriendRequest}
                currentPlayerId={player?.id}
              />
            )}
          </Layout>
        </PathContext.Provider>
      </QuestContext.Provider>
    </PlayerContext.Provider>
  );
}
