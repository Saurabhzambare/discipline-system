export default function ContinueButton({ children, onClick, disabled, variant = 'solid', className = '', style = {} }) {
  const base = 'w-full min-h-11 rounded-xl font-semibold transition duration-300';
  const byVariant =
    variant === 'ghost'
      ? 'border border-[#2A2A3A] bg-transparent text-[#E8E8ED] hover:shadow-[0_0_14px_rgba(255,255,255,0.12)]'
      : 'border border-transparent bg-[#E8E8ED] text-[#0A0A0F] hover:opacity-90';

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      style={style}
      className={`${base} ${byVariant} ${className} disabled:opacity-50 disabled:cursor-not-allowed`}
    >
      {children}
    </button>
  );
}
