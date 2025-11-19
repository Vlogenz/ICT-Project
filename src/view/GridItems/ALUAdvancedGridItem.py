from src.constants import CELL_SIZE
from src.model import ALUAdvanced
from src.view.GridItems.GridItem import GridItem

class ALUAdvancedGridItem(GridItem):
    def __init__(self, logicComponent: ALUAdvanced, **kwargs):
        super().__init__(logicComponent, **kwargs)
        size = CELL_SIZE - 8
        self.inputs["input1"].moveTo(0, size / 3 - 8)
        self.inputs["input2"].moveTo(0, 2 * size / 3 - 8)
        self.inputs["Ainvert"].moveTo(size / 3 - 8, 0)
        self.inputs["Bnegate"].moveTo(2 * size / 3 - 16 + 1, 0)
        self.inputs["OP"].moveTo(size / 2 - 8, size-16)
        self.outputs["zero"].moveTo(size-16, size / 3 - 8)
        self.outputs["outValue"].moveTo(size-16, 2 * size / 3 - 8)
        self.updateRects()
