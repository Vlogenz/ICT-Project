from src.model import LogicComponent, Input, HalfAdder, FullAdder, Multiplexer2Inp, Multiplexer4Inp, Multiplexer8Inp, ALUSimple, ALUAdvanced
from .GridItem import GridItem
from .InputGridItem import InputGridItem
from .HalfAdderGridItem import HalfAdderGridItem
from .FullAdderGridItem import FullAdderGridItem
from .Multiplexer2InpGridItem import Multiplexer2InpGridItem
from .Multiplexer4InpGridItem import Multiplexer4InpGridItem
from .Multiplexer8InpGridItem import Multiplexer8InpGridItem
from .ALUSimpleGridItem import ALUSimpleGridItem
from .ALUAdvancedGridItem import ALUAdvancedGridItem

class GridItemFactory:
    @staticmethod
    def createGridItem(component: LogicComponent, immovable: bool = False) -> GridItem:
        if isinstance(component, Input):
            return InputGridItem(component, immovable=immovable)
        if isinstance(component, HalfAdder):
            return HalfAdderGridItem(component, immovable=immovable)
        if isinstance(component, FullAdder):
            return FullAdderGridItem(component, immovable=immovable)
        if isinstance(component, Multiplexer2Inp):
            return Multiplexer2InpGridItem(component, immovable=immovable)
        if isinstance(component, Multiplexer4Inp):
            return Multiplexer4InpGridItem(component, immovable=immovable)
        if isinstance(component, Multiplexer8Inp):
            return Multiplexer8InpGridItem(component, immovable=immovable)
        if isinstance(component, ALUSimple):
            return ALUSimpleGridItem(component, immovable=immovable)
        if isinstance(component, ALUAdvanced):
            return ALUAdvancedGridItem(component, immovable=immovable)
        return GridItem(component, immovable=immovable)