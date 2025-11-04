from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QPushButton

from src.infrastructure.eventBus import getBus
from src.control.LevelFileController import LevelFileController
COLUMNS = 5

class LevelSelectionScene(QtWidgets.QWidget):
    """
    Shows a grid with a cell for each level.
    """

    def __init__(self, levelFileController: LevelFileController):
        super().__init__()
        self.setWindowTitle("Level selection")
        self.levelFileController = levelFileController
        self.bus = getBus()

        self.central = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self)

        headerLabel = QtWidgets.QLabel("Select a level")
        headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.grid = QtWidgets.QGridLayout()
        self.toggleLevelLockButton = QtWidgets.QPushButton()
        
        if self.levelFileController.getAllLevelsUnlocked():
            self.toggleLevelLockButton.setText("Lock levels")
        else:
            self.toggleLevelLockButton.setText("Unlock all levels")
        self.toggleLevelLockButton.clicked.connect(self.toggleLevelLock)

        mainSceneBtn = QPushButton(text="< Back to Main Screen", parent=self)
        mainSceneBtn.clicked.connect(lambda: self.bus.emit("goToMain"))

        self.layout.addWidget(mainSceneBtn, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(headerLabel)
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.toggleLevelLockButton)


        self.levelButtons = []
        self.createLevelButtons()



    def createLevelButtons(self):
        """Initialize all level buttons. If a level is done, it gets the 'done' label.
        If it is locked, it gets the 'locked' label and you cannot open it.
        """
        levels = self.levelFileController.getAvailableLevels()
        completed = self.levelFileController.getCompletedLevels()
        unlocked = self.levelFileController.getAllLevelsUnlocked()
        max_completed = max(completed) if completed else -1

        for i in levels:
            button = QtWidgets.QPushButton()
            text = f"Level {i}"
            if i in completed:
                text += " (Done)"
            elif not unlocked and i > max_completed + 1:
                text += " (Locked)"
            button.setText(text)
            if not (not unlocked and i > max_completed + 1):
                button.clicked.connect(lambda checked=False, lvl=i: self.onLevelClicked(lvl))
            self.grid.addWidget(button, i//COLUMNS, i%COLUMNS)
            self.levelButtons.append(button)

    def onLevelClicked(self, level_number: int):
        """User clicks on a level"""
        self.bus.emit("levelSelection:levelSelected", level_number)

    def toggleLevelLock(self):
        """Toggles whether all levels are unlocked.
        """
        if not self.levelFileController.getAllLevelsUnlocked():
            self.levelFileController.setAllLevelsUnlocked(True)
            self.toggleLevelLockButton.setText("Lock levels")
        else:
            self.levelFileController.setAllLevelsUnlocked(False)
            self.toggleLevelLockButton.setText("Unlock all levels")
        self.updateLevelButtons()

    def updateLevelButtons(self):
        """Updates the level buttons."""
        for b in self.levelButtons:
            self.grid.removeWidget(b)
            b.deleteLater()
        self.levelButtons.clear()
        self.createLevelButtons()

