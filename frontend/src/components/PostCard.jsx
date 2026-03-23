import { useEffect, useMemo, useState } from 'react';

const REACTION_OPTIONS = [
  { value: 'like', label: 'Like' },
  { value: 'fire', label: 'Fire' },
  { value: 'respect', label: 'Respect' },
  { value: 'clap', label: 'Clap' },
];

function formatPostType(postType) {
  if (!postType) return 'Update';
  return postType
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function formatVisibility(visibility) {
  if (!visibility) return 'Public';
  return visibility
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function formatCreatedAt(createdAt) {
  if (!createdAt) return 'Unknown date';

  const date = new Date(createdAt);
  if (Number.isNaN(date.getTime())) return 'Unknown date';

  return date.toLocaleString();
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
}) {
  const [newComment, setNewComment] = useState('');
  const [commentError, setCommentError] = useState('');
  const [submittingComment, setSubmittingComment] = useState(false);
  const [commentActionLoadingId, setCommentActionLoadingId] = useState(null);
  const [editingCommentId, setEditingCommentId] = useState(null);
  const [editingCommentContent, setEditingCommentContent] = useState('');

  const [reactionLoading, setReactionLoading] = useState(false);
  const [reactionError, setReactionError] = useState('');

  useEffect(() => {
    setCommentError('');
    setReactionError('');

    if (editingCommentId) {
      const targetComment = post.comments?.find((comment) => comment.id === editingCommentId);
      if (!targetComment) {
        setEditingCommentId(null);
        setEditingCommentContent('');
      }
    }
  }, [editingCommentId, post.comments]);

  const reactionSummary = useMemo(() => {
    const summary = { like: 0, fire: 0, respect: 0, clap: 0 };
    (post.reactions || []).forEach((reaction) => {
      if (summary[reaction.reaction_type] !== undefined) {
        summary[reaction.reaction_type] += 1;
      }
    });
    return summary;
  }, [post.reactions]);

  const myReaction = useMemo(
    () => (post.reactions || []).find((reaction) => reaction.player?.id === currentPlayerId) || null,
    [currentPlayerId, post.reactions],
  );

  async function handleAddComment(event) {
    event.preventDefault();
    const trimmedComment = newComment.trim();

    if (!trimmedComment) {
      setCommentError('Please write a comment before submitting.');
      return;
    }

    setSubmittingComment(true);
    setCommentError('');

    try {
      await onAddComment(post.id, trimmedComment);
      setNewComment('');
      await onRefreshPost(post.id);
    } catch (error) {
      setCommentError(error.message || 'Could not add comment.');
    } finally {
      setSubmittingComment(false);
    }
  }

  function startEditing(comment) {
    setEditingCommentId(comment.id);
    setEditingCommentContent(comment.content);
    setCommentError('');
  }

  function cancelEditing() {
    setEditingCommentId(null);
    setEditingCommentContent('');
  }

  async function handleSaveComment(commentId) {
    const trimmedComment = editingCommentContent.trim();

    if (!trimmedComment) {
      setCommentError('Edited comment cannot be empty.');
      return;
    }

    setCommentActionLoadingId(commentId);
    setCommentError('');

    try {
      await onUpdateComment(post.id, commentId, trimmedComment);
      cancelEditing();
      await onRefreshPost(post.id);
    } catch (error) {
      setCommentError(error.message || 'Could not update comment.');
    } finally {
      setCommentActionLoadingId(null);
    }
  }

  async function handleDeleteComment(commentId) {
    setCommentActionLoadingId(commentId);
    setCommentError('');

    try {
      await onDeleteComment(post.id, commentId);
      if (editingCommentId === commentId) {
        cancelEditing();
      }
      await onRefreshPost(post.id);
    } catch (error) {
      setCommentError(error.message || 'Could not delete comment.');
    } finally {
      setCommentActionLoadingId(null);
    }
  }

  async function handleReactionSelect(reactionType) {
    setReactionLoading(true);
    setReactionError('');

    try {
      await onSetReaction(post.id, reactionType);
      await onRefreshPost(post.id);
    } catch (error) {
      setReactionError(error.message || 'Could not update reaction.');
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
    } catch (error) {
      setReactionError(error.message || 'Could not remove reaction.');
    } finally {
      setReactionLoading(false);
    }
  }

  return (
    <article className="rounded-xl border border-slate-700 bg-slate-900/70 p-4">
      <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
        <span className="rounded-full border border-cyan-500/40 bg-cyan-500/10 px-2 py-1 text-cyan-300">
          {formatPostType(post.post_type)}
        </span>
        <span className="rounded-full border border-slate-700 bg-slate-800/80 px-2 py-1 text-slate-300">
          {formatVisibility(post.visibility)}
        </span>
      </div>

      <p className="mt-3 text-sm text-slate-300">
        <span className="text-slate-400">Author:</span>{' '}
        <span className="font-medium text-slate-100">{post.author?.username || 'Unknown Hunter'}</span>
      </p>

      <p className="mt-3 whitespace-pre-wrap text-sm leading-relaxed text-slate-200">{post.content}</p>

      <p className="mt-4 text-xs text-slate-400">Posted: {formatCreatedAt(post.created_at)}</p>

      <div className="mt-4 border-t border-slate-800 pt-4">
        <h4 className="text-sm font-semibold text-slate-200">Reactions</h4>

        <div className="mt-2 flex flex-wrap gap-2">
          {REACTION_OPTIONS.map((option) => {
            const active = myReaction?.reaction_type === option.value;
            return (
              <button
                key={option.value}
                type="button"
                onClick={() => handleReactionSelect(option.value)}
                disabled={reactionLoading}
                className={`rounded-lg border px-3 py-1 text-xs transition ${
                  active
                    ? 'border-cyan-500/70 bg-cyan-500/20 text-cyan-200'
                    : 'border-slate-700 bg-slate-900 text-slate-300 hover:border-cyan-500/50 hover:text-cyan-200'
                } disabled:cursor-not-allowed disabled:opacity-60`}
              >
                {option.label} ({reactionSummary[option.value] || 0})
              </button>
            );
          })}

          {myReaction ? (
            <button
              type="button"
              onClick={handleReactionRemove}
              disabled={reactionLoading}
              className="rounded-lg border border-rose-500/50 bg-rose-500/10 px-3 py-1 text-xs text-rose-200 transition hover:bg-rose-500/20 disabled:cursor-not-allowed disabled:opacity-60"
            >
              Remove reaction
            </button>
          ) : null}
        </div>

        {reactionError ? <p className="mt-2 text-xs text-rose-300">{reactionError}</p> : null}
      </div>

      <div className="mt-4 border-t border-slate-800 pt-4">
        <h4 className="text-sm font-semibold text-slate-200">Comments</h4>

        {!post.comments || post.comments.length === 0 ? (
          <p className="mt-2 text-sm text-slate-400">No comments yet.</p>
        ) : (
          <div className="mt-3 space-y-3">
            {post.comments.map((comment) => {
              const isEditing = editingCommentId === comment.id;
              const isMine = currentPlayerId && comment.author?.id === currentPlayerId;
              const commentBusy = commentActionLoadingId === comment.id;

              return (
                <div key={comment.id} className="rounded-lg border border-slate-800 bg-slate-950/70 p-3">
                  <p className="text-xs text-slate-400">{comment.author?.username || 'Unknown Hunter'}</p>

                  {isEditing ? (
                    <div className="mt-2 space-y-2">
                      <textarea
                        value={editingCommentContent}
                        onChange={(event) => setEditingCommentContent(event.target.value)}
                        rows={3}
                        disabled={commentBusy}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none ring-cyan-400/40 transition focus:ring disabled:opacity-70"
                      />
                      <div className="flex gap-2">
                        <button
                          type="button"
                          onClick={() => handleSaveComment(comment.id)}
                          disabled={commentBusy}
                          className="rounded-lg border border-cyan-500/60 bg-cyan-500/20 px-3 py-1 text-xs text-cyan-200 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                          {commentBusy ? 'Saving...' : 'Save'}
                        </button>
                        <button
                          type="button"
                          onClick={cancelEditing}
                          disabled={commentBusy}
                          className="rounded-lg border border-slate-700 px-3 py-1 text-xs text-slate-300 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <p className="mt-1 whitespace-pre-wrap text-sm text-slate-200">{comment.content}</p>
                  )}

                  <p className="mt-2 text-xs text-slate-500">{formatCreatedAt(comment.created_at)}</p>

                  {isMine && !isEditing ? (
                    <div className="mt-2 flex gap-2">
                      <button
                        type="button"
                        onClick={() => startEditing(comment)}
                        disabled={commentBusy}
                        className="rounded-lg border border-slate-700 px-2 py-1 text-xs text-slate-300 disabled:cursor-not-allowed disabled:opacity-60"
                      >
                        Edit
                      </button>
                      <button
                        type="button"
                        onClick={() => handleDeleteComment(comment.id)}
                        disabled={commentBusy}
                        className="rounded-lg border border-rose-500/50 bg-rose-500/10 px-2 py-1 text-xs text-rose-200 disabled:cursor-not-allowed disabled:opacity-60"
                      >
                        {commentBusy ? 'Deleting...' : 'Delete'}
                      </button>
                    </div>
                  ) : null}
                </div>
              );
            })}
          </div>
        )}

        <form className="mt-4 space-y-2" onSubmit={handleAddComment}>
          <label className="block space-y-1">
            <span className="text-xs uppercase tracking-[0.08em] text-slate-400">Add comment</span>
            <textarea
              value={newComment}
              onChange={(event) => {
                setNewComment(event.target.value);
                if (commentError) setCommentError('');
              }}
              rows={2}
              disabled={submittingComment}
              placeholder="Write a comment..."
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none ring-cyan-400/40 transition focus:ring disabled:opacity-70"
            />
          </label>

          <button
            type="submit"
            disabled={submittingComment}
            className="rounded-lg border border-cyan-500/60 bg-cyan-500/20 px-3 py-1 text-xs text-cyan-200 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {submittingComment ? 'Commenting...' : 'Add comment'}
          </button>
        </form>

        {commentError ? <p className="mt-2 text-xs text-rose-300">{commentError}</p> : null}
      </div>
    </article>
  );
}
