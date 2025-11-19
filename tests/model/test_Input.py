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

def test_Input_bitwidth_cycle():
    input = Input()
    input.cycleBitwidth()
    assert input.state["outValue"][1] == 8
    input.cycleBitwidth()
    assert input.state["outValue"][1] == 32

def test_Input_limits_values_by_bitwidth():
    input8 = Input()
    input32 = Input()
    bigVal = 782653

    input8.cycleBitwidth()
    input32.cycleBitwidth()
    input32.cycleBitwidth()

    input8.enteredState(bigVal)
    input32.enteredState(bigVal)

    assert input8.state["outValue"][0] == 255
    assert input32.state["outValue"][0] == bigVal

def test_Input_cycling_bitwidth_resets_value():
    input = Input()
    input.cycleBitwidth()
    input.cycleBitwidth()

    input.enteredState(500) 
    assert input.state["outValue"][0] == 500

    input.cycleBitwidth()
    assert input.state["outValue"][0] == 0