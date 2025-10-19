from src.view.GridItem import GridItem

class Connection:
    def __init__(self, srcItem: GridItem, srcKey: str, dstItem: GridItem, dstKey: str):
        self.srcItem = srcItem
        self.srcKey = srcKey
        self.dstItem = dstItem
        self.dstKey = dstKey
        self.isActive = False