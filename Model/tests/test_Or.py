import pytest
from Model.Or import Or
from .DummyInput import DummyInput

def test_or_raises_error_on_too_few_inputs():
    or_gate = Or()
    or_gate.inputs = [DummyInput(True)]
    with pytest.raises(ValueError):
        or_gate.eval()

def test_or_raises_error_on_too_many_inputs():
    or_gate = Or()
    or_gate.inputs = [DummyInput(True), DummyInput(False), DummyInput(True)]
    with pytest.raises(ValueError):
        or_gate.eval()


@pytest.mark.parametrize("a, b, expected", [
    (False, False, False),
    (False, True, True),
    (True, False, True),
    (True, True, True),
])
def test_or_logic_state_and_change(a, b, expected):
    or_gate = Or()
    or_gate.inputs = [DummyInput(a), DummyInput(b)]
    # First eval: state should change from default (likely False) to expected
    changed = or_gate.eval()
    assert or_gate.state is expected, f"Or.state should be {expected} after eval() with inputs {a}, {b}."
    assert changed is (expected != False), "Or.eval() should return True if state changed from default."
    # Second eval: state should not change if inputs are the same
    changed = or_gate.eval()
    assert changed is False, "Or.eval() should return False if state does not change."

def test_or_state_changes_multiple_times():
    or_gate = Or()
    a = DummyInput(False)
    b = DummyInput(False)
    or_gate.inputs = [a, b]
    or_gate.eval()  # state should be False
    # Change one input to True
    a.state = True
    changed = or_gate.eval()
    assert changed is True, "Or.eval() should return True when state changes from False to True."
    assert or_gate.state is True, "Or.state should be True after input changes."
    # Change both inputs to False
    a.state = False
    b.state = False
    changed = or_gate.eval()
    assert changed is True, "Or.eval() should return True when state changes from True to False."
    assert or_gate.state is False, "Or.state should be False after both inputs are False."

