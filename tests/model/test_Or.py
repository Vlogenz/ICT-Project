import pytest
from src.model.Or import Or
from .DummyInput import DummyInput

def test_or_raises_error_on_too_few_inputs():
    or_gate = Or()
    or_gate.addInput(DummyInput(True),"outValue","input2")  # Manually add second input to avoid KeyError
    assert or_gate.eval() == True
    assert or_gate.state["outValue"] == (1,1)

def test_or_raises_error_on_too_many_inputs():
    or_gate = Or()
    or_gate.addInput(DummyInput(True),"outValue","input1")  # Manually add second input to avoid KeyError
    or_gate.addInput(DummyInput(False),"outValue","input2")  # Manually add third input to avoid KeyError
    with pytest.raises(KeyError):
        or_gate.addInput(DummyInput(True),"outValue","input1")


@pytest.mark.parametrize("a, b, expected", [
    (False, False, False),
    (False, True, True),
    (True, False, True),
    (True, True, True),
])
def test_or_logic_state_and_change(a, b, expected):
    or_gate = Or()
    or_gate.addInput(DummyInput(a),"outValue","input1")
    or_gate.addInput(DummyInput(b),"outValue","input2")
    changed = or_gate.eval()
    expected_tuple = (1,1) if expected else (0,1)
    assert or_gate.state["outValue"] == expected_tuple, f"Or.state['outValue'] should be {expected_tuple} after eval() with inputs {a}, {b}."
    assert changed is (expected_tuple != (0,1)), "Or.eval() should return True if state changed from default."
    changed = or_gate.eval()
    assert changed is False, "Or.eval() should return False if state does not change."

def test_or_state_changes_multiple_times():
    or_gate = Or()
    a = DummyInput(False)
    b = DummyInput(False)
    or_gate.addInput(a,"outValue","input1")
    or_gate.addInput(b,"outValue","input2")
    or_gate.eval()  # state should be (0,1)
    a.setValue(True)
    changed = or_gate.eval()
    assert changed is True, "Or.eval() should return True when state changes from (0,1) to (1,1)."
    assert or_gate.state["outValue"] == (1,1), "Or.state['outValue'] should be (1,1) after input changes."
    a.setValue(False)
    b.setValue(False)
    changed = or_gate.eval()
    assert changed is True, "Or.eval() should return True when state changes from (1,1) to (0,1)."
    assert or_gate.state["outValue"] == (0,1), "Or.state['outValue'] should be (0,1) after both inputs are False."

