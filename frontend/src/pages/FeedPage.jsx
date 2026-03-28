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
  onViewProfile,
  onUpdatePost,
  onDeletePost,
}) {
  return (
    <div className="mx-auto max-w-2xl space-y-5">
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
          <button
            type="button"
            onClick={onRefresh}
            className="mt-3 rounded-lg border border-rose-400/40 px-3 py-1.5 text-sm"
          >
            Retry
          </button>
        </div>
      ) : null}

      {!loading && !error && posts.length === 0 ? (
        <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-8 text-center">
          <p className="text-sm text-slate-500">No posts yet. Be the first to share an update.</p>
        </div>
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
  );
}
