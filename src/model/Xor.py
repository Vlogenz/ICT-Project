import typing
from .LogicComponent import LogicComponent

class Xor(LogicComponent):
    """ XOR gate that outputs 1 if exactly one of the 1-bit inputs is 1, otherwise outputs 0. """

    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None, "input2": None}
        self.inputBitwidths: typing.Dict = {"input1": 1, "input2": 1}
        # XOR gate has exactly two inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0,1)}
    
    def eval(self) -> bool:
        """Evaluate the XOR gate, and return if the Output has changed.

		Returns:
			bool: True if the output state has changed, False otherwise.
		"""
        oldState = self.state.copy()
        if self.inputs["input1"] is None: # set input to false if no component is connected
            a: int = 0
        else:
            a: int = self.inputs["input1"][0].getState()[self.inputs["input1"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        if self.inputs["input2"] is None: # set input to false if no component is connected
            b: int = 0
        else:
            b: int = self.inputs["input2"][0].getState()[self.inputs["input2"][1]][0]
            # gets the component out of the second tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        if a != b:
            self.state["outValue"] = (1,1)
        else:
            self.state["outValue"] = (0,1)
        if self.state != oldState:
            return True
        else:
            return False