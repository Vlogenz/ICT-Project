from src.view.GridItems.GridItem import GridItem
from src.model.Multiplexer import Multiplexer8Inp
from src.constants import CELL_SIZE
class Multiplexer8InpGridItem(GridItem):
    def __init__(self, logicComponent: Multiplexer8Inp, immovable=False):
        super().__init__(logicComponent, immovable)
        size = CELL_SIZE - 8
        self.inputs["input1"].moveTo(0, size / 9 - 8)
        self.inputs["input2"].moveTo(0, 2 * size / 9 - 8)
        self.inputs["input3"].moveTo(0, 3 * size / 9 - 8)
        self.inputs["input4"].moveTo(0, 4 * size / 9 - 8)
        self.inputs["input5"].moveTo(0, 5 * size / 9 - 8)
        self.inputs["input6"].moveTo(0, 6 * size / 9 - 8)
        self.inputs["input7"].moveTo(0, 7 * size / 9 - 8)
        self.inputs["input8"].moveTo(0, 8 * size / 9 - 8)
        self.inputs["selection"].moveTo(size / 2 - 8, size - 16)
        self.updateRects()