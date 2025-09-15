import  typing
from .LogicComponent import LogicComponent

class And(LogicComponent):

    def eval(self) -> bool:
        if len(self.inputs) != 2:
            raise ValueError("AND gate must have exactly two inputs.")
        if self.inputs[0].eval() and self.inputs[1].eval():
            return True
        else:
            return False