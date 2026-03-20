# Discipline System
## Web Development Roadmap

This document describes the development roadmap for the **Discipline System web platform**.

The goal of the platform is to build a **Solo Leveling–inspired real-life RPG progression system** where players level up through discipline, fitness, and personal development.

Mobile applications (iOS and Android) will only begin **after the full web platform is stable and feature complete**.

---

# Phase 1 — Foundation Infrastructure (Completed)

## Purpose
Build the technical base of the project.

## Features

- Django backend setup
- Django REST Framework
- project folder structure
- Docker environment
- database configuration
- Git repository
- environment variables
- initial API structure

## Result

The backend infrastructure is ready.

---

# Phase 2 — Identity System (Completed)

## Purpose
Create the player account system.

## Features

- signup
- login
- authentication
- password management
- unique Player ID
- account settings basics
- `/me` endpoint
- protected API endpoints

## Result

Players can create accounts and log into the platform.

---

# Phase 3 — Player & Quest Core System (Completed)

## Purpose
Implement the core gameplay loop.

## Features

- player profile
- player stats
- EXP system
- level progression
- streak system
- quest model
- quest completion
- completion history
- EXP rewards
- quest API endpoints

## Core Loop


Player logs in
→ sees quests
→ completes quest
→ gains EXP
→ levels up
→ streak increases


This is the **foundation of the platform**.

---

# Phase 4 — Frontend Foundation

## Purpose
Build the first usable UI for the platform.

## Features

### Authentication Pages

- login page
- signup page

### Player Onboarding

Players select their discipline path:

- Runner
- Gym
- Discipline
- Tournament
- 75 Hard

### Player Dashboard

Dashboard shows:

- avatar
- player level
- EXP progress bar
- streak
- daily quests
- quest history

### Basic Profile Page

Displays:

- Player ID
- avatar
- basic stats

---

# Phase 5 — Quest Expansion System

## Purpose
Improve and expand the quest engine.

## Features

- quest categories
- path-based quests
- dynamic daily quests
- recurring quests
- difficulty levels
- reward scaling
- improved streak logic
- quest analytics

## Example Quest Types

- fitness
- discipline
- productivity
- hydration
- recovery

---

# Phase 6 — Social Platform

## Purpose
Build the community layer.

## Features

### Friend System

- friend requests
- friends list

### Player Profiles

- public profile page
- activity feed

### Social Posts

Players can post:

- quest completions
- achievements
- updates

### Interactions

- comments
- reactions

### Groups

- group creation
- group membership
- group activity feed

---

# Phase 7 — Reward Engine & Achievements

## Purpose
Introduce a structured reward system to control how EXP is earned across the platform.

## Features

### Reward Engine


Event triggered
→ Reward Engine evaluates rules
→ EXP granted to player


### EXP Distribution

- daily quests → high EXP
- hard quests → higher EXP
- group quests → bonus EXP
- social actions → small, controlled EXP
- achievements → large EXP rewards

### Social EXP Rules

- likes → limited EXP
- comments → higher EXP
- unique users only
- no self-reward
- cap per post
- cap per day

### First Action Rewards

- first post → bonus EXP
- first comment → bonus EXP
- first friend → bonus EXP

### Group Rewards

- group quest → bonus EXP
- group participation → bonus EXP

### Achievement System

Categories:
- common
- rare
- epic
- legendary

Examples:
- 7-day streak
- 30-day streak
- 100 quests completed
- first post

### Tips System

- guide players
- show one tip at a time
- adapt to player behavior

---

# Phase 8 — Competitive Systems

## Purpose
Introduce competition.

## Features

### Leaderboards

- global leaderboard
- path leaderboard
- group leaderboard

### Challenges

- running challenges
- workout challenges
- streak challenges
- weekly EXP challenges

### Tournaments

- platform-run competitions

---

# Phase 9 — Privacy & Settings System

## Purpose
Give players control over their data.

## Features

### Profile Visibility

- public
- friends only
- private

### Lock System

- avatar
- streak
- quests
- posts
- stats

### Settings

- Player ID
- password
- avatar
- privacy settings

---

# Phase 10 — Avatar System

## Purpose
Create player identity.

## Features

- avatar generation
- upload photo/video
- multiple avatars
- avatar switching
- leaderboard display

---

# Phase 11 — Device Integration

## Purpose
Connect real-world activity.

## Features

- smartwatch integration
- step tracking
- run tracking
- workout tracking

Example:


Smartwatch run detected
→ quest completed


---

# Phase 12 — Subscription System

## Purpose
Monetization.

## Features

### Free Trial
- 1 month free

### Plans
- monthly
- 6-month
- yearly

### Premium Unlocks
- advanced quests
- leaderboards
- competitions
- enhanced features

---

# Phase 13 — Merchandising System

## Purpose
Expand ecosystem.

## Features

- shop
- branded products
- custom merchandise (Player ID, QR)

---

# Phase 14 — Immersive Experience Layer

## Purpose
Solo Leveling UI.

## Features

- animations
- system messages
- level-up effects
- cinematic UI

---

# Phase 15 — Platform Stabilization

## Purpose
Prepare for scale.

## Features

- performance optimization
- bug fixes
- security
- analytics
- infrastructure

---

# Phase 16 — Mobile App Development

## Platforms

- iOS
- Android

Uses same backend API.

---

# Vision Summary

A real-life RPG ecosystem combining:

- discipline
- fitness
- social interaction
- competition
- gamification
- real-world data
- immersive experience