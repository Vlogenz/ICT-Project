import typing
from .LogicComponent import LogicComponent

class ShiftLeft2(LogicComponent):
    """ ShiftLeft2 component that shifts input value left by 2 bits. """

    def __init__(self):
        super().__init__()
        self.inputs: typing.Dict = {"input1": None} 
        self.inputBitwidths: typing.Dict = {"input1": 0}
        #   (Tuples of component and output key of that component)
        self.state: dict = {"outValue": (0,0)}
    
    def eval(self) -> bool:
        """Evaluate the ShiftLeft2, and return if the Output has changed.
        Shifts left by 2 bits and maintains the same bitwidth by cutting off the top 2 bits.

		Returns:
			bool: True if the output state has changed, False otherwise.
		"""
        oldState = self.state.copy()
        if self.inputs["input1"] is None: # set input to false if no component is connected
            a: int = 0
            # If no input connected, keep the configured bitwidth or default to 0
            outputBitwidth = self.inputBitwidths["input1"]
        else:
            a: int = self.inputs["input1"][0].getState()[self.inputs["input1"][1]][0]
            # gets the component out of the first tuple in self.inputs and then 
            #   uses the key from that tuple to access the right output from the 
            #   components state
            outputBitwidth = self.inputBitwidths["input1"]
        
        # Shift left by 2 bits and mask to keep only the bits within the original bitwidth
        shifted_value = a << 2
        if outputBitwidth > 0:
            # Create a mask to keep only the lower 'outputBitwidth' bits
            mask = (1 << outputBitwidth) - 1
            shifted_value = shifted_value & mask
        
        self.state["outValue"] = (shifted_value, outputBitwidth)
        if self.state != oldState:
            return True
        else:
            return False
        
    def addInput(self, input: "LogicComponent", key: str, internalKey: str):
        success = super().addInput(input,key,internalKey)
        if success:  # Input was successfully added to an empty slot
            bit = input.getState()[key][1]  # Get bitwidth from the output state
            self.inputBitwidths["input1"] = bit
            self.state["outValue"] = (self.state["outValue"][0], bit)
        else:
            # Check if we're trying to update an existing connection with same component
            if internalKey in self.inputs and self.inputs[internalKey] is not None:
                current_input, current_key = self.inputs[internalKey]
                if current_input == input and current_key == key:
                    # Update bitwidth for existing connection
                    bit = input.getState()[key][1]
                    self.inputBitwidths["input1"] = bit
                    self.state["outValue"] = (self.state["outValue"][0], bit)
        return ret
        
    def removeInput(self, input: "LogicComponent", key: str, internalKey: str)-> None:
        """Remove an input connection and reset input bitwidths to default values.
        
        Args:
            input (LogicComponent): The input component to be removed.
            key (str): The key of the output from the input component that is connected.
            internalKey (str): The internal key of this component where the input is connected.
        """
        super().removeInput(input, key, internalKey)
        # Reset input bitwidth to default value when input is removed
        if len(self.outputs) == 0:
            self.inputBitwidths["input1"] = 0
            self.state["outValue"] = (0, 0)  # Reset output state to default when input is removed

    def addOutput(self, output: "LogicComponent", key: str)-> None:
        """Add an output connection and update input bitwidth accordingly.
        
        Args:
            output (LogicComponent): The output component to be added.
            key (str): The key of the input from the output component.
        """
        super().addOutput(output, key)
        # Update input bitwidth based on new output state
        if self.inputs["input1"] is None:
            # No input connected: output bitwidth = bitwidth of output component
            self.inputBitwidths["input1"] = output.inputBitwidths[key]
            self.state["outValue"] = (0, output.inputBitwidths[key])

    def removeOutput(self, output: "LogicComponent", key: str)-> None:
        """Remove an output connection and update bitwidths if no outputs remain.
        
        Args:
            output (LogicComponent): The output component to be removed.
            key (str): The input key of the output component.
        """
        super().removeOutput(output, key)
        # If no more outputs and no inputs, reset bitwidth to 0
        if len(self.outputs) == 0 and self.inputs["input1"] is None:
            self.state["outValue"] = (0, 0) 
            self.inputBitwidths["input1"] = 0 