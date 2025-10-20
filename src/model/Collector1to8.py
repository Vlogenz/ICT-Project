import  typing
from .LogicComponent import LogicComponent

class Collector1to8(LogicComponent):
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None, "input2": None, "input3": None, "input4": None,
                                   "input5": None, "input6": None, "input7": None, "input8": None}
        self.inputBitwidths: typing.Dict = {"input1": 1, "input2": 1, "input3": 1, "input4": 1,
                                            "input5": 1, "input6": 1, "input7": 1, "input8": 1}
        # Collector has exactly eight inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0,8)}
        
    def eval(self):
        """Evaluate the Collector, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        outValue = 0
        for i in range(1,9):
            if self.inputs[f"input{i}"] is None: # set input to false if no component is connected
                bit = 0
            else:
                bit = self.inputs[f"input{i}"][0].getState()[self.inputs[f"input{i}"][1]][0]
                # gets the component out of the tuple in self.inputs and then 
                #   uses the key from that tuple to access the right output from the 
                #   components state
            outValue |= (bit << (i-1))
        self.state["outValue"] = (outValue, 8)
        if self.state != oldState:
            return True
        else:
            return False
    