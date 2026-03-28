import { useEffect, useRef, useState } from 'react';

export default function QuestCard({ quest, onComplete, loading, onShare }) {
  const completed = quest.assigned_completed_today ?? quest.completed_today;
  const prevCompletedRef = useRef(completed);
  const [justCompleted, setJustCompleted] = useState(false);
  const [shareFlash, setShareFlash] = useState(false);

  // Detect transition from not-completed → completed to trigger glow
  useEffect(() => {
    if (!prevCompletedRef.current && completed) {
      setJustCompleted(true);
      const t = setTimeout(() => setJustCompleted(false), 2000);
      return () => clearTimeout(t);
    }
    prevCompletedRef.current = completed;
  }, [completed]);

  async function handleShare() {
    setShareFlash(true);
    try {
      await onShare(quest);
    } finally {
      setTimeout(() => setShareFlash(false), 1500);
    }
  }

  return (
    <div
      className={`flex items-center gap-4 py-3.5 px-1 transition-all duration-500 rounded-lg ${
        justCompleted
          ? 'bg-emerald-500/10 shadow-[0_0_16px_rgba(16,185,129,0.2)]'
          : completed
            ? 'opacity-60'
            : ''
      }`}
    >
      {/* Checkbox */}
      <button
        type="button"
        onClick={() => !completed && onComplete(quest.id)}
        disabled={loading || completed}
        aria-label={completed ? 'Quest completed' : 'Complete quest'}
        className={`flex h-6 w-6 flex-shrink-0 items-center justify-center rounded border-2 transition ${
          completed
            ? 'border-cyan-500/60 bg-cyan-500/20 text-cyan-300'
            : loading
              ? 'border-slate-600 bg-slate-800 text-slate-600'
              : 'border-slate-600 bg-transparent hover:border-cyan-500/60 hover:bg-cyan-500/10'
        } disabled:cursor-not-allowed`}
      >
        {completed ? (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        ) : loading ? (
          <span className="block h-2.5 w-2.5 animate-spin rounded-full border border-slate-500 border-t-cyan-400" />
        ) : null}
      </button>

      {/* Quest info */}
      <div className="flex-1 min-w-0">
        <p className={`text-sm font-medium ${completed ? 'text-slate-500 line-through' : 'text-slate-200'}`}>
          {quest.title}
        </p>
        <div className="mt-0.5 flex flex-wrap items-center gap-2 text-[10px] text-slate-500">
          <span>{quest.category_display || quest.category}</span>
          <span>·</span>
          <span>{quest.difficulty_display || quest.difficulty}</span>
          <span>·</span>
          <span>{quest.recurrence_display || quest.recurrence}</span>
        </div>
      </div>

      {/* Right side: EXP + share button */}
      <div className="flex flex-shrink-0 items-center gap-2">
        {completed && onShare ? (
          <button
            type="button"
            onClick={handleShare}
            className={`rounded-md border px-2 py-1 text-[10px] font-medium transition ${
              shareFlash
                ? 'border-emerald-500/50 bg-emerald-500/15 text-emerald-300'
                : 'border-[#1a3a5c] text-slate-500 hover:border-cyan-500/40 hover:text-cyan-300'
            }`}
          >
            {shareFlash ? 'Shared!' : 'Share'}
          </button>
        ) : null}
        <span className={`text-sm font-bold ${completed ? 'text-slate-600' : 'text-amber-400'}`}>
          +{quest.exp_reward} EXP
        </span>
      </div>
    </div>
  );
}
