import  typing
from .LogicComponent import LogicComponent

class Collector1to6(LogicComponent):
    """ Collector that collects six 1-bit inputs into a single 6-bit output. """
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None, "input2": None, "input4": None, "input8": None,
                                   "input16": None, "input32": None}
        self.inputBitwidths: typing.Dict = {"input1": 1, "input2": 1, "input4": 1, "input8": 1,
                                            "input16": 1, "input32": 1}
        # Collector has exactly eight inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0,6)}
        
    def eval(self) -> bool:
        """Evaluate the Collector, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        outValue = 0
        for i,value in enumerate(self.inputs.values()):
            if value is None: # set input to false if no component is connected
                bit = 0
            else:
                bit = value[0].getState()[value[1]][0]
                # gets the component out of the tuple in self.inputs and then 
                #   uses the key from that tuple to access the right output from the 
                #   components state
            outValue |= (bit << (i))
        self.state["outValue"] = (outValue, 6)
        if self.state != oldState:
            return True
        else:
            return False
    