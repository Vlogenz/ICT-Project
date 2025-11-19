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
    # Should output (0, 0) when no input is connected (bitwidth stays 0)
    assert shift_left.state["outValue"] == (0, 0)
    assert changed is False  # state doesn't change from default (0, 0)
    
    # Second evaluation should not change state
    changed = shift_left.eval()
    assert changed is False


@pytest.mark.parametrize("input_value, input_bitwidth, expected_value, expected_bitwidth", [
    # Test various input values and bitwidths - now bitwidth stays the same
    # The shift left by 2 cuts off the top 2 bits
    (0, 1, 0, 1),           # 0 << 2 = 0, masked to 1 bit = 0, bitwidth stays 1
    (1, 1, 0, 1),           # 1 << 2 = 4 (100 in binary), masked to 1 bit = 0, bitwidth stays 1
    (0, 2, 0, 2),           # 0 << 2 = 0, masked to 2 bits = 0, bitwidth stays 2
    (1, 2, 0, 2),           # 1 << 2 = 4 (100), masked to 2 bits = 0, bitwidth stays 2
    (2, 2, 0, 2),           # 2 << 2 = 8 (1000), masked to 2 bits = 0, bitwidth stays 2
    (3, 2, 0, 2),           # 3 << 2 = 12 (1100), masked to 2 bits = 0, bitwidth stays 2
    (5, 3, 4, 3),           # 5 (101) << 2 = 20 (10100), masked to 3 bits = 4 (100), bitwidth stays 3
    (7, 3, 4, 3),           # 7 (111) << 2 = 28 (11100), masked to 3 bits = 4 (100), bitwidth stays 3
    (10, 4, 8, 4),          # 10 (1010) << 2 = 40 (101000), masked to 4 bits = 8 (1000), bitwidth stays 4
    (15, 4, 12, 4),         # 15 (1111) << 2 = 60 (111100), masked to 4 bits = 12 (1100), bitwidth stays 4
    (255, 8, 252, 8),       # 255 << 2 = 1020, masked to 8 bits = 252, bitwidth stays 8
    (1023, 10, 1020, 10),   # 1023 << 2 = 4092, masked to 10 bits = 1020, bitwidth stays 10
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
    
    # addInput sets state to (0, bitwidth) initially (keeps existing value which is 0)
    # eval calculates (input_value<<2)&mask
    # So state changes only if the result is different from 0
    if expected_value == 0:
        assert changed is False  # state stays (0, bitwidth)
    else:
        assert changed is True   # state changes from (0, bitwidth) to (expected_value, bitwidth)
    
    # Second evaluation should not change state
    changed = shift_left.eval()
    assert changed is False


def test_shiftleft2_bitwidth_handling():
    """Test that ShiftLeft2 correctly handles bitwidth calculations."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    
    # Test with different bitwidths - output bitwidth should equal input bitwidth
    test_cases = [
        (1, 1),    # 1-bit input should result in 1-bit output
        (8, 8),    # 8-bit input should result in 8-bit output
        (16, 16),  # 16-bit input should result in 16-bit output
        (32, 32),  # 32-bit input should result in 32-bit output
    ]
    
    for bitwidth, input_value in test_cases:
        shift_left = ShiftLeft2()  # Create new instance for each test
        dummy_input = DummyInput(input_value, bitwidth)
        shift_left.addInput(dummy_input, "outValue", "input1")
        
        # Check that input bitwidth is set correctly
        assert shift_left.inputBitwidths["input1"] == bitwidth
        
        # Check that output bitwidth equals input bitwidth (no extension)
        shift_left.eval()
        assert shift_left.state["outValue"][1] == bitwidth


def test_shiftleft2_addInput_updates_bitwidth():
    """Test that addInput correctly updates the bitwidth in the state."""
    shift_left = ShiftLeft2()
    
    # Initially, state should have bitwidth 0
    assert shift_left.state["outValue"][1] == 0
    
    # Add input with 8-bit width
    dummy_input = DummyInput(42, 8)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # State bitwidth should remain 8 (not extended)
    assert shift_left.state["outValue"][1] == 8
    assert shift_left.inputBitwidths["input1"] == 8


def test_shiftleft2_state_changes_with_input_changes():
    """Test that ShiftLeft2 state changes when input changes."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input = DummyInput(3, 4)  # 3 with 4-bit width
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # First evaluation: 3 (0011) << 2 = 12 (1100), masked to 4 bits = 12
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (12, 4)  # value=12, bitwidth=4
    assert changed is True
    
    # Change input value: 5 (0101) << 2 = 20 (10100), masked to 4 bits = 4 (0100)
    dummy_input.setValue(5, 4)
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (4, 4)  # value=4, bitwidth=4
    assert changed is True
    
    # Change input value: 1 (0001) << 2 = 4 (0100), masked to 4 bits = 4
    dummy_input.setValue(1, 4)
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (4, 4)  # value=4, bitwidth=4
    assert changed is False  # No change because result is still 4
    
    # Set different value: 2 (0010) << 2 = 8 (1000), masked to 4 bits = 8
    dummy_input.setValue(2, 4)
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (8, 4)  # value=8, bitwidth=4
    assert changed is True


def test_shiftleft2_edge_cases():
    """Test ShiftLeft2 with edge case values."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input = DummyInput(0, 1)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # Test with zero
    changed = shift_left.eval()
    assert shift_left.state["outValue"] == (0, 1)  # 0 << 2 = 0, bitwidth stays 1
    # For zero input, addInput already sets (0, 1), eval calculates 0<<2=0 with bitwidth 1, no change
    assert changed is False  
    
    # Test with maximum value for given bitwidth
    # For 3-bit input, maximum value is 7 (111)
    dummy_input.setValue(7, 3)
    shift_left.addInput(dummy_input, "outValue", "input1")  # Update bitwidth
    changed = shift_left.eval()
    # 7 (111) << 2 = 28 (11100), masked to 3 bits = 4 (100)
    assert shift_left.state["outValue"] == (4, 3)  # bitwidth stays 3
    assert changed is True


def test_shiftleft2_multiple_evaluations_same_input():
    """Test that multiple evaluations with same input don't change state."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input = DummyInput(6, 4)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # First evaluation should change state
    # 6 (0110) << 2 = 24 (11000), masked to 4 bits = 8 (1000)
    changed = shift_left.eval()
    assert changed is True
    assert shift_left.state["outValue"] == (8, 4)  # value=8, bitwidth stays 4
    
    # Subsequent evaluations should not change state
    for _ in range(3):
        changed = shift_left.eval()
        assert changed is False
        assert shift_left.state["outValue"] == (8, 4)


def test_shiftleft2_input_disconnection():
    """Test behavior when input is disconnected."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    dummy_input = DummyInput(10, 5)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # With input connected: 10 (01010) << 2 = 40 (101000), masked to 5 bits = 8 (01000)
    shift_left.eval()
    assert shift_left.state["outValue"] == (8, 5)  # bitwidth stays 5
    
    # Simulate input disconnection
    shift_left.inputs["input1"] = None
    changed = shift_left.eval()
    # Should shift False (0) by 2: 0 << 2 = 0, bitwidth stays as it was set by addInput
    assert shift_left.state["outValue"] == (0, 5)
    assert changed is True  # state changed


def test_shiftleft2_preserves_shift_operation():
    """Test that ShiftLeft2 correctly performs left shift by 2 operation with masking."""
    getBus().setManual()
    
    # Test cases: (input, bitwidth, expected_output_after_shift_and_mask)
    # Now we need to consider that the output is masked to the original bitwidth
    test_cases = [
        (1, 4, 4),      # 1 (0001) << 2 = 4 (0100), masked to 4 bits = 4
        (2, 4, 8),      # 2 (0010) << 2 = 8 (1000), masked to 4 bits = 8
        (3, 4, 12),     # 3 (0011) << 2 = 12 (1100), masked to 4 bits = 12
        (4, 4, 0),      # 4 (0100) << 2 = 16 (10000), masked to 4 bits = 0
        (10, 5, 8),     # 10 (01010) << 2 = 40 (101000), masked to 5 bits = 8 (01000)
        (15, 5, 28),    # 15 (01111) << 2 = 60 (111100), masked to 5 bits = 28 (11100)
    ]
    
    for input_val, bitwidth, expected_output in test_cases:
        shift_left = ShiftLeft2()
        dummy_input = DummyInput(input_val, bitwidth)
        shift_left.addInput(dummy_input, "outValue", "input1")
        
        shift_left.eval()
        actual_output = shift_left.state["outValue"][0]
        assert actual_output == expected_output, f"Input {input_val} (bitwidth {bitwidth}) should produce {expected_output}, got {actual_output}"


def test_shiftleft2_bitwidth_consistency():
    """Test that bitwidth handling is consistent throughout operations."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    
    # Start with 4-bit input
    dummy_input = DummyInput(5, 4)
    shift_left.addInput(dummy_input, "outValue", "input1")
    
    # Input bitwidth should be 4
    assert shift_left.inputBitwidths["input1"] == 4
    
    # Output bitwidth should stay 4
    shift_left.eval()
    assert shift_left.state["outValue"][1] == 4
    
    # Change value but keep same bitwidth
    dummy_input.setValue(3, 4)
    shift_left.eval()
    # 3 (0011) << 2 = 12 (1100), masked to 4 bits = 12
    assert shift_left.state["outValue"] == (12, 4)  # 3 << 2 = 12, bitwidth still 4
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
    # 10 (00001010) << 2 = 40 (00101000), masked to 8 bits = 40
    assert shift_left.state["outValue"] == (40, 8)  # 10 << 2 = 40, bitwidth stays 8
    
    # Remove the input
    shift_left.removeInput(dummy_input, "outValue", "input1")
    
    # Check that input bitwidth is reset to default value
    assert shift_left.inputBitwidths["input1"] == 0  # Reset to default
    assert shift_left.inputs["input1"] is None       # Input should be None
    
    # After eval(), state should be calculated as: (False<<2, 0) = (0, 0)
    shift_left.eval()
    assert shift_left.state["outValue"] == (0, 0)    # State calculated by eval()


def test_shiftleft2_removeInput_then_addInput():
    """Test behavior when removing input and then adding a new one."""
    getBus().setManual()
    shift_left = ShiftLeft2()
    
    # First input
    dummy_input1 = DummyInput(5, 4)
    shift_left.addInput(dummy_input1, "outValue", "input1")
    shift_left.eval()
    # 5 (0101) << 2 = 20 (10100), masked to 4 bits = 4 (0100)
    assert shift_left.state["outValue"] == (4, 4)  # value=4, bitwidth stays 4
    
    # Remove first input
    shift_left.removeInput(dummy_input1, "outValue", "input1")
    assert shift_left.inputBitwidths["input1"] == 0
    # After eval, state should be (0, 0) since no input connected
    shift_left.eval()
    assert shift_left.state["outValue"] == (0, 0)
    
    # Add second input with different bitwidth
    dummy_input2 = DummyInput(3, 2)
    shift_left.addInput(dummy_input2, "outValue", "input1")
    assert shift_left.inputBitwidths["input1"] == 2
    shift_left.eval()
    # 3 (11) << 2 = 12 (1100), masked to 2 bits = 0 (00)
    assert shift_left.state["outValue"] == (0, 2)  # value=0, bitwidth stays 2


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
