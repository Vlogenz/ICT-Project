from dataclasses import dataclass
from typing import Dict, List

@dataclass()
class CustomLogicComponentData:
    """
    A simple dataclass for the information that belongs to a CustomLogicComponent.
    This mainly serves as a transport type for the saving and loading processes.
    """
    name: str
    inputMap: Dict[str, int]
    outputMap: Dict[str, int]
    components: List[str]
    connections: List