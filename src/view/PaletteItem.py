import json
from symtable import Class

from PySide6 import QtWidgets, QtGui, QtCore
from src.constants import MIME_TYPE, CELL_SIZE, PR_TEXT_COLOR
from src.view.util.ImageLoader import ImageLoader


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
        pixmap = self.getImage()
        if not pixmap.isNull():
            self.imgLabel.setPixmap(pixmap)
        else:
            self.imgLabel.setText(self.componentName)

        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)

    def getImage(self) -> QtGui.QPixmap:
        imagePath = f"assets/gates/{self.componentName}.svg"
        return ImageLoader.svg_to_pixmap(imagePath, QtGui.QColor(*PR_TEXT_COLOR))

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
