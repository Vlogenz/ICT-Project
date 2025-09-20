import sys
from view.PaletteItem import PaletteItem
from view.GridWidget import GridWidget

from PySide6 import QtGui, QtWidgets

class SandboxModeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sandbox Mode")

        central = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central)
        self.setCentralWidget(central)

        # Palette
        # TODO: Show all available logic components here
        palette = QtWidgets.QVBoxLayout()
        palette.addWidget(PaletteItem("Label"))
        palette.addWidget(PaletteItem("Red Node", QtGui.QColor("#ff9999")))
        palette.addStretch()

        palette_frame = QtWidgets.QFrame()
        palette_frame.setLayout(palette)
        palette_frame.setFixedWidth(120)

        # Grid
        grid = GridWidget()

        layout.addWidget(palette_frame)
        layout.addWidget(grid, 1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = SandboxModeWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()