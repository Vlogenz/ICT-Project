from PySide6 import QtWidgets, QtCore
from typing import List, TypeVar, Type

from src.model.CustomLogicComponentData import CustomLogicComponentData
from src.view.CustomComponentPaletteItem import CustomComponentPaletteItem
from src.view.PaletteItem import PaletteItem
from src.view.util.CollapsibleSection import CollapsibleSection
from src.model import LogicComponent
from src.constants import PALETTE_COLS, COMPONENT_MAP

class LogicComponentPalette(QtWidgets.QScrollArea):

    T = TypeVar("T", bound=LogicComponent)
    def __init__(self, classes: List[Type[T]] = None, customComponents: List[CustomLogicComponentData] = None):
        super().__init__()
        if classes is not None:
            classesList = classes
        else:
            classesList = COMPONENT_MAP.values()

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setSpacing(5)

        # Create section for regular components
        if classesList:
            regularSection = CollapsibleSection("Logic Components")
            for i, class_ in enumerate(classesList):
                regularSection.addWidget(PaletteItem(class_.__name__), i // PALETTE_COLS, i % PALETTE_COLS)
            mainLayout.addWidget(regularSection)

        # Create section for custom components
        if customComponents is not None and len(customComponents) > 0:
            customSection = CollapsibleSection("Custom Components")
            for i, comp in enumerate(customComponents):
                customSection.addWidget(CustomComponentPaletteItem(comp), i // PALETTE_COLS, i % PALETTE_COLS)
            mainLayout.addWidget(customSection)

        # Add stretch to push sections to the top
        mainLayout.addStretch()

        paletteFrame = QtWidgets.QFrame()
        paletteFrame.setLayout(mainLayout)
        self.setWidget(paletteFrame)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.setStyleSheet("background-color: transparent;")
