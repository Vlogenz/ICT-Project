import typing
from .LogicComponent import LogicComponent

class RegisterBlock(LogicComponent):
    """ Register Block component with read and write capabilities. """

    def __init__(self):
        super().__init__()
        self.inputs = {"readReg1": None,"readReg2": None,"writeReg": None,"writeData": None,"regWrite": None} 
        self.inputBitwidths: typing.Dict = {"readReg1": 5, "readReg2": 5, "writeReg": 5 , "writeData": 32, "regWrite": 1}
        # Half Adder has exactly two inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"readData1": (0,32), "readData2": (0,32)}  
        self.registers: typing.List = [0 for i in range(20)] # List of instructions stored in memory
        
    

    def eval(self) -> bool:
        """Evaluate the Register Block, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        
        # Read register addresses
        if self.inputs["readReg1"] is None:
            readReg1: int = 0
        else:
            readReg1:int = self.inputs["readReg1"][0].getState()[self.inputs["readReg1"][1]][0]
        
        if self.inputs["readReg2"] is None:
            readReg2: int = 0
        else:
            readReg2: int = self.inputs["readReg2"][0].getState()[self.inputs["readReg2"][1]][0]
        
        
        
        # Read data from registers
        readData1: int = self.registers[readReg1] if readReg1 < len(self.registers) else 0
        readData2: int = self.registers[readReg2] if readReg2 < len(self.registers) else 0

        self.state = {
            "readData1": (readData1, 32),
            "readData2": (readData2, 32)
        }
        
        return True
    
    def updateRegisterValues(self):
        # Write operation
        if self.inputs["regWrite"] is not None:
            regWrite = self.inputs["regWrite"][0].getState()[self.inputs["regWrite"][1]][0]
            if regWrite == 1:
                if self.inputs["writeReg"] is not None and self.inputs["writeData"] is not None:
                    writeReg = self.inputs["writeReg"][0].getState()[self.inputs["writeReg"][1]][0]
                    writeData = self.inputs["writeData"][0].getState()[self.inputs["writeData"][1]][0]
                    if writeReg < len(self.registers):
                        self.registers[writeReg] = writeData