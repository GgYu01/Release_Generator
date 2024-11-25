from fastapi import APIRouter
from tasks.task_queue import TaskQueue
from tasks.task_executor import TaskExecutor
from typing import Dict

router = APIRouter()
task_queue = TaskQueue()
task_executor = TaskExecutor(task_queue)

@router.post("/tasks/")
def create_task(task_data: Dict[str, str]) -> dict:
    task_id = task_queue.add_task(task_data)
    return {"task_id": task_id}

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str) -> dict:
    task = task_queue.get_task(task_id)
    if task:
        return {"task_id": task_id, "status": task.status}
    else:
        return {"error": "task not found"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: str) -> dict:
    success = task_queue.delete_task(task_id)
    if success:
        return {"info": f"task '{task_id}' deleted"}
    else:
        return {"error": "task not found"}