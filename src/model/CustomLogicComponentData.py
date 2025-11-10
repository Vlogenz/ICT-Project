from dataclasses import dataclass
from src.model import LogicComponent
from typing import Dict, List, TypeVar, Type

T = TypeVar("T", bound=LogicComponent)
@dataclass()
class CustomLogicComponentData:
    name: str
    inputMap: Dict[str, int]
    outputMap: Dict[str, int]
    components: List[str]
    connections: List