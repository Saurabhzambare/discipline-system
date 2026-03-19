export default function AuthCard({ title, subtitle, children, footer }) {
  return (
    <div className="w-full max-w-md rounded-2xl border border-slate-700/80 bg-slate-900/80 p-8 shadow-[0_10px_40px_rgba(0,0,0,0.35)] backdrop-blur-sm">
      <h1 className="text-2xl font-bold text-slate-100">{title}</h1>
      <p className="mt-2 text-sm text-slate-400">{subtitle}</p>
      <div className="mt-6 space-y-4">{children}</div>
      {footer ? <div className="mt-5 text-sm text-slate-400">{footer}</div> : null}
    </div>
  );
}
