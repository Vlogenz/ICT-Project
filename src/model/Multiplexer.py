import  typing
from .LogicComponent import LogicComponent

class Multiplexer2Inp(LogicComponent):

    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"selection": None, "input1": None, "input2": None}
        self.inputBitwidths: typing.Dict = {"selection": 1, "input1": 0, "input2": 0}
        self.state: typing.Dict = {"outputValue": (0, 0)}
        #   If the state ever has a bit length of 0 then it failed to evaluate
        #   



    def addInput(self, input: "LogicComponent", key: str, internalKey: str):
        """
        Add an input connection to this component and lock input bidwidth if not already done.
        Args:
            input (LogicComponent): The input component to be added.
            key (str): The key of the output from the input component that is connected.
            internalKey (str): The internal key of this component where the input is connected.
        Returns:
            bool: True if the input was added successfully, False if the input failed to add
        """

        try:
            success: int = super().addInput(input, key, internalKey)

        #   Should be fine to just have this print the error
        #   Wouldn't be visible to the user anyways, I dont think
        except KeyError:
            print(KeyError)
            return False

        #   If the bitwidth has not been set but the input succeeded, set bandwidth to match the new input
        if self.getBitwidth(internalKey) == 0 and success:
            inputBitwidth: int = input.getBitwidth(key)
            self.inputBitwidths: typing.Dict = {"selection": 1, "input1": inputBitwidth, "input2": inputBitwidth}

        return success
    
    def eval(self) -> bool:
        """Evaluate the multiplexer, and returns if the output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        
        oldState: bool = self.state.copy()
        for input in self.inputs:
            if self.inputs[input] is None:
                return False
            
        outputKey: str = "input" + (self.inputs["selection"][0].getState()[self.inputs["selection"][1]] + 1)
        # gets the component out of the first tuple in self.inputs and then 
        #   uses the key from that tuple to access the right output from the 
        #   components state

        self.state = {"outputValue": (self.inputs[outputKey][0].getState()[self.inputs[outputKey][1]], self.inputs[outputKey][0].getBitwidth([self.inputs[outputKey][1]]))}
        # gets the component out of the tuple determined by the selection input, then 
        #   uses the key from that tuple to access the right output from the 
        #   components state
        #   Does the same for getting the bit width

        #   Check to see if data has changed
        if (self.state["outputValue"] == oldState):
            return False
        else:
            return True


        





