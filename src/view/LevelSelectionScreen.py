from PySide6 import QtGui, QtWidgets
from src.infrastructure.eventBus import getBus

class LevelSelectionScreen(QtWidgets.QWidget):
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.bus = getBus()
        # Zeigt Buttons/Karten für jedes Level
        
    def on_level_clicked(self, level_number: int):
        """User klickt auf Level"""
        self.bus.emit("levelSelection:levelSelected", level_number)
