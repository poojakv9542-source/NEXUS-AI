# NEXUS AI — File Management CAP-001 to CAP-008

This is an additions-only patch. It does not overwrite your existing database, dashboard, agent, `.env`, or `main.py`.

## 1. Copy the files
Extract this ZIP into your existing project root:
`C:\Users\Pooja K V\Desktop\AI-AGENT`

Allow folders to merge. Do not replace existing files if Windows asks about files other than the new `server/routers/files.py` and sample workspace files.

## 2. Connect the router (two lines)
Open `server/main.py` in VS Code.

Find the line:
`app = FastAPI(`

Add this import with the other imports near the top:
`from server.routers.files import router as files_router`

Then find the app setup, after the `app = FastAPI(...)` block, and add:
`app.include_router(files_router)`

Save the file. Uvicorn `--reload` should reload automatically. Keep its terminal open.

## 3. Test
Open:
`http://127.0.0.1:8000/docs`

A new **File management** section should appear.

Test these GET endpoints:
- `/files/list` — lists the safe workspace.
- `/files/read?path=sample_docs/employee_weekly_report.txt`
- `/files/find?name=meeting`
- `/files/duplicates`
- `/files/extract?path=sample_docs/employee_weekly_report.txt`

Test POST `/files/summarize` with:
`{"path":"sample_docs/employee_weekly_report.txt"}`

For `/files/rename` and `/files/organize`, first leave `confirm` as `false` to preview. Only set `confirm` to `true` after checking the preview. These actions change files inside the workspace.

## Safety boundary
The API only accepts paths relative to the dedicated `workspace` folder. It blocks paths outside that folder. Do not place private files, passwords, API keys, or `.env` files in the workspace.

## Current implementation limits
- PDF extraction requires `python -m pip install pypdf`.
- Summarization is currently a simple extractive preview, not local AI.
- These endpoints are local test tools. They do not yet connect employee computers or external company storage.
