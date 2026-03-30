# Fitness Warrior Path
# docs/game-design/paths/fitness-warrior.md

---

## How To Use This File

Read this file when:
- Building Fitness Warrior onboarding flow
- Seeding Fitness Warrior quest data
- Building split day tracking logic
- Building rest day recovery quest logic
- Building Fitness Warrior daily override logic

Always read these files first before this one:
- AGENTS.md
- docs/architecture.md
- docs/phase-5b-quest-system-redesign.md
- docs/game-design/README.md
- docs/game-design/BUILD_ORDER.md

---

## Path Overview

Path name: Fitness Warrior
Player identity: Hybrid athlete
Target audience: Gym-oriented fitness-aware users
who already train and understand their body.
Not beginners. These users know what PPL macros
and PRs are.

Goal of this path: Gamify the existing fitness
lifestyle. Reward what the player is already doing.
Keep them motivated accountable and socially engaged.

Vibe: Train hard across strength cardio and mobility.
The body is the weapon. Forge it daily.

---

## Four Pillars

This path does not use named pillars in the same
way as other paths. Quests are organized by
training type:
- Strength and lifting
- Cardio and endurance
- Hybrid training
- Recovery and mobility
- Nutrition and fuel

---

## Onboarding Questions

Opening line shown to player:
"Let's build your training profile Hunter.
4 questions. 30 seconds."

Q1 — Training Split:
Options:
- PPL (Push Pull Legs)
- Full Body
- Bro Split (Chest Back Arms Legs)
- Calisthenics
- Cardio Focused
- Custom

Q2 — Primary Goal:
Options:
- Muscle Gain
- Fat Loss
- Recomp (both)
- General Performance

Q3 — Training Days Per Week:
Options:
- 3 days
- 4 days
- 5 days
- 6 days
- 7 days

Q4 — Experience Level:
Options:
- Beginner (under 1 year)
- Intermediate (1 to 3 years)
- Advanced (3+ years)

Save all four answers to player profile.
User can update anytime in settings.

---

## Split Day Start Question

After Q1 if PPL or Bro Split is selected
show one additional question:

"What day of your split are you on today?"
Options:
- Push Day
- Pull Day
- Leg Day
- Rest Day
- Starting Fresh

Save answer to SplitDayState model.
App rotates split day automatically each day.
PPL rotation: Push then Pull then Legs then repeat.
Bro Split rotation follows user-defined order.

---

## Experience-Based Quest Visibility

Beginner: D rank and C rank visible at start
Intermediate: D rank C rank B rank visible at start
Advanced: All ranks visible D rank optional

This overrides default rank unlock by level
for initial visibility only.
Level-based EXP unlock rules still apply.

---

## Universal Daily Quests

These appear every day for ALL Fitness Warriors
regardless of split or experience level.
These fill the locked Universal Slot.
Cannot be swapped by player.

- Hit your protein target today
  EXP: 35
  Rank: D
  Cooldown: None

- Complete your workout today
  EXP: 45
  Rank: D
  Cooldown: None

- Drink 3L of water
  EXP: 25
  Rank: D
  Cooldown: None

- Sleep 7+ hours
  EXP: 30
  Rank: D
  Cooldown: None

- End post-workout shower with 60 seconds cold water
  EXP: 75
  Rank: C
  Cooldown: None

---

## Rank D Quests — Level 1 and above

- Complete 20 pushups
  EXP: 40
  Cooldown: None

- Walk 5000 steps
  EXP: 35
  Cooldown: None

- Stretch for 10 minutes
  EXP: 30
  Cooldown: None

- Do a 10 minute bodyweight workout
  EXP: 45
  Cooldown: None

- Drink water before every meal today
  EXP: 25
  Cooldown: None

---

## Rank C Quests — Level 5 and above

- Complete a 30 minute workout
  EXP: 80
  Cooldown: None

- Run or jog 3km
  EXP: 90
  Cooldown: None

- Do 5 sets of any compound lift
  EXP: 100
  Cooldown: 1 day

- Complete 100 pushups in a day
  EXP: 85
  Cooldown: None
  Note: Can be broken into sets throughout day

- Complete 20 minutes of calisthenics
  EXP: 85
  Cooldown: None

- Train for 5 consecutive days
  EXP: 110
  Cooldown: 7 days

- Eat a fat-burning focused meal today
  EXP: 70
  Cooldown: None

- Track macros for 3 consecutive days
  EXP: 90
  Cooldown: 7 days

- Cook a high protein meal from scratch
  EXP: 75
  Cooldown: None

---

## Rank B Quests — Level 10 and above

- Complete a full push pull legs session
  EXP: 150
  Cooldown: 1 day

- Run 5km without stopping
  EXP: 160
  Cooldown: 2 days

- Train 6 days this week
  EXP: 180
  Cooldown: 7 days

- Do 10 minutes mobility work post-workout
  EXP: 120
  Cooldown: None

- Beat your previous PR on any lift
  EXP: 170
  Cooldown: 3 days
  Note: Self-reported honor system

- Complete a cardio finisher after lifting
  EXP: 130
  Cooldown: 1 day

- Complete a calisthenics-only workout
  EXP: 140
  Cooldown: None

- Run 5km and do a strength session same day
  EXP: 175
  Cooldown: 2 days

- Complete a 45 minute uninterrupted workout
  EXP: 145
  Cooldown: None

---

## Rank A Quests — Level 20 and above

- Complete a 60 minute strength and cardio session
  EXP: 250
  Cooldown: 1 day

- Run 10km
  EXP: 280
  Cooldown: 3 days

- Complete a full body workout twice in one day
  EXP: 260
  Cooldown: 3 days
  Note: AM and PM split

- Train 7 days straight
  EXP: 300
  Cooldown: 14 days

- Complete a hybrid training session
  EXP: 270
  Cooldown: 2 days
  Note: Must include strength cardio and mobility
  in one session

- Log a 3 month consistent training streak
  EXP: 400
  Cooldown: One-time only

- Complete a 90 minute training session
  EXP: 265
  Cooldown: 2 days

---

## Rank S Quests — Level 30 and above

- Complete a 90 minute hybrid training session
  EXP: 450
  Cooldown: 2 days

- Run a half marathon (21km)
  EXP: 600
  Cooldown: 7 days

- Train every day for 30 days straight
  EXP: 700
  Cooldown: 30 days

- Set a new PR on 3 lifts in one week
  EXP: 500
  Cooldown: 7 days

- Complete 1000 reps in a single day
  EXP: 550
  Cooldown: 5 days
  Note: Any exercise counts toward the 1000

- Complete 6 weeks of unbroken training consistency
  EXP: 800
  Cooldown: One-time only

---

## Rest Day Recovery Quests

On scheduled rest days the app loads this recovery
quest set instead of the normal quest pool.
Rest day is determined by split day state.
Rest day quests have no cooldowns.
They exist so players earn EXP every single day
including rest days.

- Active recovery walk (20 minutes)
  EXP: 40
  Rank: D

- Stretch for 15 minutes
  EXP: 35
  Rank: D

- Sleep 8+ hours tonight
  EXP: 30
  Rank: D

- Full cold shower
  EXP: 75
  Rank: C

- Foam roll for 10 minutes
  EXP: 35
  Rank: D

- Do 15 minutes of yoga or mobility work
  EXP: 45
  Rank: D

- Eat a clean recovery meal today
  EXP: 40
  Rank: D

---

## Split Day Quest Surfacing Logic

On Push Day:
Surface chest shoulder tricep focused quests
at top of assigned slots regardless of weekly rhythm.
Examples: bench press variations, overhead press,
push movements, tricep work.

On Pull Day:
Surface back and bicep focused quests at top.
Examples: row variations, deadlift, pull movements,
bicep work.

On Leg Day:
Surface squat and hinge focused quests at top.
Examples: squat variations, deadlift, leg press,
lunge movements.

Player can always swap any surfaced quest
from their full pool.
Surfacing only affects default sort order
not what is available.

---

## Weekly Boss Quest

Appears every Monday. Resets Monday at 00:00.
Completion awards EXP plus exclusive weekly badge.

Rotating examples:

Week option 1:
"Train 6 days and hit protein target 5 out of 7 days"
EXP: 400
Badge: Weekly Warrior

Week option 2:
"Complete 3 cardio sessions and 3 strength sessions
this week"
EXP: 380
Badge: Hybrid Week

Week option 3:
"Hit a new PR and complete a 5km run in the same week"
EXP: 420
Badge: Peak Performance

Week option 4:
"Complete your workout every day this week"
EXP: 390
Badge: No Days Off

Week option 5:
"Complete a hybrid session and a rest day recovery
routine this week"
EXP: 360
Badge: Smart Warrior

---

## Adaptive Difficulty Nudge

If player completes all daily quests for
7 consecutive days trigger nudge on Day 8:

"You are dominating your current quests Hunter.
Ready to increase the challenge?"

Options:
- Yes show me harder quests
- Not yet keep current quests

If yes:
Swap D rank daily quests for C rank equivalents.
Surface more B rank quests in assigned slots.

---

## Cross-Path Bonus

Cold shower quest completed in both Fitness Warrior
AND Health Alchemist on same day:
Award +20 EXP bonus to both quests.
Message: "Body and mind forged together."

---

## Social Features

Achievement cards auto-generated for:
- Level up
- Rank unlock
- Streak milestones (7 14 21 30 60 90 days)
- Boss quest completion
- PR beaten
- Half marathon completed
- 30 day training streak

Badges for this path:
- 30-Day Warrior: 30 day training streak
- 1000 Rep Club: complete 1000 reps in one day
- S-Rank Unlocked: reach Level 30
- Half Marathon Hunter: complete 21km run quest
- Weekly Boss Slayer: complete weekly boss quest
- Hybrid Elite: complete hybrid training session
  quest 10 times

Leaderboard:
Weekly EXP leaderboard among all Fitness Warriors.
Resets every Monday at 00:00.
Shows top 10 globally plus user own rank.

Profile visibility:
Public by default.
Private option available in settings.
Public profile shows: level rank streak badges
recent achievements training split goal.

---

## Warrior-Sage Cross-Path Identity Title

If user has both Fitness Warrior and Mindset Sage
paths active and completes quests on both for
7 consecutive days:
Unlock profile title: Warrior-Sage
Unique badge and achievement card generated.
Displayed on public profile.

---

## Day 1 Starter Lineup

On the player's very first day the algorithm
does not run. Use this hardcoded lineup instead:

Quest 1: Complete 20 pushups (40 EXP D rank)
Quest 2: Walk 5000 steps (35 EXP D rank)
Quest 3: Hit your protein target today (35 EXP D rank)

Algorithm takes over from Day 2 onwards.

---

## Important Implementation Notes

1. Split day tracking assumes the app knows what
   day of the PPL split the user is on.
   On first setup ask the split day start question.
   Rotate automatically each subsequent day.
   Player can reset split day anytime in settings.

2. Equipment profile question is not in Fitness
   Warrior onboarding. It is in Health Alchemist.
   Fitness Warrior quests do not gate on equipment.

3. The beat your PR quest is self-reported and
   unverifiable. This is intentional — honor system.
   UI should acknowledge this clearly on the quest card.

4. Cold shower quest appears in both Fitness Warrior
   universal daily quests and Health Alchemist quests.
   This is intentional — cross-path bonus applies.

5. Nutrition quests like hit protein target and
   track macros appear in Fitness Warrior because
   a hybrid athlete needs both training and fuel.
   Do not move these to Health Alchemist only.

6. All quest completions are self-reported.
   No verification required for V1.