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

    def eval(self):
        """Evaluate the Collector, and return True if the Output has changed.

        The two inputs are read; if an input is not connected it is treated as 0.
        The resulting 2-bit integer is stored in self.state['outValue'] as
        (value, 2).
        """
        oldState = self.state.copy()
        outValue = 0
        for i in range(1, 3):
            key = f"input{i}"
            if self.inputs[key] is None:
                bit = 0
            else:
                # self.inputs[key] is expected to be (component, output_key)
                comp, out_key = self.inputs[key]
                bit = comp.getState()[out_key][0]
            outValue |= (bit << (i - 1))

        self.state["outValue"] = (outValue, 2)
        return self.state != oldState
