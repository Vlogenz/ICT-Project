import uuid
from PySide6 import QtWidgets, QtGui, QtCore
import json

from PySide6.QtGui import QAction, QCursor
from PySide6.QtWidgets import QMenu, QPushButton

from src.model.LogicComponent import LogicComponent
from src.constants import CELL_SIZE, MIME_TYPE
from src.infrastructure.eventBus import getBus


class GridItem(QtWidgets.QFrame):
    """An Element in the grid with inputs and outputs"""

    def __init__(self, logicComponent: LogicComponent, color: QtGui.QColor = None, uid=None, parent=None):
        super().__init__(parent)
        self.uid = uid or str(uuid.uuid4())
        self.logicComponent = logicComponent

        self.setFixedSize(CELL_SIZE - 8, CELL_SIZE - 8)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(16,16,16,0)

        self.image_path = f"Gates/{self.logicComponent.__class__.__name__}.png"
        print(self.image_path)

        imgLabel = QtWidgets.QLabel()
        imgLabel.setScaledContents(True)
        pixmap = QtGui.QPixmap(self.image_path)
        if not pixmap.isNull():
            imgLabel.setPixmap(pixmap)
        else:
            imgLabel.setText(self.logicComponent.__class__.__name__)

        self.layout.addWidget(imgLabel)

        # Apply stylesheet
        self.setStyleSheet(f"border: 1px solid lightgray; background-color: {color.name() if color else 'lightgray'};")

        # Define ports dynamically based on what the LogicComponent has
        self.outputs = {
            str(key): QtCore.QRectF(self.width() - 16, (i+1)*(self.height() / (len(self.logicComponent.getState())+1)) - 8, 16, 16)
            for i, key in enumerate(self.logicComponent.getState().keys())
        }
        self.inputs = {
            str(key): QtCore.QRectF(0, (i+1)*(self.height() / (len(self.logicComponent.getInputs())+1)) - 8, 16, 16)
            for i, key in enumerate(self.logicComponent.getInputs())
        }

        # Set up right click menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openContextMenu)

        # Add state label
        self.stateLabel = QtWidgets.QLabel(f"{self.logicComponent.getState()['outValue'][0]}")
        self.stateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.stateLabel)

        # Subscribe to component update
        self.bus = getBus()
        self.bus.subscribe("view:components_updated", self.onComponentUpdated)

    def paintEvent(self, event):
        """Draw the item and the ports. Overrides QWidget.paintEvent, which gets called automatically when update() is called."""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        # Output-Port on the right (blue)
        painter.setBrush(QtGui.QColor("blue"))
        for output_port in self.outputs.values():
            painter.drawEllipse(output_port)
        # Input-Port on the left (green)
        painter.setBrush(QtGui.QColor("green"))
        for input_port in self.inputs.values():
            painter.drawEllipse(input_port)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """Handle dragging of the item or starting a connection from a port."""
        local_pos = event.position().toPoint()
        port = self.portAt(local_pos)

        # If the user clicked on an output, start a connection and pass it to the grid
        if port[0] == "output":
            self.parentWidget().startConnection(self, port[1], event)
            return

        # If the user clicked on an input, remove the connection going to it (if any)
        elif port[0] == "input":
            self.parentWidget().removeConnectionTo(self, port[1])
            return

        # Normal Move-Drag
        if event.button() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            payload = {"action_type": "move", "id": self.uid}
            mime.setData(MIME_TYPE, json.dumps(payload).encode("utf-8"))
            drag.setMimeData(mime)

            pix = QtGui.QPixmap(self.size())
            self.render(pix)
            drag.setPixmap(pix)
            drag.setHotSpot(event.position().toPoint())

            self.hide()  # Hide the original to avoid duplication
            result = drag.exec(QtCore.Qt.MoveAction)
            if result == QtCore.Qt.IgnoreAction:
                self.show()  # Show back if canceled

    def openContextMenu(self):
        """Open a context menu with options like deleting the item."""
        menu = QMenu(self)  # Parent the menu to avoid leaks
        deleteAction = QAction("Delete component", self)
        deleteAction.triggered.connect(self.deleteItem)
        menu.addAction(deleteAction)
        menu.exec_(QCursor.pos())  # Display the menu at the cursor's current position

    def deleteItem(self):
        """Delete this item from the grid."""
        from src.view.GridWidget import GridWidget
        if isinstance(self.parent(), GridWidget):
            self.parent().removeItem(self)

    def portAt(self, pos: QtCore.QPoint):
        """Check if pos is over a port and return the port type along with the key.

        Returns:
            str: The type of the port (input or output)
            str: The key of the port, as used in the backend
        """
        for outputKey, rect in self.outputs.items():
            if rect.contains(pos):
                return "output", outputKey
        for inputKey, rect in self.inputs.items():
            if rect.contains(pos):
                return "input", inputKey
        return None, None

    def getInputRect(self, key: str) -> QtCore.QRectF:
        """Get the QRectF of the input port with the given key."""
        return self.inputs.get(key, None)

    def getOutputRect(self, key: str) -> QtCore.QRectF:
        """Get the QRectF of the output port with the given key."""
        return self.outputs.get(key)

    def onComponentUpdated(self, compList):
        if self.logicComponent in compList:
            self.updateLabel()

    def updateLabel(self):
        self.stateLabel.setText(f"{self.logicComponent.getState()['outValue'][0]}")
