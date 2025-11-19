import pytest
from src.model.InstructionMemory import InstructionMemory
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


def test_init():
    getBus().setManual()
    im = InstructionMemory()
    assert im.getInputs() == {"readAddress": None}
    assert im.getState() == {"instruction": (0,32)}

def test_eval():
    getBus().setManual()
    im = InstructionMemory()
    dummy = DummyInput(1,32)
    im.addInput(dummy,"outValue", "readAddress")
    im.loadInstructions([0,4,8,12121212])
    # Test default instruction at address 0
    dummy.setValue(0,32)
    im.eval()
    assert im.getState()["instruction"] == (0, 32)

    # Test instruction at address 4
    dummy.setValue(4,32)
    im.eval()
    assert im.getState()["instruction"] == (4, 32)

    # Test instruction at address 8
    dummy.setValue(8,32)
    im.eval()
    assert im.getState()["instruction"] == (8, 32)

    # Test instruction at address 12
    dummy.setValue(12,32)
    im.eval()
    assert im.getState()["instruction"] == (12121212, 32)
    