export default function Layout({ children, onNavigate, isAuthenticated, onLogout }) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-950/90 backdrop-blur">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
          <button
            type="button"
            onClick={() => onNavigate(isAuthenticated ? '/dashboard' : '/login')}
            className="text-left"
          >
            <p className="text-xs uppercase tracking-[0.25em] text-cyan-300">Discipline System</p>
            <p className="text-sm text-slate-400">Solo Leveling-inspired progression app</p>
          </button>
          {isAuthenticated ? (
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => onNavigate('/profile')}
                className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 hover:border-cyan-500/50 hover:text-cyan-200"
              >
                Profile
              </button>
              <button
                type="button"
                onClick={onLogout}
                className="rounded-lg border border-rose-500/40 bg-rose-500/10 px-3 py-2 text-sm text-rose-200 hover:bg-rose-500/20"
              >
                Logout
              </button>
            </div>
          ) : null}
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6">{children}</main>
    </div>
  );
}
