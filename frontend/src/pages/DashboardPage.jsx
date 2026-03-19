import ProgressCard from '../components/ProgressCard';
import QuestCard from '../components/QuestCard';

function calculateExpProgress(exp) {
  const currentLevel = Math.floor(Math.sqrt(Math.max(exp, 0) / 100)) + 1;
  const previousThreshold = Math.pow(currentLevel - 1, 2) * 100;
  const nextThreshold = Math.pow(currentLevel, 2) * 100;
  const inLevelExp = exp - previousThreshold;
  const levelRange = Math.max(nextThreshold - previousThreshold, 1);
  return {
    currentLevel,
    inLevelExp,
    levelRange,
    percent: Math.min(100, Math.max(0, Math.round((inLevelExp / levelRange) * 100))),
  };
}

export default function DashboardPage({ player, quests, loading, error, onRefresh, onCompleteQuest, completingQuestId, selectedPath, onNavigate }) {
  if (loading) {
    return <p className="text-slate-300">Loading status window...</p>;
  }

  if (error) {
    return (
      <div className="rounded-xl border border-rose-500/50 bg-rose-500/10 p-4 text-rose-200">
        <p className="font-semibold">Failed to load dashboard</p>
        <p className="mt-1 text-sm">{error}</p>
        <button
          type="button"
          onClick={onRefresh}
          className="mt-3 rounded-lg border border-rose-400/50 px-3 py-2 text-sm"
        >
          Retry
        </button>
      </div>
    );
  }

  const expProgress = calculateExpProgress(player?.exp || 0);

  return (
    <section className="space-y-6">
      <div className="rounded-2xl border border-cyan-500/30 bg-gradient-to-r from-slate-900 via-slate-900 to-slate-800 p-6 shadow-[0_0_30px_rgba(14,165,233,0.12)]">
        <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">Player Status Window</p>
        <div className="mt-3 flex flex-wrap items-end justify-between gap-3">
          <h1 className="text-3xl font-bold text-slate-100">{player?.username || 'Unknown Hunter'}</h1>
          <button
            type="button"
            onClick={() => onNavigate('/onboarding')}
            className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 hover:border-cyan-500/50 hover:text-cyan-200"
          >
            Path: {selectedPath || 'Choose'}
          </button>
        </div>

        <div className="mt-6 grid gap-3 sm:grid-cols-3">
          <ProgressCard label="Level" value={player?.level ?? 1} tone="blue" />
          <ProgressCard label="Total EXP" value={player?.exp ?? 0} tone="gold" />
          <ProgressCard label="Current Streak" value={player?.streak ?? 0} tone="green" />
        </div>

        <div className="mt-5 rounded-xl border border-slate-700 bg-slate-950/60 p-4">
          <div className="flex items-center justify-between text-sm">
            <p className="font-medium text-slate-300">EXP Progress</p>
            <p className="text-amber-300">
              {expProgress.inLevelExp} / {expProgress.levelRange}
            </p>
          </div>
          <div className="mt-2 h-3 rounded-full bg-slate-800">
            <div
              className="h-3 rounded-full bg-gradient-to-r from-cyan-500 to-amber-400"
              style={{ width: `${expProgress.percent}%` }}
            />
          </div>
        </div>
      </div>

      <div className="space-y-3 rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
        <div className="flex items-center justify-between gap-3">
          <h2 className="text-xl font-semibold text-slate-100">Active Quests</h2>
          <button
            type="button"
            onClick={onRefresh}
            className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 hover:border-cyan-500/50 hover:text-cyan-200"
          >
            Refresh
          </button>
        </div>

        {quests.length === 0 ? (
          <p className="text-sm text-slate-400">No active quests available yet.</p>
        ) : (
          <div className="space-y-3">
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
    </section>
  );
}
