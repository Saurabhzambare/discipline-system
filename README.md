# Discipline System

[![Backend Tests](https://github.com/Saurabhzambare/discipline-system/actions/workflows/backend-tests.yml/badge.svg)](https://github.com/Saurabhzambare/discipline-system/actions/workflows/backend-tests.yml)
[![Frontend Checks](https://github.com/Saurabhzambare/discipline-system/actions/workflows/frontend-checks.yml/badge.svg)](https://github.com/Saurabhzambare/discipline-system/actions/workflows/frontend-checks.yml)

An independent full-stack web app for people who want to track daily habits, workouts, or study sessions and see their progress over time. It uses a Solo Leveling–inspired quest system to turn completed activities into experience points (EXP), levels, and streaks.

## How it works

After signing in, a player opens their dashboard, completes a quest, and sees the recorded progress. The app also supports path discovery and onboarding, daily quest lineups, achievements, and leaderboards.

### Quest completion and daily boundaries

A repeated submission should leave the player's progress consistent. If the same quest completion is submitted again, the system returns a successful response with no additional EXP and keeps a single completion record. Daily lineup generation uses the player's local date so the next lineup appears at local midnight.

The [edge-case tests](backend/quests/tests_phase5b_edge_cases.py) exercise sequential duplicate submissions, local-midnight generation, and a daylight-saving transition. The [architecture guide](docs/architecture.md) describes where the quest and player logic lives.

See the [current status](docs/CURRENT_STATUS.md) for implemented scope and the [quick start](#quick-start) to run the app locally.

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

Replace the example environment values locally before running the application, including a long, random `SECRET_KEY`. The backend example uses `DB_HOST=localhost` for commands run directly on the host machine. Docker Compose overrides that value with `DB_HOST=db`, which is the PostgreSQL service name inside the Compose network. Never commit populated `.env` files or local SQLite databases.

---

## For contributors and AI coding agents

Read these in order before making changes:

1. `AGENTS.md` — coding rules and patterns
2. `docs/architecture.md` — architecture philosophy
3. `docs/CURRENT_STATUS.md` — live status dashboard
4. `docs/phase-5b-quest-system-redesign.md` — active phase scope
5. `docs/game-design/BUILD_ORDER.md` — step-level task tracker
6. Specific path or system spec only when working on it
