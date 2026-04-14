import { useCallback, useState } from 'react';
import WelcomeScreen from '../components/path-discovery/WelcomeScreen';
import QuizScreen from '../components/path-discovery/QuizScreen';
import ResultsScreen from '../components/path-discovery/ResultsScreen';
import PathCardsScreen from '../components/path-discovery/PathCardsScreen';
import CommitmentScreen from '../components/path-discovery/CommitmentScreen';
import { QUIZ_SCREEN, usePath } from '../contexts/pathContextShared';

export default function PathDiscoveryPage({ onNavigate }) {
  const {
    screen,
    questions,
    currentIndex,
    results,
    pendingPath,
    loading,
    error,
    savingPath,
    startQuiz,
    answerQuestion,
    goToPathCards,
    choosePath,
    confirmPath,
  } = usePath();

  const [submitting, setSubmitting] = useState(false);

  const handleAnswer = useCallback(
    async (questionNumber, answerKey) => {
      setSubmitting(true);
      await answerQuestion(questionNumber, answerKey);
      setSubmitting(false);
    },
    [answerQuestion],
  );

  const handleBeginJourney = useCallback(async () => {
    const success = await confirmPath();
    if (success) onNavigate('/path-onboarding');
  }, [confirmPath, onNavigate]);

  const currentQuestion = questions[currentIndex] || null;

  switch (screen) {
    case QUIZ_SCREEN.WELCOME:
      return <WelcomeScreen onStart={startQuiz} loading={loading} />;
    case QUIZ_SCREEN.QUESTION:
      return currentQuestion ? (
        <QuizScreen key={currentQuestion.number} question={currentQuestion} onAnswer={handleAnswer} submitting={submitting} />
      ) : null;
    case QUIZ_SCREEN.RESULTS:
      return <ResultsScreen results={results} onExplore={goToPathCards} />;
    case QUIZ_SCREEN.PATH_CARDS:
      return <PathCardsScreen results={results} onChoose={choosePath} />;
    case QUIZ_SCREEN.COMMITMENT:
      return <CommitmentScreen pathCode={pendingPath} onConfirm={handleBeginJourney} saving={savingPath} error={error} />;
    default:
      return <WelcomeScreen onStart={startQuiz} loading={loading} />;
  }
}
