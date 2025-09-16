import pytest
from Model.Nor import Nor
from .DummyInput import DummyInput

def test_nor_raises_error_on_too_few_inputs():
	nor_gate = Nor()
	nor_gate.inputs = [DummyInput(True)]
	with pytest.raises(ValueError):
		nor_gate.eval()

def test_nor_raises_error_on_too_many_inputs():
	nor_gate = Nor()
	nor_gate.inputs = [DummyInput(True), DummyInput(False), DummyInput(True)]
	with pytest.raises(ValueError):
		nor_gate.eval()

@pytest.mark.parametrize("a, b, expected", [
	(False, False, True),
	(False, True, False),
	(True, False, False),
	(True, True, False),
])
def test_nor_logic_state_and_change(a, b, expected):
	nor_gate = Nor()
	nor_gate.inputs = [DummyInput(a), DummyInput(b)]
	# First eval: state should change from default (likely False) to expected
	changed = nor_gate.eval()
	assert nor_gate.state == expected, f"Nor.state should be {expected} after eval() with inputs {a}, {b}."
	assert changed == (expected != False), "Nor.eval() should return True if state changed from default."
	# Second eval: state should not change if inputs are the same
	changed = nor_gate.eval()
	assert changed is False, "Nor.eval() should return False if state does not change."

def test_nor_state_changes_multiple_times():
	nor_gate = Nor()
	a = DummyInput(False)
	b = DummyInput(False)
	nor_gate.inputs = [a, b]
	# Initial eval: both False, output should be True
	changed = nor_gate.eval()
	assert nor_gate.state is True, "Nor.state should be True after both inputs are False."
	# Change one input to True, output should become False
	a.state = True
	changed = nor_gate.eval()
	assert changed is True, "Nor.eval() should return True when state changes from True to False."
	assert nor_gate.state is False, "Nor.state should be False after one input is True."
	# Change both inputs back to False, output should become True
	a.state = False
	b.state = False
	changed = nor_gate.eval()
	assert changed is True, "Nor.eval() should return True when state changes from False to True."
	assert nor_gate.state is True, "Nor.state should be True after both inputs are False."
