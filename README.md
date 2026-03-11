# DISCIPLINE SYSTEM — FULL PROJECT GUIDE (PRINT VERSION)

## What this project is

This project is a **Solo Leveling–style “System” for fitness and discipline**, built as a **full-stack web application**.

* You (and later other users) are “players”
* Daily habits/workouts are “quests”
* Completing quests gives **EXP**
* EXP increases **Level**
* Missing quests triggers **penalties**
* Over time the app builds discipline through structure + consequences

This guide is written so that even a **first-year student** can follow it to rebuild the project.

---

# SECTION 1 — TECHNOLOGIES, LANGUAGES, TOOLS (WHAT / WHY / HOW)

## 1) Python

**What it is:** a programming language.
**Why we use it:** Django is written in Python, and it’s excellent for data + logic-heavy apps.
**How we use it in this project:** all backend logic is Python (levels, EXP, tasks, streaks, penalties).

Important note: Python projects usually need isolated dependencies, so we use a **virtual environment** (`venv`).

---

## 2) Django

**What it is:** a web framework for Python.
**Why we use it:**
Django gives us a full backend foundation quickly: routing (URLs), database integration, authentication framework, admin panel, security defaults.

**How we use it:**

* Defines database models (User, Profile, Tasks)
* Runs the backend server
* Handles business logic

---

## 3) Django REST Framework (DRF)

**What it is:** a toolkit for building APIs in Django.
**Why we use it:** React (frontend) and Django (backend) need a way to communicate. React talks to Django via HTTP requests to API endpoints. DRF makes those endpoints clean and structured.

**How we use it:**

* Build endpoints like `/api/health/`, `/api/login/`, `/api/tasks/`
* Convert model objects into JSON using serializers
* Control permissions and authentication (JWT in Phase 1)

---

## 4) JavaScript

**What it is:** the programming language of the browser.
**Why we use it:** React is built with JavaScript.
**How we use it:** UI logic, API calls, interactions.

---

## 5) React

**What it is:** a frontend library for building user interfaces.
**Why we use it:**
It’s modern, professional, and portfolio-friendly. It also matches SaaS-style dashboards well.

**How we use it:**

* Build “System UI” (dashboard, daily quests, profile)
* Fetch data from Django APIs
* Display progress bars, streaks, charts

---

## 6) Vite

**What it is:** a development server/bundler for React projects.
**Why we use it:** it starts fast, is modern, and is standard for React development.
**How we use it:** it runs your React app locally at a dev URL like:

`http://localhost:5173`

**Important note (error we hit):** Vite requires modern Node versions. Node 18.15 was too old for the Vite version you installed, and it crashed. We fixed it by upgrading Node.

---

## 7) Tailwind CSS

**What it is:** a utility-first CSS framework.
**Why we use it:** it makes it easy to build beautiful UI quickly without writing a lot of custom CSS.

**How we use it:**
Instead of writing CSS files, you use Tailwind class names directly in JSX, for example:

```jsx
<div className="min-h-screen bg-slate-950 text-white">
```

**Important note (warning we hit):** VS Code sometimes shows “Unknown at rule @tailwind” in `index.css`. This is an editor warning, not a runtime error. Tailwind still works in the browser.

---

## 8) Git + GitHub + GitHub Desktop

**What it is:** version control.
**Why we use it:**

* saves your progress
* lets you go back to older working versions
* builds a professional commit history for portfolio
* allows collaboration later

**How we use it (simple workflow):**

* Make changes in VS Code
* Open GitHub Desktop
* Write a commit message
* Commit
* Push to GitHub

---

## 9) Docker + Docker Compose

**What Docker is:** a tool to run your app in containers (isolated environments).
**Why we use it:**
Docker makes it easier to run the project consistently across machines and helps deployment later.

**How we use it:**
Instead of starting backend and frontend separately, we can run everything with:

```powershell
docker compose up --build
```

**Important note:** Docker Desktop must be working for this to run.

---

# SECTION 2 — PROJECT PHASES (WHAT WE BUILD IN EACH PHASE)

This project is built in phases so you can progress without overwhelm and keep a clean GitHub history.

## Phase 0 — Local foundation (Django + React + Tailwind + basic API)

**Status:** completed except Docker (Docker is the next step to fix and finish).
**Goal:** Create a working local development environment and confirm frontend-backend communication.

Deliverables:

* Django server runs locally
* React server runs locally
* React can fetch backend API endpoint `/api/health/`
* Tailwind works (dark UI visible)
* GitHub repository contains Phase 0 commits
* Docker configuration added and working (pending if Docker Desktop issues)

---

## Phase 1 — Authentication + real database structure (JWT + Profile)

**Goal:** Convert the prototype into a real multi-user architecture (even if you’re the only user at first).

Backend work:

* Configure PostgreSQL
* Build User Profile model
* Implement JWT login/signup endpoints
* Store player stats (level, exp, streak) in database

Frontend work:

* Login/signup pages
* Protected routes
* Profile status screen that reads from API

---

## Phase 2 — Daily quests + EXP + Level system

**Goal:** The core loop of “System” becomes real.

Backend:

* Task templates
* Daily quest generation logic (manual first, automated later)
* Completion endpoint updates EXP and streak

Frontend:

* Today’s quests screen
* Complete quest button
* EXP progress bar updates

---

## Phase 3 — Penalties + Achievements + Boss Challenges

**Goal:** Add discipline enforcement and long-term motivation.

Backend:

* penalty rules
* achievement engine
* weekly boss generator

Frontend:

* achievement gallery
* boss fight screen
* penalty warning UI

---

## Phase 4 — Deployment + Domain + Professional launch

**Goal:** Make it public.

* Backend deploy (Render/Railway)
* Frontend deploy (Vercel)
* Domain setup
* Environment variables
* Monitoring/logging (optional)

---

# SECTION 3 — PHASE 0 STEP-BY-STEP (VERY DETAILED)

## Phase 0 Objective

Get local dev running with Django + React + Tailwind and confirm connection using `/api/health/`.

### Step 0.1 — Create the repository (GitHub Desktop)

Open GitHub Desktop:
Create new repo named `discipline-system`, initialize README, publish.

Why we do this:
This ensures every step is tracked. You can always roll back and show progress.

---

## PART A — BACKEND (DJANGO)

### Step A1 — Open VS Code in your repo folder

Open folder:
`discipline-system`

Why:
So VS Code terminals and file paths are correct.

---

### Step A2 — Create backend folder (if not created)

Create folder: `backend/`

---

### Step A3 — Create virtual environment (venv)

Open terminal in VS Code:

```powershell
cd backend
python -m venv venv
```

What this does:
Creates a folder `venv/` containing a separate Python installation and site-packages.

Why:
So your project’s Python libraries don’t mix with other projects.

---

### Step A4 — Activate venv (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

How to confirm:
Your terminal begins with `(venv)`.

Important note (error you faced):
If PowerShell says scripts are blocked, run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

Why this error happens:
Windows blocks running scripts by default for security.

---

### Step A5 — Install backend dependencies

```powershell
python -m pip install --upgrade pip
pip install django djangorestframework django-cors-headers python-dotenv
```

What each does:

* `django`: backend framework
* `djangorestframework`: API toolkit
* `django-cors-headers`: allows requests from React port (5173)
* `python-dotenv`: later supports `.env` for secrets

---

### Step A6 — Create Django project and app

```powershell
django-admin startproject config .
python manage.py startapp core
```

What this does:

* `config` becomes the Django project (settings + URLs)
* `core` becomes your main app where API logic lives

---

### Step A7 — Configure settings.py properly (very important)

Open: `backend/config/settings.py`

Add to `INSTALLED_APPS`:

```python
"corsheaders",
"rest_framework",
"core",
```

Important note (error you faced):
If you forget commas, Python joins strings and Django tries to import a fake app name like:
`corsheadersrest_frameworkcore`

This causes:

`ModuleNotFoundError: No module named 'corsheadersrest_frameworkcore'`

Fix:
Make sure commas exist after each string.

---

### Step A8 — Add CORS middleware and allowed origins

In `MIDDLEWARE`, ensure this is near the top:

```python
"corsheaders.middleware.CorsMiddleware",
"django.middleware.common.CommonMiddleware",
```

Add allowed origins:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

Why:
React runs on port 5173. Browsers block cross-origin requests unless CORS is enabled.

---

### Step A9 — Create health endpoint API

In `backend/core/views.py`:

```python
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "discipline-system-api"})
```

In `backend/config/urls.py` add:

```python
from core.views import health
path("api/health/", health),
```

Why:
This is our first API endpoint to prove the backend works.

---

### Step A10 — Migrate and run backend

```powershell
python manage.py migrate
python manage.py runserver
```

Test:
`http://127.0.0.1:8000/api/health/`

Important note (error you saw):
Visiting `http://127.0.0.1:8000/` gives 404.

Why:
We didn’t define a route for `/`. Only `/api/health/` and `/admin/` exist.

---

## PART B — FRONTEND (REACT + VITE + TAILWIND)

### Step B1 — Create frontend folder

Folder: `frontend/`

---

### Step B2 — Create React app using Vite

From inside `frontend` folder:

```powershell
npm create vite@latest . -- --template react
npm install
```

Important note (error you faced):
Node 18.15 caused Vite to fail because newer Vite requires Node 20+.

Fix:
Upgrade Node. You now have:

* Node v24.13.1
* npm 11.8.0

---

### Step B3 — Install Tailwind

```powershell
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Update `tailwind.config.js`:

```js
content: ["./index.html", "./src/**/*.{js,jsx}"]
```

Update `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Important note (warning you saw):
“Unknown at rule @tailwind” in VS Code.

Why:
VS Code default CSS validator doesn’t recognize Tailwind directives.

Fix:
Ignore it (Tailwind works in browser). Optionally install Tailwind IntelliSense extension.

---

### Step B4 — Connect React to Django health endpoint

In `src/App.jsx`, add a fetch to:

`http://127.0.0.1:8000/api/health/`

Why:
This proves the full stack connection works.

---

### Step B5 — Run frontend

```powershell
npm run dev
```

Open:
`http://localhost:5173`

Expected:
Dark UI + JSON from `/api/health/`.

---

### Step B6 — Commit Phase 0

In GitHub Desktop:
Commit message examples:

* `Phase 0: Setup Django API base`
* `Phase 0: Setup React + Tailwind base`
  Push to GitHub

Why:
Phase-based commits help you track milestones and build a professional history.

---

# PART C — DOCKER (PHASE 0 DOCKER SECTION)

## Step C0 — Before you start Docker

Stop local servers, otherwise ports will conflict.
In Django/React terminals press:

`CTRL + C`

---

## Step C1 — Confirm Docker is working

Run:

```powershell
docker --version
docker compose version
docker info
```

If `docker info` errors, Docker Desktop is not running correctly and must be fixed first.

---

## Step C2 — Create backend requirements.txt (for Docker)

Create: `backend/requirements.txt`

```txt
Django>=5.0
djangorestframework
django-cors-headers
python-dotenv
```

---

## Step C3 — Create backend Dockerfile

Create: `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

## Step C4 — Create frontend Dockerfile

Create: `frontend/Dockerfile`

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY . /app
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
```

---

## Step C5 — Create docker-compose.yml (repo root)

Create: `docker-compose.yml`

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
```

---

## Step C6 — Run Docker

From repo root:

```powershell
docker compose up --build
```

Test:

* Backend: `http://localhost:8000/api/health/`
* Frontend: `http://localhost:5173`

Important note (common error):
If Docker says port already in use, it means Django/React is still running locally.
Fix:
Stop them with `CTRL+C`, then run Docker again.

---

# SECTION 4 — ERRORS & HURDLES WE FACED IN PHASE 0 (DETAILED)

## Error 1 — PowerShell virtual environment activation blocked

What happened:
`Activate.ps1` did not run due to script restrictions.

Why:
Windows blocks scripts by default.

Fix:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Error 2 — Django ModuleNotFoundError for combined app name

Error:
`No module named 'corsheadersrest_frameworkcore'`

Why:
Missing commas in `INSTALLED_APPS` caused string concatenation.

Fix:
Add commas after each app name.

Example:
Wrong:

```python
"corsheaders"
"rest_framework"
```

Correct:

```python
"corsheaders",
"rest_framework",
```

---

## Error 3 — Django 404 at root URL

What happened:
`http://127.0.0.1:8000/` showed 404.

Why:
No URL route for `/` was created.
Only `/api/health/` exists.

Fix:
Use `/api/health/` or add a homepage route later.

---

## Error 4 — Vite refusing to run with Node 18

What happened:
Vite required Node 20+.

Why:
New Vite versions depend on newer Node features.

Fix:
Upgrade Node (you upgraded to Node 24+).

---

## Error 5 — Tailwind “Unknown at rule @tailwind”

What happened:
VS Code highlighted Tailwind directives as unknown.

Why:
VS Code’s CSS validator doesn’t know Tailwind syntax.

Fix:
Ignore; Tailwind works at runtime.

---

## Error 6 — `frontend/frontend` folder mistake

What happened:
React project got created in nested folder.

Why:
Vite was run inside a folder that already contained `frontend`.

Fix:
Move files up one level and delete nested folder.

---

# SECTION 5 — HOW WE KEEP THIS DOCUMENT UPDATED

Every time we hit a problem, we add:

* Error message
* Why it happened
* Fix steps
* Prevention tips

This guide becomes your “engineering notebook.”

---

## Next step (today)

Since Docker Desktop is currently failing, the very first thing you should do next is run:

```powershell
docker info
```

Then paste the error text here.
Once we fix Docker Desktop, we will complete Phase 0 Docker and commit it.

---

If you want, I can also convert THIS exact document into:

* Word
* PDF
* Markdown file format for GitHub
111111111
Just say the format.
