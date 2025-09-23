import pytest
from src.model.FullAdder import FullAdder
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

@pytest.mark.parametrize("a, b, cin, expected_sum, expected_cout", [
    (False, False, False, False, False),
    (False, False, True, True, False),
    (False, True, False, True, False),
    (False, True, True, False, True),
    (True, False, False, True, False),
    (True, False, True, False, True),
    (True, True, False, False, True),
    (True, True, True, True, True),
])
def test_full_adder_logic(a, b, cin, expected_sum, expected_cout):
    getBus().setManual()
    fa = FullAdder()
    fa.addInput(DummyInput(a), "outValue", "A")
    fa.addInput(DummyInput(b), "outValue", "B")
    fa.addInput(DummyInput(cin), "outValue", "Cin")
    fa.eval()
    expected_sum_tuple = (1,1) if expected_sum else (0,1)
    expected_cout_tuple = (1,1) if expected_cout else (0,1)
    assert fa.state["Sum"] == expected_sum_tuple, f"FullAdder Sum should be {expected_sum_tuple} for inputs {a}, {b}, {cin}"
    assert fa.state["Cout"] == expected_cout_tuple, f"FullAdder Cout should be {expected_cout_tuple} for inputs {a}, {b}, {cin}"
