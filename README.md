# NEXUS AI — Local Digital Employee Prototype

## Project overview
NEXUS AI is a local prototype of an intelligent digital employee. This submission includes:
- A FastAPI backend for health, task history, capability catalogue, and file-management APIs.
- A SQLite task-history database (`data/nexus.db`).
- A Streamlit dashboard (`dashboard/ui.py`).
- A dedicated `workspace/` containing safe sample documents for demonstrations.
- An initial capability catalogue of 72 requested capability targets.

## Run locally (Windows PowerShell)
Open PowerShell in the project root.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn server.main:app --reload --host 127.0.0.1 --port 8000
```

Open the API documentation: http://127.0.0.1:8000/docs

To run the Streamlit dashboard, open a **second** terminal in the project root, activate the same virtual environment, then run:

```powershell
streamlit run dashboard/ui.py
```

## File-management API
The FastAPI app registers the file-management router at `/files`. Its operations are restricted to the project `workspace/` directory:
- `GET /files/list`
- `GET /files/read`
- `GET /files/find`
- `POST /files/organize` (preview by default; requires `confirm=true` to move)
- `POST /files/rename` (preview by default; requires `confirm=true` to rename)
- `GET /files/duplicates`
- `POST /files/summarize` (basic extractive preview, not LLM)
- `GET /files/extract` (PDF support through pypdf)

Do not put private documents, credentials, `.env` files, or passwords in `workspace/`.

## Capability status and honest scope
The API catalogue contains 72 capability targets. The first eight file-management capabilities have corresponding API endpoint implementations. CAP-001 (listing the sample folder) was successfully demonstrated with HTTP 200. CAP-002 through CAP-008 have code but were not individually verified as part of this deadline build. CAP-009 through CAP-072 remain planned targets, not completed functionality.

The current task planner is a rule-based ANALYZE placeholder. The local Ollama model is not connected in this build. Email, calendar, Jira, Teams, Trello, browser automation, and central multi-employee deployment are not configured. Integrations require authorized account connections and approval controls before real actions.

## Safety
- File APIs accept paths relative to `workspace/` and block paths outside it.
- File move and rename endpoints preview first and require explicit confirmation.
- Use only sample or authorized files.
- This is a local prototype, not a production-ready centrally deployed employee monitoring system.

## Submission contents
See `SUBMISSION_REPORT.md` for implemented components, verification evidence, limitations, and future work.
