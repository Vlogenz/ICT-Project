import typing
from .LogicComponent import LogicComponent

class Collector8to32(LogicComponent):
    """ Collector that combines four 8-bit inputs into one 32-bit output."""
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None, "input2": None, "input3": None, "input4": None}
        self.inputBitwidths: typing.Dict = {"input1": 8, "input2": 8, "input3": 8, "input4": 8}
        # Collector has exactly four 8-bit inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0, 32)}
        
    def eval(self) -> bool:
        """Evaluate the Collector, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        outValue: int = 0
        for i,value in enumerate(self.inputs.values()):
            if value is None: # set input to false if no component is connected
                bit: int = 0
            else:
                bit: int = value[0].getState()[value[1]][0]
                # gets the component out of the tuple in self.inputs and then 
                #   uses the key from that tuple to access the right output from the 
                #   components state
            # shift the bits into the correct position and combine
            outValue |= (bit << (i*8))
        self.state["outValue"] = (outValue, 32)
        if self.state != oldState:
            return True
        else:
            return False