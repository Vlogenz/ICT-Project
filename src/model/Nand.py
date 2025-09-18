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
        oldState = self.state.copy()
        if len(self.inputs) != 2:
            raise ValueError("NAND gate must have exactly two inputs.")
        a = self.inputs[0].getState()["outValue"][0]
        b = self.inputs[1].getState()["outValue"][0]
        if a and b:
            self.state["outValue"] = (0,1)
        else:
            self.state["outValue"] = (1,1)
        if self.state != oldState:
            return True
        else:
            return False