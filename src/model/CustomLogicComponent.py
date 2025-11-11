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
        self.name = componentData.name
        for key, bitwidth in componentData.inputMap.items():
            self.inputs[key] = None
            self.inputBitwidths[key] = bitwidth
        for key, bitwidth in componentData.outputMap.items():
            self.state[key] = (0, bitwidth)
        self.childComponents = [COMPONENT_MAP[className]() for className in componentData.components]
        for connection in componentData.connections:
            srcComp = self.childComponents[connection["from"]["component"]]
            dstComp = self.childComponents[connection["to"]["component"]]
            srcComp.addOutput(dstComp, connection["to"]["input"])
            dstComp.addInput(srcComp, connection["from"]["output"], connection["to"]["input"])

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

        returnValue = False
        if Algorithms.khanFrontierEval(inputComponents, self.childComponents):
            returnValue = True
        elif Algorithms.eventDrivenEval(inputComponents, self.childComponents):
            returnValue = True
        self.mapToState()
        return returnValue

    def mapToState(self):
        outputComponents = [comp for comp in self.childComponents if isinstance(comp, Output)]
        for i, key in enumerate(self.state.keys()):
            self.state[key] = outputComponents[i].getState()["outValue"]

