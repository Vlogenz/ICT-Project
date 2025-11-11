import typing
from .LogicComponent import LogicComponent

class DataMemory(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs = {"address": None,"writeData": None,"memWrite": None,"memRead": None} 
        self.inputBitwidths: typing.Dict = {"address": 32,"writeData": 32,"memWrite": 1,"memRead": 1}
        # Half Adder has exactly two inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"readData": (0,32)}  
        self.dataList: typing.List = [0 for _ in range(128)] # List of data stored in memory

    def eval(self) -> bool:
        """Evaluate the Data Memory, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        if self.inputs["address"] is None: # set input to zero if no component is connected
            address = 0
        else:
            address = self.inputs["address"][0].getState()[self.inputs["address"][1]][0]
            # gets the component out of the first tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state

        address = address // 4  # Convert byte address to word address
        if address < len(self.dataList):
            data = self.dataList[address]
        else:
            data = 0  # Default data if address is out of range
        self.state = {
            "readData": (data, 32)
        }
        return True

    def loadData(self, data: typing.List[int]) -> None:
        """Load a list of data into the data memory.

        Args:
            data (typing.List[int]): List of data to load.
        """
        self.dataList = data
