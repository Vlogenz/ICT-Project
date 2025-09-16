import typing
from .LogicComponent import LogicComponent

class Output(LogicComponent):

    # in addition to the LogicComponent attributes, it has a state attribute
    def __init__(self):
        super().__init__()

    def eval(self) -> bool:
        """Evaluate the output state based on the input state.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        old_state = self.state
        self.state = self.inputs[0].getState()

        if self.state != old_state:
            return True
        else:
            return False
