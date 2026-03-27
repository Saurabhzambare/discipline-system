/**
 * /preview — Static visual mockups for all proposed Phase 3 features.
 * Nothing here is wired to the backend. Pure UI previews.
 */

/* ── 1. Level-up overlay ─────────────────────────────────────────────────── */
function LevelUpOverlay() {
  return (
    <div className="relative flex h-64 items-center justify-center overflow-hidden rounded-2xl border border-amber-500/30 bg-[#060d1a]">
      {/* radial glow */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_50%_50%,rgba(251,191,36,0.12)_0%,transparent_70%)]" />
      {/* ring pulses */}
      <div className="absolute h-48 w-48 rounded-full border border-amber-400/20 animate-ping" />
      <div className="absolute h-36 w-36 rounded-full border border-amber-400/30" />
      {/* content */}
      <div className="relative text-center">
        <p className="text-xs uppercase tracking-[0.3em] text-amber-400/70">Level Up!</p>
        <p className="mt-1 text-7xl font-black text-amber-300">8</p>
        <p className="mt-2 text-sm text-slate-400">You have reached level 8</p>
        <button className="mt-4 rounded-lg border border-amber-500/50 bg-amber-500/15 px-6 py-2 text-sm font-semibold text-amber-200 hover:bg-amber-500/25">
          Continue ⚔️
        </button>
      </div>
    </div>
  );
}

/* ── 2. Quest completion glow effect ─────────────────────────────────────── */
function QuestGlowDemo() {
  return (
    <div className="space-y-2 rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5">
      {/* normal quest */}
      <div className="flex items-center gap-4 rounded-lg border border-[#1a3a5c] px-3 py-3">
        <div className="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded border-2 border-slate-600 bg-transparent" />
        <span className="flex-1 text-sm text-slate-300">Morning Run — 5km</span>
        <span className="text-sm font-bold text-amber-400">+30 EXP</span>
      </div>
      {/* just-completed quest with glow */}
      <div className="flex items-center gap-4 rounded-lg border border-emerald-500/50 bg-emerald-500/8 px-3 py-3 shadow-[0_0_18px_rgba(52,211,153,0.15)] transition-all">
        <div className="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded border-2 border-emerald-500/70 bg-emerald-500/20 text-emerald-300">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        </div>
        <span className="flex-1 text-sm text-emerald-300 line-through opacity-70">Drink 2L of Water</span>
        <span className="text-sm font-bold text-emerald-400/60">+20 EXP ✓</span>
      </div>
      {/* flash badge */}
      <div className="flex justify-center">
        <span className="rounded-full border border-emerald-500/40 bg-emerald-500/10 px-4 py-1 text-xs font-semibold text-emerald-300 animate-pulse">
          +20 EXP earned!
        </span>
      </div>
    </div>
  );
}

/* ── 3. Streak warning banner ────────────────────────────────────────────── */
function StreakWarning() {
  return (
    <div className="space-y-3">
      {/* warning state */}
      <div className="flex items-center gap-3 rounded-xl border border-orange-500/40 bg-orange-500/8 px-4 py-3">
        <span className="text-xl">⚠️</span>
        <div className="flex-1">
          <p className="text-sm font-semibold text-orange-300">Protect your streak!</p>
          <p className="text-xs text-orange-400/70">You still have 3 quests remaining today. Streak: 15 days 🔥</p>
        </div>
        <span className="text-xs text-orange-400/50">11:30 PM</span>
      </div>
      {/* safe state */}
      <div className="flex items-center gap-3 rounded-xl border border-emerald-500/30 bg-emerald-500/8 px-4 py-3">
        <span className="text-xl">✅</span>
        <div className="flex-1">
          <p className="text-sm font-semibold text-emerald-300">Streak secured for today!</p>
          <p className="text-xs text-emerald-400/70">All quests complete. Streak: 15 days 🔥</p>
        </div>
      </div>
    </div>
  );
}

/* ── 4. Public player profile card ───────────────────────────────────────── */
function PublicProfileCard() {
  return (
    <div className="rounded-2xl border border-[#1a3a5c] bg-[#0a1628] p-5">
      <div className="flex items-center gap-4">
        <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-cyan-500/40 bg-cyan-500/10 text-2xl font-bold text-cyan-400">
          S
        </div>
        <div className="flex-1">
          <p className="text-lg font-bold text-slate-100">saurabh</p>
          <p className="text-xs text-slate-500">Hunter ID #4</p>
          <div className="mt-1.5 flex gap-2">
            <span className="rounded-full border border-cyan-500/40 bg-cyan-500/10 px-2 py-0.5 text-xs text-cyan-300">Level 7</span>
            <span className="rounded-full border border-[#1a3a5c] px-2 py-0.5 text-xs text-slate-400">Gym Path 💪</span>
          </div>
        </div>
        <button className="rounded-lg border border-cyan-500/50 bg-cyan-500/15 px-3 py-2 text-xs font-medium text-cyan-200 hover:bg-cyan-500/25">
          Add Friend
        </button>
      </div>
      <div className="mt-4 grid grid-cols-3 gap-2">
        {[['Level', '7', 'text-cyan-300'], ['Total EXP', '680', 'text-amber-300'], ['Streak', '15🔥', 'text-orange-400']].map(([label, val, color]) => (
          <div key={label} className="rounded-lg border border-[#1a3a5c] bg-[#060d1a] p-2.5 text-center">
            <p className="text-[10px] text-slate-500">{label}</p>
            <p className={`mt-1 text-lg font-bold ${color}`}>{val}</p>
          </div>
        ))}
      </div>
      <div className="mt-4 border-t border-[#1a3a5c]/60 pt-3">
        <p className="mb-2 text-xs text-slate-500 uppercase tracking-wide">Recent Activity</p>
        {['Completed Morning Run', 'Joined group: Gym Warriors', 'Became friends with Bharati'].map((item, i) => (
          <p key={i} className="py-1 text-xs text-slate-400">· {item}</p>
        ))}
      </div>
    </div>
  );
}

/* ── 5. Share quest to feed button ───────────────────────────────────────── */
function ShareQuestDemo() {
  return (
    <div className="space-y-3">
      {/* completed quest with share option */}
      <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-4">
        <div className="flex items-center gap-3">
          <div className="flex h-6 w-6 items-center justify-center rounded border-2 border-emerald-500/60 bg-emerald-500/20 text-emerald-300">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          </div>
          <span className="flex-1 text-sm font-medium text-emerald-300 line-through opacity-70">Morning Run — 5km</span>
          <span className="text-sm font-bold text-emerald-400/60">+30 EXP</span>
        </div>
        <div className="mt-3 flex justify-end">
          <button className="flex items-center gap-1.5 rounded-lg border border-cyan-500/40 bg-cyan-500/10 px-3 py-1.5 text-xs font-medium text-cyan-300 hover:bg-cyan-500/20">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
            </svg>
            Share to Feed
          </button>
        </div>
      </div>
      {/* how it looks as a feed post */}
      <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
        <div className="flex items-center gap-2 mb-3">
          <div className="flex h-7 w-7 items-center justify-center rounded-full border border-cyan-500/30 bg-cyan-500/10 text-xs font-bold text-cyan-400">S</div>
          <div>
            <p className="text-xs font-semibold text-slate-200">saurabh</p>
            <p className="text-[10px] text-slate-600">just now</p>
          </div>
          <span className="ml-auto rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 text-[10px] text-emerald-400">⚔️ Quest Complete</span>
        </div>
        <p className="text-sm text-slate-300">Just completed <span className="font-semibold text-emerald-300">Morning Run — 5km</span> and earned <span className="font-semibold text-amber-300">+30 EXP</span> 💪</p>
      </div>
    </div>
  );
}

/* ── 6. Sidebar notification badge ──────────────────────────────────────── */
function SidebarBadgeDemo() {
  return (
    <div className="flex gap-6 items-start">
      {/* mini sidebar */}
      <div className="flex w-16 flex-col items-center gap-1 rounded-2xl border border-[#1a3a5c] bg-[#070f1e] py-4">
        {[
          { label: 'Dash', active: false, badge: null, icon: '⊞' },
          { label: 'Feed', active: false, badge: null, icon: '💬' },
          { label: 'Groups', active: false, badge: null, icon: '👥' },
          { label: 'Profile', active: true, badge: 3, icon: '👤' },
        ].map((item) => (
          <div key={item.label} className={`relative flex w-12 flex-col items-center gap-0.5 rounded-xl py-2.5 text-[10px] ${item.active ? 'border border-cyan-500/50 bg-cyan-500/10 text-cyan-300' : 'text-slate-500'}`}>
            <span className="text-base">{item.icon}</span>
            <span>{item.label}</span>
            {item.badge && (
              <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-amber-500 text-[9px] font-bold text-black">
                {item.badge}
              </span>
            )}
          </div>
        ))}
      </div>
      <div className="flex-1 rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4">
        <p className="text-xs text-slate-400">The <span className="text-amber-300 font-semibold">3</span> badge on Profile means you have 3 incoming friend requests waiting — visible from any page without needing to go to Profile first.</p>
      </div>
    </div>
  );
}

/* ── 7. Player search ────────────────────────────────────────────────────── */
function PlayerSearchDemo() {
  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4 space-y-3">
      <div className="flex gap-2">
        <input
          readOnly
          value="sau"
          className="flex-1 rounded-lg border border-cyan-500/40 bg-[#06101e] px-3 py-2 text-sm text-slate-100 outline-none"
          placeholder="Search hunters..."
        />
        <button className="rounded-lg border border-[#1a3a5c] px-3 py-2 text-xs text-slate-400">Search</button>
      </div>
      {/* results */}
      {['saurabh — Level 7', 'saumya — Level 3', 'saul — Level 12'].map((r, i) => (
        <div key={i} className="flex items-center gap-3 rounded-lg border border-[#1a3a5c] bg-[#060d1a] px-3 py-2.5">
          <div className="flex h-7 w-7 items-center justify-center rounded-full border border-[#1a3a5c] bg-[#0a1628] text-xs font-bold text-cyan-400">
            {r.charAt(0).toUpperCase()}
          </div>
          <span className="flex-1 text-sm text-slate-300">{r}</span>
          <button className="rounded border border-cyan-500/40 px-2 py-1 text-[10px] text-cyan-300 hover:bg-cyan-500/10">Add</button>
        </div>
      ))}
    </div>
  );
}

/* ── 8. Quest filters ────────────────────────────────────────────────────── */
function QuestFiltersDemo() {
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        {[['All', true], ['Fitness', false], ['Discipline', false], ['Health', false], ['Remaining', false]].map(([label, active]) => (
          <button key={label} className={`rounded-full border px-3 py-1 text-xs font-medium transition ${active ? 'border-cyan-500/60 bg-cyan-500/15 text-cyan-300' : 'border-[#1a3a5c] text-slate-500 hover:text-slate-300'}`}>
            {label}
          </button>
        ))}
      </div>
      <div className="divide-y divide-[#1a3a5c]/40 rounded-xl border border-[#1a3a5c] bg-[#0a1628]">
        {[
          { title: 'Morning Run', cat: 'Fitness', exp: 30, done: true },
          { title: 'Drink 2L Water', cat: 'Health', exp: 20, done: false },
          { title: 'Read 20 Pages', cat: 'Discipline', exp: 25, done: false },
        ].map((q) => (
          <div key={q.title} className={`flex items-center gap-3 px-4 py-3 ${q.done ? 'opacity-50' : ''}`}>
            <div className={`h-5 w-5 flex-shrink-0 rounded border-2 ${q.done ? 'border-emerald-500/60 bg-emerald-500/20' : 'border-slate-600'}`} />
            <span className="flex-1 text-sm text-slate-300">{q.title}</span>
            <span className="rounded-full border border-[#1a3a5c] px-2 py-0.5 text-[10px] text-slate-500">{q.cat}</span>
            <span className="text-sm font-bold text-amber-400">+{q.exp}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ── 9. My Groups vs Explore tabs ────────────────────────────────────────── */
function GroupTabsDemo() {
  return (
    <div className="space-y-3">
      <div className="flex gap-1 rounded-xl border border-[#1a3a5c] bg-[#070f1e] p-1">
        {['My Groups', 'Explore'].map((t, i) => (
          <button key={t} className={`flex-1 rounded-lg py-2 text-sm font-medium transition ${i === 0 ? 'bg-[#0a1628] text-slate-100' : 'text-slate-500'}`}>{t}</button>
        ))}
      </div>
      <div className="grid gap-2 sm:grid-cols-2">
        {[
          { name: 'Gym Warriors', members: 12, private: false, owner: true },
          { name: 'Morning Crew', members: 5, private: false, owner: false },
        ].map((g) => (
          <div key={g.name} className="rounded-xl border border-cyan-500/20 bg-[#0a1628] p-3">
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold text-slate-100">{g.name}</p>
              {g.owner && <span className="text-[10px] text-amber-400">Owner</span>}
            </div>
            <p className="mt-1 text-[10px] text-slate-500">{g.members} members · 🌐 Public</p>
            <button className="mt-2 w-full rounded-lg border border-cyan-500/40 bg-cyan-500/10 py-1.5 text-xs text-cyan-300">Open</button>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ── 10. Post editing ─────────────────────────────────────────────────────── */
function PostEditDemo() {
  return (
    <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4 space-y-3">
      <div className="flex items-center gap-3">
        <div className="flex h-7 w-7 items-center justify-center rounded-full border border-cyan-500/30 bg-cyan-500/10 text-xs font-bold text-cyan-400">S</div>
        <div className="flex-1">
          <p className="text-sm font-semibold text-slate-200">saurabh</p>
          <p className="text-[10px] text-slate-600">2h ago · edited</p>
        </div>
        <div className="flex gap-1">
          <button className="rounded border border-[#1a3a5c] px-2 py-1 text-[10px] text-slate-400 hover:text-slate-200">Edit</button>
          <button className="rounded border border-rose-500/30 px-2 py-1 text-[10px] text-rose-400 hover:bg-rose-500/10">Delete</button>
        </div>
      </div>
      {/* edit mode */}
      <div className="rounded-lg border border-cyan-500/30 bg-[#060d1a] p-3 space-y-2">
        <p className="text-[10px] text-cyan-400/60 uppercase tracking-wide">Editing post...</p>
        <textarea rows={2} readOnly value="Crushed my morning workout today 💪 feeling unstoppable" className="w-full bg-transparent text-sm text-slate-200 outline-none resize-none" />
        <div className="flex gap-2">
          <button className="rounded border border-cyan-500/50 bg-cyan-500/10 px-3 py-1 text-xs text-cyan-200">Save</button>
          <button className="rounded border border-[#1a3a5c] px-3 py-1 text-xs text-slate-400">Cancel</button>
        </div>
      </div>
    </div>
  );
}

/* ── Section wrapper ─────────────────────────────────────────────────────── */
function Section({ number, title, description, children }) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <span className="flex h-7 w-7 items-center justify-center rounded-full border border-cyan-500/40 bg-cyan-500/10 text-xs font-bold text-cyan-300">
          {number}
        </span>
        <div>
          <h2 className="text-base font-semibold text-slate-100">{title}</h2>
          <p className="text-xs text-slate-500">{description}</p>
        </div>
      </div>
      {children}
    </div>
  );
}

/* ── Main preview page ───────────────────────────────────────────────────── */
export default function PreviewPage() {
  return (
    <div className="mx-auto max-w-2xl space-y-10 pb-16">
      {/* Header */}
      <div className="relative overflow-hidden rounded-2xl border border-cyan-500/30 bg-[#0a1628] p-6">
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent" />
        <p className="text-[10px] uppercase tracking-[0.25em] text-cyan-400/70">Phase 3 — Feature Previews</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-100">Proposed UI Mockups</h1>
        <p className="mt-2 text-sm text-slate-500">
          These are static previews — nothing is wired to the backend yet. Review each feature and tell me which ones to build.
        </p>
      </div>

      <Section number="1" title="Level-Up Overlay" description="Full-screen celebration when you reach a new level.">
        <LevelUpOverlay />
      </Section>

      <Section number="2" title="Quest Completion Glow" description="Subtle green glow + EXP flash when a quest is checked off.">
        <QuestGlowDemo />
      </Section>

      <Section number="3" title="Streak Warning Banner" description="Appears on the dashboard when quests aren't done and the day is ending.">
        <StreakWarning />
      </Section>

      <Section number="4" title="Public Player Profile" description="Click a friend's name to see their stats, path, and recent activity.">
        <PublicProfileCard />
      </Section>

      <Section number="5" title="Share Quest to Feed" description="One-click share after completing a quest — posts automatically to your social feed.">
        <ShareQuestDemo />
      </Section>

      <Section number="6" title="Sidebar Notification Badge" description="Amber badge on the Profile icon shows pending friend requests from any page.">
        <SidebarBadgeDemo />
      </Section>

      <Section number="7" title="Player Search" description="Search hunters by username prefix instead of needing the exact name.">
        <PlayerSearchDemo />
      </Section>

      <Section number="8" title="Quest Filters" description="Filter today's quests by category or show only remaining ones.">
        <QuestFiltersDemo />
      </Section>

      <Section number="9" title="My Groups vs Explore Tabs" description="Split the groups page into groups you belong to vs. public groups to discover.">
        <GroupTabsDemo />
      </Section>

      <Section number="10" title="Post Editing" description="Edit or delete your own posts directly in the feed. Backend already supports this.">
        <PostEditDemo />
      </Section>

      <div className="rounded-xl border border-[#1a3a5c] bg-[#0a1628] p-4 text-center">
        <p className="text-sm text-slate-400">
          Tell me which features you want to implement and I'll build them.
        </p>
      </div>
    </div>
  );
}
