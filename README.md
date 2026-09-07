# 🏡 HomeHub

> A lightweight, shared family hub for reminders, chores, notes, shopping lists, expenses, recipes, media, and more — all in one private dashboard you self-host.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3-000000.svg?logo=flask)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Compat-DB473C?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Supabase](https://img.shields.io/badge/Supabase-Compatible-18181B?logo=supabase)](https://supabase.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-Deploy-46E3B7.svg?logo=render&logoColor=white)](https://render.com/)
[![Node](https://img.shields.io/badge/Node.js-20+-339933.svg?logo=nodedotjs&logoColor=white)](https://nodejs.org/)

![HomeHub Banner](./static/icons/homehub.svg)
![HomeHub Screenshot Placeholder](./static/icons/icon-192.png?raw=true)

> 💡 If you add screenshots, GIFs, or UI mockups, drop them here and update the paths above. A `screenshots/` folder is a common convention.

---

## ✨ Features

- 📅 **Shared Calendar Reminders** — day/week/month views, recurring rules, categories, and colors
- ✅ **To-Do / Chores** — recurring chores, tags, due dates, and owner-based editing
- 🛒 **Shared Shopping List** — quantities, units, tagging, filtering, and history-backed suggestions
- 💰 **Expense Tracker** — entries, recurring expenses, categories, currency, and month views
- 📓 **Shared Notes** — quick collaborative notes with owner-controlled edits/deletes
- 📦 **Recipe Book** — Quill-rich editor, ingredients/instructions, links, and tag filtering
- 📲 **QR Generator** — text/URL + WiFi QR codes with history
- 🌦 **Weather Widget** — optional dashboard weather with geolocation or static coords
- 👥 **Who is Home + Personal Status** — presence and status for family members
- 🔔 **Web Push / PWA** — service worker, manifest, and push notification support
- 🎨 **Theming & Dark Mode** — config-driven colors, system dark mode, sidebar toggle

---

## 🧰 Built With

### Runtime & Web
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3-000000.svg?logo=flask)](https://flask.palletsprojects.com/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-Server-49AA26.svg?logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Nginx](https://img.shields.io/badge/Nginx-Basic_Auth-009639.svg?logo=nginx&logoColor=white)](https://nginx.org/)
[![Supervisor](https://img.shields.io/badge/Supervisor-Process_Management-7A0871.svg?logo=supervisor)](http://supervisord.org/)

### Data
[![SQLite](https://img.shields.io/badge/SQLite-Default-F59E0B.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Compatible-DB473C?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Supabase](https://img.shields.io/badge/Supabase-Recommended-18181B?logo=supabase)](https://supabase.com/)

### Frontend & Tooling
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Inter Font](https://img.shields.io/badge/Inter-Font-D4D4D8?logo=googlefonts&logoColor=white)](https://fonts.google.com/specimen/Inter)
[![Font Awesome 6](https://img.shields.io/badge/FontAwesome-6-528DD7.svg?logo=FortAwesome&logoColor=white)](https://fontawesome.com/)
[![Quill Editor](https://img.shields.io/badge/Quill-Rich_Text-4CAF50.svg?logo=quill&logoColor=white)](https://quilljs.com/)

### Deployment & Infra
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-Deploy-46E3B7.svg?logo=render&logoColor=white)](https://render.com/)
[![GitHub Container Registry](https://img.shields.io/badge/GHCR-Image-24292E.svg?logo=github)](https://ghcr.io/)

---

## 🖼 Visual Preview

### Dashboard (placeholder)

Center your screenshot like this:

````markdown
![HomeHub Dashboard](./screenshots/dashboard.png)
````

### Reminders Calendar (placeholder)

````markdown
![Reminders Calendar](./screenshots/reminders.png)
````

### Shopping List (placeholder)

````markdown
![Shopping List](./screenshots/shopping.png)
````

If you do not have screenshots yet, keep the placeholder images from `static/icons/` or replace them later.

---

## 🚀 Getting Started

HomeHub is a Flask app with a Tailwind-built UI, configurable via `config.yml`, and deployable either locally or to Render. By default it uses SQLite; for multi-instance or production use, connect it to PostgreSQL (Supabase works well here).

### Prerequisites

**Local dev / self-host:**

- [Python 3.12+](https://www.python.org/downloads/)
- [Node.js 20+](https://nodejs.org/) (only needed to rebuild CSS with Tailwind)
- [Git](https://git-scm.com/)
- Optional: [Docker + Docker Compose](https://docs.docker.com/get-docker/) if you want containerized runs

**Render + Supabase (free tier path):**

- A GitHub account
- A [Render](https://render.com/) account
- A [Supabase](https://supabase.com/) project (free tier)
- Basic familiarity with environment variables

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/homehub.git
cd homehub
```

If you are contributing or running from a private fork, substitute the correct repo URL.

### 2. Configure the app

Copy the example config and edit it for your household.

```bash
cp config-example.yml config.yml
```

At minimum, review:

- `instance_name`
- `family_members`
- `feature_toggles`
- `theme` colors
- `push_notifications`

If you want push notifications later, generate VAPID keys with:

```bash
python scripts/generate_vapid_keys.py
```

Then paste the output into `config.yml` under `push_notifications`.

### 3. Set secrets

HomeHub needs a Flask secret key. For local dev you can let the app auto-generate one on first run, but for production set it explicitly:

```bash
export SECRET_KEY="$(python -c "import secrets; print(secrets.token_hex(32))")"
```

Keep this value private and reuse it across restarts so existing sessions are not invalidated unexpectedly.

---

## ▶ Run locally

### Option A: Native local run (Python)

This is the simplest path for development and quick testing.

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows (Git Bash / WSL):
# .venv/Scripts/activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Build/minify the Tailwind stylesheet (needed once, or after UI changes)
npm install
npm run build:css

# 4. Run the app
python run.py
```

By default the app listens on:

```
http://0.0.0.0:5000
```

If you want auto-reloading while editing templates/JS/CSS during local dev, you can run Flask in debug mode. For production-style local runs, use the WSGI entry point:

```bash
gunicorn wsgi:app -w 1 -k sync -b 0.0.0.0:5000
```

### Option B: Docker Compose (app container)

If you want a containerized local run without Render-style basic auth:

```bash
# Copy config first if you have not already
cp config-example.yml config.yml

# Run the app profile
docker compose --profile app up --build
```

Then open:

```
http://localhost:5000
```

### Option C: Docker Compose (Render-style container with basic auth)

This profile uses the Render-flavored image plus Nginx basic auth, which is useful if you want to test the exact Render deployment locally.

```bash
docker compose --profile render up --build
```

Then open:

```
http://localhost:10000
```

It will prompt for HTTP basic auth using the `AUTH_USERNAME` and `AUTH_PASSWORD` you set in the compose environment or `.env`.

---

## ☁ Host on Render (free) with Supabase for the database

This path gives you a free web service plus a free managed Postgres database.

### Step 1 — Create a Supabase project

1. Go to [Supabase](https://supabase.com/) and create a new project.
2. Open **Project Settings → Database**.
3. Copy the **Connection string** (URI style).

You will use this as your `DATABASE_URL`.

If Supabase gives you a URI that starts with `postgres://`, HomeHub will convert it to `postgresql://` automatically. If your password contains special characters (especially `@`), make sure it is URL-encoded, or use the connection string Supabase provides for direct use.

### Step 2 — Prepare GitHub

1. Push your HomeHub repo to GitHub if it is not there already.
2. Make sure `render.yaml` is in the repo root.
3. Make sure `config.yml` is in the repo root and tuned for your household.

> By default the Render deploy path uses `config.yml` from the repo. If you prefer not to commit household-specific config, you can inject it via Render's config mounting or env-based overrides, but the blueprint provided here expects `config.yml` in the repo.

### Step 3 — Add the Render web service

You can deploy through Render's **Blueprint** flow using `render.yaml`, or manually add a Docker web service.

**If using the blueprint:**

1. In Render, create a new **Blueprint** and select your GitHub repo.
2. Render should pick up `render.yaml`.
3. Set these **environment variables** in the Render dashboard for the service:
   - `AUTH_USERNAME`
   - `AUTH_PASSWORD`
   - `DATABASE_URL` (your Supabase connection URI)
   - `FLASK_ENV` = `production`

**If deploying manually:**

1. Create a new **Web Service** on Render.
2. Connect your GitHub repo.
3. Choose **Docker** as the environment.
4. Set the Dockerfile path to `Dockerfile.render`.
5. Add the same environment variables above.

### Step 4 — Important env vars

| Variable | Purpose | Notes |
|---|---|---|
| `AUTH_USERNAME` | Primary login username for Nginx basic auth | Required by `entrypoint.sh` |
| `AUTH_PASSWORD` | Primary login password for Nginx basic auth | Required by `entrypoint.sh` |
| `DATABASE_URL` | Supabase/Postgres connection URI | Enables PostgreSQL mode |
| `SECRET_KEY` | Flask session secret | Render can auto-generate if omitted |
| `FLASK_ENV` | App environment | Set to `production` |

The `entrypoint.sh` script also supports:

- `AUTH_USERS` — extra users as `user1:pass1,user2:pass2`
- Any extra custom env var in `KEY=VALUE` form is treated as a username/password pair and added to Nginx basic auth automatically

### Step 5 — Verify deployment

1. Wait for the Render deploy to finish.
2. Visit the service URL.
3. You should see a basic auth prompt first.
4. After auth, you should reach HomeHub's login/setup flow.
5. If the database is brand new, HomeHub will create its tables automatically on startup.

### Step 6 — Free-tier caveats

- The Render free web service can spin down after inactivity and may take longer to wake up.
- For a family hub, that may be fine. If you need always-on availability, you may need a paid plan or a different host.
- Supabase free tier is separate from Render; both have their own limits.

---

## 🗄 Using Supabase as the database

HomeHub uses `DATABASE_URL` to decide whether to use Postgres. If that variable is present, it connects to Postgres; otherwise it falls back to a local SQLite file at `data/app.db`.

When using Supabase:

1. Use a direct connection string, not the pooled connection for migrations unless you have already accounted for PgBouncer behavior.
2. If you use Supabase's connection pooler, HomeHub sets `prepare_threshold=None` and `pool_pre_ping=True` for better compatibility.
3. The app still auto-creates tables and runs schema migrations on startup, so a fresh Supabase database should work without manual DDL.

A minimal runtime wiring looks like this:

```bash
export DATABASE_URL="postgresql://postgres:YourPassword@db.xxxxx.supabase.co:5432/postgres"
export SECRET_KEY="your-secret-key-here"
export FLASK_ENV="production"

python run.py
```

Or, if you are running via Gunicorn:

```bash
gunicorn wsgi:app -w 1 -k sync -b 0.0.0.0:5000
```

---

## 🔐 First-time setup

On first run you will typically:

1. Reach the app
2. Create your initial users through the setup flow
3. Log in with one of those users
4. Adjust `config.yml` and soft toggles for your household

Exact screens and flows can vary by version, but HomeHub is designed to be usable immediately after deployment with a basic auth layer plus app-level login.

---

## 📖 Usage Examples

### Create a reminder via the API

```http
POST /api/reminders
Content-Type: application/json

{
  "title": "Pay electricity bill",
  "date": "2026-09-10",
  "time": "18:00",
  "description": "Paid via online banking",
  "creator": "Dustu",
  "category": "bills",
  "color": "#0d9488"
}
```

Response:

```json
{
  "ok": true,
  "reminder": {
    "id": 12,
    "date": "2026-09-10",
    "time": "18:00",
    "title": "Pay electricity bill",
    "description": "Paid via online banking",
    "creator": "Dustu",
    "category": "bills",
    "color": "#0d9488",
    "recurring_id": null,
    "timestamp": "2026-09-07T12:00:00",
    "updated_at": null
  }
}
```

### Create a recurring reminder rule

```http
POST /api/reminders
Content-Type: application/json

{
  "title": "Team standup",
  "date": "2026-09-08",
  "time": "09:30",
  "creator": "Aranya",
  "recurring": {
    "interval": 1,
    "unit": "day",
    "end_date": "2026-12-31"
  }
}
```

### Update or delete reminders in bulk

```http
DELETE /api/reminders
Content-Type: application/json

{
  "ids": [12, 13, 14],
  "creator": "Dustu"
}
```

### Update a recurring rule

```http
PATCH /api/recurring_rules/5
Content-Type: application/json

{
  "creator": "Aranya",
  "title": "Team standup",
  "time": "10:00",
  "interval": 1,
  "unit": "day",
  "end_date": "2027-01-31"
}
```

### Frontend: use the reminders API from browser JS

The app already exposes a small client helper at `/static/js/reminders_api.js`:

```javascript
// List reminders for a given scope and date
const month = await remindersApi.list('month', '2026-09-01');

// Create a reminder
const created = await remindersApi.create({
  title: 'Buy groceries',
  date: '2026-09-09',
  time: '17:30',
  creator: 'Bidisha'
});

// Update a reminder
await remindersApi.update(created.reminder.id, {
  title: 'Buy groceries and household items',
  creator: 'Bidisha'
});

// Delete multiple reminders
await remindersApi.removeMany([1, 2, 3], 'Bidisha');
```

---

## 🧩 Configuration

Most behavior is driven by `config.yml`.

Key sections:

- `instance_name` — displayed app name
- `password` — optional password-less access control setting
- `admin_name` — admin username for UI permission checks
- `feature_toggles` — enable/disable modules
- `family_members` — household members
- `reminders` — time format, calendar start day, reminder categories
- `weather` — optional weather widget config
- `theme` — primary and sidebar colors
- `push_notifications` — VAPID keys and subject

For a safe starting point, copy `config-example.yml` to `config.yml` and edit from there.

---

## 📦 Deployment notes

### Dockerfiles

- `Dockerfile` — standard app image with Gunicorn
- `Dockerfile.render` — Render-flavored image with Nginx basic auth + Supervisor

### Process management

The Render-flavored container uses:

- Nginx for serving and basic auth
- Gunicorn for the Flask app
- Supervisor to keep both running

### Persistent data

If you are running containers, persist these paths:

- `uploads/`
- `media/`
- `pdfs/`
- `data/`
- `config.yml`

If you switch to Supabase, the database is external and does not need to be mounted.

---

## 🧭 Project structure

```text
.
├── app/
│   ├── blueprints/    # route modules
│   ├── models.py      # SQLAlchemy models
│   ├── config.py      # config.yml loader
│   └── ...
├── templates/         # Jinja2 UI
├── static/
│   ├── output.css     # built Tailwind CSS
│   ├── input.css      # Tailwind source
│   ├── js/            # browser helpers
│   └── icons/
├── nginx/
├── scripts/
├── compose.yml
├── Dockerfile
├── Dockerfile.render
├── render.yaml
├── requirements.txt
├── package.json
├── run.py
└── wsgi.py
```

---

## 🧹 Optional setup tasks

- Generate push notification keys if you want web push
- Tune `feature_toggles` so the sidebar only shows what your family uses
- Add household-specific theme colors in `config.yml`
- Keep `SECRET_KEY` stable across restarts in production
- If using Docker, mount persistent volumes for uploads, media, PDFs, and data

---

## 🤝 Contributing

Contributions are welcome. Common starting points:

- Fix a bug or improve an existing blueprint
- Improve UI/UX in templates or static assets
- Improve config-driven behavior
- Harden permission checks or input sanitization
- Improve deployment docs or containerization

Before opening a PR:

1. Keep changes consistent with the existing style
2. Be careful with credentials and secrets
3. If changing DB schema behavior, consider both SQLite and Postgres paths

---

## 📄 License

HomeHub is provided under the [MIT License](./LICENSE).

---

## ☕ Support

If you find HomeHub useful, consider supporting the project:

[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00.svg?logo=buy-me-a-coffee&logoColor=black)](https://ko-fi.com/skv)

---

*Built as a practical shared space for a family home.*

