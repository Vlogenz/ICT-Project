import typing
from .LogicComponent import LogicComponent

class Splitter32to8(LogicComponent):
    """ Splitter32to8 Logic Component
    Splits a 32-bit input into four 8-bit outputs."""
    
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None}
        self.inputBitwidths: typing.Dict = {"input1": 32}
        # Splitter has exactly one 32-bit input and four 8-bit outputs
        self.state: dict = {"outValue1": (0, 8), "outValue2": (0, 8), "outValue3": (0, 8), "outValue4": (0, 8)}

    def eval(self) -> bool:
        """Evaluate the Splitter, and return if any Output has changed.

        Returns:
            bool: True if any output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        
        if self.inputs["input1"] is None:  # set input to zero if no component is connected
            inValue: int = 0
        else:
            inValue: int = self.inputs["input1"][0].getState()[self.inputs["input1"][1]][0]
            # gets the component out of the tuple in self.inputs and then
            #   uses the key from that tuple to access the right output from the
            #   components state
        
        # Split the 32-bit input into four 8-bit outputs
        for i, key in enumerate(self.state.keys()):
            # Extract the 8-bit value for this output
            # outValue1 -> bits 0-7, outValue2 -> bits 8-15, outValue3 -> bits 16-23, outValue4 -> bits 24-31
            byte_value = (inValue >> (i * 8)) & 0xFF
            self.state[key] = (byte_value, 8)

        if self.state != oldState:
            return True
        else:
            return False