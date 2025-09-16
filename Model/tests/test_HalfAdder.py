import pytest
from Model.HalfAdder import HalfAdder
from .DummyInput import DummyInput

@pytest.mark.parametrize("a, b, expected_sum, expected_carry", [
    (False, False, False, False),
    (False, True, True, False),
    (True, False, True, False),
    (True, True, False, True),
])
def test_half_adder_logic(a, b, expected_sum, expected_carry):
    ha = HalfAdder()
    ha.inputs = [DummyInput(a), DummyInput(b)]
    ha.eval()
    assert ha.state["sum"] == expected_sum, f"HalfAdder sum should be {expected_sum} for inputs {a}, {b}"
    assert ha.state["carry"] == expected_carry, f"HalfAdder carry should be {expected_carry} for inputs {a}, {b}"