
import typing
from .LogicComponent import LogicComponent

class Connector():

    bitWidth: int
    origin: LogicComponent
    destination: typing.List[LogicComponent]

    def __init__(self):
        self.origin = None
        self.destination = []
        self.bitWidth = 0

    def setBitWidth(self, bitWidth: int):
        self.bitWidth = bitWidth

    def getBitWidth(self) -> int:
        return self.bitWidth
    

    def setOrigin(self, newOrigin: LogicComponent, key:str):
        """Set the origin component of the connector. checks if the bitwidth matches.

        Args:
            origin (LogicComponent): The origin component to set.

        Raises:
            ValueError: If the bitwidth of the origin component does not match the connector's bitwidth.
        """
        if self.bitWidth == 0 or self.bitWidth == newOrigin.getState()[key][1]:
            self.bitWidth = newOrigin.getState()[key][1] # set bitwidth if not set yet
            self.origin = newOrigin
        else:
            raise ValueError("Bitwidth of connector does not match bitwidth of connected components.")
            
    def getOrigin(self) -> LogicComponent:
        return self.origin
    

    def addDestination(self, destination: LogicComponent, key: str):
        """Add a destination component to the connector.

        Args:
            destination (LogicComponent): The destination component to add.
            key (str): The key to access the bitlength ("outValue" in most cases) of the destination component.

        Raises:
            ValueError: If the bitwidth of the destination component does not match the connector's bitwidth.
        """
        if self.bitWidth == 0 or self.bitWidth == destination.getState()[key][1]:
            self.bitWidth = destination.getState()[key][1]
            self.destination.append(destination)
        else:
            raise ValueError("Bitwidth of connector does not match bitwidth of connected components.")

    def removeDestination(self, destination: LogicComponent):
        """ Remove a destination component from the connector.
        Args:
                destination (LogicComponent): The destination component to remove.
            """
        self.destination.remove(destination)
        if len(self.destination) == 0:
            self.bitWidth = 0

    def getDestination(self) -> typing.List[LogicComponent]:
        return self.destination
