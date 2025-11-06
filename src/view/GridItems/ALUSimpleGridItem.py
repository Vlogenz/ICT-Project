from src.constants import CELL_SIZE
from src.view.GridItems.GridItem import GridItem
from src.model.ALUSimple import ALUSimple

class ALUSimpleGridItem(GridItem):
    def __init__(self, logicComponent: ALUSimple, immovable=False):
        super().__init__(logicComponent, immovable)
        size = CELL_SIZE - 8
        self.inputs["input1"].moveTo(0, size / 3 - 8)
        self.inputs["input2"].moveTo(0, 2 * size / 3 - 8)
        self.inputs["Ainvert"].moveTo(size / 3 - 8, 0)
        self.inputs["Binvert"].moveTo(2 * size / 3 - 16 + 1, 0)
        self.inputs["OP"].moveTo(size / 3 - 8, size-16)
        self.inputs["CarryIn"].moveTo(2* size / 3 - 16, size-16)
        self.updateRects()
