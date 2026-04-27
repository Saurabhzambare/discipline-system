# Current State Product Audit (2026-04-12)

This document captures a repository-grounded snapshot of what is implemented today across frontend and backend surfaces.

## Scope Notes
- Focused on current code in `frontend/src` and `backend/*`.
- Excluded roadmap aspirations unless they are visibly surfaced in UI/API.

## High-level State
- The app is a working multi-page web client with custom route handling for dashboard, feed, groups, profile, onboarding, path-onboarding, roadmap, and preview screens.
- Backend exposes authenticated APIs for quests, social, and path mechanics with dedicated services/selectors layers.
- Several UI elements are explicitly placeholders (achievements/leaderboard blocks) and a separate static preview page exists for non-wired concepts.

## Core Surfaces Present
- Dashboard with quest lineup, completion flow, swap/intention/feedback, daily summary, and path mechanics widgets.
- Profile with player stats and friend lifecycle (search, request, accept/decline/cancel/remove).
- Feed with post CRUD, comments CRUD, reactions, visibility, and profile modal.
- Groups with group creation/join/leave, member list, and group-specific feed posting.
- Path quiz onboarding and path-specific onboarding forms for all five path codes.

## Known Placeholder/Scaffold Areas
- Dashboard achievements and leaderboard cards are currently placeholder values.
- Feed right-panel mini leaderboard is placeholder composition.
- `PreviewPage` is explicitly static and not backend-wired.
- `ComingSoonPage` is roadmap surfacing rather than implemented product capability.

## Backend/Architecture Snapshot
- API shape is broad and mostly aligned with frontend calls (`api.js`).
- Business logic is moved into service modules (`quests/services.py`, `paths/services.py`, `social/services.py`) with views generally thin.
- Social visibility rules and query helpers live in selectors.
- Test coverage exists across social, quests, onboarding, and session-6 mechanics files.

## Production Readiness Caveats
- Django settings are still dev-oriented (`DEBUG=True`, empty `ALLOWED_HOSTS`, hardcoded secret key string in settings).
- Custom client-side routing (manual history state) instead of hardened routing framework.
- No evidence of pagination/infinite loading for feed/groups/posts endpoints in current UI/API usage.
