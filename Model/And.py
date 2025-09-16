import  typing
from .LogicComponent import LogicComponent

class And(LogicComponent):

    def eval(self) -> bool:
        """Evaluate the AND gate, and return if the Output has changed.

        Raises:
            ValueError: If the number of inputs is not exactly two.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state["outValue"]
        if len(self.inputs) != 2:
            raise ValueError("AND gate must have exactly two inputs.")
        a = self.inputs[0].getState()
        b = self.inputs[1].getState()
        self.state["outValue"] = a and b
        if self.state["outValue"] != oldState:
            return True
        else:
            return False