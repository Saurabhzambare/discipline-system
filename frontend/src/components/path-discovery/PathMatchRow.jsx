import PathIcon from './PathIcon';
import { getPathMeta } from '../../data/pathDiscoveryData';

export default function PathMatchRow({ result, top }) {
  const path = getPathMeta(result.path_code);
  if (!path) return null;

  return (
    <div
      className={`rounded-xl border p-4 bg-[#111119] ${top ? '' : 'border-[#2A2A3A]'}`}
      style={
        top
          ? {
              borderColor: path.color.accent,
              boxShadow: `0 0 20px ${path.color.accent}4d`,
            }
          : undefined
      }
    >
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <PathIcon pathCode={path.code} color={path.color.accent} className="h-5 w-5" />
          <span className="font-semibold text-lg">{path.name}</span>
        </div>
        <span className="font-semibold">{result.match_percentage}%</span>
      </div>
      <div className="mt-3 h-1.5 rounded-full bg-[#2A2A3A] overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{ width: `${result.match_percentage}%`, backgroundColor: path.color.accent }}
        />
      </div>
    </div>
  );
}
