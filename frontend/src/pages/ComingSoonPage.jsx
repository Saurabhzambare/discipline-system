const FEATURES = [
  {
    category: 'Social',
    items: [
      {
        title: 'Global Leaderboard',
        desc: 'Compete with every hunter on the platform. Weekly and all-time rankings.',
        status: 'soon',
      },
      {
        title: 'Guild System',
        desc: 'Form guilds with your squad, set shared goals, and track group progress.',
        status: 'soon',
      },
      {
        title: 'Challenges & Duels',
        desc: 'Challenge friends to head-to-head quest battles with custom stakes.',
        status: 'planned',
      },
    ],
  },
  {
    category: 'Progression',
    items: [
      {
        title: 'Achievement Badges',
        desc: 'Unlock rare badges for milestone completions, streaks, and special events.',
        status: 'soon',
      },
      {
        title: 'Prestige System',
        desc: 'Reset your level for a prestige rank and exclusive cosmetics at max level.',
        status: 'planned',
      },
      {
        title: 'Custom Quest Creator',
        desc: 'Build your own quests tailored to your personal goals and schedule.',
        status: 'soon',
      },
    ],
  },
  {
    category: 'Mobile & Integration',
    items: [
      {
        title: 'iOS & Android App',
        desc: 'Native mobile apps with push notifications for daily quest reminders.',
        status: 'building',
      },
      {
        title: 'Strava & Garmin Sync',
        desc: 'Auto-complete running quests by syncing your fitness tracker data.',
        status: 'planned',
      },
      {
        title: 'Apple Health & Google Fit',
        desc: 'Pull step count, sleep, and workout data directly into your quests.',
        status: 'planned',
      },
    ],
  },
  {
    category: 'Discipline Tools',
    items: [
      {
        title: 'Habit Streaks Calendar',
        desc: 'Visual monthly calendar showing your complete vs missed days at a glance.',
        status: 'building',
      },
      {
        title: 'AI Quest Coach',
        desc: 'Personalised quest recommendations and progress analysis powered by AI.',
        status: 'planned',
      },
      {
        title: 'Weekly Report Cards',
        desc: 'Email digest with your week in numbers — quests, EXP, streaks, comparisons.',
        status: 'soon',
      },
    ],
  },
];

const STATUS_CONFIG = {
  building: {
    label: 'Building Now',
    className: 'border-cyan-500/50 bg-cyan-500/10 text-cyan-300',
    dot: 'bg-cyan-400',
  },
  soon: {
    label: 'Coming Soon',
    className: 'border-amber-500/50 bg-amber-500/10 text-amber-300',
    dot: 'bg-amber-400',
  },
  planned: {
    label: 'Planned',
    className: 'border-slate-600/60 bg-slate-800/40 text-slate-400',
    dot: 'bg-slate-500',
  },
};

function FeatureCard({ title, desc, status }) {
  const cfg = STATUS_CONFIG[status];
  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-5 transition hover:border-[#2a4a6c]">
      <div className="mb-3 flex items-start justify-between gap-3">
        <p className="text-sm font-semibold text-slate-100">{title}</p>
        <span className={`flex-shrink-0 flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-[10px] font-semibold ${cfg.className}`}>
          <span className={`h-1.5 w-1.5 rounded-full ${cfg.dot}`} />
          {cfg.label}
        </span>
      </div>
      <p className="text-xs text-slate-500 leading-relaxed">{desc}</p>
    </div>
  );
}

export default function ComingSoonPage({ onNavigate }) {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="relative overflow-hidden rounded-2xl border border-[#1a3a5c] bg-gradient-to-br from-[#0a1628] to-[#071020] p-7 text-center shadow-[0_0_40px_rgba(6,182,212,0.07)]">
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />
        <p className="text-[10px] uppercase tracking-[0.3em] text-cyan-400/70">Roadmap</p>
        <h1 className="mt-2 text-3xl font-black text-slate-100">What's Coming Next</h1>
        <p className="mt-3 text-sm text-slate-400 max-w-lg mx-auto">
          The Discipline System is constantly evolving. Here's what we're building and what's on the horizon.
        </p>

        {/* Status legend */}
        <div className="mt-5 flex flex-wrap items-center justify-center gap-3">
          {Object.entries(STATUS_CONFIG).map(([key, cfg]) => (
            <span key={key} className={`flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium ${cfg.className}`}>
              <span className={`h-1.5 w-1.5 rounded-full ${cfg.dot}`} />
              {cfg.label}
            </span>
          ))}
        </div>
      </div>

      {/* Feature sections */}
      {FEATURES.map((section) => (
        <div key={section.category}>
          <p className="mb-3 text-[10px] uppercase tracking-[0.25em] text-slate-500">{section.category}</p>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {section.items.map((item) => (
              <FeatureCard key={item.title} {...item} />
            ))}
          </div>
        </div>
      ))}

      {/* CTA */}
      <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-6 text-center">
        <p className="text-sm font-semibold text-slate-200">Have a feature idea?</p>
        <p className="mt-1 text-xs text-slate-500">
          We build what hunters actually need. Share your ideas with the community.
        </p>
        <button
          type="button"
          onClick={() => onNavigate('/feed')}
          className="mt-4 rounded-xl border border-cyan-500/60 bg-cyan-500/15 px-6 py-2.5 text-sm font-semibold text-cyan-200 transition hover:bg-cyan-500/25"
        >
          Post in the Feed →
        </button>
      </div>
    </div>
  );
}
