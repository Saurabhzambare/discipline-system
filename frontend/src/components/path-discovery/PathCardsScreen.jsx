import { useMemo, useState } from 'react';
import PathDiscoveryLayout from './PathDiscoveryLayout';
import PathCard from './PathCard';
import LockedPathCard from './LockedPathCard';
import { LOCKED_PATH_TOAST, getPathMeta } from '../../data/pathDiscoveryData';

export default function PathCardsScreen({ results, onChoose }) {
  const [toast, setToast] = useState('');

  const orderedPaths = useMemo(
    () => results.map((r) => ({ path: getPathMeta(r.path_code), matchPct: r.match_percentage })).filter((row) => row.path),
    [results],
  );

  return (
    <PathDiscoveryLayout className="overflow-y-auto">
      <div className="w-full max-w-3xl mx-auto space-y-5">
        {orderedPaths.map(({ path, matchPct }) => (
          <PathCard key={path.code} path={path} matchPct={matchPct} onChoose={onChoose} />
        ))}
        <LockedPathCard
          onTap={() => {
            setToast(LOCKED_PATH_TOAST);
            setTimeout(() => setToast(''), 2200);
          }}
        />
      </div>

      {toast && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 rounded-lg border border-[#2A2A3A] bg-[#111119] px-4 py-3 text-sm text-[#D8D8DF]">
          {toast}
        </div>
      )}
    </PathDiscoveryLayout>
  );
}
