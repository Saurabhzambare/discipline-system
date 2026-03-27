import { useState } from 'react';
import AuthCard from '../components/AuthCard';

export default function SignupPage({ onSignup, onNavigate }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      await onSignup(username, password);
      onNavigate('/login');
    } catch (submitError) {
      setError(submitError.message || 'Signup failed.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#050d1a] px-4">
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(ellipse_at_50%_20%,rgba(6,182,212,0.06)_0%,transparent_60%)]" />

      <AuthCard
        title="Awaken Your Profile"
        subtitle="Create your account and start building your streak."
        footer={
          <>
            Already registered?{' '}
            <button
              type="button"
              onClick={() => onNavigate('/login')}
              className="font-medium text-cyan-400 hover:text-cyan-300"
              disabled={loading}
            >
              Go to login
            </button>
          </>
        }
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block space-y-1.5">
            <span className="text-xs uppercase tracking-wide text-slate-500">Username</span>
            <input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              minLength={3}
              required
              disabled={loading}
              className="w-full rounded-lg border border-[#1a3a5c] bg-[#06101e] px-3 py-2.5 text-sm text-slate-100 outline-none ring-cyan-400/30 transition focus:ring disabled:opacity-70"
            />
          </label>
          <label className="block space-y-1.5">
            <span className="text-xs uppercase tracking-wide text-slate-500">Password</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              minLength={8}
              required
              disabled={loading}
              className="w-full rounded-lg border border-[#1a3a5c] bg-[#06101e] px-3 py-2.5 text-sm text-slate-100 outline-none ring-cyan-400/30 transition focus:ring disabled:opacity-70"
            />
          </label>

          {error ? <p className="text-sm text-rose-400">{error}</p> : null}

          <button
            type="submit"
            disabled={loading}
            className="mt-2 w-full rounded-lg border border-cyan-500/60 bg-cyan-500/15 px-4 py-2.5 font-semibold text-cyan-200 transition hover:bg-cyan-500/25 disabled:cursor-not-allowed disabled:border-slate-700 disabled:bg-slate-800 disabled:text-slate-500"
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>
      </AuthCard>
    </div>
  );
}
