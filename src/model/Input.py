import typing
from .LogicComponent import LogicComponent

class Input(LogicComponent):

    def __init__(self):
        super().__init__()
        self.state: bool = False
        #Inputs are always empty for Input component
        self.inputs = {} # Input has no inputs
        self.outputs: typing.List["LogicComponent"] = []
        self.id = LogicComponent.id
        LogicComponent.id +=1
        # Default state for components with one output: (0,1) = (value, bitlength)
        self.state: dict = {"outValue": (0,1)} 


    def eval(self) -> bool:
        return True

    def cycleBitwidth(self):
        switch={
            1: 8,
            8: 32,
            32: 1
        }

        # Resetting the value is handled in InputGridItem
        self.state["outValue"] = [0, switch.get(self.state["outValue"][1])]

    def toggleState(self):
        if self.state["outValue"] == (0,1):
            self.state["outValue"] = (1,1)
        else:
            self.state["outValue"] = (0,1)

    def enteredState(self, inputInt: int):
        if self.state["outValue"][1] == 8 and inputInt > 255:
            inputInt = 255

        outWidth = self.state["outValue"][1]
        self.setState((inputInt, outWidth))

    def setState(self, state: tuple):
        self.state["outValue"] = state
        
    def getState(self) -> dict:
        return self.state