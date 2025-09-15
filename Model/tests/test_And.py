import pytest
from Model.And import And
from Model.LogicComponent import LogicComponent
        
class DummyInput(LogicComponent):
    def __init__(self, value):
        self._value = value
        self.inputs = []
        self.outputs = []
    def eval(self):
        return self._value

def test_and_raises_error_on_too_few_inputs():
    and_gate = And()
    and_gate.inputs = [DummyInput(True)]
    with pytest.raises(ValueError):
        and_gate.eval()

def test_and_raises_error_on_too_many_inputs():
    and_gate = And()
    and_gate.inputs = [DummyInput(True), DummyInput(False), DummyInput(True)]
    with pytest.raises(ValueError):
        and_gate.eval()

@pytest.mark.parametrize("a, b, expected", [
    (False, False, False),
    (False, True, False),
    (True, False, False),
    (True, True, True),
])
def test_and_logic(a, b, expected):
    and_gate = And()
    and_gate.inputs = [DummyInput(a), DummyInput(b)]
    assert and_gate.eval() is expected

