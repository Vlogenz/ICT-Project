"""Global constants for the whole project."""
from enum import Enum

CELL_SIZE = 100
#TODO: make grid size dynamic or "infinite" with scrolling
GRID_COLS = 8
GRID_ROWS = 8
MIME_TYPE = "application/x-qt-grid-item"
MAX_EVAL_CYCLES: int = 5

class Scene(Enum):
    MAIN = 0
    SANDBOX = 1
    LEVEL_SELECTION = 2
    LEVEL = 3
