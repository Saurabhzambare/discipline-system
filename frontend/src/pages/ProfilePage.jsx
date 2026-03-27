export default function ProfilePage({ player, selectedPathDisplay, onNavigate }) {
  return (
    <div className="max-w-2xl space-y-5">
      {/* Header card */}
      <div className="relative overflow-hidden rounded-2xl border border-[#1a3a5c] bg-gradient-to-br from-[#0a1628] to-[#071020] p-6 shadow-[0_0_40px_rgba(6,182,212,0.06)]">
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />

        <div className="flex items-start gap-5">
          {/* Avatar */}
          <div className="flex h-20 w-20 flex-shrink-0 items-center justify-center rounded-xl border border-[#1a3a5c] bg-[#060d1a] text-2xl font-bold text-cyan-400">
            {player?.username ? player.username.charAt(0).toUpperCase() : '?'}
          </div>

          <div className="flex-1 min-w-0">
            <p className="text-[10px] uppercase tracking-[0.25em] text-cyan-400/70">Player Profile</p>
            <h1 className="mt-1 text-2xl font-bold text-slate-100">{player?.username ?? 'Unknown Hunter'}</h1>
            <p className="mt-1 text-xs text-slate-500">Hunter ID #{player?.id ?? '—'}</p>

            <div className="mt-3 flex flex-wrap gap-2">
              <span className="rounded-full border border-cyan-500/40 bg-cyan-500/10 px-3 py-1 text-xs font-semibold text-cyan-300">
                Level {player?.level ?? 1}
              </span>
              <span className="rounded-full border border-[#1a3a5c] bg-[#060d1a] px-3 py-1 text-xs text-slate-400">
                {selectedPathDisplay || 'No path'}
              </span>
            </div>
          </div>

          <button
            type="button"
            onClick={() => onNavigate('/onboarding')}
            className="flex-shrink-0 rounded-lg border border-[#1a3a5c] px-3 py-2 text-xs text-slate-400 transition hover:border-cyan-500/40 hover:text-cyan-300"
          >
            Change Path
          </button>
        </div>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: 'Level', value: player?.level ?? 1, color: 'text-cyan-300', border: 'border-cyan-500/20' },
          { label: 'Total EXP', value: player?.exp ?? 0, color: 'text-amber-300', border: 'border-amber-500/20' },
          { label: 'Day Streak', value: `${player?.streak ?? 0}🔥`, color: 'text-orange-400', border: 'border-orange-500/20' },
        ].map(({ label, value, color, border }) => (
          <div key={label} className={`rounded-xl border ${border} bg-[#0a1628] p-4 text-center`}>
            <p className="text-[10px] uppercase tracking-wide text-slate-500">{label}</p>
            <p className={`mt-2 text-2xl font-bold ${color}`}>{value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
