import typing
from .LogicComponent import LogicComponent

class Output(LogicComponent):


    def eval(self) -> bool:
        """Evaluate the output state based on the input state.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        old_state = self.state.copy()
        value = self.inputs[0].getState()["outValue"]
        self.state = {"outValue": value}
        if self.state != old_state:
            return True
        else:
            return False
