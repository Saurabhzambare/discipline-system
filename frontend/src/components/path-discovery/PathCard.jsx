import ContinueButton from './ContinueButton';
import PathIcon from './PathIcon';

export default function PathCard({ path, matchPct, onChoose }) {
  const sectionLabelClass = 'text-xs uppercase tracking-[0.18em] text-[#6B6B7B] mb-2';

  return (
    <article
      className="rounded-2xl border bg-[#111119] p-5"
      style={{ borderColor: `${path.color.accent}66` }}
    >
      <div className="flex items-start justify-between gap-3 mb-4">
        <div className="flex items-center gap-3">
          <PathIcon pathCode={path.code} color={path.color.accent} className="h-6 w-6" />
          <h3 className="text-2xl font-semibold">{path.name}</h3>
        </div>
        <span className="rounded-full px-3 py-1 text-xs font-semibold text-white" style={{ backgroundColor: path.color.accent }}>
          {matchPct}% match
        </span>
      </div>

      <section className="mb-4">
        <p className={sectionLabelClass}>Who you are now</p>
        <p className="text-[#D8D8DF]">{path.whoYouAreNow}</p>
      </section>

      <section className="mb-4">
        <p className={sectionLabelClass}>Who you become</p>
        <p className="text-[#D8D8DF]">{path.whoYouBecome}</p>
      </section>

      <section className="mb-4">
        <p className={sectionLabelClass}>What you gain</p>
        <ul className="list-disc pl-5 text-[#D8D8DF] space-y-1">
          {path.whatYouGain.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>

      <section className="mb-6">
        <p className={sectionLabelClass}>This path is for you</p>
        <p className="text-[#D8D8DF]">{path.thisPathIsForYouIf}</p>
      </section>

      <ContinueButton
        onClick={() => onChoose(path.code)}
        style={{ backgroundColor: path.color.accent, color: '#fff' }}
      >
        Choose {path.name}
      </ContinueButton>
    </article>
  );
}
