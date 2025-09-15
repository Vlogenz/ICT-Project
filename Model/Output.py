import typing
from .LogicComponent import LogicComponent

class Output(LogicComponent):

    # in addition to the LogicComponent attributes, it has a state attribute
    def __init__(self):
        super().__init__()
        state: bool = False

    def eval(self) -> bool:
        self.state = self.inputs[0].eval()
        return self.state
    



