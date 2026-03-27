import QuestCard from '../components/QuestCard';

function calcExpProgress(exp) {
  const total = Math.max(exp || 0, 0);
  const inLevel = total % 100;
  return { inLevel, percent: Math.min(100, Math.round((inLevel / 100) * 100)) };
}

/* ── Arc gauge SVG ── */
function polarToXY(cx, cy, r, cwDeg) {
  const rad = ((cwDeg - 90) * Math.PI) / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

function ArcGauge({ value, max, sublabel }) {
  const cx = 70, cy = 72, r = 52;
  const startDeg = 240, totalDeg = 240;
  const pct = Math.min(1, Math.max(0, max > 0 ? value / max : 0));
  const start = polarToXY(cx, cy, r, startDeg);
  const bgEnd = polarToXY(cx, cy, r, startDeg + totalDeg);
  const fgEnd = polarToXY(cx, cy, r, startDeg + totalDeg * pct);
  const bgLarge = totalDeg > 180 ? 1 : 0;
  const fgLarge = totalDeg * pct > 180 ? 1 : 0;

  return (
    <svg viewBox="0 0 140 130" className="w-32 mx-auto">
      <defs>
        <linearGradient id="arc-grad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#06b6d4" />
          <stop offset="100%" stopColor="#f59e0b" />
        </linearGradient>
      </defs>
      <path
        d={`M ${start.x.toFixed(2)} ${start.y.toFixed(2)} A ${r} ${r} 0 ${bgLarge} 1 ${bgEnd.x.toFixed(2)} ${bgEnd.y.toFixed(2)}`}
        fill="none" stroke="#1e3a5f" strokeWidth="10" strokeLinecap="round"
      />
      {pct > 0.01 && (
        <path
          d={`M ${start.x.toFixed(2)} ${start.y.toFixed(2)} A ${r} ${r} 0 ${fgLarge} 1 ${fgEnd.x.toFixed(2)} ${fgEnd.y.toFixed(2)}`}
          fill="none" stroke="url(#arc-grad)" strokeWidth="10" strokeLinecap="round"
        />
      )}
      <text x={cx} y={cy - 6} textAnchor="middle" fill="#fbbf24" fontSize="20" fontWeight="bold">{value}</text>
      <text x={cx} y={cx + 12} textAnchor="middle" fill="#94a3b8" fontSize="10">/ {max}</text>
      <text x={cx} y={cx + 24} textAnchor="middle" fill="#475569" fontSize="9">{sublabel}</text>
    </svg>
  );
}

/* ── Right progress panel ── */
function ProgressPanel({ player, quests }) {
  const completedCount = quests.filter((q) => q.completed_today || q.assigned_completed_today).length;
  const weeklyExp = player ? (player.exp % 700) : 0;

  return (
    <aside className="flex flex-col gap-4">
      <h2 className="text-xs uppercase tracking-[0.2em] text-slate-500">Progress</h2>

      {/* Achievements (placeholder) */}
      <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-semibold text-slate-200">Achievements</p>
            <p className="mt-0.5 text-xs text-slate-500">0 Unlocked</p>
          </div>
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-500/10 text-amber-400">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
            </svg>
          </div>
        </div>
      </div>

      {/* Weekly EXP arc */}
      <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4 text-center">
        <p className="mb-2 text-xs uppercase tracking-[0.15em] text-slate-500">Weekly EXP</p>
        <ArcGauge value={weeklyExp} max={700} sublabel="Weekly EXP" />
      </div>

      {/* Streak + Quests row */}
      <div className="grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
          <p className="text-[10px] uppercase tracking-wide text-slate-500">Daily Streak</p>
          <p className="mt-1 flex items-center gap-1 text-xl font-bold text-orange-400">
            <span>🔥</span> {player?.streak ?? 0}
          </p>
        </div>
        <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
          <p className="text-[10px] uppercase tracking-wide text-slate-500">Done Today</p>
          <p className="mt-1 flex items-center gap-1 text-xl font-bold text-emerald-400">
            <span>✅</span> {completedCount}
          </p>
        </div>
      </div>

      {/* Leaderboard (placeholder) */}
      <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
        <h3 className="mb-3 text-sm font-semibold text-slate-200">Leaderboard</h3>
        <ol className="space-y-2">
          {[
            { rank: 1, name: player?.username || 'You', level: player?.level ?? 1, exp: `+${player?.exp ?? 0}` },
            { rank: 2, name: '—', level: '—', exp: '—' },
            { rank: 3, name: '—', level: '—', exp: '—' },
          ].map((entry) => (
            <li key={entry.rank} className="flex items-center gap-3">
              <span className={`w-5 text-center text-sm font-bold ${entry.rank === 1 ? 'text-amber-400' : 'text-slate-600'}`}>
                {entry.rank}
              </span>
              <div className="flex h-7 w-7 items-center justify-center rounded-full border border-[#1a3a5c] bg-slate-800 text-xs text-slate-400">
                {entry.name !== '—' ? entry.name.charAt(0).toUpperCase() : '?'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="truncate text-xs font-medium text-slate-300">{entry.name}</p>
                {entry.level !== '—' && <p className="text-[10px] text-slate-500">Level {entry.level}</p>}
              </div>
              <span className="text-xs font-semibold text-amber-400">{entry.exp !== '—' ? `${entry.exp} EXP` : '—'}</span>
            </li>
          ))}
        </ol>
      </div>
    </aside>
  );
}

/* ── Main dashboard ── */
export default function DashboardPage({
  player,
  quests,
  loading,
  error,
  onRefresh,
  onCompleteQuest,
  completingQuestId,
  selectedPathDisplay,
  onNavigate,
}) {
  const expProgress = calcExpProgress(player?.exp || 0);

  if (loading) {
    return (
      <div className="flex h-48 items-center justify-center">
        <p className="text-sm text-slate-500">Loading status window...</p>
      </div>
    );
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[1fr_280px]">
      {/* ── Center column ── */}
      <div className="space-y-5">
        {error ? (
          <div className="rounded-xl border border-rose-500/40 bg-rose-500/10 p-4 text-rose-200">
            <p className="font-semibold">Action failed</p>
            <p className="mt-1 text-sm">{error}</p>
            <button
              type="button"
              onClick={onRefresh}
              className="mt-3 rounded-lg border border-rose-400/40 px-3 py-2 text-sm"
            >
              Retry
            </button>
          </div>
        ) : null}

        {/* Character panel */}
        <div className="relative overflow-hidden rounded-2xl border border-[#1a3a5c] bg-gradient-to-br from-[#0a1628] via-[#0d1f38] to-[#071020] p-6 shadow-[0_0_40px_rgba(6,182,212,0.08)]">
          {/* Subtle top glow line */}
          <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />

          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-[10px] uppercase tracking-[0.25em] text-cyan-400/70">Player Status</p>
              <h1 className="mt-1 text-3xl font-bold text-slate-100">{player?.username || 'Unknown Hunter'}</h1>
              <div className="mt-2 flex flex-wrap items-center gap-3">
                <span className="rounded-full border border-cyan-500/40 bg-cyan-500/10 px-3 py-1 text-xs font-semibold text-cyan-300">
                  Level {player?.level ?? 1}
                </span>
                <span className="flex items-center gap-1 text-xs text-orange-400">
                  🔥 Streak: <strong>{player?.streak ?? 0} days</strong>
                </span>
              </div>
            </div>

            <button
              type="button"
              onClick={() => onNavigate('/onboarding')}
              className="rounded-lg border border-[#1a3a5c] bg-[#070f1e] px-3 py-2 text-xs text-slate-400 transition hover:border-cyan-500/40 hover:text-cyan-300"
            >
              Path: {selectedPathDisplay || 'Choose'}
            </button>
          </div>

          {/* EXP bar */}
          <div className="mt-5">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-400">EXP to next level</span>
              <span className="font-medium text-amber-300">{expProgress.inLevel} / 100</span>
            </div>
            <div className="mt-2 h-2.5 overflow-hidden rounded-full bg-[#1a3a5c]/60">
              <div
                className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-amber-400 transition-all duration-500"
                style={{ width: `${expProgress.percent}%` }}
              />
            </div>
          </div>

          {/* Stat chips row */}
          <div className="mt-4 grid grid-cols-3 gap-3">
            {[
              { label: 'Level', value: player?.level ?? 1, color: 'text-cyan-300' },
              { label: 'Total EXP', value: player?.exp ?? 0, color: 'text-amber-300' },
              { label: 'Streak', value: `${player?.streak ?? 0}d`, color: 'text-emerald-300' },
            ].map(({ label, value, color }) => (
              <div key={label} className="rounded-lg border border-[#1a3a5c]/80 bg-[#060d1a]/80 px-3 py-3 text-center">
                <p className="text-[10px] uppercase tracking-wide text-slate-500">{label}</p>
                <p className={`mt-1 text-xl font-bold ${color}`}>{value}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Quest list */}
        <div className="rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-slate-100">Today&apos;s Quests</h2>
              <p className="text-xs text-slate-500">Complete your assigned set to protect your streak.</p>
            </div>
            <button
              type="button"
              onClick={onRefresh}
              className="rounded-lg border border-[#1a3a5c] px-3 py-1.5 text-xs text-slate-400 transition hover:border-cyan-500/40 hover:text-cyan-300"
            >
              Refresh
            </button>
          </div>

          {quests.length === 0 ? (
            <p className="py-4 text-center text-sm text-slate-500">No quests assigned yet for today.</p>
          ) : (
            <div className="divide-y divide-[#1a3a5c]/40">
              {quests.map((quest) => (
                <QuestCard
                  key={quest.id}
                  quest={quest}
                  onComplete={onCompleteQuest}
                  loading={completingQuestId === quest.id}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ── Right panel ── */}
      <ProgressPanel player={player} quests={quests} />
    </div>
  );
}
