from src.control.LogicComponentController import LogicComponentController
from src.model import DataMemory, InstructionMemory, Register, Input
from src.model.LogicComponent import LogicComponent
from src.infrastructure.eventBus import getBus
from src.constants import COMPONENT_MAP

from typing import List, TypeVar, Type, Tuple

class LevelController:

    def __init__(self, logicComponentController: LogicComponentController, levelData = None, grid = None):
        self.levelData = levelData
        self.logicComponentController = logicComponentController
        self.eventBus = getBus()
        self.currentLevel = None
        self.outputPredictions = []

    def setLevel(self, levelData):
        """Sets the current level data"""
        self.levelData = levelData

    def getLevel(self):
        """Returns the current level data"""
        return self.levelData

    def setGrid(self, grid):
        """Sets the grid to build the level on"""
        self.grid = grid

    def buildLevel(self):
        """Builds the level using level data and emits an event so that the frontend updates as well."""
        self.currentLevel = self.levelData["level_id"]
        components = self.levelData["components"]

        #Info for each component:
        # - comp: the component itself
        # - pos: A Tuple[int,int] representing the cell for the component
        # - immovable: Whether it is immovable or not
        componentInfo: List = []
        for componentData in components:
            component_type_str = componentData["type"]
            
            # Convert string to class
            if component_type_str not in COMPONENT_MAP:
                raise ValueError(f"Unknown component type: {component_type_str}")
            
            component_class = COMPONENT_MAP[component_type_str]
            comp = self.logicComponentController.addLogicComponent(component_class)

            pos = tuple(componentData["position"])
            componentInfo.append({
                "comp": comp,
                "pos": pos,
                "immovable": componentData["immovable"],
                "fixedValue": componentData.get("fixedValue", False)
            })
            
            if type(comp) == Register:
                comp.state = {"outValue": (componentData["initialValue"], 32)}
                
            if type(comp) == Input:
                if "initialBitWidth" in componentData:
                    comp.state = {"outValue": (0, componentData["initialBitWidth"])}
                
            
            if type(comp) == InstructionMemory or type(comp) == DataMemory:
                memoryData = self.levelData["memoryContents"]
                if type(comp) == InstructionMemory:
                    instructions = memoryData["instructionMemory"]
                    comp.loadInstructions(instructions)
                if type(comp) == DataMemory:
                    data = memoryData["dataMemory"]
                    comp.loadData(data)

        # Set up connections if any
        if self.levelData.get("connections") is not None:
            connections = self.levelData["connections"]
            components = self.logicComponentController.getComponents()
            for connection in connections:
                try:
                    self.logicComponentController.addConnection(
                        components[connection["origin"]],
                        connection["originKey"],
                        components[connection["destination"]],
                        connection["destinationKey"]
                    )
                except KeyError as e:
                    print(f"Error adding connection: {e}")
        self.eventBus.emit("view:rebuild_circuit", componentInfo)

        if self.usesOutputPredictions():
            self.outputPredictions = [output.getState()["outValue"] for output in self.logicComponentController.outputs]
            print(f"Set outputPredictions to: {self.outputPredictions}")

    def checkSolution(self) -> bool:
        """Checks if the current configuration solves the level.
        In case there are output predictions, these will be checked first.
        This assumes that either the input values are fixed for this level or the user chooses the right predictions for their input.
        Afterward, all tests from the level file will be run.

        Returns:
            bool: True if and only if the output predictions (if any) are correct and the tests pass.
        """
        # In case there are output predictions, first check whether the predictions are right at the current input config.
        if self.usesOutputPredictions():
            for i, prediction in enumerate(self.outputPredictions):
                if not prediction == self.logicComponentController.outputs[i].getState()["outValue"]:
                    return False
        # Then iterate through tests
        for i in range(len(self.levelData["tests"])):
            test = self.levelData["tests"][i]
            for i in range(len(test["inputs"])): # iterate through inputs in specific test
                self.logicComponentController.getInputs()[i].setState(tuple(test["inputs"][i]))
            self.logicComponentController.eval()
            for i in range(len(test["expected_output"])): # iterate through expected outputs in specific test
                #print(self.logicComponentController.getOutputs()[i].getState()['outValue'],"==?", tuple(test["expected_output"][i]))
                if self.logicComponentController.getOutputs()[i].getState()['outValue'] != tuple(test["expected_output"][i]):
                    return False
        return True
    
    def resetLevel(self):
        """Resets the level to its initial state"""
        self.logicComponentController.clearComponents()
        self.buildLevel()
        
    def quitLevel(self):
        """Cleans up the level when quitting"""
        self.logicComponentController.clearComponents()
        self.currentLevel = None
        self.eventBus.emit("goToLevelSelection")
        
    def getComponentMap(self):
        """Returns the connection map of the current level"""
        return COMPONENT_MAP

    T = TypeVar("T", bound=LogicComponent)
    def getAvailableComponentClasses(self) -> List[Type[T]]:
        """Returns a list of available components for this level, given the levelData is valid."""
        availableClasses = []
        if self.levelData is not None:
            try:
                availableNames = [comp["type"] for comp in self.levelData["available_components"]]
                for name, class_ in COMPONENT_MAP.items():
                    if name in availableNames:
                        availableClasses.append(class_)
            except Exception as e:
                print(f"Invalid levelData: {e}")
        return availableClasses
    
    def getHints(self):
        """Returns the hints for the current level"""
        if self.levelData is not None and "hints" in self.levelData:
            return self.levelData["hints"]
        return []

    def usesOutputPredictions(self) -> bool:
        """Whether the current level uses output predictions by the user or not.

        Returns:
            bool: True if and only if the levelData file has the attribute 'usesOutputPredictions' with value True.
        """
        if self.levelData is None:
            return False
        return self.levelData.get("usesOutputPredictions", False)
