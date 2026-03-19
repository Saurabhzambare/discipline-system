# Phase 5 — Quest Expansion System

## Purpose of this document

This document defines the scope and implementation direction for **Phase 5: Quest Expansion System**.

Its goal is to make Phase 5 clear for both:

- the project owner
- future contributors
- AI coding agents

This phase should be implemented in a clean, minimal, architecture-respecting way.

---

# 1. Phase goal

Phase 5 expands the quest system beyond basic completion into a more dynamic, engaging, and scalable system.

This phase introduces or formalizes:

- quest categories
- path-based quests
- dynamic daily quests
- recurring quest logic
- difficulty levels
- reward scaling
- improved streak interaction with quests

This is the phase where the system evolves from a simple task list into a structured habit and progression engine.

---

# 2. Why this phase matters

Before Phase 5:

- quests exist
- quests can be completed
- quests give EXP

But the system is still relatively static.

With Phase 5:

- quests become structured and meaningful
- player identity (path) affects gameplay
- daily engagement becomes stronger
- habit loops become more consistent
- progression becomes more engaging and varied

This phase strengthens long-term retention and sets up future systems like challenges, leaderboards, and social competition.

---

# 3. Included scope

Phase 5 includes the following core areas.

---

## 3.1 Quest categories

Quests should be organized into meaningful categories.

Examples:

- fitness
- discipline
- productivity
- health
- recovery

Expected direction:

- categories are explicit and stored in a structured way
- quests belong to one or more categories
- categories can be extended in the future

---

## 3.2 Path-based quests

Quests should be influenced by the player's selected path.

Examples:

- Gym → workout-related quests
- Runner → running-based quests
- Discipline → general self-improvement quests
- Tournament → structured competitive quests (basic version for now)
- 75 Hard → strict predefined rules (simplified version for now)

Expected direction:

- player path influences which quests are assigned
- system remains flexible for adding new paths later
- avoid hardcoding path logic in a brittle way

---

## 3.3 Dynamic daily quests

The system should generate or assign daily quests.

Expected direction:

- quests refresh daily
- players receive a set of daily quests
- logic is deterministic or controlled (not random chaos)
- quest assignment is testable

---

## 3.4 Recurring quests

Support recurring quest patterns.

Examples:

- daily workout
- drink water
- study session
- morning routine

Expected direction:

- recurrence logic is explicit
- recurring quests integrate cleanly with daily quest assignment
- avoid duplicating logic across endpoints

---

## 3.5 Difficulty levels

Quests may have different difficulty levels.

Examples:

- easy
- medium
- hard

Expected direction:

- difficulty affects EXP reward
- difficulty is clearly defined and stored
- logic remains simple and extensible

---

## 3.6 Reward scaling

EXP rewards should scale based on:

- difficulty
- quest type
- possibly streak or consistency (optional for this phase, keep simple)

Expected direction:

- reward logic is explicit and testable
- no hidden reward rules scattered across the codebase
- progression system remains predictable

---

## 3.7 Improved streak interaction

Streak logic should integrate better with quest behavior.

Expected direction:

- streak depends on meaningful completion patterns
- streak rules remain explicit and testable
- avoid spreading streak logic across multiple endpoints

---

# 4. Excluded scope / non-goals

The following items are explicitly out of scope for this phase unless separately approved.

## Not included by default

- achievements system
- badges/titles
- social feed
- groups or friends
- leaderboards
- player challenges
- tournaments (advanced version)
- subscription/premium gating
- merchandising system
- smartwatch/device integration
- full analytics system
- advanced UI redesign
- full onboarding redesign
- full path progression system

## Also out of scope

- broad backend refactors
- splitting the backend into new apps unnecessarily
- rewriting Phase 3 logic unless required for clean integration
- mixing multiple future phases into this implementation

Phase 5 should stay focused.

---

# 5. Current architecture position for this phase

## Important rule

Do **not** introduce a major structural refactor.

The current backend structure remains:

- `players`
- `quests`
- `users`
- `core`

## Expected architectural direction

- quest logic remains in `quests`
- player progression remains in `players`
- quest completion continues to orchestrate progression updates
- new quest logic should be implemented through services where appropriate
- avoid placing complex logic in views or serializers

---

# 6. Recommended implementation direction

---

## 6.1 Inspect current quest system first

Before implementing:

- inspect `quests/models.py`
- inspect `quests/services.py`
- inspect current quest completion flow
- inspect how EXP is currently assigned
- identify reusable patterns

Do not rebuild what already exists.

---

## 6.2 Suggested responsibility split

### `quests`

Primary owner of:

- quest definitions
- quest categories
- difficulty
- recurrence logic
- daily quest assignment logic
- orchestration of quest completion

### `players`

Owner of:

- progression state (EXP, level, streak)
- player path selection
- player-specific quest state if needed

---

## 6.3 Service-layer preference

Preferred direction:

- quest assignment logic handled via services
- quest completion handled via services
- reward logic handled via services
- progression updates triggered through service calls

Possible structure:

- `quests/services.py` handles:
  - daily quest assignment
  - quest completion orchestration
- `players/services.py` or `players/progression.py` handles:
  - EXP updates
  - level updates
  - streak updates

---

## 6.4 Avoid hardcoding

Avoid:

- fixed quest sets with no flexibility
- rigid path logic
- hardcoded reward values scattered across files

Keep systems simple but extendable.

---

# 7. Acceptance criteria

Phase 5 is considered complete when the following are true.

## Functional acceptance criteria

- quests are categorized
- player path influences quest assignment
- daily quests are generated or assigned
- recurring quests behave correctly
- difficulty levels affect rewards
- EXP rewards scale appropriately
- streak logic integrates cleanly with quest completion

## Code quality acceptance criteria

- logic is not buried in views or serializers
- service-layer style is used where appropriate
- app boundaries are respected
- no unnecessary refactor occurred
- code remains readable and maintainable

## Documentation acceptance criteria

- new quest behaviors are documented where needed
- assumptions are documented in implementation summary
- architecture alignment is maintained

## Testing acceptance criteria

- quest assignment logic is tested
- reward scaling is tested
- difficulty behavior is tested
- recurring quest logic is tested
- streak interaction with quests is tested

---

# 8. Testing expectations

## Recommended test focus

- daily quest generation correctness
- path-based quest assignment
- recurring quest behavior
- EXP reward scaling
- difficulty-based reward differences
- streak updates tied to quest completion

## Testing principle

Test business logic at the service level where possible.

Avoid relying only on endpoint-level tests.

---

# 9. Architecture rules specific to this phase

## Rule 1
Do not perform a major refactor.

## Rule 2
Do not create new apps unless clearly necessary.

## Rule 3
Do not bury quest logic in views.

## Rule 4
Do not bury reward logic in serializers.

## Rule 5
Keep quest logic in the quest domain.

## Rule 6
Keep progression logic in the player domain.

## Rule 7
Keep systems explicit and testable.

---

# 10. Suggested implementation checklist

Before coding:

- read `AGENTS.md`
- read `docs/architecture.md`
- read `docs/web-development-roadmap.md`
- inspect current quest system
- create execution plan
- list assumptions
- list risks

During coding:

- keep logic explicit
- use services where appropriate
- avoid duplication
- keep scope focused

After coding:

- explain changed files
- explain assumptions
- explain any API changes
- update docs if needed

---

# 11. Practical summary

Phase 5 should transform the quest system from simple tasks into a structured progression engine.

That means:

- quests should feel purposeful
- daily engagement should feel guided
- progression should feel more dynamic

But implementation must remain disciplined:

- no premature advanced systems
- no unnecessary refactors
- no mixing of unrelated features
- no hidden business logic

Keep it structured, testable, and scalable.