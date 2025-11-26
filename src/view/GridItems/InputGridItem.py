from src.constants import CELL_SIZE
from src.view.GridItems.GridItem import GridItem
from src.model.Input import Input
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QPushButton, QLineEdit


class InputGridItem(GridItem):
    """A specific kind of GridItem that represents an Input component.
    In addition to the regular GridItem, it has a button that can cycle the bitwidth, as well as one for the input value.
    This is used to set the state of the underlying Input component and defaults to 0.
    """

    def __init__(self, logicComponent: Input, **kwargs):
        super().__init__(logicComponent, **kwargs)
        self.fixedValue: bool = kwargs.get("fixedValue", False)
        self.logicComponent = logicComponent
        self.outputs["outValue"].moveTo(CELL_SIZE - 24, 8)
        self.updateRects()

        # Create the button to rotate through bitwidths
        self.bitwidthButton = QPushButton(f"Bitwidth: {self.logicComponent.state["outValue"][1]}")
        self.layout.addWidget(self.bitwidthButton)

        # Add the toggle for 1 bit
        self.toggleButton = QPushButton(f"Toggle")
        self.layout.addWidget(self.toggleButton)

        self.toggleButton.hide()

        # Add the text box for 8/32 bits
        self.numberInput = QLineEdit()
        # Set the initial value from the component's state
        self.numberInput.insert(str(self.logicComponent.state["outValue"][0]))
        self.numberInput.setMaxLength(10)
        self.numberInput.setValidator(QIntValidator())

        self.layout.addWidget(self.numberInput)
        self.numberInput.hide()

        if not self.fixedValue:
            self.bitwidthButton.clicked.connect(self.cycleBitwidth)
            self.toggleButton.clicked.connect(self.toggleState)
            self.numberInput.editingFinished.connect(self.enterState)
        else:
            self.bitwidthButton.setDisabled(True)
            self.toggleButton.setDisabled(True)
            self.toggleButton.setStyleSheet("color:gray;")
            self.numberInput.setReadOnly(True)

        self.refresh()
    
    def refresh(self):

        # Determine whether or not we should change input via toggle or input
        if self.logicComponent.state["outValue"][1] == 1:
            self.numberInput.hide()
            self.toggleButton.show()
            self.toggleState()  # Done twice to force a refresh
            self.toggleState()

        else:
            self.toggleButton.hide()
            self.numberInput.show()
            self.enterState()
            
    def toggleState(self):
        self.logicComponent.toggleState()
        self.updatePortLabels()

    def cycleBitwidth(self): 
        self.logicComponent.cycleBitwidth()
        self.bitwidthButton.setText(f"Bitwidth: {self.logicComponent.state["outValue"][1]}")
        self.updatePortLabels()
        self.refresh()

    def enterState(self):
        enteredInt = int(self.numberInput.text())
        if self.logicComponent.state["outValue"][1] == 8 and enteredInt > 255:
            self.numberInput.setText("255")

        self.logicComponent.enteredState(enteredInt)
        self.updatePortLabels()