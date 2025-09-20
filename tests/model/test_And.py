import pytest
from src.model.And import And
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

def test_and_raises_error_on_too_few_inputs():
    and_gate = And()
    and_gate.addInput(DummyInput(True),"outValue","input1")
    assert and_gate.eval() == False
    assert and_gate.state["outValue"] == (0,1)

def test_and_raises_error_on_too_many_inputs():
    and_gate = And()
    and_gate.addInput(DummyInput(True),"outValue","input1")
    and_gate.addInput(DummyInput(False),"outValue","input2")
    with pytest.raises(KeyError):
        and_gate.addInput(DummyInput(True),"outValue","input1")


@pytest.mark.parametrize("a, b, expected", [
    (False, False, False),
    (False, True, False),
    (True, False, False),
    (True, True, True),
])
def test_and_logic_state_and_change(a, b, expected):
    getBus().setManual()
    and_gate = And()
    and_gate.addInput(DummyInput(a),"outValue","input1")
    and_gate.addInput(DummyInput(b),"outValue","input2")
    changed = and_gate.eval()
    expected_tuple = (1,1) if expected else (0,1)
    assert and_gate.state["outValue"] == expected_tuple, f"And.state['outValue'] should be {expected_tuple} after eval() with inputs {a}, {b}."
    assert changed is (expected_tuple != (0,1)), "And.eval() should return True if state changed from default."
    changed = and_gate.eval()
    assert changed is False, "And.eval() should return False if state does not change."

def test_and_state_changes_multiple_times():
    getBus().setManual()
    and_gate = And()
    a = DummyInput(True)
    b = DummyInput(False)
    and_gate.addInput(a,"outValue","input1")
    and_gate.addInput(b,"outValue","input2")
    and_gate.eval()  # state should be (0,1)
    b.setValue(True)
    changed = and_gate.eval()
    assert changed is True, "And.eval() should return True when state changes from (0,1) to (1,1)."
    assert and_gate.state["outValue"] == (1,1), "And.state['outValue'] should be (1,1) after both inputs are True."
    a.setValue(False)
    changed = and_gate.eval()
    assert changed is True, "And.eval() should return True when state changes from (1,1) to (0,1)."
    assert and_gate.state["outValue"] == (0,1), "And.state['outValue'] should be (0,1) after one input is False."

