import json
from symtable import Class

from PySide6 import QtWidgets, QtGui, QtCore
import pickle
from constants import MIME_TYPE
from src.model.LogicComponent import LogicComponent


class PaletteItem(QtWidgets.QFrame):
    """Drag-Source in the palette on the side."""

    def __init__(self, logicComponentClass: Class, color: QtGui.QColor = None, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFixedSize(70, 40)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        lbl = QtWidgets.QLabel(logicComponentClass.__name__)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(lbl)

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

