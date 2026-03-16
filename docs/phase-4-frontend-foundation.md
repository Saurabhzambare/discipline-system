# Phase 4 — Frontend Foundation

## Purpose of this document

This document defines the scope and implementation direction for **Phase 4: Frontend Foundation**.

Its goal is to make Phase 4 clear for both:

- the project owner
- future contributors
- AI coding agents

This phase should be implemented in a clean, minimal, architecture-respecting way.

---

# 1. Phase goal

Phase 4 builds the first proper user-facing web experience on top of the backend systems completed so far.

This phase introduces or formalizes:

- login page UI
- signup page UI
- frontend auth flow integration
- onboarding / path selection UI
- player dashboard UI
- visible progression display
- basic profile display
- frontend structure that can grow cleanly

This is the phase where the platform starts to feel like a real web product instead of only a backend system.

---

# 2. Why this phase matters

Before Phase 4, the project has the core backend gameplay loop but does not yet fully express it in the browser.

With Phase 4:

- players can actually experience the system visually
- progression becomes visible and motivating
- the dashboard becomes a real status window
- the product becomes usable in a more complete way
- later systems such as social, leaderboards, privacy, and premium features have a UI foundation to build on

This phase is the bridge between backend functionality and real player experience.

---

# 3. Included scope

Phase 4 includes the following core areas.

## 3.1 Login page

The frontend should provide a proper login page.

Expected direction:

- player can enter credentials
- auth flow connects to the existing backend
- login errors are handled clearly
- success state leads the player into the application flow

---

## 3.2 Signup page

The frontend should provide a proper signup page.

Expected direction:

- player can create an account
- signup integrates with existing backend behavior
- validation and error handling are clear
- success state transitions cleanly into onboarding or authenticated flow

---

## 3.3 Frontend auth flow integration

Frontend should properly work with the backend auth system already completed earlier.

Expected direction:

- token/session handling follows the current backend/API approach
- authenticated state is preserved appropriately
- protected UI areas are gated correctly
- logout flow works cleanly

---

## 3.4 Onboarding / path selection

This phase should introduce the first UI for player onboarding after account creation or first entry.

Expected direction:

- player can select a path
- path options may include:
  - Runner
  - Gym
  - Discipline
  - Tournament
  - 75 Hard
- the implementation can be simple for now
- this phase does not need the full advanced path system yet

The goal is to establish player identity and prepare the dashboard experience.

---

## 3.5 Player dashboard

The player dashboard should become the first real status window of the platform.

Expected direction:

- dashboard shows progression clearly
- dashboard shows active quests
- dashboard shows useful player information
- dashboard reflects the Solo Leveling-inspired product direction without overbuilding the final immersive layer yet

---

## 3.6 Visible progression display

The frontend should clearly display the progression data created in Phase 3.

Expected direction:

- show level
- show EXP
- show streak
- show quest-related progression information
- include a visible EXP progress bar if practical in this phase

This is one of the most important parts of Phase 4.

---

## 3.7 Basic profile display

The player should have a basic visible profile area/page.

Expected direction:

- show Player ID
- show avatar placeholder or current avatar if available
- show basic player stats
- keep it minimal and aligned with current backend state

This phase does not require the full future public-profile/social system.

---

## 3.8 Frontend structure improvement

The frontend should begin moving toward a component-based structure.

Expected direction:

- avoid keeping everything in a single large `App.jsx`
- create reusable UI components where appropriate
- keep structure simple and beginner-friendly
- prepare the frontend for later phases without overengineering

---

# 4. Excluded scope / non-goals

The following items are explicitly out of scope for this phase unless separately approved.

## Not included by default

- social feed
- comments / reactions
- friend system
- groups
- leaderboards
- player challenges
- subscription UI/paywall system
- merchandising pages
- smartwatch/device integration
- full avatar generation flow
- immersive 3D UI system
- sound effects
- cinematic Solo Leveling effects
- full privacy settings
- full settings system
- full public profile system
- large design system abstraction
- broad frontend rewrite for theoretical future scale

## Also out of scope

- unrelated cleanup
- broad backend refactors
- rewriting stable Phase 1–3 backend behavior unless necessary to support frontend integration
- mixing multiple future phases into this implementation

Phase 4 should stay focused.

---

# 5. Current architecture position for this phase

## Important rule

Phase 4 should build on top of the backend systems already completed through Phase 3.

This phase should not assume major backend changes are required.

## Expected architectural direction

- frontend consumes existing backend APIs
- UI reflects current progression state from backend
- component structure should improve gradually
- frontend should not become a giant single file
- backend contracts should only change if truly necessary

---

# 6. Recommended implementation direction

This section describes the intended shape, not a forced exact file path.

## 6.1 First inspect current frontend and API usage

Before implementing:

- inspect current `frontend/src`
- inspect current `App.jsx`
- inspect current auth flow
- inspect existing API calls
- inspect current backend endpoints used by frontend
- identify what already exists and what needs to be formalized

Do not rebuild blindly if useful foundations already exist.

---

## 6.2 Suggested responsibility split

### Authentication UI
Likely includes:

- login form component/page
- signup form component/page
- auth state handling
- protected-route or equivalent logic if needed

### Onboarding UI
Likely includes:

- path selection screen
- simple onboarding decision flow
- storage/submission of selected path if supported

### Dashboard UI
Likely includes:

- player stats card
- EXP display
- progress bar
- streak display
- quest list
- completion/history area

### Profile UI
Likely includes:

- Player ID display
- avatar display or placeholder
- summary stats

---

## 6.3 Component-based preference

Preferred direction:

- break the UI into reusable pieces
- keep components small and understandable
- avoid premature complex frontend architecture
- organize by feature or role where it makes sense

Possible component directions:

- `LoginForm`
- `SignupForm`
- `PlayerStatsCard`
- `ExpBar`
- `StreakBadge`
- `QuestList`
- `QuestCard`
- `ProfileCard`

The exact shape should match the current frontend code style, but the direction should remain component-oriented.

---

# 7. Acceptance criteria

Phase 4 is considered complete when the following are true.

## Functional acceptance criteria

- player can log in through the frontend
- player can sign up through the frontend
- authenticated frontend flow works against current backend
- onboarding/path selection UI exists in a usable form
- player dashboard displays current progression state
- player can see level, EXP, and streak clearly
- player can see quests from the frontend
- quest completion updates visible state appropriately
- basic profile display exists

## Code quality acceptance criteria

- frontend structure is cleaner than a single giant page/file
- reusable components are introduced where appropriate
- unrelated files were not modified without reason
- backend was not refactored unnecessarily
- implementation remains readable and maintainable

## Documentation acceptance criteria

- important frontend flow changes are documented if needed
- any meaningful API contract changes are documented if needed
- architectural decisions remain aligned with `docs/architecture.md`

## UX acceptance criteria

- progression is visible and motivating
- the dashboard feels like a true status/progression screen
- the current gameplay loop is understandable in the browser

---

# 8. Testing expectations

At minimum, verification should cover the most important frontend flows introduced in this phase.

## Recommended verification focus

- login flow works
- signup flow works
- authenticated player data loads correctly
- dashboard renders progression values correctly
- quest list displays correctly
- completing a quest updates visible progression state correctly
- onboarding/path selection UI behaves correctly
- no obvious regression in previously working frontend behavior

## Testing principle

Use the current project style, but ensure that key user flows are meaningfully verified.

If formal automated frontend tests are not yet established, at least ensure strong manual verification of the major flows.

---

# 9. Architecture rules specific to this phase

## Rule 1
Do not perform a major frontend or backend refactor just to build the first usable UI.

## Rule 2
Do not keep expanding a giant `App.jsx` if the UI is clearly growing beyond a reasonable size.

## Rule 3
Do not force a complicated frontend architecture too early.

## Rule 4
Do not rebuild stable backend behavior unless the frontend genuinely requires small changes.

## Rule 5
Keep progression visible and central in the UI.

## Rule 6
Do not mix later-phase features into this phase.

## Rule 7
Prefer simple, clean, reusable UI structure over clever complexity.

---

# 10. Suggested implementation checklist

Before coding:

- read `AGENTS.md`
- read `docs/architecture.md`
- read `docs/web-development-roadmap.md`
- inspect current frontend files
- inspect backend endpoints used by frontend
- create a short execution plan
- list assumptions
- list risks

During coding:

- keep changes scoped
- improve frontend structure incrementally
- keep auth flow clear
- keep progression display obvious
- add/update verification as appropriate

After coding:

- explain changed files
- explain assumptions
- explain any API response changes
- update docs if needed

---

# 11. Practical summary

Phase 4 should make the existing system feel real in the browser.

That means a player should be able to understand:

- I have an account
- I have a path
- I have quests
- I gain EXP
- I level up
- I maintain a streak

But it should be implemented with discipline:

- no premature advanced systems
- no giant refactor
- no UI chaos inside one big file
- no mixing of multiple later phases

Keep it simple, clear, usable, and aligned with the roadmap.