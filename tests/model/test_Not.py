import pytest
from src.model.Not import Not
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

def test_not_raises_error_on_too_few_inputs():
    not_gate = Not()
    assert not_gate.eval() == False
    assert not_gate.state["outValue"] == (1,1)

def test_not_raises_error_on_too_many_inputs():
    not_gate = Not()
    not_gate.addInput(DummyInput(True),"outValue","input")
    assert not not_gate.addInput(DummyInput(False),"outValue","input")


@pytest.mark.parametrize("a, expected", [
    (False, True),
    (True, False),
])
def test_not_logic_state_and_change(a, expected):
    getBus().setManual()
    not_gate = Not()
    not_gate.addInput(DummyInput(a),"outValue","input")
    changed = not_gate.eval()
    expected_tuple = (1,1) if expected else (0,1)
    assert not_gate.state["outValue"] == expected_tuple, f"Not.state['outValue'] should be {expected_tuple} after eval() with input {a}."
    assert changed is (expected_tuple != (1,1)), "Not.eval() should return True if state changed from default."
    changed = not_gate.eval()
    assert changed is False, "Not.eval() should return False if state does not change."

def test_not_state_changes_multiple_times():
    getBus().setManual()
    not_gate = Not()
    a = DummyInput(False)
    not_gate.addInput(a,"outValue","input")
    not_gate.eval()  # state should be (1,1)
    a.setValue(True)
    changed = not_gate.eval()
    assert changed is True, "Not.eval() should return True when state changes from (1,1) to (0,1)."
    assert not_gate.state["outValue"] == (0,1), "Not.state['outValue'] should be (0,1) after input changes."
    a.setValue(False)
    changed = not_gate.eval()
    assert changed is True, "Not.eval() should return True when state changes from (0,1) to (1,1)."
    assert not_gate.state["outValue"] == (1,1), "Not.state['outValue'] should be (1,1) after input changes."
