

# from PySide6 import QtWidgets
# import sys
# from src.infrastructure.eventBus import getBus

# from src.control.LogicComponentController import LogicComponentController
# from src.view.SandboxModeScene import SandboxModeScene
# from src.view.LevelSelectionScene import LevelSelectionScene
# from src.view.LevelScene import LevelScene
# from src.view.MainScene import MainScene
# from src.constants import Scene
# from src.control.LevelFileController import LevelFileController
# from src.control.LevelController import LevelController



# class AppController():
#     def __init__(self):
#         self.app = QtWidgets.QApplication(sys.argv)
#         self.app.aboutToQuit.connect(self._cleanup)  # connect signal
#         self.bus = getBus()
#         self.bus.subscribe("levelSelection:levelSelected", self.onLevelSelected)
#         self.bus.subscribe("goToLevelSelection", lambda: self.switchToScene(Scene.LEVEL_SELECTION))
#         self.bus.subscribe("goToSandboxMode", lambda: self.switchToScene(Scene.SANDBOX))
#         self.bus.subscribe("goToMain", lambda: self.switchToScene(Scene.MAIN))
#         self.bus.subscribe("stopApp", lambda: self.stopApp())
#         self.logicController = LogicComponentController()
#         self.levelFileController = LevelFileController()
#         self.levelController = LevelController(self.logicController)
#         self.window: QtWidgets.QMainWindow = QtWidgets.QMainWindow()

#         self.window.setCentralWidget(MainScene())

#     def run(self):
#         self.window.showMaximized()
#         sys.exit(self.app.exec())

#     def switchToScene(self, scene: Scene):
#         newScene = self.window.centralWidget()
#         match scene:
#             case Scene.SANDBOX:
#                 newScene = SandboxModeScene(self.logicController)
#             case Scene.LEVEL_SELECTION:
#                 newScene = LevelSelectionScene(self.levelFileController)
#             case Scene.LEVEL:
#                 newScene = LevelScene(self.levelController, self.levelFileController)
#             case Scene.MAIN:
#                 newScene = MainScene()

#         if newScene is not self.window.centralWidget():

#             self.window.setCentralWidget(newScene)
#             self.window.setWindowTitle(newScene.windowTitle())

#     def onLevelSelected(self, levelNumber: int):
#         """Handles level selection event from LevelSelectionScreen"""

#         levelData = self.levelFileController.loadLevel(levelNumber)
#         self.levelController.setLevel(levelData)
#         self.switchToScene(Scene.LEVEL)

#     def stopApp(self):
#         """cleanly stops the application"""
#         self.app.quit()
        
#     def _cleanup(self):
#         """Called automatically before the app quits"""
#         #TODO call methods for data saving and cleanup
#         print("Cleanup: Saving data and cleaning up resources...")  # Optional: für Debugging



from PySide6 import QtWidgets, QtCore, QtGui
import sys
from src.infrastructure.eventBus import getBus

# Your existing imports...
from src.control.LogicComponentController import LogicComponentController
from src.view.SandboxModeScene import SandboxModeScene
from src.view.LevelSelectionScene import LevelSelectionScene
from src.view.LevelScene import LevelScene
from src.view.MainScene import MainScene
from src.constants import Scene
from src.control.LevelFileController import LevelFileController
from src.control.LevelController import LevelController

class AppController():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.aboutToQuit.connect(self._cleanup)
        self.bus = getBus()
        self.bus.subscribe("levelSelection:levelSelected", self.onLevelSelected)
        self.bus.subscribe("goToLevelSelection", lambda: self.switchToScene(Scene.LEVEL_SELECTION))
        self.bus.subscribe("goToSandboxMode", lambda: self.switchToScene(Scene.SANDBOX))
        self.bus.subscribe("goToMain", lambda: self.switchToScene(Scene.MAIN))
        self.bus.subscribe("stopApp", lambda: self.stopApp())

        self.logicController = LogicComponentController()
        self.levelFileController = LevelFileController()
        self.levelController = LevelController(self.logicController)

        self.window = QtWidgets.QMainWindow()
        self.window.setCentralWidget(MainScene())
        self.window.setWindowTitle("Logic Gates Game")

        # Set up fade-in opacity effect
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.window)
        self.window.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(800)  # Fade duration in ms
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)

    def run(self):
        self.window.show()
        self.fade_animation.start()
        sys.exit(self.app.exec())

    def switchToScene(self, scene: Scene):
        newScene = self.window.centralWidget()
        if scene == Scene.SANDBOX:
            newScene = SandboxModeScene(self.logicController)
        elif scene == Scene.LEVEL_SELECTION:
            newScene = LevelSelectionScene(self.levelFileController)
        elif scene == Scene.LEVEL:
            newScene = LevelScene(self.levelController, self.levelFileController)
        elif scene == Scene.MAIN:
            newScene = MainScene()

        if newScene is not self.window.centralWidget():
            self.window.setCentralWidget(newScene)
            self.window.setWindowTitle(newScene.windowTitle())
            # Optionally, fade in new scene here too
            effect = QtWidgets.QGraphicsOpacityEffect(newScene)
            newScene.setGraphicsEffect(effect)
            anim = QtCore.QPropertyAnimation(effect, b"opacity")
            anim.setDuration(500)
            anim.setStartValue(0)
            anim.setEndValue(1)
            anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def onLevelSelected(self, levelNumber: int):
        levelData = self.levelFileController.loadLevel(levelNumber)
        self.levelController.setLevel(levelData)
        self.switchToScene(Scene.LEVEL)

    def stopApp(self):
        self.app.quit()

    def _cleanup(self):
        print("Cleanup: Saving data and cleaning up resources...")
