from PySide6 import QtCore, QtWidgets
from src.infrastructure.eventBus import getBus
from src.control.LevelFileController import LevelFileController
COLUMNS = 7

class LevelSelectionWindow(QtWidgets.QMainWindow):
    """
    Shows a grid with a cell for each level.
    """

    def __init__(self, appController, levelFileController: LevelFileController):
        super().__init__()
        self.setWindowTitle("Level selection")
        self.appController = appController
        self.levelFileController = levelFileController
        self.bus = getBus()

        # Import metafile, and unlocked metafile
        metaFile = self.levelFileController.loadMetaFile()
        self.levelUnlocked = metaFile["level_unlocked"]

        central = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(central)
        self.setCentralWidget(central)
        self.grid = QtWidgets.QGridLayout()

        headerLabel = QtWidgets.QLabel("Select a level")
        headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(headerLabel)
        self.layout.addLayout(self.grid)

        # load levels
        levels = levelFileController.getAvailableLevels()
        print(levels)

        # create a cell for each level and put it on the grid
        for i in levels:
            button = QtWidgets.QPushButton(f"Level {i}")
            button.clicked.connect(lambda: self.on_level_clicked(i))
            self.grid.addWidget(button, i//COLUMNS, i%COLUMNS)
        
    def on_level_clicked(self, level_number: int):
        """User clicks on a level"""
        self.bus.emit("levelSelection:levelSelected", level_number)
        print("opening level: {level_number}")
