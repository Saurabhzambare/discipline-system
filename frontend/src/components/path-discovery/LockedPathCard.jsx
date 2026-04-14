import PathIcon from './PathIcon';

export default function LockedPathCard({ onTap }) {
  return (
    <button
      type="button"
      onClick={onTap}
      className="w-full rounded-2xl border border-[#2A2A3A] bg-[#111119] p-8 text-center opacity-60"
    >
      <div className="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-full border border-[#2A2A3A]">
        <PathIcon pathCode="locked" color="#6B6B7B" className="h-7 w-7" />
      </div>
      <p className="text-lg font-semibold text-[#A0A0AE]">Coming Soon</p>
    </button>
  );
}
