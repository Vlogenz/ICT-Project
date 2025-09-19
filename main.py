import sys

from PySide6 import QtWidgets

from view.SandboxModeWindow import SandboxModeWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = SandboxModeWindow()
    w.show()
    sys.exit(app.exec())
