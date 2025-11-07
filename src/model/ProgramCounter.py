import typing
from .LogicComponent import LogicComponent
from src.infrastructure.eventBus import getBus

class ProgramCounter(LogicComponent):
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input": None}
        self.inputBitwidths: typing.Dict = {"input": 32}
        # ProgramCounter has exactly two inputs (data and clock)
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0,32)}  # Initial state
        self.bus = getBus()
        
        
    def eval(self) -> bool:
        """Evaluate the program counter state based on the input state.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        
        if self.inputs["input"] is None: # set input to zero if no component is connected
            value = 0
        else:
            value = self.inputs["input"][0].getState()[self.inputs["input"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        self.state = {"outValue": (value, 32)}
        self.bus.emit("newCycle")
        return True
           