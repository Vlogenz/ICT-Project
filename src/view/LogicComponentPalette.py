from PySide6 import QtWidgets, QtCore

from src.view.PaletteItem import PaletteItem
from src.constants import PALETTE_COLS

class LogicComponentPalette(QtWidgets.QScrollArea):

    def __init__(self, classes):
        super().__init__()

        self.layout = QtWidgets.QGridLayout()
        for i, class_ in enumerate(classes):
            # Use index for a x-column grid
            self.layout.addWidget(PaletteItem(class_), i // PALETTE_COLS, i % PALETTE_COLS)
        paletteFrame = QtWidgets.QFrame()
        paletteFrame.setLayout(self.layout)
        self.setWidget(paletteFrame)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.setStyleSheet("background-color: transparent;")
