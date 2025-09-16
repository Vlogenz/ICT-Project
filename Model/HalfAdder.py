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
        oldState = self.state
        if len(self.inputs) != 2:
            raise ValueError("Half Adder must have exactly two inputs.")
        # Half Adder logic: sum is True if exactly one input is True
        a = self.inputs[0].getState()
        b = self.inputs[1].getState()
        self.state = {"sum": (a != b), "carry": (a and b)}
        if self.state != oldState:
            return True
        else:
            return False