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
        
        oldState = self.state
        if len(self.inputs) != 1:
            raise ValueError("NOT gate must have exactly one input.")
        self.state = not self.inputs[0].getState()
        if self.state != oldState:
            return True
        else:  
            return False