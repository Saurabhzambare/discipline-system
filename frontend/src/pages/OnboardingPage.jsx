import { useCallback, useState } from 'react';
import { LOCKED_PATH, PATH_DATA, PATH_MAP } from '../data/pathData';
import { QUIZ_SCREEN, usePath } from '../contexts/PathContext';

// ── Welcome Screen ────────────────────────────────────────────────────────────

function WelcomeScreen({ onStart, loading }) {
  return (
    <div className="min-h-screen bg-[#050d1a] flex flex-col items-center justify-center px-6 text-center">
      <div className="max-w-md animate-fade-in">
        <p className="text-xs uppercase tracking-[0.4em] text-cyan-400/60 mb-8">
          Identity Trial
        </p>
        <h1 className="text-4xl font-black text-slate-100 leading-tight mb-6">
          Discover Your Path
        </h1>
        <p className="text-slate-400 leading-relaxed mb-3">
          Before you begin your journey Hunter — let us understand who you are right now.
        </p>
        <p className="text-slate-500 text-sm leading-relaxed mb-12">
          There are no wrong answers.
          <br />
          Only honest ones.
        </p>
        <button
          type="button"
          onClick={onStart}
          disabled={loading}
          className="rounded-xl border border-cyan-500/50 bg-cyan-500/10 px-10 py-4 text-base font-bold text-cyan-200 transition hover:bg-cyan-500/20 hover:border-cyan-400/70 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Preparing...' : 'Begin'}
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
      setTimeout(() => {
        onAnswer(question.number, key);
        setSelected(null);
      }, 500);
    },
    [selected, submitting, question.number, onAnswer],
  );

  return (
    <div className="min-h-screen bg-[#050d1a] flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-lg">
        {/* Question text */}
        <h2 className="text-xl font-bold text-slate-100 text-center leading-snug mb-10">
          {question.text}
        </h2>

        {/* Answer options */}
        <div className="flex flex-col gap-3">
          {question.options.map((option) => {
            const isSelected = selected === option.key;
            return (
              <button
                key={option.key}
                type="button"
                onClick={() => handleSelect(option.key)}
                disabled={Boolean(selected) || submitting}
                className={`w-full rounded-xl border px-5 py-4 text-left text-sm leading-relaxed transition-all duration-200 ${
                  isSelected
                    ? 'border-cyan-400/70 bg-cyan-500/15 text-cyan-100 shadow-[0_0_20px_rgba(6,182,212,0.15)]'
                    : 'border-[#1a3a5c] bg-[#0a1628] text-slate-300 hover:border-[#2a4a7c] hover:bg-[#0d1f38]'
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
  const opener = topPath?.resultsOpener || '';

  return (
    <div className="min-h-screen bg-[#050d1a] flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-lg">
        <p className="text-xs uppercase tracking-[0.4em] text-cyan-400/60 text-center mb-4">
          Your Path Affinity
        </p>

        {/* Top path opener */}
        {opener && (
          <p
            className="text-center text-slate-300 text-sm leading-relaxed mb-10 italic border-l-2 pl-4 mx-4"
            style={{ borderColor: topPath?.color?.accent || '#06b6d4' }}
          >
            {opener}
          </p>
        )}

        {/* All 5 paths with percentage bars */}
        <div className="flex flex-col gap-4 mb-10">
          {results.map((r, idx) => {
            const path = PATH_MAP[r.path_code];
            if (!path) return null;
            const isTop = idx === 0;
            return (
              <div
                key={r.path_code}
                className={`rounded-xl border p-4 transition-all ${
                  isTop
                    ? 'border-opacity-70 shadow-lg'
                    : 'border-[#1a3a5c] bg-[#080f1e]'
                }`}
                style={
                  isTop
                    ? {
                        borderColor: path.color.accent,
                        backgroundColor: `${path.color.bg}55`,
                        boxShadow: `0 0 24px ${path.color.accent}25`,
                      }
                    : {}
                }
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{path.icon}</span>
                    <span className={`text-sm font-bold ${isTop ? 'text-slate-100' : 'text-slate-300'}`}>
                      {path.name}
                    </span>
                    {isTop && (
                      <span
                        className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full"
                        style={{ color: path.color.accent, backgroundColor: `${path.color.accent}20` }}
                      >
                        Top Match
                      </span>
                    )}
                  </div>
                  <span
                    className="text-sm font-black"
                    style={{ color: isTop ? path.color.accent : '#94a3b8' }}
                  >
                    {r.match_percentage}%
                  </span>
                </div>
                {/* Progress bar */}
                <div className="h-1.5 w-full rounded-full bg-slate-800 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{
                      width: `${r.match_percentage}%`,
                      backgroundColor: path.color.accent,
                      opacity: isTop ? 1 : 0.5,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        <p className="text-center text-xs text-slate-500 mb-8">
          Your strongest match is highlighted. All paths are always available to you.
        </p>

        <div className="flex justify-center">
          <button
            type="button"
            onClick={onExplore}
            className="rounded-xl border border-cyan-500/50 bg-cyan-500/10 px-10 py-4 text-sm font-bold text-cyan-200 hover:bg-cyan-500/20 transition"
          >
            Explore Your Paths →
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Path Cards Screen ─────────────────────────────────────────────────────────

function PathCardsScreen({ results, onChoose }) {
  // Order PATH_DATA by match percentage from results
  const orderedPaths = results
    .map((r) => ({ ...PATH_MAP[r.path_code], matchPct: r.match_percentage }))
    .filter(Boolean);

  return (
    <div className="min-h-screen bg-[#050d1a] px-4 py-10 overflow-y-auto">
      <div className="max-w-lg mx-auto">
        <p className="text-xs uppercase tracking-[0.4em] text-cyan-400/60 text-center mb-2">
          Choose Your Path
        </p>
        <h2 className="text-2xl font-black text-slate-100 text-center mb-8">
          Your Results
        </h2>

        <div className="flex flex-col gap-6">
          {/* Live path cards */}
          {orderedPaths.map((path) => (
            <PathCard key={path.code} path={path} matchPct={path.matchPct} onChoose={onChoose} />
          ))}

          {/* Locked 6th path */}
          <LockedPathCard />
        </div>
      </div>
    </div>
  );
}

function PathCard({ path, matchPct, onChoose }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div
      className="rounded-2xl border overflow-hidden"
      style={{ borderColor: `${path.color.accent}40`, backgroundColor: `${path.color.bg}33` }}
    >
      {/* Card header */}
      <div
        className="px-5 pt-5 pb-4"
        style={{ borderBottom: `1px solid ${path.color.accent}20` }}
      >
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-3">
            <span className="text-3xl">{path.icon}</span>
            <div>
              <h3 className="text-lg font-black text-slate-100">{path.name}</h3>
              <p className="text-xs text-slate-400 mt-0.5">{path.tagline}</p>
            </div>
          </div>
          {/* Match badge */}
          <span
            className="text-xs font-black px-2.5 py-1 rounded-full flex-shrink-0"
            style={{ color: path.color.accent, backgroundColor: `${path.color.accent}20` }}
          >
            {matchPct}% match
          </span>
        </div>
      </div>

      {/* Who you are now */}
      <div className="px-5 py-4">
        <p className="text-[11px] uppercase tracking-widest mb-2" style={{ color: path.color.accent }}>
          Where you are now
        </p>
        <p className="text-sm text-slate-400 leading-relaxed">{path.whoYouAreNow}</p>
      </div>

      {/* Expandable details */}
      {expanded && (
        <>
          <div className="px-5 py-4 border-t border-slate-800">
            <p className="text-[11px] uppercase tracking-widest mb-2" style={{ color: path.color.accent }}>
              Who you become in 90 days
            </p>
            <p className="text-sm text-slate-400 leading-relaxed">{path.whoYouBecome}</p>
          </div>

          <div className="px-5 py-4 border-t border-slate-800">
            <p className="text-[11px] uppercase tracking-widest mb-3" style={{ color: path.color.accent }}>
              What you gain
            </p>
            <ul className="flex flex-col gap-2">
              {path.whatYouGain.map((item) => (
                <li key={item} className="flex items-start gap-2 text-sm text-slate-400">
                  <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full" style={{ backgroundColor: path.color.accent }} />
                  {item}
                </li>
              ))}
            </ul>
          </div>

          <div className="px-5 py-4 border-t border-slate-800">
            <p className="text-[11px] uppercase tracking-widest mb-2" style={{ color: path.color.accent }}>
              This path is for you if
            </p>
            <p className="text-sm text-slate-400 leading-relaxed italic">{path.thisPathIsForYouIf}</p>
          </div>
        </>
      )}

      {/* Card actions */}
      <div className="px-5 pb-5 flex items-center gap-3">
        <button
          type="button"
          onClick={() => setExpanded((e) => !e)}
          className="flex-1 rounded-xl border border-slate-700 bg-slate-800/50 py-2.5 text-xs font-semibold text-slate-400 hover:text-slate-200 hover:border-slate-600 transition"
        >
          {expanded ? 'Show less' : 'Read more'}
        </button>
        <button
          type="button"
          onClick={() => onChoose(path.code)}
          className="flex-1 rounded-xl border py-2.5 text-xs font-bold transition hover:opacity-90"
          style={{
            borderColor: path.color.accent,
            backgroundColor: `${path.color.accent}18`,
            color: path.color.accent,
          }}
        >
          Choose {path.name}
        </button>
      </div>
    </div>
  );
}

function LockedPathCard() {
  const [tapped, setTapped] = useState(false);
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/40 overflow-hidden opacity-60">
      <div className="px-5 py-5 flex items-center gap-4">
        <span className="text-3xl grayscale">🔒</span>
        <div className="flex-1">
          <h3 className="text-lg font-black text-slate-500">{LOCKED_PATH.name}</h3>
          <p className="text-xs text-slate-600 mt-0.5">{LOCKED_PATH.tagline}</p>
        </div>
        <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-slate-800 text-slate-500">
          Coming Soon
        </span>
      </div>
      <div className="px-5 pb-5">
        {tapped ? (
          <p className="text-xs text-slate-500 italic">{LOCKED_PATH.lockedMessage}</p>
        ) : (
          <button
            type="button"
            onClick={() => setTapped(true)}
            className="w-full rounded-xl border border-slate-700 bg-slate-800/30 py-2.5 text-xs font-semibold text-slate-600 cursor-not-allowed"
          >
            Path Locked
          </button>
        )}
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
      <div className="max-w-md">
        <span className="text-6xl mb-6 block">{path.icon}</span>

        <div className="mb-8 space-y-3">
          {lines.map((line, i) => (
            <p
              key={i}
              className={
                i === 0
                  ? 'text-xl font-black text-slate-100'
                  : i === lines.length - 1
                  ? 'text-sm font-bold mt-4'
                  : 'text-sm text-slate-400 leading-relaxed'
              }
              style={i === lines.length - 1 ? { color: path.color.accent } : {}}
            >
              {line}
            </p>
          ))}
        </div>

        {error && (
          <p className="text-xs text-red-400 mb-4">{error}</p>
        )}

        <button
          type="button"
          onClick={onConfirm}
          disabled={saving}
          className="rounded-xl border px-10 py-4 text-sm font-bold transition hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
          style={{
            borderColor: path.color.accent,
            backgroundColor: `${path.color.accent}18`,
            color: path.color.accent,
          }}
        >
          {saving ? 'Saving your path...' : 'Begin My Journey'}
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

  const handleBeginJourney = useCallback(async () => {
    const success = await confirmPath();
    if (success) onNavigate('/dashboard');
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
      return <PathCardsScreen results={results} onChoose={choosePath} />;

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
