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
    <div className="flex min-h-[calc(100vh-10rem)] items-center justify-center">
      <AuthCard
        title="Awaken Your Profile"
        subtitle="Create your account and start building your streak."
        footer={
          <>
            Already registered?{' '}
            <button
              type="button"
              onClick={() => onNavigate('/login')}
              className="font-medium text-cyan-300 hover:text-cyan-200"
              disabled={loading}
            >
              Go to login
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
              minLength={3}
              required
              disabled={loading}
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 outline-none ring-cyan-400/40 transition focus:ring disabled:opacity-70"
            />
          </label>

          <label className="block space-y-1">
            <span className="text-sm text-slate-300">Password</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              minLength={8}
              required
              disabled={loading}
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 outline-none ring-cyan-400/40 transition focus:ring disabled:opacity-70"
            />
          </label>

          {error ? <p className="text-sm text-rose-300">{error}</p> : null}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg border border-cyan-500/70 bg-cyan-500/20 px-4 py-2 font-semibold text-cyan-200 transition hover:bg-cyan-500/30 disabled:cursor-not-allowed disabled:border-slate-700 disabled:bg-slate-800 disabled:text-slate-500"
          >
            {loading ? 'Creating account...' : 'Signup'}
          </button>
        </form>
      </AuthCard>
    </div>
  );
}
