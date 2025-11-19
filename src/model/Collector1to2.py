import typing
from .LogicComponent import LogicComponent


class Collector1to2(LogicComponent):
    """Collector that combines two 1-bit inputs into one 2-bit output.

    Outputs `outValue` as a tuple (value:int, bitwidth:int) where bit 0 is from
    `input1` and bit 1 is from `input2` (i.e. input1 -> LSB, input2 -> MSB).
    """

    def __init__(self):
        super().__init__()
        # Two 1-bit inputs. Each entry is either None or a tuple (component, output_key)
        self.inputs: typing.Dict = {"input1": None, "input2": None}
        self.inputBitwidths: typing.Dict = {"input1": 1, "input2": 1}
        # Output stored as (value, bitwidth)
        self.state: dict = {"outValue": (0, 2)}

    def eval(self) -> bool:
        """Evaluate the Collector, and return True if the Output has changed.

        The two inputs are read; if an input is not connected it is treated as 0.
        The resulting 2-bit integer is stored in self.state['outValue'] as
        (value, 2).
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
        self.state["outValue"] = (outValue, 2)
        if self.state != oldState:
            return True
        else:
            return False
