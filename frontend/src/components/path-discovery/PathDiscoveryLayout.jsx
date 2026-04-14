export default function PathDiscoveryLayout({ children, className = '' }) {
  return (
    <div
      className={`min-h-screen bg-[#0A0A0F] text-[#E8E8ED] px-6 py-8 md:py-12 ${className}`}
      style={{ paddingBottom: 'max(2rem, env(safe-area-inset-bottom))' }}
    >
      {children}
    </div>
  );
}
