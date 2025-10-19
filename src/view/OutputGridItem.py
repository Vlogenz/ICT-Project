from src.view.GridItem import GridItem
from src.model.Output import Output
from PySide6.QtWidgets import QLabel
from src.infrastructure.eventBus import getBus

class OutputGridItem(GridItem):
    def __init__(self, logicComponent: Output):
        super().__init__(logicComponent)
        self.logicComponent = logicComponent

        self.stateLabel = QLabel(f"{self.logicComponent.getState()['outValue'][0]}")
        self.layout.addWidget(self.stateLabel)

        self.bus = getBus()
        self.bus.subscribe("view:component_updated", self.onComponentUpdated)

    # TODO: Fix event listening
    def onComponentUpdated(self, comp):
        self.updateLabel()

    def updateLabel(self):
        print(f"Updating output")
        self.stateLabel.setText(f"{self.logicComponent.getState()['outValue'][0]}")
