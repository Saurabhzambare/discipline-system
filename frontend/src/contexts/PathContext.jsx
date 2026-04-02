import { createContext, useCallback, useContext, useState } from 'react';
import {
  completeQuiz as apiCompleteQuiz,
  getActivePaths,
  selectPath as apiSelectPath,
  startQuiz as apiStartQuiz,
  submitQuizAnswer,
} from '../api';

export const QUIZ_SCREEN = {
  WELCOME:    'welcome',
  QUESTION:   'question',
  RESULTS:    'results',
  PATH_CARDS: 'path_cards',
  COMMITMENT: 'commitment',
};

export const PathContext = createContext(null);

export function PathProvider({ children, onPathSelected }) {
  // ── Quiz state ────────────────────────────────────────────────────────────
  const [screen, setScreen] = useState(QUIZ_SCREEN.WELCOME);
  const [quizId, setQuizId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});     // { question_number: answer_key }
  const [results, setResults] = useState([]);     // sorted path results from API
  const [pendingPath, setPendingPath] = useState(null);

  // ── Path state ────────────────────────────────────────────────────────────
  const [selectedPath, setSelectedPath] = useState(null);
  const [selectedPathDisplay, setSelectedPathDisplay] = useState('');
  const [savingPath, setSavingPath] = useState(false);
  const [activePaths, setActivePaths] = useState([]);

  // ── Loading / error ───────────────────────────────────────────────────────
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // ── Actions ───────────────────────────────────────────────────────────────

  const startQuiz = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const data = await apiStartQuiz();
      setQuizId(data.quiz_id);
      setQuestions(data.questions);
      setCurrentIndex(0);
      setAnswers({});
      setResults([]);
      setPendingPath(null);
      setScreen(QUIZ_SCREEN.QUESTION);
    } catch (err) {
      setError(err.message || 'Could not start quiz.');
    } finally {
      setLoading(false);
    }
  }, []);

  const answerQuestion = useCallback(
    async (questionNumber, answerKey) => {
      // Optimistic local record
      setAnswers((prev) => ({ ...prev, [questionNumber]: answerKey }));
      setError('');
      try {
        const result = await submitQuizAnswer(quizId, questionNumber, answerKey);

        if (result.remaining === 0) {
          // All 9 answered — score and show results
          const completionData = await apiCompleteQuiz(quizId);
          setResults(completionData.results);
          setScreen(QUIZ_SCREEN.RESULTS);
        } else {
          setCurrentIndex((i) => i + 1);
        }
      } catch (err) {
        setError(err.message || 'Could not submit answer.');
      }
    },
    [quizId],
  );

  const goToPathCards = useCallback(() => {
    setScreen(QUIZ_SCREEN.PATH_CARDS);
  }, []);

  const choosePath = useCallback((pathCode) => {
    setPendingPath(pathCode);
    setScreen(QUIZ_SCREEN.COMMITMENT);
  }, []);

  const confirmPath = useCallback(async () => {
    if (!pendingPath) return false;
    setSavingPath(true);
    setError('');
    try {
      const data = await apiSelectPath(pendingPath);
      setSelectedPath(data.selected_path.code);
      setSelectedPathDisplay(data.selected_path.name);
      // Bridge to PlayerContext — App.jsx passes this callback
      if (onPathSelected) onPathSelected(data.player);
      return true;
    } catch (err) {
      setError(err.message || 'Could not save path selection.');
      return false;
    } finally {
      setSavingPath(false);
    }
  }, [pendingPath, onPathSelected]);

  const loadActivePaths = useCallback(async () => {
    try {
      const data = await getActivePaths();
      setActivePaths(data.multi_paths_active || []);
      if (data.primary_path) setSelectedPath(data.primary_path);
    } catch {
      // non-critical
    }
  }, []);

  // Called by App.jsx to sync path state when player data loads from API
  const syncFromPlayer = useCallback((player) => {
    if (player?.path) {
      setSelectedPath(player.path);
      setSelectedPathDisplay(player.path_display || '');
    }
  }, []);

  return (
    <PathContext.Provider
      value={{
        // screen management
        screen,
        setScreen,
        // quiz
        quizId,
        questions,
        currentIndex,
        answers,
        results,
        pendingPath,
        // path
        selectedPath,
        selectedPathDisplay,
        savingPath,
        activePaths,
        // status
        loading,
        error,
        // actions
        startQuiz,
        answerQuestion,
        goToPathCards,
        choosePath,
        confirmPath,
        loadActivePaths,
        syncFromPlayer,
        // legacy alias kept for any existing callers
        handleSelectPath: confirmPath,
      }}
    >
      {children}
    </PathContext.Provider>
  );
}

export function usePath() {
  return useContext(PathContext);
}
