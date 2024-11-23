from typing import Callable, Dict, List, Any
from threading import Lock

class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}
        self._lock = Lock()

    def subscribe(self, event_type: str, handler: Callable[[Any], None]) -> None:
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: Any) -> None:
        with self._lock:
            handlers = self._subscribers.get(event_type, []).copy()
        for handler in handlers:
            handler(data)

event_bus = EventBus()

class EventTypes:
    COMMIT_UPDATED = "commit_updated"
    PATCH_GENERATED = "patch_generated"
    RELEASE_NOTE_CREATED = "release_note_created"