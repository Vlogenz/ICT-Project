import typing
from .LogicComponent import LogicComponent



class FullAdder(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs = {"A": None, "B": None, "Cin": None}  # A = input1, B = input2, Cin = carry-in
        self.inputBitwidths = {"A": 1, "B": 1, "Cin": 1}
        self.state = {"Sum": (0, 1), "Cout": (0, 1)}  # Sum = output, Cout = carry-out

    def eval(self) -> bool:
        """Evaluate the Full Adder, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        
        oldState = self.state.copy()
        if self.inputs["A"] is None: # set input to false if no component is connected
            a = False
        else:
            a = self.inputs["A"][0].getState()[self.inputs["A"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state

        if self.inputs["B"] is None: # set input to false if no component is connected
            b = False
        else:
            b = self.inputs["B"][0].getState()[self.inputs["B"][1]][0]
            # gets the component out of the second tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state
        if self.inputs["Cin"] is None: # set input to false if no component is connected
            cin = False
        else:
            cin = self.inputs["Cin"][0].getState()[self.inputs["Cin"][1]][0]
            # gets the component out of the third tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state
        self.state = {
            "Sum": ((a + b + cin) % 2, 1),  # Sum is 1 if the total number of 1s is odd
            "Cout": ((a + b + cin) // 2, 1)  # Cout is 1 if two or more inputs are 1
        }
        if self.state != oldState:
            return True
        else:
            return False