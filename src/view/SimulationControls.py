from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider


class SimulationControls(QtWidgets.QFrame):
    """A control panel with buttons and a slider to control the simulation."""

    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFixedHeight(50)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        self.startStopButton = QtWidgets.QPushButton("Start")
        self.resetButton = QtWidgets.QPushButton("Reset")
        self.speedLabel = QtWidgets.QLabel("Speed:", self)
        self.speedLabel.setStyleSheet("color: black;")

        # Configure speed slider: 1 to 10 steps per second
        self.speedSlider = QSlider(Qt.Horizontal, self)
        self.speedSlider.setRange(1,10)
        self.speedSlider.setSingleStep(1)
        self.speedSlider.setPageStep(1)
        self.speedSlider.setTickPosition(QSlider.TicksBelow)
        self.speedSlider.setTickInterval(1)
        self.speedSlider.valueChanged.connect(self.updateSpeedLabel)

        layout.addWidget(self.startStopButton)
        layout.addWidget(self.resetButton)
        layout.addWidget(self.speedLabel)
        layout.addWidget(self.speedSlider)

        self.updateSpeedLabel(self.speedSlider.value())

    def updateSpeedLabel(self, value):
        """Update the speed label based on the slider value.
        Args:
            value (int): The current value of the speed slider.
        """
        if value == 10:
            self.speedLabel.setText("Speed: Instant")
        elif value == 1:
            self.speedLabel.setText("Speed: 1 step/sec")
        else:
            self.speedLabel.setText(f"Speed: {value} steps/sec")
