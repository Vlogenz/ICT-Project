import typing
from .LogicComponent import LogicComponent

class Not(LogicComponent):

    def eval(self) -> bool:
        if len(self.inputs) != 1:
            raise ValueError("NOT gate must have exactly one input.")
        return not self.inputs[0].eval()