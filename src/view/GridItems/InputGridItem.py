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
        # Respect the parent GridItem's `immovable` flag instead of
        # introducing a separate `immutable` attribute which would
        # conflict with tests and parent behavior.
        self.logicComponent = logicComponent
        self.outputs["outValue"].moveTo(CELL_SIZE - 24, 8)
        self.updateRects()
        # Always create attributes so other methods can rely on their existence
        self.bitwidthButton = None
        self.bitwidthLabel = None
        self.toggleButton = None
        self.numberInput = None

        # If the item is movable (interactive) create interactive widgets.
        # The parent `GridItem` sets `self.immovable` from constructor kwargs.
        if not getattr(self, 'immovable', False):
            # Create the button to rotate through bitwidths (interactive)
            self.bitwidthButton = QPushButton(f"Bitwidth: {self.logicComponent.state['outValue'][1]}")
            self.bitwidthButton.clicked.connect(self.cycleBitwidth)
            self.layout.addWidget(self.bitwidthButton)

            # Add the toggle for 1 bit (interactive)
            self.toggleButton = QPushButton("Toggle")
            self.toggleButton.setStyleSheet("color: black;")
            self.toggleButton.clicked.connect(self.toggleState)
            self.layout.addWidget(self.toggleButton)
            self.toggleButton.hide()

            # Add the text box for 8/32 bits (interactive)
            self.numberInput = QLineEdit()
            self.numberInput.insert("0")
            self.numberInput.setMaxLength(10)
            self.numberInput.setValidator(QIntValidator())
            self.numberInput.editingFinished.connect(self.enterState)
            self.layout.addWidget(self.numberInput)
            self.numberInput.hide()

        else:
            # Immovable mode: create non-interactive widgets but keep attribute names
            # so methods that update UI won't crash. Widgets are read-only/disabled
            # and hidden from user interaction; cycling should be done via code.
            self.bitwidthButton = QPushButton(f"Bitwidth: {self.logicComponent.state['outValue'][1]}")
            self.bitwidthButton.setEnabled(False)
            self.bitwidthButton.hide()
            self.layout.addWidget(self.bitwidthButton)

            # Visible read-only label for bitwidth
            self.bitwidthLabel = QLineEdit()
            self.bitwidthLabel.setReadOnly(True)
            self.bitwidthLabel.setText(f"Bitwidth: {self.logicComponent.state['outValue'][1]}")
            self.layout.addWidget(self.bitwidthLabel)

            # Keep the same attribute names used elsewhere so refresh() works,
            # but use read-only QLineEdit widgets.
            self.toggleButton = QLineEdit()
            self.toggleButton.setReadOnly(True)
            self.toggleButton.setText(str(self.logicComponent.state['outValue'][0]))
            self.layout.addWidget(self.toggleButton)
            self.toggleButton.hide()

            self.numberInput = QLineEdit()
            self.numberInput.setReadOnly(True)
            self.numberInput.setText(str(self.logicComponent.state['outValue'][0]))
            self.layout.addWidget(self.numberInput)
            self.numberInput.hide()

        self.refresh()
    
    def refresh(self):
        # Update UI elements to reflect the current logicComponent state
        bw = self.logicComponent.state["outValue"][1]
        val = self.logicComponent.state["outValue"][0]

        # Update bitwidth displays if they exist
        if self.bitwidthButton is not None:
            try:
                self.bitwidthButton.setText(f"Bitwidth: {bw}")
            except Exception:
                # avoid crashing if widget is disabled or not a QPushButton
                pass
        if self.bitwidthLabel is not None:
            self.bitwidthLabel.setText(f"Bitwidth: {bw}")

        # For 1-bit inputs show the toggle; for multi-bit show the numeric input.
        if bw == 1:
            if self.numberInput is not None:
                self.numberInput.hide()
            if self.toggleButton is not None:
                self.toggleButton.show()
                # Update the toggle UI to reflect the current value WITHOUT changing the model
                try:

                    # If toggleButton is a plain QPushButton keep its label
                    # as an action (e.g. "Toggle"). Only update text when
                    # the toggle widget is a QLineEdit (immutable/read-only)
                    if not isinstance(self.toggleButton, QPushButton):
                        self.toggleButton.setText(str(val))
                except Exception:
                    pass
        else:
            if self.toggleButton is not None:
                self.toggleButton.hide()
            if self.numberInput is not None:
                self.numberInput.show()
                # Update the number input to reflect the current value WITHOUT changing the model
                try:
                    self.numberInput.setText(str(val))
                except Exception:
                    pass
            
    def toggleState(self):
        # Toggle underlying model state (only available when interactive)
        self.logicComponent.toggleState()
        self.updatePortLabels()
        # Update UI to reflect new state
        if self.toggleButton is not None:
            try:
                if not isinstance(self.toggleButton, QPushButton):
                    self.toggleButton.setText(str(self.logicComponent.state['outValue'][0]))
            except Exception:
                pass

    def cycleBitwidth(self): 
        # Cycle the bitwidth on the model. UI reflects the change but in
        # immutable mode the widgets are disabled/hidden and only updated.
        self.logicComponent.cycleBitwidth()
        bw = self.logicComponent.state['outValue'][1]
        if self.bitwidthButton is not None:
            try:
                self.bitwidthButton.setText(f"Bitwidth: {bw}")
            except Exception:
                pass
        if self.bitwidthLabel is not None:
            self.bitwidthLabel.setText(f"Bitwidth: {bw}")
        self.updatePortLabels()
        self.refresh()

    def enterState(self, setValue=None):
        """
        Set the input value. If `setValue` is provided, this method will set the
        underlying model regardless of `immutable` (this is intended for hard-
        coded setup). If `setValue` is None, the value is read from the UI and
        will only be applied when the widget is interactive.
        """
        # Determine the integer to set
        if setValue is not None:
            try:
                enteredInt = int(setValue)
            except Exception:
                enteredInt = 0
        else:
            # No explicit value provided; attempt to read from UI input
            if self.numberInput is None:
                return
            try:
                enteredInt = int(self.numberInput.text())
            except Exception:
                enteredInt = 0

        # clamp for 8-bit
        if self.logicComponent.state["outValue"][1] == 8 and enteredInt > 255:
            enteredInt = 255
            if self.numberInput is not None:
                try:
                    self.numberInput.setText("255")
                except Exception:
                    pass

        # If no explicit setValue provided and immovable, don't change the model
        # (immovable == non-interactive)
        if setValue is None and getattr(self, 'immovable', False):
            # Refresh UI display to match model
            if self.numberInput is not None:
                try:
                    self.numberInput.setText(str(self.logicComponent.state['outValue'][0]))
                except Exception:
                    pass
            return

        # Apply to model and update UI
        self.logicComponent.enteredState(enteredInt)
        self.updatePortLabels()
        # Ensure UI reflects the new state
        try:
            if self.numberInput is not None:
                self.numberInput.setText(str(enteredInt))
        except Exception:
            pass
        self.refresh()