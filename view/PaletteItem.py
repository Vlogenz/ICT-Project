import json
from PySide6 import QtWidgets, QtGui, QtCore
from constants import MIME_TYPE


class PaletteItem(QtWidgets.QFrame):
    """Drag-Source in the palette on the side."""

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

