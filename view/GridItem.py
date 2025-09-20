import uuid
from PySide6 import QtWidgets, QtGui, QtCore
import json

from constants import CELL_SIZE, MIME_TYPE


class GridItem(QtWidgets.QFrame):
    """An Element in the grid with inputs and outputs"""

    def __init__(self, item_type: str, color: QtGui.QColor = None, uid=None, parent=None):
        super().__init__(parent)
        self.uid = uid or str(uuid.uuid4())
        self.item_type = item_type

        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setLineWidth(2)
        self.setFixedSize(CELL_SIZE - 8, CELL_SIZE - 8)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        lbl = QtWidgets.QLabel(item_type)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(lbl)

        if color:
            pal = self.palette()
            pal.setColor(self.backgroundRole(), color)
            self.setAutoFillBackground(True)
            self.setPalette(pal)

        # Define ports
        # TODO: change ports to arrays/list
        self.output_port = QtCore.QRectF(self.width() - 16, self.height() / 2 - 8, 16, 16)
        self.input_port = QtCore.QRectF(0, self.height() / 2 - 8, 16, 16)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        # Output-Port on the right (blue)
        painter.setBrush(QtGui.QColor("blue"))
        painter.drawEllipse(self.output_port)
        # Input-Port on the left (green)
        painter.setBrush(QtGui.QColor("green"))
        painter.drawEllipse(self.input_port)

    def port_at(self, pos: QtCore.QPoint):
        """Check if pos is over a port."""
        if self.output_port.contains(pos):
            return "output"
        if self.input_port.contains(pos):
            return "input"
        return None

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        local_pos = event.position().toPoint()
        port = self.port_at(local_pos)
        if port == "output":
            # Start a connector -> pass to grid
            self.parentWidget().start_connection(self, "output", event)
            return
        elif port == "input":
            return

        # normal Move-Drag
        if event.button() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            payload = {"action": "move", "id": self.uid}
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

    # TODO: Double click should not be for removing perspectively. Add a bin to drag items to.
    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        from view.GridWidget import GridWidget
        if isinstance(self.parent(), GridWidget):
            self.parent().remove_item(self.uid)