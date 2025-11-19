import typing
from .LogicComponent import LogicComponent

class InstructionMemory(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs = {"readAddress": None} 
        self.inputBitwidths: typing.Dict = {"readAddress": 32}
        # Half Adder has exactly two inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"instruction": (0,32)}  
        self.instructionList: typing.List = [] # List of instructions stored in memory
        
    def eval(self) -> bool:
        """Evaluate the Instruction Memory, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        if self.inputs["readAddress"] is None: # set input to zero if no component is connected
            address: int = 0
        else:
            address: int = self.inputs["readAddress"][0].getState()[self.inputs["readAddress"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        
        address = address // 4  # Convert byte address to word address
        if address < len(self.instructionList):
            instruction: int = self.instructionList[address]
        else:
            instruction: int = 0  # Default instruction if address is out of range
        self.state = {
            "instruction": (instruction, 32)
        }
        if self.state != oldState:
            return True
        else:
            return False    
    
    def loadInstructions(self, instructions: typing.List[int]) -> None:
        """Load a list of instructions into the instruction memory.

        Args:
            instructions (typing.List[int]): List of instructions to load.
        """
        self.instructionList = instructions

     