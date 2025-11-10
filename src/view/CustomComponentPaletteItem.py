from typing import override
from pathlib import Path

from src.model.CustomLogicComponent import CustomLogicComponent
from src.view.PaletteItem import PaletteItem
from src.constants import APP_NAME

class CustomComponentPaletteItem(PaletteItem):
    def __init__(self, componentName: str, componentData: CustomLogicComponent, **kwargs):
        super().__init__(componentName, **kwargs)
        self.componentData = componentData

    @override
    def getImagePath(self) -> str:
        return str(Path.home() / APP_NAME / "custom_components" / self.componentName / f"{self.componentName}.jpg")

    @override
    def getPayload(self):
        return {
                "action_type": "create",  # or "move"
                "componentName": f"{self.componentName}",
                "isCustom": True,
                "customComponentData": self.componentData
            }