from src.model import LogicComponent


class CustomLogicComponent(LogicComponent):
    """A custom component made by the user"""

    def __init__(self, inputMap: dict, outputMap: dict):
        super().__init__()
        for key, bitwidth in inputMap:
            self.inputs[key] = None
            self.inputBitwidths[key] = bitwidth
        for key, bitwidth in outputMap:
            self.state[key] = (0, bitwidth)

    def eval(self) -> bool:
        #TODO: Here we have to find a way to evaluate all sub-components.
        # - Add the components directly to LogicComponentController?
        pass
