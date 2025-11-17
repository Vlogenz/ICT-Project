import typing
from .LogicComponent import LogicComponent

class DecoderThreeBit(LogicComponent):
    """3-bit Decoder that decodes three 1-bit inputs into eight 1-bit outputs."""
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None, "input2": None, "input3": None} 
        self.inputBitwidths: typing.Dict = {"input1": 1, "input2": 1, "input3": 1} 
        self.state: dict = {"outValue1": (0, 1), "outValue2": (0, 1), "outValue3": (0, 1),"outValue4": (0, 1),
                            "outValue5": (0, 1),"outValue6": (0, 1),"outValue7": (0, 1),"outValue8": (0, 1)}  # Initial state
    
    def eval(self) -> bool:
        """Evaluate the decoder state based on the input state.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        old_state = self.state.copy()
        
        # Default input values to 0 if not connected
        a: int = 0
        b: int = 0
        c: int = 0

        if self.inputs["input1"] is not None:
            c = self.inputs["input1"][0].getState()[self.inputs["input1"][1]][0]
        
        if self.inputs["input2"] is not None:
            b = self.inputs["input2"][0].getState()[self.inputs["input2"][1]][0]
        
        if self.inputs["input3"] is not None:
            a = self.inputs["input3"][0].getState()[self.inputs["input3"][1]][0]
        
        # calculate the binary value from the three inputs (abc)
        value: int =(a<<2) + (b<<1) + c
        
        # Reset all outputs to 0
        for key in self.state.keys():
            self.state[key] = (0, 1)

        # Set the selected output to 1
        self.state[f"outValue{value + 1}"] = (1, 1)
        if self.state != old_state:
            return True
        else:
            return False