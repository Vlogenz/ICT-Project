import pytest
from Model.Xor import Xor
from Model.LogicComponent import LogicComponent

class DummyInput(LogicComponent):
    def __init__(self, value):
        super().__init__()
        self.state = value
    def eval(self):
        return self.state

def test_xor_raises_error_on_too_few_inputs():
    xor_gate = Xor()
    xor_gate.inputs = [DummyInput(True)]
    with pytest.raises(ValueError):
        xor_gate.eval()

def test_xor_raises_error_on_too_many_inputs():
    xor_gate = Xor()
    xor_gate.inputs = [DummyInput(True), DummyInput(False), DummyInput(True)]
    with pytest.raises(ValueError):
        xor_gate.eval()

@pytest.mark.parametrize("a, b, expected", [
    (False, False, False),
    (False, True, True),
    (True, False, True),
    (True, True, False),
])
def test_xor_logic_state_and_change(a, b, expected):
    xor_gate = Xor()
    xor_gate.inputs = [DummyInput(a), DummyInput(b)]
    # First eval: state should change from default (likely False) to expected
    changed = xor_gate.eval()
    assert xor_gate.state == expected, f"Xor.state should be {expected} after eval() with inputs {a}, {b}."
    assert changed == (expected != False), "Xor.eval() should return True if state changed from default."
    # Second eval: state should not change if inputs are the same
    changed = xor_gate.eval()
    assert changed is False, "Xor.eval() should return False if state does not change."

def test_xor_state_changes_multiple_times():
    xor_gate = Xor()
    a = DummyInput(False)
    b = DummyInput(False)
    xor_gate.inputs = [a, b]
    # Initial eval: both False, output should be False
    changed = xor_gate.eval()
    assert xor_gate.state is False, "Xor.state should be False after both inputs are False."
    # Change one input to True, output should become True
    a.state = True
    changed = xor_gate.eval()
    assert changed is True, "Xor.eval() should return True when state changes from False to True."
    assert xor_gate.state is True, "Xor.state should be True after one input is True."
    # Change both inputs to True, output should become False
    b.state = True
    changed = xor_gate.eval()
    assert changed is True, "Xor.eval() should return True when state changes from True to False."
    assert xor_gate.state is False, "Xor.state should be False after both inputs are True."
