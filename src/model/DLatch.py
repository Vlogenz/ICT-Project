import typing
from .LogicComponent import LogicComponent

class DLatch(LogicComponent):
    """ D Latch that stores a 1-bit value based on clock and data inputs."""

    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"inputC": None, "inputD": None} # C = clock, D = data
        self.inputBitwidths: typing.Dict = {"inputC": 1, "inputD": 1}
        # D latch has exactly two inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outQ": (0,1),
                            "out!Q": (1,1)} # Q = output, !Q = inverted output
    
    def eval(self) -> bool:
        """Evaluate the D latch, and return if the Output has changed.

		Returns:
			bool: True if the output state has changed, False otherwise.
		"""
        oldState = self.state.copy()
        if self.inputs["inputC"] is None: # set input to false if no component is connected
            c: int = 0
        else:
            c: int = self.inputs["inputC"][0].getState()[self.inputs["inputC"][1]][0]
            # gets the component out of the first tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state
        if self.inputs["inputD"] is None: # set input to false if no component is connected
            d: int = 0
        else:
            d: int = self.inputs["inputD"][0].getState()[self.inputs["inputD"][1]][0]
            # gets the component out of the second tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        if c == 1: # if clock is high, set output to D
            oldState = self.state.copy()
            self.state["outQ"] = (d,1)
            self.state["out!Q"] = (1 - d,1)
            if self.state != oldState:
                return True
            else:
                return False
        else: # if clock is low, keep output
            return False