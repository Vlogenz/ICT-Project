from enum import Enum

from PySide6 import QtWidgets
import sys
from src.infrastructure.eventBus import getBus

from src.control.LogicComponentController import LogicComponentController
from src.view.SandboxModeScene import SandboxModeScene
from src.view.LevelSelectionScene import LevelSelectionScene
from src.view.LevelScene import LevelScene

from src.control.LevelFileController import LevelFileController
from src.control.LevelController import LevelController

class Scene(Enum):
    MAIN = 0
    SANDBOX = 1
    LEVEL_SELECTION = 2
    LEVEL = 3

class AppController():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.aboutToQuit.connect(self._cleanup)  # connect signal
        self.bus = getBus()
        self.bus.subscribe("levelSelection:levelSelected", self.onLevelSelected)
        self.bus.subscribe("goToLevelSelection", lambda: self.switchToScene(Scene.LEVEL_SELECTION))
        self.logicController = LogicComponentController()
        self.levelFileController = LevelFileController()
        self.levelController = LevelController(self.logicController)
        self.window: QtWidgets.QMainWindow = QtWidgets.QMainWindow()

        self.window.setCentralWidget(LevelSelectionScene(self.levelFileController))  # TODO initialize main screen window

    def run(self):
        self.window.showMaximized()
        sys.exit(self.app.exec())

    def switchToScene(self, scene: Scene):
        newScene = self.window.centralWidget()
        match scene:
            case Scene.SANDBOX:
                newScene = SandboxModeScene(self.logicController)
            case Scene.LEVEL_SELECTION:
                newScene = LevelSelectionScene(self.levelFileController)
            case Scene.LEVEL:
                newScene = LevelScene(self.levelController, self.levelFileController)
            case _:
                #TODO: go to main screen instead
                newScene = SandboxModeScene(self.logicController)

        if newScene is not self.window.centralWidget():

            self.window.setCentralWidget(newScene)
            self.window.setWindowTitle(newScene.windowTitle())

    def onLevelSelected(self, levelNumber: int):
        """Handles level selection event from LevelSelectionScreen"""

        levelData = self.levelFileController.loadLevel(levelNumber)
        self.levelController.setLevel(levelData)
        self.switchToScene(Scene.LEVEL)

    def stopApp(self):
        """cleanly stops the application"""
        self.app.quit()
        
    def _cleanup(self):
        """Called automatically before the app quits"""
        #TODO call methods for data saving and cleanup
        print("Cleanup: Saving data and cleaning up resources...")  # Optional: für Debugging