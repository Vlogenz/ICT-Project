import typing
from .LogicComponent import LogicComponent

class Collector8to16(LogicComponent):
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None, "input2": None}
        self.inputBitwidths: typing.Dict = {"input1": 8, "input2": 8}
        # Collector has exactly four 8-bit inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0, 16)}
        
    def eval(self):
        """Evaluate the Collector, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        outValue = 0
        
        for i in range(1, 3):
            if self.inputs[f"input{i}"] is None:  # set input to zero if no component is connected
                byte_value = 0
            else:
                byte_value = self.inputs[f"input{i}"][0].getState()[self.inputs[f"input{i}"][1]][0]
                # gets the component out of the tuple in self.inputs and then 
                #   uses the key from that tuple to access the right output from the 
                #   components state
            
            # Shift the 8-bit value to its correct position in the 32-bit output
            # input1 -> bits 0-7, input2 -> bits 8-15, input3 -> bits 16-23, input4 -> bits 24-31
            outValue |= (byte_value << ((i-1) * 8))
        
        self.state["outValue"] = (outValue, 16)
        if self.state != oldState:
            return True
        else:
            return False