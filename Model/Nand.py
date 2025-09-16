import  typing
from .LogicComponent import LogicComponent

class Nand(LogicComponent):

    def eval(self) -> bool:
        """Evaluate the NAND gate, and return if the Output has changed.

        Raises:
            ValueError: If the number of inputs is not exactly two.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state["outValue"]
        if len(self.inputs) != 2:
            raise ValueError("NAND gate must have exactly two inputs.")
        # NAND logic: output is False only if both inputs are True
        a = self.inputs[0].getState()
        b = self.inputs[1].getState()
        self.state["outValue"] = not (a and b)
        if self.state["outValue"] != oldState:
            return True
        else:
            return False