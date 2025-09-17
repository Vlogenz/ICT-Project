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
    # First eval: state should change from default (likely False) to expected
    changed = xnor_gate.eval()
    assert xnor_gate.state == expected, f"Xnor.state should be {expected} after eval() with inputs {a}, {b}."
    assert changed == (expected != False), "Xnor.eval() should return True if state changed from default."
    # Second eval: state should not change if inputs are the same
    changed = xnor_gate.eval()
    assert changed is False, "Xnor.eval() should return False if state does not change."

def test_xnor_state_changes_multiple_times():
    xnor_gate = Xnor()
    a = DummyInput(False)
    b = DummyInput(False)
    xnor_gate.inputs = [a, b]
    # Initial eval: both False, output should be True
    changed = xnor_gate.eval()
    assert xnor_gate.state is True, "Xnor.state should be True after both inputs are False."
    # Change one input to True, output should become False
    a.state = True
    changed = xnor_gate.eval()
    assert changed is True, "Xnor.eval() should return True when state changes from True to False."
    assert xnor_gate.state is False, "Xnor.state should be False after one input is True."
    # Change both inputs to True, output should become True
    b.state = True
    changed = xnor_gate.eval()
    assert changed is True, "Xnor.eval() should return True when state changes from False to True."
    assert xnor_gate.state is True, "Xnor.state should be True after both inputs are True."
