# tasks/task.py

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Any, Dict
import uuid


class TaskStatus(Enum):
    """Enumeration of task statuses."""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    STOPPED = auto()


@dataclass
class Task:
    """Class representing a task in the system."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    status: TaskStatus = TaskStatus.PENDING
    function: Callable[..., Any] = None
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    result: Any = None
    error: Exception = None

    def run(self):
        """Execute the task's function with the provided arguments."""
        if self.status in [TaskStatus.COMPLETED, TaskStatus.RUNNING]:
            return
        self.status = TaskStatus.RUNNING
        try:
            self.result = self.function(*self.args, **self.kwargs)
            self.status = TaskStatus.COMPLETED
        except Exception as e:
            self.error = e
            self.status = TaskStatus.FAILED