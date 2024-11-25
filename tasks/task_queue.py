from typing import Dict, Optional
import uuid

class Task:
    def __init__(self, data: Dict[str, str]) -> None:
        self.id = str(uuid.uuid4())
        self.data = data
        self.status = 'pending'

class TaskQueue:
    def __init__(self) -> None:
        self.tasks: Dict[str, Task] = {}

    def add_task(self, data: Dict[str, str]) -> str:
        task = Task(data)
        self.tasks[task.id] = task
        return task.id

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def delete_task(self, task_id: str) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False