const PATH_OPTIONS = ['Runner', 'Gym', 'Discipline', 'Tournament', '75 Hard'];

export default function OnboardingPage({ selectedPath, onSelectPath, onNavigate }) {
  return (
    <section className="space-y-6">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
        <h1 className="text-2xl font-bold text-slate-100">Choose Your Path</h1>
        <p className="mt-2 text-sm text-slate-400">
          Pick your current focus. You can adjust this later as your goals evolve.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {PATH_OPTIONS.map((option) => {
          const active = selectedPath === option;
          return (
            <button
              key={option}
              type="button"
              onClick={() => onSelectPath(option)}
              className={`rounded-xl border p-5 text-left transition ${
                active
                  ? 'border-cyan-400/80 bg-cyan-500/15 shadow-[0_0_18px_rgba(34,211,238,0.18)]'
                  : 'border-slate-700 bg-slate-900/70 hover:border-cyan-500/40'
              }`}
            >
              <p className="text-lg font-semibold text-slate-100">{option}</p>
              <p className="mt-2 text-sm text-slate-400">Build momentum through consistent quests.</p>
            </button>
          );
        })}
      </div>

      <button
        type="button"
        onClick={() => onNavigate('/dashboard')}
        className="rounded-lg border border-cyan-500/70 bg-cyan-500/20 px-5 py-2 font-semibold text-cyan-200 hover:bg-cyan-500/30"
      >
        Continue to Dashboard
      </button>
    </section>
  );
}
