from PySide6 import QtWidgets
import sys

from src.control.LogicComponentController import LogicComponentController
from src.view.SandboxModeWindow import SandboxModeWindow

class AppController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.logicController = LogicComponentController()
        self.window = SandboxModeWindow(logicController)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())
