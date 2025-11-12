import json
from symtable import Class

from PySide6 import QtWidgets, QtGui, QtCore
from src.constants import MIME_TYPE, CELL_SIZE


class PaletteItem(QtWidgets.QFrame):
    """Drag-Source in the palette on the side."""

    def __init__(self, componentName: str, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFixedSize(CELL_SIZE - 8, CELL_SIZE - 8)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.componentName = componentName

        # Initialize image label
        self.imgLabel = QtWidgets.QLabel()
        self.imgLabel.setScaledContents(True)
        layout.addWidget(self.imgLabel)
        imagePath = self.getImagePath()
        pixmap = QtGui.QPixmap(imagePath)
        if not pixmap.isNull():
            self.imgLabel.setPixmap(pixmap)
        else:
            self.imgLabel.setText(self.componentName)
            self.imgLabel.setStyleSheet("color: black;")

        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Apply stylesheet
        self.setStyleSheet(
            f"border: 1px solid lightgray; background-color: lightgray;")

    def getImagePath(self) -> str:
        return f"assets/gates/{self.componentName}.svg"

    def getPayload(self):
        return {
                "action_type": "create",  # or "move"
                "componentName": f"{self.componentName}",
                "isCustom": False
            }

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """This gets called when the user starts dragging the item."""

        if event.button() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime_data = QtCore.QMimeData()
            payload = self.getPayload()
            mime_data.setData(MIME_TYPE, QtCore.QByteArray(json.dumps(payload).encode("utf-8")))
            drag.setMimeData(mime_data)

            pix = QtGui.QPixmap(self.size())
            self.render(pix)
            drag.setPixmap(pix)
            drag.setHotSpot(event.position().toPoint())

            drag.exec(QtCore.Qt.CopyAction)
