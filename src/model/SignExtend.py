import typing
from .LogicComponent import LogicComponent

class SignExtend(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None} 
        self.inputBitwidths: typing.Dict = {"input1": 16}
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0,1)}
    
    def eval(self) -> bool:
        """Evaluate the SignExtend, and return if the Output has changed.

		Returns:
			bool: True if the output state has changed, False otherwise.
		"""
        oldState = self.state.copy()
        if self.inputs["input1"] is None: # set input to false if no component is connected
            a = False
        else:
            a = self.inputs["input1"][0].getState()[self.inputs["input1"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        self.state["outValue"] = (a,32) # sign-extend to 32 bits
        if self.state != oldState:
            return True
        else:
            return False