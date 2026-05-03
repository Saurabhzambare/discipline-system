function formatDate(isoString) {
  if (!isoString) return '';
  const d = new Date(isoString);
  if (Number.isNaN(d.getTime())) return '';
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
}

function isHidden(fieldKey, hiddenFields, summary) {
  if (Array.isArray(hiddenFields) && hiddenFields.includes(fieldKey)) return true;
  if (!summary) return true;
  return summary[fieldKey] === null || summary[fieldKey] === undefined;
}

function StatRow({ label, value }) {
  return (
    <div className="flex items-baseline justify-between gap-3 py-1.5 text-xs">
      <span className="text-slate-500">{label}</span>
      <span className="font-medium text-slate-200 text-right truncate max-w-[60%]">{value}</span>
    </div>
  );
}

function PrivateNote({ children }) {
  return (
    <p className="mt-2 rounded-md border border-[#1a3a5c]/60 bg-[#060d1a] px-2 py-1.5 text-[11px] italic text-slate-500">
      {children}
    </p>
  );
}

function FitnessCard({ summary }) {
  const s = summary || {};
  return (
    <div className="space-y-0">
      {s.training_split != null && <StatRow label="Training Split" value={String(s.training_split)} />}
      {s.primary_goal != null && <StatRow label="Primary Goal" value={String(s.primary_goal)} />}
      {s.current_split != null && <StatRow label="Current Split" value={String(s.current_split)} />}
      {s.completed_quests != null && <StatRow label="Completed Quests" value={s.completed_quests} />}
    </div>
  );
}

function MindsetCard({ summary, hiddenFields }) {
  const s = summary || {};
  const darkNightHidden = isHidden('dark_night_count', hiddenFields, s);
  return (
    <div className="space-y-0">
      {s.archetype != null && <StatRow label="Archetype" value={String(s.archetype)} />}
      {s.wisdom_log_count != null && <StatRow label="Wisdom Logs" value={s.wisdom_log_count} />}
      {s.freedom_token_count != null && <StatRow label="Freedom Tokens" value={s.freedom_token_count} />}
      {!darkNightHidden && s.dark_night_count != null ? (
        <StatRow label="Dark Night Count" value={s.dark_night_count} />
      ) : (
        <PrivateNote>Dark Night progress is private.</PrivateNote>
      )}
    </div>
  );
}

function HealthCard({ summary }) {
  const s = summary || {};
  return (
    <div className="space-y-0">
      {s.elixir_level != null && <StatRow label="Elixir Level" value={String(s.elixir_level)} />}
      {s.brews_completed != null && <StatRow label="Brews Completed" value={s.brews_completed} />}
      {s.fill_days != null && <StatRow label="Fill Days" value={s.fill_days} />}
      {s.mercy_retained_fill_days != null && <StatRow label="Mercy-Retained Days" value={s.mercy_retained_fill_days} />}
      {s.body_journal_count != null && <StatRow label="Body Journal Entries" value={s.body_journal_count} />}
      {s.transmutation_milestone_count != null && <StatRow label="Transmutation Milestones" value={s.transmutation_milestone_count} />}
      {s.latest_transmutation != null && <StatRow label="Latest Transmutation" value={String(s.latest_transmutation)} />}
    </div>
  );
}

function DisciplineCard({ summary, hiddenFields }) {
  const s = summary || {};
  const codeHidden = isHidden('discipline_code', hiddenFields, s);
  return (
    <div className="space-y-0">
      {s.armor_piece_count != null && <StatRow label="Armor Pieces" value={s.armor_piece_count} />}
      {s.total_cracks != null && <StatRow label="Total Cracks" value={s.total_cracks} />}
      {s.grace_token_count != null && <StatRow label="Grace Tokens" value={s.grace_token_count} />}
      {s.streak_shields_available != null && <StatRow label="Streak Shields" value={s.streak_shields_available} />}
      {!codeHidden && Array.isArray(s.discipline_code) && s.discipline_code.length > 0 ? (
        <div className="mt-2">
          <p className="mb-1 text-[10px] uppercase tracking-wide text-slate-500">Discipline Code</p>
          <ul className="list-disc space-y-0.5 pl-4 text-xs text-slate-300">
            {s.discipline_code.map((rule, idx) => (
              <li key={idx}>{typeof rule === 'string' ? rule : rule?.text || JSON.stringify(rule)}</li>
            ))}
          </ul>
        </div>
      ) : codeHidden ? (
        <PrivateNote>Discipline Code is private.</PrivateNote>
      ) : null}
    </div>
  );
}

function GrindCard({ summary, hiddenFields }) {
  const s = summary || {};
  const goalHidden = isHidden('singular_goal', hiddenFields, s);
  return (
    <div className="space-y-0">
      {s.xp_multiplier != null && <StatRow label="XP Multiplier" value={`×${Number(s.xp_multiplier).toFixed(2)}`} />}
      {!goalHidden && s.singular_goal ? (
        <StatRow label="Singular Goal" value={String(s.singular_goal)} />
      ) : goalHidden ? (
        <PrivateNote>Singular Goal is private.</PrivateNote>
      ) : null}
      {s.total_skill_nodes != null && (
        <StatRow
          label="Skill Nodes"
          value={`${s.unlocked_skill_nodes ?? 0} / ${s.total_skill_nodes}`}
        />
      )}
      {s.current_skill_node != null && <StatRow label="Current Skill Node" value={String(s.current_skill_node)} />}
      {s.public_output_log_count != null && <StatRow label="Public Output Logs" value={s.public_output_log_count} />}
      {s.has_accountability_partner != null && (
        <StatRow label="Accountability Partner" value={s.has_accountability_partner ? 'Yes' : 'No'} />
      )}
    </div>
  );
}

const PATH_RENDERERS = {
  fitness_warrior: FitnessCard,
  mindset_sage: MindsetCard,
  health_alchemist: HealthCard,
  discipline_knight: DisciplineCard,
  grind_visionary: GrindCard,
};

const PATH_ACCENT = {
  fitness_warrior: 'border-orange-500/30',
  mindset_sage: 'border-purple-500/30',
  health_alchemist: 'border-emerald-500/30',
  discipline_knight: 'border-cyan-500/30',
  grind_visionary: 'border-amber-500/30',
};

export function PathProfileCards({ pathProfiles }) {
  const items = Array.isArray(pathProfiles) ? pathProfiles : [];

  if (items.length === 0) {
    return (
      <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4 text-center">
        <p className="text-xs text-slate-500">No active path profile data yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {items.map((item) => {
        const Renderer = PATH_RENDERERS[item.path];
        const accent = PATH_ACCENT[item.path] || 'border-[#1a3a5c]';
        const hiddenFields = item.visibility?.hidden_fields || [];
        return (
          <div
            key={item.path}
            className={`rounded-xl border ${accent} bg-[#0a1628] p-4 shadow-[0_0_20px_rgba(6,182,212,0.04)]`}
          >
            <div className="mb-2 flex items-center justify-between">
              <p className="text-sm font-semibold text-slate-100">{item.path_label || item.path}</p>
              {item.visibility?.is_own_profile === false && (
                <span className="rounded-full border border-[#1a3a5c] bg-[#060d1a] px-2 py-0.5 text-[9px] uppercase tracking-wide text-slate-500">
                  Public View
                </span>
              )}
            </div>
            {Renderer ? (
              <Renderer summary={item.summary} hiddenFields={hiddenFields} />
            ) : (
              <p className="text-xs text-slate-500">No summary available.</p>
            )}
          </div>
        );
      })}
    </div>
  );
}

export function BadgeSection({ badges }) {
  const data = badges || { count: 0, recent: [], titles: [] };
  const titles = Array.isArray(data.titles) ? data.titles : [];
  const recent = Array.isArray(data.recent) ? data.recent : [];
  const count = data.count ?? 0;

  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm font-semibold text-slate-100">Titles & Badges</p>
        <span className="rounded-full border border-amber-500/40 bg-amber-500/10 px-2 py-0.5 text-[10px] font-bold text-amber-300">
          Total Badges: {count}
        </span>
      </div>

      <div>
        <p className="mb-2 text-[10px] uppercase tracking-wide text-purple-300/80">Titles</p>
        {titles.length === 0 ? (
          <p className="text-xs text-slate-500">No cross-path titles unlocked yet.</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {titles.map((t) => (
              <span
                key={t.key}
                title={t.description || ''}
                className="rounded-full border border-purple-500/50 bg-gradient-to-r from-purple-500/15 to-fuchsia-500/15 px-3 py-1 text-xs font-semibold text-purple-200 shadow-[0_0_12px_rgba(168,85,247,0.15)]"
              >
                ★ {t.name}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="mt-4">
        <p className="mb-2 text-[10px] uppercase tracking-wide text-cyan-300/80">Recent Badges</p>
        {recent.length === 0 ? (
          <p className="text-xs text-slate-500">No recent badges yet.</p>
        ) : (
          <ul className="space-y-1.5">
            {recent.map((b) => (
              <li
                key={b.key}
                className="flex items-center justify-between rounded-md border border-[#1a3a5c]/60 bg-[#060d1a] px-2.5 py-1.5"
              >
                <div className="min-w-0">
                  <p className="truncate text-xs font-medium text-slate-200">{b.name}</p>
                  {b.description ? (
                    <p className="truncate text-[10px] text-slate-500">{b.description}</p>
                  ) : null}
                </div>
                <div className="flex flex-shrink-0 items-center gap-2">
                  {b.tier ? (
                    <span className="rounded-full border border-cyan-500/40 bg-cyan-500/10 px-2 py-0.5 text-[9px] uppercase tracking-wide text-cyan-300">
                      {b.tier}
                    </span>
                  ) : null}
                  <span className="text-[10px] text-slate-600">{formatDate(b.earned_at)}</span>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export function AchievementCards({ cards }) {
  const items = Array.isArray(cards) ? cards : [];

  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
      <p className="mb-3 text-sm font-semibold text-slate-100">Achievement Cards</p>
      {items.length === 0 ? (
        <p className="text-xs text-slate-500">No achievement cards yet.</p>
      ) : (
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          {items.map((card) => (
            <div
              key={card.id}
              className="rounded-lg border border-amber-500/30 bg-gradient-to-br from-[#060d1a] to-[#0a1628] p-3 shadow-[0_0_16px_rgba(245,158,11,0.06)]"
            >
              <div className="flex items-start justify-between gap-2">
                <p className="text-sm font-semibold text-amber-300">{card.title}</p>
                {card.card_type ? (
                  <span className="rounded-full border border-amber-500/40 bg-amber-500/10 px-2 py-0.5 text-[9px] uppercase tracking-wide text-amber-300">
                    {card.card_type}
                  </span>
                ) : null}
              </div>
              {card.subtitle ? (
                <p className="mt-1 text-xs text-slate-400">{card.subtitle}</p>
              ) : null}
              <p className="mt-2 text-[10px] text-slate-600">{formatDate(card.earned_at)}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
