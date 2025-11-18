import typing
from .LogicComponent import LogicComponent


class Collector1to3(LogicComponent):
    """Collector that combines three 1-bit inputs into one 3-bit output.

    Outputs `outValue` as a tuple (value:int, bitwidth:int) where bit 0 is from
    `input1` and bit 1 is from `input2` , bit 2 is from `input3` (i.e. input1 -> LSB, input3 -> MSB).
    """

    def __init__(self):
        super().__init__()
        # Two 1-bit inputs. Each entry is either None or a tuple (component, output_key)
        self.inputs: typing.Dict = {"input1": None, "input2": None, "input4": None}
        self.inputBitwidths: typing.Dict = {"input1": 1, "input2": 1, "input4": 1}
        # Output stored as (value, bitwidth)
        self.state: dict = {"outValue": (0, 3)}

    def eval(self) -> bool:
        """Evaluate the Collector, and return if the Output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        oldState = self.state.copy()
        outValue: int = 0
        for i,value in enumerate(self.inputs.values()):
            if value is None: # set input to false if no component is connected
                bit: int = 0
            else:
                bit: int = value[0].getState()[value[1]][0]
                # gets the component out of the tuple in self.inputs and then 
                #   uses the key from that tuple to access the right output from the 
                #   components state
            # shift the bit into the correct position and combine
            outValue |= (bit << (i))
        self.state["outValue"] = (outValue, 3)
        if self.state != oldState:
            return True
        else:
            return False