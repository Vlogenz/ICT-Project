from src.constants import CELL_SIZE
from src.view.GridItems.GridItem import GridItem
from src.model.HalfAdder import HalfAdder

class HalfAdderGridItem(GridItem):
    def __init__(self, logicComponent: HalfAdder, immovable=False):
        super().__init__(logicComponent, immovable)
        size = CELL_SIZE - 8
        self.inputs["inputA"].moveTo(0, size / 3 - 8)
        self.inputs["inputB"].moveTo(0, 2 * size / 3 - 8)
        self.outputs["sum"].moveTo(size - 16, size / 2 - 8)
        self.outputs["carry"].moveTo(size / 2 - 8, size - 16)
        self.updateRects()