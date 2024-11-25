from typing import Callable, Dict, List

class EventBus:
    def __init__(self) -> None:
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, listener: Callable) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def publish(self, event_type: str, data) -> None:
        for listener in self.listeners.get(event_type, []):
            listener(data)