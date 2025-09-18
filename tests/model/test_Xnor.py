import pytest
from src.model.Xnor import Xnor
from .DummyInput import DummyInput

def test_xnor_raises_error_on_too_few_inputs():
    xnor_gate = Xnor()
    xnor_gate.inputs = [DummyInput(True)]
    with pytest.raises(ValueError):
        xnor_gate.eval()

def test_xnor_raises_error_on_too_many_inputs():
    xnor_gate = Xnor()
    xnor_gate.inputs = [DummyInput(True), DummyInput(False), DummyInput(True)]
    with pytest.raises(ValueError):
        xnor_gate.eval()

@pytest.mark.parametrize("a, b, expected", [
    (False, False, True),
    (False, True, False),
    (True, False, False),
    (True, True, True),
])
def test_xnor_logic_state_and_change(a, b, expected):
    xnor_gate = Xnor()
    xnor_gate.inputs = [DummyInput(a), DummyInput(b)]
    changed = xnor_gate.eval()
    expected_tuple = (1,1) if expected else (0,1)
    assert xnor_gate.state["outValue"] == expected_tuple, f"Xnor.state['outValue'] should be {expected_tuple} after eval() with inputs {a}, {b}."
    assert changed is (expected_tuple != (0,1)), "Xnor.eval() should return True if state changed from default."
    changed = xnor_gate.eval()
    assert changed is False, "Xnor.eval() should return False if state does not change."

def test_xnor_state_changes_multiple_times():
    xnor_gate = Xnor()
    a = DummyInput(False)
    b = DummyInput(False)
    xnor_gate.inputs = [a, b]
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
