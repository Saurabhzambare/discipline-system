import { useEffect, useRef, useState } from 'react';

export default function QuestCard({ quest, onComplete, loading, onShare }) {
  const completed = quest.assigned_completed_today ?? quest.completed_today;
  const prevCompletedRef = useRef(completed);
  const [justCompleted, setJustCompleted] = useState(false);
  const [shareFlash, setShareFlash] = useState(false);

  // Note input state (Feature B)
  const [showNote, setShowNote] = useState(false);
  const [note, setNote] = useState('');

  // Detect transition from not-completed → completed to trigger glow
  useEffect(() => {
    if (!prevCompletedRef.current && completed) {
      setJustCompleted(true);
      setShowNote(false);
      const t = setTimeout(() => setJustCompleted(false), 2000);
      return () => clearTimeout(t);
    }
    prevCompletedRef.current = completed;
  }, [completed]);

  function handleCheckboxClick() {
    if (completed || loading) return;
    setShowNote(true);
  }

  async function handleComplete() {
    setShowNote(false);
    await onComplete(quest.id, note.trim() || null);
    setNote('');
  }

  function handleSkip() {
    setShowNote(false);
    onComplete(quest.id, null);
    setNote('');
  }

  async function handleShare() {
    setShareFlash(true);
    try {
      await onShare(quest, note.trim() || null);
    } finally {
      setTimeout(() => setShareFlash(false), 1500);
    }
  }

  return (
    <div
      className={`py-3.5 px-1 transition-all duration-500 rounded-lg ${
        justCompleted
          ? 'bg-emerald-500/10 shadow-[0_0_16px_rgba(16,185,129,0.2)]'
          : completed
            ? 'opacity-60'
            : ''
      }`}
    >
      <div className="flex items-center gap-4">
        {/* Checkbox */}
        <button
          type="button"
          onClick={handleCheckboxClick}
          disabled={loading || completed}
          aria-label={completed ? 'Quest completed' : 'Complete quest'}
          className={`flex h-6 w-6 flex-shrink-0 items-center justify-center rounded border-2 transition ${
            completed
              ? 'border-cyan-500/60 bg-cyan-500/20 text-cyan-300'
              : loading
                ? 'border-slate-600 bg-slate-800 text-slate-600'
                : showNote
                  ? 'border-cyan-500/60 bg-cyan-500/10'
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

        {/* Right: share + EXP */}
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

      {/* Inline note panel (Feature B) */}
      {showNote && (
        <div className="mt-3 ml-10 space-y-2 rounded-lg border border-cyan-500/20 bg-cyan-500/5 p-3">
          <p className="text-xs text-cyan-300/80">Add a note (optional) — what did you do?</p>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="e.g. Ran 5km at 6am, felt great..."
            rows={2}
            autoFocus
            className="w-full rounded-lg border border-[#1a3a5c] bg-[#06101e] px-3 py-2 text-xs text-slate-100 outline-none focus:ring focus:ring-cyan-400/20 placeholder:text-slate-600"
          />
          <div className="flex gap-2">
            <button
              type="button"
              onClick={handleComplete}
              className="rounded-lg border border-cyan-500/50 bg-cyan-500/15 px-3 py-1.5 text-xs font-medium text-cyan-200 hover:bg-cyan-500/25"
            >
              Complete Quest
            </button>
            <button
              type="button"
              onClick={handleSkip}
              className="rounded-lg border border-[#1a3a5c] px-3 py-1.5 text-xs text-slate-400 hover:text-slate-200"
            >
              Skip Note
            </button>
            <button
              type="button"
              onClick={() => setShowNote(false)}
              className="ml-auto text-xs text-slate-600 hover:text-slate-400"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
