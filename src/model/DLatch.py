import typing
from .LogicComponent import LogicComponent

class DLatch(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"C": None, "D": None} # C = clock, D = data
        self.inputBitwidths: typing.Dict = {"C": 1, "D": 1}
        # D latch has exactly two inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"Q": (0,1),
                            "!Q": (1,1)} # Q = output, !Q = inverted output
    
    def eval(self) -> bool:
        """Evaluate the D latch, and return if the Output has changed.

		Returns:
			bool: True if the output state has changed, False otherwise.
		"""
        oldState = self.state.copy()
        if self.inputs["C"] is None: # set input to false if no component is connected
            c = False
        else:
            c = self.inputs["C"][0].getState()[self.inputs["C"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        if self.inputs["D"] is None: # set input to false if no component is connected
            d = False
        else:
            d = self.inputs["D"][0].getState()[self.inputs["D"][1]][0]
            # gets the component out of the second tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        if c: # if clock is high, set output to D
            oldState = self.state.copy()
            self.state["Q"] = (d,1)
            self.state["!Q"] = (1 - d,1)
            if self.state != oldState:
                return True
            else:
                return False
        else: # if clock is low, keep output
            return False