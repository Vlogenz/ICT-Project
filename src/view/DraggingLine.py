from src.view.GridItems.GridItem import GridItem
from PySide6 import QtCore


class DraggingLine:
    """Represents a currently dragged line. It starts from the output port with srcKey at the srcItem.
    The startPos is added because it is easier to store it here than to derive it from the starting output port each time.
    The currentPos represents the current end of the line, i.e. the position of the cursor.
    """

    def __init__(self, srcItem: GridItem, srcKey: str, startPos: QtCore.QPoint, currentPos: QtCore.QPoint):
        self.srcItem = srcItem
        self.srcKey = srcKey
        self.startPos = startPos
        self.currentPos = currentPos