import uuid
from PySide6 import QtWidgets, QtGui, QtCore
import json

from PySide6.QtGui import QAction, QCursor
from PySide6.QtWidgets import QMenu

from src.model.LogicComponent import LogicComponent
from src.constants import CELL_SIZE, MIME_TYPE


class GridItem(QtWidgets.QFrame):
    """An Element in the grid with inputs and outputs"""

    def __init__(self, logicComponent: LogicComponent, color: QtGui.QColor = None, uid=None, parent=None):
        super().__init__(parent)
        self.uid = uid or str(uuid.uuid4())
        self.logicComponent = logicComponent

        self.setFixedSize(CELL_SIZE - 8, CELL_SIZE - 8)

        layout = QtWidgets.QVBoxLayout(self)
        lbl = QtWidgets.QLabel(self.logicComponent.__class__.__name__)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(lbl)

        # Apply stylesheet
        self.setStyleSheet(f"border: 1px solid lightgray; background-color: {color.name() if color != None else 'lightgray'};")

        # Define ports dynamically based on what the LogicComponent has
        if not len(self.logicComponent.getOutputs()) == 0:
            self.outputs = [
                (port, QtCore.QRectF(self.width() - 16, (i+1)*(self.height() / (len(self.logicComponent.getOutputs())+1)) - 8, 16, 16))
                for i, port in enumerate(self.logicComponent.getOutputs())
            ]
        else:
            self.outputs = []
        self.inputs = [
            (port, QtCore.QRectF(0, (i+1)*(self.height() / (len(self.logicComponent.getInputs())+1)) - 8, 16, 16))
            for i, port in enumerate(self.logicComponent.getInputs())
        ]
        print(f"outputs: {self.outputs}, inputs: {self.inputs}")

        # Set up right click menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openContextMenu)

    def paintEvent(self, event):
        """Draw the item and the ports. Overrides QWidget.paintEvent, which gets called automatically when update() is called."""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        # Output-Port on the right (blue)
        painter.setBrush(QtGui.QColor("blue"))
        for output_port in self.inputs:
            painter.drawEllipse(output_port[1])
        # Input-Port on the left (green)
        painter.setBrush(QtGui.QColor("green"))
        for input_port in self.outputs:
            painter.drawEllipse(input_port[1])

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """Handle dragging of the item or starting a connection from a port."""
        local_pos = event.position().toPoint()
        port = self.portAt(local_pos)

        # If the user clicked on an output, start a connection and pass it to the grid
        if port[0] == "output":
            self.parentWidget().startConnection(self, port, event)
            return

        # If the user clicked on an input, remove the connection going to it (if any)
        elif port[0] == "input":
            self.parentWidget().removeConnectionTo(self)
            return

        # normal Move-Drag
        if event.button() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            payload = {"action_type": "move", "id": self.uid}
            mime.setData(MIME_TYPE, json.dumps(payload).encode("utf-8"))
            drag.setMimeData(mime)

            pix = QtGui.QPixmap(self.size())
            self.render(pix)
            drag.setPixmap(pix)

            hotspot = event.position().toPoint()  # QPoint relative to widget
            drag.setHotSpot(hotspot)

            self.hide()
            result = drag.exec(QtCore.Qt.MoveAction)
            if result == QtCore.Qt.IgnoreAction:
                self.show()

    def openContextMenu(self):
        """Open a context menu with options like deleting the item."""

        menu = QMenu(self)  # Parent the menu to avoid leaks
        deleteAction = QAction("Delete component", self)
        deleteAction.triggered.connect(self.deleteItem)
        menu.addAction(deleteAction)

        menu.exec_(QCursor.pos()) # Display the menu at the cursor's current position

    def deleteItem(self):
        """Delete this item from the grid."""
        from src.view.GridWidget import GridWidget
        if isinstance(self.parent(), GridWidget):
            self.parent().removeItem(self.uid)

    def portAt(self, pos: QtCore.QPoint):
        """Check if pos is over a port."""
        for output_port, rect in self.outputs:
            if rect.contains(pos):
                return "output", output_port
        for input_port, rect in self.inputs:
            if rect.contains(pos):
                return "input", input_port
        return None, None
