import { useEffect, useRef, useState } from 'react';
import { searchPlayers } from '../api';

/* ── Send friend request panel with live search ─────────────────────────── */
function SendRequestPanel({ onSend }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [sendingId, setSendingId] = useState(null);
  const [sentIds, setSentIds] = useState(new Set());
  const [error, setError] = useState('');
  const debounceRef = useRef(null);

  useEffect(() => {
    const q = query.trim();
    if (q.length < 2) { setResults([]); return; }

    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(async () => {
      setSearching(true);
      try {
        const data = await searchPlayers(q);
        setResults(data);
      } catch {
        setResults([]);
      } finally {
        setSearching(false);
      }
    }, 300);

    return () => clearTimeout(debounceRef.current);
  }, [query]);

  async function handleSend(player) {
    setSendingId(player.id);
    setError('');
    try {
      await onSend(player.username);
      setSentIds((prev) => new Set([...prev, player.id]));
    } catch (err) {
      setError(err.message || 'Could not send request.');
    } finally {
      setSendingId(null);
    }
  }

  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#060d1a] p-4">
      <p className="mb-3 text-sm font-semibold text-slate-200">Find a Hunter</p>
      <div className="relative">
        <input
          value={query}
          onChange={(e) => { setQuery(e.target.value); if (error) setError(''); }}
          placeholder="Search by username..."
          className="w-full rounded-lg border border-[#1a3a5c] bg-[#06101e] px-3 py-2 text-sm text-slate-100 outline-none focus:ring focus:ring-cyan-400/20 placeholder:text-slate-600"
        />
        {searching && (
          <span className="absolute right-3 top-2.5 block h-4 w-4 animate-spin rounded-full border border-slate-600 border-t-cyan-400" />
        )}
      </div>

      {results.length > 0 && (
        <ul className="mt-2 divide-y divide-[#1a3a5c]/40 rounded-lg border border-[#1a3a5c] bg-[#06101e]">
          {results.map((p) => {
            const sent = sentIds.has(p.id);
            return (
              <li key={p.id} className="flex items-center gap-3 px-3 py-2.5">
                <div className="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full border border-[#1a3a5c] bg-[#0a1628] text-xs font-bold text-cyan-400">
                  {p.username.charAt(0).toUpperCase()}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-slate-200 truncate">{p.username}</p>
                  <p className="text-[10px] text-slate-500">Level {p.level}</p>
                </div>
                <button
                  type="button"
                  onClick={() => handleSend(p)}
                  disabled={sent || sendingId === p.id}
                  className={`rounded-lg border px-3 py-1 text-xs font-medium transition ${
                    sent
                      ? 'border-emerald-500/40 text-emerald-400'
                      : 'border-cyan-500/50 bg-cyan-500/10 text-cyan-300 hover:bg-cyan-500/20 disabled:opacity-60'
                  }`}
                >
                  {sent ? '✓ Sent' : sendingId === p.id ? '...' : 'Add'}
                </button>
              </li>
            );
          })}
        </ul>
      )}

      {query.trim().length >= 2 && !searching && results.length === 0 && (
        <p className="mt-2 text-xs text-slate-500">No players found.</p>
      )}

      {error ? <p className="mt-2 text-xs text-rose-400">{error}</p> : null}
    </div>
  );
}

/* ── Incoming requests list ─────────────────────────────────────────────── */
function IncomingRequests({ requests, onAccept, onDecline }) {
  const [busyId, setBusyId] = useState(null);

  if (requests.length === 0) return null;

  async function handle(id, action) {
    setBusyId(id);
    try { await action(id); } finally { setBusyId(null); }
  }

  return (
    <div className="rounded-xl border border-amber-500/30 bg-amber-500/5 p-4">
      <p className="mb-3 text-sm font-semibold text-amber-300">
        Incoming Requests
        <span className="ml-2 rounded-full bg-amber-500/20 px-2 py-0.5 text-xs text-amber-400">
          {requests.length}
        </span>
      </p>
      <ul className="space-y-2">
        {requests.map((req) => (
          <li key={req.id} className="flex items-center gap-3">
            <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full border border-[#1a3a5c] bg-[#060d1a] text-xs font-bold text-cyan-400">
              {(req.from_player?.username || '?').charAt(0).toUpperCase()}
            </div>
            <span className="flex-1 text-sm text-slate-300">{req.from_player?.username || '—'}</span>
            <button
              type="button"
              onClick={() => handle(req.id, onAccept)}
              disabled={busyId === req.id}
              className="rounded-lg border border-emerald-500/50 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-300 transition hover:bg-emerald-500/20 disabled:opacity-50"
            >
              Accept
            </button>
            <button
              type="button"
              onClick={() => handle(req.id, onDecline)}
              disabled={busyId === req.id}
              className="rounded-lg border border-[#1a3a5c] px-3 py-1 text-xs text-slate-400 transition hover:border-rose-500/40 hover:text-rose-300 disabled:opacity-50"
            >
              Decline
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ── Outgoing pending requests ──────────────────────────────────────────── */
function OutgoingRequests({ requests, onCancel }) {
  const [busyId, setBusyId] = useState(null);

  if (requests.length === 0) return null;

  async function handle(id) {
    setBusyId(id);
    try { await onCancel(id); } finally { setBusyId(null); }
  }

  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
      <p className="mb-3 text-sm font-semibold text-slate-400">Pending Sent</p>
      <ul className="space-y-2">
        {requests.map((req) => (
          <li key={req.id} className="flex items-center gap-3">
            <div className="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full border border-[#1a3a5c] bg-[#060d1a] text-xs text-slate-500">
              {(req.to_player?.username || '?').charAt(0).toUpperCase()}
            </div>
            <span className="flex-1 text-sm text-slate-400">{req.to_player?.username || '—'}</span>
            <span className="rounded-full border border-[#1a3a5c] px-2 py-0.5 text-[10px] text-slate-500">Pending</span>
            <button
              type="button"
              onClick={() => handle(req.id)}
              disabled={busyId === req.id}
              className="text-xs text-slate-600 hover:text-rose-400 disabled:opacity-50"
            >
              Cancel
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ── Friends list ───────────────────────────────────────────────────────── */
function FriendsList({ friends, onRemove }) {
  const [busyId, setBusyId] = useState(null);

  async function handle(id) {
    setBusyId(id);
    try { await onRemove(id); } finally { setBusyId(null); }
  }

  if (friends.length === 0) {
    return (
      <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-6 text-center">
        <p className="text-sm text-slate-500">No friends yet. Send a request to add hunters.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
      <p className="mb-3 text-sm font-semibold text-slate-200">
        Friends
        <span className="ml-2 text-slate-500">({friends.length})</span>
      </p>
      <ul className="divide-y divide-[#1a3a5c]/40">
        {friends.map((friend) => (
          <li key={friend.id} className="flex items-center gap-3 py-2.5">
            <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full border border-cyan-500/30 bg-cyan-500/10 text-xs font-bold text-cyan-400">
              {(friend.username || '?').charAt(0).toUpperCase()}
            </div>
            <span className="flex-1 text-sm font-medium text-slate-200">{friend.username}</span>
            <button
              type="button"
              onClick={() => handle(friend.id)}
              disabled={busyId === friend.id}
              className="text-xs text-slate-600 hover:text-rose-400 disabled:opacity-50"
            >
              {busyId === friend.id ? 'Removing...' : 'Remove'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ── Main ProfilePage ───────────────────────────────────────────────────── */
export default function ProfilePage({
  player,
  selectedPathDisplay,
  onNavigate,
  friends,
  incomingRequests,
  outgoingRequests,
  loadingFriends,
  friendsError,
  onSendFriendRequest,
  onAcceptRequest,
  onDeclineRequest,
  onCancelRequest,
  onRemoveFriend,
  onRefreshFriends,
}) {
  const [tab, setTab] = useState('profile');

  const tabs = [
    { id: 'profile', label: 'Profile' },
    {
      id: 'friends',
      label: 'Friends',
      badge: incomingRequests?.length || null,
    },
  ];

  return (
    <div className="max-w-2xl space-y-5">
      {/* Tab bar */}
      <div className="flex gap-1 rounded-xl border border-[#1a3a5c] bg-[#070f1e] p-1">
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setTab(t.id)}
            className={`relative flex flex-1 items-center justify-center gap-2 rounded-lg py-2 text-sm font-medium transition ${
              tab === t.id
                ? 'bg-[#0a1628] text-slate-100 shadow-sm'
                : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            {t.label}
            {t.badge ? (
              <span className="flex h-4 min-w-[1rem] items-center justify-center rounded-full bg-amber-500 px-1 text-[10px] font-bold text-black">
                {t.badge}
              </span>
            ) : null}
          </button>
        ))}
      </div>

      {/* ── Profile tab ── */}
      {tab === 'profile' && (
        <>
          <div className="relative overflow-hidden rounded-2xl border border-[#1a3a5c] bg-gradient-to-br from-[#0a1628] to-[#071020] p-6 shadow-[0_0_40px_rgba(6,182,212,0.06)]">
            <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />
            <div className="flex items-start gap-5">
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
        </>
      )}

      {/* ── Friends tab ── */}
      {tab === 'friends' && (
        <div className="space-y-4">
          {loadingFriends ? (
            <p className="py-4 text-center text-sm text-slate-500">Loading friends...</p>
          ) : friendsError ? (
            <div className="rounded-xl border border-rose-500/40 bg-rose-500/10 p-4 text-rose-300">
              <p className="text-sm">{friendsError}</p>
              <button type="button" onClick={onRefreshFriends} className="mt-2 text-xs hover:text-rose-200">
                Retry
              </button>
            </div>
          ) : (
            <>
              <SendRequestPanel onSend={onSendFriendRequest} />
              <IncomingRequests
                requests={incomingRequests || []}
                onAccept={onAcceptRequest}
                onDecline={onDeclineRequest}
              />
              <FriendsList friends={friends || []} onRemove={onRemoveFriend} />
              <OutgoingRequests requests={outgoingRequests || []} onCancel={onCancelRequest} />
            </>
          )}
        </div>
      )}
    </div>
  );
}
