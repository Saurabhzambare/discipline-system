import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  clearTokens,
  completeQuest,
  getAccessToken,
  getPlayerMe,
  getQuests,
  login,
  setTokens,
  signup,
  updatePlayerPath,
} from './api';
import Layout from './components/Layout';
import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';
import OnboardingPage from './pages/OnboardingPage';
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
  const [loadingDashboard, setLoadingDashboard] = useState(false);
  const [dashboardError, setDashboardError] = useState('');
  const [completingQuestId, setCompletingQuestId] = useState(null);
  const [savingPath, setSavingPath] = useState(false);
  const [flashMessage, setFlashMessage] = useState(null);

  const selectedPath = useMemo(() => player?.path || '', [player?.path]);
  const selectedPathDisplay = useMemo(() => player?.path_display || '', [player?.path_display]);

  const handleAuthExpired = useCallback(
    (message = 'Session expired. Please log in again.') => {
      clearTokens();
      setIsAuthenticated(false);
      setPlayer(null);
      setQuests([]);
      setFlashMessage({ type: 'error', text: message });
      navigate('/login');
    },
    [navigate],
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

    if (isAuthenticated && (route === '/dashboard' || route === '/profile' || route === '/onboarding')) {
      loadDashboard();
    }
  }, [isAuthenticated, loadDashboard, navigate, route]);

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

  function handleLogout() {
    clearTokens();
    setIsAuthenticated(false);
    setPlayer(null);
    setQuests([]);
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

  async function handleCompleteQuest(questId) {
    setCompletingQuestId(questId);

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

      setFlashMessage({
        type: 'success',
        text: response.leveled_up
          ? `Quest complete! +${response.exp_gained} EXP. Level up!`
          : `Quest complete! +${response.exp_gained} EXP.`,
      });
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
    page = <LoginPage onLogin={handleLogin} onNavigate={navigate} />;
  } else if (route === '/signup') {
    page = <SignupPage onSignup={handleSignup} onNavigate={navigate} />;
  } else if (route === '/onboarding') {
    page = (
      <OnboardingPage
        selectedPath={selectedPath}
        onSelectPath={handleSelectPath}
        onNavigate={navigate}
        savingPath={savingPath}
      />
    );
  } else if (route === '/profile') {
    page = <ProfilePage player={player} selectedPathDisplay={selectedPathDisplay} onNavigate={navigate} />;
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
      />
    );
  }

  return (
    <Layout
      onNavigate={navigate}
      isAuthenticated={isAuthenticated}
      onLogout={handleLogout}
      flashMessage={flashMessage}
      onDismissFlash={() => setFlashMessage(null)}
    >
      {page}
    </Layout>
  );
}
