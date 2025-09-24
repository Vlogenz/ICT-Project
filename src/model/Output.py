import typing
from .LogicComponent import LogicComponent

class Output(LogicComponent):
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input": None} 
        self.inputBitwidths: typing.Dict = {"input": 1} 
        # Output has exactly one input
        # (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0,1)}  # Initial state


    def eval(self) -> bool:
        """Evaluate the output state based on the input state.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        old_state = self.state.copy()
        if self.inputs["input"] is None: # set input to false if no component is connected
            value = False
        else:
            value = self.inputs["input"][0].getState()[self.inputs["input"][1]][0]
        # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        self.state = {"outValue": (value, 1)}
        if self.state != old_state:
            return True
        else:
            return False
