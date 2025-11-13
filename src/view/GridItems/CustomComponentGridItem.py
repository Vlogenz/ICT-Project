from pathlib import Path
from typing import override

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
    def getImagePath(self) -> str:
        # Dynamically find the image file with the correct extension
        allowed_extensions = [".png", ".jpg", ".jpeg", ".svg"]
        base_path = Path.home() / APP_NAME / "custom_components" / self.logicComponent.customComponentName
        for ext in allowed_extensions:
            image_path = base_path / f"{self.logicComponent.customComponentName}{ext}"
            if image_path.exists():
                return str(image_path)
        # If no image found, return a default path or None
        return ""

    @override
    def showComponentTooltip(self):
        self.setToolTip(f"{self.getName()} ({self.logicComponent.customComponentName} - CustomLogicComponent)")
