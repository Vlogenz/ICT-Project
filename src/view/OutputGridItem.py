from src.view.GridItem import GridItem
from src.model.Output import Output
from PySide6.QtWidgets import QLabel
from src.infrastructure.eventBus import getBus

class OutputGridItem(GridItem):
    """A specific kind of GridItem that represents an Output component.
    In addition to a regular GridItem, it has a label displaying the current state of the underlying Output component.
    This label uses the eventBus to subscribe to the actual value in the backend.
    """

    def __init__(self, logicComponent: Output):
        super().__init__(logicComponent)
        self.logicComponent = logicComponent

        self.stateLabel = QLabel(f"{self.logicComponent.getState()['outValue'][0]}")
        self.layout.addWidget(self.stateLabel)

        self.bus = getBus()
        self.bus.subscribe("view:components_updated", self.onComponentUpdated)

    def onComponentUpdated(self, compList):
        if self.logicComponent in compList:
            self.updateLabel()

    def updateLabel(self):
        self.stateLabel.setText(f"{self.logicComponent.getState()['outValue'][0]}")
