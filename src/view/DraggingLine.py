from src.view.GridItem import GridItem
from PySide6 import QtCore


class DraggingLine:
    def __init__(self, srcItem: GridItem, srcKey: str, startPos: QtCore.QPoint, currentPos: QtCore.QPoint):
        self.srcItem = srcItem
        self.srcKey = srcKey
        self.startPos = startPos
        self.currentPos = currentPos