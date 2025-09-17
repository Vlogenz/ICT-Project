import pytest
from src.model.Nand import Nand
from .DummyInput import DummyInput

def test_nand_raises_error_on_too_few_inputs():
    nand_gate = Nand()
    nand_gate.inputs = [DummyInput(True)]
    with pytest.raises(ValueError):
        nand_gate.eval()

def test_nand_raises_error_on_too_many_inputs():
    nand_gate = Nand()
    nand_gate.inputs = [DummyInput(True), DummyInput(False), DummyInput(True)]
    with pytest.raises(ValueError):
        nand_gate.eval()


@pytest.mark.parametrize("a, b, expected", [
    (False, False, True),
    (False, True, True),
    (True, False, True),
    (True, True, False),
])
def test_nand_logic_state_and_change(a, b, expected):
    nand_gate = Nand()
    nand_gate.inputs = [DummyInput(a), DummyInput(b)]
    # First eval: state should change from default (assume False) to expected
    changed = nand_gate.eval()
    assert nand_gate.state == expected, f"Nand.state should be {expected} after eval() with inputs {a}, {b}."
    # State changes if output is different from initial state (assume initial state is False)
    assert changed == (expected != False), "Nand.eval() should return True if state changed from default."
    # Second eval: state should not change if inputs are the same
    changed = nand_gate.eval()
    assert changed is False, "Nand.eval() should return False if state does not change."

def test_nand_state_changes_multiple_times():
    nand_gate = Nand()
    a = DummyInput(True)
    b = DummyInput(True)
    nand_gate.inputs = [a, b]
    # Initial eval: both True, output should be False
    changed = nand_gate.eval()
    assert nand_gate.state is False, "Nand.state should be False after both inputs are True."
    # Change one input to False, output should become True
    a.state = False
    changed = nand_gate.eval()
    assert changed is True, "Nand.eval() should return True when state changes from False to True."
    assert nand_gate.state is True, "Nand.state should be True after one input is False."
    # Change back to both True, output should become False
    a.state = True
    changed = nand_gate.eval()
    assert changed is True, "Nand.eval() should return True when state changes from True to False."
    assert nand_gate.state is False, "Nand.state should be False after both inputs are True."

