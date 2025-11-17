import typing
from .LogicComponent import LogicComponent

class Register(LogicComponent):
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input": None, "clk": None} 
        self.inputBitwidths: typing.Dict = {"input": 32, "clk": 1}
        # Register has exactly two inputs (data and clock)
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0,32)}  # Initial state
        self.nextState = (0,32)  # Next state to be loaded
        self.needNewState = False
    
    def eval(self) -> bool:
        """Evaluate the register state based on the input state.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        if self.inputs["clk"] is not None and self.inputs["clk"][0].getState()[self.inputs["clk"][1]][0] == 1:
            if self.inputs["input"] is None: # set input to zero if no component is connected
                value = 0
            else:
                value = self.inputs["input"][0].getState()[self.inputs["input"][1]][0]
                # gets the component out of the first tuple in self.inputs and then 
                #   uses the key from that tuple to access the right output from the 
                #   components state
            self.nextState = (value, 32)
            self.needNewState = True
        
        return False
    
    def updateState(self)-> bool:
        """Update the register state to the next state.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        if self.needNewState:
            self.state = {"outValue": self.nextState}
            self.needNewState = False
        return False
