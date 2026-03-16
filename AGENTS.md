# 1. Project overview

## Project name
**Discipline System**

## Product idea
A Solo Leveling–inspired gamified self-improvement web app.

It converts real-life disciplined actions into game-style progression:

- User = Player
- Habits / workouts / study tasks = Quests
- Completing quests = EXP gain
- EXP gain = level progression
- Consistency = streak growth
- Dashboard = status window

## One-line definition
**A real-life RPG-style discipline app where daily habits are turned into quests and converted into progression through EXP, levels, and streaks.**

---
# 2. Repository intent

This repository is designed to support both:
- human-led development
- AI-assisted implementation

The main goal is to keep the project:
- clean
- understandable
- maintainable
- scalable over time
- safe for incremental feature delivery

This is an evolving product, not a throwaway demo.

---
# 3. Read-first documentation rules

Before implementing any non-trivial task, read the relevant documentation first.

## Always read
- `README.md`
- `AGENTS.md`

## Read before architecture-sensitive changes
- `docs/architecture.md`

## Read before phase-specific work
- the relevant phase document in `docs/`

Example:
- progression work -> `docs/phase-3-progression.md`

## Read before planning non-trivial changes
- `docs/templates/execution-plan.md`

---
# 4. Architecture rules

## Current backend structure must be respected

Current backend apps include:

- `core`
- `users`
- `players`
- `quests`

Do **not** assume a major structural refactor is required.

## Important repo-specific architecture decisions

- `core` is intended to remain lightweight/shared
- `core` is **not** the main business domain app
- `players`, `quests`, and `users` already exist as domain-level apps
- `quests/services.py` already exists and signals service-layer usage
- large migration-heavy refactors are not the default path

## Do not do these unless explicitly asked
- do not split the entire backend into a new app structure
- do not move everything into `core`
- do not create a brand-new progression app by default
- do not perform large-scale reorganizations just because they are theoretically cleaner

## Preferred approach
- keep existing structure unless a real problem is found
- make minimal, safe, reviewable changes
- extend current app boundaries thoughtfully
- optimize for maintainability and future extensibility

---
# 5. Responsibility boundaries

Use these boundaries unless the code clearly indicates otherwise.

## `core`
Use for:
- health endpoints
- small shared/project-level functionality
- lightweight cross-cutting pieces

Do not use `core` as the default home for gameplay/business logic.

## `users`
Use for:
- authentication
- account identity
- user model/account-level concerns

## `players`
Use for:
- player profile/state
- progression-related player data
- EXP/level/streak data and related domain state

## `quests`
Use for:
- quest definitions
- quest completion flows
- quest-domain operations
- quest service orchestration

---
# 6. Business logic rules

## Preferred rule
Keep non-trivial business logic out of views when possible.

## Views should mainly do
- request handling
- permission checks
- orchestration
- calling services/selectors/serializers
- returning responses

## Serializers should mainly do
- input validation
- output formatting
- object transformation
- simple field-level logic

## Serializers should not contain
- core gameplay rules
- EXP/level/streak progression algorithms
- complex quest completion behavior

## Service-layer preference
If a task touches:
- EXP
- levels
- streaks
- quest completion rules
- progression rules
- cross-model updates

then prefer a service-layer approach where appropriate.

Examples:
- `quests/services.py`
- `players/services.py`
- `players/progression.py`

Exact implementation can follow existing code style, but the direction should remain service-oriented and explicit.

---
# 7. Progression-specific rules

If a task touches:
- EXP rewards
- level progression
- streak tracking
- quest completion behavior
- progression API output

then:

1. inspect current `players` and `quests` code first
2. determine what already exists
3. preserve current app boundaries
4. avoid placing progression rules directly inside views
5. avoid hiding gameplay rules inside serializers
6. keep progression state close to the player domain
7. let quest completion flows call progression logic through services where appropriate

---
# 8. Workflow rules

## For non-trivial work
Before implementation:

1. read the docs
2. inspect relevant files
3. create a short execution plan
4. summarize assumptions
5. summarize risks
6. if the task is large or risky, wait for approval before major changes
7. implement only after planning

Use:
- `docs/templates/execution-plan.md`

## Non-trivial means any task that changes
- architecture
- models
- migrations
- API contracts
- business logic
- progression logic
- quest completion behavior
- multi-file feature behavior

## Small trivial tasks may skip full planning
Examples:
- typo fixes
- comment cleanup
- tiny doc corrections
- very small non-behavioral formatting changes

When in doubt, plan first.

---
# 9. Scope-control rules

## Do not modify unrelated files
Only change files necessary for the task.

## Do not broaden scope silently
If you discover a related problem:
- mention it
- note whether it blocks the task
- do not automatically expand into a large refactor

## If docs and code conflict
Report the conflict first.

Do not silently “pick one” for major architectural decisions.

## If architecture is unclear
Inspect the code and explain your assumptions before implementation.

---
# 10. Documentation rules

When changes affect behavior, structure, or contracts, update docs where appropriate.

## Update documentation when relevant
Examples:
- API response shape changed
- progression rules changed
- new service-layer pattern introduced
- new setup steps added
- architecture boundaries clarified

## Keep docs practical
Do not write inflated or generic documentation.
Prefer short, accurate, repository-specific explanations.

---
# 11. Testing rules

Add or update tests where appropriate, especially when changing:

- business logic
- quest completion logic
- progression rules
- EXP/level/streak behavior
- API outputs that expose progression behavior

## Test focus areas
- service logic
- quest completion behavior
- progression calculations
- streak edge cases
- level threshold behavior
- regression protection

## Testing principle
Business rules should be testable without needing to test everything only through views.

---
# 12. Change explanation rules

After implementation, clearly explain:

- which files changed
- why each file changed
- any assumptions made
- any risks or follow-up items
- any API changes
- any migration impacts
- any docs updated

This explanation should be concise but complete.

---
# 13. Code style rules

Prioritize:
- readability
- maintainability
- explicit naming
- predictable flow
- simple composition

Avoid:
- clever abstractions with low readability
- hidden side effects
- mixing unrelated concerns
- premature generalization
- large framework-style patterns unless already justified by the codebase

---
# 14. Future extensibility guidance

The system is expected to grow later into features such as:
- achievements
- daily/weekly quests
- analytics
- leaderboard/community
- premium features
- broader SaaS behavior

Write code that supports future growth, but do not force future architecture too early.

Good rule:
**make the next change easy without rebuilding the whole project now.**

---
# 15. Done means checklist

A task is not fully done unless these are true where applicable:

- relevant docs were checked first
- architecture was respected
- relevant existing files were inspected
- assumptions were identified
- unrelated files were not changed
- service-layer approach was used where appropriate
- core gameplay logic was not buried inside views/serializers
- tests were added or updated where appropriate
- docs were updated if behavior/contracts changed
- changed files were clearly explained
- API changes were documented if needed

---
# 16. Execution plan requirement template reference

For non-trivial tasks, use:

- `docs/templates/execution-plan.md`

That plan should be completed before implementation work begins.

---
# 17. Final working rule

When unsure:
- inspect first
- document assumptions
- keep the change small
- preserve current structure
- prefer clarity over theoretical perfection