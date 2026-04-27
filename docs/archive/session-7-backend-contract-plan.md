# Session 7 Backend-Authoritative Contract Plan

1. Session 7 Goal
- Freeze Session 7 as the final backend/API behavior layer for quest experience flows, with only minimal proving UI and no investment in final visual design.

2. Exact Scope Breakdown
- Quest board with progressive slot UI (day-based reveal only).
- Completion ring.
- End-of-day summary screen payload + trigger conditions.
- Tomorrow preview (categories only).
- Missed day return screen contract.
- Adaptive difficulty nudge trigger + choice handling.

3. Backend Responsibilities
- Keep lineup generation, progression, protections, and all EXP server-side.
- Add/normalize Session 7 API payloads for:
  - quest-board state (slot metadata, carried-over flags, swapability)
  - completion ring aggregate state
  - EOD summary + tomorrow category preview
  - missed-day return message state
  - adaptive nudge state + acknowledgement/opt-in endpoint
- Keep views thin and push all rules into services.

4. API Contracts That Must Be Stable
- Daily lineup response as canonical quest-board source.
- Summary endpoint payload for EOD display.
- Swap/intention/feedback APIs and their side effects.
- A stable tomorrow-preview response with category-only fields.
- A stable missed-day-state field in lineup bootstrap payload.
- A stable adaptive-nudge response + action endpoint.

5. Minimum Frontend Proving Requirements
- Render progressive quest board states from backend fields.
- Render completion ring from API aggregate values.
- Render EOD summary modal/screen from API payload.
- Render tomorrow preview categories-only view.
- Render missed-day return interstitial from API state.
- Render adaptive nudge prompt and call action endpoint.

6. What Must Be Deferred To Lovable
- Final visual system and layout architecture.
- Full dashboard redesign and interaction polish.
- Full onboarding UX rewrite.
- Final path mechanics presentation and IA cleanup.
- Micro-animations, visual storytelling, and polished transitions.

7. Risks / Hidden Dependencies
- Endpoint naming drift between docs and implementation must be reconciled before Lovable starts.
- Timezone + scheduler behavior must be deterministic for EOD/midnight logic.
- Current frontend contains placeholder and preview routes that can confuse scope boundaries.
- Monolithic `App.jsx` state orchestration can hide contract regressions.
- Tests currently failing in quests/players indicate baseline instability.

8. Recommended Build Order
1) Contract audit + endpoint naming normalization.
2) Service-layer completion for missing Session 7 behaviors (tomorrow preview, adaptive nudge, missed-day message contract).
3) API response schema freeze (serializers + tests).
4) Thin frontend proving screens/components for all Session 7 flows.
5) Regression suite pass and contract doc handoff for Lovable.

9. Definition of Done For Session 7
- All six Session 7 features exist as backend-authoritative behavior.
- Stable documented API contracts with tests for normal + edge cases.
- Minimal proving UI demonstrates each flow without design coupling.
- No critical business rule in frontend-only logic.
- Handoff package ready for Lovable rewrite without backend rework.

10. Final Clean Execution Prompt
"Implement Session 7 strictly as a backend-contract completion pass with minimal proving UI. Use BUILD_ORDER Session 7 and daily-quest-logic only. Keep views thin and all rules in services. Freeze stable APIs for quest board progressive slots, completion ring data, EOD summary, tomorrow categories-only preview, missed-day return state, and adaptive difficulty nudge state/actions. Add/adjust tests first for contract behavior, then implement services and serializers, then add only lean proving UI. Do not polish visuals. Do not redesign architecture for final UX. Ensure outputs are Lovable-ready and minimize future rework."
