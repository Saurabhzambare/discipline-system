# Health Alchemist Path
# docs/game-design/paths/health-alchemist.md

---

## How To Use This File

Read this file when:
- Building Health Alchemist onboarding flow
- Building Alchemist Setup Guide
- Seeding Health Alchemist quest data
- Building Elixir System
- Building Body Journal feature
- Building Health Alchemist daily override logic

Always read these files first before this one:
- AGENTS.md
- docs/architecture.md
- docs/phase-5b-quest-system-redesign.md
- docs/game-design/README.md
- docs/game-design/BUILD_ORDER.md

---

## Path Overview

Path name: Health Alchemist
Player identity: Body as laboratory
Target audience: Anyone wanting to optimize their
body from within and people dealing with stress
and burnout.

Goal of this path: Transform the user's body
through deliberate daily practice. Ancient wisdom
meets modern biohacking. Spiritual and holistic
on the surface science-backed underneath.

Vibe: The user is an Alchemist transforming their
body through deliberate daily practice.
Every habit is an ingredient in the formula.
Every consistent day brews the elixir.

---

## Six Pillars

Pillar names must appear everywhere in the UI —
quest cards dashboard headers progress breakdowns
onboarding screens.

The Fuel Formula
- Covers: Nutrition and Diet

The Restoration Chamber
- Covers: Sleep and Recovery

The Inner Ecosystem
- Covers: Gut Health and Digestion

The Emotional Crucible
- Covers: Mental and Emotional Health

The Purification Ritual
- Covers: Hydration and Detox

The Transmission Protocol
- Covers: Preventive Care and Checkups

---

## Pillar Unlock By Level

To avoid overwhelming new users introduce pillars
gradually as player levels up.

Level 1: Fuel Formula and Purification Ritual
Level 5: Restoration Chamber unlocked
Level 10: Inner Ecosystem unlocked
Level 20: Emotional Crucible and Transmission
Protocol unlocked

New pillar unlock triggers notification:
"A new pillar of your formula has been revealed
Alchemist."

---

## Onboarding Questions

Opening line shown to player:
"Your body is the laboratory Alchemist.
Let us build your formula."

Q1 — What is your primary health goal?
Options:
- Optimize Energy
- Reduce Stress and Burnout
- Improve Gut Health
- Build Better Sleep
- Full Body Transformation

Q2 — What is your current relationship with health?
Options:
- Starting From Scratch
- Have Some Good Habits
- Already Health Conscious
- Looking To Biohack and Optimize

Q3 — Which area needs the most work?
Options:
- Nutrition
- Sleep
- Mental Health
- Hydration
- All Of Them

Q4 — What do you currently have access to?
This is a multi-select question.
Options:
- Cold Shower
- Ice Bath or Cold Plunge
- Sauna
- Fitness Tracker or Wearable
- Supplements
- None Yet

Save all answers to player profile including
equipment profile saved to EquipmentProfile model.
User can update anytime in settings.

---

## Experience-Based Quest Visibility

Starting From Scratch:
D rank and C rank visible at start

Have Some Good Habits:
D rank C rank B rank visible at start

Already Health Conscious or Looking To Biohack:
All ranks visible

---

## Alchemist Setup Guide

Shown AFTER onboarding questions and BEFORE
dashboard loads.
Styled as an in-game equipment room or item shop.

Opening line:
"Every Alchemist needs their tools. Here is what
will accelerate your transformation — and how to
get it without breaking the bank."

LEGAL DISCLAIMER — must appear in THREE places:
1. Top of Setup Guide before any recommendations
2. Bottom of Setup Guide
3. One line note on every individual supplement card

Disclaimer text (use exactly):
"These are general wellness suggestions not medical
advice. Consult a healthcare professional before
starting any new supplement protocol."

This is non-negotiable. All three placements
must be present. Do not remove or shorten.

---

## Setup Guide — Section A: Supplement Cards

Each supplement card has two tabs:
Tab 1 — Take It (supplement info and why it helps)
Tab 2 — Eat It Instead (whole food alternatives)

No purchase links. No affiliate pressure.
Pure information. User decides what to do with it.

Supplement 1: Creatine Monohydrate
Why it helps: Energy strength and cognitive function
Food alternative: Red meat and fish

Supplement 2: Vitamin D3
Why it helps: Immune system mood and bone health
Food alternative: Sunlight 20 minutes daily
fatty fish and egg yolks

Supplement 3: Omega-3 Fish Oil
Why it helps: Inflammation reduction and brain health
Food alternative: Salmon sardines walnuts
and flaxseeds

Supplement 4: Magnesium Glycinate
Why it helps: Sleep quality stress reduction
and muscle recovery
Food alternative: Dark chocolate spinach almonds
and pumpkin seeds

Supplement 5: Probiotics
Why it helps: Gut microbiome digestion and immunity
Food alternative: Yogurt kefir kimchi
sauerkraut and kombucha

Supplement 6: Zinc
Why it helps: Immune function recovery
and hormonal health
Food alternative: Pumpkin seeds chickpeas
cashews and beef

---

## Setup Guide — Section B: Equipment Cards

Each equipment card shows:
- What it is for
- Cheapest way to get it
- Free or food-based alternative

Frame every card as a recommendation not a
requirement. Language must be encouraging not pushy.

Equipment 1: Cold Plunge Setup
Why it helps: Cold therapy recovery and
mental toughness
Budget alternative: Large storage bin or bucket
your body fits in plus 2 bags of ice
approximately 5 dollars total. Effective
and accessible.

Equipment 2: Sauna Access
Why it helps: Detox recovery and
cardiovascular health
Budget alternative: Local gym sauna YMCA
or community center membership

Equipment 3: Fitness Tracker or Wearable
Why it helps: HRV tracking sleep quality
monitoring and step counting
Budget alternative: Mi Band or Fitbit Inspire
approximately 30 to 50 dollars.
More than enough to start.
Free sleep tracker apps also work.

Equipment 4: Foam Roller
Why it helps: Muscle recovery mobility
and circulation
Budget alternative: Tennis ball for targeted
muscle spots. Free and highly effective.

Equipment 5: Journal or Notebook
Why it helps: Body journaling reflection
and pattern tracking
Budget alternative: Built-in digital Body Journal
in this app. No purchase needed.

Equipment 6: Blender
Why it helps: Protein shakes smoothies
and gut health drinks
Budget alternative: Overnight oats with fork
and bowl. Same nutrition zero equipment.

---

## Setup Guide — Section C: Personalized Starter Pack

Generated from Q1 and Q2 onboarding answers.
Appears at bottom of Setup Guide.
Build conditional logic for all goal and
experience combinations.

Example — Goal is Stress and Burnout
AND experience is Starting From Scratch:
"Your Starter Formula Alchemist:
Start with Magnesium Glycinate before bed
or chamomile tea.
Cold therapy: Fill bathtub with cold water
and one bag of ice.
Tracking: Use a free sleep tracker app to start.
Food priority: Add spinach salmon and yogurt
to your weekly shop.
You do not need everything at once. Start with
one change. Master it. Then add the next."

Example — Goal is Gut Health
AND experience is Already Health Conscious:
"Your Starter Formula Alchemist:
Priority supplement: Probiotics — or eat kimchi
and kefir daily.
Add one fermented food to every meal this week.
Eliminate processed food for 3 days and track
how you feel.
Begin logging your Inner Ecosystem in your
Body Journal."

Build similar conditional logic for all
goal and experience combinations.
Starter pack must always end with:
"You do not need everything at once. Start with
one change. Master it. Then add the next."

---

## Universal Daily Quests

These appear every day for ALL Health Alchemist
users regardless of experience level.
These fill the locked Universal Slot.
Cannot be swapped by player.

- Drink 2L of water today
  EXP: 30
  Rank: D
  Cooldown: None

- Eat one whole food meal today
  EXP: 35
  Rank: D
  Cooldown: None

- Take your supplements today
  EXP: 25
  Rank: D
  Cooldown: None
  Note: If player selected None Yet in Q4
  show alternative quest:
  "Research one supplement that could benefit
  your goals" EXP: 25

- Complete the Alchemist Morning Protocol
  EXP: 150
  Rank: C
  Cooldown: None

---

## Morning Protocol Quest

This is the signature daily quest of the
Health Alchemist path.
Always fills the first assigned slot every morning.
Cannot be swapped by player.

Complete all four before 9AM:
1. Drink 500ml water immediately on waking
2. Get 10 minutes of natural sunlight
3. Take your supplements
4. No phone for first 30 minutes after waking

All four completed = 150 EXP awarded as
single quest completion.

If player completes 30 Morning Protocol quests
in a row generate achievement card:
"Alchemist Morning Protocol — 30 Days Complete"

---

## Rank D Quests — Level 1 and above

Fuel Formula:
- Eat one whole food meal today
  EXP: 35
  Cooldown: None

- Eat one serving of vegetables or fruit
  EXP: 30
  Cooldown: None

- Avoid processed food for one meal today
  EXP: 30
  Cooldown: None

Purification Ritual:
- Drink 2L of water today
  EXP: 30
  Cooldown: None

- Drink warm lemon water first thing in the morning
  EXP: 30
  Cooldown: None

- Spend 10 minutes outside in sunlight
  EXP: 30
  Cooldown: None

---

## Rank C Quests — Level 5 and above

Fuel Formula:
- Avoid processed food for the entire day
  EXP: 85
  Cooldown: None

- Take all supplements at the correct time today
  EXP: 70
  Cooldown: None

- Research one supplement that could benefit
  your goals
  EXP: 25
  Cooldown: None
  Note: Show only if player selected None Yet in Q4

Restoration Chamber:
- Sleep 7+ hours and track it
  EXP: 80
  Cooldown: None

- Sleep before midnight for 3 consecutive days
  EXP: 90
  Cooldown: 3 days

Inner Ecosystem:
- Eat a gut-friendly meal (fermented food
  or fiber-rich)
  EXP: 80
  Cooldown: None

- Add probiotics or fermented food to every
  meal today
  EXP: 75
  Cooldown: None

Purification Ritual:
- Drink 3L of water today
  EXP: 70
  Cooldown: None

- End shower with 60 seconds of cold water
  EXP: 75
  Cooldown: None
  Note: Available to ALL users — cold shower
  requires no equipment

Emotional Crucible:
- Do 10 minutes of stress breathwork
  EXP: 75
  Cooldown: None

- Identify your biggest stressor today and do
  one thing to reduce it
  EXP: 80
  Cooldown: None

- Spend 20 minutes in nature with no phone
  EXP: 90
  Cooldown: None

---

## Rank B Quests — Level 10 and above

Fuel Formula:
- Track all macros and hit targets today
  EXP: 140
  Cooldown: None

- Eat zero processed food for 3 consecutive days
  EXP: 170
  Cooldown: 7 days

- Do a 16 hour intermittent fast
  EXP: 150
  Cooldown: 2 days

Restoration Chamber:
- Sleep 8+ hours for 5 consecutive days
  EXP: 180
  Cooldown: 7 days

- Complete a sauna session (20 minutes minimum)
  EXP: 150
  Cooldown: 2 days
  Equipment gated: requires Sauna in Q4

Inner Ecosystem:
- Follow a gut reset day — clean eating no alcohol
  no sugar
  EXP: 160
  Cooldown: 3 days

- Add fermented food to every meal for
  3 consecutive days
  EXP: 145
  Cooldown: 7 days

Purification Ritual:
- Complete a full cold shower (3 minutes minimum)
  EXP: 130
  Cooldown: 1 day

- Complete an ice bath or cold plunge session
  EXP: 160
  Cooldown: 2 days
  Equipment gated: requires Ice Bath or
  Cold Plunge in Q4

- Complete cold plunge and sauna contrast therapy
  in one session
  EXP: 200
  Cooldown: 3 days
  Equipment gated: requires both Ice Bath
  and Sauna in Q4

Cold therapy disclaimer — show before completion
of any cold therapy quest:
"Listen to your body. Never push through pain
or dizziness."

Emotional Crucible:
- Complete a full Wim Hof breathwork session
  EXP: 140
  Cooldown: 1 day

- Track your stress level morning and evening
  for 7 days
  EXP: 160
  Cooldown: 7 days

- Have one honest conversation about how you
  are really feeling
  EXP: 140
  Cooldown: None

- Spend a full hour doing something that
  genuinely restores you
  EXP: 150
  Cooldown: None

Transmission Protocol:
- Write a full body audit — energy digestion
  mood and sleep
  EXP: 145
  Cooldown: 7 days

- Track your steps and hit 10000 today
  EXP: 130
  Cooldown: None
  Equipment gated: requires Fitness Tracker in Q4

---

## Rank A Quests — Level 20 and above

Fuel Formula:
- Follow a clean eating protocol for
  7 consecutive days
  EXP: 300
  Cooldown: 7 days

- Complete a supplement stack consistently
  for 30 days
  EXP: 350
  Cooldown: 30 days

Restoration Chamber:
- Sleep before 10PM for 5 consecutive days
  EXP: 260
  Cooldown: 7 days

- Achieve 8+ hours of sleep every night
  for 14 days
  EXP: 320
  Cooldown: 14 days

Inner Ecosystem:
3-day gut reset quest chain:
Day 1: Clean eating only
EXP: 120
Day 2: Add fermented food to every meal
EXP: 120
Day 3: No sugar no alcohol no processed food
EXP: 130
Chain completion bonus: +100 EXP
Day 2 unlocks only after Day 1 complete.
Day 3 unlocks only after Day 2 complete.
Build as a quest chain in the database.

Purification Ritual:
- Complete cold plunge and sauna contrast therapy
  for 7 days
  EXP: 290
  Cooldown: 7 days
  Equipment gated: requires both Ice Bath and
  Sauna in Q4

Emotional Crucible:
- Complete a digital detox day combined with
  a clean eating day
  EXP: 260
  Cooldown: 3 days

- Do a 7 day stress tracking log in Body Journal
  EXP: 270
  Cooldown: 7 days

Transmission Protocol:
- Track HRV sleep quality and energy for 7 days
  EXP: 290
  Cooldown: 7 days
  Equipment gated: requires Fitness Tracker in Q4

---

## Rank S Quests — Level 30 and above

Fuel Formula:
3-day clean eating reset chain:
Day 1: Zero processed food
EXP: 200
Day 2: Zero processed food plus track macros
EXP: 200
Day 3: Zero processed food plus hit all
nutrition targets
EXP: 200
Chain completion bonus: +200 EXP
Total EXP for full chain: 800
Cooldown: 30 days after chain completion
Build as a quest chain same as gut reset above.

- Maintain complete supplement protocol
  for 90 days
  EXP: 800
  Cooldown: One-time only

Restoration Chamber:
- Maintain a perfect sleep schedule for 30 days
  EXP: 650
  Cooldown: 30 days

Purification Ritual:
- Complete cold therapy every day for 30 days
  EXP: 700
  Cooldown: 30 days

Transmission Protocol:
- Complete a full body health audit — blood work
  vitals and doctor checkup
  EXP: 500
  Cooldown: 90 days

- Achieve 30 days of clean eating optimal sleep
  and daily hydration simultaneously
  EXP: 900
  Cooldown: One-time only
  Note: Tracked as three simultaneous daily
  check-ins for 30 days

---

## Elixir System

This mechanic is the primary consistency reward
for the Health Alchemist path.

ELIXIR BOTTLE UI:
A glowing elixir bottle is displayed prominently
on the dashboard.
Each day the user completes their daily quests
the bottle fills.
The liquid color shifts as days progress:

Day 1 to 2: Pale yellow — Base Formula
Day 3 to 4: Amber — Heating Up
Day 5 to 6: Deep orange — Nearly Complete
Day 7: Glowing gold — Elixir Complete

COMPLETING THE ELIXIR:
On Day 7 a Drink Your Elixir button appears.
User taps it to complete the ritual.

Rewards on completion:
300 bonus EXP
Elixir completion badge logged to profile
Transmutation counter advances by 1
Completion message:
"The formula is complete Alchemist. Your body
absorbs the transformation."

MERCY MECHANIC:
If streak breaks before Day 7:
Elixir does NOT reset to zero.
Bottle retains 50% fill shown as cracked
but not empty.
Message displayed:
"Your elixir is incomplete but not lost.
Resume your formula Alchemist."
This prevents total abandonment after
one missed day.

TRANSMUTATION MILESTONES:
Every 4 completed elixirs (28 days of
consistent health habits):
Unlock a Transmutation — permanent profile
title upgrade.

Title progression:
1 elixir: Apprentice Alchemist
2 elixirs: The Brewer
3 elixirs: Formula Seeker
4 elixirs: Transmuter
5+ elixirs: Grand Alchemist

Each title upgrade triggers:
Achievement card generated
Unique badge added to profile
Full screen congratulation animation

---

## Body Journal Feature

The Body Journal is a personal health timeline
unique to the Health Alchemist path.

HOW IT WORKS:
After completing any Restoration Chamber or
Transmission Protocol quest user is optionally
prompted:
"How does your body feel today?"

User rates four metrics using simple 1 to 5 sliders:
- Energy level
- Digestion quality
- Mood
- Sleep quality

Entry saved with date quest name and current level.
Entries are private by default.

BODY JOURNAL UI:
Accessible as a dedicated tab on dashboard.
Shows entries in reverse chronological order.
Displays simple trend lines for each metric
over time.
Entry count shown:
"Body Journal — 30 days of data tracked"

MILESTONE NOTIFICATIONS:
7 entries: "One week of body data tracked."
30 entries: "Your formula is revealing patterns
Alchemist."
90 entries: "Three months of transformation
documented."

SHAREABILITY:
At 30 and 90 entry milestones generate
shareable achievement card:
"Health Alchemist — [X] Days of Body Data Tracked"

IMPORTANT:
Body Journal data must be preserved permanently
regardless of whether Health Alchemist path is
active or deactivated.
If path deactivated: Body Journal becomes read-only.
Player can still view history but cannot add
new entries until path is reactivated.

---

## Weekly Boss Quest

Appears every Monday. Resets Monday at 00:00.
Completion awards EXP plus exclusive weekly badge.

Rotating examples:

Week option 1:
"Complete the Morning Protocol every day this week"
EXP: 400
Badge: Morning Alchemist

Week option 2:
"Hit 3L water and 7+ hours sleep every day
this week"
EXP: 380
Badge: Foundation Week

Week option 3:
"Complete 3 cold therapy sessions this week"
EXP: 420
Badge: Cold Warrior

Week option 4:
"Eat zero processed food for 5 days this week"
EXP: 390
Badge: Clean Formula

Week option 5:
"Log Body Journal entries every day this week"
EXP: 370
Badge: Body Tracker

---

## Adaptive Difficulty Nudge

If player completes all daily quests for
7 consecutive days trigger nudge on Day 8:

"Your formula is working Alchemist. Ready to
intensify your protocol?"

Options:
- Yes upgrade my formula
- Not yet keep current protocol

If yes:
Surface more B rank quests.
Upgrade D rank universal quests to C rank
equivalents.

---

## Cross-Path Bonuses

Cold shower completed in both Fitness Warrior
AND Health Alchemist on same day:
Award +20 EXP bonus to both quests.
Message: "Body and mind forged together."

Breathwork completed in both Mindset Sage AND
Health Alchemist on same day:
Award +20 EXP bonus to both quests.
Message: "Breath connects body and soul."

---

## Social Features

Achievement cards auto-generated for:
- Level up
- Rank unlock
- Elixir completion
- Transmutation title upgrade
- Body Journal milestones
- Boss quest completion
- Morning Protocol 30 day streak
- The Optimized Human title unlocked

Badges for this path:
- Purification Ritual: 30 day cold therapy streak
- Grand Alchemist: Level 30 reached
- Elixir Transmuter: 4 elixirs complete
- Clean Formula: 7 days zero processed food
- Restoration Master: 30 day sleep streak
- Inner Ecosystem Guardian: 30 days gut health
  quests completed
- The Optimized Human: Fitness Warrior and
  Mindset Sage and Health Alchemist all active
  7 consecutive days

Leaderboard:
Weekly EXP leaderboard among all Health Alchemist
users.
Resets every Monday at 00:00.
Shows top 10 globally plus user own rank.

Profile visibility:
Public by default.
Private option available in settings.
Public profile shows: level rank streak badges
recent achievements current Elixir progress.

---

## Day 1 Starter Lineup

On the player's very first day the algorithm
does not run. Use this hardcoded lineup instead:

Quest 1: Drink 2L of water today (30 EXP D rank)
Quest 2: Complete the Alchemist Morning Protocol
(150 EXP C rank)
Quest 3: Eat one whole food meal today
(35 EXP D rank)

Algorithm takes over from Day 2 onwards.

---

## Daily Override Logic

Every morning:
Morning Protocol quest always fills first
assigned slot.
Cannot be swapped by player.

If Elixir is on Day 7:
Surface highest EXP available quests in
remaining assigned slots to maximize
completion day reward.

Equipment gated quests:
Never appear in assigned or bonus slots for
players who do not have required equipment
in their EquipmentProfile.
Only appear in swap drawer if player has
the equipment.
Player can update equipment profile in settings
at any time to unlock these quests.

---

## Equipment Gating Rules

These quests require specific equipment
and must be hidden from players who do not
have that equipment selected in Q4:

Requires Sauna:
- Complete a sauna session (20 minutes minimum)
- Complete cold plunge and sauna contrast therapy
  in one session
- Complete cold plunge and sauna contrast therapy
  for 7 days

Requires Ice Bath or Cold Plunge:
- Complete an ice bath or cold plunge session
- Complete cold plunge and sauna contrast therapy
  in one session (requires both)

Requires Fitness Tracker or Wearable:
- Track your steps and hit 10000 today
- Track HRV sleep quality and energy for 7 days

Cold shower quests (end shower with 60 seconds
cold water, full cold shower 3 minutes) are
available to ALL users regardless of equipment.
Cold shower requires no equipment.

---

## Important Implementation Notes

1. Supplement disclaimer must appear in THREE places:
   top of Setup Guide before recommendations
   bottom of Setup Guide
   one line on every supplement card
   Do not remove or shorten the disclaimer text.
   This is non-negotiable.

2. Equipment gating logic: quests requiring equipment
   the user does not have must be hidden from
   quest pool until they update their profile.
   Player can update equipment profile in settings.

3. The 3-day gut reset and 3-day clean eating reset
   are quest chains. Day 2 unlocks only after Day 1
   is marked complete. Day 3 unlocks only after
   Day 2 complete. Build chain logic in backend.

4. Body Journal prompt is always optional.
   Never block quest completion waiting for
   a Body Journal entry.

5. Body Journal data must survive path deactivation.
   If player deactivates Health Alchemist their
   Body Journal history is preserved as read-only.

6. The cold therapy disclaimer must appear before
   the player can mark any cold therapy quest
   complete. One tap to acknowledge then complete.

7. Personalized starter pack in Setup Guide uses
   Q1 goal and Q2 experience to generate the
   correct recommendation text. Build conditional
   logic for all combinations.

8. All quest completions are self-reported.
   No verification required for V1.