import pytest
from Model.Not import Not
from .DummyInput import DummyInput

def test_not_raises_error_on_too_few_inputs():
    not_gate = Not()
    not_gate.inputs = []
    with pytest.raises(ValueError):
        not_gate.eval()

def test_not_raises_error_on_too_many_inputs():
    not_gate = Not()
    not_gate.inputs = [DummyInput(True), DummyInput(False)]
    with pytest.raises(ValueError):
        not_gate.eval()


@pytest.mark.parametrize("a, expected", [
    (False, True),
    (True, False),
])
def test_not_logic_state_and_change(a, expected):
    not_gate = Not()
    not_gate.inputs = [DummyInput(a)]
    # First eval: state should change from default to expected
    changed = not_gate.eval()
    assert not_gate.state is expected, f"Not.state should be {expected} after eval() with input {a}."
    assert changed is (expected != False), "Not.eval() should return True if state changed from default."
    # Second eval: state should not change if input is the same
    changed = not_gate.eval()
    assert changed is False, "Not.eval() should return False if state does not change."

def test_not_state_changes_multiple_times():
    not_gate = Not()
    a = DummyInput(False)
    not_gate.inputs = [a]
    not_gate.eval()  # state should be True
    # Change input to True
    a.state = True
    changed = not_gate.eval()
    assert changed is True, "Not.eval() should return True when state changes from True to False."
    assert not_gate.state is False, "Not.state should be False after input changes."
    # Change input back to False
    a.state = False
    changed = not_gate.eval()
    assert changed is True, "Not.eval() should return True when state changes from False to True."
    assert not_gate.state is True, "Not.state should be True after input changes."
