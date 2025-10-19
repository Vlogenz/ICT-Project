from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainterPath

from src.control.LogicComponentController import LogicComponentController
from src.constants import GRID_COLS, GRID_ROWS, CELL_SIZE, MIME_TYPE
from src.model.Input import Input
from src.model.Output import Output
from src.view.DraggingLine import DraggingLine
from src.view.GridItem import GridItem
from src.view.Connection import Connection
import json
import random
from typing import List, Tuple

from src.view.InputGridItem import InputGridItem
from src.view.OutputGridItem import OutputGridItem


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
                print("Update line to start from dragging item")
                src_pos = self.draggingItem.pos()
            else:
                print(f"src key: {connection.srcKey}")
                item = connection.srcItem
                src_pos = item.mapToParent(item.getOutputRect(connection.srcKey).center().toPoint())
            if self.draggingItem == connection.dstItem:
                dst_pos = self.draggingItem.pos()
            else:
                item = connection.dstItem
                dst_pos = item.mapToParent(item.getInputRect(connection.dstKey).center().toPoint())

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
        return any(self.cellAt(item.pos()) == cell for item in self.items)

    def addItem(self, cell, item: GridItem):
        """
        Also adds the item at the given cell (x, y). The cell must be free."""
        gx, gy = cell
        self.items.append(item)
        item.setParent(self)
        item.move(gx * CELL_SIZE + 4, gy * CELL_SIZE + 4)
        item.show()

    def removeItem(self, item: GridItem):
        """Removes the give item from the backend and from the grid."""
        try:
            index = self.items.index(item)
            print("Item found")
            self.logicController.removeLogicComponent(item.logicComponent)
            deleteItem = self.items.pop(index)
            deleteItem.setParent(None)
            deleteItem.deleteLater()
            self.connections = [conn for conn in self.connections if conn.srcItem != deleteItem and conn.dstItem != deleteItem]
        except ValueError:
            print("Item not found")

    def removeItemByUID(self, uid):
        filteredItems = [item for item in self.items]
        if len(filteredItems) == 1:
            self.removeItem(filteredItems[0])

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
        print(f"move event")
        payload = json.loads(event.mimeData().data(MIME_TYPE).data().decode("utf-8"))
        if payload.get("action_type") == "move":
            if self.draggingItem is None:
                uid = payload.get("id")
                filteredItems = [item for item in self.items if item.uid == uid]
                if len(filteredItems)!=0:
                    self.draggingItem = filteredItems[0]
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
                component = self.logicController.addLogicComponent(cls)
                print(f"Component: {component}")
                if isinstance(component, Input):
                    new_item = InputGridItem(logicComponent=component)
                elif isinstance(component, Output):
                    new_item = OutputGridItem(logicComponent=component)
                else:
                    new_item = GridItem(logicComponent=component)
                self.addItem(cell, new_item)
                print(f"Created new {class_name}")
            except Exception as e:
                print("Error creating GridItem:", e)
        elif action_type == "move":
            uid = payload.get("id")
            if not any(item.uid == uid for item in self.items):
                event.ignore()
                return
            item = [item for item in self.items if item.uid == uid][0]
            if self.isOccupied(cell) and self.cellAt(item.pos()) != cell:
                event.ignore()
                item.show()
                return
            item.move(cell[0] * CELL_SIZE + 4, cell[1] * CELL_SIZE + 4)
            item.show()
            self.draggingItem = None
            self.update()
            event.acceptProposedAction()
        else:
            print("Unknown action type:", action_type)
            event.acceptProposedAction()

    # --- Starting a connection ---
    def startConnection(self, item: GridItem, outputKey: str, event: QtGui.QMouseEvent):
        """Starts drawing a connection line between GridItems."""
        start = item.mapToParent(item.getOutputRect(outputKey).center().toPoint())
        self.draggingLine = DraggingLine(item, outputKey, start, event.position().toPoint())

    def removeConnectionTo(self, dstItem: GridItem, dstKey: str):
        """Removes the connection going to the given item's input port (if any)."""
        connectionsToDelete = [conn for conn in self.connections if conn.dstItem == dstItem and conn.dstKey == dstKey]
        for conn in connectionsToDelete:
            self.logicController.removeConnection(conn.srcItem.logicComponent, conn.srcKey, conn.dstItem.logicComponent, conn.dstKey)
        self.connections = list(set(self.connections) - set(connectionsToDelete))
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
            srcKey = self.draggingLine.srcKey
            start = self.draggingLine.startPos
            for item in self.items:
                local = item.mapFromParent(event.pos())
                port = item.portAt(local)
                # Check if the line ends on an input port of another item and not on itself
                if port[0] == "input" and srcItem.uid != item.uid:
                    # Add the connection
                    outputKey = srcItem.portAt(srcItem.mapFromParent(start))[1]
                    inputKey = item.portAt(local)[1]
                    self.logicController.addConnection(self.draggingLine.srcItem.logicComponent, outputKey, item.logicComponent, inputKey)
                    self.connections.append(Connection(srcItem, srcKey, item, port[1]))
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