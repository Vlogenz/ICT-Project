import uuid
from PySide6 import QtWidgets, QtGui, QtCore
import json

from PySide6.QtGui import QAction, QCursor, QBrush, QPalette
from PySide6.QtWidgets import QMenu, QPushButton

from src.model.LogicComponent import LogicComponent
from src.constants import CELL_SIZE, MIME_TYPE
from src.infrastructure.eventBus import getBus


class GridItem(QtWidgets.QFrame):
    """An Element in the grid with inputs and outputs"""

    def __init__(self, logicComponent: LogicComponent, uid=None, parent=None, **kwargs):
        super().__init__(parent)
        self.uid = uid or str(uuid.uuid4())
        self.logicComponent = logicComponent
        self.immovable = kwargs.get("immovable", False)
        self.scale_factor = kwargs.get("scaleFactor", 1.0)

        base_width = CELL_SIZE - 8
        self.setFixedSize(int(base_width * self.scale_factor), int(base_width * self.scale_factor))

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        
        self.image_path = self.getImagePath()

        self.pixmap = QtGui.QPixmap(self.image_path)
        if self.pixmap.isNull():
            nameLabel = QtWidgets.QLabel(self.getName())
            nameLabel.setAlignment(QtCore.Qt.AlignCenter)
            nameLabel.setStyleSheet("color: black;")
            self.layout.addWidget(nameLabel)

        # Define ports dynamically based on what the LogicComponent has
        self.outputs = {
            str(key): QtCore.QRectF(base_width - 16, (i+1)*(base_width / (len(self.logicComponent.getState())+1)) - 8, 16, 16)
            for i, key in enumerate(self.logicComponent.getState().keys())
        }
        self.inputs = {
            str(key): QtCore.QRectF(0, (i+1)*(base_width / (len(self.logicComponent.getInputs())+1)) - 8, 16, 16)
            for i, key in enumerate(self.logicComponent.getInputs())
        }

        # Create output labels
        self.outputLabels = {}
        for key, rect in self.outputs.items():
            #TODO: Adjust width of the label to content
            label = QtWidgets.QLabel(str(self.logicComponent.getState()[key][0]))
            label.setGeometry(rect.toRect())
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet("border-radius: 8px; background-color: blue; color: white; font-size: 8px;")
            label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
            label.setParent(self)
            self.outputLabels[key] = label

        # Create input labels
        self.inputLabels = {}
        for key, rect in self.inputs.items():
            label = QtWidgets.QLabel("NC")
            label.setGeometry(rect.toRect())
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet("border-radius: 8px; background-color: green; color: white; font-size: 8px;")
            label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
            label.setParent(self)
            self.inputLabels[key] = label

        self.updatePortLabels()
        self.updateRects()

        # Set up right click menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openContextMenu)

        # Subscribe to component update
        self.bus = getBus()
        self.bus.subscribe("view:components_updated", self.onComponentUpdated)

        # Enable mouse tracking for tooltips
        self.setMouseTracking(True)

        print(f"Created GridItem for logic component with id: {self.logicComponent.id}")

    def getImagePath(self) -> str:
        return f"assets/gates/{self.logicComponent.__class__.__name__}.svg"

    def getName(self) -> str:
        return self.logicComponent.__class__.__name__

    def paintEvent(self, event):
        """Draw the item and the ports. Overrides QWidget.paintEvent, which gets called automatically when update() is called."""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        if not self.pixmap.isNull():
            painter.drawPixmap(self.rect(), self.pixmap)

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
        if event.button() == QtCore.Qt.LeftButton and not self.immovable:
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

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        """Update tooltip based on the port under the mouse."""
        pos = event.position().toPoint()
        port = self.portAt(pos)
        if port[0] == "output":
            key = port[1]
            state = self.logicComponent.getState().get(key, "Unknown")
            self.setToolTip(f"Output '{key}':\n- Value: {state[0]}\n- Bitwidth: {state[1]}")
        elif port[0] == "input":
            key = port[1]
            input_conn = self.logicComponent.getInputs().get(key)
            if input_conn and input_conn[0] is not None:
                comp, outkey = input_conn
                state = comp.getState().get(outkey, "Unknown")
                self.setToolTip(f"Input '{key}':\n- Value: {state[0]}\n- Bitwidth: {state[1]}")
            else:
                self.setToolTip(f"Input '{key}': Not connected\n- Bitwidth: {self.logicComponent.inputBitwidths[key]}")
        else:
            self.setToolTip("")

        # If dragging a line, propagate the event to parent for updating the dragging line
        if self.parentWidget() and hasattr(self.parentWidget(), 'draggingLine') and self.parentWidget().draggingLine:
            global_pos = self.mapToParent(event.position().toPoint())
            new_event = QtGui.QMouseEvent(QtGui.QMouseEvent.MouseMove, global_pos, event.button(), event.buttons(), event.modifiers())
            self.parentWidget().mouseMoveEvent(new_event)

    def openContextMenu(self):
        """Open a context menu with options like deleting the item."""
        menu = QMenu(self)  # Parent the menu to avoid leaks
        if not self.immovable:
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
            scaled_rect = QtCore.QRectF(rect.x() * self.scale_factor, rect.y() * self.scale_factor, rect.width() * self.scale_factor, rect.height() * self.scale_factor)
            if scaled_rect.contains(pos):
                return "output", outputKey
        for inputKey, rect in self.inputs.items():
            scaled_rect = QtCore.QRectF(rect.x() * self.scale_factor, rect.y() * self.scale_factor, rect.width() * self.scale_factor, rect.height() * self.scale_factor)
            if scaled_rect.contains(pos):
                return "input", inputKey
        return None, None

    def getInputRect(self, key: str) -> QtCore.QRectF:
        """Get the QRectF of the input port with the given key."""
        rect = self.inputs.get(key, None)
        if rect:
            return QtCore.QRectF(rect.x() * self.scale_factor, rect.y() * self.scale_factor, rect.width() * self.scale_factor, rect.height() * self.scale_factor)
        return None

    def getOutputRect(self, key: str) -> QtCore.QRectF:
        """Get the QRectF of the output port with the given key."""
        rect = self.outputs.get(key)
        if rect:
            return QtCore.QRectF(rect.x() * self.scale_factor, rect.y() * self.scale_factor, rect.width() * self.scale_factor, rect.height() * self.scale_factor)
        return None

    def updateRects(self):
        """Update the geometry of labels based on scale_factor."""
        scale = self.scale_factor
        for key, rect in self.outputs.items():
            scaled_rect = QtCore.QRectF(rect.x() * scale, rect.y() * scale, rect.width() * scale, rect.height() * scale)
            self.outputLabels[key].setGeometry(scaled_rect.toRect())
        for key, rect in self.inputs.items():
            scaled_rect = QtCore.QRectF(rect.x() * scale, rect.y() * scale, rect.width() * scale, rect.height() * scale)
            self.inputLabels[key].setGeometry(scaled_rect.toRect())

    def onComponentUpdated(self, compList):
        """Event handler for the view:components_updated event. Updated port labels."""
        if self.logicComponent in compList:
            self.updatePortLabels()

    def updatePortLabels(self):
        """Updates all port labels of the GridItem according to the underlying values in the backend.
        If an input port is not connected, it will show 'NC'.
        """
        for key, label in self.outputLabels.items():
            state = self.logicComponent.getState().get(key, [0, 0])
            label.setText(str(state[0]))
        for key, label in self.inputLabels.items():
            input_conn = self.logicComponent.getInputs().get(key)
            if input_conn and input_conn[0] is not None:
                comp, outkey = input_conn
                state = comp.getState().get(outkey, [0, 0])
                label.setText(str(state[0]))
            else:
                label.setText("NC")

    def unsubscribe(self):
        """Removes the subscription to the view:components_updated event.
        Should be called first whenever you delete a GridItem.
        """
        self.bus.unsubscribe("view:components_updated", self.onComponentUpdated)
