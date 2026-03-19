export default function ProgressCard({ label, value, tone = 'blue' }) {
  const toneClass = {
    blue: 'border-cyan-400/50 text-cyan-300',
    gold: 'border-amber-400/50 text-amber-300',
    green: 'border-emerald-400/50 text-emerald-300',
  }[tone];

  return (
    <div className={`rounded-xl border bg-slate-900/60 p-4 ${toneClass}`}>
      <p className="text-xs uppercase tracking-wide text-slate-400">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-slate-100">{value}</p>
    </div>
  );
}
