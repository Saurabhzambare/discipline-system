import { useCallback, useEffect, useState } from 'react';
import {
  clearTokens,
  completeQuest,
  getAccessToken,
  getPlayerMe,
  getQuests,
  login,
  setTokens,
  signup,
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
  const [selectedPath, setSelectedPath] = useState(localStorage.getItem('discipline_path') || '');

  const loadDashboard = useCallback(async () => {
    setLoadingDashboard(true);
    setDashboardError('');

    try {
      const [playerData, questData] = await Promise.all([getPlayerMe(), getQuests()]);
      setPlayer(playerData);
      setQuests(questData);
    } catch (error) {
      if (error.status === 401) {
        clearTokens();
        setIsAuthenticated(false);
        setPlayer(null);
        navigate('/login');
      }
      setDashboardError(error.message || 'Could not load dashboard data.');
    } finally {
      setLoadingDashboard(false);
    }
  }, [navigate]);

  useEffect(() => {
    const protectedRoute = !PUBLIC_ROUTES.includes(route);

    if (!isAuthenticated && protectedRoute) {
      navigate('/login');
      return;
    }

    if (isAuthenticated && route === '/') {
      navigate('/dashboard');
      return;
    }

    if (!isAuthenticated && route === '/') {
      navigate('/login');
      return;
    }

    if (isAuthenticated && (route === '/dashboard' || route === '/profile')) {
      loadDashboard();
    }
  }, [isAuthenticated, loadDashboard, navigate, route]);

  async function handleLogin(username, password) {
    const tokenData = await login(username, password);
    setTokens(tokenData.access, tokenData.refresh);
    setIsAuthenticated(true);
    navigate('/dashboard');
  }

  async function handleSignup(username, password) {
    await signup(username, password);
  }

  function handleLogout() {
    clearTokens();
    setIsAuthenticated(false);
    setPlayer(null);
    setQuests([]);
    navigate('/login');
  }

  function handleSelectPath(path) {
    setSelectedPath(path);
    localStorage.setItem('discipline_path', path);
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
          quest.id === questId ? { ...quest, completed_today: true } : quest,
        ),
      );
    } catch (error) {
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
      />
    );
  } else if (route === '/profile') {
    page = <ProfilePage player={player} selectedPath={selectedPath} />;
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
        selectedPath={selectedPath}
        onNavigate={navigate}
      />
    );
  }


  return (
    <Layout onNavigate={navigate} isAuthenticated={isAuthenticated} onLogout={handleLogout}>
      {page}
    </Layout>
  );
}
