const PATH_OPTIONS = [
  { value: 'runner', label: 'Runner', icon: '🏃', desc: 'Daily runs and cardio challenges.' },
  { value: 'gym', label: 'Gym', icon: '💪', desc: 'Strength training and lifting quests.' },
  { value: 'discipline', label: 'Discipline', icon: '🧠', desc: 'Focus, habits, and mental edge.' },
  { value: 'tournament', label: 'Tournament', icon: '⚔️', desc: 'Competitive performance goals.' },
  { value: '75_hard', label: '75 Hard', icon: '🔥', desc: 'The full 75 Hard protocol.' },
];

export default function OnboardingPage({ selectedPath, onSelectPath, onNavigate, savingPath }) {
  return (
    <div className="max-w-3xl space-y-6">
      <div className="relative overflow-hidden rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-6">
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />
        <p className="text-[10px] uppercase tracking-[0.25em] text-cyan-400/70">Progression Path</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-100">Choose Your Path</h1>
        <p className="mt-2 text-sm text-slate-500">
          Pick your current focus. Your path shapes which quests get assigned to you each day.
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {PATH_OPTIONS.map((option) => {
          const active = selectedPath === option.value;
          return (
            <button
              key={option.value}
              type="button"
              onClick={() => onSelectPath(option.value)}
              disabled={savingPath}
              className={`rounded-xl border p-5 text-left transition ${
                active
                  ? 'border-cyan-500/60 bg-cyan-500/10 shadow-[0_0_20px_rgba(6,182,212,0.12)]'
                  : 'border-[#1a3a5c] bg-[#0a1628] hover:border-cyan-500/30 hover:bg-[#0d1f38]'
              } disabled:cursor-not-allowed disabled:opacity-70`}
            >
              <p className="text-2xl">{option.icon}</p>
              <p className="mt-2 text-base font-semibold text-slate-100">{option.label}</p>
              <p className="mt-1 text-xs text-slate-500">{option.desc}</p>
              {active && (
                <span className="mt-3 inline-block rounded-full border border-cyan-500/50 bg-cyan-500/10 px-2 py-0.5 text-[10px] text-cyan-300">
                  Selected
                </span>
              )}
            </button>
          );
        })}
      </div>

      <button
        type="button"
        onClick={() => onNavigate('/dashboard')}
        className="rounded-lg border border-cyan-500/60 bg-cyan-500/15 px-6 py-2.5 font-semibold text-cyan-200 transition hover:bg-cyan-500/25"
      >
        Continue to Dashboard
      </button>
    </div>
  );
}
