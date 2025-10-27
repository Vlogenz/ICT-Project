import sys

from src.control.LevelController import LevelController
from src.control.LogicComponentController import LogicComponentController
from src.view.PaletteItem import PaletteItem
from src.view.GridWidget import GridWidget
from src.view.DeleteArea import DeleteArea
import src.model as model

from PySide6 import QtGui, QtWidgets
import inspect
import pkgutil
import importlib

from src.view.SimulationControls import SimulationControls


class LevelWindow(QtWidgets.QMainWindow):
    """Main window for a selected level"""

    def __init__(self, levelData, levelController: LevelController, logicController: LogicComponentController):
        super().__init__()
        self.setWindowTitle("Level " + levelData["level_id"])

        self.logicController = logicController
        self.levelController = levelController
        self.levelData = levelData

        central = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(central)
        self.setCentralWidget(central)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QtGui.QColor("white"))
        self.setPalette(pal)

        # Palette
        palette = QtWidgets.QGridLayout()
        classes = list(self.iterClassesInPackage(model))
        print(f"classes: {classes}")
        for i, class_ in enumerate(classes):
            # Use index for a two-column grid
            palette.addWidget(PaletteItem(class_), i//2, i%2)

        # Grid
        grid = GridWidget(logicController)

        # Delete area
        deleteArea = DeleteArea(grid)
        palette.addWidget(deleteArea)

        palette_frame = QtWidgets.QFrame()
        palette_frame.setLayout(palette)
        palette_frame.setFixedWidth(200)

        # Simulation controls
        simControls = SimulationControls(self.logicController)

        # Build the level
        levelController.buildLevel()

    def iterClassesInPackage(self, package):
        componentMap = self.levelController.getComponentMap()

        for i in range(len(self.levelData["available_components"])):
            component = self.levelData["available_components"][i]["type"]
            moduleName = componentMap[component]
            module = importlib.import_module(moduleName)

            for name, cls in inspect.getmembers(module, inspect.isclass):
                if cls.__module__ == module.__name__:
                    yield cls
