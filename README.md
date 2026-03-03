# SOLO LEVELING – DISCIPLINE SYSTEM

# Phase 1 – PostgreSQL + Docker Networking + Environment Setup

---

# 1️⃣ What Was the Goal of Phase 1?

The goal of Phase 1 was:

* Replace SQLite with PostgreSQL
* Run PostgreSQL inside Docker
* Connect Django backend to Postgres
* Understand Docker architecture
* Understand virtual environments properly
* Fix configuration errors correctly
* Build a clean SaaS-ready backend foundation

---

# 2️⃣ Our Initial Architecture Confusion

At the beginning, we had confusion about how Django was running.

There were two possible setups:

---

## Option A

Django runs locally (venv + manage.py)
Postgres runs in Docker

Django connects using:

```
DB_HOST=127.0.0.1
```

---

## Option B

Django runs inside Docker
Postgres runs inside Docker

Django connects using:

```
DB_HOST=db
```

(where `db` is the Docker service name)

---

## What Actually Happened

From your Docker Desktop screenshot, we discovered:

* Django backend was already running inside Docker
* So we were actually in Option B
* There was no Postgres container yet

So we locked:

✅ Full Docker architecture (backend + db)

---

# 3️⃣ Understanding Docker in This Project

Docker is used to isolate:

* Python runtime
* Django
* Postgres
* Frontend
* All dependencies

Think of Docker as:

> A fully isolated apartment for your app.

Instead of installing Postgres locally,
we run:

```
postgres:16
```

inside a container.

---

# 4️⃣ Adding PostgreSQL to docker-compose.yml

We added this service:

```yaml
db:
  image: postgres:16
  container_name: discipline_db
  environment:
    POSTGRES_DB: discipline_db
    POSTGRES_USER: discipline_user
    POSTGRES_PASSWORD: discipline_password
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

And at bottom:

```yaml
volumes:
  postgres_data:
```

---

# 5️⃣ First Major Error: YAML Structure Error

### Error Message:

```
services.volumes additional properties 'postgres_data' not allowed
```

---

## What Happened?

We accidentally placed:

```
volumes:
  postgres_data:
```

inside the `services:` block.

Docker expected a service name, but saw `volumes`.

---

## Why It Happened

YAML is indentation-sensitive.

In Docker Compose:

* `services:` is top-level
* `volumes:` must also be top-level
* You cannot nest named volumes under services

---

## Fix

Move this:

```yaml
volumes:
  postgres_data:
```

to the bottom of the file (aligned left).

After fix:

```
docker compose down
docker compose up --build -d
```

---

# 6️⃣ Database Networking Inside Docker

Very important concept.

Inside Docker:

Containers talk using service names.

So:

```
DB_HOST=db
```

NOT:

```
DB_HOST=127.0.0.1
```

Because:

* 127.0.0.1 = inside the container itself
* db = other container on Docker network

---

# 7️⃣ Creating .env File

We created:

```
backend/.env
```

Containing:

```
DB_NAME=discipline_db
DB_USER=discipline_user
DB_PASSWORD=discipline_password
DB_HOST=db
DB_PORT=5432
```

Why use .env?

* Do not hardcode secrets
* Easier environment switching
* Clean configuration separation

---

# 8️⃣ Installing Required Packages

Inside requirements.txt:

```
python-dotenv
psycopg2-binary
```

Why?

* psycopg2-binary → allows Django to talk to Postgres
* python-dotenv → loads environment variables from .env

Then rebuild:

```
docker compose down
docker compose up --build -d
```

---

# 9️⃣ Updating settings.py Correctly

Correct top of settings.py:

```python
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
```

Important:

* Only ONE BASE_DIR
* Do not duplicate it
* load_dotenv comes after BASE_DIR

Then replace DATABASES section with:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}
```

---

# 🔟 Running Migrations Inside Docker

Because backend runs inside container, we must run:

```
docker compose exec backend python manage.py migrate
```

NOT local manage.py.

This is critical.

---

# 1️⃣1️⃣ VS Code Dotenv Error

Error:

```
Import "dotenv" could not be resolved
```

---

## What Happened?

VS Code was using global Python interpreter,
not backend/venv interpreter.

So Pylance could not see installed packages.

---

## Fix

Select interpreter:

```
backend/venv/Scripts/python.exe
```

NOT:

* pythonw.exe
* pip.exe

After selecting:

* Restart VS Code
* Error disappears

---

# 1️⃣2️⃣ Understanding Virtual Environment vs Docker

Very important concept.

Virtual Environment isolates:

* Python packages only

Docker isolates:

* OS
* Python
* Dependencies
* Network
* Services

Right now:

Docker container = runtime environment
Local venv = development support for VS Code

---

# 1️⃣3️⃣ Final Working Architecture

```
Docker Desktop
│
├── backend (Django)
├── db (Postgres)
└── frontend (React)
```

Backend connects to db using:

```
DB_HOST=db
```

Port mapping:

```
8000 → backend
5432 → Postgres
5173 → frontend
```

---

# 1️⃣4️⃣ Key Engineering Lessons Learned

1. YAML indentation matters.
2. Docker networking uses service names.
3. 127.0.0.1 means different things inside containers.
4. Migrations must run inside the container.
5. VS Code interpreter must match project environment.
6. Never duplicate BASE_DIR in Django settings.
7. Always rebuild Docker after changing requirements.
8. Separate configuration using .env.
9. Docker volumes persist database data.
10. Infrastructure debugging requires understanding layers.

---

# 1️⃣5️⃣ Why This Setup Is Professional

This setup is SaaS-ready because:

* Uses PostgreSQL (production database)
* Uses environment variables
* Uses containerization
* Uses dependency isolation
* Clean separation of services
* Reproducible stack
* Easy future deployment

---

# 1️⃣6️⃣ What Phase 1 Achieved

By the end of this stage:

* PostgreSQL is running inside Docker
* Django connects successfully
* Migrations run without errors
* Environment is clean
* Infrastructure is stable
* Errors were debugged properly
* Architecture is clear

---

# 🎯 Final Status

Infrastructure Phase 1: ✅ COMPLETE

Next Phase:
Create `players` app and build the Player model.

