from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPainterPath, QPainterPathStroker

from src.control.LogicComponentController import LogicComponentController
from src.constants import GRID_COLS, GRID_ROWS, CELL_SIZE, MIME_TYPE
from src.model import ALUAdvanced, ALUSimple
from src.model.Input import Input
from src.model.LogicComponent import LogicComponent
from src.infrastructure.eventBus import getBus
from src.view.ALUGridItem import ALUGridItem
from src.view.DraggingLine import DraggingLine
from src.view.GridItem import GridItem
from src.view.Connection import Connection
import json
from typing import List, Tuple

from src.view.InputGridItem import InputGridItem

class GridWidget(QtWidgets.QWidget):
    """Main drop area with grid, items and connections."""

    def __init__(self, logicController: LogicComponentController, cols=GRID_COLS, rows=GRID_ROWS, parent=None):
        super().__init__(parent)
        self.logicController = logicController
        self.cols = cols
        self.rows = rows
        self.scale_factor = 1.0  # Initial scale
        self.setAcceptDrops(True)
        self.items: List[GridItem] = []
        self.connections: List[Connection] = []
        self.draggingLine: DraggingLine = None
        self.draggingItem: GridItem = None
        self.tempPos = None
        #self.setMinimumSize(int(cols * CELL_SIZE * self.scale_factor), int(rows * CELL_SIZE * self.scale_factor))

        #Initialize event bus
        self.eventBus = getBus()
        self.eventBus.subscribe("view:components_updated", self.updateConnectionActivity)
        self.eventBus.subscribe("view:components_cleared", self.visuallyRemoveAllItems)
        self.eventBus.subscribe("view:rebuild_circuit", self.rebuildCircuit)

    def paintEvent(self, event):
        """Redraws the entire grid, items and connections. It overrides QWidget.paintEvent, which gets called automatically when update() is called."""
        painter = QtGui.QPainter(self)

        # Grid
        pen = QtGui.QPen(QtGui.QColor(200, 200, 200))
        painter.setPen(pen)
        for c in range(self.cols + 1):
            x = c * CELL_SIZE * self.scale_factor
            painter.drawLine(x, 0, x, self.rows * CELL_SIZE * self.scale_factor)
        for r in range(self.rows + 1):
            y = r * CELL_SIZE * self.scale_factor
            painter.drawLine(0, y, self.cols * CELL_SIZE * self.scale_factor, y)

        # painting connections
        black_pen = QtGui.QPen(QtGui.QColor("black"), 2)
        red_pen = QtGui.QPen(QtGui.QColor("red"), 2)
        painter.setPen(black_pen)
        for i,connection in enumerate(self.connections):
            # Currently dragged item position
            if self.draggingItem == connection.srcItem and self.tempPos:
                item = self.draggingItem
                rect_center = item.getOutputRect(connection.srcKey).center()
                src_pos = QtCore.QPoint(self.tempPos[0] + rect_center.x(), self.tempPos[1] + rect_center.y())
            else:
                item = connection.srcItem
                src_pos = item.mapToParent(item.getOutputRect(connection.srcKey).center().toPoint())
            if self.draggingItem == connection.dstItem and self.tempPos:
                item = self.draggingItem
                rect_center = item.getInputRect(connection.dstKey).center()
                dst_pos = QtCore.QPoint(self.tempPos[0] + rect_center.x(), self.tempPos[1] + rect_center.y())
            else:
                item = connection.dstItem
                dst_pos = item.mapToParent(item.getInputRect(connection.dstKey).center().toPoint())

            path = QtGui.QPainterPath(src_pos)
            # Draw orthogonal route from src to dst
            self.intelligentOrthogonalRoute(path, src_pos, dst_pos, self.connections[:i])
            connection.setPath(path)
            if connection.isActive:
                painter.setPen(red_pen)
            else:
                painter.setPen(black_pen)
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
        x = (pos.x() / self.scale_factor) // CELL_SIZE
        y = (pos.y() / self.scale_factor) // CELL_SIZE
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return (int(x), int(y))
        return None

    def isOccupied(self, cell):
        """Returns true if and only if a GridItem occupies the given cell."""
        return any(self.cellAt(item.pos()) == cell for item in self.items)

    def addItem(self, cell, item: GridItem):
        """
        Also adds the item at the given cell (x, y). The cell must be free."""
        if not self.isOccupied(cell):
            gx, gy = cell
            self.items.append(item)
            item.setParent(self)
            item.move(gx * CELL_SIZE + 4, gy * CELL_SIZE + 4)
            item.cell_x = gx
            item.cell_y = gy
            item.show()

    def addComponent(self, cell, component: LogicComponent, immovable=False):
        if isinstance(component, Input):
            new_item = InputGridItem(logicComponent=component, immovable=immovable)
        elif isinstance(component, ALUSimple) or isinstance(component, ALUAdvanced):
            new_item = ALUGridItem(logicComponent=component, immovable=immovable)
        else:
            new_item = GridItem(logicComponent=component, immovable=immovable)
        self.addItem(cell, new_item)

    def _visuallyAddConnection(self, srcComp: LogicComponent, srcKey: str, dstComp: LogicComponent, dstKey: str):
        """Adds a Connection object to the list of connections and updates the grid."""
        srcItem = [item for item in self.items if item.logicComponent == srcComp][0]
        dstItem = [item for item in self.items if item.logicComponent == dstComp][0]
        self.connections.append(Connection(srcItem, srcKey, dstItem, dstKey))
        dstItem.update()
        self.update()

    def removeItem(self, item: GridItem):
        """Removes the give item from the backend and from the grid."""
        try:
            index = self.items.index(item)
            self.logicController.removeLogicComponent(item.logicComponent)
            deleteItem = self.items.pop(index)
            deleteItem.unsubscribe()
            deleteItem.setParent(None)
            deleteItem.deleteLater()
            self.connections = [conn for conn in self.connections if conn.srcItem != deleteItem and conn.dstItem != deleteItem]
            self.update()
        except ValueError:
            return

    def visuallyRemoveAllItems(self):
        """Just removes all GridItems and Connections from the grid, not the underlying logic components.
        Only call this method when the backend already removed stuff (i.e. cleared components).
        """
        for item in self.items:
            item.unsubscribe()
            item.setParent(None)
            item.deleteLater()
        self.items.clear()
        self.connections.clear()
        self.update()

    def removeItemByUID(self, uid):
        filteredItems = [item for item in self.items if item.uid == uid]
        if len(filteredItems) == 1:
            self.removeItem(filteredItems[0])

    def rebuildCircuit(self, componentInfo: List[Tuple[int,int,bool]]):
        """Rebuilds all visual elements for the circuit:
        - A GridItem for each component that is currently in the logicController
        - A connection for each of the logic component's connections
        """
        self.visuallyRemoveAllItems()
        for i,comp in enumerate(self.logicController.components):
            self.addComponent((componentInfo[i][0], componentInfo[i][1]), comp, immovable=componentInfo[i][2])
        for item in self.items:
            for dstComp, dstKey in item.logicComponent.outputs:
                srcKey = dstComp.inputs[dstKey][1]
                self._visuallyAddConnection(item.logicComponent, srcKey, dstComp, dstKey)

    # --- Drag & Drop ---
    def dragEnterEvent(self, event):
        """This gets called when something is dragged into the widget, e.g. from the palette."""
        if event.mimeData().hasFormat(MIME_TYPE):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """This gets called when something is dragged over the widget."""
        payload = json.loads(event.mimeData().data(MIME_TYPE).data().decode("utf-8"))
        if payload.get("action_type") == "move":
            if self.draggingItem is None:
                uid = payload.get("id")
                filteredItems = [item for item in self.items if item.uid == uid]
                if len(filteredItems)!=0:
                    self.draggingItem = filteredItems[0]
            cell = self.cellAt(event.position().toPoint())
            if cell:
                self.tempPos = ((cell[0] * CELL_SIZE + 4) * self.scale_factor, (cell[1] * CELL_SIZE + 4) * self.scale_factor)
            self.update()
        event.acceptProposedAction()

    def dropEvent(self, event):
        """This gets called when something is dropped onto the widget. If the cell is occupied, the drop is ignored."""
        payload = json.loads(event.mimeData().data(MIME_TYPE).data().decode("utf-8"))
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
                module = getattr(package, class_name)
                cls = module
                component = self.logicController.addLogicComponent(cls)
                self.addComponent(cell, component)
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
            item.move((cell[0] * CELL_SIZE + 4) * self.scale_factor, (cell[1] * CELL_SIZE + 4) * self.scale_factor)
            item.cell_x = cell[0]
            item.cell_y = cell[1]
            item.show()
            self.draggingItem = None
            self.tempPos = None
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
        if self.draggingLine:
            self.draggingLine.currentPos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        """This is called whenever the mouse button is released. If a line is being dragged, it checks if it ends on an input port."""
        if self.draggingLine:
            srcItem =  self.draggingLine.srcItem
            srcKey = self.draggingLine.srcKey
            start = self.draggingLine.startPos

            for item in self.items:
                local = item.mapFromParent(event.position())
                port = item.portAt(local)

                # Check if the line ends on an input port of another item and not on itself
                if port[0] == "input" and srcItem.uid != item.uid:

                    # Add the connection
                    outputKey = srcItem.portAt(srcItem.mapFromParent(start))[1]
                    inputKey = item.portAt(local)[1]

                    if self.logicController.addConnection(self.draggingLine.srcItem.logicComponent, outputKey, item.logicComponent, inputKey):
                        self.connections.append(Connection(srcItem, srcKey, item, port[1]))
                        item.update()
                    else:
                        self.showErrorToast("You cannot add this connection here!",
                                       "Either the bitwidth is incompatible or the input is already occupied.")
                    break

            self.draggingLine = None
            self.update()

    def orthogonalRoute(self, path: QPainterPath, src: QPoint, dst: QPoint):
        """A helper method to draw an orthogonal route from src to dst.
        Args:
            path (QPainterPath): The QPainterPath to draw into
            src (QPoint): The start point
            dst (QPoint): The end point
        """
        startOffset = 20 * self.scale_factor

        if dst.x() < src.x():
            # Draw a 5-segment orthogonal line
            midy = (src.y() + dst.y()) / 2
            path.lineTo(src.x() + startOffset, src.y())
            path.lineTo(src.x() + startOffset, midy)
            path.lineTo(dst.x() - startOffset, midy)
            path.lineTo(dst.x() - startOffset, dst.y())
            path.lineTo(dst)
        else:
            # Draw a 3-segment orthogonal line
            path.lineTo(src.x() + startOffset, src.y())
            path.lineTo(src.x() + startOffset, dst.y())
            path.lineTo(dst)

    # TODO: Perspectively restructure this (and regular orthogonalRoute) to the connection class for better modularity. Low priority though.
    def intelligentOrthogonalRoute(self, pathToCreate: QPainterPath, src: QPoint, dst: QPoint,
                                   connectionsToAvoid: List[Connection]):
        connectionPaths = [conn.getPath() for conn in connectionsToAvoid]

        def wouldCauseOverlap(x,y) -> bool:
            # Check if the given point lies on one of the connectionsToAvoid
            point = QPoint(x,y)
            causesOverlap = False
            i = 0
            stroker = QPainterPathStroker()
            stroker.setWidth(2)
            while not causesOverlap and i < len(connectionPaths):
                stroked_path = stroker.createStroke(connectionPaths[i])
                if stroked_path.contains(point):
                    causesOverlap = True
                i += 1
            return causesOverlap

        startOffset = 20 * self.scale_factor
        overlapOffset = 10 * self.scale_factor

        if dst.x() < src.x():
            # Draw a 5-segment orthogonal line if dst is left of src
            midy = (src.y() + dst.y()) / 2
            pointA = [src.x() + startOffset, src.y()]
            while wouldCauseOverlap(pointA[0], pointA[1]):
                pointA[0] += overlapOffset
            pointB = [pointA[0], midy]
            while wouldCauseOverlap(pointB[0], pointB[1]):
                pointA[0] += overlapOffset
                pointB[0] += overlapOffset
                pointB[1] += overlapOffset
            pointC = [dst.x() - startOffset, pointB[1]]
            while wouldCauseOverlap(pointC[0], pointC[1]):
                pointC[0] -= overlapOffset
            pointD = [pointC[0], dst.y()]
            while wouldCauseOverlap(pointD[0], pointD[1]):
                pointC[0] -= overlapOffset
                pointD[0] -= overlapOffset
            pointE = dst
            pointsToDraw = [pointA, pointB, pointC, pointD, pointE]
        else:
            # Draw a 3-segment orthogonal line otherwise
            pointA = [src.x() + startOffset, src.y()]
            while wouldCauseOverlap(pointA[0], pointA[1]):
                pointA[0] += overlapOffset
            pointB = [pointA[0], dst.y()]
            while wouldCauseOverlap(pointB[0], pointB[1]):
                pointA[0] += overlapOffset
                pointB[0] += overlapOffset
            pointC = dst
            pointsToDraw = [pointA, pointB, pointC]

        # Add all the points to the pathToCreate
        for point in pointsToDraw:
            if isinstance(point, list):
                pathToCreate.lineTo(QPoint(point[0], point[1]))
            else:
                pathToCreate.lineTo(point)

    def updateConnectionActivity(self, components: List[LogicComponent]):
        """Updates the isActive attribute of all the connections on the grid.
        A connection becomes active if and only if the logicComponent of its srcItem is among the given list.

        Args:
            components (List[LogicComponent]): The list of logic components that were updated and whose outgoing connections should become active.
        """

        for conn in self.connections:
            if conn.srcItem.logicComponent in components:
                conn.isActive = True
            else:
                conn.isActive = False

        self.update()

    def showErrorToast(self, title: str, text: str):
        """Shows an error message box with the given title and text

        Args:
            title (str): The title for the message box
            text (str): The text for the message box
        """
        QtWidgets.QMessageBox.critical(self, title, text)

    def unsubscribe(self):
        """Unsubscribes the GridWidget from all subscriptions. This does not include the ones of the GridItems."""
        self.eventBus.unsubscribe("view:components_updated", self.updateConnectionActivity)
        self.eventBus.unsubscribe("view:components_cleared", self.visuallyRemoveAllItems)
        self.eventBus.unsubscribe("view:rebuild_circuit", self.rebuildCircuit)

    def wheelEvent(self, event):
        """Handle mouse wheel for zooming."""
        if event.modifiers() & QtCore.Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.scale_factor *= 1.1  # Zoom in
            else:
                self.scale_factor /= 1.1  # Zoom out
            self.scale_factor = max(0.1, min(5.0, self.scale_factor))  # Clamp scale
            self.setMinimumSize(int(self.cols * CELL_SIZE * self.scale_factor), int(self.rows * CELL_SIZE * self.scale_factor))
            for item in self.items:
                item.scale_factor = self.scale_factor
                item.setFixedSize(int((CELL_SIZE - 8) * self.scale_factor), int((CELL_SIZE - 8) * self.scale_factor))
                item.move(int((item.cell_x * CELL_SIZE + 4) * self.scale_factor), int((item.cell_y * CELL_SIZE + 4) * self.scale_factor))
                item.updateRects()
            self.update()
            event.accept()
        else:
            super().wheelEvent(event)
