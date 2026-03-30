import { useEffect, useMemo, useState } from 'react';

const REACTION_OPTIONS = [
  { value: 'like', emoji: '👍' },
  { value: 'fire', emoji: '🔥' },
  { value: 'respect', emoji: '💪' },
  { value: 'clap', emoji: '👏' },
];

const VISIBILITY_OPTIONS = [
  { value: 'public', label: 'Public' },
  { value: 'friends_only', label: 'Friends Only' },
];

function timeAgo(isoString) {
  if (!isoString) return '';
  const diff = Math.floor((Date.now() - new Date(isoString)) / 1000);
  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

export default function PostCard({
  post,
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
  const [newComment, setNewComment] = useState('');
  const [commentError, setCommentError] = useState('');
  const [submittingComment, setSubmittingComment] = useState(false);
  const [commentActionLoadingId, setCommentActionLoadingId] = useState(null);
  const [editingCommentId, setEditingCommentId] = useState(null);
  const [editingCommentContent, setEditingCommentContent] = useState('');
  const [reactionLoading, setReactionLoading] = useState(false);
  const [reactionError, setReactionError] = useState('');
  const [showComments, setShowComments] = useState(false);

  // Post-level edit state (Feature 10)
  const [editingPost, setEditingPost] = useState(false);
  const [editContent, setEditContent] = useState('');
  const [editVisibility, setEditVisibility] = useState('public');
  const [postActionBusy, setPostActionBusy] = useState(false);
  const [postError, setPostError] = useState('');

  const isMyPost = currentPlayerId && post.author?.id === currentPlayerId;

  useEffect(() => {
    setCommentError('');
    setReactionError('');
    if (editingCommentId) {
      const found = post.comments?.find((c) => c.id === editingCommentId);
      if (!found) { setEditingCommentId(null); setEditingCommentContent(''); }
    }
  }, [editingCommentId, post.comments]);

  const reactionSummary = useMemo(() => {
    const s = { like: 0, fire: 0, respect: 0, clap: 0 };
    (post.reactions || []).forEach((r) => { if (s[r.reaction_type] !== undefined) s[r.reaction_type] += 1; });
    return s;
  }, [post.reactions]);

  const myReaction = useMemo(
    () => (post.reactions || []).find((r) => r.player?.id === currentPlayerId) || null,
    [currentPlayerId, post.reactions],
  );

  const commentCount = post.comments?.length ?? 0;

  function startEditPost() {
    setEditContent(post.content);
    setEditVisibility(post.visibility || 'public');
    setEditingPost(true);
    setPostError('');
  }

  async function handleSavePost() {
    const text = editContent.trim();
    if (!text) return;
    setPostActionBusy(true);
    setPostError('');
    try {
      await onUpdatePost(post.id, { content: text, visibility: editVisibility });
      await onRefreshPost(post.id);
      setEditingPost(false);
    } catch (err) {
      setPostError(err.message || 'Could not update post.');
    } finally {
      setPostActionBusy(false);
    }
  }

  async function handleDeletePost() {
    if (!window.confirm('Delete this post?')) return;
    setPostActionBusy(true);
    try {
      await onDeletePost(post.id);
    } catch (err) {
      setPostError(err.message || 'Could not delete post.');
      setPostActionBusy(false);
    }
  }

  async function handleAddComment(event) {
    event.preventDefault();
    const text = newComment.trim();
    if (!text) { setCommentError('Please write a comment first.'); return; }
    setSubmittingComment(true);
    setCommentError('');
    try {
      await onAddComment(post.id, text);
      setNewComment('');
      await onRefreshPost(post.id);
    } catch (err) {
      setCommentError(err.message || 'Could not add comment.');
    } finally {
      setSubmittingComment(false);
    }
  }

  async function handleSaveComment(commentId) {
    const text = editingCommentContent.trim();
    if (!text) { setCommentError('Comment cannot be empty.'); return; }
    setCommentActionLoadingId(commentId);
    setCommentError('');
    try {
      await onUpdateComment(post.id, commentId, text);
      setEditingCommentId(null);
      setEditingCommentContent('');
      await onRefreshPost(post.id);
    } catch (err) {
      setCommentError(err.message || 'Could not update comment.');
    } finally {
      setCommentActionLoadingId(null);
    }
  }

  async function handleDeleteComment(commentId) {
    setCommentActionLoadingId(commentId);
    setCommentError('');
    try {
      await onDeleteComment(post.id, commentId);
      if (editingCommentId === commentId) { setEditingCommentId(null); setEditingCommentContent(''); }
      await onRefreshPost(post.id);
    } catch (err) {
      setCommentError(err.message || 'Could not delete comment.');
    } finally {
      setCommentActionLoadingId(null);
    }
  }

  async function handleReactionSelect(value) {
    setReactionLoading(true);
    setReactionError('');
    try {
      await onSetReaction(post.id, value);
      await onRefreshPost(post.id);
    } catch (err) {
      setReactionError(err.message || 'Could not update reaction.');
    } finally {
      setReactionLoading(false);
    }
  }

  async function handleReactionRemove() {
    setReactionLoading(true);
    setReactionError('');
    try {
      await onRemoveReaction(post.id);
      await onRefreshPost(post.id);
    } catch (err) {
      setReactionError(err.message || 'Could not remove reaction.');
    } finally {
      setReactionLoading(false);
    }
  }

  const isQuestPost = post.post_type === 'quest_completion';

  return (
    <article className={`relative overflow-hidden rounded-xl border p-5 ${
      isQuestPost
        ? 'border-amber-500/30 bg-gradient-to-br from-[#0a1628] to-[#120a00] shadow-[0_0_20px_rgba(245,158,11,0.06)]'
        : 'border-[#1a3a5c] bg-[#0a1628]'
    }`}>
      {/* Quest post top glow line */}
      {isQuestPost && (
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-amber-500/40 to-transparent rounded-t-xl" />
      )}

      {/* Author row */}
      <div className="flex items-center gap-3">
        <div className={`flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full border text-xs font-bold ${
          isQuestPost
            ? 'border-amber-500/40 bg-amber-500/10 text-amber-300'
            : 'border-[#1a3a5c] bg-[#060d1a] text-cyan-400'
        }`}>
          {(post.author?.username || '?').charAt(0).toUpperCase()}
        </div>
        <div className="flex-1 min-w-0">
          {/* Clickable username (Feature 4) */}
          <button
            type="button"
            onClick={() => onViewProfile && onViewProfile(post.author?.username)}
            className={`text-sm font-semibold text-slate-200 ${onViewProfile ? 'hover:text-cyan-300 transition' : ''}`}
          >
            {post.author?.username || 'Unknown Hunter'}
          </button>
          <p className="text-[10px] text-slate-600">{timeAgo(post.created_at)}</p>
        </div>
        {isQuestPost && (
          <span className="rounded-full border border-amber-500/40 bg-amber-500/10 px-2 py-0.5 text-[10px] font-medium text-amber-400">
            ⚔️ Quest
          </span>
        )}
        <span className="rounded-full border border-[#1a3a5c] px-2 py-0.5 text-[10px] text-slate-500">
          {post.visibility === 'friends_only' ? '🔒 Friends' : '🌐 Public'}
        </span>
        {post.is_edited && (
          <span className="text-[10px] text-slate-600 italic">edited</span>
        )}

        {/* Post edit/delete buttons (Feature 10) */}
        {isMyPost && onUpdatePost && !editingPost && (
          <div className="flex gap-1 ml-1">
            <button
              type="button"
              onClick={startEditPost}
              disabled={postActionBusy}
              className="rounded px-2 py-1 text-[10px] text-slate-500 hover:text-cyan-300 transition"
            >
              Edit
            </button>
            {onDeletePost && (
              <button
                type="button"
                onClick={handleDeletePost}
                disabled={postActionBusy}
                className="rounded px-2 py-1 text-[10px] text-slate-500 hover:text-rose-400 transition"
              >
                {postActionBusy ? '...' : 'Delete'}
              </button>
            )}
          </div>
        )}
      </div>

      {/* Content or inline edit */}
      {editingPost ? (
        <div className="mt-3 space-y-2">
          <textarea
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            rows={3}
            disabled={postActionBusy}
            className="w-full rounded-lg border border-[#1a3a5c] bg-[#06101e] px-3 py-2 text-sm text-slate-100 outline-none focus:ring focus:ring-cyan-400/20 disabled:opacity-70"
          />
          <div className="flex items-center gap-2">
            <select
              value={editVisibility}
              onChange={(e) => setEditVisibility(e.target.value)}
              disabled={postActionBusy}
              className="rounded-lg border border-[#1a3a5c] bg-[#06101e] px-2 py-1.5 text-xs text-slate-300 outline-none"
            >
              {VISIBILITY_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
            <button type="button" onClick={handleSavePost} disabled={postActionBusy || !editContent.trim()}
              className="rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-3 py-1.5 text-xs text-cyan-200 disabled:opacity-60">
              {postActionBusy ? 'Saving...' : 'Save'}
            </button>
            <button type="button" onClick={() => setEditingPost(false)} disabled={postActionBusy}
              className="rounded-lg border border-[#1a3a5c] px-3 py-1.5 text-xs text-slate-400">
              Cancel
            </button>
          </div>
          {postError && <p className="text-xs text-rose-400">{postError}</p>}
        </div>
      ) : (
        <p className="mt-3 whitespace-pre-wrap text-sm leading-relaxed text-slate-300">{post.content}</p>
      )}

      {/* Reactions */}
      <div className="mt-4 flex flex-wrap items-center gap-2">
        {REACTION_OPTIONS.map((opt) => {
          const active = myReaction?.reaction_type === opt.value;
          const count = reactionSummary[opt.value] || 0;
          return (
            <button
              key={opt.value}
              type="button"
              onClick={() => active ? handleReactionRemove() : handleReactionSelect(opt.value)}
              disabled={reactionLoading}
              className={`flex items-center gap-1 rounded-lg border px-2.5 py-1 text-xs transition ${
                active
                  ? 'border-cyan-500/50 bg-cyan-500/15 text-cyan-200'
                  : 'border-[#1a3a5c] bg-[#060d1a] text-slate-400 hover:border-cyan-500/30 hover:text-slate-200'
              } disabled:cursor-not-allowed disabled:opacity-60`}
            >
              <span>{opt.emoji}</span>
              {count > 0 && <span>{count}</span>}
            </button>
          );
        })}

        {/* Comment toggle */}
        <button
          type="button"
          onClick={() => setShowComments((v) => !v)}
          className="ml-auto flex items-center gap-1.5 rounded-lg border border-[#1a3a5c] px-2.5 py-1 text-xs text-slate-500 transition hover:border-cyan-500/30 hover:text-slate-300"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          {commentCount > 0 ? commentCount : ''} {showComments ? 'Hide' : 'Comments'}
        </button>
      </div>

      {reactionError ? <p className="mt-2 text-xs text-rose-400">{reactionError}</p> : null}

      {/* Comments section */}
      {showComments && (
        <div className="mt-4 border-t border-[#1a3a5c]/60 pt-4 space-y-3">
          {commentCount === 0 ? (
            <p className="text-xs text-slate-600">No comments yet.</p>
          ) : (
            post.comments.map((comment) => {
              const isEditing = editingCommentId === comment.id;
              const isMine = currentPlayerId && comment.author?.id === currentPlayerId;
              const busy = commentActionLoadingId === comment.id;

              return (
                <div key={comment.id} className="rounded-lg border border-[#1a3a5c]/60 bg-[#060d1a] p-3">
                  <div className="flex items-center gap-2">
                    <div className="flex h-5 w-5 items-center justify-center rounded-full bg-[#0a1628] text-[9px] font-bold text-slate-400">
                      {(comment.author?.username || '?').charAt(0).toUpperCase()}
                    </div>
                    <p className="text-xs font-medium text-slate-400">{comment.author?.username || 'Unknown'}</p>
                    <p className="ml-auto text-[10px] text-slate-600">{timeAgo(comment.created_at)}</p>
                  </div>

                  {isEditing ? (
                    <div className="mt-2 space-y-2">
                      <textarea
                        value={editingCommentContent}
                        onChange={(e) => setEditingCommentContent(e.target.value)}
                        rows={2}
                        disabled={busy}
                        className="w-full rounded-lg border border-[#1a3a5c] bg-[#06101e] px-2.5 py-2 text-xs text-slate-100 outline-none focus:ring focus:ring-cyan-400/20 disabled:opacity-70"
                      />
                      <div className="flex gap-2">
                        <button type="button" onClick={() => handleSaveComment(comment.id)} disabled={busy}
                          className="rounded border border-cyan-500/50 bg-cyan-500/10 px-2.5 py-1 text-xs text-cyan-200 disabled:opacity-60">
                          {busy ? 'Saving...' : 'Save'}
                        </button>
                        <button type="button" onClick={() => { setEditingCommentId(null); setEditingCommentContent(''); }} disabled={busy}
                          className="rounded border border-[#1a3a5c] px-2.5 py-1 text-xs text-slate-400 disabled:opacity-60">
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <p className="mt-1.5 whitespace-pre-wrap text-xs text-slate-300">{comment.content}</p>
                  )}

                  {isMine && !isEditing ? (
                    <div className="mt-2 flex gap-2">
                      <button type="button" onClick={() => { setEditingCommentId(comment.id); setEditingCommentContent(comment.content); }} disabled={busy}
                        className="text-[10px] text-slate-500 hover:text-slate-300 disabled:opacity-60">
                        Edit
                      </button>
                      <button type="button" onClick={() => handleDeleteComment(comment.id)} disabled={busy}
                        className="text-[10px] text-rose-500 hover:text-rose-400 disabled:opacity-60">
                        {busy ? 'Deleting...' : 'Delete'}
                      </button>
                    </div>
                  ) : null}
                </div>
              );
            })
          )}

          <form className="flex gap-2" onSubmit={handleAddComment}>
            <input
              value={newComment}
              onChange={(e) => { setNewComment(e.target.value); if (commentError) setCommentError(''); }}
              disabled={submittingComment}
              placeholder="Add a comment..."
              className="flex-1 rounded-lg border border-[#1a3a5c] bg-[#06101e] px-3 py-2 text-xs text-slate-100 outline-none focus:ring focus:ring-cyan-400/20 disabled:opacity-70 placeholder:text-slate-600"
            />
            <button
              type="submit"
              disabled={submittingComment}
              className="rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-3 py-2 text-xs text-cyan-200 disabled:opacity-60"
            >
              {submittingComment ? '...' : 'Post'}
            </button>
          </form>

          {commentError ? <p className="text-xs text-rose-400">{commentError}</p> : null}
        </div>
      )}
    </article>
  );
}
