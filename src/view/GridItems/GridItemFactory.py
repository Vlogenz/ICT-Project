from src.model import LogicComponent, Input, HalfAdder, FullAdder, Multiplexer2Inp, Multiplexer4Inp, Multiplexer8Inp, ALUSimple, ALUAdvanced
from .CustomComponentGridItem import CustomComponentGridItem
from .GridItem import GridItem
from .InputGridItem import InputGridItem
from .HalfAdderGridItem import HalfAdderGridItem
from .FullAdderGridItem import FullAdderGridItem
from .Multiplexer2InpGridItem import Multiplexer2InpGridItem
from .Multiplexer4InpGridItem import Multiplexer4InpGridItem
from .Multiplexer8InpGridItem import Multiplexer8InpGridItem
from .ALUSimpleGridItem import ALUSimpleGridItem
from .ALUAdvancedGridItem import ALUAdvancedGridItem
from ...model.CustomLogicComponent import CustomLogicComponent


class GridItemFactory:
    @staticmethod
    def createGridItem(component: LogicComponent, **kwargs) -> GridItem:
        if isinstance(component, Input):
            return InputGridItem(component, **kwargs)
        if isinstance(component, HalfAdder):
            return HalfAdderGridItem(component, **kwargs)
        if isinstance(component, FullAdder):
            return FullAdderGridItem(component, **kwargs)
        if isinstance(component, Multiplexer2Inp):
            return Multiplexer2InpGridItem(component, **kwargs)
        if isinstance(component, Multiplexer4Inp):
            return Multiplexer4InpGridItem(component, **kwargs)
        if isinstance(component, Multiplexer8Inp):
            return Multiplexer8InpGridItem(component, **kwargs)
        if isinstance(component, ALUSimple):
            return ALUSimpleGridItem(component, **kwargs)
        if isinstance(component, ALUAdvanced):
            return ALUAdvancedGridItem(component, **kwargs)
        if isinstance(component, CustomLogicComponent):
            return CustomComponentGridItem(component, **kwargs)
        return GridItem(component, **kwargs)