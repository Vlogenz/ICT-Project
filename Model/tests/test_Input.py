import pytest
from Model.Input import Input

def test_Default():
    input = Input()
    assert input.eval() is False, "Default state should be False"


def test_SetState():
    input = Input()
    input.state = True
    assert input.eval() is True, "State should return True after being set to True"
    input.state = False
    assert input.eval() is False, "State should return False after being set to False"


def test_ToggleState():
    input = Input()
    
    # Toggle from False to True
    input.toggleState()
    assert input.eval() is True

    # Toggle back to False
    input.toggleState()
    assert input.eval() is False