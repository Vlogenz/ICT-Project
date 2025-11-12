
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QLineEdit, QGridLayout, QDialogButtonBox, QPushButton, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from src.control.CustomComponentController import CustomComponentController
from src.control.LogicComponentController import LogicComponentController


class CreateCustomComponentDialog(QDialog):
    """A popup dialog for creating a custom logic component."""

    def __init__(self, logicController: LogicComponentController):
        """
        Initializes the dialog with the following elements:
        - A QLabel and a QLineEdit for each Input and Output component on the grid.
        - A sprite selection button together with a pixmap that shows the currently selected sprite, if any
        - A help button that toggles a small help text on how to use the dialog.
        - Buttons to save or cancel the process.
        """

        super().__init__()
        self.setWindowTitle("Create Custom Component")
        layout = QVBoxLayout()
        self.logicController = logicController

        self.inputNameLabels = []
        self.outputNameLabels = []

        # Component Name
        nameLabel = QLabel("Component Name:")
        self.nameEdit: QLineEdit = QLineEdit()
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

        for input in logicController.inputs:
            inputKeysLayout.addWidget(QLabel(f"Input {len(self.inputNameLabels) + 1} (Bitwidth: {input.getState()['outValue'][1]})"), len(self.inputNameLabels), 0)
            lineEdit = QLineEdit(f"input{len(self.inputNameLabels) + 1}")
            inputKeysLayout.addWidget(lineEdit, len(self.inputNameLabels), 1)
            self.inputNameLabels.append(lineEdit)
        for _ in range(len(logicController.outputs)):
            outputKeysLayout.addWidget(QLabel(f"Output {len(self.outputNameLabels) + 1}"), len(self.outputNameLabels), 0)
            lineEdit = QLineEdit(f"output{len(self.outputNameLabels) + 1}")
            outputKeysLayout.addWidget(lineEdit, len(self.outputNameLabels), 1)
            self.outputNameLabels.append(lineEdit)

        # Sprite Selection
        spriteButton = QPushButton("Select Sprite")
        spriteButton.clicked.connect(self.selectSprite)
        self.spriteLabel = QLabel("No sprite selected")
        self.spriteLabel.setAlignment(Qt.AlignCenter)
        self.spritePath = None
        layout.addWidget(spriteButton)
        layout.addWidget(self.spriteLabel)

        # Help section
        self.helpLabel = QLabel(
            "The order of the inputs and outputs is based on the order you dragged them onto the grid.\n"
            "If you do not remember, drag them on the grid again in the order you would prefer."
        )
        self.helpLabel.hide()
        self.toggleHelpButton = QPushButton("Help")
        self.toggleHelpButton.clicked.connect(self.toggleHelp)
        layout.addWidget(self.toggleHelpButton)
        layout.addWidget(self.helpLabel)

        # Buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.submitForm)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        self.setLayout(layout)
        print("Initialized create custom component dialog")

    def selectSprite(self):
        """Opens a file selection window to select an image file as sprite."""

        file_path, _ = QFileDialog.getOpenFileName(self, "Select Sprite Image", "", "Image Files (*.png *.jpg *.jpeg *.svg)")
        if file_path:
            self.spritePath = file_path
            pixmap = QPixmap(file_path)
            self.spriteLabel.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
            self.spriteLabel.setText("")

    def toggleHelp(self):
        """Toggles whether the help text is visible or not."""

        if self.helpLabel.isVisible():
            self.helpLabel.hide()
            self.toggleHelpButton.setText("Help")
        else:
            self.helpLabel.show()
            self.toggleHelpButton.setText("Hide help")

    def submitForm(self):
        """Collects the data from the form's input fields and sends it to the custom component controller."""

        inputMap = {}
        outputMap = {}
        for i, input in enumerate(self.logicController.inputs):
            key = self.inputNameLabels[i].text()
            inputMap[key] = input.getState()["outValue"][1]
        for i, output in enumerate(self.logicController.outputs):
            key = self.outputNameLabels[i].text()
            outputMap[key] = output.getState()["outValue"][1]

        newComponent = {
            "name": self.nameEdit.text(),
            "inputMap": inputMap,
            "outputMap": outputMap,
            "components": self.logicController.getComponents(),
            "spritePath": self.spritePath,
        }
        print(f"Creating component: {newComponent}")
        CustomComponentController.createCustomComponent(newComponent)
