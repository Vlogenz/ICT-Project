import typing
from .LogicComponent import LogicComponent



class ALUControl(LogicComponent):

    "Note: This is a simplified ALU Control Unit for demonstration purposes, and can only support a limited set of operations."

    def __init__(self):
        super().__init__()
        self.inputs = {"ALUop": None, "funct": None}  
        self.inputBitwidths = {"ALUop": 2, "funct": 6}
        self.state = {"ainvert": (0, 1), "binvert": (0, 1), "operation": (0, 2)}  

    def eval(self) -> bool:
        """Evaluate the Control Unit, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()

        if self.inputs["ALUop"] is None or self.inputs["funct"] is None:
            ALUop = 0
        else:
            ALUop = self.inputs["ALUop"][0].getState()[self.inputs["ALUop"][1]][0]
            funct = self.inputs["funct"][0].getState()[self.inputs["funct"][1]][0]
        
        if ALUop == 0:  # lw or sw
            self.state = {
                "ainvert": (0, 1),
                "binvert": (0, 1),
                "operation": (0, 2)  # ADD
            }
        elif ALUop == 1:  # beq
            self.state = {
                "ainvert": (0, 1),
                "binvert": (1, 1),
                "operation": (2, 2)  # SUBTRACT
            }
        
        elif ALUop == 2:  # R-type
            if funct == 0:  # ADD
                self.state = {
                    "ainvert": (0, 1),
                    "binvert": (0, 1),
                    "operation": (2, 2)
                }
            elif funct == 2:  # SUBTRACT
                self.state = {
                    "ainvert": (0, 1),  
                    "binvert": (1, 1),
                    "operation": (2, 2)
                }
            elif funct == 4:  # AND
                self.state = {
                    "ainvert": (0, 1),
                    "binvert": (0, 1),
                    "operation": (0, 2)
                }
            elif funct == 5:  # OR
                self.state = {
                    "ainvert": (0, 1),
                    "binvert": (0, 1),
                    "operation": (1, 2)
                }
            elif funct == 10:  # SLT
                self.state = {
                    "ainvert": (0, 1),
                    "binvert": (1, 1),
                    "operation": (3, 2)  
                }
            else: #Default to ADD for unknown funct
                self.state = {
                    "ainvert": (0, 1),
                    "binvert": (0, 1),
                    "operation": (0, 2)  
                }

        if self.state != oldState:
            return True
        else:
            return False