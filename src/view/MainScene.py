from PySide6 import QtWidgets
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

        teachingBtn = QPushButton(text="Learning Mode", parent=self)
        teachingBtn.setFixedSize(200, 150)
        teachingBtn.clicked.connect(lambda: self.bus.emit("goToLevelSelection"))

        sandboxBtn = QPushButton(text="Sandbox Mode", parent=self)
        sandboxBtn.setFixedSize(200, 150)
        sandboxBtn.clicked.connect(lambda: self.bus.emit("goToSandboxMode"))


        exitBtn = QPushButton(text="Exit", parent=self)
        exitBtn.setFixedSize(200, 100)
        exitBtn.clicked.connect(lambda: self.bus.emit("stopApp"))


        layout.addWidget(teachingBtn)
        layout.addWidget(sandboxBtn)
        layout.addWidget(exitBtn)

    # def openTeachingMode(self):
    #     from src.view.TeachingModeWindow import TeachingModeWindow
    #     self.teachingWindow = TeachingModeWindow(self.logicController)
    #     self.teachingWindow.show()
    #     self.close()

    def closeApplication(self):
        self.close()