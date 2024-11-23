# tasks/task_queue.py

from threading import Lock
from typing import Dict, List
from tasks.task import Task, TaskStatus
from utils.logger import get_logger

logger = get_logger(__name__)


class TaskQueue:
    """
    Class representing the task queue.
    
    Manages task addition, retrieval, and status updates.
    """

    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._queue: List[Task] = []
        self._lock = Lock()

    def add_task(self, task: Task):
        """Add a task to the queue."""
        with self._lock:
            self._tasks[task.id] = task
            self._queue.append(task)
            logger.info(f"Task {task.id} added to the queue.")

    def get_task(self, task_id: str) -> Task:
        """Retrieve a task by its ID."""
        with self._lock:
            return self._tasks.get(task_id)

    def remove_task(self, task_id: str):
        """Remove a task from the queue and task list."""
        with self._lock:
            task = self._tasks.pop(task_id, None)
            if task and task in self._queue:
                self._queue.remove(task)
                logger.info(f"Task {task_id} removed from the queue.")

    def get_all_tasks(self) -> List[Task]:
        """Get a list of all tasks."""
        with self._lock:
            return list(self._tasks.values())

    def get_pending_tasks(self) -> List[Task]:
        """Get a list of pending tasks."""
        with self._lock:
            return [task for task in self._queue if task.status == TaskStatus.PENDING]

    def update_task_status(self, task_id: str, status: TaskStatus):
        """Update the status of a task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                task.status = status
                logger.info(f"Task {task_id} status updated to {status.name}.")

    def stop_task(self, task_id: str):
        """Stop a running task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if task and task.status == TaskStatus.RUNNING:
                # Implement task stopping logic if possible
                task.status = TaskStatus.STOPPED
                logger.info(f"Task {task_id} has been stopped.")

    def clear_completed_tasks(self):
        """Remove completed tasks from the queue and task list."""
        with self._lock:
            completed_tasks = [task_id for task_id, task in self._tasks.items()
                               if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.STOPPED]]
            for task_id in completed_tasks:
                self.remove_task(task_id)