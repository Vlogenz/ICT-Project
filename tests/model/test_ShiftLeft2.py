import pytest
from src.model.ShiftLeft2 import ShiftLeft2
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


def test_shiftleft2_initialization():
    """Test that ShiftLeft2 initializes correctly."""
    shift_left = ShiftLeft2()
    assert "input1" in shift_left.inputs
    assert shift_left.inputs["input1"] is None
    assert shift_left.inputBitwidths["input1"] == 0
    assert shift_left.state["outValue"] == (0, 0)  # default state


def test_shiftleft2_no_input_connected():
    """Test that ShiftLeft2 handles no input connected (defaults to False/0)."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    changed = shift_left.eval()
    # Should output (False << 2, 0 + 2) = (0, 2) when no input is connected
    assert shift_left.state["outValue"] == (0, 2)
    assert changed is True  # state changed from default (0, 0) to (0, 2)
    
    # Second evaluation should not change state
    changed = shift_left.eval()
    assert changed is False


@pytest.mark.parametrize("input_value, input_bitwidth, expected_value, expected_bitwidth", [
    # Test various input values and bitwidths
    (0, 1, 0, 3),           # 0 << 2 = 0, bitwidth 1 + 2 = 3
    (1, 1, 4, 3),           # 1 << 2 = 4, bitwidth 1 + 2 = 3
    (2, 2, 8, 4),           # 2 << 2 = 8, bitwidth 2 + 2 = 4
    (3, 2, 12, 4),          # 3 << 2 = 12, bitwidth 2 + 2 = 4
    (5, 3, 20, 5),          # 5 << 2 = 20, bitwidth 3 + 2 = 5
    (7, 3, 28, 5),          # 7 << 2 = 28, bitwidth 3 + 2 = 5
    (15, 4, 60, 6),         # 15 << 2 = 60, bitwidth 4 + 2 = 6
    (255, 8, 1020, 10),     # 255 << 2 = 1020, bitwidth 8 + 2 = 10
    (1023, 10, 4092, 12),   # 1023 << 2 = 4092, bitwidth 10 + 2 = 12
])
def test_shiftleft2_with_various_inputs(input_value, input_bitwidth, expected_value, expected_bitwidth):
    """Test ShiftLeft2 with various input values and bitwidths."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input = DummyInput(input_value, input_bitwidth)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # Check that addInput correctly set the bitwidths
    assert shift_left.inputBitwidths["input1"] == input_bitwidth
    
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (expected_value, expected_bitwidth)
    
    # For input_value 0: addInput sets state to (0, bitwidth+2), eval calculates 0<<2=0 with same bitwidth
    # So state doesn't change during eval(), hence changed should be False
    if input_value == 0:
        assert changed is False  # state doesn't change during eval for zero input
    else:
        assert changed is True   # state should change from addInput state to eval result
    
    # Second evaluation should not change state
    changed = shift_left.eval()
    assert changed is False


def test_shiftleft2_bitwidth_handling():
    """Test that ShiftLeft2 correctly handles bitwidth calculations."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    
    # Test with different bitwidths
    test_cases = [
        (1, 1),    # 1-bit input should result in 3-bit output
        (8, 8),    # 8-bit input should result in 10-bit output
        (16, 16),  # 16-bit input should result in 18-bit output
        (32, 32),  # 32-bit input should result in 34-bit output
    ]
    
    for bitwidth, input_value in test_cases:
        shift_left = ShiftLeft2()  # Create new instance for each test
        dummy_input = DummyInput(input_value, bitwidth)
        shift_left.addInput(dummy_input, "outValue", "input1")
        
        # Check that input bitwidth is set correctly
        assert shift_left.inputBitwidths["input1"] == bitwidth
        
        # Check that output bitwidth is input bitwidth + 2
        shift_left.eval()
        assert shift_left.state["outValue"][1] == bitwidth + 2


def test_shiftleft2_addInput_updates_bitwidth():
    """Test that addInput correctly updates the bitwidth in the state."""
    shift_left = ShiftLeft2()
    
    # Initially, state should have bitwidth 0
    assert shift_left.state["outValue"][1] == 0
    
    # Add input with 8-bit width
    dummy_input = DummyInput(42, 8)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # State bitwidth should be updated to 8 + 2 = 10
    assert shift_left.state["outValue"][1] == 10
    assert shift_left.inputBitwidths["input1"] == 8


def test_shiftleft2_state_changes_with_input_changes():
    """Test that ShiftLeft2 state changes when input changes."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input = DummyInput(3, 4)  # 3 with 4-bit width
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # First evaluation: 3 << 2 = 12
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (12, 6)  # value=12, bitwidth=4+2=6
    assert changed is True
    
    # Change input value: 5 << 2 = 20
    dummy_input.setValue(5, 4)
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (20, 6)  # value=20, bitwidth=6
    assert changed is True
    
    # Change input value: 1 << 2 = 4
    dummy_input.setValue(1, 4)
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (4, 6)  # value=4, bitwidth=6
    assert changed is True
    
    # Set same value again - should not change
    dummy_input.setValue(1, 4)
    changed = shift_left.eval()
    assert changed is False


def test_shiftleft2_edge_cases():
    """Test ShiftLeft2 with edge case values."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input = DummyInput(0, 1)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # Test with zero
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (0, 3)  # 0 << 2 = 0, bitwidth = 1 + 2 = 3
    # For zero input, addInput already sets (0, 3), eval calculates 0<<2=0 with bitwidth 3, no change
    assert changed is False  
    
    # Test with maximum value for given bitwidth
    # For 3-bit input, maximum value is 7
    dummy_input.setValue(7, 3)
    shift_left.addInput(dummy_input, "outValue", "input1")  # Update bitwidth
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (28, 5)  # 7 << 2 = 28, bitwidth = 3 + 2 = 5
    assert changed is True


def test_shiftleft2_multiple_evaluations_same_input():
    """Test that multiple evaluations with same input don't change state."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input = DummyInput(6, 4)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # First evaluation should change state
    changed = shift_left.eval()
    assert changed is True
    assert shift_left.state["outValue"] == (24, 6)  # 6 << 2 = 24, bitwidth = 4 + 2 = 6
    
    # Subsequent evaluations should not change state
    for _ in range(3):
        changed = shift_left.eval()
        assert changed is False
        assert shift_left.state["outValue"] == (24, 6)


def test_shiftleft2_input_disconnection():
    """Test behavior when input is disconnected."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input = DummyInput(10, 5)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # With input connected: 10 << 2 = 40
    shift_left.eval()
    assert shift_left.state["outValue"] == (40, 7)  # bitwidth = 5 + 2 = 7
    
    # Simulate input disconnection
    shift_left.inputs["input1"] = None
    changed = shift_left.eval()
    # Should shift False (0) by 2: 0 << 2 = 0, but bitwidth stays as it was set by addInput
    assert shift_left.state["outValue"] == (0, 7)
    assert changed is True  # state changed


def test_shiftleft2_preserves_shift_operation():
    """Test that ShiftLeft2 correctly performs left shift by 2 operation."""
    getBus().setManual()
    
    # Test cases: (input, expected_output_after_shift_left_2)
    test_cases = [
        (1, 4),     # 1 << 2 = 4
        (2, 8),     # 2 << 2 = 8
        (3, 12),    # 3 << 2 = 12
        (4, 16),    # 4 << 2 = 16
        (10, 40),   # 10 << 2 = 40
        (15, 60),   # 15 << 2 = 60
    ]
    
    for input_val, expected_output in test_cases:
        shift_left = ShiftLeft2()
        # Use appropriate bitwidth to fit the input value
        bitwidth = max(1, input_val.bit_length())
        dummy_input = DummyInput(input_val, bitwidth)
        shift_left.addInput(dummy_input, "outValue", "input1")
        
        shift_left.eval()
        actual_output = shift_left.state["outValue"][0]
        assert actual_output == expected_output, f"Input {input_val} should produce {expected_output}, got {actual_output}"


def test_shiftleft2_bitwidth_consistency():
    """Test that bitwidth handling is consistent throughout operations."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    
    # Start with 4-bit input
    dummy_input = DummyInput(5, 4)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # Input bitwidth should be 4
    assert shift_left.inputBitwidths["input1"] == 4
    
    # Output bitwidth should be 4 + 2 = 6
    shift_left.eval()
    assert shift_left.state["outValue"][1] == 6
    
    # Change value but keep same bitwidth
    dummy_input.setValue(3, 4)
    shift_left.eval()
    assert shift_left.state["outValue"] == (12, 6)  # 3 << 2 = 12, bitwidth still 6
    assert shift_left.inputBitwidths["input1"] == 4  # Input bitwidth unchanged


def test_shiftleft2_removeInput_resets_bitwidths():
    """Test that removeInput correctly resets the input bitwidths to default values."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input = DummyInput(10, 8)
    
    # Add input with 8-bit width
    shift_left.addInput(dummy_input, "outValue", "input1")
    assert shift_left.inputBitwidths["input1"] == 8
    shift_left.eval()
    assert shift_left.state["outValue"] == (40, 10)  # 10 << 2 = 40, bitwidth = 8 + 2 = 10
    
    # Remove the input
    shift_left.removeInput(dummy_input, "outValue", "input1")
    
    # Check that input bitwidth is reset to default value
    assert shift_left.inputBitwidths["input1"] == 0  # Reset to default
    assert shift_left.inputs["input1"] is None       # Input should be None
    
    # After eval(), state should be calculated as: (False<<2, 0+2) = (0, 2)
    shift_left.eval()
    assert shift_left.state["outValue"] == (0, 2)    # State calculated by eval()


def test_shiftleft2_removeInput_then_addInput():
    """Test behavior when removing input and then adding a new one."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    
    # First input
    dummy_input1 = DummyInput(5, 4)
    shift_left.addInput(dummy_input1, "outValue", "input1")
    shift_left.eval()
    assert shift_left.state["outValue"] == (20, 6)  # 5 << 2 = 20, bitwidth = 4 + 2 = 6
    
    # Remove first input
    shift_left.removeInput(dummy_input1, "outValue", "input1")
    assert shift_left.inputBitwidths["input1"] == 0
    # After eval, state should be (0, 2) since no input connected
    shift_left.eval()
    assert shift_left.state["outValue"] == (0, 2)
    
    # Add second input with different bitwidth
    dummy_input2 = DummyInput(3, 2)
    shift_left.addInput(dummy_input2, "outValue", "input1")
    assert shift_left.inputBitwidths["input1"] == 2
    shift_left.eval()
    assert shift_left.state["outValue"] == (12, 4)  # 3 << 2 = 12, bitwidth = 2 + 2 = 4


def test_shiftleft2_removeInput_error_handling():
    """Test that removeInput properly handles error cases."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input1 = DummyInput(5, 4)
    dummy_input2 = DummyInput(3, 2)
    
    # Add input1
    shift_left.addInput(dummy_input1, "outValue", "input1")
    
    # Try to remove wrong input - should raise KeyError
    with pytest.raises(KeyError):
        shift_left.removeInput(dummy_input2, "outValue", "input1")
    
    # Try to remove with wrong key - should raise KeyError  
    with pytest.raises(KeyError):
        shift_left.removeInput(dummy_input1, "wrongKey", "input1")
    
    # Try to remove with wrong internal key - should raise KeyError
    with pytest.raises(KeyError):
        shift_left.removeInput(dummy_input1, "outValue", "wrongInternalKey")
    
    # Correct removal should work
    shift_left.removeInput(dummy_input1, "outValue", "input1")
    assert shift_left.inputs["input1"] is None
