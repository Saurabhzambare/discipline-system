# Path Discovery System
# docs/game-design/systems/path-discovery.md

---

## How To Use This File

Read this file when:
- Building the Path Discovery Quiz backend
- Building the quiz frontend flow
- Building the results screen
- Building path cards
- Building the commitment screen
- Building multi-path unlock logic
- Building quiz retake feature

Always read these files first before this one:
- AGENTS.md
- docs/architecture.md
- docs/phase-5b-quest-system-redesign.md
- docs/game-design/README.md
- docs/game-design/BUILD_ORDER.md

---

## System Overview

The Path Discovery System is the first experience
a new user has after signing up.
It also runs for existing users who are being
re-onboarded after the Phase 5B migration.

Purpose:
Most users do not know which path is right for them.
They know they want to improve but they do not know
where to start or who they actually are right now.

The Path Discovery System solves this by:
1. Showing users a mirror — reflecting their
   current reality back at them
2. Recommending the right path based on answers
3. Showing them who they will become if they commit
4. Letting them choose with full confidence

This system runs ONCE on first signup before any
path is selected or any quest is shown.
It can be retaken anytime from profile settings.

---

## Full User Flow

Signup completed
→ Welcome Screen
→ Identity Quiz (9 questions)
→ Results Screen (all 5 paths with match %)
→ Path Cards (transformation stories)
→ Path Selection
→ Commitment Screen
→ Path-Specific Onboarding
→ Dashboard

---

## Welcome Screen

First screen shown after signup.
Before quiz begins.

UI requirements:
Full dark screen.
Single centered text block.
Slow fade in animation.
No navigation elements.
No skip button.

Message text:
"Before you begin your journey Hunter — let us
understand who you are right now.
There are no wrong answers.
Only honest ones."

Button: "Begin"
Button fades in after message completes.
Tapping Begin starts the quiz.

---

## Quiz UI Requirements

These requirements apply to every single
question screen:

- Full dark background throughout
- One question displayed per screen — full screen
- Slow animated transition between questions —
  fade or slide
- No progress bar visible anywhere
- Answer options displayed as tappable cards
- Selected answer highlights immediately
- App auto-advances to next question after
  brief pause on selection
- No back button — quiz flows forward only
- Entire quiz completable in under 3 minutes
- Answer option ORDER must be randomized
  server-side per question per user
  This prevents pattern gaming where users
  recognize that option E is always Health Alchemist

---

## Scoring Logic

Five paths scored independently across 9 questions.

Paths:
- FW = Fitness Warrior
- MS = Mindset Sage
- HA = Health Alchemist
- DK = Discipline Knight
- GV = Grind Visionary

Maximum possible score per path: 27 points
Match percentage formula:
(path_score divided by 27) multiplied by 100
Round to nearest whole number.

Store raw scores AND percentages per user
in database. Both values needed for future
features and analytics.

---

## Question 1

Question text:
"When you wake up in the morning what is your
first feeling?"

Option A:
"My body feels heavy and I just want more sleep"
FW: 2 points
HA: 2 points

Option B:
"My mind is already racing with thoughts
and stress"
MS: 3 points
HA: 1 point

Option C:
"I feel okay but I know I am not living up to
my potential"
DK: 3 points
GV: 1 point

Option D:
"I feel behind — like everyone else is ahead
of me"
GV: 3 points
DK: 1 point

Option E:
"I feel unfocused — I have energy but no
direction"
FW: 1 point
MS: 1 point
DK: 1 point
GV: 1 point

---

## Question 2

Question text:
"What does your average day look like right now?"

Option A:
"I go to the gym or exercise but the rest of my
day is unstructured"
FW: 2 points
DK: 2 points

Option B:
"I work or study but I feel mentally drained
and scattered"
MS: 2 points
HA: 2 points

Option C:
"I have no real routine — each day just
happens to me"
DK: 3 points
MS: 1 point

Option D:
"I have big goals but I spend more time thinking
than doing"
GV: 3 points
DK: 1 point

Option E:
"I feel healthy physically but something is
missing inside"
HA: 2 points
MS: 2 points

---

## Question 3

Question text:
"What is the gap you feel most in your life
right now?"

Option A:
"My body does not match the effort I put in"
FW: 3 points
HA: 1 point

Option B:
"My mind works against me more than for me"
MS: 3 points
HA: 1 point

Option C:
"I know what to do but I cannot make myself
do it consistently"
DK: 3 points
GV: 1 point

Option D:
"I have a vision but I am not building toward
it fast enough"
GV: 3 points
DK: 1 point

Option E:
"I feel drained stressed or burnt out from
the inside"
HA: 3 points
MS: 1 point

---

## Question 4

Question text:
"If you could change one thing about yourself
in 90 days what would it be?"

Option A:
"Be stronger leaner and more athletic"
FW: 3 points

Option B:
"Be calmer clearer and more mentally resilient"
MS: 3 points

Option C:
"Be more consistent and disciplined in
everything I do"
DK: 3 points

Option D:
"Have built real skills or shipped real work
I am proud of"
GV: 3 points

Option E:
"Feel genuinely healthy energized and restored
from within"
HA: 3 points

---

## Question 5

Question text:
"What do you respect most in other people?"

Option A:
"Their physical dedication and athletic ability"
FW: 3 points

Option B:
"Their calm wisdom and emotional intelligence"
MS: 3 points

Option C:
"Their unbreakable consistency and self-control"
DK: 3 points

Option D:
"Their ambition output and relentless work ethic"
GV: 3 points

Option E:
"Their vitality health and how they take care
of themselves"
HA: 3 points

---

## Question 6

Question text:
"When you fail to keep a commitment to yourself
what is usually the reason?"

Option A:
"I lose motivation after missing a few workouts"
FW: 2 points
DK: 1 point

Option B:
"My thoughts and emotions get in the way"
MS: 2 points
HA: 1 point

Option C:
"I start strong but cannot maintain the routine"
DK: 3 points

Option D:
"I get distracted and work on the wrong things"
GV: 2 points
DK: 1 point

Option E:
"My energy and health make everything harder"
HA: 2 points
FW: 1 point

---

## Question 7

Question text:
"What kind of achievement would make you feel
most proud?"

Option A:
"Completing a physical challenge — a race or
a body transformation"
FW: 3 points

Option B:
"Finishing a book developing a new mindset or
overcoming a deep fear"
MS: 3 points

Option C:
"Building a routine so solid it runs without
willpower"
DK: 3 points

Option D:
"Launching a project earning from my skill or
leveling up my career"
GV: 3 points

Option E:
"Healing my body from within and feeling
genuinely well"
HA: 3 points

---

## Question 8

Question text:
"Which statement resonates most with where you
are right now?"

Option A:
"I train but I am not as consistent or as fit
as I want to be"
FW: 3 points

Option B:
"I overthink everything and struggle to find
mental peace"
MS: 3 points

Option C:
"I know exactly what I should do — I just do
not do it"
DK: 3 points

Option D:
"I have a goal but I am not making enough
progress toward it"
GV: 3 points

Option E:
"I am burning out and my body and mind are
paying the price"
HA: 3 points

---

## Question 9

Question text:
"What does your ideal self look like in
one year?"

Option A:
"Athletic strong disciplined in body — people
notice the change"
FW: 3 points

Option B:
"Calm wise emotionally unshakeable — I think
before I react"
MS: 3 points

Option C:
"Structured reliable consistent — I do what
I say I will do"
DK: 3 points

Option D:
"Skilled building earning — I have created
something real"
GV: 3 points

Option E:
"Vibrant healthy optimized — I feel as good
as I look"
HA: 3 points

---

## Results Calculation

After Question 9 is answered:

Step 1:
Tally total points per path across all
9 questions.

Step 2:
Calculate match percentage per path:
(path_score divided by 27) multiplied by 100
Round to nearest whole number.

Step 3:
Sort all five paths by match percentage
descending.
Top path = primary recommendation.

Step 4:
Save all raw scores and match percentages
to PathMatchScore model linked to quiz.

Step 5:
Serve results to frontend immediately.
Do not make player wait.

---

## Results Screen

Shown immediately after Question 9 is answered.

UI requirements:
Dark background.
Dramatic reveal animation.
Primary recommended path appears first with
full animation before other paths appear.

OPENING LINE:
Changes based on which path has highest
match percentage.

If Fitness Warrior is top match:
"You are a warrior who has not yet found your
battlefield. Your body is your weapon — and it
is time to forge it."

If Mindset Sage is top match:
"Your greatest battles happen inside your own
mind. It is time to become the master of your
thoughts."

If Discipline Knight is top match:
"You know exactly what you need to do. The only
thing standing between you and your goals is the
system to execute it."

If Grind Visionary is top match:
"You have a vision that most people cannot see
yet. It is time to build the proof."

If Health Alchemist is top match:
"Your body is trying to tell you something.
It is time to listen — and transform from within."

MATCH DISPLAY:
Show all five paths with icons and percentages
sorted from highest to lowest match.

Display format:
⚔️  Fitness Warrior          [XX]% match
🧘  Mindset Sage              [XX]% match
🛡️  Discipline Knight         [XX]% match
⚗️  Health Alchemist          [XX]% match
🔥  Grind Visionary           [XX]% match

Highest match path has glow or highlighted
border effect to distinguish it.

Text below the list:
"Your strongest match is highlighted.
All paths are always available to you."

Button: "Explore Your Paths"
Leads to Path Cards screen.

---

## Path Cards Screen

After results screen player sees all five
path cards.
Paths displayed in order of match percentage —
highest first.
Player can scroll through all cards before
choosing.
Each card shows the path's match percentage
badge in top right corner.

Each path card contains four sections:

SECTION 1 — WHO YOU ARE NOW
Identity mirror statement.
Reflects the player's current reality.

SECTION 2 — WHO YOU BECOME IN 90 DAYS
Transformation story.
Specific and concrete — not vague promises.

SECTION 3 — WHAT YOU GAIN
Bullet list of core benefits.
5 to 6 items maximum.

SECTION 4 — THIS PATH IS FOR YOU IF
Mirror statement that speaks directly to
the player's situation.

CHOOSE BUTTON:
Each card has a Choose [Path Name] button.
Tapping it leads to Commitment Screen for
that path.

---

## Path Card Content

---

FITNESS WARRIOR CARD

Match badge: [XX]% match

Who you are now:
"You train but inconsistency plateau or lack
of structure is keeping you from the body and
performance you know you are capable of."

Who you become in 90 days:
"In 90 days you will have built a structured
training system around your split developed
hybrid strength and endurance established
nutrition habits that fuel performance and
built a streak that proves to yourself you
are someone who shows up no matter what."

What you gain:
- A gamified training system built around
  your actual split
- Daily quests that reward what you are
  already doing
- Strength endurance and conditioning
  working together
- A public social profile showing your
  athletic progress
- Badges and achievements that make your
  discipline visible

This path is for you if:
"You already train or want to — but you need
a system that keeps you accountable tracks
your progress like a game and makes consistency
feel rewarding instead of exhausting."

Button: "Choose Fitness Warrior"

---

MINDSET SAGE CARD

Match badge: [XX]% match

Who you are now:
"Your mind is your biggest obstacle.
Overthinking self-doubt lack of mental clarity
or the inability to stay present is costing you
more than you realize."

Who you become in 90 days:
"In 90 days you will have built a daily
meditation and journaling practice developed
emotional resilience through consistent Shadow
Training filled your Wisdom Log with 90 personal
insights and built the mental stillness to think
clearly under pressure."

What you gain:
- A daily mental training system across
  four pillars
- Freedom Day tokens earned through consistency
- A personal Wisdom Log that becomes your
  life philosophy
- The Dark Night Quest for your hardest days
- An identity shift from reactive thinker
  to deliberate Sage

This path is for you if:
"You want to stop being controlled by your
emotions your phone and your overthinking —
and start moving through life with the calm
clarity of someone who has done the inner work."

Button: "Choose Mindset Sage"

---

DISCIPLINE KNIGHT CARD

Match badge: [XX]% match

Who you are now:
"You know exactly what you need to do. The gap
is not knowledge — it is execution. You start
strong and fade. You make promises to yourself
and break them. The routine never sticks."

Who you become in 90 days:
"In 90 days you will have built an unbreakable
daily routine forged four pieces of your armor
through consistent weekly execution sworn and
honored your personal Discipline Code and become
someone whose word to themselves actually means
something."

What you gain:
- The Armor System — visible public proof
  of your consistency
- A personal Discipline Code you write
  and live by
- The War Room daily planning tool built
  into the app
- A Temptation Log that tracks your growing
  Iron Will
- Weekly automated reports showing your
  discipline data

This path is for you if:
"You are tired of knowing what to do and not
doing it. You want a system with real consequences
for breaking it and real rewards for honoring it —
and you want the world to see your armor growing."

Button: "Choose Discipline Knight"

---

HEALTH ALCHEMIST CARD

Match badge: [XX]% match

Who you are now:
"You feel drained stressed or burnt out. Your
body is running on empty. You know your health
habits need work but you do not know where to
start or what actually matters."

Who you become in 90 days:
"In 90 days you will have built a morning
protocol that optimizes your body from the
moment you wake up established nutrition and
hydration habits that fuel your energy completed
multiple Elixirs through consistent daily
practice and developed a Body Journal with
90 days of personal health data showing your
transformation."

What you gain:
- A personalized supplement and nutrition
  guide built for your goals
- The Elixir System — a brewing streak with
  a mercy mechanic
- A Body Journal tracking energy sleep mood
  and digestion daily
- Budget-friendly biohacking tools and cold
  therapy guidance
- An Alchemist Setup Guide showing exactly
  how to start

This path is for you if:
"You want to feel as good on the inside as
you want to look on the outside. You are ready
to treat your body like a laboratory and
experiment with the habits that actually
transform your energy health and vitality."

Button: "Choose Health Alchemist"

---

GRIND VISIONARY CARD

Match badge: [XX]% match

Who you are now:
"You have a vision — something you want to
build learn or become. But the gap between
where you are and where you want to be feels
overwhelming. You consume more than you create.
You think more than you ship."

Who you become in 90 days:
"In 90 days you will have built a daily skill
practice around your chosen field logged real
output in your portfolio progressed through your
Skill Tree potentially generated your first income
from your skill and built a multiplier streak that
compounds every action you take."

What you gain:
- An XP multiplier that rewards compound
  consistency
- A Skill Tree that maps your progression
  in your chosen field
- An Output Log that becomes your proof
  of work portfolio
- The Vision Board showing your singular
  goal and countdown daily
- The First Dollar legendary moment when
  your skill pays off

This path is for you if:
"You have something you want to build — a skill
a career a side hustle a body of work. You need
a system that turns daily effort into visible
progress and makes showing up feel like leveling
up."

Button: "Choose Grind Visionary"

---

## Commitment Screen

After player taps any Choose Path button show
a full screen commitment message before
finalizing the selection.

UI requirements:
Full dark screen.
Path icon centered.
Slow animation.
No back button.

Commitment message changes per path:

Fitness Warrior:
"You have chosen the path of the Fitness Warrior.
This is not just a choice — it is a declaration.
Every quest you complete from this day forward
is proof of who you are becoming.
The forge begins now Hunter."

Mindset Sage:
"You have chosen the path of the Mindset Sage.
This is not just a choice — it is a declaration.
Every moment of stillness you create is a weapon
being sharpened.
The inner journey begins now Hunter."

Discipline Knight:
"You have chosen the path of the Discipline
Knight.
This is not just a choice — it is a declaration.
Every day you show up adds armor that the world
can see.
The forge begins now Hunter."

Health Alchemist:
"You have chosen the path of the Health Alchemist.
This is not just a choice — it is a declaration.
Every habit you build is an ingredient in your
transformation.
The laboratory opens now Hunter."

Grind Visionary:
"You have chosen the path of the Grind Visionary.
This is not just a choice — it is a declaration.
Every day you show up compounds into the empire
you are building.
The grind begins now Hunter."

Button: "Begin My Journey"

Tapping Begin My Journey:
Saves path selection to UserPathSelection model.
Routes player to path-specific onboarding
questions for their chosen path.
Path-specific onboarding described in
each path file in docs/game-design/paths/

---

## Multi-Path Unlock Logic

Users choose ONE primary path on signup.
Additional paths unlock through consistent use.

UNLOCK TRIGGER:
Check consecutive day count on each player login.
After 30 consecutive days on primary path
automatically trigger multi-path unlock prompt.

PROMPT MESSAGE:
"You have proven yourself on your primary path
Hunter. Are you ready to add a second path to
your journey?"

PROMPT OPTIONS:
- Yes — show path selection for remaining paths
- Not yet — dismiss prompt

If Not yet selected:
Dismiss prompt.
Ask again at Day 60 if player still has
only one active path.

SECOND PATH SELECTION:
Show same path cards screen but with
Already Active label on primary path card.
Player selects a second path.
Second path onboarding runs immediately.

SUBSEQUENT PATHS:
Each additional path unlocks every 30 days of
consistency on ALL currently active paths.
Not just the primary path.
Third path at Day 60 of multi-path consistency.
Fourth path at Day 90.
Fifth path at Day 120.

CRITICAL RULE:
Never push multi-path selection before Day 30.
Overwhelming new users before they are committed
kills retention permanently.

---

## Quiz Retake Feature

Player can retake the Identity Quiz anytime
from profile settings.

Settings label: "Retake Path Discovery Quiz"

ON RETAKE:
Run full 9 question quiz again exactly as
on first signup.
Show new results with updated match percentages.
Player can switch primary path if desired.

IMPORTANT DATA RULE:
Previous quiz records must be preserved.
Never overwrite old quiz data.
Always append new quiz as separate record.
Store retake_count on PathDiscoveryQuiz model.

IF PLAYER SWITCHES PATH AFTER RETAKE:
Show message:
"Your previous journey has been saved Hunter.
Your new path begins now. The hunter evolves."
Previous path data preserved in database.
New path onboarding runs immediately.

---

## Sixth Path Placeholder

On the path selection screen and path cards
screen show a sixth locked placeholder card.

Visual: Same card style as other paths but
greyed out with lock icon overlay.
Label: "Coming Soon"

Tap response:
"A new path is being forged. Stay disciplined
Hunter — it is coming."

Non-selectable.
No functionality behind it.
No data model needed for this placeholder.

---

## Data Models Needed

Review existing models before creating any
of these. Extend existing models where possible.

PathDiscoveryQuiz:
- user (FK to User)
- completed (boolean)
- completed_at (datetime)
- retake_count (integer default 0)

QuizAnswer:
- quiz (FK to PathDiscoveryQuiz)
- question_number (integer 1 to 9)
- answer_selected (char A B C D or E)
- points_awarded (JSON — points per path
  for this specific answer)

PathMatchScore:
- quiz (FK to PathDiscoveryQuiz)
- path (char — FW MS DK HA GV)
- raw_score (integer)
- match_percentage (integer)

UserPathSelection:
- user (FK to User)
- primary_path (char)
- selected_at (datetime)
- multi_paths_active (JSON array of path codes)
- multi_path_unlock_day (integer — day count
  when next path unlocks)

---

## API Endpoints Needed

Follow existing API patterns in:
backend/quests/views.py
backend/social/views.py

Suggested endpoints:

POST /api/paths/quiz/start/
Start a new PathDiscoveryQuiz for user.
Returns quiz ID.

POST /api/paths/quiz/answer/
Submit one answer.
Request: quiz_id question_number answer_selected
Returns: next question or results if Q9

GET /api/paths/quiz/results/
Get match percentages for completed quiz.
Returns all five paths with scores and percentages
sorted by percentage descending.

POST /api/paths/select/
Save path selection after commitment screen.
Request: path code
Triggers path-specific onboarding flow.

POST /api/paths/retake/
Start a new quiz retake.
Preserves all previous quiz records.

GET /api/paths/active/
Get all currently active paths for user.
Returns primary path and any additional paths.

---

## Important Implementation Notes

1. Answer order randomization must be server-side.
   Never randomize on the frontend.
   Randomization per question per user must be
   consistent within one quiz session but different
   across quiz retakes and across different users.

2. Scoring logic must be server-side only.
   Never calculate match percentages on frontend.
   Frontend receives only the final sorted results.

3. Quiz must feel like self-discovery not a test.
   UI design is critical:
   Dark background throughout.
   One question at a time full screen.
   Slow transitions between questions.
   No progress bar visible at any point.
   Never show question numbers like 3 of 9.

4. Path cards must be ordered dynamically by
   match percentage per user. Do not hardcode
   the display order.

5. Commitment screen saves path selection before
   routing to onboarding. If routing fails after
   commitment the path selection must still be saved.
   Use database transaction to ensure atomicity.

6. Multi-path unlock check runs on every login.
   Not just on day 30. Check consecutive days on
   login and trigger prompt if threshold reached.

7. Previous quiz records must never be deleted.
   Even if player retakes quiz 10 times all 10
   records are preserved in PathDiscoveryQuiz table.

8. The sixth path placeholder requires no backend
   work. Frontend only. No API endpoint needed.
   No data model needed.

9. Re-onboarding existing users after Phase 5B
   migration: on their next login check if they
   have completed PathDiscoveryQuiz. If not show
   the quiz flow before dashboard loads.
   This handles the migration re-onboard requirement
   from docs/phase-5b-quest-system-redesign.md
   without touching user accounts.