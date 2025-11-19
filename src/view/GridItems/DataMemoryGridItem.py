from src.constants import CELL_SIZE
from src.view.GridItems import GridItem
from src.model import DataMemory


class DataMemoryGridItem(GridItem):
    def __init__(self, logicComponent: DataMemory, **kwargs):
        super().__init__(logicComponent, **kwargs)
        size = CELL_SIZE - 8
        self.inputs["memWrite"].moveTo(size / 2 - 8, 0)
        self.inputs["memRead"].moveTo(size / 2 - 8, size - 16)
        self.inputs["address"].moveTo(0, size / 3 - 16)
        self.inputs["writeData"].moveTo(0, 2 * size / 3)
        self.updateRects()
