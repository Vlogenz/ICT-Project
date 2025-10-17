from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainterPath

from src.control.LogicComponentController import LogicComponentController
from src.constants import GRID_COLS, GRID_ROWS, CELL_SIZE, MIME_TYPE
from src.view.DraggingLine import DraggingLine
from src.view.GridItem import GridItem
from src.view.Connection import Connection
import json
import random
from typing import List

class GridWidget(QtWidgets.QWidget):
    """Main drop area with grid, items and connections."""

    def __init__(self, logicController: LogicComponentController, cols=GRID_COLS, rows=GRID_ROWS, parent=None):
        super().__init__(parent)
        self.logicController = logicController
        self.cols = cols
        self.rows = rows
        self.setAcceptDrops(True)
        self.items: List[GridItem] = []
        self.connections: List[Connection] = []
        self.draggingLine: DraggingLine = None
        #TODO: rework dragging item handling
        self.dragging_item_pos = None
        self.dragging_item_uid = None
        self.draggingItem: GridItem = None
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
        #TODO: rework connections
        pen_conn = QtGui.QPen(QtGui.QColor("black"), 2)
        painter.setPen(pen_conn)
        for connection in self.connections:
            # Currently dragged item position
            if self.draggingItem == connection.srcItem:
                src_pos = self.draggingItem.pos()
            else:
                src_pos = connection.srcItem.getOutputRect(connection.srcKey).center().toPoint()
            if self.draggingItem == connection.dstItem:
                dst_pos = self.draggingItem.pos()
            else:
                dst_pos = connection.dstItem.getInputRect(connection.dstKey).center().toPoint()

            path = QtGui.QPainterPath(src_pos)
            # Draw orthogonal route from src to dst
            self.orthogonalRoute(path, src_pos, dst_pos)
            painter.drawPath(path)

        # temporary connections
        if self.draggingLine:
            start = self.draggingLine.startPos
            cur = self.draggingLine.currentPos
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
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """This gets called when something is dragged over the widget."""
        self.useRandomOffset = False
        payload = json.loads(event.mimeData().data(MIME_TYPE).data().decode("utf-8"))
        if payload.get("action_type") == "move":
            uid = payload.get("id")
            if uid in self.items:
                self.dragging_item_pos = event.position().toPoint()
                self.dragging_item_uid = uid
                self.update()
        event.acceptProposedAction()

    def dropEvent(self, event):
        """This gets called when something is dropped onto the widget. If the cell is occupied, the drop is ignored."""
        self.useRandomOffset = True
        pos = event.position().toPoint()
        cell = self.cellAt(pos)
        if not cell:
            event.ignore()
            return

        if not event.mimeData().hasFormat(MIME_TYPE):
            event.ignore()
            return

        try:
            raw_data = bytes(event.mimeData().data(MIME_TYPE)).decode("utf-8")
            payload = json.loads(raw_data)
        except Exception as e:
            print("Failed to parse MIME data:", e)
            event.ignore()
            return

        action_type = payload.get("action_type")
        class_name = payload.get("class_name")
        package_name = "src.model"

        if action_type == "create":
            # Dynamically import and create a GridItem of this class
            try:
                package = __import__(package_name, fromlist=[class_name])
                print(f"package: {package}")
                module = getattr(package, class_name)
                print(f"module: {module}")
                cls = getattr(module, class_name)
                print(f"Class: {cls}")
                component = cls()
                print(f"Component: {component}")
                new_item = GridItem(logicComponent=component)
                self.addItem(cell, new_item)
                print(f"Created new {class_name}")
            except Exception as e:
                print("Error creating GridItem:", e)
        elif action_type == "move":
            uid = payload.get("id")
            if uid not in self.items:
                event.ignore()
                return
            _, _, item = self.items[uid]
            if self.isOccupied(cell) and self.items[uid][:2] != cell:
                event.ignore()
                item.show()
                return
            self.items[uid] = (cell[0], cell[1], item)
            item.move(cell[0] * CELL_SIZE + 4, cell[1] * CELL_SIZE + 4)
            item.show()
            self.dragging_item_uid = None
            self.dragging_item_pos = None
            self.update()
            event.acceptProposedAction()
        else:
            print("Unknown action type:", action_type)
            event.acceptProposedAction()

    # --- Starting a connection ---
    def startConnection(self, item: GridItem, outputKey: str, event: QtGui.QMouseEvent):
        """Starts drawing a connection line between GridItems."""
        start = item.mapToParent(item.getOutputRect(outputKey).center().toPoint())
        self.draggingLine = DraggingLine(item, start, event.position().toPoint())

    def removeConnectionTo(self, item: GridItem):
        """Removes the connection going to the given item's input port (if any)."""
        self.connections = [(s, d) for s, d in self.connections if d != item.uid]
        self.update()

    def mouseMoveEvent(self, event):
        """This is called whenever the mouse moves within the widget. If a line is being dragged, it updates the line."""
        self.useRandomOffset = False
        if self.draggingLine:
            self.draggingLine.currentPos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """This is called whenever the mouse button is released. If a line is being dragged, it checks if it ends on an input port."""
        self.useRandomOffset = True
        if self.draggingLine:
            srcItem =  self.draggingLine.srcItem
            start = self.draggingLine.startPos
            for uid, (_, _, item) in self.items.items():
                local = item.mapFromParent(event.pos())
                # Check if the line ends on an input port of another item and not on itself
                if item.portAt(local)[0] == "input" and srcItem.uid != uid:
                    # Add the connection
                    outputKey = srcItem.portAt(srcItem.mapFromParent(start))[1]
                    inputKey = item.portAt(local)[1]
                    self.logicController.addConnection(self.draggingLine.srcItem.logicComponent, outputKey, item.logicComponent, inputKey)
                    self.connections.append((srcItem.uid, uid))
                    break
            self.draggingLine = None
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
            offset = random.randint(20,50)
        else:
            offset = 20

        # Draw a 6-segment orthogonal line
        path.lineTo(src.x() + offset, src.y())
        path.lineTo(src.x() + offset, midy)
        path.lineTo(midx, midy)
        path.lineTo(dst.x() - offset, midy)
        path.lineTo(dst.x() - offset, dst.y())
        path.lineTo(dst)