from pathlib import Path
from typing import override

from src.model.CustomLogicComponent import CustomLogicComponent
from src.view.GridItems import GridItem
from src.constants import APP_NAME


class CustomComponentGridItem(GridItem):
    def __init__(self, logicComponent:CustomLogicComponent, **kwargs):
        self.name = logicComponent.name
        super().__init__(logicComponent, **kwargs)

    @override
    def getName(self) -> str:
        return self.name

    @override
    def getImagePath(self) -> str:
        return str(Path.home() / APP_NAME / "custom_components" / self.name / f"{self.name}.jpg")