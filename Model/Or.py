import typing
from .LogicComponent import LogicComponent

class Or(   LogicComponent):
    
    def eval(self) -> bool:
        """Evaluate the OR gate, and return if the Output has changed.

        Raises:
            ValueError: If the number of inputs is not exactly two.

        Returns:
            bool: True if the output state has changed, False otherwise.
        """
        
        oldState = self.state["outValue"]
        if len(self.inputs) != 2:
            raise ValueError("OR gate must have exactly two inputs.")
        if self.inputs[0].getState() or self.inputs[1].getState():
            self.state["outValue"] = True
        else:
            self.state["outValue"] = False
        if self.state["outValue"] != oldState:
            return True
        else:  
            return False