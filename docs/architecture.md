# Architecture

## Purpose of this document

This document explains the intended architecture direction of **Discipline System**.

Its job is to keep future development clean and consistent by clarifying:

- what the system is
- how the current backend is organized
- which app should own which responsibilities
- where business logic should live
- how roadmap phases relate to system boundaries
- where engagement mechanics fit
- how future expansion should happen without premature refactoring

This document is especially important for:

- future contributors
- AI coding agents
- phase-based implementation work

**Last updated:** 2026-04-22

---

# 1. System overview

Discipline System is a Solo Leveling–inspired discipline web app that turns real-life actions into progression.

Core loop:

- user acts as a **player**
- daily actions become **quests**
- completed quests award **EXP**
- EXP contributes to **level progression**
- consistency contributes to **streak growth**
- dashboard acts as a **status window**

Long-term product direction:

- gamified self-improvement platform
- community and competition features
- premium ecosystem
- device-connected activity
- immersive UI
- mobile apps only after the web platform is complete and stable

---

# 2. Current architecture philosophy

The current architecture philosophy is:

- keep the codebase understandable
- keep app boundaries clear
- avoid large refactors unless there is a real need
- use services for non-trivial business logic
- keep future scaling in mind without forcing it too early
- preserve the current structure unless a real problem is found
- build the web app first, then mobile later

Important current decision:

**We are not doing a major backend structural refactor right now.**

That means:

- the current app structure should be respected
- new features should be added cleanly within existing boundaries where possible
- a new app should only be introduced when the domain clearly justifies it
- features should be phased according to roadmap priority

---

# 3. Current backend structure

```text
backend/
  config/       — Django project settings, URLs, WSGI/ASGI
  core/         — Shared utilities, common mixins, small reusable pieces
  users/        — Custom user model, authentication (JWT), signup/login
  players/      — Player profile, EXP, level, streak, daily intention, daily summary
  quests/       — Quest definitions, completions, daily lineups, 5-layer assignment engine
  paths/        — Path discovery quiz, path onboarding, path-specific profiles and mechanics
  social/       — Friends, feed, groups, badges, achievement cards, weekly boss quests
  manage.py
  requirements.txt
  Dockerfile
  .env
  db.sqlite3
```

---

# 4. App responsibilities

## `users`

Owns:
- user account model (extends Django AbstractUser)
- authentication flow (JWT issue, refresh, logout)
- password management
- signup/login serializers and views

Does NOT own:
- player progression state (lives in `players`)
- profile display logic (shared between `players` and `social`)

## `players`

Owns:
- Player model (the gameplay-side user)
- EXP, level, streak tracking
- Level formula: quadratic `EXP needed = level² × 50 − 50`
- Daily intention (Full Send / Steady / Recovery)
- Daily completion summary records
- Player path field (currently `fitness_warrior`, `mindset_sage`, `health_alchemist`, `discipline_knight`, `grind_visionary`)
- Per-user timezone (for midnight reset logic)

Does NOT own:
- quest definitions or completion logic (lives in `quests`)
- path-specific mechanics (lives in `paths`)

## `quests`

Owns:
- Quest model (all quest definitions, universal + path-specific)
- QuestCompletion history (immutable log)
- DailyQuestLineup + DailyQuestLineupItem (normalized lineup storage)
- Five-layer daily assignment algorithm (server-side)
- Quest swap, feedback, intention adjustment services
- Quest expiry logic by rank
- Completion ring data aggregation
- End-of-day summary generation
- Tomorrow preview (categories only)
- Adaptive difficulty nudge
- Seed data command (`seed_quests`)
- Midnight scheduler management command

Does NOT own:
- path mechanic side-effects (lives in `paths`)
- badge/achievement generation (lives in `social`)

## `paths`

Owns:
- Path Discovery Quiz (9 questions, scoring, match percentages)
- UserPathSelection and multi-path unlock logic
- PathOnboardingProgress (resume-safe step tracking)
- Path-specific onboarding profiles (one model per path)
- Path-specific mechanics:
  - Fitness Warrior: SplitDayState, EquipmentProfile
  - Mindset Sage: WisdomLog, DarkNightEntry, Freedom Day tokens
  - Health Alchemist: ElixirProgress, BodyJournal, TransmutationMilestone, EquipmentProfile
  - Discipline Knight: DisciplineCode, ArmorSystem, ArmorPiece, GraceToken, StreakShield, WarRoomEntry, TemptationLog, KnightWeeklyReport
  - Grind Visionary: XPMultiplier, MultiplierProtection, SingularGoal, SkillTree, SkillTreeNode, OutputLog, PostFirstDollarChain
- QuestChain (cross-app — lives in paths for organizational reasons)
- TransmutationMilestone

Does NOT own:
- quest seed data (lives in `quests`)
- lineup generation (lives in `quests`)
- leaderboards or achievement cards (lives in `social`)

## `social`

Owns:
- FriendRequest, Friendship
- SocialPost, PostComment, PostReaction
- ActivityEvent (activity feed)
- SocialGroup, GroupMembership
- AccountabilityPartnerRequest, AccountabilityPartnership
- Badge, UserBadge
- AchievementCard
- WeeklyBossQuest, WeeklyBossCompletion
- Leaderboards (when built in Session 8)
- Cross-path identity titles (when built in Session 8)

Does NOT own:
- quest completion logic (lives in `quests`)
- path onboarding (lives in `paths`)

## `core`

Owns:
- small shared utilities
- common mixins or base classes
- anything truly cross-cutting

Does NOT own:
- domain-specific business logic
- feature-level concerns

Keep `core` light. If something feels like a feature, it belongs in a domain app.

---

# 5. Where business logic lives

**Service layer pattern is the default.** Heavy logic goes in
`{app}/services.py` (or a subpackage of services). Views orchestrate;
serializers validate and represent; models stay clean.

Current service files:

- `backend/quests/services.py` — lineup generation, completion, swap, feedback, intention, summary, tomorrow preview, adaptive nudge, protection order
- `backend/paths/services.py` — quiz scoring, onboarding save flows, path mechanic persistence
- `backend/social/services.py` — friend/post/group/reaction actions
- `backend/players/services.py` (if present) — progression helpers

Query helpers for read-only visibility rules live in selectors:
- `backend/social/selectors.py`

---

# 6. Frontend architecture

`frontend/src/` is a React 19 + Vite + Tailwind app.

Current state:
- Custom manual routing via `history.pushState` in `App.jsx`
- `App.jsx` is monolithic — centralizes most state and handlers
- `api.js` is a single file with all backend call helpers
- Pages in `frontend/src/pages/`
- Reusable components in `frontend/src/components/`
- `PathContext.jsx` provides React Context for path state

Planned improvements (Stage C in CURRENT_STATUS.md):
- Migrate from custom routing to React Router
- Break up `App.jsx` into smaller state containers
- Introduce a design-token system in Tailwind config
- Build out shared component primitives

---

# 7. Data store

- **Development:** SQLite (`db.sqlite3`)
- **Production:** PostgreSQL (via Railway)
- **Migrations:** Django migrations, always shown to developer before running

---

# 8. Scheduling

- **Midnight quest lineup generation:** Django management command
  (`generate_daily_lineup` or equivalent), triggered by Railway cron
  in production. Runs per-player, using player-local timezone.
- **No Celery, no Redis** — this is a deliberate simplicity choice.
  If background work grows, Celery + Redis can be introduced later.

---

# 9. Roadmap phase alignment

See `docs/web-development-roadmap.md` for full phase list.
See `docs/CURRENT_STATUS.md` for live progress.

Current active work: **Phase 5B** (Quest System Redesign).

Phases 1–4 and Phase 5 (original) are complete. Phase 6 (Social Platform)
was built largely in parallel with Phase 5B and is mostly functional;
some social features depend on Phase 5B Session 8 (badges, leaderboards,
achievement cards).

---

# 10. Non-negotiables

1. **All EXP calculations are server-side.** The frontend never computes EXP.
2. **Timezone is per-user.** Midnight resets, expiry, and EOD summaries use player-local time.
3. **Service-layer pattern is the default.** Views stay thin.
4. **Migrations are shown to the developer before being run.**
5. **No feature work goes to `main` without passing tests.**
6. **Body Journal data is preserved permanently** regardless of path deactivation.
