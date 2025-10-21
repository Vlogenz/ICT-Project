import json
from symtable import Class

from PySide6 import QtWidgets, QtGui, QtCore
from src.constants import MIME_TYPE


class PaletteItem(QtWidgets.QFrame):
    """Drag-Source in the palette on the side."""

    def __init__(self, logicComponentClass: Class, color: QtGui.QColor = None, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFixedSize(90, 40)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        self.image_path = f"Gates/{logicComponentClass.__name__}.png"

        img_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(self.image_path)
        if not pixmap.isNull():
            img_label.setPixmap(
                pixmap.scaled(28, 28, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            )
            img_label.setAlignment(QtCore.Qt.AlignCenter)
        else:
            img_label.setText(logicComponentClass.__name__)

        img_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(img_label)

        self.logicComponentClass = logicComponentClass
        self.color = color

        # Apply stylesheet
        self.setStyleSheet(
            f"border: 1px solid lightgray; background-color: {color.name() if color != None else 'lightgray'};")

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """This gets called when the user starts dragging the item."""

        if event.button() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime_data = QtCore.QMimeData()
            payload = {
                "action_type": "create",  # or "move"
                "class_name": f"{self.logicComponentClass.__name__}",
            }
            mime_data.setData(MIME_TYPE, QtCore.QByteArray(json.dumps(payload).encode("utf-8")))
            drag.setMimeData(mime_data)

            pix = QtGui.QPixmap(self.size())
            self.render(pix)
            drag.setPixmap(pix)

            drag.exec(QtCore.Qt.CopyAction)
