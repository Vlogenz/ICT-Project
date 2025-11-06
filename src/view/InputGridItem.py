from src.view.GridItem import GridItem
from src.model.Input import Input
from PySide6.QtWidgets import QPushButton


class InputGridItem(GridItem):
    """A specific kind of GridItem that represents an Input component.
    In addition to the regular GridItem, it has a button that can be toggled between 0 and 1.
    This is used to set the state of the underlying Input component and defaults to 0.
    """

    def __init__(self, logicComponent: Input, immovable=False):
        super().__init__(logicComponent, immovable=immovable)
        self.logicComponent = logicComponent

        # Add a toggle button
        self.toggleButton = QPushButton(f"Toggle")
        self.toggleButton.setStyleSheet("color: black;")
        self.toggleButton.clicked.connect(self.toggleState)
        self.layout.addWidget(self.toggleButton)

    def toggleState(self):
        self.logicComponent.toggleState()
        self.updatePortLabels()
