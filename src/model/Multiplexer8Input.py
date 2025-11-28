import  typing
from .LogicComponent import LogicComponent

# ===== AI NOTE =====
# Some lines of code in this class were coded using AI to streamline the development process, but never entire code sections.
# Those lines of code make up less than 10% of the code and everything was peer-reviewed by humans and changes were made for fine-tuning.
# ===================

class Multiplexer8Inp(LogicComponent):
    """ 8-input Multiplexer that selects one of the eight inputs based on a 3-bit selection input. """

    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {
            "selection": None, 
            "input1": None, 
            "input2": None, 
            "input3": None, 
            "input4": None,
            "input5": None, 
            "input6": None, 
            "input7": None, 
            "input8": None}
        
        self.inputBitwidths: typing.Dict = {
            "selection": 3, 
            "input1": 0, 
            "input2": 0, 
            "input3": 0, 
            "input4": 0,
            "input5": 0, 
            "input6": 0, 
            "input7": 0, 
            "input8": 0}
        
        self.state: typing.Dict = {"outputValue": (0, 0)}
        #   If the state ever has a bit length of 0 then it failed to evaluate


    def getOutputBitwidth(self)-> int:
        """returns the bitwidth of the outputs

        Returns:
            int: the bitwidth of the input
        """

        #   Note: Does not account for mismatched widths
        outputs: typing.List = self.getOutputs()

        if len(outputs) == 0: return self.getBitwidth("input1")

        return outputs[0][0].getBitwidth(outputs[0][1])
    
    def addInput(self, input: "LogicComponent", key: str, internalKey: str)-> bool:
        """
        Add an input connection to this component and lock input bidwidth if not already done.
        Args:
            input (LogicComponent): The input component to be added.
            key (str): The key of the output from the input component that is connected.
            internalKey (str): The internal key of this component where the input is connected.
        Returns:
            bool: True if the input was added successfully, False if the input failed to add
        """

        #   Redundant(?) check to ensure that the selection value isn't too big for the multiplexer
        #   we subtract 2 from the inputs length to exclude selection and to counter length starting from 1
        #   Here it ensures that the value is either 0 or 1, we handle transforming this into something usable in eval()
        if internalKey == "selection" and input.getState()[key][0] > (len(self.inputs) - 2):
            return False
        
        #   Generalized check for comparing new input bitwidth to what is permitted
        #   If the input bitwidth is not what is set then we reject it, unless it is not set yet
        if self.getBitwidth(internalKey) != 0 and self.getBitwidth(internalKey) != input.getState()[key][1]:
            return False

        try:
            success: int = super().addInput(input, key, internalKey)

        #   Should be fine to just have this print the error
        #   Wouldn't be visible to the user anyways, I dont think
        except KeyError:
            print(KeyError)
            return False

        #   If the bitwidth has not been set but the input succeeded, set bandwidth to match the new input
        if self.getBitwidth(internalKey) == 0 and success:
            inputBitwidth: int = input.getState()[key][1]
            self.inputBitwidths: typing.Dict = {
                "selection": 3, 
                "input1": inputBitwidth, 
                "input2": inputBitwidth, 
                "input3": inputBitwidth, 
                "input4": inputBitwidth,
                "input5": inputBitwidth, 
                "input6": inputBitwidth, 
                "input7": inputBitwidth, 
                "input8": inputBitwidth}

        return success
    
    def addOutput(self, output, key) -> bool:
        """
        Add an output connection to this component and lock bitwidths if not already done.
        Args:
            output (LogicComponent): The output component to be added.
            key (str): The key of the input from the output component.
        Returns:
            bool: True if the output was added successfully, False if the input failed to add
        """

        bitwidth: int = self.getOutputBitwidth()

        #   Reject mismatches, bitwidth locking occurs after connecting to avoid potential locks with no connection to disconnect
        if bitwidth != 0 and output.inputBitwidths[key] != bitwidth:
            return False

        super().addOutput(output, key)

        if bitwidth == 0:
            bitwidth = self.getOutputBitwidth()
            self.inputBitwidths: typing.Dict = {
                "selection": 3, 
                "input1": bitwidth, 
                "input2": bitwidth, 
                "input3": bitwidth, 
                "input4": bitwidth,
                "input5": bitwidth, 
                "input6": bitwidth, 
                "input7": bitwidth, 
                "input8": bitwidth}
        
        return True
    
    def removeInput(self, input: "LogicComponent", key:str, internalKey: str)-> bool:
        """
        Remove an input connection from this component, resets input bitwidth if all inputs are disconnected.
        Args:
            input (LogicComponent): The input component to be removed.
            key (str): The key of the output from the input component that is connected.
            internalKey (str): The internal key of this component where the input is connected.
        Returns:
            bool: True if removal succeeded, False otherwise
        """  
        try:
            super().removeInput(input, key, internalKey)

        except KeyError:
            print(KeyError)
            return False
        
        #   The rest of this code handles resetting bidwidths 
        empty: bool = True
        for input in self.inputs:
            if self.inputs[input] is not None and input != "selection":
                empty = False
                break

        if empty == True:
            self.inputBitwidths: typing.Dict = {
                "selection": 3, 
                "input1": 0, 
                "input2": 0, 
                "input3": 0, 
                "input4": 0,
                "input5": 0, 
                "input6": 0, 
                "input7": 0, 
                "input8": 0}
            self.state: typing.Dict = {"outputValue": (0, 0)}
        
        return True
    
    def removeOutput(self, output: "LogicComponent", key: str)-> bool:
        """
        Remove an output connection from this component, resets all bitwidths if nothing is connected.
        Args:
            output (str): The output to be disconnected
            key (str): The key of the input from the output component.
        Returns:
            bool: True if removal succeeded, False otherwise
        """  

        super().removeOutput(output, key)
    
        #   The rest of this code handles resetting bidwidths 
        empty: bool = True
        for input in self.inputs:
            if self.inputs[input] is not None and input != "selection":
                empty = False
                break

        if len(self.outputs) != 0:
            empty = False

        if empty == True:
            self.inputBitwidths: typing.Dict = {
                "selection": 3, 
                "input1": 0, 
                "input2": 0, 
                "input3": 0, 
                "input4": 0,
                "input5": 0, 
                "input6": 0, 
                "input7": 0, 
                "input8": 0}
            self.state: typing.Dict = {"outputValue": (0, 0)}
        
        return True

    def eval(self) -> bool:
        """Evaluate the multiplexer, and returns if the output has changed.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """

        oldState: bool = self.state.copy()
        
        # Add all (non selection) inputs to a list
        inputVals: list = []
        for input in self.inputs:
            if input == "selection": continue

            if self.inputs[input] == None: inputVals.append(0)
            else: inputVals.append(self.inputs[input][0].getState()[self.inputs[input][1]][0])
        
        # Get the value of selection to use in the choice
        if self.inputs["selection"] == None: s = 0
        else:
            s = int(self.inputs["selection"][0].getState()[self.inputs["selection"][1]][0])

        # Pick the right output value from the list
        self.state = {"outputValue": (inputVals[s], self.inputBitwidths[(f"input" + str(s+1))])}

        #   Check to see if data has changed
        if (self.state["outputValue"] == oldState):
            return False
        else:
            return True
