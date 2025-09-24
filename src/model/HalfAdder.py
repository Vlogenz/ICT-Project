
import typing
from .LogicComponent import LogicComponent

class HalfAdder(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs = {"inputA": None, "inputB": None} 
        self.inputBitwidths: typing.Dict = {"inputA": 1, "inputB": 1}
        # Half Adder has exactly two inputs
        #   (Tuples of component and output key of that component)
        self.state: dict = {"sum": (0,1),
                            "carry": (0,1)}  

    def eval(self) -> bool:
        """Evaluate the Half Adder, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        if self.inputs["inputA"] is None: # set input to false if no component is connected
            a = False
        else:
            a = self.inputs["inputA"][0].getState()[self.inputs["inputA"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        
        if self.inputs["inputB"] is None: # set input to false if no component is connected
            b = False
        else:
            b = self.inputs["inputB"][0].getState()[self.inputs["inputB"][1]][0]
            # gets the component out of the second tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        self.state = {
            "sum": (1,1) if a != b else (0,1),
            "carry": (1,1) if a and b else (0,1)
        }
        if self.state != oldState:
            return True
        else:
            return False