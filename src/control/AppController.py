from PySide6 import QtWidgets
import sys
from src.infrastructure.eventBus import getBus

from src.control.LogicComponentController import LogicComponentController
from src.view.SandboxModeWindow import SandboxModeWindow
from src.view.LevelSelectionWindow import LevelSelectionWindow

from src.control.LevelFileController import LevelFileController
from src.control.LevelController import LevelController

class AppController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.aboutToQuit.connect(self._cleanup)  # Signal verbinden
        self.window = None #TODO initialize main screen window
        self.bus = getBus()
        self.bus.subscribe("levelSelection:levelSelected", self.onLevelSelected)
        self.logicController = LogicComponentController()
        self.levelFileController = LevelFileController()
        self.levelController = LevelController(self.levelFileController)
        #self.startSandboxMode() # TODO remove this line when main screen is ready
        self.showLevelSelectionScreen()
        

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())
        
    def showMainScreen(self):
        self.window = None #  TODO MainScreenWindow() add main screen window
        self.window.show()

    def startSandboxMode(self):
        self.logicController = LogicComponentController()
        self.window = SandboxModeWindow(self.logicController)
        self.window.show()
        
    def showLevelSelectionScreen(self):
        self.window = LevelSelectionWindow(self.logicController, self.levelFileController)
        self.window.show()
        
    def onLevelSelected(self, levelNumber: int):
        """Handles level selection event from LevelSelectionScreen"""
        levelData = self.levelFileController.loadLevel(levelNumber)
        self.window = None # TODO LevelWindow(levelData, self.levelController, self.logicController)
        self.window.show()

    def stopApp(self):
        """cleanly stops the application"""
        self.app.quit()
        
    def _cleanup(self):
        """Called automatically before the app quits"""
        #TODO call methods for data saving and cleanup
        print("Cleanup: Saving data and cleaning up resources...")  # Optional: für Debugging