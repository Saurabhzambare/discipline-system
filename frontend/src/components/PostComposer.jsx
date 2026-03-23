import { useState } from 'react';

const VISIBILITY_OPTIONS = [
  { value: 'public', label: 'Public' },
  { value: 'friends_only', label: 'Friends only' },
];

export default function PostComposer({ onCreatePost }) {
  const [content, setContent] = useState('');
  const [visibility, setVisibility] = useState('public');
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');

  const canSubmit = content.trim().length > 0 && !submitting;

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmedContent = content.trim();
    if (!trimmedContent) {
      setSubmitError('Please write something before posting.');
      return;
    }

    setSubmitting(true);
    setSubmitError('');

    try {
      await onCreatePost({ content: trimmedContent, visibility });
      setContent('');
      setVisibility('public');
    } catch (error) {
      setSubmitError(error.message || 'Could not create post.');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-5">
      <h2 className="text-lg font-semibold text-slate-100">Create Post</h2>
      <p className="mt-1 text-sm text-slate-400">Share an update with the community.</p>

      <form className="mt-4 space-y-4" onSubmit={handleSubmit}>
        <label className="block space-y-1">
          <span className="text-sm text-slate-300">Content</span>
          <textarea
            value={content}
            onChange={(event) => {
              setContent(event.target.value);
              if (submitError) setSubmitError('');
            }}
            disabled={submitting}
            rows={4}
            placeholder="What did you accomplish today?"
            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none ring-cyan-400/40 transition focus:ring disabled:opacity-70"
          />
        </label>

        <label className="block space-y-1">
          <span className="text-sm text-slate-300">Visibility</span>
          <select
            value={visibility}
            onChange={(event) => {
              setVisibility(event.target.value);
              if (submitError) setSubmitError('');
            }}
            disabled={submitting}
            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none ring-cyan-400/40 transition focus:ring disabled:opacity-70"
          >
            {VISIBILITY_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        {submitError ? <p className="text-sm text-rose-300">{submitError}</p> : null}

        <button
          type="submit"
          disabled={!canSubmit}
          className="rounded-lg border border-cyan-500/60 bg-cyan-500/20 px-4 py-2 text-sm font-medium text-cyan-200 transition hover:bg-cyan-500/30 disabled:cursor-not-allowed disabled:border-slate-700 disabled:bg-slate-800 disabled:text-slate-500"
        >
          {submitting ? 'Posting...' : 'Post'}
        </button>
      </form>
    </section>
  );
}
