import { useState } from 'react';
import AuthCard from '../components/AuthCard';

export default function LoginPage({ onLogin, onNavigate }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      await onLogin(username, password);
    } catch (submitError) {
      setError(submitError.message || 'Login failed.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-[calc(100vh-10rem)] items-center justify-center">
      <AuthCard
        title="Enter the Gate"
        subtitle="Sign in to continue your progression journey."
        footer={
          <>
            New hunter?{' '}
            <button
              type="button"
              onClick={() => onNavigate('/signup')}
              className="font-medium text-cyan-300 hover:text-cyan-200"
            >
              Create account
            </button>
          </>
        }
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block space-y-1">
            <span className="text-sm text-slate-300">Username</span>
            <input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 outline-none ring-cyan-400/40 transition focus:ring"
            />
          </label>
          <label className="block space-y-1">
            <span className="text-sm text-slate-300">Password</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 outline-none ring-cyan-400/40 transition focus:ring"
            />
          </label>

          {error ? <p className="text-sm text-rose-300">{error}</p> : null}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg border border-cyan-500/70 bg-cyan-500/20 px-4 py-2 font-semibold text-cyan-200 transition hover:bg-cyan-500/30 disabled:cursor-not-allowed disabled:border-slate-700 disabled:bg-slate-800 disabled:text-slate-500"
          >
            {loading ? 'Signing in...' : 'Login'}
          </button>
        </form>
      </AuthCard>
    </div>
  );
}
