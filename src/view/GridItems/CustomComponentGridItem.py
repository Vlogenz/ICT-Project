from pathlib import Path
from typing import override
from PySide6 import QtGui

from src.model.CustomLogicComponent import CustomLogicComponent
from src.view.GridItems import GridItem
from src.constants import APP_NAME


class CustomComponentGridItem(GridItem):
    def __init__(self, logicComponent:CustomLogicComponent, **kwargs):
        self.logicComponent = logicComponent
        super().__init__(logicComponent, **kwargs)

    @override
    def getName(self) -> str:
        if self.logicComponent.getLabel() != "":
            return self.logicComponent.getLabel()
        return self.logicComponent.customComponentName

    @override
    def getImage(self) -> QtGui.QPixmap:
        # Dynamically find the image file with the correct extension
        allowed_extensions = [".png", ".jpg", ".jpeg", ".svg"]
        base_path = Path.home() / APP_NAME / "custom_components" / self.logicComponent.customComponentName
        image_path = ""
        for ext in allowed_extensions:
            image_path = base_path / f"{self.logicComponent.customComponentName}{ext}"
            if image_path.exists():
                break
        return QtGui.QPixmap(image_path)

    @override
    def showComponentTooltip(self):
        self.setToolTip(f"{self.getName()} ({self.logicComponent.customComponentName} - CustomLogicComponent)")
