import ContinueButton from './ContinueButton';
import PathDiscoveryLayout from './PathDiscoveryLayout';
import { WELCOME_LINES } from '../../data/pathDiscoveryData';

export default function WelcomeScreen({ onStart, loading }) {
  return (
    <PathDiscoveryLayout className="flex items-center justify-center">
      <div className="w-full max-w-xl text-center">
        <p className="text-4xl leading-tight font-semibold">
          {WELCOME_LINES[0]}
        </p>
        <p className="mt-9 text-2xl text-[#6B6B7B]">{WELCOME_LINES[1]}</p>

        <div className="mt-14 max-w-sm mx-auto">
          <ContinueButton onClick={onStart} disabled={loading} variant="ghost">
            {loading ? 'Preparing...' : 'Begin'}
          </ContinueButton>
        </div>
      </div>
    </PathDiscoveryLayout>
  );
}
