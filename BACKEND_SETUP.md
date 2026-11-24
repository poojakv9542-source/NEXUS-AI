# NEXUS AI — local FastAPI backend starter

This patch adds a local API without replacing your current dashboard, agent, or SQLite database.

## 1. Install packages (PowerShell)

Open PowerShell in `C:\Users\Pooja K V\Desktop\AI-AGENT`, activate your existing venv, then run:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements-backend.txt
```

## 2. Start the API

```powershell
python -m uvicorn server.main:app --reload --host 127.0.0.1 --port 8000
```

## 3. Test in your browser

- API home: http://127.0.0.1:8000/
- Health/database: http://127.0.0.1:8000/health
- All 72 capability targets: http://127.0.0.1:8000/capabilities
- Interactive API tester: http://127.0.0.1:8000/docs
- Existing tasks: http://127.0.0.1:8000/tasks

## Important truth about current implementation

The uploaded code currently implements only `ANALYZE`, `LIST_FILES`, and `READ_FILE` at the executor level. The planner always produces an `ANALYZE` action. This patch exposes the existing task database through FastAPI and registers all 72 requested capability targets. It does **not** pretend all 72 are implemented. Each capability must be built and tested before its status is changed to implemented.

The API uses your existing `data/nexus.db`. Do not delete that file. This is a local development server, not yet a central server for multiple employees.

Do not put `.env`, passwords, API keys, or `venv/` into a ZIP you share.
