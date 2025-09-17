import pytest
from src.model.And import And
from .DummyInput import DummyInput

def test_and_raises_error_on_too_few_inputs():
    and_gate = And()
    and_gate.inputs = [DummyInput(True)]
    with pytest.raises(ValueError):
        and_gate.eval()

def test_and_raises_error_on_too_many_inputs():
    and_gate = And()
    and_gate.inputs = [DummyInput(True), DummyInput(False), DummyInput(True)]
    with pytest.raises(ValueError):
        and_gate.eval()


@pytest.mark.parametrize("a, b, expected", [
    (False, False, False),
    (False, True, False),
    (True, False, False),
    (True, True, True),
])
def test_and_logic_state_and_change(a, b, expected):
    and_gate = And()
    and_gate.inputs = [DummyInput(a), DummyInput(b)]
    # First eval: state should change from default (likely False) to expected
    changed = and_gate.eval()
    assert and_gate.state is expected, f"And.state should be {expected} after eval() with inputs {a}, {b}."
    assert changed is (expected != False), "And.eval() should return True if state changed from default."
    # Second eval: state should not change if inputs are the same
    changed = and_gate.eval()
    assert changed is False, "And.eval() should return False if state does not change."

def test_and_state_changes_multiple_times():
    and_gate = And()
    a = DummyInput(True)
    b = DummyInput(False)
    and_gate.inputs = [a, b]
    and_gate.eval()  # state should be False
    # Change both inputs to True
    b.state = True
    changed = and_gate.eval()
    assert changed is True, "And.eval() should return True when state changes from False to True."
    assert and_gate.state is True, "And.state should be True after both inputs are True."
    # Change one input to False
    a.state = False
    changed = and_gate.eval()
    assert changed is True, "And.eval() should return True when state changes from True to False."
    assert and_gate.state is False, "And.state should be False after one input is False."

