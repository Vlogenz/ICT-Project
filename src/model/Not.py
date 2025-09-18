import typing
from .LogicComponent import LogicComponent

class Not(LogicComponent):

    def eval(self) -> bool:
        """Evaluate the NOT gate, and return if the Output has changed.

        Raises:
            ValueError: If the number of inputs is not exactly one.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        
        oldState = self.state.copy()
        if len(self.inputs) != 1:
            raise ValueError("NOT gate must have exactly one input.")
        a = self.inputs[0].getState()["outValue"][0]
        if a == 0:
            self.state["outValue"] = (1,1)
        else:
            self.state["outValue"] = (0,1)
        if self.state != oldState:
            return True
        else:
            return False