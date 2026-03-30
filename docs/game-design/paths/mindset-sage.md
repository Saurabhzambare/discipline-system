# Mindset Sage Path
# docs/game-design/paths/mindset-sage.md

---

## How To Use This File

Read this file when:
- Building Mindset Sage onboarding flow
- Seeding Mindset Sage quest data
- Building Freedom Day Token system
- Building Wisdom Log feature
- Building Dark Night Quest
- Building Mindset Sage daily override logic

Always read these files first before this one:
- AGENTS.md
- docs/architecture.md
- docs/phase-5b-quest-system-redesign.md
- docs/game-design/README.md
- docs/game-design/BUILD_ORDER.md

---

## Path Overview

Path name: Mindset Sage
Player identity: Mental warrior
Target audience: Anyone on a self-improvement journey.
Not niche — broad appeal. These users want to think
differently act deliberately and move through life
with uncommon clarity and emotional control.

Goal of this path: Transform the user's identity
through daily mental practice. The app should not
feel like a wellness tool. It should feel like
mental warrior training. Every quest every pillar
name every UI element should reinforce that identity.

Vibe: Ancient wisdom meets modern mental training.
The mind is the greatest weapon. Sharpen it daily.

---

## Four Pillars

Pillar names must appear everywhere in the UI —
quest cards dashboard headers progress breakdowns
onboarding screens.

Inner Stillness
- Covers: Meditation and Breathwork

Knowledge Forging
- Covers: Reading and Learning

Mirror Work
- Covers: Journaling and Self-Reflection

Shadow Training
- Covers: Mental Toughness and Discomfort

---

## Onboarding Questions

Opening line shown to player:
"The mind is your greatest weapon Sage.
Tell us how you wield it."

Q1 — What draws you to this path?
Options:
- Mental Clarity
- Stress Relief
- Personal Growth
- Discipline Building

Q2 — How much time can you dedicate daily?
Options:
- 15 minutes
- 30 minutes
- 1 hour
- As much as needed

Q3 — Experience with mindset practices?
Options:
- Complete Beginner
- Some Experience
- Daily Practitioner

Q4 — Which Sage archetype calls to you?
Options:
- The Stoic — masters emotional control and resilience
- The Scholar — pursues knowledge and wisdom
  relentlessly
- The Monk — seeks inner peace through stillness
  and presence
- The Warrior-Sage — combines mental and physical
  discipline

Save all four answers to player profile.
User can update anytime in settings.

---

## Sage Archetype Quest Pool Filtering

Based on archetype selected during onboarding
the app surfaces relevant quests first in
the user's daily pool.

The Stoic:
Prioritize Shadow Training quests and Stoic
Challenge quests at top of pool.

The Scholar:
Prioritize Knowledge Forging quests and Wisdom
Log related quests at top of pool.

The Monk:
Prioritize Inner Stillness quests and breathwork
quests at top of pool.

The Warrior-Sage:
Balanced mix of all four pillars.
Cross-path quests surfaced if user also has
Fitness Warrior path active.

All quests remain accessible regardless of archetype.
Archetype only affects default sort order
in the quest pool.

---

## Experience-Based Quest Visibility

Complete Beginner: D rank and C rank visible at start
Some Experience: D rank C rank B rank visible at start
Daily Practitioner: All ranks visible D rank optional

---

## Universal Daily Quests

These appear every day for ALL Mindset Sage users
regardless of archetype or experience level.
These fill the locked Universal Slot.
Cannot be swapped by player.

- Meditate for 5 minutes
  EXP: 35
  Rank: D
  Cooldown: None

- Write 3 things you are grateful for
  EXP: 30
  Rank: D
  Cooldown: None

- Read 10 pages of any book
  EXP: 35
  Rank: D
  Cooldown: None

- Sit in silence for 5 minutes with no phone
  EXP: 30
  Rank: D
  Cooldown: None

---

## Rank D Quests — Level 1 and above

Inner Stillness:
- Meditate for 5 minutes
  EXP: 35
  Cooldown: None

- Do 5 minutes of deep breathing
  EXP: 30
  Cooldown: None

Knowledge Forging:
- Read 10 pages of any book
  EXP: 35
  Cooldown: None

- Listen to a 15 minute educational podcast
  EXP: 30
  Cooldown: None

Mirror Work:
- Write down your goal for tomorrow
  EXP: 25
  Cooldown: None

- Write 3 things you are grateful for
  EXP: 30
  Cooldown: None

Shadow Training:
- Take a cold shower
  EXP: 40
  Cooldown: None

- Do one thing outside your comfort zone today
  EXP: 40
  Cooldown: None

---

## Rank C Quests — Level 5 and above

Inner Stillness:
- Meditate for 15 minutes
  EXP: 75
  Cooldown: None

- Do box breathing for 10 minutes
  EXP: 70
  Cooldown: None

Knowledge Forging:
- Read for 30 minutes uninterrupted
  EXP: 80
  Cooldown: None

- Write down 3 lessons learned today
  EXP: 75
  Cooldown: None

Mirror Work:
- Write a full journal entry (minimum 150 words)
  EXP: 85
  Cooldown: None

- Do one thing today purely for someone else
  with zero expectation of return
  EXP: 110
  Cooldown: None

Shadow Training:
- Spend the entire day without social media
  EXP: 100
  Cooldown: 3 days

- Do not justify or explain your decisions
  to anyone today
  EXP: 100
  Cooldown: None

Stoic Challenge (Shadow Training sub-pillar):
- Respond to one frustrating situation with
  complete calm today
  EXP: 120
  Cooldown: None

- Go the entire day without complaining
  or gossiping
  EXP: 140
  Cooldown: None

---

## Rank B Quests — Level 10 and above

Inner Stillness:
- Meditate for 30 minutes
  EXP: 140
  Cooldown: None

- Complete a full Wim Hof or box breathing session
  EXP: 130
  Cooldown: 1 day

Knowledge Forging:
- Read for 1 hour uninterrupted
  EXP: 150
  Cooldown: None

- Read a full book chapter and summarize it
  in your Wisdom Log
  EXP: 145
  Cooldown: None

Mirror Work:
- Write a weekly review covering wins losses
  and lessons
  EXP: 160
  Cooldown: 7 days

- Identify your biggest fear write it down
  and sit with it
  EXP: 150
  Cooldown: 3 days

Shadow Training:
- Do something that genuinely scares you today
  EXP: 170
  Cooldown: 3 days

- Wake up at 5AM
  EXP: 140
  Cooldown: None

- No complaints for an entire day
  EXP: 150
  Cooldown: None

Stoic Challenge:
- Spend 10 minutes contemplating your own mortality
  EXP: 130
  Cooldown: 3 days

- Respond to one frustrating situation with
  complete calm today
  EXP: 120
  Cooldown: None

Dark Night Quest (special — see Section below):
- Today was hard. Write honestly about what
  broke you and what it revealed.
  EXP: 200
  Cooldown: None
  Activation: Manual only — never auto-assigned

---

## Rank A Quests — Level 20 and above

- Meditate every day for 7 days straight
  EXP: 280
  Cooldown: 7 days

- Read a full non-fiction book this week
  EXP: 300
  Cooldown: 7 days

- Write a monthly reflection — full honest review
  EXP: 270
  Cooldown: 30 days

- Complete a digital detox day — no phone until 6PM
  EXP: 260
  Cooldown: 3 days

- Do a 10 minute visualization session daily
  for 5 days
  EXP: 290
  Cooldown: 7 days

- Wake up at 5AM for 5 consecutive days
  EXP: 310
  Cooldown: 7 days

---

## Rank S Quests — Level 30 and above

- Meditate every day for 30 days
  EXP: 600
  Cooldown: 30 days

- Read 12 books in a year
  EXP: 800
  Cooldown: One-time only

- Write in your journal every day for 30 days
  EXP: 650
  Cooldown: 30 days

- Complete a 24 hour digital detox —
  no phone no screen
  EXP: 500
  Cooldown: 14 days

- Do something that redefines your comfort zone
  EXP: 550
  Cooldown: 7 days

- Write a personal manifesto — your values
  vision and rules for life
  EXP: 700
  Cooldown: One-time only

---

## Freedom Day Token System

This mechanic is unique to the Mindset Sage path.
It is the primary consistency reward mechanic.

EARNING TOKENS:
Complete all assigned daily quests for
7 consecutive days — earn 1 Freedom Day token.
Tokens stack up to a maximum of 3.
Token counter is visible on the dashboard
as a glowing orb icon.
Earning a token triggers a short animation
and message:
"Your discipline has been recognized Sage.
A Freedom Day awaits."

TOKEN OVERFLOW:
If player earns a 4th token while already at
maximum of 3 — award 200 bonus EXP instead.
Message:
"Your Freedom Day tokens are full Sage.
Your consistency has been converted to
200 bonus EXP."
This rule is final. Do not ask developer again.

REDEEMING TOKENS:
User taps Redeem Freedom Day button anytime
from dashboard.
Token is consumed immediately on redemption.
User chooses when to redeem — fully their decision.

WHAT HAPPENS ON A FREEDOM DAY:
Quest board is completely empty for this path.
Zero quests assigned.
Full screen special UI loads with message:
"You have earned this Sage. Your discipline
speaks for itself. Go explore. Go live.
Come back stronger."
Display on screen: current level current streak
total Freedom Days taken.
Background: zen-styled minimal design —
dark calm intentional.
Streak does NOT break — Freedom Day counts
as a completed day.
A Freedom Day badge is logged to profile
history with the date.
User can still optionally open their Wisdom Log
to write if they want — but nothing is required.
Other active paths show their quests normally.
Only Mindset Sage quest board clears.

---

## Wisdom Log Feature

The Wisdom Log is a personal knowledge library
unique to the Mindset Sage path.
It lives inside the user's profile and dashboard.

HOW IT WORKS:
After completing any Knowledge Forging or Mirror
Work quest the user is optionally prompted:
"What is one insight you are taking from today?"
User writes one sentence or short paragraph —
free text input.
Entry saved with date quest name and player level.
Entries are private by default.
User can make individual entries public.

WISDOM LOG UI:
Accessible from dashboard as a dedicated tab
or section.
Shows all entries in reverse chronological order.
Entry count displayed prominently:
"Your Wisdom Log — 47 insights collected"

MILESTONE NOTIFICATIONS:
10 entries: "The ink of wisdom grows Sage."
25 entries: "A quarter century of insight."
50 entries: "The Wisdom Log deepens."
100 entries: "Wisdom Keeper achieved."

SHAREABILITY:
At milestone counts generate a shareable
achievement card:
"Sage Level [X] — [X] Wisdom Entries Logged"
Card includes username level entry count
app branding.
User can download as image to share on Instagram
or post to their in-app public profile.

---

## Dark Night Quest

The Dark Night Quest is a special quest unique
to Mindset Sage. It is NOT assigned automatically.
It is manually activated by the user on
difficult days.

PURPOSE:
On days when life is hard instead of abandoning
the app and breaking their streak the user
activates this quest and turns their pain
into progress.

HOW IT WORKS:
A subtle Dark Night button is always visible
on the Mindset Sage dashboard.
Small not prominent but always there.
User taps it on a hard day.
Quest activates with prompt:
"Today was hard. Write honestly about what
broke you and what it revealed."
User writes in a private journal entry —
minimum 100 words.

ON COMPLETION:
200 EXP awarded.
Streak protected.
Special dark-themed completion screen shown.
Message:
"The Sage who faces darkness becomes the light.
Well done."
Entry saved to Wisdom Log marked as
Dark Night Entry.
Unique dark badge logged to profile.

CONSTRAINTS:
Maximum 1 Dark Night Quest per day.
No cooldown — available whenever user needs it.
Always self-reported and private.
Does not replace regular daily quests —
it supplements them.
Counts as completing one assigned slot
for the day.

---

## Weekly Boss Quest

Appears every Monday. Resets Monday at 00:00.
Completion awards EXP plus exclusive weekly badge.

Rotating examples:

Week option 1:
"Meditate journal and read every day this week"
EXP: 450
Badge: Sage Week

Week option 2:
"Complete a digital detox and write a weekly review"
EXP: 400
Badge: The Detox Sage

Week option 3:
"Wake up at 5AM for 5 days straight"
EXP: 430
Badge: The Early Sage

Week option 4:
"Complete 3 Stoic Challenge quests this week"
EXP: 420
Badge: The Stoic

Week option 5:
"Fill 7 Wisdom Log entries this week"
EXP: 410
Badge: Wisdom Seeker

---

## Cross-Path Bonuses

Breathwork completed in both Mindset Sage AND
Health Alchemist on same day:
Award +20 EXP bonus to both quests.
Message: "Breath connects body and soul."

5AM wake up completed in both Mindset Sage AND
Discipline Knight on same day:
Award +25 EXP bonus to both quests.
Message: "The early hours belong to the
disciplined mind."

Reading quest completed in both Mindset Sage AND
Grind Visionary on same day:
Award +25 EXP bonus to both quests.
Message: "Knowledge into action."

---

## Social Features

Achievement cards auto-generated for:
- Level up
- Rank unlock
- Freedom Day redeemed
- Wisdom Log milestones (10 25 50 100 entries)
- Boss quest completion
- Dark Night Quest completion
- Warrior-Sage cross-path title unlocked

Badges for this path:
- Inner Stillness: 30 day meditation streak
- The Scholar: 12 books read
- Mirror Sage: 30 day journal streak
- Shadow Walker: 10 Shadow Training quests completed
- Freedom Earned: first Freedom Day redeemed
- Dark Night Survivor: first Dark Night Quest
  completed
- Wisdom Keeper: 100 Wisdom Log entries logged

Leaderboard:
Weekly EXP leaderboard among all Mindset Sage users.
Resets every Monday at 00:00.
Shows top 10 globally plus user own rank.

Profile visibility:
Public by default.
Private option available in settings.
Public profile shows: level rank streak badges
recent achievements Wisdom Log entry count.

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

Quest 1: Meditate for 5 minutes (35 EXP D rank)
Quest 2: Write 3 things you are grateful for
(30 EXP D rank)
Quest 3: Sit in silence for 5 minutes with
no phone (30 EXP D rank)

Algorithm takes over from Day 2 onwards.

---

## Daily Override Logic

Every Sunday:
Automatically include weekly review quest in
one assigned slot.
This quest cannot be swapped out on Sundays.

If Freedom Day is redeemed:
Clear ALL assigned slots for Mindset Sage.
Show Freedom Day screen instead of quest board
for this path only.
Other active paths show their quests normally.

If Dark Night Quest was activated:
Count as completing one assigned slot for the day.
Do not surface Dark Night Quest in the algorithm —
it is always manually activated by player only.

---

## Important Implementation Notes

1. Freedom Day token overflow (4th token earned
   while at max 3) must award 200 bonus EXP.
   This rule is confirmed and final.

2. Dark Night Quest must never appear in the
   daily assignment algorithm or suggested lineup.
   It is exclusively manually activated.

3. The Wisdom Log prompt after quests is always
   optional. Never block quest completion waiting
   for a Wisdom Log entry.

4. Stoic Challenge quests are a sub-type of
   Shadow Training. They should be tagged as
   pillar: Shadow Training in the quest model
   with a stoic_challenge boolean flag or similar.

5. The cold shower quest appears in both this path
   and Fitness Warrior. Cross-path bonus applies
   when both are completed same day.

6. Weekly review quest on Sunday fills one assigned
   slot and cannot be swapped. Show a lock icon
   on that quest card on Sundays.

7. All quest completions are self-reported.
   No verification required for V1.