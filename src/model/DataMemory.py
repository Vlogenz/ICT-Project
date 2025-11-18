import typing
from .LogicComponent import LogicComponent

class DataMemory(LogicComponent):
    """ Data Memory component that can read and write 32-bit data. """

    def __init__(self):
        super().__init__()
        self.inputs = {"address": None,"writeData": None,"memWrite": None,"memRead": None} 
        self.inputBitwidths: typing.Dict = {"address": 32,"writeData": 32,"memWrite": 1,"memRead": 1}
        # Data Memory has exactly four inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"readData": (0,32)}  
        self.dataList: typing.List = [0 for _ in range(128)] # List of data stored in memory

    def eval(self) -> bool:
        """Evaluate the Data Memory, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        if self.inputs["memWrite"] is not None:
            memWrite: int = self.inputs["memWrite"][0].getState()[self.inputs["memWrite"][1]][0]
        else:
            memWrite: int = 0  # Default to no write if no component is connected
        if self.inputs["memRead"] is not None:
            memRead: int = self.inputs["memRead"][0].getState()[self.inputs["memRead"][1]][0]
        else:
            memRead: int = 0  # Default to no read if no component is connected
        if memRead and memWrite:
            raise ValueError("DataMemory cannot read and write at the same time.")
        if self.inputs["address"] is None: # set input to zero if no component is connected
            address: int = 0
        else:
            address: int = self.inputs["address"][0].getState()[self.inputs["address"][1]][0]
            # gets the component out of the first tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state
        address = address // 4  # Convert byte address to word address
        if memWrite:
            if self.inputs["writeData"] is None: # set input to zero if no component is connected
                writeData: int = 0
            else:
                writeData: int = self.inputs["writeData"][0].getState()[self.inputs["writeData"][1]][0]
                # gets the component out of the first tuple in self.inputs and then
                #   uses the key from that tuple to access the right output from the
                #   components state
            # Write data to memory
            if address < len(self.dataList) and address >= 0:
                self.dataList[address] = writeData
            return False  # No output change on write
        

        if memRead:
            if address < len(self.dataList) and address >= 0:
                data = self.dataList[address]
            else:
                data = 0  # Default data if address is out of range
            self.state = {
                "readData": (data, 32)
            }
            return True

    def loadData(self, data: typing.List[int]) -> None:
        """Load a list of data into the data memory.
           Only for testing and level initialization.

        Args:
            data (typing.List[int]): List of data to load.
        """
        self.dataList = data
