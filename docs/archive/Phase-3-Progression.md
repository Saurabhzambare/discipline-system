
---
## Purpose of this document

This document defines the scope and implementation direction for **Phase 3: Progression**.

Its goal is to make Phase 3 clear for both:
- the project owner
- future contributors
- AI coding agents

This phase should be implemented in a clean, minimal, architecture-respecting way.

---
# 1. Phase goal

Phase 3 adds the first real progression loop to the system.

This phase introduces or formalizes:

- EXP rewards when completing quests
- level progression logic
- streak tracking
- service-layer progression behavior
- progression-related API output where needed
- tests for progression logic

This is the phase where the app begins to feel like an actual game system rather than only a task tracker.

---
# 2. Why this phase matters

Before Phase 3, the app can list quests and record actions.

Phase 3 makes those actions meaningful.

Without progression:
- quest completion is just a record
- the app does not yet fully deliver the Solo Leveling-inspired loop

With progression:
- actions have visible consequences
- users see measurable growth
- the system starts reinforcing consistency
- the dashboard becomes a true status/progression window

This is a foundational product phase.

---

# 3. Included scope

Phase 3 includes the following core areas.

## 3.1 EXP rewards
When a quest is completed, the system should be able to award EXP based on the quest’s EXP reward definition.

Expected direction:
- EXP reward comes from the quest domain
- EXP is applied to the player’s progression state

---

## 3.2 Level progression
The system should determine how player level changes as EXP increases.

Expected direction:
- progression rules should be explicit and testable
- level calculation should not be hidden in views
- level-up behavior should be deterministic

---

## 3.3 Streak tracking
The system should track consistency in a clear, defined way.

Expected direction:
- streak logic must be explicitly documented in code and tests
- edge cases should be considered
- streak updates should happen through business logic, not scattered conditionals in multiple endpoints

---

## 3.4 Progression service-layer logic
Core progression behavior should be handled through a service-layer approach where appropriate.

Expected direction:
- quest completion flow may orchestrate progression updates
- progression logic should remain centralized enough to stay testable and maintainable

---

## 3.5 API exposure of progression state
If needed for frontend behavior, API responses should expose updated progression information such as:
- EXP
- level
- streak
- level-up result metadata if useful

The exact shape should follow current API patterns and avoid unnecessary contract churn.

---

## 3.6 Tests
Progression logic must be covered by tests appropriate to the current project style.

This phase is not complete without meaningful test coverage for the core gameplay rules it introduces.

---

# 4. Excluded scope / non-goals

The following items are explicitly out of scope for this phase unless separately approved.

## Not included by default
- achievements system
- badges/titles
- penalties
- boss battles
- skill trees
- social feeds
- leaderboard/community ranking
- premium subscriptions
- advanced analytics
- large dashboard redesign
- major architectural refactor
- creation of a brand-new dedicated progression Django app by default

## Also out of scope
- broad cleanup of unrelated files
- restructuring the entire repository for theoretical future scale
- mixing multiple future phases into this implementation

Phase 3 should stay focused.

---

# 5. Current architecture position for this phase

## Important rule
Do **not** assume that a new progression app must be created now.

The current backend structure already includes:
- `players`
- `quests`
- `users`
- `core`

That is sufficient for a clean Phase 3 implementation.

## Expected architectural direction
- progression state should live with the player domain
- quest completion behavior remains part of quest-domain flow
- progression rules should live in service-layer code where appropriate
- views should orchestrate, not contain core gameplay rules
- serializers should validate/represent, not drive progression mechanics

---

# 6. Recommended implementation direction

This section describes the intended shape, not a forced exact file path.

## 6.1 First inspect current code
Before implementing:
- inspect `players`
- inspect `quests`
- inspect `quests/services.py`
- inspect current models/views/serializers/tests
- identify what progression-related fields or behavior already exist

Do not build from assumptions if the code already contains useful foundations.

---

## 6.2 Suggested responsibility split

### `players`
Likely home for:
- EXP state
- level state
- streak state
- progression-related player data
- progression calculation/update service helpers

### `quests`
Likely home for:
- quest completion action
- quest reward source data
- orchestration that triggers progression update

### `core`
Should remain lightweight/shared and should not become the main home for Phase 3 gameplay logic.

---

## 6.3 Service-layer preference
Preferred direction:

- quest completion flow triggers a service
- service records completion and coordinates progression changes
- progression rules are applied through explicit service logic
- API response returns updated state where needed

Possible implementation shapes:
- `quests/services.py` orchestrates quest completion and calls player progression helpers
- `players/services.py` or `players/progression.py` handles EXP/level/streak rules

The exact shape should match the existing code style, but the separation of concerns should remain clear.

---

# 7. Acceptance criteria

Phase 3 is considered complete when the following are true.

## Functional acceptance criteria
- completing a quest awards EXP
- player level updates correctly according to defined progression rules
- streak updates correctly according to defined streak rules
- progression updates are not scattered across views/serializers in an ad hoc way
- progression data is accessible through relevant API output if needed by the frontend

## Code quality acceptance criteria
- implementation respects current app boundaries
- business logic is placed in a service-layer style approach where appropriate
- unrelated files were not modified without reason
- code remains readable and maintainable
- implementation avoids unnecessary structural refactors

## Documentation acceptance criteria
- any new API behavior is documented if needed
- important assumptions are documented in the implementation summary
- architectural decisions remain aligned with `docs/architecture.md`

## Testing acceptance criteria
- core progression logic is covered by tests
- quest completion to progression behavior has meaningful verification
- key edge cases are tested

---

# 8. Testing expectations

At minimum, testing should cover the most important progression rules introduced in this phase.

## Recommended test focus
- quest completion awards correct EXP
- EXP accumulates correctly across multiple completions
- level progression updates correctly at thresholds
- streak increments correctly on valid consecutive behavior
- streak resets or behaves correctly on broken sequences, depending on defined rules
- duplicate completion or invalid completion cases are handled correctly if relevant to current business rules

## Testing principle
Do not rely only on endpoint-level tests if the core business logic can be tested more directly in services.

Progression rules should be easy to verify in isolation.

---

# 9. Architecture rules specific to this phase

## Rule 1
Do not perform a major refactor just to implement progression.

## Rule 2
Do not create a new progression app by default.

## Rule 3
Do not place core progression rules directly in views unless an extremely small project-specific reason exists.

## Rule 4
Do not bury EXP/level/streak rules inside serializers.

## Rule 5
Keep progression state near the player domain.

## Rule 6
Let quest completion flows orchestrate progression updates rather than duplicating logic across endpoints.

## Rule 7
Prefer explicit and testable business rules over hidden model/view side effects.

---

# 10. Suggested implementation checklist

Before coding:
- read `AGENTS.md`
- read `docs/architecture.md`
- inspect relevant `players` and `quests` files
- create a short execution plan
- list assumptions
- list risks

During coding:
- keep changes scoped
- preserve app boundaries
- keep progression logic explicit
- add/update tests

After coding:
- explain changed files
- explain any assumptions
- explain any API response changes
- update docs if needed

---

# 11. Practical summary

Phase 3 should make the app feel like a progression system.

That means:
- quest completion must do more than create a record
- it must advance the player meaningfully

But it should be implemented with discipline:

- no premature new app
- no unnecessary refactor
- no gameplay logic hidden in the wrong layers
- no broad unrelated changes

Keep it minimal, clean, testable, and future-friendly.