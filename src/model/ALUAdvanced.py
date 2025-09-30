import  typing
from .LogicComponent import LogicComponent

class ALUAdvanced(LogicComponent):  # A simple 32-bit ALU 
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None, "input2": None, "OP": None, "Ainvert": None, "Bnegate": None}
        self.inputBitwidths: typing.Dict = {"input1": 32, "input2": 32, "OP": 2, "Ainvert": 1, "Bnegate": 1}
        self.state: dict = {"outValue": (0,32), "zero": (0,1)}
    
    def eval(self) -> bool:
        """Evaluate the ALU, and return if the Output has changed.

        input1 and input2 are 32-bit integers that will be operated on.
        OP will control which operation is performed:
            00 = AND
            01 = OR
            10 = ADD (SUB is supported through Bnegate)
            11 = SLT (Set on Less Than)
        
        Ainvert controls input1 inversion:
            0 = input1 stays the same
            1 = input1 is inverted (bitwise NOT)
                    
        Bnegate controls input2 negation for subtraction:
            0 = input2 stays the same (normal operation)
            1 = input2 is two's complement negated (enables subtraction: input1 - input2)

        Outputs:
            outValue: 32-bit result of the operation
            zero: 1 if outValue is 0, 0 otherwise (used for beq instruction)

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        if self.inputs["input1"] is None: # set input to 0 if no component is connected
            a = 0
        else:
            a = self.inputs["input1"][0].getState()[self.inputs["input1"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        if self.inputs["input2"] is None: # set input to 0 if no component is connected
            b = 0
        else:
            b = self.inputs["input2"][0].getState()[self.inputs["input2"][1]][0]
            # gets the component out of the second tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        if self.inputs["OP"] is None: # set input to 0 if no component is connected
            op = 0
        else:
            op = self.inputs["OP"][0].getState()[self.inputs["OP"][1]][0]
            # gets the component out of the third tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
        
        # Handle Ainvert input
        if self.inputs["Ainvert"] is None:
            ainvert = 0
        else:
            ainvert = self.inputs["Ainvert"][0].getState()[self.inputs["Ainvert"][1]][0]
        
        # Handle Bnegate input
        if self.inputs["Bnegate"] is None:
            bnegate = 0
        else:
            bnegate = self.inputs["Bnegate"][0].getState()[self.inputs["Bnegate"][1]][0]
        
        # Apply inversion if needed
        if ainvert == 1:
            a = (~a) & 0xFFFFFFFF  # Bitwise NOT and mask to 32 bits
        if bnegate == 1:
            b = (~b + 1) & 0xFFFFFFFF  # in comparisson to ALUSimple: +1 is necessary, as we removed CarryIn and now Bnegate implies (the now removed) CarryIn = 1

       
        if op == 0:       # AND
            self.state["outValue"] = (a & b, 32)
        elif op == 1:     # OR
            self.state["outValue"] = (a | b, 32)
        elif op == 2:     # ADD
            result = a + b  # Addition (subtraction handled by Bnegate)
            # Mask to simulate 32-bit overflow behavior
            self.state["outValue"] = (result & 0xFFFFFFFF, 32)
        elif op == 3:  # SLT (Set on Less Than)
            # Convert to signed 32-bit integers for proper comparison
            signed_a = a if a < 0x80000000 else a - 0x100000000
            signed_b = b if b < 0x80000000 else b - 0x100000000
            self.state["outValue"] = (1 if signed_a < signed_b else 0, 32)
        else:  # Invalid OP code
            raise ValueError(f"Invalid OP code: {op}. Supported codes are 0 (AND), 1 (OR), 2 (ADD), 3 (SLT).")
        
        # Set zero output - 1 if result is 0, 0 otherwise
        self.state["zero"] = (1 if self.state["outValue"][0] == 0 else 0, 1)
        
        if self.state != oldState:
            return True
        else:
            return False