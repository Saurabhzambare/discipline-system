# Execution Plan Template

Use this template before making non-trivial changes.

This template is meant for both humans and AI coding agents.

Non-trivial changes include anything that affects:

- architecture
- models
- migrations
- API contracts
- business logic
- progression logic
- quest completion behavior
- multi-file feature behavior
- subscription/access behavior
- leaderboard behavior
- privacy rules
- device integration
- social features

---

# Task summary

Describe the task in 2–5 clear sentences.

Include:

- what is being changed
- why it is being changed
- what outcome is expected

---

# Relevant docs to read

List the documents that must be reviewed before implementation.

Typical examples:

- `README.md`
- `AGENTS.md`
- `docs/architecture.md`
- relevant phase document
- roadmap / product system docs if relevant

Mark each as:

- [ ] read
- [ ] not needed

Example:

- [ ] `README.md`
- [ ] `AGENTS.md`
- [ ] `docs/architecture.md`
- [ ] `docs/phase-3-progression.md`

---

# Current code areas to inspect

List the files, folders, or modules that should be inspected before making changes.

Examples:

- `backend/players/models.py`
- `backend/players/views.py`
- `backend/players/serializers.py`
- `backend/quests/models.py`
- `backend/quests/services.py`
- `backend/quests/views.py`
- `backend/users/models.py`
- existing tests related to the feature
- relevant frontend components if UI is involved

Add notes for why each area matters.

---

# Current understanding

Summarize what the code appears to already do.

Include:

- current related behavior
- known data flow
- existing patterns that should be followed
- anything unclear that still needs confirmation

This section should be based on inspection, not guesses.

---

# System boundary check

Which product system does this task belong to?

Choose one or more:

- Identity
- Player Profile & Progression
- Quest & Completion
- Social & Relationships
- Privacy & Visibility
- Commerce & Subscription
- Device & Activity Sync
- Experience Layer (UI / immersion)

Explain why the task belongs there.

This is required to avoid mixing unrelated responsibilities.

---

# Current phase / roadmap fit

State which roadmap phase this task belongs to.

Examples:

- Phase 4 — Frontend Foundation
- Phase 5 — Quest Expansion
- Phase 7 — Competitive Systems

If the task does not fit the current phase cleanly, explain why it is still being done now.

---

# Current core-loop impact

Does this task directly strengthen the core loop?

Core loop:

```text
Quest
→ Completion
→ EXP
→ Level
→ Streak
→ Repeat