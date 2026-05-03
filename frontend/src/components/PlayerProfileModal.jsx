import { useEffect, useState } from 'react';
import { getPublicProfile } from '../api';
import { PathProfileCards, BadgeSection, AchievementCards } from './ProfileExtensions';

function timeAgo(isoString) {
  if (!isoString) return '';
  const diff = Math.floor((Date.now() - new Date(isoString)) / 1000);
  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

export default function PlayerProfileModal({ username, onClose, onSendRequest, currentPlayerId }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [requestSent, setRequestSent] = useState(false);
  const [requestBusy, setRequestBusy] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError('');
    getPublicProfile(username)
      .then((data) => { if (!cancelled) setProfile(data); })
      .catch((err) => { if (!cancelled) setError(err.message || 'Could not load profile.'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [username]);

  async function handleAddFriend() {
    if (!profile || !onSendRequest) return;
    setRequestBusy(true);
    try {
      await onSendRequest(profile.username);
      setRequestSent(true);
    } catch {
      // silently ignore — could already be friends
    } finally {
      setRequestBusy(false);
    }
  }

  const isOwnProfile = profile && currentPlayerId && profile.id === currentPlayerId;

  return (
    /* Backdrop */
    <div
      className="fixed inset-0 z-50 flex items-center justify-center px-4"
      style={{ background: 'rgba(5,13,26,0.85)', backdropFilter: 'blur(4px)' }}
      onClick={onClose}
    >
      <div
        className="relative flex w-full max-w-md max-h-[90vh] flex-col overflow-hidden rounded-2xl border border-[#1a3a5c] bg-[#0a1628] shadow-[0_0_60px_rgba(6,182,212,0.1)]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Top glow line */}
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />

        {/* Close button */}
        <button
          type="button"
          onClick={onClose}
          className="absolute right-3 top-3 flex h-7 w-7 items-center justify-center rounded-lg border border-[#1a3a5c] text-slate-500 transition hover:text-slate-200"
        >
          ✕
        </button>

        <div className="overflow-y-auto p-6">
          {loading ? (
            <div className="flex h-32 items-center justify-center">
              <p className="text-sm text-slate-500">Loading profile...</p>
            </div>
          ) : error ? (
            <p className="py-8 text-center text-sm text-rose-400">{error}</p>
          ) : profile ? (
            <>
              {/* Avatar + name */}
              <div className="flex items-center gap-4">
                <div className="flex h-14 w-14 flex-shrink-0 items-center justify-center rounded-full border-2 border-cyan-500/40 bg-cyan-500/10 text-xl font-black text-cyan-300">
                  {profile.username.charAt(0).toUpperCase()}
                </div>
                <div>
                  <h2 className="text-lg font-bold text-slate-100">{profile.username}</h2>
                  <p className="text-xs text-slate-500">Hunter #{profile.id}</p>
                </div>
              </div>

              {/* Stats row */}
              <div className="mt-5 grid grid-cols-3 gap-3">
                {[
                  { label: 'Level', value: profile.level, color: 'text-cyan-300' },
                  { label: 'EXP', value: profile.exp, color: 'text-amber-300' },
                  { label: 'Streak', value: `${profile.streak}d`, color: 'text-orange-400' },
                ].map(({ label, value, color }) => (
                  <div key={label} className="rounded-lg border border-[#1a3a5c]/80 bg-[#060d1a] p-3 text-center">
                    <p className="text-[10px] uppercase tracking-wide text-slate-500">{label}</p>
                    <p className={`mt-1 text-lg font-bold ${color}`}>{value}</p>
                  </div>
                ))}
              </div>

              {/* Path profile cards */}
              <div className="mt-5">
                <p className="mb-2 text-xs uppercase tracking-[0.15em] text-slate-500">Active Paths</p>
                <PathProfileCards pathProfiles={profile.path_profiles} />
              </div>

              {/* Titles & Badges */}
              <div className="mt-5">
                <BadgeSection badges={profile.badges} />
              </div>

              {/* Achievement Cards */}
              <div className="mt-5">
                <AchievementCards cards={profile.achievement_cards} />
              </div>

              {/* Recent posts */}
              {profile.recent_posts?.length > 0 && (
                <div className="mt-5">
                  <p className="mb-2 text-xs uppercase tracking-[0.15em] text-slate-500">Recent Activity</p>
                  <div className="space-y-2">
                    {profile.recent_posts.slice(0, 3).map((post) => (
                      <div key={post.id} className="rounded-lg border border-[#1a3a5c]/60 bg-[#060d1a] p-3">
                        <p className="text-xs text-slate-300 line-clamp-2">{post.content}</p>
                        <p className="mt-1 text-[10px] text-slate-600">{timeAgo(post.created_at)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Add friend button */}
              {!isOwnProfile && onSendRequest && (
                <button
                  type="button"
                  onClick={handleAddFriend}
                  disabled={requestBusy || requestSent}
                  className={`mt-5 w-full rounded-xl border py-2.5 text-sm font-semibold transition ${
                    requestSent
                      ? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300'
                      : 'border-cyan-500/50 bg-cyan-500/15 text-cyan-200 hover:bg-cyan-500/25 disabled:opacity-60'
                  }`}
                >
                  {requestSent ? '✓ Request Sent' : requestBusy ? 'Sending...' : '+ Add Friend'}
                </button>
              )}
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}
