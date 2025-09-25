import typing
from .LogicComponent import LogicComponent

class ShiftLeft2(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None} 
        self.inputBitwidths: typing.Dict = {"input1": 0}
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0,0)}
    
    def eval(self) -> bool:
        """Evaluate the ShiftLeft2, and return if the Output has changed.

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
        self.state["outValue"] = (a<<2,self.inputBitwidths["input1"]+2) # shift left by 2 bits
        if self.state != oldState:
            return True
        else:
            return False
        
    def addInput(self, input: "LogicComponent", key: str, internalKey: str):
        ret = super().addInput(input,key,internalKey)
        bit = input.getState()[key][1]  # Get bitwidth from the output state
        self.state["outValue"] = (self.state["outValue"][0], bit + 2)
        self.inputBitwidths["input1"] = bit
        return ret
        
    def removeInput(self, input: "LogicComponent", key: str, internalKey: str):
        """Remove an input connection and reset input bitwidths to default values.
        
        Args:
            input (LogicComponent): The input component to be removed.
            key (str): The key of the output from the input component that is connected.
            internalKey (str): The internal key of this component where the input is connected.
        """
        super().removeInput(input, key, internalKey)
        # Reset input bitwidth to default value when input is removed
        # The state will be recalculated by eval() method: (0<<2, 0+2) = (0, 2)
        # or by the next addInput call
        self.inputBitwidths["input1"] = 0  