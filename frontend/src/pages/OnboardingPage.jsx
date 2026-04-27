import { useCallback, useState } from 'react';
import { LOCKED_PATH, PATH_MAP } from '../data/pathData';
import { QUIZ_SCREEN, usePath } from '../contexts/pathContextShared';

// All five screens are dark, centered, single-column, and chromeless (no
// global navigation is rendered — Layout short-circuits on /onboarding).
// Visual direction: Loveable cinematic handoff. Product truth:
// docs/game-design/systems/path-discovery.md.

// ── Welcome Screen ────────────────────────────────────────────────────────────

function WelcomeScreen({ onStart, loading }) {
  return (
    <div className="min-h-screen bg-[#050d1a] flex flex-col items-center justify-center px-6 text-center">
      <div className="max-w-xl animate-fade-in">
        <h1 className="text-3xl md:text-4xl font-bold text-slate-100 leading-[1.35] mb-8">
          Before you begin your journey, Hunter — let us understand who
          you are right now.
        </h1>
        <p className="text-slate-400 text-base leading-relaxed mb-14 animate-fade-in-delay-1">
          There are no wrong answers. Only honest ones.
        </p>
        <button
          type="button"
          onClick={onStart}
          disabled={loading}
          className="animate-fade-in-delay-2 rounded-xl border border-slate-700/80 bg-slate-800/60 px-14 py-4 text-sm font-semibold text-slate-100 tracking-wide transition hover:border-slate-500 hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Preparing…' : 'Begin'}
        </button>
      </div>
    </div>
  );
}

// ── Question Screen ───────────────────────────────────────────────────────────

function QuestionScreen({ question, onAnswer, submitting }) {
  const [selected, setSelected] = useState(null);

  const handleSelect = useCallback(
    (key) => {
      if (selected || submitting) return;
      setSelected(key);
      // Tiny highlight moment before advancing so the tap feels acknowledged.
      setTimeout(() => {
        onAnswer(question.number, key);
        setSelected(null);
      }, 450);
    },
    [selected, submitting, question.number, onAnswer],
  );

  return (
    <div className="min-h-screen bg-[#050d1a] flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-xl animate-fade-in" key={question.number}>
        {/* No question number, no progress bar, no back button — by design. */}
        <h2 className="text-2xl md:text-3xl font-bold text-slate-100 text-center leading-snug mb-12">
          {question.text}
        </h2>

        <div className="flex flex-col gap-3">
          {question.options.map((option) => {
            const isSelected = selected === option.key;
            return (
              <button
                key={option.key}
                type="button"
                onClick={() => handleSelect(option.key)}
                disabled={Boolean(selected) || submitting}
                className={`w-full rounded-xl border px-5 py-4 text-left text-[15px] leading-relaxed transition-all duration-200 ${
                  isSelected
                    ? 'border-slate-300/60 bg-slate-700/40 text-slate-50'
                    : 'border-slate-800 bg-slate-900/60 text-slate-300 hover:border-slate-600 hover:bg-slate-800/70 hover:text-slate-100'
                } disabled:cursor-not-allowed`}
              >
                {option.text}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ── Results Screen ────────────────────────────────────────────────────────────

function ResultsScreen({ results, onExplore }) {
  const top = results[0];
  const topPath = top ? PATH_MAP[top.path_code] : null;

  return (
    <div className="min-h-screen bg-[#050d1a] flex flex-col items-center justify-center px-6 py-16">
      <div className="w-full max-w-xl animate-fade-in">
        {/* Path-specific opener — large, in top-path accent colour. */}
        {topPath && (
          <h2
            className="text-2xl md:text-3xl font-bold text-center leading-[1.35] mb-12"
            style={{ color: topPath.color.accent }}
          >
            {topPath.resultsOpener}
          </h2>
        )}

        {/* Ranked path list with animated percentage bars. */}
        <div className="flex flex-col gap-3 mb-12 animate-fade-in-delay-1">
          {results.map((r, idx) => {
            const path = PATH_MAP[r.path_code];
            if (!path) return null;
            const isTop = idx === 0;
            return (
              <div
                key={r.path_code}
                className="rounded-xl border px-5 py-4 transition"
                style={
                  isTop
                    ? {
                        borderColor: path.color.accent,
                        backgroundColor: `${path.color.accent}12`,
                        boxShadow: `0 0 28px ${path.color.accent}22`,
                      }
                    : {
                        borderColor: '#1e293b',
                        backgroundColor: 'rgba(15, 23, 42, 0.5)',
                      }
                }
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className="text-xl leading-none">{path.icon}</span>
                    <span
                      className={`text-sm font-semibold ${isTop ? 'text-slate-50' : 'text-slate-200'}`}
                    >
                      {path.name}
                    </span>
                  </div>
                  <span
                    className="text-sm font-bold tabular-nums"
                    style={{ color: isTop ? path.color.accent : '#94a3b8' }}
                  >
                    {r.match_percentage}%
                  </span>
                </div>
                <div className="h-1.5 w-full rounded-full bg-slate-800/70 overflow-hidden">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${r.match_percentage}%`,
                      backgroundColor: path.color.accent,
                      opacity: isTop ? 1 : 0.55,
                      transition: 'width 900ms ease-out',
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        <p className="text-center text-xs text-slate-500 mb-8 animate-fade-in-delay-2">
          Your strongest match is highlighted. Explore all paths before choosing.
        </p>

        <div className="flex justify-center animate-fade-in-delay-2">
          <button
            type="button"
            onClick={onExplore}
            className="rounded-xl border border-slate-600 bg-slate-800/70 px-10 py-3.5 text-sm font-semibold text-slate-100 tracking-wide transition hover:border-slate-400 hover:bg-slate-800"
          >
            Explore Your Paths
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Path Cards Screen ─────────────────────────────────────────────────────────

function PathCardsScreen({ results, onChoose, saving }) {
  // Order by match percentage (server-sorted results are the source of truth).
  const orderedPaths = results
    .map((r) => {
      const path = PATH_MAP[r.path_code];
      return path ? { ...path, matchPct: r.match_percentage } : null;
    })
    .filter(Boolean);

  return (
    <div className="min-h-screen bg-[#050d1a] px-4 py-12 overflow-y-auto">
      <div className="max-w-xl mx-auto animate-fade-in">
        <div className="flex flex-col gap-6">
          {orderedPaths.map((path) => (
            <PathCard
              key={path.code}
              path={path}
              matchPct={path.matchPct}
              onChoose={onChoose}
              saving={saving}
            />
          ))}
          <LockedPathCard />
        </div>
      </div>
    </div>
  );
}

function PathCard({ path, matchPct, onChoose, saving }) {
  return (
    <div
      className="rounded-2xl border overflow-hidden"
      style={{
        borderColor: `${path.color.accent}40`,
        backgroundColor: 'rgba(15, 23, 42, 0.45)',
      }}
    >
      {/* Header */}
      <div className="px-6 pt-6 pb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-2xl leading-none">{path.icon}</span>
          <h3 className="text-lg font-bold text-slate-50">{path.name}</h3>
        </div>
        <span
          className="text-[11px] font-bold tracking-wide px-2.5 py-1 rounded-full"
          style={{ color: path.color.accent, backgroundColor: `${path.color.accent}1f` }}
        >
          {matchPct}% match
        </span>
      </div>

      {/* Sections (always expanded per design spec). */}
      <div className="px-6 pb-2">
        <Section label="Who you are now" color={path.color.accent}>
          <p className="text-sm text-slate-300 leading-relaxed">{path.whoYouAreNow}</p>
        </Section>

        <Section label="Who you become" color={path.color.accent}>
          <p className="text-sm text-slate-300 leading-relaxed">{path.whoYouBecome}</p>
        </Section>

        <Section label="What you gain" color={path.color.accent}>
          <ul className="flex flex-col gap-1.5">
            {path.whatYouGain.map((item) => (
              <li key={item} className="flex items-start gap-2 text-sm text-slate-300">
                <span
                  className="mt-[7px] h-1 w-1 flex-shrink-0 rounded-full"
                  style={{ backgroundColor: path.color.accent }}
                />
                {item}
              </li>
            ))}
          </ul>
        </Section>

        <Section label="This path is for you if" color={path.color.accent}>
          <p className="text-sm text-slate-400 leading-relaxed">{path.thisPathIsForYouIf}</p>
        </Section>
      </div>

      {/* Choose CTA — strong, solid in path accent. */}
      <div className="px-6 pt-2 pb-6">
        <button
          type="button"
          onClick={() => onChoose(path.code)}
          disabled={saving}
          className="w-full rounded-xl py-3.5 text-sm font-bold text-white transition hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
          style={{ backgroundColor: path.color.accent }}
        >
          Choose {path.name}
        </button>
      </div>
    </div>
  );
}

function Section({ label, color, children }) {
  return (
    <div className="py-3 border-t border-slate-800/80 first:border-t-0">
      <p
        className="text-[10px] uppercase tracking-[0.18em] mb-2 font-semibold"
        style={{ color }}
      >
        {label}
      </p>
      {children}
    </div>
  );
}

function LockedPathCard() {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/40 overflow-hidden opacity-70">
      <div className="px-6 py-8 flex flex-col items-center text-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6 text-slate-500"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={1.8}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 11c-1.1 0-2 .9-2 2v2h4v-2c0-1.1-.9-2-2-2zM6 11V8a6 6 0 0112 0v3M5 11h14v10H5z"
          />
        </svg>
        <p className="text-sm font-semibold text-slate-400">Coming Soon</p>
        <p className="text-xs text-slate-600 max-w-xs">{LOCKED_PATH.lockedMessage}</p>
      </div>
    </div>
  );
}

// ── Commitment Screen ─────────────────────────────────────────────────────────

function CommitmentScreen({ pathCode, onConfirm, saving, error }) {
  const path = pathCode ? PATH_MAP[pathCode] : null;
  if (!path) return null;

  const lines = path.commitmentMessage.split('\n');

  return (
    <div className="min-h-screen bg-[#050d1a] flex flex-col items-center justify-center px-6 text-center">
      <div className="max-w-lg animate-fade-in">
        {/* Path icon framed in a soft halo in path colour. */}
        <div
          className="mx-auto mb-10 flex h-24 w-24 items-center justify-center rounded-full border"
          style={{
            borderColor: `${path.color.accent}60`,
            backgroundColor: `${path.color.accent}12`,
            boxShadow: `0 0 60px ${path.color.accent}33`,
          }}
        >
          <span className="text-4xl leading-none">{path.icon}</span>
        </div>

        <div className="mb-12 space-y-4 animate-fade-in-delay-1">
          {lines.map((line, i) => {
            const isTitle = i === 0;
            const isClosing = i === lines.length - 1;
            return (
              <p
                key={i}
                className={
                  isTitle
                    ? 'text-xl md:text-2xl font-bold text-slate-50 leading-snug'
                    : isClosing
                    ? 'text-sm font-semibold tracking-wide mt-6'
                    : 'text-[15px] text-slate-300 leading-relaxed'
                }
                style={isClosing ? { color: path.color.accent } : undefined}
              >
                {line}
              </p>
            );
          })}
        </div>

        {error && (
          <p className="text-xs text-rose-400 mb-4" role="alert">
            {error}
          </p>
        )}

        <button
          type="button"
          onClick={onConfirm}
          disabled={saving}
          className="w-full max-w-sm rounded-xl py-4 text-sm font-bold text-white tracking-wide transition hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed animate-fade-in-delay-2"
          style={{ backgroundColor: path.color.accent }}
        >
          {saving ? 'Saving your path…' : 'Begin My Journey'}
        </button>
      </div>
    </div>
  );
}

// ── Main Page Component ───────────────────────────────────────────────────────

export default function OnboardingPage({ onNavigate }) {
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

  // Atomic: server persists selection before we route onward. If it fails,
  // stay on the commitment screen and surface the error.
  const handleBeginJourney = useCallback(async () => {
    const success = await confirmPath();
    if (success) onNavigate('/path-onboarding');
  }, [confirmPath, onNavigate]);

  const currentQuestion = questions[currentIndex] || null;

  switch (screen) {
    case QUIZ_SCREEN.WELCOME:
      return <WelcomeScreen onStart={startQuiz} loading={loading} />;

    case QUIZ_SCREEN.QUESTION:
      if (!currentQuestion) return null;
      return (
        <QuestionScreen
          key={currentQuestion.number}
          question={currentQuestion}
          onAnswer={handleAnswer}
          submitting={submitting}
        />
      );

    case QUIZ_SCREEN.RESULTS:
      return <ResultsScreen results={results} onExplore={goToPathCards} />;

    case QUIZ_SCREEN.PATH_CARDS:
      return (
        <PathCardsScreen results={results} onChoose={choosePath} saving={savingPath} />
      );

    case QUIZ_SCREEN.COMMITMENT:
      return (
        <CommitmentScreen
          pathCode={pendingPath}
          onConfirm={handleBeginJourney}
          saving={savingPath}
          error={error}
        />
      );

    default:
      return <WelcomeScreen onStart={startQuiz} loading={loading} />;
  }
}
