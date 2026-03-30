export default function AuthCard({ title, subtitle, children, footer }) {
  return (
    <div className="w-full max-w-md rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-8 shadow-[0_0_60px_rgba(6,182,212,0.08)]">
      {/* Top glow line */}
      <div className="mb-6 h-px bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent" />
      <h1 className="text-2xl font-bold text-slate-100">{title}</h1>
      <p className="mt-2 text-sm text-slate-500">{subtitle}</p>
      <div className="mt-6 space-y-4">{children}</div>
      {footer ? <div className="mt-5 text-sm text-slate-500">{footer}</div> : null}
    </div>
  );
}
