import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  acceptFriendRequest,
  cancelFriendRequest,
  clearTokens,
  completeLineupItem,
  completeQuest,
  createGroup,
  createPostComment,
  createSocialPost,
  declineFriendRequest,
  deletePostComment,
  deleteSocialPost,
  getAccessToken,
  getNotifications,
  getOnboardingStatus,
  getAccountabilityRequests,
  getBodyJournalEntries,
  getDailyLineup,
  getDailyCompletionSummary,
  getDisciplineMechanicsStatus,
  getGrindMechanicsStatus,
  getHealthMechanicsStatus,
  getKnightWeeklyReport,
  getOutputLogs,
  getTemptationLogs,
  getSwapAlternatives,
  getWarRoomEntries,
  getVisionBoardSummary,
  getWisdomLogs,
  getFriendRequests,
  getFriends,
  getGroups,
  getPlayerMe,
  getPublicProfile,
  getSocialPost,
  getSocialPosts,
  googleAuth,
  joinGroup,
  leaveGroup,
  login,
  removePostReaction,
  removeFriend,
  sendFriendRequest,
  sendAccountabilityRequest,
  setPostReaction,
  setTokens,
  setDailyIntention,
  signup,
  acceptAccountabilityRequest,
  createTemptationLog,
  rejectAccountabilityRequest,
  submitQuestFeedback,
  swapQuest,
  redeemFreedomDayToken,
  activateDarkNight,
  upsertBodyJournalEntry,
  upsertOutputLog,
  upsertWisdomLog,
  updatePostComment,
  updateSocialPost,
  upsertWarRoomEntry,
  searchPlayers,
} from './api';
import { PathProvider } from './contexts/PathContext';
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
import PathOnboardingPage from './pages/PathOnboardingPage';
import PreviewPage from './pages/PreviewPage';
import ProfilePage from './pages/ProfilePage';
import SignupPage from './pages/SignupPage';

const PUBLIC_ROUTES = ['/login', '/signup'];

function deriveProgressFromTotalExp(totalExp = 0, level = 1) {
  const safeLevel = Math.max(1, Number(level) || 1);
  const safeExp = Math.max(0, Number(totalExp) || 0);
  const expFor = (lvl) => (lvl * lvl * 50) - 50;
  const currentFloor = expFor(safeLevel);
  const nextFloor = expFor(safeLevel + 1);
  const expForLevel = Math.max(1, nextFloor - currentFloor);
  const expInLevel = Math.max(0, safeExp - currentFloor);
  return {
    exp_in_level: expInLevel,
    exp_for_level: expForLevel,
    exp_to_next_level: Math.max(0, nextFloor - safeExp),
  };
}

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
  const [dailyLineup, setDailyLineup] = useState(null);
  const [lineupItems, setLineupItems] = useState([]);
  const [intention, setIntentionState] = useState(null);
  const [swapsRemaining, setSwapsRemaining] = useState(3);
  const [featuresUnlocked, setFeaturesUnlocked] = useState({ slot_labels: false, swap: false, full_customization: false });
  const [feedPosts, setFeedPosts] = useState([]);
  const [loadingDashboard, setLoadingDashboard] = useState(false);
  const [loadingFeed, setLoadingFeed] = useState(false);
  const [dashboardError, setDashboardError] = useState('');
  const [feedError, setFeedError] = useState('');
  const [completingQuestId, setCompletingQuestId] = useState(null);
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
  const [onboardingStatus, setOnboardingStatus] = useState(null);

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
      const [playerData, lineupPayload] = await Promise.all([getPlayerMe(), getDailyLineup()]);
      setPlayer(playerData);
      if (lineupPayload?.lineup) {
        setDailyLineup(lineupPayload.lineup);
        setLineupItems(lineupPayload.lineup.items || []);
        setIntentionState(lineupPayload.lineup.intention || null);
        setSwapsRemaining(lineupPayload.lineup.swaps_remaining ?? 3);
        setFeaturesUnlocked(lineupPayload.lineup.features_unlocked || { slot_labels: false, swap: false, full_customization: false });
        const mapped = (lineupPayload.lineup.items || [])
          .filter((item) => item.quest_id)
          .map((item) => ({
            id: item.quest_id,
            item_id: item.item_id,
            title: item.title,
            description: item.description,
            path_target: item.path_target,
            rank: item.rank,
            pillar: item.pillar,
            exp_reward: item.exp_reward,
            universal_daily: item.slot_type === 'universal',
            is_weekly_boss: item.selection_reason === 'weekly_rhythm',
            cooldown_days: 0,
            completed_today: item.completed_today,
            assigned_completed_today: item.assigned_completed_today,
            feedback: item.feedback || null,
          }));
        setQuests(mapped);
      } else {
        setDailyLineup(null);
        setLineupItems([]);
        setQuests([]);
      }
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

  const loadOnboardingStatus = useCallback(async () => {
    if (!isAuthenticated || !player?.path) {
      setOnboardingStatus(null);
      return;
    }
    try {
      const data = await getOnboardingStatus();
      setOnboardingStatus(data);
    } catch {
      setOnboardingStatus(null);
    }
  }, [isAuthenticated, player?.path]);

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
    if (!isAuthenticated || !player?.path || !onboardingStatus) return;
    if (!onboardingStatus.onboarding_complete && route !== '/path-onboarding') {
      navigate('/path-onboarding');
      return;
    }
    if (onboardingStatus.onboarding_complete && route === '/path-onboarding') {
      navigate('/dashboard');
    }
  }, [isAuthenticated, player?.path, onboardingStatus, route, navigate]);

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
    if (isAuthenticated && player?.path) {
      loadOnboardingStatus();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [handleAuthExpired, isAuthenticated, loadDashboard, loadFeed, loadFriends, loadGroups, loadNotifications, loadOnboardingStatus, navigate, player?.path, route]);

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

  async function handleCompleteQuest(questId, note) {
    setCompletingQuestId(questId);
    const questForShare = quests.find((q) => q.id === questId);

    try {
      let response;
      if (questForShare?.item_id) {
        response = await completeLineupItem(questForShare.item_id);
        response = {
          exp_gained: (response.exp_earned || 0) + (response.bonus_exp || 0),
          player_exp: response.player_exp,
          player_streak: response.streak_update,
          new_level: response.new_level,
          leveled_up: response.level_up,
        };
      } else {
        response = await completeQuest(questId);
      }

      setPlayer((previous) => {
        if (!previous) return previous;
        const progressState = deriveProgressFromTotalExp(response.player_exp, response.new_level);
        return {
          ...previous,
          exp: response.player_exp,
          level: response.new_level,
          streak: response.player_streak,
          ...progressState,
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
        setLevelUpInfo({ newLevel: response.new_level, achievedAt: Date.now() });
      } else {
        setFlashMessage({
          type: 'success',
          text: note ? `Quest complete! +${response.exp_gained} EXP — shared to feed.` : `Quest complete! +${response.exp_gained} EXP.`,
        });
      }
      await loadDashboard();
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
    page = <OnboardingPage onNavigate={navigate} />;
  } else if (route === '/path-onboarding') {
    page = (
      <PathOnboardingPage
        player={player}
        onNavigate={navigate}
        onOnboardingComplete={(updatedPlayer) => {
          setPlayer(updatedPlayer);
          setOnboardingStatus((prev) => ({ ...(prev || {}), onboarding_complete: true }));
        }}
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
        dailyLineup={dailyLineup}
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
        onSetIntention={async (value) => {
          const targetDate = dailyLineup?.date;
          if (!targetDate) return;
          const result = await setDailyIntention(targetDate, value);
          await loadDashboard();
          return result;
        }}
        onGetSwapAlternatives={async (itemId) => getSwapAlternatives(itemId)}
        onSwapQuest={async (itemId, newQuestId) => {
          await swapQuest(itemId, newQuestId);
          await loadDashboard();
        }}
        onSubmitFeedback={async (itemId, feedback) => {
          await submitQuestFeedback(itemId, feedback);
          await loadDashboard();
        }}
        onLoadSummary={async (targetDate) => getDailyCompletionSummary(targetDate)}
        onLoadWarRoomEntries={async () => getWarRoomEntries()}
        onSubmitWarRoomEntry={async (payload) => upsertWarRoomEntry(payload)}
        onLoadKnightWeeklyReport={async (weekStart) => getKnightWeeklyReport(weekStart)}
        onGetWisdomLogs={async () => getWisdomLogs()}
        onUpsertWisdomLog={async (payload) => upsertWisdomLog(payload)}
        onRedeemFreedomDay={async (payload) => redeemFreedomDayToken(payload)}
        onActivateDarkNight={async (payload) => activateDarkNight(payload)}
        onGetBodyJournalEntries={async () => getBodyJournalEntries()}
        onGetHealthMechanicsStatus={async () => getHealthMechanicsStatus()}
        onUpsertBodyJournalEntry={async (payload) => upsertBodyJournalEntry(payload)}
        onGetVisionBoardSummary={async () => getVisionBoardSummary()}
        onGetOutputLogs={async () => getOutputLogs()}
        onGetGrindMechanicsStatus={async () => getGrindMechanicsStatus()}
        onUpsertOutputLog={async (payload) => upsertOutputLog(payload)}
        onGetDisciplineMechanicsStatus={async () => getDisciplineMechanicsStatus()}
        onGetTemptationLogs={async () => getTemptationLogs()}
        onCreateTemptationLog={async (payload) => createTemptationLog(payload)}
        onGetAccountabilityRequests={async (direction) => getAccountabilityRequests(direction)}
        onSearchPlayers={async (q) => searchPlayers(q)}
        onSendAccountabilityRequest={async (toPlayerId) => sendAccountabilityRequest(toPlayerId)}
        onAcceptAccountabilityRequest={async (requestId) => acceptAccountabilityRequest(requestId)}
        onRejectAccountabilityRequest={async (requestId) => rejectAccountabilityRequest(requestId)}
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
          dailyLineup,
          lineupItems,
          intention,
          swapsRemaining,
          featuresUnlocked,
          completingQuestId,
          handleCompleteQuest,
          loadDailyLineup: loadDashboard,
          setIntention: async (targetDate, value) => {
            const result = await setDailyIntention(targetDate, value);
            setIntentionState(result.intention_set);
            await loadDashboard();
            return result;
          },
          swapQuest: async (itemId, newQuestId) => {
            const result = await swapQuest(itemId, newQuestId);
            await loadDashboard();
            return result;
          },
          submitFeedback: async (itemId, feedback) => {
            const result = await submitQuestFeedback(itemId, feedback);
            await loadDashboard();
            return result;
          },
          loadSummary: async (targetDate) => getDailyCompletionSummary(targetDate),
        }}
      >
        <PathProvider onPathSelected={(updatedPlayer) => setPlayer(updatedPlayer)}>
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
        </PathProvider>
      </QuestContext.Provider>
    </PlayerContext.Provider>
  );
}
