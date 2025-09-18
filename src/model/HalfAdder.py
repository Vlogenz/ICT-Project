
import typing
from .LogicComponent import LogicComponent

class HalfAdder(LogicComponent):

    def __init__(self):
        super().__init__()
        self.state: dict = {"sum": False,
                            "carry": False}  

    def eval(self) -> bool:
        """Evaluate the Half Adder, and return if the Output has changed.
        Raises:
            ValueError: If the number of inputs is not exactly two.
        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        if len(self.inputs) != 2:
            raise ValueError("Half Adder must have exactly two inputs.")
        a = self.inputs[0].getState()["outValue"][0]
        b = self.inputs[1].getState()["outValue"][0]
        self.state = {
            "sum": (1,1) if a != b else (0,1),
            "carry": (1,1) if a and b else (0,1)
        }
        if self.state != oldState:
            return True
        else:
            return False