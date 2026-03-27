export default function QuestCard({ quest, onComplete, loading }) {
  const completed = quest.assigned_completed_today ?? quest.completed_today;

  return (
    <div className={`flex items-center gap-4 py-3.5 px-1 transition ${completed ? 'opacity-60' : ''}`}>
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

      {/* EXP reward */}
      <span className={`flex-shrink-0 text-sm font-bold ${completed ? 'text-slate-600' : 'text-amber-400'}`}>
        +{quest.exp_reward} EXP
      </span>
    </div>
  );
}
