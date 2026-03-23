import PostCard from '../components/PostCard';
import PostComposer from '../components/PostComposer';

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
}) {
  return (
    <section className="space-y-4">
      <div className="rounded-2xl border border-cyan-500/30 bg-gradient-to-r from-slate-900 via-slate-900 to-slate-800 p-6 shadow-[0_0_30px_rgba(14,165,233,0.12)]">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">Community</p>
            <h1 className="mt-2 text-2xl font-bold text-slate-100">Social Feed</h1>
            <p className="mt-1 text-sm text-slate-400">Recent public and friends-only updates you can view.</p>
          </div>
          <button
            type="button"
            onClick={onRefresh}
            className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 hover:border-cyan-500/50 hover:text-cyan-200"
          >
            Refresh
          </button>
        </div>
      </div>

      <PostComposer onCreatePost={onCreatePost} />

      {loading ? (
        <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
          <p className="text-sm text-slate-300">Loading social feed...</p>
        </div>
      ) : null}

      {!loading && error ? (
        <div className="rounded-xl border border-rose-500/50 bg-rose-500/10 p-4 text-rose-200">
          <p className="font-semibold">Could not load feed</p>
          <p className="mt-1 text-sm">{error}</p>
          <button
            type="button"
            onClick={onRefresh}
            className="mt-3 rounded-lg border border-rose-400/50 px-3 py-2 text-sm"
          >
            Retry
          </button>
        </div>
      ) : null}

      {!loading && !error && posts.length === 0 ? (
        <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
          <p className="text-sm text-slate-400">No posts yet. The social feed is currently empty.</p>
        </div>
      ) : null}

      {!loading && !error && posts.length > 0 ? (
        <div className="space-y-3">
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
            />
          ))}
        </div>
      ) : null}
    </section>
  );
}
