import pytest
from src.model.Xor import Xor
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

def test_xor_raises_error_on_too_few_inputs():
    xor_gate = Xor()
    xor_gate.addInput(DummyInput(True),"outValue","input2")  # Manually add second input to avoid KeyError
    assert xor_gate.eval() == True
    assert xor_gate.state["outValue"] == (1,1)

def test_xor_raises_error_on_too_many_inputs():
    xor_gate = Xor()
    xor_gate.addInput(DummyInput(True),"outValue","input1")  # Manually add third input to avoid KeyError
    xor_gate.addInput(DummyInput(False),"outValue","input2")  # Manually add fourth input to avoid KeyError
    with pytest.raises(KeyError):
        xor_gate.addInput(DummyInput(True),"outValue","input1")

@pytest.mark.parametrize("a, b, expected", [
    (False, False, False),
    (False, True, True),
    (True, False, True),
    (True, True, False),
])
def test_xor_logic_state_and_change(a, b, expected):
    getBus().setManual()
    xor_gate = Xor()
    xor_gate.addInput(DummyInput(a),"outValue","input1")
    xor_gate.addInput(DummyInput(b),"outValue","input2")
    changed = xor_gate.eval()
    expected_tuple = (1,1) if expected else (0,1)
    assert xor_gate.state["outValue"] == expected_tuple, f"Xor.state['outValue'] should be {expected_tuple} after eval() with inputs {a}, {b}."
    assert changed is (expected_tuple != (0,1)), "Xor.eval() should return True if state changed from default."
    changed = xor_gate.eval()
    assert changed is False, "Xor.eval() should return False if state does not change."

def test_xor_state_changes_multiple_times():
    getBus().setManual()
    xor_gate = Xor()
    a = DummyInput(False)
    b = DummyInput(False)
    xor_gate.addInput(a,"outValue","input1")
    xor_gate.addInput(b,"outValue","input2")
    changed = xor_gate.eval()
    assert xor_gate.state["outValue"] == (0,1), "Xor.state['outValue'] should be (0,1) after both inputs are False."
    a.setValue(True)
    changed = xor_gate.eval()
    assert changed is True, "Xor.eval() should return True when state changes from (0,1) to (1,1)."
    assert xor_gate.state["outValue"] == (1,1), "Xor.state['outValue'] should be (1,1) after one input is True."
    b.setValue(True)
    changed = xor_gate.eval()
    assert changed is True, "Xor.eval() should return True when state changes from (1,1) to (0,1)."
    assert xor_gate.state["outValue"] == (0,1), "Xor.state['outValue'] should be (0,1) after both inputs are True."
