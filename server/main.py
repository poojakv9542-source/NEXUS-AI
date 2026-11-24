from pathlib import Path
import sys
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.memory import NexusMemory
from app.agent import NexusAgent
from server.capabilities import CAPABILITIES
from server.routers.files import router as files_router

app = FastAPI(
    title="NEXUS AI Local Backend",
    version="0.1.0",
    description="Local development API for the NEXUS AI employee prototype."
)

# Register the local, workspace-restricted file-management API.
app.include_router(files_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    instruction: str = Field(min_length=1, max_length=5000)

class TaskResponse(BaseModel):
    task_id: int
    status: str
    instruction: str
    result: Optional[str] = None
    error: Optional[str] = None

@app.get("/")
def root():
    return {"service": "NEXUS AI", "backend": "FastAPI", "mode": "local"}

@app.get("/health")
def health():
    memory = NexusMemory()
    try:
        tasks = memory.get_all_tasks()
        return {
            "ok": True,
            "database": "connected",
            "database_path": str(ROOT / "data" / "nexus.db"),
            "recorded_tasks": len(tasks),
            "ai_engine": "not_connected_in_this_backend_patch"
        }
    finally:
        memory.close()

@app.get("/capabilities")
def list_capabilities(category: Optional[str] = None):
    items = CAPABILITIES
    if category:
        items = [item for item in items if item["category"].lower() == category.lower()]
    return {
        "total": len(items),
        "categories": list(dict.fromkeys(item["category"] for item in items)),
        "capabilities": items,
        "notice": "These are the requested capability targets. 'planned' means not implemented yet."
    }

@app.get("/tasks")
def get_tasks():
    memory = NexusMemory()
    try:
        return {"tasks": memory.get_all_tasks()}
    finally:
        memory.close()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    memory = NexusMemory()
    try:
        task = memory.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    finally:
        memory.close()

@app.post("/tasks/execute")
def execute_task(request: TaskRequest):
    agent = NexusAgent()
    try:
        result = agent.process_instruction(request.instruction.strip())
        return {
            "task_id": result["task_id"],
            "status": result["status"],
            "objective": result["objective"],
            "actions": [
                {
                    "action_type": action.action_type,
                    "description": action.description,
                    "requires_approval": action.requires_approval,
                    "parameters": action.parameters
                } for action in result["actions"]
            ],
            "execution_results": result["execution_results"],
            "notice": "Current uploaded agent only performs the ANALYZE placeholder. Other capability execution is not implemented yet."
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        agent.close()
