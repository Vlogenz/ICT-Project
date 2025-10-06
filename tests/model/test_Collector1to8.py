import pytest
from src.model.Collector1to8 import Collector1to8
from .DummyInput import DummyInput
from src.infrastructure.eventBus import getBus


class TestCollector1to8:
    """Comprehensive tests for Collector1to8 component covering all edge cases."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        getBus().setManual()
        self.collector = Collector1to8()

    def test_collector_initialization(self):
        """Test that Collector1to8 initializes correctly."""
        assert len(self.collector.inputs) == 8
        assert all(self.collector.inputs[f"input{i}"] is None for i in range(1, 9))
        assert all(self.collector.inputBitwidths[f"input{i}"] == 1 for i in range(1, 9))
        assert self.collector.state["outValue"] == (0, 8)

    def test_collector_no_inputs_connected(self):
        """Test collector behavior when no inputs are connected."""
        changed = self.collector.eval()
        assert self.collector.state["outValue"] == (0, 8)
        assert changed is False  # No change from initial state

    def test_collector_single_input_connected(self):
        """Test collector with only one input connected."""
        for i in range(1, 9):
            collector = Collector1to8()
            collector.addInput(DummyInput(1), "outValue", f"input{i}")
            changed = collector.eval()
            expected_value = 1 << (i - 1)  # Bit position i-1
            assert collector.state["outValue"] == (expected_value, 8)
            assert changed is True

    def test_collector_all_inputs_high(self):
        """Test collector when all inputs are high (1)."""
        for i in range(1, 9):
            self.collector.addInput(DummyInput(1), "outValue", f"input{i}")
        
        changed = self.collector.eval()
        expected_value = 0b11111111  # All 8 bits set
        assert self.collector.state["outValue"] == (expected_value, 8)
        assert changed is True

    def test_collector_all_inputs_low(self):
        """Test collector when all inputs are low (0)."""
        for i in range(1, 9):
            self.collector.addInput(DummyInput(0), "outValue", f"input{i}")
        
        changed = self.collector.eval()
        assert self.collector.state["outValue"] == (0, 8)
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
    def test_collector_bit_patterns(self, pattern):
        """Test collector with various bit patterns."""
        collector = Collector1to8()
        
        # Connect inputs according to the bit pattern
        for i in range(8):
            bit_value = (pattern >> i) & 1
            collector.addInput(DummyInput(bit_value), "outValue", f"input{i+1}")
        
        changed = collector.eval()
        assert collector.state["outValue"] == (pattern, 8)
        assert changed is True

    def test_collector_mixed_connected_disconnected_inputs(self):
        """Test collector with some inputs connected and others disconnected."""
        # Connect only even-numbered inputs with value 1
        for i in range(2, 9, 2):  # inputs 2, 4, 6, 8
            self.collector.addInput(DummyInput(1), "outValue", f"input{i}")
        
        changed = self.collector.eval()
        expected_value = 0b10101010  # Bits 1, 3, 5, 7 set (0-indexed)
        assert self.collector.state["outValue"] == (expected_value, 8)
        assert changed is True

    def test_collector_state_change_detection(self):
        """Test that eval() correctly detects state changes."""
        # Initial evaluation with no inputs
        changed = self.collector.eval()
        assert changed is False  # No change from initial state
        
        # Add an input and evaluate
        self.collector.addInput(DummyInput(1), "outValue", "input1")
        changed = self.collector.eval()
        assert changed is True
        assert self.collector.state["outValue"] == (1, 8)
        
        # Evaluate again without changes
        changed = self.collector.eval()
        assert changed is False  # No change from previous state

    def test_collector_input_overwrite_behavior(self):
        """Test behavior when trying to overwrite existing input connections."""
        dummy1 = DummyInput(1)
        dummy2 = DummyInput(0)
        
        # Add first input
        success1 = self.collector.addInput(dummy1, "outValue", "input1")
        assert success1 is True
        
        # Try to overwrite the same input
        success2 = self.collector.addInput(dummy2, "outValue", "input1")
        assert success2 is False  # Should fail
        
        # Verify original input is still connected
        self.collector.eval()
        assert self.collector.state["outValue"] == (1, 8)

    def test_collector_invalid_input_keys(self):
        """Test collector behavior with invalid input keys."""
        dummy = DummyInput(1)
        
        # Try to add input with invalid key
        with pytest.raises(KeyError):
            self.collector.addInput(dummy, "outValue", "invalid_input")

