from symtable import Class
from PySide6 import QtWidgets, QtCore
from typing import List, TypeVar, Type

from src.view.PaletteItem import PaletteItem
from src.model import LogicComponent
from src.constants import PALETTE_COLS, COMPONENT_MAP

class LogicComponentPalette(QtWidgets.QScrollArea):

    T = TypeVar("T", bound=LogicComponent)
    def __init__(self, classes: List[Type[T]] = None):
        super().__init__()
        if classes is not None:
            classesList = classes
        else:
            classesList = COMPONENT_MAP.values()

        self.layout = QtWidgets.QGridLayout()
        for i, class_ in enumerate(classesList):
            # Use index for a x-column grid
            self.layout.addWidget(PaletteItem(class_), i // PALETTE_COLS, i % PALETTE_COLS)
        paletteFrame = QtWidgets.QFrame()
        paletteFrame.setLayout(self.layout)
        self.setWidget(paletteFrame)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.setStyleSheet("background-color: transparent;")
