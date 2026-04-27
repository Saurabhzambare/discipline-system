# Phase 5 — Smooth UI and Quest Expansion

## Purpose of this document

This document explains what was implemented in **Phase 5** for Discipline System.

Phase 5 was split into two coordinated parts:

- **Phase 5A**: Smooth Game Feel / UX Polish
- **Phase 5B**: Quest Expansion System

The implementation goal was to improve reliability and product feel without broad refactors.

---

# 1. Phase purpose

Phase 5 upgrades both the user experience and the quest engine.

Before Phase 5:

- core gameplay worked
- quests were globally listed
- path selection existed only in frontend local storage
- quest metadata and assignment behavior were limited

After Phase 5:

- UX feedback is clearer during auth and quest actions
- session-expiry behavior is smoother
- frontend EXP progress now matches backend progression logic
- backend persists player path
- quests include structured metadata
- daily quest assignments are persisted per player per day
- reward scaling is explicit and service-driven

---

# 2. Scope

## Included

- login/signup/dashboard/profile/onboarding UX polish
- better loading/disabled/error/success feedback
- frontend/backend progression consistency fix
- backend player path persistence and update endpoint
- quest metadata expansion (category, difficulty, recurrence, optional path target)
- deterministic daily quest assignment
- scaled reward handling via service rules
- updated completion flow against daily assignment
- tests for key service/API behaviors

## Excluded

- achievements and badges
- social features
- leaderboards
- tournaments/raids systems
- notifications and penalties
- major frontend redesign
- major backend refactor

---

# 3. Phase 5A summary (Smooth Game Feel)

Implemented improvements:

- Added better session-expiry handling in API/auth flow.
- Added top-level flash feedback for success/error messages.
- Added stronger loading/disabled behavior on auth forms and path selection.
- Improved dashboard error presentation for action failures.
- Updated quest cards to show richer metadata and status.
- Fixed EXP progress bar math to match backend level rule:
  - backend rule: each 100 EXP = +1 level
  - frontend progress now displays `exp % 100` toward next level.

---

# 4. Phase 5B summary (Quest Expansion System)

Implemented upgrades:

1. **Backend-owned player path**
   - `Player.path` persisted with validated choices.
   - Added `PATCH /api/player/path/` endpoint.

2. **Quest metadata expansion**
   - Added `category`, `difficulty`, `recurrence`, `path_target` fields to quests.

3. **Persisted daily assignment model**
   - Added `PlayerDailyQuestAssignment` model with:
     - player
     - quest
     - assignment_date
     - assigned_exp_reward
     - completed state

4. **Deterministic assignment behavior**
   - Daily assignment generated in service layer.
   - Repeated calls on same day reuse persisted assignments.
   - Assignment filters respect path targeting and recurrence schedule.

5. **Reward scaling**
   - Service-level explicit difficulty multipliers:
     - easy: 1.0
     - medium: 1.3
     - hard: 1.6
   - Scaled reward saved in assignment and used during completion.

6. **Streak integration**
   - Preserved first-completion-per-day streak behavior.
   - Completion now requires today’s assignment and marks assignment completed.

---

# 5. Architecture decisions

- Kept business logic in services (`quests/services.py`).
- Kept views thin (`quests/views.py`, `players/views.py`).
- Kept serializers focused on representation/validation.
- Preserved app boundaries:
  - `quests` owns assignment/reward/completion orchestration
  - `players` owns path/profile state

No new app was introduced.

---

# 6. Data model changes

## players

- `Player.path` added.

## quests

- `Quest.category` added.
- `Quest.difficulty` added.
- `Quest.recurrence` added.
- `Quest.path_target` added.
- `PlayerDailyQuestAssignment` added.

---

# 7. API changes

## Updated

- `GET /api/player/me/`
  - now includes `path` and `path_display`.

- `GET /api/quests/`
  - now returns assigned daily quest records (per player/day) with metadata and assignment completion state.

- `POST /api/quests/complete/`
  - now validates today assignment existence before completion.
  - returns scaled reward values.

## New

- `PATCH /api/player/path/`
  - body: `{ "path": "runner|gym|discipline|tournament|75_hard" }`
  - response: updated player payload.

---

# 8. Frontend changes

- API client now supports path update endpoint.
- Session-expiry handling clears tokens and gives clearer message.
- App uses backend path value instead of localStorage as source of truth.
- Onboarding persists selected path via API.
- Dashboard and quest cards show improved status/error clarity.
- EXP progress display aligned with backend linear leveling rule.
- Forms/buttons use disabled/loading states consistently.

---

# 9. Testing coverage

Added/updated tests for:

- player path persistence and update endpoint
- deterministic daily assignment behavior
- path-targeted assignment behavior
- recurring schedule checks
- reward scaling by difficulty
- completion requiring assignment
- streak behavior with assignment completion
- quest list and quest completion API responses

---

# 10. Acceptance checklist

## Phase 5A

- [x] clearer loading/disabled states in major flows
- [x] clearer error/success feedback
- [x] smoother session-expiry behavior
- [x] frontend EXP progress matches backend logic

## Phase 5B

- [x] backend persists player path
- [x] quests include richer metadata
- [x] daily assignments are persisted and deterministic
- [x] rewards scale through explicit service rules
- [x] streak/completion behavior remains coherent
- [x] tests cover core new rules

---

# 11. Notes and future considerations

- Current assignment strategy intentionally stays minimal and deterministic.
- Future improvements can add assignment caps/weights while preserving service boundaries.
- If weekly recurrence needs custom weekday configuration, add explicit fields in a future phase.
- Frontend could later show assignment_date and completion timestamp for richer history.
