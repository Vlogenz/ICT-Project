from PySide6 import QtWidgets
import sys
from src.infrastructure.eventBus import getBus

from src.control.LogicComponentController import LogicComponentController
from src.view.SandboxModeScene import SandboxModeScene
from src.view.LevelSelectionScene import LevelSelectionScene
from src.view.LevelScene import LevelScene
from src.view.MainScene import MainScene
from src.constants import Scene, BG_COLOR, PR_COLOR_1, PR_COLOR_2
from src.control.LevelFileController import LevelFileController
from src.control.LevelController import LevelController



class AppController():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        stylesheet = f"""
            QMainWindow {{
            background-color: rgb{BG_COLOR};
            }}
            QPushButton {{
            background-color: rgb{PR_COLOR_1};
            color: rgb{BG_COLOR};
            font-size: 24px;
            font-weight: bold;
            border-radius: 10px;
            }}
            #btn-secondary-bold {{
            background-color: rgb{PR_COLOR_2};
            color: rgb{BG_COLOR};
            font-size: 24px;
            font-weight: bold;
            border-radius: 10px;
            }}
            #btn-secondary {{
            background-color: rgb{PR_COLOR_2};
            color: rgb{BG_COLOR};
            font-size: 24px;
            border-radius: 10px;
            }}
             #level-button {{
            border: 5px solid rgb{PR_COLOR_2};
            border-radius: 10px;
            background-color: rgb{BG_COLOR};
            color: rgb{PR_COLOR_2};
            font-size: 16px;
            }} 
            """
        self.app.setStyleSheet(stylesheet)
        self.app.aboutToQuit.connect(self._cleanup)  # connect signal
        self.bus = getBus()
        self.bus.subscribe("levelSelection:levelSelected", self.onLevelSelected)
        self.bus.subscribe("goToLevelSelection", lambda: self.switchToScene(Scene.LEVEL_SELECTION))
        self.bus.subscribe("goToSandboxMode", lambda: self.switchToScene(Scene.SANDBOX))
        self.bus.subscribe("goToMain", lambda: self.switchToScene(Scene.MAIN))
        self.bus.subscribe("stopApp", lambda: self.stopApp())
        self.logicController = LogicComponentController()
        self.levelFileController = LevelFileController()
        self.levelController = LevelController(self.logicController)
        self.window: QtWidgets.QMainWindow = QtWidgets.QMainWindow()

        self.window.setCentralWidget(MainScene())

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
            case Scene.MAIN:
                newScene = MainScene()

        if newScene is not self.window.centralWidget():
            oldScene = self.window.centralWidget()
            self.window.setCentralWidget(newScene)
            oldScene.deleteLater()
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
        pass