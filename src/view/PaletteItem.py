import json
from symtable import Class

from PySide6 import QtWidgets, QtGui, QtCore
from src.constants import MIME_TYPE, CELL_SIZE


class PaletteItem(QtWidgets.QFrame):
    """Drag-Source in the palette on the side."""

    def __init__(self, logicComponentClass: Class, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFixedSize(CELL_SIZE - 8, CELL_SIZE - 8)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_path = f"assets/gates/{logicComponentClass.__name__}.svg"

        img_label = QtWidgets.QLabel()
        img_label.setScaledContents(True)
        pixmap = QtGui.QPixmap(self.image_path)
        if not pixmap.isNull():
            img_label.setPixmap(pixmap)
        else:
            img_label.setText(logicComponentClass.__name__)

        img_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(img_label)

        self.logicComponentClass = logicComponentClass

        # Apply stylesheet
        self.setStyleSheet(
            f"border: 1px solid lightgray; background-color: lightgray;")

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
            drag.setHotSpot(event.position().toPoint())

            drag.exec(QtCore.Qt.CopyAction)
