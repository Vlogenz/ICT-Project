from src.view.GridItem import GridItem

class Connection:
    """Represents an established connection between two items in the grid.
    Apart from the start and destination item, we also need the for the output and input port, respectively.
    This is so that the connection goes to the right place and also to add it to the backend correctly.
    Additionally, the attribute isActive says, whether the connection is part of the current evaluation step.
    This is especially useful for animated evaluation (speed slider not on instant).
    """

    def __init__(self, srcItem: GridItem, srcKey: str, dstItem: GridItem, dstKey: str):
        self.srcItem = srcItem
        self.srcKey = srcKey
        self.dstItem = dstItem
        self.dstKey = dstKey
        self.isActive = False