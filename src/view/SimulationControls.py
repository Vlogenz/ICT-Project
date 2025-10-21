from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider, QPushButton, QLabel

from src.control.LogicComponentController import LogicComponentController


class SimulationControls(QtWidgets.QFrame):
    """A control panel with buttons and a slider to control the simulation."""

    def __init__(self, logicController: LogicComponentController):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFixedHeight(50)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        self.logicController = logicController

        self.startStopButton: QPushButton = QPushButton("Start")
        self.resetButton: QPushButton = QPushButton("Reset")
        self.speedLabel: QLabel = QLabel("Speed:", self)
        self.speedLabel.setStyleSheet("color: black;")

        # Configure speed slider: 1 to 10 steps per second
        self.speedSlider: QSlider = QSlider(Qt.Horizontal, self)
        self.speedSlider.setRange(1,10)
        self.speedSlider.setSingleStep(1)
        self.speedSlider.setPageStep(1)
        self.speedSlider.setTickPosition(QSlider.TicksBelow)
        self.speedSlider.setTickInterval(1)
        self.speedSlider.valueChanged.connect(self.updateSpeed)

        self.configureControlFunctionality()

        layout.addWidget(self.startStopButton)
        layout.addWidget(self.resetButton)
        layout.addWidget(self.speedLabel)
        layout.addWidget(self.speedSlider)

        self.updateSpeed(self.speedSlider.value())

    def updateSpeed(self, value):
        """Update the speed and its label based on the slider value.
        Args:
            value (int): The current value of the speed slider.
        """
        if value == 10:
            self.logicController.setTickLength(0)
            self.speedLabel.setText("Speed: Instant")
        else:
            self.logicController.setTickLength(1 / value)
            if value == 1:
                self.speedLabel.setText("Speed: 1 step/sec")
            else:
                self.speedLabel.setText(f"Speed: {value} steps/sec")
        print(f"New tick length: {self.logicController.tickLength}")

    def configureControlFunctionality(self):
        self.startStopButton.clicked.connect(self.startSimulation)

    def startSimulation(self):
        self.logicController.eval()