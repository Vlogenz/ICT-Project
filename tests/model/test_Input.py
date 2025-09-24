import pytest
from src.model.Input import Input


def test_Input_eval_always_true():
    input = Input()
    assert input.eval() is True, "Input.eval() should always return True regardless of state."



def test_Input_set_state():
    input = Input()
    input.setState((1,1))
    assert input.state["outValue"] == (1,1), "Input.state['outValue'] should be (1,1) after setState((1,1))."
    assert input.eval() is True, "Input.eval() should always return True."
    input.setState((0,1))
    assert input.state["outValue"] == (0,1), "Input.state['outValue'] should be (0,1) after setState((0,1))."
    assert input.eval() is True, "Input.eval() should always return True."



def test_Input_toggle_state():
    input = Input()
    initial_state = input.state["outValue"]
    input.toggleState()
    assert input.state["outValue"] != initial_state, "Input.toggleState() should invert the state."
    assert input.eval() is True, "Input.eval() should always return True."
    input.toggleState()
    assert input.state["outValue"] == initial_state, "Input.toggleState() should invert the state back."
    assert input.eval() is True, "Input.eval() should always return True."