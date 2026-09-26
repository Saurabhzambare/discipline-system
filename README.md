# Discipline System

[![Backend Tests](https://github.com/Saurabhzambare/discipline-system/actions/workflows/backend-tests.yml/badge.svg)](https://github.com/Saurabhzambare/discipline-system/actions/workflows/backend-tests.yml)
[![Frontend Checks](https://github.com/Saurabhzambare/discipline-system/actions/workflows/frontend-checks.yml/badge.svg)](https://github.com/Saurabhzambare/discipline-system/actions/workflows/frontend-checks.yml)

A Solo Leveling–inspired discipline web app where real-life habits become quests and are converted into progression through EXP, levels, and streaks.

## What this app is

Discipline System is a gamified self-improvement web application.

It turns daily habits, workouts, study tasks, and other disciplined actions into a gameplay loop:

- **User = Player**
- **Habits / workouts / study tasks = Quests**
- **Completing quests = EXP gain**
- **EXP gain = Level progression**
- **Consistency = Streak growth**
- **Dashboard = Status window**

The goal is to make self-improvement feel like an RPG progression system.

## One-line definition

**A real-life RPG-style discipline app where daily habits are turned into quests and converted into progression through EXP, levels, and streaks.**

---

## Core gameplay loop

1. User signs up or logs in
2. User views their dashboard and available quests
3. User completes a quest
4. System awards EXP
5. System updates level progression
6. System updates streak data where appropriate
7. User sees measurable growth over time

This project is being built in clear phases so the system stays maintainable and beginner-friendly while remaining extensible for future growth.

See `docs/CURRENT_STATUS.md` for up-to-date phase and session status.

---

## Product direction

The current product direction is:

- **web app first**
- mobile apps later
- strong core loop first
- social / competition / premium ecosystem later
- immersive Solo Leveling-style experience later

The system grows in phases toward a larger platform including:

- five identity-based player paths (see below)
- richer quest systems
- social/community features (already present: friends, feed, groups)
- leaderboards and challenges
- privacy controls
- avatar identity
- subscription plans
- merch ecosystem
- smartwatch / device integration
- immersive UI effects

Not all of these are immediate implementation targets. The product is built in phases.

---

## The Five Paths

Phase 5B introduced the five-path identity system. Players take a
9-question discovery quiz and commit to one primary path. Additional
paths unlock after 30 consecutive days.

- **Fitness Warrior** — body as weapon. Strength, hybrid training, PPL rotation.
- **Mindset Sage** — mind as temple. Meditation, journaling, stoic practice, Freedom Day tokens.
- **Health Alchemist** — body as laboratory. Nutrition, sleep, cold therapy, Elixir System.
- **Discipline Knight** — self as kingdom. Oath-driven discipline, Armor System, War Room planning.
- **Grind Visionary** — life as mission. Singular goal, XP Multiplier, Skill Tree, Output Log, Accountability Partner.

The old placeholder paths (Runner, Gym, Discipline, Tournament, 75 Hard)
have been fully replaced.

---

## Tech stack

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL application database / SQLite test database
- JWT authentication

### Frontend

- React 19
- Vite
- Tailwind CSS

### Dev tools

- GitHub
- Docker
- Docker Compose
- Railway (deployment target)

---

## Repository structure

```text
discipline-system/
  backend/
    config/
    core/
    users/
    players/
    quests/
    paths/
    social/
    manage.py
    requirements.txt
    Dockerfile
    .env.example
  frontend/
    src/
      pages/
      components/
      App.jsx
      api.js
    public/
    package.json
    Dockerfile
    .env.example
  docs/
    CURRENT_STATUS.md
    AGENTS.md
    architecture.md
    phase-5b-quest-system-redesign.md
    web-development-roadmap.md
    game-design/
      README.md
      BUILD_ORDER.md
      paths/
      systems/
    templates/
    archive/
  docker-compose.yml
  README.md
```

---

## Quick start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_quests
python manage.py runserver

# Frontend
cd frontend
npm install
cp .env.example .env
npm run dev
```

Replace the example environment values locally before running the application. Never commit populated `.env` files or local SQLite databases.

---

## For contributors and AI coding agents

Read these in order before making changes:

1. `AGENTS.md` — coding rules and patterns
2. `docs/architecture.md` — architecture philosophy
3. `docs/CURRENT_STATUS.md` — live status dashboard
4. `docs/phase-5b-quest-system-redesign.md` — active phase scope
5. `docs/game-design/BUILD_ORDER.md` — step-level task tracker
6. Specific path or system spec only when working on it
