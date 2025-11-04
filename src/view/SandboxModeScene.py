import sys

from src.control.LogicComponentController import LogicComponentController
from src.view.PaletteItem import PaletteItem
from src.view.GridWidget import GridWidget
from src.view.DeleteArea import DeleteArea
import src.model as model
from src.infrastructure.eventBus import getBus

from PySide6 import QtGui, QtWidgets
import inspect
import pkgutil
import importlib

from src.view.SimulationControls import SimulationControls


class SandboxModeScene(QtWidgets.QWidget):
    """Main window for the sandbox mode."""

    def __init__(self, logicController: LogicComponentController):
        super().__init__()
        self.setWindowTitle("Sandbox Mode")

        self.bus = getBus()
        self.logicController = logicController

        self.central = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(self)

        pal = self.palette()
        pal.setColor(self.backgroundRole(), QtGui.QColor("white"))
        self.setPalette(pal)

        # Back to Main Screen button
        backButton = QtWidgets.QPushButton("< Back to Main Screen")
        backButton.clicked.connect(self.goToMain)


        # Palette
        palette = QtWidgets.QGridLayout()
        classes = list(self.iter_classes_in_package(model))
        for i, class_ in enumerate(classes):
            # Use index for a two-column grid
            palette.addWidget(PaletteItem(class_), i//3, i%3)

        # Grid
        self.grid = GridWidget(logicController)

        # Delete area
        deleteArea = DeleteArea(self.grid)
        palette.addWidget(deleteArea)

        palette_frame = QtWidgets.QFrame()
        palette_frame.setLayout(palette)

        # Simulation controls
        simControls = SimulationControls(self.logicController)

        # Add the items to the main grid layout
        layout.addWidget(palette_frame, 1, 0, 2, 1)
        layout.addWidget(simControls, 0, 1)

        # Wrap grid in scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(self.grid)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area, 1, 1)
        layout.addWidget(backButton, 0, 0)

    def goToMain(self):
        self.logicController.clearComponents()
        self.grid.unsubscribe()
        self.bus.emit("goToMain")

    def iter_classes_in_package(self, package):
        for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            module = importlib.import_module(module_name)
            for name, cls in inspect.getmembers(module, inspect.isclass):
                if cls.__module__ == module.__name__:
                    yield cls
