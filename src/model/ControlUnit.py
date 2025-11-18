import typing
from .LogicComponent import LogicComponent



class ControlUnit(LogicComponent):
    "note that this is a simplified control unit, which can only handle lw, sw, beq and r-type instructions"

    def __init__(self):
        super().__init__()
        self.inputs = {"input": None}  
        self.inputBitwidths = {"input": 6 }
        self.state = {"RegDst": (0, 1), "Branch": (0, 1), "MemRead": (0, 1), "MemtoReg": (0, 1), "AluOp": (0, 2), "MemWrite": (0, 1), "AluSrc": (0, 1), "RegWrite": (0, 1)}  

    def eval(self) -> bool:
        """Evaluate the Control Unit, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()

        if self.inputs["input"] is None:
            opcode = 0
        else:
            opcode = self.inputs["input"][0].getState()[self.inputs["input"][1]][0]

        # R-type instructions
        if opcode == 0:
            self.state = {
                "RegDst": (1, 1),
                "Branch": (0, 1),
                "MemRead": (0, 1),
                "MemtoReg": (0, 1),
                "AluOp": (2, 2),
                "MemWrite": (0, 1),
                "AluSrc": (0, 1),
                "RegWrite": (1, 1)
            }
        # lw instruction
        elif opcode == 35:
            self.state = {
                "RegDst": (0, 1),
                "Branch": (0, 1),
                "MemRead": (1, 1),
                "MemtoReg": (1, 1),
                "AluOp": (0, 2),
                "MemWrite": (0, 1),
                "AluSrc": (1, 1),
                "RegWrite": (1, 1)
            }
        # sw instruction
        elif opcode == 43:
            self.state = {
                "RegDst": (0, 1),  # don't care
                "Branch": (0, 1),
                "MemRead": (0, 1),
                "MemtoReg": (0, 1),  # don't care
                "AluOp": (0, 2),
                "MemWrite": (1, 1),
                "AluSrc": (1, 1),
                "RegWrite": (0, 1)
            }
        # beq instruction
        elif opcode == 4:
            self.state = {
                "RegDst": (0, 1),  # don't care
                "Branch": (1, 1),
                "MemRead": (0, 1),
                "MemtoReg": (0, 1),  # don't care
                "AluOp": (1, 2),
                "MemWrite": (0, 1),
                "AluSrc": (0, 1),
                "RegWrite": (0, 1)
            }
        # unsupported opcode - set all signals to 0
        else:
            self.state = {
                "RegDst": (0, 1),
                "Branch": (0, 1),
                "MemRead": (0, 1),
                "MemtoReg": (0, 1),
                "AluOp": (0, 2),
                "MemWrite": (0, 1),
                "AluSrc": (0, 1),
                "RegWrite": (0, 1)
            }
        if self.state != oldState:
            return True
        else:
            return False