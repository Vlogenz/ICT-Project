from PySide6.QtWidgets import QWidget, QDialog, QLabel, QVBoxLayout, QLineEdit, QGridLayout, QDialogButtonBox, QPushButton, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from src.control.LogicComponentController import LogicComponentController
from src.model import Input, Output


class CreateCustomComponentDialog(QDialog):
    def __init__(self, logicController: LogicComponentController):
        super().__init__()
        self.setWindowTitle("Create Custom Component")

        layout = QVBoxLayout()

        self.inputNameLabels = []
        self.outputNameLabels = []

        # Component Name
        nameLabel = QLabel("Component Name:")
        self.nameEdit = QLineEdit()
        layout.addWidget(nameLabel)
        layout.addWidget(self.nameEdit)

        # Name the input labels
        inputKeysLabel = QLabel("Set keys for the inputs:")
        inputKeysLayout = QGridLayout()
        layout.addWidget(inputKeysLabel)
        layout.addLayout(inputKeysLayout)

        # Name the output labels
        outputKeysLabel = QLabel("Set keys for the outputs:")
        layout.addWidget(outputKeysLabel)
        outputKeysLayout = QGridLayout()
        layout.addLayout(outputKeysLayout)

        for component in logicController.components:
            if isinstance(component, Input):
                inputKeysLayout.addWidget(QLabel(f"Input {len(self.inputNameLabels) + 1} (Bitwidth: {component.getState()['outValue'][1]})"), len(self.inputNameLabels), 0)
                lineEdit = QLineEdit(f"input{len(self.inputNameLabels) + 1}")
                inputKeysLayout.addWidget(lineEdit, len(self.inputNameLabels), 1)
                self.inputNameLabels.append(lineEdit)
            elif isinstance(component, Output):
                outputKeysLayout.addWidget(QLabel(f"Output {len(self.outputNameLabels) + 1}"), len(self.outputNameLabels), 0)
                lineEdit = QLineEdit(f"output{len(self.outputNameLabels) + 1}")
                outputKeysLayout.addWidget(lineEdit, len(self.outputNameLabels), 1)
                self.outputNameLabels.append(lineEdit)

        # Sprite Selection
        spriteButton = QPushButton("Select Sprite")
        spriteButton.clicked.connect(self.select_sprite)
        self.spriteLabel = QLabel("No sprite selected")
        self.spriteLabel.setAlignment(Qt.AlignCenter)
        self.spritePath = None
        layout.addWidget(spriteButton)
        layout.addWidget(self.spriteLabel)

        # Buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        self.setLayout(layout)
        print("Initialized create custom component dialog")

    def select_sprite(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Sprite Image", "", "Image Files (*.png *.jpg *.jpeg *.svg)")
        if file_path:
            self.spritePath = file_path
            pixmap = QPixmap(file_path)
            self.spriteLabel.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
            self.spriteLabel.setText("")
