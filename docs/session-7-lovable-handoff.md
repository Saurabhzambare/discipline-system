# Session 7 Lovable Handoff (Contract-First)

Date: 2026-04-12

## Final Session 7 Endpoints

### Quest board / lineup
- `GET /api/quests/daily/?date=YYYY-MM-DD` (date optional)
- Includes:
  - `lineup.items[]` with `slot_type`, `is_locked`, `is_carried_over`, `selection_reason`, `feedback`
  - `lineup.progressive_reveal` with backend-driven `ui_mode`, `day_on_path`, `slot_labels_visible`
  - `lineup.features_unlocked` and `swaps_remaining`
  - top-level `missed_day` and `missed_day_return`

### Completion ring
- `GET /api/quests/completion-ring/?date=YYYY-MM-DD`
- Returns aggregate completion and path breakdown for API-driven ring rendering.

### End-of-day summary
- `GET /api/quests/summary/?date=YYYY-MM-DD`
- Alias supported: `GET /api/quests/summary/today/`
- Returns summary payload including:
  - identity/date/day/streak
  - completed/total
  - exp totals and path breakdown
  - progress to next level
  - highlight
  - embedded tomorrow preview (categories only)

### Tomorrow preview (categories only)
- `GET /api/quests/tomorrow-preview/?date=YYYY-MM-DD`
- Never returns quest titles by contract.

### Missed-day return contract
- Included in daily lineup bootstrap as:
  - `missed_day`
  - `missed_day_return { show, days_missed, message }`

### Adaptive difficulty nudge
- `GET /api/quests/adaptive-nudge/?date=YYYY-MM-DD`
- `POST /api/quests/adaptive-nudge/` with body:
  - `{ "decision": "accept" | "decline" }`
- Backend stores preference and controls future lineup bias behavior.

### Naming normalization / backward compatibility
- Existing normalized routes retained.
- Alias route added for alternatives:
  - `GET /api/quests/alternatives/?item_id=<id>` (maps to swap alternatives)

## Request/Response Expectations (Frontend Invariants)

1. Frontend must treat lineup response as source of truth for slot behavior.
2. Frontend must not calculate EXP/progression logic.
3. Tomorrow preview UI must render categories only.
4. Adaptive nudge prompt visibility must use `show_nudge` from API.
5. Missed-day interstitial must be driven by `missed_day_return.show` and text from API.

## Backend-Owned Rules (Do Not Re-implement in Lovable)

- Quest generation and slot composition.
- Swap/intention/feedback side effects.
- EXP, streak, level, mechanics triggers.
- Missed-day protection ordering.
- Adaptive difficulty decision persistence and harder-quest bias.

## Intentionally Temporary in Current UI

- Session 7 proving widgets in dashboard are intentionally minimal.
- Modal/interstitial implementations are for contract proof, not final UX.
- Current layout/state organization is not the final Lovable architecture.

## What Lovable Should Redesign Later

- Final quest board visual system and interactions.
- Completion ring visual treatment and placement.
- End-of-day summary presentation and transitions.
- Tomorrow preview, missed-day, adaptive-nudge UX polish.
- Overall dashboard UX and information architecture.

## Contract Caveats / Edge Cases

- Summary endpoint can generate same-day summary on first call if missing snapshot.
- Tomorrow preview may trigger lineup generation when onboarding is complete and lineup absent.
- Adaptive nudge currently evaluates 7 consecutive full-completion days from summaries.
- Some legacy alias routes exist to reduce naming drift integration risk.
