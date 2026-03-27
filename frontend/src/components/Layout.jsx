import { useEffect } from 'react';

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

export default function Layout({
  children,
  onNavigate,
  isAuthenticated,
  onLogout,
  flashMessage,
  onDismissFlash,
  route,
  playerName,
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
            return (
              <button
                key={item.path}
                type="button"
                onClick={() => onNavigate(item.path)}
                title={item.label}
                className={`flex flex-col items-center gap-1 rounded-xl px-2 py-3 text-[10px] font-medium transition w-14 ${
                  active
                    ? 'border border-cyan-500/50 bg-cyan-500/10 text-cyan-300 shadow-[0_0_12px_rgba(6,182,212,0.15)]'
                    : 'border border-transparent text-slate-500 hover:border-[#1a3a5c] hover:text-slate-300'
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
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
        <header className="border-b border-[#1a3a5c]/40 bg-[#070f1e]/80 px-6 py-4 backdrop-blur">
          <p className="text-sm text-slate-400">
            Welcome back,{' '}
            <span className="font-semibold text-slate-100">{playerName || 'Hunter'}</span>
          </p>
        </header>

        <main className="flex-1 px-6 py-6">
          <FlashBanner flashMessage={flashMessage} />
          {children}
        </main>
      </div>
    </div>
  );
}
