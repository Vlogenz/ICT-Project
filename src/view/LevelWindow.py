from src.control.LevelController import LevelController
from src.control.LogicComponentController import LogicComponentController

from src.infrastructure.eventBus import getBus

from src.view.PaletteItem import PaletteItem
from src.view.GridWidget import GridWidget
from src.view.DeleteArea import DeleteArea
from src.view.SimulationControls import SimulationControls

from PySide6 import QtGui, QtWidgets
from pyqttoast import Toast, ToastPreset


class LevelWindow(QtWidgets.QWidget):
    """Main window for a selected level"""
    #TODO: Add separate Check button and have Start only for pre-testing before the check

    def __init__(self, levelController: LevelController):
        super().__init__()

        self.logicController = levelController.logicComponentController
        self.levelController = levelController
        self.levelData = self.levelController.getLevel()
        self.eventBus = getBus()

        self.central = QtWidgets.QWidget()

        self.setWindowTitle(f"Level {self.levelData["level_id"]}")
        self.layout = QtWidgets.QGridLayout(self)

        pal = self.palette()
        pal.setColor(self.backgroundRole(), QtGui.QColor("white"))
        self.setPalette(pal)

        # Back to level selection button
        self.backButton = QtWidgets.QPushButton("< Back to level selection")
        self.backButton.clicked.connect(lambda: self.eventBus.emit("goToLevelSelection"))
        self.backButton.clicked.connect(lambda: self.levelController.quitLevel())

        # Palette
        palette = QtWidgets.QGridLayout()
        classes = self.levelController.getAvailableComponentClasses()
        print(f"classes: {classes}")
        for i, class_ in enumerate(classes):
            # Use index for a two-column grid
            palette.addWidget(PaletteItem(class_), i//2, i%2)

        # Grid
        self.grid = GridWidget(self.logicController)

        # Delete area
        deleteArea = DeleteArea(self.grid)
        palette.addWidget(deleteArea)

        palette_frame = QtWidgets.QFrame()
        palette_frame.setLayout(palette)

        # Simulation controls
        simControls = SimulationControls(self.logicController)
        simControls.configureStart(self.checkSolution)
        simControls.configureReset(self.levelController.resetLevel)

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
        self.layout.addWidget(palette_frame, 2, 0)
        self.layout.addWidget(simControls, 0, 1)
        self.layout.addWidget(self.grid, 1, 1, 2, 1)

    def checkSolution(self):
        """Calls the levelController to check the solution.
        If the solution was right, a toast with a success message will be displayed.
        Otherwise, the toast will show a negative message.
        """
        solutionIsRight = self.levelController.checkSolution()
        toast = Toast(self)
        toast.setDuration(3000)  # Hide after 3 seconds
        if solutionIsRight:
            toast.setTitle("You did it!")
            toast.setText("All checks succeeded. You can proceed to the next level.")
            toast.applyPreset(ToastPreset.SUCCESS)
        else:
            toast.setTitle("Not quite!")
            toast.setText("Some tests failed. Give it another try.")
            toast.applyPreset(ToastPreset.ERROR)  # Apply style preset
        toast.show()

