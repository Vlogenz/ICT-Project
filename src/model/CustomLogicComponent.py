from src.Algorithms import Algorithms
from src.model import LogicComponent
from src.model.CustomLogicComponentData import CustomLogicComponentData
from src.model.Input import Input
from src.model.Output import Output
from src.constants import COMPONENT_MAP

class CustomLogicComponent(LogicComponent):
    """A custom component made by the user"""

    def __init__(self, componentData: CustomLogicComponentData):
        super().__init__()
        self.customComponentName = componentData.name
        for key, bitwidth in componentData.inputMap.items():
            self.inputs[key] = None
            self.inputBitwidths[key] = bitwidth
        for key, bitwidth in componentData.outputMap.items():
            self.state[key] = (0, bitwidth)
        self.childComponents = [COMPONENT_MAP[className]() for className in componentData.components]
        for connection in componentData.connections:
            srcComp = self.childComponents[connection["origin"]]
            dstComp = self.childComponents[connection["destination"]]
            srcComp.addOutput(dstComp, connection["destinationKey"])
            dstComp.addInput(srcComp, connection["originKey"], connection["destinationKey"])

    def eval(self) -> bool:
        """Evaluates all child components in order

        Returns:
          Bool: True if evaluation was successful, false if not.
        """
        # Filter child components to get only Input components
        inputComponents = [comp for comp in self.childComponents if isinstance(comp, Input)]

        # Map external input values to internal inputs
        for i, externalInput in enumerate(self.inputs.values()):
            if externalInput is not None:
                inputComponents[i].setState(externalInput[0].getState()["outValue"])

        # Internal evaluation
        returnValue = False
        if Algorithms.khanFrontierEval(inputComponents, self.childComponents):
            returnValue = True
        elif Algorithms.eventDrivenEval(inputComponents, self.childComponents):
            returnValue = True

        # Map internal output values to state
        outputComponents = [comp for comp in self.childComponents if isinstance(comp, Output)]
        for i, key in enumerate(self.state.keys()):
            self.state[key] = outputComponents[i].getState()["outValue"]

        return returnValue
