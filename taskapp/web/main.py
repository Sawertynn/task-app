from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from uuid import UUID
from taskapp.tasks import TaskManager
from taskapp.storage.filedb import FileDB

fdb = FileDB("data/tasks.json")
app = FastAPI()
manager = TaskManager(fdb)

# Serve static frontend
frontend_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/", response_class=FileResponse)
def index():
    return frontend_dir / "index.html"

@app.get("/tasks")
def list_tasks():
    return [task.to_dict() for task in manager.list_tasks()]

@app.post("/tasks")
def create_task(data: dict):
    title = data.get("title")
    parent_id = data.get("parent_id")
    task = manager.add_task(title=title, parent_id=UUID(parent_id) if parent_id else None)
    return task.to_dict()

@app.post("/tasks/{task_id}/toggle")
def toggle_task(task_id: str):
    task = manager.toggle(UUID(task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()

@app.post("/tasks/{task_id}/delete")
def delete_task(task_id: str):
    success = manager.delete(UUID(task_id))
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok"}

@app.post("/tasks/{task_id}/edit")
def edit_task(task_id: str, data: dict):
    task = manager.get_task(UUID(task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = data.get("title", task.title)
    manager.save()
    return task.to_dict()

@app.post("/tasks/{task_id}/move")
def move_task(task_id: str, data: dict):
    new_parent_id = data.get("parent_id")
    task = manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.parent_id = UUID(new_parent_id) if new_parent_id else None
    manager.save()
    return task.to_dict()

