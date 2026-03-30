# Grind Visionary Path
# docs/game-design/paths/grind-visionary.md

---

## How To Use This File

Read this file when:
- Building Grind Visionary onboarding flow
- Seeding Grind Visionary quest data
- Building XP Multiplier system
- Building Vision Board feature
- Building Skill Tree per grind focus
- Building Output Log feature
- Building Accountability Partner system
- Building First Dollar legendary moment
- Building Grind Visionary daily override logic

Always read these files first before this one:
- AGENTS.md
- docs/architecture.md
- docs/phase-5b-quest-system-redesign.md
- docs/game-design/README.md
- docs/game-design/BUILD_ORDER.md

---

## Path Overview

Path name: Grind Visionary
Player identity: Thinks big and works hard on
the right things
Target audience: Students building skills and
knowledge toward a singular vision. People who
are starting from scratch or developing their
craft and want a system that grows with them.

Goal of this path: Turn daily effort into visible
progress. Make showing up feel like leveling up.
The longer the player stays consistent the more
every action compounds in value.

Vibe: Smart grind — work hard on the right things.
Not hustle culture for its own sake. Deliberate
focused compounding effort toward a defined vision.

---

## Six Pillars With Progressive Unlock

Pillar names must appear everywhere in the UI —
quest cards dashboard headers progress breakdowns
onboarding screens.

The Mastery Lab
- Covers: Skill Building and Learning
- Unlocks: Level 1

The Workshop
- Covers: Creative Output and Projects
- Unlocks: Level 1

The Ascension Track
- Covers: Career and Professional Growth
- Unlocks: Level 5

The Empire
- Covers: Side Hustle and Entrepreneurship
- Unlocks: Level 10

The Alliance
- Covers: Networking and Relationships
- Unlocks: Level 20

The Signal
- Covers: Online Presence and Personal Brand
- Unlocks: Level 20

New pillar unlock triggers notification:
"A new dimension of your vision has opened
Visionary."

---

## Onboarding Questions

Opening line shown to player:
"Every empire started with one decision — to begin.
What are you building Visionary?"

Q1 — What is your grind focus?
Options:
- Coding and Tech
- Design and Creative
- Writing and Content
- Business and Entrepreneurship
- Marketing and Growth
- Finance and Investing
- Other — Define Your Own

If Other is selected show free text field:
"Name your field"
Save the custom field name.

Q2 — Where are you right now?
Options:
- Complete Beginner — Just Starting
- Have Some Skills — Want To Go Deeper
- Intermediate — Ready To Build And Ship
- Advanced — Scaling What I Have Built

Q3 — What is your singular goal?
Free text field.
Prompt shown above field:
"In 12 months I want to..."
Saved to SingularGoal model.
Displayed on Vision Board dashboard daily
as permanent reminder.

Q4 — By when do you want to achieve this goal?
Options:
- 3 Months
- 6 Months
- 1 Year
- 2 Years
Saved as goal deadline.
Dashboard shows countdown:
"247 days remaining toward your vision."

Q5 — How many hours per day can you dedicate
to your grind?
Options:
- 30 Minutes
- 1 Hour
- 2 Hours
- 3+ Hours

Q6 — What does your current output look like?
Options:
- I Consume More Than I Create
- I Create Occasionally But Inconsistently
- I Ship Work Regularly
- I Have An Audience Or Income Already

Save all answers to player profile.
User can update anytime in settings.

---

## Experience-Based Quest Visibility

Complete Beginner or I Consume More Than I Create:
D rank and C rank visible at start

Intermediate or I Create Occasionally:
D rank C rank B rank visible at start

Advanced or I Ship Work Regularly or
I Have Audience Or Income:
All ranks visible

---

## Universal Daily Quests

These appear every day for ALL Grind Visionary
users regardless of focus or level.
These fill the locked Universal Slot.
Cannot be swapped by player.

- Spend 30 minutes on your grind focus today
  EXP: 40
  Rank: D
  Cooldown: None

- Review your singular goal and write one
  action toward it today
  EXP: 30
  Rank: D
  Cooldown: None

- Log one thing you learned or created today
  EXP: 25
  Rank: D
  Cooldown: None

---

## Rank D Quests — Level 1 and above

The Mastery Lab:
- Spend 30 minutes learning your chosen skill
  EXP: 40
  Cooldown: None

- Watch or read one educational resource
  in your field
  EXP: 35
  Cooldown: None

- Write down 3 things you learned today
  EXP: 30
  Cooldown: None

The Workshop:
- Work on any creative project for 20 minutes
  EXP: 40
  Cooldown: None

- Write down your project idea in full detail
  EXP: 35
  Cooldown: None

- Complete one small task in your current project
  EXP: 35
  Cooldown: None

---

## Rank C Quests — Level 5 and above

The Mastery Lab:
- Study your skill for 1 hour uninterrupted
  EXP: 85
  Cooldown: None

- Apply something you learned this week
  in a real project
  EXP: 90
  Cooldown: None

- Identify your biggest skill gap and make
  a plan to close it
  EXP: 80
  Cooldown: None

- Teach someone else something you know
  EXP: 85
  Cooldown: None

The Workshop:
- Complete one milestone in your current project
  EXP: 90
  Cooldown: None

- Work on your project for 1 hour uninterrupted
  EXP: 85
  Cooldown: None

- Write a draft of something — even if unfinished
  EXP: 75
  Cooldown: None

The Ascension Track (Level 5 unlock):
- Write down your 1 year goal in specific detail
  EXP: 35
  Cooldown: None

- Research 3 opportunities in your field
  right now
  EXP: 80
  Cooldown: None

- Update your resume portfolio or LinkedIn today
  EXP: 80
  Cooldown: None

The Empire (Level 10 unlock):
- Work on your side project for 1 hour
  EXP: 85
  Cooldown: None

- Identify one potential customer or user
  for your idea
  EXP: 80
  Cooldown: None

The Alliance (Level 20 unlock):
- Comment thoughtfully on the work of someone
  you admire in your field
  EXP: 35
  Cooldown: None

- Join one online community or Discord related
  to your skill today
  EXP: 30
  Cooldown: None

- Send a cold DM or email to someone whose work
  you respect — introduce yourself genuinely
  EXP: 85
  Cooldown: None

- Share a resource or insight in a community
  you are part of
  EXP: 75
  Cooldown: None

The Signal (Level 20 unlock):
- Create a profile on one platform related
  to your field
  EXP: 30
  Cooldown: None

- Write one thing you learned today —
  even just for yourself
  EXP: 25
  Cooldown: None

- Write a post draft — even if you do not
  publish it yet
  EXP: 30
  Cooldown: None

- Share a skill tip or insight online
  EXP: 75
  Cooldown: None

- Publish your first public post about your
  learning journey
  EXP: 75
  Cooldown: None

---

## Rank B Quests — Level 10 and above

The Mastery Lab:
- Complete a 2 hour deep skill practice session
  EXP: 155
  Cooldown: 1 day

- Complete one structured tutorial or course
  module
  EXP: 145
  Cooldown: None

The Workshop:
- Finish and publish a piece of work —
  article project or design
  EXP: 170
  Cooldown: 3 days

- Dedicate 3 hours to your project in one day
  EXP: 165
  Cooldown: 2 days

- Ship something imperfect rather than wait
  for perfect
  EXP: 150
  Cooldown: None

The Ascension Track:
- Pitch an idea project or yourself to someone
  EXP: 160
  Cooldown: 3 days

- Apply for one opportunity — job internship
  or collaboration
  EXP: 155
  Cooldown: 3 days

The Empire:
- Generate your first dollar from your skill
  or side hustle
  EXP: 200
  Cooldown: One-time only
  Note: LEGENDARY QUEST — see First Dollar
  section below for special treatment

- Validate your idea with one real person
  outside your circle
  EXP: 155
  Cooldown: None

The Alliance:
- Have a meaningful conversation with a mentor
  or peer in your field
  EXP: 155
  Cooldown: 3 days

- Attend a virtual or in-person event in
  your field
  EXP: 155
  Cooldown: 3 days

- Share your weekly progress with your
  accountability partner
  EXP: 100
  Cooldown: 7 days
  Note: Only visible when Accountability Partner
  is active

The Signal:
- Build or update your personal portfolio
  with new work
  EXP: 150
  Cooldown: 7 days

- Engage authentically online for
  7 consecutive days
  EXP: 160
  Cooldown: 7 days

- Post consistently for 5 consecutive days
  EXP: 155
  Cooldown: 7 days

---

## Rank A Quests — Level 20 and above

The Mastery Lab:
- Study your skill every day for
  14 consecutive days
  EXP: 320
  Cooldown: 14 days

The Workshop:
- Complete a full project from start to finish
  this week
  EXP: 300
  Cooldown: 7 days

- Ship 4 pieces of work in one month
  EXP: 310
  Cooldown: 30 days

The Ascension Track:
- Land a new opportunity — job client
  collaboration or interview
  EXP: 350
  Cooldown: One-time per opportunity

The Empire:
- Generate consistent income from your skill
  for 30 days
  EXP: 400
  Cooldown: 30 days

The Alliance:
- Build meaningful relationships with 3 people
  in your field this month
  EXP: 280
  Cooldown: 30 days

The Signal:
- Grow your online presence consistently
  for 30 days
  EXP: 290
  Cooldown: 30 days

---

## Rank S Quests — Level 30 and above

The Mastery Lab:
- Complete a full course or certification
  in your field
  EXP: 700
  Cooldown: One-time only

The Workshop:
- Ship a project you are genuinely proud of
  EXP: 750
  Cooldown: One-time only

The Empire:
- Build something used or appreciated
  by 100 people
  EXP: 800
  Cooldown: One-time only

- Generate a full month of income from
  your own work
  EXP: 900
  Cooldown: One-time only

The Alliance:
- Build a network of 10 meaningful professional
  relationships
  EXP: 600
  Cooldown: One-time only

The Signal:
- Speak present or teach publicly about
  your skill
  EXP: 650
  Cooldown: 7 days

---

## First Dollar Legendary Moment

When player completes the Generate your first
dollar from your skill or side hustle quest
trigger a legendary completion moment.

This must be the most dramatic completion
animation in the entire app.

TRIGGER SEQUENCE:
Full screen gold explosion animation.
Message displayed:
"The empire has its foundation Visionary.
This is where it begins."

REWARDS:
Special badge: First Blood — First Dollar Earned
Achievement card auto-generated — most shareable
moment in the app.
200 EXP awarded with current XP multiplier applied.
Quest permanently displayed on public profile
as a milestone.

POST-FIRST-DOLLAR QUEST CHAIN:
Automatically unlocks after First Dollar
quest is completed.
These three quests unlock sequentially —
each unlocks only after the previous is complete.

Quest 1: Generate your first 10 dollars
EXP: 250
Unlocks: immediately after First Dollar

Quest 2: Generate your first 100 dollars
EXP: 400
Unlocks: after Quest 1 complete

Quest 3: Generate your first consistent
monthly income
EXP: 600
Unlocks: after Quest 2 complete

These chain quests keep momentum alive after
the legendary First Dollar moment.

---

## XP Multiplier System

The XP Multiplier is the primary consistency
mechanic for the Grind Visionary path.
The longer the player stays consistent the
more every quest is worth.
Compound effort creates compound rewards.
This mirrors how skills and opportunities
actually work in real life.

MULTIPLIER TIERS:
Day 1 to 6: 1.0x — Title: The Dreamer
Day 7 to 13: 1.25x — Title: The Builder
Day 14 to 20: 1.5x — Title: The Grinder
Day 21 to 29: 1.75x — Title: The Visionary
Day 30 and above: 2.0x — Title: The Realized

HOW IT WORKS:
Every EXP reward is automatically multiplied
by the current tier before being added to
player total.
Multiplier applied to ALL quest completions
including universal daily quests boss quests
and cross-path bonuses.
All multiplier calculations must be server-side
only. Never client-side.

Example:
Player on Day 21 completes Study skill 1 hour.
Base EXP: 85
Multiplied: 85 times 1.75 = 149 EXP earned.

DASHBOARD DISPLAY:
Multiplier shown visibly on dashboard at all times:
"Current Grind Multiplier: 1.75x — Day 21 streak"

MULTIPLIER COUNTDOWN BAR:
Show a progress bar beneath multiplier display
filling toward next tier threshold.
One day before next tier upgrade show
notification:
"Tomorrow your grind multiplies Visionary.
Show up."

Example display when on Day 6:
"1 day away from 1.25x multiplier —
do not break the chain"

STREAK BREAK LOGIC:
If streak breaks:
Multiplier resets to 1.0x immediately.
Message:
"The grind was interrupted Visionary. But the
vision remains. Start again — the multiplier
awaits."
Previous highest multiplier streak saved to
profile as personal record.
Personal best multiplier and streak days
visible on public profile.

MULTIPLIER PROTECTION:
Earned automatically after 14 consecutive days
of quest completion.
If streak breaks after Day 14 — one missed day
does not reset multiplier. Activates automatically.
Must complete 7 more consecutive days after
use to earn protection again.
Message on activation:
"Your past grind protected your momentum.
The vision continues."
Protection icon visible on dashboard when active.

---

## Vision Board

A dedicated command center section on the
user dashboard.

Displays:
- Singular goal text from onboarding Q3
- Goal deadline countdown:
  "247 days remaining toward your vision."
- Current multiplier and streak
- Progress bar to next multiplier tier
- Last 3 Output Log entries
- Current skill tree node and next node
  to unlock
- Grind focus field label

Vision Board is always visible on dashboard.
It is not a separate page — it is a section
of the main dashboard for this path.

---

## Skill Tree

Based on grind focus selected in onboarding
a visual skill tree shows the player's
progression through their field.
Each node unlocks as player completes Mastery
Lab quests at corresponding levels.
Displayed on Vision Board and as dedicated tab.

NODE UNLOCK LOGIC:
Each node unlocks based on cumulative Mastery
Lab quest completions at each level tier.
Unlocking a node triggers a notification
and visual animation on the skill tree.
Message:
"A new level of mastery has been reached
Visionary."

SKILL TREE NODES PER FOCUS:

Coding and Tech:
Node 1: Fundamentals
Node 2: First Project
Node 3: Frontend or Backend Basics
Node 4: First Deployed App
Node 5: Freelance Ready
Node 6: Building Products
Node 7: Senior Developer

Design and Creative:
Node 1: Tool Basics
Node 2: First Design
Node 3: Style Development
Node 4: Portfolio Piece
Node 5: Client Ready
Node 6: Signature Style
Node 7: Recognized Creator

Writing and Content:
Node 1: Daily Writing Habit
Node 2: First Published Piece
Node 3: Finding Your Voice
Node 4: Consistent Output
Node 5: Building Audience
Node 6: Monetizing Words
Node 7: Established Writer

Business and Entrepreneurship:
Node 1: Idea Validation
Node 2: First Customer Conversation
Node 3: MVP Built
Node 4: First Dollar
Node 5: Repeatable Revenue
Node 6: Scaling
Node 7: Empire

Marketing and Growth:
Node 1: Platform Basics
Node 2: First Campaign
Node 3: Analytics Understanding
Node 4: First Viral Post
Node 5: Audience Building
Node 6: Brand Strategy
Node 7: Growth Leader

Finance and Investing:
Node 1: Financial Literacy
Node 2: Budget Built
Node 3: First Investment
Node 4: Emergency Fund
Node 5: Portfolio Building
Node 6: Passive Income
Node 7: Financial Freedom

Custom — Other field:
Node 1: Beginner
Node 2: Developing
Node 3: Competent
Node 4: Proficient
Node 5: Advanced
Node 6: Expert
Node 7: Master
Node names display as:
"[User's field name] — [Node name]"
Example: "Graphic Design — Competent"

---

## Output Log

Every time a player completes a Workshop or
Empire quest they are optionally prompted:
"What did you ship today? Log it for your record."

INPUT FIELDS:
- Description: free text — what did you create
  or ship?
- Link: optional URL to the work
- Date: auto-filled from completion timestamp
- Quest linked: auto-filled from completed quest

Entries saved to player profile in chronological
order.
Accessible as dedicated Output Log tab.
Entries private by default.
User can make individual entries public.

MILESTONE NOTIFICATIONS AND BADGES:
10 outputs logged:
"The Builder — 10 pieces shipped"
Badge plus achievement card generated.

25 outputs logged:
"The Creator — 25 pieces shipped"
Badge plus achievement card generated.

50 outputs logged:
"The Prolific Visionary — 50 pieces shipped"
Badge plus achievement card generated.

100 outputs logged:
"The Legendary Output — 100 pieces shipped"
Badge plus achievement card generated.

---

## Accountability Partner System

The Grind Visionary path is the most solitary
of all paths. The Accountability Partner system
adds social pressure and support.

HOW IT WORKS:
Player can invite one other Discipline System
user to be their accountability partner
from their profile settings.
Both users must accept the partnership.
Maximum one active partner at a time.

WHAT PARTNERS SEE:
Partners can view each other's:
- Current multiplier and streak
- Output Log entries (public ones only)
- Weekly quest completion rate
- Vision Board goal if user sets to visible

PARTNER NOTIFICATIONS:
Partner receives notification when other person:
- Completes a quest
- Ships work and logs it in Output Log
- Levels up
- Earns a multiplier tier upgrade
- Breaks or protects their streak

ACCOUNTABILITY QUEST:
Weekly quest unlocks only when Accountability
Partner is active:
"Share your weekly progress with your
accountability partner — what did you build
this week?"
EXP: 100
Rank: B
Cooldown: 7 days

PARTNERSHIP MILESTONE:
Both partners maintain active streaks for
30 consecutive days simultaneously:
Both receive badge: The Alliance —
30 days grinding together.
Achievement card generated for both users.

---

## Weekly Boss Quest

Appears every Monday. Resets Monday at 00:00.
Boss quest EXP is multiplied by current
XP multiplier when awarded.
Completion awards EXP plus exclusive weekly badge.

Rotating examples:

Week option 1:
"Study your skill every day and ship one piece
of work this week"
EXP: 420
Badge: The Builder Week

Week option 2:
"Reach out to 3 people in your field this week"
EXP: 400
Badge: The Connector

Week option 3:
"Post online every day this week"
EXP: 390
Badge: The Signal

Week option 4:
"Complete 10 hours of deep skill work this week"
EXP: 450
Badge: Deep Grind

Week option 5:
"Ship something and share it with your
accountability partner this week"
EXP: 410
Badge: The Alliance Move

---

## Adaptive Difficulty Nudge

If player completes all daily quests for
7 consecutive days trigger nudge on Day 8:

"Your multiplier is building Visionary. Ready
to push harder?"

Options:
- Yes increase the challenge
- Not yet keep current quests

If yes:
Surface more B rank quests in assigned slots.
Upgrade D rank daily quests to C rank equivalents.

---

## Cross-Path Bonuses

Deep work quest completed in Grind Visionary
same day as Siege quest in Discipline Knight:
Award +20 EXP cross-path bonus with multiplier
applied.
Message: "Discipline fuels the vision.
The grind compounds."

Mastery Lab quest completed same day as
Knowledge Forging quest in Mindset Sage:
Award +25 EXP cross-path bonus with multiplier
applied.
Message: "The Scholar applies wisdom.
Knowledge becomes power."

---

## Social Features

Achievement cards auto-generated for:
- Level up
- Rank unlock
- Each multiplier tier reached
- First Dollar legendary moment
- Output Log milestones 10 25 50 100
- Skill tree node unlocks
- Boss quest completion
- Accountability Partner 30 day milestone
- The Renaissance Human title unlocked
- Each one-time only S rank quest completed

Badges for this path:
- The Dreamer: path selected and goal defined
- The Builder: Day 7 streak 1.25x reached
- The Grinder: Day 14 streak 1.5x reached
- The Visionary: Day 21 streak 1.75x reached
- The Realized: Day 30 streak 2.0x reached
- First Blood: first dollar earned
- The Builder: 10 outputs logged
- The Prolific Visionary: 50 outputs logged
- The Alliance: accountability partner
  30 day milestone

LEADERBOARDS FOR THIS PATH:
Weekly EXP leaderboard with multiplier applied —
higher multiplier players naturally rise faster.
Resets every Monday at 00:00.

Multiplier streak leaderboard:
Shows highest current active multiplier streaks.
Personal best multiplier record visible on profile.

Output Log leaderboard:
Most Output Log entries this month.

Renaissance Human dedicated leaderboard tier:
Players with The Renaissance Human title shown
in dedicated top tier globally.

Profile visibility:
Public by default.
Private option available in settings.
Public profile shows: singular goal skill tree
progress current multiplier output log public
entries level rank streak badges personal best
multiplier record recent achievements.

---

## Day 1 Starter Lineup

On the player's very first day the algorithm
does not run. Use this hardcoded lineup instead:

Quest 1: Spend 30 minutes on your grind focus
today (40 EXP D rank)
Quest 2: Review your singular goal and write one
action toward it today (30 EXP D rank)
Quest 3: Log one thing you learned or created
today (25 EXP D rank)

Algorithm takes over from Day 2 onwards.

---

## Daily Override Logic

If player is one day from multiplier tier upgrade:
Surface highest available EXP quests in all
assigned slots regardless of weekly rhythm.
Show motivation message on quest board:
"Tomorrow your multiplier upgrades Visionary.
Make today count."

Every Sunday:
Vision Board review quest fills one assigned slot.

If Accountability Partner is active:
Surface accountability quest in one slot
on Sundays.

---

## Important Implementation Notes

1. XP Multiplier calculations must be server-side
   only. Never calculate or apply multiplier
   on the frontend. All EXP awards pass through
   multiplier calculation before being saved.
   Build as a reusable server-side utility
   function.

2. Multiplier protection auto-activates on missed
   day only after Day 14 streak is reached.
   Requires 7 more consecutive days after use
   to re-earn. Do not activate before Day 14.

3. Pillar unlock by level is strict:
   Alliance and Signal hidden until Level 20.
   Empire hidden until Level 10.
   Ascension Track hidden until Level 5.
   Mastery Lab and Workshop available from Level 1.
   Quests from locked pillars must not appear
   in assigned slots bonus slots or swap drawer
   until the player reaches the required level.

4. First Dollar quest is one-time only and must
   trigger the legendary animation sequence.
   This is the highest priority frontend moment
   in this path. Build the animation before
   any other Visionary frontend work.

5. Post-First-Dollar quest chain must unlock
   automatically on First Dollar completion.
   No manual activation required.
   Quest 2 unlocks after Quest 1 complete.
   Quest 3 unlocks after Quest 2 complete.

6. Accountability Partner system requires
   two-way acceptance before partnership
   activates. Notifications sent to partner
   on quest completion events.

7. Output Log prompt after Workshop or Empire
   quest is always optional. Never block
   quest completion waiting for an Output Log
   entry.

8. Vision Board is a dashboard section not
   a separate page. It should be visible on
   the main dashboard without navigation.

9. Skill tree node unlock thresholds need to
   be defined per focus per node based on
   cumulative Mastery Lab quest completions.
   Build unlock threshold logic per focus
   per node.

10. Weekly boss quest EXP is multiplied by
    current XP multiplier same as regular quests.
    Boss quest EXP calculation uses the same
    server-side multiplier utility function.

11. All quest completions are self-reported.
    No verification required for V1.