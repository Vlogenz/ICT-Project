from src.control.LevelController import LevelController
from src.control.LevelFileController import LevelFileController
from src.control.LogicComponentController import LogicComponentController
from src.view.Hint import Hint
from src.view.LogicComponentPalette import LogicComponentPalette

from src.view.PaletteItem import PaletteItem
from src.view.GridWidget import GridWidget
from src.view.DeleteArea import DeleteArea
from src.view.SimulationControls import SimulationControls

from PySide6 import QtGui, QtWidgets


class LevelScene(QtWidgets.QWidget):
    """Main window for a selected level"""
    #TODO: Add separate Check button and have Start only for pre-testing before the check

    def __init__(self, levelController: LevelController, levelFileController: LevelFileController):
        super().__init__()

        self.levelController = levelController
        self.logicController = self.levelController.logicComponentController
        self.levelFileController = levelFileController
        self.levelData = self.levelController.getLevel()

        self.central = QtWidgets.QWidget()

        self.setWindowTitle(f"Level {self.levelData["level_id"]}")
        self.layout = QtWidgets.QGridLayout(self)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QtGui.QColor("white"))
        self.setPalette(pal)

        # Back to level selection button
        self.backButton = QtWidgets.QPushButton("< Back to level selection")
        self.backButton.clicked.connect(self.goToLevelSelection)

        sidebarFrame = QtWidgets.QGridLayout()

        # Palette
        classes = self.levelController.getAvailableComponentClasses()
        palette = LogicComponentPalette(classes)
        sidebarFrame.addWidget(palette, 0, 0, 1, 2)

        # Grid
        self.grid = GridWidget(self.logicController)

        # Delete area
        deleteArea = DeleteArea(self.grid)
        sidebarFrame.addWidget(deleteArea, 1, 1)

        # Hint button
        hintButton = Hint(self.levelController)
        sidebarFrame.addWidget(hintButton, 1, 0)


        # Simulation controls
        simControls = SimulationControls(self.logicController)
        simControls.configureReset(self.levelController.resetLevel)
        simControls.addButton("Check solution", self.checkSolution, 0)

        # Build the level
        levelController.setGrid(self.grid)
        levelController.buildLevel()

        # Add a label for level description
        levelInfoLabel = QtWidgets.QLabel()
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


        # Add the widgets to the layout
        self.layout.addWidget(self.backButton, 0, 0)
        self.layout.addWidget(levelInfoLabel, 1, 0)
        self.layout.addLayout(sidebarFrame, 2, 0)
        self.layout.addWidget(simControls, 0, 1)

        # Wrap grid in scroll area
        gridScrollArea = QtWidgets.QScrollArea()
        gridScrollArea.setWidget(self.grid)
        gridScrollArea.setWidgetResizable(True)
        self.layout.addWidget(gridScrollArea, 1, 1, 2, 1)

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
            QtWidgets.QMessageBox.critical(self, "Not quite!", "Some tests failed. Give it another try.")

    def goToLevelSelection(self):
        """Cleans up the logic components and the grid and then emits the event to switch to the level selection."""
        self.grid.unsubscribe()
        self.levelController.quitLevel()
