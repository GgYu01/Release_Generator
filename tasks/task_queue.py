# -*- coding: utf-8 -*-

"""
Module for managing task queues and statuses.
"""

from queue import Queue
from threading import Thread
from utils.logger import logger
from typing import Dict

class TaskQueue:
    def __init__(self):
        self.queue = Queue()
        self.tasks: Dict[int, Dict] = {}
        self.task_id_counter = 0

    def add_task(self):
        self.task_id_counter += 1
        task_id = self.task_id_counter
        task = Thread(target=self.execute_task, args=(task_id,))
        self.tasks[task_id] = {'thread': task, 'status': 'pending'}
        task.start()
        logger.info(f"Task {task_id} started")
        return task_id

    def execute_task(self, task_id: int):
        self.tasks[task_id]['status'] = 'running'
        try:
            # Placeholder for actual task execution logic
            # For example, call the main script logic here
            # This should be replaced with actual implementation
            import main
            main.main()
            self.tasks[task_id]['status'] = 'completed'
            logger.info(f"Task {task_id} completed")
        except Exception as e:
            self.tasks[task_id]['status'] = 'failed'
            logger.error(f"Task {task_id} failed with error: {e}")

    def get_status(self, task_id: int) -> str:
        return self.tasks.get(task_id, {}).get('status', 'unknown')

    def stop_task(self, task_id: int) -> bool:
        task = self.tasks.get(task_id)
        if task and task['status'] == 'running':
            # Implement task stopping logic if possible
            # Python threads cannot be forcefully stopped, so this might require task cooperation
            self.tasks[task_id]['status'] = 'stopped'
            logger.info(f"Task {task_id} stopped")
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            logger.info(f"Task {task_id} deleted")
            return True
        return False
