export default function QuestCard({ quest, onComplete, loading }) {
  const statusClass = quest.completed_today
    ? 'border-emerald-500/50 bg-emerald-500/10 text-emerald-300'
    : 'border-cyan-500/40 bg-cyan-500/10 text-cyan-300';

  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900/70 p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h3 className="text-base font-semibold text-slate-100">{quest.title}</h3>
          <p className="mt-1 text-sm text-slate-400">{quest.description}</p>
        </div>
        <span className={`rounded-full border px-3 py-1 text-xs font-medium ${statusClass}`}>
          {quest.completed_today ? 'Completed today' : 'Available'}
        </span>
      </div>

      <div className="mt-4 flex items-center justify-between">
        <p className="text-sm font-medium text-amber-300">+{quest.exp_reward} EXP</p>
        <button
          type="button"
          onClick={() => onComplete(quest.id)}
          disabled={loading || quest.completed_today}
          className="rounded-lg border border-cyan-500/60 bg-cyan-500/20 px-4 py-2 text-sm font-medium text-cyan-200 transition hover:bg-cyan-500/30 disabled:cursor-not-allowed disabled:border-slate-700 disabled:bg-slate-800 disabled:text-slate-500"
        >
          {quest.completed_today ? 'Done' : loading ? 'Completing...' : 'Complete'}
        </button>
      </div>
    </div>
  );
}
