import typing
from .LogicComponent import LogicComponent



class Adder32bit(LogicComponent):
    """ 32-bit Adder that adds two 32-bit inputs and produces a 32-bit output. """

    def __init__(self):
        super().__init__()
        self.inputs = {"inputA": None, "inputB": None, }  
        self.inputBitwidths = {"inputA": 32, "inputB": 32}
        self.state = {"outSum": (0, 32)}  

    def eval(self) -> bool:
        """Evaluate the Full Adder, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        
        oldState = self.state.copy()
        if self.inputs["inputA"] is None: # set input to false if no component is connected
            a: int = 0
        else:
            a: int = self.inputs["inputA"][0].getState()[self.inputs["inputA"][1]][0]
            # gets the component out of the first tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state

        if self.inputs["inputB"] is None: # set input to false if no component is connected
            b: int = 0
        else:
            b: int = self.inputs["inputB"][0].getState()[self.inputs["inputB"][1]][0]
            # gets the component out of the second tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state
        self.state = {
            "outSum": ((a + b), 32)  # Sum is 1 if the total number of 1s is odd
        }
        if self.state != oldState:
            return True
        else:
            return False