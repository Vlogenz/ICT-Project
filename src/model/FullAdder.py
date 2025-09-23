import typing
from .LogicComponent import LogicComponent



class FullAdder(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs = {"inputA": None, "inputB": None, "inputCin": None}  
        self.inputBitwidths = {"inputA": 1, "inputB": 1, "inputCin": 1}
        self.state = {"outSum": (0, 1), "cOut": (0, 1)}  

    def eval(self) -> bool:
        """Evaluate the Full Adder, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        
        oldState = self.state.copy()
        if self.inputs["inputA"] is None: # set input to false if no component is connected
            a = False
        else:
            a = self.inputs["inputA"][0].getState()[self.inputs["inputA"][1]][0]
            # gets the component out of the first tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state

        if self.inputs["inputB"] is None: # set input to false if no component is connected
            b = False
        else:
            b = self.inputs["inputB"][0].getState()[self.inputs["inputB"][1]][0]
            # gets the component out of the second tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state
        if self.inputs["inputCin"] is None: # set input to false if no component is connected
            cin = False
        else:
            cin = self.inputs["inputCin"][0].getState()[self.inputs["inputCin"][1]][0]
            # gets the component out of the third tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state
        self.state = {
            "outSum": ((a + b + cin) % 2, 1),  # Sum is 1 if the total number of 1s is odd
            "cOut": ((a + b + cin) // 2, 1)  # Cout is 1 if two or more inputs are 1
        }
        if self.state != oldState:
            return True
        else:
            return False