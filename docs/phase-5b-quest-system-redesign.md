# Phase 5B — Quest System Redesign

## Status
In Progress

## Phase Type
Expansion of Phase 5 — Quest Expansion System

## Must Read Before Implementing
- AGENTS.md
- docs/architecture.md
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

The Player.path field must be updated via a Django
migration. Show the developer the migration file
before running it.

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

6. New Django app recommended:
   backend/paths/
   This app should own: path discovery quiz, path
   onboarding, path-specific mechanics per path.
   Confirm against existing structure before creating.

7. Extend the existing social app for achievement
   cards, badges, and leaderboards. Do not create
   a separate social-achievements app.

8. Never run migrations without showing the developer
   the full migration file first and getting approval.

9. Body Journal data must be preserved permanently
   regardless of whether Health Alchemist path
   is active or deactivated.

10. Freedom Day token overflow: if player earns a
    fourth token while already at maximum of three,
    award 200 bonus EXP instead of the token.

11. Cross-path bonus quests must be exempt from
    Recovery day filtering — always surface if
    available even on Recovery days.

12. Tomorrow preview must show quest categories only.
    Never show specific quest titles in preview.
    This prevents players gaming the system by
    waiting for easier quests.

13. Never shame a player for missing a day.
    All missed day language must be forward-facing.

14. Quest model must include a pack_id field for
    future expansion pack support even if unused now.

---

## Files To Inspect Before Writing Any Code

backend/players/models.py
- Read Player model carefully
- Note existing path field and its current choices
- Note level, exp, streak fields

backend/quests/models.py
- Read Quest model carefully
- Read PlayerDailyQuestAssignment model
- Note all existing fields before extending

backend/quests/services.py
- Understand existing quest service patterns
- New quest logic must follow same patterns

backend/quests/management/commands/seed_quests.py
- Read existing seed logic
- Extend this file — do not replace it
- Clear old data then seed new data

backend/social/models.py
- Read all existing social models
- Badge and achievement models extend here

backend/social/services.py
- Follow existing service patterns

frontend/src/pages/OnboardingPage.jsx
- Read current onboarding flow
- This will be replaced by Path Discovery System
- Confirm with developer before replacing

frontend/src/pages/DashboardPage.jsx
- Read current dashboard structure
- Quest board, completion ring, end of day summary
- extend this page — do not rebuild from scratch

frontend/src/components/QuestCard.jsx
- Read existing quest card component
- Extend to support new quest types and slot UI

frontend/src/components/ProgressCard.jsx
- Read existing progress card
- Extend to support completion ring

frontend/src/api.js
- Read existing API call patterns
- All new API calls must follow same patterns

---

## Pre-Build Checklist

Before writing any code Claude Code must complete
all of the following and show results to developer:

- [ ] All files listed above inspected and summarized
- [ ] Conflict map produced showing:
      what already exists
      what needs to be created
      what needs to be modified
      what needs to be deleted
- [ ] Migration plan for Player.path field shown
- [ ] Confirmation that old quest data wipe plan
      is safe and will not affect user accounts
- [ ] List of new models to be created confirmed
      against existing models (no duplicates)
- [ ] Developer approval received on conflict map
- [ ] Only then begin building

---

## Definition of Done

Phase 5B is complete when all items in
docs/game-design/BUILD_ORDER.md are checked off
and the following are verified:

- [ ] Player.path field updated with new path values
- [ ] Old quest seed data wiped cleanly
- [ ] All five paths have complete quest data seeded
- [ ] Path Discovery Quiz works end to end
- [ ] Path-specific onboarding works all five paths
- [ ] Daily Quest Assignment Engine runs at midnight
      in player local timezone
- [ ] Quest board shows correct daily lineup per player
- [ ] All path-specific mechanics working
- [ ] Cross-path bonus system working
- [ ] Social achievement features working
- [ ] Existing user accounts completely unaffected
- [ ] Existing social features still working
- [ ] No broken migrations
- [ ] All new code follows service layer pattern
- [ ] All EXP logic is server-side only