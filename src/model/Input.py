import typing
from .LogicComponent import LogicComponent

class Input(LogicComponent):

    def __init__(self):
        super().__init__()
        self.outputs: typing.List["LogicComponent"] = []
        # Input doesnt have inputs


    def eval(self) -> bool:
        return True

    def toggleState(self):
        self.state = not self.state

    def setState(self, state: bool):
        self.state = state