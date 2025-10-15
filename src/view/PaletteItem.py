import sys
import json
from PySide6 import QtWidgets, QtGui, QtCore
from constants import MIME_TYPE

class PaletteItem(QtWidgets.QFrame):
    """Drag-Source in the palette on the side."""

    def __init__(self, label: str, image_path: str = None, color: QtGui.QColor = None, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFixedSize(90, 40)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        self.image_path = image_path

        if self.image_path:  # Show gate image if provided
            img_label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(image_path)
            img_label.setPixmap(
                pixmap.scaled(28, 28, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            )
            img_label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(img_label)

        lbl = QtWidgets.QLabel(label)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(lbl)

        self.label = label
        self.color = color

        # Apply stylesheet
        self.setStyleSheet(
            f"border: 1px solid lightgray; background-color: {color.name() if color != None else 'lightgray'};")

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """This gets called when the user starts dragging the item."""

        if event.button() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            payload = {"action": "create", "type": self.label, "image_path": self.image_path}
            if self.color:
                payload["color"] = self.color.name()
            mime.setData(MIME_TYPE, json.dumps(payload).encode("utf-8"))
            drag.setMimeData(mime)

            pix = QtGui.QPixmap(self.size())
            self.render(pix)
            drag.setPixmap(pix)

            drag.exec(QtCore.Qt.CopyAction)
