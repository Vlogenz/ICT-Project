import pytest
from src.model.SignExtend import SignExtend
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


def test_signextend_initialization():
    """Test that SignExtend initializes correctly."""
    sign_extend = SignExtend()
    assert "input1" in sign_extend.inputs
    assert sign_extend.inputs["input1"] is None
    assert sign_extend.inputBitwidths["input1"] == 16
    assert sign_extend.state["outValue"] == (0, 1)  # default state


def test_signextend_no_input_connected():
    """Test that SignExtend handles no input connected (defaults to False/0)."""
    getBus().setManual()
    sign_extend = SignExtend()
    changed = sign_extend.eval()
    # Should output (False, 32) which is (0, 32) when no input is connected
    assert sign_extend.state["outValue"] == (0, 32)
    assert changed is True  # state changed from default (0, 1) to (0, 32)
    
    # Second evaluation should not change state
    changed = sign_extend.eval()
    assert changed is False


@pytest.mark.parametrize("input_value, bitwidth, expected_output", [
    # Positive numbers (MSB = 0) should remain unchanged
    (0, 16, 0),           # Zero
    (1, 16, 1),           # Small positive
    (0x7FFF, 16, 0x7FFF), # Maximum positive 16-bit (32767)
    
    # Negative numbers (MSB = 1) should be sign-extended
    # Note: In two's complement, negative numbers have MSB = 1
    (0x8000, 16, 0x8000),  # -32768 (minimum negative 16-bit)
    (0xFFFF, 16, 0xFFFF),  # -1 in two's complement
    (0xFFFE, 16, 0xFFFE),  # -2 in two's complement
])
def test_signextend_with_various_inputs(input_value, bitwidth, expected_output):
    """Test SignExtend with various input values."""
    getBus().setManual()
    sign_extend = SignExtend()
    dummy_input = DummyInput(input_value, bitwidth)
    sign_extend.addInput(dummy_input, "outValue", "input1")
    
    changed = sign_extend.eval()
    assert sign_extend.state["outValue"] == (expected_output, 32)
    assert changed is True  # state should change from default
    
    # Second evaluation should not change state
    changed = sign_extend.eval()
    assert changed is False


def test_signextend_state_changes_with_input_changes():
    """Test that SignExtend state changes when input changes."""
    getBus().setManual()
    sign_extend = SignExtend()
    dummy_input = DummyInput(0x1234, 16)  # Positive number
    sign_extend.addInput(dummy_input, "outValue", "input1")
    
    # First evaluation
    changed = sign_extend.eval()
    assert sign_extend.state["outValue"] == (0x1234, 32)
    assert changed is True
    
    # Change input to a different positive number
    dummy_input.setValue(0x5678, 16)
    changed = sign_extend.eval()
    assert sign_extend.state["outValue"] == (0x5678, 32)
    assert changed is True
    
    # Change input to a negative number (MSB = 1)
    dummy_input.setValue(0x8001, 16)  # -32767 in two's complement
    changed = sign_extend.eval()
    assert sign_extend.state["outValue"] == (0x8001, 32)
    assert changed is True
    
    # Set same value again - should not change
    dummy_input.setValue(0x8001, 16)
    changed = sign_extend.eval()
    assert changed is False


def test_signextend_handles_edge_cases():
    """Test SignExtend with edge case values."""
    getBus().setManual()
    sign_extend = SignExtend()
    dummy_input = DummyInput(0, 16)
    sign_extend.addInput(dummy_input, "outValue", "input1")
    
    # Test with zero
    changed = sign_extend.eval()
    assert sign_extend.state["outValue"] == (0, 32)
    assert changed is True
    
    # Test with maximum positive 16-bit value
    dummy_input.setValue(0x7FFF, 16)
    changed = sign_extend.eval()
    assert sign_extend.state["outValue"] == (0x7FFF, 32)
    assert changed is True
    
    # Test with minimum negative 16-bit value (MSB = 1)
    dummy_input.setValue(0x8000, 16)
    changed = sign_extend.eval()
    assert sign_extend.state["outValue"] == (0x8000, 32)
    assert changed is True


def test_signextend_preserves_input_bitwidth_requirement():
    """Test that SignExtend expects 16-bit input as specified in inputBitwidths."""
    sign_extend = SignExtend()
    assert sign_extend.inputBitwidths["input1"] == 16


def test_signextend_multiple_evaluations_same_input():
    """Test that multiple evaluations with same input don't change state."""
    getBus().setManual()
    sign_extend = SignExtend()
    dummy_input = DummyInput(0xABCD, 16)
    sign_extend.addInput(dummy_input, "outValue", "input1")
    
    # First evaluation should change state
    changed = sign_extend.eval()
    assert changed is True
    assert sign_extend.state["outValue"] == (0xABCD, 32)
    
    # Subsequent evaluations should not change state
    for _ in range(3):
        changed = sign_extend.eval()
        assert changed is False
        assert sign_extend.state["outValue"] == (0xABCD, 32)


def test_signextend_input_disconnection():
    """Test behavior when input is disconnected."""
    getBus().setManual()
    sign_extend = SignExtend()
    dummy_input = DummyInput(0x1234, 16)
    sign_extend.addInput(dummy_input, "outValue", "input1")
    
    # With input connected
    sign_extend.eval()
    assert sign_extend.state["outValue"] == (0x1234, 32)
    
    # Simulate input disconnection
    sign_extend.inputs["input1"] = None
    changed = sign_extend.eval()
    assert sign_extend.state["outValue"] == (0, 32)  # Should default to False/0
    assert changed is True  # state changed
