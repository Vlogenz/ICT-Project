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
        
        old_state = self.state
        if len(self.inputs) != 1:
            raise ValueError("NOT gate must have exactly one input.")
        self.state = not self.inputs[0].eval()
        if self.state != old_state:
            return True
        else:  
            return False