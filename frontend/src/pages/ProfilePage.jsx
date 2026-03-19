export default function ProfilePage({ player, selectedPath }) {
  return (
    <section className="max-w-2xl">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/75 p-6">
        <h1 className="text-2xl font-bold text-slate-100">Player Profile</h1>
        <p className="mt-2 text-sm text-slate-400">Minimal profile view for Phase 4.</p>

        <div className="mt-6 grid gap-5 sm:grid-cols-[120px,1fr]">
          <div className="flex h-28 w-28 items-center justify-center rounded-xl border border-slate-700 bg-slate-950 text-sm text-slate-400">
            Avatar
          </div>
          <div className="space-y-3 text-sm">
            <p><span className="text-slate-400">Username:</span> <span className="text-slate-100">{player?.username ?? 'Unknown'}</span></p>
            <p><span className="text-slate-400">Player ID:</span> <span className="text-slate-100">#{player?.id ?? '-'}</span></p>
            <p><span className="text-slate-400">Level:</span> <span className="text-slate-100">{player?.level ?? 1}</span></p>
            <p><span className="text-slate-400">EXP:</span> <span className="text-amber-300">{player?.exp ?? 0}</span></p>
            <p><span className="text-slate-400">Streak:</span> <span className="text-emerald-300">{player?.streak ?? 0}</span></p>
            <p><span className="text-slate-400">Path:</span> <span className="text-cyan-300">{selectedPath || 'Not selected'}</span></p>
          </div>
        </div>
      </div>
    </section>
  );
}
