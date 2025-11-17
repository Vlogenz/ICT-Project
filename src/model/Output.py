import typing
from .LogicComponent import LogicComponent

class Output(LogicComponent):
    """ Output component with one input and no outputs. """
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input": None} 
        self.inputBitwidths: typing.Dict = {"input": 0} 
        # Output has exactly one input
        # (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0,0)}  # Initial state


    def eval(self) -> bool:
        """Evaluate the output state based on the input state.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        old_state = self.state.copy()
        if self.inputs["input"] is None: # set input to false if no component is connected
            value: int = 0
        else:
            value: int = self.inputs["input"][0].getState()[self.inputs["input"][1]][0]
        # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        self.state = {"outValue": (value, self.inputBitwidths["input"])}
        if self.state != old_state:
            return True
        else:
            return False
        
    def addInput(self, input, key, internalKey)-> bool:
        """ Add an input to the Output component."""
        success = super().addInput(input, key, internalKey)
        if success:
            self.inputBitwidths["input"] = input.getState()[key][1]
            self.state = {"outValue": (0, self.inputBitwidths["input"])}
        return success
    
    def removeInput(self, input, key, internalKey)-> None:
        """ Remove an input from the Output component."""
        super().removeInput(input, key, internalKey)
        self.inputBitwidths["input"] = 0
        
