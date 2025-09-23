import sys
from src.view.PaletteItem import PaletteItem
from src.view.GridWidget import GridWidget
from src.view.DeleteArea import DeleteArea

from PySide6 import QtGui, QtWidgets

from src.view.SimulationControls import SimulationControls


class SandboxModeWindow(QtWidgets.QMainWindow):
    """Main window for the sandbox mode."""

    def __init__(self):
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
        palette.addWidget(PaletteItem("Label"))
        palette.addWidget(PaletteItem("Red Node", QtGui.QColor("#ff9999")))
        palette.addStretch()

        # Grid
        grid = GridWidget()

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
