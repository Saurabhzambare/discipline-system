
# Architecture

## Purpose of this document

This document explains the intended architecture direction of **Discipline System**.

Its job is to keep future development clean and consistent by clarifying:

- what the system is
- how the current backend is organized
- which app should own which responsibilities
- where business logic should live
- how roadmap phases relate to system boundaries
- where engagement mechanics fit
- how future expansion should happen without premature refactoring

This document is especially important for:

- future contributors
- AI coding agents
- phase-based implementation work

---

# 1. System overview

Discipline System is a Solo Leveling–inspired discipline web app that turns real-life actions into progression.

Core loop:

- user acts as a **player**
- daily actions become **quests**
- completed quests award **EXP**
- EXP contributes to **level progression**
- consistency contributes to **streak growth**
- dashboard acts as a **status window**

Long-term product direction:

- gamified self-improvement platform
- community and competition features
- premium ecosystem
- device-connected activity
- immersive UI
- mobile apps only after the web platform is complete and stable

---

# 2. Current architecture philosophy

The current architecture philosophy is:

- keep the codebase understandable
- keep app boundaries clear
- avoid large refactors unless there is a real need
- use services for non-trivial business logic
- keep future scaling in mind without forcing it too early
- preserve the current structure unless a real problem is found
- build the web app first, then mobile later

Important current decision:

**We are not doing a major backend structural refactor right now.**

That means:

- the current app structure should be respected
- new features should be added cleanly within existing boundaries where possible
- a new app should only be introduced when the domain clearly justifies it
- features should be phased according to roadmap priority

---

# 3. Current backend structure

Current backend structure:

```text
backend/
  config/
  core/
  players/
  quests/
  users/