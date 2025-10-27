from PySide6 import QtGui, QtWidgets
from src.infrastructure.eventBus import getBus

class LevelSelectionScreen(QtWidgets.QWidget):
    """
    Shows a grid with a cell for each level.
    """

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.bus = getBus()

        self.grid = QtWidgets.QGridLayout()
        # load levels



        
        # create a cell for each level and put it on the grid
        
    def on_level_clicked(self, level_number: int):
        """User clicks on a level"""
        self.bus.emit("levelSelection:levelSelected", level_number)
