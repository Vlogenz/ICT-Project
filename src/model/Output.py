import typing
from .LogicComponent import LogicComponent

class Output(LogicComponent):
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input": None}  # Output has exactly one input
        self.state: dict = {"outValue": (0,1)}  # Initial state


    def eval(self) -> bool:
        """Evaluate the output state based on the input state.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        old_state = self.state.copy()
        value = self.inputs["input"][0].getState()[self.inputs["input"][1]][0]
        self.state = {"outValue": (value, 1)}
        if self.state != old_state:
            return True
        else:
            return False
