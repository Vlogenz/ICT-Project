
import typing
from .LogicComponent import LogicComponent

class HalfAdder(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs = {"inputA": None, "inputB": None} # Half Adder has exactly two inputs
        self.state: dict = {"sum": (0,1),
                            "carry": (0,1)}  

    def eval(self) -> bool:
        """Evaluate the Half Adder, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        if self.inputs["inputA"] is None:
            a = False
        else:
            a = self.inputs["inputA"][0].getState()[self.inputs["inputA"][1]][0]
        
        if self.inputs["inputB"] is None:
            b = False
        else:
            b = self.inputs["inputB"][0].getState()[self.inputs["inputB"][1]][0]
        self.state = {
            "sum": (1,1) if a != b else (0,1),
            "carry": (1,1) if a and b else (0,1)
        }
        if self.state != oldState:
            return True
        else:
            return False