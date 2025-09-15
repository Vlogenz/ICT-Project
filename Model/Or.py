import typing
from .LogicComponent import LogicComponent

class Or(   LogicComponent):
    
    def eval(self) -> bool:
        if len(self.inputs) != 2:
            raise ValueError("OR gate must have exactly two inputs.")
        if self.inputs[0].eval() or self.inputs[1].eval():
            return True
        else:
            return False