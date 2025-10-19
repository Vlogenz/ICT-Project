from src.view.GridItem import GridItem
from src.model.Input import Input
from PySide6.QtWidgets import QPushButton


class InputGridItem(GridItem):
    def __init__(self, logicComponent: Input):
        super().__init__(logicComponent)
        self.logicComponent = logicComponent

        self.toggleStateButton = QPushButton(f"{self.logicComponent.getState()['outValue'][0]}")
        self.toggleStateButton.clicked.connect(self.toggleState)
        self.layout.addWidget(self.toggleStateButton)

    def toggleState(self):
        self.logicComponent.toggleState()
        self.toggleStateButton.setText(f"{self.logicComponent.getState()['outValue'][0]}")
