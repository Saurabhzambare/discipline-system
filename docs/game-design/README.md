# Game Design — README
# docs/game-design/README.md

---

## What This Folder Contains

This folder contains the complete game design
specification for the Discipline System quest and
path system (Phase 5B).

Every file in this folder was written specifically
for Claude Code to read and implement. Each file
is focused on one system or one path only so that
Claude Code loads only what it needs per session.

---

## IMPORTANT — Read This Before Anything Else

This folder does not work alone.

Before reading any file in this folder you must
first read these files in this exact order:

1. AGENTS.md (root folder)
2. docs/architecture.md
3. docs/phase-5b-quest-system-redesign.md

Those three files contain:
- coding rules and patterns to follow
- architecture principles for this project
- migration decisions that are final
- execution plan and pre-build checklist

Do not skip them. Do not assume you know what
they say. Read them every session.

---

## Folder Structure
```
docs/game-design/
│
├── README.md                 ← this file
├── BUILD_ORDER.md            ← session tracker
│
├── paths/
│   ├── fitness-warrior.md
│   ├── mindset-sage.md
│   ├── health-alchemist.md
│   ├── discipline-knight.md
│   └── grind-visionary.md
│
└── systems/
    ├── path-discovery.md
    └── daily-quest-logic.md
```

---

## What Each File Contains

### BUILD_ORDER.md
Step by step session tracker with checkboxes.
Read this at the start of every session to know
exactly where to continue from.
Check off each step as it is completed.
Never skip steps. Never build out of order.

---

### paths/fitness-warrior.md
Complete specification for the Fitness Warrior path.

Contains:
- Path overview and target audience
- Onboarding questions (4 questions plus split day)
- Split day tracking logic (PPL rotation)
- Universal daily quests
- Full quest list for all ranks D C B A S
- Rest day recovery quest set
- Weekly boss quest examples
- Adaptive difficulty nudge
- Social features and badges
- Equipment profile from onboarding

Read this file when:
- Building Fitness Warrior onboarding
- Seeding Fitness Warrior quest data
- Building split day tracking logic
- Building rest day logic

---

### paths/mindset-sage.md
Complete specification for the Mindset Sage path.

Contains:
- Path overview and target audience
- Four pillars with renamed identities
- Onboarding questions (4 questions plus archetype)
- Sage archetype system and quest filtering
- Universal daily quests
- Full quest list for all ranks D C B A S
- Freedom Day Token system (full design)
- Wisdom Log feature
- Dark Night Quest (manual activation)
- Weekly boss quest examples
- Social features and badges

Read this file when:
- Building Mindset Sage onboarding
- Seeding Mindset Sage quest data
- Building Freedom Day Token system
- Building Wisdom Log
- Building Dark Night Quest

---

### paths/health-alchemist.md
Complete specification for the Health Alchemist path.

Contains:
- Path overview and target audience
- Six pillars with Alchemist renamed identities
- Pillar unlock by level
- Onboarding questions (4 questions)
- Equipment profile and equipment gating logic
- Alchemist Setup Guide full design:
  supplement cards with food alternatives
  equipment cards with budget alternatives
  personalized starter pack logic
  legal disclaimer placement (3 locations)
- Universal daily quests
- Morning Protocol signature quest
- Full quest list for all ranks D C B A S
- Elixir System full design with mercy mechanic
- Transmutation milestone titles
- Body Journal feature
- Weekly boss quest examples
- Social features and badges

Read this file when:
- Building Health Alchemist onboarding
- Building Alchemist Setup Guide
- Seeding Health Alchemist quest data
- Building Elixir System
- Building Body Journal

---

### paths/discipline-knight.md
Complete specification for the Discipline Knight path.

Contains:
- Path overview and target audience
- Six pillars with Knight renamed identities
- Onboarding questions (4 questions plus Oath Screen)
- Discipline Code oath system full design
- Content moderation filter on Discipline Code
- Universal daily quests
- Full quest list for all ranks D C B A S
- Armor System full design:
  6 piece progression over 6 weeks
  crack mechanic
  Grace Token mechanic
  Streak Shield mechanic
  armor prestige (silver to gold)
- War Room daily planning tool
- Temptation Log
- Knight Weekly Report auto-generation
- Weekly boss quest examples
- Honor Review quest (Sunday only)
- Social features and badges

Read this file when:
- Building Discipline Knight onboarding
- Building Oath Screen and Discipline Code
- Seeding Discipline Knight quest data
- Building Armor System
- Building War Room
- Building Weekly Report

---

### paths/grind-visionary.md
Complete specification for the Grind Visionary path.

Contains:
- Path overview and target audience
- Six pillars with progressive unlock by level
- Onboarding questions (6 questions)
- Singular goal and deadline setup
- Grind focus skill tree definitions for all fields
- Universal daily quests
- Full quest list for all ranks D C B A S
- XP Multiplier system full design:
  1.0x to 2.0x over 30 days
  multiplier countdown bar
  multiplier protection mechanic
- Vision Board feature
- Skill Tree per grind focus (7 focus areas)
- Output Log feature
- Accountability Partner system
- First Dollar legendary moment full design
- Post-First-Dollar quest chain
- Weekly boss quest examples
- Social features and badges

Read this file when:
- Building Grind Visionary onboarding
- Seeding Grind Visionary quest data
- Building XP Multiplier system
- Building Vision Board
- Building Skill Tree
- Building Output Log
- Building Accountability Partner
- Building First Dollar moment

---

### systems/path-discovery.md
Complete specification for the Path Discovery System.

Contains:
- System overview and purpose
- Full user flow from signup to dashboard
- Welcome screen design and copy
- All 9 quiz questions with full answer options
- Complete scoring logic per answer per path
- Match percentage calculation formula
- Answer order randomization requirement
- Results screen design and opening lines per path
- All 5 path cards with full content:
  who you are now
  who you become in 90 days
  what you gain
  this path is for you if
- Commitment screen copy per path
- Multi-path unlock logic (Day 30 trigger)
- Quiz retake feature
- Data models needed

Read this file when:
- Building the Path Discovery Quiz backend
- Building the quiz frontend flow
- Building the results screen
- Building path cards
- Building the commitment screen
- Building multi-path unlock logic

---

### systems/daily-quest-logic.md
Complete specification for the Daily Quest
Assignment Engine.

Contains:
- System overview and daily flow
- Timezone handling requirement
- Progressive complexity reveal by day
  (Day 1-6 simple, Day 7 slots, Day 14 swaps,
  Day 30 customization)
- Day 1 hardcoded starter lineup per path
- Quest slot structure and types
  (Universal locked, Assigned swappable, Bonus open)
- Default slot counts per active path count
- Level-scaled maximum total daily quests
- Player slot customization in settings
- Daily Intention prompt (Full Send, Steady, Recovery)
- Five-layer assignment algorithm:
  Layer 1 lock universal quests
  Layer 2 hard filters
  Layer 3 weekly rhythm as default
  Layer 4 smart suggestion logic
  Layer 5 fill remaining slots
- Weekly rhythm tables for all five paths
- Swap system with 3-swap limit
- Quest feedback thumbs system
- Quest expiry logic by rank
- Path-specific daily override logic per path
- Cross-path daily bonus logic
- Missed day logic and return experience
- Completion ring design (single segmented ring)
- End of day summary (9PM trigger)
- Tomorrow preview (categories only)
- Data models needed

Read this file when:
- Building the assignment algorithm
- Building the midnight scheduler
- Building the quest board frontend
- Building the swap system
- Building the completion ring
- Building the end of day summary
- Building the missed day return screen

---

## How To Use This Folder Per Session

### Starting A New Session

At the start of every Claude Code session say:

"Read AGENTS.md. Then read docs/architecture.md.
Then read docs/phase-5b-quest-system-redesign.md.
Then read docs/game-design/README.md.
Then read docs/game-design/BUILD_ORDER.md.
Find the first unchecked step and tell me what
it is before doing anything."

### Working On A Specific Path

When working on a specific path say:

"Read docs/game-design/paths/[path-name].md.
Complete step [number] from BUILD_ORDER.md."

### Working On A System

When working on a system say:

"Read docs/game-design/systems/[system-name].md.
Complete step [number] from BUILD_ORDER.md."

### Resuming After A Break

When resuming after any gap say:

"Read docs/game-design/BUILD_ORDER.md.
Show me all checked and unchecked steps.
Then continue from the first unchecked step."

---

## Cross-Path System Summary

These cross-path bonuses apply across all paths.
Full logic is in systems/daily-quest-logic.md.

Bonus pairs:
- Cold shower: Fitness Warrior + Health Alchemist
  +20 EXP both complete same day
- Breathwork: Mindset Sage + Health Alchemist
  +20 EXP both complete same day
- Deep work: Discipline Knight + Grind Visionary
  +20 EXP both complete same day
- 5AM wake up: Mindset Sage + Discipline Knight
  +25 EXP both complete same day
- Reading: Mindset Sage + Grind Visionary
  +25 EXP both complete same day

Maximum one cross-path bonus per day.
Cross-path bonuses exempt from Recovery day filter.

Cross-path identity titles:
- Warrior-Sage: Fitness Warrior + Mindset Sage
  active 7 consecutive days both
- The Optimized Human: Fitness + Mindset + Health
  active 7 consecutive days all three
- The Complete Human: Fitness + Mindset + Health
  + Discipline active 7 consecutive days all four
- The Renaissance Human: All five paths active
  7 consecutive days — highest title in app

---

## Core Game Constants

Level progression formula:
EXP needed = level squared times 50 minus 50

Rank unlock by player level:
- D rank: Level 1
- C rank: Level 5
- B rank: Level 10
- A rank: Level 20
- S rank: Level 30

Multi-path unlock:
- Primary path chosen on signup
- Second path unlocks after 30 consecutive days
- Each additional path unlocks every 30 days
  of consistency on all currently active paths
- Never push multi-path before Day 30

Freedom Day token overflow:
- Maximum 3 tokens stacked
- If 4th token earned while at max 3
  award 200 bonus EXP instead

Discipline Code content moderation:
- Filter runs server-side before saving
- If flagged user must rewrite before saving
- Previous versions saved to profile history

Supplement disclaimer placement (Health Alchemist):
- Top of Setup Guide before any recommendations
- Bottom of Setup Guide
- One line note on every supplement card

---

## Sixth Path Placeholder

A sixth locked path slot must appear on the
path selection screen.

Visual: same card style as other paths but
greyed out with lock icon.
Label: Coming Soon
Tap response: "A new path is being forged.
Stay disciplined Hunter — it is coming."
Non-selectable. No functionality behind it.

---

## Expansion Packs (Future — Do Not Build Now)

Plan the Quest model to support future expansion
packs by including a pack_id field.
Do not build pack UI or logic now.
Just ensure the data model is extensible.