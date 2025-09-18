import pytest
from src.model.Output import Output
from .DummyInput import DummyInput


def test_Output_state_changes_from_default():
    output = Output()
    dummy = DummyInput(True)
    output.inputs.append(dummy)
    changed = output.eval()
    assert changed is True, "Output.eval() should return True when state changes."
    assert output.state["outValue"] == (1,1), "Output.state['outValue'] should be updated to (1,1)."


def test_Output_state_does_not_change():
    output = Output()
    dummy = DummyInput(False)
    output.inputs.append(dummy)
    output.eval()
    changed = output.eval()
    assert changed is False, "Output.eval() should return False when state does not change."
    assert output.state["outValue"] == (0,1), "Output.state['outValue'] should remain (0,1)."

def test_Output_state_changes_multiple_times():
    output = Output()
    dummy = DummyInput(False)
    output.inputs.append(dummy)
    output.eval()
    dummy.setValue(True)
    changed = output.eval()
    assert changed is True, "Output.eval() should return True when state changes from (0,1) to (1,1)."
    assert output.state["outValue"] == (1,1), "Output.state['outValue'] should be updated to (1,1)."
    dummy.setValue(False)
    changed = output.eval()
    assert changed is True, "Output.eval() should return True when state changes from (1,1) to (0,1)."
    assert output.state["outValue"] == (0,1), "Output.state['outValue'] should be updated to (0,1)."