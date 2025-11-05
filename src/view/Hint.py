
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QMessageBox

from src.control.LevelController import LevelController

class Hint(QtWidgets.QPushButton):
    """Button to show a hint for the current level"""

    def __init__(self, levelController: LevelController, parent=None):
        super().__init__(parent)
        self.levelController = levelController
        #self.setFixedSize(80, 80)
        self.image_path = "assets/sprites/LampOff.svg"
        icon = QtGui.QIcon(self.image_path)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(70, 70))
        self.current_hint_index = 0
        self.levelData = self.levelController.getLevel()

        # Connect the button's own clicked signal
        self.clicked.connect(self.show_hint)

    def show_hint(self):
        self.change_icon()
        hints = self.levelController.getHints()
        if not hints:
            QtWidgets.QMessageBox.information(self, "No Hints", "No hints available for this level.")
            return

        hint_text = hints[self.current_hint_index]
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Hint")
        msgBox.setText(hint_text)

        pixmap = QtGui.QPixmap("assets/sprites/LampOn.svg")
        msgBox.setIconPixmap(pixmap.scaled(70, 70, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        # Add buttons depending on hint index
        next_button = None
        if self.current_hint_index < len(hints) - 1:
            next_button = msgBox.addButton("Next", QMessageBox.ButtonRole.AcceptRole)
        exit_button = msgBox.addButton("Exit", QMessageBox.ButtonRole.RejectRole)

        msgBox.exec()

        clicked_button = msgBox.clickedButton()
        if clicked_button == next_button:
            self.current_hint_index += 1
            self.show_hint()
        else:
            self.current_hint_index = 0  # Reset for next time

    def change_icon(self):
        self.image_path = "assets/sprites/LampOn.svg"
        icon = QtGui.QIcon(self.image_path)
        self.setIcon(icon)
