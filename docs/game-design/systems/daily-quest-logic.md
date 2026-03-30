# Daily Quest Assignment Logic
# docs/game-design/systems/daily-quest-logic.md

---

## How To Use This File

Read this file when:
- Building the five-layer assignment algorithm
- Building the midnight scheduler
- Building the quest board frontend
- Building the swap system
- Building the quest feedback system
- Building the daily intention prompt
- Building the completion ring component
- Building the end of day summary screen
- Building the missed day return screen
- Building the tomorrow preview feature

Always read these files first before this one:
- AGENTS.md
- docs/architecture.md
- docs/phase-5b-quest-system-redesign.md
- docs/game-design/README.md
- docs/game-design/BUILD_ORDER.md

---

## System Overview

The Daily Quest Assignment Logic is the brain
of the entire app.

It generates a personalized daily quest lineup
for each player every single day across all
active paths.

Core principles:
- App suggests — player always has final say
- Complexity revealed gradually not all at once
- Real life takes priority over rigid schedules
- The system gets smarter the longer a player
  uses it
- Never shame a player for missing a day

---

## Daily Flow

Morning app open
→ Daily Intention prompt
→ Quest board loads with suggested lineup
→ Player completes or swaps quests freely
→ Quests completed throughout the day
→ If all quests done before 6PM:
  show mid-day completion message
→ 9PM end of day summary triggers
→ Tomorrow preview available from summary

---

## Critical — Timezone Handling

Store player timezone on signup.
The algorithm runs at midnight in the player's
LOCAL timezone.
Never run the midnight algorithm at UTC midnight
for all players simultaneously.

If player timezone is not set default to UTC
and prompt player to set timezone on next login.

This is critical for the daily experience to
feel correct. A player in Calgary is UTC-7.
Midnight UTC is 5PM their time. Their quests
would reset mid-evening which is wrong and
confusing.

---

## Progressive Complexity Reveal

The slot system complexity is revealed gradually
based on how many days the player has been active.

The five-layer algorithm runs identically from
Day 1 underneath. Only what the player sees
changes.

DAY 1 TO 6:
Show 3 quests only.
Simple list view.
No slot UI visible.
No slot labels.
No swap feature shown.
Player just sees three quest cards and completes.
Goal: prove the daily habit before showing
complexity.

DAY 7:
Introduce slot UI with animated tutorial.
Brief in-app message:
"You have proven yourself for 7 days Hunter.
Your quest board is expanding. Here is how
it works."
Show slot UI for first time with animation
explaining Universal Assigned and Bonus slots.
Expand to full slot count based on player
settings.

DAY 14:
Swap feature unlocked.
Brief explanation shown once:
"You can now swap suggested quests for ones
that better fit your day. Use swaps wisely —
you get 3 per path per day."
Swap icons appear on assigned slot quest cards.

DAY 30:
Full slot customization available in settings.
Message shown once:
"Your discipline has earned you full control
of your quest board Hunter. Customize your
daily limits in settings."

---

## Day 1 Hardcoded Starter Lineup

On the player's very first day the algorithm
does not run. Use these hardcoded lineups instead.

The algorithm takes over from Day 2 onwards.

Day 1 starter lineup per path:

Fitness Warrior:
Quest 1: Complete 20 pushups (40 EXP D rank)
Quest 2: Walk 5000 steps (35 EXP D rank)
Quest 3: Hit your protein target today
(35 EXP D rank)

Mindset Sage:
Quest 1: Meditate for 5 minutes (35 EXP D rank)
Quest 2: Write 3 things you are grateful for
(30 EXP D rank)
Quest 3: Sit in silence for 5 minutes with
no phone (30 EXP D rank)

Health Alchemist:
Quest 1: Drink 2L of water today (30 EXP D rank)
Quest 2: Complete the Alchemist Morning Protocol
(150 EXP C rank)
Quest 3: Eat one whole food meal today
(35 EXP D rank)

Discipline Knight:
Quest 1: Make your bed immediately after waking
(25 EXP D rank)
Quest 2: Write tomorrow's schedule tonight
(35 EXP D rank)
Quest 3: Clean your workspace before starting
your day (30 EXP D rank)

Grind Visionary:
Quest 1: Spend 30 minutes on your grind focus
today (40 EXP D rank)
Quest 2: Review your singular goal and write
one action toward it today (30 EXP D rank)
Quest 3: Log one thing you learned or created
today (25 EXP D rank)

---

## Quest Slot System

Each active path gets its own dedicated quest
slots per day.
Slots are independent per path.
Completing Fitness Warrior quests does not
affect Mindset Sage slot count.

DEFAULT SLOT COUNT PER PATH:
1 active path: 5 slots
2 active paths: 4 slots each
3 active paths: 3 slots each
4 active paths: 3 slots each
5 active paths: 2 slots each

PLAYER CUSTOMIZATION:
Available from Day 30 onwards in settings.
Player adjusts slots per path within limits
based on time commitment set during onboarding:

30 minutes commitment:
Minimum 2 slots, maximum 4 slots per path

1 hour commitment:
Minimum 3 slots, maximum 6 slots per path

2 hours commitment:
Minimum 4 slots, maximum 8 slots per path

3+ hours commitment:
Minimum 5 slots, maximum 10 slots per path

MAXIMUM TOTAL DAILY QUESTS — LEVEL SCALED:
Total quests across ALL active paths cannot exceed:

Level 1 to 9: 8 quests maximum total
Level 10 to 19: 10 quests maximum total
Level 20 to 29: 12 quests maximum total
Level 30 and above: 15 quests maximum total

If player tries to set slots that would exceed
their level cap show warning:
"That is a heavy load Hunter. Are you sure?
Overcommitting kills streaks faster than
anything."

SLOT TYPES PER PATH:
Each path's daily slots divide into three types:

UNIVERSAL SLOT:
Filled by path's universal daily quest.
Locked — cannot be swapped by player.
Always appears first in path quest list.
One universal slot per path per day.
Defined in each path file.

ASSIGNED SLOTS:
Filled by the five-layer algorithm.
Swappable — player can replace with alternative.
Makes up majority of daily slots.
Suggestions improve over time via smart layer.

BONUS SLOT:
One open slot per path per day.
Player picks freely from full available
quest pool for their path and rank.
Appears last in path quest list.
Labeled: "Choose your own quest"
Unlocked from Day 7 onwards.

---

## Daily Intention Prompt

Every morning when player opens the app
before quest board loads show a single
full-screen intention prompt.

Show once per day only.
Do not show again if player has already
set their intention today.

UI:
Dark screen.
Single question centered.
Three tap option cards below.

Question text:
"What is your intention for today Hunter?"

OPTION A — Full Send:
"Full Send — I am completing everything today"

OPTION B — Steady:
"Steady — I will do what I can"

OPTION C — Recovery:
"Recovery — I need a lighter day"

LOGIC PER ANSWER:

Full Send:
Load full suggested lineup as normal.
Add one bonus Push Quest card at bottom of
each path list labeled: "Push Quest — optional"
Push Quest is one rank above player's current
average completion rank.

Steady:
Load standard suggested lineup as normal.
No changes to assignment algorithm output.

Recovery:
Replace all assigned slots with universal
quests only plus D rank quests from active paths.
Cap total quests at 5 regardless of path count.
Streak is NOT broken on recovery days.
Show message on quest board:
"Recovery mode active. Light quests only today.
Rest is part of the grind."

IMPORTANT:
Cross-path bonus quests are always exempt
from Recovery day filtering.
If a cross-path bonus pair was identified
for today it stays in the lineup even on
Recovery days.
Maximum one cross-path bonus pair on
Recovery days.

Intention answer saved to DailyIntention model.
Used by smart suggestion layer to learn patterns.
If player consistently chooses Recovery on
same weekday: auto-surface lighter lineup
on that day going forward.

---

## Five-Layer Assignment Algorithm

This algorithm runs server-side at midnight
local time per player.
Results stored in DailyQuestLineup model
ready to serve instantly when player opens app.
Never generate lineup on demand at app open.
Always pre-generated overnight.

---

## Layer 1 — Lock Universal Quests

Identify each active path's universal daily
quest as defined in each path file.
Place in universal slot — locked and
non-swappable.
These never change day to day for the same path.

---

## Layer 2 — Apply Hard Filters

Remove from consideration any quest that is:

On active cooldown:
Cooldown period has not elapsed since
last completion.

Below rank eligibility:
Quest rank higher than player's current
level allows.
Unless experience-based visibility override
applies from onboarding.

Requiring equipment player does not have:
Equipment not selected in EquipmentProfile.
Applies to Health Alchemist quests only.

Completed in last 24 hours:
Quest was already completed today.

One-time only and already completed:
Quest is flagged one-time and player has
a completion record for it.

Pillar not yet unlocked at player level:
Applies to Health Alchemist pillar unlocks
and Grind Visionary pillar unlocks.

---

## Layer 3 — Apply Weekly Rhythm As Default

Use weekly pillar rhythm as starting suggestion
for which pillar to prioritize in assigned slots.

IMPORTANT: Rhythm is a default not a rule.
Smart layer in Layer 4 can override rhythm.

RHYTHM TRANSITION OVER TIME:
Day 1 to 13: Use default rhythm tables exactly.
Day 14: Begin building personalized rhythm
from DailyQuestCompletion history.
Personalized pattern weighted at 30% on Day 14.
Increase weight by 5% per day until Day 30.
From Day 30 onwards personalized pattern
weighted at 100%.
Default rhythm kept as fallback if insufficient
completion history data exists.

DEFAULT WEEKLY RHYTHMS PER PATH:

Fitness Warrior:
Monday: Strength compound lifts priority
Tuesday: Cardio and endurance priority
Wednesday: Hybrid training priority
Thursday: Strength volume priority
Friday: Cardio and calisthenics priority
Saturday: Full hybrid session priority
Sunday: Recovery quests only

Mindset Sage:
Monday: Inner Stillness priority
Tuesday: Knowledge Forging priority
Wednesday: Shadow Training priority
Thursday: Mirror Work priority
Friday: Inner Stillness and Stoic Challenge
Saturday: Knowledge Forging priority
Sunday: Mirror Work weekly review priority

Discipline Knight:
Monday: War Room week planning priority
Tuesday: The Siege deep work priority
Wednesday: The Forge routine priority
Thursday: Iron Will temptation priority
Friday: The Treasury priority
Saturday: The Kingdom priority
Sunday: Honor Review and weekly report priority

Health Alchemist:
Monday: Fuel Formula priority
Tuesday: Purification Ritual priority
Wednesday: Restoration Chamber priority
Thursday: Inner Ecosystem priority
Friday: Emotional Crucible priority
Saturday: Full protocol all pillars
Sunday: Body Journal and Transmission Protocol

Grind Visionary:
Monday: Mastery Lab deep learning priority
Tuesday: Workshop create and ship priority
Wednesday: Mastery Lab apply skills priority
Thursday: Empire side hustle work priority
Friday: Workshop publish something priority
Saturday: Alliance and Signal priority
Sunday: Vision Board review and Output Log

---

## Layer 4 — Apply Smart Suggestion Logic

After rhythm fills pillar priority refine
quest selection using player history data
stored in QuestPreference model.

COMPLETION PATTERN ANALYSIS:
Quests completed consistently:
Suggest similar difficulty level.
Preference score increases with completions.

Quests skipped 3 or more times:
Surface less frequently.
Preference score decreases with skips.

Quests never attempted:
Surface occasionally to encourage variety.
New quest exploration bonus in scoring.

Quests approaching streak milestone:
Prioritize to help player hit milestone.

PLAYER FEEDBACK ANALYSIS:
Quest marked thumbs up: preference score +3
Quest marked thumbs down: preference score -3
Completion without feedback: preference score +1
Skip without feedback: preference score -1
Thumbs feedback weighted 3x more than passive
completion pattern data.

STREAK AND MULTIPLIER AWARENESS:
If streak above 14 days:
Suggest slightly harder quests to maintain
challenge.

If streak just recovered after break:
Suggest slightly easier quests for 3 days
to rebuild momentum.

If Grind Visionary player is one day from
multiplier tier upgrade:
Surface highest available EXP quests regardless
of weekly rhythm.

INTENTION PATTERN ANALYSIS:
If player chose Recovery on same weekday 2
or more times:
Auto-surface lighter lineup on that day.

If player chose Full Send consistently:
Gradually increase difficulty of suggestions.

TIME PATTERN ANALYSIS:
If player typically completes quests before 9AM:
Front-load time-sensitive quests in lineup.

If player completes after 8PM:
Deprioritize quests that reference morning
activities.

QUEST SCORING FUNCTION:
Build a quest scoring function that combines:
QuestPreference preference score: weight 40%
Completion recency — quests not done recently
score higher: weight 20%
Weekly rhythm pillar match: weight 25%
Rank appropriateness for player level: weight 15%
Higher total score equals higher priority
for assignment.

---

## Layer 5 — Fill Remaining Slots

If insufficient quests pass all filters to
fill assigned slots:

Step 1: Pull from adjacent pillar in same path.
Step 2: If still insufficient drop to one rank
lower temporarily.
Step 3: Never show empty assigned slot.
Always fill all slots even if using lower rank.

Log insufficient quest pool as a warning in
backend logs for admin review.
This helps identify paths that need more quests
seeded at certain rank levels.

---

## Path-Specific Daily Override Logic

These overrides run AFTER the five-layer
algorithm and modify the lineup for specific
path conditions.
Overrides take priority over algorithm output.

FITNESS WARRIOR OVERRIDES:

If today is player's scheduled rest day:
Replace ALL assigned slots with recovery quests.
Recovery quest set defined in fitness-warrior.md.

If today is Push day on PPL split:
Prioritize chest shoulder tricep focused quests
in assigned slots regardless of weekly rhythm.

If today is Pull day:
Prioritize back and bicep focused quests.

If today is Leg day:
Prioritize squat and hinge focused quests.

---

MINDSET SAGE OVERRIDES:

Every Sunday:
Automatically include weekly review quest in
one assigned slot.
This slot cannot be swapped on Sundays.
Show lock icon on that quest card.

If Freedom Day is redeemed:
Clear ALL assigned slots for Mindset Sage path.
Show Freedom Day screen for this path only.
Other active paths display their quests normally.

If Dark Night Quest was activated manually:
Count as completing one assigned slot for day.
Never surface Dark Night Quest in algorithm.
It is exclusively manually activated by player.

---

HEALTH ALCHEMIST OVERRIDES:

Every morning:
Morning Protocol quest always fills first
assigned slot.
Cannot be swapped by player.
This applies every day without exception.

If Elixir is on Day 7:
Surface highest available EXP quests in
remaining assigned slots to maximize
completion day reward.

Equipment gated quests:
Never appear in assigned or bonus slots for
players without that equipment in profile.
Only appear in swap drawer if player has
the required equipment.
Player can update equipment profile in settings.

---

DISCIPLINE KNIGHT OVERRIDES:

Every Sunday:
Honor Review quest fills one assigned slot.
Available Sunday only.
On all other days show countdown on quest card:
"Available Sunday — [X] days away."
Lock icon shown other days.

War Room morning planning quest:
Always fills first assigned slot every day.
Cannot be swapped.

If armor piece is cracked:
Surface Forge pillar quests in majority of
assigned slots to prioritize repair over
other pillars.
Continue until crack is repaired.

---

GRIND VISIONARY OVERRIDES:

If player is one day from multiplier tier upgrade:
Surface highest available EXP quests in all
assigned slots regardless of weekly rhythm.
Show message on quest board header:
"Tomorrow your multiplier upgrades Visionary.
Make today count."

Every Sunday:
Vision Board review quest fills one assigned slot.

If Accountability Partner is active:
Surface accountability quest in one slot
on Sundays.

---

## Cross-Path Daily Bonus Logic

For players with multiple active paths the
algorithm checks for cross-path bonus
opportunities daily.

MAXIMUM ONE CROSS-PATH BONUS PER DAY:
Algorithm identifies all available cross-path
bonus pairs for that player that day.
Selects only the highest EXP value pair.
Surfaces that pair only.
No other cross-path bonuses shown until
next day.
This keeps cross-path bonuses feeling special
and meaningful rather than routine.

CROSS-PATH PAIRS:

Cold shower — Fitness Warrior and Health Alchemist:
If cold shower quest available in both paths:
Surface in both paths lineups same day.
Both quest cards show gold border.
Label on both cards:
"Complete both for +20 EXP bonus"
Bonus awarded when both marked complete same day.
Message: "Body and mind forged together."

Breathwork — Mindset Sage and Health Alchemist:
If breathwork quest available in both paths:
Surface in both lineups.
Gold border on both cards.
+20 EXP bonus on completion of both.
Message: "Breath connects body and soul."

Deep work — Discipline Knight and Grind Visionary:
If deep work quest available in both paths:
Surface in both lineups.
Gold border on both cards.
+20 EXP bonus on completion of both.
Message: "Discipline fuels the vision."

5AM wake up — Mindset Sage and Discipline Knight:
If 5AM quest available in both paths:
Surface in both lineups.
Gold border on both cards.
+25 EXP bonus on completion of both.
Message: "The early hours belong to the
disciplined mind."

Reading — Mindset Sage and Grind Visionary:
If reading or knowledge quest available in both:
Surface in both lineups.
Gold border on both cards.
+25 EXP bonus on completion of both.
Message: "Knowledge into action."

RECOVERY DAY EXEMPTION:
Cross-path bonus quests are always exempt
from Recovery day filtering.
If a cross-path bonus pair is identified
it surfaces even on Recovery days.
Maximum one cross-path bonus pair on
Recovery days still applies.

---

## Swap System

Available from Day 14 onwards.
Swap icon visible on each assigned slot
quest card.
No swap icon on universal slot card.
No swap icon on bonus slot card.

SWAP UI:
Player taps swap icon on assigned quest card.
Bottom drawer opens showing up to 6 alternative
quests from same path.
Alternatives filtered by:
Same rank as swapped quest or one rank below.
Excludes quests already in today's lineup.
Excludes quests on active cooldown.
Excludes quests failing hard filters from Layer 2.
Alternatives ordered by preference score
descending from QuestPreference model.
Player taps any alternative to replace.
Drawer closes and quest card updates
with smooth animation.

SWAP LIMITS:
Maximum 3 swaps per day per path.
After 3 swaps swap icon disappears from
remaining assigned quest cards for that path.
Message shown when limit reached:
"You have used your swaps for today Hunter.
Commit to what is in front of you."

SWAP LEARNING:
Each swap recorded in DailySwap model.
If player swaps same quest 3 or more times:
Quest flagged as low preference in smart
suggestion layer.
If player consistently swaps toward same
quest type: that type weighted higher in
future suggestions.

---

## Quest Feedback System

After completing or skipping any quest show
two small feedback icons beneath the quest
card before it dismisses.

Icons:
👍 — I want more like this
👎 — Show this less often

One tap only.
No confirmation dialog.
No text required from player.
Feedback saved immediately to QuestFeedback
model and updates QuestPreference score.

Feedback is always optional.
If player does not tap either icon within
3 seconds icons fade and quest dismisses
normally.
Never block quest dismissal waiting for
feedback.

SCORING IMPACT:
Thumbs up: preference score +3
Thumbs down: preference score -3
Completion without feedback: score +1
Skip without feedback: score -1

---

## Quest Expiry Logic

D rank quests:
If incomplete: carries over to next day once.
If still incomplete after carry over: expires
at midnight.
Carry over indicator shown on quest card:
Amber card color plus text:
"Carried over from yesterday — complete today
or it expires"

C rank quests:
Same carry over logic as D rank.
Expires after one carry over day.

B rank quests:
Expires at midnight — no carry over.
No warning color — disappears on reset.

A rank quests:
Expires at midnight — no carry over.

S rank quests:
Expires at midnight — no carry over.

Universal daily quests:
Always expires at midnight — resets fresh daily.
Never carries over regardless of rank.

Weekly Boss Quest:
Expires end of Sunday at 23:59.
No carry over to following week.

EXPIRY NOTIFICATION:
At 10PM local time if player has incomplete
quests send push notification:
"2 hours remain on today's quests Hunter.
Finish strong."

Only send notification if:
Player has not completed all quests AND
Player has not opened app in last 2 hours.
Never send notification if player is actively
using app right now.

---

## Missed Day Logic

Check last active date on each player login.
If gap greater than 1 day trigger missed
day logic.

PROTECTION MECHANICS — apply in this order:

Step 1: Discipline Knight Grace Token
If available: auto-consume token.
Armor does not crack.

Step 2: Discipline Knight Streak Shield
If Grace Token already used: auto-activate shield.
Armor does not crack.
Streak protected.

Step 3: Grind Visionary Multiplier Protection
If earned: auto-activate protection.
Multiplier does not reset.

Step 4: Health Alchemist Elixir Mercy
Elixir retains 50% fill shown as cracked.
Does not reset to zero.

Step 5: Streak break
If no protections available:
Streak breaks.
Relevant mechanics reset per path rules.
Armor cracks if Discipline Knight.
Multiplier resets if Grind Visionary.

RETURN EXPERIENCE:
When player opens app after missed day
show full screen for exactly 3 seconds:

"You were away yesterday Hunter.
The journey continues today.
One missed day does not define you —
what you do next does."

Then load fresh daily lineup for today.
No reference to missed quests anywhere.
No incomplete quest list from yesterday shown.
Never shame the player for missing a day.
All language must be forward-facing.
Log missed day to backend for analytics only.

---

## Completion Ring

A single ring displayed prominently on dashboard.
Ring is divided into colored arc segments —
one segment per active path.

SEGMENT COLORS:
Fitness Warrior: Red
Mindset Sage: Purple
Health Alchemist: Green
Discipline Knight: Blue
Grind Visionary: Gold

Each segment fills as quests for that path
are completed throughout the day.
Segment arc length proportional to quest count
for that path relative to total daily quests.

Example with 3 active paths each with 3 quests:
Each path gets one third of the ring arc.
As Fitness Warrior quests complete red segment
fills gradually.

RING BORDER COLOR STATES:
0 to 33% total completion: Red border
34 to 66% total completion: Amber border
67 to 99% total completion: Blue border
100% total completion: Gold border with slow
pulse animation

RING CENTER DISPLAY:
Shows completed quests vs total:
"7 / 9" displayed centered inside ring.
Updates in real time as quests are completed.
No page refresh required.
Use websocket or polling for real-time update.

RING INTERACTION:
Tapping any colored segment opens that path's
quest list directly.
Tapping ring center opens combined quest view
showing all active paths together.

SINGLE PATH PLAYERS:
Ring shows one solid color segment — full circle.
Same fill and color state logic applies.

---

## End Of Day Experience

TWO TRIGGER CONDITIONS:

Condition A — Early completion:
If player completes ALL quests before 6PM
show brief mid-day completion message:
"All quests complete Hunter. The rest of the
day is yours — or push for bonus quests."
Offer one optional bonus quest per active path.
Full end of day summary still triggers at 9PM.

Condition B — Standard end of day:
Full summary triggers at 9PM local time
regardless of whether all quests are complete.
If player is actively completing a quest at 9PM
delay summary trigger until that quest is marked
complete or 9:30PM whichever comes first.

FULL SUMMARY SCREEN:
Full screen dark overlay.
Animated reveal.
Feels like end of battle debrief.

SUMMARY CONTENT:

Header section:
DAY [X] COMPLETE — [DATE]
HUNTER: [Username]
STREAK: [X] days fire emoji

Performance section:
Quests Completed: X of X total
EXP Earned Today: [X] EXP
Per path breakdown with quests and EXP per path
Total EXP toward next level with progress bar

Highlights section — show HIGHEST PRIORITY
that applies today:

Priority 1: Level up occurred today
"LEVEL UP — You are now Level [X] Hunter."

Priority 2: New rank unlocked today
"Rank [X] quests are now available."

Priority 3: Streak milestone hit today
Milestones: 7 14 21 30 60 90 days
"Streak milestone: [X] days straight."

Priority 4: Multiplier tier upgraded today
"Multiplier increased: You are now at [X]x grind."

Priority 5: Armor piece forged today
"Your [piece name] has been forged.
The knight grows stronger."

Priority 6: Elixir completed today
"Elixir complete. Your body absorbs the
transformation."

Priority 7: Freedom Day token earned today
"Freedom Day earned. Rest when you choose Sage."

Priority 8: Personal best EXP day
"Personal best: Most EXP earned in a single day."

Priority 9: No milestone — default message
"Consistent. Deliberate. Unstoppable.
See you tomorrow."

Tomorrow preview section:
Shows quest CATEGORIES only — never specific
quest titles.
Prevents gaming by waiting for easier quests.

Example category previews:
Fitness Warrior: "Strength training focus tomorrow."
Mindset Sage: "Knowledge Forging focus tomorrow."
Discipline Knight: "Deep work focus tomorrow."
Health Alchemist: "Purification focus tomorrow."
Grind Visionary: "Workshop and shipping focus
tomorrow."

If tomorrow is rest day for Fitness Warrior:
"Recovery quests available tomorrow. Rest earned."

If tomorrow is Monday:
"Weekly Boss Quest available tomorrow."

Buttons at bottom of summary:
[Share Today's Summary] →
Generates shareable achievement card showing
day number EXP earned streak paths active
app branding.

[See Tomorrow's Preview] →
Shows category-level preview for all active paths.
Read only — cannot complete tomorrow's quests early.

[Close] →
Returns to dashboard.

---

## Data Models Needed

Review all existing models before creating
any of these. Extend existing models where
possible. Confirm against existing quests
app models especially PlayerDailyQuestAssignment.

DailyQuestLineup:
- user (FK)
- path (char)
- date (date)
- generated_at (datetime)
- quests_assigned (JSON array of quest IDs)
- universal_quest_id (FK to Quest)
- bonus_slot_quest_id (FK to Quest nullable)
- intention (char — F S R for Full Steady Recovery)

DailyQuestCompletion:
- user (FK)
- quest (FK)
- path (char)
- date (date)
- completed_at (datetime)
- exp_earned (integer — after multiplier applied)
- swapped_from_quest_id (FK to Quest nullable)

QuestFeedback:
- user (FK)
- quest (FK)
- feedback (char — U for up D for down)
- given_at (datetime)

QuestPreference:
- user (FK)
- quest (FK)
- preference_score (integer running total)
- completion_count (integer)
- skip_count (integer)
- swap_count (integer)
- last_suggested (date)
- last_completed (date)

DailyIntention:
- user (FK)
- date (date)
- intention (char — F S R)

DailySwap:
- user (FK)
- path (char)
- date (date)
- swap_count (integer)
- swapped_from_quest_id (FK to Quest)
- swapped_to_quest_id (FK to Quest)
- swapped_at (datetime)

CrossPathBonus:
- user (FK)
- date (date)
- pair_type (char — identifier for which pair)
- quest_one_id (FK to Quest)
- quest_two_id (FK to Quest)
- bonus_exp (integer)
- awarded (boolean)
- awarded_at (datetime nullable)

DailyCompletionSummary:
- user (FK)
- date (date)
- total_quests (integer)
- completed_quests (integer)
- total_exp_earned (integer)
- streak_day (integer)
- highlight_type (char)
- highlight_text (text)
- paths_summary (JSON)

---

## API Endpoints Needed

Follow existing API patterns in:
backend/quests/views.py
backend/quests/services.py

Suggested endpoints:

GET /api/quests/daily/
Get today's pre-generated lineup for all
active paths.
Returns lineup per path with quest details
slot types and cross-path bonus flags.

POST /api/quests/daily/complete/
Mark a quest as complete for today.
Request: quest_id path
Returns: EXP earned streak update
any milestone triggered.

POST /api/quests/daily/swap/
Swap a suggested quest for an alternative.
Request: quest_id path replacement_quest_id
Returns: updated lineup or error if swap
limit reached.

POST /api/quests/feedback/
Submit thumbs up or down feedback on a quest.
Request: quest_id feedback (U or D)
Returns: confirmation.

POST /api/quests/intention/
Set daily intention for today.
Request: intention (F S R)
Returns: updated lineup based on intention.

GET /api/quests/summary/today/
Get end of day summary data.
Returns: completion stats EXP earned
highlights tomorrow preview categories.

GET /api/quests/alternatives/
Get swap alternatives for a quest.
Request: quest_id path
Returns: up to 6 alternative quests
ordered by preference score.

---

## Build Order For This System

Build in this exact order.
Complete each step before moving to next.

Step 1: Data models and migrations
Step 2: Five-layer algorithm as management
command or Celery task
Step 3: Timezone-aware midnight scheduler
Step 4: Quest completion and expiry endpoints
Step 5: Swap system endpoints
Step 6: Quest feedback endpoints
Step 7: Frontend quest board with progressive
complexity reveal
Step 8: Completion ring component
Step 9: Daily intention prompt
Step 10: End of day summary screen
Step 11: Cross-path bonus display
Step 12: Missed day logic and return experience

---

## Important Implementation Notes

1. The five-layer algorithm must run server-side
   only as a Django management command or
   Celery task. Never run on-demand at app open.
   Always pre-generate at midnight local time.
   Store results in DailyQuestLineup model.
   Serve instantly from database when player
   opens app.

2. All EXP calculations including multipliers
   and cross-path bonuses must be server-side
   only. Never calculate EXP on frontend.

3. Timezone must be stored per user on signup.
   All time-sensitive logic uses player local
   timezone. Midnight reset expiry notifications
   and end of day summary all use local time.

4. Completion ring must update in real time
   as quests are completed. No page refresh.
   Use polling or websocket for live update.

5. Tomorrow preview must show categories only.
   Never show specific quest titles in preview.
   This is a hard rule. Prevents gaming.

6. Never shame player for missing a day.
   All missed day language is forward-facing.
   Return screen shows for exactly 3 seconds
   then automatically transitions to dashboard.

7. Cross-path bonuses are always exempt from
   Recovery day filtering. This is confirmed
   and final. Do not filter them on Recovery days.

8. The progressive complexity reveal is a UI
   change only. The algorithm runs identically
   from Day 1. Only what the player sees changes
   based on how many days they have been active.

9. Swap alternatives query must exclude quests
   already in today's lineup quests on cooldown
   and quests failing hard filters. Return
   maximum 6 alternatives ordered by preference
   score descending.

10. Weekly Boss Quest appears every Monday and
    resets Monday at 00:00 local time.
    Grind Visionary boss quest EXP must have
    the XP multiplier applied using the same
    server-side multiplier utility function.

11. The DailyQuestLineup model should extend or
    replace PlayerDailyQuestAssignment if that
    model already exists. Inspect the existing
    model carefully before deciding whether to
    extend or replace. Show developer the plan
    before making any changes to existing models.