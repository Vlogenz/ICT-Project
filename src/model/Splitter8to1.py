import  typing
from .LogicComponent import LogicComponent

class Splitter8to1(LogicComponent):
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None}
        self.inputBitwidths: typing.Dict = {"input1": 8}
        # Splitter has exactly one input and eight outputs
        self.state: dict = {"outValue1": (0,1), "outValue2": (0,1), "outValue3": (0,1), "outValue4": (0,1),
                           "outValue5": (0,1), "outValue6": (0,1), "outValue7": (0,1), "outValue8": (0,1)}
        
    def eval(self):
        """Evaluate the Splitter, and return if any Output has changed.

        Returns:
            bool: True if any output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        if self.inputs["input1"] is None: # set input to zero if no component is connected
            inValue = 0
        else:
            inValue = self.inputs["input1"][0].getState()[self.inputs["input1"][1]][0]
            # gets the component out of the tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        for i in range(1,9):
            bit = (inValue >> (i-1)) & 1
            self.state[f"outValue{i}"] = (bit, 1)
        if self.state != oldState:
            return True
        else:
            return False
