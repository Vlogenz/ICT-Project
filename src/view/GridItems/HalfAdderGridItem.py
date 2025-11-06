from src.constants import CELL_SIZE
from src.view.GridItems.GridItem import GridItem
from src.model import HalfAdder

class HalfAdderGridItem(GridItem):
    def __init__(self, logicComponent: HalfAdder, **kwargs):
        super().__init__(logicComponent, **kwargs)
        size = CELL_SIZE - 8
        self.inputs["inputA"].moveTo(0, size / 3 - 8)
        self.inputs["inputB"].moveTo(0, 2 * size / 3 - 8)
        self.outputs["sum"].moveTo(size - 16, size / 2 - 8)
        self.outputs["carry"].moveTo(size / 2 - 8, size - 16)
        self.updateRects()