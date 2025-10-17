from src.view.GridItem import GridItem
from PySide6 import QtCore


class DraggingLine:
    def __init__(self, srcItem: GridItem, startPos: QtCore.QPoint, currentPos: QtCore.QPoint):
        self.srcItem = srcItem
        self.startPos = startPos
        self.currentPos = currentPos