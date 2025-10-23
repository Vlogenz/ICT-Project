from typing import override

from src.view.GridItem import GridItem
from src.model.Input import Input
from PySide6.QtWidgets import QPushButton


class InputGridItem(GridItem):
    """A specific kind of GridItem that represents an Input component.
    In addition to the regular GridItem, it has a button that can be toggled between 0 and 1.
    This is used to set the state of the underlying Input component and defaults to 0.
    """

    def __init__(self, logicComponent: Input):
        super().__init__(logicComponent)
        self.logicComponent = logicComponent

        # Turn stateLabel into a button
        self.layout.removeWidget(self.stateLabel)
        self.stateLabel.deleteLater()
        self.stateLabel = QPushButton(f"{self.logicComponent.getState()['outValue'][0]}")
        self.stateLabel.clicked.connect(self.toggleState)
        self.layout.addWidget(self.stateLabel)

    def toggleState(self):
        self.logicComponent.toggleState()
        self.updateLabel()
