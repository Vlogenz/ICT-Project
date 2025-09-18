import  typing
from .LogicComponent import LogicComponent

class Nand(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None, "input2": None} # NAND gate has exactly two inputs
        self.state: dict = {"outValue": (1,1)}
    
    def eval(self) -> bool:
        """Evaluate the NAND gate, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        if self.inputs["input1"] is None:
            a = False
        else:
            a = self.inputs["input1"][0].getState()[self.inputs["input1"][1]][0]
        if self.inputs["input2"] is None:
            b = False
        else:
            b = self.inputs["input2"][0].getState()[self.inputs["input2"][1]][0]
        if a and b:
            self.state["outValue"] = (0,1)
        else:
            self.state["outValue"] = (1,1)
        if self.state != oldState:
            return True
        else:
            return False