
README.md

```md
# Discipline System

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

---

## Product direction

The current product direction is:

- **web app first**
- mobile apps later
- strong core loop first
- social / competition / premium ecosystem later
- immersive Solo Leveling-style experience later

The system is intended to grow over time into a larger platform that may include:

- player paths such as Gym, Runner, Discipline, Tournament, and 75 Hard
- richer quest systems
- social/community features
- leaderboards and challenges
- privacy controls
- avatar identity
- subscription plans
- merch ecosystem
- smartwatch / device integration
- immersive UI effects

Not all of these are immediate implementation targets. The product is built in phases.

---

## Tech stack

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL (target primary DB for ongoing phases)
- JWT authentication

### Frontend

- React
- Vite
- Tailwind CSS

### Dev tools

- GitHub
- Docker
- Docker Compose

---

## Repository structure

```text
discipline-system/
  backend/
    config/
    core/
    players/
    quests/
    users/
    manage.py
    requirements.txt
    Dockerfile
    .env
    db.sqlite3
  frontend/
    src/
    public/
    package.json
    Dockerfile
  docs/
    phase-0-setup.md
  docker-compose.yml
  README.md