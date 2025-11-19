import pytest
from src.model.Output import Output
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


def test_Output_state_changes_from_default():
    getBus().setManual()
    output = Output()
    dummy = DummyInput(True)
    output.addInput(dummy,"outValue","input")
    changed = output.eval()
    assert changed is True, "Output.eval() should return True when state changes."
    assert output.state["outValue"] == (1,1), "Output.state['outValue'] should be updated to (1,1)."


def test_Output_state_does_not_change():
    getBus().setManual()
    output = Output()
    dummy = DummyInput(False)
    output.addInput(dummy,"outValue","input")
    output.eval()
    changed = output.eval()
    assert changed is False, "Output.eval() should return False when state does not change."
    assert output.state["outValue"] == (0,1), "Output.state['outValue'] should remain (0,1)."

def test_Output_state_changes_multiple_times():
    getBus().setManual()
    output = Output()
    dummy = DummyInput(False)
    output.addInput(dummy,"outValue","input")
    output.eval()
    dummy.setValue(True)
    changed = output.eval()
    assert changed is True, "Output.eval() should return True when state changes from (0,1) to (1,1)."
    assert output.state["outValue"] == (1,1), "Output.state['outValue'] should be updated to (1,1)."
    dummy.setValue(False)
    changed = output.eval()
    assert changed is True, "Output.eval() should return True when state changes from (1,1) to (0,1)."
    assert output.state["outValue"] == (0,1), "Output.state['outValue'] should be updated to (0,1)."
    

def test_different_bitwidth_input():
    getBus().setManual()
    output = Output()
    dummy = DummyInput(4, bitwidth=4)
    output.addInput(dummy,"outValue","input")
    output.eval()
    assert output.inputBitwidths["input"] == 4, "Output.inputBitwidths['input'] should match DummyInput's bitwidth."
    
def test_remove_input_resets_bitwidth():
    getBus().setManual()
    output = Output()
    dummy = DummyInput(4, bitwidth=4)
    output.addInput(dummy,"outValue","input")
    output.eval()
    output.removeInput(dummy,"outValue","input")
    assert output.inputBitwidths["input"] == 0, "Output.inputBitwidths['input'] should be reset to 0 after removing input."