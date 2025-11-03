
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QPushButton
from src.infrastructure.eventBus import getBus
import pyfiglet

class MainScene(QtWidgets.QMainWindow):
    # Main Window to select which mode the user wants use

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.bus = getBus()

        central = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(central)
        self.setCentralWidget(central)

        # ASCII Art Überschrift
        fig = pyfiglet.Figlet(font='slant')  # oder 'banner', 'big', 'block', etc.
        ascii_art = fig.renderText("Gated Neighbourhood")

        titleLabel = QtWidgets.QLabel(ascii_art)
        titleLabel.setStyleSheet("font-family: 'Courier'; font-size: 25px;")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titleLabel, 0,0,1,2)

        teachingBtn = QPushButton(text="Learning Mode", parent=self)
        teachingBtn.setMinimumSize(200, 150)
        teachingBtn.clicked.connect(lambda: self.bus.emit("goToLevelSelection"))

        sandboxBtn = QPushButton(text="Sandbox Mode", parent=self)
        sandboxBtn.setMinimumSize(200, 150)
        sandboxBtn.clicked.connect(lambda: self.bus.emit("goToSandboxMode"))


        exitBtn = QPushButton(text="Exit", parent=self)
        exitBtn.setMinimumSize(200, 100)
        exitBtn.clicked.connect(lambda: self.bus.emit("stopApp"))


        layout.addWidget(teachingBtn, 1,0)
        layout.addWidget(sandboxBtn, 1,1)
        layout.addWidget(exitBtn, 2,0,1,2)

    def closeApplication(self):
        self.close()