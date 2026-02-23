Perfect. Below is your **Phase 0 Markdown version** formatted cleanly for GitHub README.

You can copy-paste this directly into:

```
README.md
```

or into:

```
docs/phase-0-setup.md
```

---

# 🚀 Phase 0 — Local Development Setup

**Discipline System (Full-Stack Django + React + Docker)**

---

## 🎯 Phase 0 Goal

By the end of Phase 0:

* ✅ Django backend running locally
* ✅ React frontend running locally
* ✅ Tailwind UI working
* ✅ React connected to Django API
* ✅ Docker configured for local development
* ✅ All changes committed to GitHub

---

# 🛠 Tech Stack (Phase 0)

## Backend

* **Python**
* **Django**
* **Django REST Framework**
* **django-cors-headers**

## Frontend

* **React**
* **Vite**
* **Tailwind CSS**

## Dev Tools

* **VS Code**
* **GitHub Desktop**
* **Node.js (v20+)**
* **Docker Desktop**

---

# 📁 Project Structure

```
discipline-system/
│
├── backend/
│
├── frontend/
│
├── docs/
│   └── phase-0-setup.md
│
└── docker-compose.yml
```

---

# 🔵 Step 1 — Create GitHub Repository

### Why?

To track all progress professionally and avoid losing work.

### Steps:

1. Open GitHub Desktop
2. File → New Repository
3. Name: `discipline-system`
4. Check “Initialize with README”
5. Publish repository

Commit message:

```
Phase 0: Initialize project structure
```

---

# 🟢 Step 2 — Backend Setup (Django)

## 2.1 Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### Activate (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

If blocked:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 2.2 Install Dependencies

```bash
pip install django djangorestframework django-cors-headers python-dotenv
```

### What They Do

| Package       | Purpose                         |
| ------------- | ------------------------------- |
| Django        | Backend framework               |
| DRF           | Builds REST APIs                |
| CORS Headers  | Allows frontend to call backend |
| python-dotenv | Environment variables support   |

---

## 2.3 Create Django Project

```bash
django-admin startproject config .
python manage.py startapp core
```

---

## 2.4 Configure Settings

Add to `INSTALLED_APPS`:

```python
"corsheaders",
"rest_framework",
"core",
```

⚠️ **Common Error**

If you see:

```
ModuleNotFoundError: corsheadersrest_frameworkcore
```

Cause: Missing commas between app names.

Fix: Add commas properly.

---

## 2.5 Add CORS Middleware

```python
"corsheaders.middleware.CorsMiddleware",
```

Allow React:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

---

## 2.6 Create Health Endpoint

`core/views.py`

```python
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})
```

`config/urls.py`

```python
path("api/health/", health),
```

---

## 2.7 Run Backend

```bash
python manage.py migrate
python manage.py runserver
```

Test:

```
http://127.0.0.1:8000/api/health/
```

⚠️ 404 on `/` is normal — only `/api/health/` exists.

---

# 🔵 Step 3 — Frontend Setup (React + Vite)

## 3.1 Create React App

```bash
cd frontend
npm create vite@latest . -- --template react
npm install
```

---

### ⚠️ Node Version Error

If you see:

```
Vite requires Node 20+
```

Fix:
Upgrade Node to latest LTS.

Check:

```bash
node -v
npm -v
```

---

# 🟣 Step 4 — Tailwind Setup

Install:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Update `tailwind.config.js`:

```js
content: ["./index.html", "./src/**/*.{js,jsx}"],
```

Update `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

### ⚠️ VS Code Warning

```
Unknown at rule @tailwind
```

This is safe to ignore.
It is only a VS Code CSS validation warning.

---

# 🔗 Step 5 — Connect React to Django

Update `App.jsx`:

```javascript
useEffect(() => {
  fetch("http://127.0.0.1:8000/api/health/")
    .then((r) => r.json())
    .then(setHealth);
}, []);
```

Run:

```bash
npm run dev
```

Open:

```
http://localhost:5173
```

You should see:

* Dark UI (Tailwind working)
* JSON health response (backend connected)

---

# 🐳 Step 6 — Docker Setup

## backend/Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

## frontend/Dockerfile

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
```

---

## docker-compose.yml

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
```

---

## Run Docker

```bash
docker compose up --build
```

Test:

```
http://localhost:8000/api/health/
http://localhost:5173
```

---

### ⚠️ Common Docker Error

```
Port already in use
```

Fix:
Stop local Django/React servers before running Docker.

---

# ✅ Phase 0 Completion Checklist

* [ ] Django running
* [ ] React running
* [ ] Tailwind visible
* [ ] React fetch works
* [ ] Docker runs successfully
* [ ] All commits pushed to GitHub

---

# 🚀 Next Phase (Phase 1)

* JWT Authentication
* Custom User Model
* PostgreSQL (Docker)
* Profile system (Level / EXP / Streak)
* Protected React routes

---

If you’d like, I can now:

* 🔷 Generate a professional GitHub README header with badges
* 🔷 Create a clean architecture diagram
* 🔷 Prepare Phase 1 markdown template
* 🔷 Help you design your commit structure strategy

Just tell me what’s next 🔥
