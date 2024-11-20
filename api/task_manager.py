# api/task_manager.py
"""
Task management interfaces.
"""

from fastapi import APIRouter, BackgroundTasks
from tasks.task_executor import TaskExecutor
from tasks.task_queue import task_queue
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()
executor = TaskExecutor()


@router.post("/tasks/start")
async def start_task():
    """
    Starts a new task.
    """
    task_id = executor.create_task()
    logger.info(f"Started task with ID: {task_id}")
    return {"task_id": task_id, "status": "Task started."}


@router.get("/tasks/status")
async def get_tasks_status():
    """
    Retrieves the status of all tasks.
    """
    tasks_status = executor.get_tasks_status()
    return tasks_status


@router.post("/tasks/stop/{task_id}")
async def stop_task(task_id: str):
    """
    Stops a running task.

    :param task_id: ID of the task to stop.
    """
    result = executor.stop_task(task_id)
    return result


@router.delete("/tasks/delete/{task_id}")
async def delete_task(task_id: str):
    """
    Deletes a task.

    :param task_id: ID of the task to delete.
    """
    result = executor.delete_task(task_id)
    return result
