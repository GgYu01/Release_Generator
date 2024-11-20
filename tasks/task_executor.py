# tasks/task_executor.py
"""
Executes the task logic.
"""

import threading
import uuid
from typing import Dict
from core.release_note_writer import ReleaseNoteWriter
from utils.logger import get_logger

logger = get_logger(__name__)


class TaskExecutor:
    """
    Executes tasks and manages their state.
    """

    def __init__(self):
        self.tasks = {}

    def create_task(self) -> str:
        """
        Creates and starts a new task.

        :return: Task ID.
        """
        task_id = str(uuid.uuid4())
        task_thread = threading.Thread(target=self.execute_task, args=(task_id,))
        self.tasks[task_id] = {"thread": task_thread, "status": "running"}
        task_thread.start()
        return task_id

    def execute_task(self, task_id: str):
        """
        Executes the task logic.

        :param task_id: ID of the task.
        """
        logger.info(f"Executing task {task_id}")
        # Implement the task logic here
        # For demonstration, we'll just sleep
        import time
        time.sleep(5)
        self.tasks[task_id]["status"] = "completed"
        logger.info(f"Task {task_id} completed.")

    def get_tasks_status(self) -> Dict[str, str]:
        """
        Gets the status of all tasks.

        :return: Dictionary of task IDs and their statuses.
        """
        return {task_id: info["status"] for task_id, info in self.tasks.items()}

    def stop_task(self, task_id: str) -> Dict[str, str]:
        """
        Stops a running task.

        :param task_id: ID of the task.
        """
        if task_id in self.tasks:
            # Note: Stopping threads in Python is not straightforward.
            # This is just a placeholder.
            self.tasks[task_id]["status"] = "stopped"
            logger.info(f"Task {task_id} stopped.")
            return {"task_id": task_id, "status": "Task stopped."}
        else:
            return {"error": "Task not found."}

    def delete_task(self, task_id: str) -> Dict[str, str]:
        """
        Deletes a task.

        :param task_id: ID of the task.
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            logger.info(f"Task {task_id} deleted.")
            return {"task_id": task_id, "status": "Task deleted."}
        else:
            return {"error": "Task not found."}
