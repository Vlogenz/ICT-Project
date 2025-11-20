# src/view/MainScene.py
from pathlib import Path
from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtWidgets import QPushButton, QLabel

from src.constants import APP_NAME, BG_COLOR, PR_COLOR_1, PR_COLOR_2
from src.infrastructure.eventBus import getBus


class MainScene(QtWidgets.QMainWindow):
    # Main Window to select which mode the user wants use
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.bus = getBus()

        central = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(central)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(30)
        self.setCentralWidget(central)

        layout.setRowStretch(0, 2)   # top area
        layout.setRowStretch(1, 5)   # logo
        layout.setRowStretch(2, 1)   # spacer
        layout.setRowStretch(3, 2)   # buttons

        # ensure 3 equal columns for button alignment
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        # Logo (PNG) in the middle row, spanning all 3 columns
        image_path = Path("assets/gates/MainScreenLogo.png")
        logo_label = QLabel(self)
        logo_label.setAlignment(QtCore.Qt.AlignCenter)


        pixmap = QtGui.QPixmap(str(image_path))
        scaled_pixmap = pixmap.scaled(450, 450, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)


        layout.addWidget(logo_label, 1, 0, 1, 3, alignment=QtCore.Qt.AlignCenter)

        # Buttons container placed in the bottom row, centered and horizontal
        btn_container = QtWidgets.QWidget()
        btn_layout = QtWidgets.QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(40, 10, 40, 40)
        btn_layout.setSpacing(100)
        btn_layout.setAlignment(QtCore.Qt.AlignCenter)

        teachingBtn = QPushButton(text="Learning", parent=self)
        teachingBtn.setMinimumSize(200, 120)
        teachingBtn.setProperty("class", "large")
        teachingBtn.clicked.connect(lambda: self.bus.emit("goToLevelSelection"))

        sandboxBtn = QPushButton(text="Sandbox", parent=self)
        sandboxBtn.setProperty("class", "btn-secondary large")
        sandboxBtn.setMinimumSize(200, 120)
        sandboxBtn.clicked.connect(lambda: self.bus.emit("goToSandboxMode"))

        exitBtn = QPushButton(text="Exit", parent=self)
        exitBtn.setMinimumSize(200, 120)
        exitBtn.setProperty("class", "large")
        exitBtn.clicked.connect(lambda: self.bus.emit("stopApp"))

        btn_layout.addWidget(teachingBtn)
        btn_layout.addWidget(sandboxBtn)
        btn_layout.addWidget(exitBtn)

        # put the container in the grid's bottom row spanning 3 columns
        layout.addWidget(btn_container, 3, 0, 1, 3, alignment=QtCore.Qt.AlignCenter)

    def closeApplication(self):
        self.close()