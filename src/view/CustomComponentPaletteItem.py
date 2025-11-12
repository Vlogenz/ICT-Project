from typing import override
from pathlib import Path

from src.model.CustomLogicComponentData import CustomLogicComponentData
from src.view.PaletteItem import PaletteItem
from src.constants import APP_NAME
from dataclasses import asdict

class CustomComponentPaletteItem(PaletteItem):
    def __init__(self, componentData: CustomLogicComponentData, **kwargs):
        super().__init__(componentName=componentData.name, **kwargs)
        self.componentData = componentData

    @override
    def getImagePath(self) -> str:
        # Try all supported image extensions
        supported_exts = [".png", ".jpg", ".jpeg", ".svg"]
        base_path = Path.home() / APP_NAME / "custom_components" / self.componentName
        for ext in supported_exts:
            candidate = base_path / f"{self.componentName}{ext}"
            if candidate.exists():
                return str(candidate)
        # Optionally, return None or a default image path if not found
        return ""

    @override
    def getPayload(self):
        return {
                "action_type": "create",  # or "move"
                "componentName": f"{self.componentName}",
                "isCustom": True,
                "customComponentData": asdict(self.componentData)
            }