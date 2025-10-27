Flask + PostgreSQL Backend

Overview
This backend provides a minimal, production-ready Flask application wired to PostgreSQL via SQLAlchemy and Flask-Migrate, with environment-based configuration and CORS enabled for the React frontends.

Features
- App factory pattern (`create_app`)
- SQLAlchemy ORM + Flask-Migrate (Alembic)
- Env-based configuration via python-dotenv
- CORS enabled for local dev
- Healthcheck and example Users API

Quick Start
1) Create and fill env file
   - Copy `.env.example` to `.env` and update values.

2) Create virtual environment and install deps
   - Windows (PowerShell):
     - `python -m venv .venv`
     - `.\.venv\Scripts\Activate.ps1`
     - `pip install -r requirements.txt`

3) Initialize database migrations
   - `set FLASK_APP=wsgi.py` (PowerShell: `$env:FLASK_APP="wsgi.py"`)
   - `flask db init` (first time only)
   - `flask db migrate -m "init"`
   - `flask db upgrade`

4) Run the server
   - Development: `flask run --port 5050`
   - Or: `python wsgi.py` (uses app.run for convenience in dev)

Endpoints
- GET `/health` → { status: "ok" }
- GET `/api/users` → list users
- POST `/api/users` → create user { name, email }

Configuration
- See `config.py` for settings. Key env vars:
  - `FLASK_ENV` (development/production)
  - `SECRET_KEY`
  - `DATABASE_URL` (e.g., postgresql+psycopg2://user:pass@localhost:5432/dbname)
  - `CORS_ORIGINS` (optional, comma-separated list)

Project Structure
```
db/
  app.py           # create_app factory, extensions
  wsgi.py          # entrypoint for flask run / gunicorn
  config.py        # configuration classes
  requirements.txt # pinned deps
  .env.example     # env template
  migrations/      # alembic migrations (created by flask db init)
  models/
    __init__.py
    user.py
  routes/
    __init__.py
    health.py
    users.py
```

Notes
- For production, run with a WSGI server like gunicorn: `gunicorn -w 4 -b 0.0.0.0:5050 wsgi:app`
- Ensure your database is reachable from the server environment and that the `DATABASE_URL` is correct.




