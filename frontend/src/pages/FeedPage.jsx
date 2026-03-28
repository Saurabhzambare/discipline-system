import PostCard from '../components/PostCard';
import PostComposer from '../components/PostComposer';

/* ── Feature E: Rich empty state ── */
function FeedEmptyState({ onNavigate, onFocusComposer }) {
  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-8 text-center">
      <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full border border-[#1a3a5c] bg-[#060d1a] text-3xl">
        ⚔️
      </div>
      <h3 className="text-base font-semibold text-slate-200">Your feed is quiet</h3>
      <p className="mt-2 text-sm text-slate-500">
        Complete a quest and share it, or write your first update to get started.
      </p>
      <div className="mt-5 flex flex-col items-center gap-2 sm:flex-row sm:justify-center">
        <button
          type="button"
          onClick={onFocusComposer}
          className="rounded-lg border border-cyan-500/50 bg-cyan-500/15 px-4 py-2 text-sm font-medium text-cyan-200 hover:bg-cyan-500/25"
        >
          Write a post
        </button>
        <button
          type="button"
          onClick={() => onNavigate('/dashboard')}
          className="rounded-lg border border-[#1a3a5c] px-4 py-2 text-sm text-slate-400 hover:text-slate-200"
        >
          View quests
        </button>
      </div>
    </div>
  );
}

/* ── Feature A: Right panel ── */
function FeedRightPanel({ player, friends, onNavigate }) {
  const expInLevel = player ? player.exp % 100 : 0;
  const expPct = Math.min(100, Math.round((expInLevel / 100) * 100));

  return (
    <aside className="space-y-4">
      {/* Player mini stats */}
      {player && (
        <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
          <div className="flex items-center gap-3 mb-3">
            <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full border border-cyan-500/40 bg-cyan-500/10 text-sm font-bold text-cyan-300">
              {player.username.charAt(0).toUpperCase()}
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-200">{player.username}</p>
              <p className="text-[10px] text-slate-500">Level {player.level}</p>
            </div>
          </div>
          <div className="space-y-1.5">
            <div className="flex items-center justify-between text-[10px] text-slate-500">
              <span>EXP Progress</span>
              <span className="text-amber-400 font-medium">{expInLevel} / 100</span>
            </div>
            <div className="h-1.5 overflow-hidden rounded-full bg-[#1a3a5c]/60">
              <div
                className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-amber-400 transition-all"
                style={{ width: `${expPct}%` }}
              />
            </div>
          </div>
          <div className="mt-3 grid grid-cols-2 gap-2">
            <div className="rounded-lg border border-[#1a3a5c]/60 bg-[#060d1a] p-2 text-center">
              <p className="text-[10px] text-slate-600">Streak</p>
              <p className="text-sm font-bold text-orange-400">🔥 {player.streak}d</p>
            </div>
            <div className="rounded-lg border border-[#1a3a5c]/60 bg-[#060d1a] p-2 text-center">
              <p className="text-[10px] text-slate-600">Total EXP</p>
              <p className="text-sm font-bold text-amber-400">{player.exp}</p>
            </div>
          </div>
        </div>
      )}

      {/* Friends online / list */}
      <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
        <div className="flex items-center justify-between mb-3">
          <p className="text-xs font-semibold text-slate-300">Friends</p>
          <button
            type="button"
            onClick={() => onNavigate('/profile')}
            className="text-[10px] text-slate-500 hover:text-cyan-400"
          >
            Manage →
          </button>
        </div>
        {friends.length === 0 ? (
          <div className="py-3 text-center">
            <p className="text-xs text-slate-600">No friends yet.</p>
            <button
              type="button"
              onClick={() => onNavigate('/profile')}
              className="mt-1 text-[10px] text-cyan-500 hover:text-cyan-400"
            >
              Find hunters to add
            </button>
          </div>
        ) : (
          <ul className="space-y-1.5">
            {friends.slice(0, 8).map((f) => (
              <li key={f.id} className="flex items-center gap-2">
                <div className="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full border border-[#1a3a5c] bg-[#060d1a] text-[9px] font-bold text-cyan-400">
                  {f.username.charAt(0).toUpperCase()}
                </div>
                <span className="text-xs text-slate-400">{f.username}</span>
              </li>
            ))}
            {friends.length > 8 && (
              <p className="text-[10px] text-slate-600 pt-1">+{friends.length - 8} more</p>
            )}
          </ul>
        )}
      </div>

      {/* Mini leaderboard (placeholder — real data = player + friends) */}
      <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
        <p className="mb-3 text-xs font-semibold text-slate-300">Top Hunters</p>
        <ol className="space-y-2">
          {[
            player ? { rank: 1, name: player.username, exp: player.exp } : null,
            ...friends.slice(0, 2).map((f, i) => ({ rank: i + 2, name: f.username, exp: '—' })),
          ]
            .filter(Boolean)
            .map((entry) => (
              <li key={entry.rank} className="flex items-center gap-2.5">
                <span className={`w-4 text-center text-xs font-bold ${entry.rank === 1 ? 'text-amber-400' : 'text-slate-600'}`}>
                  {entry.rank}
                </span>
                <div className="flex h-6 w-6 items-center justify-center rounded-full border border-[#1a3a5c] bg-[#060d1a] text-[9px] text-slate-400">
                  {entry.name.charAt(0).toUpperCase()}
                </div>
                <span className="flex-1 truncate text-xs text-slate-300">{entry.name}</span>
                <span className="text-[10px] font-semibold text-amber-400">{entry.exp !== '—' ? `${entry.exp} EXP` : '—'}</span>
              </li>
            ))}
        </ol>
      </div>
    </aside>
  );
}

export default function FeedPage({
  posts,
  loading,
  error,
  onRefresh,
  onCreatePost,
  currentPlayerId,
  onRefreshPost,
  onAddComment,
  onUpdateComment,
  onDeleteComment,
  onSetReaction,
  onRemoveReaction,
  onViewProfile,
  onUpdatePost,
  onDeletePost,
  player,
  friends,
  onNavigate,
}) {
  return (
    <div className="grid gap-6 xl:grid-cols-[1fr_260px]">
      {/* ── Left: main feed ── */}
      <div className="min-w-0 space-y-5">
        {/* Header */}
        <div className="relative overflow-hidden rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5">
          <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-[10px] uppercase tracking-[0.25em] text-cyan-400/70">Community</p>
              <h1 className="mt-1 text-xl font-bold text-slate-100">Social Feed</h1>
            </div>
            <button
              type="button"
              onClick={onRefresh}
              className="rounded-lg border border-[#1a3a5c] px-3 py-1.5 text-xs text-slate-400 transition hover:border-cyan-500/40 hover:text-cyan-300"
            >
              Refresh
            </button>
          </div>
        </div>

        <PostComposer onCreatePost={onCreatePost} />

        {loading ? (
          <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-5">
            <p className="text-sm text-slate-500">Loading feed...</p>
          </div>
        ) : null}

        {!loading && error ? (
          <div className="rounded-xl border border-rose-500/40 bg-rose-500/10 p-4 text-rose-300">
            <p className="font-semibold">Could not load feed</p>
            <p className="mt-1 text-sm">{error}</p>
            <button type="button" onClick={onRefresh} className="mt-3 rounded-lg border border-rose-400/40 px-3 py-1.5 text-sm">
              Retry
            </button>
          </div>
        ) : null}

        {/* Feature E: rich empty state */}
        {!loading && !error && posts.length === 0 ? (
          <FeedEmptyState onNavigate={onNavigate} onFocusComposer={() => document.querySelector('textarea')?.focus()} />
        ) : null}

        {!loading && !error && posts.length > 0 ? (
          <div className="space-y-4">
            {posts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                currentPlayerId={currentPlayerId}
                onRefreshPost={onRefreshPost}
                onAddComment={onAddComment}
                onUpdateComment={onUpdateComment}
                onDeleteComment={onDeleteComment}
                onSetReaction={onSetReaction}
                onRemoveReaction={onRemoveReaction}
                onViewProfile={onViewProfile}
                onUpdatePost={onUpdatePost}
                onDeletePost={onDeletePost}
              />
            ))}
          </div>
        ) : null}
      </div>

      {/* ── Right: Feature A panel ── */}
      <FeedRightPanel player={player} friends={friends || []} onNavigate={onNavigate} />
    </div>
  );
}
