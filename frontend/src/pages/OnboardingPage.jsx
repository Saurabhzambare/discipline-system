const PATH_OPTIONS = [
  {
    value: 'runner',
    label: 'Runner',
    icon: '🏃',
    desc: 'Daily runs, sprint intervals, and cardio challenges built around distance and pace.',
    quests: ['Morning run — 3 km', 'Sprint intervals', 'Weekly long run'],
    color: 'emerald',
  },
  {
    value: 'gym',
    label: 'Gym',
    icon: '💪',
    desc: 'Strength training, progressive overload, and nutrition discipline.',
    quests: ['Workout session — 45 min', 'Hit protein target', 'Log your lifts'],
    color: 'cyan',
  },
  {
    value: 'discipline',
    label: 'Discipline',
    icon: '🧠',
    desc: 'Cold showers, early rises, no social media, deep focus habits.',
    quests: ['Cold shower — 2 min', 'Wake up before 6 AM', 'No social media before noon'],
    color: 'violet',
  },
  {
    value: 'tournament',
    label: 'Tournament',
    icon: '⚔️',
    desc: 'Competitive performance, skill practice, and mental conditioning.',
    quests: ['1 hr deliberate practice', 'Study 2 replays', 'Compete in a match'],
    color: 'amber',
  },
  {
    value: '75_hard',
    label: '75 Hard',
    icon: '🔥',
    desc: 'The full 75 Hard protocol. Two workouts, strict diet, gallon of water, 10 pages daily.',
    quests: ['Workout #1 — 45 min', 'Workout #2 outdoors', 'Follow your diet'],
    color: 'rose',
  },
];

const COLOR_MAP = {
  emerald: {
    active: 'border-emerald-500/60 bg-emerald-500/10 shadow-[0_0_20px_rgba(16,185,129,0.12)]',
    badge: 'border-emerald-500/50 bg-emerald-500/10 text-emerald-300',
    dot: 'bg-emerald-400',
  },
  cyan: {
    active: 'border-cyan-500/60 bg-cyan-500/10 shadow-[0_0_20px_rgba(6,182,212,0.12)]',
    badge: 'border-cyan-500/50 bg-cyan-500/10 text-cyan-300',
    dot: 'bg-cyan-400',
  },
  violet: {
    active: 'border-violet-500/60 bg-violet-500/10 shadow-[0_0_20px_rgba(139,92,246,0.12)]',
    badge: 'border-violet-500/50 bg-violet-500/10 text-violet-300',
    dot: 'bg-violet-400',
  },
  amber: {
    active: 'border-amber-500/60 bg-amber-500/10 shadow-[0_0_20px_rgba(245,158,11,0.12)]',
    badge: 'border-amber-500/50 bg-amber-500/10 text-amber-300',
    dot: 'bg-amber-400',
  },
  rose: {
    active: 'border-rose-500/60 bg-rose-500/10 shadow-[0_0_20px_rgba(239,68,68,0.12)]',
    badge: 'border-rose-500/50 bg-rose-500/10 text-rose-300',
    dot: 'bg-rose-400',
  },
};

export default function OnboardingPage({ selectedPath, onSelectPath, onNavigate, savingPath, isRequired }) {
  const canContinue = Boolean(selectedPath);

  return (
    <div className="min-h-screen bg-[#050d1a] flex items-start justify-center px-4 py-10">
      <div className="w-full max-w-3xl space-y-6">

        {/* Header */}
        <div className="relative overflow-hidden rounded-2xl border border-[#1a3a5c] bg-gradient-to-br from-[#0a1628] to-[#071020] p-7 text-center shadow-[0_0_40px_rgba(6,182,212,0.07)]">
          <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />
          <p className="text-[10px] uppercase tracking-[0.3em] text-cyan-400/70">Step 1 of 1</p>
          <h1 className="mt-2 text-3xl font-black text-slate-100">Choose Your Path</h1>
          <p className="mt-3 text-sm text-slate-400 max-w-md mx-auto">
            Your path determines which quests get assigned to you every day.
            Pick the one that matches your current goal.
          </p>
          {isRequired && (
            <div className="mt-4 inline-block rounded-full border border-amber-500/30 bg-amber-500/10 px-4 py-1.5 text-xs text-amber-300">
              ⚡ Required before you can access the app
            </div>
          )}
        </div>

        {/* Path cards */}
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {PATH_OPTIONS.map((option) => {
            const active = selectedPath === option.value;
            const colors = COLOR_MAP[option.color];
            return (
              <button
                key={option.value}
                type="button"
                onClick={() => onSelectPath(option.value)}
                disabled={savingPath}
                className={`rounded-xl border p-5 text-left transition-all duration-200 ${
                  active
                    ? colors.active
                    : 'border-[#1a3a5c] bg-[#0a1628] hover:border-[#2a4a6c] hover:bg-[#0d1f38]'
                } disabled:cursor-not-allowed disabled:opacity-70`}
              >
                <p className="text-2xl">{option.icon}</p>
                <p className="mt-2 text-base font-bold text-slate-100">{option.label}</p>
                <p className="mt-1.5 text-xs text-slate-500 leading-relaxed">{option.desc}</p>

                {/* Sample quests preview */}
                <ul className="mt-3 space-y-1">
                  {option.quests.map((q) => (
                    <li key={q} className="flex items-center gap-1.5 text-[10px] text-slate-600">
                      <span className={`h-1 w-1 flex-shrink-0 rounded-full ${active ? colors.dot : 'bg-slate-700'}`} />
                      {q}
                    </li>
                  ))}
                </ul>

                {active && (
                  <span className={`mt-3 inline-block rounded-full border px-2.5 py-0.5 text-[10px] font-semibold ${colors.badge}`}>
                    ✓ Selected
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* Continue button */}
        <div className="flex items-center justify-between">
          {!isRequired && (
            <button
              type="button"
              onClick={() => onNavigate('/dashboard')}
              className="text-sm text-slate-500 hover:text-slate-300 transition"
            >
              ← Back to dashboard
            </button>
          )}
          <button
            type="button"
            onClick={() => onNavigate('/dashboard')}
            disabled={!canContinue || savingPath}
            className={`ml-auto rounded-xl border px-8 py-3 text-sm font-bold transition ${
              canContinue
                ? 'border-cyan-500/60 bg-cyan-500/15 text-cyan-200 hover:bg-cyan-500/25'
                : 'cursor-not-allowed border-[#1a3a5c] text-slate-600'
            }`}
          >
            {savingPath ? 'Saving...' : canContinue ? 'Enter the System →' : 'Select a path to continue'}
          </button>
        </div>
      </div>
    </div>
  );
}
