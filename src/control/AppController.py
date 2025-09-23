from PySide6 import QtWidgets
import sys

from src.view.SandboxModeWindow import SandboxModeWindow

class AppController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = SandboxModeWindow()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())
