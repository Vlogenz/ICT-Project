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
        old_state = self.state
        if len(self.inputs) != 2:
            raise ValueError("AND gate must have exactly two inputs.")
        if self.inputs[0].eval() and self.inputs[1].eval():
            self.state = True
        else:
            self.state = False
        if self.state != old_state:
            return True
        else:
            return False