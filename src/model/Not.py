import typing
from .LogicComponent import LogicComponent

class Not(LogicComponent):
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input": None} 
        # NOT gate has exactly one input
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (1,1)}

    def eval(self) -> bool:
        """Evaluate the NOT gate, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        
        oldState = self.state.copy()
        if self.inputs["input"] is None: # set input to false if no component ist connected
            a = False
        else:
            a = self.inputs["input"][0].getState()[self.inputs["input"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        if a == 0:
            self.state["outValue"] = (1,1)
        else:
            self.state["outValue"] = (0,1)
        if self.state != oldState:
            return True
        else:
            return False