import pytest
from src.model.Splitter8to1 import Splitter8to1
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


class TestSplitter8to1:
    """Comprehensive tests for Splitter8to1 component covering all edge cases - reverse of Collector tests."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        getBus().setManual()
        self.splitter = Splitter8to1()

    def test_splitter_initialization(self):
        """Test that Splitter8to1 initializes correctly."""
        assert len(self.splitter.inputs) == 1
        assert self.splitter.inputs["input1"] is None
        assert self.splitter.inputBitwidths["input1"] == 8
        # Check all 8 outputs are initialized to (0,1)
        for i in range(8):
            assert self.splitter.state[f"outValue{2**i}"] == (0, 1)

    def test_splitter_no_input_connected(self):
        """Test splitter behavior when no input is connected."""
        changed = self.splitter.eval()
        # All outputs should be (0,1)
        for i in range(8):
            assert self.splitter.state[f"outValue{2**i}"] == (0, 1)
        assert changed is False  # No change from initial state

    def test_splitter_single_bit_values(self):
        """Test splitter with single bit values (reverse of collector single input)."""
        for bit_position in range(8):
            splitter = Splitter8to1()
            input_value = 1 << bit_position  # Set only one bit
            splitter.addInput(DummyInput(input_value, 8), "outValue", "input1")
            changed = splitter.eval()
            
            # Check that only the corresponding output is high
            for i in range(8):
                if i == bit_position:  # bit_position is 0-indexed, outputs are powers of two
                    assert splitter.state[f"outValue{2**i}"] == (1, 1)
                else:
                    assert splitter.state[f"outValue{2**i}"] == (0, 1)
            assert changed is True

    def test_splitter_all_outputs_high(self):
        """Test splitter when input has all bits set (reverse of collector all inputs high)."""
        input_value = 0b11111111  # All 8 bits set (255)
        self.splitter.addInput(DummyInput(input_value, 8), "outValue", "input1")
        
        changed = self.splitter.eval()
        # All outputs should be (1,1)
        for i in range(8):
            assert self.splitter.state[f"outValue{2**i}"] == (1, 1)
        assert changed is True

    def test_splitter_all_outputs_low(self):
        """Test splitter when input is zero (reverse of collector all inputs low)."""
        input_value = 0b00000000  # All bits clear (0)
        self.splitter.addInput(DummyInput(input_value, 8), "outValue", "input1")
        
        changed = self.splitter.eval()
        # All outputs should be (0,1)
        for i in range(8):
            assert self.splitter.state[f"outValue{2**i}"] == (0, 1)
        assert changed is False  # No change from initial state

    @pytest.mark.parametrize("pattern", [
        0b10101010,
        0b01010101,
        0b11110000,
        0b00001111,
        0b10000001,
        0b01111110,
        0b11111111,
        0b00000001,
        0b10000000,
        0b00010000,
    ])
    def test_splitter_bit_patterns(self, pattern):
        """Test splitter with various bit patterns (reverse of collector bit patterns)."""
        splitter = Splitter8to1()
        splitter.addInput(DummyInput(pattern, 8), "outValue", "input1")
        
        changed = splitter.eval()
        
        # Check each output matches the corresponding bit in the pattern
        for i in range(8):
            expected_bit = (pattern >> i) & 1
            expected_output = (expected_bit, 1)
            assert splitter.state[f"outValue{2**i}"] == expected_output
        assert changed is True

    def test_splitter_partial_bit_pattern(self):
        """Test splitter with partial bit pattern (reverse of mixed connected/disconnected)."""
        # Set bits at positions 1, 3, 5, 7 (0-indexed), which corresponds to outputs 2, 4, 6, 8
        input_value = 0b10101010
        self.splitter.addInput(DummyInput(input_value, 8), "outValue", "input1")
        
        changed = self.splitter.eval()
        
        # Check outputs: 2, 4, 6, 8 should be high, others low
        expected_outputs = {
            1: (0, 1), 2: (1, 1), 3: (0, 1), 4: (1, 1),
            5: (0, 1), 6: (1, 1), 7: (0, 1), 8: (1, 1)
        }
        
        for i in range(8):
            assert self.splitter.state[f"outValue{2**i}"] == expected_outputs[i+1]
        assert changed is True

    def test_splitter_state_change_detection(self):
        """Test that eval() correctly detects state changes."""
        # Initial evaluation with no input
        changed = self.splitter.eval()
        assert changed is False  # No change from initial state
        
        # Add an input and evaluate
        self.splitter.addInput(DummyInput(1, 8), "outValue", "input1")
        changed = self.splitter.eval()
        assert changed is True
        assert self.splitter.state["outValue1"] == (1, 1)
        for i in range(1,8):
            assert self.splitter.state[f"outValue{2**i}"] == (0, 1)
        
        # Evaluate again without changes
        changed = self.splitter.eval()
        assert changed is False  # No change from previous state

    def test_splitter_input_overwrite_behavior(self):
        """Test behavior when trying to overwrite existing input connection."""
        dummy1 = DummyInput(1, 8)
        dummy2 = DummyInput(255, 8)
        
        # Add first input
        success1 = self.splitter.addInput(dummy1, "outValue", "input1")
        assert success1 is True
        
        # Try to overwrite the same input
        success2 = self.splitter.addInput(dummy2, "outValue", "input1")
        assert success2 is False  # Should fail
        
        # Verify original input is still connected
        self.splitter.eval()
        assert self.splitter.state["outValue1"] == (1, 1)
        for i in range(1,8):
            assert self.splitter.state[f"outValue{2**i}"] == (0, 1)

    def test_splitter_invalid_input_keys(self):
        """Test splitter behavior with invalid input keys."""
        dummy = DummyInput(1, 8)
        
        # Try to add input with invalid key
        with pytest.raises(KeyError):
            self.splitter.addInput(dummy, "outValue", "invalid_input")
