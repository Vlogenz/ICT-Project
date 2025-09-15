import pytest
from Model.Output import Output
from Model.LogicComponent import LogicComponent

class DummyInput(LogicComponent):
    def __init__(self, value):
        self._value = value
        self.inputs = []
        self.outputs = []
    def eval(self):
        return self._value

def test_Output_returns_input_false():
    output = Output()
    dummy = DummyInput(False)
    output.inputs.append(dummy)
    assert output.eval() is False, "Output should return False when input eval() is False"

def test_Output_returns_input_true():
    output = Output()
    dummy = DummyInput(True)
    output.inputs.append(dummy)
    assert output.eval() is True, "Output should return True when input eval() is True"