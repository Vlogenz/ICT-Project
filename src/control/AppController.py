from enum import Enum

from PySide6 import QtWidgets
import sys
from src.infrastructure.eventBus import getBus

from src.control.LogicComponentController import LogicComponentController
from src.view.SandboxModeWindow import SandboxModeWindow
from src.view.LevelSelectionWindow import LevelSelectionWindow
from src.view.LevelWindow import LevelWindow

from src.control.LevelFileController import LevelFileController
from src.control.LevelController import LevelController

class Window(Enum):
    MAIN = 0
    SANDBOX = 1
    LEVEL_SELECTION = 2
    LEVEL = 3

class AppController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.aboutToQuit.connect(self._cleanup)  # Signal verbinden
        self.bus = getBus()
        self.bus.subscribe("levelSelection:levelSelected", self.onLevelSelected)
        self.bus.subscribe("goToLevelSelection", lambda: self.switchToWindow(Window.LEVEL_SELECTION))
        self.logicController = LogicComponentController()
        self.levelFileController = LevelFileController()
        self.levelController = LevelController(self.logicController)
        self.window: QtWidgets.QMainWindow = LevelSelectionWindow(self.levelFileController)  # TODO initialize main screen window

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

    def switchToWindow(self, window: Window):
        #TODO: Do not use separate windows but set the central widget to the new content
        newWindow = self.window
        match window:
            case Window.SANDBOX:
                newWindow = SandboxModeWindow(self.logicController)
            case Window.LEVEL_SELECTION:
                newWindow = LevelSelectionWindow(self.levelFileController)
            case Window.LEVEL:
                newWindow = LevelWindow(self.levelController, self.logicController, self.levelFileController)
            case _:
                #TODO: go to main screen instead
                newWindow = SandboxModeWindow(self.logicController)
        if newWindow is not self.window:
            oldWindow = self.window
            self.window = newWindow
            oldWindow.close()
            self.window.show()
        
    def onLevelSelected(self, levelNumber: int):
        """Handles level selection event from LevelSelectionScreen"""
        levelData = self.levelFileController.loadLevel(levelNumber)
        self.levelController.setLevel(levelData)
        self.switchToWindow(Window.LEVEL)

    def stopApp(self):
        """cleanly stops the application"""
        self.app.quit()
        
    def _cleanup(self):
        """Called automatically before the app quits"""
        #TODO call methods for data saving and cleanup
        print("Cleanup: Saving data and cleaning up resources...")  # Optional: für Debugging