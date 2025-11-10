from src.model import LogicComponent
from dataclasses import dataclass
from typing import List

@dataclass
class CustomLogicComponent:
    """A custom component made by the user"""
    name: str
    inputKeys: List[str]
    outputKeys: List[str]
    components: List[LogicComponent]