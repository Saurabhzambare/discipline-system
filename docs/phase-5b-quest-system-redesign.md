# Phase 5B — Quest System Redesign

## Status
**In Progress.** See `docs/CURRENT_STATUS.md` for the single source of truth
on session progress. Update both this doc and CURRENT_STATUS.md at the end
of every session.

### Progress Snapshot (updated 2026-05-02)

- ✅ Session 1: Foundation models complete
- ✅ Session 2: Path Discovery quiz complete
- ✅ Session 3: Quest seeding complete (with hardening patch)
- ✅ Session 4: Path onboarding flows complete (resume-safe status, DK oath moderation, GV skill-tree initialization)
- ✅ Session 5: Daily Quest Assignment Engine complete (lineup generation, intention/swap/feedback/summary entry points)
- ✅ Session 6: Path mechanic persistence hooks, log endpoints, protection-order service, accountability partner invite flow — complete
- ✅ Session 7: Backend contract layer complete — quest board, completion ring, EOD summary, tomorrow preview, missed-day return, adaptive difficulty nudge
- ✅ Session 8: Social & achievement features — complete (C3A–C3D)
- ⬜ Session 9: Final verification — not started

## Phase Type
Expansion of Phase 5 — Quest Expansion System

## Must Read Before Implementing
- AGENTS.md
- docs/architecture.md
- docs/CURRENT_STATUS.md
- docs/game-design/README.md
- docs/game-design/BUILD_ORDER.md
- docs/game-design/paths/fitness-warrior.md
- docs/game-design/paths/mindset-sage.md
- docs/game-design/paths/health-alchemist.md
- docs/game-design/paths/discipline-knight.md
- docs/game-design/paths/grind-visionary.md
- docs/game-design/systems/path-discovery.md
- docs/game-design/systems/daily-quest-logic.md

---

## Phase Goal

Replace the existing placeholder path and quest system
with a fully designed five-path RPG quest system.

The original Phase 5 introduced basic quest categories
and placeholder paths:
- runner
- gym
- discipline
- tournament
- 75hard

Phase 5B replaces this entirely with a complete game
design built around five identity-based paths, an
intelligent daily quest assignment engine, and
path-specific progression mechanics.

This phase must be completed before Phase 7
(Reward Engine and Achievements) and Phase 8
(Competitive Systems) can begin.

---

## Frontend Strategy (UPDATED 2026-04-22)

**The plan to hand off the frontend to Lovable has been abandoned.**

All frontend work — including final visual polish, dashboard redesign,
onboarding UX, and path mechanics presentation — will be completed here
using Claude Code. Any references to "Lovable handoff" in historical
docs (`docs/archive/session-7-*`) are obsolete.

What this means in practice:

- The current React frontend is the frontend we ship.
- Session 7 "proving UI" widgets will be polished in-place in Stage C
  of the plan in CURRENT_STATUS.md — not rebuilt elsewhere.
- Tailwind-based component primitives and a cohesive design system
  will be developed incrementally within `frontend/src/`.

---

## Data Migration Decision — CONFIRMED BY DEVELOPER

This decision is final. Do not ask again. Do not
preserve old data. Follow exactly as stated below.

WIPE:
- All existing quest data
- All existing path assignment data
- All existing PlayerDailyQuestAssignment records
- All existing quest seed data from seed_quests.py

KEEP:
- All user accounts — do not touch users app
- All Player records — do not touch player identity
- All social app data — posts, groups, friendships

RE-ONBOARD:
- Existing users will go through the new
  Path Discovery System on next login
- This is handled by the path discovery flow
  described in docs/game-design/systems/path-discovery.md

---

## Old Paths Being Removed

These Player.path field values are being removed:
- runner
- gym
- discipline
- tournament
- 75hard

---

## New Paths Being Introduced

These Player.path field values are being introduced:
- fitness_warrior
- mindset_sage
- health_alchemist
- discipline_knight
- grind_visionary

The Player.path field was updated via Django migration in Session 1.

---

## Scope of Phase 5B

### System 1 — Path Discovery System
Full spec: docs/game-design/systems/path-discovery.md

A 9-question identity quiz shown to every new user
and every existing user on re-onboarding.
Recommends the right path based on quiz answers.
Shows all five paths with match percentages.
Player commits to one primary path.
Additional paths unlock after 30 days of consistency.

### System 2 — Five Core Paths
Full specs: docs/game-design/paths/

Complete quest system for all five paths.
Each path has:
- Rank tiers: D rank, C rank, B rank, A rank, S rank
- Rank unlock by level:
  D = Level 1, C = Level 5, B = Level 10,
  A = Level 20, S = Level 30
- Pillar-based quest organization
- Universal daily quests (locked slots)
- Path-specific quest pool
- Cooldown logic per quest
- Path-specific onboarding questions
- Experience-based quest visibility
- Weekly boss quest (Monday reset)

### System 3 — Daily Quest Assignment Engine
Full spec: docs/game-design/systems/daily-quest-logic.md

An intelligent server-side algorithm that generates
a personalized daily quest lineup for each player.
Runs at midnight in the player's local timezone.
Uses a five-layer assignment algorithm.
Player can swap suggested quests within limits.
Includes daily intention prompt, expiry logic,
completion ring, and end of day summary.

### System 4 — Path-Specific Mechanics

Fitness Warrior:
- Split day tracking (PPL rotation)
- Rest day recovery quest set
- Equipment profile from onboarding

Mindset Sage:
- Freedom Day Token system
- Wisdom Log feature
- Dark Night Quest
- Sage archetype system

Health Alchemist:
- Elixir System with mercy mechanic
- Body Journal feature
- Alchemist Setup Guide with supplement and
  equipment recommendations
- Legal disclaimer in three places on setup guide

Discipline Knight:
- Armor System (6 pieces over 6 weeks)
- Discipline Code oath during onboarding
- Grace Token mechanic
- Streak Shield mechanic
- War Room daily planning tool
- Temptation Log
- Knight Weekly Report auto-generation
- Content moderation filter on Discipline Code

Grind Visionary:
- XP Multiplier system (1.0x to 2.0x over 30 days)
- Multiplier Protection mechanic
- Vision Board with singular goal and countdown
- Skill Tree per grind focus
- Output Log
- Accountability Partner system
- First Dollar legendary moment
- Post-First-Dollar quest chain

### System 5 — Cross-Path System
Bonus EXP pairs when matching quests completed
across multiple active paths on same day.
Maximum one cross-path bonus per day.
Cross-path identity titles:
- Warrior-Sage
- The Optimized Human
- The Complete Human
- The Renaissance Human (all five paths active)

### System 6 — Social Achievement Features
Achievement cards auto-generated for milestones.
Path-specific badge collections.
Weekly EXP leaderboard per path.
Global cross-path leaderboard.
Path-specific leaderboards (armor, multiplier).
Public profile enhancements per path.

---

## Core Game Constants

EXP formula for level progression:
EXP needed = level squared times 50 minus 50

Rank unlock by player level:
- D rank: Level 1
- C rank: Level 5
- B rank: Level 10
- A rank: Level 20
- S rank: Level 30

---

## Phase Boundaries

### In Scope
Everything described in the game-design docs folder.

### Out Of Scope For This Phase
- Push notifications
- Email notifications
- Native mobile features
- Payment or subscription logic
- Advanced content moderation beyond basic filter
- Device integrations (smartwatch, step tracking)
- Custom path (dropped — not being built)

---

## Architecture Rules For This Phase

Follow all rules in AGENTS.md and docs/architecture.md.

Additional rules specific to this phase:

1. All new business logic goes in service layer files.
   Follow the pattern in backend/quests/services.py
   and backend/social/services.py.
   Views stay thin. Models stay clean.

2. The five-layer quest assignment algorithm must run
   server-side only. Never client-side.

3. All EXP calculations including multipliers and
   cross-path bonuses must be server-side only.

4. Quiz answer order randomization must be
   server-side only to prevent pattern gaming.

5. Timezone must be stored per user. All time-sensitive
   logic uses player local timezone — midnight reset,
   expiry notifications, end of day summary.

6. Backend app structure (FINAL for Phase 5B):
   - `backend/paths/` owns path discovery quiz, path
     onboarding, path-specific mechanics per path
   - `backend/social/` extended for achievement cards,
     badges, and leaderboards (no separate app)

7. Never run migrations without showing the developer
   the full migration file first and getting approval.

8. Body Journal data must be preserved permanently
   regardless of whether Health Alchemist path
   is active or deactivated.

9. Freedom Day token overflow: if player earns a
   fourth token while already at maximum of three,
   award 200 bonus EXP instead of the token.

10. Cross-path bonus quests must be exempt from
    Recovery day filtering — always surface if
    available even on Recovery days.

11. Tomorrow preview must show quest categories only.
    Never show specific quest titles in preview.
    This prevents players gaming the system by
    waiting for easier quests.

12. Never shame a player for missing a day.
    All missed day language must be forward-facing.

13. Quest model must include a pack_id field for
    future expansion pack support even if unused now.

---

## Files To Inspect Before Writing Any Code

### Backend

- `backend/players/models.py` — Player model, EXP/level/streak fields
- `backend/quests/models.py` — Quest, QuestCompletion, DailyQuestLineup, DailyQuestLineupItem
- `backend/quests/services.py` — 5-layer assignment, swap, feedback, intention, summary, tomorrow preview, adaptive nudge
- `backend/quests/management/commands/seed_quests.py` — quest seed data for all 5 paths
- `backend/paths/models.py` — path discovery, onboarding progress, all path-specific profiles and mechanics
- `backend/paths/services.py` — quiz scoring, onboarding save flows, mechanics orchestration
- `backend/social/models.py` — friend/post/group/badge/achievement models
- `backend/social/services.py` — social domain service patterns

### Frontend

- `frontend/src/App.jsx` — routing and state orchestration (monolithic — technical debt)
- `frontend/src/api.js` — all API call helpers
- `frontend/src/pages/PathOnboardingPage.jsx` — 5-path onboarding flow
- `frontend/src/pages/DashboardPage.jsx` — quest board, completion ring, path mechanics widgets
- `frontend/src/pages/ProfilePage.jsx`
- `frontend/src/pages/FeedPage.jsx`
- `frontend/src/pages/GroupsPage.jsx`
- `frontend/src/components/Layout.jsx` — sidebar nav, flash banner
- `frontend/src/components/QuestCard.jsx`

---

## Definition of Done

Phase 5B is complete when all items in
`docs/game-design/BUILD_ORDER.md` are checked off
and the following are verified:

- [x] Player.path field updated with new path values
- [x] Old quest seed data wiped cleanly
- [x] All five paths have complete quest data seeded
- [x] Path Discovery Quiz works end to end (verified in C4-1 Step 89)
- [x] Path-specific onboarding works all five paths (verified in C4-1 Step 92)
- [x] Daily Quest Assignment Engine runs at midnight
      in player local timezone (verified in C4-2 timezone + DST tests)
- [x] Quest board shows correct daily lineup per player (verified in C4-1 Steps 89/93)
- [x] All path-specific mechanics working (Session 6 + C4-1 Step 94)
- [x] Cross-path bonus system working (C4-1 Step 95 — detection + bonus EXP + Visionary multiplier safety)
- [x] Social achievement features working (Session 8 + C4-1 Step 98)
- [x] Existing user accounts completely unaffected (C4-1 Step 90)
- [x] Existing social features still working (C4-1 Step 91)
- [x] No broken migrations (C4-3 Step 99 — paths/0008 and social/0006 BigAutoField drift resolved)
- [x] All new code follows service layer pattern (C4-3 Step 100 audit)
- [x] All EXP logic is server-side only (C4-3 Step 101 — frontend `deriveProgressFromTotalExp` removed)

---

### Phase 5B Sign-Off

Phase 5B closed on **2026-05-09** under C4-3.

- Final backend test count: **322 tests passing**.
- Final Django check: clean.
- Final `makemigrations --check --dry-run`: clean.
- Final frontend lint + Vite build: clean.
- C4-1 added end-to-end integration tests (`backend/social/tests_phase5b_e2e.py`, 41 tests covering BUILD_ORDER Steps 89–98).
- C4-2 added edge-case verification tests (`backend/quests/tests_phase5b_edge_cases.py`, 17 tests covering timezone, DST spring-forward, missed-day protection priority order, duplicate-completion safety).
- C4-3 closed Steps 99–105: BigAutoField migration drift resolved, duplicate-completion contract made idempotent, server-side EXP authority enforced, sixth-path placeholder confirmed inert.

Stage D (production hardening — DEBUG/SECRET_KEY/ALLOWED_HOSTS, React Router migration, pagination) is the recommended next session.

---

## Notes

Historical session plans and handoff documents (including the abandoned
Lovable plan) are preserved in `docs/archive/` for context but are no
longer operative.
