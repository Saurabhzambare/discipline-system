import ContinueButton from './ContinueButton';
import PathDiscoveryLayout from './PathDiscoveryLayout';
import PathMatchRow from './PathMatchRow';
import { getPathMeta } from '../../data/pathDiscoveryData';

export default function ResultsScreen({ results, onExplore }) {
  const top = results[0];
  const topPath = top ? getPathMeta(top.path_code) : null;

  return (
    <PathDiscoveryLayout className="flex items-center justify-center">
      <div className="w-full max-w-xl">
        <h2 className="text-center text-[52px] leading-tight font-semibold mb-8" style={{ color: topPath?.color?.accent || '#E8E8ED' }}>
          {topPath?.resultsOpener}
        </h2>

        <div className="space-y-3">
          {results.map((result, idx) => (
            <PathMatchRow key={result.path_code} result={result} top={idx === 0} />
          ))}
        </div>

        <p className="mt-8 text-center text-[#6B6B7B]">Your strongest match is highlighted. Explore all paths before choosing.</p>

        <div className="mt-6">
          <ContinueButton onClick={onExplore}>Explore Your Paths</ContinueButton>
        </div>
      </div>
    </PathDiscoveryLayout>
  );
}
