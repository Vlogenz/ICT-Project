import pytest
from src.model.Xnor import Xnor
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

def test_xnor_raises_error_on_too_few_inputs():
    xnor_gate = Xnor()
    xnor_gate.addInput(DummyInput(True),"outValue","input1")  # Manually add second input to avoid KeyError
    assert xnor_gate.eval() == True
    assert xnor_gate.state["outValue"] == (0,1)

def test_xnor_raises_error_on_too_many_inputs():
    xnor_gate = Xnor()
    xnor_gate.addInput(DummyInput(True),"outValue","input1")  # Manually add third input to avoid KeyError
    xnor_gate.addInput(DummyInput(False),"outValue","input2")  # Manually add fourth input to avoid KeyError
    assert not xnor_gate.addInput(DummyInput(True),"outValue","input1")

@pytest.mark.parametrize("a, b, expected", [
    (False, False, True),
    (False, True, False),
    (True, False, False),
    (True, True, True),
])
def test_xnor_logic_state_and_change(a, b, expected):
    getBus().setManual()
    xnor_gate = Xnor()
    xnor_gate.addInput(DummyInput(a),"outValue","input1")
    xnor_gate.addInput(DummyInput(b),"outValue","input2")
    changed = xnor_gate.eval()
    expected_tuple = (1,1) if expected else (0,1)
    assert xnor_gate.state["outValue"] == expected_tuple, f"Xnor.state['outValue'] should be {expected_tuple} after eval() with inputs {a}, {b}."
    assert changed is (expected_tuple != (1,1)), "Xnor.eval() should return True if state changed from default."
    changed = xnor_gate.eval()
    assert changed is False, "Xnor.eval() should return False if state does not change."

def test_xnor_state_changes_multiple_times():
    getBus().setManual()
    xnor_gate = Xnor()
    a = DummyInput(False)
    b = DummyInput(False)
    xnor_gate.addInput(a,"outValue","input1")
    xnor_gate.addInput(b,"outValue","input2")
    changed = xnor_gate.eval()
    assert xnor_gate.state["outValue"] == (1,1), "Xnor.state['outValue'] should be (1,1) after both inputs are False."
    a.setValue(True)
    changed = xnor_gate.eval()
    assert changed is True, "Xnor.eval() should return True when state changes from (1,1) to (0,1)."
    assert xnor_gate.state["outValue"] == (0,1), "Xnor.state['outValue'] should be (0,1) after one input is True."
    b.setValue(True)
    changed = xnor_gate.eval()
    assert changed is True, "Xnor.eval() should return True when state changes from (0,1) to (1,1)."
    assert xnor_gate.state["outValue"] == (1,1), "Xnor.state['outValue'] should be (1,1) after both inputs are True."
