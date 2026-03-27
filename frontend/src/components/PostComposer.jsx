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
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-5">
      <h2 className="text-sm font-semibold text-slate-200">Share an Update</h2>
      <form className="mt-3 space-y-3" onSubmit={handleSubmit}>
        <textarea
          value={content}
          onChange={(event) => {
            setContent(event.target.value);
            if (submitError) setSubmitError('');
          }}
          disabled={submitting}
          rows={3}
          placeholder="What did you accomplish today?"
          className="w-full rounded-lg border border-[#1a3a5c] bg-[#06101e] px-3 py-2.5 text-sm text-slate-100 outline-none ring-cyan-400/20 transition focus:ring disabled:opacity-70 placeholder:text-slate-600"
        />

        <div className="flex items-center gap-3">
          <select
            value={visibility}
            onChange={(event) => setVisibility(event.target.value)}
            disabled={submitting}
            className="rounded-lg border border-[#1a3a5c] bg-[#06101e] px-3 py-2 text-xs text-slate-300 outline-none ring-cyan-400/20 transition focus:ring disabled:opacity-70"
          >
            {VISIBILITY_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>

          <button
            type="submit"
            disabled={!canSubmit}
            className="ml-auto rounded-lg border border-cyan-500/50 bg-cyan-500/15 px-4 py-2 text-sm font-medium text-cyan-200 transition hover:bg-cyan-500/25 disabled:cursor-not-allowed disabled:border-[#1a3a5c] disabled:bg-transparent disabled:text-slate-600"
          >
            {submitting ? 'Posting...' : 'Post'}
          </button>
        </div>

        {submitError ? <p className="text-sm text-rose-400">{submitError}</p> : null}
      </form>
    </div>
  );
}
