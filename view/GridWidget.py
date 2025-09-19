from PySide6 import QtCore, QtGui, QtWidgets

from constants import GRID_COLS, GRID_ROWS, CELL_SIZE, MIME_TYPE
from view.GridItem import GridItem
import json


class GridWidget(QtWidgets.QWidget):
    """Zentrale Drop-Fläche mit Ports und Verbindungen."""

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

    def paintEvent(self, event):
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
                midx = (src_pos.x() + dst_pos.x()) / 2
                path.cubicTo(midx, src_pos.y(), midx, dst_pos.y(), dst_pos.x(), dst_pos.y())
                painter.drawPath(path)

        # temporary connections
        if self.dragging_line:
            _, start, cur = self.dragging_line
            path = QtGui.QPainterPath(start)
            midx = (start.x() + cur.x()) / 2
            path.cubicTo(midx, start.y(), midx, cur.y(), cur.x(), cur.y())
            painter.drawPath(path)

    def cell_at(self, pos: QtCore.QPoint):
        x = pos.x() // CELL_SIZE
        y = pos.y() // CELL_SIZE
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return (x, y)
        return None

    def is_occupied(self, cell):
        return any((gx, gy) == cell for gx, gy, _ in self.items.values())

    def add_item(self, cell, widget: GridItem):
        gx, gy = cell
        self.items[widget.uid] = (gx, gy, widget)
        widget.setParent(self)
        widget.move(gx * CELL_SIZE + 4, gy * CELL_SIZE + 4)
        widget.show()

    def remove_item(self, uid):
        if uid in self.items:
            _, _, w = self.items.pop(uid)
            w.setParent(None)
            w.deleteLater()
            self.connections = [(s, d) for s, d in self.connections if s != uid and d != uid]

    # --- Drag & Drop ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(MIME_TYPE):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        payload = json.loads(event.mimeData().data(MIME_TYPE).data().decode("utf-8"))
        if payload.get("action") == "move":
            uid = payload.get("id")
            if uid in self.items:
                self.dragging_item_pos = event.position().toPoint()
                self.dragging_item_uid = uid
                self.update()
        event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.position().toPoint()
        cell = self.cell_at(pos)
        if not cell:
            event.ignore()
            return

        payload = json.loads(event.mimeData().data(MIME_TYPE).data().decode("utf-8"))
        action = payload.get("action")

        if action == "create":
            if self.is_occupied(cell):
                event.ignore()
                return
            typ = payload.get("type", "Item")
            color = payload.get("color")
            col = QtGui.QColor(color) if color else None
            item = GridItem(typ, color=col, parent=self)
            self.add_item(cell, item)
            event.acceptProposedAction()

        elif action == "move":
            uid = payload.get("id")
            if uid not in self.items:
                event.ignore()
                return
            _, _, item = self.items[uid]
            if self.is_occupied(cell) and self.items[uid][:2] != cell:
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

    # --- Starting a connection ---
    def start_connection(self, item: GridItem, port: str, event: QtGui.QMouseEvent):
        if port == "output":
            start = item.mapToParent(item.output_port.center().toPoint())
            self.dragging_line = (item.uid, start, event.position().toPoint())
            self.grabMouse()

    def mouseMoveEvent(self, event):
        if self.dragging_line:
            self.dragging_line = (self.dragging_line[0], self.dragging_line[1], event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if self.dragging_line:
            src_uid, start, _ = self.dragging_line
            for uid, (_, _, item) in self.items.items():
                local = item.mapFromParent(event.pos())
                if item.port_at(local) == "input":
                    self.connections.append((src_uid, uid))
                    break
            self.dragging_line = None
            self.releaseMouse()
            self.update()

