import pytest
from src.model.HalfAdder import HalfAdder
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus

@pytest.mark.parametrize("a, b, expected_sum, expected_carry", [
    (False, False, False, False),
    (False, True, True, False),
    (True, False, True, False),
    (True, True, False, True),
])
def test_half_adder_logic(a, b, expected_sum, expected_carry):
    getBus().setManual()
    ha = HalfAdder()
    ha.addInput(DummyInput(a), "outValue", "inputA")
    ha.addInput(DummyInput(b), "outValue", "inputB")
    ha.eval()
    expected_sum_tuple = (1,1) if expected_sum else (0,1)
    expected_carry_tuple = (1,1) if expected_carry else (0,1)
    assert ha.state["sum"] == expected_sum_tuple, f"HalfAdder sum should be {expected_sum_tuple} for inputs {a}, {b}"
    assert ha.state["carry"] == expected_carry_tuple, f"HalfAdder carry should be {expected_carry_tuple} for inputs {a}, {b}"