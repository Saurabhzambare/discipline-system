# Discipline System — Current Status

**Last updated:** 2026-04-29 (Session B1 complete)
**Purpose:** This is the single source of truth for where the project stands.
Every session should read this first. Update it at the end of every session.

---

## 1. Active Phase

**Phase 5B — Quest System Redesign** (in progress)

We are in the middle of Phase 5B. Multiple sessions have been completed.
The next work is closing out Session 6, then executing Sessions 8 and 9.
The old plan to hand off the frontend to Lovable has been **abandoned**.
All frontend polish will be done here using Claude Code.

---

## 2. Phase 5B Session Progress

| Session | Scope | Status |
|---------|-------|--------|
| Pre-build audit | Repo inspection, conflict map | ✅ Complete |
| Session 1 | Foundation models (Quest, DailyQuestLineup, path models, migrations) | ✅ Complete |
| Session 2 | Path Discovery Quiz (9-question backend, scoring, match %, retake) | ✅ Complete |
| Session 3 | Quest seeding for all 5 paths (+ hardening patch) | ✅ Complete |
| Session 4 | Path-specific onboarding flows, DK oath moderation, GV skill tree init | ✅ Complete |
| Session 5 | Daily Quest Assignment Engine (5-layer algo, lineups, swaps, intention, feedback, summary) | ✅ Complete |
| Session 6 | Path mechanic persistence hooks, log endpoints, protection-order service, accountability partner flow | 🟡 In progress |
| Session 7 | Backend contract freeze (quest board, completion ring, EOD summary, tomorrow preview, missed-day, adaptive nudge) | ✅ Complete |
| Session A1 | Repo stabilize: fix stale tests, ESLint, Session 6 gaps, CI, .gitignore | ✅ Complete |
| Session A2 | Push to origin/main, README badges, Stage A docs | ✅ Complete |
| Session B1 | Personalization weight, feedback learning fix, swap learning — all wired and tested | ✅ Complete |
| Session 8 | Social & Achievement Features (badges, leaderboards, cross-path titles, weekly boss) | ⬜ Not started |
| Session 9 | End-to-end verification + Phase 5B completion sign-off | ⬜ Not started |

---

## 3. What Exists Today

### Backend apps (`backend/`)

- **`config/`** — Django project settings, URLs, WSGI/ASGI.
- **`core/`** — Shared utilities.
- **`users/`** — Custom user model, auth (JWT), signup/login.
- **`players/`** — Player profile, EXP, level (quadratic formula), streak, daily intention, daily summary.
- **`quests/`** — Quest, QuestCompletion, DailyQuestLineup, DailyQuestLineupItem, services (5-layer assignment, swap, feedback, intention, summary, tomorrow preview, adaptive nudge, personalization weight, swap learning), management command `seed_quests`.
- **`paths/`** — PathDiscoveryQuiz, QuizAnswer, PathMatchScore, UserPathSelection, PathOnboardingProgress, path-specific profiles (FitnessWarriorProfile, MindsetSageProfile, HealthAlchemistProfile, DisciplineKnightProfile, GrindVisionaryProfile), path-specific mechanics (SplitDayState, ArmorSystem, ArmorPiece, ElixirProgress, EquipmentProfile, DisciplineCode, GraceToken, StreakShield, WarRoomEntry, TemptationLog, KnightWeeklyReport, XPMultiplier, MultiplierProtection, SingularGoal, SkillTree, SkillTreeNode, OutputLog, PostFirstDollarChain, QuestChain, TransmutationMilestone, BodyJournal, WisdomLog, DarkNightEntry), management command `seed_session6_test_accounts`.
- **`social/`** — FriendRequest, Friendship, SocialPost, PostComment, PostReaction, ActivityEvent, SocialGroup, GroupMembership, AccountabilityPartnerRequest, AccountabilityPartnership, Badge, UserBadge, AchievementCard, WeeklyBossQuest, WeeklyBossCompletion.

### Backend test modules

- `core/tests.py`
- `users/tests.py` — passing
- `social/tests.py` — passing
- `players/tests.py` — passing
- `quests/tests.py` — passing (Session 7 contract tests)
- `quests/tests_session5.py` — passing
- `quests/tests_b1_personalization.py` — passing (15 tests: weight, feedback, swap, integration)
- `paths/tests_session6.py` — passing (includes Sage archetype filtering tests)
- `paths/tests_onboarding_completion.py`
- `paths/tests_seed_session6_accounts.py`

Total: 75 tests, all passing.

### Frontend pages (`frontend/src/pages/`)

- `LoginPage.jsx`
- `SignupPage.jsx`
- `PathOnboardingPage.jsx` (new 5-path onboarding: quiz → results → path-specific form → commitment)
- `DashboardPage.jsx` (quest lineup, completion ring, intention, swap, feedback, EOD summary, path mechanics widgets, placeholder leaderboard)
- `ProfilePage.jsx` (player stats, friends list, friend request lifecycle)
- `FeedPage.jsx` (posts CRUD, comments, reactions, profile modal, placeholder mini-leaderboard)
- `GroupsPage.jsx` (create/join/leave groups, group feed)
- `ComingSoonPage.jsx` (roadmap showcase — not wired to backend)
- `PreviewPage.jsx` (static demo screen — not wired)

### Frontend components (`frontend/src/components/`)

- `Layout.jsx` (sidebar nav, top bar, notification bell, flash banner)
- `QuestCard.jsx`
- `ProgressCard.jsx`
- (plus embedded sub-components in pages)

### Frontend state / utilities

- `App.jsx` (monolithic route + state orchestrator — technical debt)
- `api.js` (all API call helpers)
- `PathContext.jsx` (React Context for path state)

---

## 4. Known Outstanding Issues

### Code quality

1. **Monolithic `App.jsx`.** State orchestration is concentrated in one file; should eventually be broken up.
2. **Pending Django migrations.** Django 5 auto-detects `id` field type changes (AutoField → BigAutoField) for `paths` and `social` apps. Migrations `paths/0008_*` and `social/0005_*` need to be created and run before deploying to a fresh database. No functional impact on dev SQLite.

### Phase 5B functional gaps

3. **Session 6 partially complete.** Outstanding: Step 73 (accountability partner invite flow), Step 76 (path-mechanic log endpoint audit).
4. **Session 8 not started.** No achievement cards generated, badge system not wired to trigger events, leaderboards not implemented, cross-path identity titles not granted, weekly boss quest system only partially seeded.
5. **Placeholder UI.** Dashboard leaderboard card, feed right-panel mini-leaderboard, and achievement blocks currently show hardcoded dummy data.
6. **Layer 3 weekly rhythm tables not implemented.** `_apply_smart_suggestions` now has personalization weight (Day 14+ pillar history blending), but the per-path default weekly pillar priority tables (Mon=strength, Tue=cardio, etc.) from the spec are not yet built. The personalization layer correctly blends history from Day 14+ but has no default rhythm to blend against before Day 14.

### Production readiness

7. `DEBUG=True` in Django settings.
8. `ALLOWED_HOSTS` empty.
9. `SECRET_KEY` hardcoded in settings.
10. Custom client-side routing (manual `history.pushState`) — should migrate to a proper router (React Router) before launch.
11. No pagination on feed/groups/posts endpoints.
12. **Pending Django migrations** — Django 5 BigAutoField drift detected in `paths` (0008) and `social` (0005) apps. No functional impact on dev SQLite. Must be created and applied before deploying to a fresh PostgreSQL instance.

---

## 5. Path to Completion

### Stage A — Stabilize ✅ COMPLETE (Sessions A1 + A2)

- ✅ Rewrote stale `players/tests.py` and `quests/tests.py`.
- ✅ Fixed all 9 frontend ESLint errors (PathContext split, unused imports removed).
- ✅ Session 6 gaps addressed: Sage archetype filtering (Step 57), Knight Weekly Report Sunday trigger (Step 67), protection-order consolidation verified (Step 75). Remaining: Steps 73, 76.
- ✅ Reconciled local branches with `origin/main`; pushed clean baseline.
- ✅ Added GitHub Actions CI: `backend-tests.yml` and `frontend-checks.yml`.
- ✅ Added `.gitignore`; untracked 10 legacy `.pyc` files.
- ✅ Deleted `OnboardingPage.jsx` orphan; all `/onboarding` routes redirect to `/path-onboarding`.
- ✅ Fixed `CheckConstraint(check=...)` → `condition=` for Django 5.1+ compat (5 constraints).
- ✅ Added `manage.py check` step to CI before test run.

### Stage B — Finish Phase 5B backend (2–3 sessions)

- ✅ **Session B1** — Personalization weight, feedback learning fix (+3/-3), swap learning wired into `_apply_smart_suggestions`. 15 new tests.
- **Session 8** — Social & Achievement Features (BUILD_ORDER steps 80–88).
- **Session 9** — End-to-end verification (BUILD_ORDER steps 89–105).

### Stage C — Frontend polish pass (3–5 sessions)

This replaces the abandoned Lovable plan. Work is done here in Claude Code.

- Design system pass: Tailwind tokens, colour palette (Solo Leveling dark/cyan/amber), typography scale, shared component primitives.
- Replace placeholder Dashboard leaderboard with real backend leaderboard data (depends on Session 8).
- Replace placeholder Feed leaderboard with real data.
- Polish completion ring, EOD summary modal, tomorrow preview, missed-day return interstitial, adaptive nudge prompt — currently shipped as minimal "proving UI."
- Polish path mechanics widgets: War Room, Wisdom Log, Body Journal, Output Log, Vision Board, Skill Tree display.
- Login/signup visual redesign toward immersive Solo Leveling aesthetic.
- Migrate `App.jsx` custom routing to React Router.

### Stage D — Production deployment (1–2 sessions)

- Move `SECRET_KEY` to env; set `DEBUG=False`; populate `ALLOWED_HOSTS`; configure CORS.
- Configure PostgreSQL for production; run migrations.
- Railway deployment: Dockerfile review, `railway.toml`, env vars, cron for midnight quest scheduler.
- Add error logging (Sentry or similar).
- Basic monitoring.

### Stage E — Post-launch (Phases 7+)

Per `docs/web-development-roadmap.md`:

- Phase 7 — Formalize reward engine & achievements
- Phase 8 — Competitive systems (tournaments, challenges)
- Phase 9 — Privacy & settings system
- Phase 10 — Avatar system
- Phase 11 — Device integration
- Phase 12 — Subscription system
- Phase 13 — Merchandising
- Phase 14 — Immersive experience layer
- Phase 15 — Platform stabilization
- Phase 16 — Mobile apps (iOS + Android)

---

## 6. Architectural Decisions (Locked)

- **Level formula:** quadratic — `EXP needed = level² × 50 − 50`
- **State management:** React Context + custom hooks (NOT Redux)
- **Scheduler:** Django management command via cron (NOT Celery or Redis)
- **Backend app boundaries:** users / players / quests / paths / social / core. No further app splits planned during Phase 5B.
- **Frontend routing:** currently custom, planned migration to React Router in Stage C.
- **Database:** SQLite (dev), PostgreSQL (prod).
- **Deployment target:** Railway with Docker.
- **Auth:** JWT (already configured).
- **All EXP logic is server-side only.** No frontend EXP calculation.
- **Timezone:** Per-user timezone stored on Player; all midnight resets use player-local time.

---

## 7. Documents That Matter Right Now

Read these at the start of every coding session:

1. `AGENTS.md` — project coding rules
2. `docs/architecture.md` — architecture philosophy
3. `docs/CURRENT_STATUS.md` — this file
4. `docs/phase-5b-quest-system-redesign.md` — active phase scope
5. `docs/game-design/BUILD_ORDER.md` — step-level task tracker
6. `docs/game-design/README.md` — index to path and system specs
7. Specific path or system spec only when working on it

Everything else is historical reference — see `docs/archive/` once cleanup lands.

---

## 8. How To Update This Doc

At the end of every session:

1. Update the "Last updated" date at the top.
2. Move completed work into the done columns.
3. Add any new "Known Issues" you discovered.
4. Remove issues you resolved.
5. Commit in the same PR as the code changes.
