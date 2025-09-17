import pytest
from src.model.Input import Input


def test_Input_eval_always_true():
    input = Input()
    assert input.eval() is True, "Input.eval() should always return True regardless of state."



def test_Input_set_state():
    input = Input()
    input.setState(True)
    assert input.state is True, "Input.state should be True after setState(True)."
    assert input.eval() is True, "Input.eval() should always return True."
    input.setState(False)
    assert input.state is False, "Input.state should be False after setState(False)."
    assert input.eval() is True, "Input.eval() should always return True."



def test_Input_toggle_state():
    input = Input()
    initial_state = input.state
    input.toggleState()
    assert input.state != initial_state, "Input.toggleState() should invert the state."
    assert input.eval() is True, "Input.eval() should always return True."
    input.toggleState()
    assert input.state == initial_state, "Input.toggleState() should invert the state back."
    assert input.eval() is True, "Input.eval() should always return True."