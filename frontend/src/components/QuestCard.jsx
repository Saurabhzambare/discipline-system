export default function QuestCard({ quest, onComplete, loading }) {
  const completed = quest.assigned_completed_today ?? quest.completed_today;
  const statusClass = completed
    ? 'border-emerald-500/50 bg-emerald-500/10 text-emerald-300'
    : 'border-cyan-500/40 bg-cyan-500/10 text-cyan-300';

  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900/70 p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h3 className="text-base font-semibold text-slate-100">{quest.title}</h3>
          <p className="mt-1 text-sm text-slate-400">{quest.description}</p>
          <div className="mt-2 flex flex-wrap gap-2 text-xs">
            <span className="rounded-full border border-slate-700 bg-slate-800/80 px-2 py-1 text-slate-300">
              {quest.category_display || quest.category}
            </span>
            <span className="rounded-full border border-slate-700 bg-slate-800/80 px-2 py-1 text-slate-300">
              {quest.difficulty_display || quest.difficulty}
            </span>
            <span className="rounded-full border border-slate-700 bg-slate-800/80 px-2 py-1 text-slate-300">
              {quest.recurrence_display || quest.recurrence}
            </span>
          </div>
        </div>
        <span className={`rounded-full border px-3 py-1 text-xs font-medium ${statusClass}`}>
          {completed ? 'Completed today' : 'Available'}
        </span>
      </div>

      <div className="mt-4 flex items-center justify-between">
        <p className="text-sm font-medium text-amber-300">+{quest.exp_reward} EXP</p>
        <button
          type="button"
          onClick={() => onComplete(quest.id)}
          disabled={loading || completed}
          className="rounded-lg border border-cyan-500/60 bg-cyan-500/20 px-4 py-2 text-sm font-medium text-cyan-200 transition hover:bg-cyan-500/30 disabled:cursor-not-allowed disabled:border-slate-700 disabled:bg-slate-800 disabled:text-slate-500"
        >
          {completed ? 'Done' : loading ? 'Completing...' : 'Complete'}
        </button>
      </div>
    </div>
  );
}
