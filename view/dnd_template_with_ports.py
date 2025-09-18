# dnd_template_with_ports.py
"""
Drag & Drop Vorlage mit PySide6 + Ports & Verbindungen

Features:
- Links: Palette mit 2 Items
- Mitte: Grid (Raster) als Drop-Ziel
- GridItems können erstellt, verschoben, gelöscht werden
- Jedes Item hat Input- und Output-Port
- Verbindung: Output -> Input durch Klicken+Ziehen einer Linie
"""

import sys
import json
import uuid
from PySide6 import QtCore, QtGui, QtWidgets

# Konstanten
CELL_SIZE = 100
GRID_COLS = 6
GRID_ROWS = 4
MIME_TYPE = "application/x-qt-grid-item"


class PaletteItem(QtWidgets.QFrame):
    """Drag-Quelle in der Palette."""

    def __init__(self, label: str, color: QtGui.QColor = None, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFixedSize(70, 40)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        lbl = QtWidgets.QLabel(label)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(lbl)

        self.label = label
        self.color = color
        if color:
            pal = self.palette()
            pal.setColor(self.backgroundRole(), color)
            self.setAutoFillBackground(True)
            self.setPalette(pal)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            payload = {"action": "create", "type": self.label}
            if self.color:
                payload["color"] = self.color.name()
            mime.setData(MIME_TYPE, json.dumps(payload).encode("utf-8"))
            drag.setMimeData(mime)

            pix = QtGui.QPixmap(self.size())
            self.render(pix)
            drag.setPixmap(pix)

            drag.exec(QtCore.Qt.CopyAction)


class GridItem(QtWidgets.QFrame):
    """Ein Element im Grid. Mit Input/Output-Port."""

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

        # Ports definieren (größere Klickbereiche)
        self.output_port = QtCore.QRectF(self.width() - 16, self.height() / 2 - 8, 16, 16)
        self.input_port = QtCore.QRectF(0, self.height() / 2 - 8, 16, 16)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        # Output-Port rechts (blau)
        painter.setBrush(QtGui.QColor("blue"))
        painter.drawEllipse(self.output_port)
        # Input-Port links (grün)
        painter.setBrush(QtGui.QColor("green"))
        painter.drawEllipse(self.input_port)

    def port_at(self, pos: QtCore.QPoint):
        """Prüfen, ob pos in einem Port liegt"""
        if self.output_port.contains(pos):
            return "output"
        if self.input_port.contains(pos):
            return "input"
        return None

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        local_pos = event.position().toPoint()
        port = self.port_at(local_pos)
        if port == "output":
            # Verbindung starten -> an Grid weiterreichen
            self.parentWidget().start_connection(self, "output", event)
            return
        elif port == "input":
            # Input-Port wird nicht direkt gedraggd
            return

        # normaler Move-Drag
        if event.button() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            payload = {"action": "move", "id": self.uid}
            mime.setData(MIME_TYPE, json.dumps(payload).encode("utf-8"))
            drag.setMimeData(mime)

            pix = QtGui.QPixmap(self.size())
            self.render(pix)
            drag.setPixmap(pix)

            self.hide()
            result = drag.exec(QtCore.Qt.MoveAction)
            if result == QtCore.Qt.IgnoreAction:
                self.show()

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        if isinstance(self.parent(), GridWidget):
            self.parent().remove_item(self.uid)


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
        self.setMinimumSize(cols * CELL_SIZE, rows * CELL_SIZE)

    def paintEvent(self, event):
        # Grid
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(200, 200, 200))
        painter.setPen(pen)
        for c in range(self.cols + 1):
            x = c * CELL_SIZE
            painter.drawLine(x, 0, x, self.rows * CELL_SIZE)
        for r in range(self.rows + 1):
            y = r * CELL_SIZE
            painter.drawLine(0, y, self.cols * CELL_SIZE, y)

        # feste Verbindungen zeichnen
        pen_conn = QtGui.QPen(QtGui.QColor("black"), 2)
        painter.setPen(pen_conn)
        for src, dst in self.connections:
            if src in self.items and dst in self.items:
                _, _, src_item = self.items[src]
                _, _, dst_item = self.items[dst]
                p1 = src_item.mapToParent(src_item.output_port.center().toPoint())
                p2 = dst_item.mapToParent(dst_item.input_port.center().toPoint())
                path = QtGui.QPainterPath(p1)
                midx = (p1.x() + p2.x()) / 2
                path.cubicTo(midx, p1.y(), midx, p2.y(), p2.x(), p2.y())
                painter.drawPath(path)

        # temporäre Verbindung
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
            event.acceptProposedAction()

    # --- Verbindung starten ---
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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag & Drop mit Ports")

        central = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central)
        self.setCentralWidget(central)

        # Palette
        palette = QtWidgets.QVBoxLayout()
        palette.addWidget(PaletteItem("Label"))
        palette.addWidget(PaletteItem("Rotes Feld", QtGui.QColor("#ff9999")))
        palette.addStretch()

        palette_frame = QtWidgets.QFrame()
        palette_frame.setLayout(palette)
        palette_frame.setFixedWidth(120)

        # Grid
        grid = GridWidget()

        layout.addWidget(palette_frame)
        layout.addWidget(grid, 1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
