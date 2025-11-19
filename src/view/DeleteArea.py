from PySide6 import QtWidgets, QtCore, QtGui
import json
from src.constants import MIME_TYPE

class DeleteArea(QtWidgets.QFrame):
    """A drop target area to delete items."""

    def __init__(self, gridWidget, parent=None):
        super().__init__(parent)
        self.gridWidget = gridWidget
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setStyleSheet("background-color: lightcoral; border: 2px dashed red;")
        self.setAcceptDrops(True)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        label = QtWidgets.QLabel("Delete")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        """Handle drag enter events."""
        if event.mimeData().hasFormat(MIME_TYPE):
            data = json.loads(event.mimeData().data(MIME_TYPE).data().decode("utf-8"))
            if data.get("action_type") == "move":
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent):
        """Handle drop events to delete items."""
        if event.mimeData().hasFormat(MIME_TYPE):
            data = json.loads(event.mimeData().data(MIME_TYPE).data().decode("utf-8"))
            if data.get("action_type") == "move":
                uid = data.get("id")
                if uid:
                    self.gridWidget.removeItemByUID(uid)
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()