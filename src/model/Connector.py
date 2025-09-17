
import typing
from .LogicComponent import LogicComponent

class Connector():

    state: bool = False
    origin: LogicComponent = None
    destination: typing.List[LogicComponent] = None

    def __init__(self):
        self.origin = None
        self.destination = None 
        self.state = False

    
    def setState(self, state: bool):
        self.state = state

    def getState(self) -> bool:
        return self.state
    

    def setOrigin(self, origin: LogicComponent):
        self.origin = origin

    def getOrigin(self) -> LogicComponent:
        return self.origin
    

    def addDestination(self, destination: LogicComponent):
        """Add a destination component to the connector.
        Args:
            destination (LogicComponent): The destination component to add.
        """
        self.destination.append(destination)

    def removeDestination(self, destination: LogicComponent):
        """Remove a destination component from the connector.
        Args:
            destination (LogicComponent): The destination component to remove.
        """
        self.destination.remove(destination)

    def getDestination(self) -> typing.List[LogicComponent]:
        return self.destination
