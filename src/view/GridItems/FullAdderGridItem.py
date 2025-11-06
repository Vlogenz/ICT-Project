from src.constants import CELL_SIZE
from src.view.GridItems.GridItem import GridItem
from src.model.FullAdder import FullAdder

class FullAdderGridItem(GridItem):
    def __init__(self, logicComponent: FullAdder, immovable=False):
        super().__init__(logicComponent, immovable)
        size = CELL_SIZE - 8
        self.inputs["inputA"].moveTo(0, size / 3 - 8)
        self.inputs["inputB"].moveTo(0, 2 * size / 3 - 8)
        self.inputs["inputCin"].moveTo(size / 2 - 8, 0)
        self.outputs["outSum"].moveTo(size - 16, size / 2 - 8)
        self.outputs["cOut"].moveTo(size / 2 - 8, size - 16)
        self.updateRects()
