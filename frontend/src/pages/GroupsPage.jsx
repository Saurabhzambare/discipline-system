import { useCallback, useEffect, useState } from 'react';
import PostCard from '../components/PostCard';
import PostComposer from '../components/PostComposer';
import { createSocialPost, getGroupFeed, getGroupMembers } from '../api';

/* ── Create group form ───────────────────────────────────────────────────── */
function CreateGroupForm({ onCreate, onCancel }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [isPrivate, setIsPrivate] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    setError('');
    try {
      await onCreate({ name: name.trim(), description: description.trim(), is_private: isPrivate });
      onCancel();
    } catch (err) {
      setError(err.message || 'Could not create group.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-xl border border-cyan-500/30 bg-[#0a1628] p-5">
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent" />
      <h3 className="mb-4 text-sm font-semibold text-slate-200">New Group</h3>
      <form className="space-y-3" onSubmit={handleSubmit}>
        <label className="block space-y-1">
          <span className="text-xs uppercase tracking-wide text-slate-500">Group Name</span>
          <input
            value={name}
            onChange={(e) => { setName(e.target.value); if (error) setError(''); }}
            placeholder="e.g. Morning Runners"
            disabled={loading}
            className="w-full rounded-lg border border-[#1a3a5c] bg-[#06101e] px-3 py-2 text-sm text-slate-100 outline-none focus:ring focus:ring-cyan-400/20 disabled:opacity-70 placeholder:text-slate-600"
          />
        </label>
        <label className="block space-y-1">
          <span className="text-xs uppercase tracking-wide text-slate-500">Description (optional)</span>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={2}
            disabled={loading}
            placeholder="What is this group about?"
            className="w-full rounded-lg border border-[#1a3a5c] bg-[#06101e] px-3 py-2 text-sm text-slate-100 outline-none focus:ring focus:ring-cyan-400/20 disabled:opacity-70 placeholder:text-slate-600"
          />
        </label>
        <label className="flex cursor-pointer items-center gap-3">
          <div
            onClick={() => setIsPrivate((v) => !v)}
            className={`relative h-5 w-9 rounded-full transition ${isPrivate ? 'bg-cyan-500' : 'bg-slate-700'}`}
          >
            <span className={`absolute top-0.5 left-0.5 h-4 w-4 rounded-full bg-white transition-transform ${isPrivate ? 'translate-x-4' : ''}`} />
          </div>
          <span className="text-sm text-slate-400">Private group</span>
        </label>
        {error ? <p className="text-xs text-rose-400">{error}</p> : null}
        <div className="flex gap-2 pt-1">
          <button
            type="submit"
            disabled={loading || !name.trim()}
            className="rounded-lg border border-cyan-500/50 bg-cyan-500/15 px-4 py-2 text-sm font-medium text-cyan-200 transition hover:bg-cyan-500/25 disabled:cursor-not-allowed disabled:border-[#1a3a5c] disabled:bg-transparent disabled:text-slate-600"
          >
            {loading ? 'Creating...' : 'Create'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            disabled={loading}
            className="rounded-lg border border-[#1a3a5c] px-4 py-2 text-sm text-slate-400 transition hover:text-slate-200"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

/* ── Group card (list view) ──────────────────────────────────────────────── */
function GroupCard({ group, currentPlayerId, onJoin, onOpen }) {
  const [busy, setBusy] = useState(false);
  const isOwner = group.owner?.id === currentPlayerId;
  const isMember = group.is_member;

  async function handleJoin() {
    setBusy(true);
    try { await onJoin(group.id); } finally { setBusy(false); }
  }

  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4 transition hover:border-cyan-500/30">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <h3 className="text-sm font-semibold text-slate-100 truncate">{group.name}</h3>
            {group.is_private ? (
              <span className="rounded-full border border-[#1a3a5c] px-2 py-0.5 text-[10px] text-slate-500">🔒 Private</span>
            ) : (
              <span className="rounded-full border border-emerald-500/30 px-2 py-0.5 text-[10px] text-emerald-500">🌐 Public</span>
            )}
            {isOwner && (
              <span className="rounded-full border border-amber-500/30 px-2 py-0.5 text-[10px] text-amber-400">Owner</span>
            )}
          </div>
          {group.description ? (
            <p className="mt-1 text-xs text-slate-500 line-clamp-2">{group.description}</p>
          ) : null}
          <p className="mt-2 text-[10px] text-slate-600">
            {group.member_count} member{group.member_count !== 1 ? 's' : ''} · by {group.owner?.username}
          </p>
        </div>

        <div className="flex flex-shrink-0 flex-col gap-2 items-end">
          {isMember || isOwner ? (
            <button
              type="button"
              onClick={() => onOpen(group)}
              className="rounded-lg border border-cyan-500/50 bg-cyan-500/10 px-3 py-1.5 text-xs font-medium text-cyan-300 transition hover:bg-cyan-500/20"
            >
              Open
            </button>
          ) : (
            <button
              type="button"
              onClick={handleJoin}
              disabled={busy}
              className="rounded-lg border border-[#1a3a5c] px-3 py-1.5 text-xs text-slate-400 transition hover:border-cyan-500/40 hover:text-cyan-300 disabled:opacity-50"
            >
              {busy ? '...' : 'Join'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

/* ── Group detail view ───────────────────────────────────────────────────── */
function GroupDetail({ group, currentPlayerId, onLeave, onBack, onAddComment, onUpdateComment, onDeleteComment, onSetReaction, onRemoveReaction, onViewProfile, onUpdatePost, onDeletePost }) {
  const [members, setMembers] = useState([]);
  const [feed, setFeed] = useState([]);
  const [loadingDetail, setLoadingDetail] = useState(true);
  const [detailError, setDetailError] = useState('');
  const [leaveBusy, setLeaveBusy] = useState(false);
  const isOwner = group.owner?.id === currentPlayerId;

  const loadDetail = useCallback(async () => {
    setLoadingDetail(true);
    setDetailError('');
    try {
      const [membersData, feedData] = await Promise.all([
        getGroupMembers(group.id),
        getGroupFeed(group.id),
      ]);
      setMembers(membersData);
      setFeed(feedData);
    } catch (err) {
      setDetailError(err.message || 'Could not load group.');
    } finally {
      setLoadingDetail(false);
    }
  }, [group.id]);

  useEffect(() => { loadDetail(); }, [loadDetail]);

  async function handleCreatePost({ content, visibility }) {
    await createSocialPost({ content, visibility, group_id: group.id });
    await loadDetail();
  }

  async function handleRefreshPost() {
    const updated = await getGroupFeed(group.id);
    setFeed(updated);
  }

  async function handleLeave() {
    setLeaveBusy(true);
    try { await onLeave(group.id); onBack(); } finally { setLeaveBusy(false); }
  }

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="relative overflow-hidden rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5">
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onBack}
            className="rounded-lg border border-[#1a3a5c] px-2.5 py-1.5 text-xs text-slate-400 hover:text-slate-200"
          >
            ← Back
          </button>
          <div className="flex-1 min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-lg font-bold text-slate-100">{group.name}</h1>
              {group.is_private ? (
                <span className="text-[10px] text-slate-500">🔒 Private</span>
              ) : (
                <span className="text-[10px] text-emerald-500">🌐 Public</span>
              )}
            </div>
            {group.description ? <p className="mt-0.5 text-xs text-slate-500">{group.description}</p> : null}
          </div>
          {!isOwner && (
            <button
              type="button"
              onClick={handleLeave}
              disabled={leaveBusy}
              className="rounded-lg border border-rose-500/30 bg-rose-500/10 px-3 py-1.5 text-xs text-rose-300 hover:bg-rose-500/20 disabled:opacity-50"
            >
              {leaveBusy ? '...' : 'Leave'}
            </button>
          )}
        </div>
      </div>

      {loadingDetail ? (
        <p className="py-6 text-center text-sm text-slate-500">Loading group...</p>
      ) : detailError ? (
        <div className="rounded-xl border border-rose-500/40 bg-rose-500/10 p-4 text-rose-300 text-sm">{detailError}</div>
      ) : (
        <div className="grid gap-5 xl:grid-cols-[1fr_220px]">
          {/* Feed column */}
          <div className="space-y-4">
            <PostComposer onCreatePost={handleCreatePost} />
            {feed.length === 0 ? (
              <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-6 text-center">
                <p className="text-sm text-slate-500">No posts yet. Be the first to share something.</p>
              </div>
            ) : (
              feed.map((post) => (
                <PostCard
                  key={post.id}
                  post={post}
                  currentPlayerId={currentPlayerId}
                  onRefreshPost={handleRefreshPost}
                  onAddComment={onAddComment}
                  onUpdateComment={onUpdateComment}
                  onDeleteComment={onDeleteComment}
                  onSetReaction={onSetReaction}
                  onRemoveReaction={onRemoveReaction}
                  onViewProfile={onViewProfile}
                  onUpdatePost={onUpdatePost}
                  onDeletePost={onDeletePost ? (postId) => onDeletePost(postId, loadDetail) : undefined}
                />
              ))
            )}
          </div>

          {/* Members column */}
          <aside className="space-y-3">
            <h3 className="text-xs uppercase tracking-[0.2em] text-slate-500">
              Members ({members.length})
            </h3>
            <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-3">
              <ul className="divide-y divide-[#1a3a5c]/40">
                {members.map((m) => (
                  <li key={m.id} className="flex items-center gap-2.5 py-2">
                    <div className="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full border border-[#1a3a5c] bg-[#060d1a] text-xs font-bold text-cyan-400">
                      {(m.player?.username || '?').charAt(0).toUpperCase()}
                    </div>
                    <span className="flex-1 truncate text-xs text-slate-300">{m.player?.username}</span>
                    {m.role === 'owner' && (
                      <span className="text-[10px] text-amber-400">Owner</span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          </aside>
        </div>
      )}
    </div>
  );
}

/* ── Main GroupsPage ─────────────────────────────────────────────────────── */
export default function GroupsPage({
  groups,
  loading,
  error,
  currentPlayerId,
  onRefresh,
  onCreateGroup,
  onJoinGroup,
  onLeaveGroup,
  onAddComment,
  onUpdateComment,
  onDeleteComment,
  onSetReaction,
  onRemoveReaction,
  onViewProfile,
  onUpdatePost,
  onDeletePost,
}) {
  const [showCreate, setShowCreate] = useState(false);
  const [openGroup, setOpenGroup] = useState(null);
  const [activeTab, setActiveTab] = useState('mine');

  async function handleJoin(groupId) {
    await onJoinGroup(groupId);
  }

  if (openGroup) {
    return (
      <GroupDetail
        group={openGroup}
        currentPlayerId={currentPlayerId}
        onLeave={onLeaveGroup}
        onBack={() => { setOpenGroup(null); onRefresh(); }}
        onAddComment={onAddComment}
        onUpdateComment={onUpdateComment}
        onDeleteComment={onDeleteComment}
        onSetReaction={onSetReaction}
        onRemoveReaction={onRemoveReaction}
        onViewProfile={onViewProfile}
        onUpdatePost={onUpdatePost}
        onDeletePost={onDeletePost}
      />
    );
  }

  const myGroups = groups.filter((g) => g.is_member || g.owner?.id === currentPlayerId);
  const exploreGroups = groups.filter((g) => !g.is_member && g.owner?.id !== currentPlayerId);
  const displayGroups = activeTab === 'mine' ? myGroups : exploreGroups;

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="relative overflow-hidden rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5">
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-[10px] uppercase tracking-[0.25em] text-cyan-400/70">Community</p>
            <h1 className="mt-1 text-xl font-bold text-slate-100">Groups</h1>
            <p className="mt-0.5 text-xs text-slate-500">Join or create groups to share progress with others.</p>
          </div>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={onRefresh}
              className="rounded-lg border border-[#1a3a5c] px-3 py-1.5 text-xs text-slate-400 hover:border-cyan-500/40 hover:text-cyan-300"
            >
              Refresh
            </button>
            <button
              type="button"
              onClick={() => setShowCreate((v) => !v)}
              className="rounded-lg border border-cyan-500/50 bg-cyan-500/15 px-3 py-1.5 text-xs font-medium text-cyan-200 hover:bg-cyan-500/25"
            >
              {showCreate ? 'Cancel' : '+ New Group'}
            </button>
          </div>
        </div>
      </div>

      {showCreate && (
        <CreateGroupForm
          onCreate={async (data) => { await onCreateGroup(data); setShowCreate(false); await onRefresh(); }}
          onCancel={() => setShowCreate(false)}
        />
      )}

      {/* Tabs (Feature 9) */}
      <div className="flex gap-1 rounded-xl border border-[#1a3a5c] bg-[#070f1e] p-1">
        {[
          { id: 'mine', label: `My Groups`, count: myGroups.length },
          { id: 'explore', label: 'Explore', count: exploreGroups.length },
        ].map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setActiveTab(tab.id)}
            className={`flex flex-1 items-center justify-center gap-2 rounded-lg py-2 text-sm font-medium transition ${
              activeTab === tab.id
                ? 'bg-[#0a1628] text-slate-100 shadow-sm'
                : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            {tab.label}
            <span className={`rounded-full px-1.5 py-0.5 text-[10px] ${
              activeTab === tab.id ? 'bg-cyan-500/20 text-cyan-300' : 'bg-[#1a3a5c]/60 text-slate-500'
            }`}>
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {loading ? (
        <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-6 text-center">
          <p className="text-sm text-slate-500">Loading groups...</p>
        </div>
      ) : error ? (
        <div className="rounded-xl border border-rose-500/40 bg-rose-500/10 p-4 text-rose-300">
          <p className="text-sm">{error}</p>
          <button type="button" onClick={onRefresh} className="mt-2 text-xs hover:text-rose-200">Retry</button>
        </div>
      ) : displayGroups.length === 0 ? (
        <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-8 text-center">
          <p className="text-sm text-slate-500">
            {activeTab === 'mine'
              ? "You haven't joined any groups yet. Check Explore to find one."
              : 'No other groups to explore. Create a new one!'}
          </p>
        </div>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2">
          {displayGroups.map((group) => (
            <GroupCard
              key={group.id}
              group={group}
              currentPlayerId={currentPlayerId}
              onJoin={handleJoin}
              onOpen={setOpenGroup}
            />
          ))}
        </div>
      )}
    </div>
  );
}
