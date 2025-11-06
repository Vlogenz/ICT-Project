from src.constants import CELL_SIZE
from src.view.GridItems.GridItem import GridItem
from src.model.Multiplexer import Multiplexer2Inp

class Multiplexer2InpGridItem(GridItem):
    def __init__(self, logicComponent: Multiplexer2Inp, immovable=False):
        super().__init__(logicComponent, immovable)
        size = CELL_SIZE - 8
        self.inputs["input1"].moveTo(0, size / 3 - 8)
        self.inputs["input2"].moveTo(0, 2 * size / 3 - 8)
        self.inputs["selection"].moveTo(size / 2 - 8, size - 16)
        self.updateRects()
