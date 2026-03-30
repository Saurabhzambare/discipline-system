# Discipline Knight Path
# docs/game-design/paths/discipline-knight.md

---

## How To Use This File

Read this file when:
- Building Discipline Knight onboarding flow
- Building Oath Screen and Discipline Code system
- Seeding Discipline Knight quest data
- Building Armor System
- Building War Room planning tool
- Building Temptation Log
- Building Knight Weekly Report
- Building Discipline Knight daily override logic

Always read these files first before this one:
- AGENTS.md
- docs/architecture.md
- docs/phase-5b-quest-system-redesign.md
- docs/game-design/README.md
- docs/game-design/BUILD_ORDER.md

---

## Path Overview

Path name: Discipline Knight
Player identity: Armor forged through daily
consistency
Target audience: People who want to build an
unbreakable daily routine. Not beginners looking
for motivation — people serious about building
systems that run automatically.

Goal of this path: The user forges their discipline
piece by piece like armor. Every completed week adds
armor to their public profile. The world can see how
far they have come. Breaking consistency cracks the
armor visibly. Honoring their code makes them
stronger.

Vibe: Progressive — discipline builds slowly like
armor. Honorable and code-based. Structured but
human. The knight does not negotiate with excuses.

---

## Six Pillars

Pillar names must appear everywhere in the UI —
quest cards dashboard headers progress breakdowns
onboarding screens.

The War Room
- Covers: Time Management and Scheduling

The Forge
- Covers: Habit Building and Consistency

The Siege
- Covers: Focus and Deep Work

The Iron Will
- Covers: Resisting Temptation and Urges

The Treasury
- Covers: Financial Discipline

The Kingdom
- Covers: Environment and Lifestyle Design

---

## Onboarding Questions

Opening line shown to player:
"Discipline is not a talent. It is armor.
Built piece by piece day by day.
Let us begin forging yours."

Q1 — What does your current daily routine
look like?
Options:
- I Have No Routine
- I Have A Partial Routine
- I Have A Routine But Break It Often
- I Have A Solid Routine And Want To Level It Up

Q2 — What is your biggest discipline challenge?
Options:
- Waking Up Consistently
- Staying Focused
- Resisting Distractions
- Managing Money
- All Of Them

Q3 — How structured do you want your quest
assignments?
Options:
- Fully Structured — Tell Me Exactly What To Do
- Semi-Structured — Give Me Options
- Flexible — I Will Choose From The Pool

Q4 — How many hours per day can you dedicate
to discipline building?
Options:
- 30 Minutes
- 1 Hour
- 2 Hours
- As Much As It Takes

Save all four answers to player profile.
User can update anytime in settings.

---

## Experience-Based Quest Visibility

I Have No Routine:
D rank and C rank visible at start

I Have A Partial Routine or I Have A Routine
But Break It Often:
D rank C rank B rank visible at start

I Have A Solid Routine:
All ranks visible

---

## Oath Screen

Shown AFTER Q4 and BEFORE dashboard loads.
This is part of onboarding not a separate page.

Opening message:
"Before you don your armor Knight — you must
swear your code. These are the rules you commit
to living by. Break them and your armor cracks.
Honor them and you become unbreakable."

User writes 3 to 5 personal rules in free
text fields.
Show these example rules as inspiration only —
not as defaults:
- I will wake up at the same time every day
- I will complete my most important task before
  checking my phone
- I will not spend money on things that do not
  serve my goals
- I will do what I said I would do
- I will not negotiate with my own excuses

After user submits their code display this
consequence message:
"Your code is sworn Knight. It is now part of
your armor. Honor it and you grow stronger.
Break it and your armor will show the world."

CONTENT MODERATION:
Discipline Code text must pass through a
server-side content moderation filter before
saving.
If flagged show message:
"Your code contains content that violates
community guidelines. Please rewrite it Knight."
Code is not saved until it passes the filter.
Basic keyword filtering is sufficient for V1.

DISCIPLINE CODE STORAGE:
Save to DisciplineCode model linked to player.
User can update their code from settings
at any time.
When updated show message:
"Your code has been reforged Knight. Honor it
with even greater conviction."
Previous code versions saved to profile history —
not public but visible to user.

WHERE THE CODE APPEARS:
- Displayed on public profile beneath
  armor visualization
- Shown briefly every morning when app opens
  before quest board loads — 3 second display
  with fade
- Referenced in Honor Review quest every Sunday
- Shown on achievement cards when shared

---

## Universal Daily Quests

These appear every day for ALL Discipline Knights
regardless of routine level or experience.
These fill the locked Universal Slot.
Cannot be swapped by player.

- Write tomorrow's schedule tonight
  EXP: 35
  Rank: D
  Cooldown: None

- Make your bed immediately after waking
  EXP: 25
  Rank: D
  Cooldown: None

- Complete one task before checking your phone
  EXP: 35
  Rank: D
  Cooldown: None

- Open War Room and set top 3 priorities
  for today
  EXP: 35
  Rank: D
  Cooldown: None

---

## Rank D Quests — Level 1 and above

The War Room:
- Write tomorrow's schedule tonight
  EXP: 35
  Cooldown: None

- Review your schedule at midday
  EXP: 25
  Cooldown: None

The Forge:
- Wake up at the same time as yesterday
  EXP: 30
  Cooldown: None

- Complete your morning routine without
  skipping a step
  EXP: 35
  Cooldown: None

The Siege:
- Complete one task before checking your phone
  EXP: 35
  Cooldown: None

- Work for 30 minutes with zero distractions
  EXP: 35
  Cooldown: None

The Iron Will:
- Resist one temptation you normally give into
  EXP: 35
  Cooldown: None

- Say no to one unnecessary purchase today
  EXP: 30
  Cooldown: None

The Treasury:
- Write down every purchase you made today
  and how it made you feel
  EXP: 35
  Cooldown: None

- Identify one recurring expense you could
  eliminate
  EXP: 30
  Cooldown: None

The Kingdom:
- Make your bed immediately after waking
  EXP: 25
  Cooldown: None

- Clean your workspace before starting your day
  EXP: 30
  Cooldown: None

---

## Rank C Quests — Level 5 and above

The War Room:
- Plan your full day in time blocks
  EXP: 80
  Cooldown: None

- Complete your full planned schedule for
  the day
  EXP: 95
  Cooldown: None

- Do a brain dump — write every open loop
  in your head
  EXP: 90
  Cooldown: None

The Forge:
- Go to bed at your target sleep time
  EXP: 75
  Cooldown: None

- Complete your morning routine perfectly for
  3 consecutive days
  EXP: 90
  Cooldown: 3 days

The Siege:
- Do 90 minutes of deep focused work
  EXP: 90
  Cooldown: None

- Identify your single most important task
  and do it first
  EXP: 85
  Cooldown: None

- Work in a new environment today —
  library cafe or park
  EXP: 100
  Cooldown: None

The Iron Will:
- Delete or disable one distracting app
  for 24 hours
  EXP: 85
  Cooldown: None

- Before any non-essential purchase wait
  24 hours and then decide
  EXP: 80
  Cooldown: None

The Treasury:
- Define a savings goal today — write the
  exact amount and deadline
  EXP: 80
  Cooldown: None

- Identify 3 non-essential subscriptions
  you could cancel
  EXP: 75
  Cooldown: None

- Cook your own meal instead of ordering out
  EXP: 70
  Cooldown: None

The Kingdom:
- Remove one source of friction from your
  daily routine
  EXP: 85
  Cooldown: None

- Set up your workspace the night before
  EXP: 75
  Cooldown: None

- Eliminate one bad environmental trigger today
  EXP: 90
  Cooldown: None

---

## Rank B Quests — Level 10 and above

The War Room:
- Complete every task on your daily schedule
  EXP: 150
  Cooldown: None

- Wake up at 5AM and complete morning routine
  EXP: 155
  Cooldown: None

- Do a full life audit — time money habits
  and environment
  EXP: 160
  Cooldown: 30 days

The Forge:
- Maintain your full routine for 5 consecutive
  days
  EXP: 170
  Cooldown: 7 days

- Honor Review — read Discipline Code rate
  yourself 1 to 10 write what you honored
  and what you broke
  EXP: 160
  Cooldown: 7 days
  Available: Sunday only
  Note: Show countdown on quest card other days
  "Available Sunday — [X] days away"

The Siege:
- Complete a 3 hour deep work session
  uninterrupted
  EXP: 160
  Cooldown: 1 day

- Complete a full Pomodoro session —
  4 rounds of 25 minutes
  EXP: 130
  Cooldown: None

- Turn off all notifications for 4 hours
  EXP: 120
  Cooldown: None

- Complete your hardest task at your peak
  energy time
  EXP: 140
  Cooldown: None

The Iron Will:
- Resist your biggest temptation for an
  entire day
  EXP: 165
  Cooldown: None

- Complete a no-phone morning — no phone
  until noon
  EXP: 150
  Cooldown: 2 days

The Treasury:
- Track all spending for 7 consecutive days
  EXP: 170
  Cooldown: 7 days

- Do a weekly financial review — income
  expenses and savings
  EXP: 160
  Cooldown: 7 days

- Go one full day spending zero on
  non-essentials
  EXP: 140
  Cooldown: None

The Kingdom:
- Design your ideal morning environment —
  lay out clothes prep food set space
  EXP: 120
  Cooldown: None

- Do a full environment audit — identify
  3 things slowing you down
  EXP: 140
  Cooldown: None

- Create one system that automates a
  recurring decision
  EXP: 160
  Cooldown: None

---

## Rank A Quests — Level 20 and above

The War Room:
- Execute your full schedule perfectly for
  7 consecutive days
  EXP: 300
  Cooldown: 7 days

The Forge:
- Build and follow a complete daily routine
  for 14 days
  EXP: 320
  Cooldown: 14 days

The Siege:
- Complete deep work sessions every day
  for 7 days
  EXP: 280
  Cooldown: 7 days

The Iron Will:
- Complete a 30 day no-impulse-buy challenge
  EXP: 350
  Cooldown: 30 days

The Treasury:
- Spend zero on non-essentials for
  7 consecutive days
  EXP: 270
  Cooldown: 7 days

The Kingdom:
- Redesign your entire daily environment
  for optimization
  EXP: 260
  Cooldown: 14 days

---

## Rank S Quests — Level 30 and above

The War Room:
- Execute your full schedule without deviation
  for 21 days
  EXP: 680
  Cooldown: 21 days

The Forge:
- Maintain a perfect daily routine for
  30 consecutive days
  EXP: 700
  Cooldown: 30 days

The Siege:
- Complete deep work every single day
  for 30 days
  EXP: 650
  Cooldown: 30 days

The Iron Will:
- Build a habit so automatic it requires
  zero willpower
  EXP: 750
  Cooldown: One-time only

The Treasury:
- Save a defined financial goal amount
  within one month
  EXP: 600
  Cooldown: 30 days

The Kingdom:
- Design a life system so optimized it
  runs itself
  EXP: 800
  Cooldown: One-time only

---

## Armor System

This mechanic is the primary consistency reward
for the Discipline Knight path.
Armor is fully public — visible to all players
on leaderboard and profile pages.

ARMOR PROGRESSION:
Each week of completed daily quests forges one
piece of armor onto the knight's visual profile.

Week 1: Boots forged
Week 2: Gauntlets forged
Week 3: Chest Plate forged
Week 4: Shoulder Guards forged
Week 5: Helmet forged
Week 6: Shield and Sword forged —
fully armored knight

Each new piece triggers a forging animation
on dashboard:
"Your discipline has been tested and proven
Knight. The forge rewards you."
Armor piece appears on knight silhouette
with fire animation.

FULL ARMOR MILESTONE:
When all 6 pieces are forged:
Full screen animation — knight stands fully
armored sword raised.
Message: "You are fully forged Knight.
Your discipline is unbreakable."
Unlock title: The Fully Forged Knight
on public profile.
500 bonus EXP awarded.
Exclusive achievement card generated for sharing.

ARMOR PRESTIGE:
After full armor achieved if user maintains
perfect consistency for another 6 weeks:
Armor color shifts from silver to gold visually.
Title upgrades to The Golden Knight.
New achievement card generated.

CRACK MECHANIC:
If consistency breaks before a week completes:
Most recently forged armor piece shows a
visible crack on public profile.
Armor does NOT disappear — crack is visible
to all players.
Message: "Your armor has been tested Knight.
Return to the forge."
Repairing a cracked piece requires 3 consecutive
days of full quest completion.
Once repaired crack disappears and progression
resumes.

GRACE TOKEN MECHANIC:
Each armor piece has one Grace Token per
calendar month.
Resets on first day of each calendar month.
If user misses one day and has unused
Grace Token:
Armor does NOT crack.
Token is consumed.
Message: "Life happens Knight. Your grace has
been invoked. Your armor holds — but only once."
Missing two days in a row still cracks armor
regardless of Grace Token.

STREAK SHIELD MECHANIC:
Earned by completing 14 consecutive days of
full quest completion.
Activates automatically when a day is missed
after Grace Token is already used.
Protects streak and armor from cracking —
one time use.
Message on activation:
"Your past discipline has protected you Knight.
The shield has been used."
User must earn another 14 consecutive days
to receive a new shield.
Shield icon displayed visibly on dashboard
when active.

---

## War Room Planning Tool

A built-in daily planning tool inside the app.
Accessible as a dedicated tab on the dashboard.

MORNING PLANNING:
User opens War Room each morning.
Sets top 3 priorities for the day.
Optionally time-blocks their schedule.
Completing morning War Room planning: 35 EXP

EVENING REVIEW:
User returns to War Room in the evening.
Marks which priorities and blocks were completed.
Completing evening War Room review: 35 EXP

DAILY BONUS:
Both morning planning AND evening review
completed same day: +20 EXP bonus.
Message: "A knight who plans and reviews
is a knight who improves."

WAR ROOM DATA:
Store daily morning and evening completion
as separate boolean fields per user per day
in WarRoomEntry model.
Used to generate Knight Weekly Report
every Sunday.

---

## Temptation Log

A simple logging tool unique to Iron Will quests.
Accessible from dashboard.

When user completes an Iron Will quest they are
optionally prompted to log the temptation:
- What was the temptation? (free text)
- Did you resist? Yes / Partially / No
- How did it feel? (optional free text)

Entries saved privately to user profile.

MILESTONE:
At 30 logged temptation resistances:
"Iron Will achieved — you have faced your
temptations 30 times and chosen strength."
Iron Will badge plus achievement card generated.

---

## Knight Weekly Report

Auto-generated every Sunday.
Delivered as a notification and viewable in
profile history.

Report contains:
- Total quests completed vs total available
  this week
- Current armor status and any cracks
- Discipline Code honor rating (from Honor
  Review if completed that Sunday)
- Top performing pillar this week
- Weakest pillar this week
- War Room completion rate (morning plus
  evening planning)
- One personalized improvement suggestion
  based on data
- Current streak and shield status

PERSONALIZED SUGGESTION LOGIC:
If Siege pillar completion below 50% this week:
"Your focus wavered this week Knight. Tomorrow
morning identify your single most important task
before anything else."

If Treasury quests all missed this week:
"Your Treasury was neglected this week. Start
small — write down every purchase tomorrow
and notice how it feels."

If Forge quests all missed this week:
"Your routine broke this week Knight. Tomorrow
just make your bed and set your schedule.
Start there."

If War Room completion below 50%:
"Your planning slipped this week. Five minutes
of planning saves hours of confusion. Open the
War Room first thing tomorrow."

If all pillars strong:
"Exceptional discipline this week Knight.
The armor is holding. Keep forging."

---

## Weekly Boss Quest

Appears every Monday. Resets Monday at 00:00.
Completion awards EXP plus exclusive weekly badge.

Rotating examples:

Week option 1:
"Complete War Room morning and evening planning
every day this week"
EXP: 420
Badge: War Room Commander

Week option 2:
"Resist your biggest temptation every day
this week"
EXP: 400
Badge: Iron Will Week

Week option 3:
"Complete deep work sessions every day
this week"
EXP: 410
Badge: Siege Master

Week option 4:
"Follow your full routine without breaking
for 7 days"
EXP: 450
Badge: The Unbroken

Week option 5:
"Complete your Honor Review and full financial
review this week"
EXP: 390
Badge: The Auditor

---

## Adaptive Difficulty Nudge

If player completes all daily quests for
7 consecutive days trigger nudge on Day 8:

"You are holding the line Knight. Ready to
forge harder?"

Options:
- Yes increase the challenge
- Not yet keep current quests

If yes:
Surface more B rank quests in assigned slots.
Upgrade D rank daily quests to C rank
equivalents.

---

## Cross-Path Bonuses

Deep work quest completed in Discipline Knight
same day as Mastery Lab quest in Grind Visionary:
Award +20 EXP bonus to both quests.
Message: "Discipline fuels the vision."

5AM wake up completed in both Discipline Knight
AND Mindset Sage on same day:
Award +25 EXP bonus to both quests.
Message: "The early hours belong to the
disciplined mind."

---

## Social Features

Achievement cards auto-generated for:
- Level up
- Rank unlock
- Each armor piece forged
- Full armor achieved — The Fully Forged Knight
- Gold prestige achieved — The Golden Knight
- Streak Shield earned
- Iron Will milestone — 30 temptation resistances
- Boss quest completion
- The Complete Human title unlocked
- Honor Review completed 4 weeks in a row

Badges for this path:
- The Squire: path selected and oath sworn
- First Forge: Week 1 armor complete
- Fully Forged: All 6 armor pieces complete
- The Golden Knight: Prestige armor achieved
- Iron Will: 30 temptation resistances logged
- War Room Commander: War Room completed
  30 days straight
- The Siege Master: Deep work completed
  30 days straight
- The Complete Human: All 4 paths active
  7 consecutive days

ARMOR LEADERBOARD:
Permanent all-time leaderboard showing most
armor pieces forged globally.
Shows armor prestige status (silver or gold).
This leaderboard does not reset weekly.

WEEKLY EXP LEADERBOARD:
Weekly EXP leaderboard among all Discipline
Knights.
Resets every Monday at 00:00.
Shows top 10 globally plus user own rank.

Profile visibility:
Public by default.
Private option available in settings.
Public profile shows: armor visualization with
any cracks level rank streak badges
Discipline Code beneath armor recent achievements.

---

## Day 1 Starter Lineup

On the player's very first day the algorithm
does not run. Use this hardcoded lineup instead:

Quest 1: Make your bed immediately after waking
(25 EXP D rank)
Quest 2: Write tomorrow's schedule tonight
(35 EXP D rank)
Quest 3: Clean your workspace before starting
your day (30 EXP D rank)

Algorithm takes over from Day 2 onwards.

---

## Daily Override Logic

Every Sunday:
Honor Review quest automatically fills one
assigned slot.
Available Sunday only.
Locked on all other days with countdown shown:
"Available Sunday — [X] days away."
Show lock icon on quest card other days.

War Room morning planning quest:
Always fills first assigned slot every day.
Cannot be swapped by player.

If armor piece is cracked:
Surface Forge pillar quests in majority of
assigned slots to prioritize repair over
other pillars.

---

## Important Implementation Notes

1. Discipline Code content moderation must run
   server-side before saving. If flagged user
   must rewrite before saving is allowed.
   Previous code versions are saved to profile
   history — not public but visible to user.

2. Armor visibility is fully public. All players
   can see which armor pieces are forged and
   which are cracked on public profiles and
   the armor leaderboard.

3. Grace Token resets on first day of each
   calendar month. One token per armor piece
   per month. Missing two days in a row cracks
   armor regardless of Grace Token status.

4. Streak Shield auto-activates on missed day
   only after Grace Token is already used for
   that month. Requires 14 consecutive days
   to earn. Requires 14 more consecutive days
   after use to re-earn.

5. Honor Review quest is only available on
   Sundays. Show countdown timer on quest card
   on all other days. This is a hard rule —
   do not make it available other days.

6. War Room morning planning quest always fills
   first assigned slot. It cannot be swapped.
   This is the anchor quest for this path.

7. Knight Weekly Report generates every Sunday
   automatically. It uses War Room data quest
   completion rates armor status and pillar
   breakdown. Build as automated Sunday task.

8. The Treasury quests use awareness and behavior
   framing not tracking infrastructure. No expense
   tracking feature needed. Quests ask users to
   write observe and reflect — not sync bank accounts.

9. Discipline Code displays on public profile
   beneath armor visualization. Users must be
   aware their code is visible publicly when
   they write it. Add clear note during oath screen.

10. All quest completions are self-reported.
    No verification required for V1.