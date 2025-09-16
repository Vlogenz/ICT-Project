
import typing
from .LogicComponent import LogicComponent

class Connector():

    bitWidth: int = 0 
    origin: LogicComponent = None
    destination: typing.List[LogicComponent] = None

    def __init__(self):
        self.origin = None
        self.destination = None 
        self.bitWidth = 1

    def setBitWidth(self, bitWidth: int):
        self.bitWidth = bitWidth

    def getBitWidth(self) -> int:
        return self.bitWidth
    

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