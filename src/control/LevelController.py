from src.control.LogicComponentController import LogicComponentController
from src.model.Input import Input
from src.model.Output import Output
from src.model.And import And
from src.model.Or import Or
from src.model.Not import Not
from src.model.Nand import Nand
from src.model.Nor import Nor
from src.model.Xor import Xor
from src.model.Xnor import Xnor

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
        # Füge hier weitere Komponenten hinzu wenn nötig
    }
    
    def __init__(self, logicComponentController: LogicComponentController):
        self.levelData = None
        self.logicComponentController = logicComponentController
        self.currentLevel = None
    
    def setLevel(self, levelData):
        """Sets the current level data"""
        self.levelData = levelData
    
    #TODO: This does not update the components in the frontend yet.
    # We could emit an event here for each component. The event handler in the frontend should add the item on the grid (GridWidget->addItem).
    def buildLevel(self):
        """Builds the level using level data"""
        self.currentLevel = self.levelData["level_id"]
        components = self.levelData["components"]
        for componentData in components:
            component_type_str = componentData["type"]
            
            # String in Klasse umwandeln
            if component_type_str not in self.COMPONENT_MAP:
                raise ValueError(f"Unknown component type: {component_type_str}")
            
            component_class = self.COMPONENT_MAP[component_type_str]
            self.logicComponentController.addLogicComponent(component_class)
            
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
        
    def getComponentMap(self):
        """Returns the connection map of the current level"""
        return self.COMPONENT_MAP