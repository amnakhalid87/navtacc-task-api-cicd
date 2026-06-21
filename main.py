from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = []


class Task(BaseModel):
    name: str
    is_done: bool = False


@app.get('/')
def home():
    return {
        "message": "Task Manager API is running!",
        "endpoints": {
            "/health": "Check API status",
            "/tasks": "GET all tasks, POST create task",
            "/tasks/{id}": "GET specific task"
        }
    }


@app.get('/health')
def health_check():
    return {"status": "OK"}


@app.get('/tasks')
def get_all_tasks():
    return {
        "total": len(tasks),
        "tasks": tasks
    }


@app.get('/tasks/{task_id}')
def get_single_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasks[task_id]
    status = "done" if task["is_done"] else "not done yet"

    return {
        "id": task_id,
        "name": task["name"],
        "is_done": task["is_done"],
        "status": status
    }


@app.post('/tasks', status_code=201)
def create_task(task: Task):
    if not task.name.strip():
        raise HTTPException(status_code=400, detail="Task name cannot be empty")

    task_dict = task.dict()
    tasks.append(task_dict)

    return {
        "message": "Task created successfully",
        "task": task_dict,
        "total_tasks": len(tasks)
    }

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = tasks.pop(task_id)
    return {
        "message": "Task deleted",
        "deleted_task": deleted_task,
        "remaining_tasks": len(tasks)
    }

@app.put('/tasks/{task_id}')
def update_task(task_id: int, task: Task):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    tasks[task_id] = task.dict()
    return {
        "message": "Task updated",
        "task": tasks[task_id]
    }