"""Global constants for the whole project."""
from enum import Enum
from src.model import *

CELL_SIZE = 100
GRID_COLS = 59
GRID_ROWS = 40
PALETTE_COLS = 3
MIME_TYPE = "application/x-qt-grid-item"
MAX_EVAL_CYCLES: int = 5
APP_NAME = "CircuitQuest"

class Scene(Enum):
    MAIN = 0
    SANDBOX = 1
    LEVEL_SELECTION = 2
    LEVEL = 3

#TODO: Rearrange this in a meaningful way.
COMPONENT_MAP = {
    "Input": Input,
    "Output": Output,
    "And": And,
    "Or": Or,
    "Not": Not,
    "Nand": Nand,
    "Nor": Nor,
    "Xor": Xor,
    "Xnor": Xnor,
    "DLatch": DLatch,
    "HalfAdder": HalfAdder,
    "FullAdder": FullAdder,
    "Multiplexer2Inp": Multiplexer2Inp,
    "Multiplexer4Inp": Multiplexer4Inp,
    "Multiplexer8Inp": Multiplexer8Inp,
    "Collector1to8": Collector1to8,
    "Collector1to6": Collector1to6,
    "Collector1to5": Collector1to5,
    "Collector1to3": Collector1to3,
    "Collector1to2": Collector1to2,
    "Collector8to32": Collector8to32,
    "Splitter8to1": Splitter8to1,
    "Splitter32to8": Splitter32to8,
    "ALUSimple": ALUSimple,
    "ALUAdvanced": ALUAdvanced,
    "SignExtend": SignExtend,
    "ShiftLeft2": ShiftLeft2,
    "DecoderThreeBit": DecoderThreeBit,
    "Register": Register,
    "DataMemory": DataMemory,
    "InstructionMemory": InstructionMemory,
    "ProgramCounter": ProgramCounter,
    "RegisterBlock": RegisterBlock,
    "Adder32bit": Adder32bit
    
    }
