# Phase 6 — Social Platform

## Phase Goal

Build the first community layer of the Discipline System.

Until Phase 5, the app is primarily a personal progression system:
- player account
- quests
- EXP
- level
- streak
- dashboard

Phase 6 introduces social features so players can:
- connect with other players
- view public profiles
- share activity
- post updates
- react and comment
- participate in groups

This phase is the foundation for the Discipline System to evolve from a solo productivity app into a multiplayer accountability and motivation platform.

---

## Why This Phase Matters

A discipline app becomes much more powerful when progress is visible and shared.

Social systems improve:
- accountability
- motivation
- retention
- community feeling
- long-term engagement

This phase should be built in a way that is simple now, but expandable later.

Future features that may depend on this phase:
- notifications
- achievements showcase
- follow system
- leaderboards
- boss raids / team challenges
- private messaging
- group moderation
- content reporting
- social discovery
- premium communities

---

## Scope of Phase 6

This phase includes the following systems:

### 1. Friend System
- send friend request
- accept friend request
- decline friend request
- cancel outgoing friend request
- remove friend
- list current friends
- list incoming/outgoing friend requests

### 2. Player Profiles
- public profile endpoint/page
- show player identity and progression summary
- show selected public activity
- support profile lookup by username or player id

### 3. Activity Feed
- store social activity events
- display recent public activity on player profiles
- optionally display a home/social feed for friend activity

### 4. Social Posts
Players can create posts for:
- quest completions
- achievements
- general updates

Posts should support:
- author
- text content
- optional post type
- visibility rules kept simple for now

### 5. Interactions
- reactions on posts
- comments on posts

### 6. Groups
- create group
- join group
- leave group
- group membership list
- group activity feed

---

## High-Level Product Design

This phase introduces a new concept:

> A player is no longer only a private game entity.  
> A player is now also a social entity.

That means we need a clean separation between:
- progression logic
- quest logic
- social logic

Social features should not be deeply mixed into quest services or player progression code.

Instead, we should create a dedicated social domain.

---

## Recommended App Structure

Create a new Django app:

`backend/social/`

This app should own:
- friend relationships
- friend requests
- social posts
- comments
- reactions
- activity feed events
- groups
- group memberships

This keeps Phase 6 isolated and easier to maintain.

---

## ELI5 — What We Are Building

Think of the app like a game.

Before Phase 6:
- you level up alone
- you complete quests alone
- only you see your progress

After Phase 6:
- you can add other players as friends
- people can visit your profile
- your progress can appear as activity
- you can post updates
- people can react and comment
- players can join groups and see shared activity

So Phase 6 is basically turning the app from:

**“my personal tracker”**

into

**“a shared world with other players.”**

---

## Architecture Principles for This Phase

1. Keep the social app separate from players and quests.
2. Reuse the existing Player model as the social identity anchor.
3. Use service-layer logic for actions with rules:
   - send friend request
   - accept friend request
   - create activity event
   - create group membership
4. Keep APIs explicit and predictable.
5. Start simple with privacy:
   - profiles public by default
   - posts public to friends/public depending on simple design choice
6. Build with future extensibility in mind:
   - notifications later
   - moderation later
   - richer feeds later

---

## Data Model Design

## 1. Friend Request

Purpose:
Track pending friend relationships between two players.

Suggested fields:
- id
- from_player (FK to Player)
- to_player (FK to Player)
- status
  - pending
  - accepted
  - declined
  - cancelled
- created_at
- responded_at

Rules:
- cannot send request to self
- cannot duplicate pending request
- cannot send request if already friends
- if reverse pending request exists, either reject or auto-resolve based on service logic
- accepted request should create a friendship relation

---

## 2. Friendship

Purpose:
Represent an active friendship between two players.

Suggested fields:
- id
- player_one (FK to Player)
- player_two (FK to Player)
- created_at

Rules:
- one friendship per pair
- enforce normalized ordering internally if helpful
- friendship should be symmetric in behavior even if stored once

Example:
If A and B are friends, querying either player should show the other.

---

## 3. Social Post

Purpose:
Store user-created social content.

Suggested fields:
- id
- author (FK to Player)
- post_type
  - update
  - quest_completion
  - achievement
- content
- related_quest_completion (optional FK if later needed)
- related_achievement_key (optional future-safe field)
- created_at
- updated_at
- is_edited
- visibility
  - public
  - friends_only
  - group_only (optional, maybe later)
- group (nullable FK if group post support is included now)

Rules:
- content required for update posts
- system-generated quest completion posts may allow templated content
- keep file uploads/media out of scope for this phase unless explicitly planned

---

## 4. Post Comment

Purpose:
Allow players to comment on posts.

Suggested fields:
- id
- post (FK to SocialPost)
- author (FK to Player)
- content
- created_at
- updated_at
- is_edited

Rules:
- comments belong to one post
- soft delete can be future work
- for now hard delete or no delete support is acceptable depending on implementation scope

---

## 5. Post Reaction

Purpose:
Allow players to react to posts.

Suggested fields:
- id
- post (FK to SocialPost)
- player (FK to Player)
- reaction_type
  - like
  - fire
  - respect
  - clap
  - etc. (start small)
- created_at

Rules:
- one reaction per player per post
- if same player reacts again, either update the reaction or reject duplicate depending on API design
- keep this simple and deterministic

---

## 6. Activity Event

Purpose:
Create a feed-friendly record of important events.

Suggested fields:
- id
- actor (FK to Player)
- event_type
  - quest_completed
  - achievement_unlocked
  - post_created
  - friend_added
  - joined_group
- text_snapshot
- related_post (nullable FK)
- related_player (nullable FK)
- related_group (nullable FK)
- created_at
- is_public

Why this model matters:
This gives us a flexible feed system without over-coupling feed rendering to many different tables.

This is very important for future scalability.

---

## 7. Group

Purpose:
Allow communities within the platform.

Suggested fields:
- id
- name
- slug
- description
- owner (FK to Player)
- created_at
- updated_at
- is_private

Rules:
- group name should be unique enough for user clarity
- slug should be unique
- owner is initial admin/creator
- deeper role system can come later

---

## 8. Group Membership

Purpose:
Connect players to groups.

Suggested fields:
- id
- group (FK to Group)
- player (FK to Player)
- role
  - owner
  - member
- joined_at

Rules:
- one membership per player/group pair
- owner should automatically be a member
- leaving/deleting owner logic can be kept simple for now

---

## Suggested API Surface

These endpoint names are suggestions. Exact routing can follow your current project style.

---

## Friend System APIs

### Send friend request
`POST /api/social/friends/requests/`

Request:
```json
{
  "to_player_id": 12
}