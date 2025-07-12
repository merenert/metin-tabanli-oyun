from collections import defaultdict
from typing import Callable, Any

class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable[[Any], None]):
        self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable):
        if callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(callback)

    def publish(self, event_name: str, data: Any = None):
        for callback in self._subscribers.get(event_name, []):
            callback(data)

# Global event bus örneği
event_bus = EventBus()