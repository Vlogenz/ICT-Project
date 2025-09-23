import pytest
from src.model.Nand import Nand
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

def test_nand_raises_error_on_too_few_inputs():
    nand_gate = Nand()
    nand_gate.addInput(DummyInput(True),"outValue","input1")
    assert nand_gate.eval() == False
    assert nand_gate.state["outValue"] == (1,1)

def test_nand_raises_error_on_too_many_inputs():
    nand_gate = Nand()
    nand_gate.addInput(DummyInput(True),"outValue","input1")
    nand_gate.addInput(DummyInput(False),"outValue","input2")
    assert nand_gate.addInput(DummyInput(True),"outValue","input1") == False


@pytest.mark.parametrize("a, b, expected", [
    (False, False, True),
    (False, True, True),
    (True, False, True),
    (True, True, False),
])
def test_nand_logic_state_and_change(a, b, expected):
    getBus().setManual()
    nand_gate = Nand()
    nand_gate.addInput(DummyInput(a),"outValue","input1")
    nand_gate.addInput(DummyInput(b),"outValue","input2")
    changed = nand_gate.eval()
    expected_tuple = (1,1) if expected else (0,1)
    assert nand_gate.state["outValue"] == expected_tuple, f"Nand.state['outValue'] should be {expected_tuple} after eval() with inputs {a}, {b}."
    assert changed is (expected_tuple != (1,1)), "Nand.eval() should return True if state changed from default."
    changed = nand_gate.eval()
    assert changed is False, "Nand.eval() should return False if state does not change."


def test_nand_state_changes_multiple_times():
    getBus().setManual()
    nand_gate = Nand()
    a = DummyInput(True)
    b = DummyInput(True)
    nand_gate.addInput(a,"outValue","input1")
    nand_gate.addInput(b,"outValue","input2")
    changed = nand_gate.eval()
    assert nand_gate.state["outValue"] == (0,1), "Nand.state['outValue'] should be (0,1) after both inputs are True."
    a.setValue(False)
    changed = nand_gate.eval()
    assert changed is True, "Nand.eval() should return True when state changes from (0,1) to (1,1)."
    assert nand_gate.state["outValue"] == (1,1), "Nand.state['outValue'] should be (1,1) after one input is False."
    a.setValue(True)
    changed = nand_gate.eval()
    assert changed is True, "Nand.eval() should return True when state changes from (1,1) to (0,1)."
    assert nand_gate.state["outValue"] == (0,1), "Nand.state['outValue'] should be (0,1) after both inputs are True again."

