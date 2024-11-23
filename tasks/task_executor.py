# tasks/task_executor.py

import threading
import time
from tasks.task_queue import TaskQueue
from tasks.task import TaskStatus
from utils.logger import get_logger

logger = get_logger(__name__)


class TaskExecutor:
    """
    Class responsible for executing tasks from the task queue.
    
    Runs in a separate thread and processes tasks in order.
    """

    def __init__(self, task_queue: TaskQueue):
        self.task_queue = task_queue
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info("TaskExecutor thread started.")

    def _run(self):
        """Internal method to run tasks in the queue."""
        while not self._stop_event.is_set():
            pending_tasks = self.task_queue.get_pending_tasks()
            if not pending_tasks:
                time.sleep(1)  # Wait before checking again
                continue
            task = pending_tasks[0]
            logger.info(f"Executing task {task.id} ({task.name}).")
            task.run()
            if task.status == TaskStatus.COMPLETED:
                logger.info(f"Task {task.id} completed successfully.")
            elif task.status == TaskStatus.FAILED:
                logger.error(f"Task {task.id} failed with error: {task.error}")
            # Optionally remove task after execution
            # self.task_queue.remove_task(task.id)

    def stop(self):
        """Stop the task executor thread."""
        self._stop_event.set()
        self._thread.join()
        logger.info("TaskExecutor thread stopped.")

    def is_running(self) -> bool:
        """Check if the executor thread is running."""
        return self._thread.is_alive()