import typing
from .LogicComponent import LogicComponent

class EncoderEightBit(LogicComponent):
    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None, "input2": None, "input3": None,"input4": None,
                            "input5": None,"input6": None,"input7": None,"input8": None}
        self.inputBitwidths: typing.Dict = {"input1": 1, "input2": 1, "input3": 1,"input4": 1,
                            "input5": 1,"input6": 1,"input7": 1,"input8": 1} 
        self.state: dict = {"outValue1": (0,1), "outValue2": (0,1), "outValue3": (0,1)}   # Initial state
    
    def eval(self) -> bool:
        """Evaluate the encoder state based on the input state.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        old_state = self.state.copy()

        # Find which input is active (set to 1)
        active_index = None
        for i in range(1, 9):
            input_name = f"input{i}"
            input_conn = self.inputs.get(input_name)
            if input_conn is not None:
                value = input_conn[0].getState()[input_conn[1]][0]
                if value == 1:
                    active_index = i - 1  # zero-based index
                    break

        if active_index is not None:
            self.state["outValue3"] = ((active_index >> 2) & 1, 1)
            self.state["outValue2"] = ((active_index >> 1) & 1, 1)
            self.state["outValue1"] = (active_index & 1, 1)
        else:
            self.state["outValue3"] = (0, 1)
            self.state["outValue2"] = (0, 1)
            self.state["outValue1"] = (0, 1)

        return self.state != old_state
        
        
        
        