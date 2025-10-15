from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainterPath

from constants import GRID_COLS, GRID_ROWS, CELL_SIZE, MIME_TYPE
from src.view.GridItem import GridItem, portAt
import json
import random


class GridWidget(QtWidgets.QWidget):
    """Main drop area with grid, items and connections."""

    def __init__(self, cols=GRID_COLS, rows=GRID_ROWS, parent=None):
        super().__init__(parent)
        self.cols = cols
        self.rows = rows
        self.setAcceptDrops(True)
        self.items = {}  # uid -> (x, y, widget)
        self.connections = []  # Liste (src_uid, dst_uid)
        self.dragging_line = None  # (src_uid, start, current)
        self.dragging_item_pos = None
        self.dragging_item_uid = None
        self.setMinimumSize(cols * CELL_SIZE, rows * CELL_SIZE)

        # The random offset is used to avoid overlapping lines
        # It should be set to False when dragging an item or a line so that is does not look weird
        self.useRandomOffset = True

    def paintEvent(self, event):
        """Redraws the entire grid, items and connections. It overrides QWidget.paintEvent, which gets called automatically when update() is called."""
        painter = QtGui.QPainter(self)

        # Grid
        pen = QtGui.QPen(QtGui.QColor(200, 200, 200))
        painter.setPen(pen)
        for c in range(self.cols + 1):
            x = c * CELL_SIZE
            painter.drawLine(x, 0, x, self.rows * CELL_SIZE)
        for r in range(self.rows + 1):
            y = r * CELL_SIZE
            painter.drawLine(0, y, self.cols * CELL_SIZE, y)

        # painting connections
        pen_conn = QtGui.QPen(QtGui.QColor("black"), 2)
        painter.setPen(pen_conn)
        for src, dst in self.connections:
            if src in self.items and dst in self.items:
                _, _, src_item = self.items[src]
                _, _, dst_item = self.items[dst]

                # Currently dragged item position
                if self.dragging_item_uid == src:
                    src_pos = self.dragging_item_pos
                else:
                    src_pos = src_item.mapToParent(src_item.output_port.center().toPoint())
                if self.dragging_item_uid == dst:
                    dst_pos = self.dragging_item_pos
                else:
                    dst_pos = dst_item.mapToParent(dst_item.input_port.center().toPoint())

                path = QtGui.QPainterPath(src_pos)
                # Draw orthogonal route from src to dst
                self.orthogonalRoute(path, src_pos, dst_pos)
                painter.drawPath(path)

        # temporary connections
        if self.dragging_line:
            _, start, cur = self.dragging_line
            path = QtGui.QPainterPath(start)
            self.orthogonalRoute(path, start, cur)
            painter.drawPath(path)

    def cellAt(self, pos: QtCore.QPoint):
        """Returns the cell (x, y) at the given position or None if out of bounds."""
        x = pos.x() // CELL_SIZE
        y = pos.y() // CELL_SIZE
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return (x, y)
        return None

    def isOccupied(self, cell):
        """Returns true if and only if a GridItem occupies the given cell."""
        return any((gx, gy) == cell for gx, gy, _ in self.items.values())

    def addItem(self, cell, widget: GridItem):
        """Adds the given widget at the given cell (x, y). The cell must be free."""
        gx, gy = cell
        self.items[widget.uid] = (gx, gy, widget)
        widget.setParent(self)
        widget.move(gx * CELL_SIZE + 4, gy * CELL_SIZE + 4)
        widget.show()

    def removeItem(self, uid):
        """Removes the item with the given uid from the grid."""
        if uid in self.items:
            _, _, w = self.items.pop(uid)
            w.setParent(None)
            w.deleteLater()
            self.connections = [(s, d) for s, d in self.connections if s != uid and d != uid]

    # --- Drag & Drop ---
    def dragEnterEvent(self, event):
        """This gets called when something is dragged into the widget, e.g. from the palette."""
        if event.mimeData().hasFormat(MIME_TYPE):
            print("Drag entered with format match")
            event.acceptProposedAction()
        else:
            print("Drag entered ignored")
            event.ignore()

    def dragMoveEvent(self, event):
        """This gets called when something is dragged over the widget."""
        self.useRandomOffset = False
        payload = json.loads(event.mimeData().data(MIME_TYPE).data().decode("utf-8"))
        if payload.get("action") == "move":
            uid = payload.get("id")
            if uid in self.items:
                self.dragging_item_pos = event.position().toPoint()
                self.dragging_item_uid = uid
                self.update()
        event.acceptProposedAction()

    def dropEvent(self, event):
        self.useRandomOffset = True
        payload = json.loads(event.mimeData().data(MIME_TYPE).data().decode("utf-8"))
        pos = event.position().toPoint()
        cell = self.cellAt(pos)
        if not cell:
            event.ignore()
            return

        action = payload.get("action")

        # In case the item is dragged newly from the palette
        if action == "create":
            if self.isOccupied(cell):
                event.ignore()
                return
            item_type = payload.get("type", "Item")
            color = payload.get("color")
            col = QtGui.QColor(color) if color else None
            image_path = payload.get("image_path")
            item = GridItem(item_type, image_path, color=col, parent=self)
            self.addItem(cell, item)
            event.acceptProposedAction()

        # In case the item is moved within the grid
        elif action == "move":
            uid = payload.get("id")
            if uid not in self.items:
                event.ignore()
                return
            old_x, old_y, item = self.items[uid]
            if self.isOccupied(cell) and (old_x, old_y) != cell:
                event.ignore()
                item.show()  # Restore if drop is invalid
                return
            # Remove from old position visually and logically
            item.hide()  # Hide before moving to avoid duplicate
            self.items[uid] = (cell[0], cell[1], item)
            item.move(cell[0] * CELL_SIZE + 4, cell[1] * CELL_SIZE + 4)
            item.show()  # Show at new position
            self.dragging_item_uid = None
            self.dragging_item_pos = None
            self.update()  # Force redraw to clear old position
            print(f"Moved item {uid} to {cell}")
            event.acceptProposedAction()

    # --- Starting a connection ---
    def startConnection(self, item: GridItem, port: str, event: QtGui.QMouseEvent):
        """Starts drawing a connection line between GridItems."""
        if port == "output":
            start = item.mapToParent(item.output_port.center().toPoint())
            self.dragging_line = (item.uid, start, event.position().toPoint())

    def removeConnectionTo(self, item: GridItem):
        """Removes the connection going to the given item's input port (if any)."""
        self.connections = [(s, d) for s, d in self.connections if d != item.uid]
        self.update()

    def mouseMoveEvent(self, event):
        """This is called whenever the mouse moves within the widget. If a line is being dragged, it updates the line."""
        self.useRandomOffset = False
        if self.dragging_line:
            self.dragging_line = (self.dragging_line[0], self.dragging_line[1], event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        """This is called whenever the mouse button is released. If a line is being dragged, it checks if it ends on an input port."""
        self.useRandomOffset = True
        if self.dragging_line:
            src_uid, start, _ = self.dragging_line
            for uid, (_, _, item) in self.items.items():
                local = item.mapFromParent(event.pos())
                # Check if the line ends on an input port of another item and not on itself
                if portAt(item.output_port, item.input_port, local) == "input" and src_uid != uid:
                    self.connections.append((src_uid, uid))
                    break
            self.dragging_line = None
            self.update()

    def orthogonalRoute(self, path: QPainterPath, src: QPointF, dst: QPointF):
        """A helper method to draw an orthogonal route from src to dst.
        Args:
            path (QPainterPath): The QPainterPath to draw into
            src (QPointF): The start point
            dst (QPointF): The end point
        """
        midx = (src.x() + dst.x()) / 2
        midy = (src.y() + dst.y()) / 2

        # Use a random offset to avoid overlapping lines
        if self.useRandomOffset:
            offset = random.randint(20, 50)
        else:
            offset = 20

        # Draw a 6-segment orthogonal line
        path.lineTo(src.x() + offset, src.y())
        path.lineTo(src.x() + offset, midy)
        path.lineTo(midx, midy)
        path.lineTo(dst.x() - offset, midy)
        path.lineTo(dst.x() - offset, dst.y())
        path.lineTo(dst)