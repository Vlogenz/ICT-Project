import typing
from .LogicComponent import LogicComponent

class Input(LogicComponent):

    def __init__(self):
        self.state: bool = False
        #Inputs are always empty for Input component
        self.outputs: typing.List["LogicComponent"] = []
        self.id = LogicComponent.id
        LogicComponent.id +=1
        # Default state for components with one output: (0,1) = (value, bitlength)
        self.state: dict = {"outValue": (0,1)} 


    def eval(self) -> bool:
        return True

    def toggleState(self):
        if self.state["outValue"] == (0,1):
            self.state["outValue"] = (1,1)
        else:
            self.state["outValue"] = (0,1)

    def setState(self, state: tuple):
        self.state["outValue"] = state