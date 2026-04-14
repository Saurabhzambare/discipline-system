import ContinueButton from './ContinueButton';
import PathDiscoveryLayout from './PathDiscoveryLayout';
import PathIcon from './PathIcon';
import { getPathMeta } from '../../data/pathDiscoveryData';

export default function CommitmentScreen({ pathCode, onConfirm, saving, error }) {
  const path = getPathMeta(pathCode);
  if (!path) return null;

  return (
    <PathDiscoveryLayout className="flex items-center justify-center">
      <div className="w-full max-w-xl text-center">
        <div
          className="mx-auto mb-10 flex h-28 w-28 items-center justify-center rounded-full bg-[#111119]"
          style={{ boxShadow: `0 0 30px ${path.color.accent}66` }}
        >
          <PathIcon pathCode={path.code} color={path.color.accent} className="h-14 w-14" />
        </div>

        <p className="text-[42px] leading-tight mb-10">{path.commitmentMessage.replace(/\n/g, ' ')}</p>

        {error && <p className="mb-4 text-sm text-rose-300">{error}</p>}

        <div className="max-w-sm mx-auto">
          <ContinueButton
            onClick={onConfirm}
            disabled={saving}
            style={{ backgroundColor: path.color.accent, color: '#fff' }}
          >
            {saving ? 'Saving your path...' : 'Begin My Journey'}
          </ContinueButton>
        </div>
      </div>
    </PathDiscoveryLayout>
  );
}
