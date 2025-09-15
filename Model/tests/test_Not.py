import pytest
from Model.Not import Not
from Model.LogicComponent import LogicComponent
        
class DummyInput(LogicComponent):
    def __init__(self, value):
        self._value = value
        self.inputs = []
        self.outputs = []
    def eval(self):
        return self._value

def test_not_raises_error_on_too_few_inputs():
    not_gate = Not()
    not_gate.inputs = []
    with pytest.raises(ValueError):
        not_gate.eval()

def test_not_raises_error_on_too_many_inputs():
    not_gate = Not()
    not_gate.inputs = [DummyInput(True), DummyInput(False)]
    with pytest.raises(ValueError):
        not_gate.eval()

@pytest.mark.parametrize("a, expected", [
    (False, True),
    (True, False),
])
def test_not_logic(a, expected):
    not_gate = Not()
    not_gate.inputs = [DummyInput(a)]
    assert not_gate.eval() is expected
