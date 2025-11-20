from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath

from src.constants import PR_COLOR_2, BG_COLOR
from src.infrastructure.eventBus import getBus
from src.control.LevelFileController import LevelFileController
COLUMNS = 5
BORDER_WIDTH = 5

class WrappingButton(QtWidgets.QWidget):
    clicked = QtCore.Signal()

    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.label = QtWidgets.QLabel(text)
        self.label.setProperty("class", "level-button")
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setContentsMargins(0,0,0,0)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def setText(self, text):
        self.label.setText(text)

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

        self.headerLabel = QtWidgets.QLabel("<h1>Select a level</h1>")
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headerLabel.setStyleSheet(f"color: rgb{PR_COLOR_2}")
        self.headerLabel.setContentsMargins(0,0,0,0)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(10)
        self.toggleLevelLockButton = QtWidgets.QPushButton()
        
        if self.levelFileController.getAllLevelsUnlocked():
            self.toggleLevelLockButton.setText("Lock levels")
        else:
            self.toggleLevelLockButton.setText("Unlock all levels")
        self.toggleLevelLockButton.clicked.connect(self.toggleLevelLock)

        mainSceneBtn = QPushButton(text="< Back to Main Screen", parent=self)
        mainSceneBtn.clicked.connect(lambda: self.bus.emit("goToMain"))

        self.layout.addWidget(mainSceneBtn, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.headerLabel)
        self.layout.addSpacing(75)
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.toggleLevelLockButton)

        self.layout.setStretch(3, 1)

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

        col: int = 0
        for blockTitle, blockLevels in levels.items():
            blockTitleLabel = QtWidgets.QLabel(f"<strong>{blockTitle}</strong>")
            blockTitleLabel.setProperty("class", "btn-secondary large")
            blockTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
            blockTitleLabel.setContentsMargins(0,0,0,0)
            self.grid.addWidget(blockTitleLabel, 0, col)
            colButtons = []

            row: int = 1
            for levelId, levelName in blockLevels.items():

                button = WrappingButton()
                text = levelName
                if levelId in completed:
                    text += " (Done)"
                elif not unlocked and int(levelId) > max_completed + 1:
                    text += " (Locked)"
                button.setText(text)
                if not (not unlocked and int(levelId) > max_completed + 1):
                    button.clicked.connect(lambda checked=False, lvl=levelId: self.onLevelClicked(lvl))
                self.grid.addWidget(button, row, col)
                colButtons.append(button)
                row += 1

            self.levelButtons.append(colButtons)
            col += 1
            for i in range(self.grid.columnCount()):
                self.grid.setColumnStretch(i, 1)
            self.update()

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
        while self.grid.count():
            item = self.grid.takeAt(0)
            item.widget().deleteLater()
            del item
        self.levelButtons.clear()
        self.createLevelButtons()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(*PR_COLOR_2), 5)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(pen)

        # Calculate text positions for header
        header_font_metrics = self.headerLabel.fontMetrics()
        header_text_height = header_font_metrics.height()
        header_text_bottom_y = self.headerLabel.geometry().center().y() + header_text_height / 2 + 20

        for col in range(self.grid.columnCount()):
            # Draw line from header label to section header
            p1 = QtCore.QPoint(self.headerLabel.geometry().center().x(), header_text_bottom_y)
            item2 = self.grid.itemAtPosition(0, col)
            p2 = QtCore.QPoint(item2.geometry().center().x(), item2.geometry().top())
            path = QPainterPath(p1)
            midY = (p1.y() + p2.y()) / 2
            path.lineTo(QtCore.QPoint(p1.x(), midY))
            path.lineTo(QtCore.QPoint(p2.x(), midY))
            path.lineTo(p2)
            painter.drawPath(path)

            # Draw lines between each element in column
            for row in range(self.grid.rowCount()):
                # Get button centers relative to this widget
                item1 = self.grid.itemAtPosition(row, col)
                item2 = self.grid.itemAtPosition(row+1, col)
                if item1 is not None and item2 is not None:
                    p1 = QtCore.QPoint(item1.geometry().center().x(), item1.geometry().bottom())
                    p2 = QtCore.QPoint(item2.geometry().center().x(), item2.geometry().top())
                    painter.drawLine(p1, p2)
