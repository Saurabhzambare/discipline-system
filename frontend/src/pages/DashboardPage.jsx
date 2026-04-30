import { useCallback, useEffect, useMemo, useState } from 'react';
import QuestCard from '../components/QuestCard';
import { getWeeklyLeaderboard } from '../api';

function calcExpProgress(player) {
  const inLevel = Math.max(player?.exp_in_level || 0, 0);
  const forLevel = Math.max(player?.exp_for_level || 100, 1);
  return {
    inLevel,
    forLevel,
    toNext: Math.max(player?.exp_to_next_level || 0, 0),
    percent: Math.min(100, Math.round((inLevel / forLevel) * 100)),
  };
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

function MiniCompletionRing({ completed = 0, total = 0 }) {
  const safeTotal = Math.max(1, total || 1);
  const pct = Math.min(100, Math.round((completed / safeTotal) * 100));
  const radius = 28;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (pct / 100) * circumference;
  return (
    <svg viewBox="0 0 80 80" className="h-20 w-20">
      <circle cx="40" cy="40" r={radius} stroke="#1a3a5c" strokeWidth="8" fill="none" />
      <circle
        cx="40"
        cy="40"
        r={radius}
        stroke={pct >= 100 ? '#f59e0b' : pct >= 67 ? '#3b82f6' : pct >= 34 ? '#f59e0b' : '#ef4444'}
        strokeWidth="8"
        fill="none"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform="rotate(-90 40 40)"
      />
      <text x="40" y="36" textAnchor="middle" fill="#e2e8f0" fontSize="11" fontWeight="bold">
        {completed}/{total}
      </text>
      <text x="40" y="50" textAnchor="middle" fill="#94a3b8" fontSize="8">
        {pct}%
      </text>
    </svg>
  );
}

/* ── Level-up overlay ── */
function LevelUpOverlay({ newLevel, onDismiss }) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      style={{ background: 'radial-gradient(ellipse at center, rgba(251,191,36,0.18) 0%, rgba(5,13,26,0.92) 70%)' }}
      onClick={onDismiss}
    >
      <div className="relative flex flex-col items-center gap-4 px-8 py-10 text-center" onClick={(e) => e.stopPropagation()}>
        {/* Ping rings */}
        <span className="pointer-events-none absolute inset-0 m-auto h-48 w-48 animate-ping rounded-full border border-amber-400/20" />
        <span
          className="pointer-events-none absolute inset-0 m-auto h-64 w-64 animate-ping rounded-full border border-amber-400/10 delay-300"
          style={{ animationDelay: '0.3s' }}
        />

        <div className="relative flex h-24 w-24 items-center justify-center rounded-full border-2 border-amber-400/60 bg-amber-500/10 shadow-[0_0_40px_rgba(251,191,36,0.4)]">
          <span className="text-4xl">⬆</span>
        </div>

        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-400/70">Rank Achieved</p>
          <h2 className="mt-1 text-5xl font-black text-amber-300">Level {newLevel}</h2>
          <p className="mt-2 text-sm text-slate-400">You have grown stronger, Hunter.</p>
        </div>

        <button
          type="button"
          onClick={onDismiss}
          className="mt-2 rounded-xl border border-amber-500/40 bg-amber-500/15 px-8 py-3 text-sm font-semibold text-amber-200 transition hover:bg-amber-500/25"
        >
          Continue
        </button>
      </div>
    </div>
  );
}

/* ── Streak warning banner ── */
function StreakWarning({ quests }) {
  const total = quests.length;
  if (total === 0) return null;

  const remaining = quests.filter((q) => !(q.completed_today || q.assigned_completed_today)).length;
  const allDone = remaining === 0;

  return (
    <div
      className={`flex items-center gap-3 rounded-xl border px-4 py-3 text-sm transition-all ${
        allDone
          ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300'
          : 'border-orange-500/30 bg-orange-500/10 text-orange-300'
      }`}
    >
      <span className="text-base">{allDone ? '✅' : '⚡'}</span>
      {allDone ? (
        <span>All quests complete! Your streak is safe.</span>
      ) : (
        <span>
          <strong>{remaining}</strong> quest{remaining !== 1 ? 's' : ''} remaining — complete them to protect your streak!
        </span>
      )}
    </div>
  );
}

/* ── Quest filter pills ── */
const FILTERS = [
  { key: 'all', label: 'All' },
  { key: 'remaining', label: 'Remaining' },
  { key: 'fitness', label: 'Fitness' },
  { key: 'discipline', label: 'Discipline' },
  { key: 'health', label: 'Health' },
  { key: 'mindset', label: 'Mindset' },
];

/* ── Right progress panel ── */
function ProgressPanel({ player, quests, doneTodayCount }) {
  const completedCount = doneTodayCount ?? quests.filter((q) => q.completed_today || q.assigned_completed_today).length;
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

      {/* Weekly leaderboard */}
      <WeeklyLeaderboardCard player={player} />
    </aside>
  );
}

/* ── Weekly leaderboard card ── */
function WeeklyLeaderboardCard({ player }) {
  const path = player?.path || '';
  const [state, setState] = useState({ data: null, loading: !!path, error: '' });

  useEffect(() => {
    if (!path) return undefined;
    let cancelled = false;
    getWeeklyLeaderboard(path)
      .then((result) => {
        if (!cancelled) setState({ data: result, loading: false, error: '' });
      })
      .catch((err) => {
        if (!cancelled) setState({ data: null, loading: false, error: err.message || 'Failed to load leaderboard.' });
      });
    return () => {
      cancelled = true;
    };
  }, [path]);

  const { data, loading, error } = state;

  const top = (data?.leaderboard || []).slice(0, 5);
  const userRank = data?.user_rank ?? null;
  const showOwnRank = userRank && userRank > 5;

  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
      <h3 className="mb-3 text-sm font-semibold text-slate-200">Weekly Leaderboard</h3>
      {loading && <p className="text-xs text-slate-500">Loading…</p>}
      {!loading && error && (
        <p className="text-xs text-rose-400">{error}</p>
      )}
      {!loading && !error && top.length === 0 && (
        <p className="text-xs text-slate-500">No data yet.</p>
      )}
      {!loading && !error && top.length > 0 && (
        <ol className="space-y-2">
          {top.map((entry) => {
            const isMe = player?.id === entry.player_id;
            return (
              <li key={entry.player_id} className="flex items-center gap-3">
                <span className={`w-5 text-center text-sm font-bold ${entry.rank === 1 ? 'text-amber-400' : 'text-slate-600'}`}>
                  {entry.rank}
                </span>
                <div className="flex h-7 w-7 items-center justify-center rounded-full border border-[#1a3a5c] bg-slate-800 text-xs text-slate-400">
                  {entry.username ? entry.username.charAt(0).toUpperCase() : '?'}
                </div>
                <div className="flex-1 min-w-0">
                  <p className={`truncate text-xs font-medium ${isMe ? 'text-amber-300' : 'text-slate-300'}`}>
                    {entry.username}{isMe ? ' (You)' : ''}
                  </p>
                </div>
                <span className="text-xs font-semibold text-amber-400">{entry.exp} EXP</span>
              </li>
            );
          })}
        </ol>
      )}
      {showOwnRank && (
        <p className="mt-3 border-t border-[#1a3a5c] pt-2 text-xs text-slate-400">
          You: <span className="font-semibold text-amber-300">#{userRank}</span>
        </p>
      )}
    </div>
  );
}

/* ── Main dashboard ── */
export default function DashboardPage({
  player,
  quests,
  dailyLineup,
  loading,
  error,
  onRefresh,
  onCompleteQuest,
  completingQuestId,
  selectedPathDisplay,
  onNavigate,
  levelUpInfo,
  onDismissLevelUp,
  onShareQuest,
  onSetIntention,
  onGetSwapAlternatives,
  onSwapQuest,
  onSubmitFeedback,
  onLoadSummary,
  onLoadCompletionRing,
  onLoadTomorrowPreview,
  onLoadAdaptiveNudge,
  onSetAdaptiveNudgeDecision,
  onLoadWarRoomEntries,
  onSubmitWarRoomEntry,
  onLoadKnightWeeklyReport,
  onGetWisdomLogs,
  onUpsertWisdomLog,
  onRedeemFreedomDay,
  onActivateDarkNight,
  onGetBodyJournalEntries,
  onGetHealthMechanicsStatus,
  onUpsertBodyJournalEntry,
  onGetVisionBoardSummary,
  onGetOutputLogs,
  onGetGrindMechanicsStatus,
  onUpsertOutputLog,
  onGetDisciplineMechanicsStatus,
  onGetTemptationLogs,
  onCreateTemptationLog,
  onGetAccountabilityRequests,
  onSearchPlayers,
  onSendAccountabilityRequest,
  onAcceptAccountabilityRequest,
  onRejectAccountabilityRequest,
}) {
  const INTENTION_COPY = {
    full_send: 'No difficulty reduction — keeps your current lineup as-is.',
    steady: 'May soften one unfinished assigned quest to an easier option.',
    recovery: 'Attempts to shift unfinished assigned quests to lighter D-rank options.',
  };
  const expProgress = calcExpProgress(player);
  const [activeFilter, setActiveFilter] = useState('all');
  const [summary, setSummary] = useState(null);
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [summaryOpen, setSummaryOpen] = useState(false);
  const [completionRing, setCompletionRing] = useState(null);
  const [tomorrowPreview, setTomorrowPreview] = useState(null);
  const [adaptiveNudge, setAdaptiveNudge] = useState(null);
  const [missedReturn, setMissedReturn] = useState(null);
  const [swapState, setSwapState] = useState({ open: false, alternatives: [], quest: null, loading: false });
  const [intentionSaving, setIntentionSaving] = useState(false);
  const [intentionNotice, setIntentionNotice] = useState('');
  const [swapNotice, setSwapNotice] = useState('');
  const [feedbackByItem, setFeedbackByItem] = useState(() =>
    Object.fromEntries((quests || []).filter((q) => q.item_id).map((q) => [q.item_id, q.feedback || null])),
  );
  const [feedbackSavingByItem, setFeedbackSavingByItem] = useState({});
  const [warRoomEntries, setWarRoomEntries] = useState([]);
  const [warRoomPhase, setWarRoomPhase] = useState('morning');
  const [warRoomObjectives, setWarRoomObjectives] = useState('');
  const [warRoomReflection, setWarRoomReflection] = useState('');
  const [warRoomLoading, setWarRoomLoading] = useState(false);
  const [warRoomNotice, setWarRoomNotice] = useState('');
  const [warRoomHydrated, setWarRoomHydrated] = useState(false);
  const [weeklyReport, setWeeklyReport] = useState(null);
  const [weeklyLoading, setWeeklyLoading] = useState(false);
  const [mechanicsLoading, setMechanicsLoading] = useState(false);
  const [mechanicsNotice, setMechanicsNotice] = useState('');
  const [wisdomLogs, setWisdomLogs] = useState([]);
  const [wisdomText, setWisdomText] = useState('');
  const [bodyJournalEntries, setBodyJournalEntries] = useState([]);
  const [bodyJournalPayload, setBodyJournalPayload] = useState({ energy_level: 5, sleep_hours: 7, weight_kg: '', notes: '' });
  const [visionBoardSummary, setVisionBoardSummary] = useState(null);
  const [outputLogs, setOutputLogs] = useState([]);
  const [outputPayload, setOutputPayload] = useState({ deep_work_hours: 1, tasks_shipped: 1, notes: '' });
  const [healthStatus, setHealthStatus] = useState(null);
  const [disciplineStatus, setDisciplineStatus] = useState(null);
  const [grindStatus, setGrindStatus] = useState(null);
  const [temptationLogs, setTemptationLogs] = useState([]);
  const [temptationDescription, setTemptationDescription] = useState('');
  const [accountabilityIncoming, setAccountabilityIncoming] = useState([]);
  const [accountabilityOutgoing, setAccountabilityOutgoing] = useState([]);
  const [accountabilitySearch, setAccountabilitySearch] = useState('');
  const [accountabilityResults, setAccountabilityResults] = useState([]);
  const [accountabilitySearching, setAccountabilitySearching] = useState(false);
  const [isLevelUpOpen, setIsLevelUpOpen] = useState(false);
  const doneTodayCount = quests.filter((q) => q.completed_today || q.assigned_completed_today).length;
  const levelUpEventKey = useMemo(
    () => (levelUpInfo ? `${levelUpInfo.newLevel}-${levelUpInfo.achievedAt || 'default'}` : null),
    [levelUpInfo],
  );

  const dismissLevelUp = useCallback(() => {
    setIsLevelUpOpen(false);
    if (onDismissLevelUp) onDismissLevelUp();
  }, [onDismissLevelUp]);

  async function refreshWarRoomEntries() {
    if (!onLoadWarRoomEntries) return;
    const entries = await onLoadWarRoomEntries();
    setWarRoomEntries(entries || []);
  }

  const loadMechanics = useCallback(async () => {
    setMechanicsLoading(true);
    try {
      const [
        nextWisdom,
        nextBodyJournal,
        nextVisionBoard,
        nextOutputLogs,
        nextHealthStatus,
        nextDisciplineStatus,
        nextGrindStatus,
        nextTemptationLogs,
        incoming,
        outgoing,
      ] = await Promise.all([
        onGetWisdomLogs ? onGetWisdomLogs() : Promise.resolve([]),
        onGetBodyJournalEntries ? onGetBodyJournalEntries() : Promise.resolve([]),
        onGetVisionBoardSummary ? onGetVisionBoardSummary() : Promise.resolve(null),
        onGetOutputLogs ? onGetOutputLogs() : Promise.resolve([]),
        onGetHealthMechanicsStatus ? onGetHealthMechanicsStatus() : Promise.resolve(null),
        onGetDisciplineMechanicsStatus ? onGetDisciplineMechanicsStatus() : Promise.resolve(null),
        onGetGrindMechanicsStatus ? onGetGrindMechanicsStatus() : Promise.resolve(null),
        onGetTemptationLogs ? onGetTemptationLogs() : Promise.resolve([]),
        onGetAccountabilityRequests ? onGetAccountabilityRequests('incoming') : Promise.resolve([]),
        onGetAccountabilityRequests ? onGetAccountabilityRequests('outgoing') : Promise.resolve([]),
      ]);
      setWisdomLogs(nextWisdom || []);
      setBodyJournalEntries(nextBodyJournal || []);
      setVisionBoardSummary(nextVisionBoard || null);
      setOutputLogs(nextOutputLogs || []);
      setHealthStatus(nextHealthStatus || null);
      setDisciplineStatus(nextDisciplineStatus || null);
      setGrindStatus(nextGrindStatus || null);
      setTemptationLogs(nextTemptationLogs || []);
      setAccountabilityIncoming(incoming || []);
      setAccountabilityOutgoing(outgoing || []);
    } finally {
      setMechanicsLoading(false);
    }
  }, [
    onGetAccountabilityRequests,
    onGetBodyJournalEntries,
    onGetHealthMechanicsStatus,
    onGetDisciplineMechanicsStatus,
    onGetGrindMechanicsStatus,
    onGetTemptationLogs,
    onGetOutputLogs,
    onGetVisionBoardSummary,
    onGetWisdomLogs,
  ]);

  useEffect(() => {
    setFeedbackByItem(
      Object.fromEntries((quests || []).filter((q) => q.item_id).map((q) => [q.item_id, q.feedback || null])),
    );
  }, [quests]);

  useEffect(() => {
    refreshWarRoomEntries();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [onLoadWarRoomEntries]);

  useEffect(() => {
    loadMechanics();
  }, [loadMechanics]);

  useEffect(() => {
    if (!dailyLineup?.date) return;
    if (onLoadCompletionRing) {
      onLoadCompletionRing(dailyLineup.date).then((data) => setCompletionRing(data)).catch(() => {});
    }
    if (onLoadTomorrowPreview) {
      onLoadTomorrowPreview(dailyLineup.date).then((data) => setTomorrowPreview(data)).catch(() => {});
    }
    if (onLoadAdaptiveNudge) {
      onLoadAdaptiveNudge(dailyLineup.date).then((data) => setAdaptiveNudge(data)).catch(() => {});
    }
    setMissedReturn(dailyLineup?.missed_day_return || null);
  }, [dailyLineup?.date, onLoadCompletionRing, onLoadTomorrowPreview, onLoadAdaptiveNudge, dailyLineup?.missed_day_return]);

  useEffect(() => {
    if (!dailyLineup?.missed_day_return?.show) return;
    setMissedReturn(dailyLineup.missed_day_return);
    const t = setTimeout(() => setMissedReturn(null), 3000);
    return () => clearTimeout(t);
  }, [dailyLineup?.missed_day_return]);

  useEffect(() => {
    if (levelUpInfo) {
      setIsLevelUpOpen(true);
    }
  }, [levelUpEventKey, levelUpInfo]);

  useEffect(() => {
    if (!warRoomEntries.length) return;
    const latest = warRoomEntries[0];
    const defaultPhase = latest.evening_exp_awarded > 0 || latest.reflection ? 'evening' : 'morning';
    setWarRoomPhase(defaultPhase);
    if (!warRoomHydrated) {
      if (Array.isArray(latest.objectives) && latest.objectives.length > 0) {
        setWarRoomObjectives(latest.objectives.join('\n'));
      }
      if (latest.reflection) {
        setWarRoomReflection(latest.reflection);
      }
      setWarRoomHydrated(true);
    }
  }, [warRoomEntries, warRoomHydrated]);

  const filteredQuests = quests.filter((q) => {
    if (activeFilter === 'remaining') return !(q.completed_today || q.assigned_completed_today);
    if (activeFilter === 'all') return true;
    return (q.category_display || q.category || '').toLowerCase() === activeFilter;
  });

  if (loading) {
    return (
      <div className="flex h-48 items-center justify-center">
        <p className="text-sm text-slate-500">Loading status window...</p>
      </div>
    );
  }

  return (
    <>
      {/* Level-up overlay (Features 1) */}
      {levelUpInfo && isLevelUpOpen && (
        <LevelUpOverlay newLevel={levelUpInfo.newLevel} onDismiss={dismissLevelUp} />
      )}

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

          {/* Streak warning banner (Feature 3) */}
          {quests.length > 0 && <StreakWarning quests={quests} />}

          {dailyLineup?.date ? (
            <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
              <p className="text-[11px] uppercase tracking-[0.2em] text-slate-500">Daily Intention</p>
              <p className="mt-1 text-xs text-slate-400">
                Pick your pace for today. This tunes your lineup vibe: <span className="text-cyan-300">Full Send</span> (push hard),{' '}
                <span className="text-cyan-300">Steady</span> (balanced), or <span className="text-cyan-300">Recovery</span> (lighter day).
              </p>
              <p className="mt-2 text-[11px] text-slate-500">
                Effect now: {INTENTION_COPY[dailyLineup?.intention] || INTENTION_COPY.steady}
              </p>
              <div className="mt-3 flex flex-wrap gap-2">
                {[
                  { value: 'full_send', label: 'Full Send' },
                  { value: 'steady', label: 'Steady' },
                  { value: 'recovery', label: 'Recovery' },
                ].map((option) => {
                  const active = dailyLineup?.intention === option.value;
                  return (
                    <button
                      key={option.value}
                      type="button"
                      onClick={async () => {
                        if (!onSetIntention || intentionSaving || active) return;
                        setIntentionSaving(true);
                        setIntentionNotice('Saving intention...');
                        try {
                          const result = await onSetIntention(option.value);
                          const lineupAdjusted = Boolean(result?.lineup_adjusted);
                          setIntentionNotice(
                            lineupAdjusted
                              ? `Saved: ${option.label} selected. Today's lineup was adjusted immediately.`
                              : `Saved: ${option.label} selected. No immediate lineup change was needed.`,
                          );
                        } finally {
                          setIntentionSaving(false);
                        }
                      }}
                      disabled={intentionSaving}
                      className={`rounded-lg border px-3 py-1.5 text-xs font-medium transition ${
                        active
                          ? 'border-cyan-500/60 bg-cyan-500/15 text-cyan-200'
                          : 'border-[#1a3a5c] text-slate-400 hover:border-cyan-500/40 hover:text-cyan-300'
                      } disabled:cursor-wait disabled:opacity-70`}
                    >
                      {option.label}
                      {active ? ' ✓' : ''}
                    </button>
                  );
                })}
                <button
                  type="button"
                  onClick={async () => {
                    if (!dailyLineup?.date || !onLoadSummary) return;
                    setSummaryLoading(true);
                    try {
                      const payload = await onLoadSummary(dailyLineup.date);
                      setSummary(payload);
                    } finally {
                      setSummaryLoading(false);
                    }
                  }}
                  className="ml-auto rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-3 py-1.5 text-xs text-emerald-200 hover:bg-emerald-500/20"
                >
                  {summaryLoading ? 'Loading…' : 'View Daily Summary'}
                </button>
              </div>
              {intentionNotice ? (
                <p className="mt-2 text-xs text-cyan-300">{intentionNotice}</p>
              ) : null}
              {summary ? (
                <div className="mt-3 rounded-lg border border-[#1a3a5c] bg-[#071020] p-3 text-xs text-slate-300">
                  <p>Completed: {summary.quests_completed}/{summary.quests_total}</p>
                  <p>Total EXP: {summary.total_exp_earned} (bonus {summary.bonus_exp_earned})</p>
                  <p>Streak: {summary.streak_status}</p>
                </div>
              ) : null}
            </div>
          ) : null}

          {/* Character panel */}
          <div className="relative overflow-hidden rounded-2xl border border-[#1a3a5c] bg-gradient-to-br from-[#0a1628] via-[#0d1f38] to-[#071020] p-6 shadow-[0_0_40px_rgba(6,182,212,0.08)]">
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
                  <span className="rounded-full border border-violet-500/30 bg-violet-500/10 px-3 py-1 text-xs font-medium text-violet-200">
                    Pillar Identity: {player?.path_display || 'Unassigned'}
                  </span>
                </div>
              </div>

              <button
                type="button"
                onClick={() => onNavigate('/path-onboarding')}
                className="rounded-lg border border-[#1a3a5c] bg-[#070f1e] px-3 py-2 text-xs text-slate-400 transition hover:border-cyan-500/40 hover:text-cyan-300"
              >
                Path: {selectedPathDisplay || 'Choose'}
              </button>
            </div>

            {/* EXP bar */}
            <div className="mt-5">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400">EXP to next level</span>
                <span className="font-medium text-amber-300">{expProgress.inLevel} / {expProgress.forLevel} ({expProgress.toNext} left)</span>
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

          <div className="rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5">
            <div className="flex items-center justify-between gap-2">
              <h2 className="text-lg font-semibold text-slate-100">War Room</h2>
              <button
                type="button"
                onClick={async () => {
                  if (!onLoadKnightWeeklyReport) return;
                  setWeeklyLoading(true);
                  try {
                    const report = await onLoadKnightWeeklyReport();
                    setWeeklyReport(report);
                  } finally {
                    setWeeklyLoading(false);
                  }
                }}
                className="rounded-lg border border-indigo-500/40 bg-indigo-500/10 px-3 py-1.5 text-xs text-indigo-200 hover:bg-indigo-500/20"
              >
                {weeklyLoading ? 'Loading report…' : 'Load Weekly Report'}
              </button>
            </div>
            <p className="mt-1 text-xs text-slate-500">Minimal Discipline Knight flow: morning plan, evening reflection, and EXP feedback.</p>
            {warRoomEntries[0] ? (
              <p className="mt-1 text-[11px] text-slate-400">
                Saved today: morning {warRoomEntries[0].morning_exp_awarded > 0 ? '✅' : '—'} · evening {warRoomEntries[0].evening_exp_awarded > 0 ? '✅' : '—'} · same-day bonus {warRoomEntries[0].bonus_exp_awarded > 0 ? `+${warRoomEntries[0].bonus_exp_awarded}` : '0'}
              </p>
            ) : null}
            <div className="mt-3 flex gap-2">
              {['morning', 'evening'].map((phase) => (
                <button
                  key={phase}
                  type="button"
                  onClick={() => setWarRoomPhase(phase)}
                  className={`rounded-lg border px-3 py-1.5 text-xs ${
                    warRoomPhase === phase
                      ? 'border-cyan-500/60 bg-cyan-500/15 text-cyan-200'
                      : 'border-[#1a3a5c] text-slate-400'
                  }`}
                >
                  {phase === 'morning' ? 'Morning Entry' : 'Evening Entry'}
                </button>
              ))}
            </div>
            {warRoomPhase === 'morning' ? (
              <textarea
                value={warRoomObjectives}
                onChange={(e) => setWarRoomObjectives(e.target.value)}
                rows={3}
                placeholder="Top objectives (one per line)"
                className="mt-3 w-full rounded-lg border border-[#1a3a5c] bg-[#071020] p-2 text-xs text-slate-100"
              />
            ) : (
              <textarea
                value={warRoomReflection}
                onChange={(e) => setWarRoomReflection(e.target.value)}
                rows={3}
                placeholder="Evening reflection"
                className="mt-3 w-full rounded-lg border border-[#1a3a5c] bg-[#071020] p-2 text-xs text-slate-100"
              />
            )}
            <button
              type="button"
              disabled={warRoomLoading || !onSubmitWarRoomEntry}
              onClick={async () => {
                if (!onSubmitWarRoomEntry) return;
                setWarRoomLoading(true);
                setWarRoomNotice('');
                try {
                  const payload = warRoomPhase === 'morning'
                    ? { phase: 'morning', objectives: warRoomObjectives.split('\n').map((v) => v.trim()).filter(Boolean) }
                    : { phase: 'evening', reflection: warRoomReflection };
                  const result = await onSubmitWarRoomEntry(payload);
                  setWarRoomNotice(`Saved. +${result.exp_awarded_now || 0} EXP${result.bonus_awarded_now ? ` (+${result.bonus_awarded_now} same-day bonus)` : ''}.`);
                  await refreshWarRoomEntries();
                  onRefresh?.();
                } finally {
                  setWarRoomLoading(false);
                }
              }}
              className="mt-3 rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-3 py-1.5 text-xs text-emerald-200"
            >
              {warRoomLoading ? 'Submitting…' : 'Submit War Room Entry'}
            </button>
            {warRoomNotice ? <p className="mt-2 text-xs text-emerald-300">{warRoomNotice}</p> : null}
            {warRoomEntries[0] ? (
              <p className="mt-2 text-xs text-slate-400">
                Latest entry week: {warRoomEntries[0].week_start} • morning +{warRoomEntries[0].morning_exp_awarded} • evening +{warRoomEntries[0].evening_exp_awarded} • bonus +{warRoomEntries[0].bonus_exp_awarded}
              </p>
            ) : null}
            {weeklyReport?.report_payload ? (
              <div className="mt-3 rounded-lg border border-[#1a3a5c] bg-[#071020] p-3 text-xs text-slate-300">
                <p>Week: {weeklyReport.week_start} → {weeklyReport.week_end}</p>
                <p>War Room mornings: {weeklyReport.report_payload?.war_room?.morning_plans_completed ?? 0}</p>
                <p>War Room evenings: {weeklyReport.report_payload?.war_room?.evening_reviews_completed ?? 0}</p>
                <p>Same-day bonuses: {weeklyReport.report_payload?.war_room?.same_day_bonuses ?? 0}</p>
              </div>
            ) : null}
          </div>

          <div className="rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5">
            <h2 className="text-lg font-semibold text-slate-100">Session 6 Mechanics Access</h2>
            <p className="mt-1 text-xs text-slate-500">Minimal usable access for path mechanics already implemented on backend.</p>
            {mechanicsNotice ? <p className="mt-2 text-xs text-cyan-300">{mechanicsNotice}</p> : null}
            <div className="mt-4 grid gap-3 lg:grid-cols-2">
              <div className="rounded-lg border border-[#1a3a5c] bg-[#071020] p-3">
                <p className="text-xs font-semibold text-slate-200">Mindset Sage</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  <button
                    type="button"
                    onClick={async () => {
                      if (!onRedeemFreedomDay) return;
                      const result = await onRedeemFreedomDay({});
                      setMechanicsNotice(`Freedom Day redeemed for ${result.used_on}.`);
                    }}
                    className="rounded-md border border-cyan-500/40 bg-cyan-500/10 px-2 py-1 text-[11px] text-cyan-200"
                  >
                    Redeem Freedom Day
                  </button>
                  <button
                    type="button"
                    onClick={async () => {
                      if (!onActivateDarkNight) return;
                      const result = await onActivateDarkNight({ entry: 'Activated from dashboard.' });
                      setMechanicsNotice(`Dark Night activated. +${result.exp_awarded || 0} EXP.`);
                    }}
                    className="rounded-md border border-indigo-500/40 bg-indigo-500/10 px-2 py-1 text-[11px] text-indigo-200"
                  >
                    Activate Dark Night
                  </button>
                </div>
                <div className="mt-3">
                  <textarea
                    value={wisdomText}
                    onChange={(e) => setWisdomText(e.target.value)}
                    rows={2}
                    placeholder="Wisdom Log entry"
                    className="w-full rounded-md border border-[#1a3a5c] bg-[#0a1628] p-2 text-xs text-slate-100"
                  />
                  <button
                    type="button"
                    onClick={async () => {
                      if (!wisdomText.trim() || !onUpsertWisdomLog) return;
                      await onUpsertWisdomLog({ entry: wisdomText.trim() });
                      setWisdomText('');
                      await loadMechanics();
                      setMechanicsNotice('Wisdom Log saved.');
                    }}
                    className="mt-2 rounded-md border border-emerald-500/40 bg-emerald-500/10 px-2 py-1 text-[11px] text-emerald-200"
                  >
                    Save Wisdom Log
                  </button>
                  <p className="mt-2 text-[11px] text-slate-400">Entries: {wisdomLogs.length}</p>
                </div>
              </div>

              <div className="rounded-lg border border-[#1a3a5c] bg-[#071020] p-3">
                <p className="text-xs font-semibold text-slate-200">Health Alchemist</p>
                <div className="mt-2 grid grid-cols-3 gap-2 text-[11px]">
                  {['energy_level', 'sleep_hours', 'weight_kg'].map((key) => (
                    <label key={key} className="text-slate-400">
                      {key}
                      <input
                        type="number"
                        step="0.1"
                        min={key === 'energy_level' ? 1 : 0}
                        max={key === 'energy_level' ? 10 : undefined}
                        value={bodyJournalPayload[key]}
                        onChange={(e) => setBodyJournalPayload((prev) => ({ ...prev, [key]: e.target.value === '' ? '' : Number(e.target.value) }))}
                        className="mt-1 w-full rounded border border-[#1a3a5c] bg-[#0a1628] px-1.5 py-1 text-slate-100"
                      />
                    </label>
                  ))}
                </div>
                <textarea
                  value={bodyJournalPayload.notes}
                  onChange={(e) => setBodyJournalPayload((prev) => ({ ...prev, notes: e.target.value }))}
                  rows={2}
                  placeholder="Body Journal notes"
                  className="mt-2 w-full rounded-md border border-[#1a3a5c] bg-[#0a1628] p-2 text-xs text-slate-100"
                />
                <button
                  type="button"
                  onClick={async () => {
                    if (!onUpsertBodyJournalEntry) return;
                    await onUpsertBodyJournalEntry({
                      energy_level: bodyJournalPayload.energy_level === '' ? null : bodyJournalPayload.energy_level,
                      sleep_hours: bodyJournalPayload.sleep_hours === '' ? null : bodyJournalPayload.sleep_hours,
                      weight_kg: bodyJournalPayload.weight_kg === '' ? null : bodyJournalPayload.weight_kg,
                      notes: bodyJournalPayload.notes,
                    });
                    setBodyJournalPayload({ energy_level: 5, sleep_hours: 7, weight_kg: '', notes: '' });
                    await loadMechanics();
                    setMechanicsNotice('Body Journal saved.');
                  }}
                  className="mt-2 rounded-md border border-emerald-500/40 bg-emerald-500/10 px-2 py-1 text-[11px] text-emerald-200"
                >
                  Save Body Journal
                </button>
                <p className="mt-2 text-[11px] text-slate-400">Entries: {bodyJournalEntries.length}</p>
                <p className="mt-1 text-[11px] text-slate-500">
                  Elixir brews: {healthStatus?.elixir?.brews_completed ?? 0} · fill days: {healthStatus?.elixir?.fill_days ?? 0}
                </p>
                <p className="mt-1 text-[11px] text-slate-500">
                  Milestones unlocked: {healthStatus?.transmutation_milestones?.length ?? 0}
                </p>
              </div>

              <div className="rounded-lg border border-[#1a3a5c] bg-[#071020] p-3">
                <p className="text-xs font-semibold text-slate-200">Grind Visionary</p>
                <p className="mt-2 text-[11px] text-slate-400">
                  Vision Board: {visionBoardSummary?.goal?.title || 'No goal set'} {visionBoardSummary?.goal?.countdown_days != null ? `(${visionBoardSummary.goal.countdown_days} days left)` : ''}
                </p>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    min={0}
                    step="0.1"
                    value={outputPayload.deep_work_hours}
                    onChange={(e) => setOutputPayload((prev) => ({ ...prev, deep_work_hours: Number(e.target.value) || 0 }))}
                    placeholder="Deep work hrs"
                    className="rounded-md border border-[#1a3a5c] bg-[#0a1628] p-2 text-xs text-slate-100"
                  />
                  <input
                    type="number"
                    min={0}
                    value={outputPayload.tasks_shipped}
                    onChange={(e) => setOutputPayload((prev) => ({ ...prev, tasks_shipped: Number(e.target.value) || 0 }))}
                    placeholder="Tasks shipped"
                    className="rounded-md border border-[#1a3a5c] bg-[#0a1628] p-2 text-xs text-slate-100"
                  />
                </div>
                <textarea
                  value={outputPayload.notes}
                  onChange={(e) => setOutputPayload((prev) => ({ ...prev, notes: e.target.value }))}
                  rows={2}
                  placeholder="Output notes"
                  className="mt-2 w-full rounded-md border border-[#1a3a5c] bg-[#0a1628] p-2 text-xs text-slate-100"
                />
                <button
                  type="button"
                  onClick={async () => {
                    if (!onUpsertOutputLog) return;
                    await onUpsertOutputLog(outputPayload);
                    setOutputPayload({ deep_work_hours: 1, tasks_shipped: 1, notes: '' });
                    await loadMechanics();
                    setMechanicsNotice('Output Log saved.');
                  }}
                  className="mt-2 rounded-md border border-emerald-500/40 bg-emerald-500/10 px-2 py-1 text-[11px] text-emerald-200"
                >
                  Save Output Log
                </button>
                <p className="mt-2 text-[11px] text-slate-400">Output logs: {outputLogs.length}</p>
                <p className="mt-1 text-[11px] text-slate-500">
                  XP Multiplier: {grindStatus?.xp_multiplier?.multiplier ?? 1}x · Protection: {grindStatus?.multiplier_protection?.available ?? 0}
                </p>
                <p className="mt-1 text-[11px] text-slate-500">
                  Skill Tree: {grindStatus?.skill_tree?.unlocked_nodes ?? 0}/{grindStatus?.skill_tree?.total_nodes ?? 0} unlocked · Chain stage: {grindStatus?.first_dollar_chain?.chain_stage ?? 0}
                </p>
              </div>

              <div className="rounded-lg border border-[#1a3a5c] bg-[#071020] p-3">
                <p className="text-xs font-semibold text-slate-200">Discipline Knight</p>
                <p className="mt-2 text-[11px] text-slate-400">
                  Armor pieces: {disciplineStatus?.armor?.pieces?.length ?? 0} · cracks: {disciplineStatus?.armor?.total_cracks ?? 0}
                </p>
                <p className="mt-1 text-[11px] text-slate-400">
                  Grace tokens: {disciplineStatus?.grace_tokens?.available ?? 0} · shields: {disciplineStatus?.streak_shield?.shields_available ?? 0}
                </p>
                <textarea
                  value={temptationDescription}
                  onChange={(e) => setTemptationDescription(e.target.value)}
                  rows={2}
                  placeholder="Log temptation resisted"
                  className="mt-2 w-full rounded-md border border-[#1a3a5c] bg-[#0a1628] p-2 text-xs text-slate-100"
                />
                <button
                  type="button"
                  onClick={async () => {
                    if (!temptationDescription.trim() || !onCreateTemptationLog) return;
                    await onCreateTemptationLog({ description: temptationDescription.trim(), resisted: true });
                    setTemptationDescription('');
                    await loadMechanics();
                    setMechanicsNotice('Temptation log saved.');
                  }}
                  className="mt-2 rounded-md border border-emerald-500/40 bg-emerald-500/10 px-2 py-1 text-[11px] text-emerald-200"
                >
                  Save Temptation Log
                </button>
                <p className="mt-1 text-[11px] text-slate-500">Temptation logs: {temptationLogs.length}</p>
              </div>

              <div className="rounded-lg border border-[#1a3a5c] bg-[#071020] p-3">
                <p className="text-xs font-semibold text-slate-200">Accountability Partner</p>
                {mechanicsLoading ? (
                  <p className="mt-2 text-[11px] text-slate-500">Loading accountability requests…</p>
                ) : (
                  <>
                    <div className="mt-2 flex gap-2">
                      <input
                        value={accountabilitySearch}
                        onChange={(e) => setAccountabilitySearch(e.target.value)}
                        placeholder="Search player username"
                        className="flex-1 rounded-md border border-[#1a3a5c] bg-[#0a1628] p-2 text-xs text-slate-100"
                      />
                      <button
                        type="button"
                        onClick={async () => {
                          if (!onSearchPlayers || accountabilitySearch.trim().length < 2) return;
                          setAccountabilitySearching(true);
                          try {
                            const results = await onSearchPlayers(accountabilitySearch.trim());
                            setAccountabilityResults(results || []);
                          } finally {
                            setAccountabilitySearching(false);
                          }
                        }}
                        className="rounded-md border border-cyan-500/40 bg-cyan-500/10 px-2 py-1 text-[11px] text-cyan-200"
                      >
                        {accountabilitySearching ? 'Searching…' : 'Search'}
                      </button>
                    </div>
                    {accountabilityResults.slice(0, 4).map((p) => (
                      <div key={p.id} className="mt-2 flex items-center justify-between rounded border border-[#1a3a5c] px-2 py-1 text-[11px] text-slate-300">
                        <span>{p.username}</span>
                        <button
                          type="button"
                          onClick={async () => {
                            if (!onSendAccountabilityRequest) return;
                            await onSendAccountabilityRequest(p.id);
                            await loadMechanics();
                            setMechanicsNotice(`Accountability request sent to ${p.username}.`);
                          }}
                          className="rounded border border-emerald-500/40 bg-emerald-500/10 px-2 py-0.5 text-emerald-200"
                        >
                          Invite
                        </button>
                      </div>
                    ))}
                    <p className="mt-2 text-[11px] text-slate-400">Incoming requests: {accountabilityIncoming.length}</p>
                    {accountabilityIncoming.slice(0, 3).map((r) => (
                      <div key={r.id} className="mt-1 flex items-center justify-between rounded border border-[#1a3a5c] px-2 py-1 text-[11px] text-slate-300">
                        <span>{r.from_player?.username || 'Unknown'}</span>
                        <div className="flex gap-1">
                          <button
                            type="button"
                            onClick={async () => {
                              await onAcceptAccountabilityRequest?.(r.id);
                              await loadMechanics();
                              setMechanicsNotice('Accountability request accepted.');
                            }}
                            className="rounded border border-emerald-500/40 bg-emerald-500/10 px-1.5 py-0.5 text-emerald-200"
                          >
                            Accept
                          </button>
                          <button
                            type="button"
                            onClick={async () => {
                              await onRejectAccountabilityRequest?.(r.id);
                              await loadMechanics();
                              setMechanicsNotice('Accountability request rejected.');
                            }}
                            className="rounded border border-rose-500/40 bg-rose-500/10 px-1.5 py-0.5 text-rose-200"
                          >
                            Reject
                          </button>
                        </div>
                      </div>
                    ))}
                    <p className="mt-1 text-[11px] text-slate-400">Outgoing requests: {accountabilityOutgoing.length}</p>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Quest list */}
          <div className="rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-slate-100">Today&apos;s Quests</h2>
                <p className="text-xs text-slate-500">Complete your assigned set to protect your streak.</p>
                <p className="mt-1 text-[11px] text-slate-400">
                  Need a better fit? Use <span className="text-cyan-300">Swap</span> on eligible quests.
                </p>
                <p className="mt-1 text-[11px] text-slate-500">
                  {dailyLineup?.features_unlocked?.swap
                    ? `Swap unlocked (Day ${dailyLineup?.days_on_path || 0}). Up to ${dailyLineup?.swaps_remaining ?? 0} swap(s) left today.`
                    : `Swap unlocks on Day 14 of your current path. You are on Day ${dailyLineup?.days_on_path || 0}.`}
                </p>
              </div>
              <button
                type="button"
                onClick={onRefresh}
                className="rounded-lg border border-[#1a3a5c] px-3 py-1.5 text-xs text-slate-400 transition hover:border-cyan-500/40 hover:text-cyan-300"
              >
                Refresh
              </button>
              <button
                type="button"
                onClick={async () => {
                  if (!onLoadSummary) return;
                  setSummaryLoading(true);
                  try {
                    const data = await onLoadSummary(dailyLineup?.date);
                    setSummary(data);
                    setSummaryOpen(true);
                  } finally {
                    setSummaryLoading(false);
                  }
                }}
                className="ml-2 rounded-lg border border-cyan-500/40 px-3 py-1.5 text-xs text-cyan-300 transition hover:bg-cyan-500/10"
              >
                {summaryLoading ? 'Loading Summary…' : 'View EOD Summary'}
              </button>
            </div>

            {/* Filter pills (Feature 8) */}
            <div className="mb-4 flex flex-wrap gap-2">
              {FILTERS.map((f) => (
                <button
                  key={f.key}
                  type="button"
                  onClick={() => setActiveFilter(f.key)}
                  className={`rounded-full px-3 py-1 text-xs font-medium transition border ${
                    activeFilter === f.key
                      ? 'border-cyan-500/50 bg-cyan-500/15 text-cyan-300'
                      : 'border-[#1a3a5c] text-slate-500 hover:border-[#2a4a6c] hover:text-slate-300'
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>

            {quests.length === 0 ? (
              <p className="py-4 text-center text-sm text-slate-500">No quests assigned yet for today.</p>
            ) : filteredQuests.length === 0 ? (
              <p className="py-4 text-center text-sm text-slate-500">No quests match this filter.</p>
            ) : (
              <div className="divide-y divide-[#1a3a5c]/40">
                {swapNotice ? (
                  <div className="mb-3 rounded-lg border border-cyan-500/30 bg-cyan-500/10 px-3 py-2 text-xs text-cyan-200">
                    {swapNotice}
                  </div>
                ) : null}
                {filteredQuests.map((quest) => (
                  <QuestCard
                    key={quest.id}
                    quest={quest}
                    onComplete={onCompleteQuest}
                    loading={completingQuestId === quest.id}
                    onShare={onShareQuest}
                    canSwap={Boolean(dailyLineup?.features_unlocked?.swap)}
                    swapMeta={{ daysOnPath: dailyLineup?.days_on_path || 0, unlockDay: 14 }}
                    onSwap={async (targetQuest) => {
                      if (!onGetSwapAlternatives || !targetQuest?.item_id) return;
                      setSwapState({ open: true, alternatives: [], quest: targetQuest, loading: true });
                      try {
                        const data = await onGetSwapAlternatives(targetQuest.item_id);
                        setSwapState({ open: true, alternatives: data.alternatives || [], quest: targetQuest, loading: false });
                      } catch {
                        setSwapState({ open: true, alternatives: [], quest: targetQuest, loading: false });
                      }
                    }}
                    onFeedback={async (itemId, feedback) => {
                      if (!itemId || !onSubmitFeedback) return;
                      setFeedbackSavingByItem((prev) => ({ ...prev, [itemId]: true }));
                      setFeedbackByItem((prev) => ({ ...prev, [itemId]: feedback }));
                      try {
                        await onSubmitFeedback(itemId, feedback);
                      } finally {
                        setFeedbackSavingByItem((prev) => ({ ...prev, [itemId]: false }));
                      }
                    }}
                    feedbackValue={feedbackByItem[quest.item_id] ?? quest.feedback ?? null}
                    feedbackSaving={Boolean(feedbackSavingByItem[quest.item_id])}
                  />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* ── Right panel ── */}
        <ProgressPanel player={player} quests={quests} doneTodayCount={doneTodayCount} />
      </div>
      <div className="mt-4 rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4 text-xs text-slate-300">
        <p className="font-semibold text-slate-100">Session 7 Contract Proving</p>
        <div className="mt-2 flex items-center gap-3">
          <MiniCompletionRing completed={completionRing?.completed ?? 0} total={completionRing?.total ?? 0} />
          <div>
            <p>Completion Ring (API-driven)</p>
            <p className="text-[11px] text-slate-500">No client-side quest math.</p>
          </div>
        </div>
        <p className="mt-1">
          Tomorrow categories: {(tomorrowPreview?.categories || []).join(', ') || '—'}
        </p>
        {adaptiveNudge?.show_nudge ? (
          <div className="mt-2 rounded border border-amber-500/40 bg-amber-500/10 p-2 text-amber-200">
            <p>{adaptiveNudge.message}</p>
            <div className="mt-2 flex gap-2">
              <button
                type="button"
                onClick={async () => {
                  await onSetAdaptiveNudgeDecision?.('accept');
                  const next = await onLoadAdaptiveNudge?.(dailyLineup?.date);
                  setAdaptiveNudge(next || null);
                }}
                className="rounded border border-emerald-500/40 bg-emerald-500/10 px-2 py-1 text-[11px]"
              >
                Yes upgrade my quests
              </button>
              <button
                type="button"
                onClick={async () => {
                  await onSetAdaptiveNudgeDecision?.('decline');
                  const next = await onLoadAdaptiveNudge?.(dailyLineup?.date);
                  setAdaptiveNudge(next || null);
                }}
                className="rounded border border-[#1a3a5c] px-2 py-1 text-[11px]"
              >
                Not yet keep current
              </button>
            </div>
          </div>
        ) : null}
      </div>
      {swapState.open ? (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/60 p-4">
          <div className="w-full max-w-md rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
            <h3 className="text-sm font-semibold text-slate-100">Swap Quest</h3>
            <p className="mt-1 text-xs text-slate-400">{swapState.quest?.title}</p>
            <div className="mt-3 space-y-2 max-h-72 overflow-auto">
              {swapState.loading ? (
                <p className="text-xs text-slate-500">Loading alternatives...</p>
              ) : swapState.alternatives.length === 0 ? (
                <p className="text-xs text-slate-500">No alternatives available.</p>
              ) : (
                swapState.alternatives.map((alt) => (
                  <button
                    key={alt.id}
                    type="button"
                    onClick={async () => {
                      await onSwapQuest?.(swapState.quest.item_id, alt.id);
                      setSwapState({ open: false, alternatives: [], quest: null, loading: false });
                      setSwapNotice('Quest swapped successfully.');
                    }}
                    className="w-full rounded-lg border border-[#1a3a5c] bg-[#071020] px-3 py-2 text-left text-xs text-slate-200 hover:border-cyan-500/40"
                  >
                    {alt.title} <span className="text-amber-300">+{alt.exp_reward} EXP</span>
                  </button>
                ))
              )}
            </div>
            <button
              type="button"
              onClick={() => setSwapState({ open: false, alternatives: [], quest: null, loading: false })}
              className="mt-3 rounded-lg border border-[#1a3a5c] px-3 py-1.5 text-xs text-slate-400"
            >
              Close
            </button>
          </div>
        </div>
      ) : null}
      {summaryOpen && summary ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="w-full max-w-lg rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4 text-xs text-slate-300">
            <p className="text-sm font-semibold text-slate-100">End of Day Summary</p>
            <p className="mt-2">Date: {summary.summary_date}</p>
            <p>Hunter: {summary.username}</p>
            <p>Completed: {summary.quests_completed}/{summary.quests_total}</p>
            <p>Total EXP: {summary.total_exp_earned}</p>
            <p className="mt-2 font-semibold text-slate-200">Tomorrow Preview (categories only)</p>
            <p>{(summary.tomorrow_preview?.categories || []).join(', ') || '—'}</p>
            <button
              type="button"
              onClick={() => setSummaryOpen(false)}
              className="mt-3 rounded border border-[#1a3a5c] px-3 py-1 text-xs text-slate-300"
            >
              Close
            </button>
          </div>
        </div>
      ) : null}
      {missedReturn?.show ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
          <div className="rounded-xl border border-cyan-500/40 bg-[#0a1628] p-6 text-center text-slate-100">
            <p className="text-lg font-semibold">Welcome Back</p>
            <p className="mt-2 text-sm text-slate-300">{missedReturn.message || 'Fresh start today.'}</p>
          </div>
        </div>
      ) : null}
    </>
  );
}
