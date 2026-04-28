# Discipline System — Build Order and Progress Tracker
# docs/game-design/BUILD_ORDER.md

**Last updated:** 2026-04-28

---

## How To Use This File

This file is the step-level task tracker for Phase 5B.
For a higher-level status, read `docs/CURRENT_STATUS.md`.

At the start of every Claude Code session say:

> "Read AGENTS.md. Read docs/architecture.md.
> Read docs/CURRENT_STATUS.md.
> Read docs/phase-5b-quest-system-redesign.md.
> Read docs/game-design/README.md.
> Read docs/game-design/BUILD_ORDER.md.
> Find the first unchecked step and tell me
> what it is before doing anything."

Rules:
- Never skip a step
- Never build out of order
- Check off each step only when fully complete
- If a step reveals a conflict stop and
  report it to the developer before continuing
- Never run a migration without showing the
  developer the migration file first

---

## Pre-Build — Repository Audit

- [x] Read AGENTS.md in full
- [x] Read docs/architecture.md in full
- [x] Read docs/phase-5b-quest-system-redesign.md in full
- [x] Read docs/game-design/README.md in full
- [x] Read all files in docs/game-design/paths/
- [x] Read all files in docs/game-design/systems/
- [x] Inspect backend/players/models.py
- [x] Inspect backend/quests/models.py
- [x] Inspect backend/quests/services.py
- [x] Inspect backend/quests/management/commands/seed_quests.py
- [x] Inspect backend/social/models.py
- [x] Inspect backend/social/services.py
- [x] Inspect backend/social/serializers.py
- [x] Inspect backend/social/views.py
- [x] Inspect backend/players/serializers.py
- [x] Inspect backend/players/views.py
- [x] Inspect backend/users/models.py
- [x] Inspect frontend/src/pages/OnboardingPage.jsx
- [x] Inspect frontend/src/pages/DashboardPage.jsx
- [x] Inspect frontend/src/pages/ProfilePage.jsx
- [x] Inspect frontend/src/components/QuestCard.jsx
- [x] Inspect frontend/src/components/ProgressCard.jsx
- [x] Inspect frontend/src/api.js
- [x] Conflict map produced and approved

---

## Session 1 — Foundation Models ✅ COMPLETE

- [x] Step 1: Create new `paths` Django app
- [x] Step 2: Migrate Player.path field from old to new choices
- [x] Step 3: Create quest model extensions (pack_id, rank, path_target, category, difficulty, recurrence, universality flag)
- [x] Step 4: Create DailyQuestLineup + DailyQuestLineupItem models (normalized)
- [x] Step 5: Create path-specific profile and mechanic models:
      PathDiscoveryQuiz, QuizAnswer, PathMatchScore,
      UserPathSelection, PathOnboardingProgress,
      FitnessWarriorProfile, MindsetSageProfile,
      HealthAlchemistProfile, DisciplineKnightProfile,
      GrindVisionaryProfile, SplitDayState,
      ArmorSystem, ArmorPiece, ElixirProgress,
      EquipmentProfile, DisciplineCode, GraceToken,
      StreakShield, WarRoomEntry, TemptationLog,
      KnightWeeklyReport, XPMultiplier,
      MultiplierProtection, SingularGoal, SkillTree,
      SkillTreeNode, OutputLog, PostFirstDollarChain,
      QuestChain, TransmutationMilestone, BodyJournal,
      WisdomLog, DarkNightEntry
      Plus social.Badge, UserBadge, AchievementCard,
      WeeklyBossQuest, WeeklyBossCompletion
- [x] Step 6: Show all migration files to developer
- [x] Step 7: Run migrations
- [x] Step 8: Verify database integrity
- [x] Step 9: Add timezone field to Player

---

## Session 2 — Path Discovery System ✅ COMPLETE

- [x] Step 10: Build quiz scoring backend logic
- [x] Step 11: Build answer order randomization (server-side, seeded per quiz)
- [x] Step 12: Build PathDiscoveryQuiz API endpoints (create, submit, results)
- [x] Step 13: Build UserPathSelection endpoints (select, get, retake)
- [x] Step 14: Build multi-path unlock logic (30-day milestone check)
- [x] Step 15: Build frontend quiz flow
- [x] Step 16: Build results screen
- [x] Step 17: Build path cards screen
- [x] Step 18: Build commitment screen
- [x] Step 19: Build sixth path locked placeholder

---

## Session 3 — Quest Seeding ✅ COMPLETE

- [x] Step 20: Extend seed_quests.py (wipe + reseed, not replace)
- [x] Step 21: Seed universal daily quests
- [x] Step 22: Seed Fitness Warrior quests (all ranks D-S)
- [x] Step 23: Seed Mindset Sage quests (all ranks D-S)
- [x] Step 24: Seed Health Alchemist quests (all ranks D-S + supplement disclaimer text)
- [x] Step 25: Seed Discipline Knight quests (all ranks D-S)
- [x] Step 26: Seed Grind Visionary quests (all ranks D-S)
- [x] Step 27: Seed weekly boss quests per path + upsert WeeklyBossQuest records
- [x] (Hardening patch): seed QuestChain edges for ha_gut_reset_chain;
      remove duplicate JSON.stringify in quiz/path API callers

---

## Session 4 — Path Onboarding Flows ✅ COMPLETE

- [x] Step 28: Fitness Warrior onboarding (4 questions + split day)
- [x] Step 29: Mindset Sage onboarding (4 questions + archetype)
- [x] Step 30: Health Alchemist onboarding (4 questions + equipment multi-select)
- [x] Step 31: Alchemist Setup Guide (supplement cards, equipment cards, disclaimer in 3 places)
- [x] Step 32: Discipline Knight onboarding (4 questions)
- [x] Step 33: Discipline Code Oath screen (with server-side V1 keyword moderation)
- [x] Step 34: Grind Visionary onboarding (6 questions)
- [x] Step 35: Skill Tree initialization on GV onboarding complete

---

## Session 5 — Daily Quest Assignment Engine ✅ COMPLETE

- [x] Step 36: Five-layer assignment algorithm (server-side)
- [x] Step 37: Timezone-aware midnight scheduler (Django management command)
- [x] Step 38: Day 1 hardcoded starter lineup per path
- [x] Step 39: Progressive complexity reveal logic (Day 1-6 / Day 7 / Day 14 / Day 30)
- [x] Step 40: Quest expiry logic by rank
- [x] Step 41: Swap system (max 3 per day, preference learning)
- [x] Step 42: Quest feedback thumbs system
- [x] Step 43: Daily intention prompt (Full Send / Steady / Recovery)
- [x] Step 44: Fitness Warrior daily override logic (rest/push/pull/leg day)
- [x] Step 45: Mindset Sage daily override logic (Sunday review, Freedom Day, Dark Night)
- [x] Step 46: Health Alchemist daily override logic (Morning Protocol lock, elixir day 7, equipment gating)
- [x] Step 47: Discipline Knight daily override logic (Sunday Honor Review, War Room lock, armor cracked override)
- [x] Step 48: Grind Visionary daily override logic (multiplier upgrade surface, Sunday Vision Board, accountability quest)
- [x] Step 49: Cross-path bonus detection (max one per day, gold border flag)
- [x] Step 50: Missed day logic (protection order: Grace → Shield → Multiplier → Elixir Mercy → break)

---

## Session 6 — Path-Specific Mechanics 🟡 IN PROGRESS

### Fitness Warrior mechanics
- [x] Step 51: Split day rotation service (PPL auto-rotate)
- [x] Step 52: Rest day detection and recovery quest set loading
- [x] Step 53: Equipment-gated quest filtering

### Mindset Sage mechanics
- [x] Step 54: Freedom Day Token accumulation + overflow bonus EXP
- [x] Step 55: Wisdom Log CRUD + count milestones
- [x] Step 56: Dark Night Quest manual activation + entry logging
- [x] Step 57: Sage archetype quest pool filtering — wired in `_apply_path_overrides` (Session A1)

### Health Alchemist mechanics
- [x] Step 58: Elixir System brew counter + Day 7 completion
- [x] Step 59: Elixir mercy mechanic (1 miss allowed)
- [x] Step 60: Body Journal CRUD + read-only mode when path deactivated
- [x] Step 61: Transmutation milestone titles

### Discipline Knight mechanics
- [x] Step 62: Armor System (6 pieces, crack mechanic)
- [x] Step 63: Grace Token accumulation + consumption
- [x] Step 64: Streak Shield auto-activation
- [x] Step 65: War Room morning + evening entries + same-day bonus EXP
- [x] Step 66: Temptation Log CRUD
- [x] Step 67: Knight Weekly Report auto-generation on Sunday — wired into `generate_daily_quests` command (Session A1)

### Grind Visionary mechanics
- [x] Step 68: XP Multiplier calculation (1.0x → 2.0x over 30 days)
- [x] Step 69: Multiplier Protection (1 miss allowed per tier)
- [x] Step 70: Vision Board + singular goal + countdown
- [x] Step 71: Skill Tree node unlock sequence
- [x] Step 72: Output Log CRUD + public/private flag
- [ ] Step 73: Accountability Partner invite flow (social domain) — in progress
- [x] Step 74: First Dollar legendary moment + post-first-dollar quest chain

### Cross-cutting
- [x] Step 75: Protection-order service consolidated into single helper — verified in `paths/mechanics.py:apply_missed_day_protections` (Session A1)
- [ ] Step 76: Path-mechanic log endpoints wired to frontend widgets — audit gaps

---

## Session 7 — Backend Contract Layer ✅ COMPLETE

- [x] Step 77: Completion ring endpoint + payload
- [x] Step 78: End-of-day summary endpoint + tomorrow preview embed
- [x] Step 79: Tomorrow preview categories-only endpoint (no titles)
- [x] Step 80a: Missed-day return state in daily lineup bootstrap
- [x] Step 81a: Adaptive difficulty nudge read + write endpoints + persistence
- [x] Step 82a: Quest board progressive slot metadata (ui_mode, day_on_path, features_unlocked, swaps_remaining)
- [x] Step 83a: Backward-compatible endpoint aliases for summary/alternatives

---

## Session 8 — Social and Achievement Features ⬜ NOT STARTED

Read before this session:
docs/game-design/systems/path-discovery.md
docs/game-design/README.md cross-path section

- [ ] Step 80: Build achievement card generation —
      auto-generated shareable image cards
      triggered by defined milestone events
      card contains: username level achievement
      date app branding
      user can download as image for Instagram
      user can post to in-app public profile
- [ ] Step 81: Build badge system —
      all path-specific badges defined
      badge awarded on milestone completion
      badges visible on public profile
      badge collection viewable by other players
- [ ] Step 82: Build weekly EXP leaderboard
      per path —
      resets Monday 00:00
      shows top 10 globally plus user own rank
- [ ] Step 83: Build global cross-path
      EXP leaderboard —
      combined EXP across all active paths
      with multiplier applied for Visionary
- [ ] Step 84: Build armor leaderboard (Knight) —
      permanent all-time
      shows most armor pieces forged globally
      armor color shown (silver or gold prestige)
- [ ] Step 85: Build multiplier streak leaderboard
      (Visionary) —
      current active multiplier streak
      resets if multiplier breaks
- [ ] Step 86: Build cross-path identity titles —
      Warrior-Sage
      The Optimized Human
      The Complete Human
      The Renaissance Human
      titles displayed on public profile
      achievement card generated on unlock
      Renaissance Human gets dedicated
      leaderboard tier globally
- [ ] Step 87: Build public profile enhancements —
      armor visualization (Knight)
      Discipline Code display (Knight)
      multiplier and streak (Visionary)
      singular goal if user sets visible (Visionary)
      Wisdom Log entry count (Sage)
      Elixir progress visualization (Alchemist)
      skill tree current node (Visionary)
      output log public entries (Visionary)
- [ ] Step 88: Build weekly boss quest system —
      appears every Monday reset Monday 00:00
      one boss quest per path
      rotating examples per path as defined
      completion awards EXP plus exclusive badge
      Visionary boss quest EXP has
      multiplier applied

---

## Session 9 — Final Verification ⬜ NOT STARTED

- [ ] Step 89: Full end-to-end flow tested —
      new user signup through path discovery
      through onboarding through first week
      of daily quests
- [ ] Step 90: Existing user account flow tested —
      existing user logs in
      gets redirected to path discovery quiz
      completes re-onboarding
      account data intact
      social data intact
- [ ] Step 91: All existing social features
      verified still working —
      posts comments reactions friends groups
- [ ] Step 92: All five path onboarding flows
      tested end to end
- [ ] Step 93: Daily quest assignment engine
      tested for all five paths
- [ ] Step 94: All path-specific mechanics tested
- [ ] Step 95: Cross-path bonus system tested
- [ ] Step 96: Cross-path identity titles tested
- [ ] Step 97: Leaderboards tested
- [ ] Step 98: Achievement cards tested
- [ ] Step 99: No broken migrations confirmed
- [ ] Step 100: All new code follows service layer pattern
- [ ] Step 101: All EXP logic confirmed server-side only
- [ ] Step 102: Timezone logic confirmed
- [ ] Step 103: Quest model pack_id field confirmed
- [ ] Step 104: Sixth path placeholder confirmed non-functional
- [ ] Step 105: BUILD_ORDER.md fully checked off — Phase 5B complete

---

## Notes and Decisions Log

[2026-04-12] — Session 7 completed as backend contract freeze.
Minimal proving UI shipped in dashboard. At the time, plan was to
hand off to Lovable.

[2026-04-22] — Lovable handoff plan ABANDONED. All frontend polish
will be done here using Claude Code. See CURRENT_STATUS.md Stage C
for frontend polish plan.

[2026-04-22] — Documentation cleanup. Historical phase docs and
session-7 Lovable handoff docs moved to docs/archive/.

[2026-04-28] — Session A1 cleanup. Wired Sage archetype filtering (Step 57),
Knight Weekly Report Sunday trigger (Step 67). Verified protection-order
consolidation (Step 75). Deleted OnboardingPage.jsx orphan; all /onboarding
routes redirect to /path-onboarding. Backend: 63 tests green. Frontend: lint
clean, build succeeds. Pending: Steps 73 and 76 (Session 6 remaining gaps).

---
