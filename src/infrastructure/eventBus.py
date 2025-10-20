from collections import defaultdict

class EventBus:
    """
    A lightweight event bus for subscribing to and emitting events.
    """
    def __init__(self):
        self._subs = defaultdict(list)
        self.manual = False
        
    def subscribe(self, event, handler):
        """Subscribe a handler to an event."""
        self._subs[event].append(handler)
        
    
    def emit(self, event, *args, **kwargs):
        if not self.manual:
            for h in list(self._subs.get(event, [])):
                h(*args, **kwargs)
    
    # for testing and step by step
    def setManual(self):
        self.manual = True
    
    def setAuto(self):
        self.manual = False
            

_bus = None

def getBus() -> EventBus:
    """Lazily provide a global bus instance."""
    global _bus
    if _bus is None:
        _bus = EventBus()
    return _bus

def setBus(bus: EventBus):
    """Replace the global bus instance
    Don't do this unless you really know what you're doing."""
    global _bus
    _bus = bus
