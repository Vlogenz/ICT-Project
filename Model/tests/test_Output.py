import pytest
from Model.Output import Output
from .DummyInput import DummyInput


def test_Output_state_changes_from_default():
    output = Output()
    dummy = DummyInput(True)
    output.inputs.append(dummy)
    # Initial state is False, so should change to True
    changed = output.eval()
    assert changed is True, "Output.eval() should return True when state changes."
    assert output.state["outValue"] is True, "Output.state['outValue'] should be updated to True."


def test_Output_state_does_not_change():
    output = Output()
    dummy = DummyInput(False)
    output.inputs.append(dummy)
    # First call: state changes from default to False (no change)
    output.eval()  # set initial state
    changed = output.eval()  # call again, should not change
    assert changed is False, "Output.eval() should return False when state does not change."
    assert output.state["outValue"] is False, "Output.state['outValue'] should remain False."

def test_Output_state_changes_multiple_times():
    output = Output()
    dummy = DummyInput(False)
    output.inputs.append(dummy)
    output.eval()  # set initial state to False
    # Change input to True
    dummy.state = True
    changed = output.eval()
    assert changed is True, "Output.eval() should return True when state changes from False to True."
    assert output.state["outValue"] is True, "Output.state['outValue'] should be updated to True."
    # Change input back to False
    dummy.state = False
    changed = output.eval()
    assert changed is True, "Output.eval() should return True when state changes from True to False."
    assert output.state["outValue"] is False, "Output.state['outValue'] should be updated to False."