# Test Audit — 2026-04-04

## Scope
Full repository test audit only (no feature implementation), covering backend Django checks/tests, frontend build/lint checks, and test-related configuration/docs alignment.

## Inventory

### Backend
- Django system checks via `python manage.py check`.
- Django test modules:
  - `backend/core/tests.py`
  - `backend/users/tests.py`
  - `backend/social/tests.py`
  - `backend/players/tests.py`
  - `backend/quests/tests.py`
  - `backend/quests/tests_session5.py`

### Frontend
- `npm run lint` (ESLint).
- `npm run build` (Vite production build).
- No frontend unit/integration test script present in `frontend/package.json`.

### CI / Tooling config discovered
- `docker-compose.yml`
- No `.github/workflows/*` CI config found in repository.

## Executed Commands (audit run)
1. `python manage.py check`
2. `python manage.py test`
3. `python manage.py test core users social paths players quests`
4. `python manage.py test users`
5. `python manage.py test social`
6. `python manage.py test players`
7. `python manage.py test quests.tests`
8. `python manage.py test quests.tests_session5`
9. `npm run lint`
10. `npm run build`

## Result Summary

### Passing
- Django system checks pass.
- `users` tests pass.
- `social` tests pass.
- `quests.tests_session5` pass.
- Frontend production build passes.

### Failing
- `players` tests: 2 failures caused by stale path assumptions (`gym`, `runner`) and old expected display values.
- `quests.tests`: 4 failures + 5 errors.
  - Errors from tests calling legacy assignment wrapper without path onboarding/selection setup.
  - Failures from outdated EXP threshold expectations and old one-quest daily list assumptions.
- `npm run lint`: 9 ESLint errors (unused variables and React Fast Refresh export rule violations).

## Diagnosis Categories

### Stale test assumptions (primary)
- Player path tests still assert old pre-Phase-5B path codes (`gym`, `runner`) that are no longer valid choices.
- Quest progression tests assume pre-redesign level thresholds (e.g., 100 EXP -> level 2) instead of current quadratic formula.
- Legacy quest assignment/completion tests do not set up `UserPathSelection` onboarding state required by Session 5 lineup flow.
- Quest list API test assumes exactly one returned quest, but lineup model can include universal + path items.

### Real code quality / tooling issues
- Frontend lint fails due to real source warnings elevated to errors:
  - Unused imports/variables in `App.jsx` and `GroupsPage.jsx`.
  - `react-refresh/only-export-components` violations in `PathContext.jsx`.

### Environment/setup issues
- None blocking backend/frontend checks in this environment.
- Non-blocking npm warning about `http-proxy` env config observed.

### Docs/code mismatch
- Test suite portions (`players/tests.py`, `quests/tests.py`) are inconsistent with documented Phase 5B path model and onboarding-dependent quest generation.

## Priority Fix Order (recommended)
1. Rewrite/replace stale `players/tests.py` and stale sections in `quests/tests.py` to align with Phase 5B architecture.
2. Keep `quests/tests_session5.py` as baseline and expand around current lineup/onboarding contract.
3. Resolve frontend ESLint errors to restore a clean quality gate.
4. Add CI workflows that run backend checks/tests + frontend lint/build on every PR to prevent drift recurrence.

## Process Mistakes Identified
- Architecture changed (Phase 5B), but legacy tests were not migrated in same session(s).
- Backward-compat wrappers remained while tests still target old semantics, obscuring intended contract changes.
- No CI gate enforcing synchronized updates between gameplay redesign docs and tests.

## Prevention Recommendations
- Treat phase docs as contract changes requiring a mandatory “test migration checklist” in the same PR.
- Add PR template checkbox: “Updated or removed stale tests affected by architectural change.”
- Maintain a clear `legacy` vs `current` test partition with explicit deprecation dates.
- Enforce CI so stale tests/lint drift is caught immediately.
