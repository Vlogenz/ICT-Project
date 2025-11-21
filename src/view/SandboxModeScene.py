from src.control.CustomComponentController import CustomComponentController
from src.control.LogicComponentController import LogicComponentController
from src.view.CreateCustomComponentDialog import CreateCustomComponentDialog
from src.view.LogicComponentPalette import LogicComponentPalette
from src.view.GridWidget import GridWidget
from src.view.DeleteArea import DeleteArea
import src.model as model
from src.infrastructure.eventBus import getBus

from PySide6 import QtGui, QtWidgets

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
        palette = LogicComponentPalette(customComponents=CustomComponentController.loadCustomComponents())

        # Grid
        self.grid = GridWidget(logicController)

        # Delete area
        deleteArea = DeleteArea(self.grid)

        sidebarFrame = QtWidgets.QVBoxLayout()
        sidebarFrame.addWidget(palette)
        sidebarFrame.addWidget(deleteArea)

        # Simulation controls
        simControls = SimulationControls(self.logicController)
        simControls.addButton("Save as logic component", self.openCreateCustomComponentDialog)

        # Add the items to the main grid layout
        layout.addLayout(sidebarFrame, 1, 0, 2, 1)
        layout.addWidget(simControls, 0, 1)

        # Wrap grid in scroll area
        gridScrollArea = QtWidgets.QScrollArea()
        gridScrollArea.setWidget(self.grid)
        gridScrollArea.setWidgetResizable(True)
        layout.addWidget(gridScrollArea, 1, 1)
        layout.addWidget(backButton, 0, 0)

    def goToMain(self):
        self.logicController.clearComponents()
        self.grid.unsubscribe()
        self.bus.emit("goToMain")

    def openCreateCustomComponentDialog(self):
        dialog = CreateCustomComponentDialog(self.logicController)
        dialog.exec()
