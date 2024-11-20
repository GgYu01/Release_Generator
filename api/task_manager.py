# -*- coding: utf-8 -*-

"""
FastAPI router for task management.
"""

from fastapi import APIRouter
from tasks.task_queue import TaskQueue

router = APIRouter()
task_queue = TaskQueue()

@router.post("/start")
async def start_task():
    task_id = task_queue.add_task()
    return {"task_id": task_id}

@router.get("/status/{task_id}")
async def get_task_status(task_id: int):
    status = task_queue.get_status(task_id)
    return {"task_id": task_id, "status": status}

@router.post("/stop/{task_id}")
async def stop_task(task_id: int):
    result = task_queue.stop_task(task_id)
    return {"task_id": task_id, "stopped": result}

@router.delete("/delete/{task_id}")
async def delete_task(task_id: int):
    result = task_queue.delete_task(task_id)
    return {"task_id": task_id, "deleted": result}
