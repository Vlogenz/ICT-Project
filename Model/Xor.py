import typing
from .LogicComponent import LogicComponent

class Xor(LogicComponent):

    def eval(self) -> bool:
        """Evaluate the XOR gate, and return if the Output has changed.

        Raises:
            ValueError: If the number of inputs is not exactly two.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        
        oldState = self.state["outValue"]
        if len(self.inputs) != 2:
            raise ValueError("OR gate must have exactly two inputs.")
        # XOR logic: output True if exactly one input is True
        a = self.inputs[0].getState()
        b = self.inputs[1].getState()
        self.state["outValue"] = (a != b)
        if self.state["outValue"] != oldState:
            return True
        else:  
            return False