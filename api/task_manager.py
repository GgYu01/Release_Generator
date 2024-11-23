# api/task_manager.py

"""
Task Management API endpoints.

Supports creating, querying, stopping, and deleting tasks.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict
import uuid
from tasks.task_queue import task_queue, TaskStatus
from tasks.task_executor import execute_task
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/create", summary="Create a new task")
async def create_task(task_type: str, parameters: Dict = None):
    """
    Create a new task and add it to the task queue.

    :param task_type: Type of the task to create
    :param parameters: Optional parameters for the task
    :return: Task ID and status
    """
    try:
        task_id = str(uuid.uuid4())
        task_info = {
            "id": task_id,
            "type": task_type,
            "status": TaskStatus.PENDING,
            "parameters": parameters or {},
        }
        task_queue.add_task(task_info)
        logger.info(f"Created new task with ID {task_id}")
        return {"task_id": task_id, "status": task_info["status"]}
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{task_id}", summary="Get task status")
async def get_task_status(task_id: str):
    """
    Retrieve the status of a task.

    :param task_id: ID of the task
    :return: Task status and details
    """
    try:
        task_info = task_queue.get_task(task_id)
        if not task_info:
            logger.error(f"Task not found: {task_id}")
            raise HTTPException(status_code=404, detail="Task not found")
        return {"task_id": task_id, "status": task_info["status"], "details": task_info}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error retrieving task status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop/{task_id}", summary="Stop a running task")
async def stop_task(task_id: str):
    """
    Stop a running task.

    :param task_id: ID of the task to stop
    :return: Success message
    """
    try:
        result = task_queue.stop_task(task_id)
        if result:
            logger.info(f"Stopped task {task_id}")
            return {"message": "Task stopped successfully"}
        else:
            logger.error(f"Task not found or cannot stop: {task_id}")
            raise HTTPException(status_code=404, detail="Task not found or cannot be stopped")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error stopping task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{task_id}", summary="Delete a task")
async def delete_task(task_id: str):
    """
    Delete a task from the queue.

    :param task_id: ID of the task to delete
    :return: Success message
    """
    try:
        result = task_queue.delete_task(task_id)
        if result:
            logger.info(f"Deleted task {task_id}")
            return {"message": "Task deleted successfully"}
        else:
            logger.error(f"Task not found or cannot delete: {task_id}")
            raise HTTPException(status_code=404, detail="Task not found or cannot be deleted")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        raise HTTPException(status_code=500, detail=str(e))