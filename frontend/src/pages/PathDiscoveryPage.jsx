import { useEffect } from 'react';
import { usePath, QUIZ_SCREEN } from '../contexts/pathContextShared';
import { getPathData } from '../data/pathData';

const CARD = 'rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5';

function WelcomeScreen({ onStart, loading }) {
  return (
    <div className={CARD}>
      <p className="text-xs uppercase tracking-[0.3em] text-cyan-400/70">Path Discovery</p>
      <h1 className="mt-1 text-2xl font-black text-slate-100">Find your path, Hunter.</h1>
      <p className="mt-3 text-sm text-slate-400">
        Answer 9 questions and we will match you to one of five RPG paths.
        Each path is a 90-day system shaped around who you want to become.
      </p>
      <button
        type="button"
        onClick={onStart}
        disabled={loading}
        className="mt-5 rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-4 py-2 text-cyan-200 disabled:opacity-50"
      >
        {loading ? 'Starting…' : 'Begin the Quiz'}
      </button>
    </div>
  );
}

function QuestionScreen({ question, index, total, onAnswer, answer }) {
  if (!question) return null;
  return (
    <div className={CARD}>
      <p className="text-xs uppercase tracking-wide text-slate-500">
        Question {index + 1} of {total}
      </p>
      <h2 className="mt-2 text-lg font-bold text-slate-100">{question.text}</h2>
      <div className="mt-4 grid gap-2">
        {question.options.map((opt) => (
          <button
            key={opt.key}
            type="button"
            onClick={() => onAnswer(question.number, opt.key)}
            className={`rounded-lg border px-3 py-2 text-left text-sm ${
              answer === opt.key
                ? 'border-cyan-400/70 bg-cyan-500/15 text-cyan-100'
                : 'border-[#1a3a5c] bg-[#071020] text-slate-300 hover:border-cyan-500/40'
            }`}
          >
            {opt.text}
          </button>
        ))}
      </div>
    </div>
  );
}

function ResultsScreen({ results, onContinue }) {
  return (
    <div className={CARD}>
      <p className="text-xs uppercase tracking-[0.3em] text-cyan-400/70">Results</p>
      <h2 className="mt-1 text-2xl font-black text-slate-100">Your Path Matches</h2>
      <ul className="mt-4 space-y-2">
        {results.map((r) => {
          const data = getPathData(r.path_code);
          return (
            <li
              key={r.path_code}
              className="flex items-center justify-between rounded-lg border border-[#1a3a5c] bg-[#071020] px-3 py-2"
            >
              <div className="flex items-center gap-2">
                <span className="text-xl">{data?.icon || '•'}</span>
                <div>
                  <p className="text-sm font-semibold text-slate-100">
                    #{r.rank} {r.path_name}
                  </p>
                  {data?.tagline ? (
                    <p className="text-xs text-slate-400">{data.tagline}</p>
                  ) : null}
                </div>
              </div>
              <span className="text-sm font-bold text-cyan-300">
                {r.match_percentage}%
              </span>
            </li>
          );
        })}
      </ul>
      <button
        type="button"
        onClick={onContinue}
        className="mt-5 rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-4 py-2 text-cyan-200"
      >
        Choose Your Path
      </button>
    </div>
  );
}

function PathCardsScreen({ results, onChoose }) {
  return (
    <div className="space-y-3">
      <div className={CARD}>
        <p className="text-xs uppercase tracking-[0.3em] text-cyan-400/70">Choose</p>
        <h2 className="mt-1 text-2xl font-black text-slate-100">Pick Your Path</h2>
        <p className="mt-2 text-sm text-slate-400">
          Your top match is highlighted, but the choice is yours.
        </p>
      </div>
      {results.map((r) => {
        const data = getPathData(r.path_code);
        if (!data) return null;
        return (
          <div key={r.path_code} className={CARD}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-lg font-bold text-slate-100">
                  {data.icon} {data.name}
                </p>
                <p className="text-xs text-slate-400">{data.tagline}</p>
              </div>
              <span className="text-sm font-bold text-cyan-300">
                {r.match_percentage}%
              </span>
            </div>
            <p className="mt-3 text-sm text-slate-300">{data.thisPathIsForYouIf}</p>
            <button
              type="button"
              onClick={() => onChoose(r.path_code)}
              className="mt-3 rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-4 py-2 text-sm text-cyan-200"
            >
              Choose {data.name}
            </button>
          </div>
        );
      })}
    </div>
  );
}

function CommitmentScreen({ pendingPath, onConfirm, onBack, saving, error }) {
  const data = getPathData(pendingPath);
  if (!data) return null;
  return (
    <div className={CARD}>
      <p className="text-xs uppercase tracking-[0.3em] text-cyan-400/70">Commitment</p>
      <h2 className="mt-1 text-2xl font-black text-slate-100">
        {data.icon} {data.name}
      </h2>
      <p className="mt-3 whitespace-pre-line text-sm text-slate-300">
        {data.commitmentMessage}
      </p>
      {error ? <p className="mt-3 text-sm text-rose-300">{error}</p> : null}
      <div className="mt-5 flex gap-2">
        <button
          type="button"
          onClick={onBack}
          className="rounded-lg border border-[#1a3a5c] bg-[#071020] px-4 py-2 text-sm text-slate-300"
        >
          Back
        </button>
        <button
          type="button"
          onClick={onConfirm}
          disabled={saving}
          className="rounded-lg border border-emerald-500/50 bg-emerald-500/10 px-4 py-2 text-emerald-200 disabled:opacity-50"
        >
          {saving ? 'Committing…' : 'I Commit to This Path'}
        </button>
      </div>
    </div>
  );
}

export default function PathDiscoveryPage({ onNavigate }) {
  const ctx = usePath();
  const {
    screen,
    setScreen,
    questions,
    currentIndex,
    answers,
    results,
    pendingPath,
    selectedPath,
    savingPath,
    loading,
    error,
    startQuiz,
    answerQuestion,
    goToPathCards,
    choosePath,
    confirmPath,
  } = ctx;

  // If a path was just confirmed, route to onboarding so the user
  // continues into the path-specific flow.
  useEffect(() => {
    if (selectedPath && screen === QUIZ_SCREEN.COMMITMENT) {
      onNavigate('/path-onboarding');
    }
  }, [selectedPath, screen, onNavigate]);

  const handleConfirm = async () => {
    const ok = await confirmPath();
    if (ok) onNavigate('/path-onboarding');
  };

  const currentQuestion = questions[currentIndex];

  return (
    <div className="min-h-screen bg-[#050d1a] p-4 sm:p-8">
      <div className="mx-auto max-w-3xl space-y-4">
        {error ? (
          <div className={CARD}>
            <p className="text-sm text-rose-300">{error}</p>
          </div>
        ) : null}

        {screen === QUIZ_SCREEN.WELCOME && (
          <WelcomeScreen onStart={startQuiz} loading={loading} />
        )}

        {screen === QUIZ_SCREEN.QUESTION && (
          <QuestionScreen
            question={currentQuestion}
            index={currentIndex}
            total={questions.length}
            onAnswer={answerQuestion}
            answer={currentQuestion ? answers[currentQuestion.number] : null}
          />
        )}

        {screen === QUIZ_SCREEN.RESULTS && (
          <ResultsScreen results={results} onContinue={goToPathCards} />
        )}

        {screen === QUIZ_SCREEN.PATH_CARDS && (
          <PathCardsScreen results={results} onChoose={choosePath} />
        )}

        {screen === QUIZ_SCREEN.COMMITMENT && (
          <CommitmentScreen
            pendingPath={pendingPath}
            onConfirm={handleConfirm}
            onBack={() => setScreen(QUIZ_SCREEN.PATH_CARDS)}
            saving={savingPath}
            error={error}
          />
        )}
      </div>
    </div>
  );
}
