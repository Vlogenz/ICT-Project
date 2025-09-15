import typing
from .LogicComponent import LogicComponent

class Input(LogicComponent):

    def __init__(self):
        self.outputs: typing.List["LogicComponent"] = []
        # Input doesnt have inputs
        self.state: bool = False

    def eval(self) -> bool:
        return self.state
    

    def toggleState(self):
        self.state = not self.state

    def setState(self, state: bool):
        self.state = state