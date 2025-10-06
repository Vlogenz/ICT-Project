import sys

from src.control.LogicComponentController import LogicComponentController
from src.view.PaletteItem import PaletteItem
from src.view.GridWidget import GridWidget
from src.view.DeleteArea import DeleteArea

from PySide6 import QtGui, QtWidgets
import inspect
import pkgutil
import importlib

from src.view.SimulationControls import SimulationControls


class SandboxModeWindow(QtWidgets.QMainWindow):
    """Main window for the sandbox mode."""

    def __init__(self, logicController: LogicComponentController):
        super().__init__()
        self.setWindowTitle("Sandbox Mode")

        central = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(central)
        self.setCentralWidget(central)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QtGui.QColor("white"))
        self.setPalette(pal)

        # Palette
        # TODO: Show all available logic components here
        palette = QtWidgets.QVBoxLayout()
        classes = self.get_component_classes()
        for class_ in classes:
            palette.addWidget(PaletteItem(f"{class_}"))
        palette.addStretch()

        # Grid
        grid = GridWidget(logicController)

        # Delete area
        deleteArea = DeleteArea(grid)
        palette.addWidget(deleteArea)

        palette_frame = QtWidgets.QFrame()
        palette_frame.setLayout(palette)
        palette_frame.setFixedWidth(120)

        # Simulation controls
        simControls = SimulationControls()

        # Add the items to the main grid layout
        layout.addWidget(palette_frame, 0, 0, 2, 1)
        layout.addWidget(simControls, 0, 1)
        layout.addWidget(grid, 1, 1)

        #class_list = self.get_classes_in_package("src.model")
        #for cls in class_list:
        #    print(cls)

    def get_component_classes(self):
        classes = []
        package = importlib.import_module("src.model")

        for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module.name:
                    classes.append(obj)
        return classes
