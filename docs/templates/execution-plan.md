# Execution Plan Template

Use this template before making non-trivial changes.

Non-trivial changes include anything that affects:
- architecture
- models
- migrations
- API contracts
- business logic
- progression logic
- quest completion behavior
- multi-file feature behavior

This template is meant for both humans and AI coding agents.

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
- relevant phase doc (example: `docs/phase-3-progression.md`)

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
- `backend/quests/models.py`
- `backend/quests/services.py`
- `backend/quests/views.py`
- `backend/players/serializers.py`
- existing tests related to the feature

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

# Assumptions

List assumptions being made before implementation.

Examples:
- player progression state already exists in the `players` app
- quest completion currently flows through `quests/services.py`
- frontend depends on a specific response shape
- current tests establish a preferred service-layer pattern

If an assumption is high-risk, label it clearly.

---

# Files likely to change

List the files most likely to be updated.

Examples:
- models
- serializers
- views
- services
- urls
- tests
- docs

Do not include unrelated files.

---

# Risks / concerns

List the main risks before implementation.

Examples:
- hidden existing behavior may conflict with the planned change
- docs may not match current code
- response contract changes may affect frontend
- progression logic may need edge-case clarification
- model changes may require migrations

Be specific.

---

# Proposed implementation approach

Describe the intended implementation in a short step-by-step form.

Keep it practical.

Example format:
1. inspect current models and service flow
2. identify where progression state currently lives
3. add or update service-layer progression logic
4. connect quest completion flow to progression update
5. update API output if needed
6. add/update tests
7. update docs if necessary

---

# Scope boundaries

State what is explicitly in scope and out of scope.

## In scope
- specific feature behavior
- directly related tests
- small doc updates if needed

## Out of scope
- unrelated cleanup
- broad refactors
- future-phase features unless explicitly requested

This prevents silent scope creep.

---

# Approval checkpoint

Use this section for large or risky work.

If the task changes any of the following:
- architecture
- models
- migrations
- API contracts
- progression rules
- quest completion behavior

then summarize:

## Planned change summary
Brief summary of the intended change.

## Why this approach
Why this implementation path fits the current architecture.

## What could go wrong
Any important risk or uncertainty.

## Approval needed?
- [ ] yes
- [ ] no

For large or risky work, wait for approval before implementation.

---

# Verification steps

Describe how the change will be verified.

Examples:
- run backend tests
- test the endpoint manually
- verify progression values after quest completion
- confirm no unrelated endpoints broke
- confirm docs reflect behavior

Be specific.

---

# Definition of done

The task is done when:

- [ ] relevant docs were checked first
- [ ] relevant code areas were inspected
- [ ] assumptions were documented
- [ ] architecture boundaries were respected
- [ ] only relevant files were changed
- [ ] tests were added or updated where appropriate
- [ ] docs were updated if needed
- [ ] changed files can be explained clearly
- [ ] API changes were documented if applicable

---

# Post-implementation summary

Complete this section after coding.

## Changed files
List every changed file.

## Why each file changed
One short explanation per file.

## Tests added/updated
Summarize test coverage changes.

## Docs updated
List any documentation changes.

## Follow-up items
List any non-blocking future work discovered during implementation.