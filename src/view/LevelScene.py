from src.constants import PALETTE_COLS, CELL_SIZE
from src.control.LevelController import LevelController
from src.control.LevelFileController import LevelFileController
from src.view.Hint import Hint
from src.view.LogicComponentPalette import LogicComponentPalette
from src.view.OutputPrediction import OutputPrediction

from src.view.GridWidget import GridWidget
from src.view.DeleteArea import DeleteArea
from src.view.SimulationControls import SimulationControls

from PySide6 import QtGui, QtWidgets, QtCore


class LevelScene(QtWidgets.QWidget):
    """Main window for a selected level"""

    def __init__(self, levelController: LevelController, levelFileController: LevelFileController):
        super().__init__()

        self.levelController = levelController
        self.logicController = self.levelController.logicComponentController
        self.levelFileController = levelFileController
        self.levelData = self.levelController.getLevel()

        self.central = QtWidgets.QWidget()

        self.setWindowTitle(f"Level {self.levelData['level_id']}")
        self.layout = QtWidgets.QGridLayout(self)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QtGui.QColor("white"))
        self.setPalette(pal)

        # Back to level selection button
        self.backButton = QtWidgets.QPushButton("< Back to level selection")
        self.backButton.clicked.connect(self.goToLevelSelection)

        # Grid
        self.grid = GridWidget(self.logicController)

        # Build the level
        levelController.setGrid(self.grid)
        levelController.buildLevel()

        sidebarFrame = QtWidgets.QVBoxLayout()

        # Add a label for level description
        levelInfoLabel = QtWidgets.QLabel()
        levelInfoLabel.setFixedWidth(PALETTE_COLS * CELL_SIZE + 20)
        levelInfoLabel.setStyleSheet("padding-left: 10px; padding-right: 10px")
        levelInfoLabel.setWordWrap(True)
        try:
            levelName = self.levelData["name"]
            levelDescription = self.levelData["description"]
            levelObjectives = ""
            for objective in self.levelData["objectives"]:
                levelObjectives += f"<li>{objective}</li>"
            levelInfoLabel.setText(
                f"<h1>{levelName}</h1>"
                f"<p>{levelDescription}"
                f"<h2>Objectives</h2>"
                f"<ol>{levelObjectives}</ol>"
            )
        except Exception as e:
            print(f"Error loading level information: {e}")
            levelInfoLabel.setText("Could not load level information")

        levelInfoContainer = QtWidgets.QScrollArea()
        levelInfoContainer.setWidget(levelInfoLabel)
        levelInfoContainer.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        levelInfoContainer.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.levelInfoContainer = levelInfoContainer
        sidebarFrame.addWidget(levelInfoContainer)

        # OutputPrediction, if necessary
        if self.levelController.usesOutputPredictions():
            sidebarFrame.addWidget(OutputPrediction(self.levelController))

        # Palette
        classes = self.levelController.getAvailableComponentClasses()
        if len(classes) != 0:
            palette = LogicComponentPalette(classes)
            sidebarFrame.addWidget(palette)

        # Delete area
        deleteArea = DeleteArea(self.grid)

        # Hint button
        hintButton = Hint(self.levelController)

        deleteAndHintContainer = QtWidgets.QHBoxLayout()
        deleteAndHintContainer.addWidget(hintButton)
        deleteAndHintContainer.addWidget(deleteArea)
        sidebarFrame.addLayout(deleteAndHintContainer)

        # Simulation controls
        simControls = SimulationControls(self.logicController)
        simControls.configureReset(self.levelController.resetLevel)
        simControls.addButton("Check solution", self.checkSolution, 0)

        # Wrap grid in scroll area
        gridScrollArea = QtWidgets.QScrollArea()
        gridScrollArea.setWidget(self.grid)
        gridScrollArea.setWidgetResizable(True)

        # Add the widgets to the layout
        self.layout.addWidget(self.backButton, 0, 0)
        self.layout.addLayout(sidebarFrame, 1, 0)
        self.layout.addWidget(simControls, 0, 1)
        self.layout.addWidget(gridScrollArea, 1, 1)

    def checkSolution(self):
        """Calls the levelController to check the solution.
        If the solution was right, a message box with a success message will be displayed.
        Otherwise, the message box will show a negative message.
        """
        solutionIsRight = self.levelController.checkSolution()
        if solutionIsRight:
            self.levelFileController.updateCompletedLevels(self.levelController.currentLevel)
            QtWidgets.QMessageBox.information(self, "You did it!", "All checks succeeded. You can proceed to the next level.")
        else:
            failureMessage = "Some tests failed, give it another try."
            if self.levelController.usesOutputPredictions():
                failureMessage += " Make sure to check your output predictions."
            QtWidgets.QMessageBox.critical(self, "Not quite!", failureMessage)

    def goToLevelSelection(self):
        """Cleans up the logic components and the grid and then emits the event to switch to the level selection."""
        self.grid.unsubscribe()
        self.levelController.quitLevel()
