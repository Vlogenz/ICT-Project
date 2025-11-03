from src.control.LogicComponentController import LogicComponentController
from src.model.LogicComponent import LogicComponent
from src.model.Input import Input
from src.model.Output import Output
from src.model.And import And
from src.model.Or import Or
from src.model.Not import Not
from src.model.Nand import Nand
from src.model.Nor import Nor
from src.model.Xor import Xor
from src.model.Xnor import Xnor
from src.infrastructure.eventBus import getBus

from typing import List, TypeVar, Type, Tuple

class LevelController:
    COMPONENT_MAP = {
        "Input": Input,
        "Output": Output,
        "And": And,
        "Or": Or,
        "Not": Not,
        "Nand": Nand,
        "Nor": Nor,
        "Xor": Xor,
        "Xnor": Xnor,
        # Add further components here when necessary
    }
    
    def __init__(self, logicComponentController: LogicComponentController, levelData = None, grid = None):
        self.levelData = levelData
        self.logicComponentController = logicComponentController
        self.currentLevel = None
        self.eventBus = getBus()
    
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

        #Additional info for each component:
        # - which cell to put it in: int, int
        # - whether it is immovable or not: bool
        componentInfo: List[Tuple[int,int,bool]] = []
        for componentData in components:
            component_type_str = componentData["type"]
            
            # Convert string to class
            if component_type_str not in self.COMPONENT_MAP:
                raise ValueError(f"Unknown component type: {component_type_str}")
            
            component_class = self.COMPONENT_MAP[component_type_str]
            self.logicComponentController.addLogicComponent(component_class)

            pos = tuple(componentData["position"])
            componentInfo.append((pos[0], pos[1], componentData["immovable"]))
            
        # Set up connections if any
        if self.levelData.get("connections") is None:
            return
        connections = self.levelData["connections"]
        components = self.logicComponentController.getComponents()
        for connection in connections:
            self.logicComponentController.addConnection(
                components[connection["origin"]],
                connection["originKey"],
                components[connection["destination"]],
                connection["destinationKey"]
            )
        self.eventBus.emit("view:rebuild_circuit", componentInfo)

    def checkSolution(self) -> bool:
        """Checks if the current configuration solves the level"""
        for i in range(len(self.levelData["tests"])): # Iterate through tests
            test = self.levelData["tests"][i]
            for i in range(len(test["inputs"])): # iterate through inputs in specific test
                self.logicComponentController.getInputs()[i].setState(tuple(test["inputs"][i]))
            self.logicComponentController.eval()
            for i in range(len(test["expected_output"])): # iterate through expected outputs in specific test
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
        return self.COMPONENT_MAP

    T = TypeVar("T", bound=LogicComponent)
    def getAvailableComponentClasses(self) -> List[Type[T]]:
        """Returns a list of available components for this level, given the levelData is valid."""
        availableClasses = []
        if self.levelData is not None:
            try:
                availableNames = [comp["type"] for comp in self.levelData["available_components"]]
                for name, class_ in self.COMPONENT_MAP.items():
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
