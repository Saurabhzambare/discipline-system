# Discipline System — Build Order and Progress Tracker
# docs/game-design/BUILD_ORDER.md

---

## How To Use This File

This file is the single source of truth for what
has been built and what still needs to be built.

At the start of every Claude Code session say:
"Read AGENTS.md. Read docs/architecture.md.
Read docs/phase-5b-quest-system-redesign.md.
Read docs/game-design/README.md.
Read docs/game-design/BUILD_ORDER.md.
Find the first unchecked step and tell me
what it is before doing anything."

Rules:
- Never skip a step
- Never build out of order
- Check off each step only when fully complete
- If a step reveals a conflict stop and
  report it to the developer before continuing
- Never run a migration without showing the
  developer the migration file first

---

## Pre-Build — Repository Audit
## Complete This Entirely Before Writing Any Code

- [ ] Read AGENTS.md in full
- [ ] Read docs/architecture.md in full
- [ ] Read docs/phase-5b-quest-system-redesign.md
      in full
- [ ] Read docs/game-design/README.md in full
- [ ] Read all files in docs/game-design/paths/
- [ ] Read all files in docs/game-design/systems/
- [ ] Inspect backend/players/models.py —
      note Player model fields especially path field
      and current path choices
- [ ] Inspect backend/quests/models.py —
      note Quest model fields and
      PlayerDailyQuestAssignment model fields
- [ ] Inspect backend/quests/services.py —
      understand existing service patterns
- [ ] Inspect backend/quests/management/
      commands/seed_quests.py —
      understand existing seed logic
- [ ] Inspect backend/social/models.py —
      note all existing social models
- [ ] Inspect backend/social/services.py —
      understand existing social service patterns
- [ ] Inspect backend/social/serializers.py
- [ ] Inspect backend/social/views.py
- [ ] Inspect backend/players/serializers.py
- [ ] Inspect backend/players/views.py
- [ ] Inspect backend/users/models.py
- [ ] Inspect frontend/src/pages/OnboardingPage.jsx
- [ ] Inspect frontend/src/pages/DashboardPage.jsx
- [ ] Inspect frontend/src/pages/ProfilePage.jsx
- [ ] Inspect frontend/src/components/QuestCard.jsx
- [ ] Inspect frontend/src/components/ProgressCard.jsx
- [ ] Inspect frontend/src/api.js
- [ ] Produce full conflict map showing:
      what already exists
      what needs to be created
      what needs to be modified
      what needs to be deleted
      migration plan for Player.path field
      list of all new models to be created
      confirmation no duplicate models exist
- [ ] Show conflict map to developer
- [ ] Get developer approval on conflict map
- [ ] Get developer approval on migration plan
- [ ] Pre-build audit complete — approved to build

---

## Session 1 — Foundation Models and Migration

- [ ] Step 1: Show developer the Player.path
      migration file before running —
      update path field choices to:
      fitness_warrior, mindset_sage,
      health_alchemist, discipline_knight,
      grind_visionary
- [ ] Step 2: Developer approves migration —
      run migration
- [ ] Step 3: Clear old quest seed data cleanly —
      show developer the clear plan before executing
- [ ] Step 4: Extend Quest model with new fields —
      pillar, pack_id, equipment_required,
      universal_daily, path_specific, cooldown_days
      (confirm against existing model first —
      only add fields that do not already exist)
- [ ] Step 5: Create new models — confirm each
      against existing models before creating:

      Path Discovery models:
      PathDiscoveryQuiz
      QuizAnswer
      PathMatchScore
      UserPathSelection

      Fitness Warrior models:
      SplitDayState

      Mindset Sage models:
      WisdomLog
      FreedomDayToken
      DarkNightEntry
      SageArchetype

      Health Alchemist models:
      BodyJournal
      ElixirProgress
      TransmutationMilestone
      EquipmentProfile
      QuestChain

      Discipline Knight models:
      ArmorSystem
      ArmorPiece
      DisciplineCode
      GraceToken
      StreakShield
      TemptationLog
      WarRoomEntry
      WeeklyReport

      Grind Visionary models:
      GrindFocus
      SingularGoal
      XPMultiplier
      MultiplierProtection
      OutputLog
      SkillTree
      SkillTreeNode
      AccountabilityPartner
      VisionBoard
      PostFirstDollarChain

      Daily Quest Assignment models:
      DailyQuestLineup
      DailyQuestCompletion
      QuestFeedback
      QuestPreference
      DailyIntention
      DailySwap
      CrossPathBonus
      DailyCompletionSummary

      Social Achievement models
      (add to existing social app):
      Badge
      UserBadge
      AchievementCard
      WeeklyBossQuest
      WeeklyBossCompletion

- [ ] Step 6: Show developer all migration files
      before running
- [ ] Step 7: Developer approves — run migrations
- [ ] Step 8: Verify database integrity —
      no broken relations, no missing tables
- [ ] Step 9: Add timezone field to user or
      player profile — used for midnight reset
      and end of day summary timing

---

## Session 2 — Path Discovery System

Read before this session:
docs/game-design/systems/path-discovery.md

- [ ] Step 10: Build quiz scoring backend logic —
      server-side only, points per path per answer,
      match percentage calculation
- [ ] Step 11: Build answer order randomization —
      server-side, different order per question
      per user to prevent pattern gaming
- [ ] Step 12: Build PathDiscoveryQuiz
      API endpoints:
      POST create quiz session
      POST submit answer
      GET results with match percentages
- [ ] Step 13: Build UserPathSelection endpoints:
      POST select path
      GET current path selection
      POST retake quiz
- [ ] Step 14: Build multi-path unlock logic —
      check consecutive day count on login,
      trigger prompt automatically at Day 30
- [ ] Step 15: Build frontend quiz flow —
      full dark screen UI
      one question per screen
      slow animated transitions
      no progress bar visible
      auto-advance on answer tap
      no back button
- [ ] Step 16: Build results screen —
      opening line changes per top match path
      all five paths shown with match percentages
      highest match path highlighted with glow
- [ ] Step 17: Build path cards screen —
      all five cards ordered by match percentage
      each card shows:
      match percentage badge
      who you are now
      who you become in 90 days
      what you gain
      this path is for you if
      Choose path button
- [ ] Step 18: Build commitment screen —
      full screen dark overlay
      path-specific commitment message
      Begin My Journey button
- [ ] Step 19: Build sixth path locked placeholder —
      same card style greyed out with lock icon
      label: Coming Soon
      tap shows: a new path is being forged message
      non-selectable no functionality behind it
- [ ] Step 20: Replace or extend existing
      OnboardingPage.jsx with new
      Path Discovery flow —
      confirm with developer before replacing

---

## Session 3 — Quest Data Seeding

Read before this session:
docs/game-design/paths/fitness-warrior.md
docs/game-design/paths/mindset-sage.md
docs/game-design/paths/health-alchemist.md
docs/game-design/paths/discipline-knight.md
docs/game-design/paths/grind-visionary.md

- [x] Step 21: Extend seed_quests.py —
      clear old quest data first
      then seed new data
      do not replace the file
      follow existing seed patterns
- [x] Step 22: Seed Fitness Warrior quests —
      all ranks D C B A S
      universal daily quests
      rest day recovery quests
      weekly boss quests
- [x] Step 23: Seed Mindset Sage quests —
      all ranks D C B A S
      all four pillars
      Stoic Challenge quests
      Dark Night Quest
      universal daily quests
      weekly boss quests
- [x] Step 24: Seed Health Alchemist quests —
      all ranks D C B A S
      all six pillars
      Morning Protocol quest
      equipment gated quests flagged
      quest chain quests linked
      universal daily quests
      weekly boss quests
- [x] Step 25: Seed Discipline Knight quests —
      all ranks D C B A S
      all six pillars
      Honor Review quest (Sunday only flag)
      War Room quests
      universal daily quests
      weekly boss quests
- [x] Step 26: Seed Grind Visionary quests —
      all ranks D C B A S
      all six pillars with level unlock flags
      First Dollar quest flagged as legendary
      Post-First-Dollar chain linked
      universal daily quests
      weekly boss quests
- [x] Step 27: Verify all quest data in
      Django admin — check counts per path
      per rank, check cooldown fields,
      check pillar assignments

Session 3 patch notes (hardening):
- Added `paths.QuestChain` model and migration for directed chain links (`parent_quest` → `child_quest` with `sequence_order`).
- Seed command now upserts chain edges for `ha_gut_reset_chain`.
- Seed command now upserts `social.WeeklyBossQuest` records from boss quest templates.
- Enforced exact supplement disclaimer text on all supplement-related Health Alchemist quest descriptions.
- API contract fix: removed duplicate `JSON.stringify` in quiz/path API callers so request serialization is handled once in helper.

---

## Session 4 — Path Onboarding Flows

Read before this session:
docs/game-design/paths/fitness-warrior.md
docs/game-design/paths/mindset-sage.md
docs/game-design/paths/health-alchemist.md
docs/game-design/paths/discipline-knight.md
docs/game-design/paths/grind-visionary.md

- [ ] Step 28: Build Fitness Warrior onboarding —
      4 questions plus split day setup question
      save training split, goal, days per week,
      experience level, split day start
      experience-based quest visibility logic
- [ ] Step 29: Build Mindset Sage onboarding —
      4 questions plus archetype selection
      save motivation, time commitment,
      experience level, archetype
      archetype quest pool filtering logic
      experience-based quest visibility logic
- [ ] Step 30: Build Health Alchemist onboarding —
      4 questions plus equipment multi-select
      save goal, health relationship,
      focus area, equipment profile
      experience-based quest visibility logic
      equipment gating logic for quest pool
- [ ] Step 31: Build Alchemist Setup Guide —
      shown after onboarding before dashboard loads
      supplement cards with two tabs:
      Take It tab and Eat It Instead tab
      equipment cards with budget alternatives
      personalized starter pack based on
      Q1 and Q2 onboarding answers
      legal disclaimer in exactly three places:
      top of guide, bottom of guide,
      one line on each supplement card
- [ ] Step 32: Build Discipline Knight onboarding —
      4 questions
      save routine level, challenge, structure
      preference, time commitment
      experience-based quest visibility logic
- [ ] Step 33: Build Discipline Code Oath Screen —
      shown after onboarding questions
      user writes 3 to 5 personal rules
      example rules shown as inspiration only
      content moderation filter runs server-side
      before saving — if flagged user must rewrite
      after submission show commitment message
      save code to profile
      display on public profile beneath armor
      show briefly every morning on app open
      3 second fade before quest board loads
- [ ] Step 34: Build Grind Visionary onboarding —
      6 questions
      save grind focus (with custom text if Other),
      experience level, singular goal text,
      goal deadline, daily hours, current output
      singular goal displayed on dashboard daily
      goal deadline countdown shown
      experience-based quest visibility logic
- [ ] Step 35: Build skill tree initialization —
      on Grind Visionary onboarding complete
      create SkillTree record for user
      based on grind focus selected
      first node set as active

---

## Session 5 — Daily Quest Assignment Engine

Read before this session:
docs/game-design/systems/daily-quest-logic.md

- [ ] Step 36: Build five-layer assignment algorithm
      as Django management command or Celery task —
      Layer 1: lock universal quests
      Layer 2: hard filters
      Layer 3: weekly rhythm as default
      Layer 4: smart suggestion logic
      Layer 5: fill remaining slots
      Algorithm runs server-side only
- [ ] Step 37: Build timezone-aware midnight
      scheduler — runs at midnight in player
      local timezone not UTC
- [ ] Step 38: Build Day 1 hardcoded starter
      lineup per path — algorithm takes over
      from Day 2
- [ ] Step 39: Build progressive complexity
      reveal logic:
      Day 1-6: 3 quests simple list no slot UI
      Day 7: slot UI unlocks with tutorial
      Day 14: swap feature unlocks
      Day 30: settings customization unlocks
- [ ] Step 40: Build quest expiry logic:
      D rank: carry over once then expire midnight
      C rank: carry over once then expire midnight
      B rank: expire midnight no carry over
      A rank: expire midnight no carry over
      S rank: expire midnight no carry over
      Universal: expire midnight reset fresh
      Weekly boss: expire Sunday 23:59
- [ ] Step 41: Build swap system:
      swap icon on assigned slot quest cards
      opens drawer with up to 6 alternatives
      same rank or one rank below
      excludes quests already in today lineup
      maximum 3 swaps per day per path
      after limit show commitment message
      swaps logged for preference learning
- [ ] Step 42: Build quest feedback thumbs system:
      thumbs up and thumbs down icons
      appear after completing or skipping quest
      fade after 3 seconds if not tapped
      always optional never blocking
      saved to QuestFeedback model immediately
- [ ] Step 43: Build daily intention prompt:
      shown on first app open each day
      before quest board loads
      Full Send: full lineup plus push quest
      Steady: standard lineup unchanged
      Recovery: universal plus D rank only
      max 5 quests on recovery days
      streak not broken on recovery days
      cross-path bonuses exempt from
      recovery day filtering
- [ ] Step 44: Build Fitness Warrior daily
      override logic:
      rest day loads recovery quest set
      push day surfaces chest shoulder tricep first
      pull day surfaces back bicep first
      leg day surfaces squat hinge first
- [ ] Step 45: Build Mindset Sage daily
      override logic:
      Sunday locks weekly review in one slot
      Freedom Day redeemed clears all Sage
      assigned slots shows Freedom Day screen
      Dark Night activation counts as one slot
- [ ] Step 46: Build Health Alchemist daily
      override logic:
      Morning Protocol always fills first slot
      cannot be swapped
      Elixir Day 7 surfaces highest EXP quests
      equipment gated quests never in assigned
      or bonus slots without equipment in profile
- [ ] Step 47: Build Discipline Knight daily
      override logic:
      Sunday Honor Review fills one assigned slot
      Sunday only locked other days with countdown
      War Room planning always fills first slot
      cannot be swapped
      armor cracked surfaces Forge quests majority
- [ ] Step 48: Build Grind Visionary daily
      override logic:
      one day from multiplier upgrade surfaces
      highest EXP quests all assigned slots
      show motivation message on quest board
      Sunday Vision Board review fills one slot
      partner active surfaces accountability
      quest Sunday slot
- [ ] Step 49: Build cross-path bonus detection:
      maximum one cross-path bonus per day
      algorithm picks highest EXP value pair
      flags quests with cross_path_bonus boolean
      gold border on flagged quest cards
      bonus EXP awarded when both complete same day
- [ ] Step 50: Build missed day logic:
      check last active date on login
      apply protections in order:
      Grace Token then Streak Shield then
      Multiplier Protection then Elixir Mercy
      then streak break
      return screen shown 3 seconds full screen
      forward-facing language never shaming
      load fresh lineup no reference to missed

---

## Session 6 — Path-Specific Mechanics

Read before this session the relevant path file
from docs/game-design/paths/

- [ ] Step 51: Build Freedom Day Token system —
      earn token after 7 consecutive days
      max 3 tokens stacked
      overflow awards 200 bonus EXP instead
      token counter visible on dashboard
      as glowing orb icon
      redeem button on dashboard
      on redemption: clear quest board
      show Freedom Day screen
      streak not broken
      badge logged to profile with date
      Wisdom Log still accessible optionally
- [ ] Step 52: Build Wisdom Log —
      optional prompt after Knowledge Forging
      or Mirror Work quest completion
      free text input saved with date
      quest name and level
      private by default individual public option
      milestone notifications 10 25 50 100
      shareable achievement card at milestones
- [ ] Step 53: Build Dark Night Quest —
      always visible subtle button on dashboard
      manual activation only
      minimum 100 words required
      200 EXP on completion
      streak protected
      dark themed completion screen
      entry saved to Wisdom Log as
      Dark Night Entry
      maximum 1 per day
- [ ] Step 54: Build Elixir System —
      elixir bottle visual on dashboard
      fills over 7 consecutive days
      color progression:
      Day 1-2 pale yellow
      Day 3-4 amber
      Day 5-6 deep orange
      Day 7 glowing gold
      Drink Your Elixir button on Day 7
      completion: 300 bonus EXP plus badge
      plus Transmutation counter advance
      mercy mechanic: streak break before Day 7
      bottle retains 50 percent fill
      shown as cracked but not empty
- [ ] Step 55: Build Transmutation milestones —
      1 elixir: Apprentice Alchemist
      2 elixirs: The Brewer
      3 elixirs: Formula Seeker
      4 elixirs: Transmuter
      5 plus elixirs: Grand Alchemist
      each triggers achievement card
      plus badge plus animation
- [ ] Step 56: Build Body Journal —
      optional prompt after Restoration Chamber
      or Transmission Protocol quest
      four 1-5 sliders:
      energy digestion mood sleep
      saved with date quest name level
      private by default
      trend lines shown over time
      milestones 7 30 90 entries
      preserved permanently regardless of
      path activation status
- [ ] Step 57: Build Armor System —
      6 piece armor progression:
      Week 1: Boots
      Week 2: Gauntlets
      Week 3: Chest Plate
      Week 4: Shoulder Guards
      Week 5: Helmet
      Week 6: Shield and Sword
      forging animation per piece
      fully public on profile and leaderboard
- [ ] Step 58: Build Armor crack mechanic —
      streak break before week complete
      most recent piece shows visible crack
      on public profile
      repair requires 3 consecutive days
      crack disappears on repair
- [ ] Step 59: Build Grace Token mechanic —
      one token per armor piece per calendar month
      resets first day of each month
      one missed day with unused token
      armor holds token consumed
      two missed days in a row cracks armor
      regardless of token
- [ ] Step 60: Build Streak Shield mechanic —
      earned after 14 consecutive days
      auto-activates on missed day after
      Grace Token already used
      one time use
      re-earn after 7 more consecutive days
      shield icon visible on dashboard when active
- [ ] Step 61: Build full armor milestone —
      all 6 pieces forged triggers:
      full screen animation
      title: The Fully Forged Knight
      500 bonus EXP
      achievement card generated
- [ ] Step 62: Build armor prestige —
      full armor maintained 6 more weeks
      armor color shifts silver to gold visually
      title upgrades to The Golden Knight
- [ ] Step 63: Build War Room planning tool —
      dedicated tab on dashboard
      morning: set top 3 priorities
      optional time blocks
      35 EXP for completing morning planning
      evening: mark priorities completed
      35 EXP for completing evening review
      both same day plus 20 EXP bonus
      War Room data stored for weekly report
- [ ] Step 64: Build Temptation Log —
      optional prompt after Iron Will quest
      what was the temptation
      did you resist yes partially no
      how did it feel optional free text
      private to user
      30 logged resistances milestone
      triggers Iron Will badge plus
      achievement card
- [ ] Step 65: Build Knight Weekly Report —
      auto-generated every Sunday
      delivered as notification
      viewable in profile history
      contains:
      quests completed vs available
      armor status and cracks
      Discipline Code honor rating
      top performing pillar
      weakest pillar
      War Room completion rate
      one personalized improvement suggestion
      streak and shield status
- [ ] Step 66: Build XP Multiplier system —
      Day 1-6: 1.0x The Dreamer
      Day 7-13: 1.25x The Builder
      Day 14-20: 1.5x The Grinder
      Day 21-29: 1.75x The Visionary
      Day 30 plus: 2.0x The Realized
      all EXP multiplied by current tier
      server-side calculation only
      multiplier shown on dashboard
      countdown bar to next tier
      one day before upgrade notification
      streak break resets to 1.0x
      personal best saved to profile
- [ ] Step 67: Build Multiplier Protection —
      earned after 14 consecutive days
      one missed day does not reset multiplier
      re-earn after 7 more consecutive days
      protection icon on dashboard when active
- [ ] Step 68: Build Vision Board —
      composite view on dashboard:
      singular goal text
      deadline countdown days remaining
      current multiplier and streak
      progress bar to next multiplier tier
      last 3 Output Log entries
      current skill tree node and next unlock
      grind focus field label
- [ ] Step 69: Build Skill Tree —
      visual tree per grind focus
      7 focus areas with defined nodes
      node unlocks based on cumulative
      Mastery Lab quest completions
      unlock triggers animation and notification
      displayed on Vision Board and
      as dedicated tab
- [ ] Step 70: Build Output Log —
      optional prompt after Workshop
      or Empire quest completion
      fields: description free text
      optional URL
      auto-filled date and quest linked
      private by default individual public option
      milestones 10 25 50 100 outputs
      each milestone badge plus achievement card
- [ ] Step 71: Build Accountability Partner system —
      invite one other Discipline System user
      both must accept
      maximum one active partner
      partners see each other:
      multiplier streak public output log
      weekly completion rate
      vision board goal if user sets visible
      partner notifications on quest complete
      level up multiplier upgrade streak events
      partnership 30 day milestone both active
      both receive badge and achievement card
- [ ] Step 72: Build First Dollar legendary moment —
      quest completion triggers:
      full screen gold explosion animation
      specific message copy
      badge: First Blood First Dollar Earned
      achievement card auto-generated
      200 EXP with multiplier applied
      quest permanently displayed on public profile
      this must be most dramatic completion
      animation in the entire app
- [ ] Step 73: Build Post-First-Dollar quest chain —
      auto-unlocks after First Dollar completion:
      Quest 1: Generate first 10 dollars 250 EXP
      Quest 2: Generate first 100 dollars 400 EXP
      Quest 3: First consistent monthly income
      600 EXP
      each unlocks only after previous complete

---

## Session 7 — Frontend Quest Experience

Read before this session:
docs/game-design/systems/daily-quest-logic.md

- [ ] Step 74: Build quest board with
      progressive slot UI —
      Day 1-6: simple list 3 quests
      Day 7 plus: slot UI with labels
      Universal slot locked no swap icon
      Assigned slot swappable with swap icon
      Bonus slot open player choice
      Carry over quests shown amber warning color
- [ ] Step 75: Build completion ring component —
      single SVG or Canvas ring on dashboard
      divided into colored arc segments
      one segment per active path
      colors:
      Fitness Warrior red
      Mindset Sage purple
      Health Alchemist green
      Discipline Knight blue
      Grind Visionary gold
      ring border states:
      0-33 percent red
      34-66 percent amber
      67-99 percent blue
      100 percent gold with pulse animation
      center shows completed of total
      tap segment opens that path quest list
      tap center opens combined quest view
      updates in real time no page refresh
- [ ] Step 76: Build end of day summary screen —
      triggers at 9PM local time
      if all complete before 6PM show
      mid-day message first then full at 9PM
      delay if actively completing quest
      full screen dark overlay animated reveal
      contains:
      day number date username streak
      quests completed of total
      EXP earned today per path breakdown
      total EXP toward next level progress bar
      highlight section one of nine priorities
      tomorrow preview categories only
      three buttons:
      Share Today Summary
      See Tomorrow Preview
      Close
- [ ] Step 77: Build tomorrow preview —
      categories only never specific quest titles
      available from end of day summary
      and from settings
      read only cannot complete early
- [ ] Step 78: Build missed day return screen —
      full screen 3 seconds
      forward-facing language only
      never shame the player
      load fresh lineup after dismissal
      no reference to missed quests anywhere
- [ ] Step 79: Build adaptive difficulty nudge —
      if all daily quests completed
      7 consecutive days
      Day 8 trigger:
      message and two options
      Yes upgrade my quests
      Not yet keep current
      if yes surface harder quests

---

## Session 8 — Social and Achievement Features

Read before this session:
docs/game-design/systems/path-discovery.md
docs/game-design/README.md cross-path section

- [ ] Step 80: Build achievement card generation —
      auto-generated shareable image cards
      triggered by defined milestone events
      card contains: username level achievement
      date app branding
      user can download as image for Instagram
      user can post to in-app public profile
- [ ] Step 81: Build badge system —
      all path-specific badges defined
      badge awarded on milestone completion
      badges visible on public profile
      badge collection viewable by other players
- [ ] Step 82: Build weekly EXP leaderboard
      per path —
      resets Monday 00:00
      shows top 10 globally plus user own rank
- [ ] Step 83: Build global cross-path
      EXP leaderboard —
      combined EXP across all active paths
      with multiplier applied for Visionary
- [ ] Step 84: Build armor leaderboard (Knight) —
      permanent all-time
      shows most armor pieces forged globally
      armor color shown (silver or gold prestige)
- [ ] Step 85: Build multiplier streak leaderboard
      (Visionary) —
      current active multiplier streak
      resets if multiplier breaks
- [ ] Step 86: Build cross-path identity titles —
      Warrior-Sage
      The Optimized Human
      The Complete Human
      The Renaissance Human
      titles displayed on public profile
      achievement card generated on unlock
      Renaissance Human gets dedicated
      leaderboard tier globally
- [ ] Step 87: Build public profile enhancements —
      armor visualization (Knight)
      Discipline Code display (Knight)
      multiplier and streak (Visionary)
      singular goal if user sets visible (Visionary)
      Wisdom Log entry count (Sage)
      Elixir progress visualization (Alchemist)
      skill tree current node (Visionary)
      output log public entries (Visionary)
- [ ] Step 88: Build weekly boss quest system —
      appears every Monday reset Monday 00:00
      one boss quest per path
      rotating examples per path as defined
      completion awards EXP plus exclusive badge
      Visionary boss quest EXP has
      multiplier applied

---

## Session 9 — Final Verification

- [ ] Step 89: Full end-to-end flow tested —
      new user signup through path discovery
      through onboarding through first week
      of daily quests
- [ ] Step 90: Existing user account flow tested —
      existing user logs in
      gets redirected to path discovery quiz
      completes re-onboarding
      account data intact
      social data intact
- [ ] Step 91: All existing social features
      verified still working —
      posts comments reactions friends groups
- [ ] Step 92: All five path onboarding flows
      tested end to end
- [ ] Step 93: Daily quest assignment engine
      tested for all five paths
- [ ] Step 94: All path-specific mechanics
      tested:
      Freedom Day Token
      Wisdom Log
      Dark Night Quest
      Elixir System
      Body Journal
      Armor System with crack and repair
      Grace Token
      Streak Shield
      War Room
      Weekly Report
      XP Multiplier
      Vision Board
      Skill Tree
      Output Log
      Accountability Partner
      First Dollar moment
- [ ] Step 95: Cross-path bonus system tested —
      all five bonus pairs trigger correctly
      maximum one per day enforced
      recovery day exemption confirmed
- [ ] Step 96: Cross-path identity titles tested —
      all four titles unlock correctly
- [ ] Step 97: Leaderboards tested —
      all leaderboards populate correctly
      weekly reset verified
- [ ] Step 98: Achievement cards tested —
      generate correctly for all trigger events
- [ ] Step 99: No broken migrations confirmed
- [ ] Step 100: All new code follows service
       layer pattern confirmed
- [ ] Step 101: All EXP logic confirmed
       server-side only
- [ ] Step 102: Timezone logic confirmed —
       midnight reset uses player local timezone
- [ ] Step 103: Quest model pack_id field
       confirmed present for future expansion
- [ ] Step 104: Sixth path placeholder
       confirmed non-functional
- [ ] Step 105: BUILD_ORDER.md fully checked off —
       Phase 5B complete

---

## Notes and Decisions Log

Add implementation notes, conflict resolutions,
and developer decisions here as you go.
Date each note.

Format:
[DATE] — [NOTE]

---
