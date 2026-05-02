import { useEffect, useRef, useState } from 'react';

import { markNotificationsSeen } from '../api';

const NAV_ITEMS = [
  {
    path: '/dashboard',
    label: 'Dashboard',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
      </svg>
    ),
  },
  {
    path: '/feed',
    label: 'Feed',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
      </svg>
    ),
  },
  {
    path: '/groups',
    label: 'Groups',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
  },
  {
    path: '/profile',
    label: 'Profile',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
      </svg>
    ),
  },
  {
    path: '/coming-soon',
    label: 'Roadmap',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
      </svg>
    ),
  },
];

function FlashBanner({ flashMessage }) {
  if (!flashMessage) return null;
  const cls =
    flashMessage.type === 'error'
      ? 'border-rose-500/50 bg-rose-500/10 text-rose-200'
      : 'border-emerald-500/40 bg-emerald-500/10 text-emerald-200';
  return (
    <div className={`mb-5 rounded-xl border px-4 py-3 text-sm ${cls}`}>
      {flashMessage.text}
    </div>
  );
}

function timeAgo(isoString) {
  if (!isoString) return '';
  const diff = Math.floor((Date.now() - new Date(isoString)) / 1000);
  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

const NOTIF_ICONS = {
  quest_completed: '⚔️',
  level_up: '⭐',
  badge_earned: '🏅',
  weekly_boss_defeated: '🐉',
  cross_path_title_earned: '👑',
  multiplier_upgrade: '✨',
  streak_milestone: '🔥',
  partner_quest_completed: '🤝',
  partner_level_up: '🤝',
  first_dollar: '💵',
  friend_added: '👤',
  joined_group: '👥',
  post_created: '📝',
};

const MARK_SEEN_DELAY_MS = 1000;

function NotificationBell({ notifications, onMarkSeen }) {
  const [open, setOpen] = useState(false);
  const [locallySeen, setLocallySeen] = useState(() => new Set());
  const markedRef = useRef(new Set());
  const ref = useRef(null);

  const rawItems = notifications.items || [];
  const items = rawItems.map((n) =>
    locallySeen.has(n.id) ? { ...n, is_seen: true } : n,
  );
  const baseUnseen = notifications.unseen_count || 0;
  const newlyMarked = rawItems.filter((n) => !n.is_seen && locallySeen.has(n.id)).length;
  const count = Math.max(0, baseUnseen - newlyMarked);

  useEffect(() => {
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  useEffect(() => {
    if (!open) return undefined;
    const timer = setTimeout(async () => {
      const unseenIds = items
        .filter((n) => !n.is_seen && !markedRef.current.has(n.id))
        .map((n) => n.id);
      if (unseenIds.length === 0) return;
      unseenIds.forEach((id) => markedRef.current.add(id));
      try {
        await onMarkSeen(unseenIds);
        setLocallySeen((prev) => {
          const next = new Set(prev);
          unseenIds.forEach((id) => next.add(id));
          return next;
        });
      } catch {
        // bell stays usable; allow retry on next open
        unseenIds.forEach((id) => markedRef.current.delete(id));
      }
    }, MARK_SEEN_DELAY_MS);
    return () => clearTimeout(timer);
  }, [open, items, onMarkSeen]);

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="relative flex h-8 w-8 items-center justify-center rounded-lg border border-[#1a3a5c] text-slate-400 transition hover:border-cyan-500/40 hover:text-cyan-300"
        title="Notifications"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        {count > 0 && (
          <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-[9px] font-bold text-white">
            {count > 9 ? '9+' : count}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 top-10 z-50 w-80 overflow-hidden rounded-xl border border-[#1a3a5c] bg-[#070f1e] shadow-[0_8px_32px_rgba(0,0,0,0.5)]">
          <div className="flex items-center justify-between border-b border-[#1a3a5c]/60 px-4 py-3">
            <p className="text-sm font-semibold text-slate-200">Notifications</p>
            {count > 0 && (
              <span className="rounded-full bg-rose-500/20 px-2 py-0.5 text-[10px] text-rose-300">{count}</span>
            )}
          </div>

          <div className="max-h-80 overflow-y-auto">
            {items.length === 0 ? (
              <p className="px-4 py-6 text-center text-xs text-slate-500">No new notifications.</p>
            ) : (
              <ul className="divide-y divide-[#1a3a5c]/40">
                {items.map((n) => {
                  const unseen = !n.is_seen;
                  return (
                    <li
                      key={n.id}
                      className={`flex gap-3 px-4 py-3 transition ${
                        unseen
                          ? 'bg-cyan-500/5 border-l-2 border-cyan-500/60 hover:bg-[#0a1628]/60'
                          : 'hover:bg-[#0a1628]/60'
                      }`}
                    >
                      <span className="mt-0.5 text-base flex-shrink-0">{NOTIF_ICONS[n.event_type] || '🔔'}</span>
                      <div className="flex-1 min-w-0">
                        <p className={`text-xs ${unseen ? 'font-semibold text-slate-100' : 'text-slate-300'}`}>
                          {n.text_snapshot || n.event_type}
                        </p>
                        <p className="mt-0.5 text-[10px] text-slate-600">{timeAgo(n.created_at)}</p>
                      </div>
                      {unseen && (
                        <span className="mt-1 h-2 w-2 flex-shrink-0 rounded-full bg-cyan-400" aria-label="Unseen" />
                      )}
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default function Layout({
  children,
  onNavigate,
  isAuthenticated,
  onLogout,
  flashMessage,
  onDismissFlash,
  route,
  playerName,
  incomingRequestCount,
  notifications,
}) {
  useEffect(() => {
    if (!flashMessage) return undefined;
    const timeout = setTimeout(() => onDismissFlash(), 3000);
    return () => clearTimeout(timeout);
  }, [flashMessage, onDismissFlash]);

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-[#050d1a] text-slate-100">
        <div className="mx-auto max-w-lg px-4 pt-6">
          <FlashBanner flashMessage={flashMessage} />
        </div>
        {children}
      </div>
    );
  }

  // Path Discovery flow is a cinematic, chromeless experience — no sidebar,
  // no header, no notifications. Source of truth:
  // docs/game-design/systems/path-discovery.md ("No navigation elements").
  if (route === '/onboarding' || route === '/path-onboarding') {
    return (
      <div className="min-h-screen bg-[#050d1a] text-slate-100">
        {children}
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-[#050d1a] text-slate-100">
      {/* ── Sidebar ── */}
      <aside className="fixed left-0 top-0 z-40 flex h-screen w-[72px] flex-col items-center border-r border-[#1a3a5c]/50 bg-[#070f1e] py-5">
        {/* Logo gem */}
        <button
          type="button"
          onClick={() => onNavigate('/dashboard')}
          className="mb-7 flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/15 text-cyan-400 transition hover:bg-cyan-500/25"
          title="Dashboard"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2L2 9l10 13L22 9 12 2z" />
          </svg>
        </button>

        {/* Nav items */}
        <nav className="flex flex-1 flex-col items-center gap-1">
          {NAV_ITEMS.map((item) => {
            const active = route === item.path;
            const showBadge = item.path === '/profile' && incomingRequestCount > 0;
            return (
              <button
                key={item.path}
                type="button"
                onClick={() => onNavigate(item.path)}
                title={item.label}
                className={`relative flex flex-col items-center gap-1 rounded-xl px-2 py-3 text-[10px] font-medium transition w-14 ${
                  active
                    ? 'border border-cyan-500/50 bg-cyan-500/10 text-cyan-300 shadow-[0_0_12px_rgba(6,182,212,0.15)]'
                    : 'border border-transparent text-slate-500 hover:border-[#1a3a5c] hover:text-slate-300'
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
                {showBadge && (
                  <span className="absolute -right-0.5 top-1 flex h-4 w-4 items-center justify-center rounded-full bg-amber-400 text-[9px] font-bold text-slate-900">
                    {incomingRequestCount > 9 ? '9+' : incomingRequestCount}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Logout */}
        <button
          type="button"
          onClick={onLogout}
          title="Logout"
          className="flex flex-col items-center gap-1 rounded-xl px-2 py-3 text-[10px] font-medium text-slate-600 transition hover:text-rose-400 w-14"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span>Logout</span>
        </button>
      </aside>

      {/* ── Main content ── */}
      <div className="ml-[72px] flex min-h-screen flex-1 flex-col">
        {/* Top greeting bar */}
        <header className="flex items-center justify-between border-b border-[#1a3a5c]/40 bg-[#070f1e]/80 px-6 py-4 backdrop-blur">
          <p className="text-sm text-slate-400">
            Welcome back,{' '}
            <span className="font-semibold text-slate-100">{playerName || 'Hunter'}</span>
          </p>
          <NotificationBell
            notifications={notifications || { items: [], unseen_count: 0 }}
            onMarkSeen={markNotificationsSeen}
          />
        </header>

        <main className="flex-1 px-6 py-6">
          <FlashBanner flashMessage={flashMessage} />
          {children}
        </main>
      </div>
    </div>
  );
}
