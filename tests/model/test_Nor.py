import pytest
from src.model.Nor import Nor
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

def test_nor_raises_error_on_too_few_inputs():
	nor_gate = Nor()
	nor_gate.addInput(DummyInput(True),"outValue","input1")
	assert nor_gate.eval() == True
	assert nor_gate.state["outValue"] == (0,1)

def test_nor_raises_error_on_too_many_inputs():
	nor_gate = Nor()
	nor_gate.addInput(DummyInput(True),"outValue","input1")
	nor_gate.addInput(DummyInput(False),"outValue","input2")
	assert not nor_gate.addInput(DummyInput(True),"outValue","input1")

@pytest.mark.parametrize("a, b, expected", [
	(False, False, True),
	(False, True, False),
	(True, False, False),
	(True, True, False),
])
def test_nor_logic_state_and_change(a, b, expected):
    getBus().setManual()
    nor_gate = Nor()
    nor_gate.addInput(DummyInput(a),"outValue","input1")
    nor_gate.addInput(DummyInput(b),"outValue","input2")
    changed = nor_gate.eval()
    expected_tuple = (1,1) if expected else (0,1)
    assert nor_gate.state["outValue"] == expected_tuple, f"Nor.state['outValue'] should be {expected_tuple} after eval() with inputs {a}, {b}."
    assert changed is (expected_tuple != (1,1)), "Nor.eval() should return True if state changed from default."
    changed = nor_gate.eval()
    assert changed is False, "Nor.eval() should return False if state does not change."

def test_nor_state_changes_multiple_times():
    getBus().setManual()
    nor_gate = Nor()
    a = DummyInput(False)
    b = DummyInput(False)
    nor_gate.addInput(a,"outValue","input1")
    nor_gate.addInput(b,"outValue","input2")
    changed = nor_gate.eval()
    assert nor_gate.state["outValue"] == (1,1), "Nor.state['outValue'] should be (1,1) after both inputs are False."
    a.setValue(True)
    changed = nor_gate.eval()
    assert changed is True, "Nor.eval() should return True when state changes from (1,1) to (0,1)."
    assert nor_gate.state["outValue"] == (0,1), "Nor.state['outValue'] should be (0,1) after one input is True."
    a.setValue(False)
    b.setValue(False)
    changed = nor_gate.eval()
    assert nor_gate.state["outValue"] == (1,1), "Nor.state['outValue'] should be (1,1) after both inputs are False again."
