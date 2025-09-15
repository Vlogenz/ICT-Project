import pytest
from Model.Or import Or
from Model.LogicComponent import LogicComponent
        
class DummyInput(LogicComponent):
    def __init__(self, value):
        self._value = value
        self.inputs = []
        self.outputs = []
    def eval(self):
        return self._value

def test_or_raises_error_on_too_few_inputs():
    or_gate = Or()
    or_gate.inputs = [DummyInput(True)]
    with pytest.raises(ValueError):
        or_gate.eval()

def test_or_raises_error_on_too_many_inputs():
    or_gate = Or()
    or_gate.inputs = [DummyInput(True), DummyInput(False), DummyInput(True)]
    with pytest.raises(ValueError):
        or_gate.eval()

@pytest.mark.parametrize("a, b, expected", [
    (False, False, False),
    (False, True, True),
    (True, False, True),
    (True, True, True),
])
def test_or_logic(a, b, expected):
    or_gate = Or()
    or_gate.inputs = [DummyInput(a), DummyInput(b)]
    assert or_gate.eval() is expected

