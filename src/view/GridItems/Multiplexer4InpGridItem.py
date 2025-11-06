from src.constants import CELL_SIZE
from src.view.GridItems.GridItem import GridItem
from src.model.Multiplexer import Multiplexer4Inp

class Multiplexer4InpGridItem(GridItem):
    def __init__(self, logicComponent: Multiplexer4Inp, **kwargs):
        super().__init__(logicComponent, **kwargs)
        size = CELL_SIZE - 8
        self.inputs["input1"].moveTo(0, size / 5 - 8)
        self.inputs["input2"].moveTo(0, 2 * size / 5 - 8)
        self.inputs["input3"].moveTo(0, 3 * size / 5 - 8)
        self.inputs["input4"].moveTo(0, 4 * size / 5 - 8)
        self.inputs["selection"].moveTo(size / 2 - 8, size - 16)
        self.updateRects()
