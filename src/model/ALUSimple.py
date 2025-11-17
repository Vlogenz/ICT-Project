import  typing
from .LogicComponent import LogicComponent

class ALUSimple(LogicComponent):  # A simple 32-bit ALU 
    """ A 32-bit ALU that supports AND, OR, and ADD operations with input inversion."""
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None, "input2": None, "OP": None, "Ainvert": None, "Binvert": None, "CarryIn": None}
        self.inputBitwidths: typing.Dict = {"input1": 32, "input2": 32, "OP": 2, "Ainvert": 1, "Binvert": 1, "CarryIn": 1}
        self.state: dict = {"outValue": (0,32)}
    
    def eval(self) -> bool:
        """Evaluate the ALU, and return if the Output has changed.

        input1 and input2 are 32-bit integers that will be operated on.
        OP will control which operation is performed:
            00 = AND
            01 = OR
            10 = ADD (SUB is supported through Binvert + CarryIn)
        
        Ainvert and Binvert control input inversion:
            0 = input stays the same
            1 = input is inverted (bitwise NOT)
        
        CarryIn adds an extra +1 to ADD operations:
            0 = no carry in
            1 = add +1 to the result (enables two's complement subtraction with Binvert)

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        if self.inputs["input1"] is None: # set input to 0 if no component is connected
            a: int = 0
        else:
            a: int = self.inputs["input1"][0].getState()[self.inputs["input1"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        if self.inputs["input2"] is None: # set input to 0 if no component is connected
            b: int = 0
        else:
            b: int = self.inputs["input2"][0].getState()[self.inputs["input2"][1]][0]
            # gets the component out of the second tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        if self.inputs["OP"] is None: # set input to 0 if no component is connected
            op: int = 0
        else:
            op: int = self.inputs["OP"][0].getState()[self.inputs["OP"][1]][0]
            # gets the component out of the third tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        
        # Handle Ainvert input
        if self.inputs["Ainvert"] is None:
            ainvert: int = 0
        else:
            ainvert: int = self.inputs["Ainvert"][0].getState()[self.inputs["Ainvert"][1]][0]

        # Handle Binvert input
        if self.inputs["Binvert"] is None:
            binvert: int = 0
        else:
            binvert: int = self.inputs["Binvert"][0].getState()[self.inputs["Binvert"][1]][0]
        
        # Handle CarryIn input
        if self.inputs["CarryIn"] is None:
            carryin: int = 0
        else:
            carryin: int = self.inputs["CarryIn"][0].getState()[self.inputs["CarryIn"][1]][0]

        # Apply inversion if needed
        if ainvert == 1:
            a = (~a) & 0xFFFFFFFF  # Bitwise NOT and mask to 32 bits (necessary because ~a produces negative numbers)
        if binvert == 1:
            b = (~b) & 0xFFFFFFFF  # Bitwise NOT and mask to 32 bits (necessary because ~b produces negative numbers)
            
        if op == 0:       # AND
            self.state["outValue"] = (a & b, 32)
        elif op == 1:     # OR
            self.state["outValue"] = (a | b, 32)
        elif op == 2:     # ADD
            result = a + b + carryin  # Add carry-in for two's complement operations
            # Mask to simulate 32-bit overflow behavior
            self.state["outValue"] = (result & 0xFFFFFFFF, 32)
        else:             # Invalid OP code
            raise ValueError(f"Invalid OP code: {op}. Supported codes are 0 (AND), 1 (OR), 2 (ADD).")
        
        if self.state != oldState:
            return True
        else:
            return False
